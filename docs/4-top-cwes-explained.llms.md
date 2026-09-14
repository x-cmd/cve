---
name: 4-top-cwes-explained
description: How CVE rows join against CWE ids, ranked by count and by mean CVSS, and why the 'since 2024' window exists.
type: reference
---

# Core Content

core_features:

- Join: each CVE has a cwe column with one or more ids; explode to (CVE, CWE) pairs.
- A CVE with cwe='79;352' contributes +1 to both CWE-79 and CWE-352.
- By count: sort CWEs by total CVE references descending.
- By mean CVSS: sort CWEs by mean CVSS score across their CVEs, with ≥ 10 samples per CWE.
- since 2024 window drops pre-2024 CVEs to reflect what engineers are getting wrong RIGHT NOW.
- Stable tiebreaks: by mean CVSS desc, then by CWE id asc.

## Key Information

highlights:

- Empty-CWE CVEs are excluded from ranking (~15-20% of recent CVEs).
- Withdrawn / rejected CVEs are dropped by the pipeline.
- CNAs can re-classify CVEs (adding/removing CWEs), causing rankings to shift between runs.

## Use Cases

use_cases:

- Understand why the rankings shift every 4 hours.
- Pick the right ranking axis (count vs mean CVSS).
- Calibrate your own code audit priorities.

## Related Resources

official:
  website: <https://x-cmd.com/cve/>

## Summary

The mechanics behind the Top 10 / Top 100 CWE tables — the explode-join, the since-2024 window, the ≥ 10-sample floor on the mean-CVSS ranking, and why rankings drift every CI run.
