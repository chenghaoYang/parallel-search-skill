# r2-microsoft
question: Microsoft 对 ACP-Zed（Zed 的 Agent Client Protocol）有没有官方立场（VS Code、GitHub Copilot 是否已经或计划接入）？除了 Agent Framework（已确认原生支持 MCP/A2A/AG-UI）之外，Microsoft 有没有其他和这些协议同层、值得记录的自家协议或项目（例如 NLWeb——它是不是一个独立协议，还是构建在 MCP 之上的应用/网站惯例？它和 MCP 的关系是什么）？
checked: https://github.com/microsoft/vscode/issues/265496, https://docs.github.com/en/copilot/reference/copilot-cli-reference/acp-server, https://github.com/microsoft/ai-agents-for-beginners/blob/main/11-agentic-protocols/README.md, https://blogs.microsoft.com/blog/2025/05/19/microsoft-build-2025-the-age-of-ai-agents-and-building-the-open-agentic-web/, https://news.microsoft.com/source/features/company-news/introducing-nlweb-bringing-conversational-interfaces-directly-to-the-web/, https://github.com/nlweb-ai/NLWeb, https://github.com/github/copilot-cli/issues/222

## claims
- [C1] VS Code 对 ACP 支持：GitHub issue #265496（2025年9月6日开启）处于"under-discussion"状态，微软尚未发布官方立场 | src: https://github.com/microsoft/vscode/issues/265496 | quote: "Issue marked as under-discussion" | type: official
- [C2] GitHub Copilot CLI 对 ACP 支持处于公开预览状态：可通过 `--acp` 选项启动 ACP 服务器 | src: https://docs.github.com/en/copilot/reference/copilot-cli-reference/acp-server | quote: "ACP support in GitHub Copilot CLI is in public preview and subject to change." | type: official
- [C3] GitHub Copilot CLI Issue #222（2025年10月6日开启）请求 ACP 支持，但目前该请求已关闭且未实施，无分配开发者或完成时间表 | src: https://github.com/github/copilot-cli/issues/222 | quote: "no assigned developers, no linked pull requests or branches, no milestone or completion timeline" | type: secondary
- [C4] Microsoft Agent Framework 原生支持 MCP、A2A、AG-UI（已确认 R1） | src: https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/ | quote: "MCP support lets agents dynamically discover and invoke external tools" | type: official
- [C5] NLWeb 是微软推出的开源项目，用于为网站创建自然语言接口，返回使用 Schema.org 的 JSON 响应 | src: https://github.com/nlweb-ai/NLWeb | quote: "a simple protocol to interact with a site using natural language. It returns responses in JSON using Schema.org." | type: official
- [C6] 每个 NLWeb 实例都是 MCP 服务器：NLWeb 不是独立协议，而是构建在 MCP 之上的应用/网站惯例 | src: https://news.microsoft.com/source/features/company-news/introducing-nlweb-bringing-conversational-interfaces-directly-to-the-web/ | quote: "Every NLWeb instance is also a Model Context Protocol (MCP) server, allowing websites to make their content discoverable and accessible to agents" | type: official
- [C7] Microsoft Build 2025 宣布对 MCP 提供"广泛的第一方支持"（broad first-party support），涉及 GitHub、Copilot Studio、Azure AI Foundry 和 Windows 11 | src: https://blogs.microsoft.com/blog/2025/05/19/microsoft-build-2025-the-age-of-ai-agents-and-building-the-open-agentic-web/ | quote: "Microsoft is providing broad first-party support for MCP across its platforms including GitHub, Copilot Studio, Azure AI Foundry, and Windows 11." | type: official
- [C8] Copilot Studio 原生支持 MCP：用户可通过"Add a Tool"搜索 MCP 服务器并自动集成 | src: https://www.microsoft.com/en-us/copilot/blog/copilot-studio/model-context-protocol-mcp-is-now-generally-available-in-microsoft-copilot-studio/ | quote: "MCP is now generally available in Microsoft Copilot Studio" | type: official
- [C9] A2A 协议（Agent-to-Agent）是 Microsoft 自有协议，允许不同运行时的代理跨平台通信（如 Python 代理与 .NET 代理协调） | src: https://devblogs.microsoft.com/agent-framework/a2a-v1-is-here-cross-platform-agent-communication-in-microsoft-agent-framework-for-net/ | quote: "A2A Protocol enables agents to communicate across different runtimes. For example, an agent built in Python can seamlessly coordinate with an agent running in a .NET environment." | type: official

## conflicts
- GitHub Copilot CLI ACP 支持状态不清晰：GitHub Copilot CLI 文档声称 ACP 支持处于"public preview"（https://docs.github.com/en/copilot/reference/copilot-cli-reference/acp-server），但相关 GitHub issue #222 显示该功能请求已关闭且未实施。

## gaps
- VS Code 官方是否计划接入 ACP 的明确时间表或承诺声明
- GitHub Copilot Chat 对 ACP 的官方支持状态（Issue #303160 仅表示讨论阶段）
- NLWeb 的完整规范和 v1.0 发布状态
- Microsoft 是否有其他和 MCP/A2A/NLWeb 同层的自有协议项目

## leads
- GitHub issue #265496（VS Code ACP 支持）和 #303160（Copilot Chat ACP 支持）可继续关注官方反应
- NLWeb 的 Registry/Discovery 机制与 MCP 的具体集成方式值得深入研究
- GitHub Copilot CLI 的 ACP 支持状态需要与官方澄清
