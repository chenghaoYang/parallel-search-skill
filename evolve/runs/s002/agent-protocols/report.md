# Agent 协议：各管一条接缝

> 回答 MCP、A2A、两份 ACP、AG-UI 各连接谁，以及鉴权、版本、治理、怎么选。截至 2026-09-24 的官方页。先读第 0 节再查表。四大厂整表仍空着。

## 0. 一屏看懂

- 四条接缝可以叠用：MCP 是 Host 里的 Client 对一个工具 Server（1:1）；A2A 是 Client 对不透明的远端 agent；Zed ACP 是编辑器对 coding agent；AG-UI 是 producer 把事件流交给 consumer（UI / SDK）。[1][10][11][20][28]
- ACP 有两份规范。IBM 全名 Agent Communication Protocol：REST，对象是 Run，`info.version` 0.2.0。Zed 全名 Agent Client Protocol：JSON-RPC，对象是 `session/prompt`，稳定主版本 1。[14][20][25]
- IBM 那份已宣布并入 A2A：2025-08-29 LF 写明停止独立开发，仓库 2025-08-27 归档。对比页仍列「相对 A2A 的优点」，和公告矛盾。BeeAI 平台改为跑 A2A。新接 agent 互操作用 A2A 的 Task，不要新接 `/runs`。[13][15][16][17]
- HTTP+SSE 这个传输名自协议版本 2025-03-26 起被 Streamable HTTP 换下，2026-07-28 登记为 Deprecated；移除条件是 SEP-2596 到 Final 后再过三个月。现行响应仍可以是 `text/event-stream`，客户端对 JSON 和 SSE 都必须支持。独立 GET SSE 与 `Last-Event-ID` 续传已去掉。Removed 名单当时为空。[3][4][5][6]
- 现行 MCP 是 **2026-07-28**（上一版 2025-11-25），无状态：删协议级 session、`Mcp-Session-Id`、`initialize`。同版 Deprecated 还有 Roots、Sampling、Logging 和 RFC7591 动态注册。弃用窗至少 12 个月。[1][4][6]
- 选型按接缝：工具用 MCP；agent 委托用 A2A；IDE 用 Zed ACP（v2 草案公告日 2026-07-20）；UI 事件用 AG-UI 1.0。AG-UI 写三者可同时使用。MCP 与 A2A 都在 Agentic AI Foundation（MCP 2025-12-09 捐入，A2A 2026-08-27 为 Growth Stage），项目仍各自自治。Zed ACP 由 Zed 与 JetBrains 共治（RFD，Apache-2.0）。AG-UI 组织是 `ag-ui-protocol`，一方 SDK 为 TypeScript、Python、.NET。MCP 改规范走 SEP，决策人是 BDFL。[8][9][12][24][26][28][30]

## 1. Taxonomy

主轴是对话两端。辅轴是工作单元。

| 家族 | 两端 | 工作单元 | 现在看 |
|---|---|---|---|
| 上下文与工具 | Client ↔ Server | 一次 JSON-RPC | MCP 2026-07-28 |
| Agent 互操作 | Client ↔ Remote Agent | Task | A2A。IBM ACP 是同层前身 |
| 编程客户端 | 编辑器 ↔ agent 子进程 | `session/prompt` | Agent Client Protocol v1 |
| 人机界面 | producer ↔ consumer | `RunAgentInput` → 事件流 | AG-UI 1.0 |

列：D2 对象原名，D3 传输，D4 发现，D5 鉴权，D6 版本，D8 状态在哪。D1/D7/D9 已收进第 0、3 节。

## 2. 对照矩阵

