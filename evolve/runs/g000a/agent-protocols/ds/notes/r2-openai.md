# r2-openai
question: OpenAI 官方现在支持 MCP、A2A、IBM 的 Agent Communication Protocol、Zed 的 Agent Client Protocol、AG-UI 到哪一步；自家被叫做 ACP 的东西到底是不是前两个 ACP。
checked: https://developers.openai.com/plugins/concepts/mcp-server, https://developers.openai.com/apps-sdk, https://developers.openai.com/commerce, https://developers.openai.com/commerce.md, https://developers.openai.com/commerce/guides/get-started, https://developers.openai.com/commerce/guides/key-concepts.md, https://www.agenticcommerce.dev/, https://github.com/agentic-commerce-protocol/agentic-commerce-protocol, https://learn.chatgpt.com/docs/extend/mcp, https://developers.openai.com/api/docs/guides/tools-connectors-mcp.md, https://developers.openai.com/api/docs/guides/agents-api/tools/mcp.md

## claims
- [C1] OpenAI.MCP：插件文档把 MCP 定义为连接 AI client 与外部工具/数据的开放规范。 | src: https://developers.openai.com/plugins/concepts/mcp-server | quote: "The Model Context Protocol (MCP) is an open specification for connecting AI clients to external tools and data." | type: official
- [C2] OpenAI.MCP：插件里的 MCP server 可选，用于读实时信息、执行动作或接入其他服务。 | src: https://developers.openai.com/plugins/concepts/mcp-server | quote: "A plugin can include an MCP server when it needs to read live information, take actions, or integrate with another service." | type: official
- [C3] OpenAI.MCP：插件 MCP server 可暴露 Tools、Resources、Prompts、Instructions。 | src: https://developers.openai.com/plugins/concepts/mcp-server | quote: "An MCP server can expose: Tools: Functions the model can call with structured inputs. Resources: Data or content the client can read. Prompts: Reusable prompt templates. Instructions: Server-wide guidance for using its capabilities." | type: official
- [C4] OpenAI.MCP：生产插件 MCP 要求稳定 HTTPS 上的 streamable HTTP。 | src: https://developers.openai.com/plugins/concepts/mcp-server | quote: "Deploy production MCP servers at stable HTTPS endpoints using the streamable HTTP transport." | type: official
- [C5] OpenAI.MCP：Responses API 的 MCP 接入使用 tool type mcp。 | src: https://developers.openai.com/api/docs/guides/tools-connectors-mcp.md | quote: "Use the mcp tool type in the Responses API." | type: official
- [C6] OpenAI.MCP：Responses 的远程 MCP 传输是 Streamable HTTP 或 HTTP/SSE。 | src: https://developers.openai.com/api/docs/guides/tools-connectors-mcp.md | quote: "The Responses API works with remote MCP servers that support either the Streamable HTTP or the HTTP/SSE transport protocols." | type: official
- [C7] OpenAI.MCP：Responses 列出工具时产出 type mcp_list_tools。 | src: https://developers.openai.com/api/docs/guides/tools-connectors-mcp.md | quote: "If successful in retrieving the list of tools, a new mcp_list_tools output item will appear in the model response output." | type: official
- [C8] OpenAI.MCP：Responses 执行工具时产出 type mcp_call。 | src: https://developers.openai.com/api/docs/guides/tools-connectors-mcp.md | quote: "If the model decides to call one of the available tools from the MCP server, you will also find a mcp_call output" | type: official
- [C9] OpenAI.MCP：Agents API 自己发现并调用 MCP，应用不必逐次处理。 | src: https://developers.openai.com/api/docs/guides/agents-api/tools/mcp.md | quote: "The Agents API discovers the tools, calls the server, and returns results to the agent. Your application does not need to handle each call." | type: official
- [C10] OpenAI.MCP：Agents API 的 HTTP MCP 写入 agent.tools，type 为 mcp，transport.type 为 http；省略 connection_origin 时由 OpenAI 连。 | src: https://developers.openai.com/api/docs/guides/agents-api/tools/mcp.md | quote: "Add an HTTP MCP server to agent.tools. The server must be reachable from OpenAI." | type: official
- [C11] OpenAI.MCP：Agents API 的 stdio MCP 跑在 session environment；environment.type 取 self_hosted 或 openai_hosted。 | src: https://developers.openai.com/api/docs/guides/agents-api/tools/mcp.md | quote: "Set the session's environment.type to self_hosted or openai_hosted." | type: official
- [C12] OpenAI.MCP：ChatGPT 桌面、Codex CLI、IDE 扩展支持 MCP，并共用同一 Codex host 配置。 | src: https://learn.chatgpt.com/docs/extend/mcp | quote: "The ChatGPT desktop app, Codex CLI, and IDE extension support MCP servers and share MCP configuration for the same Codex host." | type: official
- [C13] OpenAI.MCP：Codex host 支持 STDIO 与 Streamable HTTP（bearer、OAuth）。 | src: https://learn.chatgpt.com/docs/extend/mcp | quote: "STDIO servers: Servers that run as a local process (started by a command). Streamable HTTP servers: Servers that you access at an address." | type: official
- [C14] OpenAI.variant 全称是 Agentic Commerce Protocol (ACP)，连接买家、其 AI agent 与商家以完成购买。 | src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol | quote: "The Agentic Commerce Protocol (ACP) is an interaction model and open standard for connecting buyers, their AI agents, and businesses to complete purchases seamlessly." | type: official
- [C15] OpenAI.variant：该规范由 OpenAI 与 Stripe 维护，状态 beta。 | src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol | quote: "The specification is maintained by OpenAI and Stripe and is currently in beta." | type: official
- [C16] OpenAI.variant 版本：仓库 spec 已发布目录 2026-04-17，注释含 Cart、feed、orders、authentication 与 MCP。 | src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol | quote: "2026-04-17/ # Cart, feed, orders, authentication, and MCP" | type: official
- [C17] OpenAI.variant 通信边（协议站）：买家、AI agents、businesses 之间的程序化商务流。 | src: https://www.agenticcommerce.dev/ | quote: "An open standard for programmatic commerce flows between buyers, AI agents, and businesses." | type: official
- [C18] OpenAI.variant：任何 AI agent 都可调用已启用 ACP 的 checkout；OpenAI 是第一个用 ChatGPT 实现 ACP 的 AI 平台。 | src: https://www.agenticcommerce.dev/ | quote: "Any AI agent can call an ACP-enabled checkout." | type: official
- [C19] OpenAI.variant：Stripe 与 OpenAI 制定 ACP，作为 agent 与 business 交易的共同语言。 | src: https://www.agenticcommerce.dev/ | quote: "Stripe and OpenAI developed the Agentic Commerce Protocol to define a common language for how agents and businesses transact" | type: official
- [C20] OpenAI.variant：checkout 配置可用传统 API 或 MCP 发布，ACP 与 MCP 被写成可并存的接入方式。 | src: https://www.agenticcommerce.dev/ | quote: "Publish your checkout configuration with a traditional API or MCP." | type: official
- [C21] OpenAI.variant：Apache 2.0。 | src: https://www.agenticcommerce.dev/ | quote: "ACP is open source and community-designed under the Apache 2.0 license." | type: official
- [C22] OpenAI 文档把 ACP 当作 Agentic Commerce Protocol 的简称，入门是向 OpenAI 交结构化商品 feed。 | src: https://developers.openai.com/commerce/guides/get-started | quote: "Start your ACP integration by sharing a structured product feed with OpenAI." | type: official
- [C23] OpenAI.variant 通信边（产品文档）：ChatGPT 作为顾客的 AI agent，调用商家的 ACP 端点创建或更新 checkout session。 | src: https://developers.openai.com/commerce/guides/key-concepts.md | quote: "ChatGPT calls the merchant’s Agentic Commerce Protocol endpoints to create or update a checkout session, and securely share information." | type: official
- [C24] OpenAI.variant 支付边：OpenAI 把支付细节交给商家或其 PSP；OpenAI 不是 merchant of record。 | src: https://developers.openai.com/commerce/guides/key-concepts.md | quote: "OpenAI is not the merchant of record in the Agentic Commerce Protocol." | type: official
- [C25] OpenAI.variant：Delegated Payment Spec 的接收方是 merchant 或其指定 PSP。 | src: https://developers.openai.com/commerce/guides/key-concepts.md | quote: "The Delegated Payment Spec allows OpenAI to securely share payment details with the merchant or its designated payment service provider (PSP)." | type: official
- [C26] 协议站补句：OpenAI 是第一个用 ChatGPT 实现 ACP 的平台。 | src: https://www.agenticcommerce.dev/ | quote: "OpenAI is the first AI platform to implement ACP with ChatGPT" | type: official

