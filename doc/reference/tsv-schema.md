# TSV schema (`cve-YYYY.tsv`)

9 columns, tab-separated, header row. Rows are in **descending cve-id
order** within each year file.

| # | Column | Type | Example | Meaning |
|---|---|---|---|---|
| 1 | `cve` | str | `CVE-2026-90616` | Full CVE id |
| 2 | `year` | int | `2026` | Year segment, parsed from id |
| 3 | `no` | int | `90616` | Numeric segment (5-digit ids allowed since 2025) |
| 4 | `vp` | str | `Flatpak/Flatpak` | `<vendor>/<product>` joined by `;` (whitespace folded) |
| 5 | `ghsa` | str | `GHSA-8688-9X26-HHXJ` | GitHub Security Advisory id(s), `;`-joined or empty |
| 6 | `score` | float | `7.4` | Highest CVSS base (v4 → v3.1 → v3.0 → v2) or empty |
| 7 | `patched` | 0/1 | `1` | `1` if upstream `solutions[]` non-empty |
| 8 | `cwe` | str | `61` | CWE id(s) (CWE- prefix stripped), `;`-joined or empty |
| 9 | `desc` | str | `In Flatpak before 1.18.1, ...` | First sentence of English description (≤ 240 chars) |

## Field-by-field

### `cve`

Full CVE id including the `CVE-` prefix. Always matches
`CVE-\d{4}-\d+` (4-or-5-digit sequence). Sort by the **integer**
value of the sequence segment — lexicographic sort puts `9999`
before `10000`-`99999` and breaks `x cve | head`.

### `year`

The `YYYY` segment. Used to bucket rows into per-year files
(`cve-2024.tsv`, `cve-2025.tsv`, etc). Always 4 digits.

### `no`

The numeric segment of the id. Up to 5 digits as of 2025.

### `vp`

`<vendor>/<product>` joined by `;`. One entry per affected item
from `containers.cna.affected[]`. Whitespace (newlines, tabs, runs
of spaces) is collapsed to single spaces; empty vendor or product
on a given entry becomes `/`. Example for a multi-affected
record:

```
google/chrome;google/chrome_os
```

### `ghsa`

GitHub Security Advisory id(s) joined by `;`, or empty if no
GHSA reference is present in `containers.cna.references[]`. The
`GHSA-` prefix is preserved (matching GitHub's own format).

### `score`

The **highest** CVSS base score available, in this priority
order: v4.0 → v3.1 → v3.0 → v2.0. First hit wins. Stored as a
plain decimal (e.g. `7.4`); empty when no CVSS is published.

### `patched`

`1` if `containers.cna.solutions[]` is non-empty (CNA published
a remediation), `0` otherwise. This is a weak signal — a `0`
doesn't necessarily mean unpatched; the CNA may have published a
fix without populating `solutions[]`.

### `cwe`

CWE id(s) joined by `;` with the `CWE-` prefix stripped. Example:
a CVE mapped to both SQL Injection and Path Traversal emits
`89;22`. Use `cwe.slim.tsv` (or `cwe.zh.tsv` for Chinese names)
to expand to human-readable labels.

### `desc`

First sentence of the English description, truncated at 240 chars
on a word boundary. The full description is in NVD's JSON record
(see `x cve detail CVE-YYYY-NNNN`). Truncating keeps per-year
files at ~1-9 MB each and makes `x cve fz` lists scannable.

## Conventions

- All 9 columns are always present. Missing values are emitted as
  empty fields, never as `null` / `NaN` / `-`.
- Newlines and tabs inside any free-text column are escaped /
  folded at emit time. See `_extract_vp` and `_extract_description`
  in `.x-cmd/_cve_index.py`.
- No quoting. Tabs are the only delimiter — pipe through `awk -F'\t'`
  or `pandas.read_csv(sep='\t')`.

## Related

- [Bulk query recipes](../guides/bulk-query-by-cwe.md)
- [Python integration (DuckDB / pandas / polars)](../guides/integrate-with-python.md)
- [CWE catalog mirror](./cwe-catalog.md)
- [Release assets reference](./release-assets.md)
