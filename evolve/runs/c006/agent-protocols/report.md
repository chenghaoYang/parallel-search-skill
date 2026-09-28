# Agent 时代的协议地图：MCP / A2A / ACP×4 / AG-UI

> 每个「协议」连接哪两端、谁治理、现状、怎么选。截至 2026-09-25，以官方 spec/公告为准。[n] 见文末。

## 0. 一屏看懂

- **「ACP」至少 4 个，互不相关**：IBM Agent Communication Protocol（并入 A2A、repo 已归档）[14][15]、Zed Agent Client Protocol（编辑器↔agent）[17]、OpenAI/Stripe Agentic Commerce Protocol（购物）[30]、AGNTCY/Cisco Agent Connect Protocol [41]。
- **「MCP 的 SSE 废弃」属实但常被误读**：废弃的是独立的 HTTP+SSE 传输，2025-03-26 起被 Streamable HTTP 取代并标 deprecated；SSE 仍是 Streamable HTTP 内部可选机制，且至今未被移除 [3][8]。
- **四大主协议不竞争、分层互补**：MCP 连工具/数据、A2A 连别的 agent、Zed ACP 连编辑器、AG-UI 连用户前端，官方互认互补 [11][25]。
- **治理向 Linux 基金会集中**：MCP→AAIF（2025-12）、A2A→LF（2025-06）、IBM ACP→A2A；仅 AG-UI 仍由 CopilotKit 主导（MIT）[10][12][21]。
- **MCP 是唯一四厂通吃的协议**。A2A 有 Google/微软 GA，OpenAI 明说不内建（认可与 a2a-sdk 组合）、Anthropic 合办过 A2A webinar；AG-UI 被微软 Agent Framework 集成，OpenAI 官方拒绝集成 [31][32][43][46]。
- **选型一句话**：接工具 MCP、agent 互调 A2A、IDE 接 coding agent 用 Zed ACP、做 agent 前端用 AG-UI——常叠加使用。

## 1. Taxonomy

分类轴 = **协议连接哪两端**——决定问题域，也解释为何不互相替代。

| 家族 | 实体 | 为什么是一类 |
|---|---|---|
| 应用 ↔ 工具/数据 | MCP（扩展 MCP Apps；替代叙事 UTCP） | 把外部能力标准化喂给模型 |
| Agent ↔ Agent | A2A（IBM ACP 并入）、AGNTCY ACP、ANP | 独立 agent 对等委派、不共享内部状态 |
| 编辑器/客户端 ↔ Agent | Zed ACP | 类 LSP：编辑器拉起 agent 子进程 |
| 前端 UI ↔ Agent | AG-UI（生成式 UI 层：A2UI） | 一次请求进、一条有序类型化事件流出 |
| 商务/支付 | OpenAI/Stripe ACP、Google AP2、Google×Shopify UCP、Coinbase x402 | 在以上协议之上做交易 |
| 非 wire 协议 | AGENTS.md、Agent Skills、NLWeb | 常被误叫「协议」的约定/格式 |

## 2. 对照矩阵

