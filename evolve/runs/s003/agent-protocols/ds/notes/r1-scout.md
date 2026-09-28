# r1-scout
question: 在 MCP / A2A / IBM ACP / Zed ACP / AG-UI 范围内，找用户会踩的坑与网格里还没有的相邻协议/厂商变体；只产出已打开过的官方入口 URL。
checked: https://openai.github.io/openai-agents-python/mcp/, https://developers.openai.com/apps-sdk, https://platform.claude.com/docs/en/agents-and-tools/mcp-connector, https://a2a-protocol.org/latest/, https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp, https://learn.microsoft.com/en-us/agent-framework/journey/agent-to-agent, https://ai.google.dev/gemini-api/docs/function-calling, https://agentcommunicationprotocol.dev/introduction/welcome, https://a2ui.org/, https://www.utcp.io/, https://agent-network-protocol.com/, https://modelcontextprotocol.io/extensions/apps

## claims
- [C1] OpenAI Agents Python SDK 原生支持 MCP，四种集成：HostedMCPTool（Responses API 代调）、MCPServerStreamableHttp、MCPServerSse、MCPServerStdio | src: https://openai.github.io/openai-agents-python/mcp/ | quote: 「The Agents Python SDK understands multiple MCP transports. This lets you reuse existing MCP servers or build your own」 | type: official
- [C2] SSE 传输弃用是官方文档原文，非二手传言 | src: https://openai.github.io/openai-agents-python/mcp/ | quote: 「The MCP project has deprecated the Server-Sent Events transport. Prefer Streamable HTTP or stdio for new integrations and keep SSE only for legacy servers.」 | type: official
- [C3] developers.openai.com/apps-sdk 现在落地为「Plugins」文档集（疑似改名），插件=skills+MCP server+可选 UI；还有一页「Submit your Claude Code plugin to OpenAI」 | src: https://developers.openai.com/apps-sdk | quote: 「Build and publish plugins with skills, MCP servers, and optional UI.」 | type: official
- [C4] Anthropic Messages API 的 MCP connector 是 beta（header `mcp-client-2025-11-20`，另有 `mcp-client-2026-09-15` 可钉工具列表）；只支持 tool calls；仅远程 HTTP | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: 「only tool calls are currently supported」「The server must be publicly exposed through HTTP (supports both Streamable HTTP and SSE transports). Local STDIO servers cannot be connected directly.」平台表：Amazon Bedrock / Google Cloud = not available | type: official
- [C5] A2A 官方定位与 MCP 互补，且明确「not a replacement」 | src: https://a2a-protocol.org/latest/ | quote: 「MCP is for agent-to-tool communication」「A2A is for agent-to-agent communication」「Not a replacement for MCP」 | type: official
- [C6] A2A 治理叙述：正文「originally developed by Google and donated to the Linux Foundation」，但页顶 banner「A2A joins the Agentic AI Foundation」(blog 2026-08-27)——归属口径可能已变 | src: https://a2a-protocol.org/latest/ | quote: 「A2A was originally developed by Google and donated to the Linux Foundation.」 | type: official
- [C7] Copilot Studio 支持 MCP 但仅限 tools 和 resources，且需开 generative orchestration | src: https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp | quote: 「Copilot Studio currently supports MCP tools and resources.」「You must turn on generative orchestration to use MCP.」（ms.date 2026-08-26） | type: official
- [C8] Microsoft Agent Framework 内置 A2A 客户端与托管 | src: https://learn.microsoft.com/en-us/agent-framework/journey/agent-to-agent | quote: 「Agent Framework provides an A2A agent service for calling remote agents and A2A hosting for exposing agents.」 | type: official
- [C9] Gemini Interactions API 支持远程 MCP：tool type `"mcp_server"`；两个坑：仅 Streamable HTTP、server 名不能含 `-` | src: https://ai.google.dev/gemini-api/docs/function-calling | quote: 「Remote MCP only works with Streamable HTTP servers. SSE (Server-Sent Events) servers are not supported.」「MCP server names should not include the `-` character.」 | type: official
- [C10] IBM ACP 已并入 A2A——重大坑：再写 ACP-IBM 当活跃独立协议会过时 | src: https://agentcommunicationprotocol.dev/introduction/welcome | quote: 「ACP is now part of A2A under the Linux Foundation!」（附 migration guide 链接） | type: official
- [C11] A2UI 是独立规范（Google 创建、Apache 2.0、CopilotKit 参与），当前 v0.9.1、v1.0 候选；与 AG-UI 不是同一物——官方建议用 AG-UI 做 transport harness | src: https://a2ui.org/ | quote: 「A2UI enables AI agents to generate rich, interactive user interfaces that render natively across web, mobile, and desktop—without executing arbitrary code.」「Scaffold an AG-UI app or harness for your agent framework, then enable A2UI rendering」 | type: official
- [C12] MCP Apps 是 MCP 官方扩展（非独立协议），MCP-UI 是其实现生态里的社区包；UTCP（v1.1）与 ANP（1.1 分层栈：did:wba/WNS/messaging/payment）各自是独立规范 | src: https://modelcontextprotocol.io/extensions/apps ; https://www.utcp.io/ ; https://agent-network-protocol.com/ | quote: 「MCP Apps is an extension to the core MCP specification. Host support varies by client.」/「UTCP is a lightweight, secure, and scalable standard that enables AI agents and applications to discover and call tools directly using their native protocols - no wrapper servers required.」/「ANP is organized as a layered protocol suite」 | type: official