## conflicts
- 谁能用 ACP：协议站说任何企业或 AI 平台都可实现规范，且任何 AI agent 可调用 ACP checkout；OpenAI Get Started 写 ChatGPT 商品 feed 入驻仅限获批合作方。未裁决。 src: https://www.agenticcommerce.dev/ quote: "Any business or AI platform can implement the ACP spec to participate in agentic commerce" ; src: https://developers.openai.com/commerce/guides/get-started quote: "Onboarding product feeds in ChatGPT is currently available to approved partners."
- 结账代理是谁：协议站写 buyers / AI agents / businesses，并称任何 agent 可调用；OpenAI key concepts 把代理写成 ChatGPT，端点在商家。未裁决。 src: https://www.agenticcommerce.dev/ quote: "Any AI agent can call an ACP-enabled checkout." ; src: https://developers.openai.com/commerce/guides/key-concepts.md quote: "The Agentic Checkout Spec enables ChatGPT to act as the customer’s AI agent"

## gaps
- OpenAI.A2A = ∅。已搜 site:developers.openai.com、site:openai.com 的 A2A / Agent2Agent / agent-to-agent；命中仅为 community.openai.com 讨论帖，无 openai.com 或 developers.openai.com 官方产品页。未用新闻填。
- OpenAI.ACP-IBM = ∅。已搜 site:developers.openai.com 与 site:openai.com 的 "Agent Communication Protocol"；无官方页。
- OpenAI.ACP-Zed = ∅。已搜 site:developers.openai.com、site:openai.com、site:github.com/openai 的 "Agent Client Protocol" / agent-client-protocol；无 OpenAI 官方实现页。
- OpenAI.AG-UI = ∅。已搜 site:developers.openai.com 与 site:openai.com 的 AG-UI / ag-ui；无官方页。
- Responses API 未被打开的官方页叫做互操作协议。已搜 site:developers.openai.com "Responses API" interoperability；命中把它叫做 API primitive / agentic loop（https://developers.openai.com/api/docs/guides/migrate-to-responses 未在本轮 web_fetch）。
- 已打开页没有「ACP 不是 IBM Agent Communication Protocol，也不是 Zed Agent Client Protocol」的明示否定句。不同一协议是据全称与通信边推断：商务购买（买家的 agent↔商家/PSP），不是 agent↔agent，也不是 editor↔coding agent。
- 搜索索引曾给 https://developers.openai.com/commerce 一句 “connective layer between merchants and ChatGPT users”；web_fetch 该 URL 与 https://developers.openai.com/commerce.md 只有文档地图，该句未复核，不入库。
- https://developers.openai.com/apps-sdk 打开后标题是 Plugins，未见独立 Apps SDK 正文。

## leads
- Realtime MCP 页未打开：https://developers.openai.com/api/docs/guides/realtime-mcp （搜索摘要有 type mcp、server_url、connector_id）。
- Codex App Server 是另一套双向 JSON-RPC，英文原文页本轮未打开：https://developers.openai.com/codex/app-server 。
- ACP 仓库 spec/2026-04-17 注释含 MCP，OpenAPI 正文未打开。
