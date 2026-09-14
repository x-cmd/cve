---
x-title: 怎么使用数据
x-desc: 三种消费 CVE / CWE 数据的方式 —— curl + xz 用原始 TSV、x cve shell 模块、DuckDB / pandas。
x-sidebar: 怎么使用数据
x-keywords: CVE, CWE, AI 安全, 漏洞情报
x-json-ld:
  '@context': https://schema.org
  '@graph':
    - '@type': TechArticle
      headline: '如何使用这些数据'
      inLanguage: 'zh-Hans'
      about: '数据消费'
---
三种消费 CVE / CWE 数据的方式，按集成成本递增排列。


# Using the data

Three ways to consume the CVE / CWE data, in increasing order of
integration cost.

## 1. Raw TSVs (`curl` + `xz`)

Data lives at
[github.com/x-cmd/cve/releases/tag/data](https://github.com/x-cmd/cve/releases/tag/data)
as plain xz-compressed TSVs. No install, no shell module, no
API key.

```sh
# One year of CVEs (~5 MB xz)
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz \
  | xz -dc > cve-2026.tsv

# Whole catalog (~21 MB xz)
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-all.tar.xz \
  | tar -xJ

# Just the CWE catalog (~150 KB xz)
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cwe.tsv.xz \
  | xz -dc > cwe.tsv
```

The 9 columns of `cve-YYYY.tsv` are documented in
[`3-latest-cves-explained`](./3-latest-cves-explained.en.md). A
worked example:

```sh
# Top 10 CVEs by score in 2026
awk -F'\t' '$6!=""' cve-2026.tsv \
  | sort -t$'\t' -k6,6nr \
  | head -10 \
  | cut -f1,4,6
```

## 2. `x cve` shell module

[`x cve`](https://x-cmd.com/mod/cve) wraps the TSVs and exposes
a small CLI for one-record lookups. Install
[x-cmd](https://x-cmd.com/install), then:

```sh
x cve                          # list all CVEs (newest first)
x cve fz                       # fzf picker
x cve info CVE-2024-0001        # one record by id (YYYY-NNNN shorthand works too)
x cve detail CVE-2024-0001      # full upstream JSON from CVEProject/cvelistV5
x shodan cve CVE-2024-0001      # EPSS + KEV + exploit-writeups enrichment
x cwe ls                        # every CWE in the catalog
x cwe 79                        # one CWE's full description
```

`x cve` reads the per-year TSVs from this repo's release assets,
so it works air-gapped once the assets have been fetched.

## 3. Python — DuckDB / pandas / polars

The TSVs are plain text; all three read them directly.

### DuckDB (recommended for SQL-style queries)

```python
import duckdb
con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs;")

# One year via HTTP
df = con.execute("""
  SELECT * FROM read_csv(
    'https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz',
    delim='\t', header=true, compression='gzip'
  )
""").df()
```

DuckDB's `union_all_by_name` joins all 28 per-year files into one
logical table:

```python
years = list(range(2024, 2027))
tables = [
    f"read_csv('https://github.com/x-cmd/cve/releases/download/data/cve-{y}.tsv.xz', delim='\\t', header=true, compression='gzip')"
    for y in years
]
df_all = con.execute(" UNION ALL ".join(tables)).df()

# Every XSS CVE scored >= 7 since 2024
xss = df_all.filter(
    (df_all["cwe"].fillna("").str.contains(r"(^|;)79(;|$)")) &
    (df_all["score"].astype(float) >= 7)
).sort("score", descending=True)
```

### pandas

```python
import pandas as pd
df = pd.read_csv("cve-2026.tsv", sep="\t", dtype=str, keep_default_na=False)
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["patched"] = df["patched"].astype(int)

# Top vendors for CWE-79 (XSS) since 2024
mask = df["cwe"].str.contains(r"(^|;)79(;|$)", regex=True, na=False)
vendors = (
    df[mask].assign(v=df["vp"].str.split(";"))
            .explode("v")["v"]
            .value_counts()
            .head(20)
)
```

### polars

```python
import polars as pl
df = pl.read_csv("cve-2026.tsv", separator="\t", infer_schema_length=10000)
xss = df.filter(
    pl.col("cwe").str.contains(r"(^|;)79(;|$)"),
    pl.col("score").cast(pl.Float64, strict=False) >= 7,
).sort("score", descending=True)
```

## When to pick which

- **One record, browsing, Shodan enrichment** → `x cve` (option 2).
- **Bulk analytics, joins into Python/R/DuckDB, scripted ETL** →
  raw TSV (option 1 or 3).

The raw TSVs are the same data either way — `x cve` is just a
small convenience layer on top.

## What's next

- The schema reference: [`3-latest-cves-explained`](./3-latest-cves-explained.en.md).
- The CWE join + ranking logic: [`4-top-cwes-explained`](./4-top-cwes-explained.en.md).
- How the data is built: [`2-how-data-is-built`](./2-how-data-is-built.en.md).
- [README.md](../../README.md) for the live tables.
