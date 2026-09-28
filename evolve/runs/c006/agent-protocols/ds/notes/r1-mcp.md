# r1-mcp
question: MCP（Model Context Protocol）的官方 spec 现状：连接面、治理、传输、核心抽象、鉴权、版本时间线、大厂采用、代表实现。
checked: https://modelcontextprotocol.io/specification, https://modelcontextprotocol.io/specification/2025-06-18/basic/transports, https://modelcontextprotocol.io/specification/2025-03-26/basic/transports, https://modelcontextprotocol.io/specification/versioning, https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization, https://modelcontextprotocol.io/community/governance, https://modelcontextprotocol.io/specification/2025-06-18/changelog, https://modelcontextprotocol.io/specification/2025-11-25/changelog, https://modelcontextprotocol.io/specification/2026-07-28/changelog, https://www.anthropic.com/news/model-context-protocol, https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation, https://github.com/modelcontextprotocol, https://openai.github.io/openai-agents-python/mcp/

## claims

D1 连接面
- [C1] MCP 连接 LLM 应用与外部数据/工具；JSON-RPC 2.0 消息在三方间通信：Host（发起连接的 LLM 应用）、Client（host 内连接器）、Server（提供上下文与能力） | src: https://modelcontextprotocol.io/specification | quote: "Hosts: LLM applications that initiate connections" | type: official
- [C2] 自我定位类比 LSP：为 AI 应用生态标准化上下文/工具接入 | src: https://modelcontextprotocol.io/specification | quote: "MCP takes some inspiration from the Language Server Protocol" | type: official

D2 发起方/治理
- [C3] Anthropic 于 2024-11-25 宣布并开源 MCP（含 spec、SDK、Claude Desktop 支持与预置 server 仓库） | src: https://www.anthropic.com/news/model-context-protocol | quote: "we're open-sourcing the Model Context Protocol (MCP), a new standard for connecting AI assistants" | type: official
- [C4] 2025-12-09 Linux Foundation 宣布成立 Agentic AI Foundation（AAIF），创始项目为 MCP（Anthropic）、goose（Block）、AGENTS.md（OpenAI） | src: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | quote: "announced the formation of the Agentic AI Foundation (AAIF), and founding contributions of three leading projects" | type: official
- [C5] MCP 法律实体为 LF Projects 旗下 series；治理变更需 LF Projects, LLC 批准 | src: https://modelcontextprotocol.io/community/governance | quote: "Model Context Protocol has been established as Model Context Protocol a Series of LF Projects, LLC" | type: official
- [C6] 治理层级 Contributors→Maintainers→Core Maintainers→Lead Maintainers(BDFL)，三者组成 Steering Group；现任 Lead Maintainers：David Soria Parra、Den Delimarsky；变更走 SEP（Specification Enhancement Proposal）流程 | src: https://modelcontextprotocol.io/community/governance | quote: "Lead Maintainers hold final authority and can veto any decision by Core Maintainers or Maintainers" | type: official
- [C7] License：代码与 spec 均 Apache-2.0，文档 CC BY 4.0 | src: https://modelcontextprotocol.io/community/governance | quote: "all code and specification contributions to the project must be made using the Apache License, Version 2.0" | type: official

