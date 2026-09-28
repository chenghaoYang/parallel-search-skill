# r1-mcp
question: Model Context Protocol 官方规范里，角色、原语、传输（尤其 SSE 是否废弃）、状态、发现、鉴权、治理与版本、以及它自己怎么说和其他 agent 协议的关系。
checked: https://modelcontextprotocol.io/specification/2026-07-28, https://modelcontextprotocol.io/specification/2026-07-28/architecture, https://modelcontextprotocol.io/specification/2026-07-28/basic/index, https://modelcontextprotocol.io/specification/2026-07-28/server, https://modelcontextprotocol.io/specification/2026-07-28/changelog, https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning, https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning, https://modelcontextprotocol.io/specification/2026-07-28/deprecated, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http, https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization, https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/authorization-server-discovery, https://modelcontextprotocol.io/specification/2025-11-25/changelog, https://modelcontextprotocol.io/specification/2025-06-18/changelog, https://modelcontextprotocol.io/specification/2025-03-26/changelog, https://modelcontextprotocol.io/specification/2025-03-26/basic/transports, https://modelcontextprotocol.io/specification/2024-11-05/basic/transports, https://modelcontextprotocol.io/community/governance, https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/

## claims
- [C1] D1 Host 是发起连接的 LLM 应用。 | src: https://modelcontextprotocol.io/specification/2026-07-28 | quote: "Hosts: LLM applications that initiate connections" | type: official
- [C2] D1 每个 client 只连一个 server。 | src: https://modelcontextprotocol.io/specification/2026-07-28/architecture | quote: "communicates with exactly one server" | type: official
- [C4] D1 完整对话留在 host。 | src: https://modelcontextprotocol.io/specification/2026-07-28/architecture | quote: "Full conversation history stays with the host" | type: official
- [C5] D4 2026-07-28 起协议无状态。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/index | quote: "(MCP) is a stateless protocol" | type: official
- [C6] D2 Tools 是给模型执行的函数。 | src: https://modelcontextprotocol.io/specification/2026-07-28/server | quote: "Tools: Executable functions that allow models to perform actions or retrieve information" | type: official
- [C7] D2 客户端特性含 elicitation、sampling、roots。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/index | quote: "Elicitation, sampling and root directory lists provided by clients" | type: official
- [C8] D2/D4 tasks 移出核心，扩展 id 为 io.modelcontextprotocol/tasks。 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "out of the core protocol and into an official extension (`io.modelcontextprotocol/tasks`)" | type: official
- [C10] D2 2026-07-28 弃用 Roots、Sampling、Logging。 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Deprecate the Roots, Sampling, and Logging features" | type: official
- [C11] D3 2024-11-05 的 HTTP+SSE 要求两个端点。 | src: https://modelcontextprotocol.io/specification/2024-11-05/basic/transports | quote: "The server MUST provide two endpoints:" | type: official
- [C12] D3 2025-03-26 changelog 用 Replaced，不用 deprecated。 | src: https://modelcontextprotocol.io/specification/2025-03-26/changelog | quote: "Replaced the previous HTTP+SSE transport" | type: official
- [C13] D3 同版正文已称 HTTP+SSE deprecated。 | src: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports | quote: "the deprecated HTTP+SSE transport" | type: official
- [C14] D3 changelog 最早写 deprecated 是 2026-07-28，并写 since 2025-03-26。2025-06-18 与 2025-11-25 全文无此词。 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "deprecated since protocol version 2025-03-26" | type: official
- [C18] D3 HTTP+SSE 尚未按弃用政策 Removed。 | src: https://modelcontextprotocol.io/specification/2026-07-28/deprecated | quote: "No features have been removed under this policy yet." | type: official
- [C17] D3 现行单一 MCP endpoint 接受 POST。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "a single HTTP endpoint (the MCP endpoint) that accepts POST." | type: official
- [C21] D3 现行响应仍可是按请求的 SSE 流。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "a Server-Sent Events (SSE) stream scoped to that request" | type: official
- [C22] D3 stdio 仍在，客户端启动服务器子进程。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio | quote: "the client launches the MCP server as a subprocess." | type: official
- [C23] D4 删除协议级 session 与 Mcp-Session-Id。 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Remove protocol-level sessions and the Mcp-Session-Id header" | type: official
- [C24] D5 server/discover 为服务器 MUST。 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "servers MUST implement this RPC" | type: official
- [C25] D6 鉴权 OPTIONAL。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "Authorization is OPTIONAL for MCP implementations." | type: official
- [C26] D6 STDIO 不遵循该 HTTP 鉴权，凭证来自环境。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "retrieve credentials from the environment." | type: official
- [C27] D6 OAuth 2.1 自规范 2025-03-26 写入。 | src: https://modelcontextprotocol.io/specification/2025-03-26/changelog | quote: "authorization framework based on OAuth 2.1" | type: official
- [C35] D6 WWW-Authenticate 用参数 resource_metadata 指向元数据 URL。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/authorization-server-discovery | quote: "WWW-Authenticate HTTP header under `resource_metadata`" | type: official
- [C29] D6 访问令牌放 Authorization: Bearer。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "Authorization: Bearer <access-token>" | type: official
- [C30] D6 2026-07-28 弃用 RFC7591 DCR。 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Deprecate the OAuth 2.0 Dynamic Client Registration Protocol (RFC7591)" | type: official
- [C31] D7 版本号为 YYYY-MM-DD；当前 2026-07-28。 | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning | quote: "version identifiers following the format YYYY-MM-DD" | type: official
- [C28] D7 现维护实体写为 LF Projects, LLC。该页未出现 Anthropic。 | src: https://modelcontextprotocol.io/community/governance | quote: "a Series of LF Projects, LLC" | type: official
- [C33] D7 博客：Anthropic 捐给 Linux Foundation 下的 AAIF。 | src: https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/ | quote: "Anthropic is donating MCP to the Agentic AI Foundation, a directed fund under the Linux Foundation." | type: secondary
- [C34] D9 架构页与 2026-07-28 changelog 各开两次，加首页、basic/index、三份旧 changelog：无 A2A/ACP/AG-UI。类比是 LSP。 | src: https://modelcontextprotocol.io/specification/2026-07-28 | quote: "MCP takes some inspiration from the Language Server Protocol" | type: official

## conflicts
- C12 的 2025-03-26 changelog 只写 Replaced；C13 同版正文写 deprecated；C14 写成 since 2025-03-26。不裁决。changelog 里该词最早是 2026-07-28。
- 首页 “Clients may offer” 下只列 Elicitation；C7 仍列 sampling 与 roots；C10 弃用它们。changelog 另有 “remain fully functional during the deprecation window”。不裁决。
- learn/versioning：“at least twelve months, or at least ninety days”。注册表 HTTP+SSE：“Three months after SEP-2596 reaches Final”。不裁决。

## gaps
- D8 未填。未打开 OpenAI / Anthropic / Google / Microsoft 自己的文档。
- D9 仅 C34 所列页面，不是全站。
- 未打开 https://modelcontextprotocol.io/legacy/concepts/transports （无原句，不记冲突）。未打开 PKCE 子页，不写 S256。未核 SEP-2596 是否 Final。
## leads
- 博客：“co-founded by Anthropic, Block and OpenAI”。治理页 Lead：David Soria Parra、Den Delimarsky。
- “Removal of the GET stream endpoint.”
