# CVE Insights for AI Builders

<!-- cve-data-as-of:START -->
**Data as of: 2026-09-13** _(refreshed daily from upstream cvelistV5 — pull this page tomorrow and the rankings will have moved)._
<!-- cve-data-as-of:END -->

> 🌐 **中文版：[README.cn.md](./README.cn.md)** —— same data, Chinese CWE names (MITRE 官方中文翻译, ~91% 覆盖；缺失自动回退英文).
>
> - **[The 10 newest CVEs](#the-10-newest-cves)** — what landed in your stack this week.
> - **[What CVEs keep teaching us](#what-cves-keep-teaching-us)** — top weakness classes since 2024; the same names show up again and again.
> - **[How fast is CVE growing?](#how-fast-is-cve-growing)** — 2026 is on track for ~75k, double 2024's 38k; is your scanner keeping up?
> - **[Reports](#reports)** — the raw TSVs behind the tables above (free, no API key).
> - **[About x-cmd/cve](#about-xcmdcve)** — this repo is the producer, `x cve` is the consumer.
> - **[FAQ](#faq)** — the questions people actually ask.
>
> For end users: [`SKILL.md`](./SKILL.md) (raw TSV recipes). For developers: [`CONTRIBUTING.md`](./CONTRIBUTING.md) (pipeline).
>
> **📑 Contents**
> - [The 10 newest CVEs](#the-10-newest-cves)
> - [What CVEs keep teaching us](#what-cves-keep-teaching-us)
> - [How fast is CVE growing?](#how-fast-is-cve-growing)
> - [Reports](#reports)
> - [About x-cmd/cve](#about-xcmdcve)
> - [Developer docs](#developer-docs)
> - [License](#license)
> - [Related](#related)
> - [FAQ](#faq)
>
> **For end users** — `x cve` recipes, raw TSV downloads: see [`SKILL.md`](./SKILL.md).
> **For developers** — schema, repo layout, scripts, CI pipeline: see [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## The 10 newest CVEs

The 10 newest CVEs published to MITRE — these are the freshest
records on the index. If any of the products below are in your
dependency tree (almost certainly), click through to the NVD page
and check the affected-version range against your pinned versions.

<!-- BEGIN cve.latest-10.report.md -->

**The 10 newest CVEs** (descending CVE id = newest published first).

| CVE | Score | Product | CWE | Description |
| --- | ---:  | ---     | :-: | ---         |
| [CVE-2026-90679](https://nvd.nist.gov/vuln/detail/CVE-2026-90679) | 4.3 | Forgejo/Forgejo | [348](https://cwe.mitre.org/data/definitions/348.html) | Forgejo 13.0.0 through 16.0.4, when "[federation] ENABLED = true" is set, has a… |
| [CVE-2026-90678](https://nvd.nist.gov/vuln/detail/CVE-2026-90678) | 7.5 | HAProxy/HAProxy | [130](https://cwe.mitre.org/data/definitions/130.html) | An issue was discovered in HAProxy 3.3.0 through 3.4.4 and in 3.5-dev1 through… |
| [CVE-2026-90668](https://nvd.nist.gov/vuln/detail/CVE-2026-90668) | 8.7 | UnrealIRCd/UnrealIRCd | [770](https://cwe.mitre.org/data/definitions/770.html) | The webserver in UnrealIRCd 6.0.5 through 6.2.6 before 6.2.7 does not limit the… |
| [CVE-2026-90651](https://nvd.nist.gov/vuln/detail/CVE-2026-90651) | 8.1 | Socket/Socket Firewall | [295](https://cwe.mitre.org/data/definitions/295.html) | Socket Firewall (socketdev/socket-registry-firewall) in registry mode before… |
| [CVE-2026-90648](https://nvd.nist.gov/vuln/detail/CVE-2026-90648) | 7.1 | WebAssembly/wabt | [252](https://cwe.mitre.org/data/definitions/252.html) | wasm2c in WebAssembly wabt through 1.0.41 allows sandbox escape in some… |
| [CVE-2026-90647](https://nvd.nist.gov/vuln/detail/CVE-2026-90647) | 9.1 | Kalkitech/ASE2000 V2 Communication Test Set | [295](https://cwe.mitre.org/data/definitions/295.html) | ASE/Kalkitech ASE2000 V2 Communication Test Set 2.35 through 2.37 on Windows… |
| [CVE-2026-90616](https://nvd.nist.gov/vuln/detail/CVE-2026-90616) | 7.4 | Flatpak/Flatpak | [61](https://cwe.mitre.org/data/definitions/61.html) | In Flatpak before 1.18.1, a malicious sandboxed app can obtain arbitrary read… |
| [CVE-2026-90560](https://nvd.nist.gov/vuln/detail/CVE-2026-90560) | 8.8 | luben/zstd-jni | [125](https://cwe.mitre.org/data/definitions/125.html) | zstd-jni versions 1.2.0 through 1.5.7-13 contain an out-of-bounds read… |
| [CVE-2026-90559](https://nvd.nist.gov/vuln/detail/CVE-2026-90559) | 8.7 | xerial/snappy-java | [787](https://cwe.mitre.org/data/definitions/787.html) | snappy-java through 1.1.10.8 contains an out-of-bounds write vulnerability in… |
| [CVE-2026-90558](https://nvd.nist.gov/vuln/detail/CVE-2026-90558) | 9.8 | irontec/sngrep | [121](https://cwe.mitre.org/data/definitions/121.html) | sngrep through 1.8.4 contains stack buffer overflow vulnerabilities in SIP… |

_Click a CVE id for the full record on NVD._
<!-- END cve.latest-10.report.md -->

## What CVEs keep teaching us

> The table below is regenerated on every CI run from
> [`report/cwe.top100.by-cve-count.since-2024.report.tsv`](./report/cwe.top100.by-cve-count.since-2024.report.tsv).
> Since 2024, XSS, SQL Injection, and Missing Authorization have
> been the top three weakness classes — every year, with very
> little reshuffling below. If your AI app renders user-supplied
> content or talks to a SQL backend, you're one unescaped
> interpolation away from shipping these.

<!-- BEGIN cwe.report.md -->

_117,528 CVEs across 683 distinct CWEs since 2024._

### What mistake do engineers keep making most often since 2024?

_Top 10 CWE by CVE count._

| Rank | CWE | Name | CVEs | Avg score |
| ---: | :-: | :--- | ---: | ---:      |
| 1 | [79](https://cwe.mitre.org/data/definitions/79.html) | Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') | 17,205 | 6.17 |
| 2 | [89](https://cwe.mitre.org/data/definitions/89.html) | Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') | 7,731 | 7.46 |
| 3 | [862](https://cwe.mitre.org/data/definitions/862.html) | Missing Authorization | 6,336 | 5.97 |
| 4 | [74](https://cwe.mitre.org/data/definitions/74.html) | Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') | 4,295 | 7.02 |
| 5 | [22](https://cwe.mitre.org/data/definitions/22.html) | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | 3,322 | 7.18 |
| 6 | [352](https://cwe.mitre.org/data/definitions/352.html) | Cross-Site Request Forgery (CSRF) | 3,276 | 5.81 |
| 7 | [94](https://cwe.mitre.org/data/definitions/94.html) | Improper Control of Generation of Code ('Code Injection') | 2,793 | 6.79 |
| 8 | [416](https://cwe.mitre.org/data/definitions/416.html) | Use After Free | 2,570 | 7.67 |
| 9 | [78](https://cwe.mitre.org/data/definitions/78.html) | Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') | 2,532 | 8.10 |
| 10 | [125](https://cwe.mitre.org/data/definitions/125.html) | Out-of-bounds Read | 2,320 | 6.34 |

### When that mistake is made, how bad is it since 2024?

_Top 10 CWE by average CVSS score. Min 10 CVEs to suppress single-CWE outliers._

| Rank | CWE | Name | CVEs | Avg score | Max |
| ---: | :-: | :--- | ---: | ---:      | ---: |
| 1 | [506](https://cwe.mitre.org/data/definitions/506.html) | Embedded Malicious Code | 48 | 9.15 | 10.0 |
| 2 | [95](https://cwe.mitre.org/data/definitions/95.html) | Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') | 136 | 8.56 | 10.0 |
| 3 | [565](https://cwe.mitre.org/data/definitions/565.html) | Reliance on Cookies without Validation and Integrity Checking | 18 | 8.38 | 9.8 |
| 4 | [502](https://cwe.mitre.org/data/definitions/502.html) | Deserialization of Untrusted Data | 1,748 | 8.34 | 10.0 |
| 5 | [288](https://cwe.mitre.org/data/definitions/288.html) | Authentication Bypass Using an Alternate Path or Channel | 465 | 8.27 | 10.0 |
| 6 | [917](https://cwe.mitre.org/data/definitions/917.html) | Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') | 29 | 8.21 | 10.0 |
| 7 | [29](https://cwe.mitre.org/data/definitions/29.html) | Path Traversal: '..filename' | 49 | 8.16 | 9.9 |
| 8 | [120](https://cwe.mitre.org/data/definitions/120.html) | Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') | 1,118 | 8.12 | 10.0 |
| 9 | [306](https://cwe.mitre.org/data/definitions/306.html) | Missing Authentication for Critical Function | 1,273 | 8.12 | 10.0 |
| 10 | [121](https://cwe.mitre.org/data/definitions/121.html) | Stack-based Buffer Overflow | 1,835 | 8.12 | 10.0 |
<!-- END cwe.report.md -->

<!-- BEGIN cve.report.md -->

## How fast is CVE growing?

> 2026 is on track for ~75,000 CVEs — double 2024's 38,451 in
> just two years. If your scanning cadence is annual, you're
> 6-12 months behind the most recent year. Source:
> [`report/cve.report.tsv`](./report/cve.report.tsv).

| Year | CVEs | Scored | Avg score | Max score |
| ---: | ---: | ---:   | ---:      | ---:      |
| 2026 _(YTD as of 2026-09-13)_ | 56,168 | 52,947 | 7.08 | 10.0 |
| 2025 | 43,471 | 42,044 | 6.79 | 10.0 |
| 2024 | 38,451 | 37,057 | 6.81 | 10.0 |
| 2023 | 30,616 | 24,751 | 6.73 | 10.0 |
| 2022 | 26,445 | 17,468 | 6.79 | 10.0 |
| 2021 | 22,601 | 10,834 | 6.83 | 10.0 |
| 2020 | 19,392 | 6,916 | 6.84 | 10.0 |
| 2019 | 16,096 | 3,527 | 6.84 | 10.0 |
| 2018 | 16,188 | 2,292 | 6.92 | 10.0 |
| 2017 | 14,762 | 1,375 | 7.18 | 10.0 |
| 2016 | 9,367 | 408 | 7.10 | 10.0 |
| 2015 | 8,111 | 252 | 6.26 | 10.0 |
| 2014 | 8,427 | 290 | 6.62 | 10.0 |
| 2013 | 6,221 | 154 | 7.44 | 10.0 |
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
| **Total** | **372,348** | **200,917** | **6.87** | **10.0** |
<!-- END cve.report.md -->

## Reports

The tables above are sliced from the derived reports in
[`report/`](./report/) (sibling of `data/`) — see
[`report/README.md`](./report/README.md) for methodology, the SINCE_DATE
cutoff, and how the top-10 markdown is sliced from the top-100 TSV.

### Per-year CVE stats

| File | Format | Window |
| ---  | ---    | ---    |
| [`report/cve.report.md`](./report/cve.report.md)   | Markdown table | all years |
| [`report/cve.report.tsv`](./report/cve.report.tsv) | TSV            | all years |

### Latest-N CVEs (front-of-page table)

| File | Format | Window |
| ---  | ---    | ---    |
| [`report/cve.latest-10.report.md`](./report/cve.latest-10.report.md)   | Markdown table | newest 10 CVEs |
| [`report/cve.latest-10.report.tsv`](./report/cve.latest-10.report.tsv) | TSV            | newest 10 CVEs |

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


## Developer docs

Repository layout, schema details, scripts, and CI pipeline live in
[`CONTRIBUTING.md`](./CONTRIBUTING.md).

How to use the data → [`SKILL.md`](./SKILL.md).

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

## FAQ

### What is CVE?

**CVE** (Common Vulnerabilities and Exposures) is the public, free
catalog of every publicly disclosed computer-security vulnerability,
maintained by [MITRE](https://cve.mitre.org/) under funding from
the U.S. Department of Homeland Security. Each entry gets a unique
id (`CVE-YYYY-NNNN`) plus a short English description, a list of
affected vendor/products, a CVSS base score, and the weakness class
([CWE](https://cwe.mitre.org/)) the vuln maps to. As of 2026 the
catalog holds ~370,000 records going back to CVE-1999-0001.

### What is CWE?

**CWE** (Common Weakness Enumeration) is the taxonomy of software
weakness *types* — categories like "Cross-Site Scripting",
"Use After Free", "Path Traversal". A CVE points at one or more
CWE ids in its `problemTypes[]` array; this repo joins the two so
you can ask "how many XSS vulns shipped this year?" without
scanning 370k records by hand. MITRE's full CWE catalog lives at
[`data/cwe.tsv`](./data/cwe.tsv); the slim id→name join table is
[`data/cwe.slim.tsv`](./data/cwe.slim.tsv).

### What is the difference between CVE and CWE?

- **CVE** = a *specific instance* of a bug (e.g. CVE-2026-90616:
  Flatpak before 1.18.1 has a sandbox-escape).
- **CWE** = the *category* of bug (e.g. CWE-22: Path Traversal).

A single CVE typically references one or more CWE ids that
describe the class of weakness. CWE counts across CVEs are how
this repo ranks "which mistakes keep happening most".

### What are the most common CWE weaknesses?

The **Top 10 CWE by CVE count** table at the top of this README
shows what's getting shipped most since 2024. As of this run:

1. [CWE-79](https://cwe.mitre.org/data/definitions/79.html) — Cross-Site Scripting (XSS)
2. [CWE-89](https://cwe.mitre.org/data/definitions/89.html) — SQL Injection
3. [CWE-862](https://cwe.mitre.org/data/definitions/862.html) — Missing Authorization
4. [CWE-22](https://cwe.mitre.org/data/definitions/22.html) — Path Traversal
5. [CWE-94](https://cwe.mitre.org/data/definitions/94.html) — Code Injection
6. [CWE-78](https://cwe.mitre.org/data/definitions/78.html) — OS Command Injection
7. [CWE-416](https://cwe.mitre.org/data/definitions/416.html) — Use After Free
8. [CWE-20](https://cwe.mitre.org/data/definitions/20.html) — Improper Input Validation
9. [CWE-125](https://cwe.mitre.org/data/definitions/125.html) — Out-of-bounds Read
10. [CWE-352](https://cwe.mitre.org/data/definitions/352.html) — CSRF

XSS and SQLi have topped this list every year since CVE started.
For the top-100 (all years and since-2024 windows), see
[`report/cwe.top100.by-cve-count.report.tsv`](./report/cwe.top100.by-cve-count.report.tsv).

### What are the most dangerous (highest CVSS) CWE classes?

The **Top 10 CWE by average CVSS score** table ranks weakness
*types* by the mean CVSS base score of the CVEs that reference
them (with at least 10 samples to suppress single-CVE outliers).
The head of this list tends to be dominated by:

- [CWE-506](https://cwe.mitre.org/data/definitions/506.html) — Embedded Malicious Code
- [CWE-95](https://cwe.mitre.org/data/definitions/95.html) — Eval Injection
- [CWE-502](https://cwe.mitre.org/data/definitions/502.html) — Deserialization of Untrusted Data
- [CWE-288](https://cwe.mitre.org/data/definitions/288.html) — Authentication Bypass via Alternate Channel
- [CWE-121](https://cwe.mitre.org/data/definitions/121.html) — Stack-based Buffer Overflow

These are the classes that, when shipped, *hurt the most*. The
table is regenerated on every CI run — see
[`report/cwe.top100.by-cve-score.report.tsv`](./report/cwe.top100.by-cve-score.report.tsv)
for the full top-100.

### What are the latest published CVEs?

The **10 newest CVEs** table at the very top of this README is
the front-of-page answer. It's regenerated every 4 hours directly
from MITRE's feed, so the table you see is at most a few hours
behind "right now". For the machine-readable top-N, see
[`report/cve.latest-10.report.tsv`](./report/cve.latest-10.report.tsv)
or run `python3 .x-cmd/latest.py N` for any other N.

### How many CVEs are published per year?

The "How fast is CVE growing?" table on this page answers that
question year-by-year with totals, scored count, and average /
max CVSS. The short answer: CVE volume has roughly doubled in
the past five years, with 2026 already past 56,000 records in
the first three quarters. Full per-year TSV lives at
[`report/cve.report.tsv`](./report/cve.report.tsv).

### Why does `cve-2015.tsv` have 8,110 rows but a max CVE id of 1,142,857?

Because MITRE assigned **large reserved id blocks** to the big
CNAs (Microsoft, Apple, Adobe, Google, Oracle) and each CNA
filled only a fraction. The 99% gap in 2015 and similar years is
not a bug — it's the structural shape of the post-2014 CNA
distribution model. Post-2020 the gap settled at 38-53%, the
steady-state mix of reserved blocks + REJECT (withdrawn)
records + duplicate-merge dedup.

| Year | Rows | Max NNNN | Gap | Gap % |
|---|---|---|---|---|
| 2014 | 8,426 | 125,128 | 116,702 | 93% |
| 2015 | 8,110 | 1,142,857 | 1,134,747 | 99% |
| 2018 | 16,187 | 1,999,047 | 1,982,860 | 99% |
| 2024 | 38,450 | 58,382 | 19,932 | 34% |
| 2026 YTD | 56,167 | 90,679 | 34,512 | 38% |

This is also why the per-year TSV is sorted by the NNNN
**integer** (not lexicographic) — so `CVE-2026-10000` shows up
where it actually belongs, not buried under the gap. Full
numbers in
[docs/5-yearly-stats-explained.md](./docs/5-yearly-stats-explained.md).

### How do I look up a single CVE?

For one record by id (e.g. `CVE-2024-0001`), the upstream
authority is the [NVD detail page](https://nvd.nist.gov/vuln/detail/CVE-2024-0001)
(NIST). The repo's companion [`x cve`](https://x-cmd.com/mod/cve)
shell module gives you the same answer offline:

```sh
x cve info CVE-2024-0001
x cve info 2024-0001            # YYYY-NNNN shorthand works too
x cve detail CVE-2024-0001      # full upstream JSON
```

`x cve` reads the per-year TSVs in this repo, so it works
air-gapped once the release asset has been fetched.

### How do I download the full CVE database?

Three options, all free and unauthenticated:

```sh
# 1. One specific year (smallest payload, ~5 MB xz)
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz     | xz -dc > cve-2026.tsv

# 2. Whole catalog as a tarball (~21 MB xz)
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-all.tar.xz     | tar -xJ

# 3. Just the CWE catalog (~150 KB xz, ~3 MB raw)
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cwe.tsv.xz     | xz -dc > cwe.tsv
```

Each asset is regenerated every 4 hours when upstream changes.
Files are plain tab-separated TSVs — see
[TSV columns](#tsv-columns-9) for the schema. No API key,
no rate limit.

### How do I query CVEs by CWE / vendor / CVSS?

The TSV columns are documented under
[TSV columns](#tsv-columns-9). Because everything is plain
text, standard Unix tooling is enough:

```sh
# All XSS CVEs scored >= 7.0 since 2024
xz -dc cve-2024.tsv xz -dc cve-2025.tsv xz -dc cve-2026.tsv 2>/dev/null     | awk -F'\t' '$8 ~ /(^|;)79(;|$)/ && $6+0 >= 7'

# All CVEs affecting Apache HTTP Server in the current year
xz -dc cve-2026.tsv     | awk -F'\t' '$4 ~ /Apache\/HTTP Server/ {print $1, $6, $9}'

# Top vendors by CVE count since 2024
xz -dc cve-2024.tsv xz -dc cve-2025.tsv xz -dc cve-2026.tsv 2>/dev/null     | awk -F'\t' { for (i=1;i<=split($4,p,";");i++) print p[i] }'     | sort | uniq -c | sort -rn | head -20
```

The release includes pre-aggregated variants for the common
queries — see [`report/`](./report/) for top-100 CWE rankings
by count and by score.

### Where do the Chinese CWE names come from?

The Chinese names surfaced in the CWE ranking tables come from
[cwe.org.cn](https://cwe.org.cn) — MITRE's official Chinese
mirror. The fetcher ([`.x-cmd/cwe_zh.py`](./.x-cmd/cwe_zh.py))
runs on every CI cycle and writes
[`data/cwe.zh.tsv`](./data/cwe.zh.tsv) (~91% coverage of the
969-entry catalog). The remaining 9% (mostly views and deprecated
ids) gracefully fall back to English names in the rendered
table — see [issue #2](https://github.com/x-cmd/cve/issues/2).
Force a re-fetch with `python3 .x-cmd/cwe_zh.py --force`.

### Is there a CVE database in Chinese / 中文 CVE 数据库?

