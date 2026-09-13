# 最近 10 个 CVE

<!-- cve-data-as-of:START -->
**数据截至：2026-09-13** _（每日从上游 cvelistV5 更新 —— 明天再看，榜单就会有变化）。_
<!-- cve-data-as-of:END -->

> 🌐 **English version: [README.md](./README.md)**.

<!-- BEGIN cve.latest-10.report.md -->

**The 10 newest CVEs** (descending CVE id = newest published first).

| CVE | Score | Product | CWE | Description |
| --- | ---:  | ---     | :-: | ---         |
| [CVE-2026-90668](https://nvd.nist.gov/vuln/detail/CVE-2026-90668) | 8.7 | UnrealIRCd/UnrealIRCd | [770](https://cwe.mitre.org/data/definitions/770.html) | The webserver in UnrealIRCd 6.0.5 through 6.2.6 before 6.2.7 does not limit the… |
| [CVE-2026-90651](https://nvd.nist.gov/vuln/detail/CVE-2026-90651) | 8.1 | Socket/Socket Firewall | [295](https://cwe.mitre.org/data/definitions/295.html) | Socket Firewall (socketdev/socket-registry-firewall) in registry mode before… |
| [CVE-2026-90648](https://nvd.nist.gov/vuln/detail/CVE-2026-90648) | 7.1 | WebAssembly/wabt | [252](https://cwe.mitre.org/data/definitions/252.html) | wasm2c in WebAssembly wabt through 1.0.41 allows sandbox escape in some… |
| [CVE-2026-90647](https://nvd.nist.gov/vuln/detail/CVE-2026-90647) | 9.1 | Kalkitech/ASE2000 V2 Communication Test Set | [295](https://cwe.mitre.org/data/definitions/295.html) | ASE/Kalkitech ASE2000 V2 Communication Test Set 2.35 through 2.37 on Windows… |
| [CVE-2026-90616](https://nvd.nist.gov/vuln/detail/CVE-2026-90616) | 7.4 | Flatpak/Flatpak | [61](https://cwe.mitre.org/data/definitions/61.html) | In Flatpak before 1.18.1, a malicious sandboxed app can obtain arbitrary read… |
| [CVE-2026-90560](https://nvd.nist.gov/vuln/detail/CVE-2026-90560) | 8.8 | luben/zstd-jni | [125](https://cwe.mitre.org/data/definitions/125.html) | zstd-jni versions 1.2.0 through 1.5.7-13 contain an out-of-bounds read… |
| [CVE-2026-90559](https://nvd.nist.gov/vuln/detail/CVE-2026-90559) | 8.7 | xerial/snappy-java | [787](https://cwe.mitre.org/data/definitions/787.html) | snappy-java through 1.1.10.8 contains an out-of-bounds write vulnerability in… |
| [CVE-2026-90558](https://nvd.nist.gov/vuln/detail/CVE-2026-90558) | 9.8 | irontec/sngrep | [121](https://cwe.mitre.org/data/definitions/121.html) | sngrep through 1.8.4 contains stack buffer overflow vulnerabilities in SIP… |
| [CVE-2026-90557](https://nvd.nist.gov/vuln/detail/CVE-2026-90557) | 6.9 | freeciv/freeciv | [125](https://cwe.mitre.org/data/definitions/125.html) | Freeciv versions 3.1.0 through 3.2.5 contain an out-of-bounds read… |
| [CVE-2026-90556](https://nvd.nist.gov/vuln/detail/CVE-2026-90556) | 8.5 | freeciv/freeciv | [122](https://cwe.mitre.org/data/definitions/122.html) | Freeciv versions before 3.2.6 contain a heap buffer overflow in worklist_load()… |

_Click a CVE id for the full record on NVD._
<!-- END cve.latest-10.report.md -->

# CVE 教会我们什么

> 本页是上游 CVE 索引的实时镜像。下方表格（逐年统计、CWE 错误 Top 10、按严重程度 Top 10）由每日 CI 自动生成，并非人工编排。

<!-- BEGIN cwe.report.zh.md -->

自 2024 年以来，共 117,493 个 CVE，涉及 683 个不同的 CWE。

### 2024 年以来，工程师们最常犯的错误是什么？

_Top 10 CWE by CVE count —— 按 CVE 数量排序的前 10。_

| Rank | CWE | Name | CVEs | Avg score |
| ---: | :-: | :--- | ---: | ---:      |
| 1 | [79](https://cwe.mitre.org/data/definitions/79.html) | 网页生成过程中的输入中和不当（“跨站脚本”） | 17,204 | 6.17 |
| 2 | [89](https://cwe.mitre.org/data/definitions/89.html) | SQL 命令中使用的特殊元素中和不当（“SQL 注入”） | 7,730 | 7.46 |
| 3 | [862](https://cwe.mitre.org/data/definitions/862.html) | 缺少授权 | 6,335 | 5.97 |
| 4 | [74](https://cwe.mitre.org/data/definitions/74.html) | 对下游组件使用的输出中特殊元素的未正确中和 ('注入') | 4,292 | 7.02 |
| 5 | [22](https://cwe.mitre.org/data/definitions/22.html) | 对受限目录的路径名限制不当（“路径遍历”） | 3,321 | 7.18 |
| 6 | [352](https://cwe.mitre.org/data/definitions/352.html) | 跨站请求伪造 (CSRF) | 3,276 | 5.81 |
| 7 | [94](https://cwe.mitre.org/data/definitions/94.html) | 不当的代码生成控制（“代码注入”） | 2,790 | 6.79 |
| 8 | [416](https://cwe.mitre.org/data/definitions/416.html) | 释放后重用 (Use After Free) | 2,570 | 7.67 |
| 9 | [78](https://cwe.mitre.org/data/definitions/78.html) | 对操作系统命令中使用的特殊元素的中和不当（“OS 命令注入”） | 2,531 | 8.10 |
| 10 | [125](https://cwe.mitre.org/data/definitions/125.html) | 越界读取 | 2,320 | 6.34 |

### 2024 年以来，犯下这些错误后果有多严重？

_Top 10 CWE by average CVSS score —— 至少 10 个 CVE 以避免单个 CWE 极端值的影响。_

| Rank | CWE | Name | CVEs | Avg score | Max |
| ---: | :-: | :--- | ---: | ---:      | ---: |
| 1 | [506](https://cwe.mitre.org/data/definitions/506.html) | 嵌入式恶意代码 | 48 | 9.15 | 10.0 |
| 2 | [95](https://cwe.mitre.org/data/definitions/95.html) | 动态评估代码中指令中和不当（“Eval 注入”） | 136 | 8.56 | 10.0 |
| 3 | [565](https://cwe.mitre.org/data/definitions/565.html) | 依赖未经验证和完整性检查的 Cookie | 18 | 8.38 | 9.8 |
| 4 | [502](https://cwe.mitre.org/data/definitions/502.html) | 不受信任数据的反序列化 | 1,747 | 8.34 | 10.0 |
| 5 | [288](https://cwe.mitre.org/data/definitions/288.html) | 通过备用路径或通道绕过身份验证 | 465 | 8.27 | 10.0 |
| 6 | [917](https://cwe.mitre.org/data/definitions/917.html) | 未对表达式语言语句中使用的特殊元素进行充分净化（“表达式语言注入”） | 29 | 8.21 | 10.0 |
| 7 | [29](https://cwe.mitre.org/data/definitions/29.html) | 路径遍历：'\..\filename' | 49 | 8.16 | 9.9 |
| 8 | [120](https://cwe.mitre.org/data/definitions/120.html) | 缓冲区复制时未检查输入大小（“经典缓冲区溢出”） | 1,117 | 8.12 | 10.0 |
| 9 | [306](https://cwe.mitre.org/data/definitions/306.html) | 关键功能缺少身份验证 | 1,273 | 8.12 | 10.0 |
| 10 | [121](https://cwe.mitre.org/data/definitions/121.html) | 基于栈的缓冲区溢出 | 1,835 | 8.12 | 10.0 |
<!-- END cwe.report.zh.md -->

<!-- BEGIN cve.report.md -->

## CVE 增长得有多快？

_逐年 CVE 数量与严重程度。_

| Year | CVEs | Scored | Avg score | Max score |
| ---: | ---: | ---:   | ---:      | ---:      |
| 2026 _（截至 2026-09-13）_ | 56,163 | 52,942 | 7.08 | 10.0 |
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
| **Total** | **372,343** | **200,912** | **6.87** | **10.0** |
<!-- END cve.report.md -->

## 报表（Reports）

上方的多张表都是从 [`report/`](./report/) 目录（与 `data/` 同级）下的衍生报表中切片出来的。详细的方法论、SINCE_DATE 阈值、以及 top-10 markdown 是如何从 top-100 TSV 切片出来的，请参阅 [`report/README.md`](./report/README.md)。

### 逐年 CVE 统计

| 文件 | 格式 | 时间范围 |
| ---  | ---    | ---    |
| [`report/cve.report.md`](./report/cve.report.md)   | Markdown 表格 | 全部年份 |
| [`report/cve.report.tsv`](./report/cve.report.tsv) | TSV            | 全部年份 |

### 最新 N 条 CVE（页面顶部表格）

| 文件 | 格式 | 时间范围 |
| ---  | ---    | ---    |
| [`report/cve.latest-10.report.md`](./report/cve.latest-10.report.md)   | Markdown 表格 | 最新 10 条 CVE |
| [`report/cve.latest-10.report.tsv`](./report/cve.latest-10.report.tsv) | TSV            | 最新 10 条 CVE |

### CWE 排名 — 4 份 Top 100 TSV（每个 排序维度 × 时间窗口 各一份）

| 文件 | 排序维度 | 时间范围 |
| ---  | ---  | ---    |
| [`report/cwe.top100.by-cve-count.report.tsv`](./report/cwe.top100.by-cve-count.report.tsv)               | CVE 数量  | 全部年份 |
| [`report/cwe.top100.by-cve-score.report.tsv`](./report/cwe.top100.by-cve-score.report.tsv)               | 平均评分  | 全部年份 |
| [`report/cwe.top100.by-cve-count.since-2024.report.tsv`](./report/cwe.top100.by-cve-count.since-2024.report.tsv) | CVE 数量  | 2024 年以来 |
| [`report/cwe.top100.by-cve-score.since-2024.report.tsv`](./report/cwe.top100.by-cve-score.since-2024.report.tsv) | 平均评分  | 2024 年以来 |

### CWE 排名 — Markdown（每个维度 Top 10，2024 年以来）

| 文件 | 格式 |
| ---  | ---    |
| [`report/cwe.report.md`](./report/cwe.report.md) | Markdown，两张 Top-10 表 —— top-10 markdown 是从上述两份 since-2024 的 TSV 中切片的 |

## 关于 x-cmd/cve

本仓库基于 [`CVEProject/cvelistV5`](https://github.com/CVEProject/cvelistV5) 构建每日更新的、按年份索引的 CVE 数据库。

本仓库即**生产端**：读取 [`CVEProject/cvelistV5`](https://github.com/CVEProject/cvelistV5)，按年抽取为一份精简的 9 列 TSV，xz 压缩后发布为 [GitHub Release 资源](https://github.com/x-cmd/cve/releases/tag/data)（`https://github.com/x-cmd/cve/releases/download/data/<name>.xz`）。**消费端**是 [`x cve`](https://x-cmd.com/mod/cve) shell 模块，按需下载、xz 解压、运行时无需联网访问上游。姊妹模块 [`x cwe`](https://x-cmd.com/mod/cwe) 用于浏览 CWE 目录。

### 用户如何获取 CVE 数据（4 条命令）

```sh
# 1. 浏览 —— 列出 / fzf 缓存的全部 CVE，最新的在最前
x cve
x cve fz

# 2. 按 id 查询单条 CVE（也支持 YYYY-NNNN 简写）
x cve info CVE-2024-0001
x cve info 2024-0001            # 效果同上，无需写前缀

# 3. 拉取 CVEProject/cvelistV5 的完整原始 JSON：
#    受影响的产品、参考、时间线、ADP 容器等
x cve detail CVE-2024-0001

# 4. 用 Shodan 的 CVE 数据库做补充 —— EPSS、KEV 列表、
#    漏洞利用文章、厂商公告，一次性聚合：
x shodan cve CVE-2024-0001
#    (https://x-cmd.com/mod/shodan/cve)
```

`x cve` 与 `x shodan cve` 可以干净地串联：

```sh
x cve fz | x shodan cve -      # 在 shodan 中预览全部 CVE
x shodan cve CVE-2024-0001     # 等价写法，不需要管道
```

无需 API key、无需 sudo、无需后台服务 —— `x cve` 是一个轻量的 shell 模块，背后依赖本仓库每日发布的 per-year TSV。

## 仓库结构（Repository layout）

```
.
├── .x-cmd/
│   ├── tsv.py              # 从本地 cvelistV5 clone 完整重建
│   ├── cwe.py              # MITRE CWE 目录镜像 → data/cwe.tsv + .slim.tsv
│   ├── cwe_zh.py           # MITRE 中文镜像 (cwe.org.cn) → data/cwe.zh.tsv（issue #2）
│   ├── cwe_report.py       # 聚合 data/cve-*.tsv ∩ data/cwe.slim.tsv (+ .zh.tsv) → report/cwe.report.{tsv,md,zh.md}
│   ├── report.py           # 按年统计 → report/cve.report.{tsv,md}
│   ├── latest.py           # 最新 N 条 → report/cve.latest-N.report.{tsv,md}
│   └── _cve_index.py       # 共享的解析 / IO 帮助函数
├── data/                   # 每次 CI 重建 —— 不入 git
│   ├── cve-YYYY.tsv        # 每年一份 TSV（按 CVE id 降序排列）
│   ├── index.tsv           # year \t rows \t file
│   └── cve.tsv.state.json  # 每文件 mtime（tsv.py 增量用）
├── report/                 # 每次 CI 重建 —— 入 git
│   ├── README.md           # 报表索引 + 方法论
│   ├── cve.report.{tsv,md} # 逐年统计
│   ├── cve.latest-10.report.{tsv,md}  # 最新 10 条 CVE
│   ├── cwe.top100.by-*.report.tsv  # CWE 排名 TSV（4 份）
│   └── cwe.report.{md,zh.md}  # CWE 排名 Markdown（since 2024，Top 10；zh.md 是中文 README 用）
└── .github/workflows/
    └── release.yml         # 每 4 小时：tsv.py --rebuild → 报表 → xz → 上传
```

`data/` 在每次 CI 运行时从零重建，所以 `main` 上的工作树保持小巧（脚本和 workflow 本身）。

## 行序 —— 最新优先

每份 `cve-YYYY.tsv` 按 **CVE id 降序** 排列：

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

`x cve` 消费端按反序遍历年份文件（`ls -r`），而每个文件本身就是反序的，所以直接 `cat` 就是「最新 CVE 在流的最前面」。不需要 `tac`，不需要对数据做二次扫描，没有任何惊喜。

为什么要反序存储？`x cve ls` 和 `x cve fz` 的用户关心 *最新* 的 CVE —— 当天发布的、最新爆出的高危。生产端的 `save_year_files` 用 `sort(reverse=True)` 对每个桶排序，让磁盘顺序和显示顺序一致。

## TSV 列（9 列）

| # | 列名   | 含义                                                                       |
| - | -------- | ----------------------------------------------------------------------------- |
| 1 | `cve`    | 完整 CVE id，例如 `CVE-2024-0001`。                                            |
| 2 | `year`   | 从 id 中解析出的年份段。                                                       |
| 3 | `no`     | 从 id 中解析出的数字段。                                                       |
| 4 | `vp`     | 来自 `containers.cna.affected[]` 的 `<vendor>/<product>;...`，用 `;` 连接。       |
| 5 | `ghsa`   | `references` 中的 GitHub Security Advisory id，用 `;` 连接；没有则为空。         |
| 6 | `score`  | 最高的 CVSS 基础分（v4.0 → v3.1 → v3.0 → v2.0，第一个命中即胜出）。              |
| 7 | `patched`| 如果 `containers.cna.solutions[]` 非空则为 `1`，否则为 `0`。                    |
| 8 | `cwe`    | CWE 编号（前缀已剥离），用 `;` 连接；没有则为空。                                |
| 9 | `desc`   | 英文描述，只取第一句（≤240 字符）。                                            |

第 9 列只保留第一句 —— Linux CNA 经常把完整的内核 slab dump（上千字节的 `fp=0x...` 十六进制）贴到描述字段。截断后每年的文件只有 ~1-9 MB，让 `x cve fz` 的列表更易扫读。

## 脚本

所有脚本零依赖（Python 3.8+ 标准库）。在仓库根目录运行：

```sh
# 从本地 cvelistV5 clone 完整重建（~350k 记录约 2 分钟）
python3 .x-cmd/tsv.py

# 强制重新解析每个文件（忽略 mtime 状态）
python3 .x-cmd/tsv.py --rebuild

# 拉取 MITRE CWE 目录 → data/cwe.tsv（完整 21 列）+
# data/cwe.slim.tsv（仅 id+name，用于 join）。
python3 .x-cmd/cwe.py

# 从 MITRE 中文镜像 (cwe.org.cn) 拉取 CWE 中文名 → data/cwe.zh.tsv。
# 30 天本地缓存；缺则 README.cn.md 自动回退英文。
python3 .x-cmd/cwe_zh.py

# 聚合交叉引用：每个 CWE 被多少 CVE 引用、平均分、最大分。
# 读取 data/cve-*.tsv + data/cwe.slim.tsv + data/cwe.zh.tsv。
python3 .x-cmd/cwe_report.py

# 最新 N 条 CVE（默认 10）→ 报告顶部表格。
# 只读每个 per-year TSV 的头部。
python3 .x-cmd/latest.py

# 逐年统计 → report/cve.report.{tsv,md}。
python3 .x-cmd/report.py
```

### CWE 数据 —— 我们发布什么、衍生什么

四份 `report/cwe.*.report.tsv` 文件已在上面的 [Reports](#报表reports) 段列出。本节只描述另外两份上游衍生的 MITRE CWE 目录文件：

| 文件 | 形态 | 来源 | 用途 |
| ---  | ---   | ---    | ---     |
| `data/cwe.tsv`        | 21 列 TSV (~3 MB)，包含 MITRE 所有字段 | MITRE 2000.csv 的字面镜像 | x-cwe 模块 + 任何想拿完整 CWE 目录、不愿访问 MITRE 的消费者 |
| `data/cwe.slim.tsv`   | 2 列 TSV (~50 KB)，仅 `CWE-ID` + `Name` | 从 `data/cwe.tsv` 派生 | 在 cwe_report.py 中与 `data/cve-*.tsv` 做 join |



| 文件 | 形态 | 来源 | 用途 |
| ---  | ---   | ---    | ---     |
| `data/cwe.tsv`        | 21 列 TSV (~3 MB)，保留 MITRE 所有字段 | MITRE 2000.csv 的字面镜像（表头行，空格替换为 `_`） | x-cwe 模块，以及任何想要完整 CWE 目录、不想访问 MITRE 的消费者 |
| `data/cwe.slim.tsv`   | 2 列 TSV (~50 KB)，`CWE-ID\tName` | 从 `data/cwe.tsv` 派生（行序一致） | 在 cwe_report.py 中与 `data/cve-*.tsv` join |
| `report/cwe.top100.by-*.report.tsv` | 5 列 TSV (~6 KB)，`cwe_id\tname\tcve_count\tavg_score\tmax_score`，**Top 100**（共 4 份：by-count/by-score × all/since-2024） | 从 `data/cve-*.tsv` ∩ `data/cwe.slim.tsv` 聚合 | 给需要 top-N 数据的工具直接消费 |
| `report/cwe.report.md`  | Markdown，含两张 Top-10 表（since 2024） | 同上，切片到 Top 10 | 由 release.yml 的 inline 步骤拼接到 README 顶部 |

**为什么要镜像 CWE 目录**：上游 MITRE 2000.csv.zip 是 644 KB，解压后的 csv 约 3 MB。xz 压缩到约 150 KB。我们能负担得起一份完整镜像，且让离线消费者获得与 MITRE 完全相同的数据，不必再走一次网络。TSV 保留了 MITRE 的列名（只是空格 → 下划线），下游代码可以同时使用两种格式。

**为什么现在还不把 per-CVE 目录作为 release asset 发布**：x-cwe 模块目前是从 MITRE 自己拉 2000.csv 并在本地缓存（`~/.x-cmd.root/local/data/cwe/`）。未来版本的 x-cwe 可以选择从本仓库的 release 中读 `data/cwe.tsv`，但目前还没接通。

## 持续集成（CI）

`.github/workflows/release.yml` 每 4 小时（每小时 37 分，避开整点高峰）跑一次，外加手动触发。每次运行：

1. 克隆 CVEProject/cvelistV5（depth 1）并执行 `.x-cmd/tsv.py --rebuild` 以刷新 `data/cve-*.tsv`。
2. 从 MITRE 重新生成 `data/cwe.tsv` + `data/cwe.slim.tsv`（`.x-cmd/cwe.py`），以及 CWE 交叉引用报表（`.x-cmd/cwe_report.py` → `report/cwe.*.report.tsv` 与 `report/cwe.report.md`）。
3. 重新生成逐年统计报表（`.x-cmd/report.py` → `report/cve.report.{tsv,md}`）。
4. 把两份报表 markdown 拼接到 `README.md`（以及本中文版 `README.cn.md`）的最前面（BEGIN/END 标记保证幂等），然后把 `README.md`、`README.cn.md` 加七份 `report/*` 文件一起 commit 回 `main`（若没有改动则跳过），让 github.com 上的 README 永远跟着最新数据走。
5. 对每个有变动的 per-year 文件做 xz 压缩（`xz -9`，体积约缩 85%），替换对应的 release asset，强制移动 `data-packaged` git tag 让下次 diff 仍然正确。

`.xz` 文件不入 `main` —— 二进制归 release asset，源码归源码。per-year `data/cve-*.tsv` 与 CWE 目录（`data/cwe.tsv`、`data/cwe.slim.tsv`）在这个流程下也不入 git；只有衍生报表和 README 会 commit 回去，让 git 历史聚焦在真正的代码改动上。

## 许可证（License）

Apache License 2.0 —— 见 [`LICENSE`](./LICENSE)。

底层的 CVE 记录派生自 [CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5)，后者以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 发布。下游消费者使用这些 TSV 时必须保留该署名。

## 相关链接（Related）

- [x-cmd/cve 模块文档](https://x-cmd.com/mod/cve) —— 消费端（shell 模块）
- [x-cmd/cwe 模块文档](https://x-cmd.com/mod/cwe) —— 姊妹模块
- [x-cmd/x-cmd](https://github.com/x-cmd/x-cmd) —— 模块源码（`mod/cve/`）
- [CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5) —— 上游数据

## 常见问题（FAQ）

### 什么是 CVE？

**CVE**（Common Vulnerabilities and Exposures，公共漏洞和暴露）
是 MITRE 在美国国土安全部资助下维护的公开漏洞目录——每一份
公开披露的计算机安全漏洞都会拿到一个唯一 id（`CVE-YYYY-NNNN`），
加上英文简短描述、受影响的厂商/产品、CVSS 基础分、漏洞类别
（[CWE](https://cwe.mitre.org/)）。截至 2026 年，目录里有
约 37 万条记录，最早可追溯到 CVE-1999-0001。

### 什么是 CWE？

**CWE**（Common Weakness Enumeration，通用缺陷枚举）是软件
弱点**类型**的分类体系——比如「跨站脚本」「释放后重用」「路径遍历」
这类「错误模式」分类。每条 CVE 在 `problemTypes[]` 字段里引用
一个或多个 CWE id；本仓库把两份目录 join 起来，让你不用扫 37 万
条 CVE 也能回答「今年出了多少 XSS 漏洞？」。完整 CWE 目录在
[`data/cwe.tsv`](./data/cwe.tsv)，精简 id→name 映射在
[`data/cwe.slim.tsv`](./data/cwe.slim.tsv)。

### CVE 和 CWE 有什么区别？

- **CVE** = 某个**具体**漏洞（例如 CVE-2026-90616：Flatpak
  在 1.18.1 之前存在沙箱逃逸）。
- **CWE** = 该漏洞归属的**类别**（例如 CWE-22：路径遍历）。

一条 CVE 通常引用一个或多个 CWE id 来描述弱点类别。本仓库
按 CWE 聚合 CVE 数，排出「最常犯的错误」。

### 最常见的 CWE 弱点是哪些？

本页顶部 **Top 10 CWE by CVE count** 表给出 2024 年以来
最常被引用的弱点类别。本仓库本次运行时头部大致是：

1. [CWE-79](https://cwe.mitre.org/data/definitions/79.html) — 跨站脚本 (XSS)
2. [CWE-89](https://cwe.mitre.org/data/definitions/89.html) — SQL 注入
3. [CWE-862](https://cwe.mitre.org/data/definitions/862.html) — 缺少授权
4. [CWE-22](https://cwe.mitre.org/data/definitions/22.html) — 路径遍历
5. [CWE-94](https://cwe.mitre.org/data/definitions/94.html) — 代码注入
6. [CWE-78](https://cwe.mitre.org/data/definitions/78.html) — OS 命令注入
7. [CWE-416](https://cwe.mitre.org/data/definitions/416.html) — 释放后重用
8. [CWE-20](https://cwe.mitre.org/data/definitions/20.html) — 输入验证不当
9. [CWE-125](https://cwe.mitre.org/data/definitions/125.html) — 越界读取
10. [CWE-352](https://cwe.mitre.org/data/definitions/352.html) — CSRF

XSS 和 SQL 注入自 CVE 体系建立以来每年都在榜上。Top-100
（全部年份 / since 2024 两个窗口）见
[`report/cwe.top100.by-cve-count.report.tsv`](./report/cwe.top100.by-cve-count.report.tsv)。

### 最危险的（CVSS 最高）CWE 类别是哪些？

**Top 10 CWE by average CVSS score** 表按「引用该 CWE 的 CVE
平均 CVSS 基础分」排序（至少 10 个样本，避免单 CVE 极值干扰）。
头部通常被这些类别占据：

- [CWE-506](https://cwe.mitre.org/data/definitions/506.html) — 嵌入式恶意代码
- [CWE-95](https://cwe.mitre.org/data/definitions/95.html) — Eval 注入
- [CWE-502](https://cwe.mitre.org/data/definitions/502.html) — 不受信任数据反序列化
- [CWE-288](https://cwe.mitre.org/data/definitions/288.html) — 替代通道认证绕过
- [CWE-121](https://cwe.mitre.org/data/definitions/121.html) — 栈缓冲区溢出

这些是「一旦犯下后果最严重」的类别。每次 CI 都会重新生成——
完整 Top-100 见
[`report/cwe.top100.by-cve-score.report.tsv`](./report/cwe.top100.by-cve-score.report.tsv)。

### 最新发布的 CVE 是哪些？

页面最顶部 **「最近 10 个 CVE」** 表就是答案。每 4 小时直接从
MITRE 源重新生成，与「当下」最多差几小时。机器可读版本：
[`report/cve.latest-10.report.tsv`](./report/cve.latest-10.report.tsv)，
或 `python3 .x-cmd/latest.py N` 拿任意 N。

### 每年发布多少 CVE？

页面里的「CVE 增长得有多快？」逐年表给出每年总量、已打分
条目数、平均分、最高分。简要回答：过去五年 CVE 总量翻了将近
一番，2026 年仅前三季度已经超过 5.6 万条。逐年 TSV：
[`report/cve.report.tsv`](./report/cve.report.tsv)。

### 怎么查单条 CVE？

按 id 查（如 `CVE-2024-0001`）的话，上游权威是
[NVD 详情页](https://nvd.nist.gov/vuln/detail/CVE-2024-0001)。
本仓库的姊妹模块 [`x cve`](https://x-cmd.com/mod/cve)
让你离线查：

```sh
x cve info CVE-2024-0001
x cve info 2024-0001            # 也支持 YYYY-NNNN 简写
x cve detail CVE-2024-0001      # 完整上游 JSON
```

`x cve` 读的就是本仓库 per-year TSV，下载一次 release asset
即可离线用。

### 怎么下载完整 CVE 数据库？

三种方式，全部免费、无需鉴权：

```sh
# 1. 指定某一年（最小体积，约 5 MB xz）
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz \
    | xz -dc > cve-2026.tsv

# 2. 整个目录一份 tarball（约 21 MB xz）
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-all.tar.xz \
    | tar -xJ

# 3. 仅 CWE 目录（约 150 KB xz，约 3 MB 原文）
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cwe.tsv.xz \
    | xz -dc > cwe.tsv
```

每次上游变更后 4 小时内重打包。所有文件都是普通制表符分隔
TSV——schema 见 [TSV 列（9 列）](#tsv-列9列)。无 API key，
无限速。

### 怎么按 CWE / 厂商 / CVSS 查 CVE？

TSV 9 列含义见 [TSV 列（9 列）](#tsv-列9列)。因为是纯文本，
标准 Unix 工具就够：

```sh
# 2024 年以来所有 score >= 7.0 的 XSS
xz -dc cve-2024.tsv xz -dc cve-2025.tsv xz -dc cve-2026.tsv 2>/dev/null \
    | awk -F'\t' '$8 ~ /(^|;)79(;|$)/ && $6+0 >= 7'

# 当年所有影响 Apache HTTP Server 的 CVE
xz -dc cve-2026.tsv \
    | awk -F'\t' '$4 ~ /Apache\/HTTP Server/ {print $1, $6, $9}'

# 2024 年以来按厂商统计 CVE 数
xz -dc cve-2024.tsv xz -dc cve-2025.tsv xz -dc cve-2026.tsv 2>/dev/null \
    | awk -F'\t' '{ for (i=1;i<=split($4,p,";");i++) print p[i] }' \
    | sort | uniq -c | sort -rn | head -20
```

仓库 release 也预聚合了常见查询结果——见
[`report/`](./report/) 下的 Top-100 CWE 排名。

### 中文 CWE 名从哪儿来？

CWE 排名表里的中文名来自 [cwe.org.cn](https://cwe.org.cn)——
MITRE 官方中文镜像。抓取脚本
[`.x-cmd/cwe_zh.py`](./.x-cmd/cwe_zh.py) 每次 CI 跑一次，
输出 [`data/cwe.zh.tsv`](./data/cwe.zh.tsv)（覆盖 969 个 CWE
中约 91%）。剩下的 9%（多数是 view 和已废弃 id）渲染时
自动回退英文名——见
[issue #2](https://github.com/x-cmd/cve/issues/2)。要强制
重抓：`python3 .x-cmd/cwe_zh.py --force`。

### 有中文 CVE 数据库 / 中文版吗？

本仓库的中文版是 [`README.cn.md`](./README.cn.md)。同样的
数据，中文呈现：

- CWE 名来自 MITRE 官方中文镜像。
- 顶部「最近 10 个 CVE」表。
- 「工程师们最常犯的错误是什么？」CWE 排名表。
- 「CVE 增长得有多快？」逐年统计表。
- 末尾「常见问题（FAQ）」。

中文名缺失自动回退英文——不丢任何数据。

### 数据多久更新一次？

发布 workflow 每 4 小时跑一次（`37 */4 * * *` UTC，外加每次
push 到 `main`）——见
[`.github/workflows/release.yml`](./.github/workflows/release.yml)。
MITRE 一有新 CVE 公布，最多 4 小时就出现在这里。README
顶部「数据截至：YYYY-MM-DD」时间戳从刚拼接的
`report/cve.report.md` 里抽出，永远跟数据一致。

### 可以商用吗？

可以，但有一个署名要求。本仓库脚本、`report/*` 衍生报表、
本 README 走 [Apache License 2.0](./LICENSE)。底层 CVE
记录本身由 [CVEProject](https://github.com/CVEProject) 按
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
发布——商用没问题，只要保留署名并注明你做的修改。同样的
要求适用于衍生品（漏洞扫描器、SBOM 工具、威胁情报仪表盘）。

### 怎么把数据集成进自己的脚本？

三种套路：

1. **下载 asset 然后 grep/awk。** 纯 TSV，最简单：
   `curl ... | xz -dc | awk ...`。无 SDK、无第三方库。

2. **用 [`x cve`](https://x-cmd.com/mod/cve) shell 模块。**
   它包了一层 TSV，提供 `x cve ls`、`x cve fz`、
   `x cve info CVE-YYYY-NNNN`、`x cve detail CVE-YYYY-NNNN`、
   `x cve cwe CWE-NN`。安装后跑 `x cve --help`。

3. **直接读上游 [cvelistV5 仓库](https://github.com/CVEProject/cvelistV5)。**
   本仓库用同一个源——见 [`.x-cmd/tsv.py`](./.x-cmd/tsv.py)
   里的解析模式，自己接 JSON pipeline 时可以参考。

### 跟 NVD / OSV.dev / GHSA 有什么区别？

四份数据都派生自 CVE，但答的问题不同：

- **NVD (nvd.nist.gov)** — 权威 CVSS 分 + CPE 字典；REST API；
  有速率限制。
- **OSV.dev** — 漏洞数据关联到包生态（npm / PyPI / Maven
  等）；做 SCA 工具很合适。
- **GHSA (GitHub Security Advisories)** — 社区维护、生态感知
  （Dependabot alerts）。
- **本仓库** — 上游 cvelistV5 目录的精简镜像 + 衍生排名
  （按 CVE 数 / 按评分 / 逐年体量）+ 预聚合统计。专为
  「扫 / grep / awk」工作流优化，不是 REST API。

看场景选。「现在最糟糕的 CWE 类别是什么？」「给我快速 top-N」
走本仓库最快；做生产级漏洞管理用 NVD / OSV / GHSA，那边有
正经 API 和生态关联。

### 发现 bug / 缺数据 / 中文名错了怎么办？

按问题类型分三个地方：

- **本仓库 pipeline 的 bug**（错排序、缺行、死链）：开
  [issue](https://github.com/x-cmd/cve/issues)。
- **缺或错的 CVE 记录**：数据直采自
  [CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5)，
  权威修复在那里提交。
- **中文 CWE 名错或缺**：上游是 MITRE 官方中文镜像的
  `https://cwe.org.cn/data/definitions/<id>.html`。在那里或
  这里开 issue 即可；上游修好后下一次定时任务会自动重抓。
  立刻强制重抓：`python3 .x-cmd/cwe_zh.py --force`。
