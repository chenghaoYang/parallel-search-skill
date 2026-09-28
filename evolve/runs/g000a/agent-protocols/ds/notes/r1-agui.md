# r1-agui
question: AG-UI 官方规范现在规定谁和谁通信、事件/对象原名、传输、发现、鉴权、版本、治理、状态放在哪一端、官方如何描述它和 MCP、A2A 的关系。
checked: https://docs.ag-ui.com/spec/1.0.md, https://docs.ag-ui.com/spec/1.0/basic/index.md, https://docs.ag-ui.com/spec/1.0/architecture.md, https://docs.ag-ui.com/spec/1.0/basic/run-input.md, https://docs.ag-ui.com/spec/1.0/basic/transports/index.md, https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse.md, https://docs.ag-ui.com/spec/1.0/basic/transports/http-protobuf.md, https://docs.ag-ui.com/spec/1.0/basic/versioning.md, https://docs.ag-ui.com/spec/1.0/basic/capabilities.md, https://docs.ag-ui.com/spec/1.0/events/state.md, https://docs.ag-ui.com/spec/1.0/changelog.md, https://docs.ag-ui.com/spec/1.0/schema.json, https://docs.ag-ui.com/agentic-protocols.md, https://docs.ag-ui.com/introduction.md, https://docs.ag-ui.com/concepts/architecture.md, https://docs.ag-ui.com/spec/draft/changelog.md, https://raw.githubusercontent.com/ag-ui-protocol/ag-ui/main/README.md, https://raw.githubusercontent.com/ag-ui-protocol/ag-ui/main/.github/CODEOWNERS, https://github.com/ag-ui-protocol/ag-ui/releases

