# Agent 协议地图：MCP、A2A、两种 ACP、AG-UI

> 各协议管哪一条边、能否互换；鉴权、版本、治理如何选。官方页截至 2026-09-24。厂商支持本轮不写。

## 0. 一屏看懂

1. 四条边，不能替代。MCP：Host 里的 Client 对一个 Server。A2A：Client 对 Remote Agent。Zed ACP：编辑器对 coding agent。AG-UI：producer 把一轮运行收成事件给 consumer。[1][13][17][27][36]
2. 两个 ACP 不是一回事。IBM 的 Agent Communication Protocol 是 REST。Zed 的 Agent Client Protocol 是 JSON-RPC。两边官方页都没把对方写成自己。[17][27]
3. IBM ACP 不要新接。欢迎页写已并入 Linux Foundation 下的 A2A；2025-08-25 停更；仓库 2025-08-27 归档。对比页仍把它们写成两个标准。[17][20][21][22]
4. MCP 的 HTTP+SSE 自规范 `2025-03-26` 起 deprecated，由该版传输页替换；2026-07-28 的现行 HTTP 叫 Streamable HTTP（POST 到单一 endpoint，带 `MCP-Protocol-Version`）。特征仍留在规范里。移除日三说并存，见第 5 节。[3][4][5][6]
5. 状态各放一边：MCP 的对话在 Host；A2A 的 Task 在 Server；Zed 的 session 自带 history；AG-UI 把 state 放进下一轮输入。[2][13][34][41]
6. 版本：MCP `2026-07-28`（无握手）[8][11]；A2A `1.0.0` [13]；IBM OpenAPI `0.2.0` [23]；Zed 稳定版 `1`，v2 概览已改方法名 [32][35]；AG-UI `"1.0"`（2026-09-17 冻结）[39]。
7. 治理：MCP 是 AAIF（Linux Foundation）创始项目，与 goose、AGENTS.md 并列 [10]。A2A 的 TSC 含 Google、IBM Research、Microsoft 等；博文称 AAIF Growth Stage [14][15]。Zed ACP 由 Zed 与 JetBrains 共治 [33]。AG-UI 无标准组织，CODEOWNERS 为 `@ag-ui-protocol/copilotkit` [43]。
8. 四家厂商的支持和自家变体：还是缺口，不写结论。

## 1. Taxonomy

分类轴是通信边：同一条边才替代，不同边只叠放。第二轴是状态在哪一端。ACP 这个缩写不能当轴。

| 家族 | 边 | 成员 |
|---|---|---|
| F1 工具与上下文 | Host 内 Client ↔ 一个 Server | MCP。对象是 `Resources`、`Prompts`、`Tools`，对话不在 Server [1][2] |
| F2 智能体任务 | Client ↔ Remote Agent | A2A。不碰对方 memory 与 tools [13]。IBM ACP 是 REST `/runs` 的归档前身 [18] |
| F3 编码会话 | 编辑器 ↔ coding agent | Zed ACP。`initialize` 之后 `session/prompt` [28] |
| F4 界面事件 | producer ↔ consumer | AG-UI。一次请求进，一条事件流出 [36] |

怎么选：工具和数据用 MCP；交给别的智能体用 A2A 1.0；IDE 用 Zed ACP v1，工具仍走会话里的 MCP [34]；网页用 AG-UI，它可 front for MCP 与 A2A [40]。

维度见第 2 节各表：edge、objects、wire、discovery、auth、version、gov、state、compose。

## 2. 对照矩阵

| | edge 与 objects | state |
|---|---|---|
| MCP | Hosts / Clients / Servers；Client 只连一个 Server。`Resources`、`Prompts`、`Tools` [1][2] | 无状态，对话在 Host [2] |
| A2A | Client → A2A Server (Remote Agent)。`Task`（id 由 server 生成）；`ROLE_USER`；Part：`text`/`raw`/`url`/`data` [13] | GetTask 读 server。终态 `TASK_STATE_COMPLETED`/`FAILED`/`CANCELED`/`REJECTED`；中断 `TASK_STATE_INPUT_REQUIRED`/`TASK_STATE_AUTH_REQUIRED` [13] |
| ACP-IBM | 连接 agents、applications、humans。工作单元是 run（`run_id`）和 Session [17][18][25] | Session 跨交互保存 history 与 state [25] |
| ACP-Zed | Agents 与 Clients。方法 `initialize`、`authenticate`、`session/new`、`session/prompt` [28] | session 自带 context、history、state [34] |
| AG-UI | producer 发流，consumer 读；反向只有 `RunAgentInput` [36][45] | 下一轮 input 带回当前 state [41] |

