---
x-title: Reading the yearly CVE growth table
x-desc: How to read the per-year CVE volume + CVSS stats table — YTD, scored vs unscored, what the totals mean.
x-sidebar: Yearly stats explained
x-keywords: per-year CVE stats, YTD as of, scored vs unscored, cve.report.tsv, total
x-json-ld:
  '@context': https://schema.org
  '@graph':
    - '@type': TechArticle, headline: Reading the yearly CVE growth table, inLanguage: en, about: cve.report.tsv
---

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

![CVE records per year, 1999 → 2026](./assets/cve-growth.svg)

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

## Why the CVE id range is bigger than the row count

For each year the per-year TSV holds fewer rows than the maximum
NNNN sequence value would suggest. Sample (computed from
`data/cve-YYYY.tsv`):

| Year | Rows | Max NNNN | Gap | Gap % |
|---|---|---|---|---|
| 2014 | 8,426 | 125,128 | 116,702 | 93% |
| 2015 | 8,110 | 1,142,857 | 1,134,747 | 99% |
| 2018 | 16,187 | 1,999,047 | 1,982,860 | 99% |
| 2024 | 38,450 | 58,382 | 19,932 | 34% |
| 2026 YTD | 56,167 | 90,679 | 34,512 | 38% |

The 98-99% gaps for 2014-2019 are not bugs. In that era MITRE
assigned **large reserved id blocks** to the big CNAs — Microsoft,
Apple, Adobe, Google, Oracle each got whole 10000-id ranges and
filled only a fraction. Concrete shape of 2014 (verified against
the upstream `cvelistV5` JSON tree):

| 2014 NNNN range | Rows | Likely owner |
|---|---|---|
| 1 – 9,999 | 8,162 | general / small CNAs |
| 10,000 – 19,999 | 102 | Microsoft (reserved) |
| 20,000 – 99,999 | 0 | (no CNAs filled this range) |
| 100,000 – 109,999 | 39 | Microsoft (mid-range) |
| 120,000 – 125,127 | 123 | Apple (late-2014 block) |

So the 93% gap in 2014 is two big blocks reserved for Microsoft
(100k) and Apple (120k) that each got 1-2% filled. The 99% gap
in 2015 follows the same shape. Once the CNA-based system
matured around 2020 the gap settled at 38-53%, which is the
steady-state combination of:

- **Reserved blocks** the CNAs hold but haven't yet assigned.
- **REJECT** records — MITRE marks a CVE withdrawn; we drop the
  row on the next rebuild but the id number is never reused.
- **Duplicate merges** — multiple JSON files describing the same
  CVE get deduped to a single row by `tsv.py`'s `cve_id` key.

This is why [issue #3](https://github.com/x-cmd/cve/issues/3)
matters: an older lexicographic sort would put `CVE-2026-99999`
**before** `CVE-2026-10000` (because `'9' > '1'` in string compare),
hiding the real highest id under a mountain of reserved-but-
empty slots. Sorting by the NNNN integer makes the gap visible
and the file browsable.

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
