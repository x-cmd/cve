# What CVEs keep teaching us

> _Refreshed daily from upstream cvelistV5 — pull this page tomorrow
> and the rankings will have moved._

<!-- BEGIN cwe.report.md -->

_101,529 CVEs across 666 distinct CWEs since 2024._

### What mistake do engineers keep making most often since 2024?

_Top 10 CWE by CVE count._

| Rank | CWE | Name | CVEs | Avg score |
| ---: | :-: | :--- | ---: | ---:      |
| 1 | [79](https://cwe.mitre.org/data/definitions/79.html) | Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') | 16,072 | 6.15 |
| 2 | [89](https://cwe.mitre.org/data/definitions/89.html) | Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') | 7,150 | 7.44 |
| 3 | [862](https://cwe.mitre.org/data/definitions/862.html) | Missing Authorization | 5,484 | 5.86 |
| 4 | [74](https://cwe.mitre.org/data/definitions/74.html) | Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') | 3,987 | 7.01 |
| 5 | [352](https://cwe.mitre.org/data/definitions/352.html) | Cross-Site Request Forgery (CSRF) | 3,113 | 5.78 |
| 6 | [22](https://cwe.mitre.org/data/definitions/22.html) | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | 2,746 | 7.18 |
| 7 | [94](https://cwe.mitre.org/data/definitions/94.html) | Improper Control of Generation of Code ('Code Injection') | 2,462 | 6.64 |
| 8 | [78](https://cwe.mitre.org/data/definitions/78.html) | Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') | 2,086 | 8.03 |
| 9 | [416](https://cwe.mitre.org/data/definitions/416.html) | Use After Free | 2,042 | 7.65 |
| 10 | [20](https://cwe.mitre.org/data/definitions/20.html) | Improper Input Validation | 1,954 | 6.98 |

### When that mistake is made, how bad is it since 2024?

_Top 10 CWE by average CVSS score. Min 10 CVEs to suppress single-CWE outliers._

| Rank | CWE | Name | CVEs | Avg score | Max |
| ---: | :-: | :--- | ---: | ---:      | ---: |
| 1 | [506](https://cwe.mitre.org/data/definitions/506.html) | Embedded Malicious Code | 35 | 8.98 | 10.0 |
| 2 | [95](https://cwe.mitre.org/data/definitions/95.html) | Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') | 98 | 8.44 | 10.0 |
| 3 | [288](https://cwe.mitre.org/data/definitions/288.html) | Authentication Bypass Using an Alternate Path or Channel | 408 | 8.31 | 10.0 |
| 4 | [502](https://cwe.mitre.org/data/definitions/502.html) | Deserialization of Untrusted Data | 1,540 | 8.30 | 10.0 |
| 5 | [565](https://cwe.mitre.org/data/definitions/565.html) | Reliance on Cookies without Validation and Integrity Checking | 16 | 8.29 | 9.8 |
| 6 | [917](https://cwe.mitre.org/data/definitions/917.html) | Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') | 29 | 8.21 | 10.0 |
| 7 | [470](https://cwe.mitre.org/data/definitions/470.html) | Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection') | 43 | 8.20 | 10.0 |
| 8 | [29](https://cwe.mitre.org/data/definitions/29.html) | Path Traversal: '..filename' | 48 | 8.15 | 9.9 |
| 9 | [120](https://cwe.mitre.org/data/definitions/120.html) | Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') | 1,049 | 8.13 | 10.0 |
| 10 | [121](https://cwe.mitre.org/data/definitions/121.html) | Stack-based Buffer Overflow | 1,609 | 8.12 | 10.0 |
<!-- END cwe.report.md -->

<!-- BEGIN cve.report.md -->

## How fast is CVE growing?

_Per-year CVE volume and severity._

| Year | CVEs | Scored | Avg score | Max score |
| ---: | ---: | ---:   | ---:      | ---:      |
| 2026 _(YTD as of 2026-07-24)_ | 36,410 | 34,654 | 7.02 | 10.0 |
| 2025 | 43,224 | 40,852 | 6.76 | 10.0 |
| 2024 | 38,425 | 36,189 | 6.77 | 10.0 |
| 2023 | 30,602 | 24,345 | 6.71 | 10.0 |
| 2022 | 26,425 | 17,111 | 6.76 | 10.0 |
| 2021 | 22,587 | 10,644 | 6.81 | 10.0 |
| 2020 | 19,386 | 6,817 | 6.83 | 10.0 |
| 2019 | 16,093 | 3,522 | 6.83 | 10.0 |
| 2018 | 16,188 | 2,291 | 6.92 | 10.0 |
| 2017 | 14,760 | 1,373 | 7.18 | 10.0 |
| 2016 | 9,366 | 407 | 7.10 | 10.0 |
| 2015 | 8,111 | 250 | 6.25 | 10.0 |
| 2014 | 8,427 | 290 | 6.62 | 10.0 |
| 2013 | 6,221 | 153 | 7.44 | 10.0 |
| 2012 | 5,488 | 147 | 7.82 | 10.0 |
| 2011 | 4,646 | 96 | 7.54 | 10.0 |
| 2010 | 5,074 | 95 | 7.74 | 10.0 |
| 2009 | 4,921 | 65 | 8.01 | 10.0 |
| 2008 | 7,005 | 41 | 7.31 | 9.8 |
| 2007 | 6,458 | 38 | 8.00 | 9.8 |
| 2006 | 6,995 | 42 | 7.94 | 9.8 |
| 2005 | 4,627 | 21 | 6.23 | 9.8 |
| 2004 | 2,644 | 11 | 7.33 | 9.8 |
| 2003 | 1,504 | 6 | 5.73 | 7.5 |
| 2002 | 2,357 | 11 | 7.43 | 9.8 |
| 2001 | 1,537 | 5 | 7.54 | 9.8 |
| 2000 | 1,236 | 0 | — | 0.0 |
| 1999 | 1,540 | 24 | 7.62 | 9.8 |
| **Total** | **352,257** | **179,500** | **6.82** | **10.0** |
<!-- END cve.report.md -->

## Reports

The two tables above are sliced from the seven derived reports in
[`report/`](./report/) (sibling of `data/`) — see
[`report/README.md`](./report/README.md) for methodology, the SINCE_DATE
cutoff, and how the top-10 markdown is sliced from the top-100 TSV.

### Per-year CVE stats

| File | Format | Window |
| ---  | ---    | ---    |
| [`report/cve.report.md`](./report/cve.report.md)   | Markdown table | all years |
| [`report/cve.report.tsv`](./report/cve.report.tsv) | TSV            | all years |

### CWE rankings — top 100 TSVs (one per axis × window)

| File | Axis | Window |
| ---  | ---  | ---    |
| [`report/cwe.top100.by-cve-count.report.tsv`](./report/cwe.top100.by-cve-count.report.tsv)               | CVE count  | all years |
| [`report/cwe.top100.by-cve-score.report.tsv`](./report/cwe.top100.by-cve-score.report.tsv)               | avg score  | all years |
| [`report/cwe.top100.by-cve-count.since-2024.report.tsv`](./report/cwe.top100.by-cve-count.since-2024.report.tsv) | CVE count  | since 2024 |
| [`report/cwe.top100.by-cve-score.since-2024.report.tsv`](./report/cwe.top100.by-cve-score.since-2024.report.tsv) | avg score  | since 2024 |

### CWE rankings — markdown (top 10 per axis, since 2024)

| File | Format |
| ---  | ---    |
| [`report/cwe.report.md`](./report/cwe.report.md) | Markdown, two top-10 tables — the top-10 markdown is sliced from the two since-2024 TSVs above |

## About x-cmd/cve

This repo is the **producer**: it reads
[`CVEProject/cvelistV5`](https://github.com/CVEProject/cvelistV5),
extracts a slim 9-column TSV per year, xz-compresses it, and publishes
the artifacts as [GitHub Release assets](https://github.com/x-cmd/cve/releases/tag/data)
(`https://github.com/x-cmd/cve/releases/download/data/<name>.xz`).
The consumer is the [`x cve`](https://x-cmd.com/mod/cve) shell module,
which downloads on demand and never touches the upstream tree at runtime.
Companion module [`x cwe`](https://x-cmd.com/mod/cwe) browses the CWE
catalog.

### How users get CVE data (the 4 commands)

```sh
# 1. Browse — list / fzf over every cached CVE, newest first.
x cve
x cve fz

# 2. Look up a single CVE by id (or YYYY-NNNN shorthand).
x cve info CVE-2024-0001
x cve info 2024-0001            # same thing, no prefix needed

# 3. Pull the FULL upstream JSON record from CVEProject/cvelistV5:
#    affected products, references, timeline, ADP containers, etc.
x cve detail CVE-2024-0001

# 4. Enrich with Shodan's CVE database — EPSS, KEV listing,
#    exploit writeups, vendor advisories aggregated into one record:
x shodan cve CVE-2024-0001
#    (https://x-cmd.com/mod/shodan/cve)
```

`x cve` and `x shodan cve` chain cleanly:

```sh
x cve fz | x shodan cve -      # preview every CVE in shodan
x shodan cve CVE-2024-0001     # equivalent, no pipe needed
```

No API keys, no sudo, no background services — `x cve` is a thin
shell module backed by the per-year TSVs this repo publishes daily.

## Repository layout

```
.
├── .x-cmd/
│   ├── tsv.py              # full rebuild from a local cvelistV5 clone
│   ├── cwe.py              # MITRE CWE catalog mirror → data/cwe.tsv + .slim.tsv
│   ├── cwe_report.py       # aggregate data/cve-*.tsv ∩ data/cwe.slim.tsv → report/cwe.report.{tsv,md}
│   ├── report.py           # per-year stats → report/cve.report.{tsv,md}
│   └── _cve_index.py       # shared parse / IO helpers
├── data/                   # regenerated on every CI run — NOT in git
│   ├── cve-YYYY.tsv        # one TSV per year (rows in DESCENDING cve-id order)
│   ├── index.tsv           # year \t rows \t file
│   └── cve.tsv.state.json  # per-file mtimes (for tsv.py incremental)
└── report/                 # regenerated on every CI run — committed to main
    ├── README.md           # docks the seven files + methodology
    ├── cve.report.{tsv,md} # per-year stats
    ├── cwe.top100.by-cve-count.report.tsv               # all years, by count
    ├── cwe.top100.by-cve-score.report.tsv               # all years, by score
    ├── cwe.top100.by-cve-count.since-2024.report.tsv   # since 2024, by count
    ├── cwe.top100.by-cve-score.since-2024.report.tsv   # since 2024, by score
    └── cwe.report.md       # since 2024, top-10 markdown (sliced from the TSVs)
├── README.cn.md            # Chinese version of README.md (auto-updated)
└── .github/workflows/
    └── release.yml         # every 4h: tsv.py --rebuild → reports → xz → upload
```

`data/` is regenerated from scratch on every CI run, so the working
tree on `main` stays small.

## Row order — newest first

Every `cve-YYYY.tsv` is written with rows in **descending cve-id order**:

```
CVE-2026-99999
CVE-2026-99998
CVE-2026-99997
...
CVE-2026-00002
CVE-2026-00001
CVE-2025-99999
...
CVE-1999-00001
```

The `x cve` consumer walks year files in reverse (`ls -r`) and each
file is already in reverse order, so a plain `cat` produces
"newest CVE at the top of the stream". No `tac`, no second pass over
the data, no surprises.

Why store in reverse? `x cve ls` and `x cve fz` users care about
*latest* CVEs first — the freshly issued ones, today's score-bombs.
The producer's `save_year_files` sorts each bucket with
`sort(reverse=True)` so the on-disk order matches the display order.

## TSV columns (9)

| # | Column   | Meaning                                                                       |
| - | -------- | ----------------------------------------------------------------------------- |
| 1 | `cve`    | Full CVE id, e.g. `CVE-2024-0001`.                                            |
| 2 | `year`   | Year segment parsed from the id.                                              |
| 3 | `no`     | Numeric segment parsed from the id.                                           |
| 4 | `vp`     | `<vendor>/<product>;...` from `containers.cna.affected[]`, `;`-joined.       |
| 5 | `ghsa`   | GitHub Security Advisory id(s) in `references`, `;`-joined. Empty if absent.  |
| 6 | `score`  | Highest CVSS base score (v4.0 → v3.1 → v3.0 → v2.0, first hit wins).           |
| 7 | `patched`| `1` if `containers.cna.solutions[]` is non-empty, else `0`.                   |
| 8 | `cwe`    | CWE number(s) (prefix-stripped) joined with `;`. Empty if absent.             |
| 9 | `desc`   | English description, first sentence only (≤240 chars).                        |

Field 9 is truncated to the first sentence — Linux CNA routinely
pastes full kernel slab dumps (kilobytes of `fp=0x...` hex) into the
description field. Truncating keeps per-year files at ~1-9 MB each
and makes `x cve fz` lists scannable.

## Scripts

All scripts are dependency-free (Python 3.8+ stdlib). Run from the
repo root:

```sh
# Full rebuild from a local cvelistV5 clone (~2 minutes for ~350k records)
python3 .x-cmd/tsv.py

# Force re-parse every file (ignore mtime state)
python3 .x-cmd/tsv.py --rebuild

# Fetch MITRE CWE catalog → data/cwe.tsv (full 21 columns) +
# data/cwe.slim.tsv (id+name only, used for joins).
python3 .x-cmd/cwe.py

# Aggregate cross-reference: how many CVEs reference each CWE,
# mean + max score. Reads data/cve-*.tsv + data/cwe.slim.tsv.
python3 .x-cmd/cwe_report.py
```

### CWE data — what we publish vs what we derive

The four `report/cwe.*.report.tsv` files are listed in the
[Reports](#reports) section above. Below are the two upstream CWE
catalog files this repo derives from MITRE:

| File | Shape | Source | Purpose |
| ---  | ---   | ---    | ---     |
| `data/cwe.tsv`        | 21-column TSV (~3 MB), all MITRE fields | Verbatim mirror of MITRE 2000.csv | x-cwe module + any consumer that wants the full CWE catalog without hitting MITRE directly |
| `data/cwe.slim.tsv`   | 2-column TSV (~50 KB), `CWE-ID` + `Name` only | Derived from `data/cwe.tsv` | Joined against `data/cve-*.tsv` for cwe_report.py |



| File | Shape | Source | Purpose |
| ---  | ---   | ---    | ---     |
| `data/cwe.tsv`        | 21-column TSV (~3 MB), all MITRE fields preserved | Verbatim mirror of MITRE 2000.csv (header row, spaces in column names replaced with `_`) | x-cwe module and any consumer that wants the full CWE catalog without hitting MITRE directly |
| `data/cwe.slim.tsv`   | 2-column TSV (~50 KB), `CWE-ID\tName` only        | Derived from `data/cwe.tsv` (same row order) | Joined against `data/cve-*.tsv` for cwe_report.py |
| `report/cwe.top100.by-cve-count.report.tsv`              | 5-column TSV (~6 KB), top 100 by CVE count, all years | Aggregated from `data/cve-*.tsv` ∩ `data/cwe.slim.tsv` | Machine-readable top-N ranking |
| `report/cwe.top100.by-cve-score.report.tsv`              | 5-column TSV (~6 KB), top 100 by avg CVSS, all years | same | same |
| `report/cwe.top100.by-cve-count.since-2024.report.tsv`  | 5-column TSV (~6 KB), top 100 by CVE count, since 2024 | same, year >= 2024 | same |
| `report/cwe.top100.by-cve-score.since-2024.report.tsv`  | 5-column TSV (~6 KB), top 100 by avg CVSS, since 2024 | same, year >= 2024 | same |
| `report/cwe.report.md`  | Markdown with two top-10 tables (since 2024) | Sliced from the two since-2024 TSVs | Stitches into the README + README.cn front-matter via release.yml's inline step |

**Why we mirror the catalog**: the upstream MITRE 2000.csv.zip is
644 KB and the unzipped csv is ~3 MB. xz-compressed to ~150 KB.
We can afford to ship a full mirror, and it gives offline consumers
the same data they'd get from MITRE without the network hop. The
TSV keeps MITRE's column names (only spaces → underscores) so
downstream code can use either format.

**Why we don't ship a copy of the per-CVE catalog as a release
asset today**: the x-cwe module currently fetches 2000.csv from
MITRE on its own and caches it locally (`~/.x-cmd.root/local/data/cwe/`).
A future version of x-cwe could optionally read `data/cwe.tsv` from
this repo's release instead, but that's not wired up yet.

## CI

`.github/workflows/release.yml` runs every 4 hours (37 minutes past
the hour, off-the-hour to spread load), plus on manual dispatch.
Each run:

1. Clones CVEProject/cvelistV5 (depth 1) and runs
   `.x-cmd/tsv.py --rebuild` to refresh `data/cve-*.tsv`.
2. Regenerates `data/cwe.tsv` + `data/cwe.slim.tsv` from MITRE
   (`.x-cmd/cwe.py`) and the CWE cross-reference report
   (`.x-cmd/cwe_report.py` → `report/cwe.report.{tsv,md}`).
3. Regenerates the year-stats report (`.x-cmd/report.py` →
   `report/cve.report.{tsv,md}`).
4. Inlines both report markdown files into `README.md` as the first
   section (idempotent — BEGIN/END markers round-trip), then commits
   `README.md` + the four `*.report.{md,tsv}` back to `main` (skip if
   nothing changed), so the README on github.com always tracks the
   latest data.
5. xz-compresses each changed per-year file (`xz -9`, ~85% reduction),
   replaces the matching release asset, force-moves the
   `data-packaged` git tag so the next run's diff is correct.

No `.xz` files are committed to `main` — binaries live in release
assets, not source. The per-year `data/cve-*.tsv` and the CWE catalog
(`data/cwe.tsv`, `data/cwe.slim.tsv`) likewise stay out of git under
this flow; only the derived reports and the README are committed back,
keeping the git history focused on real code changes.

The workflow used to have a separate `delta-update` workflow that ran
on the same 4-hour cadence and produced an incremental `data/cve.tsv`;
its output was overwritten by step 1's full rebuild every time
release.yml followed via `workflow_run`, so the incremental work was
dead weight. See [issue #1](https://github.com/x-cmd/cve/issues/1)
for the numbers.

## License

Apache License 2.0 — see [`LICENSE`](./LICENSE).

The underlying CVE records are derived from
[CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5),
which is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Downstream consumers of these TSVs must retain that attribution.

## Related

- [x-cmd/cve module docs](https://x-cmd.com/mod/cve) — consumer (shell)
- [x-cmd/cwe module docs](https://x-cmd.com/mod/cwe) — companion module
- [x-cmd/x-cmd](https://github.com/x-cmd/x-cmd) — module source (`mod/cve/`)
- [CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5) — upstream data