AG-UI 事件（`EventType` 共 31 个）：`TEXT_MESSAGE_START`/`CONTENT`/`END`/`CHUNK`；`TOOL_CALL_START`/`ARGS`/`END`/`CHUNK`/`RESULT`；`STATE_SNAPSHOT`/`STATE_DELTA`/`MESSAGES_SNAPSHOT`。[37]

| | wire | discovery |
|---|---|---|
| MCP | JSON-RPC 2.0。stdio：子进程上换行分隔。Streamable HTTP：POST 单一 endpoint，回复 JSON 或该请求的 SSE；头 `MCP-Protocol-Version` [1][3][4] | `server/discover`，Servers MUST 实现 [9] |
| A2A | `JSONRPC`、`GRPC`、`HTTP+JSON`。JSON-RPC 流式是 SSE `text/event-stream`。gRPC 服务 `A2AService` [13] | `/.well-known/agent-card.json`；`supportedInterfaces` 第一项 preferred [13] |
| ACP-IBM | 普通 HTTP，对照 JSON-RPC。`POST /runs` 必填 `agent_name`、`input`，可选 `session_id`、`mode`（`sync`/`async`/`stream`），再 `GET /runs/{run_id}` [17][18] | `GET /agents`；`/.well-known/agent.yml`。注册表还不是 spec [19] |
| ACP-Zed | JSON-RPC 2.0 over stdio（stdin/stdout）。Streamable HTTP 仍是 draft proposal [27][29] | `https://cdn.agentclientprotocol.com/registry/v1/latest/registry.json` [30] |
| AG-UI | HTTP 实现 MUST SSE；Protobuf OPTIONAL。MAY：WebSockets、message buses、in-process pipes [38] | ∅。无 capabilities exchange [42] |

| | auth | version | gov |
|---|---|---|---|
| MCP | OPTIONAL，同页又 MUST 实现 RFC9728 [7] | `2026-07-28`；无握手 [8][11] | AAIF 创始项目 [10] |
| A2A | 五选一：`apiKeySecurityScheme`、`httpAuthSecurityScheme`、`oauth2SecurityScheme`、`openIdConnectSecurityScheme`、`mtlsSecurityScheme` [13] | `1.0.0` [13] | TSC [14]；AAIF Growth Stage [15] |
| ACP-IBM | 生产页：Basic、Bearer、JWT。创建 run：`security: []` [24][26] | OpenAPI `0.2.0` [23] | 宣布并入 A2A；仓库归档 [17][21] |
| ACP-Zed | `authMethods`，再 `authenticate`。未见 OAuth 原名 [31] | 稳定版 `1`；v2 为 `auth/login`、`auth/logout` [32][35] | Zed 与 JetBrains [33] |
| AG-UI | ∅，defines no credential [38] | `"1.0"` [39] | 无标准组织；`@ag-ui-protocol/copilotkit` [36][43] |

| | compose |
|---|---|
| MCP | 受 Language Server Protocol 启发。规范无 A2A/ACP/AG-UI 对照句 [1] |
| A2A | 不替代 MCP：MCP 是 agent-to-tool，A2A 是 agent-to-agent [14] |
| ACP-IBM | agent 之间的通信；欢迎页宣布成为 A2A 的一部分 [17][22] |
| ACP-Zed | MCP 负责外部 tools 与 data；server 随会话交给 agent [34] |
| AG-UI | MCP 接工具，A2A 接 agent，AG-UI 接用户，并可 front for 前两者 [40] |

## 3. 变体与适配层

厂商变体未核验。规范写明的叠放：

| 适配 | 和参照的差 |
|---|---|
| IBM ACP → A2A | 同边的前身：`/runs` + Session，不是 `Task` / `TASK_STATE_*` / agent card。A2A 1.0 摘录无 “incorporated ACP” |
| Zed 携带 MCP | 会话不替代 MCP [34] |
| AG-UI 在前 | 只加事件，不改 MCP/A2A 载荷 [40] |

## 4. 用户需要知道的坑

