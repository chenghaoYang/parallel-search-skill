# Taxonomy 网格 v2（R2 收束后）

## 状态总览
Grid A（5 个基本面协议）✅ 全部一手来源填充。Grid B（4 大厂 × 5 列）✅ 全部填充，多数 official。「三个 ACP」✅ 已确认+分级（2 死 1 活）。AAIF 治理 ✅ 精确日期+原句。

## 分类轴（不变）
协议连接的「两端」是谁。

| 家族 | 两端 | 成员 |
|---|---|---|
| Agent ↔ 工具/数据 | agent 运行时 ↔ 外部工具、API、数据源 | MCP ● |
| Agent ↔ Agent | 独立 agent/系统跨主体协作 | A2A ●；ACP-IBM ✝→A2A（2025-08-29 并入，官方原句）；AGNTCY-ACP ✝→A2A（2026-04-11 仓库归档） |
| Agent 后端 ↔ 用户界面 | agent 逻辑 ↔ 前端/聊天 UI | AG-UI ● |
| 宿主应用 ↔ 本地 Agent | 编辑器/IDE ↔ 它拉起的 agent 子进程 | ACP-Zed ● |

**关键叙事**：agent↔agent 家族里，A2A 是唯一幸存者——IBM 和 AGNTCY 的"ACP"都并入/让位于它；Zed 的 ACP 活着是因为它本来就不在这个家族。

## Grid B：大厂支持面 — ✅ 已填（R2）
| Vendor | MCP | A2A | ACP | AG-UI | 自家变体 |
|---|---|---|---|---|---|
| OpenAI | ✅ 多产品线+MCP steering committee | ❌ 仅GitHub issue | ❌ 无证据 | 🔄 In Progress | AgentKit/Realtime API/Agentic Commerce Protocol |
| Anthropic | ✅ 起源方 | 🔄 webinar级，未集成 | ❌ 明确拒绝(not planned) | ❓ 无声明 | Skills/Computer Use |
| Google | ✅ 2025-12-11官宣 | ✅ 起源方+A2A Extension | ✅ Zed ACP参考实现 | ✅ 2025-09-26集成 | ADK/A2A Extension |
| Microsoft | ✅ 5条产品线GA/preview | ✅ Foundry GA+TSC成员 | ❌ 无直接；AHP可用ACP做后端 | ✅ Agent Framework | NLWeb/M365 Agents SDK/AHP |

## R2 新发现 vs R1 假设
- AGNTCY 的 "Agent Connect Protocol (ACP)" 一手来源确认存在（github.com/agntcy/acp-spec 官方仓库），但已于 2026-04-11 归档弃用，secondary 来源称"deprecated in favor of A2A" → 疑点①从"两个"变"三个"，且三个里两个已经并入 A2A。
- MCP→AAIF 治理转移：一手来源确认，精确到日期（2025-12-09）和原句（Mike Krieger 引言）。
- 新增细节：A2A 本身后来（据称 2026-08）也作为 "hosted project"（非 founding）加入 AAIF——但这个具体日期目前只有 secondary/不完整来源支撑（r2-aaif-governance C7 标注"搜索结果摘要，需进一步核实"）。**这条主张写进了 report 的「一屏看懂」和矩阵，按规则属于「影响大」的主张，R3 应核实或软化。**
- Outshift 官方博客称 ACP 是"AGNTCY 架构核心组件"，但 Linux Foundation 官方"四大基础设施"列表未列入 ACP——两个一手来源对 ACP 地位描述不一致，docs.agntcy.org 关键页 404。

## R2 收束
report.md 从 5763 → 6955 字符（budget 9000，余量 ~2000）。snapshots/report.r2.md 已存。

## R3 计划（2 workers，收尾核实，不求大而求准）
r3-aaif-a2a-date → 核实"A2A 于 2026-08 作为 hosted project 加入 AAIF"的一手来源和确切日期；找不到就明确记录，report 里软化措辞
r3-agntcy-status → 找 AGNTCY/Linux Foundation 官方（非 GitHub 归档横幅）对 ACP 现状/与 A2A 关系的权威表述，解决 Outshift vs LF 列表不一致
