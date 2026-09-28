# r2-google
question: Google（Gemini、ADK、Vertex、Cloud）官方支持 MCP、A2A、两种 ACP、AG-UI 到哪一步；AP2 与 UCP 是不是这四个协议的变体，各管哪条边。
checked: https://adk.dev/mcp/, https://adk.dev/a2a/intro/, https://adk.dev/integrations/ag-ui/, https://a2a-protocol.org/latest/, https://ap2-protocol.org/, https://ucp.dev/, https://ucp.dev/latest/specification/overview/, https://docs.cloud.google.com/mcp/overview, https://ai.google.dev/gemini-api/docs/coding-agents, https://docs.cloud.google.com/architecture/choose-agentic-ai-architecture-components, https://docs.cloud.google.com/agent-builder/agent-engine/develop/a2a, https://docs.cloud.google.com/gemini-enterprise-agent-platform/build, https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/create-an-a2a-agent, https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/use-an-a2a-agent

## claims
- [C1] Google.MCP：ADK agent 可当 MCP client。 | src: https://adk.dev/mcp/ | quote: "An ADK agent can act as an MCP client and use tools provided by external MCP servers." | type: official
- [C2] Google.MCP：ADK 也可把 tools 包成 MCP server。 | src: https://adk.dev/mcp/ | quote: "How to build an MCP server that wraps ADK tools, making them accessible to any MCP client." | type: official
- [C3] Google.MCP：Cloud 远程 MCP server 支持 MCP version 2026-07-28，并写明协议由 Anthropic 开发。页脚 Last updated 2026-09-22 UTC。 | src: https://docs.cloud.google.com/mcp/overview | quote: "MCP is an open source protocol developed by Anthropic that standardizes how AI applications connect to data sources. Our MCP servers support version 2026-07-28 of MCP." | type: official
- [C4] Google.MCP：同页 MCP host 例子含 Gemini CLI。 | src: https://docs.cloud.google.com/mcp/overview | quote: "The main AI application that you're using or building—for example, Claude, VS Code, Gemini CLI, or Cursor IDE." | type: official
- [C5] Google.MCP：Gemini API 文档的 MCP 是公共 Docs server https://gemini-api-docs-mcp.dev。页脚 Last updated 2026-09-01 UTC。 | src: https://ai.google.dev/gemini-api/docs/coding-agents | quote: "Gemini hosts a public Model Context Protocol (MCP) server at https://gemini-api-docs-mcp.dev." | type: official
- [C6] Google.MCP/A2A：Agent Runtime 编排 MCP 与 A2A，但不托管自定义 MCP server。Last updated 2026-04-21 UTC。 | src: https://docs.cloud.google.com/architecture/choose-agentic-ai-architecture-components | quote: "Orchestrate agents and tools that use MCP and A2A. Agent Runtime efficiently manages the runtime for these components, but it doesn't support the hosting of custom MCP servers." | type: official
- [C7] Google.A2A 归属：Google 开发并捐给 Linux Foundation。 | src: https://a2a-protocol.org/latest/ | quote: "A2A was originally developed by Google and donated to the Linux Foundation." | type: official
- [C8] Google.A2A 边：A2A 站写 MCP 是 agent-to-tool。 | src: https://a2a-protocol.org/latest/ | quote: "MCP is for agent-to-tool communication: it standardizes how an agent connects to its tools, APIs, and resources to get information." | type: official
- [C9] Google.A2A 边：A2A 是 agent-to-agent，包括已用 MCP 的 agent。 | src: https://a2a-protocol.org/latest/ | quote: "A2A is for agent-to-agent communication: as a universal, decentralized standard, A2A lets independent agents — including those using MCP — discover each other, delegate tasks, and share results." | type: official
- [C10] Google.A2A：ADK 暴露侧叫 A2AServer。 | src: https://adk.dev/a2a/intro/ | quote: "ADK provides a simple way to "expose" this agent, turning it into an A2AServer." | type: official
- [C11] Google.A2A：Gemini Enterprise Agent Platform 的 Agent Runtime 可开发并部署 A2A。create 页脚 Last updated 2026-09-22 UTC。 | src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/create-an-a2a-agent | quote: "Agent Runtime lets you develop and deploy agents using the Agent2Agent (A2A) protocol." | type: official
- [C12] Google.A2A：该功能标为 Pre-GA（页首 Preview）。 | src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/create-an-a2a-agent | quote: "Pre-GA features are available "as is" and might have limited support." | type: official
- [C13] Google.A2A：托管 agent 的操作对应 A2A API。use 页脚 Last updated 2026-09-22 UTC。 | src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/use-an-a2a-agent | quote: "An A2A agent hosted on Agent Runtime exposes a set of operations that correspond directly to the A2A protocol's API endpoints." | type: official
- [C14] Google.AG-UI：ADK 集成页把 AG-UI 写成 agent 与用户之间的开放协议。 | src: https://adk.dev/integrations/ag-ui/ | quote: "AG-UI is an open protocol that handles streaming events, client state, and bi-directional communication between your agents and users." | type: official
- [C15] Google.AG-UI：Architecture Center 写把 AG-UI 与 ADK 组合。 | src: https://docs.cloud.google.com/wiki/choose-agentic-ai-architecture-components | quote: "To build interactive AI applications, combine AG-UI with Agent Development Kit (ADK)." | type: official
- [C16] AP2 全称 Agent Payments Protocol (AP2)，面向 emerging Agent Economy。扩展对象两句见 conflicts。 | src: https://ap2-protocol.org/ | quote: "Agent Payments Protocol (AP2) is an open protocol for the emerging Agent Economy." | type: official
- [C17] AP2 的边是支付：ADK 建 agent、MCP 装工具、A2A 协作、AP2 管支付。 | src: https://ap2-protocol.org/ | quote: "Build agents with ADK (or any framework), equip with MCP (or any tool), collaborate via A2A, and use AP2 to secure payments with gen AI agents." | type: official
- [C18] UCP 规范标题给出全称 Universal Commerce Protocol (UCP)。 | src: https://ucp.dev/latest/specification/overview/ | quote: "Universal Commerce Protocol (UCP) Official Specification" | type: official
- [C19] UCP：AP2、A2A、MCP 为 support built-in，传输是 REST 与 JSON-RPC。 | src: https://ucp.dev/ | quote: "UCP is built on industry standards — REST and JSON-RPC transports; Agent Payments Protocol (AP2), Agent2Agent (A2A), and Model Context Protocol (MCP) support built-in — so different systems can work together without custom integration." | type: official
- [C20] UCP 规范 transport 枚举为 rest、mcp、a2a、embedded。 | src: https://ucp.dev/latest/specification/overview/ | quote: "Transport protocol for this service binding. Enum: rest, mcp, a2a, embedded" | type: official

