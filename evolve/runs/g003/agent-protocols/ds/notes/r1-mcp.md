# r1-mcp
question: Model Context Protocol（MCP）官方规范现在如何定义两端角色、核心对象、传输（尤其 HTTP+SSE 是否 deprecated/removed）、发现、会话生命周期、鉴权、规范版本与治理主体。
checked: https://modelcontextprotocol.io/specification/2026-07-28, https://modelcontextprotocol.io/specification/2026-07-28/architecture, https://modelcontextprotocol.io/specification/2026-07-28/changelog, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio, https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning, https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization, https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations, https://modelcontextprotocol.io/specification/2026-07-28/server/discover, https://modelcontextprotocol.io/specification/2026-07-28/server/tools, https://modelcontextprotocol.io/specification/2026-07-28/deprecated, https://modelcontextprotocol.io/specification/2025-03-26/changelog, https://modelcontextprotocol.io/specification/2025-03-26/basic/transports, https://modelcontextprotocol.io/specification/2024-11-05/basic/transports, https://modelcontextprotocol.io/community/governance, https://modelcontextprotocol.io/community/feature-lifecycle, https://modelcontextprotocol.io/llms.txt, https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/

## claims
- [C1] D1: 2026-07-28 角色是 Host、Client、Server，不是对等两端。 | src: https://modelcontextprotocol.io/specification/2026-07-28 | quote: "Hosts: LLM applications that initiate connections" | type: official
- [C2] D1: 每个 client 由 host 创建，且只连一个 server。 | src: https://modelcontextprotocol.io/specification/2026-07-28/architecture | quote: "communicates with exactly one server" | type: official
- [C3] D2: 架构把 resources、tools、prompts 称为 MCP primitives。 | src: https://modelcontextprotocol.io/specification/2026-07-28/architecture | quote: "Expose resources, tools and prompts via MCP primitives" | type: official
- [C6] D2: 2026-07-28 服务器不发起 JSON-RPC request，客户端不发 JSON-RPC response。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | quote: "servers do not initiate JSON-RPC requests and clients do not send JSON-RPC responses" | type: official
- [C7] D2: Tool 设计为 model-controlled，由语言模型发现并调用。 | src: https://modelcontextprotocol.io/specification/2026-07-28/server/tools | quote: "Tools in MCP are designed to be model-controlled" | type: official
- [C8] D3: 现行标准传输是 stdio 与 Streamable HTTP；后者一次 POST，应答为 JSON 或该请求的 SSE。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | quote: "replies arrive as a JSON object or a request-scoped SSE stream." | type: official
- [C9] D3: 客户端仍 MUST 支持 text/event-stream。SSE 应答帧未删除。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "text/event-stream (an SSE response stream). The client MUST support both." | type: official
- [C10] D3: 2024-11-05 将 HTTP with SSE 定为标准传输，服务器 MUST 提供两个端点。 | src: https://modelcontextprotocol.io/specification/2024-11-05/basic/transports | quote: "The server MUST provide two endpoints:" | type: official
- [C11] D3: 最早替换记录是 2025-03-26 changelog（上一版 2024-11-05），用词是 Replaced。 | src: https://modelcontextprotocol.io/specification/2025-03-26/changelog | quote: "Replaced the previous HTTP+SSE transport with a more flexible Streamable HTTP transport" | type: official
- [C12] D3: 同版传输页已称该传输 deprecated。 | src: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports | quote: "backwards compatibility with the deprecated HTTP+SSE transport" | type: official
- [C13] D3: 2026-07-28 称 HTTP+SSE 自 2025-03-26 起 deprecated，并列为 Deprecated。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "has been deprecated since protocol version 2025-03-26 and is classified as Deprecated" | type: official
- [C14] D3: 废弃表把 HTTP+SSE 的最早删除写成 SEP-2596 达 Final 后三个月。 | src: https://modelcontextprotocol.io/specification/2026-07-28/deprecated | quote: "Three months after SEP-2596 reaches Final" | type: official
- [C15] D3: 2026-07-28 的 Streamable HTTP 不再支持 Last-Event-ID 续传。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "Resumable SSE streams via Last-Event-ID are not supported." | type: official
- [C16] D4: 服务器 MUST 实现 server/discover。 | src: https://modelcontextprotocol.io/specification/2026-07-28/server/discover | quote: "Servers MUST implement it." | type: official
- [C17] D4: 工具发现方法是 tools/list。 | src: https://modelcontextprotocol.io/specification/2026-07-28/server/tools | quote: "To discover available tools, clients send a tools/list request." | type: official
- [C19] D5: 2026-07-28 没有协商握手。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning | quote: "There is no negotiation handshake." | type: official
- [C20] D5: 2026-07-28 changelog 删除协议级 session 与 Mcp-Session-Id。 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Remove protocol-level sessions and the Mcp-Session-Id header" | type: official
- [C21] D6: 鉴权 OPTIONAL。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "Authorization is OPTIONAL for MCP implementations." | type: official
- [C23] D6: 服务器 MUST 实现 RFC9728。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "MCP servers MUST implement OAuth 2.0 Protected Resource Metadata (RFC9728)." | type: official
- [C24] D6: 客户端 MUST 实现 PKCE。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations | quote: "MCP clients MUST implement PKCE" | type: official
- [C25] D6: Dynamic Client Registration 已废弃并仅为兼容保留。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "Dynamic Client Registration is deprecated and retained for backwards compatibility" | type: official
- [C26] D7: 版本页称 Modern 为修订 2026-07-28 及以后。 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning | quote: "revision 2026-07-28 and later" | type: official
- [C27] D8: 法律主体写为 LF Projects, LLC 的 series。 | src: https://modelcontextprotocol.io/community/governance | quote: "Model Context Protocol a Series of LF Projects, LLC" | type: official
- [C28] D8: 2025-12-09 Anthropic 把 MCP 捐给 Linux Foundation 下的 AAIF。 | src: https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/ | quote: "Anthropic is donating MCP to the Agentic AI Foundation, a directed fund under the Linux Foundation." | type: official
- [C29] D9: 规范自称连接 LLM 应用、外部数据源与 tools。 | src: https://modelcontextprotocol.io/specification/2026-07-28 | quote: "integration between LLM applications and external data sources and tools." | type: official

## conflicts
- SSE 用词未裁决。https://modelcontextprotocol.io/specification/2025-03-26/changelog ："Replaced the previous HTTP+SSE transport with a more flexible Streamable HTTP transport"。https://modelcontextprotocol.io/specification/2025-03-26/basic/transports ："backwards compatibility with the deprecated HTTP+SSE transport"。https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http ："deprecated since protocol version 2025-03-26 and is classified as Deprecated"。https://modelcontextprotocol.io/specification/2026-07-28/deprecated ："No features have been removed under this policy yet."
- 删除时点未裁决。https://modelcontextprotocol.io/community/feature-lifecycle ："at least twelve"，"not from the date the SEP reaches Final"。废弃表："Three months after SEP-2596 reaches Final"。

## gaps
- D9: llms.txt 与已打开的规范首页、架构、tools、changelog、治理、AAIF 博客无 A2A、AG-UI、Agent Client Protocol、Agent2Agent、ACP。无否定原句。
- 未打开 /specification/draft 与 SEP-2596。

## leads
- io.modelcontextprotocol/ui 是 MCP Apps，不是 AG-UI。
