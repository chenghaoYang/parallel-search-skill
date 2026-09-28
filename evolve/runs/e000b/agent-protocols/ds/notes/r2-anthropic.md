# r2-anthropic
question: Anthropic 对 A2A 有没有官方立场？Claude Code 支持 ACP-Zed（Zed 的 Agent Client Protocol）这件事，Anthropic 自己的渠道（不是 Zed 那边）有没有确认（changelog、文档、博客）？Claude Agent SDK "served over AG-UI" 这件事，Anthropic 自己有没有确认（不是 AG-UI 官方集成页那边单方面说的）？
checked: zed.dev/blog/claude-code-via-acp, anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai, platform.claude.com/docs/en/managed-agents, code.claude.com/docs/en/overview, github.com/anthropics/claude-code/releases, github.com/anthropics/claude-agent-sdk-python/blob/main/CHANGELOG.md, anthropic.com/news/model-context-protocol

## claims
- [C1] Anthropic 赞助了关于"如何构建和连接可协作工作的 AI agents"的 webinar（2025-08-27），涉及 MCP 和 A2A 与 Claude on Vertex AI 的实现 | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "how to build and connect AI agents that collaborate together to create high-performing, multi-agent systems." | type: official
- [C2] MCP 是 Anthropic 创建的开放标准，用于连接 AI assistants 和数据源 | src: https://www.anthropic.com/news/model-context-protocol | quote: "open standard developed by Anthropic that enables secure connections between AI assistants and data sources" | type: official
- [C3] Anthropic 于 2025-12-01 左右将 MCP 捐献给 Linux Foundation 的 Agentic AI Foundation | src: 搜索结果综合 | type: secondary
- [C4] Claude Code 在 Zed 中的集成是通过 Zed 构建的适配器实现，而不是 Anthropic 官方采纳 ACP-Zed 标准 | src: https://zed.dev/blog/claude-code-via-acp | quote: "built an adapter that wraps Claude Code's SDK and translates its interactions into ACP's JSON RPC format" | type: secondary
- [C5] Zed 于 2025-09-03 宣布 Claude Code Beta 支持（通过 ACP） | src: https://zed.dev/blog/claude-code-via-acp | quote: "Claude Code is now available in public beta within Zed through the Agent Client Protocol (ACP)... Publication Date: September 3rd, 2025" | type: secondary

## conflicts
- A2A 协议归属问题：搜索结果表明 A2A 是 Google 于 2025-04-09 宣布并后来捐献给 Linux Foundation 的协议，而非 Anthropic 创建；Anthropic 通过 MCP 参与代理生态，但 MCP 和 A2A 是不同的协议。Anthropic 在 webinar 中讨论两个协议的并行应用，但官方文档未声称拥有或发起 A2A。

## gaps
- Anthropic 官方渠道（blog、docs、changelog）是否有关于"Claude Code 支持 ACP-Zed"的确认声明（除 Zed 一侧的公告外）
- Anthropic 官方渠道是否有关于"Claude Agent SDK 通过 AG-UI 提供"或"served over AG-UI"的确认（AG-UI GitHub issue #439 是社区请求，非 Anthropic 官方声明）
- Anthropic 对 A2A 协议采用的正式立场文档

## leads
- AG-UI GitHub issue #439（https://github.com/ag-ui-protocol/ag-ui/issues/439）显示社区建议将 Claude Agent SDK 集成到 AG-UI，但未见 Anthropic 官方参与或确认这一集成实现
- Claude Platform Managed Agents 文档未提及与 AG-UI 的集成关系
