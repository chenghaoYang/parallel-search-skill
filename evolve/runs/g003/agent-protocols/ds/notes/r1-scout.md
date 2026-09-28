# r1-scout
question: 在 MCP、A2A、ACP、AG-UI 周围，还有哪些用户会撞上的同名或相邻协议，以及 OpenAI、Anthropic、Google、Microsoft 各自官方文档里点名支持其中哪些。本工人只为下一轮提供线索，不把线索写成定论。
checked: https://developers.openai.com/apps-sdk/concepts/mcp-server, https://developers.openai.com/commerce/, https://code.claude.com/docs/en/mcp, https://a2a-protocol.org/latest/, https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/, https://docs.stripe.com/agentic-commerce/acp, https://aaif.io/news/linux-foundation-announces-formation-of-aaif, https://ecma-international.org/publications-and-standards/standards/ecma-430/

## claims
- [C1] Stripe 文档把 ACP 定义为 Agentic Commerce Protocol，作者为 Stripe、OpenAI、Meta。 | src: https://docs.stripe.com/agentic-commerce/acp | quote: "The Agentic Commerce Protocol (ACP) is an open standard created by Stripe, OpenAI, and Meta" | type: official
- [C2] 同页把规范指到 agenticcommerce.dev；OpenAPI 链接路径含 `spec/2026-04-17`。 | src: https://docs.stripe.com/agentic-commerce/acp | quote: "See agenticcommerce.dev for the full specification." | type: official
- [C3] OpenAI commerce 索引用 ACP 称呼这条集成。 | src: https://developers.openai.com/commerce/ | quote: "Start your ACP integration by sharing a structured product feed." | type: official
- [C4] 同索引把 key concepts 写成 Agentic Commerce Protocol。 | src: https://developers.openai.com/commerce/ | quote: "Understand the concepts of the Agentic Commerce Protocol" | type: official
- [C5] AAIF 稿日期 2025-12-09：创始贡献是 MCP、goose、AGENTS.md。 | src: https://aaif.io/news/linux-foundation-announces-formation-of-aaif | quote: "founding contributions of leading technical projects including Anthropic’s Model Context Protocol (MCP), Block’s goose, and OpenAI’s AGENTS.md." | type: official
- [C6] 同稿写 OpenAI 贡献 ACP（链到 https://developers.openai.com/commerce/）、Agents SDK、Apps SDK。 | src: https://aaif.io/news/linux-foundation-announces-formation-of-aaif | quote: "OpenAI was an early adopter of MCP and has contributed ACP, Codex CLI, and the Agents SDK and Apps SDK" | type: official
- [C7] A2A 站：原为 Google 开发，后捐给 Linux Foundation。 | src: https://a2a-protocol.org/latest/ | quote: "A2A was originally developed by Google and donated to the Linux Foundation." | type: official
- [C8] 同页：MCP 是 agent-to-tool。 | src: https://a2a-protocol.org/latest/ | quote: "MCP is for agent-to-tool communication" | type: official
- [C9] 同页：A2A 是 agent-to-agent，可包含使用 MCP 的 agent。 | src: https://a2a-protocol.org/latest/ | quote: "A2A lets independent agents — including those using MCP — discover each other, delegate tasks, and share results." | type: official
- [C10] 同页横幅写加入 AAIF，链到 2026-08-27 博文；博文未打开。 | src: https://a2a-protocol.org/latest/ | quote: "A2A joins the Agentic AI Foundation" | type: official
- [C11] Learn 页 front matter `ms.date` 2026-09-08、`updated_at` 2026-09-15：AG-UI 是协议，链到 https://docs.ag-ui.com/introduction 。 | src: https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/ | quote: "AG-UI is a protocol that enables you to build web-based AI agent applications" | type: official
- [C12] ECMA-430 页定义 NLIP。下载名含 `1st_edition_december_2025`；PDF 未开。 | src: https://ecma-international.org/publications-and-standards/standards/ecma-430/ | quote: "Natural Language Interaction Protocol (NLIP), which is an application-level communication protocol defined between AI Agents or between a human and an AI agent." | type: official

## conflicts
- 时间差，不裁决：C5（2025-12-09）创始名单无 A2A；C10 横幅指向 https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/ ，博文未打开。
- Apps SDK URL 的 web_fetch 正文是 "A plugin can include an MCP server"，无 "Apps SDK"。搜索索引曾有 "With Apps SDK, MCP is the backbone"。未再打开，不算已核实冲突。

## gaps
- 未打开故不能写成支持：OpenAI 的 Agents API MCP、Docs MCP、remote MCP、Agents SDK 正文；Apps SDK 见 conflicts。Anthropic 的 API/Messages 文档。Google ADK/Gemini。Microsoft Copilot Studio A2A、MCP catalog、Foundry。
- https://code.claude.com/docs/en/mcp 全文无 A2A/ACP/AG-UI/Agent2Agent。不是全站结论。
- 未打开：IBM/Zed ACP 站、agenticcommerce.dev、ANP、UTCP、agents.json 三套、e2b Agent Protocol、AGNTCY、UCP。AG-UI 子页 mcp-apps 未开。

