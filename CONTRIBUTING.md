# Contributing

This page covers the developer side of the x-cmd/cve pipeline —
how the data is generated, how the TSV is laid out on disk, and
how to run the scripts locally.

**Looking to use the data?** See
[`README.md`](./README.md) for the user-facing tables + the
companion [`SKILL.md`](./SKILL.md) for `x cve` recipes and raw
TSV downloads.

## Repository layout

```text
.
├── .x-cmd/
│   ├── tsv.py              # full rebuild from a local cvelistV5 clone
│   ├── cwe.py              # MITRE CWE catalog mirror → data/cwe.tsv + .slim.tsv
│   ├── cwe_zh.py           # MITRE Chinese mirror (cwe.org.cn) → data/cwe.zh.tsv (issue #2)
│   ├── cwe_report.py       # aggregate data/cve-*.tsv ∩ data/cwe.slim.tsv (+ .zh.tsv) → report/cwe.report.{tsv,md,zh.md}
│   ├── report.py           # per-year stats → report/cve.report.{tsv,md}
│   ├── latest.py           # newest-N CVEs → report/cve.latest-N.report.{tsv,md}
│   └── _cve_index.py       # shared parse / IO helpers
├── data/                   # regenerated on every CI run — NOT in git
│   ├── cve-YYYY.tsv        # one TSV per year (rows in DESCENDING cve-id order)
│   ├── index.tsv           # year \t rows \t file
│   └── cve.tsv.state.json  # per-file mtimes (for tsv.py incremental)
└── report/                 # regenerated on every CI run — committed to main
    ├── README.md                              # docks the files + methodology
    ├── cve.report.{tsv,md}                    # per-year stats
    ├── cve.latest-10.report.{tsv,md}          # newest 10 CVEs (front-of-page table)
    ├── cwe.top100.by-cve-count.report.tsv     # all years, by count
    ├── cwe.top100.by-cve-score.report.tsv     # all years, by score
    ├── cwe.top100.by-cve-count.since-2024.report.tsv   # since 2024, by count
    ├── cwe.top100.by-cve-score.since-2024.report.tsv   # since 2024, by score
    ├── cwe.report.md                          # English, since 2024, top-10 markdown
    └── cwe.report.zh.md                       # Chinese, since 2024, top-10 markdown
├── README.cn.md            # Chinese version of README.md (auto-updated)
└── .github/workflows/
    └── release.yml         # every 4h: tsv.py --rebuild → reports → xz → upload
```

`data/` is regenerated from scratch on every CI run, so the working
tree on `main` stays small.

## Row order — newest first

Every `cve-YYYY.tsv` is written with rows in **descending cve-id order**:

```text
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

# Fetch MITRE Chinese mirror (cwe.org.cn) → data/cwe.zh.tsv.
# 30-day local cache; on missing data the Chinese README falls
# back to English names (issue #2).
python3 .x-cmd/cwe_zh.py

# Aggregate cross-reference: how many CVEs reference each CWE,
# mean + max score. Reads data/cve-*.tsv + data/cwe.slim.tsv
# + data/cwe.zh.tsv.
python3 .x-cmd/cwe_report.py

# Newest-N CVEs (default 10) for the front-of-page table.
# Reads only the head of each per-year TSV.
python3 .x-cmd/latest.py

# Per-year stats → report/cve.report.{tsv,md}.
python3 .x-cmd/report.py
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
