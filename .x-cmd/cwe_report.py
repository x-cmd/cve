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

Outputs (under report/, sibling of data/) — four TSVs and one MD,
all named to make their ranking axis and time window self-describing:

    cwe.top100.by-cve-count.report.tsv           all years, top 100 by CVE count
    cwe.top100.by-cve-score.report.tsv           all years, top 100 by avg CVSS score
    cwe.top100.by-cve-count.since-2024.report.tsv    SINCE_YEAR window, top 100 by CVE count
    cwe.top100.by-cve-score.since-2024.report.tsv    SINCE_YEAR window, top 100 by avg CVSS score
    cwe.report.md                                single markdown, SINCE_YEAR window,
                                                  two top-10 tables (count + score),
                                                  ready to be inlined into the README

The "since-SINCE_YEAR" views answer the only question most readers
actually have: "what are engineers getting wrong NOW and which hurts
the most?" All-years views overweight CVEs from 2010-2018 when CNA
coverage was much thinner and the score distribution was different.

We deliberately do NOT publish a copy of MITRE's 2000.csv — cve repo
only ships derived aggregates. Users wanting the full CWE catalog
hit MITRE directly via `x cwe` (which has its own download path).
"""

from __future__ import annotations

import sys
from pathlib import Path

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data"
DEFAULT_REPORT = Path(__file__).resolve().parent.parent / "report"

# TSV column positions in cve-YYYY.tsv (matches _cve_index.py output):
#   $1 cve  $2 year  $3 no  $4 vp  $5 ghsa  $6 score  $7 patched  $8 cwe  $9 desc
COL_YEAR = 1   # 0-based → $2
COL_CWE = 7   # 0-based → $8
COL_SCORE = 5  # 0-based → $6

# Cutoff for "by avg score" ranking. Below this, a single outlier score
# can dominate the mean and the ranking is noise. 10 CVEs is the floor
# we use elsewhere for similar cutoffs (see report.py totals, etc.).
MIN_CVE_FOR_SCORE_RANK = 10
TOP_N = 10         # rows shown in each markdown table
TOP_N_TSV = 100    # rows written to the TSV — the markdown slices its
                   # top-10 from the same pool so the TSV is a strict
                   # superset of what's inlined.

# Cutoff for the "since YYYY" tables. CWEs that show up only in older
# CVEs and have dropped off the radar stay out of the recent view —
# useful because it surfaces what attackers actually exploit TODAY
# rather than what's accumulated historically. 2024 keeps the tables
# focused on the last ~2.5 years of activity as of writing (2026).
SINCE_YEAR = 2024


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


def write_report(out: Path,
                 rows: list[tuple[str, str, int, float, float]],
                 *,
                 rank_by: str) -> None:
    """Write the top TOP_N_TSV CWEs as a tab-separated file.

    `rank_by` selects the ranking axis ("count" or "score"). The header
    row is fixed so downstream tooling can rely on the schema; rows are
    sorted according to `rank_by` before truncation.
    """
    if rank_by == "count":
        # Stable sort: most-referenced CWEs first, then by max score
        # desc, then by cwe_id ascending.
        sorted_rows = sorted(rows, key=lambda r: (-r[2], -r[4], r[0]))
    elif rank_by == "score":
        # Stable sort: highest avg score first (min MIN_CVE_FOR_SCORE_RANK
        # so single-CWE outliers don't dominate), tiebreak on count desc
        # so ties favor the better-attested CWE.
        sorted_rows = sorted(
            (r for r in rows if r[2] >= MIN_CVE_FOR_SCORE_RANK),
            key=lambda r: (-r[3], -r[2], r[0]),
        )
    else:
        raise ValueError(f"rank_by must be 'count' or 'score', got {rank_by!r}")

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("cwe_id\tname\tcve_count\tavg_score\tmax_score\n")
        for cid, name, count, avg, mx in sorted_rows[:TOP_N_TSV]:
            if count <= 0:
                continue
            avg_str = f"{avg:.2f}"
            mx_str = f"{mx:.1f}"
            fh.write(f"{cid}\t{name}\t{count}\t{avg_str}\t{mx_str}\n")


def _emit_topn_count_table(fh, rows: list[tuple[str, str, int, float, float]]) -> None:
    """Emit the 5-column top-N table for "by CVE count" (Rank, CWE,
    Name, CVEs, Avg score)."""
    fh.write("| Rank | CWE | Name | CVEs | Avg score |\n")
    fh.write("| ---: | :-: | :--- | ---: | ---:      |\n")
    for i, (cid, name, count, avg, _mx) in enumerate(rows, 1):
        if count <= 0:
            continue
        fh.write(f"| {i} | [{cid}](https://cwe.mitre.org/data/definitions/{cid}.html) "
                 f"| {name} | {count:,} | {avg:.2f} |\n")


def _emit_topn_score_table(fh, rows: list[tuple[str, str, int, float, float]]) -> None:
    """Emit the 6-column top-N table for "by avg CVSS score" (Rank,
    CWE, Name, CVEs, Avg, Max)."""
    fh.write("| Rank | CWE | Name | CVEs | Avg score | Max |\n")
    fh.write("| ---: | :-: | :--- | ---: | ---:      | ---: |\n")
    for i, (cid, name, count, avg, mx) in enumerate(rows, 1):
        fh.write(f"| {i} | [{cid}](https://cwe.mitre.org/data/definitions/{cid}.html) "
                 f"| {name} | {count:,} | {avg:.2f} | {mx:.1f} |\n")


def write_report_md(out: Path,
                    rows_since: list[tuple[str, str, int, float, float]]) -> None:
    """Write the markdown snippet the README inlines.

    Single markdown file, SINCE_YEAR window, two top-10 tables: one by
    CVE count (which engineering mistake keeps getting made most
    often?) and one by mean CVSS score (which mistake, when made,
    hurts the most?). Both top-10s are sliced from the same top-100
    pools that the TSVs hold, so the markdown is a strict subset of
    the published data.

    Output is a bare markdown document — no BEGIN/END markers — so the
    file is also readable on its own. release.yml wraps it with
    BEGIN/END when stitching into README.md.
    """
    out.parent.mkdir(parents=True, exist_ok=True)

    # Headline numbers used in the preamble.
    since_cve = sum(r[2] for r in rows_since)
    since_cwe = sum(1 for r in rows_since if r[2] > 0)

    # by-count: first TOP_N of rows_since sorted by cve_count desc
    # (matches the cwe.top100.by-cve-count.since-2024.report.tsv head).
    by_count = sorted(
        (r for r in rows_since if r[2] > 0),
        key=lambda r: (-r[2], -r[4], r[0]),
    )[:TOP_N]

    # by-score: top TOP_N by mean CVSS score, restricted to CWEs with
    # enough samples (matches the cwe.top100.by-cve-score.since-2024
    # .report.tsv head).
    by_score = sorted(
        (r for r in rows_since if r[2] >= MIN_CVE_FOR_SCORE_RANK),
        key=lambda r: (-r[3], -r[2], r[0]),
    )[:TOP_N]

    with out.open("w", encoding="utf-8") as fh:
        fh.write(f"_{since_cve:,} CVEs across {since_cwe:,} distinct CWEs "
                 f"since {SINCE_YEAR}._\n\n")

        # The blockquote carries the question (the WHY); the heading
        # carries the answer-shaped name (the WHAT). Putting the
        # question first reads more naturally and signals that the
        # table exists to answer it.
        fh.write("> What mistake do engineers keep making most often since "
                 f"{SINCE_YEAR}?\n\n")
        fh.write(f"### Top {TOP_N} CWE by CVE count\n\n")
        _emit_topn_count_table(fh, by_count)

        fh.write("\n> When that mistake is made, how bad is it since "
                 f"{SINCE_YEAR}?\n")
        fh.write(f"> _Min {MIN_CVE_FOR_SCORE_RANK} CVEs to suppress "
                 "single-CWE outliers._\n\n")
        fh.write(f"### Top {TOP_N} CWE by average CVSS score\n\n")
        _emit_topn_score_table(fh, by_score)


def _report_filename(rank_by: str, since: int | None) -> str:
    """Build a self-describing filename for one of the four TSV outputs.

    `rank_by` is "count" or "score"; `since` is the SINCE_YEAR value
    (or None for the all-years view).
    """
    parts = [f"cwe.top{TOP_N_TSV}.by-cve-{rank_by}"]
    if since is not None:
        parts.append(f"since-{since}")
    parts.append("report.tsv")
    return ".".join(parts)


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        data_dir = Path(argv[1])
    else:
        data_dir = DEFAULT_DATA
    if len(argv) > 2:
        report_dir = Path(argv[2])
    else:
        report_dir = DEFAULT_REPORT

    if not data_dir.is_dir():
        print(f"error: data directory not found: {data_dir}", file=sys.stderr)
        return 1

    catalog = load_cwe_catalog(data_dir / "cwe.slim.tsv")
    if not catalog:
        print("warn: data/cwe.slim.tsv missing — run .x-cmd/cwe.py first",
              file=sys.stderr)

    # All-years pool — drives the two all-years TSVs.
    scores_by_cwe_all = collect_cve_scores_by_cwe(data_dir)
    rows_all = aggregate(catalog, scores_by_cwe_all)

    # Since-SINCE_YEAR pool — drives the two since-YYYY TSVs + the MD.
    scores_by_cwe_since = collect_cve_scores_by_cwe(data_dir, min_year=SINCE_YEAR)
    rows_since = aggregate(catalog, scores_by_cwe_since)

    # Four TSV outputs, two ranking axes × two time windows.
    outputs = [
        (report_dir / _report_filename("count", None),    rows_all,    "count"),
        (report_dir / _report_filename("score", None),    rows_all,    "score"),
        (report_dir / _report_filename("count", SINCE_YEAR), rows_since, "count"),
        (report_dir / _report_filename("score", SINCE_YEAR), rows_since, "score"),
    ]
    for path, rows, rank_by in outputs:
        write_report(path, rows, rank_by=rank_by)
        n_written = min(TOP_N_TSV, sum(1 for r in rows if r[2] > 0))
        print(f"wrote {path} ({n_written} CWE rows)", file=sys.stderr)

    # Single markdown output — SINCE_YEAR window, two top-10 tables.
    write_report_md(report_dir / "cwe.report.md", rows_since)
    print(f"wrote {report_dir / 'cwe.report.md'}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))