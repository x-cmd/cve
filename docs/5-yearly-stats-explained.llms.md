---
name: 5-yearly-stats-explained
description: How to read the per-year CVE volume + CVSS stats table — YTD, scored vs unscored, what the Totals row means.
type: reference
---

# Core Content
core_features:
  - Year column: 4-digit year or **Total** (sum across all years).
  - CVEs column: count of CVE rows for the year.
  - Scored column: of those, how many have a non-empty CVSS score.
  - Avg score column: mean CVSS across scored CVEs in the year.
  - Max score column: highest CVSS seen in the year.
  - Current-year row carries a YTD annotation (e.g. '2026 (YTD as of 2026-09-12)').
  - Total row: sum of CVEs across all years, weighted-avg score.
  - Avg score renders as em-dash (—) when no scored CVEs in that year.

# Key Information
highlights:
  - Total grows monotonically (withdrawn CVEs are dropped retroactively).
  - Recent yearly volume: ~56k in 2026 YTD, ~43k in 2025, ~38k in 2024.
  - Roughly doubling every five years.

# Use Cases
use_cases:
  - Calibrate your scanning cadence (annual cadence = 6-12 months behind).
  - Compare severity trends year-over-year.
  - Identify years with high severity (Max score close to 10).

# Related Resources
official:
  website: https://x-cmd.com/cve/

# Summary
Per-year CVE volume + scored count + average + max CVSS, going back to 1999. The YTD annotation on the current-year row, what the em-dash for Avg score means, and why Total grows monotonically.
