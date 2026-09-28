# Agent 协议各管哪一段

> 四份规范多半不是竞品，而是四条边界。材料看到 2026-09-24。先读第 0 节，再用表核对官方名字。

## 0. 一屏看懂

1. 按谁和谁说话来分。MCP：宿主里的客户端对一个服务器 [1][2]。A2A：agent 委托远程 agent [14]。Zed ACP：编辑器对编码代理 [24]。AG-UI：界面消费 agent 的事件流 [35][36]。
2. 两个 ACP 不是同一份规范。IBM/BeeAI 全称 Agent Communication Protocol，REST，client 对 server [17][21]。Zed 全称 Agent Client Protocol，JSON-RPC，编辑器对 coding agent [24][27]。
3. IBM 这份不要当新项目的现行标准。2025-08-29 的 LF 帖写 officially merging with A2A，并 winding down active development [23]。仓库 2025-08-27 起 archived、read-only [19]。规范站首页仍写 community-driven governance [21]。
4. 「MCP 的 SSE 已废弃」只说对一半。被替换的是 2024-11-05 的双端点 HTTP+SSE [6]：2025-03-26 changelog 用 Replaced [7]；同版正文和 2026-07-28 changelog 写 deprecated since protocol version 2025-03-26 [8][4]。政策页写还没有任何特性被 Removed [9]。现行仍是单个接受 POST 的端点，响应可以是 scoped to that request 的 SSE [10]。stdio 仍在，服务器是子进程 [11]。
5. OpenAI、Anthropic、Google、微软支持谁、有没有自家变体：本轮没有厂商文档，这里不给结论。
6. 对话历史不在同一侧。MCP 把完整对话留在 host，且协议 stateless [2][3]。A2A 用 Task [14]。IBM ACP 用 session id [19]。Zed 的 session 自带历史 [25]。AG-UI 的 `threadId` 由应用铸造，同一 thread 上 `runId` 不复用 [37]。

## 1. Taxonomy

主轴是通信边界（能不能互相替代）。辅轴是交互时态：无状态调用、任务状态机、编辑器会话、事件流。缩写相同不是同一家族。

| 家族 | 谁和谁 | 现在看哪份 | 时态 |
|---|---|---|---|
| 模型上下文 | Host 发起；每个 client 只连一个 server [1][2] | MCP，路径版本 2026-07-28 | 无状态；长任务不在核心 [3][4] |
| 智能体互操作 | A2A Client 对 Remote Agent [14] | A2A。IBM ACP 是宣布并入的前规范 [23] | Task [14]，或 ACP 的 Run [18] |
| 编码代理客户端 | IDE/Client 对 coding agent [24] | Zed ACP 稳定版 1 [31]；v2 稳定前会改 [32] | Session [25] |
| 人机界面 | producer 发事件，consumer 读 [36] | AG-UI 1.0 [40] | 一个 thread 上多次 run [37] |

维度：D1 角色名；D2 官方对象和操作；D3 传输与弃用；D4 调用还是会话/任务；D5 发现；D6 鉴权；D7 维护者与版本；D8 四家厂商自己的文档；D9 它如何定位别的协议。

选型：模型要工具和数据，用 MCP。整段工作交给另一个 agent，用 A2A，不要新开 IBM ACP。编辑器驱动编码代理，用 Zed ACP，且不要和 MCP 共用一条 socket [34]。前端按流渲染，用 AG-UI。

## 2. 对照矩阵