| | MCP | A2A | ACP-IBM（停更） | ACP-Zed | AG-UI |
|---|---|---|---|---|---|
| 两端 | Host↔Server，应用↔工具 [1] | client↔remote agent，opaque 对等 [11] | agent↔agent/人 [16] | 编辑器↔agent 子进程 [17] | agent↔用户前端 [21] |
| 发起/治理 | Anthropic 2024-11→AAIF/LF，Apache-2.0，SEP 流程 [7][9][10] | Google 2025-04→LF TSC，Apache-2.0 [12][13] | IBM 2025-03→LF→并入 A2A [14] | Zed 2025-08，JetBrains 共建，Apache-2.0 [18][19] | CopilotKit 2025-05，MIT，未入基金会 [21][22] |
| 传输 | stdio 或 Streamable HTTP（SSE 可选），JSON-RPC 2.0 [2] | 三种等价绑定：JSON-RPC+SSE / gRPC / HTTP+JSON [11] | REST/HTTP（OpenAPI）[16] | JSON-RPC over stdio；远程 /acp 端点（Streamable HTTP+WS）仍 draft RFD [17][20] | normative：HTTP+SSE、HTTP+Protobuf；WS 仅 custom transport/schema flag [24] |
| 顶层抽象 | Tools/Resources/Prompts+Elicitation；扩展 Tasks/Apps [1] | Task/Message/Part/Artifact/AgentCard（`/.well-known/agent-card.json`）[11] | agent/run/message/session；/ping /runs /session [16] | session/prompt/update/cancel、fs、terminal、permission [17] | RunAgentInput→8 族约 31 种事件 [26] |
| 鉴权 | OPTIONAL；HTTP 下 OAuth 2.1 子集（RFC9728/8414/PKCE）[6] | OpenAPI 3.2 SecurityScheme：apiKey/http/oauth2/oidc/mTLS [11] | spec 无 securitySchemes；部署层 Basic/Bearer/JWT [16] | initialize 报 authMethods（agent/terminal）[17] | spec 明文不定义 credential（归 binding/应用层） [24] |
| 版本 | 日期版号=最后破坏性变更日；当前 2026-07-28（移除握手与 session）[4][5] | v1.0.x（GitHub v1.0.1=2026-05），`A2A-Version` header 协商 [11] | spec 0.2.0；repo 2025-08-27 归档 [15] | wire v1 稳定；schema v2 为 alpha [17][20] | spec 1.0（npm 1.0.0=2026-09-17）[22] |
| SDK/采用 | 10 语言官方 SDK、Registry；97M+/月下载 [10] | Py/JS/Java/.NET/Go/Rust SDK+tck [11] | BeeAI Framework [14] | ~40 agent（Gemini CLI、Claude Code/Codex 经 adapter）[18] | TS/Py/.NET/Go 等；LangGraph/CrewAI/Mastra [21] |

## 3. 大厂支持矩阵

| | MCP | A2A | AG-UI | Zed ACP | 自家协议/变体 |
|---|---|---|---|---|---|
| OpenAI | ✅ Agents SDK/Responses/ChatGPT；Apps SDK built on MCP [27][28] | 不内建 SDK 抽象，建议与 a2a-sdk 组合 [31] | 官方关闭集成请求（py/js SDK）[32] | Codex CLI 经第三方 adapter（Zed 维护）[19] | Agentic Commerce Protocol [29][30]、AGENTS.md [10] |
| Anthropic | ✅ 发起方，Claude 全系 [9] | 与 Google Cloud 合办 A2A webinar（轻量表态）[46] | quickstarts 已合并 AG-UI 集成 PR [47] | Claude Code 经社区 adapter，非原生 [19] | MCP 本体、Agent Skills |
| Google | ✅ ADK 双向、Cloud 托管 [33] | ✅ 发起方+LF 创始 [12][13] | ADK 列 first-party 集成 [21] | Gemini CLI=首个参考实现 [18] | A2UI [35]、AP2 [36]、UCP [37] |
| 微软 | ✅ Build 2025 全线；Windows ODR=MCP 注册表 [38][44] | ✅ Foundry v1.0 GA（Entra ID 必需）、Copilot Studio 2026-04 GA、Teams SDK [40][45] | ✅ Agent Framework 官方集成 [43] | — | NLWeb（每实例同时是 MCP server）[39] |

## 4. 变体与坑

**变体/适配**：MCP Apps（官方扩展，`ui://` 资源渲染 iframe UI）统一了 MCP-UI 与 OpenAI Apps SDK 两套方案 [43]；AG-UI 可经 middleware 包 A2A agent [21]；Claude Code/Codex 靠 adapter 进 ACP 生态 [19]。

**坑**：
1. ACP 同名×4——引用先看全称；IBM 版文档站仍在线但已停更并入 A2A [14][15][30][41]。
2. 「SSE 没了」误读——SSE 流式仍在；HTTP+SSE 已具备移除资格（SEP-2596 Final 后 3 个月≈2026-08）但尚未移除 [3][8]。
3. MCP 版本号=最后破坏性变更日（首版 2024-11-05 早于 11-25 宣布日）；2026-07-28 移除 initialize 握手与 `Mcp-Session-Id`，老组合会断 [4][5]。
4. AP2 也有两个：Google Agent Payments Protocol vs ANP Agent Payment Protocol [36][48]。
5. AG-UI 文档新旧并存：README 写 ~16 事件，spec 1.0 实列约 31 个 [21][26]。
6. deprecated≠移除：MCP Roots/Sampling/Logging/DCR 自 2026-07-28 deprecated，最早移除 ≥2027-07-28 [8]。

## 5. 未决与置信度

