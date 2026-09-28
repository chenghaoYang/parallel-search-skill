# Agent 时代的「协议」地图

> 回答：MCP / A2A / 各家的「ACP」/ AG-UI 分别管哪一段、谁治理、大厂支持谁、怎么选。截至 2026-09-25，事实均出自官方文档（[n] 见文末）。

## 0. 一屏看懂

1. **按「谁在跟谁说话」分五层**，不互斥、真实系统里叠着用：agent↔工具(MCP)、agent↔agent(A2A)、agent↔界面(AG-UI/MCP Apps/A2UI)、IDE↔agent(Zed ACP)、agent↔支付/商业(ACP-commerce/UCP/AP2/x402)。
2. **「ACP」至少有四个，不是一回事**：IBM Agent Communication Protocol（agent↔agent，2025-08-29 已并入 A2A）[11][20]；Zed Agent Client Protocol（编辑器↔coding agent）[14]；OpenAI/Stripe Agentic Commerce Protocol（支付）[16]；AGNTCY Agent Connect Protocol（agent 调用，疑似弃用）[18][19]。引用前先确认全称和仓库 org。
3. **MCP 的 SSE：半对**。被废弃的是独立的「HTTP+SSE 传输」——2025-03-26 被 Streamable HTTP 取代（"Replaced the previous HTTP+SSE transport"），2026-07-28 正式列入 Deprecated [2][3][4]；SSE 机制本身仍在 Streamable HTTP 内部用于流式推送 [3]。
4. **治理大迁移到 Linux Foundation 系**：MCP、AGENTS.md、goose 进 AAIF（2025-12-09）；A2A 先入 LF 再入 AAIF（2026-08-27）；x402 进 LF x402 Foundation；AG-UI 仍归 CopilotKit，Zed ACP 归自家 org [6][9][13][21]。
5. **大厂站位**：MCP 四家全支持（事实标准）；A2A 由 Google/Microsoft/AWS/IBM 站台，OpenAI 不在 SDK 内置 [33]；UI 层 OpenAI+Anthropic 共建 MCP Apps、Google 另推 A2UI；商务层分裂为 OpenAI/Stripe ACP vs Google/Shopify UCP。
6. **选型**：接工具/数据用 MCP；跨组织多 agent 协作用 A2A；编辑器内嵌 agent 用 Zed ACP；自建前端用 AG-UI、宿主内嵌 UI 用 MCP Apps；收款按阵营选 ACP-commerce 或 UCP/AP2，机器微支付看 x402。

## 1. Taxonomy

**分类轴 = 交互的两端是谁**；第二轴区分「线上协议（wire protocol）」与「负载格式/约定」——后者没有自己的传输层，骑在前者上面。

| 层 | 家族 | 成员 | 为什么一类 |
|---|---|---|---|
| L1 agent↔工具/数据 | MCP | MCP + 官方扩展 MCP Apps | Host/Client/Server、JSON-RPC 工具调用 |
| L2 agent↔agent | A2A 系 | A2A；IBM-ACP（已并入）；AGNTCY ACP（疑弃）；ANP/AITP（边缘） | 任务委派/消息/发现 |
| L3 agent↔界面 | UI 层 | AG-UI（运行时事件流）；MCP Apps、A2UI（UI 负载格式） | 把 agent 输出变成可交互 UI |
| L4 IDE↔agent | 客户端协议 | Zed ACP | 编辑器为宿主、agent 为子进程，类比 LSP |
| L5 agent↔商业 | 支付/电商 | ACP-commerce、UCP、AP2、x402 | checkout、支付凭证、HTTP 402 |
| 周边 | 约定/目录 | AGENTS.md、WebMCP、NLWeb、MCP Registry | 常被误当协议 |

## 2. 对照矩阵（线上协议）

