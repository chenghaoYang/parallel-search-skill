# r1-mcp-core
question: Model Context Protocol (MCP) 官方文档中，协议的定位/管辖层是什么（管的是谁和谁之间的交互）、核心抽象/第一公民概念叫什么（Tools/Resources/Prompts/Sampling 等字段名）、架构角色划分（Host/Client/Server）、传输方式有哪些（stdio、HTTP+SSE、Streamable HTTP）、以及「HTTP+SSE 传输是否已被废弃/替换」的官方原文表述（具体是哪个版本废弃、替换成什么、原句怎么说）、规范当前成熟度状态（是否 1.0/GA，是否有生产可用性警告）。
checked: https://modelcontextprotocol.io/specification/2026-07-28, https://modelcontextprotocol.io/specification/2026-07-28/architecture, https://modelcontextprotocol.io/specification/2026-07-28/basic, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports, https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx

## claims
- [C1] MCP 协议定位为在 LLM 应用（Host）、连接器（Client）、外部服务（Server）之间建立 JSON-RPC 2.0 消息通信 | src: https://modelcontextprotocol.io/specification/2026-07-28 | quote: "The protocol uses JSON-RPC 2.0 messages to establish communication between: Hosts: LLM applications that initiate connections, Clients: Connectors within the host application, Servers: Services that provide context and capabilities" | type: official

- [C2] 架构角色三分：Host（容器与协调者，创建和管理多个 Client 实例）、Client（与一个 Server 进行 1:1 通信）、Server（提供专门的上下文和能力） | src: https://modelcontextprotocol.io/specification/2026-07-28/architecture | quote: "The host process acts as the container and coordinator... Each client is created by the host and communicates with exactly one server... Servers provide specialized context and capabilities" | type: official

- [C3] 核心抽象/第一公民概念（Server 端）：Resources（上下文和数据）、Prompts（模板化消息和工作流）、Tools（AI 模型执行的函数）| src: https://modelcontextprotocol.io/specification/2026-07-28 | quote: "Servers offer any of the following features to clients: Resources: Context and data, for the user or the AI model to use, Prompts: Templated messages and workflows for users, Tools: Functions for the AI model to execute" | type: official

- [C4] 核心抽象/第一公民概念（Client 端）：Elicitation（Server 向 Client 发起的请求，获取额外信息） | src: https://modelcontextprotocol.io/specification/2026-07-28 | quote: "Clients may offer the following features to servers: Elicitation: Server-initiated requests for additional information from users" | type: official

- [C5] 标准传输方式一：stdio - 通过客户端启动的子进程的标准流进行换行符分隔的消息传输 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | quote: "[stdio](/specification/2026-07-28/basic/transports/stdio): newline-delimited messages over the standard streams of a client-launched subprocess" | type: official

- [C6] 标准传输方式二：Streamable HTTP - 每条消息都是一个 HTTP POST 到单一 MCP 端点；应答以 JSON 对象或 request-scoped SSE 流形式返回 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | quote: "[Streamable HTTP](/specification/2026-07-28/basic/transports/streamable-http): each message is an HTTP POST to a single MCP endpoint; replies arrive as a JSON object or a request-scoped SSE stream" | type: official

- [C7] HTTP+SSE 传输自协议版本 2025-03-26 以来已被软弃用（soft-deprecated），在 2026-07-28 中正式重新分类为"Deprecated"under feature lifecycle policy | src: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx | quote: "Reclassify the HTTP+SSE transport (deprecated since protocol version `2025-03-26`) as Deprecated under the feature lifecycle policy ([SEP-2596](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2596))" | type: official

- [C8] HTTP+SSE 传输的替换品为 Streamable HTTP，根据 changelog "Deprecated"部分的官方建议 | src: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx | quote: "Migrate to [Streamable HTTP](/specification/2026-07-28/basic/transports/streamable-http)" | type: official

- [C9] MCP 2026-07-28 规范被描述为"production-grade infrastructure"且已获得行业领导者（AWS、Google Cloud、Microsoft 等）确认为"ready for enterprise deployment" | src: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/blog/content/posts/2026-07-28-spec-ga/index.md | quote: "Industry leaders from AWS, Google Cloud, Microsoft, and others affirm the specification represents 'production-grade infrastructure' ready for enterprise deployment" | type: official

- [C10] 协议版本号 2026-07-28 是当前最新版本的规范，基于 TypeScript schema 作为权威来源 | src: https://modelcontextprotocol.io/specification/2026-07-28 | quote: "This specification defines the authoritative protocol requirements, based on the TypeScript schema in [schema.ts](https://github.com/modelcontextprotocol/specification/blob/main/schema/2026-07-28/schema.ts)" | type: official

## conflicts
None identified.

## gaps
- MCP 规范是否正式标记为 1.0 或 GA 版本（现有文档用"production-grade"和"enterprise-ready"但未明确说"1.0"或"GA"）
- Streamable HTTP 传输中，SSE 是否为强制（optional）还是被完全移除（文档说"replies arrive as JSON object or request-scoped SSE stream"，但未明确说 SSE 是否必须实现）

## leads
- SEP-2596（Feature Lifecycle and Deprecation Policy）定义了 HTTP+SSE 的弃用政策，具体见 https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2596
- "Streamable HTTP 替代 HTTP+SSE"这一变化在 protocol version 2025-03-26 时引入，具体见 https://modelcontextprotocol.io/specification/2025-03-26/basic/transports
