#!/usr/bin/env python3
"""
tsv.py — Build and incrementally maintain per-year TSV indexes of cvelistV5.

Output layout (under --out, defaulting to this directory):
    cve-YYYY.tsv      one TSV per year, sorted by cve id
    index.tsv         manifest: year\trows\tfile (the simplest index)
    cve.tsv.state.json  per-file mtimes so subsequent runs skip unchanged files

TSV columns (tab-separated):
    cve     full CVE id, e.g. CVE-2024-0001
    year    the year segment parsed from the CVE id
    no      the numeric segment parsed from the CVE id
    ghsa    GitHub Security Advisory id(s) in `references`, `;`-joined; empty if none
    score   the highest CVSS base score across all containers (CNA + ADP); empty if none
    desc    the English description from the CNA container (single-line); empty if none

For incremental updates between full rebuilds, re-run with `--rebuild`
against a freshly-cloned cvelistV5 — see .github/workflows/release.yml.

Usage:
    python3 tsv.py                 # incremental update against the source
    python3 tsv.py --rebuild       # ignore state, re-parse everything
    python3 tsv.py --src <dir>     # override cvelistV5 root directory
    python3 tsv.py --out <dir>     # override output directory
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _cve_index import (
    load_json_state,
    load_year_files,
    parse_record,
    save_json_state,
    save_year_files,
    write_manifest,
)

# This script lives at .x-cmd/tsv.py inside the repo; the data lives
# at the sibling data/ directory. DEFAULT_OUT points there so a bare
# `python3 tsv.py` writes to the right place.
DEFAULT_SRC = Path("/Users/l/.x-repo/github.com/CVEProject/cvelistV5/cves")
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "data"
DEFAULT_STATE = DEFAULT_OUT / "cve.tsv.state.json"


def iter_cve_files(src: Path):
    if not src.is_dir():
        raise FileNotFoundError(f"source dir not found: {src}")
    for path in sorted(src.rglob("CVE-*.json")):
        if path.is_file():
            yield path


def build(src: Path, out: Path, state: Path, rebuild: bool) -> tuple[int, int]:
    """Run the (incremental) build. Returns (rows_written, rows_updated)."""
    if rebuild:
        rows_by_cve, order, _ = {}, {}, {}
        prev_state: dict[str, float] = {}
    else:
        rows_by_cve, order, _ = load_year_files(out)
        prev_state = load_json_state(state, {})

    new_state: dict[str, float] = {}
    seen_paths: set[str] = set()
    written = 0
    updated = 0

    for path in iter_cve_files(src):
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        key = str(path)
        new_state[key] = mtime
        seen_paths.add(key)

        row = parse_record(path)
        if row is None:
            continue
        cve_id = row[0]
        new_cells = list(row)

        if prev_state.get(key) == mtime and cve_id in rows_by_cve:
            continue

        if cve_id in rows_by_cve and rows_by_cve[cve_id] != new_cells:
            updated += 1
        elif cve_id not in rows_by_cve:
            written += 1
            order[cve_id] = len(order)
        rows_by_cve[cve_id] = new_cells

    # Determine which years actually have rows after the rebuild — those
    # are the ones we'll write. We rewrite every year with rows so the
    # on-disk set always reflects the in-memory truth.
    years_with_rows = save_year_files(out, rows_by_cve, order)
    write_manifest(out, years_with_rows)

    pruned_state = {k: v for k, v in new_state.items() if k in seen_paths}
    save_json_state(state, pruned_state)
    return written, updated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args(argv)

    try:
        added, updated = build(args.src, args.out, args.state, args.rebuild)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    manifest = args.out / "index.tsv"
    total = 0
    years = 0
    if manifest.is_file():
        with manifest.open("r", encoding="utf-8") as fh:
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 2 and parts[0] != "year":
                    try:
                        total += int(parts[1])
                        years += 1
                    except ValueError:
                        pass
    print(f"tsv: +{added} new, ~{updated} updated, {total} rows across {years} years -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())