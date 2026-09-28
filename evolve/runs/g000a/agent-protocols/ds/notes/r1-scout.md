# r1-scout
question: 在 MCP / A2A / ACP / AG-UI 这个范围内，找出下一轮必须打开的官方页面：四家大厂各自怎么表态，以及用户会跟这四个缩写搞混的其他协议或自家变体。只做识别，不摘规范字段。
checked: https://developers.openai.com/commerce, https://developers.openai.com/commerce/guides/get-started, https://developers.openai.com/commerce/guides/key-concepts, https://developers.openai.com/apps-sdk, https://developers.openai.com/plugins/concepts/mcp-server, https://www.agenticcommerce.dev/, https://claude.com/docs/connectors/overview, https://claude.com/blog/agent-capabilities-api, https://a2a-protocol.org/latest/, https://adk.dev/mcp/, https://ap2-protocol.org/, https://ucp.dev/, https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent, https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/activity-protocol, https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/, https://code.visualstudio.com/docs/copilot/customization/mcp-servers, https://docs.ag-ui.com/introduction, https://modelcontextprotocol.io/extensions/apps/overview, https://agent-network-protocol.com/, https://nlip-project.org/, https://github.com/langchain-ai/agent-protocol

## claims
- [C1] OpenAI 把 MCP 定成开放规范。 | src: https://developers.openai.com/plugins/concepts/mcp-server | quote: "The Model Context Protocol (MCP) is an open specification for connecting AI clients to external tools and data." | type: official
- [C2] OpenAI 把商户集成称作 ACP。无页内日期。 | src: https://developers.openai.com/commerce/guides/get-started | quote: "Start your ACP integration by sharing a structured product feed with OpenAI." | type: official
- [C3] ACP 站：Stripe 与 OpenAI 制定的 agent 与商家共同语言。 | src: https://www.agenticcommerce.dev/ | quote: "Stripe and OpenAI developed the Agentic Commerce Protocol to define a common language for how agents and businesses transact—including coordinating checkout and securely sharing payment credentials." | type: official
- [C4] apps-sdk URL 现标题为 Plugins，不是新协议名。 | src: https://developers.openai.com/apps-sdk | quote: "Build and publish plugins with skills, MCP servers, and optional UI." | type: official
- [C5] Claude Connectors 由 Anthropic 创建的 MCP 驱动。 | src: https://claude.com/docs/connectors/overview | quote: "They are powered by the Model Context Protocol (MCP), an open standard created by Anthropic that provides a unified way for AI applications to interact with the outside world." | type: official
- [C6] ADK 把 MCP 定成 Gemini/Claude 连接外部系统的开放标准。 | src: https://adk.dev/mcp/ | quote: "The Model Context Protocol (MCP) is an open standard designed to standardize how Large Language Models (LLMs) like Gemini and Claude communicate with external applications, data sources, and tools." | type: official
- [C7] A2A 是 agent 互操作开放标准。 | src: https://a2a-protocol.org/latest/ | quote: "The Agent2Agent (A2A) Protocol is an open standard for seamless communication and collaboration between AI agents." | type: official
- [C8] A2A 原由 Google 开发，已捐给 Linux Foundation。 | src: https://a2a-protocol.org/latest/ | quote: "A2A was originally developed by Google and donated to the Linux Foundation." | type: official
- [C9] AP2 是 Agent Economy 的开放支付协议。 | src: https://ap2-protocol.org/ | quote: "Agent Payments Protocol (AP2) is an open protocol for the emerging Agent Economy." | type: official
- [C10] UCP 是平台、agent 与商家的共同语言。 | src: https://ucp.dev/ | quote: "The common language for platforms, agents, and businesses." | type: official
- [C11] Copilot Studio 把 A2A 定成开放标准（ms.date 2026-08-26）。 | src: https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent | quote: "The Agent2Agent (A2A) protocol is an open standard for communication and collaboration between agents." | type: official
- [C12] Activity Protocol 是微软自家标准通信协议（updated_at 2026-08-19）。 | src: https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/activity-protocol | quote: "Activity Protocol is a standard communication protocol used across Microsoft in many Microsoft SDKs, services, and clients." | type: official
- [C13] Agent Framework 把 AG-UI 定成网页 agent 协议（ms.date 2026-09-08）。 | src: https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/ | quote: "AG-UI is a protocol that enables you to build web-based AI agent applications with advanced features like real-time streaming, state management, and interactive UI components." | type: official
- [C14] VS Code 把 MCP 定成开放标准（页脚 9/16/2026）。 | src: https://code.visualstudio.com/docs/copilot/customization/mcp-servers | quote: "Model Context Protocol (MCP) is an open standard for connecting AI models to external tools and services." | type: official
- [C15] MCP Apps 是核心 MCP 的扩展。 | src: https://modelcontextprotocol.io/extensions/apps/overview | quote: "MCP Apps is an extension to the core MCP specification." | type: official
- [C16] NLIP 首页定为厂商中立的智能体通信协议；未展开全称。 | src: https://nlip-project.org/ | quote: "Open, vendor-neutral protocol for intelligent agent communications." | type: official

