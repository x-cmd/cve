---
name: 2-how-data-is-built
description: How CVEProject/cvelistV5 becomes per-year TSVs every 4 hours — the 6 Python scripts and the release.yml workflow.
type: pipeline
---

# Core Content

core_features:

- .x-cmd/tsv.py: walks every CVE JSON, emits data/cve-YYYY.tsv (9 cols, NNNN desc).
- .x-cmd/cwe.py: MITRE CWE catalog → data/cwe.tsv (21 cols) + data/cwe.slim.tsv (2 cols).
- .x-cmd/cwe_zh.py: MITRE Chinese mirror → data/cwe.zh.tsv (~91% coverage).
- .x-cmd/cwe_report.py: Top-N CWE rankings → report/cwe.report.{tsv,md,zh.md}.
- .x-cmd/latest.py: newest N CVEs → report/cve.latest-N.report.{tsv,md}.
- .x-cmd/report.py: per-year stats → report/cve.report.{tsv,md}.
- CI: .github/workflows/release.yml runs every 4h (cron `37 */4 * * *` UTC) + on every push to main.
- xz -9 each changed per-year TSV; re-pack cve-all.tar.xz; upload to GitHub release `data`.

## Key Information

highlights:

- All 6 scripts are dependency-free (Python 3.8+ stdlib).
- Only tsv.py needs a network clone of cvelistV5.
- Per-year TSVs are NOT in git — released as xz assets only.
- report/* TSVs and READMEs ARE in git.
- data/cwe.{tsv,slim.tsv,zh.tsv} ARE in git (rarely change).

## Use Cases

use_cases:

- Understand where the live data on the README comes from.
- Reproduce the pipeline locally.
- Diagnose CI failures.

## Related Resources

official:
  website: <https://x-cmd.com/cve/>

## Summary

The pipeline behind the data — 6 Python scripts and one workflow file. Every 4 hours: clone cvelistV5, walk CVE JSON, emit per-year TSVs, fetch CWE catalog, rank by count and by mean CVSS, fetch Chinese names, inline the results into README, xz-compress, upload as release assets.
