#!/usr/bin/env python3
"""
cwe_report.py — derive cwe.report.tsv from data/cwe.tsv + data/cve-*.tsv.

For every CWE in the catalog, compute:
    cwe_id, name, cve_count, scored_count, avg_score, max_score

Where:
    cve_count   = number of cve-*.tsv rows whose `cwe` column contains
                  this CWE id (the column may have multiple ids; we
                  match on substring).
    scored_count= of those CVEs, how many have a non-empty score.
    avg_score   = mean score across the scored ones.
    max_score   = highest score seen.

Output: data/cwe.report.tsv (tab-separated, sorted by cve_count desc).

We deliberately do NOT publish a copy of MITRE's 2000.csv — cve repo
only ships derived aggregates. Users wanting the full CWE catalog
hit MITRE directly via `x cwe` (which has its own download path).
"""

from __future__ import annotations

import sys
from pathlib import Path

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data"

# TSV column positions in cve-YYYY.tsv (matches _cve_index.py output):
#   $1 cve  $2 year  $3 no  $4 vp  $5 ghsa  $6 score  $7 patched  $8 cwe  $9 desc
COL_CWE = 7   # 0-based → $8
COL_SCORE = 5  # 0-based → $6


def collect_cve_scores_by_cwe(data_dir: Path) -> dict[str, list[float]]:
    """Walk data/cve-*.tsv and bucket scored CVEs by every CWE id they
    reference. A row with `cwe=787;119` contributes to both 787 and
    119.
    """
    scores: dict[str, list[float]] = {}

    for fp in data_dir.glob("cve-*.tsv"):
        try:
            with fp.open("r", encoding="utf-8", newline="") as fh:
                for line in fh:
                    cols = line.rstrip("\n").split("\t")
                    if len(cols) <= max(COL_CWE, COL_SCORE):
                        continue
                    cwe_field = cols[COL_CWE]
                    if not cwe_field:
                        continue
                    score_str = cols[COL_SCORE]
                    if not score_str:
                        continue
                    try:
                        score = float(score_str)
                    except ValueError:
                        continue
                    # CWE field is ";"-joined numbers (prefix stripped).
                    for cid in cwe_field.split(";"):
                        cid = cid.strip()
                        if not cid:
                            continue
                        scores.setdefault(cid, []).append(score)
        except OSError as exc:
            print(f"warn: cannot read {fp}: {exc}", file=sys.stderr)
            continue

    return scores


def load_cwe_catalog(catalog_tsv: Path) -> list[tuple[str, str]]:
    """Read data/cwe.slim.tsv (id, name only).

    The slim catalog is what cwe.py emits for joining — full 21-column
    data lives in data/cwe.tsv (which we publish as a release asset
    because it's small enough to mirror MITRE's catalog).
    """
    catalog: list[tuple[str, str]] = []
    if not catalog_tsv.is_file():
        return catalog
    with catalog_tsv.open("r", encoding="utf-8", newline="") as fh:
        next(fh, None)   # skip header
        for line in fh:
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 2:
                continue
            catalog.append((cols[0].strip(), cols[1].strip()))
    return catalog


def write_report(out: Path, rows: list[tuple[str, str, int, float, float]]) -> None:
    """rows: list of (cwe_id, name, cve_count, avg_score, max_score)."""
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("cwe_id\tname\tcve_count\tavg_score\tmax_score\n")
        for cid, name, count, avg, mx in rows:
            avg_str = f"{avg:.2f}" if count else "—"
            mx_str = f"{mx:.1f}" if count else "—"
            fh.write(f"{cid}\t{name}\t{count}\t{avg_str}\t{mx_str}\n")


def main(argv: list[str]) -> int:
    data_dir = Path(argv[1]) if len(argv) > 1 else DEFAULT_DATA
    if not data_dir.is_dir():
        print(f"error: data directory not found: {data_dir}", file=sys.stderr)
        return 1

    catalog = load_cwe_catalog(data_dir / "cwe.slim.tsv")
    if not catalog:
        print("warn: data/cwe.slim.tsv missing — run .x-cmd/cwe.py first",
              file=sys.stderr)

    scores_by_cwe = collect_cve_scores_by_cwe(data_dir)

    rows: list[tuple[str, str, int, float, float]] = []
    for cid, name in catalog:
        s = scores_by_cwe.get(cid, [])
        if s:
            count = len(s)
            avg = sum(s) / count
            mx = max(s)
        else:
            count, avg, mx = 0, 0.0, 0.0
        rows.append((cid, name, count, avg, mx))

    # Sort: most-referenced CWEs first, then by max score desc, then
    # by cwe_id ascending for stability.
    rows.sort(key=lambda r: (-r[2], -r[4], r[0]))

    write_report(data_dir / "cwe.report.tsv", rows)

    print(f"wrote {data_dir / 'cwe.report.tsv'} ({len(rows)} CWE rows)",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))