---
name: 3-latest-cves-explained
description: How to read the 10-newest-CVE table at the top of the README — column meanings, CVSS primer, what 'patched' really means.
type: reference
---

# Core Content

core_features:

- CVE column: full id like CVE-2026-90616; click for NVD detail page.
- Score column: highest CVSS base score (0-10). 9+ critical, 7-8.9 high, 4-6.9 medium.
- Product column: <vendor>/<product> joined by ; if multiple.
- CWE column: first CWE id with +N if more; click for MITRE weakness definition.
- Description column: first sentence only, ≤ 80 chars.
- CVSS primer: v4.0 → v3.1 → v3.0 → v2.0 priority; highest wins.
- Blank CVSS ≠ low severity; it means MITRE has no published score.
- patched: 0/1 is a weak signal: doesn't mean unpatched / your-version-pulled-it.

## Key Information

highlights:

- CVSS v4.0 spec: first.org/cvss/v4.0/specification-document.
- NVD CVSS calculator: nvd.nist.gov/vuln-metrics/cvss/v4-calculator.
- CVEs are sorted by NNNN integer (5-digit ids allowed since 2025).

## Use Cases

use_cases:

- Identify which CVEs affect your dependencies.
- Decide which to patch first (CVSS as starting point).
- Understand the 'patched' column's limitations.

## Related Resources

official:
  website: <https://x-cmd.com/cve/>

## Summary

What every column in the latest-10-CVE table means — CVE id, CVSS score, product, CWE, description. CVSS primer covering v4.0 / v3.1 / v3.0 / v2.0 priority, why blank CVSS isn't 'low severity', and why the 'patched' column is a weak signal.
