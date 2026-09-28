# r1-scout
question: 在 MCP、A2A、IBM ACP、Zed ACP、AG-UI 已入网格的前提下，2026 年读者还会碰到哪些相邻「协议」或四家大厂的自家变体？只点名并给官方一句话定义。
checked: https://a2ui.org/, https://webmachinelearning.github.io/webmcp/, https://github.com/universal-tool-calling-protocol/utcp-specification, https://github.com/agent-network-protocol/AgentNetworkProtocol, https://github.com/microsoft/NLWeb, https://github.com/modelcontextprotocol/ext-apps/blob/main/README.md, https://developers.openai.com/apps-sdk/, https://agentskills.io/, https://www.anthropic.com/news/model-hardware-standard-research-preview, https://developers.openai.com/plugins/concepts/mcp-server.md, https://github.com/google-agentic-commerce/AP2, https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/activity-protocol, https://github.com/google-agentic-commerce/AP2/blob/main/docs/ap2/specification.md

## claims
- [C1] A2UI（Google 创建、Apache-2.0，CopilotKit 等参与）：agent 到 client 渲染器，标准化 agent 生成的声明式 UI JSON 消息；当前 v0.9.1 production、v1.0 candidate | src: https://a2ui.org/ | quote: "A2UI enables AI agents to generate rich, interactive user interfaces that render natively across web, mobile, and desktop—without executing arbitrary code." | type: official
- [C2] WebMCP（W3C Web Machine Learning CG，编辑来自 Microsoft 和 Google）：web 应用到 AI agents/浏览器 agent，标准化 document.modelContext 上注册 JS「tools」的 API；Draft CG Report 2026-09-17，非 W3C 标准 | src: https://webmachinelearning.github.io/webmcp/ | quote: "The WebMCP API enables web applications to provide JavaScript-based tools to AI agents." | type: official
- [C3] UTCP（universal-tool-calling-protocol 组织）：tool providers 到 AI clients，标准化跨原生协议（HTTP/WebSocket/CLI/MCP 等）的工具发现与调用，v1.0 | src: https://github.com/universal-tool-calling-protocol/utcp-specification | quote: "UTCP provides a standardized way for AI systems and other clients to discover and call tools from different providers, regardless of the underlying protocol used (HTTP, WebSocket, CLI, etc.)." | type: official
- [C4] ANP Agent Network Protocol（开源社区，MIT）：agent 到 agent，标准化身份（did:wba）、WNS 命名、描述、发现、端到端消息、AP2 支付的协议套件；已发布 ANP 1.1 | src: https://github.com/agent-network-protocol/AgentNetworkProtocol | quote: "ANP aims to become the HTTP of the Agentic Web era: a protocol suite for agent identity, naming, discovery, negotiation, secure messaging, and application-level collaboration." | type: official
- [C5] NLWeb（Microsoft，repo 在 nlweb-ai/NLWeb）：网站到人类用户与 agents，标准化自然语言 ask 接口并返回 Schema.org JSON；每个实例同时是 MCP server | src: https://github.com/nlweb-ai/NLWeb | quote: "A simple protocol to interact with a site using natural language. It returns responses in JSON using Schema.org." | type: official
- [C6] MCP Apps（modelcontextprotocol/ext-apps，SEP-1865 落地）：MCP server 到 host chat client，标准化工具附带 ui:// HTML 资源在沙箱 iframe 内联渲染（扩展标识 io.modelcontextprotocol/ui）；spec stable 2026-01-26 | src: https://github.com/modelcontextprotocol/ext-apps/blob/main/README.md | quote: "MCP Apps provide a standardized way to deliver interactive UIs from MCP servers." | type: official
- [C7] Agent Skills（Anthropic 发起的开放标准，agentskills.io）：skill 文件夹到 agent，标准化 SKILL.md 格式的可加载知识/流程包；是格式不是通信协议 | src: https://agentskills.io/ | quote: "Agent Skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows." | type: official
- [C8] Model Hardware Standard / MHS（Anthropic，2026-08-27 research preview，未开源）：agent 到物理设备，标准化设备 driver 与 read/write 原语使 agent 能发现和安全操作硬件 | src: https://www.anthropic.com/news/model-hardware-standard-research-preview | quote: "a shared specification for AI agents to safely operate physical devices" | type: official
- [C9] OpenAI Apps SDK/Plugins（OpenAI 官方开发者文档）：开发者 MCP server 到 ChatGPT，不构成新开放协议——plugin = skills + MCP server + 可选 UI（MCP Apps）；apps-sdk 文档现已并入 developers.openai.com/plugins/ | src: https://developers.openai.com/plugins/ | quote: "Build and publish plugins with skills, MCP servers, and optional UI." | type: official
- [C10] AP2 Agent Payments Protocol（Google，google-agentic-commerce）：shopping agent 到 merchant/credential provider，标准化 agent 支付中密码学签名的 Checkout/Payment Mandate 授权；spec v0.2 | src: https://github.com/google-agentic-commerce/AP2/blob/main/docs/ap2/specification.md | quote: "The Agentic Payment Protocol (AP2) provides a protocol to secure Agent-performed payment transactions." | type: official
- [C11] Activity Protocol（Microsoft，原 Bot Framework Activity schema，microsoft/Agents repo）：channel/用户 到 agent，标准化 Activity JSON 结构与消息/事件流转；供 M365 Copilot、Copilot Studio、Teams、M365 Agents SDK 使用（页面 ms.date 2026-04-28） | src: https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/activity-protocol | quote: "Activity Protocol defines the structure of an `Activity` and how messages, events, and interactions flow from a channel to your code and everywhere else in between." | type: official

