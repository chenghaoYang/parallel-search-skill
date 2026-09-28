# Agent 协议对照：MCP、A2A、两种 ACP、AG-UI

> 这些名字各管哪条边界、怎么叠、不要记错哪句口号。版本以页面原文为准：MCP 规范 2026-07-28、A2A 规范页 Latest 1.0.0、Zed ACP wire `1`、AG-UI spec 1.0。厂商产品支持这轮不进正文。先读 §0–§1，原名在表里，打架和没引全的在 §5。

## 0. 一屏看懂

1. 先看两端是谁。MCP：Host 里的 Client 连一个 Server，换工具和上下文 [1][2]。A2A：Client 把任务交给不透明的 Remote Agent，不共享对方的 state、memory、tools [14][15]。Zed ACP：编辑器 Client 驱动 coding agent，agent 通常是子进程 [26]。AG-UI：producer 推事件流，consumer（界面）来读 [39][44]。
2. 两个 ACP 是两份规范。IBM/BeeAI 的全名是 Agent Communication Protocol，REST；仓库写「ACP is now part of A2A under the Linux Foundation!」，并于 2025-08-27 归档 [23][25]。Zed 与 JetBrains 的全名是 Agent Client Protocol，JSON-RPC，现行 wire 版本是整数 `1` [26][33]。同名不同边界，见 §1。
3. 「MCP 的 SSE 废了」只对旧传输成立一半。2026-07-28 的 Streamable HTTP 页写：2024-11-05 的 HTTP+SSE **传输**自 2025-03-26 起 deprecated [4]。同一修订里，POST 的响应仍可以是 JSON，或 request-scoped SSE [4]。2025-03-26 changelog 的原句是 “Replaced the previous HTTP+SSE transport with … Streamable HTTP” [6]。起点句还要反证，见 §5。
4. 2026-07-28 的 MCP changelog 写明去掉 `initialize` / `notifications/initialized` 握手；架构页写 MCP is a stateless protocol，每个请求自带版本和能力 [2][5]。`Mcp-Session-Id` 会话机制 “None of these mechanisms are part of this revision” [4]。
5. A2A 官网写 MCP 与 A2A complementary，不是替代：MCP 管 agent-to-tool，A2A 管 agent-to-agent [15]。AG-UI 写三者可以同时用 [40]。
6. 选型就按边界：接工具用 MCP；委托另一个 agent 用 A2A（IBM 仓库已指向 A2A [23]）；IDE 挂 coding agent 用 Zed ACP；界面渲染过程用 AG-UI。OpenAI、Anthropic、Google、微软的产品支持这轮是空格。

## 1. Taxonomy

分类轴是**连接边界**。差异（委托 vs 工具、编辑器子进程 vs REST agent、事件流 vs 任务）都落在这根轴上。IBM ACP 和 A2A 同属「agent ↔ agent」，所以页面会写并入；Zed ACP 属于「editor ↔ agent」，不会被这次并入消掉。

| 家族 | 两端 | 现行文档拿哪份 |
|---|---|---|
| F1 工具与上下文 | Host/Client ↔ Server | MCP |
| F2 任务委托 | Client ↔ Remote Agent | A2A。ACP-IBM 的仓库 banner 指向 A2A |
| F3 编辑器会话 | IDE Client ↔ agent 进程 | Agent Client Protocol（Zed） |
| F4 界面事件 | producer ↔ consumer | AG-UI |

维度：D1 谁和谁 · D2 对象原名 · D3 传输 · D4 状态在哪一端 · D5 怎么发现 · D6 鉴权 · D7 版本/弃用 · D8 谁治理 · D9 相邻协议怎么说。

## 2. 对照矩阵

### D1 边界 · D2 对象

