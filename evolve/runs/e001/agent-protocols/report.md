# Agent 时代的「协议」全景：MCP / A2A / ACP / AG-UI 怎么分清楚

> 本文回答 agent 生态里几种互操作「协议」各管什么、谁治理、大厂站哪边、怎么选。截至 2026-09-24；部分数据时效性强，见第 5 节。先看「一屏看懂」，需要细节再查表。

## 0. 一屏看懂
1. **"ACP" 撞名撞了三次，且 agent↔agent 这条线上 A2A 事实上"赢了"**：IBM/BeeAI 的 Agent Communication Protocol 已于 2025-08-29 正式并入 A2A、仓库归档 [3]；Cisco/AGNTCY 的 Agent Connect Protocol 仓库已于 2026-04-11 归档，现行官方文档已不再列出它，只保留 SLIM 作为"A2A 等协议的传输层"——相当于事实上被 A2A 取代，但 AGNTCY 官方从未发过正式弃用声明 [6]；只有 Zed 的 Agent Client Protocol 活着——因为它根本不是同一类协议（连接"编辑器↔本地 agent 子进程"，不是 agent 之间）[5]。三者除了缩写一样，互相没有继承关系。
2. **MCP 的 SSE 传输确实已废弃**：2025-03-26 标记 deprecated，2026-07-28 正式 reclassify，替代方案 Streamable HTTP；相关 SEP 转正后 3 个月即可移除 [1]。
3. 四个"活着"的协议连接四种不同的两端：MCP＝agent↔工具/数据；A2A＝agent↔agent；AG-UI＝agent 后端↔用户界面；ACP-Zed＝宿主应用↔本地 agent。**官方立场是互补不是竞争**——AG-UI 文档明确说"三者通常被同一个 agent 同时使用"[4]。
4. 治理集中到 Linux Foundation，但地位不等：MCP 是 2025-12-09 成立的 Agentic AI Foundation（AAIF）三个 founding contribution 之一（Anthropic CPO 原话："Donating MCP...ensures it stays open, neutral, and community-driven"）[2]；A2A 更早独立捐赠给 LF（2025-06-23），AAIF 2026-08-17 官宣 A2A 以"hosted project"身份加入，地位比 founding 项目低一级 [2]；ACP-Zed（独立 Apache-2.0 项目）和 AG-UI（VC 创业公司 CopilotKit 主导）都还没捐给任何基金会 [4][5]。
5. **四大厂 MCP 全部官方支持，A2A 只有 Google/Microsoft 真正落地到产品**：OpenAI 对 A2A 未见任何官方声明；Anthropic 办过 MCP+A2A 联合 webinar，但产品同样未集成（GitHub issue 仍开放、未采纳），甚至把"支持 ACP"的功能请求明确关闭为 not planned [7][8]。每家还都在造功能重叠的自家协议/工具层（见第 3 节）。
6. 鉴权没有统一标准：MCP 用 OAuth 2.1+RFC8707/9207 [1]；A2A 支持 OAuth2/API key/mTLS/HTTP Basic 且强制 TLS1.2+ [2]；ACP-Zed 只定义 agent/terminal 两种登录握手，不规定凭证格式 [5]；AG-UI 明确"不内置鉴权，复用宿主 HTTP 端点机制"[4]。

## 1. Taxonomy
分类轴：协议标准化的是"哪两端"之间的通信。

| 家族 | 两端 | 成员（●活跃 / ✝已死或让位）|
|---|---|---|
| Agent ↔ 工具/数据 | agent 运行时 ↔ 外部工具、API、数据源 | MCP ● |
| Agent ↔ Agent | 独立 agent/系统跨主体协作 | A2A ●；ACP-IBM ✝→A2A；AGNTCY-ACP ✝→A2A |
| Agent 后端 ↔ 用户界面 | agent 逻辑 ↔ 前端/聊天 UI | AG-UI ● |
| 宿主应用 ↔ 本地 Agent | 编辑器/IDE ↔ 它拉起的 agent 子进程 | ACP-Zed ● |

维度：连接对象｜起源→现治理｜版本｜传输层｜鉴权｜与大厂关系。

## 2. 对照矩阵

**核心协议：谁连谁 / 谁治理 / 多新**

