# Agent 协议：各管一条接缝

> 回答 MCP、A2A、ACP、AG-UI 各连接谁，以及鉴权、版本、治理、四大厂。截至 2026-09-24 的官方页。「ACP」在正文里写全名。

## 0. 一屏看懂

- 四条接缝可以叠用：MCP 是 Host 里的 Client 对一个工具 Server；A2A 是 Client 对不透明的远端 agent；Zed 的 Agent Client Protocol 是编辑器对 coding agent；AG-UI 是 producer 把事件流交给 UI。[1][9][14][16][17]
- 叫 ACP 的官方规范不是一份。IBM 的 Agent Communication Protocol 是 agent↔agent 的 REST（对象 Run），讨论帖宣布并入 A2A，仓库 2025-08-27 归档。Zed 的是 Agent Client Protocol。AGNTCY 的 Agent Connect Protocol 是另一份远程 agent API，规范仓 2026-04-11 归档。OpenAI 文档里的 ACP 是 Agentic Commerce Protocol。反证没有找到把 IBM 与 Zed 两份写成同一协议的官方页。[13][15][20][21][27]
- HTTP+SSE 这个传输名自 2025-03-26 起是 Deprecated，不是 Removed。SEP-2596 页状态为 Final。登记仍写 Final 后再过三个月才移除，并写明移除要等发版时的维护者决定；Removed 列表当时是空的。兼容旧端点的小节还在，用词是 can maintain。Streamable HTTP 要求 `Accept` 同时列出 `application/json` 和 `text/event-stream`。[3][4][5][6][8]
- 现行 MCP 是 **2026-07-28**，无状态，删掉协议级 session 和 `initialize`。Roots、Sampling、Logging、动态客户端注册同版 Deprecated。HTTP 鉴权可选：OAuth 2.1，server 作 resource server，MUST RFC9728；stdio 用环境凭据。token 禁止放进 query。[1][5][6][7]
- 接工具用 MCP，委托 agent 用 A2A，IDE 用 Zed 的 Client Protocol，画面用 AG-UI。不要新接 IBM 的 `/runs`。四家开发文档都写了 MCP。A2A 写在 Google ADK 和微软的架构指南里；OpenAI Agents Python SDK 维护者写明不放进该 SDK。AG-UI 写在 ADK 和微软 Agent Framework（集成表标 Preview）。[22][26][28][29][31][32]
- MCP 于 2025-12-09 捐入 Agentic AI Foundation，规范仍由 BDFL 经 SEP 决定。A2A 于 2026-08-27 成为该基金会 Growth Stage。Zed 的 Client Protocol 由 Zed 与 JetBrains 联合治理。项目技术方向各自自治。[10][11][12][39]

## 1. Taxonomy

主轴是对话两端，辅轴是工作单元。ACP 是撞车的缩写，不是一个家族。

| 家族 | 两端 | 工作单元 | 现在看 |
|---|---|---|---|
| 上下文与工具 | Client ↔ Server | 一次 JSON-RPC | MCP 2026-07-28 |
| Agent 互操作 | Client ↔ Remote Agent | Task（前身是 Run） | A2A 规范站 1.0.0 |
| 编程客户端 | 编辑器 ↔ agent | `session/prompt` | Agent Client Protocol |
| 人机界面 | producer ↔ consumer | `RunAgentInput` → 事件流 | AG-UI 1.0 |
| 商业 | 平台 ↔ 商户 | 结账 | Agentic Commerce Protocol、UCP |

## 2. 对照矩阵