## conflicts
- AP2 同页两套扩展对象都保留。src: https://ap2-protocol.org/ quote: "The protocol is available as an extension for the open-source Agent2Agent (A2A) protocol and Universal Commerce Protocol with more integrations in progress." 同页 quote: "As a non-proprietary, open extension for A2A and MCP, AP2 fosters a competitive environment for innovation, broad merchant reach, and user choice."
- MCP 是否算 inter-agent：https://docs.cloud.google.com/gemini-enterprise-agent-platform/build （Last updated 2026-09-22 UTC）quote: "support for inter-agent collaboration with Model Context Protocol (MCP) and Agent-to-Agent (A2A) protocol." 对 https://a2a-protocol.org/latest/ quote: "MCP is for agent-to-tool communication: it standardizes how an agent connects to its tools, APIs, and resources to get information." 不裁决。

## gaps
- Google.ACP-IBM：在 cloud.google.com、docs.cloud.google.com、adk.dev、ai.google.dev、developers.google.com 搜 "Agent Communication Protocol"，无产品页说支持 IBM ACP。
- Google.ACP-Zed：同范围搜 "Agent Client Protocol"，无产品页说支持 Zed ACP。
- Gemini 模型端点（generateContent、Interactions、Live）未见“本身是 MCP/A2A/ACP/AG-UI server”；已打开的只是 Docs MCP。
- UCP 首页/overview 与 AP2 首页都没有“扩展 ACP-IBM、ACP-Zed 或 AG-UI”的句子。
- https://docs.cloud.google.com/agent-builder/agent-engine/develop/a2a 打开后是 “Scale your agents”，不是旧 Develop A2A 教程。

## leads
- A2A 站顶栏 “A2A joins the Agentic AI Foundation”，与捐给 LF 并存。
- A2UI 可走 A2A 或 AG-UI：https://cloud.google.com/blog/topics/developers-practitioners/guide-to-gemini-enterprise-and-a2ui-integration （未摘正文）。
- AG2 模板与 A2A 并列：https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/create-an-ag2-agent ；未打开，不要当成 ACP。
- ADK 消费侧组件名 RemoteA2aAgent。use 页还有 on_get_task、on_cancel_task、handle_authenticated_agent_card。