## conflicts
- AP2 同页扩展对象不一致。https://ap2-protocol.org/ quote: "The protocol is available as an extension for the open-source Agent2Agent (A2A) protocol and Universal Commerce Protocol with more integrations in progress." 又写 quote: "As a non-proprietary, open extension for A2A and MCP, AP2 fosters a competitive environment for innovation, broad merchant reach, and user choice."
- A2A 全称不一致：a2a-protocol.org 写 Agent2Agent；docs.ag-ui.com/introduction 表内写 Agent to Agent；Copilot Studio 同页兼有 Agent-to-Agent。

## gaps
- OpenAI：未见 Responses/Agents API 被称作互操作协议，也未见自有 A2A/AG-UI 页。搜索：site:openai.com OR site:developers.openai.com "A2A" OR "AG-UI"。buy-it 页空；codex/mcp 跳到 learn.chatgpt.com，正文未取。
- Anthropic：未见 A2A/ACP/AG-UI 产品页。docs.anthropic.com MCP 路径跳到 modelcontextprotocol.io，正文未取。
- Google 商家 UCP 指南未打开。google.github.io/adk-docs/mcp 跳到 adk.dev/mcp。
- Semantic Kernel 未打开。搜索：Semantic Kernel MCP A2A site:learn.microsoft.com。Foundry 端点页未打开。
- agents.json 无已打开官方首页。搜索："agents.json" official protocol homepage。ECMA-430 未打开。

## leads
- agentic-commerce-protocol | OpenAI/Stripe 的 ACP 规范仓库，不同于 IBM/Zed 的 ACP | https://github.com/agentic-commerce-protocol/agentic-commerce-protocol
- OpenAI Plugins | Apps SDK 现名 | https://developers.openai.com/plugins/concepts/plugins
- Codex MCP | 正文未取 | https://learn.chatgpt.com/docs/extend/mcp
- OpenAI Agents API | 是否称协议，未打开 | https://openai.com/index/introducing-the-agents-api/
- Anthropic MCP connector | 旧文档域名会跳走 | https://docs.anthropic.com/en/docs/agents-and-tools/mcp-connector
- MCP and A2A webinar | Anthropic 活动提到 A2A，未打开 | https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai
- Agent Payments Protocol (AP2) | 支付协议；扩展对象同页冲突 | https://ap2-protocol.org/ap2/specification/
- Universal Commerce Protocol | 内建 AP2/A2A/MCP | https://ucp.dev/latest/specification/overview/
- Google UCP Guide | 商家采用页，未打开 | https://developers.google.com/merchant/ucp
- Activity Protocol | 微软自家通道协议 | https://github.com/microsoft/Agents/blob/main/specs/activity/protocol-activity.md
- Copilot Studio 对照表 | MCP servers、Activity Protocol、A2A 三条路径 | https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent
- Microsoft Foundry agent | 搜索称默认 Responses 与 A2A；未核验 | https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-foundry-agent
- A2A Hosting | Agent Framework，未打开 | https://learn.microsoft.com/en-us/agent-framework/hosting/agent-to-agent
- MCP Apps | MCP 官方扩展 | https://apps.extensions.modelcontextprotocol.io/
- A2UI | 与 AG-UI 不同的生成式 UI | https://docs.ag-ui.com/concepts/generative-ui-specs
- Agent Network Protocol (ANP) | 另有名为 AP2 的支付适配 | https://agent-network-protocol.com/specs/1.1/agent-payment
- NLIP | 首页未展开全称 | https://github.com/nlip-project/nlip_spec
- ECMA-430 | NLIP 标准，未打开 | https://ecma-international.org/publications-and-standards/standards/ecma-430/
- Agent Protocol | LangChain 服务 API，不是 A2A；README 已读未单列 | https://langchain-ai.github.io/agent-protocol/openapi.json
- agents.txt / agents.json | 未打开，未证明是官方协议 | https://agents-txt.com/spec