## claims
- [C1] 全称 The Agent–User Interaction (AG-UI) Protocol。 | src: https://docs.ag-ui.com/introduction.md | quote: "The Agent–User Interaction (AG-UI) Protocol" | type: official
- [C2] 发事件流的角色原名 producer：agent、proxy、bridge 或 test double。读流的角色原名 consumer。 | src: https://docs.ag-ui.com/spec/1.0.md | quote: "A producer is whatever emits the event stream — an agent, a proxy, a bridge, a test double. A consumer is whatever reads it — a client SDK, a UI, a recorder, another proxy." | type: official
- [C3] 反向恰好一条消息，原名 RunAgentInput，用来打开一次 exchange。 | src: https://docs.ag-ui.com/spec/1.0/basic/run-input.md | quote: "Exactly one message flows the other way: RunAgentInput, sent once to open each exchange." | type: official
- [C4] 应用保存与 agent 共享的 state。 | src: https://docs.ag-ui.com/spec/1.0/architecture.md | quote: "keeps the state the agent shares with it" | type: official
- [C5] 信封原名 BaseEvent。type 必填，取 EventType 的 31 个值之一。 | src: https://docs.ag-ui.com/spec/1.0/basic/index.md | quote: "one of the 31 values of EventType." | type: official
- [C6] 文本原名 TEXT_MESSAGE_START、TEXT_MESSAGE_CONTENT、TEXT_MESSAGE_END、TEXT_MESSAGE_CHUNK。 | src: https://docs.ag-ui.com/spec/1.0/basic/index.md | quote: "TEXT_MESSAGE_START TEXT_MESSAGE_CONTENT TEXT_MESSAGE_END TEXT_MESSAGE_CHUNK" | type: official
- [C7] 工具原名 TOOL_CALL_START、TOOL_CALL_ARGS、TOOL_CALL_END、TOOL_CALL_CHUNK、TOOL_CALL_RESULT。 | src: https://docs.ag-ui.com/spec/1.0/basic/index.md | quote: "TOOL_CALL_START TOOL_CALL_ARGS TOOL_CALL_END TOOL_CALL_CHUNK TOOL_CALL_RESULT" | type: official
- [C8] 状态事件原名 STATE_SNAPSHOT、STATE_DELTA、MESSAGES_SNAPSHOT。 | src: https://docs.ag-ui.com/spec/1.0/basic/index.md | quote: "STATE_SNAPSHOT STATE_DELTA MESSAGES_SNAPSHOT" | type: official
- [C9] RunAgentInput 的 threadId 与 runId 均为 REQUIRED。 | src: https://docs.ag-ui.com/spec/1.0/basic/run-input.md | quote: "threadId names the conversation and runId names the run this input requests; both are REQUIRED." | type: official
- [C10] schema $id 为 https://ag-ui.com/spec/1.0/schema.json。 | src: https://docs.ag-ui.com/spec/1.0/schema.json | quote: "https://ag-ui.com/spec/1.0/schema.json" | type: official
- [C11] 说 HTTP 的实现 MUST 支持 SSE 绑定；Protobuf 绑定 OPTIONAL。 | src: https://docs.ag-ui.com/spec/1.0/basic/transports/index.md | quote: "An implementation that speaks HTTP MUST support the SSE binding; the protobuf binding is OPTIONAL." | type: official
- [C12] 客户端 POST 到 agent endpoint，体为 UTF-8 JSON 的 RunAgentInput，Content-Type application/json。 | src: https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse.md | quote: "The client sends POST to the agent endpoint. The body is the RunAgentInput as a single JSON object, UTF-8 encoded, with Content-Type: application/json." | type: official
- [C13] Protobuf 媒体类型 application/vnd.ag-ui.event+proto。 | src: https://docs.ag-ui.com/spec/1.0/basic/transports/http-protobuf.md | quote: "Content-Type is exactly application/vnd.ag-ui.event+proto" | type: official
- [C14] 自定义传输 MAY 为 WebSockets、message buses、in-process pipes。 | src: https://docs.ag-ui.com/spec/1.0/basic/transports/index.md | quote: "WebSockets, message buses, in-process pipes." | type: official
- [C15] 鉴权不在协议内：AG-UI defines no credential。绑定可带 HTTP authentication、ambient identity，或为空。 | src: https://docs.ag-ui.com/spec/1.0/basic/transports/index.md | quote: "AG-UI defines no credential, and a binding carries whatever its channel uses" | type: official
- [C16] 版本标识是冻结版本所在段，形式 MAJOR.MINOR，按分量数值比较。 | src: https://docs.ag-ui.com/spec/1.0/basic/versioning.md | quote: "the segment a frozen version lives under, MAJOR.MINOR, compared numerically" | type: official
- [C17] 一次请求进、一条有序 typed events 出。 | src: https://docs.ag-ui.com/spec/1.0.md | quote: "one request in, one ordered stream of typed events out" | type: official
- [C18] 2026-09-17 官方 release：draft schema 冻为 1.0，PROTOCOL_VERSION 为 "1.0"，$id 迁到 /spec/1.0/schema.json。 | src: https://github.com/ag-ui-protocol/ag-ui/releases | quote: "Froze the draft schema as 1.0; PROTOCOL_VERSION now reads \"1.0\"" | type: official
- [C19] 发现：形状名 AgentCapabilities，但本版无 binding 携带 capabilities exchange；如何取得声明留给实现。 | src: https://docs.ag-ui.com/spec/1.0/basic/capabilities.md | quote: "No transport binding in this version carries a capabilities exchange" | type: official
- [C20] MCP（Model Context Protocol）连接 agents 到 tools 与 context。 | src: https://docs.ag-ui.com/agentic-protocols.md | quote: "MCP (Model Context Protocol) Connects agents to tools and to context" | type: official
- [C21] 状态跨 run 保留，下一次输入带回当前值作为起点。 | src: https://docs.ag-ui.com/spec/1.0/events/state.md | quote: "the next run's input carries it back as the starting value" | type: official
- [C22] A2A（Agent to Agent）连接 agents 到其他 agents。AG-UI 经 user-facing applications 连接 agents 到 users。 | src: https://docs.ag-ui.com/agentic-protocols.md | quote: "A2A (Agent to Agent) Connects agents to other agents. AG-UI (Agent–User Interaction) Connects agents to users (through user-facing applications)." | type: official
- [C23] 贡献者加了 handshakes，让 AG-UI front for MCP 与 A2A 上的 agents。 | src: https://docs.ag-ui.com/agentic-protocols.md | quote: "allowing AG-UI to \"front for\" agents through MCP and A2A protocols" | type: official
- [C24] 规范只写由 TypeScript、Python、.NET 三个 first-party SDK 维护，未点名标准组织。 | src: https://docs.ag-ui.com/spec/1.0.md | quote: "AG-UI is maintained with three first-party SDKs — TypeScript, Python and .NET" | type: official
- [C25] 仓库默认 CODEOWNERS 为 @ag-ui-protocol/copilotkit。 | src: https://raw.githubusercontent.com/ag-ui-protocol/ag-ui/main/.github/CODEOWNERS | quote: "* @ag-ui-protocol/copilotkit" | type: official
- [C26] README 列出 Biweekly AG-UI Working Group。 | src: https://raw.githubusercontent.com/ag-ui-protocol/ag-ui/main/README.md | quote: "Biweekly AG-UI Working Group" | type: official

## conflicts
- 事件数：1.0 “one of the 31 values of EventType”（https://docs.ag-ui.com/spec/1.0/basic/index.md）对概念页 “any of the 16 standardized event types”（https://docs.ag-ui.com/concepts/architecture.md）与 README “~16 standard event types”（https://raw.githubusercontent.com/ag-ui-protocol/ag-ui/main/README.md）。
- 传输：1.0 “MUST support the SSE binding”（https://docs.ag-ui.com/spec/1.0/basic/transports/index.md）对概念页 “doesn't mandate”（https://docs.ag-ui.com/concepts/architecture.md）。
- 严格性：概念页 “format exactly”（https://docs.ag-ui.com/concepts/architecture.md）对 1.0 “MUST emit only what the schema defines”（https://docs.ag-ui.com/spec/1.0/architecture.md）。
## gaps
- AG-UI.auth：无 header、scheme、token。已读 transports 与 http-sse；只说 refused auth 是开跑前 HTTP error。
- AG-UI.discovery：无 well-known 或方法名。Capabilities 页把 retrieval 留给实现。
- AG-UI.gov：规范无章程。仅有 CODEOWNERS、CopilotKit Luma Working Group，以及 born from CopilotKit。
- protocolVersion 在 schema 里是自由 string，不是 const。

## leads
- 集成包 @ag-ui/a2a-middleware、@ag-ui/mcp-middleware 不是 1.0 事件字段。draft changelog URL 现已显示 1.0 正文。
