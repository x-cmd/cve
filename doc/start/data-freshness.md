# Data freshness

When does a new CVE show up here?

## Schedule

The release workflow runs every 4 hours at `37 */4 * * *` UTC, plus
on every push to `main`. Worst-case latency for a newly published
CVE: **4 hours** from the moment MITRE publishes it.

## Verifying freshness

Every front-of-page README has a "Data as of: YYYY-MM-DD" stamp
pulled from the freshly-stitched `report/cve.report.md`. The two
labels always match:

- `README.md`: **Data as of: YYYY-MM-DD**
- `report/cve.report.md`: the per-year stats table

If the stamp hasn't moved in 24+ hours, something is wrong —
open an issue at <https://github.com/x-cmd/cve/issues>.

## How the pipeline fits together

```
cve-YYYY.tsv (raw) ──► tsv.py --rebuild (Step 1 of release.yml)
                              │
                              ▼
                        data/cve-*.tsv  (committed to main)
                              │
                              ▼
                   cwe.py + cwe_zh.py + cwe_report.py
                              │
                              ▼
                report/*.tsv + report/cwe.report.{md,zh.md}
                              │
                              ▼
          release.yml inline step ─► README + README.cn.md
                              │
                              ▼
                      xz -9 + release asset upload
                              │
                              ▼
        https://github.com/x-cmd/cve/releases/download/data/*
```

## What doesn't trigger a refresh

- A new CWE entry that doesn't appear in any CVE: `cwe.py` runs on
  the 4-hour cron and will pick it up next run.
- A CVE reassigned to a different CWE: yes, picked up — `tsv.py`
  re-emits the row with the new `cwe` column.
- A CVE withdrawn: depends on whether MITRE marks the JSON record
  `REJECT` — withdrawn records usually disappear from
  `cvelistV5` and our pipeline naturally drops them.

## Rate of arrival

See [`how-fast-is-cve-growing.md`](../guides/cve-vs-cwe-vs-cpe.md)
or the live per-year stats table at the top of
[`README.md`](../../README.md).