| | D1 | D2（摘录里出现的原名） |
|---|---|---|
| MCP | Host 发起；Client 与一个 Server 1:1；Server 提供 context 与 capabilities [1][2] | JSON-RPC。Server：Prompts、Resources、Tools；Client 可提供 Elicitation [1]。方法：`tools/list`、`tools/call` [11]；`resources/read`、`prompts/get` [4]；`server/discover` [8] |
| A2A | A2A Client 代表 user 或另一系统；A2A Server 即 Remote Agent [14] | Agent Card、Task、Message、Part、Artifact [14]。方法名 PascalCase，例 `SendMessage`、`GetTask`；REST 例 `POST /message:send` [14] |
| ACP-IBM | client / server / agent；server 用 REST 暴露一个或多个 agent [20] | AgentManifest、Run、Message、MessagePart、Session、Event [19]。路径含 `/agents`、`POST /runs`、`/runs/{run_id}/cancel`、`/runs/{run_id}/events` [19] |
| ACP-Zed | Client 多是 code editor；Agent 改代码，通常为子进程 [26] | JSON-RPC 2.0。Agent 方法摘录：`initialize`、`authenticate`、`session/new`、`session/prompt`、`session/load`、`session/set_mode`、`logout`；通知 `session/cancel` [26] |
| AG-UI | producer 发事件，consumer 读；连接 user-facing app 与 agentic backend [39][44] | spec 1.0：31 个 `EventType`、8 族，含 `RUN_*`、`STEP_*`、`TEXT_MESSAGE_*`、`TOOL_CALL_*`、`REASONING_*`、`STATE_*`、`ACTIVITY_*`、`SUBAGENT_*`、`RAW`、`CUSTOM` [36]。上行是 `RunAgentInput` [45] |

Zed Client 侧摘录还有 `session/request_permission`、`fs/read_text_file`、`fs/write_text_file`、`terminal/create`、`terminal/output`、`terminal/kill`、`elicitation/create`，通知 `session/update` [26]。

### D3 传输 · D4 状态 · D5 发现

| | D3 | D4 | D5 |
|---|---|---|---|
| MCP | 传输页描述 stdio（子进程标准流、换行分隔）和 Streamable HTTP（每个消息一次 POST）[3]。响应可以是 JSON 或 request-scoped SSE [4]。旧 HTTP+SSE 传输的 deprecated 句见 §0 | 该修订写无状态；去掉 initialize 握手；`Mcp-Session-Id` 不属于本修订 [2][4][5] | 每请求带 client capabilities；`server/discover` MUST，返回版本、capabilities、身份 [8] |
| A2A | JSON-RPC 2.0 over HTTP；SSE（`text/event-stream`）用于 streaming [14]。绑定还写了 gRPC、HTTP/REST [14]。另有向 client webhook 的 HTTP POST [14] | 状态在 server 的 `Task.status`。终态 `COMPLETED`/`FAILED`/`CANCELED`/`REJECTED`；中断 `INPUT_REQUIRED`/`AUTH_REQUIRED` [14] | `https://{server_domain}/.well-known/agent-card.json` [14]。v0.3.0 起从 `agent.json` 改为此名 [17] |
| ACP-IBM | HTTP REST。`POST /runs` 的 200 可以是 `application/json` 或 `text/event-stream` [19] | `RunStatus`：`created`、`in-progress`、`awaiting`、`cancelling`、`cancelled`、`completed`、`failed`。`RunMode`：`sync`、`async`、`stream` [19] | Basic=`GET /agents`；Open=`/.well-known/agent.yml`；Registry 页写 “not yet part of the official ACP spec”；另有 Embedded [21] |
| ACP-Zed | v1 写出的传输是 stdio；Streamable HTTP 标 “draft proposal in progress” [27] | session 在 Agent 端：各自的 context、conversation history、state；`session/new` 后得到 `sessionId` [30] | `initialize` 交换 `protocolVersion` 与 capabilities；省略的能力视为 UNSUPPORTED [28]。ACP Registry 是精选集，只收支持 authentication 的 agent [34] |
| AG-UI | 说 HTTP 的实现 MUST 支持 HTTP+SSE（POST 输入，SSE 帧带 JSON）；Protobuf 绑定 OPTIONAL [37]。MAY 使用 WebSocket、message bus、进程内管道 [37] | producer 发 `STATE_SNAPSHOT`（整份替换）、`STATE_DELTA`（RFC 6902）、`MESSAGES_SNAPSHOT` [41] | 有 `AgentCapabilities` schema；本版没有传输级 capabilities 交换 [38]。`protocolVersion` 在 `RunAgentInput` 与 `RUN_STARTED` 上往返 [45] |

