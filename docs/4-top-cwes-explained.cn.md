---

x-title: Top CWE 排名怎么算的
x-desc: CVE 怎么 join 到 CWE、按数量排名、按平均 CVSS 排名、为什么有「since 2024」窗口。
x-sidebar: Top CWE 解读
x-keywords: CWE join, mean CVSS, since 2024, MIN_CVE_FOR_SCORE_RANK, top 100 CWE
x-json-ld:
  '@context': <https://schema.org>
  '@graph':
    - '@type': TechArticle
      headline: 'Top CWE 排名怎么算的'
      inLanguage: 'zh-Hans'
      about: 'CWE 排名'
---

# Top CWE 排名怎么算的

[`README.md`](../../README.md) 上的两张 CWE 表来自同一个 join、按两种方式排序。这页解释 join 做了什么、两种排序轴的含义，以及数字为什么会随时间漂移。

## Join：每条 CVE × 它引用的每个 CWE

`data/cve-YYYY.tsv` 里每行 CVE 的 `cwe` 列都包含一个或多个 CWE id（已剥掉前缀、用 `;` 连接）：

```text
CVE-2024-12345  cwe="79;352"     # XSS + CSRF
CVE-2024-67890  cwe="89"          # SQL 注入
CVE-2024-99999  cwe=""            # 未分配弱点类别
```

排序时，我们把多 CWE 的行**展开**成每对 (CVE, CWE) 一条记录。一条 `cwe="79;352"` 的 CVE 同时给 CWE-79 和 CWE-352 各贡献 +1。`cwe` 为空的 CVE 不贡献任何东西。

## 按 CVE 数量排名

`report/cwe.top100.by-cve-count.report.tsv` 把所有 CWE 按展开后的计数倒序排。稳定排序规则：均分 CVSS 高的优先，再按 CWE id 升序。

**为什么有「since 2024」窗口：** 不设窗口的话，全年代视图会被 2008–2018 年的 CVE 主导 —— 2010 年代 PHP 时代的 SQL 注入全部冒上来，而现代的类别（LLM prompt 注入、agent 鉴权、MCP 供应链）永远挤不到前列。`since 2024` 视图把 2024 年之前的数据全部丢掉，让排名反映**当下工程师在犯什么错** —— 见 [`.x-cmd/cwe_report.py`](https://github.com/x-cmd/cve/blob/main/.x-cmd/cwe_report.py) 里的 `SINCE_YEAR` 常量。

## 按平均 CVSS 排名

`report/cwe.top100.by-cve-score.report.tsv` 按 CWE 关联的所有 CVE 的 **CVSS 基础分平均值** 排序（每个 CWE 至少 10 个样本 —— 见 `MIN_CVE_FOR_SCORE_RANK`）。

**为什么用均值而不是中位数：** CVSS 分数集中在几个离散值（4.0、7.5、9.8 ……），用中位数会让每个 CWE 都打成 7.5 的平局。均值才能反映一个类别是否*系统性*地比另一个类别得分更高。

**为什么需要「至少 10 个样本」的下限：** 一条 2020 年的 CVE-2020-1234 被归类为 `Embedded Malicious Code`（CWE-506）且分值 9.8，会独自霸榜 —— 那只是个案，不是类别趋势。10 个样本的下限把这些离群值压下去。

## 排名里不包含的内容

- **CWE 视图与类别**（CWE-699「Software Development」、CWE-1000「Research Concepts」）。`cwe_report.py` 只对单个 CWE 排名，汇总类别这里不会出。需要的话直接从 MITRE 目录抓（[cwe.mitre.org/data/csv/2000.csv.zip](https://cwe.mitre.org/data/csv/2000.csv.zip)）。
- **CWE 为空的 CVE。** 最近 CVE 里大约 15–20% 的 `problemTypes[]` 在上游 JSON 里为空。它们会出现在年度统计里，但不会进入任何 CWE 排名。
- **已撤回 / 已驳回的 CVE。** 一旦 MITRE 把记录标记为 `REJECT`，流水线会在下一次 `tsv.py` 重建时丢掉它 —— 那些行就直接从目录里消失了。

## 为什么数字每次跑会变

两个原因让这张表每 4 小时就动一次：

1. **新 CVE 不断进入。** MITRE 在 2026 年每天发布约 50–200 条 CVE；每条都可能引用新的 CWE id，或强化已有的 CWE。
2. **CNA 重新分类。** CNA 可以更新某条 CVE 的 `problemTypes[]` —— 比如给原本只标了 CWE-79 的 CVE 再加上 CWE-862。下次重建时会捡到这条更新，行数和排名相应变化。

预聚合的 TSV 每次 CI 都会提交到 git，所以你可以跑 `git log -- report/cwe.top100.by-cve-count.since-2024.report.tsv` 看排名的历史形状。

## 文件怎么生成的

`.x-cmd/cwe_report.py` 做 join + 排序，输出两份 TSV（全部年份 + since 2024）和两份 markdown（英文 + 中文）。中文版本只在 `data/cwe.zh.tsv` 至少有一行时才输出 —— 见 [`1-how-data-is-built.md`](./1-how-data-is-built.md) 了解这个文件是怎么填进去的。

## 继续阅读

- [`1-how-data-is-built.md`](./1-how-data-is-built.md) —— 流水线与脚本
- [`2-latest-cves-explained.md`](./2-latest-cves-explained.md) —— 各列含义
- [`4-yearly-stats-explained.md`](./4-yearly-stats-explained.md) —— README 上的第三张表
- [`5-using-the-data.md`](./5-using-the-data.md) —— 拉取排名 TSV 自己切片
