# x-cmd/cve docs

Daily-updated CVE / CWE index — schema, recipes, and reference for
every published vulnerability since CVE-1999-0001.

## Quick navigation

### [start/](./start/) — get going in 60 seconds
- [quickstart.md](./start/quickstart.md) — `curl` a year of CVEs in one line
- [x-cve-shell.md](./start/x-cve-shell.md) — `x cve` shell module recipes
- [data-freshness.md](./start/data-freshness.md) — when does a new CVE show up

### [guides/](./guides/) — task-shaped recipes
- [lookup-one-cve.md](./guides/lookup-one-cve.md) — by id (NVD, x cve, raw TSV)
- [bulk-query-by-cwe.md](./guides/bulk-query-by-cwe.md) — every CVE referencing a CWE
- [integrate-with-python.md](./guides/integrate-with-python.md) — DuckDB / pandas / polars
- [cve-vs-cwe-vs-cpe.md](./guides/cve-vs-cwe-vs-cpe.md) — picking the right id

### [reference/](./reference/) — schema and metadata
- [tsv-schema.md](./reference/tsv-schema.md) — the 9 columns of `cve-YYYY.tsv`
- [cwe-catalog.md](./reference/cwe-catalog.md) — the CWE catalog mirror + Chinese names
- [release-assets.md](./reference/release-assets.md) — every `.xz` asset and its size
- [contributing.md](./reference/contributing.md) — for developers adding to this repo

## What this repo is

A daily-updated mirror of [CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5)
plus the [MITRE CWE catalog](https://cwe.mitre.org/), published as
plain xz-compressed TSVs on the
[`data`](https://github.com/x-cmd/cve/releases/tag/data) GitHub
release. Used by the [`x cve`](https://x-cmd.com/mod/cve) shell
module and anyone who wants offline CVE data.

## Related

- [SKILL.md](../SKILL.md) — AI-facing how-to (schema + recipes in one file)
- [CONTRIBUTING.md](../CONTRIBUTING.md) — developer-facing pipeline docs
- [README.md](../README.md) — the public-facing front of the repo
