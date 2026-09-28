# r1-a2a
question: A2A（Agent2Agent Protocol）的连接对象是什么？起源方（Google）与现在的治理方是谁——是否已经捐赠给 Linux Foundation，哪些企业参与治理/steering committee？版本历史？传输层机制？消息格式与核心概念？鉴权机制官方 spec 怎么规定？

checked: https://a2a-protocol.org/latest/specification/, https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/, https://a2a-protocol.org/latest/definitions/, https://github.com/a2aproject/A2A/releases, https://a2a-protocol.org/latest/topics/enterprise-ready/, https://github.com/a2aproject/A2A/blob/main/GOVERNANCE.md

## claims

- [C1] A2A 连接对象是「独立 agent/系统之间的跨主体协作」，通过 AgentCard 发现彼此能力。 | src: https://a2a-protocol.org/latest/specification/ | quote: "facilitate communication and interoperability between independent, potentially opaque AI agent systems" | type: official

- [C2] Google 于 2025 年 4 月 9 日首次发布 A2A 协议（v0.1.0），包括 50+ 初始合作伙伴。 | src: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ | quote: "Google has unveiled the Agent2Agent Protocol (A2A)" | type: official

- [C3] Google 于 2025 年 6 月 23 日将 A2A 协议捐赠给 Linux Foundation，建立 Agent2Agent 项目实现厂商中立治理。 | src: https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/ | quote: "Google Cloud transferred the Agent2Agent (A2A) protocol specification to the Linux Foundation" | type: official

- [C4] A2A 技术指导委员会（TSC）由 8 个企业代表组成：Google、Microsoft、Cisco、AWS、Salesforce、ServiceNow、SAP、IBM。 | src: https://github.com/a2aproject/A2A/blob/main/GOVERNANCE.md | quote: "Technical Steering Committee (TSC) comprising eight member organizations" | type: official

- [C5] 当前版本为 v1.0.1（发布 2026 年 5 月 28 日），v1.0.0 于 2026 年 3 月 12 日发布。 | src: https://github.com/a2aproject/A2A/releases | quote: "v1.0.1 (released May 28)" | type: official

- [C6] A2A 支持三种等效的传输协议：JSON-RPC 2.0、gRPC、HTTP+JSON REST，所有均基于 HTTPS。 | src: https://a2a-protocol.org/latest/specification/ | quote: "Three standard implementations...JSON-RPC 2.0...gRPC...HTTP/REST" | type: official

- [C7] 核心数据结构包括 Task（工作单元，含状态转移）、Message（通信单元）、Part（灵活内容容器）、AgentCard（自描述清单）、Artifact（输出表示）。 | src: https://a2a-protocol.org/latest/definitions/ | quote: "Task...Message...Part...AgentCard...Artifacts" | type: official

- [C8] AgentCard 是 JSON 元数据文档，发布在 /.well-known/agent-card.json，描述 agent 身份、能力、支持的传输、认证要求。 | src: https://a2a-protocol.org/latest/specification/ | quote: "Agent Card—a JSON metadata document...typically at https://{domain}/.well-known/agent-card.json" | type: official

- [C9] 鉴权机制支持 OAuth2、API keys、mutual TLS、HTTP Basic Auth，凭证通过标准 HTTP header 传递（Authorization、X-API-Key）。 | src: https://a2a-protocol.org/latest/topics/enterprise-ready/ | quote: "Credentials travel in standard HTTP headers...OAuth2 tokens or API keys" | type: official

- [C10] 服务器必须对缺失/无效凭证返回 401 Unauthorized，对已验证用户缺乏权限返回 403 Forbidden。 | src: https://a2a-protocol.org/latest/topics/enterprise-ready/ | quote: "401 Unauthorized for missing/invalid credentials or 403 Forbidden" | type: official

- [C11] v1.0 发布（2026 年 3 月 12 日）引入 JWS（RFC 7515）加密签名的 AgentCard 与 JCS 规范化（RFC 8785），用于域验证。 | src: https://a2a-protocol.org/latest/blog/2026/03/12/a2a-protocol-ships-v10-production-ready-standard-for-agent-to-agent-communication/ | quote: "cryptographically signed Agent Cards using JWS (RFC 7515)" | type: official

- [C12] Task 生命周期状态包括：submitted、working、completed、failed、canceled、input required、rejected、auth required。 | src: https://a2a-protocol.org/latest/specification/ | quote: "lifecycle states...submitted, working, completed, failed, canceled, input required, rejected, auth required" | type: official

- [C13] 传输层强制要求 TLS 1.2 或更高版本，生产环境必须使用 HTTPS。 | src: https://a2a-protocol.org/latest/topics/enterprise-ready/ | quote: "TLS 1.2 or higher with strong cipher suites" | type: official

- [C14] 协议使用 Protocol Buffers 作为权威数据模型定义，同时发布为 JSON Schema 2020-12。 | src: https://a2a-protocol.org/latest/specification/ | quote: "Protocol Buffers as the authoritative definition...JSON Schema 2020-12" | type: official

- [C15] 官方立场：MCP 和 A2A 解决不同层次问题，MCP 用于单 agent 层面的工具集成，A2A 专注 agent 间通信协调。 | src: https://a2a-protocol.org/latest/blog/2026/03/12/a2a-protocol-ships-v10-production-ready-standard-for-agent-to-agent-communication/ | quote: "MCP and A2A solve different layers of the problem...tool integration...coordination between agents" | type: official

- [C16] 生产部署包括 Microsoft Azure AI Foundry、Amazon Bedrock AgentCore、Salesforce Agentforce。 | src: https://opensource.googleblog.com/2026/04/a-year-of-open-collaboration-celebrating-the-anniversary-of-a2a.html | quote: "production deployments inside Microsoft Azure AI Foundry, Amazon Bedrock AgentCore, and Salesforce Agentforce" | type: official

## conflicts

## gaps
- TSC 具体的轮换机制、成员续任时间表未明确说明。
- v0.2.0–v0.3.0 版本变更日志和细节未完整记录。
- Steady state 治理转换的具体时间表和成员变化未最终确定。
- Out-of-band 凭证获取流程的标准规范未在 spec 中明确。

## leads
- Linux Foundation Agentic AI Foundation (AAIF) 对 A2A 与 MCP 治理的整合——需检查官方 AAIF 公告。
- A2A 与 ACP-IBM 的并入关系——需 r1-acp-ibm 补充。
