# r2-google
question: Google 官方文档里 Gemini、ADK、A2A、UCP 各支持/定义哪些协议？是否提到 MCP、IBM ACP、Zed ACP、AG-UI？UCP 是否算自家协议、官方如何定位与 MCP/A2A 的兼容？
checked: https://ucp.dev/ | https://ucp.dev/latest/specification/overview/ | https://ucp.dev/documentation/core-concepts/ | https://adk.dev/a2a/ | https://adk.dev/tools-custom/mcp-tools/ | https://adk.dev/integrations/ag-ui/ | https://ai.google.dev/gemini-api/docs/function-calling | https://a2a-protocol.org/latest/topics/a2a-and-mcp/ | https://github.com/a2aproject/A2A/releases/tag/v1.0.1

## claims
- [C1] Gemini API (Interactions API) 原生支持 remote MCP servers 作为工具，type="mcp_server" | src: https://ai.google.dev/gemini-api/docs/function-calling | quote: "Interactions API supports connecting to remote MCP servers to give the model access to external tools and services." | type: official
- [C2] Gemini Remote MCP 仅支持 Streamable HTTP，不支持 SSE | src: https://ai.google.dev/gemini-api/docs/function-calling | quote: "Remote MCP only works with Streamable HTTP servers. SSE (Server-Sent Events) servers are not supported." | type: official
- [C3] ADK 支持 A2A 协议（expose/consume，Python/Go/Java 等）| src: https://adk.dev/a2a/ | quote: "different agents need to collaborate and interact using Agent2Agent (A2A) Protocol" | type: official
- [C4] ADK 双向支持 MCP：McpToolset 作为 MCP client 消费外部 server；也可把 ADK tools 包成 MCP server | src: https://adk.dev/tools-custom/mcp-tools/ | quote: "This guide walks you through two ways of integrating Model Context Protocol (MCP) with ADK." | type: official
- [C5] ADK MCP 支持版本标注 Python v0.1.0 / TypeScript v0.2.0 / Go v0.1.0 / Java v0.1.0 / Kotlin v0.7.0；页面横幅 ADK TypeScript 2.0 GA | src: https://adk.dev/tools-custom/mcp-tools/ | quote: "Supported in ADKPython v0.1.0TypeScript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.7.0" | type: official
- [C6] ADK 官方集成页支持 AG-UI（经 CopilotKit，Python/TypeScript/Go/Java）| src: https://adk.dev/integrations/ag-ui/ | quote: "AG-UI is an open protocol that handles streaming events, client state, and bi-directional communication between your agents and users." | type: official
- [C7] A2A 官网将 A2A 与 MCP 定位为互补：MCP=纵向（agent→tools），A2A=横向（agent→agent）| src: https://a2a-protocol.org/latest/topics/a2a-and-mcp/ | quote: "A2A ❤️ MCP: Complementary Protocols for Agentic Systems ... A2A is about agents partnering on tasks; MCP is more about agents using capabilities." | type: official
- [C8] UCP 是独立开放规范（自家协议），由 Google、Shopify、Etsy、Walmart、Target、Amazon、Microsoft、Meta 等共同开发 | src: https://ucp.dev/ | quote: "UCP is an open standard ... Co-developed by industry leaders" ; core-concepts: "The Universal Commerce Protocol (UCP) is an open standard for interoperability between commerce entities." | type: official
- [C9] UCP 官方定位兼容关系：内建 AP2、A2A、MCP 支持，基于 REST 和 JSON-RPC 传输 | src: https://ucp.dev/ | quote: "UCP is built on industry standards — REST and JSON-RPC transports; Agent Payments Protocol (AP2), Agent2Agent (A2A), and Model Context Protocol (MCP) support built-in" | type: official
- [C10] UCP 面向 AI 平台侧写明与 MCP、A2A 及现有 agent 框架兼容 | src: https://ucp.dev/ | quote: "Compatible with MCP, A2A, and existing agent frameworks." | type: official
- [C11] UCP 服务 transport 枚举为 rest/mcp/a2a/embedded；MCP 用 OpenRPC，A2A 用 Agent Card | src: https://ucp.dev/latest/specification/overview/ | quote: "REST: OpenAPI 3.x; MCP: OpenRPC (JSON format); A2A: Agent Card Specification ... Enum: rest, mcp, a2a, embedded" | type: official
- [C12] UCP core-concepts 传输表：MCP 面向 "AI agents via Model Context Protocol"，A2A 面向 "Agent-to-Agent protocol integrations"；A2A endpoint 即 Agent Card URL | src: https://ucp.dev/documentation/core-concepts/ + https://ucp.dev/latest/specification/overview/ | quote: "an AI agent may prefer MCP, a traditional web app may use REST" ; "endpoint for A2A transport refers to the Agent Card URL" | type: official
- [C13] UCP 版本用日期标识 YYYY-MM-DD，规范示例最新快照 version "2026-08-25"（另有 draft、2026-01-11、2026-04-08 路径）| src: https://ucp.dev/latest/specification/overview/ | quote: "version": "2026-08-25" ; "UCP uses date-based version identifiers (YYYY-MM-DD)" | type: official
- [C14] MCP 传输下平台经 JSON-RPC params.meta["ucp-agent"].profile 传 profile URI | src: https://ucp.dev/latest/specification/overview/ | quote: "MCP Transport: Platforms MUST include a meta object containing request metadata" | type: official
- [C15] A2A v1.0.1 GitHub tag 页正文列出 spec 级 bugfix（版本冲突证据，单独记录）| src: https://github.com/a2aproject/A2A/releases/tag/v1.0.1 | quote: "1.0.1 (2026-05-26) Bug Fixes: spec: prefer application/a2a+json in HTTP binding (#1753); spec: recent transcoding-related error changes (#1627); TaskStatus values in the specification (#1801)" | type: official

## conflicts
- A2A 版本：站上规范标注 1.0.0（另一工人记录，2026-08-27 加入 AAIF），但 github.com/a2aproject/A2A 存在 v1.0.1 tag（页内日期 2026-05-26，发布显示 28 May，a2a-bot 发布）且正文明确含 spec 变更（C15）。不裁决。

## gaps
- IBM Agent Communication Protocol (ACP)：已查页面（ucp.dev 首页/spec/core-concepts、adk.dev/a2a、adk.dev/mcp-tools、adk.dev/ag-ui、ai.google.dev function-calling、a2a-and-mcp 页）均无提及；站内检索亦无 Google 官方文档命中。
- Zed Agent Client Protocol (ACP)：同上，已查页面未提及；仅 discuss.ai.google.dev 论坛用户帖提及把 Antigravity agy CLI 包成 ACP server（非官方文档）。
- Gemini API 文档已查页（function-calling）未提及 A2A/AG-UI/UCP；Vertex AI Agent Engine（cloud.google.com）有 A2A 文档但未逐页取原句。

## leads
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/create-an-a2a-agent （Vertex/Gemini Enterprise Agent Platform 原生 A2A 支持）
- https://adk.dev/integrations/ 中有 A2UI（Agent-to-UI）集成条目；https://ucp.dev/2026-04-08/specification/checkout-a2a/ 为 UCP checkout 的 A2A binding 细节页
- UCP GitHub 仓库 https://github.com/Universal-Commerce-Protocol/ucp（非 github.com/google 命名空间）
