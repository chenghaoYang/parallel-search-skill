# r1-scout
question: 在 MCP / A2A / ACP / AG-UI 这个范围内，用户会踩的命名坑，以及网格里还没有的相邻规范；并列出 OpenAI、Anthropic、Google、微软各自文档里和这些协议有关的官方 URL。
checked: https://agentcommunicationprotocol.dev/introduction/welcome, https://github.com/orgs/i-am-bee/discussions/5, https://agentclientprotocol.com/get-started/introduction, https://agentclientprotocol.com/protocol/overview, https://a2ui.org/introduction/what-is-a2ui/, https://a2ui.org/introduction/agent-ui-ecosystem/, https://docs.ag-ui.com/spec/1.0, https://developer.chrome.com/docs/ai/webmcp, https://github.com/agent-network-protocol/AgentNetworkProtocol, https://agent-network-protocol.com/docs/anp-getting-started-guide, https://developers.openai.com/commerce, https://developers.openai.com/commerce/guides/get-started.md, https://developers.openai.com/commerce/guides/key-concepts, https://developers.openai.com/apps-sdk/concepts/mcp-server, https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md, https://adk.dev/a2a/, https://adk.dev/mcp/, https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp, https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/agent-services/a2a

## claims
- [C1] IBM 欢迎页：ACP 已并入 A2A。 | src: https://agentcommunicationprotocol.dev/introduction/welcome | quote: "ACP is now part of A2A under the Linux Foundation!" | type: official
- [C2] 同页正文仍把 ACP 定义成现行互操作协议。 | src: https://agentcommunicationprotocol.dev/introduction/welcome | quote: "The Agent Communication Protocol (ACP) is an open protocol for agent interoperability" | type: official
- [C3] 2025-08-25 公告：ACP 正式并入 A2A。 | src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "ACP is officially merging with the A2A under the Linux Foundation" | type: official
- [C5] Zed 的 ACP 是 Agent Client Protocol，编辑器/IDE↔coding agent。 | src: https://agentclientprotocol.com/get-started/introduction | quote: "The Agent Client Protocol (ACP) standardizes communication between code editors/IDEs and coding agents" | type: official
- [C6] A2UI 全称 Agent to UI，声明式 UI 协议。 | src: https://a2ui.org/introduction/what-is-a2ui/ | quote: "A2UI (Agent to UI) is a declarative UI protocol for agent-driven interfaces." | type: official
- [C7] A2UI 官方把 AG-UI 定为传输、把自己定为载荷。 | src: https://a2ui.org/introduction/agent-ui-ecosystem/ | quote: "AG-UI is a transport protocol connecting agent backends to frontends with real-time state sync. A2UI is a UI format" | type: official
- [C8] WebMCP（Chrome，2026-08-07 更新）是网页向 agent 暴露工具的提议标准，本页未写成 Model Context Protocol。 | src: https://developer.chrome.com/docs/ai/webmcp | quote: "WebMCP is a proposed web standard to help you build and expose structured tools for AI agents." | type: official
- [C9] ANP = Agent Network Protocol，agent↔agent。 | src: https://github.com/agent-network-protocol/AgentNetworkProtocol | quote: "Agent Network Protocol (ANP) is an open-source communication protocol for intelligent agents." | type: official
- [C10] ANP-06 全称 Agent Communication Meta-Protocol，仍是草案。 | src: https://github.com/agent-network-protocol/AgentNetworkProtocol | quote: "ANP-06: Agent Communication Meta-Protocol" | type: official
- [C11] ANP-10 自称 Agent Payment Protocol (AP2)。 | src: https://github.com/agent-network-protocol/AgentNetworkProtocol | quote: "ANP-10: Agent Payment Protocol (AP2)" | type: official
- [C12] OpenAI 商务文档用 ACP 指商品目录集成。 | src: https://developers.openai.com/commerce/guides/get-started.md | quote: "Start your ACP integration by sharing a structured product feed with OpenAI." | type: official
- [C13] 同页全称是 Agentic Commerce Protocol。 | src: https://developers.openai.com/commerce/guides/get-started.md | quote: "You can learn more about the Agentic Commerce Protocol at agenticcommerce.dev" | type: official
- [C14] Anthropic MCP connector 仅 tool calls（beta mcp-client-2025-11-20）。 | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: "only tool calls are currently supported." | type: official
- [C15] Google 套件名 Agent Development Kit (ADK)，协议名 Agent2Agent。 | src: https://adk.dev/a2a/ | quote: "using Agent2Agent (A2A) Protocol" | type: official
- [C16] 微软展开名是 Agent-to-Agent；产品名 Agent Framework（ms.date 2026-09-16）。 | src: https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/agent-services/a2a | quote: "exposed via the Agent-to-Agent (A2A) protocol." | type: official

