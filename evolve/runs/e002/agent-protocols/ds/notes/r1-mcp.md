# r1-mcp
question: MCP（Model Context Protocol）官方规范说了什么——它管什么交互、拓扑（谁是host/client/server）、传输层（尤其：SSE 传输是否已被废弃，官方原话和版本号是什么）、消息格式、鉴权机制、会话状态归属、版本规则（当前最新版本号/日期）、治理方式（是 Anthropic 独家维护还是有开放治理/steering committee）、官方列出的采用者/SDK、以及规范里是否提到与 A2A/ACP/AG-UI 等其他协议的关系。
checked: https://modelcontextprotocol.io, https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture, https://github.com/modelcontextprotocol, https://modelcontextprotocol.io/specification/2026-07-28/basic, https://modelcontextprotocol.io/specification/2026-07-28/architecture, https://modelcontextprotocol.io/docs/2026-07-28/sdk, https://modelcontextprotocol.io/specification/2026-07-28/deprecated, https://modelcontextprotocol.io/community/contributing, https://modelcontextprotocol.io/community/governance, https://github.com/modelcontextprotocol/specification/releases

## claims

### 管什么交互
- [C1] MCP 管理三类服务端原语（primitives）：Tools（可执行函数）、Resources（数据源）、Prompts（交互模板） | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "MCP defines three core primitives that *servers* can expose: **Tools**: Executable functions... **Resources**: Data sources... **Prompts**: Reusable templates"

- [C2] MCP 管理客户端原语：Elicitation（服务端请求用户输入）；Sampling、Logging 在 2026-07-28 版本已弃用 | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "**Deprecated**: The following client primitives are deprecated as of protocol version `2026-07-28`. **Sampling**... **Logging**..."

- [C3] MCP 支持 Notifications（实时更新通知）和 Extensions（如 Tasks 扩展用于长运行操作） | src: https://modelcontextprotocol.io/specification/2026-07-28/basic | quote: "MCP uses [JSON-RPC 2.0]... The protocol supports real-time notifications... Extensions are always opt-in"

### 拓扑
- [C4] MCP 采用 Host-Client-Server 三角关系，其中 Host 创建多个 Client，每个 Client 与一个 Server 建立 1:1 专属连接 | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "MCP follows a client-server architecture where an MCP host... establishes connections to one or more MCP servers. The MCP host... creates one MCP client for each MCP server."

- [C5] Host 是 AI 应用（如 Claude Desktop、VSCode），Client 是 Host 内部组件维护连接，Server 是提供上下文的程序 | src: https://modelcontextprotocol.io/specification/2026-07-28/architecture | quote: "**Hosts**: LLM applications that initiate connections; **Clients**: Connectors within the host application; **Servers**: Services that provide context and capabilities"

- [C6] 本地 Server 使用 Stdio transport（单客户端），远程 Server 使用 Streamable HTTP transport（多客户端） | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "Local MCP servers that use the STDIO transport typically serve a single MCP client, whereas remote MCP servers that use the Streamable HTTP transport will typically serve many MCP clients."

### 传输层
- [C7] MCP 支持两种标准传输：Stdio（本地进程通信）和 Streamable HTTP（远程服务器通信，带可选 SSE） | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "**Stdio transport**: Uses standard input/output streams... **Streamable HTTP transport**: Uses HTTP POST for client-to-server messages with optional Server-Sent Events for streaming capabilities."

- [C8] HTTP+SSE transport 在版本 2025-03-26 被标记为 Deprecated，迁移路径是使用 Streamable HTTP | src: https://modelcontextprotocol.io/specification/2026-07-28/deprecated | quote: "[HTTP+SSE transport](/specification/2024-11-05/basic/transports#http-with-sse)... Deprecated in: `2025-03-26`... [Streamable HTTP](/specification/2026-07-28/basic/transports/streamable-http)"

- [C9] SSE 在当前版本中作为 Streamable HTTP transport 的"可选"特性保留，而非完全移除 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | quote: "replies arrive as a JSON object or a request-scoped SSE stream"

- [C10] 弃用 SEP：SEP-2596，最早移除时间为"Three months after SEP-2596 reaches Final" | src: https://modelcontextprotocol.io/specification/2026-07-28/deprecated | quote: "Deprecation SEP: [SEP-2596]... Earliest removal: Three months after SEP-2596 reaches Final"

### 消息格式
- [C11] MCP 使用 JSON-RPC 2.0 作为底层 RPC 协议 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic | quote: "All messages between MCP clients and servers **MUST** follow the [JSON-RPC 2.0](https://www.jsonrpc.org/specification) specification."

- [C12] 所有 MCP 消息包含结构化的 `_meta` 字段，每个请求携带 protocolVersion、clientInfo、clientCapabilities | src: https://modelcontextprotocol.io/specification/2026-07-28/basic | quote: "Client requests carry the following `io.modelcontextprotocol/*` fields in `_meta`... `io.modelcontextprotocol/protocolVersion`... `io.modelcontextprotocol/clientInfo`... `io.modelcontextprotocol/clientCapabilities`"

### 鉴权机制
- [C13] Stdio transport 从环境变量读取凭证，HTTP transport 支持 bearer tokens、API keys、custom headers，推荐使用 OAuth 获取认证令牌 | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "supports standard HTTP authentication methods including bearer tokens, API keys, and custom headers. MCP recommends using OAuth to obtain authentication tokens."

