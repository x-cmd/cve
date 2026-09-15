---

x-title: 怎么使用数据
x-desc: 三种消费 CVE / CWE 数据的方式 —— curl + xz 用原始 TSV、x cve shell 模块、DuckDB / pandas。
x-sidebar: 怎么使用数据
x-keywords: CVE, CWE, AI 安全, 漏洞情报
x-json-ld:
  '@context': <https://schema.org>
  '@graph':
    - '@type': TechArticle
      headline: '如何使用这些数据'
      inLanguage: 'zh-Hans'
      about: '数据消费'
---

# 怎么使用数据

三种使用 CVE / CWE 数据的方式，按集成成本从低到高排列。

## 1. 原始 TSV（`curl` + `xz`）

数据托管在
[github.com/x-cmd/cve/releases/tag/data](https://github.com/x-cmd/cve/releases/tag/data)，
就是普通的 xz 压缩 TSV。无需安装、无需 shell 模块、无需 API key。

```sh
# 一年 CVE（约 5 MB xz）
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz \
  | xz -dc > cve-2026.tsv

# 全量目录（约 21 MB xz）
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-all.tar.xz \
  | tar -xJ

# 只要 CWE 目录（约 150 KB xz）
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cwe.tsv.xz \
  | xz -dc > cwe.tsv
```

`cve-YYYY.tsv` 的 9 个列在
[`3-latest-cves-explained`](./3-latest-cves-explained.en.md) 有说明。实战示例：

```sh
# 2026 年分数最高的 10 条 CVE
awk -F'\t' '$6!=""' cve-2026.tsv \
  | sort -t$'\t' -k6,6nr \
  | head -10 \
  | cut -f1,4,6
```

## 2. `x cve` shell 模块

[`x cve`](https://x-cmd.com/mod/cve) 把 TSV 包了一层，提供一个小 CLI 用于单条记录查询。先装
[x-cmd](https://x-cmd.com/install)，然后：

```sh
x cve                          # 列出所有 CVE（最新优先）
x cve fz                       # fzf 选择器
x cve info CVE-2024-0001        # 按 id 查一条记录（YYYY-NNNN 简写也行）
x cve detail CVE-2024-0001      # 来自 CVEProject/cvelistV5 的完整上游 JSON
x shodan cve CVE-2024-0001      # EPSS + KEV + exploit-writeups 富化
x cwe ls                        # 目录中所有 CWE
x cwe 79                        # 单条 CWE 的完整描述
```

`x cve` 从本仓库 release 资产读取按年切分的 TSV，所以只要资产被拉取过，就能离线工作。

## 3. Python — DuckDB / pandas / polars

TSV 就是纯文本，三者都能直接读。

### DuckDB（推荐用于 SQL 风格查询）

```python
import duckdb
con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs;")

# 通过 HTTP 读取一年数据
df = con.execute("""
  SELECT * FROM read_csv(
    'https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz',
    delim='\t', header=true, compression='gzip'
  )
""").df()
```

DuckDB 把全部 28 个按年文件合并成一张逻辑表：

```python
years = list(range(2024, 2027))
tables = [
    f"read_csv('https://github.com/x-cmd/cve/releases/download/data/cve-{y}.tsv.xz', delim='\\t', header=true, compression='gzip')"
    for y in years
]
df_all = con.execute(" UNION ALL ".join(tables)).df()

# 2024 年以来分数 >= 7 的所有 XSS CVE
xss = df_all.filter(
    (df_all["cwe"].fillna("").str.contains(r"(^|;)79(;|$)")) &
    (df_all["score"].astype(float) >= 7)
).sort("score", descending=True)
```

### pandas

```python
import pandas as pd
df = pd.read_csv("cve-2026.tsv", sep="\t", dtype=str, keep_default_na=False)
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["patched"] = df["patched"].astype(int)

# 2024 年以来 CWE-79 (XSS) 的头部供应商
mask = df["cwe"].str.contains(r"(^|;)79(;|$)", regex=True, na=False)
vendors = (
    df[mask].assign(v=df["vp"].str.split(";"))
            .explode("v")["v"]
            .value_counts()
            .head(20)
)
```

### polars

```python
import polars as pl
df = pl.read_csv("cve-2026.tsv", separator="\t", infer_schema_length=10000)
xss = df.filter(
    pl.col("cwe").str.contains(r"(^|;)79(;|$)"),
    pl.col("score").cast(pl.Float64, strict=False) >= 7,
).sort("score", descending=True)
```

## 何时选哪个

- **单条记录、浏览、Shodan 富化** → `x cve`（方案 2）。
- **批量分析、join 进 Python/R/DuckDB、脚本化 ETL** →
  原始 TSV（方案 1 或 3）。

两种方式拿到的 TSV 是同一份数据 —— `x cve` 只是上面套的一层轻量便利封装。

## 接下来读什么

- 字段定义：[`3-latest-cves-explained`](./3-latest-cves-explained.en.md)。
- CWE join + 排名逻辑：[`4-top-cwes-explained`](./4-top-cwes-explained.en.md)。
- 数据怎么生成的：[`2-how-data-is-built`](./2-how-data-is-built.en.md)。
- [README.md](../../README.md) 查看实时表格。