## leads
未标「已开」的引语只来自搜索索引，不能当 claim。
- OpenAI Agents API MCP：https://developers.openai.com/api/docs/guides/agents-api/tools/mcp 。索引有 `type: mcp`、`connection_origin` `service`|`environment`、HTTP/stdio。
- OpenAI Docs MCP：https://developers.openai.com/learn/docs-mcp 。索引："OpenAI hosts a public Model Context Protocol (MCP) server"；URL `https://developers.openai.com/mcp`。
- OpenAI Apps SDK：重开 https://developers.openai.com/apps-sdk/concepts/mcp-server 与 https://developers.openai.com/plugins/concepts/mcp-server 。见 conflicts。C6 只证明 AAIF 点名 Apps SDK。
- OpenAI Agents SDK：https://openai.github.io/openai-agents-python/ 与 https://developers.openai.com/api/docs/guides/agents/sdk 。索引有 "direct control over tools, MCP servers, and runtime behavior"。
- OpenAI 商业 ACP（非 IBM/Zed）：已见 C3–C4。打开 https://developers.openai.com/commerce/guides/key-concepts.md 与 https://developers.openai.com/commerce/specs/checkout.md 。
- 第三个 ACP：已见 C1。打开 https://agenticcommerce.dev 与 https://github.com/agentic-commerce-protocol/agentic-commerce-protocol 。
- Anthropic：已开 https://code.claude.com/docs/en/mcp ，原句 "through the Model Context Protocol (MCP), an open source standard for AI-tool integrations." 再开 https://code.claude.com/docs/en/agent-sdk/mcp 与 API 文档。
- Google ADK×A2A：https://google.github.io/adk-docs/a2a/ 。索引："using Agent2Agent (A2A) Protocol"。
- Google ADK×MCP：https://google.github.io/adk-docs/mcp/ 。索引："Supported in ADK Python TypeScript Go Java"，并点 Gemini、Claude。
- A2A×AAIF：博文 URL 见 conflicts。LF 启动稿索引 2025-06-23 有 "an open protocol created by Google"（linuxfoundation.org/press 下 A2A launch，未开）。
- Microsoft Copilot Studio A2A + Activity Protocol：https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent 。索引："You can connect your custom agent to another agent that supports the A2A protocol." 同页索引把 MCP servers 与 Activity Protocol（M365 Agents SDK）并列。en-gb 是否仍标 preview 未核。
- Microsoft MCP catalog：https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-microsoft-mcp-servers 。索引 Last updated 2026-02-04。
- Agent Framework×Copilot Studio：https://learn.microsoft.com/en-us/agent-framework/agents/providers/copilot-studio 。索引称 agent definition 含 MCP servers。
- AG-UI 本体：C11 只是集成。同页 "Use MCP Apps with your AG-UI endpoint"；包 `Microsoft.Agents.AI.Hosting.AGUI.AspNetCore`、`agent-framework-ag-ui`。打开 https://docs.ag-ui.com/introduction 。
- IBM ACP→A2A：https://agentcommunicationprotocol.dev/introduction/welcome 。索引："ACP is now part of A2A under the Linux Foundation!" 与商业 ACP、Zed ACP 不同物。
- Zed ACP：https://agentclientprotocol.com 。编辑器到 coding agent，不是 agent-to-agent。
- AAIF 后续：https://aaif.io 。2026-04-02 LF 活动稿索引仍只列 MCP、goose、AGENTS.md，可能早于 C10；URL 在 linuxfoundation.org/press 搜 AGNTCon MCPCon。
- AGENTS.md / goose：http://agents.md 与 https://block.github.io/goose 。C5 把前者当仓库指导、后者当带 MCP 的框架，先不要升成线协议。
- AGNTCY（SLIM 只跟这条）：https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos 。索引 2025-07-29：与 A2A、MCP 互操作，并出现 SLIM。
- NLIP 绑定：已开 ECMA-430。打开该 PDF 与 ECMA-431/432/433。索引中的 PDF 文字提到 ECMA-434，未核。
- ANP：https://github.com/agent-network-protocol/AgentNetworkProtocol 与 https://www.agent-network-protocol.com/specs/agent-discovery.html 。索引："ANP aims to become the HTTP of the Agentic Web era"。
- UTCP：https://utcp.io/ 。索引："no wrapper servers required." Version: 1.1，有 MCP 插件行。
- agents.json 三套勿合并：(1) https://www.agent-json.org/ (2) https://www.ietf.org/archive/id/draft-narvaneni-agent-uri-03.html 的 `/.well-known/agents.json` 与 `agent://` (3) https://agents-txt.com/schema/agents-json/v1.0.json 。
- 旧 Agent Protocol：https://github.com/e2b-dev/agent-protocol 。索引：`POST /ap/v1/agent/tasks`。https://agentprotocol.ai/about/ 索引自称非官方，不要当规范。
- UCP：https://docs.stripe.com/agentic-commerce 。索引表："Protocol used | UCP or ACP | MPP or x402"。已开的 ACP 页没有这句。