## conflicts
- 三套 ACP 已打开页互不点名：IBM Agent Communication Protocol（welcome）；Zed Agent Client Protocol（introduction）；OpenAI 同页 ACP 与 Agentic Commerce Protocol（get-started.md）。原句见 C2、C5、C13。
- IBM 欢迎页横幅 "ACP is now part of A2A" 对正文仍把 ACP 当互操作协议（同一 URL）。公告写 "winding down active development"（https://github.com/orgs/i-am-bee/discussions/5）。
- A2A 展开：Google "Agent2Agent (A2A) Protocol"（https://adk.dev/a2a/）对微软 "Agent-to-Agent (A2A) protocol"（https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/agent-services/a2a）。
- 微软同页 well-known：C# "https://{domain}/.well-known/agent-card.json" 对 Python "/.well-known/agent.json"。未打开 https://a2a-protocol.org/ 。

## gaps
- 两 ACP 站 site: 检索未见互相点名；welcome 与 introduction 全文也没有对方全称。未拉 llms.txt。
- https://agentcommunicationprotocol.dev/about/mcp-and-a2a 搜索仍并列 ACP/A2A，未 fetch。
- https://developers.openai.com/apps-sdk/concepts/mcp-server 返回无 "Apps SDK"。未再打开 https://developers.openai.com/plugins/concepts/mcp-server 。
- https://webmachinelearning.github.io/webmcp 未打开，不引「页面即 MCP server」。Google AP2 与 https://ucp.dev/ 未打开，不能和 ANP 的 AP2 对质。
- docs.anthropic.com 的 MCP 入口跨主机跳到重复 /docs 路径，未采用。ANP 入门页几乎空。微软 Agents Framework / 365 Agents SDK / Agent 365 枢纽页未打开。

## leads
- 并入公告：https://github.com/orgs/i-am-bee/discussions/5 ；https://agentcommunicationprotocol.dev/introduction/welcome ；迁移 https://github.com/i-am-bee/beeai-platform/blob/main/docs/community-and-support/acp-a2a-migration-guide.mdx 。agent↔agent，现并入 A2A。
- 第三套 ACP：OpenAI Agentic Commerce Protocol，商户↔ChatGPT。https://developers.openai.com/commerce/guides/get-started 。未打开 https://agenticcommerce.dev 与 https://github.com/agentic-commerce-protocol/agentic-commerce-protocol 。
- A2UI≠AG-UI。https://a2ui.org/introduction/what-is-a2ui/ ；spec https://docs.ag-ui.com/spec/1.0 ；对比 https://a2ui.org/introduction/agent-ui-ecosystem/ （传输 vs 载荷）。
- MCP Apps：对比表称 MCP extension SEP-1865，ui://+iframe，MCP server↔host。未打开 https://modelcontextprotocol.io/docs/extensions/apps 。
- WebMCP：网页↔浏览器 agent。https://developer.chrome.com/docs/ai/webmcp 。草案未打开 https://webmachinelearning.github.io/webmcp 。仓库 https://github.com/webmachinelearning/webmcp 。
- ANP：开放互联网 agent↔agent。https://github.com/agent-network-protocol/AgentNetworkProtocol 。ANP-06=Agent Communication Meta-Protocol（草案）；ANP-10=Agent Payment Protocol (AP2)。
- Google AP2 未 fetch，需与 ANP-10 对名：https://github.com/google-agentic-commerce/AP2 ；https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol 。UCP 未打开：https://ucp.dev/ （搜索称 Universal Commerce Protocol，商户商务生命周期）。
- OpenAI 未定论：Apps SDK 请求 https://developers.openai.com/apps-sdk/concepts/mcp-server （正文可疑）。未打开 https://developers.openai.com/plugins/concepts/mcp-server 与 Agents SDK https://developers.openai.com/api/docs/guides/agents 。
- Anthropic 已开 connector（仅 tools；mcp-client-2025-04-04 已弃用）。未打开 https://platform.claude.com/docs/en/agent-sdk/mcp 与 https://platform.claude.com/docs/en/managed-agents/mcp-connector 。
- Google ADK：https://adk.dev/a2a/ 与 https://adk.dev/mcp/ 。未打开 https://a2a-protocol.org/ 。
- 微软：Copilot Studio https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp （已开，只支持 MCP tools/resources）。Agent Framework https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/agent-services/a2a 。未打开 https://learn.microsoft.com/en-us/microsoft-copilot-studio/ （搜索摘要有 Microsoft 365 Agents SDK、Agent 365、Microsoft Agents Framework）。
- 未打开：AG-UI 集成目录 https://docs.ag-ui.com/integrations （点名 Microsoft Agent Framework、Google ADK）。Zed registry https://agentclientprotocol.com/get-started/registry ；overview 为 stdio+JSON-RPC。
