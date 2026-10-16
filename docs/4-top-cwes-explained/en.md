---
x-title: How the Top CWE tables are computed
x-desc: How CVE rows are joined against CWE ids, ranked by count and by mean CVSS, and why the "since 2024" window exists.
x-sidebar: Top CWEs explained
x-keywords: CWE join, mean CVSS, since 2024, MIN_CVE_FOR_SCORE_RANK, top 100 CWE
x-json-ld:
  '@context': https://schema.org
  '@graph':
    - '@type': TechArticle
      headline: 'How the Top CWE tables are computed'
      inLanguage: 'en'
      about: 'CWE ranking'
---

# How the Top CWE tables are computed

The two CWE tables on [`README.md`](../../README.md) come from
the same join, ranked two different ways. This page explains
what the join does, what the two ranking axes mean, and why the
numbers shift over time.

## The join: every CVE × every CWE it references

Each CVE row in `data/cve-YYYY.tsv` has a `cwe` column holding
one or more CWE ids (prefix stripped, joined by `;`):

```text
CVE-2024-12345  cwe="79;352"     # XSS + CSRF
CVE-2024-67890  cwe="89"          # SQL Injection
CVE-2024-99999  cwe=""            # no weakness category assigned
```

For ranking, we **explode** the multi-CWE rows into one record
per (CVE, CWE) pair. A CVE with `cwe="79;352"` contributes +1
to both CWE-79 and CWE-352. A CVE with empty `cwe` contributes
to nothing.

## Ranking by CVE count

`report/cwe.top100.by-cve-count.report.tsv` sorts every CWE
descending by that exploded count. Stable tiebreak: by mean CVSS
score desc, then by CWE id asc.

**Why "since 2024" exists:** without a window, the all-years
view is dominated by CVEs from 2008-2018 — every SQL injection
in the 2010 PHP era shows up, and the modern classes (LLM
prompt injection, agent authorization, MCP supply chain) never
make the top of the list. The `since 2024` view drops everything
before 2024 so the ranking reflects **what engineers are getting
wrong right now** — see the SINCE_YEAR constant in
[`.x-cmd/cwe_report.py`](https://github.com/x-cmd/cve/blob/main/.x-cmd/cwe_report.py).

## Ranking by mean CVSS

`report/cwe.top100.by-cve-score.report.tsv` sorts CWEs by
**mean CVSS base score** across their associated CVEs (with at
least 10 samples per CWE — see `MIN_CVE_FOR_SCORE_RANK`).

**Why mean and not median:** CVSS scores cluster around
discrete values (4.0, 7.5, 9.8, etc.), and median would give
every CWE a tie at 7.5. The mean reflects whether a class
*systematically* scores higher than another.

**Why the "at least 10 samples" floor:** a single CVE-2020-1234
classified as `Embedded Malicious Code` (CWE-506) with score
9.8 would otherwise dominate the ranking — that's a single
incident, not a class trend. The 10-sample floor suppresses
those outliers.

## What's not in the ranking

- **CWE views and categories** (CWE-699 "Software Development",
  CWE-1000 "Research Concepts"). The `cwe_report.py` ranks
  individual CWEs only; aggregated categories aren't surfaced
  here. If you need that, fetch the MITRE catalog directly
  ([cwe.mitre.org/data/csv/2000.csv.zip](https://cwe.mitre.org/data/csv/2000.csv.zip)).
- **Empty-CWE CVEs.** ~15-20% of recent CVEs have an empty
  `problemTypes[]` in the upstream JSON. They appear in the
  per-year stats but not in any CWE ranking.
- **Withdrawn / rejected CVEs.** Once MITRE marks a record as
  `REJECT`, our pipeline drops it from the next `tsv.py` rebuild
  — those rows simply disappear from the catalog.

## Why the numbers shift run-to-run

Two reasons the table changes every 4 hours:

1. **New CVEs landing.** MITRE publishes ~50-200 CVEs per day
   in 2026; each may reference new CWE ids or reinforce
   existing ones.
2. **CNAs re-classifying.** A CNA can publish an update to a
   CVE's `problemTypes[]` — e.g. adding CWE-862 to a CVE that
   originally only had CWE-79. Our rebuild picks that up on the
   next run; the row count and ranking shift accordingly.

The pre-aggregated TSVs are committed to git on every CI run, so
you can `git log -- report/cwe.top100.by-cve-count.since-2024.report.tsv`
to see the historical shape of the ranking.

## How the file is built

`.x-cmd/cwe_report.py` does the join + ranking, emits both TSVs
(all years + since 2024) and two markdown files (English +
Chinese). The Chinese version is only emitted when
`data/cwe.zh.tsv` has at least one row — see
[`1-how-data-is-built.md`](./1-how-data-is-built.md) for how that
file is populated.

## Where to read next

- [`1-how-data-is-built.md`](./1-how-data-is-built.md) — pipeline + scripts
- [`2-latest-cves-explained.md`](./2-latest-cves-explained.md) — column meanings
- [`4-yearly-stats-explained.md`](./4-yearly-stats-explained.md) — the third table on the README
- [`5-using-the-data.md`](./5-using-the-data.md) — pull the ranking TSVs and slice them yourself
