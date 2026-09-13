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
