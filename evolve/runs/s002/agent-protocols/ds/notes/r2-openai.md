# r2-openai
question: OpenAI 官方文档现在支持 MCP、A2A、IBM Agent Communication Protocol、Zed Agent Client Protocol、AG-UI 中的哪些？有没有自家协议或变体（Apps SDK、MCP Apps、function calling 是否被叫做协议）？给出 API/产品里的原名。
checked: https://developers.openai.com/api/docs/guides/tools-connectors-mcp, https://developers.openai.com/apps-sdk/concepts/mcp-server (内容现为 plugins/concepts/mcp-server), https://developers.openai.com/plugins/ (apps-sdk URL 落到此), https://developers.openai.com/llms.txt, https://developers.openai.com/commerce, https://developers.openai.com/commerce/guides/key-concepts.md, https://learn.chatgpt.com/docs/llms.txt (Codex docs), https://learn.chatgpt.com/docs/app-server, https://developers.openai.com/api/docs/guides/function-calling.md, https://openai.github.io/openai-agents-python/mcp/, https://github.com/openai/openai-agents-python/pull/1245

## claims
- [C1] Responses API 原生支持远程 MCP server：tools 数组里放 `{"type":"mcp","server_label","server_url","server_description","require_approval"}`，另有 `allowed_tools`、`authorization` 字段 | src: https://developers.openai.com/api/docs/guides/tools-connectors-mcp | quote: "Use the `mcp` tool type in the Responses API. Set `server_url` for a remote MCP server" | type: official
- [C2] Responses API 只接 Streamable HTTP 或 HTTP/SSE 的 MCP server | src: 同 C1 | quote: "The Responses API works with remote MCP servers that support either the Streamable HTTP or the HTTP/SSE transport protocols." | type: official
- [C3] MCP 在 Response output 里的 item 类型名：`mcp_list_tools`、`mcp_call`、`mcp_approval_request`、输入侧 `mcp_approval_response` | src: 同 C1 | quote: "which will create a `mcp_list_tools` output item" / `"type": "mcp_call"` / `"type": "mcp_approval_request"` | type: official
- [C4] OpenAI 自家 MCP 扩展「Secure MCP Tunnel」：`tunnel_id` 字段 + GitHub 仓库 openai/tunnel-client，接私网 MCP server | src: 同 C1 | quote: "Secure MCP Tunnel connects a local or private MCP server without exposing it to the public internet." | type: official
- [C5] `connector_id`（Dropbox/Gmail/Google Calendar 等 hosted connector）对 2026-09-01 之后发布的模型弃用 | src: 同 C1 | quote: "`connector_id` is deprecated for models released after September 1, 2026." | type: official
- [C6] Agents Python SDK 四种 MCP 接入：`HostedMCPTool`（托管）、`MCPServerStreamableHttp`、`MCPServerSse`、`MCPServerStdio`，另 `MCPServerManager` | src: https://openai.github.io/openai-agents-python/mcp/ | quote: "The Agents Python SDK understands multiple MCP transports." | type: official
- [C7] Agents SDK 依赖范围 `mcp>=1.19.0,<3`，兼容 MCP Python SDK v1 和 v2 | src: 同 C6 | quote: "The Agents SDK supports both major versions of the `mcp` Python package through the dependency range `mcp>=1.19.0,<3`." | type: official
- [C8] SDK 文档注明 MCP 项目已弃用 SSE transport | src: 同 C6 | quote: "The MCP project has deprecated the Server-Sent Events transport. Prefer Streamable HTTP or stdio" | type: official
- [C9] Codex 支持 MCP（docs 条目「Model Context Protocol — Give Codex access to third-party tools and context」）；原 `codex mcp-server` 已移除 | src: https://learn.chatgpt.com/docs/llms.txt | quote: "Codex MCP server removal: Migrate from the removed Codex MCP server to the app server" | type: official
- [C10] ChatGPT plugins / Apps SDK 文档树以 MCP server 为核心构件；docs 集合名仍为 "ChatGPT plugins and Apps SDK" | src: https://developers.openai.com/llms.txt + https://developers.openai.com/plugins/ | quote: "ChatGPT plugins and Apps SDK: Build plugins with MCP servers, tools, UI components" | type: official
- [C11] MCP Apps = ChatGPT 侧 UI 扩展机制：MCP server 可返回可选 UI resource | src: https://developers.openai.com/apps-sdk/concepts/mcp-server | quote: "An MCP server can also return an optional UI resource for clients that support MCP Apps" | type: official
- [C12] Codex app-server 有一个 OpenAI 扩展的 MCP 变体能力 `mcpServerOpenaiFormElicitation` | src: https://learn.chatgpt.com/docs/app-server | quote: "allow downstream MCP servers to send the OpenAI extended-form variant of `mcpServer/elicitation/request`" | type: official
- [C13] A2A：官方 SDK 明确不收。openai-agents-python PR #1245（A2A AgentCardBuilder）被 maintainer seratch 关闭（2025-07-25） | src: https://github.com/openai/openai-agents-python/pull/1245 | quote: "we don't have immediate plans to add A2A support to this SDK." | type: official
- [C14] 2025-11-06 同 PR maintainer 重申拒绝，建议社区自建 adapter | src: 同 C13 | quote: "we'd prefer to hold off on adding this adapter layer as part of the core SDK." | type: official
- [C15] OpenAI 自家协议：Agentic Commerce Protocol（ACP，与 Stripe 合作），文档树 developers.openai.com/commerce；下含 Agentic Checkout Spec、Delegated Payment Spec | src: https://developers.openai.com/commerce/guides/key-concepts.md | quote: "ChatGPT calls the merchant's Agentic Commerce Protocol endpoints" | type: official
- [C16] Delegated Payment 首个实现是 Stripe | src: 同 C15 | quote: "Stripe's Shared Payment Token is the first Delegated Payment Spec-compatible implementation" | type: official
- [C17] Codex 自家客户端协议 = "app-server protocol"：JSON-RPC 2.0 over stdio/ws/unix，方法如 `initialize`、`thread/start`、`turn/start`；实现开源在 openai/codex 仓库 codex-rs/app-server | src: https://learn.chatgpt.com/docs/app-server | quote: "Like MCP, `codex app-server` supports bidirectional communication using JSON-RPC 2.0 messages" | type: official
- [C18] function calling 不被称作协议：官方名 "Function calling (also known as tool calling)"，是一种 tool 类型（`"type":"function"`、输出 item `function_call`/`function_call_output`） | src: https://developers.openai.com/api/docs/guides/function-calling.md | quote: "Function calling (also known as tool calling) provides a powerful and flexible way for OpenAI models to interface with external systems" | type: official

