# r1-mcp
question: MCP（Model Context Protocol，Anthropic 发起）管什么、怎么传输、怎么鉴权、状态归属、谁治理、当前版本、谁在用。重点核实一个具体传闻：「MCP 的 SSE 传输已经废弃」是否属实——精确到版本号、修订日期、原句、替代方案叫什么名字。
checked: https://modelcontextprotocol.io,https://modelcontextprotocol.io/specification,https://modelcontextprotocol.io/specification/2026-07-28/architecture,https://modelcontextprotocol.io/specification/2026-07-28/basic,https://modelcontextprotocol.io/specification/2026-07-28/basic/transports,https://modelcontextprotocol.io/specification/2025-03-26/basic/transports,https://modelcontextprotocol.io/specification/2024-11-05/basic/transports,https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture,https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization,https://github.com/modelcontextprotocol

## claims
- [C1] MCP 是开源标准，用于 LLM 应用和外部系统集成 | src: https://modelcontextprotocol.io | quote: "MCP is an open-source standard for connecting AI applications to external systems." | type: official
- [C2] MCP 使用 JSON-RPC 2.0 消息格式，在协议层面与传输层无关 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic | quote: "All messages between MCP clients and servers MUST follow the JSON-RPC 2.0 specification." | type: official
- [C3] 2026-07-28 版本支持两个标准 transport：stdio 和 Streamable HTTP | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | quote: "The protocol currently defines two standard transport mechanisms for client-server communication: 1. stdio 2. Streamable HTTP" | type: official
- [C4] Streamable HTTP 替代了 2024-11-05 版本的 HTTP+SSE transport | src: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports | quote: "This replaces the HTTP+SSE transport from protocol version 2024-11-05." | type: official
- [C5] 2024-11-05 版本定义了 HTTP with Server-Sent Events (SSE) 作为 transport | src: https://modelcontextprotocol.io/specification/2024-11-05/basic/transports | quote: "MCP currently defines two standard transport mechanisms: 1. stdio 2. HTTP with Server-Sent Events (SSE)" | type: official
- [C6] Streamable HTTP transport 仍支持使用 SSE 进行流式传输 | src: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports | quote: "Server can optionally make use of Server-Sent Events (SSE) to stream multiple server messages." | type: official
- [C7] HTTP+SSE 旧 transport 的向后兼容性在 Streamable HTTP 中定义 | src: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports | quote: "Clients and servers can maintain backwards compatibility with the deprecated HTTP+SSE transport (from protocol version 2024-11-05)" | type: official
- [C8] 新 Streamable HTTP transport 与旧 HTTP+SSE transport 完全不同的架构 | src: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports | quote: "In the Streamable HTTP transport, the server operates as an independent process that can handle multiple client connections. This transport uses HTTP POST and GET requests." | type: official
- [C9] Streamable HTTP 替代方案在 2025-03-26 版本中引入 | src: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports | quote: "This replaces the HTTP+SSE transport from protocol version 2024-11-05. See the backwards compatibility guide below." | type: official
- [C10] MCP 是 stateless protocol，每个请求自包含所有必需的 metadata | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/index | quote: "Servers MUST NOT rely on prior requests over the same connection to establish context. Every request supplies this metadata in its _meta field." | type: official
- [C11] HTTP-based transports 的鉴权遵循 OAuth 2.1 规范，使用 Bearer token | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "MCP client MUST use the Authorization request header field: Authorization: Bearer <access-token>" | type: official
- [C12] STDIO transport 应从环境变量而非 HTTP header 获取凭证 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "Implementations using an STDIO transport SHOULD NOT follow this specification, and instead retrieve credentials from the environment." | type: official
- [C13] MCP 鉴权对 HTTP-based transports 为可选，对 STDIO transport 不适用 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "Authorization is OPTIONAL for MCP implementations. Implementations using an HTTP-based transport SHOULD conform to this specification." | type: official
- [C14] MCP 受 Language Server Protocol (LSP) 启发 | src: https://modelcontextprotocol.io/specification/2026-07-28 | quote: "MCP takes some inspiration from the Language Server Protocol, which standardizes how to add support for programming languages across a whole ecosystem." | type: official
- [C15] MCP 当前最新版本为 2026-07-28（July 28, 2026），标记为 stable release | src: https://github.com/modelcontextprotocol/specification/releases | quote: "2026-07-28 (July 28, 2026) - This marks the stable release of the 2026-07-28 revision." | type: official
- [C16] MCP 由 The Linux Foundation host，Anthropic 发起 | src: https://github.com/modelcontextprotocol | quote: "MCP is an open-source initiative hosted by The Linux Foundation that facilitates integration between LLM applications and external data sources." | type: official
- [C17] Claude、ChatGPT、VS Code、Cursor、MCPJam 等应用支持 MCP | src: https://modelcontextprotocol.io | quote: "AI assistants like Claude and ChatGPT, development tools like Visual Studio Code, Cursor, MCPJam, and many others all support MCP" | type: official
- [C18] 官方维护多个 SDK（TypeScript、Python 等）和 reference server implementations | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "MCP SDKs: SDKs for different programming languages that implement MCP. MCP Reference Server Implementations" | type: official
- [C19] 完全 SSE transport 在 2024-11-05 版本中的定义要求客户端建立 SSE 连接获取 endpoint 事件 | src: https://modelcontextprotocol.io/specification/2024-11-05/basic/transports | quote: "When a client connects, the server MUST send an endpoint event containing a URI for the client to use for sending messages." | type: official
- [C20] 新 Streamable HTTP 改进了旧 SSE transport 的缺陷：单一 MCP endpoint 支持 POST 和 GET | src: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports | quote: "The server MUST provide a single HTTP endpoint path (hereafter referred to as the MCP endpoint) that supports both POST and GET methods." | type: official

## conflicts
- [CF1] HTTP+SSE vs Streamable HTTP naming：官方文档在 2024-11-05 版本中称为「HTTP with Server-Sent Events」，在 2025-03-26 版本中改为「Streamable HTTP」。这两个名称指代不同的 protocol 版本，不是同一个 protocol 的别名。

## gaps
- SSE 传输在 2025-03-26 之后的具体折弃过程及时间表（是否完全移除还是仍可兼容）
- Streamable HTTP 相比 HTTP+SSE 的性能对比数据
- MCP 采用统计（部署数量、用户数）

## leads
- MCP 应用场景细节及各大 AI 厂商的集成现状应由专门的 scout worker 调研
- 考虑查看 MCP GitHub 仓库的具体 CHANGELOG 文件以获得更精确的版本发布时间表
- Streamable HTTP 在 resumability 和 session management 的改进是关键创新点，值得深挖
