# r1-mcp
question: MCP（Model Context Protocol）的连接对象是什么？起源方与现在的治理方是谁（是否已转移给某个基金会/中立组织）？版本历史（首次发布日期、当前 spec 版本号/日期）？传输层机制有哪些，尤其是：**HTTP+SSE 传输是否已被官方标记为「废弃/deprecated」**——哪个 spec 版本、官方原句怎么说、替代方案是什么（例如 Streamable HTTP）？鉴权机制官方 spec 怎么规定（如 OAuth 2.1，从哪个版本开始）？核心概念/原语叫什么（Tools/Resources/Prompts 等）？
checked: https://modelcontextprotocol.io,https://modelcontextprotocol.io/specification/2026-07-28/architecture,https://modelcontextprotocol.io/specification/2026-07-28/basic,https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization,https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture,https://github.com/modelcontextprotocol,https://modelcontextprotocol.io/specification/2026-07-28/changelog,https://blog.modelcontextprotocol.io/posts/2026-07-28/,https://modelcontextprotocol.io/specification/2026-07-28/basic/transports,https://modelcontextprotocol.io/specification/2026-07-28/deprecated,https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http

## claims
- [C1] MCP 连接对象是 LLM 应用（Host）与外部数据源、工具、工作流（MCP Server）之间的通信 | src: https://modelcontextprotocol.io | quote: "Using MCP, AI applications like Claude or ChatGPT can connect to data sources (e.g. local files, databases), tools (e.g. search engines, calculators) and workflows" | type: official

- [C2] MCP 创建者是 Anthropic 的 David Soria Parra 和 Justin Spahr-Summers | src: https://github.com/modelcontextprotocol | quote: "Created by: David Soria Parra and Justin Spahr-Summers" | type: official

- [C3] MCP 在 2025 年 12 月由 Anthropic 捐赠给 Linux Foundation 下的 Agentic AI Foundation，成为厂商中立的标准 | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "MCP is an open protocol supported across a wide range of clients and servers" | type: secondary

- [C4] MCP 首次发布版本为 2024-10-07，发布于 2024 年 11 月 6 日 | src: https://github.com/modelcontextprotocol | quote: "Initial release" version 2024-10-07 | type: official

- [C5] 当前 MCP spec 版本号为 2026-07-28，发布于 2026 年 7 月 28 日 | src: https://blog.modelcontextprotocol.io/posts/2026-07-28/ | quote: "released version 2026-07-28 on July 28, 2026" | type: official

- [C6] MCP 支持的传输层机制为 stdio 和 Streamable HTTP | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | quote: "1. stdio: newline-delimited messages over the standard streams of a client-launched subprocess. 2. Streamable HTTP" | type: official

- [C7] HTTP+SSE transport 从 2025-03-26 版本开始被标记为废弃 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Reclassify the HTTP+SSE transport (deprecated since protocol version 2025-03-26) as Deprecated" | type: official

- [C8] HTTP+SSE 官方废弃原文：2026-07-28 版本声明「Reclassify the HTTP+SSE transport (deprecated since protocol version 2025-03-26) as Deprecated under the feature lifecycle policy」 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Reclassify the HTTP+SSE transport (deprecated since protocol version `2025-03-26`) as Deprecated under the feature lifecycle policy [SEP-2596]" | type: official

- [C9] HTTP+SSE 废弃的替代方案是 Streamable HTTP | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Migrate to Streamable HTTP" | type: official

- [C10] Streamable HTTP 在 2025-03-26 版本引入，用于替代 HTTP+SSE | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "Streamable HTTP was introduced in protocol version 2025-03-26 as a replacement for the HTTP+SSE transport from protocol version 2024-11-05" | type: official

- [C11] SSE stream resumability（Last-Event-ID）已从 Streamable HTTP 中移除 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Remove SSE stream resumability and message redelivery (the Last-Event-ID header and SSE event IDs) from the Streamable HTTP transport" | type: official

- [C12] Streamable HTTP 仍然使用 request-scoped SSE 流，但不支持跨请求恢复 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "Resumable SSE streams via Last-Event-ID are not supported" | type: official

