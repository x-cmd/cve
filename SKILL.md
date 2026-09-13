---
name: cve
description: Daily-updated CVE / CWE index for the x-cmd shell module. Use when the user asks for "CVE database", "vulnerability list", "CWE catalog", "x cve", "latest CVEs", "top CWEs", or wants to look up / download / query CVE records.
metadata: type=database, source=cveproject-cvelistv5, schema=tsv-9-col, refresh=4h, license=cc-by-4.0, scope=cve-cwe
---
# x-cmd/cve — using the CVE / CWE data
Two consumption paths. Pick whichever fits the workflow.

## 1. Directly use the TSV (no install)
Data is plain xz-compressed TSVs at https://github.com/x-cmd/cve/releases/tag/data.
```sh
# One year (~5 MB xz) — fastest way to get started
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz | xz -dc > cve-2026.tsv
# Whole catalog (~21 MB xz)
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-all.tar.xz | tar -xJ
# CWE catalog only (~150 KB xz, ~3 MB raw)
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cwe.tsv.xz | xz -dc > cwe.tsv
```

## 2. Use `x cve` shell module (auto-caching + queries)
```bash
x cve                          # list all CVEs (newest first)
x cve fz                       # fzf picker
x cve info CVE-2024-0001        # one record by id (YYYY-NNNN shorthand works too)
x cve detail CVE-2024-0001      # full upstream JSON from CVEProject/cvelistV5
x shodan cve CVE-2024-0001      # EPSS + KEV + exploit-writeups enrichment
x cve -h                       # full help
```

## TSV schema (9 columns, `cve-YYYY.tsv`)
| # | Col | Type | Example | Meaning |
|---|---|---|---|---|
| 1 | cve | str | `CVE-2026-90616` | Full CVE id |
| 2 | year | int | `2026` | Year segment |
| 3 | no | int | `90616` | Numeric segment (5-digit ids allowed since 2025) |
| 4 | vp | str | `Flatpak/Flatpak` | `<vendor>/<product>` joined by `;` (whitespace folded) |
| 5 | ghsa | str | `GHSA-8688-9X26-HHXJ` | GitHub Security Advisory id(s), `;`-joined or empty |
| 6 | score | float | `7.4` | Highest CVSS base (v4 → v3.1 → v3.0 → v2) or empty |
| 7 | patched | 0/1 | `1` | `1` if upstream `solutions[]` non-empty |
| 8 | cwe | str | `61` | CWE id(s) (CWE- prefix stripped), `;`-joined or empty |
| 9 | desc | str | `In Flatpak before 1.18.1, ...` | First sentence of English description (≤ 240 chars) |

## CWE schema (2 columns, `cwe.slim.tsv`)
| Col | Example |
|---|---|
| CWE-ID | `79` |
| Name | `Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')` |

`data/cwe.zh.tsv` (same 2 columns) carries MITRE's official Chinese names from cwe.org.cn (~91% coverage; English fallback for the rest).

## Common awk queries
```sh
# XSS (CWE-79) scored >= 7 since 2024
xz -dc cve-2024.tsv cve-2025.tsv cve-2026.tsv 2>/dev/null \
  | awk -F'\t' '$8 ~ /(^|;)79(;|$)/ && $6+0 >= 7'
# Apache HTTP Server CVEs in 2026
xz -dc cve-2026.tsv | awk -F'\t' '$4 ~ /Apache\/HTTP Server/ {print $1, $6, $9}'
# Top vendors by CVE count since 2024
xz -dc cve-2024.tsv cve-2025.tsv cve-2026.tsv 2>/dev/null \
  | awk -F'\t' '{ for (i=1;i<=split($4,p,";");i++) print p[i] }' \
  | sort | uniq -c | sort -rn | head -20
```

## Pre-aggregated rankings (under `report/`)
File | Ranks | Window
---|---|---
`report/cwe.top100.by-cve-count.report.tsv` | by count | all years
`report/cwe.top100.by-cve-score.report.tsv` | by avg CVSS | all years
`report/cwe.top100.by-cve-count.since-2024.report.tsv` | by count | since 2024
`report/cwe.top100.by-cve-score.since-2024.report.tsv` | by avg CVSS | since 2024
`report/cwe.report.md` / `report/cwe.report.zh.md` | Top-10 markdown | since 2024
`report/cve.latest-10.report.{tsv,md}` | newest 10 CVEs | —

## Quick decision
- One record, browsing, Shodan enrichment → §2 (`x cve`).
- Bulk analytics across ~370k rows or joins into Python / R / DuckDB → §1 (curl + awk).

## Sources
- https://github.com/CVEProject/cvelistV5 — upstream JSON (CC BY 4.0)
- https://cwe.mitre.org — CWE catalog (CC BY 4.0)
- https://cwe.org.cn — MITRE's official Chinese mirror
- https://nvd.nist.gov — NVD detail pages
- https://x-cmd.com/mod/cve — `x cve` shell module
- https://x-cmd.com/mod/cwe — `x cwe` shell module
- https://x-cmd.com/mod/shodan/cve — `x shodan cve` enrichment
