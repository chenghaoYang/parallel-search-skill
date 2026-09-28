# r1-agui
question: AG-UI（Agent-User Interaction Protocol，或规范封面使用的正式名称）官方文档里，两端角色、事件原语、传输、状态、发现、鉴权、版本与治理，以及它如何定位和 MCP、A2A、A2UI 的关系。
checked: https://docs.ag-ui.com/llms.txt, https://docs.ag-ui.com/introduction.md, https://docs.ag-ui.com/spec/1.0.md, https://docs.ag-ui.com/spec/1.0/architecture.md, https://docs.ag-ui.com/spec/1.0/basic/index.md, https://docs.ag-ui.com/spec/1.0/basic/run-input.md, https://docs.ag-ui.com/spec/1.0/basic/capabilities.md, https://docs.ag-ui.com/spec/1.0/basic/versioning.md, https://docs.ag-ui.com/spec/1.0/basic/transports/index.md, https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse.md, https://docs.ag-ui.com/spec/1.0/basic/transports/http-protobuf.md, https://docs.ag-ui.com/spec/1.0/events/state.md, https://docs.ag-ui.com/spec/1.0/changelog.md, https://docs.ag-ui.com/spec/draft/changelog.md, https://docs.ag-ui.com/agentic-protocols.md, https://docs.ag-ui.com/concepts/generative-ui-specs.md, https://docs.ag-ui.com/concepts/architecture.md, https://docs.ag-ui.com/development/updates.md, https://docs.ag-ui.com/development/contributing.md, https://github.com/ag-ui-protocol/ag-ui, https://raw.githubusercontent.com/ag-ui-protocol/ag-ui/main/README.md

