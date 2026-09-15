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
---

# 怎么读最新 CVE 表

顶部表格——由 `.x-cmd/latest.py` 从每个 per-year TSV 的头部生成——展示索引里最新收录的 10 条 CVE。
每次 CI 跑都会刷新，所以新发布的 CVE 在 MITRE 收录后 4 小时内就会出现在这里。

## 字段说明

每行有 5 个可见字段。两个是指向性字段
（`CVE` → NVD 详情，`CWE` → MITRE 定义），两个是信号字段
（`Score`、`Description`），剩下一个是产品字段（`Product`）。

| 字段 | 含义 | 怎么用 |
|---|---|---|
| `CVE` | 完整 CVE id，形如 `CVE-2026-90616` | 点开看 NVD 完整详情页（受影响版本、引用、时间线） |
| `Score` | 最高的 CVSS 基础分，保留一位小数 | 已发布的严重程度评级；9+ 为严重，7-8.9 为高，4-6.9 为中 |
| `Product` | `<vendor>/<product>`，多个时用 `;` 连接 | Bug 所在的产品 — 你的 AI 技术栈多半依赖其中之一 |
| `CWE` | 仅首个 CWE id（多个时附 `+N`） | Bug 的*类别*（XSS、路径遍历、eval 注入……） |
| `Description` | 上游英文描述的第一句，≤ 80 字符 | 一句话「是什么」— 想知道更多请点 CVE 链接 |

## 一分钟看懂 CVSS

CVSS（Common Vulnerability Scoring System，通用漏洞评分系统）是一个 0–10 的严重程度分值，
由 CNA（CVE Numbering Authority，通常是厂商或 MITRE 这样的协调机构）发布。

**没错，现在在用的 CVSS 一共有四个版本**，全部由
[FIRST.org](https://www.first.org/cvss/) 维护（Forum of Incident Response and Security Teams，CVSS 背后的标准组织）。
每条记录由 CNA 自行选择发哪个版本；生态里的其他角色只是消费 CNA 选定的那个版本：

- **CVSS v4.0** — 当前规范（2023+）。2024 年以来的新记录通常使用 v4。
- **CVSS v3.1** — 事实上的现行标准，2019 年起被大多数主流 CNA 采用。2019–2024 的记录绝大多数用的就是它。
- **CVSS v3.0** — 较老的 v3 变体；已被 v3.1 取代，但仍出现在部分记录中。
- **CVSS v2.0** — 遗留版本；多数 2017 年之前的记录还在用它。

**为什么多版本能并存：** FIRST 把每个 CVSS 版本都当作一份稳定、独立维护的标准来对待 —— 新版本发布时，旧版本不会被退役，因为工具、扫描器、历史记录都依赖稳定可解析的格式。CNA 选择与自己评分工具和流程相匹配的版本。生态必须把所有版本都处理掉。

**本仓库内：** `data/cve-YYYY.tsv` 按 v4 → v3.1 → v3.0 → v2 的优先级顺序存储所有版本中最高的那个分值。
空白分值意味着 CNA 从未发布过评分 —— 并不代表「严重程度低」。
底层计算逻辑参见
[CVSS v4.0 规范](https://www.first.org/cvss/v4.0/specification-document)。
快速查询的话，[NVD 的 CVSS 计算器](https://nvd.nist.gov/vuln-metrics/cvss/v4-calculator)
是最易用的交互工具。

## 「已发布补丁」是弱信号

底层 TSV 的第 7 列（`patched`，首页表里不显示）在 MITRE 的 `containers.cna.solutions[]` 非空时为 `1`。两点注意事项：

- **`solutions[]` 为空并不代表没打补丁。** 很多 CNA
  （尤其是较小的开源项目）修了 bug 但没填这个结构化字段。
  维护者已经在 `HEAD` 里修了，但 MITRE 这边没有机器可读的信号。
- **`patched: 1` 也不代表你装的版本里有这个修复。**
  它只表示*上游有修复存在*。你固定版本的依赖是否把这个修复吃进来，是另一个问题 —— 那是
  `dependabot` / Renovate / `npm audit fix` 的活儿。

## 「最新」实际指什么

表格按 **CVE id** 排序，而不是按 `Date` 或 `Modified`。
id 的序号段按数值排序——所以 `CVE-2026-90616`
排在 `CVE-2026-90615` 之前；但 `CVE-2026-10000` 出现时，
不会被排到 `CVE-2026-99999` 之后（因为它还没被分配到
天然的 4 位数区间之外）。

5 位序号区间的切换发生在 2025 年年中 —— 当时一个 bug 曾
短暂出现，导致表格只显示 `CVE-YYYY-9999`，详见
[issue #3](https://github.com/x-cmd/cve/issues/3)。

## 表格怎么生成的

`report/cve.latest-10.report.{tsv,md}` 由
`.x-cmd/latest.py` 生成。它只读每个 per-year TSV 的头部
（年内已经按 NNNN 降序），逐行取够 N 条为止，输出带 NVD + MITRE CWE
链接的 markdown 表。README 的 BEGIN/END 标记包住的就是这个文件的内容。

## 看实时表格

当前的 Top 10 在
[`README.md`](../../README.md) 顶部，每 4 小时刷新一次。

## 继续阅读

- [`3-top-cwes-explained.md`](./3-top-cwes-explained.md) — CWE 列究竟编码了什么
- [`4-yearly-stats-explained.md`](./4-yearly-stats-explained.md) — 「CVE 增长有多快」那张表
- [`5-using-the-data.md`](./5-using-the-data.md) — 按 CVE id 或 CWE 过滤拉取
