# r2-anthropic
question: Anthropic / Claude 官方支持 MCP、A2A、两种 ACP、AG-UI 到哪一步，有没有自家互操作协议变体。
checked: https://claude.com/docs/connectors/overview, https://platform.claude.com/docs/en/agents-and-tools/mcp-connector, https://claude.com/blog/agent-capabilities-api, https://www.anthropic.com/news/model-context-protocol, https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation, https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai, https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp, https://code.claude.com/docs/en/mcp-quickstart, https://www.anthropic.com/news/model-hardware-standard-research-preview

## claims
- [C1] Connectors 由 Anthropic 创建的 MCP 驱动。 | src: https://claude.com/docs/connectors/overview | quote: "They are powered by the Model Context Protocol (MCP), an open standard created by Anthropic that provides a unified way for AI applications to interact with the outside world." | type: official
- [C2] Claude.ai 是完整 remote MCP，并支持 MCP Apps。 | src: https://claude.com/docs/connectors/overview | quote: "Claude.ai — Full remote MCP support & MCP Apps" | type: official
- [C3] Claude Code 产品面是 remote MCP 加 plugins。 | src: https://claude.com/docs/connectors/overview | quote: "Claude Code — Remote MCP access and plugins" | type: official
- [C4] 自定义连接器从 Anthropic 云连远程 MCP，不是从本机出站；含 claude.ai、Desktop、Cowork、移动端。 | src: https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp | quote: "When you add a custom connector, Claude connects to your remote MCP server from Anthropic's cloud infrastructure, rather than from your local device. This is true across every Claude client, including claude.ai, Claude Desktop, Cowork, and the mobile apps." | type: official
- [C5] Desktop 的 claude_desktop_config.json 本地 MCP 走本机网络，不可用于 Cowork 或 claude.ai。 | src: https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp | quote: "Local MCP servers configured in Claude Desktop via `claude_desktop_config.json` are a separate mechanism and do use your local network, but those aren't available in Cowork or claude.ai." | type: official
- [C6] Messages API MCP connector 不要求调用方自建 MCP client。 | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: "Claude's Model Context Protocol (MCP) connector feature enables you to connect to remote MCP servers directly from the Messages API without a separate MCP client." | type: official
- [C7] 废弃头 mcp-client-2025-04-04 的迁移目标是 mcp-client-2025-11-20。 | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: "New beta header: Change from `mcp-client-2025-04-04` to `mcp-client-2025-11-20`" | type: official
- [C8] mcp-client-2026-09-15 含 2025-11-20 的能力，文档要求改发这个头，并写明 Claude API 可用。 | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: "It includes everything `mcp-client-2025-11-20` does, so send it in place of that header. It's available on the Claude API." | type: official
- [C9] 该 connector 目前只支持 MCP tool calls。 | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: "Of the feature set of the MCP specification, only tool calls are currently supported." | type: official
- [C10] 服务器须公网 HTTP（Streamable HTTP 与 SSE）；本地 STDIO 不能直连。 | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: "The server must be publicly exposed through HTTP (supports both Streamable HTTP and SSE transports). Local STDIO servers cannot be connected directly." | type: official
- [C11] featureMetadata：Amazon Bedrock: not available。 | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: "Amazon Bedrock: not available" | type: official
- [C12] 同一元数据：Google Cloud: not available。 | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: "Google Cloud: not available" | type: official
- [C13] MCP 由 Anthropic 的 David Soria Parra 与 Justin Spahr-Summers 创建。 | src: https://www.anthropic.com/news/model-context-protocol | quote: "MCP was created at Anthropic by David Soria Parra and Justin Spahr-Summers." | type: official
- [C14] 2024-11-25 发布稿把 Zed、Replit、Codeium、Sourcegraph 写成正在用 MCP 增强平台。 | src: https://www.anthropic.com/news/model-context-protocol | quote: "development tools companies including Zed, Replit, Codeium, and Sourcegraph are working with MCP to enhance their platforms" | type: official
- [C15] 2025-12-09：MCP 捐给 Linux Foundation 的 AAIF；并列项目还有 Block 的 goose 与 OpenAI 的 AGENTS.md。 | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "Anthropic is donating the Model Context Protocol to the Linux Foundation's new Agentic AI Foundation, where it will join goose by Block and AGENTS.md by OpenAI as founding projects." | type: official
- [C16] Claude Code 远程 MCP 示例命令带 --transport http，URL 为 https://code.claude.com/docs/mcp。 | src: https://code.claude.com/docs/en/mcp-quickstart | quote: "claude mcp add --transport http claude-code-docs https://code.claude.com/docs/mcp" | type: official
- [C17] A2A 只在 2025-08-27 的 Partner Series 活动页出现，内容是 Vertex AI 演示，不是产品或 API 文档。 | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "This webinar, presented by Anthropic and Google Cloud, will dive deep into the practical implementation of multi-agent systems using Model Context Protocol (MCP) and Agent-to Agent protocol (A2A) with Claude on Vertex AI." | type: official
- [C18] 2026-08-27：MHS 是 model-agnostic 规范，任意 agent harness 可用包括 MCP 在内的标准协议访问。 | src: https://www.anthropic.com/news/model-hardware-standard-research-preview | quote: "It is also model-agnostic, and any agent harness can access it using standard protocols, such as the Model Context Protocol." | type: official
- [C19] MHS 控制硬件的机制是 MCP、命令行和代码文件（API）。 | src: https://www.anthropic.com/news/model-hardware-standard-research-preview | quote: "For MHS, there are three such mechanisms: MCP, the command line interface, and code files (APIs)." | type: official

