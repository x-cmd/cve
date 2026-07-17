"""
_cve_index.py — shared helpers used by both tsv.py (full rebuild) and
delta_update.py (incremental, deltaLog-driven).

It exposes:
    parse_record(path_or_payload, *, is_path=True) -> tuple | None
    load_tsv(path)  -> (rows_by_cve, order)
    save_tsv(path, rows_by_cve, order)
    load_year_files(root) -> (rows_by_cve, order, year_files)
    save_year_files(root, rows_by_cve, order, *, only_years=None) -> set[str]
    write_manifest(root, year_files) -> Path
    load_json_state / save_json_state

The on-disk layout is per-year:
    <root>/cve-YYYY.tsv      one TSV per year, sorted by cve id
    <root>/index.tsv         manifest: year\trows\tfile (the simplest index)

Everything here is dependency-free (Python 3.8+ stdlib only).
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

CVE_ID_RE = re.compile(r"^CVE-(\d{4})-(\d{4,7})$")
GHSA_RE = re.compile(r"GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}", re.IGNORECASE)


# ---------- record parsing ---------------------------------------------------


def parse_record(source: Any, *, is_path: bool = True) -> tuple | None:
    """Parse a CVE record from a Path or an already-loaded dict.

    Returns a 9-tuple
        (cve, year, no, vp, ghsa, score, patched, cwe, desc)
    where:
        cve      — full CVE id, e.g. "CVE-2024-0001"
        year     — 4-digit year segment
        no       — numeric segment
        vp       — "<vendor>/<product>;<vendor>/<product>;..." — all
                   affected vendor/product pairs joined with ";". No
                   limit (a vuln in a popular library can touch dozens of
                   products). Missing vendor/product yields empty string.
        ghsa     — GHSA id(s) found in references, ";" joined
        score    — highest CVSS base score across v4 / v3.1 / v3.0 / v2
        patched  — "1" if containers.cna.solutions[] is non-empty, else "0"
        cwe      — CWE numbers (prefix-stripped) joined with ";". No limit.
        desc     — English description, single-line

    Returns None when the record is REJECTED, malformed, or not a CVE JSON.
    """
    if is_path:
        path = Path(source)
        year_no = CVE_ID_RE.match(path.stem)
        if year_no is None:
            return None
        year, number = year_no.group(1), year_no.group(2)
        try:
            with path.open("r", encoding="utf-8") as fh:
                record = json.load(fh)
        except (OSError, json.JSONDecodeError):
            return None
        if not isinstance(record, dict):
            return None
    else:
        record = source
        if not isinstance(record, dict):
            return None
        meta = record.get("cveMetadata", {})
        cve_id = meta.get("cveId", "")
        m = CVE_ID_RE.match(cve_id)
        if m is None:
            return None
        year, number = m.group(1), m.group(2)

    if record.get("cveMetadata", {}).get("state") == "REJECTED":
        return None

    cve_id = record.get("cveMetadata", {}).get("cveId")
    if not cve_id:
        return None

    vp = _extract_vp(record)
    desc = _extract_description(record)
    score = _extract_score(record)
    ghsa = _extract_ghsa(record)
    patched = _extract_patched(record)
    cwe = _extract_cwe(record)
    return (cve_id, year, number, vp, ghsa, score, patched, cwe, desc)


def _extract_description(record: dict) -> str:
    """Return the full English description verbatim.

    We collapse internal whitespace (newlines / tabs) to single spaces
    so each row fits on a single TSV line, but otherwise preserve the
    entire upstream text — including the slab dumps, call traces, and
    hex addresses that Linux CNA routinely pastes in. Truncating or
    summarising the description at the producer level would silently
    drop information; consumers that want a shorter view should slice
    the row at display time, not at write time.
    """
    cna = record.get("containers", {}).get("cna", {})
    for entry in cna.get("descriptions", []) or []:
        if entry.get("lang") == "en":
            value = entry.get("value", "") or ""
            return " ".join(value.split())
    return ""


def _extract_score(record: dict) -> str:
    best: float | None = None

    def consider(obj: dict) -> None:
        nonlocal best
        for key in ("cvssV4_0", "cvssV3_1", "cvssV3_0", "cvssV2_0"):
            node = obj.get(key)
            if not isinstance(node, dict):
                continue
            raw = node.get("baseScore")
            if raw is None:
                continue
            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue
            if best is None or value > best:
                best = value

    cna = record.get("containers", {}).get("cna", {})
    for metric in cna.get("metrics", []) or []:
        if isinstance(metric, dict):
            consider(metric)

    for adp in record.get("containers", {}).get("adp", []) or []:
        if not isinstance(adp, dict):
            continue
        for metric in adp.get("metrics", []) or []:
            if isinstance(metric, dict):
                consider(metric)

    return "" if best is None else f"{best:g}"


def _extract_ghsa(record: dict) -> str:
    seen: list[str] = []
    seen_set: set[str] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            url = node.get("url")
            if isinstance(url, str):
                for match in GHSA_RE.findall(url):
                    upper = match.upper()
                    if upper not in seen_set:
                        seen_set.add(upper)
                        seen.append(upper)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(record.get("containers", {}))
    return ";".join(seen)


def _extract_vp(record: dict) -> str:
    """Extract <vendor>/<product>;<vendor>/<product>;... for every affected
    entry in containers.cna.affected[]. No limit — a single library vuln
    can affect dozens of products, and the user wants them all.

    Order matches the source JSON. Empty cells (missing vendor or product)
    are kept as empty strings so the field width is predictable.
    """
    pairs: list[str] = []
    for aff in record.get("containers", {}).get("cna", {}).get("affected", []) or []:
        vendor = aff.get("vendor") or ""
        product = aff.get("product") or ""
        # Always emit `<vendor>/<product>`, even if both are empty —
        # preserves the count of affected entries. `///` means "no data".
        pairs.append(f"{vendor}/{product}")
    return ";".join(pairs)


def _extract_patched(record: dict) -> str:
    """Return "1" if the CNA published a remediation (solutions[] non-empty),
    else "0". A non-empty solution is the strongest signal we have for
    "patch available" without parsing every reference URL.
    """
    cna = record.get("containers", {}).get("cna", {})
    return "1" if cna.get("solutions") else "0"


_CWE_PREFIX_RE = re.compile(r"^CWE-", re.IGNORECASE)

def _extract_cwe(record: dict) -> str:
    """Extract CWE numbers (prefix-stripped) joined with ";". No limit.

    Source: containers.cna.problemTypes[].descriptions[].cweId. We strip
    the "CWE-" prefix because callers can always re-add it; storing just
    the number keeps the field tight.
    """
    ids: list[str] = []
    seen: set[str] = set()
    for pt in record.get("containers", {}).get("cna", {}).get("problemTypes", []) or []:
        for desc in pt.get("descriptions", []) or []:
            cid = desc.get("cweId")
            if not cid:
                continue
            n = _CWE_PREFIX_RE.sub("", str(cid))
            if n and n not in seen:
                seen.add(n)
                ids.append(n)
    return ";".join(ids)


# ---------- tsv i/o ----------------------------------------------------------


_CVE_COLUMNS = 9


def load_tsv(path: Path) -> tuple[dict[str, list[str]], dict[str, int]]:
    """Load existing TSV into (rows_by_cve, order). Missing file -> empty."""
    rows: dict[str, list[str]] = {}
    order: dict[str, int] = {}
    if not path.is_file():
        return rows, order
    with path.open("r", encoding="utf-8", newline="") as fh:
        for idx, line in enumerate(fh):
            parts = line.rstrip("\n").split("\t")
            if len(parts) < _CVE_COLUMNS:
                parts = parts + [""] * (_CVE_COLUMNS - len(parts))
            cve_id = parts[0]
            if not cve_id:
                continue
            rows[cve_id] = parts[:_CVE_COLUMNS]
            order[cve_id] = idx
    return rows, order


def save_tsv(path: Path, rows_by_cve: dict[str, list[str]], order: dict[str, int]) -> None:
    """Atomically write the TSV with rows in descending cve-id order
    (newest first), so consumers reading top-to-bottom see the latest
    CVEs first without needing a reverse pass."""
    known = set(order)
    next_idx = (max(order.values()) + 1) if order else 0
    for cid in sorted(rows_by_cve):
        if cid not in known:
            order[cid] = next_idx
            next_idx += 1

    sorted_ids = sorted(rows_by_cve, key=lambda c: order[c], reverse=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            for cid in sorted_ids:
                fh.write("\t".join(rows_by_cve[cid]) + "\n")
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


# ---------- per-year i/o -----------------------------------------------------


def year_file_path(root: Path, year: str) -> Path:
    return root / f"cve-{year}.tsv"


def manifest_path(root: Path) -> Path:
    return root / "index.tsv"


def load_year_files(root: Path) -> tuple[dict[str, list[str]], dict[str, int], dict[str, Path]]:
    """Load every existing cve-YYYY.tsv under `root` into memory.

    Returns (rows_by_cve, order, year_files) where `year_files` maps the
    year string -> on-disk path that produced its rows. Missing dir -> empty.
    """
    rows: dict[str, list[str]] = {}
    order: dict[str, int] = {}
    year_files: dict[str, Path] = {}

    if not root.is_dir():
        return rows, order, year_files

    for path in sorted(root.glob("cve-*.tsv")):
        m = re.match(r"cve-(\d{4})\.tsv$", path.name)
        if not m:
            continue
        year = m.group(1)
        year_files[year] = path
        try:
            with path.open("r", encoding="utf-8", newline="") as fh:
                for line in fh:
                    parts = line.rstrip("\n").split("\t")
                    if len(parts) < _CVE_COLUMNS:
                        parts = parts + [""] * (_CVE_COLUMNS - len(parts))
                    cve_id = parts[0]
                    if not cve_id:
                        continue
                    # trust the year segment from the file name over the row
                    parts[1] = year
                    rows[cve_id] = parts[:_CVE_COLUMNS]
                    order[cve_id] = len(order)
        except OSError as exc:
            print(f"warn: cannot read {path}: {exc}", file=sys.stderr)

    return rows, order, year_files


def save_year_files(
    root: Path,
    rows_by_cve: dict[str, list[str]],
    order: dict[str, int],
    *,
    only_years: set[str] | None = None,
) -> set[str]:
    """Write per-year TSV files atomically.

    If `only_years` is given, only those years are (re)written; older years
    remain on disk untouched. Always returns the set of years that have at
    least one row, so the caller can refresh the manifest.
    """
    root.mkdir(parents=True, exist_ok=True)

    # Bucket rows by year.
    buckets: dict[str, list[str]] = {}
    for cve_id, cells in rows_by_cve.items():
        year = cells[1] if len(cells) > 1 else ""
        if not year:
            continue
        buckets.setdefault(year, []).append("\t".join(cells))

    years_with_rows = set(buckets)
    target_years = set(only_years) if only_years is not None else years_with_rows

    # Sort each bucket by cve id descending — newest id first.
    # Consumers (x cve ls / fz) want the latest CVEs at the top of
    # the stream, so we store them in that order on disk and avoid
    # an extra `tac` pass at read time.
    for year in target_years & years_with_rows:
        buckets[year].sort(reverse=True)

    for year in target_years:
        out = year_file_path(root, year)
        fd, tmp_name = tempfile.mkstemp(prefix=out.name + ".", dir=str(root))
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
                for line in buckets.get(year, []):
                    fh.write(line + "\n")
            os.replace(tmp_name, out)
        except Exception:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise

    return years_with_rows


def write_manifest(root: Path, years_with_rows: set[str]) -> Path:
    """Emit index.tsv sorted by year ascending."""
    manifest = manifest_path(root)
    fd, tmp_name = tempfile.mkstemp(prefix=manifest.name + ".", dir=str(root))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as out:
            out.write("year\trows\tfile\n")
            for year in sorted(years_with_rows):
                year_path = year_file_path(root, year)
                try:
                    with year_path.open("r", encoding="utf-8") as inp:
                        rows = sum(1 for _ in inp)
                except OSError:
                    rows = 0
                out.write(f"{year}\t{rows}\t{year_path.name}\n")
        os.replace(tmp_name, manifest)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    return manifest


# ---------- json state -------------------------------------------------------


def load_json_state(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return default


def save_json_state(path: Path, data: Any) -> None:
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, sort_keys=True, indent=2)
            fh.write("\n")
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise