---
x-title: 数据怎么生成的
x-desc: CVEProject/cvelistV5 每 4 小时怎么变成这仓库的 per-year TSV。
x-sidebar: 数据怎么生成的
x-keywords: cvelistV5, tsv.py, cwe.py, cwe_zh.py, release.yml, CI 流水线, xz
x-json-ld:
  '@context': https://schema.org
  '@graph':
    - '@type': TechArticle
      headline: '数据怎么生成的'
      inLanguage: 'zh-Hans'
      about: 'x-cmd/cve 流水线'
---

# 数据怎么生成的

每 4 小时，GitHub Actions 上的 CI 会克隆
[CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5)，
遍历每条 CVE JSON 记录，输出一个按年份索引的 9 列 TSV。MITRE CWE 目录也用同样的方式拉取。整个流水线只有六个 Python 脚本加一个 workflow 文件，没有任何外部依赖。

## 流水线总览

```text
cvelistV5 JSON ─► tsv.py ─► data/cve-YYYY.tsv
                                  │
mitre.org 2000.csv ─► cwe.py ─► data/cwe.tsv + data/cwe.slim.tsv
                                  │
cwe.org.cn pages   ─► cwe_zh.py ─► data/cwe.zh.tsv
                                  │
                                  ├─► cwe_report.py ─► report/cwe.report.{tsv,md,zh.md}
                                  ├─► latest.py     ─► report/cve.latest-N.report.{tsv,md}
                                  └─► report.py     ─► report/cve.report.{tsv,md}

release.yml inline step ─► README.md + README.cn.md (front-of-page tables)
release.yml xz step      ─► release/data/*.xz (xz-compressed TSVs)
```

## 脚本（全部 Python 3.8+ 标准库）

| 脚本 | 读取 | 写入 | 作用 |
|---|---|---|---|
| `.x-cmd/tsv.py` | cvelistV5 JSON | `data/cve-YYYY.tsv` | 每条 CVE 一行，9 列，按 NNNN 倒序数值排序 |
| `.x-cmd/cwe.py` | MITRE 2000.csv | `data/cwe.tsv` + `data/cwe.slim.tsv` | 完整 21 列目录 + 2 列 id→name |
| `.x-cmd/cwe_zh.py` | cwe.org.cn 按 id 的 HTML | `data/cwe.zh.tsv` | MITRE 官方中文镜像，覆盖率约 91% |
| `.x-cmd/cwe_report.py` | `data/cve-*.tsv` + `data/cwe.{slim,zh}.tsv` | `report/cwe.report.{tsv,md,zh.md}` | Top-N CWE 按数量 / 按分数 |
| `.x-cmd/latest.py` | `data/cve-*.tsv`（仅头部） | `report/cve.latest-N.report.{tsv,md}` | 首页表格用的最新 N 条 CVE |
| `.x-cmd/report.py` | `data/cve-*.tsv` | `report/cve.report.{tsv,md}` | 各年 CVE 量 + 平均 / 最大 CVSS |

`_cve_index.py` 是共享解析器（json → 9 单元格行）和 IO 助手，以上脚本都在用。

## 调度

`.github/workflows/release.yml` 每 4 小时运行一次，cron 表达式为
`37 */4 * * *` UTC；此外每次 push 到 `main` 也会触发。一次典型的运行：

1. **Clone** [CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5) shallow。
2. **tsv.py --rebuild** —— 遍历每条 CVE JSON，写出 `data/cve-YYYY.tsv`。
3. **cwe.py** —— 拉取 MITRE CWE 目录 → `data/cwe.{tsv,slim.tsv}`。
4. **cwe_zh.py** —— 从 cwe.org.cn 拉取中文名 → `data/cwe.zh.tsv`。
5. **cwe_report.py** —— Top-N CWE 排名 → `report/cwe.report.*`。
6. **latest.py** —— 最新 10 条 CVE → `report/cve.latest-10.report.*`。
7. **report.py** —— 各年统计 → `report/cve.report.*`。
8. **内联拼接** —— 把 markdown 报告拼回 `README.md`
   和 `README.cn.md`（BEGIN/END 标记，幂等）。
9. **Commit** 新的 `data/`、`report/`、README 文件回 `main`。
10. **xz -9** 压缩每个有变化的 per-year TSV，并重新打包 `cve-all.tar.xz`。
11. **上传** 到 [`data`](https://github.com/x-cmd/cve/releases/tag/data)
    GitHub release —— 只传有变化的资源（与上一次 release 的 tarball 做字节级 `cmp`）。

如果某天上游没动静（零变更），第 9-11 步整段跳过；
消费端缓存的 sha256 保持有效。

## 输出落到哪里

- **`data/cve-*.tsv`** **不在** git 里。每次 CI 重建后，只作为 `cve-YYYY.tsv.xz` release 资源发布。
- **`report/*.{tsv,md}`** **在** git 里。预聚合的排名和首页 markdown 是 README 表格的 source of truth。
- **`data/cwe.{tsv,slim.tsv,zh.tsv}`** **在** git 里。这些文件很少变动（最多一季度一次），提交进 git 成本很低。

## 9 列（TL;DR —— 完整说明见后）

`cve`、`year`、`no`、`vp`、`ghsa`、`score`、`patched`、`cwe`、`desc`。
各字段含义见 [`2-latest-cves-explained.md`](./2-latest-cves-explained.md)。

## 继续阅读

- [`3-top-cwes-explained.md`](./3-top-cwes-explained.md) —— Top 10 CWE 表格怎么算的
- [`4-yearly-stats-explained.md`](./4-yearly-stats-explained.md) —— YTD、有分 vs 无分、合计
- [`5-using-the-data.md`](./5-using-the-data.md) —— 具体的 curl / `x cve` / Python 例子
