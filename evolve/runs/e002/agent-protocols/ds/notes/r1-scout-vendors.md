# r1-scout-vendors
question: OpenAI、Anthropic、Google、Microsoft 这四家公司各自在官方文档/博客/发布公告里宣布支持或采用了 MCP、A2A、ACP-IBM/ACP-Zed、AG-UI 这几个协议中的哪些？各自是否有自己的替代/变体框架或协议？
checked: https://developers.openai.com/api/docs/mcp, https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation, https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/, https://azure.microsoft.com/en-us/blog/agent-factory-connecting-agents-apps-and-data-with-new-open-standards-like-mcp-and-a2a/, https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai, https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/mcp, https://developers.googleblog.com/build-cross-language-multi-agent-team-with-google-agent-development-kit-and-a2a/, https://openai.com/index/the-next-evolution-of-the-agents-sdk/, https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/, https://zed.dev/acp, https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/

## claims
- [C1] OpenAI 官方支持 MCP：通过 Responses API、ChatGPT developer mode、插件中提供 MCP 服务器支持 | src: https://developers.openai.com/api/docs/mcp | quote: "support for remote MCP servers" | type: official
- [C2] OpenAI 有官方 Agents SDK 框架：开源框架，支持多语言（Python、TypeScript），用于设计、构建和部署智能体 | src: https://openai.com/index/the-next-evolution-of-the-agents-sdk/ | quote: "The Agents SDK is an orchestration framework for designing, building, and deploying agents" | type: official
- [C3] Anthropic 是 MCP 的创造者和维护者：在 2024 年 11 月推出，后于 2025 年 3 月捐赠给 Linux Foundation 下的 Agentic AI Foundation | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "Anthropic has donated the Model Context Protocol (MCP) to the Agentic AI Foundation" | type: official
- [C4] Anthropic 官方支持 A2A：通过与 Google Cloud 合作的网络研讨会"Deploying multi-agent systems using MCP and A2A with Claude on Vertex AI"提供技术指导和实现支持 | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "Deploying multi-agent systems using MCP and A2A with Claude on Vertex AI" | type: official
- [C5] Google 发起并推动 A2A 协议：2025 年 6 月捐赠给 Linux Foundation，超过 50 家技术合作伙伴支持 | src: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ | quote: "Google launched the Agent2Agent (A2A) protocol on September 17, 2026" | type: official
- [C6] Google 官方支持 MCP：在 Gemini Enterprise Agent Platform、Cloud Assist 和 Workflow Builder 中提供 MCP 服务器支持 | src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/mcp | quote: "MCP Reference: aiplatform.googleapis.com | Gemini Enterprise Agent Platform" | type: official
- [C7] Google 有官方 Agent Development Kit (ADK)：支持多语言（Python、Java、Go、TypeScript），用于构建、调试和部署企业级 AI 智能体 | src: https://developers.googleblog.com/build-cross-language-multi-agent-team-with-google-agent-development-kit-and-a2a/ | quote: "open-source agent development framework...simplify the full stack end-to-end development of agents and multi-agent systems" | type: official
- [C8] Google 有 A2UI（Agent-to-User Interface）协议而非 AG-UI：与 Flutter 团队共同开发的开放协议，用于描述 UI 树结构 | src: https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/ | quote: "A2UI is an open protocol introduced by Google...describes a UI: a tree of components" | type: official
- [C9] Microsoft 官方支持 MCP：在 Copilot Studio、Azure AI Foundry 和 Agent Framework 中支持远程 MCP 服务器 | src: https://azure.microsoft.com/en-us/blog/agent-factory-connecting-agents-apps-and-data-with-new-open-standards-like-mcp-and-a2a/ | quote: "Microsoft Agent Framework...multi-agent orchestration...MCP" | type: official
- [C10] Microsoft 官方支持 A2A：在 Copilot Studio（2025 年 5 月公开预览，2026 年 5 月正式发布）和 Azure AI Foundry 中支持 A2A 协议 | src: https://azure.microsoft.com/en-us/blog/agent-factory-connecting-agents-apps-and-data-with-new-open-standards-like-mcp-and-a2a/ | quote: "A2A (Agent-to-Agent) protocol support enables cross-runtime agent collaboration" | type: official
- [C11] Microsoft 有 Semantic Kernel Agent Framework：Semantic Kernel 1.45+ (.NET) 和 1.27+ (Python) 中的智能体框架，支持多智能体协调 | src: https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/ | quote: "The Semantic Kernel Agent Framework provides a platform...for the creation of AI agents" | type: official
- [C12] Microsoft 有 Microsoft Agent Framework：后继 Semantic Kernel 的企业级平台，用于开发、部署和管理 AI 智能体 | src: https://learn.microsoft.com/en-us/agent-framework/overview/ | quote: "Microsoft Agent Framework is the successor to Semantic Kernel for building AI agents" | type: official
- [C13] OpenAI 未官方支持 ACP-Zed（Agent Client Protocol）：OpenAI 的 Codex/Agents 在 VS Code 中遵循 MCP 标准而非 ACP | src: https://www.theregister.com/2025/08/28/google_zed_acp/ | quote: "Microsoft standardized VS Code's agent mode on MCP rather than ACP" | type: secondary
- [C14] Google 官方支持 ACP-Zed（Agent Client Protocol）：Gemini CLI AI 智能体直接集成到 Zed 编辑器 | src: https://www.theregister.com/2025/08/28/google_zed_acp/ | quote: "Google's Gemini CLI AI agent can now be integrated directly into the Zed code editor" | type: secondary
- [C15] Anthropic 对 ACP-Zed 的支持通过适配器而非原生：Claude Code 通过 Zed 构建的网桥适配器在 ACP 编辑器中运行 | src: https://www.theregister.com/2025/08/28/google_zed_acp/ | quote: "Claude Code works in ACP editors via a bridge adapter built by Zed, as Anthropic has not natively adopted ACP" | type: secondary
- [C16] Microsoft 未官方支持 ACP-Zed：VS Code 团队对原生 ACP 支持的开源问题未有正式承诺 | src: https://www.theregister.com/2025/08/28/google_zed_acp/ | quote: "an open tracking issue for native ACP support has sat without a commitment from the VS Code team" | type: secondary
- [C17] Agentic AI Foundation 的共同创始人是 Anthropic、Block 和 OpenAI，由 Linux Foundation 管理 | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "co-founded by Anthropic, Block and OpenAI, with support from Google, Microsoft, Amazon Web Services (AWS), Cloudflare, and Bloomberg" | type: official
- [C18] ACP-IBM 已于 2025 年 8 月正式并入 A2A 标准，成为统一的代理间通信标准 | src: https://www.ibm.com/think/topics/agent-communication-protocol | quote: "in August 2025, IBM's Agent Communication Protocol (ACP) officially merged with A2A under the Linux Foundation" | type: secondary
- [C19] OpenAI、Anthropic、Google 均不官方声明支持 AG-UI（Agent-User Interaction Protocol）：AG-UI 由 CopilotKit 团队主导，但未见四大厂官方采纳声明 | src: https://www.copilotkit.ai/ag-ui | quote: "AG-UI is an open protocol for connecting AI agents to frontend applications" | type: secondary

