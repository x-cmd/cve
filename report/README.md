# Reports

Derived aggregates from this repo's per-year CVE TSVs. All four files
are regenerated on every CI run (`.github/workflows/release.yml`,
every 4h) and committed back to main.

| File | Shape | Source | What it answers |
| ---  | ---   | ---    | ---             |
| [`cve.report.md`](cve.report.md)   | Markdown table | `data/cve-*.tsv` | "How has CVE volume and severity changed year over year?" |
| [`cve.report.tsv`](cve.report.tsv) | TSV (one row per year, plus a Total row) | same | machine-readable form of the above |
| [`cwe.report.md`](cwe.report.md)   | Markdown, two top-10 tables | `data/cve-*.tsv` ∩ `data/cwe.slim.tsv` | "What mistakes are engineers making **now** and which hurt the most?" |
| [`cwe.report.tsv`](cwe.report.tsv) | TSV (top 100 CWEs since 2024) | same | machine-readable form; the markdown slices its top-10 from this pool |

## Methodology

### CVE year stats (`cve.report.*`)

One row per year that has at least one CVE (all 28 years from 1999
through the current year), plus a Total row. Each row carries the
year's CVE count, how many had a scored CVSS, the mean score across
the scored ones, and the highest score seen. Source-of-truth:
`data/cve-*.tsv`.

### CWE rankings (`cwe.report.*`)

Restricted to CVEs whose `year` column parses to ≥ **2024** (the
"SINCE_YEAR" constant in `.x-cmd/cwe_report.py`). This keeps the
ranking focused on what's actually being discovered today — an
all-years view overweighted CVEs from 2010-2018 when CNA coverage was
much thinner and the score distribution was different.

Two slices ship:

1. **By CVE count** — which engineering mistakes keep getting made
   most often?
2. **By average CVSS score** (with a `min 10 CVEs` cutoff to
   suppress single-CWE outliers) — when that mistake is made, how
   bad is it on average?

The TSV holds the top **100** CWEs by raw CVE count. The markdown
top-10 is sliced from the same pool (top 10 by count for table 1;
same pool re-sorted by mean score for table 2), so the markdown is
a strict subset of the TSV.

## Regeneration

Every CI run on `.github/workflows/release.yml`:

1. `tsv.py --rebuild` writes fresh `data/cve-*.tsv`.
2. `report.py` writes `report/cve.report.{tsv,md}`.
3. `cwe_report.py` writes `report/cwe.report.{tsv,md}`.
4. The inline step stitches both `.md` files into `README.md`
   (BEGIN/END markers, idempotent).
5. The commit step pushes `README.md` + the four `report/*` files
   back to main.

To regenerate locally:

```sh
python3 .x-cmd/report.py
python3 .x-cmd/cwe_report.py
```

Both scripts are stdlib-only and take optional `[data_dir]` /
`[report_dir]` arguments.
