---

x-title: 怎么读年度 CVE 增长表
x-desc: 怎么读 per-year CVE 量 + CVSS 统计表 — YTD、已打分 vs 未打分、Total 行的含义。
x-sidebar: 年度统计解读
x-keywords: CVE, CWE, AI 安全, 漏洞情报
x-json-ld:
  '@context': <https://schema.org>
  '@graph':
    - '@type': TechArticle
      headline: '年度 CVE 增长表怎么读'
      inLanguage: 'zh-Hans'
      about: 'cve.report.tsv'
---

# 怎么读年度 CVE 增长表

[`README.md`](../../README.md) 上的第三张表——「CVE 增长得有多快？」——来自 `report/cve.report.{tsv,md}`。它展示自 1999 年以来每年的 CVE 量 + 已打分数量 + 平均 + 最高 CVSS。

## 各列含义

| 字段 | 是什么 | 怎么用 |
|---|---|---|
| `Year` | 4 位年份，或 `**Total**` | 单年行可排序；Total 行是所有年份的合计 |
| `CVEs` | 该年的 CVE 行数 | 当年实际发布的新漏洞数量 |
| `Scored` | 其中有多少有非空 CVSS 分 | Scored / total = 「已打分占比」。空白分意味着未发布 CVSS，不是「低危」 |
| `Avg score` | 已打分 CVSS 的均值 | 单数字总结；样本少时会误导，看趋势比较有用 |
| `Max score` | 当年最高的 CVSS | 「这年最严重到几」的指标 |

当前年份那一行带 `YTD` 标注（例如 `2026 (YTD as of 2026-09-12)`），因为这一行还没结束——`CVEs` 数量是局部的，不是最终值。形态和年终数字一样，只是小一些。

## Total 行

`Total` 是**所有年份的合计**，不是唯一 CVE id 的数量。因为目录会保留历史记录（我们不会追溯性地丢掉已撤回的 CVE），所以 Total 单调非递减——只会随着新年份加入而增长或持平。

有两个相关的 Total，分布在不同文件里：

- `report/cve.report.tsv` 的 `Total` —— 各年 `CVEs` 之和（原始目录规模）。截至 2026-09-12 约为 370,000。
- `cwe_report.py` 里 CWE 排名的 `sum(r[2] for r in rows_since)` —— `since 2024` 窗口中不同的 `(CVE, CWE)` 对。数字不同；不在 README 上。

## 为什么有些年份 Avg score 是 `—`

当年已打分 CVE 为零时（当前数据里是 2000 年），`Avg score` 单元格渲染为破折号（`—`），而不是 `0.0` 或 `NaN`。TSV 里也保留同样的破折号。Total 行按 `avg = sum(scored_count × year_avg) / sum(scored_count)` 计算——跨年加权平均——所以有些年份贡献零分时整体仍然合理。

## 目录实际上增长多快？

![CVE records per year, 1999 → 2026](./assets/cve-growth.svg)

近几年的数据：

- 2018：16,188 CVE
- 2020：19,392
- 2022：26,445
- 2024：38,451
- 2026 YTD（Sep 13）：56,168 —— 按节奏到年底约 75,000

翻倍间隔在缩短：2018 → 2023（5 年）几乎翻倍（16k → 30k），2023 → 2026（3 年）按节奏会到 2.5×。2024 → 2026 只用两年就翻倍。增长在加速，不是稳定。

如果你的安全扫描节奏是一年一次，那你看到的 CVE 披露就会比真实情况落后 6–12 个月。本仓库 CI 的 4 小时刷新节奏是一种解法；订阅实时数据流（NVD RSS、厂商公告）也是一种。

## 为什么 CVE id 范围比行数大

对每一年，per-year TSV 的行数都小于 NNNN 序号最大值所暗示的数量。基于 `data/cve-YYYY.tsv` 算出的样本：

| 年份 | 行数 | 最大 NNNN | 缺口 | 缺口 % |
|---|---|---|---|---|
| 2014 | 8,426 | 125,128 | 116,702 | 93% |
| 2015 | 8,110 | 1,142,857 | 1,134,747 | 99% |
| 2018 | 16,187 | 1,999,047 | 1,982,860 | 99% |
| 2024 | 38,450 | 58,382 | 19,932 | 34% |
| 2026 YTD | 56,167 | 90,679 | 34,512 | 38% |

2014–2019 年 98–99% 的缺口不是 bug。那个年代 MITRE 给大型 CNA 分配了**大块保留 id 区间**——Microsoft、Apple、Adobe、Google、Oracle 各自拿到整 10000 的区间，只填了其中一小部分。2014 年的具体形态（已对照上游 `cvelistV5` JSON 树验证）：

| 2014 NNNN 区间 | 行数 | 可能的归属 |
|---|---|---|
| 1 – 9,999 | 8,162 | 通用 / 小型 CNA |
| 10,000 – 19,999 | 102 | Microsoft（保留） |
| 20,000 – 99,999 | 0 | （无 CNA 填充此区间） |
| 100,000 – 109,999 | 39 | Microsoft（中段） |
| 120,000 – 125,127 | 123 | Apple（2014 末段） |

所以 2014 年的 93% 缺口其实是有两大块保留区间（Microsoft 100k 和 Apple 120k），每块只填了 1–2%。2015 年的 99% 缺口形态相同。CNA 体系在 2020 年前后成熟之后，缺口稳定在 38–53%，这是以下几项因素的稳态组合：

- **保留区间**——CNA 已持有但尚未分配的 id 块。
- **`REJECT` 记录**——MITRE 把 CVE 标记为已撤回；我们在下次重建时丢掉该行，但 id 永不重用。
- **重复合并**——多条 JSON 文件描述同一条 CVE，`tsv.py` 按 `cve_id` 这个键把它们合并成一行。

这就是为什么 [issue #3](https://github.com/x-cmd/cve/issues/3) 重要：旧的字典序排序会把 `CVE-2026-99999` 排在 `CVE-2026-10000` **之前**（因为字符串比较里 `'9' > '1'`），把真实最高 id 藏在一堆保留但为空的槽位下。按 NNNN 整数排序才能让缺口可见，文件才好浏览。

## 「已打分」是什么意思

当 CNA 发布了至少一条 CVSS 向量（v2.0、v3.0、v3.1 或 v4.0），这条 CVE 就是「已打分」。较老的 CVE（1999–2016）和较小的 CNA 倾向留空这个字段；现代 CVE 几乎总是已打分（2024+ 达到 98%+）。

流水线在四个版本中按 v4 → v3.1 → v3.0 → v2 的优先级存**最高**分。`cve-YYYY.tsv` 里的 `score` 列就是这个单一数字；原始上游 JSON（通过 `x cve detail CVE-YYYY-NNNN` 可访问）带有完整向量。

## 文件怎么生成的

`.x-cmd/report.py` 遍历每个 `data/cve-YYYY.tsv`，按年统计行数 + 已打分行数 + 分值之和，然后输出 `cve.report.tsv`（5 列，机器可读）和 `cve.report.md`（给 README 的 markdown 表）。

## 继续阅读

- [`1-how-data-is-built.md`](./1-how-data-is-built.md) —— 流水线与脚本
- [`3-top-cwes-explained.md`](./3-top-cwes-explained.md) —— 另外两张表
- [`5-using-the-data.md`](./5-using-the-data.md) —— 自己查询 per-year TSV