| | D2 / D8 | D3 | D4 / D5 / D6 |
|---|---|---|---|
| MCP | JSON-RPC 2.0。Server：Resources、Prompts、Tools。Client 可提供 Elicitation。Server 不发起 request；要输入用 `InputRequiredResult`。能力在每次请求的 `_meta.io.modelcontextprotocol/clientCapabilities`。跨调用用 server 铸造的 handle | 标准传输：`stdio`、Streamable HTTP（单 POST；响应 `application/json` 或 `text/event-stream`）。HTTP+SSE 传输 Deprecated | `server/discover` 报版本、能力、身份。HTTP 鉴权可选，走 OAuth 2.1（server=resource server）；MUST RFC9728；注册优先 Client ID Metadata Documents。stdio 用环境凭据，不走这套授权。token 禁止放 query；MUST RFC8707 `resource`。版本是日期 |
| A2A | `AgentCard`、`Task`、`Message`、`Part`（恰有一个 `text`/`raw`/`url`/`data`）、`Artifact`。规范源 `spec/a2a.proto`。状态在 `Task.status`，产物在 `artifacts`，多轮在 `history` | JSON-RPC 2.0 over HTTP(S)，流为 SSE。同页主张还有 gRPC 与 HTTP+JSON。媒体类型 `application/a2a+json`，头前缀 `a2a-`。`POST /message:send`、`GET /tasks/{id}` | `/.well-known/agent-card.json`（或注册表、或直配）。`supportedInterfaces` 第一项为首选。`SecurityScheme` 五选一：`apiKey`、`httpAuth`、`oauth2`、`openIdConnect`、`mtls`（字段名带 SecurityScheme 后缀）。规范站版本 **1.0.0** |
| ACP-IBM | `AgentManifest`、`Run`、`Message`、`Session`。`RunMode`：`sync`/`async`/`stream`。`POST /runs` 的 200 可为 `text/event-stream`，异步 202 | HTTP+JSON + SSE。示例 server `http://localhost:8000` | `GET /agents`；开放发现 `/.well-known/agent.yml`。生产建议 Basic、Bearer、JWT。规范版本 **0.2.0** |
| ACP-Zed | 基线：`initialize`、`authenticate`、`session/new`、`session/prompt`、`session/request_permission`。取消：`session/cancel`。路径绝对，行号 1-based。省略的能力 = UNSUPPORTED | stdio：换行分隔，stdout 只写 ACP。Streamable HTTP 仍是草案 | `protocolVersion` 是一个整数。`authMethods` 在 initialize 结果里。能力位含 `mcpCapabilities.http` / `sse` |
| AG-UI | 必填 `threadId`、`runId`、`messages`。信封：`type`、`timestamp`、`rawEvent`、`metadata`。强制只有 run 生命周期。`RUN_FINISHED.outcome`：`success`/`interrupt`/`cancelled`。state/messages 每个 run 经 consumer 送回 | HTTP 实现 MUST 用 HTTP+SSE（POST JSON，响应 `text/event-stream`）。Protobuf 可选。WebSocket 只算自定义传输 | 版本在 `RunAgentInput.protocolVersion` 与 `RUN_STARTED.protocolVersion`。有 `AgentCapabilities` 形状，这一版没有能力交换 binding。协议不定义凭证。schema **1.0** |

[1][2][3][6][7][10][11][14][18][19][21][22][23][28][29][31][32][33][34]

## 3. 变体与适配层

| | 发现文件 | 对象 | 线格式 | 状态 |
|---|---|---|---|---|
| A2A | `agent-card.json` | Task | JSON-RPC / gRPC / HTTP+JSON | 规范站 1.0.0，AAIF |
| ACP-IBM | `agent.yml` | Run | REST + SSE | 仓库只读，已宣布并入 |

[10][13][15][18]

Zed ACP 把 MCP 放在下一层：编辑器把 MCP server 配置随 prompt 交给 agent，agent 自己去连；协议复用 MCP 的 JSON 类型。[23][27]

AG-UI 分层页写 MCP 接工具，A2A 接 agent，AG-UI 接用户应用，并有代理 MCP/A2A 的 handshake。有副作用的 tool call 要经用户同意；模型输出当不可信输入。[28][30]

OpenAI 把 MCP Apps 写成 MCP server 的可选 UI resource（`@modelcontextprotocol/ext-apps`），不是另一份顶层协议。[35]

## 4. 用户需要知道的坑