### D6 鉴权 · D7 版本 · D8 治理

| | D6 | D7 | D8 |
|---|---|---|---|
| MCP | 授权 OPTIONAL，针对 HTTP。OAuth 2.1 draft `draft-ietf-oauth-v2-1-13`；server 须提供 RFC9728 Protected Resource Metadata；401 的 `WWW-Authenticate` 带 `resource_metadata` 与 `scope`；client 须 RFC8707 [7] | 现行规范 2026-07-28 [1]。不支持的版本返回 `UnsupportedProtocolVersionError` [9]。弃用窗口摘录为最少 12 个月 [10] | 权威 schema 在规范仓库的 `schema.ts` [1]。法律实体是 LF Projects 的 Series [12]。Anthropic 将 MCP 捐给 Linux Foundation 下的 AAIF [13] |
| A2A | `securitySchemes` 恰好一种：`apiKeySecurityScheme`、`httpAuthSecurityScheme`、`oauth2SecurityScheme`、`openIdConnectSecurityScheme`、`mtlsSecurityScheme`。凭证每个请求放进 header 或 metadata [14] | 规范页 “Latest Released Version `1.0.0`” [14]。GitHub release：1.0.0（2026-03-12）[17]。请求带 `A2A-Version`，不支持则 `VersionNotSupportedError` [14]。规范源 `spec/a2a.proto` [14] | Google 原创并捐给 Linux Foundation。TSC：AWS、Cisco、Google、IBM Research、Microsoft、Salesforce、SAP、ServiceNow [15]。2026-08-27 起为 AAIF Growth Stage 项目，与 MCP、goose、AGENTS.md 并列 [16] |
| ACP-IBM | 页上写 Basic Auth、Bearer tokens、JWTs [22]。Identity Federation “under active development” [22] | OpenAPI `version: 0.2.0` [19]。仓库 tag 另有 `v1.0.0`（2025-07-01）、`v1.0.3`（2025-08-21）[23]。两套号的对应关系未见说明 | IBM Research 于 2025 年 3 月推出 [18]。文档写属于 Linux Foundation AI & Data [22]。仓库 `github.com/i-am-bee/acp`，2025-08-27 归档只读 [23] |
| ACP-Zed | `initialize` 响应里的 `authMethods`；Client 调 `authenticate`。默认类型 `agent`，另有 `terminal`。未认证请求可得到 `auth_required` [29] | 稳定协议版本 `1`（`protocolVersion` 为单个整数）[33]。Agent 不支持 Client 所提版本时回它自己的最新版本 [28]。v2 文档以 draft 发布 [35] | Zed 与 JetBrains 共同治理（interim）；lead 为 Ben Brandt、Sergey Ignatov [32]。仓库 `github.com/agentclientprotocol/agent-client-protocol`，Apache-2.0 [33] |
| AG-UI | 规范写：鉴权是 binding 和应用的事，“AG-UI defines no credential” [37] | 规范路径 `/spec/1.0/`。`@ag-ui/core` 的 `agui.protocolVersion` 为 `"1.0"`，包版本 `1.0.0` [43] | 仓库 `github.com/ag-ui-protocol/ag-ui`，MIT [42]。源于 CopilotKit 与 LangChain、CrewAI 的合作 [39]。一方 SDK：TypeScript、Python、.NET [44] |

### D9 关系

| | 官方怎么放自己 |
|---|---|
| MCP | spec 写灵感来自 LSP [1]。与 A2A 的互补句不在这份 MCP 摘录里 |
| A2A | “not competitors — they are highly complementary”；A2A 不是 tool-call 协议，不替代 MCP [15] |
| ACP-IBM | 2025-08-25 讨论帖：officially merging with the A2A，团队 winding down active development [24]。README banner：已是 A2A 的一部分 [23]。LF 文：BeeAI platform now uses A2A [18]。首页正文仍用现在时称 ACP 是开放协议 [25]，与 banner ⚔ |
| ACP-Zed | 自比 LSP [31]。尽量复用 MCP 的 JSON 表示，并为 diff 等 coding UX 另设类型 [31]。`session/new` 可带 `mcpServers`，让 Agent 去连 MCP [30] |
| AG-UI | “a single agent can and often does use all 3”；MCP 给 tools，A2A 连 agents，AG-UI 进 user-facing applications [40][42]。另有 handshakes，用来 front MCP 与 A2A 的 agent [40] |

