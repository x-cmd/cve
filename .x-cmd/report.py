#!/usr/bin/env python3
"""
report.py — build cve.report.tsv (year-by-year stats) and a markdown
table for the README.

Reads every data/cve-YYYY.tsv and computes:
    year, count, scored_count, avg_score, max_score

Writes:
    data/cve.report.tsv     — machine-readable
    data/cve.report.md      — markdown table (auto-included in README)

The README's "Stats" section is regenerated from data/cve.report.md on
every release, so the table in the README always reflects the latest
data.

Stdlib-only. Run from the repo root after delta_update / tsv.py:
    python3 .x-cmd/report.py
"""

from __future__ import annotations

import sys
from pathlib import Path

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data"

# CVE ID column is $1, score is $6. Same layout as produced by
# _cve_index.py: cve  year  no  vp  ghsa  score  patched  cwe  desc.
COL_SCORE = 5  # 0-based: 6th column = $6 in awk terms

CVE_ID_RE_PREFIX = "CVE-"


def collect_year_stats(data_dir: Path) -> list[tuple[str, int, int, float, float]]:
    """Walk data/cve-*.tsv and produce one row per year.

    Returns a list of (year, count, scored_count, avg_score, max_score)
    sorted by year descending.
    """
    rows: list[tuple[str, int, int, float, float]] = []

    for fp in sorted(data_dir.glob("cve-*.tsv"), reverse=True):
        year = fp.stem.removeprefix("cve-")
        if not year.isdigit() or len(year) != 4:
            continue

        count = 0
        scored_count = 0
        sum_score = 0.0
        max_score = 0.0

        try:
            with fp.open("r", encoding="utf-8", newline="") as fh:
                for line in fh:
                    cols = line.rstrip("\n").split("\t")
                    if len(cols) <= COL_SCORE:
                        continue
                    cve_id = cols[0]
                    if not cve_id.startswith(CVE_ID_RE_PREFIX):
                        continue
                    count += 1
                    score_str = cols[COL_SCORE]
                    if score_str:
                        try:
                            s = float(score_str)
                        except ValueError:
                            continue
                        scored_count += 1
                        sum_score += s
                        if s > max_score:
                            max_score = s
        except OSError as exc:
            print(f"warn: cannot read {fp}: {exc}", file=sys.stderr)
            continue

        avg = sum_score / scored_count if scored_count else 0.0
        rows.append((year, count, scored_count, avg, max_score))

    return rows


def write_report_tsv(rows: list[tuple[str, int, int, float, float]],
                     out: Path) -> None:
    """Write the machine-readable TSV: year\tcount\tscored\tavg\tmax."""
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("year\tcount\tscored\tavg_score\tmax_score\n")
        for year, count, scored, avg, mx in rows:
            fh.write(f"{year}\t{count}\t{scored}\t{avg:.2f}\t{mx:.1f}\n")


def write_report_md(rows: list[tuple[str, int, int, float, float]],
                    out: Path) -> None:
    """Write the markdown snippet the README inlines.

    The output is a bare markdown table — no BEGIN/END markers — so
    `cve.report.md` is also human-readable on its own. The README's
    inline step wraps this body with the BEGIN/END markers.
    """
    with out.open("w", encoding="utf-8") as fh:
        fh.write("| Year | CVEs | Scored | Avg score | Max score |\n")
        fh.write("| ---: | ---: | ---:   | ---:      | ---:      |\n")
        for year, count, scored, avg, mx in rows:
            avg_str = f"{avg:.2f}" if scored else "—"
            fh.write(f"| {year} | {count:,} | {scored:,} | {avg_str} | {mx:.1f} |\n")
        # Totals row — useful at-a-glance summary. Total avg is the
        # weighted average across all scored CVEs (each year weighted
        # by its own scored_count, not by total_count).
        total_count = sum(r[1] for r in rows)
        total_scored = sum(r[2] for r in rows)
        if total_scored:
            total_avg = sum(r[2] * r[3] for r in rows) / total_scored
        else:
            total_avg = 0.0
        overall_max = max((r[4] for r in rows), default=0.0)
        fh.write(
            f"| **Total** | **{total_count:,}** | **{total_scored:,}** | "
            f"**{total_avg:.2f}** | **{overall_max:.1f}** |\n"
        )


def main(argv: list[str]) -> int:
    data_dir = Path(argv[1]) if len(argv) > 1 else DEFAULT_DATA
    if not data_dir.is_dir():
        print(f"error: data directory not found: {data_dir}", file=sys.stderr)
        return 1

    rows = collect_year_stats(data_dir)
    if not rows:
        print(f"warn: no cve-*.tsv found under {data_dir}", file=sys.stderr)
        return 1

    tsv_out = data_dir / "cve.report.tsv"
    md_out = data_dir / "cve.report.md"
    write_report_tsv(rows, tsv_out)
    write_report_md(rows, md_out)

    print(f"wrote {tsv_out} ({len(rows)} year rows)")
    print(f"wrote {md_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))