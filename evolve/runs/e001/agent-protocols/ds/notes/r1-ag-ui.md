# r1-ag-ui
question: AG-UI（Agent-User Interaction Protocol）连接对象是什么？起源方是谁（是否是 CopilotKit）、治理方式（开源许可、是否有中立基金会）？版本历史？传输层机制（事件流、是否基于 SSE/WebSocket、具体事件类型有哪些）？鉴权机制官方怎么说？它和 MCP、A2A 的关系官方页面是怎么表述的（是否明确说「互补而非竞争」，各自负责哪一层）？

checked: https://docs.ag-ui.com/introduction, https://github.com/ag-ui-protocol/ag-ui/, https://www.copilotkit.ai/ag-ui, https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/, https://docs.ag-ui.com/agentic-protocols, https://webflow.copilotkit.ai/blog/master-the-17-ag-ui-event-types-for-building-agents-the-right-way, https://github.com/ag-ui-protocol/ag-ui/releases

## claims
- [C1] AG-UI 连接对象：Agent 后端与前端用户界面之间的双向连接。 | src: https://docs.ag-ui.com/introduction | quote: "the general-purpose, bi-directional connection between a user-facing application and any agentic backend" | type: official
- [C2] AG-UI 是开源、轻量级、事件驱动的协议。 | src: https://docs.ag-ui.com/introduction | quote: "an open, lightweight, event-based protocol that standardizes how AI agents connect to user-facing applications" | type: official
- [C3] AG-UI 起源方为 CopilotKit（venture-backed startup，非基金会治理）。 | src: https://github.com/ag-ui-protocol/ag-ui/ | quote: "MIT license, created and maintained by CopilotKit" | type: official
- [C4] AG-UI 采用 MIT 开源许可。 | src: https://github.com/ag-ui-protocol/ag-ui/blob/main/README.md | quote: "License: MIT open source" | type: official
- [C5] CopilotKit 在 2026 年 5 月融资 $27M Series A，团队由 Atai Barkai 和 Uli Barkai 兄弟创办。 | src: https://www.copilotkit.ai/blog/series-a | quote: "CopilotKit raises $27M Series A" | type: official
- [C6] AG-UI 治理状态：现由 venture-backed startup 维护，未交付中立基金会。 | src: https://rywalker.com/research/ag-ui | quote: "The steward is a venture-backed startup, not a foundation — CopilotKit raised a $27M Series A in May 2026" | type: secondary
- [C7] 协议规范首次发布于 2026 年 7 月 18 日。 | src: https://github.com/ag-ui-protocol/ag-ui/releases | quote: "Release Release 2026-07-18" | type: official
- [C8] AG-UI 核心规范版本 1.0 于 2026 年 9 月 17 日发布，所有 SDK（TypeScript、Python、.NET）均达到 1.0.0。 | src: https://github.com/ag-ui-protocol/ag-ui/releases/tag/release/2026-09-17 | quote: "Major 1.0 Release: 2026-09-17, TypeScript/npm @ag-ui/client, @ag-ui/core reached 1.0.0" | type: official
- [C9] 规范文件位置：/spec/1.0/schema.json（版本 1.0）。 | src: https://github.com/ag-ui-protocol/ag-ui/releases | quote: "The specification moved to `/spec/1.0/schema.json`" | type: official
- [C10] 传输层机制：支持 Server-Sent Events (SSE) 和 WebSocket，均传输 JSON 事件。 | src: https://docs.ag-ui.com/introduction | quote: "streaming a single sequence of JSON events over standard HTTP or an optional binary channel" | type: official
- [C11] 主传输为 SSE over HTTP，具有内置重连支持，工作于标准 HTTP，无防火墙问题。 | src: https://webflow.copilotkit.ai/blog/master-the-17-ag-ui-event-types-for-building-agents-the-right-way | quote: "SSE provides simpler unidirectional communication from server to client, includes built-in reconnection support" | type: secondary
- [C12] WebSocket 支持双向通信和低延迟场景，Chanx-kit 在 Django Channels 和 FastAPI/Starlette 上提供 WebSocket 传输。 | src: https://webflow.copilotkit.ai/blog/master-the-17-ag-ui-event-types-for-building-agents-the-right-way | quote: "Chanx-kit serves AG-UI over a WebSocket, built on chanx, a typed WebSocket layer for Django Channels and FastAPI/Starlette" | type: secondary
- [C13] AG-UI 定义了 17 种标准事件类型，分为 5 类别。 | src: https://webflow.copilotkit.ai/blog/master-the-17-ag-ui-event-types-for-building-agents-the-right-way | quote: "AG-UI defines 17 core event types organized into five categories" | type: official
- [C14] 事件类型分类：生命周期事件（5种：RunStarted, RunFinished, RunError, StepStarted, StepFinished）。 | src: https://webflow.copilotkit.ai/blog/master-the-17-ag-ui-event-types-for-building-agents-the-right-way | quote: "Lifecycle Events (5 types): RunStarted, RunFinished, RunError, StepStarted, StepFinished" | type: official
- [C15] 事件类型分类：文本消息事件（3种：TextMessageStart, TextMessageContent, TextMessageEnd）。 | src: https://webflow.copilotkit.ai/blog/master-the-17-ag-ui-event-types-for-building-agents-the-right-way | quote: "Text Message Events (3 types): TextMessageStart, TextMessageContent, TextMessageEnd" | type: official
- [C16] 事件类型分类：工具调用事件（4种：ToolCallStart, ToolCallArgs, ToolCallEnd, ToolCallResult）。 | src: https://webflow.copilotkit.ai/blog/master-the-17-ag-ui-event-types-for-building-agents-the-right-way | quote: "Tool Call Events (4 types): ToolCallStart, ToolCallArgs, ToolCallEnd, ToolCallResult" | type: official
- [C17] 事件类型分类：状态管理事件（3种：StateSnapshot, StateDelta, MessagesSnapshot）。 | src: https://webflow.copilotkit.ai/blog/master-the-17-ag-ui-event-types-for-building-agents-the-right-way | quote: "State Management Events (3 types): StateSnapshot, StateDelta, MessagesSnapshot" | type: official
- [C18] 事件类型分类：特殊事件（2种：RawEvent, CustomEvent）。 | src: https://webflow.copilotkit.ai/blog/master-the-17-ag-ui-event-types-for-building-agents-the-right-way | quote: "Special Events (2 types): RawEvent, CustomEvent" | type: official
- [C19] 所有事件遵循标准 JSON 结构，包含 type 鉴别字段。 | src: https://webflow.copilotkit.ai/blog/master-the-17-ag-ui-event-types-for-building-agents-the-right-way | quote: "All events follow a standardized JSON structure with a type discriminator field" | type: official
- [C20] 鉴权机制：可使用 Bearer token（Authorization: Bearer <oauth-token>）在请求头中传递。 | src: https://dev.to/kenhuangus/ag-ui-and-a2ui-protocols-explained | quote: "Bearer tokens in request headers (Authorization: Bearer <oauth-token>)" | type: secondary
- [C21] 鉴权机制：支持 AWS SigV4 认证用于编程访问。 | src: https://dev.to/kenhuangus/ag-ui-and-a2ui-protocols-explained | quote: "standard AWS SigV4 authentication for programmatic access" | type: secondary
- [C22] AG-UI 不内置授权机制，需在 HTTP 端点级别实现，使用应用框架的标准认证机制。 | src: https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/ | quote: "use the same authentication mechanisms as you would for any other HTTP endpoint" | type: official
- [C23] ThreadId 是相关性标识符而非授权凭证，不应作为认证边界。 | src: https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/ | quote: "An AG-UI thread ID is a correlation identifier, not an authentication boundary" | type: official
- [C24] 与 MCP 关系（官方表述）：MCP 连接 agent 与工具和上下文信息。 | src: https://docs.ag-ui.com/agentic-protocols | quote: "MCP (Model Context Protocol) links agents to tools and contextual information" | type: official
- [C25] 与 A2A 关系（官方表述）：A2A 启用 agent 与 agent 之间的直接通信和协调。 | src: https://docs.ag-ui.com/agentic-protocols | quote: "A2A (Agent to Agent) enables direct agent-to-agent communication and coordination" | type: official
- [C26] AG-UI 官方定位：作为用户与 agent 之间的交互桥梁。 | src: https://docs.ag-ui.com/agentic-protocols | quote: "AG-UI (Agent–User Interaction) bridges agents and end users through applications" | type: official
- [C27] 三种协议被描述为「互补而非竞争」。 | src: https://docs.ag-ui.com/agentic-protocols | quote: "The three protocols are complementary rather than competing" | type: official
- [C28] 单个 agent 通常同时使用全部三种协议。 | src: https://docs.ag-ui.com/agentic-protocols | quote: "individual agents commonly utilizing all three simultaneously" | type: official
- [C29] AG-UI 最近引入握手机制，允许代理 MCP 和 A2A 协议的 agent。 | src: https://docs.ag-ui.com/agentic-protocols | quote: "AG-UI recently introduced handshakes enabling it to proxy for agents that use MCP and A2A protocols" | type: official
- [C30] AG-UI 被描述为「厨房水槽」协议，以实际应用需求为基础。 | src: https://docs.ag-ui.com/agentic-protocols | quote: "the kitchen sink protocol grounded in practical requirements" | type: official
- [C31] 消息格式：事件流的 JSON 格式，标准化为同步执行事件如 run start、text emission、tool call 等。 | src: https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/ | quote: "typed execution events such as run start, text emission, tool call arguments, tool call results" | type: official
- [C32] 采用框架生态：LangChain/LangGraph、CrewAI、Microsoft Agent Framework、Google ADK、AWS、Mastra、Pydantic AI、LlamaIndex、AG2。 | src: https://docs.ag-ui.com/introduction | quote: "Microsoft Agent Framework, Google ADK, AWS Strands, Mastra, Pydantic AI, LlamaIndex, AG2; Partnerships: LangChain/LangGraph, CrewAI" | type: official
- [C33] 多语言 SDK：TypeScript/JavaScript、Python、Java、Kotlin、Go、Dart、Rust、Ruby、C++、.NET。 | src: https://docs.ag-ui.com/introduction | quote: "Community SDKs exist for Kotlin, Go, Dart, Java, Rust, Ruby, C++, and .NET" | type: official

## conflicts
- 版本号计数：搜索结果显示「~16 标准事件类型」和「17 核心事件类型」，需确认当前精确数字。根据官方博客原句，目前标准为 17 个事件类型。

## gaps
- AG-UI 首个公开发布日期前的开发时间线（是否在 CopilotKit 内部孵化、何时公开宣布）
- 规范 schema.json 是否有 API documentation 形式的 reference
- 官方规定的「线程」(threadId) 完整生命周期和数据结构 spec
- 具体的 HTTP POST 请求体格式示例规范

## leads
- CopilotKit 融资历程（$27M Series A May 2026）显示生态重视程度，但治理体制仍由商业公司主导，建议长期关注是否捐赠基金会
- AG-UI 与 MCP-UI、A2UI 的技术边界仍在演进中（MCP Apps 支持、A2UI partnership），建议跟踪 2026 年底前的治理变更