- [C14] MCP 提供了专门的 Authorization 框架用于 HTTP transport | src: https://modelcontextprotocol.io/specification/2026-07-28/basic | quote: "MCP provides an [Authorization](/specification/2026-07-28/basic/authorization) framework for use with HTTP."

### 会话状态归属
- [C15] MCP 在版本 2026-07-28 是无状态协议（stateless），每个请求自包含所有必要信息，服务端不依赖连接状态 | src: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: "MCP is a stateless protocol: all the information needed to process a request is contained in the request itself."

- [C16] 版本 2025-11-25 及更早版本使用有状态的 initialize 握手管理会话生命周期，当前版本改为 server/discover 发现机制 | src: https://modelcontextprotocol.io/docs/2025-11-25/learn/architecture | quote: "MCP is a stateful protocol that requires lifecycle management" vs. 2026-07-28 "stateless protocol"

### 版本规则
- [C17] 当前官方最新稳定版本号为 2026-07-28，发布日期为 2026 年 7 月 28 日 | src: https://github.com/modelcontextprotocol/specification/releases | quote: "2026-07-28 (Stable): This marks 'the **stable release** of the `2026-07-28` revision of the Model Context Protocol.'"

- [C18] MCP 采用日期格式的版本号（YYYY-MM-DD），支持向后兼容的协议版本协商，客户端在每个请求中声明协议版本 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic | quote: "`io.modelcontextprotocol/protocolVersion`: Protocol version for this request (e.g., `\"2026-07-28\"`)"

### 治理方式
- [C19] MCP 由 Linux Foundation（作为 "Model Context Protocol a Series of LF Projects, LLC"）主持，不是 Anthropic 独家维护 | src: https://modelcontextprotocol.io/community/governance | quote: "Model Context Protocol has been established as **Model Context Protocol a Series of LF Projects, LLC**... Policies applicable to Model Context Protocol... are located at https://www.lfprojects.org/policies/"

- [C20] 项目采用正式的分层治理模型，包含 Lead Maintainers（BDFL 角色）、Core Maintainers、Maintainers、Contributors 四级结构，决策由 Core Maintainer Group 每两周进行一次 | src: https://modelcontextprotocol.io/community/governance | quote: "**Lead Maintainers (BDFL)**: Final decision authority; **Core Maintainers**: Overall project direction; **Maintainers**: Working Groups, SDKs, components... The Core Maintainer group meets every two weeks to discuss and vote on proposals"

- [C21] Lead Maintainers 为 David Soria Parra 和 Den Delimarsky，核心决策委员会（MCP Steering Group）由 Maintainers、Core Maintainers 和 Lead Maintainers 组成 | src: https://modelcontextprotocol.io/community/governance | quote: "**Current Lead Maintainers**: David Soria Parra, Den Delimarsky"

### 采用者与 SDK
- [C22] 官方列出的采用者（AI 应用和开发工具）包括：Claude、ChatGPT、Visual Studio Code、Cursor、MCPJam | src: https://modelcontextprotocol.io | quote: "AI assistants like [Claude](https://claude.com/docs/connectors/building) and [ChatGPT](https://developers.openai.com/api/docs/mcp/), development tools like [Visual Studio Code]... [Cursor]... [MCPJam]... all support MCP"

- [C23] 官方提供 10 种语言 SDK，分为三个 tier：Tier 1（TypeScript、Python、C#、Go、Rust）功能完整，Tier 2（Java、Ruby）支持核心功能，Tier 3（Swift、PHP、Kotlin）实验阶段 | src: https://modelcontextprotocol.io/docs/2026-07-28/sdk | quote: "**TypeScript**, **Python**, **C#**, **Go**, **Rust**... Tier 1... **Java**, **Ruby**... Tier 2... **Swift**, **PHP**, **Kotlin**... Tier 3"

### 与其他协议的关系
- [C24] 官方规范和文档中未明确提及与 A2A（Agent-to-Agent）、ACP（Anthropic Context Protocol）、ACP-IBM、ACP-Zed、AG-UI 等其他协议的关系或兼容性 | src: https://modelcontextprotocol.io/specification/2026-07-28, https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | quote: 未提及这些协议

## conflicts
- SSE 是否"已废弃"存在表述模糊性：C8 表明独立的 "HTTP+SSE transport" 作为一个完整协议绑定在 2025-03-26 被正式标记为 Deprecated，但 C9 表明 SSE 本身作为 Streamable HTTP 的流式响应选项仍被保留为可选特性。这是迁移（deprecated）而非完全移除（removed）。

## gaps
- 未找到 A2A、ACP、ACP-IBM、ACP-Zed、AG-UI 等协议在官方 MCP 文档中的明确提及或关系说明
- 未找到确切的"SEP-2596 reaches Final"的目标日期，无法精确计算 SSE 最早移除时间
- Streamable HTTP 中 SSE 作为"可选"特性的具体使用场景和弃用时间表未明确文档化

## leads
- SEP-2596 完整提案页面：https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2596
- 版本历史详细信息：https://github.com/modelcontextprotocol/specification/releases
- 维护者完整列表：https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/MAINTAINERS.md
