# r1-a2a
question: A2A（Agent2Agent Protocol）官方规范的：定位/管辖层、核心抽象、传输/消息格式、状态归属、鉴权机制、版本历史、治理主体、以及官方文档如何描述A2A和MCP的关系
checked: https://a2a-protocol.org/latest/specification/,https://a2a-protocol.org/latest/topics/a2a-and-mcp/,https://github.com/a2aproject/A2A,https://github.com/a2aproject/A2A/releases,https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents,https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/,https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/,https://blog.pebblous.ai/blog/a2a-mcp-agentic-ai-foundation-authorization/en/

## claims
- [C1] A2A scope定位为"facilitates communication and interoperability between independent, potentially opaque AI agent systems" | src: https://a2a-protocol.org/latest/specification/ | quote: "facilitates communication and interoperability between independent, potentially opaque AI agent systems" | type: official
- [C2] A2A管辖层为水平层（agent-to-agent），MCP为竖直层（agent-to-tools）| src: https://a2a-protocol.org/latest/topics/a2a-and-mcp/ | quote: "A2A is horizontal. It connects agents across that boundary... MCP standardizes how an agent reaches a database, an API or a file system" | type: official
- [C3] 核心抽象包括Task：represents "the core unit of action for A2A" with unique ID, status, artifacts, interaction history | src: https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto | quote: "the core unit of action for A2A" | type: official
- [C4] 核心抽象Message："one unit of communication between client and server" containing message ID, context, task associations, role (USER or AGENT), parts, metadata | src: https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto | quote: "one unit of communication between client and server" | type: official
- [C5] 核心抽象Agent Card："a self-describing manifest for an agent" providing metadata, capabilities, security schemes, supported skills | src: https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto | quote: "a self-describing manifest for an agent" | type: official
- [C6] 核心抽象Part："a container for a section of communication content" supporting text, bytes, URLs, or JSON data | src: https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto | quote: "a container for a section of communication content" | type: official
- [C7] 核心抽象Artifact：task outputs with unique ID, name, description, content parts, optional metadata | src: https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto | quote: "task outputs" | type: official
- [C8] 传输格式：JSON-RPC 2.0 over HTTPS为最常见部署，支持gRPC和HTTP/REST | src: https://a2a-protocol.org/latest/specification/ | quote: "JSON-RPC 2.0 over HTTPS (the most common deployment), gRPC, and HTTP+JSON/REST" | type: official
- [C9] 消息格式三层架构：Canonical Data Model (Protocol Buffers)、Abstract Operations (Binding-independent)、Protocol Bindings (JSON-RPC, gRPC, HTTP/REST) | src: https://a2a-protocol.org/latest/specification/ | quote: "Canonical Data Model: Protocol Buffer definitions... Abstract Operations: Binding-independent capability descriptions... Protocol Bindings: Concrete implementations" | type: official
- [C10] 状态归属：Server（接收方agent）维护task state | src: https://a2a-protocol.org/latest/specification/ | quote: "the state is kept in a server-side task, because the connection won't outlive the job" | type: official
- [C11] 支持Task lifecycle状态：SUBMITTED, WORKING, COMPLETED, FAILED, CANCELED, INPUT_REQUIRED, REJECTED, AUTH_REQUIRED | src: https://a2a-protocol.org/latest/specification/ | quote: "submitted, working, completed, failed, canceled, input-required, rejected, or auth-required" | type: official
- [C12] 鉴权机制：OAuth 2.0 (支持device code和PKCE)、Bearer tokens (JWT)、mTLS、OpenID Connect | src: https://a2a-protocol.org/v1.0.0/specification/ | quote: "OAuth 2.0 flow modernization (removing implicit/password flows, adding device code and PKCE support)" | type: official
- [C13] v1.0引入mTLS和OAuth 2.0现代化，移除implicit和password flows | src: https://github.com/a2aproject/A2A/releases | quote: "OAuth 2.0 flow modernization (removing implicit/password flows, adding device code and PKCE support)" | type: official
- [C14] 当前版本v1.0.1发布于2026年5月28日 | src: https://github.com/a2aproject/A2A/releases | quote: "Latest Release: v1.0.1 (May 28, 2026)" | type: official
- [C15] v1.0.0重大版本发布于2026年3月12日，引入breaking changes | src: https://github.com/a2aproject/A2A/releases | quote: "Major Release: v1.0.0 (March 12, 2026)" | type: official
- [C16] 初始版本v0.2.0发布于2025年6月9日 | src: https://github.com/a2aproject/A2A/releases | quote: "v0.2.0 (June 9, 2025): Initial specification framework" | type: official
- [C17] 治理主体现为Agentic AI Foundation (AAIF) under Linux Foundation，A2A于2026年8月加入AAIF | src: https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/ | quote: "A2A... became a hosted project of AAIF, the Linux Foundation body focused specifically on agentic AI" | type: official
- [C18] 初始治理：Google于2025年6月将A2A捐赠给Linux Foundation | src: https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/ | quote: "Google Cloud has transferred the Agent2Agent (A2A) protocol to the Linux Foundation" | type: official
- [C19] 创始成员：AWS、Cisco、Google、Microsoft、Salesforce、SAP、ServiceNow | src: https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents | quote: "Major companies backing the initiative include AWS, Cisco, Google Cloud, Microsoft, Salesforce, SAP, and ServiceNow" | type: official
- [C20] 支持组织超过150个（截至2026年4月）| src: https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year | quote: "over 150 organizations" | type: official
- [C21] A2A与MCP关系为"complementary, not competing" | src: https://a2a-protocol.org/latest/topics/a2a-and-mcp/ | quote: "complementary, not competing... Used together, MCP gives each agent depth, and A2A gives your system reach" | type: official
- [C22] 官方描述MCP为vertical（垂直），A2A为horizontal（水平）| src: https://a2a-protocol.org/latest/topics/a2a-and-mcp/ | quote: "MCP handles vertical connectivity... A2A handles horizontal connectivity" | type: official
- [C23] Google官方对A2A与MCP的描述："A2A is an open protocol that complements Anthropic's MCP" | src: https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/ | quote: "A2A is an open protocol that complements Anthropic's MCP, which provides helpful tools and context to agents" | type: official
- [C24] AAIF governance结构：MCP和A2A各自保持独立的maintainers、specification process和release schedule | src: https://blog.pebblous.ai/blog/a2a-mcp-agentic-ai-foundation-authorization/en/ | quote: "each protocol keeps its own maintainers, specification process and release schedule" | type: official

## conflicts
None identified.

## gaps
- A2A-Version header机制的具体版本协商规则（向后兼容性策略）
- 具体的Part MIME type支持列表
- Artifact metadata扩展URI的详细规范
- OAuth 2.0 client credentials flow具体实现要求
- Server-Sent Events streaming具体protocol binding

## leads
- AAIF于2026年8月成立后治理结构（MCP和A2A的并列关系）可能有助理解agent protocol生态的未来演进
- A2A采纳mTLS+OAuth 2.0零信任架构（v1.0起）可能标志agent间通信安全实践的新方向
- Context ID用于维持多turn conversation状态的设计可能值得与其他protocol（如MCP）的state management对比