| 协议 | 两端 | 发起→治理 | 传输/格式 | 核心抽象 | 版本/状态 | 鉴权 |
|---|---|---|---|---|---|---|
| **MCP** | agent↔tool | Anthropic 2024-11→AAIF | JSON-RPC 2.0 over stdio 或 Streamable HTTP（单端点 POST+GET）[3] | Tools/Resources/Prompts；Sampling/Roots/Elicitation | 当前 2026-07-28（版本号=最后不兼容日期）[1][4] | OPTIONAL OAuth 2.1：RFC9728/8707、PKCE [5] |
| **A2A** | agent↔agent | Google 2025-04→LF→AAIF | 三 binding：JSON-RPC(SSE)/gRPC/HTTP+JSON REST [8] | AgentCard(`/.well-known/agent-card.json`)/Task/Message/Part/Artifact [8] | v1.0.0（2026-03-12）[10] | AgentCard 宣告 securitySchemes：APIKey/HTTP/OAuth2/OIDC/mTLS [8] |
| **IBM ACP** | agent↔agent+人 | IBM BeeAI→并入 A2A | REST/OpenAPI | 多模态消息、流式、能力发现 | 2025-08-29 归档停开发 [11][20] | — |
| **Zed ACP** | IDE↔agent | Zed→agentclientprotocol org | JSON-RPC over stdio；远程 HTTP/WS [14] | session/new·prompt·update、request_permission、terminal/*、fs/* [15] | 稳定版 v1 [14] | agent 宣告 authMethods，authenticate 方法 [15] |
| **AGNTCY ACP** | agent↔agent 调用 | AGNTCY collective（Cisco） | REST/OpenAPI | /agents/search、/threads、/runs [18] | spec 0.2.3，官网组件已无 ACP（疑弃）[19] | ❓ |
| **AG-UI** | agent↔前端 | CopilotKit 2025-05→自家 Working Group | 传输无关（SSE/WS/webhooks）；HttpAgent=POST RunAgentInput→BaseEvent 流 [21][22] | run()→事件流 31+ 类（Lifecycle/Text/ToolCall/State/Reasoning；STATE_DELTA=RFC 6902）[22] | @ag-ui/core 1.0.0（2026-09-17）[23] | spec 未定义 ∅ |
| **ACP-commerce** | agent↔商户 | OpenAI+Stripe | REST/JSON（"REST and MCP compatible"）[16] | POST /checkout_sessions 生命周期 + Delegate Payment + product feed [16] | 日期版本，最新稳定 2026-04-17（beta）[16] | Bearer（REQUIRED）+Idempotency-Key+签名 [16] |
| **UCP** | agent↔电商全链路 | Google+Shopify 2026-01 | ❓ | 发现→结算→售后；兼容 A2A/AP2/MCP [31] | ⚠ | ❓ |
| **AP2** | agent 支付授权 | Google 2025-09→FIDO Alliance TWG | A2A/MCP 的扩展 [28] | 支付授权凭证 mandates（细节未核） | v0.2 [29] | ❓ |
| **x402** | agent 机器支付 | Coinbase→LF x402 Foundation | HTTP 402 响应内嵌 pay-and-retry [32] | 稳定币为主、blockchain-agnostic | 2026-07-14 operational；40 成员含 Visa/MC/Stripe [32] | ❓ |

## 3. 变体与适配层

| 实体 | 是什么 | 与主线协议的关系 |
|---|---|---|
| **MCP Apps** | MCP 官方扩展（SEP-1865，stable 2026-01-26）：tool 经 `_meta.ui.resourceUri` 指 `ui://` HTML 资源，沙箱 iframe + postMessage 上跑 ui/* 方言 JSON-RPC [24] | 由 OpenAI Apps SDK（2025-10 preview）+ Anthropic + MCP-UI 三方收敛；hosts 含 Claude、ChatGPT、VS Code Copilot、M365 Copilot、Goose [24][26] |
| **MCP-UI** | Ido Salomon 的社区先行版 | 已并入 MCP Apps，老包变兼容实现 [25] |
| **A2UI** | Google 2025-12 的声明式 JSON UI **格式**（非 wire 协议），v0.9.1 [27] | 负载可走 A2A/AG-UI/MCP；与 AG-UI 互补（AG-UI=运行时连接，A2UI=数据格式） |
| **AGENTS.md** | 指导 coding agent 的 Markdown 约定，OpenAI 2025-08→AAIF，60k+ 项目 [30] | 不是协议 |
| **WebMCP** | W3C CG draft（Edge+Chrome 提案）：浏览器 JS API 让网页向 agent 暴露 tools [42] | 「网页版 MCP」；仅 Chromium preview |
| **NLWeb** | 微软「agentic web 的 HTML」[39] | 每个 NLWeb endpoint 也是 MCP server |
| **AGNTCY** | LF Projects 独立项目（≠AAIF），Cisco/Outshift 发起 | 组件=Directory/SLIM/OASF/Identity；AgentBridge 走 A2A，自家 ACP 让位 [19] |
| **ANP / AITP** | ANP=DID 身份+发现+加密消息栈；AITP=NEAR 的信任边界通信 [40][41] | 边缘协议 |

## 4. 大厂支持

| 厂商 | 发起/捐出 | 官方支持 | 备注 |
|---|---|---|---|
| **OpenAI** | AGENTS.md、ACP-commerce（与 Stripe）、Apps SDK | MCP：Responses API `type:"mcp"`、ChatGPT plugins、Codex [33] | 拒绝 SDK 内置 A2A（issue #472，2026-08-05）[33]；共建 MCP Apps |
| **Anthropic** | MCP（2024-11-25）→AAIF | Claude Integrations；Messages API MCP connector（beta header `mcp-client-2025-11-20`）[34][35] | 共建 MCP Apps；A2A/AG-UI 无官方表态 |
| **Google** | A2A（2025-04-09→LF→AAIF）、AP2、A2UI、UCP（与 Shopify） | Gemini API/Gen AI SDK/ADK 原生 MCP+A2A；Cloud 托管 MCP servers [36][37] | A2A 官方定位「complements MCP」[38] |
| **Microsoft** | NLWeb；WebMCP 联合提案 | MCP 横跨 GitHub/Copilot Studio/D365/Foundry/SK/Windows 11；A2A 进 Foundry+Copilot Studio [39] | 加入 MCP Steering Committee 与 A2A TSC [39] |
| IBM / AWS | IBM：ACP→并入 A2A，获 TSC 席位 [11] | AWS：Bedrock AgentCore 原生 A2A；x402 Foundation 成员 [12][32] | — |

## 5. 坑与未决

**坑**：
1. **ACP 重名**：四个协议同缩写，引用/选型前看全称（§0.2）。
2. **MCP 版本 churn 快**：2026-07-28 删 initialize 握手与 `Mcp-Session-Id` 变无状态、Roots/Sampling/Logging 弃用、DCR 弃用——旧实现要跟着升级 [4]。
3. **AG-UI 不管鉴权**：spec 无 auth 定义，自行在 proxy 层做；官网徽章写 Apache 2.0 与仓库 LICENSE(MIT) 不一致，以 LICENSE 为准 [21]。
4. **A2A 无强制默认 binding**：AgentCard 宣告什么用什么；README 仍写「JSON-RPC 2.0 over HTTP(S)」，滞后于 v1.0 [8]。
5. **MCP Registry 仍 preview**：API freeze v0.1，GA 未定 [7]。

**未决/置信度**：
- AGNTCY ACP 无正式废弃声明（仓库 2025-05 停更、官网组件无 ACP、docs 页 404）→「事实上弃用」为推断 [18][19]。
- OpenAI 产品层（ChatGPT）对 A2A 无表态，仅 SDK 层拒绝 [33]；AG-UI 未入 AAIF、Working Group 章程未公开。
- HTTP+SSE 彻底移除版本未定（lifecycle ≥12 个月窗口）；UCP/AP2/x402 细节仅定位级核实；ANP/AITP 为边缘协议。

## 来源

[1] modelcontextprotocol.io/specification/versioning
[2] modelcontextprotocol.io/specification/2025-03-26/changelog
[3] modelcontextprotocol.io/specification/2025-06-18/basic/transports
[4] modelcontextprotocol.io/specification/2026-07-28/changelog
[5] modelcontextprotocol.io/specification/2025-06-18/basic/authorization
[6] linuxfoundation.org/press/…formation-of-the-agentic-ai-foundation
[7] github.com/modelcontextprotocol/registry
[8] raw.githubusercontent.com/a2aproject/A2A/main/docs/specification.md
[9] linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project
[10] A2A v1.0 公告 — github.com/a2aproject/A2A docs/blog/posts/announcing-1.0.md
[11] lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-…
[12] linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations
[13] A2A 入 AAIF — github.com/a2aproject/A2A docs/blog/posts/a2a-joins-aaif.md
[14] github.com/agentclientprotocol/agent-client-protocol
[15] agentclientprotocol.com/protocol/overview
[16] github.com/agentic-commerce-protocol/agentic-commerce-protocol；agenticcommerce.dev
[17] developers.openai.com/commerce/
[18] github.com/agntcy/acp-spec
[19] agntcy.org；docs.agntcy.org
[20] github.com/i-am-bee/acp
[21] github.com/ag-ui-protocol/ag-ui
[22] docs.ag-ui.com/concepts/events；docs.ag-ui.com/concepts/architecture
[23] registry.npmjs.org/@ag-ui/core
[24] modelcontextprotocol.io/extensions/apps；github.com/modelcontextprotocol/ext-apps
[25] mcpui.dev；github.com/MCP-UI-Org/mcp-ui
[26] developers.openai.com/apps-sdk/mcp-apps-in-chatgpt
[27] a2ui.org；developers.googleblog.com/en/introducing-a2ui-…
[28] cloud.google.com/blog/…/announcing-agents-to-payments-ap2-protocol
[29] ap2-protocol.org
[30] agents.md；openai.com/index/agentic-ai-foundation/
[31] blog.google/products/ads-commerce/agentic-commerce-ai-tools-protocol-retailers-platforms/
[32] linuxfoundation.org/press/…operational-launch-of-x402-foundation…；x402.org
[33] developers.openai.com/api/docs/mcp；github.com/openai/openai-agents-python/issues/472
[34] platform.claude.com/docs/…/mcp-connector
[35] anthropic.com/news/model-context-protocol；claude.com/blog/integrations
[36] opensource.googleblog.com/2026/04/a-year-of-open-collaboration-…
[37] ai.google.dev/gemini-api/docs/interactions/function-calling；docs.cloud.google.com/mcp
[38] developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability
[39] blogs.microsoft.com/blog/2025/05/19/microsoft-build-2025-…；microsoft.com/microsoft-cloud/blog/2025/05/07/…a2a…/
[40] agent-network-protocol.com
[41] github.com/nearai/aitp
[42] w3c-cg.github.io/aikr/webMCP/webmcp-technical-notes.html
