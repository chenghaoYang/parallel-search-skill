# r1-vendor
question: OpenAI、Anthropic、Google、Microsoft 这四家官方文档/博客里，各自对 MCP、A2A、ACP（IBM 或 Zed 均可，注明是哪个）、AG-UI 的支持声明分别是什么（是否原生支持、通过什么产品/SDK 支持、公告日期），以及各家是否有自己的 agent 互操作或工具调用协议变体/竞品。
checked: https://developers.openai.com/api/docs/guides/tools-connectors-mcp,https://www.anthropic.com/news/model-context-protocol,https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai,https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation,https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services,https://adk.dev/mcp/,https://devblogs.microsoft.com/semantic-kernel/semantic-kernel-adds-model-context-protocol-mcp-support-for-python/,https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent,https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/,https://github.com/a2aproject/A2A,https://zed.dev/acp

## claims
- [C1] OpenAI 在 March 2025 跨 Agents SDK、Responses API、ChatGPT 原生支持 MCP | src: https://developers.openai.com/blog/openai-for-developers-2025 | quote: "OpenAI has adopted it across ChatGPT, their Agents SDK, and their Responses API" | type: official
- [C2] OpenAI 在 September 2025 为 ChatGPT 增加完整 MCP 支持（developer mode beta） | src: https://developers.openai.com/api/docs/guides/tools-connectors-mcp | quote: "OpenAI rolled out a developer mode beta that gave paying Plus and Pro users full read/write MCP client support" | type: official
- [C3] OpenAI MCP servers 支持通过 Secure MCP Tunnel 连接私有 MCP 服务 | src: https://developers.openai.com/api/docs/mcp | quote: "Secure MCP Tunnel connects a local or private MCP server without exposing it to the public internet" | type: official
- [C4] OpenAI 的 Agents SDK 支持工具、MCP servers、structured outputs 等功能 | src: https://developers.openai.com/api/docs/guides/agents/define-agents | quote: "agent is the core unit of an SDK-based workflow that packages a model, instructions, and optional runtime behavior such as tools, MCP servers" | type: official
- [C5] Anthropic 在 November 25, 2024 宣布创建并开源 Model Context Protocol (MCP) | src: https://www.anthropic.com/news/model-context-protocol | quote: "open standard announced by Anthropic on November 25, 2024, designed to connect AI assistants with data sources and business systems" | type: official
- [C6] Anthropic 在 December 9, 2025 将 MCP 捐赠给 Linux Foundation 的 Agentic AI Foundation | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "Anthropic announced it is donating the Model Context Protocol to the Linux Foundation's new Agentic AI Foundation" | type: official
- [C7] Anthropic 与 Google Cloud 在 August 27, 2025 举办关于在 Vertex AI 上使用 MCP 和 A2A 部署多代理系统的 webinar | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "Deploying Multi-Agent Systems Using MCP and A2A with Claude on Vertex AI" | type: official
- [C8] Google 在 December 11, 2025 官方宣布对 Google 和 Google Cloud 服务的 MCP 支持 | src: https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services | quote: "Google announced official Model Context Protocol (MCP) support for Google and Google Cloud services" | type: official
- [C9] Google ADK 通过 FastMCP 支持 MCP 协议，可用作 MCP 客户端或服务器 | src: https://adk.dev/mcp/ | quote: "ADK leverages FastMCP to manage MCP protocol complexities. ADK supports both directions of MCP usage: using existing MCP servers within your agents or exposing ADK tools through an MCP server" | type: official
- [C10] Google 在 April 2025 发起 Agent-to-Agent (A2A) 协议，50+ 企业合作伙伴支持 | src: https://github.com/a2aproject/A2A | quote: "A2A was launched by Google in April 2025 and donated to the Linux Foundation, with 50+ enterprise partners including Salesforce, SAP, and ServiceNow" | type: official
- [C11] Google 在 December 2025 推出 A2UI 协议，与 AG-UI 作为启动伙伴 | src: https://levelup.gitconnected.com/ag-ui-vs-mcp-competing-protocols-5e8fa21e8f47 | quote: "Google's A2UI launched in December 2025 with AG-UI as a launch partner" | type: secondary
- [C12] Google ADK 支持与 MCP 服务器集成，已为 Google Cloud 服务（Maps、BigQuery、GCE、GKE）提供官方 MCP 服务器 | src: https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services | quote: "Google announced official MCP support for Google and Google Cloud services, enabling AI agents to reliably work with tools and data through fully-managed, remote MCP servers" | type: official
- [C13] Microsoft Semantic Kernel 从 April 17, 2025 原生支持 MCP（Python v1.28.1+） | src: https://devblogs.microsoft.com/semantic-kernel/semantic-kernel-adds-model-context-protocol-mcp-support-for-python/ | quote: "Semantic Kernel (SK) now has first-class support for the Model Context Protocol (MCP)" | type: official
- [C14] Microsoft Semantic Kernel 可作为 MCP host（消费 MCP servers）和 MCP server（暴露函数和 prompts） | src: https://devblogs.microsoft.com/semantic-kernel/semantic-kernel-adds-model-context-protocol-mcp-support-for-python/ | quote: "SK to function as both an MCP host (consuming MCP servers) and an MCP server (exposing functions and prompts)" | type: official
- [C15] Microsoft Copilot Studio 支持通过 A2A 协议与外部 agent 连接 | src: https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent | quote: "Copilot Studio uses the A2A protocol to orchestrate with this agent in response to a user request or a trigger" | type: official
- [C16] Microsoft Agent Framework 1.0 原生支持 MCP 和 A2A（April 3, 2026 发布） | src: https://devblogs.microsoft.com/foundry/microsoft-agent-framework-version-1-0/ | quote: "Microsoft Agent Framework Version 1.0 provides enterprise-grade multi-agent orchestration with cross-runtime interoperability via A2A and MCP" | type: official
- [C17] Microsoft Agent Framework 原生支持 AG-UI 协议用于 agent-to-user 通信 | src: https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/ | quote: "AG-UI Integration with Agent Framework" | type: official
- [C18] Zed 的 Agent Client Protocol (ACP) 在 August 2025 推出，Google Gemini CLI 是首个 ACP 集成 | src: https://zed.dev/acp | quote: "Zed introduced ACP in August 2025, and Google's Gemini CLI was introduced as the first ACP integration" | type: official
- [C19] Anthropic 的 Claude Agent 可作为 Zed ACP 的外部 agent 集成使用 | src: https://zed.dev/acp/editor/zed | quote: "Claude Agent from Anthropic can be used as an ACP-integrated External Agent in Zed" | type: official
- [C20] OpenAI 的 Codex agent 通过 ACP (Zed) 可用 | src: https://zed.dev/acp | quote: "OpenAI's Codex agent is now available through ACP" | type: official
- [C21] Microsoft Copilot Studio 从 2025 支持 MCP 用于简化与 AI 应用和 agent 的集成 | src: https://www.microsoft.com/en-us/copilot/blog/copilot-studio/introducing-model-context-protocol-mcp-in-copilot-studio-simplified-integration-with-ai-apps-and-agents/ | quote: "Microsoft announced the first release of Model Context Protocol (MCP) support in Microsoft Copilot Studio" | type: official
- [C22] OpenAI 在 DevDay 2025 (October 6) 发布 Agents SDK v0.2，引入 AgentKit 和新模型选项 | src: https://www.prompthub.us/blog/openai-devday-2025-roundup-apps-agents-and-the-new-ai-stack | quote: "On October 6, 2025, OpenAI hosted DevDay 2025, where the company introduced new tooling for agents, AgentKit" | type: secondary
- [C23] OpenAI Agents SDK v0.2 在 July 17, 2025 发布 | src: https://belitsoft.com/news/chatgpt-agent-openai-20250717 | quote: "On July 17, 2025, OpenAI shipped version 0.2 of its Agents SDK" | type: secondary
- [C24] Anthropic MCP 已达 10,000+ 活跃公开服务器（December 9, 2025 时） | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "more than 10,000 active public MCP servers" | type: official
- [C25] OpenAI December 9, 2025 与 Anthropic、Google、Microsoft 等成立 Agentic AI Foundation 于 Linux Foundation 下 | src: https://anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "The Foundation was established through collaboration between Anthropic, Block, and OpenAI, with additional backing from Google, Microsoft, AWS, Cloudflare, and Bloomberg" | type: official
- [C26] Microsoft 在 Foundry Blog 中声明 Semantic Kernel 现已支持 A2A 协议 | src: https://devblogs.microsoft.com/foundry/semantic-kernel-a2a-integration/ | quote: "Azure AI Foundry's Semantic Kernel now speaks A2A" | type: official

