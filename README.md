# x-cmd/cve

A daily-updated, per-year CVE index built on top of
[`CVEProject/cvelistV5`](https://github.com/CVEProject/cvelistV5).

This repo is the **producer**. It reads the upstream CVE JSON tree,
extracts a slim 9-column TSV per calendar year, xz-compresses each
file, and publishes them as GitHub Release assets at the stable URL
`https://github.com/x-cmd/cve/releases/download/data/<name>.xz`.

The consumer is the x-cmd shell module
[`x cve`](https://x-cmd.com/mod/cve) (sourced from
[x-bash/cve](https://github.com/x-bash/cve)). It downloads whatever
it needs, decompresses on the fly with `xz -d`, and never has to talk
to the upstream `cvelistV5` repo at runtime.

A companion module [`x cwe`](https://x-cmd.com/mod/cwe) browses CWE
catalog entries; the `cwe` column in our TSV (column 8, prefix-stripped
numbers like `787`) is what makes cross-module linking possible.

## Repository layout

```
.
├── .x-cmd/
│   ├── tsv.py              # full rebuild from a local cvelistV5 clone
│   ├── delta_update.py     # incremental update (network, deltaLog-driven)
│   └── _cve_index.py       # shared parse / IO helpers
├── data/                   # regenerated on every CI run — NOT in git
│   ├── cve-YYYY.tsv        # one TSV per year (rows in DESCENDING cve-id order)
│   ├── index.tsv           # year \t rows \t file
│   ├── cve.tsv.state.json       # per-file mtimes (for tsv.py incremental)
│   └── cve.tsv.watermark.json   # last-consumed deltaLog fetchTime
└── .github/workflows/
    └── release.yml         # daily 02:37 UTC: run delta_update → xz → upload
```

`data/` is regenerated from scratch on every CI run, so the working
tree on `main` stays small (just the 3 scripts and the workflow).

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

# Incremental update via the upstream deltaLog (network only — fast)
python3 .x-cmd/delta_update.py
python3 .x-cmd/delta_update.py --no-proxy          # ignore HTTP_PROXY env
python3 .x-cmd/delta_update.py --since 2026-07-01  # backfill a date range
python3 .x-cmd/delta_update.py --dry-run           # just show what would change
```

## CI

`.github/workflows/release.yml` runs daily at **02:37 UTC** (off-the-hour
to spread load), and on manual dispatch. Each run:

1. Runs `delta_update.py` to refresh `data/`.
2. Compares the working tree against the `data-packaged` git tag — only
   changed year files + index are repackaged.
3. xz-compresses each changed file (`xz -9`, ~85% size reduction).
4. Deletes the existing release asset and uploads the new `.xz`.
5. Force-moves the `data-packaged` tag to the current commit so the
   next run's diff is correct.

No `.xz` files are committed to `main` — binaries live in release
assets, not source.

## License

Apache License 2.0 — see [`LICENSE`](./LICENSE).

The underlying CVE records are derived from
[CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5),
which is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Downstream consumers of these TSVs must retain that attribution.

## Related

- [x-cmd/cve module docs](https://x-cmd.com/mod/cve) — consumer (shell)
- [x-cmd/cwe module docs](https://x-cmd.com/mod/cwe) — companion module
- [x-bash/cve](https://github.com/x-bash/cve) — consumer source
- [CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5) — upstream data