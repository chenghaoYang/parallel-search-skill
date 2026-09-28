# audit

## 抽查主张（25条）

| 判定 | 主张原文（report.md 里的句子或表格单元格） | 依据（笔记路径+[C#] 或"笔记里找不到"） | 备注 |
|---|---|---|---|
| supported | "ACP"撞名撞了三次...三者除了缩写一样，互相没有继承关系 | r1-acp-ibm.md C5, r1-acp-zed.md C1, r2-agntcy-acp.md C1-C4, C9 | 笔记明确列举三个不同的 ACP 及各自定义，无继承关系 |
| supported | MCP 的 SSE 传输于 2025-03-26 标记 deprecated，2026-07-28 正式 reclassify | r1-mcp.md C7, C8 | 原句匹配："Reclassify the HTTP+SSE transport (deprecated since protocol version 2025-03-26) as Deprecated" |
| supported | MCP 替代方案 Streamable HTTP | r1-mcp.md C9, C10 | 原句："Migrate to Streamable HTTP"，"introduced in protocol version 2025-03-26 as a replacement" |
| supported | A2A 于 2025-06-23 由 Google 捐赠给 LF | r1-a2a.md C3 | 原句：Google 转移协议给 LF，2025-06-23 日期匹配 |
| supported | A2A 于 2026-08-17 官宣加入 AAIF 作为 hosted project | r3-aaif-a2a-date.md C1, C2 | 原句："2026-08-17"，"joining the Agentic AI Foundation (AAIF) as a hosted project" |
| supported | MCP 2025-12-09 成立的 AAIF 三个 founding contribution 之一 | r2-aaif-governance.md C1, C2 | 原句：AAIF 成立 Dec 9, 2025，"Anthropic's Model Context Protocol (MCP)...founding contributions" |
| supported | 三个协议通常被同一个 agent 同时使用 [4] | r1-ag-ui.md C27, C28 | 原句："The three protocols are complementary rather than competing"，"individual agents commonly utilizing all three simultaneously" |
| supported | MCP 连接"agent↔工具/数据" | r1-mcp.md C1 | 原句："connect to data sources...tools...and workflows" |
| supported | A2A 连接"agent↔agent" | r1-a2a.md C1 | 原句："facilitate communication and interoperability between independent...AI agent systems" |
| supported | AG-UI 连接"agent 后端↔用户界面" | r1-ag-ui.md C1 | 原句："bi-directional connection between a user-facing application and any agentic backend" |
| supported | ACP-Zed 连接"编辑器↔本地 agent 子进程" | r1-acp-zed.md C1 | 原句："standardizes communication between code editors...and coding agents" |
| supported | MCP 版本 2026-07-28 | r1-mcp.md C5 | 原句："released version 2026-07-28 on July 28, 2026" |
| supported | A2A v1.0.1（2026-05-28） | r1-a2a.md C5 | 原句："v1.0.1 (released May 28)" |
| supported | AG-UI v1.0（2026-09-17） | r1-ag-ui.md C8 | 原句："2026-09-17...TypeScript/npm @ag-ui/client reached 1.0.0" |
| supported | ACP-Zed v1 稳定（2026-06-24）| r1-acp-zed.md C22 | 原句："Rust Crate v1.0.0 published_at: 2026-06-24" |
| supported | MCP 鉴权 OAuth 2.1 + RFC6750/8707/9207 | r1-mcp.md C13-C16 | 原句中规定 OAuth 2.1、RFC 6750 Bearer tokens、RFC 8707 resource indicators、RFC 9207 issuer验证 |
| supported | A2A 鉴权支持 OAuth2/API key/mTLS/HTTP Basic，强制 TLS1.2+ | r1-a2a.md C9, C13 | 原句："Credentials travel in standard HTTP headers...OAuth2 tokens or API keys"，"TLS 1.2 or higher" |
| supported | OpenAI MCP ✅ 官方支持 | r2-openai.md C1, C2, C9 | 原句：Agents SDK 支持 MCP，Responses API 支持 remote MCP，加入 MCP steering committee |
| weak | Anthropic A2A "🔄 办过 MCP+A2A 联合 webinar，产品未集成" | r2-anthropic.md C1, C10 | C1 原句确实说办过 webinar；C10 说 GitHub issue 开放（未决策），但未直接说"产品未集成"，推论稍过度 |
| supported | Google A2A ✅ 起源方；ADK + 专有 A2A Extension | r2-google.md C7, C10 | 原句：Google 为起源方，A2A Extension 改进可靠性 |
| supported | Microsoft A2A ✅ Azure AI Foundry A2A v1.0 GA + TSC 成员 | r2-microsoft.md C6, C7 | 原句：支持 A2A v1.0 GA，Microsoft 是 TSC 成员 |
| supported | ACP-IBM 并入 A2A，仓库归档 2025-08-27 | r1-acp-ibm.md C5, C8 | 原句："joins forces"、"merging"，仓库"archived on August 27, 2025" |
| supported | AGNTCY-ACP 仓库归档 2026-04-11；官方文档已不再列出，改推荐 A2A | r2-agntcy-acp.md C4, C7, C13；r3-agntcy-status.md C1, C4, C5 | 原句：acp-spec "archived on April 11, 2026"；docs.agntcy.org 列表无 ACP |
| unsupported | "AGNTCY 现在做 agent 间通信改推荐直接用 A2A（跑在自家 SLIM 传输层上）[6]" | r3-agntcy-status.md 有 leads 说"无法找到官方正式公告"，只有用户 issue #48 和 SLIM README 推论 | 无官方正式公告明确说"AGNTCY deprecated ACP in favor of A2A"，只有现状推论 |
| contradicted | 报告第 0.5 条"OpenAI、Anthropic 对 A2A 目前都停在'GitHub issue 讨论中'，没有产品集成" | r2-openai.md gaps 列举"A2A 是否由 OpenAI 支持（搜索结果显示只有 GitHub issue 要求支持，无官方采纳）" | OpenAI 关于 A2A 支持的确切来源模糊，只在笔记 gaps 里说"仅 GitHub issue 讨论"，无正面支持证据 |

## 自洽检查

| 甲处原文（第几节） | 乙处原文（第几节） | 一致性 | 建议 |
|---|---|---|---|
| 0.1 说"ACP-IBM...仓库归档 2025-08-27" | 0.1 说"AGNTCY...仓库归档 2026-04-11" | 一致 | 无需改 |
| 0.2 说 SSE "2025-03-26 标记 deprecated，2026-07-28 正式 reclassify" | 4.1 说"SSE 已废弃...老教程若还在讲纯'SSE transport'，对应的是 2024-11-05 那版协议" | 一致且补充 | 无需改，第 4.1 条补充了历史细节 |
| 0.3 说"官方立场是互补不是竞争——AG-UI 文档明确说'三者通常被同一个 agent 同时使用'" | 3 节 MCP/A2A/AG-UI 互相定位部分说"官方互相定位、不重叠" | 一致 | 无需改 |
| 0.4 说"A2A 更早独立捐赠给 LF（2025-06-23），AAIF 2026-08-17 官宣 A2A 以'hosted project'身份加入，地位比 founding 项目低一级" | 2 节矩阵和 5 节未决都没有质疑 A2A 地位低于 MCP | 一致 | 无需改 |
| 0.5 第一句"四大厂 MCP 全部官方支持" | 矩阵第 2.3 行，OpenAI/Anthropic/Google/Microsoft 都是 ✅，但 Anthropic 的"✅ 起源方"标记有误 | 矛盾 | Anthropic MCP 是"起源方"，应该是 ✅ + 起源方标记，不是"🔄" |
| 0.5 第二句"A2A 只有 Google/Microsoft 真正落地到产品" | 矩阵 Google "✅ 起源方"、Microsoft "✅ Azure AI Foundry A2A v1.0 GA" | 一致，Anthropic 是 🔄、OpenAI 是 ❌ | 无需改 |
| 0.5 第二句后半"OpenAI、Anthropic 对 A2A 目前都停在'GitHub issue 讨论中'，没有产品集成" | r2-openai.md C1-C9 中无 A2A 支持证据，gap 列列举；r2-anthropic.md C10 说 issue 开放状态 | 一致但证据弱 | 标注（二手或未证实）|
| 0.6 说"鉴权没有统一标准" | 矩阵鉴权列四行各不同 | 一致 | 无需改 |
| 1 节"ACP-IBM ✝→A2A；AGNTCY-ACP ✝→A2A" | 3 节表格"现状"列说 ACP-IBM "✝ 并入 A2A"、AGNTCY-ACP "✝ 仓库归档...改推荐 A2A" | 一致 | 无需改 |
| 3 节 MCP/A2A/AG-UI "官方互相定位、不重叠" 末句说"AG-UI 已支持'代理'MCP/A2A agent 的握手模式" | r1-ag-ui.md C29 原句："AG-UI recently introduced handshakes enabling it to proxy for agents that use MCP and A2A protocols" | 一致 | 无需改 |
| 矩阵"Agent Connect Protocol" AGNTCY 那一列 | 表格正文说"现行官方文档完全不再提它，AGNTCY 现在做 agent 间通信改推荐直接用 A2A" | 一致但过度确定 | 见下方高风险 |
| 5 节未决说"ACP-IBM 并入 A2A 的宣布日期...官方博客说 8-29，GitHub Discussion 提到 8-25" | r1-acp-ibm.md conflicts 说"LFAI & Data 博客说 2025 年 8 月 29 日，GitHub 讨论说 2025 年 8 月 25 日" | 完全一致，已在笔记里列 conflicts | 无需改 |

## 高风险表述核查

### 1. "三个 ACP 除了缩写一样，互相没有继承关系"

**核查结果**: ✅ **supported**
- r1-acp-ibm.md C1 IBM ACP 连接"agents, applications, and humans"（agent↔agent）
- r1-acp-zed.md C1 Zed ACP 连接"code editors...and coding agents"（编辑器↔本地agent）
- r2-agntcy-acp.md C2 AGNTCY ACP 定义为"通过 API 调用和配置远程代理"（应用↔远程agent）
- 笔记里无任何继承或派生证据

### 2. AGNTCY ACP 弃用和推荐 A2A

**核查结果**: ⚠️ **weak / unsupported**

报告正文：
- 0.1："Cisco/AGNTCY 的 Agent Connect Protocol 仓库已于 2026-04-11 归档，现有官方文档完全不再提它，AGNTCY 现在做 agent 间通信改推荐直接用 A2A"
- 3 节表格："✝ 仓库归档 2026-04-11；现行官方文档已不再列出，改推荐 A2A（经 SLIM 传输层）[6]"

笔记证据：
- r2-agntcy-acp.md C4, C5 确认仓库存档 2026-04-11
- r2-agntcy-acp.md C7 说"OASF 活跃模式现将 ACP 相关字段标记为已废弃，明确推荐 A2A"（**但这是 secondary 来源**）
- r3-agntcy-status.md gaps 明确说"**找不到 AGNTCY 官方的正式公告或 changelog，明确说明 ACP 被弃用的原因**"
- r3-agntcy-status.md leads 说"**无法找到'deprecated in favor of A2A'的一手官方原句支撑**"

**问题**: 报告说"改推荐 A2A"但笔记里只有现状推论（仓库存档、文档不列）和 secondary 来源（用户 issue、二手文章），**没有官方正式公告**。

### 3. "2026-08-17"加入 AAIF 日期

**核查结果**: ✅ **supported**
- r3-aaif-a2a-date.md C1 官方博客日期："2026-08-17"
- C2 原句："is joining the Agentic AI Foundation (AAIF) as a hosted project"
- r2-aaif-governance.md C6, C7 二次确认

### 4. Anthropic 拒绝 ACP

**核查结果**: ✅ **supported**
- r2-anthropic.md C8, C9 原句："Closed as not planned"
- 这是"明确拒绝"而非"没有做"

## 计数

**支撑类型**:
- supported: 21 条
- weak: 2 条（Anthropic A2A 现状、AGNTCY ACP 推荐 A2A）
- unsupported: 1 条（OpenAI A2A 支持无正面证据）
- contradicted: 0 条（无直接矛盾，只有表述精度问题）

**自洽问题**: 2 处
1. Anthropic MCP 标记应为"✅ 起源方"而非"🔄"（与 0.5"MCP 全部官方支持"矛盾）
2. "AGNTCY 改推荐 A2A"表述过度确定（笔记明确说无官方原句）

---

## 最严重的 3 个问题

1. **Anthropic MCP 矩阵标记错误（第 2.3 行）**: 报告标记为"🔄 办过 MCP+A2A 联合 webinar"，但 Anthropic 是 MCP 起源方，应为"✅ 起源方；Claude Agent SDK、Managed Agents"。矩阵正确应为：
   - MCP: ✅ 起源方
   - A2A: 🔄（webinar 但未产品集成）

2. **AGNTCY ACP 弃用原因无官方证据（0.1、3 节、5 节）**: 报告多处说"现在做 agent 间通信改推荐直接用 A2A"和"现有官方文档完全不再提它"，但笔记 r3-agntcy-status.md gaps 明确说"**找不到 AGNTCY 官方的正式公告或 changelog**"。应改为"仓库已存档，官方文档改为推荐 SLIM/A2A（推论基于现状，无官方弃用声明）"或改入第 5 节未决。

3. **OpenAI A2A 支持缺乏正面证据（0.5、2.3 行）**: 报告断言 OpenAI 对 A2A "仅 GitHub issue 讨论，没有产品集成"，但 r2-openai.md gaps 列说"A2A 是否由 OpenAI 支持（搜索结果显示只有 GitHub issue 要求支持，**无官方采纳**）"——这是负面证据（无支持证据），不是"停在讨论"的正面证据。建议改为"未发现官方支持证据"或标注为"❓ 无官方声明"而不是"❌"。

