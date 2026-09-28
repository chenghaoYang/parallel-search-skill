# r2-mcp-lifecycle
question: 核实 MCP 2026-07-28 版 changelog 里"eliminates the initialize/notifications/initialized handshake"这条说法的准确含义。是否等于"协议整体变成完全无状态"，还是"只是去掉了一个特定的握手步骤，但 Streamable HTTP 传输仍然靠 Mcp-Session-Id 之类的 header/机制维持会话概念"。
checked: https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning, https://modelcontextprotocol.io/specification/2026-07-28/changelog, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http

## claims
- [C1] MCP 2026-07-28 版本的核心设计目标是完全无状态，不仅消除 initialize/notifications/initialized 握手，还移除协议级别的会话概念 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Make MCP stateless: remove the `initialize`/`notifications/initialized` handshake." | type: official
- [C2] 协议移除了 Streamable HTTP 传输中的 Mcp-Session-Id header 和所有协议级别的会话机制 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Remove protocol-level sessions and the `Mcp-Session-Id` header from the Streamable HTTP transport." | type: official
- [C3] 每个请求都通过 _meta 字段独立携带其协议版本和客户端能力，而非通过握手协商 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Every request now carries its protocol version and client capabilities in `_meta` (`io.modelcontextprotocol/protocolVersion`, `io.modelcontextprotocol/clientCapabilities`)." | type: official
- [C4] 服务器无法依赖隐含的连接范围会话状态；需要维持跨调用状态时应使用服务器创建的显式句柄作为工具参数传递 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Servers that need cross-call state use explicit, server-minted handles passed as ordinary tool arguments." | type: official
- [C5] 2026-07-28 现代协议版本通过每个请求的 per-request metadata 传递版本、身份和能力，不存在协商握手 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning | quote: "There is no negotiation handshake. Every request carries its protocol version, and the server accepts or rejects each request independently." | type: official
- [C6] 现代 per-request metadata 的请求按无状态方式处理 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning | quote: "A request carrying modern per-request `_meta` is served statelessly according to this revision." | type: official
- [C7] 2025-03-26 到 2025-11-25 的旧版 Streamable HTTP 支持通过 Mcp-Session-Id header 分配会话，但 2026-07-28 版本不再支持这些机制 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "Protocol versions 2025-03-26 through 2025-11-25 also used the Streamable HTTP transport, but in a different shape: servers could assign a session via the Mcp-Session-Id header ... None of these mechanisms are part of this revision." | type: official
- [C8] 向后兼容时，2026-07-28 服务器接收旧客户端发送的 Mcp-Session-Id header 应忽略它，不创建也不回显会话 ID | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "An Mcp-Session-Id header on a request: ignore it, and do not mint or echo session IDs." | type: official

## conflicts

## gaps
- 未发现协议内其他隐性会话维持机制的文档

## leads
- 应用层状态维持的具体实现示例（工具句柄模式）在其他规范页面中可能有详细说明，但已超出本轮核查范围
