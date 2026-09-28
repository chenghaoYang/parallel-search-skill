# r1-a2a
question: A2A 协议的当前规格：连接哪两端、治理方、传输、核心抽象、鉴权、版本、发现机制、与 MCP/IBM ACP 的关系（填 grid.md A2A 行 D1–D10）
checked: https://a2a-protocol.org/latest/, https://a2a-protocol.org/latest/specification/, https://a2a-protocol.org/latest/topics/a2a-and-mcp/, https://github.com/a2aproject/A2A/blob/main/docs/specification.md, https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto, https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md, https://github.com/a2aproject/A2A/blob/main/docs/blog/posts/announcing-1.0.md, https://github.com/a2aproject/A2A/blob/main/docs/blog/posts/a2a-joins-aaif.md, https://github.com/a2aproject/A2A/blob/main/docs/topics/agent-discovery.md, https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents, https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/, https://aaif.io/projects, https://github.com/orgs/a2aproject/repositories

## claims

D1 连接两端（agent↔agent，对等、不透明）
- [C1] A2A 规范 A2A Client 与 A2A Server(Remote Agent) 之间的边："An A2A Client: An application or agent that initiates requests to an A2A Server on behalf of a user or another system"；Server 是 "an agent or agentic system that exposes an A2A-compliant endpoint" | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "Agent2Agent Protocol (A2A): Focuses on standardizing how independent, often opaque, AI agents communicate and collaborate with each other as peers." | type: official

D2 发起者与治理
- [C2] Google 创建并于 2025 年 4 月发布，2025-06-23 在 OSS NA 宣布捐给 Linux Foundation | src: https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents | quote: "an open protocol created by Google for secure agent-to-agent communication and collaboration... launched by Google in April... Under the Linux Foundation's governance, A2A will remain vendor neutral" | type: official
- [C3] 2026-08-27 官方博客：A2A 被接受为 Agentic AI Foundation (AAIF, Linux Foundation 旗下) 的 Growth Stage 项目，与 MCP、goose、AGENTS.md 并列 | src: https://github.com/a2aproject/A2A/blob/main/docs/blog/posts/a2a-joins-aaif.md | quote: "has officially been accepted as a Growth Stage project at the Agentic AI Foundation (AAIF)... alongside sibling projects like MCP, goose, and AGENTS.md" | type: official
- [C4] 决策主体为 Technical Steering Committee，成员来自 AWS, Cisco, Google, IBM Research, Microsoft, Salesforce, SAP, ServiceNow | src: https://github.com/a2aproject/A2A/blob/main/docs/blog/posts/announcing-1.0.md | quote: "The A2A Technical Steering Committee includes representatives from AWS, Cisco, Google, IBM Research, Microsoft, Salesforce, SAP, and ServiceNow." | type: official

D3 传输与格式（三种官方绑定 + 自定义绑定；无单一必绑传输）
- [C5] 三个标准绑定：JSON-RPC 2.0、gRPC、HTTP+JSON/REST，另允许 custom bindings；"the file spec/a2a.proto is the single authoritative normative definition"（proto 为正典数据模型） | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "concrete mappings of the abstract operations and data structures to specific protocol bindings (JSON-RPC, gRPC, HTTP/REST)" | type: official
- [C6] JSON-RPC 绑定：单一 POST /rpc 端点，方法名 PascalCase（SendMessage、GetTask…），流式走 SSE | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "using JSON-RPC 2.0 for method calls and Server-Sent Events for streaming... PascalCase method names matching gRPC conventions" | type: official
- [C7] REST 绑定端点：POST /message:send、POST /message:stream(SSE, Content-Type application/a2a+json)、GET /tasks/{id}、GET /tasks、POST /tasks/{id}:cancel、POST /tasks/{id}:subscribe、/tasks/{id}/pushNotificationConfigs、GET /extendedAgentCard | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "Send message | SendMessage | SendMessage | POST /message:send ... Get task | GetTask | GetTask | GET /tasks/{id}" | type: official
- [C8] gRPC 绑定实现 service A2AService，proto package 为 lf.a2a.v1（v1.0 加 LF 前缀） | src: https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto | quote: "package lf.a2a.v1; ... service A2AService" | type: official
- [C9] 绑定非强制单选：Agent 在 AgentCard.supportedInterfaces 声明全部支持协议（值 JSONRPC/GRPC/HTTP+JSON），客户端任选 | src: https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto | quote: "The core ones officially supported are `JSONRPC`, `GRPC` and `HTTP+JSON`" | type: official
- [C10] 任务更新三条路：polling (GetTask)、streaming (SSE/gRPC stream)、push notification webhook | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "Clients retrieve task updates through polling, streaming, or push notifications" | type: official

