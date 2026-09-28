# r1-a2a
question: Agent2Agent（A2A）官方规范里，角色、原语、传输、任务状态、发现、鉴权、治理与版本，以及规范自己如何定位和 MCP / ACP 的关系。
checked: https://a2a-protocol.org/latest/specification/, https://a2a-protocol.org/latest/, https://a2a-protocol.org/latest/topics/key-concepts/, https://a2a-protocol.org/latest/topics/agent-discovery/, https://a2a-protocol.org/latest/topics/a2a-and-mcp/, https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/, https://raw.githubusercontent.com/a2aproject/A2A/main/specification/a2a.proto, https://raw.githubusercontent.com/a2aproject/A2A/main/CHANGELOG.md, https://raw.githubusercontent.com/a2aproject/A2A/main/GOVERNANCE.md, https://github.com/a2aproject/A2A/releases/tag/v0.1.0, https://research.ibm.com/projects/agent-communication-protocol, https://github.com/orgs/i-am-bee/discussions/5

## claims
- [C1] D1：两端官方名是 A2A Client 与 A2A Server (Remote Agent)。 | src: https://a2a-protocol.org/latest/specification/ | quote: "A2A Client: An application or agent that initiates requests to an A2A Server on behalf of a user or another system." | type: official
- [C2] D1：Message 发送方枚举含 ROLE_USER（client→server）与 ROLE_AGENT。 | src: https://raw.githubusercontent.com/a2aproject/A2A/main/specification/a2a.proto | quote: "The message is from the client to the server." | type: official
- [C3] D2：Task、Message、AgentCard、Part、Artifact 属数据模型；规范源是 spec/a2a.proto。 | src: https://a2a-protocol.org/latest/specification/ | quote: "the file `spec/a2a.proto` is the single authoritative normative definition of all protocol data objects and request/response messages." | type: official
- [C4] D2：Send Message 可新建 Task，或直接返回 Message。 | src: https://a2a-protocol.org/latest/specification/ | quote: "MAY create a new `Task` to process the provided message asynchronously or MAY return a direct `Message` response" | type: official
- [C5] D3：protocolBinding 核心值为 `JSONRPC`、`GRPC`、`HTTP+JSON`。 | src: https://a2a-protocol.org/latest/specification/ | quote: "The core ones officially supported are `JSONRPC`, `GRPC` and `HTTP+JSON`." | type: official
- [C6] D3：JSON-RPC 绑定用 JSON-RPC 2.0 over HTTP(S)，流式用 Server-Sent Events。 | src: https://a2a-protocol.org/latest/specification/ | quote: "using JSON-RPC 2.0 for method calls and Server-Sent Events for streaming." | type: official
- [C7] D3：changelog 标题 0.2.2（2025-06-09）下的 Features 写入 gRPC 与 REST。 | src: https://raw.githubusercontent.com/a2aproject/A2A/main/CHANGELOG.md | quote: "Add gRPC and REST definitions to A2A protocol specifications (#695)" | type: official
- [C8] D4：proto enum TaskState 含 TASK_STATE_UNSPECIFIED、SUBMITTED、WORKING、COMPLETED、FAILED、CANCELED、INPUT_REQUIRED、REJECTED、AUTH_REQUIRED。 | src: https://raw.githubusercontent.com/a2aproject/A2A/main/specification/a2a.proto | quote: "Defines the possible lifecycle states of a `Task`." | type: official
- [C9] D4：终态为 COMPLETED、FAILED、CANCELED、REJECTED；中断态为 INPUT_REQUIRED、AUTH_REQUIRED。 | src: https://a2a-protocol.org/latest/specification/ | quote: "terminal state (`TASK_STATE_COMPLETED`, `TASK_STATE_FAILED`, `TASK_STATE_CANCELED`, `TASK_STATE_REJECTED`) or an interrupted state (`TASK_STATE_INPUT_REQUIRED`, `TASK_STATE_AUTH_REQUIRED`)" | type: official
- [C10] D5：Well-Known URI 为 `https://{server_domain}/.well-known/agent-card.json`。 | src: https://a2a-protocol.org/latest/specification/ | quote: "Well-Known URI: Accessing `https://{server_domain}/.well-known/agent-card.json`" | type: official
- [C11] D5：0.3.0（2025-07-30）把 Agent Card 的 well-known 从 `agent.json` 改为 `agent-card.json`。 | src: https://raw.githubusercontent.com/a2aproject/A2A/main/CHANGELOG.md | quote: "Change Well-Known URI for Agent Card hosting from `agent.json` to `agent-card.json` (#841)" | type: official
- [C12] D6：SecurityRequirement.schemes 把方案名映到 StringList。 | src: https://raw.githubusercontent.com/a2aproject/A2A/main/specification/a2a.proto | quote: "map<string, StringList> schemes = 1;" | type: official
- [C13] D6：SecurityScheme 必须且只能是下列之一：apiKey、httpAuth、oauth2、openIdConnect、mtls。 | src: https://a2a-protocol.org/latest/specification/ | quote: "A `SecurityScheme` MUST contain exactly one of the following: `apiKeySecurityScheme`, `httpAuthSecurityScheme`, `oauth2SecurityScheme`, `openIdConnectSecurityScheme`, `mtlsSecurityScheme`" | type: official
- [C23] D6：AgentCard 的方案表字段名是 security_schemes。 | src: https://raw.githubusercontent.com/a2aproject/A2A/main/specification/a2a.proto | quote: "map<string, SecurityScheme> security_schemes = 8;" | type: official
- [C24] D7：首页写协议许可为 Apache License 2.0。 | src: https://a2a-protocol.org/latest/ | quote: "The A2A Protocol is licensed under the Apache License 2.0" | type: official
- [C14] D6：客户端必须在每次请求发送 A2A-Version。 | src: https://a2a-protocol.org/latest/specification/ | quote: "Clients MUST send the `A2A-Version` header with each request" | type: official
- [C15] D7：规范页写 Latest Released Version 1.0.0，并链到 0.3.0、0.2.6、0.1.0。页眉无日期。 | src: https://a2a-protocol.org/latest/specification/ | quote: "Latest Released Version 1.0.0" | type: official
- [C16] D7：changelog 将 1.0.0 标为 2026-03-12。 | src: https://raw.githubusercontent.com/a2aproject/A2A/main/CHANGELOG.md | quote: "## [1.0.0] (2026-03-12)" | type: official
- [C17] D7：首页写由 Google 开发并捐赠给 Linux Foundation。 | src: https://a2a-protocol.org/latest/ | quote: "A2A was originally developed by Google and donated to the Linux Foundation." | type: official
- [C18] D7：首页写由 TSC 维护，成员来自 AWS、Cisco、Google、IBM Research、Microsoft、Salesforce、SAP、ServiceNow。 | src: https://a2a-protocol.org/latest/ | quote: "maintained by a Technical Steering Committee with representatives from AWS, Cisco, Google, IBM Research, Microsoft, Salesforce, SAP, and ServiceNow" | type: official
- [C19] D7：2026-08-27 公告：被接受为 AAIF 的 Growth Stage 项目。 | src: https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/ | quote: "officially been accepted as a Growth Stage project at the Agentic AI Foundation (AAIF)." | type: official
- [C20] D9：规范附录 B 写 A2A 与 MCP 是互补协议。 | src: https://a2a-protocol.org/latest/specification/ | quote: "A2A and MCP are complementary protocols designed for different aspects of agentic systems" | type: official
- [C21] D9：BeeAI 2025-08-25 公告称 ACP 正式并入 Linux Foundation 下的 A2A。 | src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "Today, we’re excited to share that ACP is officially merging with the A2A under the Linux Foundation (@thelinuxfoundation) umbrella." | type: secondary
- [C22] D9：IBM Research 的 ACP 项目页横幅写 ACP 已属于 Linux Foundation 下的 A2A。 | src: https://research.ibm.com/projects/agent-communication-protocol | quote: "IMPORTANT UPDATE - ACP is now part of A2A under the Linux Foundation!" | type: secondary