## conflicts
- https://platform.claude.com/docs/en/agents-and-tools/mcp-connector 把迁移目标写成 mcp-client-2025-11-20（quote: "New beta header: Change from `mcp-client-2025-04-04` to `mcp-client-2025-11-20`"），同页又要求改发 mcp-client-2026-09-15（quote: "It includes everything `mcp-client-2025-11-20` does, so send it in place of that header."）。
- Messages API connector 只支持 tool calls（quote: "only tool calls are currently supported." src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector）。Claude Code quickstart 写 MCP prompts（quote: "Run MCP prompts as commands from the `/` menu" src: https://code.claude.com/docs/en/mcp-quickstart）。Claude.ai 另有 MCP Apps（C2）。未说明是否不同表面。

## gaps
- Anthropic.ACP-IBM：无产品页。搜索 "Agent Communication Protocol"、BeeAI、IBM ACP；站点 anthropic.com、claude.com、docs.claude.com、support.claude.com、code.claude.com、platform.claude.com。
- Anthropic.ACP-Zed：无 "Agent Client Protocol" / agentclientprotocol 页。Zed 只在 C14 作为 MCP 伙伴出现。
- Anthropic.AG-UI：无 AG-UI / AGUI 页。MCP Apps（C2）不是 AG-UI。
- Anthropic.A2A：除 C17 webinar 外无端点或字段。
- Anthropic.variant：无页面自称 A2A/ACP/AG-UI 变体。自创并已捐赠的是 MCP（C13、C15）；另有硬件规范 MHS（C18、C19）。
- 篇幅删掉、仍在已打开页上：Desktop/Mobile/Cowork 可用性三行；Claude API、AWS、Foundry 的 beta 行；url 须 https；非 ZDR；Claude Code 本地默认 stdio。
- https://docs.claude.com/en/docs/agents-and-tools/mcp-connector 跳到 platform 页。https://docs.anthropic.com/en/docs/claude-code/mcp 跳到 https://code.claude.com/docs/en/mcp，该 URL fetch 失败。

## leads
- Managed Agents MCP 未打开：https://platform.claude.com/docs/en/managed-agents/mcp-connector
- MCP tunnels 未打开：https://claude.com/docs/connectors/mcp-tunnels/overview
- agent teams / SendMessage 未打开，勿当成公开协议：https://code.claude.com/docs/en/cross-session-messaging
