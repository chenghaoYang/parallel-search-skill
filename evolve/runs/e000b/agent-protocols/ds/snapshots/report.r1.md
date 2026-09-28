# Agent 时代的协议全景：MCP / A2A / ACP(×2) / AG-UI

> 回答 agent 系统里这几种「协议」各管什么、怎么选、两个 ACP 是不是一回事、MCP 的 SSE 是否已废弃。数据截至 2026-09-24；具体事实带 [n] 指向文末一手来源；❓= 待下一轮核实。

## 0. 一屏看懂

- **四层协议，不是四个竞品**：agent↔工具/数据用 **MCP**；agent↔agent（跨厂商任务委派）用 **A2A**；agent↔终端用户 UI 用 **AG-UI**；编辑器/IDE↔agent 子进程用 **ACP（Zed 版）**。四者可以叠加用在同一个系统里 [8][16]。
- **两个 ACP 不是一回事，纯属撞名**：IBM 的 Agent Communication Protocol（agent 对 agent，2025-03 发布）已于 2025-08-27 并入 A2A、仓库归档只读 [9][10]；Zed 的 Agent Client Protocol（编辑器对 agent 子进程）仍在活跃开发，最新 v1.9.1（2026-09-18）。两边官方文档都没提过对方 [10][12]。
- **MCP 的 SSE 确实被替换了**：2025-03-26 版规范用 **Streamable HTTP** 替换了 2024-11-05 版的独立 "HTTP+SSE" 传输，旧传输标记为 deprecated（仅保留向后兼容）；最新 2026-07-28 版里标准传输只剩 stdio 和 Streamable HTTP，SSE 变成 Streamable HTTP 内部可选的流式手段，不再是独立选项 [1][2][3]。
- **治理都在去厂商化，但不是同一个基金会**：MCP → Linux Foundation 旗下 **Agentic AI Foundation**（Anthropic/Block/OpenAI 发起）[4][21]；A2A → **Linux Foundation A2A Project**（Google 捐赠，8 公司指导委员会）[6][7]；ACP-Zed → **Zed + JetBrains** 联合治理，计划移交独立基金会 [13]；AG-UI → CopilotKit 主导的 MIT 开源项目 [18]。
- **鉴权各管各的，没有统一标准**：MCP 建议 HTTP 传输走 OAuth 2.1 + Bearer（stdio 走环境变量，整体鉴权可选）[3]；A2A 把鉴权方式写进 Agent Card 的 securitySchemes（对齐 OpenAPI）[5]；ACP-Zed 在初始化握手用 authMethods 声明 [14]；AG-UI 不定义自有鉴权，靠底层 HTTP 传输的 Bearer/API key/SigV4 [19]。
- **四大厂基本都在接 MCP+A2A+AG-UI 三件套**，分歧在 ACP-Zed：Microsoft Agent Framework v1.0 官方称原生支持 MCP/A2A/AG-UI [23]；Google 是 A2A 发起方，同时支持 MCP 和 AG-UI [22][16]；OpenAI 官方确认支持 MCP，未见官方 A2A 表态 [20]；Anthropic 创立 MCP，AG-UI 官方集成页显示 Claude Agent SDK 走 AG-UI [16]。ACP-Zed 目前是编辑器生态自己在跑（Claude Code/Gemini CLI/Codex CLI 已接入），还没看到四大厂就协议本身表态 [15]。

## 1. Taxonomy

分类轴：协议连接的两端是谁。

| 族 | 连接两端 | 成员 |
|---|---|---|
| 工具/上下文面 | agent ↔ 工具、数据源 | MCP |
| Agent 对等面 | agent ↔ 另一个 agent（跨组织任务委派）| A2A、ACP-IBM（已并入 A2A）|
| 宿主应用面 | agent ↔ 承载它的宿主/前端 | AG-UI（终端用户 UI）、ACP-Zed（编辑器宿主，类比 LSP）|

维度：定位层｜传输｜鉴权｜状态归属｜治理｜版本｜关系（下节按此排列）。

## 2. 对照矩阵

