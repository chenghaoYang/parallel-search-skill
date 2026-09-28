# r2-anthropic
question: Anthropic 自己的官方文档说 Claude / API 支持哪些协议（MCP、A2A、两条 ACP、AG-UI），以及除 MCP 之外有没有自家开放规范的原名。
checked: https://www.anthropic.com/news/model-context-protocol, https://platform.claude.com/docs/en/agents-and-tools/mcp-connector, https://code.claude.com/docs/en/mcp, https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai, https://github.com/anthropics/claude-quickstarts/blob/main/managed-agents/copilot-kit-ag-ui/CLAUDE.md, https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills, https://platform.claude.com/docs/en/claude-code/ide-integrations (404), https://api.github.com/search/repositories?q=org:anthropics+acp

## claims
- [C1] MCP 是 Anthropic 创建并开源的协议，原名 Model Context Protocol，2024-11-25 宣布 | src: https://www.anthropic.com/news/model-context-protocol | quote: "Today, we're open-sourcing the Model Context Protocol (MCP), a new standard for connecting AI assistants to the systems where data lives" | type: official
- [C2] MCP 作者署名：Anthropic 的 David Soria Parra 与 Justin Spahr-Summers | src: https://www.anthropic.com/news/model-context-protocol | quote: "MCP was created at Anthropic by David Soria Parra and Justin Spahr-Summers." | type: official
- [C3] Claude API 通过 MCP connector 支持远程 MCP 服务器：Messages API 加 mcp_servers 数组与 mcp_toolset 工具类型，beta header mcp-client-2025-11-20（另有 mcp-client-2026-09-15 可 pin 工具列表）；仅支持 tool calls，服务器须公网 HTTP；Amazon Bedrock 与 Google Cloud not available | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: "Claude's Model Context Protocol (MCP) connector feature enables you to connect to remote MCP servers directly from the Messages API without a separate MCP client." | type: official
- [C4] Claude Code 支持连接 MCP 服务器：claude mcp add，transport 有 http / sse / ws / stdio，配置写 .mcp.json 或 ~/.claude.json | src: https://code.claude.com/docs/en/mcp | quote: "Claude Code can connect to hundreds of external tools and data sources through the Model Context Protocol (MCP), an open source standard for AI-tool integrations." | type: official
- [C5] 自家 MCP 扩展（非独立协议）：Claude Code 支持服务器声明 claude/channel 能力向会话推消息，--channels 启用 | src: https://code.claude.com/docs/en/mcp | quote: "your server declares the `claude/channel` capability and you opt it in with the `--channels` flag at startup" | type: official
- [C6] A2A：Anthropic 官网仅在与 Google Cloud 的联合 webinar（2025-08-27）提及 A2A，定位与 MCP 互补，场景是 Claude on Vertex AI；无 API/SDK 级支持表述 | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "the practical implementation of multi-agent systems using Model Context Protocol (MCP) and Agent-to Agent protocol (A2A) with Claude on Vertex AI" | type: official
- [C7] AG-UI：官方仓库 anthropics/claude-quickstarts 的 managed-agents/copilot-kit-ag-ui 示例把 Claude Managed Agent 经 AG-UI 接入 CopilotKit runtime | src: https://github.com/anthropics/claude-quickstarts/blob/main/managed-agents/copilot-kit-ag-ui/CLAUDE.md | quote: "A finance assistant chat app wiring a Claude Managed Agent to CopilotKit's self-hosted runtime over the AG-UI protocol." | type: official
- [C8] 该示例的 AG-UI 适配层是上游第三方包 @ag-ui/claude-managed-agents，Anthropic 仓库内无自有 bridge 代码 | src: https://github.com/anthropics/claude-quickstarts/blob/main/managed-agents/copilot-kit-ag-ui/CLAUDE.md | quote: "The upstream AG-UI adapter. `@ag-ui/claude-managed-agents` does the whole Managed Agents ↔ AG-UI translation" | type: official
- [C9] 除 MCP 外的自家开放规范：Agent Skills（文件夹 + SKILL.md 的开放格式，非 wire 协议），2025-12-18 以 open standard 发布于 agentskills.io | src: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | quote: "We've published Agent Skills as an open standard for cross-platform portability. (December 18, 2025)" | type: official

## conflicts
- 无：已打开的官方来源之间未见相互矛盾。

## gaps
- ACP-Zed（Agent Client Protocol）：anthropic.com、docs.claude.com、code.claude.com、platform.claude.com 均未提 ACP；api.github.com 搜 org:anthropics+acp 返回 0 repo；Claude Code 文档仅在 terminal-config 提到 Zed（Shift+Enter keymap，与协议无关）。查询："Claude Agent Client Protocol"、"Zed OR Agent Client Protocol site:docs.claude.com OR platform.claude.com OR code.claude.com"。
- ACP-IBM（Agent Communication Protocol / BeeAI）：Anthropic 域名无任何提及。查询："Agent Communication Protocol" IBM BeeAI site:anthropic.com OR site:github.com/anthropics → 无结果。
- AG-UI 无产品级文档条目，只有 quickstarts 示例（C7）。
- docs.claude.com/en/docs/mcp 整页重定向到 modelcontextprotocol.io，规范正文按简报未重读。

## leads
- ACP adapter 现行仓库为 github.com/agentclientprotocol/claude-agent-acp（原 zed-industries/claude-code-acp），npm 包 @agentclientprotocol/claude-agent-acp；ACP-Zed×Anthropic 格可用非白名单来源补。
- 文档域名现状：API 文档在 platform.claude.com（docs.claude.com 重定向），Claude Code 文档在 code.claude.com（docs.anthropic.com 重定向）。
- claude.ai/directory 是官方 MCP connector 目录；MCP connector 在 Bedrock/Google Cloud 标 not available，跨云支持有差异。