## conflicts
- 无（本轮官方页面之间未发现相互矛盾的定义）。

## gaps
- UCP Universal Commerce Protocol：AP2 spec 自述 "designed explicitly to be compatible with the Universal Commerce Protocol (UCP)"，但本轮未打开 UCP 官方页；搜索词 "google-agentic-commerce UCP github"
- OpenAI Agents SDK / Responses API / AGENTS.md 是否自称实现某开放协议：未逐一核实官方页
- Microsoft Copilot Studio "MCP connector"：未开官方文档页；从命名看是 MCP 的消费端 connector，非独立协议
- AGNTCY（Cisco 系）的 "Agent Connect Protocol/ACP"：缩写与 IBM/Zed ACP 撞车风险高，未核实官方页；搜索词 "agntcy acp github"
- W3C AI Agent Protocol Community Group（w3.org/groups/cg/agentprotocol）：搜索结果中出现，未打开页面
- openai.com/index/introducing-apps-in-chatgpt/ 抓取返回空，Apps SDK 官方表述改用 plugins 文档页

## leads
- A2UI → 建议新行：最易与 AG-UI 混淆的 Google 官方协议，实为互补（A2UI 是 UI 载荷格式，官方文档示范跑在 AG-UI/A2A 之上）；入口 https://a2ui.org/ + https://github.com/a2ui-project/a2ui
- WebMCP → 建议新行：名字直接撞 MCP，是 W3C CG 草案级浏览器 API，Microsoft+Google 编辑；入口 https://webmachinelearning.github.io/webmcp/
- ANP → 建议新行（若覆盖 agent 间身份/发现层）：与 A2A 同层的社区规范套件；入口 https://github.com/agent-network-protocol/AgentNetworkProtocol
- NLWeb → 建议新行：Microsoft 的 site↔agent 自然语言协议（/ask + Schema.org），实例兼作 MCP server；入口 https://github.com/nlweb-ai/NLWeb + https://nlweb.ai/spec
- AP2 → 建议新行（若覆盖支付/commerce）：Google 官方 agent 支付授权协议，定位为 A2A/MCP 之上的安全扩展；入口 https://github.com/google-agentic-commerce/AP2 + https://ap2-protocol.org/
- MCP Apps → 只做坑：是 MCP 官方扩展（SEP-1865 / io.modelcontextprotocol/ui），统一了 MCP-UI 与 OpenAI Apps SDK 两条前身，别当成独立协议
- Agent Skills → 只做坑：是 SKILL.md 格式标准不是 wire protocol；Anthropic 除 MCP 外的第二开放标准
- MHS → 只做坑或一句话提及：Anthropic 2026-08 research preview、尚未开源，物理设备域
- Activity Protocol → 只做坑：Microsoft 自有 channel↔agent 消息 schema（Copilot Studio/Teams 底层），非开放行业协议；spec https://github.com/microsoft/Agents/blob/main/specs/activity/protocol-activity.md
- OpenAI → 忽略为协议条目：无自家开放协议，Apps SDK/Plugins 全部构建在 MCP（+MCP Apps）上；下一轮深挖入口 https://developers.openai.com/plugins/
- UTCP → 只做坑或忽略：MCP 的开源竞品规范，存在官方 spec 但无大厂背书，别误写进大厂变体