D4 核心抽象
- [C11] Task 字段：id(REQUIRED), context_id, status(REQUIRED), artifacts, history, metadata | src: https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto | quote: "message Task { string id = 1 [(google.api.field_behavior) = REQUIRED]; string context_id = 2; TaskStatus status = 3 ... repeated Artifact artifacts = 4; repeated Message history = 5" | type: official
- [C12] TaskState 枚举 9 值：UNSPECIFIED, SUBMITTED, WORKING, COMPLETED, FAILED, CANCELED, INPUT_REQUIRED, REJECTED, AUTH_REQUIRED；前四者中 COMPLETED/FAILED/CANCELED/REJECTED 为终态 | src: https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto | quote: "enum TaskState { TASK_STATE_UNSPECIFIED = 0; TASK_STATE_SUBMITTED = 1; TASK_STATE_WORKING = 2; TASK_STATE_COMPLETED = 3; TASK_STATE_FAILED = 4; TASK_STATE_CANCELED = 5; TASK_STATE_INPUT_REQUIRED = 6; TASK_STATE_REJECTED = 7; TASK_STATE_AUTH_REQUIRED = 8; }" | type: official
- [C13] Message = 一回合通信（message_id, role=ROLE_USER/ROLE_AGENT, parts, task_id, context_id）；Artifact = 任务产出物；"Messages SHOULD NOT be used to deliver task outputs. Results SHOULD BE returned using Artifacts" | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "An output (e.g., a document, image, structured data) generated by the agent as a result of a task, composed of Parts" | type: official
- [C14] 流式事件：TaskStatusUpdateEvent / TaskArtifactUpdateEvent；流以 Task 开头、终态关闭 | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "the stream MUST begin with the Task object, followed by zero or more TaskStatusUpdateEvent or TaskArtifactUpdateEvent objects" | type: official

D5 鉴权
- [C15] AgentCard.securitySchemes 声明五种：APIKeySecurityScheme, HTTPAuthSecurityScheme, OAuth2SecurityScheme, OpenIdConnectSecurityScheme, MutualTlsSecurityScheme | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "APIKeySecurityScheme, HTTPAuthSecurityScheme, OAuth2SecurityScheme, OpenIdConnectSecurityScheme, MutualTlsSecurityScheme" | type: official
- [C16] 凭证带外获取、随每请求放 header；生产必须 HTTPS/TLS；"The client obtains the necessary credentials through an out-of-band process... includes these credentials in protocol-appropriate headers or metadata for every A2A request" | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "Production deployments MUST use encrypted communication (HTTPS for HTTP-based bindings, TLS for gRPC)" | type: official
- [C17] v1.0 移除 OAuth implicit/password 流，新增 device code/PKCE；任务内授权委托走 TASK_STATE_AUTH_REQUIRED | src: https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md | quote: "modernize oauth 2.0 flows - remove implicit/password, add device code / pkce" | type: official

D6 版本与状态
- [C18] v1.0.0 发布 2026-03-12（首个稳定版，含 breaking changes）；v1.0.1 2026-05-26 为 changelog 最新 | src: https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md | quote: "## [1.0.0] ... (2026-03-12) ### ⚠ BREAKING CHANGES" | type: official
- [C19] 版本协商：每请求带 A2A-Version header（Major.Minor），不支持返回 VersionNotSupportedError，空值按 0.3 处理；Patch 不用 | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "Agents MUST interpret empty value as 0.3 version... Patch version numbers SHOULD NOT be used" | type: official
- [C20] v1.0 破坏性变更含：HTTP 绑定 URL 去 /v1 前缀、TaskPushNotificationConfig 合并、proto 包名加 lf. 前缀；AgentCard 可同时宣告 0.3 与 1.0 以便渐进迁移 | src: https://github.com/a2aproject/A2A/blob/main/docs/blog/posts/announcing-1.0.md | quote: "AgentCard... now allows agents to advertise support for both existing v0.3 protocol behavior and v1.0 simultaneously" | type: official