### 协议本身
| 协议 | 定位层 | 传输 | 鉴权 | 状态归属 | 治理 | 当前版本 |
|---|---|---|---|---|---|---|
| MCP | agent↔工具/数据 [4] | JSON-RPC2.0；stdio / Streamable HTTP（原 HTTP+SSE 已废弃）[1][2][3] | HTTP 传输建议 OAuth2.1+Bearer；stdio 走环境变量；整体可选 [3] | 每请求自包含，服务端不假设会话上下文 [3] | Linux Foundation / AAIF，Anthropic 发起 [4] | 2026-07-28（stable）[3] |
| A2A | agent↔agent [8] | JSON-RPC2.0 over HTTP(S)，支持 SSE 流式和 webhook 异步 [5] | Agent Card.securitySchemes：apiKey/oauth2/OIDC/mTLS [5] | Task 8 态机（Submitted…Completed）[5] | Linux Foundation A2A Project，Google 捐赠，8 公司指导委员会 [6][7] | v1.0.0（2026-03-12，生产就绪）[7] |
| ACP-IBM（已并入 A2A）| agent↔agent [11] | JSON-RPC/REST over HTTP、WebSocket [11] | capability token + OAuth2（二手）[11] | 同步/异步/流式均支持（二手）[11] | 曾属 LF AI & Data，2025-08 并入 A2A [9] | 未给版本号；仓库 2025-08-27 归档只读 [10] |
| ACP-Zed | 编辑器↔agent 子进程 [12] | 本地 JSON-RPC over stdio；远程 HTTP/WebSocket（开发中）[12] | 初始化握手 authMethods，agent 自处理或终端登录 [14] | ❓未在笔记中明确规定 | Zed + JetBrains 联合治理，计划移交独立基金会 [13] | 协议版本 1；发布 v1.9.1（2026-09-18）[15] |
| AG-UI | agent 后端↔终端用户 UI [16] | 传输无关：SSE/WebSocket/webhook 均可 [17] | 不定义自有鉴权；HTTP Bearer/API key/SigV4（依赖实现）[19] | 状态存在 agent 后端，前端靠 STATE_SNAPSHOT/DELTA 事件同步 [16] | CopilotKit 主导，MIT 协议 [18] | 1.0.0（2026-09-17，此前 0.1.x）[18] |

### 大厂支持矩阵
| 厂商 | MCP | A2A | ACP-Zed | AG-UI | 自家变体 |
|---|---|---|---|---|---|
| OpenAI | ✅ ChatGPT/Agents SDK [20] | ❓未见官方表态 | ❓未见 | ❓未见官方表态 | AGENTS.md（agent 说明文件约定，非网络协议，AAIF 项目）[21] |
| Anthropic | ✅ 发起方 [4][21] | ❓未见官方表态 | Claude Code 已加 beta 支持（Zed 一侧公告）[15] | ✅ Claude Agent SDK 走 AG-UI（AG-UI 一侧公告）[16] | 无 |
| Google | ✅ ADK 支持 [22] | ✅ 发起方 [8] | Gemini CLI 为参考实现（Zed 一侧公告）[15] | ✅ ADK 支持 [16] | A2UI（Gemini Enterprise UI 注册机制，与 AG-UI 关系待核实）[22] |
| Microsoft | ✅ Agent Framework 原生 [23] | ✅ Agent Framework 原生 [23] | ❓未见 | ✅ Agent Framework 原生 [23] | 无（Agent Framework 是 SDK，非新协议）|

## 3. 变体与适配层：两个 ACP 到底差在哪

| | ACP-IBM（Agent Communication Protocol）| ACP-Zed（Agent Client Protocol）|
|---|---|---|
| 连的是谁 | agent ↔ agent，同 A2A 一层 [11] | 编辑器/IDE ↔ agent 子进程 [12] |
| 现状 | 2025-08-27 归档，团队并入 A2A [9][10] | 活跃开发，v1.9.1（2026-09-18）[15] |
| 传输 | REST/JSON-RPC over HTTP、WebSocket [11] | 本地 stdio；远程 HTTP/WS 开发中 [12] |
| 治理 | IBM Research → LF AI & Data [9] | Zed + JetBrains [13] |
| 对另一 ACP 的态度 | 官方文档未提及 Zed ACP [10] | 官方文档未提及 IBM ACP，只提 LSP 渊源 [12] |

结论：两者除了缩写相同，定位、治理、现状完全不同，不存在改名或继承关系，纯属命名巧合——且用户提问时点上 IBM 版早已停止独立存在。

## 4. 用户需要知道的坑