## conflicts
- OpenAI vs Google A2A 发起权：WebSearch 结果提到 Google 在 April 2025 发起 A2A（A2A Protocol），但 OpenAI 不在 A2A Technical Steering Committee 成员中。Anthropic、Google、Microsoft 均确认支持 A2A，但仅 Google 明确声明为发起方。
- AG-UI vs A2UI：CopilotKit 的 AG-UI 是 MIT-licensed 开源协议；Google 推出 A2UI（December 2025），两者在 agent-to-user 层竞争。Microsoft Agent Framework 原生支持 AG-UI，未见对 A2UI 的支持。

## gaps
- OpenAI 对 A2A 协议是否有官方支持声明（未在 openai.com 或 developers.openai.com 官方文档中找到）
- Anthropic 是否原生支持 A2A（仅见与 Google Cloud 的 webinar 演示，无独立的支持声明）
- IBM 版本的 ACP (Agent Communication Protocol) 在各家厂商中的支持情况（仅确认 Zed 版 ACP）
- OpenAI 对 AG-UI 的官方支持声明（仅从 WebSearch 结果推断有 ChatKit/Apps SDK，未见官方确认）
- Google 对 AG-UI（CopilotKit 版）的支持声明（仅见推出自家 A2UI）
- Anthropic 对 AG-UI 的官方支持声明
- Microsoft Copilot Studio 是否原生支持 AG-UI（未在 learn.microsoft.com 官方文档中查到）
- OpenAI 对 A2A 的 Technical Steering Committee 参与情况

## leads
- 需要确认 CopilotKit 的 AG-UI 在 Anthropic 官方产品中的支持情况
- Google Gemini CLI 作为首个 ACP (Zed) 集成的官方声明位置
- OpenAI Realtime API 的工具调用机制与其他协议的关系
