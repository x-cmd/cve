# Contributing

For developers adding to this repo — repo layout, scripts, CI
pipeline. See [`../../../CONTRIBUTING.md`](../../CONTRIBUTING.md)
for the canonical reference (this file mirrors the same content
under the `doc/` tree so it appears in the rendered site alongside
the other reference pages).

If you're looking for **how to use the data** instead, see
[`../start/quickstart.md`](../start/quickstart.md) or
[`../../../SKILL.md`](../../SKILL.md).

## Layout

```
.
├── .x-cmd/             # pipeline scripts (Python 3.8+ stdlib)
│   ├── tsv.py          # rebuild per-year CVE TSVs from cvelistV5
│   ├── cwe.py          # MITRE CWE catalog → data/cwe.tsv + .slim.tsv
│   ├── cwe_zh.py       # MITRE Chinese mirror → data/cwe.zh.tsv
│   ├── cwe_report.py   # Top-N CWE rankings → report/cwe.report.{tsv,md,zh.md}
│   ├── latest.py       # Newest-N CVEs → report/cve.latest-N.report.{tsv,md}
│   ├── report.py       # Per-year stats → report/cve.report.{tsv,md}
│   └── _cve_index.py   # shared parse / IO helpers
├── data/               # regenerated every CI run — NOT in git
├── report/             # regenerated every CI run — committed to main
├── doc/                # this directory; rendered on x-cmd.com
├── SKILL.md            # AI-facing data-usage reference
├── CONTRIBUTING.md     # developer-facing pipeline reference (mirror)
└── .github/workflows/release.yml
```

## Running the scripts locally

```sh
# Full rebuild from a local cvelistV5 clone
python3 .x-cmd/tsv.py --src /path/to/cvelistV5/cves --out data --rebuild

# Regenerate just the CWE catalog
python3 .x-cmd/cwe.py

# Regenerate Chinese CWE names (30-day cache)
python3 .x-cmd/cwe_zh.py

# Top-N CWE rankings + front-page markdown
python3 .x-cmd/cwe_report.py

# Newest-N CVEs for the front-page table
python3 .x-cmd/latest.py

# Per-year stats
python3 .x-cmd/report.py
```

All six are dependency-free (Python 3.8+ stdlib). `tsv.py` is the
only one that needs a network clone of `cvelistV5`; the rest read
from `data/`.

## CI

`.github/workflows/release.yml` runs every 4 hours at
`37 */4 * * *` UTC plus on every push to `main`. Each run:

1. Clones `CVEProject/cvelistV5` (depth 1) and runs `tsv.py --rebuild`.
2. Regenerates `data/cwe.{tsv,slim.tsv,zh.tsv}`.
3. Regenerates `report/cwe.report.{tsv,md,zh.md}`.
4. Regenerates `report/cve.latest-10.report.{tsv,md}`.
5. Regenerates `report/cve.report.{tsv,md}`.
6. Stitches both markdowns into `README.md` and `README.cn.md`
   (BEGIN/END markers, idempotent).
7. Commits data + reports + READMEs back to `main`.
8. xz-compresses any changed `data/*.tsv` and uploads to the
   `data` GitHub release (step 2-3 of release.yml's diff-driven
   upload).

## When opening a PR

- Bug in the pipeline? Open an issue at
  <https://github.com/x-cmd/cve/issues>.
- Missing / wrong CVE record? File at
  <https://github.com/CVEProject/cvelistV5> (we don't author CVE data).
- Wrong Chinese CWE name? File at <https://cwe.org.cn> (we mirror
  from there). Or run `python3 .x-cmd/cwe_zh.py --force` locally
  to re-fetch after an upstream fix.