D7 发现机制
- [C21] Agent Card = JSON 元数据文档（身份/能力/skills/端点/认证要求），well-known 路径为 /.well-known/agent-card.json（RFC 8615），另支持 registries/catalogs 与直接配置 | src: https://github.com/a2aproject/A2A/blob/main/docs/topics/agent-discovery.md | quote: "The standard path is `https://{agent-server-domain}/.well-known/agent-card.json`, following the principles of RFC 8615" | type: official
- [C22] well-known 路径在 0.3.x 期间从 agent.json 改为 agent-card.json（issue #841）；IANA 注册 URI suffix agent-card.json | src: https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md | quote: "Change Well-Known URI for Agent Card hosting from `agent.json` to `agent-card.json` (#841)" | type: official
- [C23] AgentCard REQUIRED 字段：name, description, supported_interfaces, version, capabilities, default_input_modes, default_output_modes, skills；可选 security_schemes、signatures(JWS 签名卡) | src: https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto | quote: "repeated AgentInterface supported_interfaces = 3 [(google.api.field_behavior) = REQUIRED]... repeated AgentCardSignature signatures = 13" | type: official
- [C24] 另有 GetExtendedAgentCard 操作（MUST 要求认证）返回更详细的认证版卡片 | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "The Get Extended Agent Card operation MUST require authentication" | type: official

D8 大厂支持
- [C25] Google 创建；Microsoft、AWS 等 8 家进 TSC；官方称 Google Cloud、AWS Bedrock AgentCore Runtime、Microsoft Azure AI Foundry 已内建原生 A2A 支持；150+ 组织支持；框架支持 LangGraph, CrewAI, Pydantic AI, AG2, IBM BeeAI | src: https://github.com/a2aproject/A2A/blob/main/docs/blog/posts/a2a-joins-aaif.md | quote: "Major cloud providers—including Google Cloud, AWS Bedrock AgentCore Runtime, and Microsoft Azure AI Foundry—have built native A2A support directly into their infrastructure" | type: official

D9 与 MCP / IBM ACP 关系
- [C26] 官方定位互补非竞争：MCP=agent→tools（垂直），A2A=agent↔agent（水平、对等委托） | src: https://a2a-protocol.org/latest/topics/a2a-and-mcp/ | quote: "A2A handles inter-agent collaboration and MCP handles tool integration... Use both together" | type: official
- [C27] IBM ACP 已于 2025-08-29 宣布正式并入 A2A（同在 LF 伞下），ACP 团队停止独立开发并转入 A2A，提供迁移指南；IBM 的 Kate Blair 加入 TSC | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "ACP is officially merging with the A2A under the Linux Foundation... the ACP team will be winding down active development" | type: official
- [C28] BeeAI 平台原由 ACP 驱动现已改用 A2A；BeeAI agent 可用 A2AServer adapter 变 A2A-compliant | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "The BeeAI platform, previously powered by ACP, now uses A2A to support agents from any framework." | type: official

D10 场景与实现
- [C29] 官方 SDK：a2a-python, a2a-js, a2a-java, a2a-rs, a2a-dotnet, a2a-go；另有 a2a-samples, a2a-inspector, a2a-tck, a2a-cli | src: https://github.com/orgs/a2aproject/repositories | quote: "a2a-python / a2a-js / a2a-java / a2a-rs / a2a-dotnet / a2a-go / a2a-tck" (repo 名) | type: official
- [C30] 官方称已在供应链、金融、移动平台生产环境运行；典型场景=跨框架/跨组织边界的任务委托与协作 | src: https://github.com/a2aproject/A2A/blob/main/docs/blog/posts/a2a-joins-aaif.md | quote: "runs in production across supply chains, financial services, and mobile platforms" | type: official

## conflicts
- well-known 路径随版本变化：v0.3 前为 /.well-known/agent.json，v0.3 起改为 /.well-known/agent-card.json（changelog #841）。非矛盾，但引用旧教程会写成 agent.json，成稿需注明版本。
- REST URL 在 v1.0 去掉 /v1 前缀（旧版为 /v1/message:send 之类）：changelog "Remove v1s from a2a url http bindings"；AgentInterface 注释示例仍写 "https://api.example.com/a2a/v1"（proto 注释未同步清理，措辞为示例 URL 而非规范路径）。

## gaps
- Anthropic 对 A2A 的明确立场未查到一手说法（D8 子表中 Anthropic 列仍缺）。
- JSON-RPC 绑定在 v1.0 的方法名从 message/send 风格改 PascalCase 的变更记录未单独核对 changelog 条目（spec §9.3 仅给出现状）。
- AAIF 官网未标 A2A 的 stage 名称；「Growth Stage」说法仅来自 A2A 官方博客。

## leads
- grid 里 ACP-IBM 行可直接标「已并入 A2A（2025-08-29，LF AI & Data 公告）」，D6 标 deprecated/wound-down。
- AAIF 同时托管 MCP 与 A2A（2026-08），「同基金会兄弟项目」是 D9 的新事实层。
- a2a-tck（conformance test kit）存在 → 说明已有合规测试生态。