| 协议 | 连接对象 | 起源 → 现治理 | 版本 |
|---|---|---|---|
| MCP | LLM 应用 ↔ 工具/数据/工作流 | Anthropic(2024-11) → AAIF founding contribution(2025-12-09) [1][2] | 2024-10-07 → 2026-07-28 [1] |
| A2A | 独立 agent 系统间协作 | Google(2025-04-09) → LF(2025-06-23) → AAIF hosted project(2026-08-17 官宣) [2] | v0.1 → v1.0.1(2026-05-28) [2] |
| AG-UI | agent 后端 ↔ 用户界面 | CopilotKit(VC 创业公司，未捐赠基金会) [4] | 规范 2026-07-18 → v1.0(2026-09-17) [4] |
| ACP-Zed | 编辑器 ↔ 本地 agent 子进程 | Zed Industries(2025-06-23) → 独立开源 Apache-2.0 [5] | v1 稳定(2026-06-24)；v2 alpha [5] |

**怎么连 / 鉴权**

| 协议 | 传输层 | 鉴权 |
|---|---|---|
| MCP | stdio／Streamable HTTP（**HTTP+SSE 已废弃**）[1] | OAuth 2.1 + RFC6750/8707/9207 [1] |
| A2A | JSON-RPC 2.0／gRPC／HTTP+REST 三选一，强制 TLS1.2+ [2] | OAuth2／API key／mTLS／HTTP Basic [2] |
| AG-UI | SSE 或 WebSocket，17 种事件分 5 类 [4] | 不内置，复用宿主 HTTP 端点鉴权 [4] |
| ACP-Zed | JSON-RPC 2.0 over stdio；远程传输开发中 [5] | agent/terminal 两种登录握手，不规定凭证格式 [5] |

**大厂支持面**

| Vendor | MCP | A2A | ACP | AG-UI | 自家变体 |
|---|---|---|---|---|---|
| OpenAI | ✅ Agents SDK/Responses API/ChatGPT devmode(09-2025)/Apps SDK，已加入 MCP steering committee [7] | ❓ 未见官方声明 [7] | ❌ 无证据 | 🔄 In Progress [7] | AgentKit、Realtime API、Agentic Commerce Protocol(×Stripe) [7] |
| Anthropic | ✅ 起源方；Claude Agent SDK、Managed Agents [8] | 🔄 办过 MCP+A2A 联合 webinar，产品未集成 [8] | ❌ 明确拒绝(issue closed "not planned") [8] | ❓ 无官方声明 [8] | Claude Skills(SKILL.md)、Computer Use [8] |
| Google | ✅ 2025-12-11 官方支持(Maps/BigQuery 等)+ADK McpToolset [9] | ✅ 起源方；ADK + 专有 A2A Extension [9] | ✅ Zed ACP 参考实现(Gemini CLI) [9] | ✅ 2025-09-26 ADK 集成 [9] | ADK、A2A Extension [9] |
| Microsoft | ✅ Copilot Studio GA/Azure AI Foundry/Windows ODR/Semantic Kernel/VS GA [10] | ✅ Azure AI Foundry A2A v1.0 GA + TSC 成员 [10] | ❌ 无直接支持；AHP 可用 ACP 作后端 [10] | ✅ Agent Framework(.NET/Python/Go) [10] | NLWeb、M365 Agents SDK、Agent Host Protocol(AHP) [10] |

## 3. 变体与适配层

**同名不同物，且多数已经不在了：三个"ACP"**

| | IBM/BeeAI ACP | Zed ACP | AGNTCY ACP |
|---|---|---|---|
| 全称 | Agent Communication Protocol | Agent Client Protocol | Agent Connect Protocol |
| 连接对象 | agent ↔ agent | 编辑器 ↔ 本地 agent 子进程 | 远程 agent 的 API 调用/配置 |
| 现状 | ✝ 并入 A2A，官方博客"joins forces"，仓库归档 2025-08-27 [3] | ● 活跃开发，v1 稳定，JetBrains 等 11+ 采用 [5] | ✝ 仓库归档 2026-04-11；现行官方文档已不再列出，只留 SLIM 官方定位为"A2A 等协议的传输层"（无官方弃用声明）[6] |

MCP/A2A/AG-UI 官方互相定位、不重叠：MCP 负责"agent 拿到工具和数据"，A2A 负责"agent 之间怎么协调"，AG-UI 负责"agent 怎么把过程实时呈现给用户"；AG-UI 已支持"代理"MCP/A2A agent 的握手模式 [4]。