TSC 名单里的公司名是治理席位 [15]，不是该产品已实现某协议。产品矩阵见 §5。

## 3. 变体与适配层

同一边界上，现行文本和旧教程不是同一份契约。

| 对照 | 差在哪 |
|---|---|
| MCP ≤ 握手时代 vs 2026-07-28 | changelog 写本修订删除 initialize 握手，请求改走 `_meta` 里的版本和 client capabilities [5]。更旧 lifecycle 页的原句这轮没引到 |
| HTTP+SSE 传输 vs 请求级 SSE | 被标 deprecated 的是 2024-11-05 那套 HTTP+SSE 传输 [4][6]。Streamable HTTP 仍可用 request-scoped SSE 当响应 [4] |
| ACP-IBM vs A2A | REST `Run` + `/.well-known/agent.yml` [19][21]，对 A2A 的 `Task` + `/.well-known/agent-card.json` [14]。IBM 仓库让读者去 A2A，不是两套并行标准 [23] |
| Zed ACP vs MCP | Zed 复用 MCP 的 JSON 形状，但是 editor↔agent 会话；MCP server 是 session 参数里再连出去的东西 [30][31] |
| AG-UI vs MCP/A2A | 事件流在界面这一侧；文档写可以 front 另两个协议，不是替换 [40] |

## 4. 用户需要知道的坑

1. 搜 “ACP” 会撞车。要看全名：Agent Communication Protocol（IBM，仓库已指向 A2A [23]）还是 Agent Client Protocol（编辑器，wire `1` [33]）。
2. 把 “SSE 废弃” 当成不能再出现 `text/event-stream`。废弃句针对的是旧 HTTP+SSE 传输 [4]；新传输的响应仍可以是请求级 SSE [4]。A2A、IBM ACP、AG-UI 各自的 SSE 是它们自己的流，不是 MCP 那次替换 [14][19][37]。
3. 用 `initialize` + `Mcp-Session-Id` 去接写着 2026-07-28 的 MCP server。该修订的 changelog 和传输页写这两套都不在本修订里 [4][5]。
4. A2A 发现地址还写 `/.well-known/agent.json`。release 写 v0.3.0 改成了 `agent-card.json` [17]。
5. A2A 方法写成 MCP 风格的 `message/send`。规范例是 PascalCase `SendMessage`，REST 是 `POST /message:send` [14]。
6. 把 IBM ACP 的 docs 正文当成仍在独立开发。正文是现在时 [25]，但 banner、讨论帖和归档日期写的是并入并停止独立开发 [23][24]。
7. 在 AG-UI 规范里找标准 Authorization 头。传输页写协议不定义 credential [37]。
8. 把 Zed 的远程 HTTP 当成 v1 已定义传输。v1 传输页写出的是 stdio；Streamable HTTP 仍是 draft [27]。
9. IBM 的 Registry 发现当成规范的一部分。发现页写还不是 official spec [21]。
10. 把 A2A TSC 里的 Microsoft、IBM、AWS 读成「产品已支持」。那一页只列委员会 [15]。

## 5. 未决与置信度

反证前不要把下面几句写成没有例外的历史结论：HTTP+SSE 自 2025-03-26 起一直保持 deprecated、之后没有再列入标准传输；不存在比 2026-07-28 更晚的 MCP 规范把 `initialize` 加回；没有任何官方页把两份 ACP 说成同一个，也没有页宣布 IBM ACP 恢复独立开发；AG-UI 没有另一页规定标准凭证。

