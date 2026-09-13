---
x-title: 怎么读年度 CVE 增长表
x-desc: 怎么读 per-year CVE 量 + CVSS 统计表 — YTD、已打分 vs 未打分、Total 行的含义。
x-sidebar: 年度统计解读
x-keywords: CVE, CWE, AI 安全, 漏洞情报
x-json-ld:
  '@context': https://schema.org
  '@graph':
    - '@type': TechArticle, headline: Reading the yearly CVE growth table, inLanguage: en, about: cve.report.tsv
---
README 上第三张表 ——「CVE 增长得有多快？」——来自 `report/cve.report.{tsv,md}`。展示自 1999 年以来每年的 CVE 量 + 已打分 + 平均 + 最高 CVSS。


# Reading the yearly CVE growth table

The third table on [`README.md`](../../README.md) — "How fast is
CVE growing?" — comes from `report/cve.report.{tsv,md}`. It shows
CVE volume + scored count + average + max CVSS for every year
since 1999.

## The columns

| Field | What it is | How to use it |
|---|---|---|
| `Year` | The 4-digit year, or `**Total**` | Single-year rows are sortable; the Total row is the sum across all years |
| `CVEs` | Count of CVE rows for the year | The actual count of new vulnerabilities published that calendar year |
| `Scored` | Of those, how many have a non-empty CVSS score | Scored / total = "% scored". A blank score means no CVSS published, not "low severity" |
| `Avg score` | Mean CVSS across the scored ones | A single-number summary; misleading at small sample sizes, useful for trends |
| `Max score` | Highest CVSS seen in the year | The "what's the worst this year produced" indicator |

The current-year row carries a `YTD` annotation (e.g.
`2026 (YTD as of 2026-09-12)`) because the year isn't done yet —
the `CVEs` count is partial, not final. Same shape as the
end-of-year number, just smaller.

## The total row

`Total` is the **sum across all years**, not the count of unique
CVE ids. Because the catalog keeps historical records (we don't
drop withdrawn CVEs retroactively), the total is monotonically
non-decreasing — it only grows or stays flat as new years are
added.

Two related totals exist, in different files:

- `report/cve.report.tsv` `Total` — sum of `CVEs` across years
  (raw catalog size). On 2026-09-12 this is ~370,000.
- The CWE ranking's `sum(r[2] for r in rows_since)` in
  `cwe_report.py` — distinct `(CVE, CWE)` pairs in the
  `since 2024` window. Different number; not on the README.

## Why some years have Avg score `—`

Years with zero scored CVEs (2000 in the current data) render
the `Avg score` cell as an em-dash (`—`) rather than `0.0` or
`NaN`. The TSV carries the same em-dash. The Total row computes
`avg = sum(scored_count × year_avg) / sum(scored_count)` — a
weighted average across years — so it stays sane when some years
contribute zero scores.

## How fast is the catalog actually growing?

Recent years:

- 2018: 16,188 CVEs
- 2020: 19,392
- 2022: 26,445
- 2024: 38,451
- 2026 YTD (Sep 13): 56,168 — on track for ~75,000 by year-end

The doubling interval is shrinking: 2018 → 2023 (5 years) nearly
doubled (16k → 30k), 2023 → 2026 (3 years) is on track to 2.5×.
2024 → 2026 is doubling in just two years. The growth is
accelerating, not stable.

If your security scanning cadence is annual, you're 6-12 months
behind on the most recent year's worth of disclosures. The 4-hour
refresh cadence in this repo's CI is one answer; per-stream
subscription (NVD RSS, vendor advisories) is another.

## What "scored" means

A CVE is "scored" when the CNA published at least one CVSS
vector — v2.0, v3.0, v3.1, or v4.0. Older CVEs (1999-2016) and
smaller CNAs tend to leave the field empty; modern CVEs are
almost always scored (98%+ in 2024+).

The pipeline stores the **highest** score across the four
versions, in priority order v4 → v3.1 → v3.0 → v2. The `score`
column in `cve-YYYY.tsv` is that single number; the raw upstream
JSON (accessible via `x cve detail CVE-YYYY-NNNN`) carries the
full vector.

## How the file is built

`.x-cmd/report.py` walks every `data/cve-YYYY.tsv`, counts rows +
scored rows + sums scores per year, then writes both
`cve.report.tsv` (5 cols, machine-readable) and `cve.report.md`
(markdown table for the README).

## Where to read next

- [`1-how-data-is-built.md`](./1-how-data-is-built.md) — pipeline + scripts
- [`3-top-cwes-explained.md`](./3-top-cwes-explained.md) — the other two tables
- [`5-using-the-data.md`](./5-using-the-data.md) — query the per-year TSV yourself
