# 四条线：MCP、A2A、两个 ACP、AG-UI

> 每条协议接谁、管什么、鉴权/版本/治理、怎么叠用。依据是 2026-09-24 前的官网原文。先读第 0 节。四家产品文档未核，不下「某厂已支持」。

## 0. 一屏看懂

1. 按两端选。MCP：Host 内的 Client ↔ Server。A2A：Client ↔ Remote Agent。Zed 的 Agent Client Protocol：编辑器 ↔ 编码 Agent。AG-UI：发事件的 producer ↔ 读事件的 consumer。[1][8][16][24]
2. IBM 的 Agent Communication Protocol 现写 “ACP is now part of A2A under the Linux Foundation!”，`i-am-bee/acp` 于 2025-08-27 归档。Zed 这条全称是 Agent Client Protocol，稳定版为 `1`，Zed 与 JetBrains 治理。两边页面都没有对方的名字。[13][15][16][22][39]
3. 鉴权不通用。MCP 的 HTTP 授权可选，做了就要 OAuth 2.1 和 RFC9728。A2A 看 `securitySchemes`。Zed ACP 看 `authMethods`。AG-UI 不定义凭据。字段在第 2 节。[4b][8][19][26]
4. 版本号不能套用：MCP `2026-07-28`，A2A 规范站 `1.0.0`，Zed ACP 稳定版 `1`（v2 仍是 Draft），AG-UI `1.0`，IBM OpenAPI `0.2.0`。[1][8][14][22][23]
5. 治理不在一处：MCP 于 2025-12-09 捐入 AAIF；A2A 由八席 TSC 管，2026-08-27 成为 AAIF Growth Stage；AG-UI 由 CopilotKit 发起，MIT，未见基金会。[6][10][11][28]
6. 四厂是否支持：只有协议站上的点名。HTTP+SSE 是否废弃：与旧教程相反，下表有原句，复核前不收成口号。

## 1. Taxonomy

分类轴是线上两端：同端可替代，异端则叠放。

| 家族 | 两端 | 现行代表 | 管什么 |
|---|---|---|---|
| 能力与上下文 | Client ↔ Server | MCP | Resources、Prompts、Tools |
| 智能体互操作 | Client ↔ 远端 Agent | A2A | 把任务交给另一个智能体。IBM ACP 是 2025-08 并入的前身 |
| 编辑器客户端 | 编辑器 ↔ 编码 Agent | Agent Client Protocol | 编辑器如何拉起代理；官方类比 LSP |
| 生成式界面 | producer ↔ consumer | AG-UI | 一次 run 的事件流如何进应用 |

| 两端 | 采用 |
|---|---|
| 应用要工具、数据、提示模板 | MCP |
| 智能体把任务交给另一个智能体 | A2A |
| 编辑器按需拉起编码代理 | Agent Client Protocol |
| 界面消费事件流 | AG-UI |
| 手里是 IBM ACP 的 REST / Run | 迁到 A2A；仓库已只读 [15] |

## 2. 对照矩阵

| | 角色与对象 | 发现 | 传输与流 |
|---|---|---|---|
| MCP | Host 发起。Client 与一个 Server 1:1。Server：Resources、Prompts、Tools。首页的 client 能力只列 Elicitation。Roots、Sampling、Logging 在 2026-07-28 标 Deprecated[1][2][3] | 必须实现 `server/discover`。同版删除 `initialize`，版本和能力改放每请求 `_meta`。`tools/list`、`resources/list`、`prompts/list` 仍在 [3][7] | 只有 stdio 与 Streamable HTTP。响应是一个 JSON，或该请求内的 SSE。POST 必须带 `MCP-Protocol-Version`。HTTP+SSE 传输自 `2025-03-26` 起 Deprecated（SEP-2596）。2026-07-28 删除 GET 流与 `Last-Event-ID` [3b][4] |
| A2A | Client 发请求，Remote Agent 处理任务。不管子智能体和工具调用（那是框架或 MCP 的事）[8][9] | `https://{server_domain}/.well-known/agent-card.json` [8] | 绑定 `JSONRPC`、`GRPC`、`HTTP+JSON`。JSON-RPC 2.0 over HTTP(S) 与 REST 的流式都是 SSE。生产用 HTTPS/TLS [8] |
| ACP-IBM | client 请求 server；一个 server 可托管多个 agent，REST。一次执行是 Run。`RunStatus`：`created` `in-progress` `awaiting` `cancelling` `cancelled` `completed` `failed` [14][15][38] | well-known 上的 YAML manifest；注册表尚未进规范 [29] | OpenAPI 含 `text/event-stream` [14] |
| ACP-Zed | 子进程里的编码 Agent。JSON-RPC 2.0。必须有 `session/new` `session/prompt` `session/cancel` `session/update` [17][20] | 编辑器拉起子进程，stdin/stdout。Registry 只收有鉴权的 agent [21][36] | 消息必须 UTF-8。首页写远程可走 HTTP/WebSocket；传输页与此并列，见第 5 节 [16][18] |
| AG-UI | producer 发流，consumer 读。一次 run：提交 `RunAgentInput`。`type` 判别；EventType 有 31 个值。只有 run 生命周期强制 [25][31][37] | 版本在 `RunAgentInput.protocolVersion` 与 `RUN_STARTED.protocolVersion`。1.0 的传输绑定不做能力交换 [32][41] | 默认 POST + `text/event-stream`。HTTP 必须支持 SSE。一条 `data` 一个 JSON。无 `Last-Event-ID` [26][27] |

