# Quickstart

Get a year of CVEs on your machine in one `curl`.

## Pick a consumption path

Two paths, same data:

| Path | Install | Best for |
|---|---|---|
| **Raw TSV** (`curl` + `xz`) | None — just shell + curl | Bulk analytics, scripting, Python / R / DuckDB |
| **`x cve` shell module** | `x cve` (one command) | One-record lookups, browsing, enrichment |

The rest of this page is the raw-TSV path. For `x cve`, see
[`x-cve-shell.md`](./x-cve-shell.md).

## Download one year of CVEs

```sh
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz \
  | xz -dc > cve-2026.tsv
```

~5 MB xz, ~50 MB raw (56k records in 2026 YTD).

Inspect the first row:

```sh
head -1 cve-2026.tsv | awk -F'\t' '{
  for (i=1; i<=NF; i++) printf "%d  %s\n", i, $i
}'
```

The schema (9 columns, `cve` / `year` / `no` / `vp` / `ghsa` / `score`
/ `patched` / `cwe` / `desc`) is documented in
[`reference/tsv-schema.md`](../reference/tsv-schema.md).

## First useful query

```sh
# Top 10 CVEs by score in 2026
awk -F'\t' 'NR>0 && $6!=""' cve-2026.tsv \
  | sort -t$'\t' -k6,6nr \
  | head -10 \
  | cut -f1,4,6
```

## Download more

```sh
# Whole catalog (~21 MB xz)
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-all.tar.xz \
  | tar -xJ

# Just the CWE catalog (~150 KB xz, ~3 MB raw)
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cwe.tsv.xz \
  | xz -dc > cwe.tsv
```

## What about updates?

The data is regenerated every 4 hours. See
[`data-freshness.md`](./data-freshness.md).

## Next steps

- [`guides/lookup-one-cve.md`](../guides/lookup-one-cve.md) — how to fetch one CVE by id
- [`guides/bulk-query-by-cwe.md`](../guides/bulk-query-by-cwe.md) — every CVE referencing a CWE
- [`reference/tsv-schema.md`](../reference/tsv-schema.md) — full column reference
