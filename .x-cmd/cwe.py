#!/usr/bin/env python3
"""
cwe.py — build data/cwe.tsv from the MITRE CWE catalog.

Mirrors the structure of x-cwe/lib/la/stream: parse the first 5 fields
of the MITRE 2000.csv (ID, Name, Abstraction, Status, Description),
emit `cwe-id\tname\tabstraction\tstatus\tdesc` rows in **ascending
cwe-id-numeric order** (CWE-1, CWE-2, ..., CWE-1000, ...).

Source: https://cwe.mitre.org/data/csv/2000.csv.zip
Output: data/cwe.tsv

Stdlib-only. Run from the repo root after tsv.py / delta_update.py:

    python3 .x-cmd/cwe.py

The x-cwe module reads its own copy of 2000.csv at runtime; the
companion data/cwe.tsv here is what we publish in this repo so the
cve report table can reference CWE ids by name without fetching the
upstream catalog.
"""

from __future__ import annotations

import csv
import io
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

DEFAULT_OUT = Path(__file__).resolve().parent.parent / "data"
DEFAULT_URL = "https://cwe.mitre.org/data/csv/2000.csv.zip"

# The x-cwe consumer treats the first 5 fields as the canonical
# row layout. We mirror that here so `x cve fz` (which shows
# "CWE-NNNN") lines up with what x cwe info shows when the user
# jumps from one to the other.
FIELDS = ("id", "name", "abstraction", "status", "desc")
TRUNC_DESC = 240   # same as the cve desc cap, so columns line up


def fetch_zip(url: str, timeout: float = 30.0) -> bytes:
    """Fetch the MITRE CWE catalog zip and return its bytes."""
    req = urllib.request.Request(url, headers={"User-Agent": "x-cmd/cve-data"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_csv(zbytes: bytes) -> list[dict[str, str]]:
    """Unzip + parse the MITRE 2000.csv. Return list of dicts with the
    five canonical fields.
    """
    with zipfile.ZipFile(io.BytesIO(zbytes)) as zf:
        csv_name = next((n for n in zf.namelist() if n.endswith(".csv")), None)
        if csv_name is None:
            raise ValueError("no .csv inside the zip")
        with zf.open(csv_name) as fh:
            # MITRE CSV is RFC 4180 — quotes around every field, CRLF
            # line endings, embedded double-quotes escaped as "".
            text = io.TextIOWrapper(fh, encoding="utf-8", newline="").read()

    reader = csv.DictReader(io.StringIO(text))
    out: list[dict[str, str]] = []
    for row in reader:
        # Column names in 2000.csv are like "CWE-ID", "Name", etc.
        # Map to our canonical short names — fall back to whatever
        # case-insensitive match exists if MITRE renames a column.
        cid = (
            row.get("CWE-ID")
            or row.get("cwe-id")
            or row.get("ID")
            or row.get("Id")
            or ""
        ).strip()
        if not cid:
            continue
        name = (
            row.get("Name") or row.get("name") or ""
        ).strip()
        abst = (
            row.get("Weakness Abstraction")
            or row.get("Abstraction")
            or row.get("abstraction")
            or ""
        ).strip()
        status = (
            row.get("Status") or row.get("status") or ""
        ).strip()
        desc = (row.get("Description") or row.get("description") or "").strip()
        # Collapse whitespace and truncate to first sentence (mirror
        # the cve description handling) so the TSV stays single-line.
        desc = " ".join(desc.split())
        if len(desc) > TRUNC_DESC:
            desc = desc[:TRUNC_DESC]
        out.append({
            "id": cid,
            "name": name,
            "abstraction": abst,
            "status": status,
            "desc": desc,
        })
    return out


def cwe_sort_key(row: dict[str, str]) -> tuple[int, str]:
    """Sort by CWE-id as an integer when possible (CWE-79 < CWE-100),
    fall back to lexicographic for non-numeric ids.
    """
    raw = row["id"]
    try:
        return (0, f"{int(raw):09d}")
    except ValueError:
        return (1, raw)


def write_tsv(rows: list[dict[str, str]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("\t".join(FIELDS) + "\n")
        for row in rows:
            fh.write("\t".join(row[f] for f in FIELDS) + "\n")


def main(argv: list[str]) -> int:
    url = argv[1] if len(argv) > 1 else DEFAULT_URL
    out = DEFAULT_OUT / "cwe.tsv"

    print(f"fetching {url} ...", file=sys.stderr)
    try:
        zbytes = fetch_zip(url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"error: failed to fetch {url}: {exc}", file=sys.stderr)
        return 1

    rows = parse_csv(zbytes)
    rows.sort(key=cwe_sort_key)
    write_tsv(rows, out)

    print(f"wrote {out} ({len(rows)} CWE rows)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))