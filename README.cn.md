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

### 数据从哪儿来？

直接来自 [CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5)——
MITRE 官方的 JSON 仓库，存放每一份已发布的 CVE。仓库里的
[`.x-cmd/tsv.py`](./.x-cmd/tsv.py) 在每次 CI 运行时克隆该仓库一次，
遍历 `cves/YYYY/NNxxx/CVE-YYYY-NNNNN.json`，输出 `data/` 下 9 列的精简
TSV。不抓网页、不要上游 API key，描述和 CWE 列表除折叠空白外不做任何变换。

### 数据多久更新一次？

发布 workflow 每 4 小时跑一次（`37 */4 * * *` UTC，
见 [`.github/workflows/release.yml`](./.github/workflows/release.yml)），
另在每次 push 到 `main` 时也跑。MITRE 一有新 CVE 公布，最多 4 小时内就
会出现在这里。README 顶部的「数据截至：YYYY-MM-DD」是真值时间戳——
它从刚拼接的 `report/cve.report.md` 里抽，所以永远和数据本身一致。

### 为什么不直接出 Top 100 / 全表？

Top 10 是「统计上仍然站得住脚」的最小数字：每行背后聚合几百到几万条
CVE，列表头部跨日运行足够稳定。Top 100 在
[`report/cwe.top100.by-*.report.tsv`](./report/) 里——`x cve ls` 等
真正消费全表的工具读的是 TSV，不是 README 渲染的 markdown。
`data/cve-*.tsv` 是 9 列全量，只截了描述首句。

### 为什么要拆成 per-year 文件而不是一个大文件？

per-year 切分正好对齐上游 `cvelistV5` 的目录布局（一年一个文件夹），
rebuild 就是一次干净的本地遍历——只有 2026 变了的话不必重头解析。
也让 `x cve` 消费端可以只下感兴趣的年份：`cve-2026.tsv.xz` 大约
5 MB，整个 `cve-all.tar.xz` 大约 21 MB。git 里看 per-year diff 也很直观，
一眼能看出今年新增了哪些行。

### 为什么之前「Top id 永远停在 9999」？

真 bug，已修。提交 `46759ff`
（[issue #3](https://github.com/x-cmd/cve/issues/3)）。MITRE 从 2025 年
左右开始发 5 位序号（`NNNN >= 10000`）的 CVE，老的字典序排序把 `9999`
排在 `10000`–`99999` 前面，导致 `x cve | head` 永远停在 `CVE-YYYY-9999`。
现在按 NNNN 整数排序，真正的最高 id（例如 `CVE-2026-90616`）能正确显出来。

### 「Top 10 CWE by CVE count」到底在算什么？

每条 CVE 可以列出 1 个或多个 CWE id（它归属的弱点分类）。对 MITRE
目录里的每个 CWE，统计时间窗口内有多少 CVE 引用它，按计数倒序排序。
「since 2024」窗口剔除了 2024 年之前的 CVE，所以排名反映的是「工程师
*现在* 还在犯哪些错」——加上 2008 年的 SQL 注入雪崩只会让
[SQL 注入](https://cwe.mitre.org/data/definitions/89.html) 永远排第一。

### 「Top 10 CWE by avg CVSS score」呢？

同样的 `cwe` join，但每个 CWE 取其 CVE 的 CVSS base score **均值**（至少
10 个样本，防止单 CVE 极值干扰）。回答的是「哪个错误一旦犯下后果最严重」，
而不是「哪个错误最常犯」。榜单头部是 CWE-506（嵌入式恶意代码）和
CWE-95（动态代码求值注入），因为这些 CVE 几乎都打 9+ 分。

### 中文 README 里的 CWE 中文名从哪来？

我们从 [cwe.org.cn](https://cwe.org.cn)——MITRE 官方中文镜像——抓。
抓取脚本在 [`.x-cmd/cwe_zh.py`](./.x-cmd/cwe_zh.py)，输出
[`data/cwe.zh.tsv`](./data/cwe.zh.tsv)（969 条 CWE 目录里覆盖约 91%，
剩下的 9% 大多是 view 和已废弃 id，中文站暂未翻译）。中文表里缺失
的中文名会自动回退到英文名，对应
[issue #2](https://github.com/x-cmd/cve/issues/2) 的要求。

### 不装 `x cve` 能用这些数据吗？

可以。release asset 就是普通的 xz 压缩 TSV：

```sh
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-2026.tsv.xz \
    | xz -dc | head -5
```

或者一次性拉整个 bundle：

```sh
curl -fsSL https://github.com/x-cmd/cve/releases/download/data/cve-all.tar.xz \
    | tar -xJ -C ./local-cve
```

列含义见下面 [TSV 列（9 列）](#tsv-列9列) —— 9 列全是公开 schema，
不依赖任何 API key。

### 本地怎么跑这些脚本？

[`.x-cmd/`](./.x-cmd/) 下六个脚本零依赖（Python 3.8+ 标准库）：

```sh
python3 .x-cmd/tsv.py --src /path/to/cvelistV5/cves --out data --rebuild
python3 .x-cmd/cwe.py                 # MITRE CWE 目录 → data/cwe.tsv
python3 .x-cmd/cwe_zh.py              # MITRE 中文镜像 → data/cwe.zh.tsv
python3 .x-cmd/cwe_report.py          # Top-N CWE 排名 → report/cwe.report.{tsv,md,zh.md}
python3 .x-cmd/report.py              # 逐年统计 → report/cve.report.{tsv,md}
python3 .x-cmd/latest.py              # 最新 N 条 → report/cve.latest-N.report.{tsv,md}
```

六个都从 `data/` 读、写到 `report/`。只有 `tsv.py` 需要联网 clone
`cvelistV5`，其余纯本地。CI 跑的完整流水线见
[持续集成（CI）](#持续集成ci)。

### 许可证？

我们自己写的（脚本、本 README、`report/*` 衍生报表）走 Apache 2.0，
见 [`LICENSE`](./LICENSE)。底层 CVE 记录是 CVEProject 的 CC BY 4.0——
分发 per-year TSV 时请保留该署名。

### 中文表里某条 CWE 名错了 / 缺失怎么办？

中文词典每次 CI 都从 cwe.org.cn 重新抓取，本地缓存放在
`.x-cmd/.cwe_zh.cache/`，30 天过期。如果某个名字错了，上游源头是
`https://cwe.org.cn/data/definitions/<id>.html`——在那里或这里开 issue
即可，下一次定时任务跑完后会自动刷新。要立刻强制重新抓：
`python3 .x-cmd/cwe_zh.py --force`。
