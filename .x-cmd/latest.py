#!/usr/bin/env python3
"""
latest.py — emit the top N newest CVE rows as a markdown table.

The "newest" order is whichever order the per-year TSVs are already in:
`tsv.py --rebuild` writes each cve-YYYY.tsv in numeric NNNN descending
(see `_cve_index.py:save_year_files`), and the per-year files are
named in YYYY descending, so reading the head of each file in
descending year order yields the global newest-first stream without
re-sorting.

Inputs: data/cve-*.tsv (sorted desc by NNNN within each year)
Output: report/cve.latest-N.report.{tsv,md}

  report/cve.latest-N.report.tsv  — machine-readable (cve, score, vp,
                                       cwe, desc) for the N newest CVEs
  report/cve.latest-N.report.md   — markdown table inlined into README

We read only the head of each per-year file (enough rows to cover N)
rather than streaming every line of every year; the worst case is
~N/3 KB per year file, well under a second on any modern host.

Stdlib only. Run after tsv.py:
    python3 .x-cmd/latest.py [data_dir] [report_dir]
"""

from __future__ import annotations

import sys
from pathlib import Path

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data"
DEFAULT_REPORT = Path(__file__).resolve().parent.parent / "report"

# Columns in cve-YYYY.tsv:
#   $1 cve  $2 year  $3 no  $4 vp  $5 ghsa  $6 score  $7 patched  $8 cwe  $9 desc
COL_CVE = 0
COL_YEAR = 1
COL_NO = 2
COL_VP = 3
COL_SCORE = 5
COL_PATCHED = 6
COL_CWE = 7
COL_DESC = 8

# How many rows to surface. 10 fits the README "latest 10 CVEs" promise
# without making the front-matter table compete with the per-year
# stats. Configurable via argv for callers that want a different N
# (e.g. a quarterly review report).
DEFAULT_N = 10


def collect_latest(data_dir: Path, n: int) -> list[dict[str, str]]:
    """Walk data/cve-*.tsv in reverse year order, take rows off the head
    of each until we have N. Skip header-less or malformed lines.

    Each row is returned as a dict with the columns we render in the
    README table. Lines without a parseable CVE id (orphan
    continuations from upstream formatting edge cases — should not
    occur after `tsv.py --rebuild`, but defensive) are skipped.
    """
    rows: list[dict[str, str]] = []
    for fp in sorted(data_dir.glob("cve-*.tsv"), reverse=True):
        if len(rows) >= n:
            break
        try:
            with fp.open("r", encoding="utf-8", newline="") as fh:
                for line in fh:
                    if len(rows) >= n:
                        break
                    cols = line.rstrip("\n").split("\t")
                    if len(cols) <= COL_DESC:
                        continue
                    cve_id = cols[COL_CVE].strip()
                    if not cve_id.startswith("CVE-"):
                        # Defensive: skip any orphan / continuation row.
                        continue
                    rows.append({
                        "cve": cve_id,
                        "year": cols[COL_YEAR],
                        "no": cols[COL_NO],
                        "vp": cols[COL_VP],
                        "score": cols[COL_SCORE],
                        "patched": cols[COL_PATCHED],
                        "cwe": cols[COL_CWE],
                        "desc": cols[COL_DESC],
                    })
        except OSError as exc:
            print(f"warn: cannot read {fp}: {exc}", file=sys.stderr)
            continue
    return rows


