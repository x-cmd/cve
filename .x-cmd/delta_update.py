#!/usr/bin/env python3
"""
delta_update.py — incrementally update cve.tsv using cvelistV5's deltaLog.

How it works:
    1. Fetch the upstream `cves/deltaLog.json`. It's an append-only array
       of snapshots, each with a `fetchTime`, `new`, and `updated` arrays.
    2. Skip snapshots older than the last `fetchTime` we consumed (watermark).
    3. For every entry in the new snapshots, download the raw CVE JSON via
       https://raw.githubusercontent.com/CVEProject/cvelistV5/main/<path>
       and replace that row in cve.tsv.
    4. Advance the watermark and write the TSV atomically.

Networking:
    urllib.request honors HTTP_PROXY / HTTPS_PROXY environment variables, so
    running behind a local forwarder is just:

        HTTP_PROXY=http://localhost:2026 python3 delta_update.py

    Use `--no-proxy` to bypass proxy env vars (useful when GitHub is directly
    reachable from your network).

State files (next to cve.tsv):
    cve.tsv.watermark.json   {"fetchTime": "...Z"}  - last consumed snapshot

Usage:
    python3 delta_update.py                           # online, default proxy env
    python3 delta_update.py --no-proxy                # bypass HTTP_PROXY env
    python3 delta_update.py --proxy http://host:port  # explicit proxy URL
    python3 delta_update.py --from-local path/to/deltaLog.json
    python3 delta_update.py --since 2026-07-01T00:00:00Z
    python3 delta_update.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

from _cve_index import (
    load_json_state,
    load_year_files,
    parse_record,
    save_json_state,
    save_year_files,
    write_manifest,
)

# This script lives at .x-cmd/delta_update.py inside the repo; data
# lives at the sibling data/ directory.
DEFAULT_TSV = Path(__file__).resolve().parent.parent / "data" / "cve.tsv"
DEFAULT_WATERMARK = Path(__file__).resolve().parent.parent / "data" / "cve.tsv.watermark.json"
DEFAULT_DELTA_LOG_URL = (
    "https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/deltaLog.json"
)
DEFAULT_CVE_RAW_BASE = "https://raw.githubusercontent.com/CVEProject/cvelistV5/main"

# Network timeouts (seconds). Generous on connect because the proxy hop adds latency.
CONNECT_TIMEOUT = 15.0
READ_TIMEOUT = 60.0


# ---------- proxy handling ---------------------------------------------------


def _proxy_handler(proxy_url: str | None) -> urllib.request.ProxyHandler:
    """Build a ProxyHandler. proxy_url=None uses env vars; "" disables proxy."""
    if proxy_url == "":
        # Explicit bypass: empty dict disables any proxy use.
        return urllib.request.ProxyHandler({})
    if proxy_url:
        # Apply the proxy to both http and https schemes.
        return urllib.request.ProxyHandler({
            "http": proxy_url,
            "https": proxy_url,
        })
    # Default: trust HTTP_PROXY / HTTPS_PROXY env vars.
    return urllib.request.ProxyHandler()


# ---------- http helpers -----------------------------------------------------


class FetchError(RuntimeError):
    pass


def fetch_bytes(url: str, proxy_url: str | None) -> bytes:
    handler = _proxy_handler(proxy_url)
    opener = urllib.request.build_opener(handler)
    req = urllib.request.Request(url, headers={
        "User-Agent": "cve-index-delta/1.0 (+https://github.com/x-cmd/cve)",
        "Accept": "application/json,*/*;q=0.1",
    })
    try:
        with opener.open(req, timeout=CONNECT_TIMEOUT) as resp:
            return resp.read()
    except (urllib.error.URLError, socket.timeout, TimeoutError) as exc:
        raise FetchError(f"GET {url}: {exc}") from exc


# ---------- delta log processing --------------------------------------------


def load_delta_log(source: str | Path, proxy_url: str | None) -> list[dict]:
    """Load deltaLog.json from a URL or a local path. Returns the snapshot list."""
    if isinstance(source, Path) or (isinstance(source, str) and not source.startswith("http")):
        path = Path(source)
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            raise FetchError(f"reading {path}: {exc}") from exc
    else:
        payload = fetch_bytes(source, proxy_url)
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise FetchError(f"decoding deltaLog from {source}: {exc}") from exc

    if not isinstance(data, list):
        raise FetchError(f"deltaLog at {source} is not a JSON array")
    return data


def _iter_changed(snapshot: dict) -> Iterable[dict]:
    """Yield change entries from a single snapshot."""
    for key in ("new", "updated"):
        for entry in snapshot.get(key, []) or []:
            if isinstance(entry, dict):
                yield entry


def _github_link_to_raw_path(github_link: str) -> str:
    """Convert a raw github URL to a path inside cvelistV5/."""
    marker = "/cvelistV5/"
    idx = github_link.find(marker)
    if idx < 0:
        raise FetchError(f"unexpected github link: {github_link}")
    return github_link[idx + len(marker):]


# ---------- main apply -------------------------------------------------------


def apply_changes(
    rows_by_cve: dict[str, list[str]],
    order: dict[str, int],
    snapshots: list[dict],
    since: str,
    proxy_url: str | None,
    *,
    dry_run: bool = False,
    raw_base: str | None = None,
    local_root: Path | None = None,
) -> tuple[int, int, str | None, set[str]]:
    """Apply every snapshot with fetchTime > `since`.

    Returns (added, updated, new_watermark, years_touched). `years_touched`
    is the set of year strings whose row content changed; only those year
    files (plus the manifest) need rewriting on disk.
    """
    new_watermark = since
    added = 0
    updated = 0
    years_touched: set[str] = set()

    eligible = [s for s in snapshots if s.get("fetchTime", "") > since]
    eligible.sort(key=lambda s: s.get("fetchTime", ""))

    base = raw_base or DEFAULT_CVE_RAW_BASE

    for snap in eligible:
        snap_time = snap.get("fetchTime", "")
        for entry in _iter_changed(snap):
            cve_id = entry.get("cveId")
            link = entry.get("githubLink")
            if not cve_id or not link:
                continue
            try:
                rel_path = _github_link_to_raw_path(link)
            except FetchError as exc:
                print(f"warn: skip {cve_id}: {exc}", file=sys.stderr)
                continue

            if dry_run:
                marker = "NEW" if cve_id not in rows_by_cve else "UPD"
                print(f"{marker}\t{cve_id}\t{rel_path}")
                if cve_id not in rows_by_cve:
                    added += 1
                else:
                    updated += 1
                years_touched.add(rel_path.split("/")[1] if "/" in rel_path else "")
                new_watermark = snap_time
                continue

            try:
                if local_root is not None:
                    local_path = local_root / rel_path
                    try:
                        with local_path.open("r", encoding="utf-8") as fh:
                            record = json.load(fh)
                    except (OSError, json.JSONDecodeError) as exc:
                        print(f"warn: {cve_id}: local read {local_path}: {exc}", file=sys.stderr)
                        continue
                else:
                    url = f"{base}/{rel_path}"
                    try:
                        payload = fetch_bytes(url, proxy_url)
                    except FetchError as exc:
                        print(f"warn: {cve_id}: {exc}", file=sys.stderr)
                        continue
                    try:
                        record = json.loads(payload)
                    except json.JSONDecodeError as exc:
                        print(f"warn: {cve_id}: bad JSON: {exc}", file=sys.stderr)
                        continue
            except Exception as exc:  # pragma: no cover - defensive
                print(f"warn: {cve_id}: {exc}", file=sys.stderr)
                continue

            row = parse_record(record, is_path=False)
            if row is None:
                # REJECTED or malformed → drop any existing row
                if cve_id in rows_by_cve:
                    old_year = rows_by_cve[cve_id][1] if rows_by_cve[cve_id] else ""
                    del rows_by_cve[cve_id]
                    order.pop(cve_id, None)
                    if old_year:
                        years_touched.add(old_year)
                continue

            new_cells = list(row)
            year = new_cells[1]
            if cve_id in rows_by_cve:
                if rows_by_cve[cve_id] != new_cells:
                    rows_by_cve[cve_id] = new_cells
                    updated += 1
                    years_touched.add(year)
            else:
                rows_by_cve[cve_id] = new_cells
                order[cve_id] = len(order)
                added += 1
                years_touched.add(year)
            new_watermark = snap_time

    return added, updated, new_watermark, years_touched


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--tsv", type=Path, default=DEFAULT_TSV,
                        help="output directory for cve-YYYY.tsv and index.tsv")
    parser.add_argument("--watermark", type=Path, default=DEFAULT_WATERMARK)
    parser.add_argument("--delta-log", default=DEFAULT_DELTA_LOG_URL,
                        help="URL or local path of cves/deltaLog.json")
    parser.add_argument("--from-local", dest="from_local", default=None,
                        help="shortcut: load deltaLog from this local file")
    parser.add_argument("--local-root", type=Path, default=None,
                        help="read each CVE JSON from this local cvelistV5 root "
                             "instead of fetching over the network (for testing)")
    parser.add_argument("--proxy", default=None,
                        help="explicit proxy URL, e.g. http://localhost:2026; "
                             "use '' to bypass HTTP_PROXY env vars entirely")
    parser.add_argument("--no-proxy", dest="no_proxy", action="store_true",
                        help="bypass HTTP_PROXY / HTTPS_PROXY env vars")
    parser.add_argument("--since", default=None,
                        help="ISO timestamp; override stored watermark")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the changes that would be applied")
    args = parser.parse_args(argv)

    if args.from_local:
        delta_source: str | Path = Path(args.from_local)
    else:
        delta_source = args.delta_log

    proxy_url: str | None
    if args.no_proxy:
        proxy_url = ""
    elif args.proxy is not None:
        proxy_url = args.proxy
    else:
        # Honor env vars by passing None through to urllib.
        proxy_url = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")

    try:
        snapshots = load_delta_log(delta_source, proxy_url)
    except FetchError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    # Load existing per-year files. The --tsv arg is now a directory root.
    rows_by_cve, order, year_files = load_year_files(args.tsv)

    state = {} if args.since else load_json_state(args.watermark, {})
    since = args.since or state.get("fetchTime", "")

    added, updated, new_watermark, years_touched = apply_changes(
        rows_by_cve, order, snapshots, since, proxy_url, dry_run=args.dry_run,
        local_root=args.local_root,
    )

    if args.dry_run:
        print(f"dry-run: {added} new, {updated} updated across {len(years_touched)} years, "
              f"would advance watermark to {new_watermark}")
        return 0

    if new_watermark and new_watermark > since:
        save_json_state(args.watermark, {"fetchTime": new_watermark})
        # Only rewrite years whose content actually changed — older years stay
        # frozen on disk (cache for ~1 year as per design).
        save_year_files(args.tsv, rows_by_cve, order, only_years=years_touched or None)
        # Always rebuild the manifest: row counts may shift if rows were dropped.
        years_with_rows = set()
        for cid, cells in rows_by_cve.items():
            if len(cells) > 1 and cells[1]:
                years_with_rows.add(cells[1])
        # include years whose files exist on disk (so manifest doesn't shrink them)
        years_with_rows |= set(year_files)
        write_manifest(args.tsv, years_with_rows)

    total = len(rows_by_cve)
    print(f"delta: +{added} new, ~{updated} updated across {len(years_touched)} years, "
          f"{total} total, watermark={new_watermark or since}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())