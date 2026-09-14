---
name: 6-using-the-data
description: Three ways to consume the CVE / CWE data — curl + xz on raw TSVs, x cve shell module, DuckDB / pandas / polars.
type: how-to
---

# Core Content

core_features:

- Raw TSV: curl <https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz> | xz -dc > cve-2026.tsv
- Whole catalog: curl ... cve-all.tar.xz | tar -xJ (~21 MB xz).
- x cve shell module: x cve, x cve fz, x cve info CVE-YYYY-NNNN, x cve detail, x shodan cve.
- DuckDB: read_csv('<https://...cve-2026.tsv.xz>', delim='\t', header=true, compression='gzip').
- pandas: pd.read_csv('cve-2026.tsv', sep='\t', dtype=str, keep_default_na=False).
- polars: pl.read_csv('cve-2026.tsv', separator='\t', infer_schema_length=10000).
- Pattern: when you need to filter by CWE, use regex (^|;)79(;|$) to avoid matching 179, 779, etc.

## Key Information

highlights:

- x cve reads the per-year TSVs; works air-gapped after first fetch.
- DuckDB is fastest for ad-hoc SQL on full set (~2-3 s cold).
- x cve and DuckDB read the SAME per-year TSVs.

## Use Cases

use_cases:

- Audit your stack against known CVEs.
- Build bulk analytics across all 370k rows.
- Integrate CVE data into a Python / R / DuckDB pipeline.

## Related Resources

official:
  website: <https://x-cmd.com/cve/>

## Summary

Concrete recipes for consuming the data — three paths from cheap to integrated: curl + awk on raw TSVs, x cve shell module for one-record lookups, DuckDB / pandas / polars for bulk analytics. Pattern for joining CVE rows against CWE names and filtering by CWE id.
