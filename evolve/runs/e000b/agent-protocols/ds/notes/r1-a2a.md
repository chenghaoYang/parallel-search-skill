# r1-a2a

question: A2A（Agent2Agent Protocol，Google 发起）管什么、怎么传输、怎么鉴权、状态归属、谁治理（含捐给 Linux Foundation 的细节：时间、现在的治理架构）、当前版本、谁在用（官方列出的采用方/SDK）、与其他协议关系。

checked: https://a2a-protocol.org/latest/specification/, https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/, https://github.com/a2aproject/a2a, https://a2a-protocol.org/latest/community/, https://a2a-protocol.org/latest/whats-new-v1/, https://a2a-protocol.org/v1.0.0/specification/, https://a2a-protocol.org/latest/blog/2026/03/12/a2a-protocol-ships-v10-production-ready-standard-for-agent-to-agent-communication/, https://a2a-protocol.org/latest/topics/a2a-and-mcp/, https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents

## claims

- [C1] A2A 是开放协议，使独立、可能不透明的 AI 代理系统间能通信和协作 | src: https://a2a-protocol.org/latest/specification/ | quote: "facilitate communication and interoperability between independent, potentially opaque AI agent systems" | type: official

- [C2] 传输使用 JSON-RPC 2.0 over HTTP(S)，支持同步请求、流式（Server-Sent Events）和异步通知（webhooks） | src: https://github.com/a2aproject/a2a | quote: "JSON-RPC 2.0 over HTTP(S) with support for synchronous requests, streaming via Server-Sent Events, and asynchronous notifications" | type: official

- [C3] 支持的鉴权方案：API keys、OAuth 2.0、Mutual TLS、OpenID Connect | src: https://a2a-protocol.org/latest/specification/ | quote: "Authentication supports multiple schemes (API keys, OAuth 2.0, mutual TLS)" | type: official

- [C4] Agent Card 的 securitySchemes 字段对齐 OpenAPI 认证方案（apiKey、http、oauth2、openIdConnect） | src: https://a2a-protocol.org/latest/specification/ | quote: "Agents declare the schemes they accept in AgentCard's securitySchemes field, aligning with OpenAPI" | type: official

- [C5] Task 状态机包括 8 个状态：Submitted、Working、Completed、Failed、Canceled、Input Required、Rejected、Auth Required | src: https://a2a-protocol.org/latest/specification/ | quote: "Tasks progress through defined states (Submitted, Working, Completed, Failed, Canceled, Input Required, Rejected, Auth Required)" | type: official

- [C6] Google 于 2025 年 4 月发起 A2A 协议 | src: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ | quote: "Google has unveiled the Agent2Agent Protocol (A2A)" | type: official

- [C7] 2025 年 6 月 23 日，Google 将 A2A 协议、规范和 SDK 捐给 Linux Foundation，建立中立治理 | src: https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents | quote: "Linux Foundation announced the launch of the Agent2Agent (A2A) project on June 23, 2025" | type: official

- [C8] 治理架构由 8 个主要技术公司的代表组成方向委员会：AWS、Cisco、Google、IBM Research、Microsoft、Salesforce、SAP、ServiceNow | src: https://a2a-protocol.org/latest/blog/2026/03/12/a2a-protocol-ships-v10-production-ready-standard-for-agent-to-agent-communication/ | quote: "guided by representatives from eight major technology companies: AWS, Cisco, Google, IBM Research, Microsoft, Salesforce, SAP, and ServiceNow" | type: official

- [C9] 100+ 公司支持 A2A 协议，包括 Atlassian、Cohere、Intuit、LangChain、MongoDB、PayPal、SAP 等 | src: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ | quote: "Over 50 technology partners support the initiative, including Atlassian, Cohere, Intuit, LangChain, MongoDB, PayPal, Salesforce, SAP, ServiceNow" | type: official

- [C10] 当前版本为 v1.0.0，于 2026 年 3 月 12 日发布，标记为生产就绪（production-ready） | src: https://a2a-protocol.org/latest/blog/2026/03/12/a2a-protocol-ships-v10-production-ready-standard-for-agent-to-agent-communication/ | quote: "A2A Protocol community released v1.0 on March 12, 2026, described as 'the first stable, production-ready version'" | type: official

- [C11] 提供 SDK 支持 Python、Go、JavaScript、Java、.NET 和 Rust 等多种编程语言 | src: https://github.com/a2aproject/a2a | quote: "SDKs in multiple languages: Python, Go, JavaScript, Java, .NET, and Rust" | type: official

- [C12] 支持 13+ 代理框架集成，包括 LangGraph、AutoGen、Semantic Kernel、CrewAI 等 | src: https://a2a-protocol.org/latest/community/ | quote: "integrated support in 13+ agentic frameworks, from established platforms like CrewAI and LangGraph to newer tools like Agno and Slide" | type: official

- [C13] A2A 与 MCP（Model Context Protocol）互补，解决不同问题层：MCP 处理代理对工具的交互，A2A 处理代理对代理的通信 | src: https://a2a-protocol.org/latest/topics/a2a-and-mcp/ | quote: "MCP and A2A solve different layers of the problem. MCP handles tool integration within individual agents, while A2A manages communication between agents" | type: official

- [C14] 官方文档表明 MCP 操作纵向（deepening individual agent capabilities），A2A 操作横向（connecting independent agents across organizational boundaries） | src: https://a2a-protocol.org/latest/topics/a2a-and-mcp/ | quote: "MCP operates vertically...A2A operates horizontally, connecting independent agents across organizational boundaries" | type: official

- [C15] v1.0 版本支持多协议、多租户能力和已签名 Agent Card（提供加密验证） | src: https://a2a-protocol.org/latest/blog/2026/03/12/a2a-protocol-ships-v10-production-ready-standard-for-agent-to-agent-communication/ | quote: "Multi-protocol support enabling interoperability...Multi-tenancy capabilities allowing secure hosting...Signed Agent Cards providing cryptographic verification" | type: official

## conflicts

无冲突发现。

## gaps

- Linux Foundation 下属的 A2A 项目委员会的具体治理规则（如投票权分配、添加新成员的流程）
- A2A 协议在不同的 MCP 版本间的兼容性说明
- 官方列出的完整生产采用者名单（vs 早期/实验采用）
- Agent Card 中 supported interfaces 的完整规范详情

## leads

- 检查 GitHub issue/discussions 了解 A2A 与 ACP-IBM 的正式关系声明
- 查看 v1.0.0 具体的向后兼容策略（对 v0.3.0 的支持期限）
- 深入研究 Agent Card 签名验证机制与安全模型的交互
