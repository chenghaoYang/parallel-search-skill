# Agent 时代的「协议」地图：MCP / A2A / ACP×4 / AG-UI

> 各协议规范哪条边、谁治理、怎么传输和鉴权、大厂各站哪边。截至 2026-09-25，均取自官方文档/公告。先读 §0，细节查 §2。

## 0. 一屏看懂

- **四个协议管四条不同的边，互补非竞争**：MCP=agent↔工具/数据，A2A=agent↔agent，Zed ACP=编辑器↔编程 agent，AG-UI=agent↔用户界面。[17]
- **「ACP」不是一个协议，是四个撞名缩写、其中两个已死**：IBM Agent **Communication** Protocol（2025-08 并入 A2A，仓库归档）[11][29]；Zed Agent **Client** Protocol（活跃，v1）[12]；OpenAI/Stripe Agentic **Commerce** Protocol（购物，beta）[20]；AGNTCY Agent **Connect** Protocol（2026-04 归档）[22]。看到 ACP 先问全名。
- **MCP 的 SSE 传输确实废弃了**：HTTP+SSE 传输自 2025-03-26 被 Streamable HTTP 取代，2026-07-28 追认 deprecated；SEP-2596 已 Final，最早移除窗口已到[2][3][34]。但 SSE 格式本身仍被 Streamable HTTP 用作流式回复载体——废弃的是「HTTP+SSE 绑定」[1]。
- **治理已向 Linux Foundation 收拢**：MCP 捐给 LF 旗下 AAIF[5]，A2A 捐给 LF 现为 AAIF Growth Stage[10][8]，IBM ACP 并入 A2A。仍是厂商项目的：Zed ACP（Apache）、AG-UI（MIT/CopilotKit）、A2UI（Apache/Google）。
- **大厂站位**：Google=A2A 发起方+自有一族协议（A2UI/AP2/UCP）；Microsoft 三家全接+NLWeb；OpenAI 全押 MCP（Apps SDK→MCP Apps）+商务 ACP，未见 A2A/AG-UI 官方支持；Anthropic=MCP 发起方，无产品级 A2A/AG-UI 声明，但有官方「MCP+A2A 互补」webinar 与 AG-UI quickstart。[23][25][19][35][36]
- **鉴权差异是选型关键**：MCP 有完整 OAuth 2.1 框架（可选）[4]；A2A 在 Agent Card 声明 5 种 securitySchemes[7]；Zed ACP 有 `authenticate`/`authMethods`（agent/terminal）[37]；AG-UI spec 明文不定义凭据，鉴权归 binding/应用层[16]。

## 1. Taxonomy

**分类轴 = 协议规范哪条边（连接哪两端）**，五个家族：

| 家族 | 边 | 成员 |
|---|---|---|
| F1 工具接入 | agent↔工具/数据 | MCP（边缘：UTCP/WebMCP）|
| F2 智能体互联 | agent↔agent（对等、不透明）| A2A；已死：IBM ACP、AGNTCY ACP |
| F3 宿主集成 | 编辑器↔agent | Zed ACP |
| F4 用户界面 | agent↔前端 UI | AG-UI（传输）；A2UI、MCP Apps（渲染格式）|
| F5 交易 | agent↔商户/支付 | ACP(Commerce)、AP2、UCP（只消歧）|

## 2. 对照矩阵

**身份与现状**

| | MCP | A2A | ACP-Zed | ACP-IBM | AG-UI |
|---|---|---|---|---|---|
| 连接两端 | Host/Client↔Server[1] | Client↔Remote Agent[7] | editor↔agent[12] | agent↔agent（已并入A2A）| agent backend↔前端[15] |
| 发起→治理 | Anthropic → AAIF（BDFL+SEP）[5][6] | Google → LF → AAIF Growth，8 家 TSC[23][10] | Zed，Apache，v1 稳定/v2 草案[14] | IBM → LF → 并入 A2A[11] | CopilotKit，MIT，双周 WG[18] |
| 版本 | 2026-07-28（第5版，已无状态化）| v1.0.1（1.0=2026-03）[8] | v1 | 已归档 | spec 1.0[16] |

**机制**