## conflicts
- 传输：Key Concepts 写 “JSON-RPC 2.0 is used as the payload format for all requests and responses.”（https://a2a-protocol.org/latest/topics/key-concepts/）；规范同时列出 JSONRPC、GRPC、HTTP+JSON（https://a2a-protocol.org/latest/specification/）。
- 鉴权字段：规范 prose 写 `AgentCard.securitySchemes` 与 `AgentCard.security`；proto 是 security_schemes 与 security_requirements。发现指南写 required `schemes`（https://a2a-protocol.org/latest/topics/agent-discovery/）。
- 角色字面量：术语节 role 为 "user" or "agent"；§4.1.5/proto 为 ROLE_USER / ROLE_AGENT。同一规范页。
- 版本：页眉 1.0.0；changelog 另有 1.0.1（2026-05-26），且现行正文已含 application/a2a+json。
- SubscribeToTask：§5.3 为 `POST /tasks/{id}:subscribe`；proto 为 `get: "/tasks/{id=*}:subscribe"`。
- 治理：首页只写捐赠给 LF 并由 TSC 维护；AAIF 帖写加入 Linux Foundation-directed AAIF。未写 TSC 是否改变。

## gaps
- D8 未填。未打开 OpenAI / Anthropic / Google / Microsoft 产品文档。
- 版本起点：changelog 正文最早标题是 0.2.1（2025-05-27）。v0.1.0 发布页只有 “09 Jun”，无年份。
- A2A 规范与 /latest/ 首页未写 ACP 合并。规范 HTML 无 SecurityRequirement 字段表。

## leads
- ACP 迁移：https://github.com/i-am-bee/beeai-platform/blob/main/docs/community-and-support/acp-a2a-migration-guide.mdx
- D8 须打开厂商站：Google Cloud、Azure AI Foundry、Bedrock AgentCore。OpenAI/Anthropic 未点名。
- https://a2a-protocol.org/dev/ 检索到 “IBM ACP: Incorporated into the A2A Protocol”，未打开该页。