| | 鉴权 | 状态在哪 | 版本与治理 |
|---|---|---|---|
| MCP | 可选。HTTP 授权遵循 OAuth 2.1 草案 `draft-ietf-oauth-v2-1-13`，必须实现 RFC9728，头为 `Authorization: Bearer`。RFC7591 已弃用 [3][4b] | 无状态，对话在 host。已删 `Mcp-Session-Id`；跨调用用 server 签发的句柄当工具参数 [2][3] | `2026-07-28`。LF Projects；2025-12-09 入 AAIF（并列有 goose、AGENTS.md）[1][5][6] |
| A2A | `securitySchemes` 可选，类型为 OpenAPI 3.2 Security Scheme。带外取凭证。Agent Card 可 JWS。请求带 `A2A-Version`，空值当 `0.3` [8] | 待用户输入时称 interrupted state。枚举全名未入摘录 [8] | 站上 Latest `1.0.0`。Apache-2.0。TSC：Google、Microsoft、Cisco、AWS、Salesforce、ServiceNow、SAP、IBM。2026-08-27 起 AAIF Growth Stage [8][9][10][11] |
| ACP-IBM | 文档写 Basic、Bearer、JWT。OpenAPI 无 `securitySchemes` [14][43] | 状态在 Run [14] | OpenAPI 0.2.0。2025-08-27 归档。2025-03 IBM Research 发布。博客写停止独立开发、转入 A2A [12][14][15] |
| ACP-Zed | `authMethods` 在 `initialize` 响应中 [19] | 每个 session 自带 context 和历史 [33] | 稳定版 `1`。v2 自 2026-07-20 为 Draft。Apache-2.0。Zed+JetBrains，RFD。BDFL：Ben Brandt、Sergey Ignatov [22][23][39] |
| AG-UI | 不定义凭据。副作用工具要用户同意；流不能当可执行标记渲染 [25][26] | snapshot 必须整份替换；另有 RFC 6902 patch。状态跨 run 保留并随下次输入带回 [34] | 规范 1.0，页上无发布日。MIT。CopilotKit 与 LangChain、CrewAI 发起 [25][28] |

协议站点名（⚠，不是厂商文档）：AAIF 联合创立 Anthropic、Block、OpenAI，支持方含 Google、Microsoft。[6] A2A TSC 有 Google、Microsoft；已查页无 OpenAI、Anthropic。[11] 比较页把 MCP 归 Anthropic、A2A 归 Google。[35] Registry 原句：“ACP adapter for OpenAI's coding assistant”。[36] AG-UI：Microsoft Agent Framework、Google ADK = Supported；OpenAI Agent SDK = In Progress；Claude Agent SDK = Community。[24]

官方关系：A2A 首页写与 MCP “are not competitors — they are highly complementary”（MCP 到工具，A2A 到 agent）。[9] Zed 自比 LSP，并写复用 MCP 类型。[16][21] LF 博客 2025-08-29 写 ACP 并入 A2A；比较页仍列 Advantages of ACP。[12][35] AG-UI 写 A2UI 交付 UI widgets，自己是 Agent↔User 协议。[24]

## 3. 变体

| 名字 | 相对现行规范 |
|---|---|
| IBM ACP | A2A 的前身。REST 与 `RunStatus` 停在归档站；发现物是 YAML，不是 `/.well-known/agent-card.json` [8][14] |
| Zed ACP 中的 MCP | 只写明复用 MCP 的 JSON 类型 [21] |
| A2UI；goose；AGENTS.md | A2UI 被 AG-UI 称为生成式 UI 规范，其本站未入表。goose 与 AGENTS.md 是 AAIF 里和 MCP 并列的项目 [6][24] |

## 4. 坑