| | 对象 | 传输 | 发现 / 鉴权 |
|---|---|---|---|
| MCP | Resources、Prompts、Tools。能力在每次请求的 `_meta.io.modelcontextprotocol/clientCapabilities`。`server/discover` 报版本和身份 | `stdio`、Streamable HTTP。HTTP+SSE 为 Deprecated | 见第 0 节。MUST RFC8707 `resource` |
| A2A | `AgentCard`、`Task`、`Artifact`。状态在 `Task.status`，产物在 `artifacts`。规范源 `spec/a2a.proto` | JSON-RPC over HTTP(S)，流为 SSE；同页主张还有 gRPC 与 HTTP+JSON。`POST /message:send`，`GET /tasks/{id}`。头前缀 `a2a-` | `/.well-known/agent-card.json`。`SecurityScheme` 五选一：apiKey、httpAuth、oauth2、openIdConnect、mtls |
| IBM Communication | OpenAPI **0.2.0**。`Run`，`RunMode`：`sync`/`async`/`stream` | `POST /runs` 的 200 可以是 `text/event-stream` | `GET /agents` |
| Zed Client | `initialize`、`authenticate`、`session/new`、`session/prompt`、`session/request_permission`；取消用 `session/cancel` | 已定义的是 stdio：换行分隔，stdout 只写协议消息 | 编辑器把用户的 MCP server 配置交给 agent，agent 自己去连 |
| AG-UI | 必填 `threadId`、`runId`、`messages`。强制只有 run 生命周期。`outcome`：`success`/`interrupt`/`cancelled` | 说 HTTP 就必须 HTTP+SSE。协议不定义凭证 | 版本字符串在 `RunAgentInput.protocolVersion` |

[1][2][3][7][9][15][16][19][36][37][38]

### 四大厂

「未见」只覆盖该行已查的开发文档。

| | MCP | A2A | IBM / Zed 的 ACP | AG-UI | 自家 |
|---|---|---|---|---|---|
| OpenAI | Responses 的 tool `type:"mcp"`，`server_url`。只接 Streamable HTTP 或 HTTP/SSE。SDK：`HostedMCPTool`、`MCPServerStreamableHttp`、`MCPServerSse`、`MCPServerStdio` | Python SDK 维护者：没有把 A2A 放进这个 SDK 的近期计划 | 已查文档未见。ACP 一词指商务协议 | 已查文档未见 | Agentic Commerce Protocol；Secure MCP Tunnel；MCP Apps 的 UI resource；Codex app-server（JSON-RPC） |
| Anthropic | `mcp_servers`（含 `url`、`authorization_token`）和 `mcp_toolset`。`anthropic-beta: mcp-client-2025-11-20`，`mcp-client-2026-09-15` 是超集。远程 HTTP，两种传输都接受，不能直连 stdio | 平台英文文档索引未见 | 索引未见 | 索引未见 | Managed Agents 用 `multiagent` 会话线程，不是 A2A |
| Google | Gemini：`mcp_server`，只要 Streamable HTTP；页面写 SSE server 不支持 | ADK 用 A2A 做 agent 协作。规范：MCP 是用工具，A2A 是 agent 搭档 | 已查的 ADK / Gemini / UCP 页未见 | ADK 有 AG-UI 集成 | UCP 内建 AP2、A2A、MCP |
| Microsoft | Learn（2026-07-06）：工具和数据用 MCP。NLWeb 实例同时是 MCP server，方法 `ask` | 同一页：跨平台 agent 用 A2A | 已查的 Learn 与 Agent Framework 集成页未见 | 集成表有 AG-UI，标 Preview | NLWeb：相对 MCP/A2A，如同 HTML 相对 HTTP |

[17][18][22][23][24][25][26][27][28][29][30][31][32][33][34]

## 3. 变体与适配层

| | 差异 |
|---|---|
| IBM Run → A2A Task | 同层前身。路径 `POST /runs` 对 `POST /message:send`。仓库只读，讨论帖写停止独立开发并贡献给 A2A |
| UCP | 商业规范，把 MCP 和 A2A 写成自己兼容的传输，不是改名 |
| NLWeb | 站点自然语言协议；README 里 A2A 是 soon |
| Codex app-server | 与 Zed Client Protocol 同层的 JSON-RPC，方法在 app-server 文档（如 `thread/start`），不是 `session/prompt` |
| AG-UI | 可以挡在 MCP / A2A agent 前面，面向用户应用 |

[13][15][17][21][25][30][33]

## 4. 用户需要知道的坑

