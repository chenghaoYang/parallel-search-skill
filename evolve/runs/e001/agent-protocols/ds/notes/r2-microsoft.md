# r2-microsoft
question: Microsoft 官方对 MCP、A2A、ACP（任一）、AG-UI 的支持情况分别是什么？请在以下产品线找证据：Windows、Copilot Studio、Azure AI Foundry (Agent Service)、Microsoft Agent Framework、Semantic Kernel

checked: https://learn.microsoft.com/en-us/windows/ai/mcp/overview, https://www.microsoft.com/en-us/copilot/blog/copilot-studio/model-context-protocol-mcp-is-now-generally-available-in-microsoft-copilot-studio/, https://devblogs.microsoft.com/foundry/announcing-model-context-protocol-support-preview-in-azure-ai-foundry-agent-service/, https://learn.microsoft.com/en-us/azure/foundry/agents/overview, https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/, https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-mcp-plugins, https://github.com/microsoft/agent-host-protocol/blob/main/docs/guide/ahp-and-acp.md, https://github.com/microsoft/nlweb, https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/agents-sdk-overview, https://devblogs.microsoft.com/visualstudio/mcp-is-now-generally-available-in-visual-studio/, https://github.com/microsoft/mcp, https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp, https://learn.microsoft.com/en-us/agent-framework/overview/

## claims
- [C1] Copilot Studio MCP 一般可用，发布日期 May 29, 2025 | src: https://www.microsoft.com/en-us/copilot/blog/copilot-studio/model-context-protocol-mcp-is-now-generally-available-in-microsoft-copilot-studio/ | quote: "Today, we're thrilled to announce the general availability of MCP integration in Copilot Studio" | type: official
- [C2] Windows 支持 MCP 通过 On-device Agent Registry (ODR)，提供安全、可管理的接口用于发现和使用 MCP 服务器 | src: https://learn.microsoft.com/en-us/windows/ai/mcp/overview | quote: "MCP on Windows provides the Windows On-device Agent Registry (ODR), a secure, manageable interface to discover and use agent connectors" | type: official
- [C3] Azure AI Foundry Agent Service 支持 MCP，preview 于 June 27, 2025 宣布 | src: https://devblogs.microsoft.com/foundry/announcing-model-context-protocol-support-preview-in-azure-ai-foundry-agent-service/ | quote: "Announcing Model Context Protocol Support (preview) in Azure AI Foundry Agent Service" | type: official
- [C4] Semantic Kernel 支持 MCP 插件，支持 MCPStdioPlugin 和 MCPStreamableHttpPlugin | src: https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-mcp-plugins | quote: "Semantic Kernel allows you to add plugins from a MCP Server to your agents" | type: official
- [C5] Visual Studio MCP 一般可用，发布日期 August 19, 2025 | src: https://devblogs.microsoft.com/visualstudio/mcp-is-now-generally-available-in-visual-studio/ | quote: "Model Context Protocol (MCP) support became generally available in Visual Studio" | type: official
- [C6] Azure AI Foundry Agent Service 支持 A2A 协议 v1.0（一般可用） | src: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-to-agent-authentication | quote: "The A2A Tool and incoming A2A endpoints support A2A protocol version 1.0, which is generally available" | type: official
- [C7] Microsoft 是 A2A Technical Steering Committee 成员 | src: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/a2a-endpoints-and-a2a-tool-in-microsoft-foundry-agents/4557115 | quote: "Agent-to-agent collaboration just became much easier to build in Microsoft Foundry, and the A2A Tool and incoming A2A endpoints support A2A protocol version 1.0" | type: official
- [C8] NLWeb 支持 A2A，计划支持（"soon A2A"） | src: https://github.com/microsoft/nlweb | quote: "Every NLWeb instance also acts as an MCP server (and soon A2A)" | type: official
- [C9] Microsoft Agent Framework 支持 AG-UI 集成，通过 MapAGUIServer 和 FastAPI 端点实现 .NET/Python/Go | src: https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/ | quote: "The .NET integration exposes a MAF AIAgent as an AG-UI HTTP endpoint" | type: official
- [C10] Microsoft Agent Host Protocol (AHP) 与 ACP 的关系：ACP 是点对点通信协议，AHP 是协调多客户端的层 | src: https://github.com/microsoft/agent-host-protocol/blob/main/docs/guide/ahp-and-acp.md | quote: "ACP is a point-to-point protocol... AHP is a coordination layer. ACP is a communication layer" | type: official
- [C11] NLWeb 是开源项目，是 Schema.org/RSS 与 LLM 工具的结合，支持 MCP 服务器发布内容 | src: https://github.com/microsoft/nlweb | quote: "Every NLWeb instance also acts as an MCP server" | type: official
- [C12] Microsoft 365 Agents SDK 是多通道代理开发框架，支持 C#/JavaScript/Python，但无 MCP 协议支持记录 | src: https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/agents-sdk-overview | quote: "The Microsoft 365 Agents SDK is a development framework for building conversational agents" | type: official
- [C13] Azure AI Foundry Agent Service MCP GA 随 June 2025 Foundry 更新发布 | src: https://devblogs.microsoft.com/foundry/whats-new-in-azure-ai-foundry-june-2025/ | quote: "Agent Service hit GA with Model Context Protocol (MCP) support" | type: official

## conflicts
- 无 ACP 直接支持冲突：Microsoft 产品对 ACP（Agent Communication Protocol）无一手来源记录；Microsoft 有 Agent Host Protocol (AHP) 可使用 ACP 作为后端，但这是 ACP 的客户而非官方支持

## gaps
- Microsoft 365 Agents SDK 是否明确支持 MCP、A2A、AG-UI：官方文档未提及任何协议集成
- Copilot Studio 是否支持 A2A
- Windows ODR 是否支持 A2A
- Semantic Kernel 是否支持 A2A、AG-UI
- Microsoft Agent Framework 是否支持 ACP（仅确认 AG-UI 支持）

## leads
- NLWeb 是 Microsoft 自家新协议相关产物（未来 A2A 支持可能升级）
- Microsoft Agent Host Protocol (AHP) 是 Microsoft 的协调层创新，与 ACP 互补但分职能
- 建议查 Microsoft Foundry Agent Service 完整文档确认 AG-UI 支持
