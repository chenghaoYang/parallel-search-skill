# Agent 时代的协议地图：MCP / A2A / ACP×4 / AG-UI

> 回答：每个「协议」连接哪两端、谁治理、现状如何、怎么选。截至 2026-09-25，以官方 spec 与公告为准。[n] 见文末来源。

## 0. 一屏看懂

- **「ACP」至少有 4 个，全不相关**：IBM 的 Agent Communication Protocol（已并入 A2A、repo 归档）[13][15]、Zed 的 Agent Client Protocol（编辑器↔coding agent）[18]、OpenAI/Stripe 的 Agentic Commerce Protocol（购物支付）[29]、AGNTCY/Cisco 的 Agent Connect Protocol [39]。看到 ACP 先问是哪个。
- **「MCP 的 SSE 废弃」是真的但常被误读**：废弃的是 2024-11-05 版独立的 HTTP+SSE 传输，2025-03-26 起被 Streamable HTTP 取代并标 deprecated；SSE 仍作为 Streamable HTTP 内部可选流式机制存在 [3][4]。
- **四个主协议不竞争、是分层互补**：MCP 连工具/数据、A2A 连别的 agent、Zed ACP 连编辑器、AG-UI 连用户前端。官方口径互认互补 [10][26]。
- **治理都在向 Linux 基金会集中**：MCP 2025-12 进入新成立的 Agentic AI Foundation（AAIF）、A2A 2025-06 捐给 LF、IBM ACP 并入 A2A；只有 AG-UI 仍由 CopilotKit 主导（MIT）[9][12][22]。
- **大厂公约数是 MCP**：OpenAI/Anthropic/Google/微软全部支持 MCP；A2A 有 Google 和微软站台，OpenAI 明说暂不在自家 SDK 内建 A2A 抽象 [30][45]；AG-UI 获微软 Agent Framework 官方集成 [32]。
- **选型一句话**：给 agent 接工具用 MCP，agent 之间互派任务用 A2A，IDE/编辑器接 coding agent 用 Zed ACP，给 agent 做前端界面用 AG-UI——真实系统常四者叠加。

## 1. Taxonomy

分类轴 = **协议连接哪两端**——这决定问题域，也解释它们为何不互相替代。

| 家族 | 实体 | 为什么是一类 |
|---|---|---|
| 应用 ↔ 工具/数据 | MCP（扩展：MCP Apps；替代叙事：UTCP） | 把外部能力标准化喂给模型 |
| Agent ↔ Agent | A2A（IBM ACP 已并入）、AGNTCY ACP、ANP | 独立 agent 对等委派任务、不共享内部状态 |
| 编辑器/客户端 ↔ Agent | Zed ACP | 类 LSP：编辑器拉起 agent 子进程 |
| 前端 UI ↔ Agent | AG-UI（生成式 UI 层：Google A2UI） | 一次请求进、一条有序类型化事件流出 |
| 商务/支付 | OpenAI/Stripe ACP、Google AP2、Google×Shopify UCP、Coinbase x402 | 在以上协议之上做交易/支付 |
| 非 wire 协议 | AGENTS.md、Agent Skills（约定文件）、NLWeb（网站 NL 端点） | 常被误叫「协议」的约定/格式 |

维度：D1 两端、D2 发起/治理（含 license）、D3 传输、D4 顶层抽象、D5 鉴权、D6 当前版本、D7 大厂用法、D8 SDK/采用。

## 2. 对照矩阵

