# r1-acp
question: ACP 缩写消歧——Zed Agent Client Protocol / OpenAI·Stripe Agentic Commerce Protocol / AGNTCY Agent Connect Protocol / IBM Agent Communication Protocol 各自的 D1–D8
checked: https://agentclientprotocol.com, https://github.com/zed-industries/agent-client-protocol (=agentclientprotocol/agent-client-protocol), https://agentclientprotocol.com/overview/agents, https://agentclientprotocol.com/overview/clients, https://agentclientprotocol.com/protocol/overview, https://agenticcommerce.dev, https://github.com/agentic-commerce-protocol/agentic-commerce-protocol, https://docs.stripe.com/agentic-commerce, https://developers.openai.com/commerce/, https://github.com/agntcy, https://github.com/agntcy/acp-spec (+openapi.json), https://spec.acp.agntcy.org, https://agntcy.org, https://github.com/i-am-bee/acp

## claims

### Zed ACP = Agent Client Protocol
- [C1] 全称 Agent Client Protocol；连接 code editors ↔ coding agents（类比 LSP 之於语言服务器） | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: "The Agent Client Protocol (ACP) standardizes communication between code editors (interactive programs for viewing and editing source code) and coding agents (programs that use generative AI to autonomously modify code)." | type: official
- [C2] Zed 发起；仓库 2025-06-23 创建，原 zed-industries 现迁至 agentclientprotocol org；Apache-2.0，无 CLA；有 GOVERNANCE.md/MAINTAINERS.md | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: "ACP is a protocol intended for broad adoption across the ecosystem; we follow a structured process" | type: official
- [C3] 传输：本地 agent 作为编辑器子进程，JSON-RPC over stdio；远程 agent 用 HTTP 或 WebSocket；复用 MCP 的 JSON 表示；用户可读文本默认 Markdown | src: https://agentclientprotocol.com | quote: "communicating via JSON-RPC over stdio" | type: official
- [C4] 核心抽象/方法：initialize（protocolVersion 协商+能力交换）、session/new、session/load（loadSession 能力）、session/prompt、session/update 通知、session/request_permission（tool call 授权）、terminal/*、fs/read_text_file|write_text_file（路径必须绝对）、session/set_mode、authenticate、logout | src: https://agentclientprotocol.com/protocol/overview | quote: "Request user authorization for tool calls" | type: official
- [C5] 版本：稳定协议版本为 1；线兼容由 initialize 时交换的 protocolVersion 决定；schema/v1 与 schema/v2 为 SDK 生成用构件 | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: "The current stable ACP protocol version is `1`." | type: official
- [C6] 鉴权：agent 可要求 authenticate 方法；logout 可选，需 agentCapabilities.auth.logout 能力；具体 authMethods 由 agent 宣告 | src: https://agentclientprotocol.com/protocol/overview | quote: "Authenticate with the Agent (if required)" | type: official
- [C7] Agent 侧采用：Gemini CLI、Codex CLI（经 ACP adapter）、Claude Agent（经 Zed's SDK adapter）、GitHub Copilot（public preview）、JetBrains Junie、Cursor、Cline、Goose、Qwen Code、Kimi CLI、Kiro CLI、OpenHands、Mistral Vibe 等 40+ | src: https://agentclientprotocol.com/overview/agents | quote: "Agents implementing the Agent Client Protocol" | type: official
- [C8] Client/编辑器侧：Zed、JetBrains（AI Assistant）、Neovim（CodeCompanion/avante 等插件）、Emacs（agent-shell.el）、VS Code 多个扩展、Sublime Text、Obsidian、Qt Creator、Pulsar | src: https://agentclientprotocol.com/overview/clients | type: official
- [C9] 官方 SDK：Kotlin、Java、Python、Rust（agent-client-protocol crate）、TypeScript（@agentclientprotocol/sdk）；另有社区库与 ACP Registry | src: https://github.com/agentclientprotocol/agent-client-protocol | type: official

### OpenAI/Stripe ACP = Agentic Commerce Protocol
- [C10] 全称 Agentic Commerce Protocol；连接 buyers、其 AI agents 与 businesses 完成购买 | src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol | quote: "an interaction model and open standard for connecting buyers, their AI agents, and businesses to complete purchases seamlessly" | type: official
- [C11] OpenAI 与 Stripe 共同开发并维护；Apache-2.0，需 CLA；有 SEP（Spec Enhancement Proposal）治理流程；OpenAI 是首个实现的 AI 平台（ChatGPT），Stripe 是首个兼容 PSP（Shared Payment Token） | src: https://agenticcommerce.dev | quote: "Stripe and OpenAI developed the Agentic Commerce Protocol" | type: official
- [C12] 传输/格式：REST over HTTPS + JSON，"REST and MCP compatible"；商户实现 checkout 端点 POST /checkout_sessions、/{id}、/complete、/cancel + order webhook | src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol rfcs/rfc.agentic_checkout.md | quote: "Create — POST /checkout_sessions initializes a session" | type: official
- [C13] 核心抽象：Agentic Checkout Spec（checkout session 生命周期 create/update/retrieve/complete/cancel + order_create/order_update webhook）、Delegate Payment Spec（PSP 处理安全支付令牌）、product feed、capability negotiation、extensions/discounts/payment handlers | src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol | type: official
- [C14] 版本：日期版本 YYYY-MM-DD；初版 2025-09-29；最新稳定 2026-04-17（cart, feed, orders, authentication, and MCP）；状态 beta | src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol | quote: "ACP uses date-based versioning in YYYY-MM-DD format" | type: official
- [C15] 鉴权/安全：请求头 Authorization: Bearer（REQUIRED）、Idempotency-Key、API-Version、Signature+Timestamp 请求签名；委托支付用令牌化凭证；商户保持 merchant of record | src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol rfc | quote: "The merchant remains the system of record for all orders, payments, taxes, and compliance." | type: official
- [C16] OpenAI 开发者文档确认该协议驱动 ChatGPT 商务流 | src: https://developers.openai.com/commerce/ | quote: "Build commerce flows for ChatGPT, including agentic checkout, delegated payment, and product feeds" | type: official
- [C17] Stripe 文档将 ACP 与 UCP（ucp.dev）并列为 "sell through agents" 可用协议；Stripe 侧还有 MPP/x402 机器支付路线 | src: https://docs.stripe.com/agentic-commerce | quote: "Protocol used | UCP or ACP" | type: official

### AGNTCY ACP = Agent Connect Protocol
- [C18] 全称 Agent Connect Protocol；定义"通过 API 调用和配置远程 agent 的标准接口"，OpenAPI/REST 规范 | src: https://github.com/agntcy/acp-spec | quote: "The Agent Connect Protocol defines a standard interface to invoke and configure remote agents over an API." | type: official
- [C19] Spec 版本 0.2.3；端点 /agents/search、/agents/{id}/descriptor、/threads（CRUD+history+copy）、/threads/{id}/runs（含 /stream、/wait、/cancel）、无状态 /runs、/runs/stream；schema：Agent、AgentACPDescriptor、Thread、Run（stateful/stateless）、Message、RunInterrupt | src: https://raw.githubusercontent.com/agntcy/acp-spec/main/openapi.json | type: official
- [C20] 治理：agntcy org（Apache-2.0，LICENSE 版权为 "Copyright (c) 2025 Cisco and/or its affiliates"）；AGNTCY 为 Linux Foundation 项目（LF Projects, LLC），TSC 含 Cisco、Dell、Google、Oracle、Red Hat；Cisco 与 LangChain、Galileo 发起 | src: https://github.com/agntcy/acp-spec | quote: "the specification of Agent Connect Protocol (ACP) proposed by the Agntcy Collective" | type: official
- [C21] 状态存疑：acp-spec 最后 push 2025-05-23；agntcy.org 当前组件列表（Directory、SLIM、Identity、Observability、AgentBridge-over-A2A）未提 ACP；docs 上 ACP 页面 404——似已被 SLIM/A2A 取代但无正式废弃声明 | src: https://agntcy.org | quote: "Client libraries and bindings across Directory, SLIM, OASF, Observability, Evaluation, and Identity" | type: official

### IBM ACP = Agent Communication Protocol
- [C22] 全称 Agent Communication Protocol；连接 AI agents、applications 与 humans；由 IBM BeeAI 项目（i-am-bee org）贡献者开发，驱动 BeeAI Platform | src: https://github.com/i-am-bee/acp | quote: "ACP is an open protocol for communication between AI agents, applications, and humans." | type: official
- [C23] 基于 REST：工具包含 OpenAPI 规范（REST 端点、请求/响应格式、数据模型），Python/TS SDK 以 acp-sdk 发布 PyPI/npm；能力：多模态消息、流式响应、能力发现、长任务协作、状态共享 | src: https://github.com/i-am-bee/acp | type: official
- [C24] 现状：仓库 2025-08-27 归档只读；官方横幅宣告并入 A2A | src: https://github.com/i-am-bee/acp | quote: "ACP is now part of A2A under the Linux Foundation!" | type: official

### 横向结论
- [C25] 四个 ACP 是不同协议、不同层：Zed ACP=IDE↔agent（JSON-RPC/stdio）；OpenAI/Stripe ACP=agent↔商户支付（REST）；AGNTCY ACP=agent↔agent 调用配置（REST/OpenAPI，疑似弃）；IBM ACP=agent↔agent+人（REST，已并入 A2A/LF） | src: 见上 | type: official

## conflicts
- 无实质冲突。注意点：Stripe 文档同时列 UCP 与 ACP 为可选协议（C17），提示 OpenAI/Stripe ACP 可能面临同生态竞争协议，非冲突。

## gaps
- OpenAI 官宣页 openai.com/index/buy-it-in-chatgpt 返回 403，无法取 Instant Checkout 上线日期/Etsy/Shopify 商户名单原句；仓库 changelog 显示规范初版 2025-09-29（与官宣同日，但未直接引用）。
- Zed ACP 的 authMethods 具体枚举值（OAuth/agent 自定义）未取到原句。
- AGNTCY ACP 是否有正式 deprecation/迁移声明未找到（docs.agntcy.org ACP 页 404；spec.acp.agntcy.org 为 JS 渲染无法抓取正文）。
- IBM ACP 归入 LF AI & Data 的具体时间/公告未核（README 页脚提及隶属 LF AI & Data）。

## leads
- Stripe 文档出现 UCP（ucp.dev）"Universal Commerce Protocol"，可能与 ACP 并列/竞争，值得单独一行。
- AGNTCY AgentBridge 现在走 A2A 连接 coding agent，AGNTCY 自家 ACP 让位迹象明显。
- Zed ACP 仓库同时存在 schema/v2 构件（协议稳定版仍为 1），需关注 v2 是否预示 wire 升级。
