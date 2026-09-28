# Agent 时代的「协议」地图：MCP / A2A / ACP×N / AG-UI

> 回答：这些协议各规范哪条边、谁治理、怎么传输和鉴权、大厂各站哪边。截至 2026-09-25，事实均取自官方文档与公告。先读 §0 建立认知，细节查 §2 表。

## 0. 一屏看懂

- **四个协议管四条不同的边，互补而非竞争**：MCP=agent↔工具/数据，A2A=agent↔agent，Zed ACP=编辑器↔编程 agent，AG-UI=agent↔用户界面。官方口径："MCP connects agents to tools and data. A2A connects agents to other agents."[17]
- **「ACP」不是一个协议，而是至少三个撞名缩写**：IBM 的 Agent **Communication** Protocol（已并入 A2A）、Zed 的 Agent **Client** Protocol（活跃中）、OpenAI/Stripe 的 Agentic **Commerce** Protocol（购物结账）；Cisco AGNTCY 还有第四个 Agent **Connect** Protocol。看到 ACP 先问全名。[11][12][20][22]
- **MCP 的 SSE 传输确实废弃了**：spec 2025-03-26 用 Streamable HTTP 取代 HTTP+SSE 传输，2026-07-28 追认 "deprecated since 2025-03-26"[2][3]。注意废弃的是「HTTP+SSE 这个传输绑定」——SSE 格式仍被 Streamable HTTP 用作流式回复的载体[1]。
- **治理已向 Linux Foundation 收拢**：MCP 2025-12 捐给 LF 旗下 AAIF（Agentic AI Foundation）[5]，A2A 2025-06 捐给 LF、现为 AAIF Growth Stage 项目[10][8]，IBM ACP 2025-08 并入 A2A 后归档停更[11][29]。仍属厂商项目的：Zed ACP（Apache）、AG-UI（MIT, CopilotKit）、A2UI（Apache, Google）。
- **大厂站位**：Google=A2A 发起方且自有一族协议（A2UI/AP2/UCP）；Microsoft 三家全接（MCP/A2A/AG-UI）另有 NLWeb；OpenAI 全押 MCP（Apps SDK→MCP Apps）+ 商务 ACP；Anthropic 是 MCP 发起方，对 A2A/AG-UI 无官方表态。[23][25][19][31]
- **鉴权差异是选型关键**：MCP 有完整 OAuth 2.1 授权框架（可选启用）[4]；A2A 在 Agent Card 声明 5 种 securitySchemes[7]；Zed ACP 是 stdio 子进程、没有网络鉴权概念[13]；AG-UI spec 完全不定义鉴权[16]。

## 1. Taxonomy

**分类轴 = 协议规范哪条边（连接哪两端）**，五个家族：

| 家族 | 边 | 成员 |
|---|---|---|
| F1 工具接入 | agent↔工具/数据 | MCP（边缘：UTCP、WebMCP）|
| F2 智能体互联 | agent↔agent（对等、不透明）| A2A；已并入：IBM ACP；相邻栈：AGNTCY |
| F3 宿主集成 | 编辑器/客户端↔agent | Zed ACP |
| F4 用户界面 | agent↔前端 UI | AG-UI（事件传输）；A2UI、MCP Apps（渲染格式）|
| F5 交易 | agent↔商户/支付 | ACP(Commerce)、AP2、UCP——本文只消歧 |

维度清单：D1 连接两端｜D2 发起与治理｜D3 传输与格式｜D4 核心抽象｜D5 鉴权｜D6 版本状态｜D7 发现机制｜D8 大厂支持｜D9 与 MCP 关系。

## 2. 对照矩阵

**身份与现状**

| | MCP | A2A | ACP-Zed | ACP-IBM | AG-UI |
|---|---|---|---|---|---|
| 连接两端 | Host/Client↔Server[1] | Client↔Remote Agent[7] | editor↔agent[12] | agent↔agent（已并入A2A）| agent backend↔前端[15] |
| 发起→治理 | Anthropic 2024-11 → AAIF，BDFL+SEP 流程[5][6] | Google 2025-04 → LF → AAIF Growth，8 家 TSC[23][10] | Zed，Apache，v1 稳定/v2 草案[14] | IBM 2025-03 → LF → 2025-08 并入 A2A[11] | CopilotKit，MIT，双周 WG[18] |
| 版本 | 2026-07-28（第 5 版，已无状态化）| v1.0.1（1.0=2026-03-12）| v1 | 已归档 | spec 1.0 |