D3 传输与格式
- [C8] 标准传输仅两种：stdio（客户端拉子进程）与 Streamable HTTP；可插拔 custom transports 允许 | src: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports | quote: "The protocol currently defines two standard transport mechanisms for client-server communication" | type: official
- [C9] Streamable HTTP：单一 "MCP endpoint" 同时支持 POST+GET；可选以 SSE 流式下发多条消息；带 Mcp-Session-Id 会话头（注：会话机制 2026-07-28 已移除） | src: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports | quote: "The server MUST provide a single HTTP endpoint path (hereafter referred to as the MCP endpoint) that supports both POST and GET methods." | type: official
- [C10] Streamable HTTP 自 spec 2025-03-26 引入，取代 2024-11-05 的 HTTP+SSE 传输 | src: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports | quote: "This replaces the HTTP+SSE transport from protocol version 2024-11-05." | type: official
- [C11] HTTP+SSE 在 2025-03-26 spec 中即被称 deprecated；旧版仍可用：spec 给出兼容流程（服务器并存新旧端点；客户端先 POST 探测失败再回退 GET+endpoint 事件） | src: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports | quote: "Clients and servers can maintain backwards compatibility with the deprecated HTTP+SSE transport" | type: official
- [C12] 2026-07-28 把 HTTP+SSE 正式列入 feature-lifecycle Deprecated；deprecated 特性至少在 spec 中保留 12 个月才可移除 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Reclassify the HTTP+SSE transport (deprecated since protocol version 2025-03-26) as Deprecated under the feature lifecycle policy" | type: official
- [C13] HTTP 传输要求 MCP-Protocol-Version header（2025-06-18 起 MUST；未带时服务器 SHOULD 按 2025-03-26 处理） | src: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports | quote: "the client MUST include the MCP-Protocol-Version: <protocol-version> HTTP header on all subsequent requests" | type: official
- [C14] 「SSE 废弃」的精确含义：废弃的是独立的 HTTP+SSE 传输（GET 开 SSE 流＋独立 POST 端点）；SSE 作为 Streamable HTTP 内部可选流式机制仍存在 | src: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports | quote: "Server can optionally make use of Server-Sent Events (SSE) to stream multiple server messages." | type: official

D4 核心抽象
- [C15] 服务端 primitives：Resources（上下文数据）、Prompts（模板消息/工作流）、Tools（模型可执行函数） | src: https://modelcontextprotocol.io/specification | quote: "Tools: Functions for the AI model to execute" | type: official
- [C16] 客户端能力：Elicitation（2025-06-18 新增，server 向用户请求补充信息）；Roots/Sampling/Logging 在 2026-07-28 被 Deprecate | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Deprecate the Roots, Sampling, and Logging features" | type: official
- [C17] 核心外有 opt-in Extensions：Tasks（异步长任务）、MCP Apps（内嵌 UI）、Skills over MCP | src: https://modelcontextprotocol.io/specification | quote: "MCP defines optional extensions that add modular, specialized, or experimental functionality." | type: official

D5 鉴权
- [C18] 鉴权 OPTIONAL，仅约束 HTTP 传输；基于 OAuth 2.1 草案（draft-ietf-oauth-v2-1-13）+ RFC8414 + RFC7591 + RFC9728 的子集 | src: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization | quote: "Authorization is OPTIONAL for MCP implementations." | type: official
- [C19] 角色：MCP server = OAuth 2.1 resource server；MCP client = OAuth 2.1 client；AS 可与 RS 同体或独立 | src: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization | quote: "A protected MCP server acts as an OAuth 2.1 resource server" | type: official
- [C20] 强制项：server MUST 实现 RFC9728 Protected Resource Metadata 并在 401 上用 WWW-Authenticate 指示；client MUST 用 RFC8414 发现 AS、MUST 实现 RFC8707 resource 参数、MUST 实现 PKCE；双方 SHOULD 支持 RFC7591 DCR | src: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization | quote: "MCP servers MUST implement OAuth 2.0 Protected Resource Metadata (RFC9728)." | type: official
- [C21] 2026-07-28：DCR（RFC7591）被 Deprecate，改用 Client ID Metadata Documents | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Deprecate the OAuth 2.0 Dynamic Client Registration Protocol (RFC7591) as a client registration mechanism in favor of Client ID Metadata Documents" | type: official