| | 角色与状态 | 原语、传输、发现 | 鉴权、治理、层位 |
|---|---|---|---|
| MCP | Hosts 是发起连接的 LLM 应用 [1]。每个 client 只连一个 server [2]。协议 stateless [3]。删除协议级 session 与 `Mcp-Session-Id` [4]。 | Tools：给模型执行的函数 [5]。客户端特性含 elicitation、sampling、roots [3]。2026-07-28 弃用 Roots、Sampling、Logging；Tasks 移出核心，扩展 id `io.modelcontextprotocol/tasks` [4]。双端点 HTTP+SSE 已被替换 [6][7][8][4]，尚未 Removed [9]。现行：单个 POST 端点，响应可为本次请求的 SSE [10]；stdio 为子进程 [11]。servers MUST implement this RPC [4]（方法名不在摘录内）。 | 鉴权 OPTIONAL；Bearer；stdio 从环境读凭证 [12]。OAuth 2.1 自 2025-03-26 [7]。弃用 RFC7591 [4]。治理页是 LF Projects, LLC，该页无 Anthropic [13]。类比是 LSP [1]。A2A/ACP/AG-UI 只在笔记已开的几页里未见。 |
| A2A | A2A Client 请求 A2A Server（Remote Agent）[14]。终态 `TASK_STATE_COMPLETED` / `FAILED` / `CANCELED` / `REJECTED`；中断态 `INPUT_REQUIRED` / `AUTH_REQUIRED` [14]。 | 规范源 `spec/a2a.proto`。Send Message 可新建 Task 或直接返回 Message [14]。绑定 `JSONRPC`、`GRPC`、`HTTP+JSON`；JSON-RPC 2.0 over HTTP(S)，流式用 SSE [14]。gRPC/REST 写入 0.2.2（2025-06-09）[15]。发现 `https://{server_domain}/.well-known/agent-card.json`；0.3.0（2025-07-30）从 `agent.json` 改来 [14][15]。 | 方案只能是 apiKey、httpAuth、oauth2、openIdConnect、mtls 之一；每请求 MUST `A2A-Version` [14]。页眉 1.0.0 [14]；1.0.0 日期 2026-03-12 [15]。Google 捐给 LF；TSC 含 AWS、Cisco、Google、IBM Research、Microsoft、Salesforce、SAP、ServiceNow [16]。与 MCP complementary [14]。正文未写 ACP 合并。 |
| ACP-IBM | client 对 REST server [17]。RunStatus：`created`、`in-progress`、`awaiting`、`cancelling`、`cancelled`、`completed`、`failed` [18]。session id 跨轮保存 [19]。 | 创建 run 必填 `agent_name`、`input`，可选 `session_id`、`mode`（`sync`/`async`/`stream`）[20]。OpenAPI 0.2.0 [18]。HTTP 惯例，并以 JSON-RPC 为对照 [21]。发现示例 `/.well-known/agent.yml` [22]。 | 2025-08-29 merging、winding down；BeeAI 已改用 A2A [23]。仓库 2025-08-27 归档只读 [19]。首页仍写社区治理 [21]。 |
| ACP-Zed | 编辑器/IDE 与 coding agent [24]。session 自带历史和状态 [25]。v1 stopReason：`end_turn`、`max_tokens`、`max_turn_requests`、`refusal`、`cancelled` [26]。 | JSON-RPC 2.0 [27]。v1 MUST `session/new`、`session/prompt`、`session/cancel`、`session/update` [28]。SHOULD stdio [29]。引言写 HTTP 或 WebSocket [24]。Streamable HTTP 为 draft [29]。v2 删除客户端文件系统、终端、session modes，远程不在 core [26]。Registry：`cdn.agentclientprotocol.com/registry/v1/latest/registry.json` [30]。 | 稳定版 1 [31]。v2 稳定前会改 [32]。`session/request_permission` 向用户要工具授权 [27]。Lead：Ben Brandt（Zed）、Sergey Ignatov（JetBrains）[33]。不要和 MCP 同 socket [34]。Unlike MCP，`{}` 不算 form [28]。 |
| AG-UI | 全称 The Agent–User Interaction (AG-UI) Protocol；面向用户的应用 ↔ agent 后端 [35]。producer 发流，consumer 读 [36]。`threadId` 跨 run 稳定；`runId` 不复用 [37]。 | `EventType` 31 个值；摘录中有 `RUN_STARTED`、`RUN_FINISHED`、`RUN_ERROR`、`STEP_STARTED`、`STEP_FINISHED`、`ACTIVITY_SNAPSHOT`、`ACTIVITY_DELTA` [37]。讲 HTTP 者 MUST SSE；protobuf OPTIONAL [38]。本版无 capabilities 交换 [39]。 | 不定义 credential [38]。`MAJOR.MINOR`，页为 1.0；字段 `RunAgentInput.protocolVersion` [40]。与 TS/Python/.NET SDK 同维护 [36]。把 agent 连到用户；摘录写一个 agent 可用全部三个，三个名字不在同一句 [41]。A2UI 被写成生成式 UI 规范 [35]；另页写 AG-UI 不是 [42]。 |

D8 五行都是 ❓。

## 3. 变体与适配层

| 对照 | 差在哪 |
|---|---|
| IBM ACP 相对 A2A | 发现示例是 `agent.yml` [22]，不是 `agent-card.json` [14]。状态是小写 RunStatus [18]，不是 `TASK_STATE_*` [14]。传输是 HTTP [21]，不是三种绑定 [14]。公告已指向并入 [23][19]。 |
| Zed v2 相对稳定版 1 | 删掉文件系统、终端、session modes；远程不在 core [26]；稳定前会改 [32]。现用稳定版 1 [31]。 |
| A2UI 相对 AG-UI | AG-UI 文档把 A2UI 标成生成式 UI，并写明自己不是 [35][42]。A2UI 自己的站未入正文。 |

## 4. 用户需要知道的坑