1. 搜「ACP」对全名。Communication / Run / `agent.yml` 是 IBM；Client / `session/prompt` / stdio 是 Zed。[14][20][22]
2. 2025 年的 MCP 教程把 `initialize` 和 HTTP+SSE 传输写成必选项。现行规范里前者已删，后者是 Deprecated；SSE 帧本身还在 Streamable HTTP 里。[3][4][6]
3. Claude MCP connector 仍接受 Streamable HTTP 和 SSE，且不能直连 stdio。beta header 见 `mcp-client-2025-11-20` 与 `mcp-client-2026-09-15`。这是产品兼容，不是传输被加回标准列表。[36]
4. A2A 的发送路径是 `POST /message:send`，不是 ACP 的 `POST /runs`。[10][14]
5. AG-UI README 写约 16 种事件；schema 是结构权威。端点路径没有规范成固定 URL。对比页 `about/mcp-and-a2a` 没随合并改。[17][28][29]

## 5. 未决与置信度

- 厂商四行都是 ❓。已看到入口、没按格摘完：OpenAI Agents SDK，Anthropic connector（正文只用了传输句），Google ADK 的 A2A 与 `ucp.dev`，Microsoft Learn 多 agent 页（笔记中的 `ms.date` 2026-07-06）。
- 「两份 ACP 是否为别名」还没有专向反证。两边站内索引没点名对方，只覆盖查过的页。
- SEP-2596 是否 Final：未知。2025-06-18 传输页有「兼容旧 HTTP+SSE」一句，是否还在 2026-07-28，没对过。
- A2A：站上 1.0.0；笔记称 tag v1.0.1（2026-05-28），原句是 API 摘要。gRPC/REST 与 `application/a2a+json` 在主张里，摘录只截到 JSON-RPC。`TaskState`、ACP `RunStatus`、AG-UI「31 个 EventType」、MCP 的 `InputRequiredResult` 也是主张有、摘录被截断。
- BeeAI 捐 LF：讨论帖写 2025-03 当月，新闻稿是 2025-04-29。迁移指南 404。OpenAPI 无 `securitySchemes` 是 grep，不是原句。
- MCP 规范没点名另外三家。分层来自 A2A、Zed ACP、AG-UI 的页面。
- 未进家族的线索：ANP、UCP、AP2、NLWeb、Agent Protocol（AI Engineer Foundation）、AGNTCY。

## 来源

[1] https://modelcontextprotocol.io/specification/2026-07-28/architecture
[2] https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
[3] https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http
[4] https://modelcontextprotocol.io/specification/2026-07-28/changelog
[5] https://modelcontextprotocol.io/specification/2025-03-26/changelog
[6] https://modelcontextprotocol.io/specification/2026-07-28/deprecated
[7] https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
[8] https://modelcontextprotocol.io/community/governance
[9] https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
[10] https://a2a-protocol.org/latest/specification/
[11] https://a2a-protocol.org/latest/topics/key-concepts/
[12] https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/
[13] https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
[14] https://agentcommunicationprotocol.dev/spec/openapi.yaml
[15] https://github.com/i-am-bee/acp
[16] https://github.com/orgs/i-am-bee/discussions/5
[17] https://agentcommunicationprotocol.dev/about/mcp-and-a2a
[18] https://agentcommunicationprotocol.dev/core-concepts/agent-discovery
[19] https://agentcommunicationprotocol.dev/core-concepts/production-grade
[20] https://agentclientprotocol.com/get-started/introduction
[21] https://agentclientprotocol.com/protocol/v1/overview
[22] https://agentclientprotocol.com/protocol/v1/transports
[23] https://agentclientprotocol.com/protocol/v1/initialization
[24] https://agentclientprotocol.com/community/governance
[25] https://github.com/agentclientprotocol/agent-client-protocol
[26] https://agentclientprotocol.com/announcements/acp-v2-draft
[27] https://agentclientprotocol.com/get-started/architecture
[28] https://docs.ag-ui.com/spec/1.0
[29] https://docs.ag-ui.com/spec/1.0/schema.json
[30] https://docs.ag-ui.com/agentic-protocols
[31] https://docs.ag-ui.com/spec/1.0/basic/transports
[32] https://docs.ag-ui.com/spec/1.0/basic/capabilities
[33] https://docs.ag-ui.com/spec/1.0/changelog
[34] https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse
[35] https://developers.openai.com/apps-sdk/concepts/mcp-server
[36] https://platform.claude.com/docs/en/agents-and-tools/mcp-connector