**机制**

| | 传输 | 核心抽象 | 鉴权 | 发现 |
|---|---|---|---|---|
| MCP | stdio / Streamable HTTP，JSON-RPC 2.0[1] | tools/resources/prompts + elicitation | OAuth 2.1 子集，OPTIONAL；server=Resource Server 必实现 RFC9728[4] | server/discover + list RPC + Registry[1] |
| A2A | 三绑定 JSON-RPC/gRPC/REST，SSE 流式[7] | Task（9 态）/Message/Artifact | Card 声明 APIKey/HTTP/OAuth2/OIDC/mTLS，凭证带外获取，生产必须 TLS[7] | /.well-known/agent-card.json（v0.3 前为 agent.json）[9] |
| ACP-Zed | JSON-RPC over stdio（SHOULD）；Streamable HTTP 草案[13] | session + prompt turn | ∅ 无 | ∅ 无 |
| AG-UI | 传输无关：SSE/WS/webhook/HTTP POST+二进制[15] | run(input)→BaseEvent 流，31 事件类型[16] | ∅ spec 不定义 | ∅ 无 |

**大厂支持（官方来源）**

| | MCP | A2A | AG-UI | 自家协议 |
|---|---|---|---|---|
| Anthropic | 发起方，已捐 AAIF；Claude 75+ connectors[31][5] | ∅ 未表态 | ∅ | — |
| OpenAI | Agents SDK/Agents API/Apps SDK 全面 MCP[19] | ∅ 未见 | ∅（走 MCP Apps）| Agentic Commerce Protocol（与 Stripe）、AGENTS.md[20] |
| Google | Cloud 官方 MCP servers、ADK、Gemini SDK[24] | 发起方，Vertex/ADK | ADK 集成（AG-UI 官方表）| A2UI、AP2、UCP[28][17] |
| Microsoft | Copilot Studio/Foundry/Windows ODR+MCP proxy[25][27] | Foundry Agent Service A2A API head（GA）[26] | Agent Framework 官方集成[30] | NLWeb |

## 3. 变体与适配层

- **IBM ACP → A2A**：ACP 团队停开发、出迁移指南；BeeAI 平台演进为 Agent Stack，agent 自动暴露为 A2A-compatible[11][29]。
- **Claude Code → Zed ACP**：官方 agents 列表经 `zed-industries/claude-agent-acp` 适配器接入；Codex CLI、GitHub Copilot、Goose、Kimi CLI 等 ~40 个 agent 同路[33]。客户端侧 Zed/JetBrains/neovim/VS Code/Emacs 等均支持。
- **OpenAI Apps SDK → MCP Apps**：ChatGPT apps 的 UI 变体已与 Anthropic/MCP-UI 合作上游化为 MCP 规范的 MCP Apps 扩展，`window.openai` 仅剩专有扩展[32]。
- **AG-UI 中间件定位**：事件流不必精确匹配格式，"AG-UI-compatible" 即可；有 A2A/MCP Apps 桥接器，集成 LangGraph/CrewAI/ADK/Mastra/PydanticAI/Claude Agent SDK 等[18]。

## 4. 坑（按踩中概率）

1. **ACP 撞名**：IBM/Zed/OpenAI-Stripe 三家同名不同物，AGNTCY 还有第四个。读文章/选型前必须展开缩写。[11][12][20][22]
2. **「MCP 用 SSE」已过时**：2025-03-26 前的教程教你自建 SSE server，现在应是 Streamable HTTP；旧绑定仅作向后兼容保留，SEP-2596 Final 后三个月可移除。[2][3]
3. **A2A well-known 路径改名**：v0.3 起 `agent.json` → `agent-card.json`，旧教程 404；v1.0 又移除 REST URL 的 /v1 前缀（breaking）。[8]
4. **MCP auth 落地摩擦**：spec 要求 OAuth 2.1 + RFC8707 resource indicators + RFC9728；授权服务器无 DCR 时 client 只能硬编码 client ID 或弹 UI 让用户填。[4]
5. **AG-UI「~16 events」已过时**：README/旧文写 16，spec 1.0 EventType 实为 31 个活跃类型（含 Reasoning/Subagent 类）。[16]
6. **分层说法非唯一正解**：「AG-UI 管 UI、A2A 管互联、MCP 管工具」是官方推销口径；实际 A2UI 可跑在 A2A/AG-UI 之上，MCP Apps 把 UI 塞回了 MCP。[17][28][32]

