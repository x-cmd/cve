# cve

A small public project that maintains a per-year TSV index of
[`CVEProject/cvelistV5`](https://github.com/CVEProject/cvelistV5).

This repo is the **data source**. The consumer is the `x cve` module living
under `x-bash/cve` — it fetches whatever it needs from this repo at runtime
(possibly with a curl-based parallel fetcher of its own). Keep the two roles
separate so the producer stays dependency-free and reproducible.

## Layout

```
.
├── index.tsv                  ← manifest: year\trows\tfile  (smallest possible index)
├── cve-YYYY.tsv               ← one TSV per year, full row including desc
├── cve.tsv.state.json         ← per-file mtimes for tsv.py's incremental path
├── cve.tsv.watermark.json     ← last-consumed fetchTime from deltaLog.json
├── tsv.py                     ← full rebuild (offline, walks a local clone)
├── delta_update.py            ← incremental update (network, deltaLog-driven)
├── _cve_index.py              ← shared parse/IO helpers
└── .github/workflows/delta.yml← runs every 4 hours in CI
```

## TSV columns

`cve-YYYY.tsv` per year, tab-separated, one row per non-rejected CVE record:

| Column | Meaning                                                                                       |
| ------ | --------------------------------------------------------------------------------------------- |
| `cve`  | Full CVE id, e.g. `CVE-2024-0001`.                                                            |
| `year` | Year segment parsed from the id, e.g. `2024`.                                                 |
| `no`   | Numeric segment parsed from the id, e.g. `0001`.                                              |
| `ghsa` | GitHub Security Advisory id(s) found in `references`, `;`-joined when multiple. Empty if none. |
| `score`| Highest CVSS base score across CNA + ADP containers (`cvssV4_0` > `cvssV3_1` > `cvssV3_0` > `cvssV2_0`). Empty if absent. |
| `desc` | English description from the CNA container (newlines/tabs collapsed to spaces). Empty if absent. |

`index.tsv` is just `year\trows\tfile` — a manifest for resource-constrained
clients that want to know what's available before downloading individual
year files.

## Scripts

### `tsv.py` — full rebuild

Walks a local clone of `cvelistV5/cves/` and (re)writes every per-year file
plus the manifest. Incremental: unchanged files are skipped via mtime state.

```sh
python3 tsv.py                            # incremental build
python3 tsv.py --rebuild                  # ignore state, re-parse everything
python3 tsv.py --src /path/to/cves --out /tmp/cve-out
```

### `delta_update.py` — incremental update

Consumes `cves/deltaLog.json` from upstream, fetches each changed CVE JSON
via `https://raw.githubusercontent.com/CVEProject/cvelistV5/main/<path>`, and
updates only the year file(s) that actually changed. Older years stay frozen
on disk, so a delta run touches a few megabytes at most.

Honors `HTTP_PROXY` / `HTTPS_PROXY` environment variables (so a local
forwarder like `http://localhost:2026` "防墙" is automatic). The fetcher uses
`urllib.request` — kept dependency-free and good enough for the producer
side. The consumer (`x cve`) is free to use a curl-based parallel fetcher
with HTTP/2 multiplexing.

```sh
# Online, honors HTTP_PROXY env (e.g. http://localhost:2026):
python3 delta_update.py

# Bypass proxy env vars:
python3 delta_update.py --no-proxy

# Explicit proxy URL:
python3 delta_update.py --proxy http://localhost:2026

# Offline: read deltaLog.json + every CVE JSON from a local clone
python3 delta_update.py \
    --from-local /path/to/cvelistV5/cves/deltaLog.json \
    --local-root /path/to/cvelistV5 \
    --no-proxy

# Backfill / re-apply a date range:
python3 delta_update.py --since 2026-07-01T00:00:00Z

# Just inspect what would change:
python3 delta_update.py --dry-run
```

State files (next to the TSVs):
- `cve.tsv.state.json` — per-file mtimes (used by `tsv.py`)
- `cve.tsv.watermark.json` — `{"fetchTime": "...Z"}` last consumed snapshot

## CI: `.github/workflows/delta.yml`

Runs every 4 hours (`17 */4 * * *`), plus on push and via manual dispatch.
It only commits the year file(s) that actually changed — typical diff size
for a single delta cycle is a few KB to a few MB.

## Keeping it fresh locally

```sh
cd /Users/l/.x-repo/github.com/CVEProject/cvelistV5
git pull --rebase
python3 /Users/l/.x-repo/github.com/x-cmd/cve/tsv.py
```

The full rebuild takes ~2 minutes for the whole tree (~350k records). The
incremental rebuild skips files whose mtime didn't change, so a `git pull`
followed by `python3 tsv.py` typically finishes in a couple of seconds.

## Public

This project is public. The TSVs are an intentional derived snapshot of an
already public dataset, and may be redistributed as-is.