def write_tsv(out: Path, rows: list[dict[str, str]]) -> None:
    """Emit a 6-column TSV (cve, year, no, score, vp, cwe, desc) — same
    layout as data/cve-*.tsv so consumers that already parse those can
    read this one with no new schema work.
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("cve\tyear\tno\tscore\tvp\tcwe\tdesc\n")
        for r in rows:
            # Clean tabs / newlines from free-text columns so the TSV
            # stays parseable row-by-row.
            vp = r["vp"].replace("\t", " ").replace("\n", " ")
            desc = r["desc"].replace("\t", " ").replace("\n", " ")
            fh.write(
                f"{r['cve']}\t{r['year']}\t{r['no']}\t{r['score']}\t"
                f"{vp}\t{r['cwe']}\t{desc}\n"
            )


def _format_score(s: str) -> str:
    """Render the CVSS score cell. Empty / unparseable → em-dash so the
    table column width stays stable when MITRE omits a score."""
    s = (s or "").strip()
    if not s:
        return "—"
    try:
        return f"{float(s):.1f}"
    except ValueError:
        return s


def _format_cwe(cwe_field: str) -> str:
    """Render the CWE cell as one or more markdown links. Empty → em-dash.
    Multiple ids are ';' joined upstream; we render the first as a link
    and the rest as plain numbers (so a CVE with 5 CWEs doesn't blow up
    the column).
    """
    if not cwe_field or not cwe_field.strip():
        return "—"
    ids = [c.strip() for c in cwe_field.split(";") if c.strip()]
    if not ids:
        return "—"
    head, rest = ids[0], ids[1:]
    head_md = f"[{head}](https://cwe.mitre.org/data/definitions/{head}.html)"
    if rest:
        return head_md + f" (+{len(rest)})"
    return head_md


def _format_desc(desc: str, max_chars: int = 80) -> str:
    """Render the description cell, truncated at a word boundary with
    an ellipsis. Escape pipes so markdown tables don't break.
    """
    s = (desc or "").replace("|", "\\|").replace("\n", " ").strip()
    s = " ".join(s.split())
    if len(s) <= max_chars:
        return s
    cut = s[:max_chars].rsplit(" ", 1)[0] or s[:max_chars]
    return cut + "…"


def write_md(out: Path, rows: list[dict[str, str]], *, lang: str = "en") -> None:
    """Emit the markdown table. `lang` flips the headings / footers:
    'en' for README.md, 'zh' for README.cn.md.
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        if lang == "zh":
            fh.write(f"**最新 {len(rows)} 条 CVE**（按 CVE id 降序 = 发布最新优先）\n\n")
        else:
            fh.write(f"**The {len(rows)} newest CVEs** "
                     "(descending CVE id = newest published first).\n\n")
        fh.write("| CVE | Score | Product | CWE | Description |\n")
        fh.write("| --- | ---:  | ---     | :-: | ---         |\n")
        for r in rows:
            fh.write(
                f"| [{r['cve']}](https://nvd.nist.gov/vuln/detail/{r['cve']}) "
                f"| {_format_score(r['score'])} "
                f"| {_format_desc(r['vp'], 50)} "
                f"| {_format_cwe(r['cwe'])} "
                f"| {_format_desc(r['desc'])} |\n"
            )
        if lang == "zh":
            fh.write("\n_完整描述请点 CVE 链接进 NVT。_\n")
        else:
            fh.write("\n_Click a CVE id for the full record on NVD._\n")


def _tsv_basename(n: int) -> str:
    return f"cve.latest-{n}.report.tsv"


def _md_basename(n: int) -> str:
    return f"cve.latest-{n}.report.md"


def main(argv: list[str]) -> int:
    n = DEFAULT_N
    if len(argv) > 1 and argv[1].isdigit():
        n = int(argv[1])
    data_dir = Path(argv[2]) if len(argv) > 2 else DEFAULT_DATA
    report_dir = Path(argv[3]) if len(argv) > 3 else DEFAULT_REPORT

    if not data_dir.is_dir():
        print(f"error: data directory not found: {data_dir}", file=sys.stderr)
        return 1

    rows = collect_latest(data_dir, n)
    if not rows:
        print(f"warn: no CVEs found under {data_dir}", file=sys.stderr)
        return 1

    # One TSV (machine-readable, language-neutral) and one MD.
    # The MD uses English column headers + Chinese surrounding prose
    # because the actual data cells (CVE id, score, vendor/product,
    # CWE number) are universal identifiers that don't translate.
    # CWE name strings are already provided separately via
    # cwe.report.zh.md when those rows are surfaced through the CWE
    # ranking — the latest-10 table intentionally stays identifier-only
    # to keep the per-row height manageable.
    write_tsv(report_dir / _tsv_basename(n), rows)
    print(f"wrote {report_dir / _tsv_basename(n)} ({len(rows)} rows)", file=sys.stderr)
    write_md(report_dir / _md_basename(n), rows, lang="en")
    print(f"wrote {report_dir / _md_basename(n)}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