**大厂自家变体不是标准本身**——都是标准协议之上/之外的私有层：OpenAI AgentKit（Agent Builder+ChatKit+Connector Registry）建在 MCP 之上；Google A2A Extension 用私有 header 修补"legacy A2A-ADK 实现的可靠性问题"[9]；Microsoft AHP 定位是"ACP 是点对点通信层，AHP 是协调多客户端的层"[10]；Anthropic Computer Use（computer_toolset_20260801）和 Skills（SKILL.md）目前只服务 Claude 产品线，未发布为独立开放规范。

## 4. 用户需要知道的坑
1. "SSE 已废弃"≠"MCP 不能用 HTTP"——替代方案 Streamable HTTP 仍用 SSE 做单次请求内的流式响应，只是取消跨请求恢复。老教程若还在讲纯"SSE transport"，对应的是 2024-11-05 那版协议 [1]。
2. 看到"ACP"先看连的是谁——三个候选里两个已死/让位给 A2A，只有 Zed 那个还在正常演进；碰到"IBM ACP"或"AGNTCY ACP"的旧教程，直接改查 A2A。
3. "官方支持"要看证据强弱：联合 webinar、GitHub issue open、"没搜到声明"是三种不同的确定性——Anthropic 对 A2A 是第一种，OpenAI 对 A2A 连官方表态都没搜到，两者都不等于产品已集成 [7][8]。
4. AG-UI 不是中立基金会治理，是刚融完 A 轮的创业公司主导 [4]；接入前评估这点和 MCP/A2A 的治理成熟度不同。
5. 鉴权没有统一标准，且各协议只规定"协议内"部分：接 MCP 按 OAuth2.1，接 A2A 由对方 agent 自选机制，接 AG-UI 基本靠宿主应用自己的鉴权。

## 5. 未决与置信度
- AGNTCY 官方从未发布正式弃用公告解释 ACP 为何被放弃——"改推荐 A2A"是根据仓库归档时间(2026-04-11)、现有官方文档结构（7 大组件不含 ACP）、以及一条非官方 GitHub issue（用户发起而非 AGNTCY 团队声明）推断，不是一句官方原话 [6]。
- Anthropic 对 AG-UI 的立场完全没有官方声明（既非支持也未拒绝）[8]。
- 除本文协议外，业内还有 ANP、LMOS、x402、AITP、TAP 等至少 9 个相关协议/标准，多为 secondary 来源，本文按篇幅限制未逐一展开。
- ACP-IBM 并入 A2A 的宣布日期，官方博客说 8-29，GitHub Discussion 提到 8-25，更可能是"内部讨论→仓库归档(8-27)→对外公告(8-29)"时间线而非真冲突。
- AAIF 2026-08-17 官宣 A2A 加入是"发布日期"，博客本身未明确这是否等同于正式生效日期 [2]。

## 来源
[1] MCP 官方 spec/changelog — modelcontextprotocol.io/specification/2026-07-28/{changelog, basic/authorization, basic/transports/streamable-http}
[2] A2A/AAIF 官方治理 — a2a-protocol.org/latest/specification/ ；linuxfoundation.org/press（A2A 启动、AAIF 成立两篇）；aaif.io/blog/a2a-joins-aaif（2026-08-17）；aaif.io/projects
[3] ACP-IBM 官方公告/仓库 — lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a...；github.com/i-am-bee/acp
[4] AG-UI 官方文档 — docs.ag-ui.com/{introduction, agentic-protocols}；github.com/ag-ui-protocol/ag-ui
[5] ACP-Zed 官方文档 — agentclientprotocol.com；github.com/agentclientprotocol/agent-client-protocol；zed.dev/blog/jetbrains-on-acp
[6] AGNTCY ACP 官方仓库/公告 — github.com/agntcy/{acp-spec,acp-sdk}（归档说明）；docs.agntcy.org；github.com/agntcy/.github（profile README）；raw.githubusercontent.com/agntcy/slim/main/README.md
[7] OpenAI — openai.github.io/openai-agents-python/mcp/；developers.openai.com/api/docs/guides/tools-connectors-mcp；openai.com/index/introducing-agentkit/
[8] Anthropic — anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation；code.claude.com/docs/en/agent-sdk/overview；github.com/anthropics/claude-code/issues/{6686,28300}
[9] Google — cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services；adk.dev/{mcp, a2a/a2a-extension, integrations/ag-ui}
[10] Microsoft — microsoft.com/en-us/copilot/blog/copilot-studio/...generally-available...；devblogs.microsoft.com/foundry/...；github.com/microsoft/agent-host-protocol