## claims
- [C1] D1 正式名 The Agent–User Interaction (AG-UI) Protocol。 | src: https://docs.ag-ui.com/introduction.md | quote: "The Agent–User Interaction (AG-UI) Protocol" | type: official
- [C2] D1 producer 发事件流：agent、proxy、bridge 或 test double。 | src: https://docs.ag-ui.com/spec/1.0.md | quote: "A producer is whatever emits the event stream — an agent, a proxy, a bridge, a test double." | type: official
- [C3] D1 consumer 读流：client SDK、UI、recorder 或另一个 proxy。 | src: https://docs.ag-ui.com/spec/1.0.md | quote: "A consumer is whatever reads it — a client SDK, a UI, a recorder, another proxy." | type: official
- [C4] D1 两端是 user-facing application 与任意 agentic backend，双向。 | src: https://docs.ag-ui.com/introduction.md | quote: "bi-directional connection between a user-facing application and any agentic backend." | type: official
- [C5] D2 EventType 有 31 个值；type 必填。 | src: https://docs.ag-ui.com/spec/1.0/basic/index.md | quote: "one of the 31 values of EventType." | type: official
- [C7] D2 名：RUN_STARTED RUN_FINISHED RUN_ERROR STEP_STARTED STEP_FINISHED；TEXT_MESSAGE_START TEXT_MESSAGE_CONTENT TEXT_MESSAGE_END TEXT_MESSAGE_CHUNK；TOOL_CALL_START TOOL_CALL_ARGS TOOL_CALL_END TOOL_CALL_CHUNK TOOL_CALL_RESULT。 | src: https://docs.ag-ui.com/spec/1.0/basic/index.md | quote: "`RUN_STARTED` `RUN_FINISHED` `RUN_ERROR` `STEP_STARTED` `STEP_FINISHED`" | type: official
- [C8] D2 名：REASONING_START REASONING_END REASONING_MESSAGE_START REASONING_MESSAGE_CONTENT REASONING_MESSAGE_END REASONING_MESSAGE_CHUNK REASONING_ENCRYPTED_VALUE；STATE_SNAPSHOT STATE_DELTA MESSAGES_SNAPSHOT；ACTIVITY_SNAPSHOT ACTIVITY_DELTA；SUBAGENT_STARTED SUBAGENT_FINISHED SUBAGENT_ERROR；RAW CUSTOM。 | src: https://docs.ag-ui.com/spec/1.0/basic/index.md | quote: "`ACTIVITY_SNAPSHOT` `ACTIVITY_DELTA`" | type: official
- [C9] D3 标准绑定 HTTP+SSE 与 HTTP+Protobuf。讲 HTTP 者 MUST SSE；protobuf OPTIONAL。 | src: https://docs.ag-ui.com/spec/1.0/basic/transports/index.md | quote: "MUST support the SSE binding; the protobuf binding is OPTIONAL." | type: official
- [C10] D3 SSE 默认绑定：客户端 POST RunAgentInput JSON。 | src: https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse.md | quote: "The client sends POST to the agent endpoint." | type: official
- [C12] D3 Protobuf 媒体类型 application/vnd.ag-ui.event+proto。 | src: https://docs.ag-ui.com/spec/1.0/basic/transports/http-protobuf.md | quote: "application/vnd.ag-ui.event+proto" | type: official
- [C13] D4 threadId 标识会话，应用铸造，跨 run 稳定。 | src: https://docs.ag-ui.com/spec/1.0/basic/index.md | quote: "threadId identifies a conversation. It is minted by the application and is stable across runs." | type: official
- [C14] D4 runId 标识一次 run，同一 thread 不得复用。 | src: https://docs.ag-ui.com/spec/1.0/basic/index.md | quote: "runId identifies one run. It MUST NOT be reused for another run on the same thread." | type: official
- [C16] D4 状态跨 thread 的 run 保留，下次 input 带回。 | src: https://docs.ag-ui.com/spec/1.0/events/state.md | quote: "State persists across runs on a thread until an event replaces it" | type: official
- [C17] D4 STATE_DELTA 用 RFC 6902 patch。 | src: https://docs.ag-ui.com/spec/1.0/events/state.md | quote: "Amends the current state with an RFC 6902 patch." | type: official
- [C18] D5 能力省略表示未声明，不是不支持。 | src: https://docs.ag-ui.com/spec/1.0/basic/capabilities.md | quote: "An omitted field means undeclared, not unsupported." | type: official
- [C19] D5 本版传输没有 capabilities 交换，也不定义如何取得声明。 | src: https://docs.ag-ui.com/spec/1.0/basic/capabilities.md | quote: "No transport binding in this version carries a capabilities exchange" | type: official
- [C20] D6 协议不定义 credential；认证由 binding 自带。 | src: https://docs.ag-ui.com/spec/1.0/basic/transports/index.md | quote: "AG-UI defines no credential, and a binding carries whatever its channel uses" | type: official
- [C21] D7 版本标识 MAJOR.MINOR，按分量数值比较。规范页为 1.0。 | src: https://docs.ag-ui.com/spec/1.0/basic/versioning.md | quote: "MAJOR.MINOR, compared numerically component by component" | type: official
- [C22] D7 版本字段：consumer 用 RunAgentInput.protocolVersion。 | src: https://docs.ag-ui.com/spec/1.0/basic/versioning.md | quote: "A consumer declares the protocol version it speaks on RunAgentInput.protocolVersion." | type: official
- [C23] D7 0.x 只定形状，行为在 TypeScript client。 | src: https://docs.ag-ui.com/spec/1.0/changelog.md | quote: "0.x defined shapes; behaviour lived in the TypeScript client." | type: official
- [C24] D7 最早公开条目：Update label 2025-04-09，协议初次发布。 | src: https://docs.ag-ui.com/development/updates.md | quote: "Initial release of the Agent User Interaction Protocol" | type: official
- [C25] D7 与 TypeScript、Python、.NET 三个 first-party SDK 一起维护。 | src: https://docs.ag-ui.com/spec/1.0.md | quote: "maintained with three first-party SDKs — TypeScript, Python and .NET" | type: official
- [C26] D7 README：生于 CopilotKit 与 LangChain、CrewAI 的 partnership。 | src: https://raw.githubusercontent.com/ag-ui-protocol/ag-ui/main/README.md | quote: "born from CopilotKit's initial partnership with LangChain and CrewAI" | type: official
- [C29] D9 概述把 A2UI 写成生成式 UI 规范。 | src: https://docs.ag-ui.com/introduction.md | quote: "A2UI is a generative UI specification" | type: official
- [C30] D9 AG-UI 通过用户侧应用把 agent 连到用户。 | src: https://docs.ag-ui.com/agentic-protocols.md | quote: "Connects agents to users (through user-facing applications)." | type: official
- [C31] D9 三者互补，一个 agent 可同时用全部三个。 | src: https://docs.ag-ui.com/agentic-protocols.md | quote: "a single agent can and often does use all 3 simultaneously." | type: official
- [C32] D9 AG-UI 不是生成式 UI 规范。 | src: https://docs.ag-ui.com/concepts/generative-ui-specs.md | quote: "AG-UI is not a generative UI specification" | type: official

## conflicts
- 事件数：概念页 “16 standardized event types”（https://docs.ag-ui.com/concepts/architecture.md）；README “~16 standard event types”（https://raw.githubusercontent.com/ag-ui-protocol/ag-ui/main/README.md）。规范 “31 values of EventType”（https://docs.ag-ui.com/spec/1.0/basic/index.md）且 “A producer MUST emit only what the schema defines”（https://docs.ag-ui.com/spec/1.0/architecture.md）。
- 传输：概念页列出 “SSE, webhooks, WebSockets, and more” 且 “doesn't mandate”（https://docs.ag-ui.com/concepts/architecture.md）。规范讲 HTTP 者 “MUST support the SSE binding”；自定义例子无 webhook（https://docs.ag-ui.com/spec/1.0/basic/transports/index.md）。

## gaps
- D6 无 OAuth、Bearer、API key。SSE 页仅把 refused auth 写成开跑前 HTTP 错误。
- D7 无基金会或章程。
- D5 无 well-known 与统一 base URL。RUN_STARTED.protocolVersion 未单独列主张。
- 身份字段是 threadId/runId；未再搜 schema.json 的 sessionId。D8 未填（未打开四家厂商文档）。正文无 1.0 批准日。

## leads
- 未打开：https://copilotkit.ai/ag-ui-and-a2ui ，https://github.com/google/A2UI ，https://docs.ag-ui.com/spec/1.0/schema.json ，https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-agui.html 。