1. 四个 ACP：Communication（IBM，已宣布并入 A2A）、Client（Zed）、Connect（AGNTCY，仓已归档）、Commerce（OpenAI）。[13][20][21][27]
2. 不要把 HTTP+SSE 传输或 `initialize` 当成现行 MCP 的必选项。SSE 帧还在；旧传输是 Deprecated，兼容写法是 can maintain。Gemini 远程 MCP 不接 SSE server。OpenAI SDK 写 Prefer Streamable HTTP or stdio。Claude connector 仍接受两种 HTTP。[3][5][8][22][23][24]
3. A2A 的发送路径是 `POST /message:send`，不是 `POST /runs`。[9][15]
4. A2A 规范站标 1.0.0。release v1.0.1（页上 2026-05-26）写了 spec 修复，包括优先 `application/a2a+json`。[9][35]

## 5. 未决与置信度

- 「未见」的范围：Anthropic 为 platform.claude.com 英文索引；OpenAI 为开发文档和 SDK 仓库搜索；Google 为 ADK、Gemini function-calling、UCP；微软为 Learn 多 agent 页和 Agent Framework 集成索引。没覆盖产品 UI。
- 三个月窗口的起算日，笔记用 PR #2596 的 API 字段 `merged_at`（2026-05-18）推算，不是规范页上的句子。draft 里兼容小节还在。何时 Removed，未知。
- `Part` 的 `text`/`raw`/`url`/`data`、gRPC 以外的绑定细节、`TaskState`、AG-UI「31 个事件」、IBM 生产环境的 Basic/Bearer/JWT、`/.well-known/agent.yml`，主张里有，这一稿没再单列，避免摘录对不上的名字进表。
- Zed 与 JetBrains 的联合治理、ACP v2 草案（公告日 2026-07-20）这一稿没有展开。
- MCP 规范没有点名另外三家。分层来自 A2A、Zed、AG-UI 的页面。

## 来源

[1] https://modelcontextprotocol.io/specification/2026-07-28/architecture
[2] https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
[3] https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http
[4] https://modelcontextprotocol.io/specification/2025-03-26/changelog
[5] https://modelcontextprotocol.io/specification/2026-07-28/changelog
[6] https://modelcontextprotocol.io/specification/2026-07-28/deprecated
[7] https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
[8] https://modelcontextprotocol.io/seps/2596-spec-feature-lifecycle-and-deprecation
[9] https://a2a-protocol.org/latest/specification/
[10] https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
[11] https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/
[12] https://modelcontextprotocol.io/community/governance
[13] https://github.com/i-am-bee/acp
[14] https://agentclientprotocol.com/get-started/introduction
[15] https://agentcommunicationprotocol.dev/spec/openapi.yaml
[16] https://docs.ag-ui.com/spec/1.0
[17] https://docs.ag-ui.com/agentic-protocols
[18] https://developers.openai.com/api/docs/guides/tools-connectors-mcp
[19] https://agentclientprotocol.com/protocol/v1/overview
[20] https://github.com/agntcy/acp-spec
[21] https://github.com/orgs/i-am-bee/discussions/5
[22] https://openai.github.io/openai-agents-python/mcp/
[23] https://platform.claude.com/docs/en/agents-and-tools/mcp-connector
[24] https://ai.google.dev/gemini-api/docs/function-calling
[25] https://ucp.dev/
[26] https://learn.microsoft.com/en-us/agents/architecture/multi-agent-patterns
[27] https://developers.openai.com/commerce/guides/key-concepts.md
[28] https://github.com/openai/openai-agents-python/pull/1245
[29] https://adk.dev/a2a/
[30] https://github.com/nlweb-ai/NLWeb
[31] https://learn.microsoft.com/en-us/agent-framework/integrations/
[32] https://adk.dev/integrations/ag-ui/
[33] https://learn.chatgpt.com/docs/app-server
[34] https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration
[35] https://github.com/a2aproject/A2A/releases/tag/v1.0.1
[36] https://docs.ag-ui.com/spec/1.0/basic/transports
[37] https://agentclientprotocol.com/protocol/v1/transports
[38] https://agentclientprotocol.com/get-started/architecture
[39] https://agentclientprotocol.com/community/governance
