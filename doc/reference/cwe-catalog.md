# CWE catalog

This repo mirrors MITRE's full
[CWE catalog](https://cwe.mitre.org/) as two TSVs, both
regenerated every 4 hours by the CI pipeline.

## Files

### `data/cwe.tsv` (21 columns, full catalog)

Verbatim mirror of MITRE's `2000.csv` (header preserved, spaces
in column names replaced with `_`). About 3 MB. Used by
`x-cwe` module and any consumer that needs the full CWE metadata
(weakness abstraction, status, applicable platforms, mitigation,
detection methods, related attack patterns, etc).

| Col | Header (after `cwe.py`) |
|---|---|
| 1 | `CWE-ID` |
| 2 | `Name` |
| 3 | `Weakness_Abstraction` |
| 4 | `Status` |
| 5 | `Description` |
| 6 | `Extended_Description` |
| 7 | `Related_Weaknesses` |
| 8 | `Weakness_Ordinalities` |
| 9 | `Applicable_Platforms` |
| 10 | `Background_Details` |
| 11 | `Alternate_Terms` |
| 12 | `Modes_Of_Introduction` |
| 13 | `Exploitation_Factors` |
| 14 | `Likelihood_of_Exploit` |
| 15 | `Common_Consequences` |
| 16 | `Detection_Methods` |
| 17 | `Potential_Mitigations` |
| 18 | `Observed_Examples` |
| 19 | `Functional_Areas` |
| 20 | `Affected_Resources` |
| 21 | `Taxonomy_Mappings` |
| 22 | `Related_Attack_Patterns` |
| 23 | `Notes` |

### `data/cwe.slim.tsv` (2 columns, id + name)

| Col | Header |
|---|---|
| 1 | `CWE-ID` |
| 2 | `Name` |

Same row order as `cwe.tsv` — used by `cwe_report.py` to join
against `cve-YYYY.tsv` for the Top-10 rankings.

### `data/cwe.zh.tsv` (2 columns, Chinese names)

| Col | Header |
|---|---|
| 1 | `CWE-ID` |
| 2 | `Name_Zh` |

Chinese-language names fetched from
[cwe.org.cn](https://cwe.org.cn) — MITRE's official Chinese
mirror. ~91% coverage of the 969-entry catalog; the remaining
9% (mostly views and deprecated ids) fall back to English at
render time.

Caching: `.x-cmd/.cwe_zh.cache/<id>.html` for 30 days
(success) or 1 day (failure). The `cwe_zh.py` script guards
against wiping the catalog when coverage is below 50% — see
`MIN_COVERAGE_PCT` in the script.

## Joining CVE rows against CWE names

```python
import pandas as pd

cve = pd.read_csv("cve-2026.tsv", sep="\t", dtype=str, keep_default_na=False)
cwe = pd.read_csv("cwe.slim.tsv", sep="\t", dtype=str, keep_default_na=False)
cwe_zh = pd.read_csv("cwe.zh.tsv", sep="\t", dtype=str, keep_default_na=False)

# Expand multi-CWE rows to one row per CWE id
cve_exploded = (
    cve.assign(cwe_id=cve["cwe"].str.split(";"))
        .explode("cwe_id")
        .query("cwe_id != ''")
)

# Join
enriched = cve_exploded.merge(cwe, left_on="cwe_id", right_on="CWE-ID")
enriched_zh = cve_exploded.merge(cwe_zh, left_on="cwe_id", right_on="CWE-ID")
```

## Common CWE ids you'll see at the top

Per the latest `report/cwe.top100.by-cve-count.since-2024.report.tsv`:

| Rank | CWE | Name | CVEs (since 2024) |
|---|---|---|---|
| 1 | [79](https://cwe.mitre.org/data/definitions/79.html) | Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') | ~17,000 |
| 2 | [89](https://cwe.mitre.org/data/definitions/89.html) | Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') | ~7,700 |
| 3 | [862](https://cwe.mitre.org/data/definitions/862.html) | Missing Authorization | ~6,300 |
| 4 | [22](https://cwe.mitre.org/data/definitions/22.html) | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | ~3,300 |
| 5 | [78](https://cwe.mitre.org/data/definitions/78.html) | Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') | ~2,500 |

(Numbers shift slightly every 4 hours as new CVEs land. Pull the
current `report/` for the live top-N.)

## Related

- [TSV schema](./tsv-schema.md) — column meanings for `cve-YYYY.tsv`
- [Release assets](./release-assets.md) — every `.xz` asset URL
- [Bulk query by CWE](../guides/bulk-query-by-cwe.md)