1. 缩写 ACP 先看域名。`agentcommunicationprotocol.dev` 已并入 A2A；`agentclientprotocol.com` 仍是编辑器协议。两边都不写对方。[13][16]
2. 「SSE 废弃」只指 MCP 的 HTTP+SSE 传输（自 `2025-03-26`）。Streamable HTTP 仍可用请求级 SSE。A2A 与 AG-UI 的事件流仍写 SSE。[4][8][27]
3. 新的智能体互操作以 A2A 规范为准，不以 IBM 优点页为准。Agent Card 路径用 `/.well-known/agent-card.json`，不用教程里的旧路径。[8][35]
4. Zed 的稳定本地接法是 stdin/stdout。AG-UI 跟规范的 31 个 EventType，不跟 README 的约 16 种。MCP 授权可选，但做 HTTP 授权就必须 RFC9728。许可以 LICENSE 的 Apache-2.0 迁移说明为准。[4b][21][28][37][40]

## 5. 未决与置信度

- vendors 五行都是 ⚠：没有四家厂商域名上的原句。
- 高影响、尚未回页复核，所以第 0 节不收口号：HTTP+SSE 传输 Deprecated；删除 `initialize` 与 `Mcp-Session-Id`。原句在第 2 节。
- ⚔ A2A 版本：规范站 1.0.0，GitHub latest 为 v1.0.1（2026-05-28）[8][42]。ACP-IBM 鉴权叙述对 OpenAPI。Zed 首页 HTTP/WebSocket 对 v1 传输页。AG-UI README 事件数对规范 31。
- 摘录没有、正文不写死：`TaskState` 全表、五种 security scheme 名、Zed 可选方法、`mcpServers`、AG-UI 八个事件家族名。
- ∅：MCP 未提 A2A/ACP/AG-UI；Zed 未提 IBM ACP/A2A；AG-UI 未提 ACP；A2A 已查页未提 AG-UI、Agent Client Protocol、OpenAI、Anthropic。无发布日：AG-UI 1.0、Zed v1、MCP 2026-07-28 博文。Roots/Sampling/Logging 无删除日。
- 见到但未入表：A2UI 本站、WebMCP、ANP、NLWeb、AP2、MCP Apps、Agent Skills、Activity Protocol、UTCP。

## 来源

[1] https://modelcontextprotocol.io/specification/latest
[2] https://modelcontextprotocol.io/specification/2026-07-28/architecture
[3] https://modelcontextprotocol.io/specification/2026-07-28/changelog
[3b] https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
[4] https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http
[4b] https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
[5] https://modelcontextprotocol.io/community/governance
[6] https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/blog/content/posts/2025-12-09-mcp-joins-agentic-ai-foundation.md
[7] https://modelcontextprotocol.io/specification/2026-07-28/server/discover
[8] https://a2a-protocol.org/latest/specification/
[9] https://a2a-protocol.org/latest/
[10] https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/
[11] https://raw.githubusercontent.com/a2aproject/A2A/main/GOVERNANCE.md
[12] https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
[13] https://agentcommunicationprotocol.dev
[14] https://agentcommunicationprotocol.dev/spec/openapi.yaml
[15] https://github.com/i-am-bee/acp
[16] https://agentclientprotocol.com
[17] https://agentclientprotocol.com/protocol/v1/overview
[18] https://agentclientprotocol.com/protocol/v1/transports
[19] https://agentclientprotocol.com/protocol/v1/authentication
[20] https://agentclientprotocol.com/protocol/v1/initialization
[21] https://agentclientprotocol.com/get-started/architecture
[22] https://github.com/agentclientprotocol/agent-client-protocol
[23] https://agentclientprotocol.com/announcements/acp-v2-draft
[24] https://docs.ag-ui.com/
[25] https://docs.ag-ui.com/spec/1.0
[26] https://docs.ag-ui.com/spec/1.0/basic/transports
[27] https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse
[28] https://github.com/ag-ui-protocol/ag-ui
[29] https://agentcommunicationprotocol.dev/core-concepts/agent-discovery.md
[31] https://docs.ag-ui.com/spec/1.0/events
[32] https://docs.ag-ui.com/spec/1.0/basic/versioning
[33] https://agentclientprotocol.com/protocol/v1/session-setup
[34] https://docs.ag-ui.com/spec/1.0/events/state
[35] https://agentcommunicationprotocol.dev/about/mcp-and-a2a.md
[36] https://agentclientprotocol.com/get-started/registry
[37] https://docs.ag-ui.com/spec/1.0/basic
[38] https://agentcommunicationprotocol.dev/core-concepts/architecture.md
[39] https://agentclientprotocol.com/community/governance
[40] https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/LICENSE
[41] https://docs.ag-ui.com/spec/1.0/basic/capabilities
[42] https://api.github.com/repos/a2aproject/A2A/releases/latest
[43] https://agentcommunicationprotocol.dev/core-concepts/production-grade.md
