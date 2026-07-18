#!/usr/bin/env python3
"""
cwe_report.py — derive cwe.report.tsv + cwe.report.md from
data/cwe.slim.tsv + data/cve-*.tsv.

For every CWE in the catalog, compute:
    cwe_id, name, cve_count, scored_count, avg_score, max_score

Where:
    cve_count   = number of cve-*.tsv rows whose `cwe` column contains
                  this CWE id (the column may have multiple ids; we
                  match on substring).
    scored_count= of those CVEs, how many have a non-empty score.
    avg_score   = mean score across the scored ones.
    max_score   = highest score seen.

Outputs (under data/):
    cwe.report.tsv   — machine-readable, sorted by cve_count desc
    cwe.report.md    — markdown with three top-10 tables:
                         1. most CVEs (all years)
                         2. highest avg CVSS score (all years)
                         3. highest avg CVSS score (since SINCE_YEAR)
                       ready to be inlined into the README

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
COL_YEAR = 1   # 0-based → $2
COL_CWE = 7   # 0-based → $8
COL_SCORE = 5  # 0-based → $6

# Cutoff for "by avg score" ranking. Below this, a single outlier score
# can dominate the mean and the ranking is noise. 10 CVEs is the floor
# we use elsewhere for similar cutoffs (see report.py totals, etc.).
MIN_CVE_FOR_SCORE_RANK = 10
TOP_N = 10

# Cutoff for the "since YYYY" table. CWEs that show up only in older
# CVEs and have dropped off the radar stay out of the recent table —
# useful because it surfaces what attackers actually exploit TODAY
# rather than what's accumulated historically. 2025 keeps the table
# focused on the last ~18 months of activity as of writing.
SINCE_YEAR = 2025


def collect_cve_scores_by_cwe(
    data_dir: Path,
    *,
    min_year: int | None = None,
) -> dict[str, list[float]]:
    """Walk data/cve-*.tsv and bucket scored CVEs by every CWE id they
    reference. A row with `cwe=787;119` contributes to both 787 and
    119.

    `min_year` (optional) drops rows whose `year` column parses below
    the cutoff — used to build the "since YYYY" view alongside the
    all-years view.
    """
    scores: dict[str, list[float]] = {}

    for fp in data_dir.glob("cve-*.tsv"):
        try:
            with fp.open("r", encoding="utf-8", newline="") as fh:
                for line in fh:
                    cols = line.rstrip("\n").split("\t")
                    if len(cols) <= max(COL_CWE, COL_SCORE, COL_YEAR):
                        continue
                    if min_year is not None:
                        try:
                            year = int(cols[COL_YEAR])
                        except ValueError:
                            continue
                        if year < min_year:
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


def aggregate(
    catalog: list[tuple[str, str]],
    scores_by_cwe: dict[str, list[float]],
) -> list[tuple[str, str, int, float, float]]:
    """Turn per-CWE score lists into (cwe_id, name, count, avg, max) rows."""
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
    return rows


def write_report(out: Path, rows: list[tuple[str, str, int, float, float]]) -> None:
    """rows: list of (cwe_id, name, cve_count, avg_score, max_score)."""
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("cwe_id\tname\tcve_count\tavg_score\tmax_score\n")
        for cid, name, count, avg, mx in rows:
            avg_str = f"{avg:.2f}" if count else "—"
            mx_str = f"{mx:.1f}" if count else "—"
            fh.write(f"{cid}\t{name}\t{count}\t{avg_str}\t{mx_str}\n")


def _emit_topn_table(fh, rows: list[tuple[str, str, int, float, float]]) -> None:
    """Emit the standard 6-column top-N table (Rank, CWE, Name, CVEs,
    Avg, Max). Caller chooses which slice of `rows` to pass in."""
    fh.write("| Rank | CWE | Name | CVEs | Avg score | Max |\n")
    fh.write("| ---: | :-: | :--- | ---: | ---:      | ---: |\n")
    for i, (cid, name, count, avg, mx) in enumerate(rows, 1):
        fh.write(f"| {i} | [{cid}](https://cwe.mitre.org/data/definitions/{cid}.html) "
                 f"| {name} | {count:,} | {avg:.2f} | {mx:.1f} |\n")


def write_report_md(out: Path,
                    rows: list[tuple[str, str, int, float, float]],
                    rows_since: list[tuple[str, str, int, float, float]]) -> None:
    """Write the markdown snippet the README inlines.

    Three top-10 tables:
      1. CWEs with the most CVEs (all years; already sorted by
         cve_count desc).
      2. CWEs with the highest average CVSS score, among those with at
         least MIN_CVE_FOR_SCORE_RANK CVEs (all years; avoid single-CWE
         outliers).
      3. Same as (2), but restricted to CVEs whose year >= SINCE_YEAR —
         surfaces what attackers are *currently* exploiting rather than
         what's accumulated historically.

    Output is a bare markdown document — no BEGIN/END markers — so the
    file is also readable on its own. release.yml wraps it with
    BEGIN/END when stitching into README.md.
    """
    out.parent.mkdir(parents=True, exist_ok=True)

    # Headline numbers used in the preamble.
    total_cve = sum(r[2] for r in rows)
    total_cwe = sum(1 for r in rows if r[2] > 0)
    since_cve = sum(r[2] for r in rows_since)
    since_cwe = sum(1 for r in rows_since if r[2] > 0)

    # By avg score (all years): filter to CWEs that have enough samples
    # to make the mean meaningful, then sort. Tiebreak on cve_count desc
    # so ties favor the better-attested CWE.
    by_score = sorted(
        (r for r in rows if r[2] >= MIN_CVE_FOR_SCORE_RANK),
        key=lambda r: (-r[3], -r[2], r[0]),
    )

    # By avg score (since SINCE_YEAR): same logic, smaller pool.
    by_score_since = sorted(
        (r for r in rows_since if r[2] >= MIN_CVE_FOR_SCORE_RANK),
        key=lambda r: (-r[3], -r[2], r[0]),
    )

    with out.open("w", encoding="utf-8") as fh:
        fh.write(f"_{total_cve:,} CVEs across {total_cwe:,} distinct CWEs; "
                 f"{since_cve:,} CVEs across {since_cwe:,} distinct CWEs "
                 f"since {SINCE_YEAR}._\n\n")

        fh.write(f"### Top {TOP_N} CWE by CVE count\n\n")
        fh.write("| Rank | CWE | Name | CVEs | Avg score |\n")
        fh.write("| ---: | :-: | :--- | ---: | ---:      |\n")
        for i, (cid, name, count, avg, _mx) in enumerate(rows[:TOP_N], 1):
            if count <= 0:
                continue
            fh.write(f"| {i} | [{cid}](https://cwe.mitre.org/data/definitions/{cid}.html) "
                     f"| {name} | {count:,} | {avg:.2f} |\n")

        fh.write(f"\n### Top {TOP_N} CWE by average CVSS score "
                 f"(min {MIN_CVE_FOR_SCORE_RANK} CVEs)\n\n")
        _emit_topn_table(fh, by_score[:TOP_N])

        fh.write(f"\n### Top {TOP_N} CWE by average CVSS score "
                 f"since {SINCE_YEAR} (min {MIN_CVE_FOR_SCORE_RANK} CVEs)\n\n")
        _emit_topn_table(fh, by_score_since[:TOP_N])


def main(argv: list[str]) -> int:
    data_dir = Path(argv[1]) if len(argv) > 1 else DEFAULT_DATA
    if not data_dir.is_dir():
        print(f"error: data directory not found: {data_dir}", file=sys.stderr)
        return 1

    catalog = load_cwe_catalog(data_dir / "cwe.slim.tsv")
    if not catalog:
        print("warn: data/cwe.slim.tsv missing — run .x-cmd/cwe.py first",
              file=sys.stderr)

    # All-years pool (drives the first two tables).
    scores_by_cwe = collect_cve_scores_by_cwe(data_dir)
    rows = aggregate(catalog, scores_by_cwe)

    # Since-SINCE_YEAR pool (drives the third table).
    scores_by_cwe_recent = collect_cve_scores_by_cwe(data_dir, min_year=SINCE_YEAR)
    rows_since = aggregate(catalog, scores_by_cwe_recent)

    # Sort: most-referenced CWEs first, then by max score desc, then
    # by cwe_id ascending for stability.
    rows.sort(key=lambda r: (-r[2], -r[4], r[0]))

    write_report(data_dir / "cwe.report.tsv", rows)
    write_report_md(data_dir / "cwe.report.md", rows, rows_since)

    print(f"wrote {data_dir / 'cwe.report.tsv'} ({len(rows)} CWE rows)",
          file=sys.stderr)
    print(f"wrote {data_dir / 'cwe.report.md'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))