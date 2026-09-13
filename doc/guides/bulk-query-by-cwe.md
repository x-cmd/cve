# Bulk query: every CVE referencing a CWE

For analytics — which CVEs map to CWE-79 (XSS) since 2024? What's
the CVSS distribution? Top vendors? These need bulk queries, not
one-record lookups.

## Pure awk on raw TSVs

The 8th column (`cwe`) is `;`-joined CWE ids with the `CWE-`
prefix stripped. Match the whole `;`-bounded field:

```sh
# Every XSS CVE in 2026
xz -dc <(curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz) \
  | awk -F'\t' '$8 ~ /(^|;)79(;|$)/ {print $1, $4, $6}'
```

Across multiple years (since 2024):

```sh
for y in 2024 2025 2026; do
  xz -dc <(curl -fsSL "https://github.com/x-cmd/cve/releases/download/data/cve-$y.tsv.xz")
done 2>/dev/null \
  | awk -F'\t' '$8 ~ /(^|;)79(;|$)/ && $6+0 >= 7' \
  | sort -t$'\t' -k6,6nr
```

The `($8 ~ /(^|;)79(;|$)/)` regex matches `79` exactly, not `179`,
`779`, or `789`. The `$6+0 >= 7` keeps only scored CVSS >= 7.

## Top vendors for a given CWE

```sh
xz -dc cve-2024.tsv cve-2025.tsv cve-2026.tsv 2>/dev/null \
  | awk -F'\t' '$8 ~ /(^|;)79(;|$)/ {
      for (i=1; i<=split($4, p, ";"); i++) print p[i]
    }' \
  | sort | uniq -c | sort -rn | head -20
```

## CVSS distribution per CWE

```sh
# Mean CVSS for CWE-22 (Path Traversal) since 2024
xz -dc cve-2024.tsv cve-2025.tsv cve-2026.tsv 2>/dev/null \
  | awk -F'\t' '$8 ~ /(^|;)22(;|$)/ && $6!="" {
      n++; sum += $6
      if ($6+0 > max) max = $6
    } END {
      printf "CWE-22: n=%d  mean=%.2f  max=%.1f\n", n, sum/n, max
    }'
```

## Use the pre-aggregated rankings for the common cases

`report/` ships pre-computed top-100 lists so you don't have to
re-aggregate every time:

| File | What it is |
|---|---|
| `report/cwe.top100.by-cve-count.report.tsv` | Top 100 CWEs by total CVE references, all years |
| `report/cwe.top100.by-cve-count.since-2024.report.tsv` | Same, but since 2024 |
| `report/cwe.top100.by-cve-score.report.tsv` | Top 100 CWEs by mean CVSS |
| `report/cwe.top100.by-cve-score.since-2024.report.tsv` | Same, but since 2024 |

```sh
curl -fsSL https://raw.githubusercontent.com/x-cmd/cve/main/report/cwe.top100.by-cve-count.since-2024.report.tsv \
  | column -t -s $'\t' | head -15
```

## For more than 100 CWEs or custom windows

You need the raw data. Two patterns:

- **One-off** (`awk` + `xz -dc`) — see examples above; cheap and
  transparent.
- **Repeated** — load all 28 per-year TSVs into DuckDB / pandas /
  polars. See [`integrate-with-python.md`](./integrate-with-python.md).
