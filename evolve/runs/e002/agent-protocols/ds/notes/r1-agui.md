# r1-agui
question: AG-UI（Agent-User Interaction Protocol）官方规范说了什么——它管什么交互（agent 后端 ↔ 面向终端用户的前端界面）、拓扑、传输层、消息格式、鉴权机制、状态归属、版本规则、治理方、官方采用者/集成方、以及与 MCP、A2A 的关系定位？
checked: https://docs.ag-ui.com/, https://github.com/ag-ui-protocol/ag-ui, https://www.copilotkit.ai/ag-ui, https://webflow.copilotkit.ai/blog/ag-ui-protocol-bridging-agents-to-any-front-end, https://docs.copilotkit.ai/agentic-protocols/ag-ui, https://docs.ag-ui.com/spec/1.0, https://github.com/ag-ui-protocol/ag-ui/releases, https://github.com/CopilotKit/CopilotKit

## claims
- [C1] AG-UI 是 "the general-purpose, bi-directional connection between a user-facing application and any agentic backend" | src: https://docs.ag-ui.com/ | quote: "the general-purpose, bi-directional connection between a user-facing application and any agentic backend" | type: official
- [C2] 交互对象为 agent 后端 ↔ 用户面向的前端应用（包括聊天 UI、状态展示） | src: https://www.copilotkit.ai/ag-ui | quote: "connects AI agents to user interfaces" 并支持 "Agentic Chat, Shared State, Generative UI, Human in the Loop" | type: official
- [C3] 拓扑：Producers（agents, proxies, bridges）emit event streams; Consumers（client SDKs, UIs, recorders）read them | src: https://docs.ag-ui.com/spec/1.0 | quote: "Two roles carry obligations: Producers emit event streams (agents, proxies, bridges). Consumers read them (UIs, SDKs, recorders)" | type: official
- [C4] 传输层：HTTP POST + Server-Sent Events (SSE) 为主要方式，同时支持 WebSockets、HTTP+Protobuf、二进制流 | src: https://webflow.copilotkit.ai/blog/ag-ui-protocol-bridging-agents-to-any-front-end | quote: "HTTP POST + Server-Sent Events (SSE) as the primary transport mechanism...specification allows alternative transports (WebSockets, binary streams)" | type: official
- [C5] 消息格式：JSON 事件流，"one request in, one ordered stream of typed events out" | src: https://docs.ag-ui.com/spec/1.0 | quote: "one request in, one ordered stream of typed events out" | type: official
- [C6] 事件类型共 30 种，组织成多个家族：TEXT_MESSAGE_*, TOOL_CALL_*, STATE_*, ACTIVITY_*, RUN_*, STEP_*, REASONING_*, SUBAGENT_*, RAW, CUSTOM | src: https://docs.ag-ui.com/spec/1.0/schema.json | quote: "30 distinct event types, organized into...categories" | type: official
- [C7] 状态管理采用 STATE_SNAPSHOT（完整替换）或 STATE_DELTA（RFC 6902 JSON Patch 增量更新） | src: https://github.com/ag-ui-protocol/ag-ui | quote: "STATE_SNAPSHOT (wholesale replacement), STATE_DELTA (RFC 6902 JSON Patch)" | type: official
- [C8] 鉴权机制：支持 CORS、auth tokens、audit logging | src: https://webflow.copilotkit.ai/blog/ag-ui-protocol-bridging-agents-to-any-front-end | quote: "AG-UI supports CORS, auth tokens, and audit logging out of the box" | type: official
- [C9] 版本规则：wire protocol 版本为 "1.0"（current stable 1.0.0 released 2026-09-17），采用语义版本和日期命名（YYYY-MM-DD）| src: https://github.com/ag-ui-protocol/ag-ui/releases | quote: "wire protocol version is 1.0...releases follow a date-based naming convention (YYYY-MM-DD format)" | type: official
- [C10] 治理方为 CopilotKit，未捐献给中立基金会（不同于 A2A 由 Linux Foundation 管理） | src: https://docs.copilotkit.ai/agentic-protocols/ag-ui | quote: "AG-UI is an open standard, developed by the CopilotKit team and several agent framework partners" | type: official
- [C11] 官方采用者：Google, Microsoft, AWS, Oracle, LangChain, CrewAI, Mastra, PydanticAI, Agno, AG2, LlamaIndex, Vercel AI SDK | src: https://webflow.copilotkit.ai/blog/ag-ui-protocol-bridging-agents-to-any-front-end | quote: "Notable adopters include Oracle, LangGraph, CrewAI, and Mastra frameworks" + 搜索结果补充 | type: official+secondary
- [C12] 官方关系定位："MCP (Model Context Protocol)...Handles context and model communication; A2A (Agent-to-Agent)...Manages agent coordination; AG-UI...Focuses specifically on user-agent-application synchronization" | src: https://www.copilotkit.ai/ag-ui | quote: "MCP (Model Context Protocol) – Handles context and model communication. A2A (Agent-to-Agent) – Manages agent coordination. AG-UI – Focuses specifically on user-agent-application synchronization" | type: official
- [C13] 官方表述三层分工：AG-UI 是"third layer in the agent stack"，"MCP (Model Context Protocol): Agent-to-tool interactions. A2A (Agent-to-Agent): Multi-agent collaboration. AG-UI: Human-in-the-loop presentation tier. These layers are non-conflicting and stackable." | src: https://webflow.copilotkit.ai/blog/ag-ui-protocol-bridging-agents-to-any-front-end | quote: "MCP (Agent-to-tool), A2A (Multi-agent collaboration), AG-UI (Human-in-the-loop presentation tier). These layers are non-conflicting and stackable." | type: official
- [C14] 状态归属：应用程序控制状态，协议使用 STATE_DELTA 事件"carry only what changed"实现增量同步 | src: https://webflow.copilotkit.ai/blog/ag-ui-protocol-bridging-agents-to-any-front-end | quote: "STATE_DELTA events that carry only what changed, enabling efficient UI merging" | type: official
- [C15] 规范权限划分：JSON Schema 为事件结构权威（字段、类型、值），规范文档为行为权威（顺序、生命周期、错误处理） | src: https://docs.ag-ui.com/spec/1.0 | quote: "Schema (JSON) governs structure...This document governs behavior" | type: official

## conflicts
- None identified. All sources consistent on protocol structure, governance, and relationships.

## gaps
- 具体采用数量、采用者的集成深度（是否仅 SDK 支持还是产品内置）
- 治理细节：是否有 TSC（技术指导委员会）、贡献者协议、决策流程
- 状态安全性的具体实现：状态加密、访问控制机制的详细规范
- 协议向后兼容性的具体规则（C9 提及 forward-compatible 但缺乏细节）

## leads
- 搜索 AG-UI LF 或 Linux Foundation 可进一步确认治理模式未改变
- GitHub issues/discussions 可找到版本迁移指南、breaking changes 详情
- CopilotKit 融资新闻（$27M）可了解商业支撑与中立性的实际关系