1. ACP 撞车：`/runs` 是 Agent Communication Protocol；stdio 是 Agent Client Protocol。互操作跟 A2A，IDE 跟 Zed v1。[17][27]
2. MCP 双通道 SSE 已不是现行传输。用 Streamable HTTP，并带 `MCP-Protocol-Version`。页上还留着 deprecated 条目，不等于推荐。[4][6]
3. A2A 有三种绑定，不要只做 JSON-RPC。概念页仍写全部载荷都是 JSON-RPC 2.0。[13][16]
4. AG-UI 以 1.0 的 31 个事件和 HTTP MUST SSE 为准。概念页写 16 个事件，并写 doesn't mandate。[37][38][44]
5. Zed 稳定方法是 `authenticate`。v2 概览改成 `auth/login`。远程 HTTP 仍是草案。[29][32][35]
6. IBM 不要单页抄路径和鉴权：`run/{run_id}/cancel` 对 OpenAPI `/runs/{run_id}/cancel`；JWT 对 `security: []`。仓库只读。[18][23][24][26]

## 5. 未决与置信度

四家厂商，以及 Agentic Commerce Protocol、Activity Protocol、AP2、UCP，都还是 ❓。

- SSE 何时删除：SEP-2596 Final 后三个月 [6]；至少十二个月且不从 Final 起算 [12]；博客写 year-long offramp [11]。SEP-2596 是否已 Final，未知。
- MCP 的 OPTIONAL 与 MUST RFC9728 缺限定从句 [7]。A2A 概念页与三种绑定冲突 [16]。`implicit` / `password` 仍列在规范里 [13]。
- IBM 是否等于 A2A：欢迎页和归档，对对比页 “both aim to create a standard”。该页写 Google 于 2025-04 推出 A2A；A2A 规范摘录无同句，也无 “incorporated”。[17][20][22]
- 已查过而官方没写：AG-UI 无凭证、无发现、无章程；两份 ACP 文档互不点名。
- 页面时间：MCP `2026-07-28`，A2A 博文 2026-08-27，AG-UI 冻结 2026-09-17。

## 来源

[1] https://modelcontextprotocol.io/specification/latest
[2] https://modelcontextprotocol.io/specification/2026-07-28/architecture
[3] https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
[4] https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http
[5] https://modelcontextprotocol.io/specification/2025-03-26/basic/transports
[6] https://modelcontextprotocol.io/specification/2026-07-28/deprecated
[7] https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
[8] https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning
[9] https://modelcontextprotocol.io/specification/2026-07-28/server/discover
[10] https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
[11] https://blog.modelcontextprotocol.io/posts/2026-07-28/
[12] https://modelcontextprotocol.io/community/feature-lifecycle
[13] https://a2a-protocol.org/latest/specification/
[14] https://a2a-protocol.org/latest/
[15] https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/
[16] https://a2a-protocol.org/latest/topics/key-concepts/
[17] https://agentcommunicationprotocol.dev/introduction/welcome.md
[18] https://agentcommunicationprotocol.dev/core-concepts/agent-run-lifecycle.md
[19] https://agentcommunicationprotocol.dev/core-concepts/agent-discovery.md
[20] https://github.com/orgs/i-am-bee/discussions/5
[21] https://github.com/i-am-bee/acp
[22] https://agentcommunicationprotocol.dev/about/mcp-and-a2a.md
[23] https://agentcommunicationprotocol.dev/spec/openapi.yaml
[24] https://agentcommunicationprotocol.dev/core-concepts/production-grade.md
[25] https://agentcommunicationprotocol.dev/core-concepts/stateful-agents.md
[26] https://agentcommunicationprotocol.dev/spec/run-create.md
[27] https://agentclientprotocol.com/get-started/introduction.md
[28] https://agentclientprotocol.com/protocol/v1/overview.md
[29] https://agentclientprotocol.com/protocol/v1/transports.md
[30] https://agentclientprotocol.com/get-started/registry.md
[31] https://agentclientprotocol.com/protocol/v1/authentication.md
[32] https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/README.md
[33] https://agentclientprotocol.com/community/governance.md
[34] https://agentclientprotocol.com/protocol/v1/session-setup.md
[35] https://agentclientprotocol.com/protocol/v2/overview.md
[36] https://docs.ag-ui.com/spec/1.0.md
[37] https://docs.ag-ui.com/spec/1.0/basic/index.md
[38] https://docs.ag-ui.com/spec/1.0/basic/transports/index.md
[39] https://github.com/ag-ui-protocol/ag-ui/releases
[40] https://docs.ag-ui.com/agentic-protocols.md
[41] https://docs.ag-ui.com/spec/1.0/events/state.md
[42] https://docs.ag-ui.com/spec/1.0/basic/capabilities.md
[43] https://raw.githubusercontent.com/ag-ui-protocol/ag-ui/main/.github/CODEOWNERS
[44] https://docs.ag-ui.com/concepts/architecture.md
[45] https://docs.ag-ui.com/spec/1.0/basic/run-input.md