| | 传输 | 核心抽象 | 鉴权 | 发现 |
|---|---|---|---|---|
| MCP | stdio / Streamable HTTP，JSON-RPC 2.0[1] | tools/resources/prompts + elicitation | OAuth 2.1 子集，OPTIONAL；server 必实现 RFC9728[4] | server/discover + Registry（preview）[1][38] |
| A2A | 三绑定 JSON-RPC/gRPC/REST，SSE 流式[7] | Task（9 态）/Message/Artifact | Card 声明 APIKey/HTTP/OAuth2/OIDC/mTLS；生产必须 TLS[7] | /.well-known/agent-card.json（v0.3 前为 agent.json）[9] |
| ACP-Zed | JSON-RPC over stdio（SHOULD）；Streamable HTTP 草案[13] | session + prompt turn | `authenticate`+`authMethods`（agent/terminal）+`logout`[37] | 无 |
| AG-UI | 传输无关：SSE/WS/webhook/HTTP POST[15] | run(input)→BaseEvent 流，31 事件类型[16] | ∅ spec 不定义凭据（binding 携带）[16] | 无 |

**大厂支持（官方来源）**

| | MCP | A2A | AG-UI | 自家协议 |
|---|---|---|---|---|
| Anthropic | 发起方，已捐 AAIF；Claude 75+ connectors[31][5] | 无产品级支持；官方 webinar 定位「与 MCP 互补」[35] | 官方 quickstart 示例（非产品）[36] | — |
| OpenAI | Agents SDK/Apps SDK 全面 MCP（v0.0.7, 2025-03-26）[19][39] | 未找到官方支持 | 未找到（走 MCP Apps）| Agentic Commerce Protocol、AGENTS.md[20] |
| Google | Cloud MCP servers、ADK、Gemini SDK[24] | 发起方，Vertex/ADK | ADK 集成（AG-UI 官方表）[18] | A2UI、AP2、UCP[28][17] |
| Microsoft | Copilot Studio/Foundry/Windows ODR+MCP proxy[25][27] | Foundry Agent Service A2A head（GA）[26] | Agent Framework 官方集成[30] | NLWeb |

## 3. 变体与适配层

- **IBM ACP → A2A**：停开发、出迁移指南；BeeAI 演进为 Agent Stack，agent 自动暴露为 A2A-compatible[11][29]。
- **Claude Code → Zed ACP**：经 `claude-agent-acp` 适配器；Codex CLI、Copilot、Goose、Kimi CLI 等 ~40 个 agent 同路；客户端含 Zed/JetBrains/nvim/VS Code/Emacs[33]。
- **OpenAI Apps SDK → MCP Apps**：SEP-1865 已 Final，spec 原文称 "unifies the approaches pioneered by MCP-UI and the Apps SDK into a single, open standard"；为 2026-07-28 的 opt-in extension（ext-apps 仓独立版本化）[40][32]。
- **AG-UI 中间件定位**：事件流只需 "AG-UI-compatible"；有 A2A/MCP Apps 桥接，集成 LangGraph/CrewAI/ADK/Mastra/PydanticAI/Claude Agent SDK 等[18]。
- **AGNTCY 转向**：自有 ACP 归档后转为给官方 a2a-sdk 造 SLIM 传输；AGNTCY 栈=SLIM+DIR/OASF+Identity[22]。

## 4. 坑（按踩中概率）

1. **ACP 撞名**：四家同名不同物；IBM 与 AGNTCY 两家已归档，网上大量文章还当它们是活跃协议。[11][12][20][22]
2. **「MCP 用 SSE」已过时**：应改用 Streamable HTTP；SEP-2596 Final（2026-05-18）+3 个月窗口已过，下一 revision 可移除。[2][3][34]
3. **A2A well-known 路径改名**：v0.3 起 `agent.json`→`agent-card.json`，旧教程 404；v1.0 又移除 REST URL 的 /v1 前缀（breaking）。[8]
4. **MCP auth 落地摩擦**：OAuth 2.1 + RFC8707 + RFC9728；授权服务器无 DCR 时 client 只能硬编码 client ID 或弹 UI。[4]
5. **AG-UI「~16 events」已过时**：spec 1.0 EventType 实为 31 个活跃类型。[16]
6. **归档无宣告**：AGNTCY ACP 静默归档（README 无 deprecation banner），协议死活要看仓库状态。[22]
7. **分层说法非唯一正解**：「AG-UI/A2A/MCP 三层」是官方口径；A2UI 可跑在 A2A/AG-UI 之上，MCP Apps 把 UI 塞回了 MCP。[17][28][40]

