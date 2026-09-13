# Lookup one CVE by id

Three ways — pick whichever fits your context.

## 1. `x cve info` (recommended)

```sh
x cve info CVE-2024-0001
x cve info 2024-0001        # YYYY-NNNN shorthand
x cve detail CVE-2024-0001   # full upstream JSON
```

`x cve info` shows the human-readable summary (vendor, score, CWE,
patched?). `x cve detail` shows the full `cvelistV5` JSON record
(affected products, references, timeline, ADP containers).

`x cve` reads the per-year TSVs from this repo's release assets,
so it works air-gapped once you've fetched the assets at least
once.

## 2. NVD (NIST) — canonical source

For one record by id, the upstream authority is the
[NVD detail page](https://nvd.nist.gov/vuln/detail/CVE-2024-0001).

API equivalent:

```sh
curl -fsSL "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-0001" | jq .
```

## 3. Raw TSV — when scripting

```sh
# Pull just the row for CVE-2024-0001 from the year-2024 file
xz -dc <(curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-2024.tsv.xz) \
  | awk -F'\t' '$1 == "CVE-2024-0001"'
```

Output is the 9-column row documented in
[`../reference/tsv-schema.md`](../reference/tsv-schema.md). The
`desc` field is truncated to the first sentence (≤ 240 chars); use
`x cve detail` or NVD for the full description.

## Cross-referencing back to CWE

The 8th column (`cwe`) holds a `;`-joined list of CWE ids with the
`CWE-` prefix stripped. To expand to CWE names:

```sh
xz -dc <(curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-2024.tsv.xz) \
  | awk -F'\t' '$1 == "CVE-2024-0001" {
      split($8, cwes, ";")
      for (i in cwes) {
        name = (lookup[cwes[i]] ? lookup[cwes[i]] : "lookup " cwes[i] ".html")
        print "CWE-" cwes[i] ": " name
      }
    }'
```

(`lookup[]` would be filled from `cwe.slim.tsv`; this is left as
an exercise for your scripting language of choice — see
[`integrate-with-python.md`](./integrate-with-python.md) for the
Python version.)

## When the CVE id doesn't exist yet

If the id you searched for returns nothing, three possibilities:

1. **Just-published** — wait up to 4 hours for the next CI run.
2. **Reserved, not assigned** — MITRE reserves `CVE-YYYY-NNNN`
   blocks but doesn't always publish records. Check
   [cve.org](https://cve.org/) for the official status.
3. **Withdrawn** — MITRE occasionally withdraws records; in that
   case the cve-* dir in `cvelistV5` simply doesn't contain a
   matching JSON file.

## Next steps

- [`bulk-query-by-cwe.md`](./bulk-query-by-cwe.md) — every CVE referencing a CWE
- [`integrate-with-python.md`](./integrate-with-python.md) — DuckDB / pandas joins
- [`../reference/cwe-catalog.md`](../reference/cwe-catalog.md) — the CWE catalog mirror
