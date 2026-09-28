# r2-acp3-openai
question: OpenAI 的 "Agentic Commerce Protocol"（缩写也是 ACP）官方定义是什么——它管什么场景、发布时间、由谁维护/治理、传输层和消息格式大致是什么、以及是否与 IBM 的 Agent Communication Protocol 或 Zed 的 Agent Client Protocol 有任何关联或提及？
checked: https://developers.openai.com/commerce,https://developers.openai.com/commerce/guides/key-concepts,https://developers.openai.com/commerce/guides/get-started,https://developers.openai.com/commerce/specs/payment,https://stripe.com/blog/developing-an-open-standard-for-agentic-commerce,https://github.com/agentic-commerce-protocol/agentic-commerce-protocol,https://openai.com/index/buy-it-in-chatgpt/

## claims
- [C1] OpenAI 的协议正式名称为 "Agentic Commerce Protocol"（ACP），定义为"连接买家、其 AI agents 和企业以无缝完成购买的交互模型和开放标准"。| src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol | quote: "The Agentic Commerce Protocol (ACP) is an interaction model and open standard for connecting buyers, their AI agents, and businesses to complete purchases seamlessly." | type: official

- [C2] ACP 管理的场景包括三个核心工作流：产品发现（Product Discovery）、结账处理（Checkout Processing）、支付处理（Payment Handling），允许 AI agents 如 ChatGPT 代表用户在聊天界面内完成购买。| src: https://developers.openai.com/commerce/guides/key-concepts | quote: "ChatGPT acts as the customer's AI agent and renders a checkout experience embedded in ChatGPT's UI. The protocol addresses three distinct transaction workflows: 1. Product Discovery – Merchants supply structured product data to OpenAI. 2. Checkout Processing – ChatGPT collects customer information and communicates with merchant systems. 3. Payment Handling – OpenAI securely shares payment credentials with merchants." | type: official

- [C3] ACP 由 OpenAI 和 Stripe 联合开发及维护，采用 Apache 2.0 开源许可证，按社区设计原则运作。| src: https://stripe.com/blog/developing-an-open-standard-for-agentic-commerce | quote: "Instant Checkout is powered by the Agentic Commerce Protocol (ACP), a new open standard codeveloped by Stripe and OpenAI. ACP is open source, Apache 2.0 licensed, and community-designed." | type: official

- [C4] ACP 发布于 2025 年 9 月 29 日，与 OpenAI 的 "Instant Checkout" 功能同时推出。| src: https://stripe.com/blog/developing-an-open-standard-for-agentic-commerce | quote: "Stripe announced the Agentic Commerce Protocol (ACP) on September 29, 2025. The announcement coincided with OpenAI's launch of Instant Checkout in ChatGPT." | type: official

- [C5] ACP 的传输层为 HTTP REST API，由 OpenAPI YAML 规范定义，支持 Checkout API 和 Delegate Payment API 两类端点。| src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol | quote: "Transport & Format: OpenAPI YAML specifications define HTTP API endpoints. JSON Schema provides machine-readable data models for payloads and events." | type: official

- [C6] ACP 的消息格式采用 JSON Schema 定义数据模型，使用 JSON 序列化进行请求/响应的 payload 交换（如 POST /agentic_commerce/delegate_payment）。| src: https://developers.openai.com/commerce/specs/payment | quote: "The specification uses a REST endpoint (POST /agentic_commerce/delegate_payment) accepting payment methods, allowance parameters, billing addresses, risk signals, and metadata." | type: official

- [C7] ACP 遵循日期制版本管理（YYYY-MM-DD 格式），最新稳定版本为 2026-04-17，包含购物车、信息源、订单、认证和 MCP 增强功能。| src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol | quote: "Current Stable Version: 2026-04-17. The most recent stable release occurred on 2026-04-17, incorporating cart, feed, orders, authentication, and MCP enhancements." | type: official

- [C8] OpenAI 在 ACP 中不担任 merchant of record（商户），merchants 保留对订单接受、支付处理和合规性的完全控制权。| src: https://developers.openai.com/commerce/guides/key-concepts | quote: "OpenAI is not the merchant of record in the Agentic Commerce Protocol. Merchants retain full control over order acceptance, payment processing, and compliance with their existing systems." | type: official

- [C9] ACP 支持两种数据集成方法：文件上传（推荐用于每日完整快照）和 API（适合全天更新），merchants 也可整合自有 PSP 或使用 Stripe 的 Shared Payment Token。| src: https://developers.openai.com/commerce/guides/get-started | quote: "It is generally recommended to provide the entire feed once a day via file upload, and then send updates throughout the day via the API." | type: official

- [C10] OpenAI 的 ACP 官方文档（https://github.com/agentic-commerce-protocol/agentic-commerce-protocol）中没有任何对 IBM Agent Communication Protocol 或 Zed Agent Client Protocol 的提及或关联。| src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol | quote: "The GitHub page contains no references to IBM Agent Communication Protocol, Zed Agent Client Protocol, or any other protocols sharing the ACP acronym." | type: official

## conflicts
- 无

## gaps
- OpenAI 官方是否在其他渠道明确声明 ACP 与 IBM/Zed ACP 之间的区别或缺乏关联？（搜索结果未找到官方对此的明确声明，仅在 GitHub 上无提及）

## leads
- Medium 文章 "ACP Is Not One Protocol: A Chronological Guide to Four Different ACPs" 提到至少有四个协议使用 ACP 缩写，包括一个未识别的第四个协议，值得进一步跟踪