1. 域名 `agentcommunicationprotocol.dev` 仍在讲 REST [21]，仓库已只读 [19]。新的 agent 互操作看 A2A [23]。
2. 关掉 MCP 的一切 SSE，会拒绝现行的按请求 SSE [10]。要分开看的是双端点旧传输 [6][7]，它还没被 Removed [9]。
3. A2A 发现用 `agent-card.json` [14]。`agent.json` 是 0.3.0 之前的路径 [15]。
4. AG-UI 概念页仍写约 16 种事件，并写 SSE、webhooks、WebSockets 且 doesn't mandate [43]。规范是 31 个 `EventType`，讲 HTTP 则 MUST SSE [37][38]。
5. Zed 的远程 HTTP/WebSocket 不是稳定核心 [24][29][26]。Registry 里的产品名不是厂商承诺 [30]。
6. MCP 鉴权可以不做；HTTP 与 stdio 拿凭证的方式不同 [12]。动态客户端注册已标弃用 [4]。

## 5. 未决与置信度

- D8 全空。TSC 名单不是产品支持 [16]。笔记 r1-a2a C19 未入正文。
- SSE 还没做反证轮。Replaced 与 deprecated 用词并存 [7][8][4]。GET stream 的删除只有笔记线索，无摘录。
- 无摘录就不写死：MCP 的 Resources、Prompts、是否仍是 JSON-RPC、发现 RPC 的方法名；A2A 的 SUBMITTED / WORKING；笔记冲突段里的 1.0.1。
- IBM 首页与「已并入」冲突 [21][19][23]。鉴权、发现是否入规范、迁移指南，见笔记冲突段，正文不另引。
- Zed：与 IBM 全称的否定，摘录句本身不是否定句。共同治理 [33] 对 RFD 页的 BDFL。v2 的 draft [32] 对 migration 页里的 stable baseline 字样。
- AG-UI：31 与约 16 未裁决 [37][43]。多数事件名不在 quote 里。无法人。治理页无 Anthropic [13]。捐赠叙述不在该页。
- 线索未入正文：第三个 ACP、A2UI 站点、WebMCP、ANP、MCP Apps。下轮只核会改第 0 节的。

## 来源

[1] https://modelcontextprotocol.io/specification/2026-07-28
[2] https://modelcontextprotocol.io/specification/2026-07-28/architecture
[3] https://modelcontextprotocol.io/specification/2026-07-28/basic/index
[4] https://modelcontextprotocol.io/specification/2026-07-28/changelog
[5] https://modelcontextprotocol.io/specification/2026-07-28/server
[6] https://modelcontextprotocol.io/specification/2024-11-05/basic/transports
[7] https://modelcontextprotocol.io/specification/2025-03-26/changelog
[8] https://modelcontextprotocol.io/specification/2025-03-26/basic/transports
[9] https://modelcontextprotocol.io/specification/2026-07-28/deprecated
[10] https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http
[11] https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio
[12] https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
[13] https://modelcontextprotocol.io/community/governance
[14] https://a2a-protocol.org/latest/specification/
[15] https://raw.githubusercontent.com/a2aproject/A2A/main/CHANGELOG.md
[16] https://a2a-protocol.org/latest/
[17] https://agentcommunicationprotocol.dev/core-concepts/architecture
[18] https://raw.githubusercontent.com/i-am-bee/acp/main/docs/spec/openapi.yaml
[19] https://github.com/i-am-bee/acp/blob/main/README.md
[20] https://agentcommunicationprotocol.dev/core-concepts/agent-run-lifecycle
[21] https://agentcommunicationprotocol.dev
[22] https://agentcommunicationprotocol.dev/core-concepts/agent-discovery
[23] https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
[24] https://agentclientprotocol.com/get-started/introduction.md
[25] https://agentclientprotocol.com/protocol/v1/session-setup.md
[26] https://agentclientprotocol.com/protocol/v2/migration.md
[27] https://agentclientprotocol.com/protocol/v1/overview.md
[28] https://agentclientprotocol.com/protocol/v1/initialization.md
[29] https://agentclientprotocol.com/protocol/v1/transports.md
[30] https://agentclientprotocol.com/get-started/registry.md
[31] https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/README.md
[32] https://agentclientprotocol.com/announcements/acp-v2-draft.md
[33] https://agentclientprotocol.com/community/governance.md
[34] https://agentclientprotocol.com/get-started/architecture.md
[35] https://docs.ag-ui.com/introduction.md
[36] https://docs.ag-ui.com/spec/1.0.md
[37] https://docs.ag-ui.com/spec/1.0/basic/index.md
[38] https://docs.ag-ui.com/spec/1.0/basic/transports/index.md
[39] https://docs.ag-ui.com/spec/1.0/basic/capabilities.md
[40] https://docs.ag-ui.com/spec/1.0/basic/versioning.md
[41] https://docs.ag-ui.com/agentic-protocols.md
[42] https://docs.ag-ui.com/concepts/generative-ui-specs.md
[43] https://docs.ag-ui.com/concepts/architecture.md
