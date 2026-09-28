# Log

## R0
taxonomy v0 定稿：分类轴＝协议连接哪两端（模型↔工具 / agent↔agent / client↔agent子进程 / agent↔前端UI）。10 个维度，5 个核心实体 + 大厂矩阵。计划 R1 spawn 6 个 worker，按来源边界拆（5 实体 + 1 vendor scout）。

## R1（6 spawn，全部成功，无重派）
观察：
- 核心矩阵 5×10 格基本全部 ✅（MCP 关系列=∅，官方未提；其余均有一手来源+原句）。
- Q1（ACP-IBM vs ACP-Zed）三方独立证实为**不同协议**：ACP-IBM 已于 2025-08-27 归档并入 A2A（agent↔agent, HTTP/REST），ACP-Zed 是 Zed/JetBrains 的 editor↔agent 协议（JSON-RPC2.0 over stdio，类比 LSP）。结论稳固，无需再核验。
- Q2（MCP SSE 是否废弃）已用官方 deprecated 页面原句解决：独立的 "HTTP+SSE transport" 于 spec 2025-03-26 标记 Deprecated（SEP-2596），被 Streamable HTTP 取代；但 SSE 本身作为 Streamable HTTP 内部的可选流式选项被保留。结论稳固。
- 新发现（scout leads）：OpenAI 还有一个同缩写 "Agentic Commerce Protocol"（电商支付场景，与 IBM/Zed 的 ACP 无关）——用户"ACP 有两个"的疑问实际上还有第三个撞名协议，需要一手来源核实后写入辨析。
- 治理时间线冲突：r1-scout 称 Anthropic"2025年3月"把 MCP 捐给 Agentic AI Foundation（AAIF）；但 r1-a2a 记录 A2A 直到 2026-08-17/27 才"加入 AAIF"，且用语是"a new chapter"（暗示 AAIF 此前对 A2A 是新关系）。MCP 官方治理页自称 "a Series of LF Projects, LLC"（Linux Foundation 项目壳，而非直接说 AAIF）。日期/机构关系对不上，需要核验一手来源（可能是 worker 记错年份，2025 vs 2026）。
- AG-UI 治理="未捐赠给中立基金会，CopilotKit 主导"是一条否定/边界主张，worker 自己在 leads 里标注"需确认治理模式未改变"，尚未反证。
- 大厂矩阵里 ACP-Zed 列全部只有二手来源（The Register 一篇文章），且与 ACP-Zed 官方 adopter 列表（含 Claude Code、Codex CLI）有微妙差异（"被列为 adopter"≠"厂商原生支持"，需要区分"Zed 造的桥接适配器"和"厂商原生实现"）。

动作：R2 派 4 个定向 worker（少于 R1 的 6 个，符合"逐轮更窄"要求）：
1. r2-governance：核验 MCP/A2A/ACP-IBM 与 Linux Foundation / Agentic AI Foundation 的准确关系与时间线（反证 r1-scout 的"2025年3月"日期）
2. r2-acp3-openai：核实 OpenAI Agentic Commerce Protocol 官方定义、范围、与 ACP-IBM/ACP-Zed 无关联
3. r2-agui-governance：反证"AG-UI 未捐赠给基金会"——查 AG-UI 官方/CopilotKit 近期公告
4. r2-acpzed-vendors：把大厂 × ACP-Zed 列从二手来源升级为一手来源（Zed 官方 adopter 页 + 各厂/GitHub tracking issue 原句），区分"原生支持"vs"桥接适配器"
预计 spawn：4

## R2 收束
notes_lint：10 份笔记，150 条主张（official 100/secondary 50），12 conflicts（多数已在 R2 定向解决），26 gaps，26 leads。
grid 更新：核心矩阵 96%（48/50）✅/∅，仅剩 2 个 ⚠（ACP-IBM×鉴权只有二手源——协议已停用，不再追；AG-UI×采用者——大厂未官方采用，这本身就是已核实的结论，非缺口）。0 个 ⚔ 冲突残留。
taxonomy：v0 的分类轴（连接哪两端）和次轴（治理谱系）都被 R1+R2 证据支持，未改轴。维度从 10 精简为 9（"采用者"移出核心矩阵、并入大厂矩阵，避免重复）。
两个用户疑点均已给出结论：Q1 否（且额外发现第三个撞名 ACP）；Q2 部分废弃（迁移不是移除）。
report.md 重写：9000/9000 字符（压到预算线，经 5 轮压缩：合并一屏看懂条目、砍坑清单重复表述、来源节去修饰词、矩阵单元格短语化）。

观察：核心格子已 96% ✅/∅，0 冲突残留；一屏看懂和两个疑点结论涉及的边界主张（AG-UI 治理否定、ACP-Zed 厂商支持真伪、治理时间线）均已在 R2 反证/核验过，且反证未推翻原结论。剩余 2 个 ⚠ 都是低价值（一个是已停用协议的次要细节，一个是"未采用"这个事实本身已经查实、只是采用深度这个次维度还欠数据但不影响正文结论）。继续扩展只是边际调查，不产出新的读者认知。
→ 动作：进入终审（不再扩展）。派 1 个审稿 worker 核对 report.md 对 notes 的支撑度。
预计 spawn：1

## R3 终审（1 spawn）
审稿 worker 均匀抽查 24 条具体主张（覆盖全部章节，含 ACP 撞名、治理时间线、大厂矩阵符号、未决项四类高风险内容），结果：supported 24/24，weak 0，unsupported 0，contradicted 0。详见 ds/audit.md。
指出 2 处可精修（均非错误）：① Anthropic×ACP-Zed 标 ◐ 的依据是"官方渠道未提及"而非"明确否认"，已经在矩阵单元格文字里写明"经Zed适配器,非原生"，不再额外改动；② A2A 治理日期"2025-06"精度低于 MCP 的"2025-12-09"——已改为"2025-06-23"，靠精简来源标题([8])腾出 3 字符空间，最终 8995/9000 字符，未破预算。
两个用户疑点、taxonomy、核心矩阵、大厂矩阵均已定稿，无遗留 ⚔ 冲突。终止扩展，报告定稿。

## 收尾统计
- 总 spawn：11（R1: 6 + R2: 4 + R3: 1），无失败重派。
- 字数轨迹：r2快照 9000 → 终稿 8995（budget 9000，全程未超）。
- grid 填充率：48/50 (96%) ✅/∅，2 个 ⚠ 均为已核实但证据强度较低的次要格（已停用协议的鉴权细节；"未被大厂采用"这一事实本身已证实，仅"采用深度"子维度缺数据）。
- 两个用户点名疑点均有明确结论（见 report.md 一屏看懂 #2、#3）；额外发现第三个撞名 ACP（OpenAI Agentic Commerce Protocol）。
