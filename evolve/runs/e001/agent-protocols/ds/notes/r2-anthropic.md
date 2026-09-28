# r2-anthropic
question: Anthropic（Claude 的公司）官方对 A2A（Agent2Agent）、ACP（IBM 的 Agent Communication Protocol 或 Zed 的 Agent Client Protocol）、AG-UI 的支持情况是什么（Claude 产品线里是否集成、官方文档/博客原句和 URL）？Anthropic 自己在 MCP 之外还有没有别的协议/规范级产物，例如 Agent Skills（Claude Skills）格式、Claude Agent SDK、Computer Use 相关规范？Anthropic 是否是 x402 Foundation 成员？

checked: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai, https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation, https://github.com/anthropics/claude-code/issues/6686, https://github.com/anthropics/claude-code/issues/28300, https://code.claude.com/docs/en/agent-sdk/overview, https://platform.claude.com/docs/en/managed-agents/agent-setup, https://platform.claude.com/docs/en/managed-agents/skills, https://platform.claude.com/docs/en/build-with-claude/computer-use, https://x402.org/members/

## claims
- [C1] Anthropic 官方主持了针对 MCP 和 A2A 的网络研讨会（2025年8月27日） | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "How MCP and A2A complement each other" + "how these standards enable tool integration, context sharing, task delegation, and more between agents" | type: official
- [C2] Anthropic 将 MCP 捐赠给 Agentic AI Foundation（基于 Linux Foundation） | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "a directed fund under the Linux Foundation" | type: official
- [C3] Claude Agent SDK 支持 MCP 连接 | src: https://code.claude.com/docs/en/agent-sdk/overview | quote: "Connect external tools and data sources via the Model Context Protocol" | type: official
- [C4] Managed Agents 配置包括 mcp_servers 字段支持 MCP 集成 | src: https://platform.claude.com/docs/en/managed-agents/agent-setup | quote: "mcp_servers" field for MCP servers that provide standardized third-party capabilities | type: official
- [C5] Claude Agent SDK 包含 Skills 支持（ManagedAgents 中） | src: https://platform.claude.com/docs/en/managed-agents/skills | quote: "Skills are reusable, filesystem-based resources that give your agent domain-specific expertise" + SKILL.md 格式 | type: official
- [C6] Computer Use 工具规范使用 computer_toolset_20260801 标识符（截至2026年8月） | src: https://platform.claude.com/docs/en/build-with-claude/computer-use | quote: "computer_toolset_20260801" + "Available on Claude API and Google Cloud as GA" | type: official
- [C7] Computer Use 工具包含17个成员操作（screenshot, zoom, left_click 等） | src: https://platform.claude.com/docs/en/build-with-claude/computer-use | quote: "17 Member Tools" with list of screenshot, zoom, left_click, right_click, middle_click, double_click, triple_click, left_click_drag, mouse_move, left_mouse_down, left_mouse_up, cursor_position, scroll, type, key, hold_key, wait | type: official
- [C8] ACP (Agent Client Protocol) 功能请求已于 GitHub claude-code issue #6686 提出但被关闭为"not planned" | src: https://github.com/anthropics/claude-code/issues/6686 | quote: "Closed as not planned" | type: official
- [C9] Anthropic 官方未在 Claude 产品中正式支持 ACP 标准 | src: https://github.com/anthropics/claude-code/issues/6686 | quote: 该功能请求要求实现 "claude acp serve" 命令，但被关闭，表示 Anthropic 不计划此功能 | type: official
- [C10] A2A (Agent-to-Agent) 支持在 Anthropic GitHub 上以功能请求形式讨论（issue #28300，开放状态） | src: https://github.com/anthropics/claude-code/issues/28300 | quote: "Build an MCP-based Agent-to-Agent protocol enabling" + "Shared Workspace/Channel" + "Real-time Messaging" | type: official
- [C11] Anthropic 官方 x402 Foundation 成员身份未确认 | src: https://x402.org/members/ | quote: 官方成员列表中不包含 Anthropic（仅列出AWS、Google、Mastercard、Visa等40个成员） | type: official

## conflicts
- [C2 vs C10] MCP 已被捐赠到 AAIF 治理（官方宣布），但 A2A 的 Anthropic 支持状态仍为 GitHub 功能请求（未决策）。两者治理权级别不对等。

## gaps
- AG-UI 在 Anthropic 官方文档中没有明确的协议支持声明或集成；只在 quickstarts 中作为参考实现出现
- Computer Use 规范是否有对应的标准发布（如 RFC 或协议定稿）未确认
- Claude Agent SDK 是否已开源或有公开规范定义未确认
- Anthropic 对 A2A 的长期承诺/时间表未公布

## leads
- A2A 在 Anthropic 内部处于活跃讨论状态（GitHub issue 开放），可能是未来发展方向
- Computer Use 可能是 Anthropic 独家规范级产物（computer_toolset_20260801 是专有标识符）
- ACP 被 Anthropic 明确拒绝（not planned），表明 Anthropic 不走编辑器↔agent 子进程的对接模式
