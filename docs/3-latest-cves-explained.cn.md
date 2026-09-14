---

x-title: 怎么读最新 CVE 表
x-desc: 怎么读 README 顶部的「最新 10 条 CVE」表 — 字段含义、CVSS 速通、「patched」信号为什么弱。
x-sidebar: 最新 CVE 表解读
x-keywords: CVE, CWE, AI 安全, 漏洞情报
x-json-ld:
  '@context': <https://schema.org>
  '@graph':
    - '@type': TechArticle
      headline: '最新 CVE 表怎么读'
      inLanguage: 'zh-Hans'
      about: 'cve.latest-10.report.md'
---顶部表格——由 `.x-cmd/latest.py` 从每个 per-year TSV 的头部生成——显示索引里最新收录的 10 条 CVE。
每次 CI 跑都会刷新，所以新发布的 CVE 在 MITRE 收录后 4 小时内就会出现在这里。

## 字段说明

Each row has 5 visible fields. Two of them are pointers
(`CVE` → NVD detail, `CWE` → MITRE definition), two are signals
(`Score`, `Description`), and one is the product (`Product`).

| Field | What it is | How to use it |
|---|---|---|
| `CVE` | Full CVE id like `CVE-2026-90616` | Click for the full NVD detail page (affected versions, references, timeline) |
| `Score` | Highest CVSS base score, single decimal | The published severity rating; 9+ is critical, 7-8.9 high, 4-6.9 medium |
| `Product` | `<vendor>/<product>` joined by `;` if multiple | Where the bug lives — your AI stack likely depends on one of these |
| `CWE` | First CWE id only (with `+N` if more) | The *kind* of bug (XSS, path traversal, eval injection, ...) |
| `Description` | First sentence of the upstream English description, ≤ 80 chars | The "what" — for the rest, follow the CVE link |

## 一分钟看懂 CVSS

CVSS (Common Vulnerability Scoring System) is a 0–10 severity
score published by the CNA (CNA = CVE Numbering Authority, usually
the vendor or a coordinator like MITRE). Three versions are in
active use:

- **CVSS v4.0** — current spec (2023+), preferred.
- **CVSS v3.1** — current de-facto standard before v4.0.
- **CVSS v3.0** — older v3 variant.
- **CVSS v2.0** — legacy; appears on records pre-2017.

We store the highest available, in priority order v4 → v3.1 → v3.0 → v2.
A blank score means the CNA never published one — not "low severity".

For the underlying math, see the
[CVSS v4.0 spec](https://www.first.org/cvss/v4.0/specification-document).
For a quick lookup, [NVD's CVSS calculator](https://nvd.nist.gov/vuln-metrics/cvss/v4-calculator)
is the easiest interactive tool.

## "Patch available" 是弱信号

The 7th column of the underlying TSV (`patched`, not shown in the
front-page table) is `1` if MITRE's `containers.cna.solutions[]` is
non-empty. Two caveats:

- **No `solutions[]` entry does not mean unpatched.** Many CNAs
  (especially smaller open-source projects) publish a fix without
  populating the structured field. The maintainer fixed it in
  `HEAD`, but MITRE has no machine-readable signal.
- **`patched: 1` does not mean it's in your installed version.**
  It means *a fix exists upstream*. Whether your pinned dependency
  version pulls the fix in is a separate question — that's
  `dependabot` / Renovate / `npm audit fix` territory.

## "最新" 实际是什么意思

The table is sorted by **CVE id**, not by `Date` or `Modified`. The
id's sequence segment is sorted numerically — so `CVE-2026-90616`
comes before `CVE-2026-90615`, but `CVE-2026-10000` (when it appears)
won't be pushed after `CVE-2026-99999` (it's not yet assigned
above the natural 4-digit range).

The 5-digit-sequence jump happened mid-2025 — see
[issue #3](https://github.com/x-cmd/cve/issues/3) for the bug
that briefly surfaced only `CVE-YYYY-9999`.

## 表格怎么生成的

`report/cve.latest-10.report.{tsv,md}` is produced by
`.x-cmd/latest.py`. It reads only the head of each per-year TSV
(already in NNNN-descending order within the year), takes rows
until it has N, and emits a markdown table with NVD + MITRE CWE
links. The README's BEGIN/END markers wrap this file's body.

## 看实时表格

The current top 10 lives at the top of
[`README.md`](../../README.md) and is regenerated every 4 hours.

## 继续阅读

- [`3-top-cwes-explained.md`](./3-top-cwes-explained.md) — what the CWE column actually encodes
- [`4-yearly-stats-explained.md`](./4-yearly-stats-explained.md) — the "How fast is CVE growing?" table
- [`5-using-the-data.md`](./5-using-the-data.md) — pull a specific CVE id or filter by CWE