| | MCP | A2A | ACP-IBM（停更） | ACP-Zed | AG-UI |
|---|---|---|---|---|---|
| D1 两端 | Host↔Server（应用↔工具）[1] | client↔remote agent，opaque 对等 [10] | agent↔agent/人 [16] | 编辑器↔agent 子进程 [18] | agent↔用户前端 [22] |
| D2 发起/治理 | Anthropic 2024-11→AAIF/LF，Apache-2.0，SEP 流程 [8][9][7] | Google 2025-04→LF TSC，Apache-2.0 [11][12] | IBM 2025-03→LF，已并入 A2A [13] | Zed 2025-08，JetBrains 共建，Apache-2.0 [19][20] | CopilotKit 2025-05，MIT，未入基金会 [22][47] |
| D3 传输 | stdio 或 Streamable HTTP（SSE 可选）；JSON-RPC 2.0 [2] | 三种等价绑定：JSON-RPC+SSE / gRPC / HTTP+JSON（application/a2a+json）[10] | REST/HTTP（OpenAPI）[16] | JSON-RPC over stdio；远程 HTTP/WS 为 WIP [18] | transport-agnostic；normative：HTTP+SSE、HTTP+Protobuf [25] |
| D4 抽象 | Tools/Resources/Prompts + Elicitation；扩展：Tasks/Apps [1] | Task/Message/Part/Artifact/AgentCard（`/.well-known/agent-card.json`）[10] | agent/run/message/session；/ping /runs /session [16] | session/prompt/update/cancel、fs、terminal、permission [18] | RunAgentInput→8 族约 31 种事件（TEXT_MESSAGE_*、TOOL_CALL_*、STATE_*…）[24] |
| D5 鉴权 | OPTIONAL；HTTP 下 OAuth 2.1 子集：server=资源服务器（RFC9728）、PKCE、RFC8414 发现 [6] | OpenAPI 3.2 SecurityScheme：apiKey/http/oauth2/oidc/mTLS [10] | spec 内无 securitySchemes；部署层 Basic/Bearer/JWT [16] | initialize 报 authMethods，agent/terminal 两类 [18] | spec 不定义；实现层自行带 header（Bearer 等）[25] |
| D6 版本 | 日期版号，当前 2026-07-28（移除握手与 session，无状态化）[4][5] | v1.0.x（v1.0.1=2026-05），`A2A-Version` header 协商 [10][14] | spec 0.2.0；repo 2025-08-27 归档 [15] | wire v1 稳定（schema v2 独立演进）[18] | spec 1.0（npm 1.0.0=2026-09-17）[23] |
| D8 实现 | 10 语言官方 SDK、Inspector、Registry；97M+/月下载 [9] | Py/JS/Java/.NET/Go/Rust SDK + tck/inspector [10] | BeeAI Framework（Py/TS）[17] | ~40 agent（Gemini CLI、Claude Code via adapter、Codex CLI…），client 含 Zed/JetBrains/Neovim [19] | TS/Py/.NET/Go 等 SDK；LangGraph/CrewAI/Mastra 集成 [22] |

## 3. 大厂支持矩阵

| | MCP | A2A | AG-UI | Zed ACP | 自家协议/变体 |
|---|---|---|---|---|---|
| OpenAI | ✅ Agents SDK/Responses/ChatGPT 连接器 [27] | 暂不在自家 SDK 内建 [45] | 未见官方表态 | Codex CLI 经 adapter [21] | Agentic Commerce Protocol [28][29]、Apps SDK（基于 MCP）、AGENTS.md [9] |
| Anthropic | ✅ 发起方，Claude 全系集成 [8] | 未见官方表态 | 未见官方表态 | Claude Code 经 Zed 自研 adapter 接入（非原生）[21] | MCP 本体、Agent Skills 约定 |
| Google | ✅ ADK 双向、Gemini API 直调远端 MCP、Cloud 托管 [34][35] | ✅ 发起方+LF 创始成员 [11][12] | ADK 列为 first-party 集成 [22] | Gemini CLI = 首个参考实现 [19] | A2UI（生成式 UI）[36]、AP2（支付）[37]、UCP（商务）[43] |
| 微软 | ✅ Build 2025：GitHub/VS Code/Copilot Studio/Foundry/Windows 全线；进 MCP 治理委员会 [30][33] | ✅ Foundry Agent Service、Copilot Studio、Teams AI [30] | ✅ Agent Framework 官方集成 [32] | — | NLWeb（每实例同时是 MCP server）[31] |

## 4. 变体与坑

**变体/适配**：MCP Apps（官方 ext）把 server 返回的 `ui://` 资源渲染为 iframe UI，统一了此前 MCP-UI 与 OpenAI Apps SDK 两套方案 [38]；AG-UI 可经 middleware 把 A2A agent 包成前端源 [22]；Claude Code/Codex CLI 靠社区/Zed adapter 进 ACP 生态 [21]。

**坑（按中招率排）**：
1. ACP 同名×4——引文档先看全称，IBM 版已停更并入 A2A [13][15][29][39]。
2. 「SSE 没了」误读——SDK/服务端仍可用 SSE 流式，只是不再有独立 HTTP+SSE 传输 [3][4]。
3. MCP 版本是日期不是语义版号；2026-07-28 版移除 initialize 握手与 `Mcp-Session-Id`，老 client/server 组合会断 [4][5]。
4. AP2 也有两个：Google Agent Payments Protocol vs ANP 的 Agent Payment Protocol [37][41]。
5. AG-UI 文档新旧并存：README 说 ~16 事件，spec 1.0 实列约 31 个 [24][47]。
6. IBM ACP 文档站仍在线但 repo 已归档——别照着建新系统 [15]。