D6 版本与稳定性
- [C22] 版本号 = YYYY-MM-DD，标记最近一次向后不兼容变更日期；当前版本 2026-07-28 | src: https://modelcontextprotocol.io/specification/versioning | quote: "The current protocol version is 2026-07-28" | type: official
- [C23] 版本链：2024-11-05（首版）→ 2025-03-26 → 2025-06-18 → 2025-11-25 → 2026-07-28（各 changelog 以 "previous revision" 互链） | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "since the previous revision, 2025-11-25" | type: official
- [C24] 2025-06-18 主要变更：移除 JSON-RPC batching、加 structured tool output、MCP server 归类 OAuth Resource Server、新增 elicitation、强制 MCP-Protocol-Version header | src: https://modelcontextprotocol.io/specification/2025-06-18/changelog | quote: "Classify MCP servers as OAuth Resource Servers" | type: official
- [C25] 2025-11-25：OIDC Discovery 1.0、Client ID Metadata Documents、experimental tasks、治理结构正式化（SEP-932） | src: https://modelcontextprotocol.io/specification/2025-11-25/changelog | quote: "Enhance authorization server discovery with support for OpenID Connect Discovery 1.0" | type: official
- [C26] 2026-07-28：去握手化——移除 initialize/initialized 握手与 Mcp-Session-Id，改为每请求 _meta 携带 protocolVersion/clientCapabilities；新增 MUST 实现的 server/discover；subscriptions/listen 取代 GET 流 | src: https://modelcontextprotocol.io/specification/2026-07-28/changelog | quote: "Make MCP stateless: remove the initialize/notifications/initialized handshake." | type: official

D7 大厂支持
- [C27] LF 口径：MCP 已被 Claude、Cursor、Microsoft Copilot、Gemini、VS Code、ChatGPT 采用；10,000+ 已发布 server | src: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | quote: "adopted by Claude, Cursor, Microsoft Copilot, Gemini, VS Code, ChatGPT and other popular AI platforms" | type: official
- [C28] AAIF platinum 成员：AWS、Anthropic、Block、Bloomberg、Cloudflare、Google、Microsoft、OpenAI | src: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | quote: "Platinum members of the AAIF include Amazon Web Services, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft and OpenAI." | type: official
- [C29] OpenAI 官方 Agents SDK 支持 MCP 三种传输，其文档亦注明 SSE 传输已废弃 | src: https://openai.github.io/openai-agents-python/mcp/ | quote: "The MCP project has deprecated the Server-Sent Events transport." | type: official
- [C30] 发布时早期采用者：Block、Apollo 已集成；Zed、Replit、Codeium、Sourcegraph 在接入 | src: https://www.anthropic.com/news/model-context-protocol | quote: "Early adopters like Block and Apollo have integrated MCP into their systems" | type: official

D8 典型实现
- [C31] 官方 SDK 覆盖 10 语言：TS/Python/Java/Kotlin/C#/Go/PHP/Ruby/Rust/Swift；csharp-sdk「Maintained in collaboration with Microsoft」、go-sdk 与 Google 共建 | src: https://github.com/modelcontextprotocol | quote: "Maintained in collaboration with Microsoft." | type: official
- [C32] 代表仓库：modelcontextprotocol（spec+docs）、servers（官方 server 集）、inspector（可视化调试）、conformance（一致性测试）、ext-auth/ext-apps/ext-skills（扩展） | src: https://github.com/modelcontextprotocol | quote: "Visual testing tool for MCP servers" | type: official
- [C33] 规模（Anthropic 口径，2025-12）：Python+TS SDK 月下载 97M+；官方社区 Registry 已上线 | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "97M+ monthly SDK downloads across Python and TypeScript" | type: official

## conflicts
- Anthropic 2025-12-09 博客称「November 25th spec release introduced many new features, including asynchronous operations, statelessness, server identity」（anthropic.com/news/donating-the-model-context-protocol-…），但 spec changelog 显示真正移除 initialize 握手/协议级 session（即无状态化）发生在 2026-07-28；2025-11-25 changelog 无对应条目。博客措辞与 spec 记录不一致，以 spec changelog 为准。

## gaps
- 2024-11-05 spec 版本号与 2024-11-25 公开宣布日的关系官方未明示（transports 页仅以 protocol version 2024-11-05 引用）。
- openai.com 主站 WebFetch 403，未取到 OpenAI 自家公告原文；OpenAI 采用依赖 LF 新闻稿+Agents SDK 文档。
- HTTP+SSE 的确切移除日期未查（deprecated registry 页未打开）。
- 未逐家核 Microsoft/Google 官方文档级采用细节（Copilot/Gemini 集成形态）。

## leads
- MCP Registry（官方 server 注册表）可作 D8/生态补充。
- ext-apps（MCP Apps 扩展）与 OpenAI Apps SDK 的关系值得查（grid 候选行）。
- /specification/2026-07-28/deprecated 注册表给出各 deprecated 特性的计划移除时间。