- MCP HTTP+SSE 实际移除日未定（「SEP-2596 Final+3 个月」仅资格起点）[8]。
- AG-UI 是否移交基金会官方未表态；spec 1.0 无公告日（npm 2026-09-17 近似）。
- Anthropic 对 A2A/AG-UI 仅 webinar/quickstart 级信号，无产品集成表态 [46][47]。
- A2A spec 站标最新 1.0.0，GitHub 已 v1.0.1（patch 不参与协商）[11]。
- Agentic Commerce Protocol 发起方口径不一：Stripe 页写含 Meta，GitHub 写 OpenAI+Stripe [30]。

## 来源

[1] MCP spec — https://modelcontextprotocol.io/specification
[2] MCP transports — https://modelcontextprotocol.io/specification/2025-06-18/basic/transports
[3] MCP transports 2025-03-26 — https://modelcontextprotocol.io/specification/2025-03-26/basic/transports
[4] MCP changelog 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/changelog
[5] MCP versioning — https://modelcontextprotocol.io/specification/versioning
[6] MCP authorization — https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
[7] MCP governance — https://modelcontextprotocol.io/community/governance
[8] MCP deprecated registry — https://modelcontextprotocol.io/specification/2026-07-28/deprecated
[9] Anthropic 发布 MCP — https://www.anthropic.com/news/model-context-protocol
[10] LF AAIF — https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
[11] A2A spec — https://a2a-protocol.org/latest/specification/
[12] Google 发布 A2A — https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
[13] A2A 捐 LF — https://developers.googleblog.com/google-cloud-donates-a2a-to-linux-foundation/
[14] LF：ACP 并入 A2A — https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
[15] IBM acp repo — https://github.com/i-am-bee/acp
[16] ACP-IBM 官网 — https://agentcommunicationprotocol.dev
[17] Zed ACP 概览 — https://agentclientprotocol.com/protocol/overview
[18] Zed：bring your own agent — https://zed.dev/blog/bring-your-own-agent-to-zed
[19] Zed：Claude Code via ACP — https://zed.dev/blog/claude-code-via-acp
[20] ACP v1 transports — https://agentclientprotocol.com/protocol/v1/transports
[21] AG-UI docs — https://docs.ag-ui.com/
[22] ag-ui repo — https://github.com/ag-ui-protocol/ag-ui
[24] AG-UI transports — https://docs.ag-ui.com/spec/1.0/basic/transports
[25] AG-UI 协议定位 — https://docs.ag-ui.com/agentic-protocols.md
[26] AG-UI events — https://docs.ag-ui.com/concepts/events
[27] OpenAI Agents SDK MCP — https://openai.github.io/openai-agents-python/mcp/
[28] OpenAI apps in ChatGPT — https://openai.com/index/introducing-apps-in-chatgpt/
[29] OpenAI Instant Checkout — https://openai.com/index/buy-it-in-chatgpt/
[30] Agentic Commerce Protocol — https://github.com/agentic-commerce-protocol/agentic-commerce-protocol
[31] openai-agents#472 — https://github.com/openai/openai-agents-python/issues/472
[32] openai-agents-js#70 — https://github.com/openai/openai-agents-js/issues/70
[33] Google ADK MCP — https://adk.dev/tools-custom/mcp-tools/
[35] Google A2UI — https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/
[36] Google AP2 — https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol
[37] Google UCP — https://developers.google.com/merchant/ucp
[38] MS Build 2025 — https://blogs.microsoft.com/blog/2025/05/19/microsoft-build-2025-the-age-of-ai-agents-and-building-the-open-agentic-web/
[39] Microsoft NLWeb — https://news.microsoft.com/source/features/company-news/introducing-nlweb-bringing-conversational-interfaces-directly-to-the-web/
[40] Foundry A2A — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/enable-agent-to-agent-endpoint
[41] AGNTCY connect docs — https://github.com/agntcy/docs/blob/d7d5db4e/docs/syntactic/connect.md
[43] Agent Framework AG-UI — https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/
[44] Windows ODR — https://learn.microsoft.com/en-us/windows/ai/mcp/overview
[45] Copilot Studio whats-new — https://learn.microsoft.com/en-us/microsoft-copilot-studio/whats-new
[46] Anthropic×Google A2A webinar — https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai
[47] claude-quickstarts AG-UI PR — https://github.com/anthropics/claude-quickstarts/pull/438
[48] ANP — https://github.com/agent-network-protocol/AgentNetworkProtocol
