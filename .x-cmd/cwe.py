#!/usr/bin/env python3
"""
cwe.py — fetch the MITRE CWE catalog and write it as a TSV.

Source: https://cwe.mitre.org/data/csv/2000.csv.zip
Output: data/cwe.tsv (tab-separated, all MITRE columns preserved)

We preserve every column from the upstream CSV — mitigations, related
weaknesses, observed examples, applicable platforms, common
consequences, detection methods, modes of introduction, etc. The
x-cwe module and any other consumer can map these directly back to
MITRE's column names. The raw 2000.csv.zip is ~644 KB and the
uncompressed csv is ~3 MB — small enough that we don't need to thin
the columns. (The on-the-wire release asset will be xz-compressed
to roughly 100-200 KB.)

Rows are emitted in ascending numeric cwe-id order (CWE-1, CWE-2,
... CWE-1434). MITRE skips a few early ids (CWE-1..4 are deprecated
placeholders) so the sequence is sparse; we just sort numerically.
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

# MITRE's CSV column names (2000.csv). We preserve these verbatim so
# downstream consumers can use them as-is.
MITRE_FIELDS = [
    "CWE-ID", "Name", "Weakness Abstraction", "Status", "Description",
    "Extended Description", "Related Weaknesses", "Weakness Ordinalities",
    "Applicable Platforms", "Background Details", "Alternate Terms",
    "Modes Of Introduction", "Exploitation Factors",
    "Likelihood of Exploit", "Common Consequences", "Detection Methods",
    "Potential Mitigations", "Observed Examples", "Functional Areas",
    "Affected Resources", "Taxonomy Mappings", "Related Attack Patterns",
    "Notes",
]
# Renamed tab header for the TSV — replaces spaces with underscores so
# column names work as awk / pandas fields.
TSV_FIELDS = [f.replace(" ", "_") for f in MITRE_FIELDS]


def fetch_zip(url: str, timeout: float = 30.0) -> bytes:
    """Fetch the MITRE CWE catalog zip and return its bytes."""
    req = urllib.request.Request(url, headers={"User-Agent": "x-cmd/cve-data"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_csv(zbytes: bytes) -> list[dict[str, str]]:
    """Unzip + parse the MITRE 2000.csv. Return list of dicts keyed by
    the MITRE column names (preserving all fields).
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
        # Drop rows without a CWE id (last "None" row in some MITRE dumps).
        cid = (row.get("CWE-ID") or "").strip()
        if not cid:
            continue
        # Re-emit every column we know about, preserving order. Missing
        # columns become empty strings.
        record = {}
        for mitre_field, tsv_field in zip(MITRE_FIELDS, TSV_FIELDS):
            value = (row.get(mitre_field) or "").strip()
            # Collapse internal whitespace so each row is one TSV line.
            value = " ".join(value.split())
            record[tsv_field] = value
        out.append(record)
    return out


def cwe_sort_key(row: dict[str, str]) -> tuple[int, str]:
    """Sort by CWE-id as an integer when possible (CWE-79 < CWE-100),
    fall back to lexicographic for non-numeric ids.
    """
    raw = row["CWE-ID"]
    try:
        return (0, f"{int(raw):09d}")
    except ValueError:
        return (1, raw)


def write_tsv(rows: list[dict[str, str]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("\t".join(TSV_FIELDS) + "\n")
        for row in rows:
            fh.write("\t".join(row[f] for f in TSV_FIELDS) + "\n")


# Slim view of the catalog — just id + name — for the README's
# quick-reference table and for cwe_report.py to join against.
# We expose this as a separate function so cwe_report.py can call it
# without re-parsing the upstream zip.
def write_cwe_slim(rows: list[dict[str, str]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("CWE-ID\tName\n")
        for row in rows:
            fh.write(f"{row['CWE-ID']}\t{row['Name']}\n")


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

    # Also emit a slim 2-col id+name catalog for the report join.
    slim_out = DEFAULT_OUT / "cwe.slim.tsv"
    write_cwe_slim(rows, slim_out)

    print(f"wrote {out} ({len(rows)} CWE rows, full 21 cols)", file=sys.stderr)
    print(f"wrote {slim_out} ({len(rows)} CWE rows, slim 2 cols)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))