# r1-agui
question: AG-UI 现行官方规范管什么：谁和谁通信、事件模型、传输、鉴权、状态、版本、治理，以及它如何描述自己和 MCP、A2A、A2UI 的关系。
checked: https://docs.ag-ui.com/, https://docs.ag-ui.com/spec/1.0, https://docs.ag-ui.com/spec/1.0/architecture, https://docs.ag-ui.com/spec/1.0/basic, https://docs.ag-ui.com/spec/1.0/basic/capabilities, https://docs.ag-ui.com/spec/1.0/basic/transports, https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse, https://docs.ag-ui.com/spec/1.0/basic/versioning, https://docs.ag-ui.com/spec/1.0/events, https://docs.ag-ui.com/spec/1.0/events/state, https://docs.ag-ui.com/spec/1.0/changelog, https://github.com/ag-ui-protocol/ag-ui, https://www.npmjs.com/package/@ag-ui/core

## claims
- [C1] 自我定位：开放轻量事件协议，连接 AI agent 与面向用户的应用 | src: https://docs.ag-ui.com/ | quote: "AG-UI is an open, lightweight, event-based protocol that standardizes how AI agents connect to user-facing applications." | type: official
- [C2] 规范义务角色是 producer / consumer | src: https://docs.ag-ui.com/spec/1.0 | quote: "A producer is whatever emits the event stream — an agent, a proxy, a bridge, a test double. A consumer is whatever reads it — a client SDK, a UI, a recorder, another proxy." | type: official
- [C3] 应用侧职责：渲染流、执行前端 tool call、保存共享 state、决定用户同意 | src: https://docs.ag-ui.com/spec/1.0/architecture | quote: "It renders the stream, executes the tool calls it advertised, keeps the state the agent shares with it, and decides what requires the user's consent." | type: official
- [C4] 生产侧 = agent endpoint + bridge | src: https://docs.ag-ui.com/spec/1.0/architecture | quote: "A bridge translates a framework's native events into protocol events; the endpoint speaks a transport binding." | type: official
- [C5] 交互单位是 run：consumer 发 RunAgentInput，producer 回生命周期括起的事件流；会话是 thread | src: https://docs.ag-ui.com/spec/1.0/architecture | quote: "A consumer opens an exchange with one RunAgentInput; the producer answers with events bracketed by the run lifecycle" | type: official
- [C7] 事件信封 BaseEvent：type 必填判别字段；1.0 共 31 个 EventType、8 个家族 | src: https://docs.ag-ui.com/spec/1.0/basic | quote: "type — REQUIRED. The discriminator, one of the 31 values of EventType." | type: official
- [C8] 8 家族类型原名：RUN_STARTED/FINISHED/ERROR、STEP_*，TEXT_MESSAGE_*，TOOL_CALL_*，REASONING_*，STATE_SNAPSHOT/DELTA、MESSAGES_SNAPSHOT，ACTIVITY_*，SUBAGENT_*，RAW/CUSTOM | src: https://docs.ag-ui.com/spec/1.0/events | quote: "Everything a producer has to say arrives as events, in eight families." | type: official
- [C9] 仅 run 生命周期强制，其余为可选 feature | src: https://docs.ag-ui.com/spec/1.0/events | quote: "Only the run lifecycle is mandatory for a producer — every other family is a feature it emits when it has something to say with it." | type: official
- [C10] discovery：schema 定义 AgentCapabilities 声明形状（identity、transport、tools、state、reasoning、humanInTheLoop 等 OPTIONAL 组），但故意不规定获取途径 | src: https://docs.ag-ui.com/spec/1.0/basic/capabilities | quote: "No transport binding in this version carries a capabilities exchange, and this page does not create one" | type: official
- [C11] 版本协商带内完成 | src: https://docs.ag-ui.com/spec/1.0/basic/versioning | quote: "A consumer declares the protocol version it speaks on RunAgentInput.protocolVersion. A producer declares the version it speaks on RUN_STARTED.protocolVersion" | type: official
- [C12] 默认传输 HTTP+SSE：POST RunAgentInput JSON，Accept/响应均为 text/event-stream | src: https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse | quote: "The application POSTs the run input to the agent's endpoint; the response is a Server-Sent Events stream carrying the run." | type: official
- [C13] SSE 分帧：每 data: 恰一个 JSON 事件；必须 LF 行尾 | src: https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse | quote: "Each SSE event's data payload is exactly one protocol event as a JSON object — never more than one, never a fragment." | type: official
- [C14] 无断流恢复；重跑即新 runId | src: https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse | quote: "The binding has no stream resumption: SSE's Last-Event-ID mechanism is not used, and a broken stream cannot be re-entered." | type: official
- [C15] 第二标准绑定 HTTP+Protobuf（长度前缀帧）可选；HTTP 实现必须支持 SSE | src: https://docs.ag-ui.com/spec/1.0/basic/transports | quote: "An implementation that speaks HTTP MUST support the SSE binding; the protobuf binding is OPTIONAL." | type: official
- [C16] 允许自定义传输 | src: https://docs.ag-ui.com/spec/1.0/basic/transports | quote: "Implementations MAY carry AG-UI over other channels — WebSockets, message buses, in-process pipes." | type: official
- [C17] 鉴权不在协议内：协议不定义凭据 | src: https://docs.ag-ui.com/spec/1.0/basic/transports | quote: "Authentication and authorization are properties of the binding and the application, not of the protocol: AG-UI defines no credential" | type: official
- [C18] 安全条款：副作用工具需用户同意；模型输出按不可信输入处理 | src: https://docs.ag-ui.com/spec/1.0 | quote: "Applications MUST validate what they act on and MUST NOT render streamed content as executable markup." | type: official
- [C19] STATE_SNAPSHOT 以字段 snapshot 全量替换 | src: https://docs.ag-ui.com/spec/1.0/events/state | quote: "Replaces the agent state wholesale. ... A consumer MUST replace its state with snapshot — no merging." | type: official
- [C20] STATE_DELTA 用 RFC 6902 JSON Patch | src: https://docs.ag-ui.com/spec/1.0/events/state | quote: "Amends the current state with an RFC 6902 patch." | type: official
- [C21] 状态由 agent 与应用共持、随 run 往返（RunAgentInput.state 回传）；另有 MESSAGES_SNAPSHOT | src: https://docs.ag-ui.com/spec/1.0/events/state | quote: "State persists across runs on a thread until an event replaces it, and the next run's input carries it back as the starting value" | type: official
- [C22] 现行规范 1.0：schema.json 管结构、本文管行为；RFC 2119 用语 | src: https://docs.ag-ui.com/spec/1.0 | quote: "This specification defines the authoritative protocol requirements, based on the JSON Schema in schema.json" | type: official
- [C23] 仓库 github.com/ag-ui-protocol/ag-ui，MIT 许可 | src: https://github.com/ag-ui-protocol/ag-ui | quote: "AG-UI is open source software licensed as MIT" | type: official
- [C24] 治理：CopilotKit 发起（与 LangChain/CrewAI 合作诞生）；工作组挂 CopilotKit Luma 日历；第一方 SDK：TS/Python/.NET | src: https://github.com/ag-ui-protocol/ag-ui | quote: "AG-UI was born from CopilotKit's initial partnership with LangChain and CrewAI" | type: official
- [C25] 官网点名：Microsoft Agent Framework、Google ADK、AWS Strands/Bedrock AgentCore Supported；OpenAI Agent SDK In Progress；Anthropic 以 Claude Agent SDK 列 Community | src: https://docs.ag-ui.com/ | quote: "1st party = the platforms that have AG‑UI built in and provide documentation for guidance." | type: official
- [C26] 协议栈分层：AG-UI=Agent↔User，MCP=Agent↔Tools & Data，A2A=Agent↔Agent | src: https://docs.ag-ui.com/ | quote: "Open standard (originated by Anthropic) that lets agents securely connect to external systems — tools, workflows, and data sources." | type: official
- [C27] 与 A2UI 的官方区分 | src: https://docs.ag-ui.com/ | quote: "A2UI is a generative UI specification - allowing agents to deliver UI widgets, where AG-UI is the Agent↔User Interaction protocol" | type: official