## 5. 未决与置信度

- OpenAI 对 A2A/AG-UI：GitHub org 与文档站均无命中——「未见官方支持」≠「反对」。
- Copilot Studio 的 A2A 仅 2025-05「coming soon」，未见 GA；Foundry 侧已 GA。
- 商务 ACP 共创者两说：Stripe 文档含 Meta，agenticcommerce.dev 只写 Stripe+OpenAI[21]。
- AG-UI 未入 AAIF（创始项目仅 MCP/goose/AGENTS.md）[32]；ANP/UTCP/WebMCP/NLIP 等长尾仅点名存在。

## 来源

[1] MCP Specification — https://modelcontextprotocol.io/specification
[2] MCP 2025-03-26 changelog — https://modelcontextprotocol.io/specification/2025-03-26/changelog
[3] MCP Deprecated registry — https://modelcontextprotocol.io/specification/2026-07-28/deprecated
[4] MCP Authorization — https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
[5] MCP joins AAIF — https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
[6] MCP Governance — https://modelcontextprotocol.io/community/governance
[7] A2A specification — https://github.com/a2aproject/A2A/blob/main/docs/specification.md
[8] A2A CHANGELOG — https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md
[9] A2A discovery — https://github.com/a2aproject/A2A/blob/main/docs/topics/agent-discovery.md
[10] LF launches A2A — https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents
[11] ACP joins A2A — https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
[12] agent-client-protocol — https://github.com/zed-industries/agent-client-protocol
[13] ACP transports — https://agentclientprotocol.com/protocol/v1/transports
[14] Zed ACP 发布博文 — https://zed.dev/blog/bring-your-own-agent-to-zed
[15] AG-UI intro — https://docs.ag-ui.com/introduction
[16] AG-UI events/transports — https://docs.ag-ui.com/concepts/events ; https://docs.ag-ui.com/spec/1.0/basic/transports/index.md
[17] Google agent protocols guide — https://developers.googleblog.com/en/developers-guide-to-ai-agent-protocols/
[18] ag-ui-protocol/ag-ui — https://github.com/ag-ui-protocol/ag-ui
[19] OpenAI Apps SDK quickstart — https://developers.openai.com/apps-sdk/quickstart
[20] OpenAI ACP (Instant Checkout) — https://openai.com/index/buy-it-in-chatgpt/
[21] Agentic Commerce Protocol — https://www.agenticcommerce.dev/
[22] agntcy/acp-spec (archived) — https://github.com/agntcy/acp-spec
[23] A2A launch — https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
[24] Google Cloud MCP — https://docs.cloud.google.com/mcp/overview
[25] MS Cloud blog: A2A — https://www.microsoft.com/en-us/microsoft-cloud/blog/2025/05/07/empowering-multi-agent-apps-with-the-open-agent2agent-a2a-protocol/
[26] Foundry Agent Service GA — https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/announcing-general-availability-of-azure-ai-foundry-agent-service/4414352
[27] Windows Ignite 2025 — https://blogs.windows.com/windowsdeveloper/2025/11/18/ignite-2025-furthering-windows-as-the-premier-platform-for-developers-governed-by-security/
[28] Google A2UI — https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/
[29] i-am-bee/acp (archived) — https://github.com/i-am-bee/acp
[30] MS Agent Framework × AG-UI — https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/
[31] Anthropic MCP launch — https://www.anthropic.com/news/model-context-protocol
[32] OpenAI: Agentic AI Foundation — https://openai.com/index/agentic-ai-foundation/
[33] ACP agents — https://agentclientprotocol.com/get-started/agents
[34] SEP-2596 — https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2596
[35] Anthropic MCP+A2A webinar — https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai
[36] claude-quickstarts AG-UI — https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/copilot-kit-ag-ui
[37] ACP v1 schema — https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/schema.json ; https://agentclientprotocol.com/protocol/authentication
[38] MCP Registry — https://raw.githubusercontent.com/modelcontextprotocol/registry/main/README.md
[39] agents-python v0.0.7 — https://github.com/openai/openai-agents-python/releases/tag/v0.0.7
[40] MCP Apps — https://raw.githubusercontent.com/modelcontextprotocol/ext-apps/main/README.md
