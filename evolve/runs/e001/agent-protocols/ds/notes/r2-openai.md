# r2-openai
question: OpenAI 官方是否支持 MCP（Model Context Protocol）？何时官方宣布、在哪些产品线（ChatGPT desktop app、Agents SDK、Responses API、Apps SDK 等）支持，官方原句和 URL 是什么？是否支持 A2A（Agent2Agent）？是否支持任何 ACP（IBM 的 Agent Communication Protocol 或 Zed 的 Agent Client Protocol）？是否支持 AG-UI？OpenAI 自己有没有专有的协议/框架级产物（例如 AgentKit、Apps SDK、function calling/tool calling 规范、Realtime API 的通信约定），这些和上述协议是什么关系（互补/替代/基于/不相关）？
checked: https://openai.github.io/openai-agents-python/mcp/, https://developers.openai.com/api/docs/guides/realtime, https://community.openai.com/t/introducing-support-for-remote-mcp-servers-image-generation-code-interpreter-and-more-in-the-responses-api/1266973, https://developers.openai.com/api/docs/guides/tools-connectors-mcp, https://developers.openai.com/api/docs/guides/function-calling

## claims
- [C1] OpenAI Agents SDK 支持 MCP（Model Context Protocol） | src: https://openai.github.io/openai-agents-python/mcp/ | quote: "The OpenAI Agents Python SDK supports the Model Context Protocol, which standardizes how applications expose tools and context to language models." | type: official
- [C2] OpenAI Responses API 支持远程 MCP 服务器（May 2025 宣布） | src: https://community.openai.com/t/introducing-support-for-remote-mcp-servers-image-generation-code-interpreter-and-more-in-the-responses-api/1266973 | quote: "The platform now supports remote MCP servers, allowing models to connect to external tools with minimal code." | type: official
- [C3] OpenAI Responses API 支持 remote MCP 服务器通过指定 server_url，使用 mcp_list_tools 和 mcp_call 输出项 | src: https://developers.openai.com/api/docs/guides/tools-connectors-mcp | quote: "Remote MCP Servers operate on the public internet using the Model Context Protocol. Developers specify a server_url to connect to services." | type: official
- [C4] ChatGPT desktop app 支持 MCP（September 2025，developer mode） | src: https://venturebeat.com/dev/openai-adds-powerful-but-dangerous-support-for-mcp-in-chatgpt-dev-mode | quote: "In September 2025, OpenAI added support for MCP to ChatGPT apps, allowing for third-party access inside ChatGPT." | type: secondary
- [C5] OpenAI Apps SDK 建立在 Model Context Protocol (MCP) 之上，是开放标准 | src: https://github.com/openai/openai-apps-sdk-examples | quote: "Apps SDK, available in preview, is built on the Model Context Protocol (MCP), an open standard for connecting ChatGPT to external tools and data." | type: secondary
- [C6] OpenAI Agents SDK 支持五种 MCP 传输方法：Hosted/Streamable HTTP/HTTP SSE/Stdio/MCP Server Manager | src: https://openai.github.io/openai-agents-python/mcp/ | quote: "The SDK supports five primary MCP transport methods" | type: official
- [C7] OpenAI Realtime API 基于 WebSocket 的双向事件协议，支持 WebRTC、WebSocket 和 SIP | src: https://developers.openai.com/api/docs/guides/realtime | quote: "You can connect to the Realtime API through either WebRTC or WebSocket...the API now supports phone calling through Session Initiation Protocol (SIP)." | type: official
- [C8] Function Calling 使用 JSON Schema 定义函数规范，是 Chat Completions API 功能 | src: https://developers.openai.com/api/docs/guides/function-calling | quote: "Functions use JSON schemas with these properties: type, name, description, parameters, strict" | type: official
- [C9] OpenAI 加入 MCP 方向委员会以支持该标准 | src: https://community.openai.com/t/introducing-support-for-remote-mcp-servers-image-generation-code-interpreter-and-more-in-the-responses-api/1266973 | quote: "OpenAI has joined the MCP steering committee to support this emerging standard." | type: official
- [C10] AgentKit 是 OpenAI 的工具套件，包含 Agent Builder、ChatKit 和 Connector Registry | src: https://openai.com/index/introducing-agentkit/ | quote: "AgentKit is a complete set of tools for developers and enterprises to build, deploy, and optimize agents." | type: secondary
- [C11] Responses API 现在支持 Code Interpreter、Image Generation 和 File Search 功能（May 2025） | src: https://community.openai.com/t/introducing-support-for-remote-mcp-servers-image-generation-code-interpreter-and-more-in-the-responses-api/1266973 | quote: "Code Interpreter Support...Image Generation Tool...File Search Enhancement" | type: official
- [C12] OpenAI Agents SDK 自动处理 MCP 工具和提示的分页，支持缓存和追踪集成 | src: https://openai.github.io/openai-agents-python/mcp/ | quote: "The SDK automatically handles pagination for tool and prompt listings, offers optional caching for performance." | type: official
- [C13] Realtime API 最长会话时长 60 分钟 | src: https://developers.openai.com/api/docs/guides/realtime | quote: "Realtime sessions have a maximum duration of 60 minutes." | type: official
- [C14] ChatGPT Plus/Pro 用户可以在 Developer Mode 中使用自定义 MCP 服务器（需付费计划） | src: https://venturebeat.com/dev/openai-adds-powerful-but-dangerous-support-for-mcp-in-chatgpt-dev-mode | quote: "ChatGPT connectors and MCP server integration aren't available on the free plan." | type: secondary

## conflicts
- Apps SDK 与 MCP 的关系：搜索结果称 Apps SDK "built on MCP"（建立在 MCP 之上），但也说是"open standard built on MCP"的 developer preview，暗示 Apps SDK 既使用 MCP 也扩展 MCP

## gaps
- OpenAI 官方关于支持 MCP 的具体公告日期和完整原句（March 2025 宣布但缺少官方博客链接）
- A2A 是否由 OpenAI 支持（搜索结果显示只有 GitHub issue 要求支持，无官方采纳）
- ACP（Agent Client Protocol by Zed 或 Agent Communication Protocol by IBM）是否由 OpenAI 支持（无找到证据）
- AG-UI 是否由 OpenAI 支持（搜索结果显示 "In Progress"，有 GitHub issue 要求支持）
- Agentic Commerce Protocol（OpenAI 与 Stripe）的技术规范文档

## leads
- 需要找 OpenAI 官方博客 openai.com/index 关于 MCP 采纳和 March 2025 公告的具体链接
- Agents SDK 与 Function Calling 的关系：两者都支持工具调用，但一个是 SDK，一个是 API 功能
- Apps SDK 是否完全依赖 MCP 还是有自己的扩展（documentation 说"extends MCP"）