quote 没盖住、所以正文没写死的主张：MCP header `Mcp-Method` / `Mcp-Name` / `Accept`；`tools` 以外未单独开页的方法全表；TaskState 里的 `SUBMITTED`/`WORKING`；GitHub tag `v1.0.1`；LF 新闻稿日期 April 29, 2025；Zed 介绍页的 HTTP/WebSocket 原句；AG-UI 旧文 “~16 event types”；`@ag-ui/core@1.0.0` 的发布时间；MCP 站内是否出现 A2A（只查了索引和站内搜索）。

厂商格全部 ❓：OpenAI、Anthropic、Google、Microsoft 的 V1–V4。A2UI、UTCP、ANP、MCP Apps 只在线索里，未升格。

ACP-IBM D7、D9 为 ⚔（版本号双轨；banner 与正文时态）。其余核心格是 ✅，但是 ✅ 只表示「有官方摘录」，不是「已反证过边界主张」。

## 来源

[1] MCP specification latest — https://modelcontextprotocol.io/specification/latest
[2] MCP architecture 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/architecture
[3] MCP transports 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
[4] MCP Streamable HTTP 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http
[5] MCP changelog 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/changelog
[6] MCP changelog 2025-03-26 — https://modelcontextprotocol.io/specification/2025-03-26/changelog
[7] MCP authorization 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
[8] MCP server/discover 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/server/discover
[9] MCP versioning 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning
[10] MCP deprecated registry 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/deprecated
[11] MCP tools 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/server/tools
[12] MCP governance — https://modelcontextprotocol.io/community/governance
[13] MCP joins AAIF — https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
[14] A2A specification — https://a2a-protocol.org/latest/specification/
[15] A2A home — https://a2a-protocol.org/latest/
[16] A2A joins AAIF — https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/
[17] A2A releases — https://github.com/a2aproject/A2A/releases
[18] ACP joins A2A (LF AI & Data) — https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
[19] ACP OpenAPI — https://raw.githubusercontent.com/i-am-bee/acp/main/docs/spec/openapi.yaml
[20] ACP architecture — https://agentcommunicationprotocol.dev/core-concepts/architecture.md
[21] ACP discovery — https://agentcommunicationprotocol.dev/core-concepts/agent-discovery.md
[22] ACP production — https://agentcommunicationprotocol.dev/core-concepts/production-grade.md
[23] ACP repo — https://github.com/i-am-bee/acp
[24] ACP merge discussion — https://github.com/orgs/i-am-bee/discussions/5
[25] ACP home — https://agentcommunicationprotocol.dev
[26] Zed ACP overview — https://agentclientprotocol.com/protocol/v1/overview.md
[27] Zed ACP transports — https://agentclientprotocol.com/protocol/v1/transports.md
[28] Zed ACP initialization — https://agentclientprotocol.com/protocol/v1/initialization.md
[29] Zed ACP authentication — https://agentclientprotocol.com/protocol/v1/authentication.md
[30] Zed ACP session setup — https://agentclientprotocol.com/protocol/v1/session-setup.md
[31] Zed ACP home — https://agentclientprotocol.com
[32] Zed ACP governance — https://agentclientprotocol.com/community/governance.md
[33] Zed ACP repo — https://github.com/agentclientprotocol/agent-client-protocol
[34] ACP Registry — https://agentclientprotocol.com/get-started/registry.md
[35] Zed ACP llms.txt — https://agentclientprotocol.com/llms.txt
[36] AG-UI spec events — https://docs.ag-ui.com/spec/1.0/basic/index.md
[37] AG-UI transports — https://docs.ag-ui.com/spec/1.0/basic/transports/index.md
[38] AG-UI capabilities — https://docs.ag-ui.com/spec/1.0/basic/capabilities.md
[39] AG-UI introduction — https://docs.ag-ui.com/introduction
[40] AG-UI and other protocols — https://docs.ag-ui.com/agentic-protocols.md
[41] AG-UI events concept — https://docs.ag-ui.com/concepts/events
[42] AG-UI repo — https://github.com/ag-ui-protocol/ag-ui
[43] @ag-ui/core — https://registry.npmjs.org/@ag-ui/core/latest
[44] AG-UI spec index — https://docs.ag-ui.com/spec/1.0/index.md
[45] AG-UI changelog — https://docs.ag-ui.com/spec/1.0/changelog.md