## 5. 未决与置信度

- OpenAI/Anthropic 对 A2A 无官方立场可引（查过官网与 AAIF 公告，无表态≠反对）。
- Copilot Studio 的 A2A 仅有 2025-05「coming soon」公告，未见 GA；Foundry 侧已 GA。
- OpenAI 采纳 MCP 的官宣日期只见 Altman X 帖，openai.com 无对应页（二手）。
- AGNTCY Agent Connect Protocol 维护状态未核实（spec 仓库存在）。
- IBM ACP 原 REST 端点细节已随文档站下线，无法取原句。

## 来源

[1] MCP Specification (current) — https://modelcontextprotocol.io/specification
[2] MCP 2025-03-26 changelog — https://modelcontextprotocol.io/specification/2025-03-26/changelog
[3] MCP Deprecated registry — https://modelcontextprotocol.io/specification/2026-07-28/deprecated
[4] MCP Authorization — https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
[5] MCP joins AAIF — https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
[6] MCP Governance — https://modelcontextprotocol.io/community/governance
[7] A2A specification — https://github.com/a2aproject/A2A/blob/main/docs/specification.md
[8] A2A CHANGELOG — https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md
[9] A2A Agent Discovery — https://github.com/a2aproject/A2A/blob/main/docs/topics/agent-discovery.md
[10] LF launches A2A project — https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents
[11] ACP joins A2A (LF AI & Data) — https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
[12] zed-industries/agent-client-protocol — https://github.com/zed-industries/agent-client-protocol
[13] ACP v1 transports — https://agentclientprotocol.com/protocol/v1/transports
[14] Zed: bring your own agent — https://zed.dev/blog/bring-your-own-agent-to-zed
[15] AG-UI introduction — https://docs.ag-ui.com/introduction
[16] AG-UI events — https://docs.ag-ui.com/concepts/events
[17] Google: developer's guide to AI agent protocols — https://developers.googleblog.com/en/developers-guide-to-ai-agent-protocols/
[18] ag-ui-protocol/ag-ui — https://github.com/ag-ui-protocol/ag-ui
[19] OpenAI Apps SDK quickstart — https://developers.openai.com/apps-sdk/quickstart
[20] OpenAI: Buy it in ChatGPT (ACP) — https://openai.com/index/buy-it-in-chatgpt/
[21] Agentic Commerce Protocol — https://www.agenticcommerce.dev/
[22] agntcy/acp-spec — https://github.com/agntcy/acp-spec
[23] Google: A2A launch — https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
[24] Google Cloud MCP — https://docs.cloud.google.com/mcp/overview
[25] Microsoft Cloud blog: A2A — https://www.microsoft.com/en-us/microsoft-cloud/blog/2025/05/07/empowering-multi-agent-apps-with-the-open-agent2agent-a2a-protocol/
[26] Azure AI Foundry Agent Service GA — https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/announcing-general-availability-of-azure-ai-foundry-agent-service/4414352
[27] Windows Ignite 2025 (ODR/MCP) — https://blogs.windows.com/windowsdeveloper/2025/11/18/ignite-2025-furthering-windows-as-the-premier-platform-for-developers-governed-by-security/
[28] Google A2UI — https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/
[29] i-am-bee/acp (archived) — https://github.com/i-am-bee/acp
[30] MS Agent Framework AG-UI — https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/
[31] Anthropic: MCP announcement — https://www.anthropic.com/news/model-context-protocol
[32] OpenAI: Agentic AI Foundation (MCP Apps) — https://openai.com/index/agentic-ai-foundation/
[33] ACP agents list — https://agentclientprotocol.com/get-started/agents