- **把"MCP 和 A2A 互补"读成"可以互相替代"**：官方定位是纵向（MCP，agent→工具）vs 横向（A2A，agent→agent），是叠加关系不是二选一 [8]。
- **以为 SSE 被整体弃用**：MCP 只是不再把 SSE 当独立 transport，Streamable HTTP 内部仍可选用 SSE 做流式推送，能力还在 [2]。
- **搜"ACP"时把 IBM 和 Zed 的混为一谈**：IBM 版 2025-08 已归档，此后"ACP"在社区语境里才逐渐特指 Zed 版；查资料要留意发布时间 [9][15]。
- **把 A2UI 当成 AG-UI 的别名**：Google Gemini Enterprise 文档里的 A2UI 目前证据不足以确认是否等同或包含 AG-UI，不要直接划等号，待核实 [22]。
- **把鉴权当协议强制项**：MCP、AG-UI 的鉴权本身是"可选/依赖实现"，不像 A2A/ACP-Zed 把鉴权方式写进协议对象（Agent Card / authMethods）里；接入时要自己补全鉴权，不能假设协议已经管了 [3][19]。

## 5. 未决与置信度

- AAIF（Agentic AI Foundation）成立/MCP 移交的精确日期未核实，只找到"由 Anthropic/Block/OpenAI 发起"的表述 [21]。
- A2UI 与 AG-UI 的关系（Google 定制层还是独立规范）待核实。
- OpenAI/Anthropic/Microsoft 对 A2A、Microsoft/OpenAI 对 ACP-Zed，目前是"未见官方表态"而非"官方声明不支持"，两者不能等同。
- ACP-IBM 的鉴权细节（capability token、K8s RBAC）仅二手来源（workos.com 博客），IBM 官方页面只给到"标准 HTTP 惯例"这一级。
- AGNTCY（Cisco 主导，Linux Foundation，65+ 公司）是 agent 发现/身份/消息基础设施层，和本文五个协议互补而非竞争，因篇幅未展开 [24]。

## 来源
[1] MCP 2024-11-05 transports — https://modelcontextprotocol.io/specification/2024-11-05/basic/transports
[2] MCP 2025-03-26 transports（Streamable HTTP 替换 HTTP+SSE）— https://modelcontextprotocol.io/specification/2025-03-26/basic/transports
[3] MCP 2026-07-28 transports/authorization（现行版）— https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
[4] MCP 治理与定位 — https://github.com/modelcontextprotocol ; https://modelcontextprotocol.io
[5] A2A 规范（传输/鉴权/任务状态）— https://a2a-protocol.org/latest/specification/
[6] A2A 捐赠 Linux Foundation（2025-06-23）— https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents
[7] A2A v1.0 发布（2026-03-12，治理委员会）— https://a2a-protocol.org/latest/blog/2026/03/12/a2a-protocol-ships-v10-production-ready-standard-for-agent-to-agent-communication/
[8] A2A 与 MCP 关系 — https://a2a-protocol.org/latest/topics/a2a-and-mcp/
[9] ACP-IBM 并入 A2A 公告（2025-08-29）— https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
[10] ACP-IBM 仓库归档（2025-08-27）— https://github.com/i-am-bee/acp
[11] ACP-IBM 概览 — https://www.ibm.com/think/topics/agent-communication-protocol
[12] ACP-Zed 简介与传输 — https://agentclientprotocol.com/get-started/introduction
[13] ACP-Zed 治理 — https://agentclientprotocol.com/community/governance
[14] ACP-Zed 鉴权 — https://agentclientprotocol.com/protocol/v2/authentication
[15] ACP-Zed 采用者与版本 — https://zed.dev/acp ; https://zed.dev/blog/bring-your-own-agent-to-zed
[16] AG-UI 首页与协议关系 — https://docs.ag-ui.com ; https://docs.ag-ui.com/agentic-protocols
[17] AG-UI 架构/传输/事件 — https://docs.ag-ui.com/concepts/architecture
[18] AG-UI GitHub（许可证/版本）— https://github.com/ag-ui-protocol/ag-ui
[19] AG-UI AWS Bedrock 实现（鉴权）— https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-agui-protocol-contract.html
[20] OpenAI MCP 支持 — https://learn.chatgpt.com/docs/extend/mcp?surface=cli ; https://openai.github.io/openai-agents-python/mcp/
[21] Anthropic MCP 起源与 AAIF — https://www.anthropic.com/news/model-context-protocol ; https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
[22] Google A2A 发起与 A2UI — https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ ; https://docs.cloud.google.com/gemini/enterprise/docs/a2ui-agents/register-and-manage-an-a2ui-agent
[23] Microsoft Agent Framework v1.0 — https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/
[24] AGNTCY — https://agntcy.org/