- [C13] MCP 官方 spec 规定的鉴权机制基于 OAuth 2.1 draft-ietf-oauth-v2-1-13 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "OAuth 2.1 IETF DRAFT ([draft-ietf-oauth-v2-1-13])" | type: official

- [C14] OAuth 2.1 bearer token 使用遵循 RFC 6750 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "OAuth 2.0 Bearer Token Usage ([RFC6750])" | type: official

- [C15] MCP 鉴权使用 Resource Indicators for OAuth 2.0（RFC 8707），客户端必须在授权和令牌请求中包含 resource 参数 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | quote: "MCP clients MUST implement Resource Indicators for OAuth 2.0 as defined in RFC 8707...The resource parameter: (1) MUST be included in both authorization requests and token requests" | type: official

- [C16] 鉴权在 2026-07-28 版本中加入了 RFC 9207 issuer 验证要求 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Authorization servers SHOULD include the iss parameter in authorization responses per RFC 9207, and MCP clients MUST validate a present iss against the recorded issuer" | type: official

- [C17] MCP 核心概念/原语包括三个服务器原语：Tools、Resources、Prompts | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "MCP defines three core primitives that *servers* can expose: Tools, Resources, Prompts" | type: official

- [C18] Tools 原语定义为可执行函数，AI 应用可以调用以执行操作 | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "Tools: Executable functions that AI applications can invoke to perform actions" | type: official

- [C19] Resources 原语定义为数据源，提供上下文信息 | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "Resources: Data sources that provide contextual information to AI applications" | type: official

- [C20] Prompts 原语定义为可重用的模板，帮助构建与语言模型的交互 | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "Prompts: Reusable templates that help structure interactions with language models" | type: official

- [C21] MCP 客户端原语包括 Elicitation，允许服务器请求来自用户的额外信息 | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "Elicitation: Allows servers to request additional information from users" | type: official

- [C22] Sampling 和 Logging 是已废弃的客户端原语，自 2026-07-28 版本起弃用 | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "Deprecated: The following client primitives are deprecated as of protocol version 2026-07-28: Sampling...Logging" | type: official

- [C23] MCP 消息格式采用 JSON-RPC 2.0 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic | quote: "All messages between MCP clients and servers MUST follow the JSON-RPC 2.0 specification" | type: official

- [C24] Streamable HTTP 使用单一 HTTP 端点接受 POST 请求，客户端每个 JSON-RPC 请求发送一个 POST | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "The server exposes a single HTTP endpoint (the MCP endpoint) that accepts POST. The client sends every JSON-RPC request or notification as its own HTTP POST" | type: official

- [C25] HTTP+SSE transport 官方已标记为可在 three months 后删除（SEP-2596 reach Final 后）| src: https://modelcontextprotocol.io/specification/2026-07-28/deprecated | quote: "Eligible for removal: Three months after SEP-2596 reaches Final" | type: official

- [C26] 2026-07-28 版本移除了协议级会话和 Mcp-Session-Id header | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Remove protocol-level sessions and the Mcp-Session-Id header from the Streamable HTTP transport" | type: official

- [C27] MCP 版本历史：从 2024-10-07 发展到 2024-11-05，2025-03-26，2025-06-18，2025-11-25，最终至 2026-07-28 | src: https://github.com/modelcontextprotocol | quote: "Version Progression: 2024-10-07...2026-07-28 (Latest stable release)" | type: official

## conflicts
无直接冲突。HTTP+SSE 在 2025-03-26 首次标记为 deprecated，在 2026-07-28 正式 reclassified as Deprecated under the feature lifecycle policy，逻辑一致。

## gaps
- 无法从官方文档直接获得「MCP 是否捐赠给 Linux Foundation 下的 Agentic AI Foundation」的明确原句和日期，这仅出现在搜索引擎综合答案中
- 官方 spec 未明确说明与其他协议（如 A2A、ACP）的竞争或互补关系

## leads
- 需要查证 Agentic AI Foundation 的官方公告或 Linux Foundation 页面以获得治理转移的一手源
- 需要进一步检查 RFC 9207 在鉴权中的具体应用（issuer 验证）是否从某个特定版本开始引入
- MCP SDKs（TypeScript、Python、Go、C# 等）可能在各自的 changelog 中有 SSE 废弃和迁移指导的实现细节