## 5. 未决与置信度

- MCP HTTP+SSE 的确切移除日期：deprecated 登记页未逐一核对（只确认「≥12 个月保留」规则）[4]。
- AG-UI 是否移交基金会：官方未表态；spec 1.0 无正式公告日期（npm 发布日近似）。
- Anthropic 对 MCP 以外协议、OpenAI 对 AG-UI/Zed-ACP：均未见官方表态（截至 2026-09-25 查官方站）。
- A2A spec 站标最新 1.0.0，GitHub 已到 v1.0.1（patch 不参与版本协商）[14]。
- Agentic Commerce Protocol 发起方口径不一：Stripe docs 写含 Meta，GitHub 写 OpenAI+Stripe [29]。

## 来源

[1] MCP spec — https://modelcontextprotocol.io/specification
[2] MCP transports 2025-06-18 — https://modelcontextprotocol.io/specification/2025-06-18/basic/transports
[3] MCP transports 2025-03-26 — https://modelcontextprotocol.io/specification/2025-03-26/basic/transports
[4] MCP changelog 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/changelog
[5] MCP versioning — https://modelcontextprotocol.io/specification/versioning
[6] MCP authorization — https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
[7] MCP governance — https://modelcontextprotocol.io/community/governance
[8] Anthropic 发布 MCP — https://www.anthropic.com/news/model-context-protocol
[9] LF 成立 AAIF — https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
[10] A2A specification — https://a2a-protocol.org/latest/specification/
[11] Google 发布 A2A — https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
[12] Google 捐 A2A 给 LF — https://developers.googleblog.com/google-cloud-donates-a2a-to-linux-foundation/
[13] LF：ACP 并入 A2A — https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
[14] A2A v1.0.0 release — https://github.com/a2aproject/A2A/releases/tag/v1.0.0
[15] IBM acp repo（已归档） — https://github.com/i-am-bee/acp
[16] ACP-IBM 官网 — https://agentcommunicationprotocol.dev
[17] IBM Research ACP 页 — https://research.ibm.com/projects/agent-communication-protocol
[18] Zed ACP 协议概览 — https://agentclientprotocol.com/protocol/overview
[19] Zed：bring your own agent — https://zed.dev/blog/bring-your-own-agent-to-zed
[20] Zed×JetBrains — https://zed.dev/blog/jetbrains-on-acp
[21] Zed：Claude Code via ACP — https://zed.dev/blog/claude-code-via-acp
[22] AG-UI docs — https://docs.ag-ui.com/
[23] AG-UI spec 1.0 — https://docs.ag-ui.com/spec/1.0/index.md
[24] AG-UI events — https://docs.ag-ui.com/concepts/events
[25] AG-UI HTTP+SSE binding — https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse.md
[26] AG-UI 协议定位 — https://docs.ag-ui.com/agentic-protocols.md
[27] OpenAI Agents SDK MCP — https://openai.github.io/openai-agents-python/mcp/
[28] OpenAI Instant Checkout — https://openai.com/index/buy-it-in-chatgpt/
[29] Agentic Commerce Protocol — https://github.com/agentic-commerce-protocol/agentic-commerce-protocol
[30] Microsoft Build 2025 — https://blogs.microsoft.com/blog/2025/05/19/microsoft-build-2025-the-age-of-ai-agents-and-building-the-open-agentic-web/
[31] Microsoft NLWeb — https://news.microsoft.com/source/features/company-news/introducing-nlweb-bringing-conversational-interfaces-directly-to-the-web/
[32] Agent Framework AG-UI 集成 — https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/
[33] VS Code MCP GA — https://github.blog/changelog/2025-07-14-model-context-protocol-mcp-support-in-vs-code-is-generally-available/
[34] Google ADK MCP — https://adk.dev/tools-custom/mcp-tools/
[35] Gemini Interactions API — https://blog.google/innovation-and-ai/technology/developers-tools/interactions-api/
[36] Google A2UI — https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/
[37] Google AP2 — https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol
[38] MCP Apps 扩展 — https://modelcontextprotocol.io/extensions/apps/overview
[39] AGNTCY ACP spec — https://github.com/agntcy/acp-spec
[40] AGENTS.md — https://agents.md/
[41] ANP — https://github.com/agent-network-protocol/AgentNetworkProtocol
[43] Google UCP — https://developers.google.com/merchant/ucp
[45] openai-agents issue#472 — https://github.com/openai/openai-agents-python/issues/472
[47] ag-ui repo — https://github.com/ag-ui-protocol/ag-ui
