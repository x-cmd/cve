# Reports

Derived aggregates from this repo's per-year CVE TSVs. All files are
regenerated on every CI run (`.github/workflows/release.yml`, every
4h) and committed back to main.

## Files

| File | Format | Top-N | Time window | Source |
| ---  | ---    | ---:  | ---         | ---    |
| [`cve.report.md`](cve.report.md)   | Markdown table | all years | all | `data/cve-*.tsv` |
| [`cve.report.tsv`](cve.report.tsv) | TSV            | all years | all | same |
| [`cwe.report.md`](cwe.report.md)   | Markdown, two top-10 tables | top 10 | since 2024 | `data/cve-*.tsv` ∩ `data/cwe.slim.tsv` |
| [`cwe.top100.by-cve-count.report.tsv`](cwe.top100.by-cve-count.report.tsv)               | TSV | top 100 | all years | same |
| [`cwe.top100.by-cve-score.report.tsv`](cwe.top100.by-cve-score.report.tsv)               | TSV | top 100 | all years | same |
| [`cwe.top100.by-cve-count.since-2024.report.tsv`](cwe.top100.by-cve-count.since-2024.report.tsv) | TSV | top 100 | since 2024 | same |
| [`cwe.top100.by-cve-score.since-2024.report.tsv`](cwe.top100.by-cve-score.since-2024.report.tsv) | TSV | top 100 | since 2024 | same |

Two ranking axes (CVE count vs. mean CVSS score) × two time windows
(all years vs. since 2024) = four TSVs, one for every combination.
The markdown is a single file because the README only needs one view
(the since-2024 view) — the markdown's two top-10 tables are sliced
from the same top-100 pools that the two since-2024 TSVs hold.

## Methodology

### CVE year stats (`cve.report.*`)

One row per year that has at least one CVE (all 28 years from 1999
through the current year), plus a Total row. Each row carries the
year's CVE count, how many had a scored CVSS, the mean score across
the scored ones, and the highest score seen. Source-of-truth:
`data/cve-*.tsv`.

### CWE rankings (`cwe.*.report.tsv` + `cwe.report.md`)

Restricted to CVEs whose `year` column parses to ≥ **2024** for the
`since-2024` files (the `SINCE_YEAR` constant in `.x-cmd/cwe_report.py`).
All-years files use the full history.

Two ranking axes:

1. **By CVE count** — which engineering mistakes keep getting made
   most often?
2. **By average CVSS score** (with a `min 10 CVEs` cutoff to
   suppress single-CWE outliers) — when that mistake is made, how
   bad is it on average?

Filenames are self-describing: `by-cve-{count|score}` is the ranking
axis, `since-YYYY` (when present) is the time window. The four files
together cover every (axis, window) combination.

## Regeneration

Every CI run on `.github/workflows/release.yml`:

1. `tsv.py --rebuild` writes fresh `data/cve-*.tsv`.
2. `report.py` writes `report/cve.report.{tsv,md}`.
3. `cwe_report.py` writes `report/cwe.report.md` plus the four
   `report/cwe.top100.by-*.report.tsv` files.
4. The inline step stitches both `.md` files into `README.md`
   (BEGIN/END markers, idempotent).
5. The commit step pushes `README.md` + the four `report/*` files
   back to main.

To regenerate locally:

```sh
python3 .x-cmd/report.py
python3 .x-cmd/cwe_report.py
```

Both scripts are stdlib-only and take optional `[data_dir]`
`[report_dir]` arguments.
