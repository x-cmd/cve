---
x-title: How the data is built
x-desc: How CVEProject/cvelistV5 becomes per-year TSVs in this repo, every 4 hours.
x-sidebar: How the data is built
x-keywords: cvelistV5, tsv.py, cwe.py, cwe_zh.py, release.yml, CI pipeline, xz
x-json-ld:
  '@context': https://schema.org
  '@graph':
    - '@type': TechArticle
      headline: 'How the data is built'
      inLanguage: 'en'
      about: 'x-cmd/cve pipeline'
---

# How the data is built

Every 4 hours, a CI run on GitHub Actions clones
[CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5),
walks every CVE JSON record, and emits a year-indexed 9-column
TSV. The MITRE CWE catalog is fetched the same way. The whole
pipeline is six Python scripts and one workflow file, all
dependency-free.

## Pipeline overview

```text
cvelistV5 JSON ─► tsv.py ─► data/cve-YYYY.tsv
                                  │
mitre.org 2000.csv ─► cwe.py ─► data/cwe.tsv + data/cwe.slim.tsv
                                  │
cwe.org.cn pages   ─► cwe_zh.py ─► data/cwe.zh.tsv
                                  │
                                  ├─► cwe_report.py ─► report/cwe.report.{tsv,md,zh.md}
                                  ├─► latest.py     ─► report/cve.latest-N.report.{tsv,md}
                                  └─► report.py     ─► report/cve.report.{tsv,md}

release.yml inline step ─► README.md + README.cn.md (front-of-page tables)
release.yml xz step      ─► release/data/*.xz (xz-compressed TSVs)
```

## The scripts (all Python 3.8+ stdlib)

| Script | Reads | Writes | What it does |
|---|---|---|---|
| `.x-cmd/tsv.py` | cvelistV5 JSON | `data/cve-YYYY.tsv` | one row per CVE, 9 cols, numeric sort by NNNN desc |
| `.x-cmd/cwe.py` | MITRE 2000.csv | `data/cwe.tsv` + `data/cwe.slim.tsv` | full 21-col catalog + 2-col id→name |
| `.x-cmd/cwe_zh.py` | cwe.org.cn per-id HTML | `data/cwe.zh.tsv` | MITRE's official Chinese mirror, ~91% coverage |
| `.x-cmd/cwe_report.py` | `data/cve-*.tsv` + `data/cwe.{slim,zh}.tsv` | `report/cwe.report.{tsv,md,zh.md}` | Top-N CWE by count / by score |
| `.x-cmd/latest.py` | `data/cve-*.tsv` (head only) | `report/cve.latest-N.report.{tsv,md}` | newest N CVEs for front-of-page table |
| `.x-cmd/report.py` | `data/cve-*.tsv` | `report/cve.report.{tsv,md}` | per-year CVE volume + average / max CVSS |

`_cve_index.py` is the shared parser (json → 9-cell row) and IO
helpers used by all the above.

## Schedule

`.github/workflows/release.yml` runs every 4 hours at
`37 */4 * * *` UTC plus on every push to `main`. A typical run:

1. **Clone** [CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5) shallow.
2. **tsv.py --rebuild** — walk every CVE JSON, write `data/cve-YYYY.tsv`.
3. **cwe.py** — fetch MITRE CWE catalog → `data/cwe.{tsv,slim.tsv}`.
4. **cwe_zh.py** — fetch Chinese names from cwe.org.cn → `data/cwe.zh.tsv`.
5. **cwe_report.py** — Top-N CWE rankings → `report/cwe.report.*`.
6. **latest.py** — newest 10 CVEs → `report/cve.latest-10.report.*`.
7. **report.py** — per-year stats → `report/cve.report.*`.
8. **Inline stitch** — splice the markdown reports into `README.md`
   and `README.cn.md` (BEGIN/END markers, idempotent).
9. **Commit** the new `data/`, `report/`, README files back to `main`.
10. **xz -9** each changed per-year TSV and re-pack `cve-all.tar.xz`.
11. **Upload** to the [`data`](https://github.com/x-cmd/cve/releases/tag/data)
    GitHub release — only changed assets (byte-level `cmp` against
    the previous release's tarball).

A no-op day (zero upstream churn) skips step 9-11 entirely;
consumers' cached sha256s stay valid.

## What lands where

- **`data/cve-*.tsv`** is **not** in git. It's rebuilt every CI run
  and shipped only as the `cve-YYYY.tsv.xz` release asset.
- **`report/*.{tsv,md}`** IS in git. The pre-aggregated rankings
  and the front-page markdowns are the source of truth for the
  README tables.
- **`data/cwe.{tsv,slim.tsv,zh.tsv}`** IS in git. These change
  rarely (once a quarter at most) so committing them is cheap.

## The 9 columns (TL;DR — full reference later)

`cve`, `year`, `no`, `vp`, `ghsa`, `score`, `patched`, `cwe`, `desc`.
See [`2-latest-cves-explained.md`](./2-latest-cves-explained.md) for
field-by-field meaning.

## Where to read next

- [`3-top-cwes-explained.md`](./3-top-cwes-explained.md) — how the Top 10 CWE tables are computed
- [`4-yearly-stats-explained.md`](./4-yearly-stats-explained.md) — YTD, scored vs unscored, totals
- [`5-using-the-data.md`](./5-using-the-data.md) — concrete curl / `x cve` / Python recipes
