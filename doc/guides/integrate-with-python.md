# Integrate with Python (DuckDB / pandas / polars)

The TSVs are plain text — DuckDB, pandas, polars all read them
directly without preprocessing.

## DuckDB (recommended for SQL-style queries)

DuckDB treats `read_csv` with `.tsv` extension as native TSV
input. Point it at the xz-compressed asset via `read_csv` over
HTTP:

```python
import duckdb

con = duckdb.connect()
con.execute("""
  INSTALL httpfs; LOAD httpfs;
""")

# One year
df = con.execute("""
  SELECT * FROM read_csv(
    'https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz',
    delim='\t', header=true, compression='gzip'
  )
""").df()

# Or just local xz via a download
import urllib.request, pathlib
pathlib.Path("cve-2026.tsv").write_bytes(
    urllib.request.urlopen("https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz").read()
)
# Decompress, then:
df = con.execute("SELECT * FROM read_csv('cve-2026.tsv', delim='\t', header=true)").df()
```

Cross-reference against CWE names:

```python
cwe = con.execute("""
  SELECT * FROM read_csv('cwe.slim.tsv', delim='\t', header=true)
""").df()

# CVE rows have cwe column like "79;352"; expand to one row per CWE id
df_exploded = (
  df.assign(cwe_id=df["cwe"].str.split(";"))
    .explode("cwe_id")
    .query("cwe_id != ''")
    .merge(cwe, left_on="cwe_id", right_on="CWE-ID")
)
```

## pandas

```python
import pandas as pd
df = pd.read_csv("cve-2026.tsv", sep="\t", dtype=str, keep_default_na=False)
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["patched"] = df["patched"].astype(int)

# XSS (CWE-79) CVEs scored >= 7
mask = df["cwe"].str.contains(r"(^|;)79(;|$)", regex=True, na=False)
xss_high = df[mask & (df["score"] >= 7)].sort_values("score", ascending=False)
```

## polars

```python
import polars as pl
df = pl.read_csv("cve-2026.tsv", separator="\t", infer_schema_length=10000)
xss = df.filter(
    pl.col("cwe").str.contains(r"(^|;)79(;|$)"),
    pl.col("score").cast(pl.Float64, strict=False) >= 7,
).sort("score", descending=True)
```

## Multiple years, single query

DuckDB's `union_all_by_name` reads multiple per-year files as one
logical table:

```python
years = [2024, 2025, 2026]
tables = [
    f"read_csv('https://github.com/x-cmd/cve/releases/download/data/cve-{y}.tsv.xz', delim='\\t', header=true, compression='gzip')"
    for y in years
]
df_all = con.execute(" UNION ALL ".join(tables)).df()
```

## Performance notes

- 28 per-year xz files, ~21 MB total uncompressed ≈ 200 MB. Fits
  in a modern laptop's RAM comfortably.
- DuckDB is the fastest of the three for ad-hoc SQL on the full
  set (~2-3 s cold, <100 ms warm).
- pandas with `dtype=str` keeps raw fidelity; cast numeric columns
  per-query to avoid silent NaN propagation.

## Next steps

- [`bulk-query-by-cwe.md`](./bulk-query-by-cwe.md) — pure-shell awk recipes
- [`../reference/tsv-schema.md`](../reference/tsv-schema.md) — column meanings
- [`../reference/cwe-catalog.md`](../reference/cwe-catalog.md) — joining against CWE names