## conflicts
- [CF1] Anthropic 的 A2A 支持级别：官方文档中未直接宣称"原生支持"或"创造者"身份，仅通过教育资源（Vertex AI 网络研讨会）体现，而 Google 则明确宣传为"发起方"和"规范维护者"
  - src A (Anthropic): https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai
  - src B (Google): https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/

## gaps
- AG-UI 实际采用情况未明：四大厂官方文档中未找到任何对 CopilotKit 的 AG-UI 协议的支持声明或集成示例
- ACP-Zed 细节缺失：仅从二手源（The Register）了解 Google 原生支持、Anthropic/OpenAI 通过适配器、Microsoft 未支持的信息，未找到各厂官方文档原句
- 是否存在其他四大厂共同推动的协议或基金会机构：除 Agentic AI Foundation（MCP 相关）外，未查到其他标准化组织

## leads
- A2UI 与 AG-UI 的关系待澄清：Google 同时推动 A2A 和 A2UI，但与 AG-UI 是否存在层级关系或竞争关系需进一步调查
- OpenAI 的"Agentic Commerce Protocol (ACP)"与题目中的"ACP-Zed"不是同一物：前者是电商领域的支付协议，需确认搜索范围是否应包含此类细分领域协议
- 各厂商对捐赠给 Linux Foundation 的协议的后续维护义务与话语权分配：是否影响其对协议的"支持"程度认定