## conflicts
- 事件数量口径不一：README 称 "~16 standard event types"（https://github.com/ag-ui-protocol/ag-ui），spec 1.0 称 "one of the 31 values of EventType"（https://docs.ag-ui.com/spec/1.0/basic）。README 疑似停留在 0.x 口径。
- overview 称 "bi-directional connection"，architecture 称 "one channel: an ordered stream of typed events, answered to a single request"。

## gaps
- ACP：所开页面均未提及，无官方关系表述。
- 包版本号：npmjs.com 抓 @ag-ui/core 被验证码拦截；README 有 npm 版本 badge 但未渲染数值。
- 文档页只标 "1.0"，未见明确发布/更新日期。
- 基金会：无提及；仅见 ag-ui-protocol org 与 CopilotKit 主持的工作组。
- RunAgentInput 其余字段未逐字段取原句；时序图原句列 "RunAgentInput (threadId, runId, messages, tools, state)"。

## leads
- A2A 以中间件集成列 Supported/Partnership；A2UI 对比页 https://copilotkit.ai/ag-ui-and-a2ui
- 索引 https://docs.ag-ui.com/llms.txt；changelog 页有 1.0 vs 0.x 变更表（outcome、subagents、reasoning 取代 THINKING_* 等）
- 仓库含 skills/ag-ui-a2ui-integration；Oracle Agent Spec 列为标准类集成