## conflicts
- 无真正冲突。注意点：a2a-protocol.org 同页并存「donated to the Linux Foundation」与 banner「joins the Agentic AI Foundation」，引用治理归属前先确认最新口径。

## gaps
- Anthropic 官方是否点名 A2A / AG-UI / ACP：打开的 MCP connector 页未提及；未翻其他 Anthropic 页面。
- 两个 ACP（IBM/Zed）在任何官方页同时出现并消歧：未找到；IBM ACP 欢迎页未提 Zed ACP。
- OpenAI 官方是否支持 A2A（区别于 MCP）：未验证。
- Copilot Studio「SSE 2025-08 后不再支持」只见于搜索摘要（mcp-add-existing-server-to-agent 页），本人未打开。
- NLIP、e2b Agent Protocol：未打开官方页，不能确认是独立规范——未确认，不要升格。

## leads
- https://openai.github.io/openai-agents-python/mcp/ — OpenAI 格主入口：hosted vs 本地传输、审批、mcp 包 v1/v2 兼容矩阵；下一轮问 Responses API hosted MCP 的限制。
- https://developers.openai.com/apps-sdk — Apps SDK 是否已改名 Plugins？与 MCP Apps 扩展的关系。
- https://platform.claude.com/docs/en/agents-and-tools/mcp-connector — Anthropic 格：beta header 演进、tools-only、Bedrock/Google Cloud 不可用；再查 code.claude.com/docs/en/mcp 与 connectors 页是否点名其他协议。
- https://a2a-protocol.org/latest/ — A2A 格：spec 1.0 三种绑定（JSON-RPC/gRPC/REST）、AAIF 归属公告。
- https://ai.google.dev/gemini-api/docs/function-calling — Google 格：Remote MCP 的 `mcp_server` 字段表与命名/传输坑；可再开 google.github.io/adk-docs 查 ADK 的 A2A/MCP。
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp + https://learn.microsoft.com/en-us/agent-framework/journey/agent-to-agent — Microsoft 格两条线：Copilot Studio MCP（含内置 MCP 目录页）与 Agent Framework A2A；未验证 Semantic Kernel 独立文档是否仍存活。
- https://agentcommunicationprotocol.dev/introduction/welcome — 坑：IBM ACP 已并入 A2A，网格该标「superseded/merged」；页内 migration guide 链接可追。
- https://a2ui.org/ — 升格候选 A2UI：全名 Agent-driven interfaces 协议，独立 spec，别把 A2UI/AG-UI 混为一谈。
- https://www.utcp.io/ 与 https://agent-network-protocol.com/ — 升格候选 UTCP v1.1、ANP 1.1：均确认是独立规范站。
- https://modelcontextprotocol.io/extensions/apps — MCP Apps=官方扩展（spec 在 apps.extensions.modelcontextprotocol.io），MCP-UI(mcpui.dev) 是社区实现：升格应为「MCP 扩展」而非并列协议。