## conflicts
- 无文档间矛盾。注意命名碰撞：OpenAI 文档里的 "ACP" 指自家 Agentic Commerce Protocol（C15），与 IBM ACP / Zed ACP 同名不同物；填矩阵时不要把 ACP 格标成"支持 IBM ACP"。

## gaps
- IBM Agent Communication Protocol：checked 的全部 URL + site 搜索均无提及（"ACP" 被自家 commerce 协议占用）。未敢写"不支持"，但无证据支持。
- Zed Agent Client Protocol：Codex 完整文档索引（learn.chatgpt.com/docs/llms.txt）无 ACP 条目；app-server 页只描述自家 JSON-RPC 协议。Codex-in-Zed 走第三方 adapter，非 OpenAI 文档内容。
- AG-UI：openai.github.io / developers.openai.com / learn.chatgpt.com / github.com/openai 的 site 搜索零命中；自家对应物是 ChatKit + MCP Apps UI（C11）。
- openai-agents-js（JS SDK）的 MCP 支持未单独核实，只查了 Python 版。
- Realtime API 的 MCP 页（/api/docs/guides/realtime-mcp）存在但未读正文。

## leads
- 社区 A2A adapter：github.com/prassanna-ravishankar/a2a-openai-agents（PyPI a2a-openai-agents）；maintainer 明确欢迎社区发布此类包。
- Zed/ACP adapter：github.com/agentclientprotocol/codex-acp（npm @agentclientprotocol/codex-acp，原 zed-industries/codex-acp 迁移至此）。
- WebMCP：Codex 文档有 "Site tools (WebMCP)" 页（learn.chatgpt.com/docs/webmcp.md），另一协议接入面。
- ChatKit（/api/docs/guides/chatkit）：OpenAI 自家可嵌入 agentic chat UI，AG-UI 的对应物。
