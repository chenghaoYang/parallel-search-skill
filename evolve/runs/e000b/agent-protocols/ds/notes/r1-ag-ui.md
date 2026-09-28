# r1-ag-ui
question: AG-UI（Agent-User Interaction Protocol）管什么、怎么传输、怎么鉴权、谁治理、当前版本、谁在用；官方文档怎么描述它和 MCP、A2A 的关系
checked: https://docs.ag-ui.com, https://github.com/ag-ui-protocol/ag-ui, https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-agui-protocol-contract.html, https://docs.ag-ui.com/concepts/architecture, https://docs.ag-ui.com/agentic-protocols, https://docs.ag-ui.com/concepts/state

## claims
- [C1] AG-UI 是"open, lightweight, event-based protocol that standardizes how AI agents connect to user-facing applications" | src: https://docs.ag-ui.com | quote: "open, lightweight, event-based protocol that standardizes how AI agents connect to user-facing applications" | type: official
- [C2] AG-UI 处理 agent 后端与用户前端 UI 交互层，补充 MCP（工具连接）和 A2A（agent 对等通信） | src: https://docs.ag-ui.com/agentic-protocols | quote: "AG-UI contributors have recently added handshakes, allowing AG-UI to 'front for' agents through MCP and A2A protocols" | type: official
- [C3] 传输支持 "any event transport (SSE, WebSockets, webhooks, etc.)" 通过中间件层 | src: https://github.com/ag-ui-protocol/ag-ui | quote: "any event transport (SSE, WebSockets, webhooks, etc.)" | type: official
- [C4] HTTP SSE（Server-Sent Events）传输："Text-based streaming for wide compatibility" | src: https://docs.ag-ui.com/concepts/architecture | quote: "Text-based streaming for wide compatibility" | type: official
- [C5] AWS Bedrock AgentCore 实现中传输为 SSE 或 WebSocket | src: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-agui-protocol-contract.html | quote: "Transport: Server-Sent Events (SSE) or WebSocket - SSE provides unidirectional streaming from server to client, while WebSocket enables bidirectional real-time communication" | type: official
- [C6] 协议定义 16 个标准事件类型（生命周期、消息、工具调用、状态、特殊类型） | src: https://docs.ag-ui.com/concepts/architecture | quote: "16 standardized events across five categories: Lifecycle, Messages, Tools, State, Special" | type: official
- [C7] 鉴权：Transport-agnostic，支持 HTTP Bearer Token 和 SigV4 认证 | src: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-agui-protocol-contract.html | quote: "AG-UI agents support multiple authentication mechanisms: OAuth 2.0 Bearer Tokens... Standard AWS SigV4 authentication" | type: official
- [C8] 鉴权可通过 HTTP 头传递 Bearer token 或 API key，支持自定义中间件 | src: https://github.com/ag-ui-protocol/ag-ui | quote: "pass authentication tokens via HTTP headers (Bearer tokens, API keys) on the POST request" | type: secondary
- [C9] 会话状态在 agent backend 保存，前端通过 STATE_SNAPSHOT 和 STATE_DELTA 事件同步 | src: https://docs.ag-ui.com/concepts/state | quote: "state resides on the agent backend, which serves as the source of truth. The frontend maintains a synchronized copy that receives updates through STATE_SNAPSHOT events - Full state representations... STATE_DELTA events - Incremental changes" | type: official
- [C10] 治理：开源项目（MIT 许可证），由 CopilotKit 主导，GitHub: github.com/ag-ui-protocol/ag-ui | src: https://github.com/ag-ui-protocol/ag-ui | quote: "MIT" (license tag), "ag-ui-protocol" (organization) | type: official
- [C11] 当前版本 1.0（2026-09-17），线路协议版本从 "draft" 改为 "1.0" | src: https://github.com/ag-ui-protocol/ag-ui/releases | quote: "ag-ui-protocol 1.0.0 was released on 2026-09-17. The wire protocol version is now the generated PROTOCOL_VERSION (1.0)" | type: official
- [C12] 前一版本为 0.x（0.1.15-0.1.22），向后兼容 | src: https://github.com/ag-ui-protocol/ag-ui/releases | quote: "Behaviour on 0.1.15 to 0.1.22 is unchanged" | type: official
- [C13] 一方采用者：Microsoft（Agent Framework）、Google（ADK）、AWS（Bedrock AgentCore, Strands Agents）、Mastra、Pydantic AI、Agno、LlamaIndex、AG2 | src: https://docs.ag-ui.com | quote: "1st party support from Microsoft, Google, AWS" | type: official
- [C14] 二方采用者：LangChain 和 CrewAI 有原生支持和文档 | src: https://docs.ag-ui.com | quote: "partnership implementations with LangChain and CrewAI" | type: official
- [C15] 社区采用：Claude Agent SDK、Langroid 及多种语言 SDK（Kotlin、Go、Dart、Java、Rust、Ruby、C++、.NET） | src: https://docs.ag-ui.com | quote: "Claude Agent SDK, Langroid, and multiple SDKs (Kotlin, Go, Dart, Java, Rust, Ruby, C++, .NET)" | type: official
- [C16] 官方对协议栈描述：MCP 连接 agents 到工具，A2A 启用 agent 间直接通信，AG-UI 是界面层 | src: https://docs.ag-ui.com/agentic-protocols | quote: "MCP (Model Context Protocol) connects agents to tools and contextual information... A2A (Agent to Agent) enables direct communication between agents. AG-UI (Agent–User Interaction) serves as the interface layer connecting agents with end users" | type: official
- [C17] AG-UI 的"kitchen sink"设计面向实际应用需求 | src: https://docs.ag-ui.com/agentic-protocols | quote: "'kitchen sink' protocol — meaning it addresses practical, real-world requirements for building sophisticated agentic applications" | type: official

## conflicts
- 无冲突发现

## gaps
- 无正式的治理委员会或标准组织信息
- 鉴权规范是否有独立文档规范（还是完全依赖具体实现）
- 状态管理中持久化存储的实现方案（AG-UI 规范本身是否规定或由应用自决）

## leads
- AWS Bedrock AgentCore 提供了官方的生产级实现参考
- Microsoft Agent Framework 集成可能有额外的鉴权/状态管理细节
- "front for MCP and A2A" 的握手机制需要深入技术细节
