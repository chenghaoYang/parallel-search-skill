# r1-ui
question: agent↔用户界面层协议：AG-UI（CopilotKit）为主体 + 同层消歧 MCP-UI/MCP Apps、OpenAI Apps SDK、Google A2UI。填 grid.md AG-UI 与 MCP-UI/MCP Apps 行 D1–D8。
checked: https://docs.ag-ui.com/introduction, https://docs.ag-ui.com/concepts/events, https://docs.ag-ui.com/concepts/architecture, https://github.com/ag-ui-protocol/ag-ui, https://github.com/ag-ui-protocol/ag-ui/blob/main/LICENSE, https://mcpui.dev/, https://github.com/MCP-UI-Org/mcp-ui, https://modelcontextprotocol.io/extensions/apps, https://github.com/modelcontextprotocol/ext-apps, https://openai.com/index/introducing-apps-in-chatgpt/, https://developers.openai.com/apps-sdk/mcp-apps-in-chatgpt, https://developers.googleblog.com/en/introducing-a2ui-an-open-project-for-agent-driven-interfaces/, https://a2ui.org/, https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation, https://aaif.io/projects, https://www.copilotkit.ai/learning/mcp-vs-a2a-vs-ag-ui, registry.npmjs.org/@ag-ui/core

## claims
- [C1] AG-UI=Agent–User Interaction Protocol，标准化 AI agent 到用户前端应用的连接 | src: https://github.com/ag-ui-protocol/ag-ui | quote: "AG-UI is an open, lightweight, event-based protocol that standardizes how AI agents connect to user-facing applications." | type: official
- [C2] 定位：与 MCP(工具)、A2A(agent↔agent) 并列，AG-UI 负责用户界面层；"general-purpose, bi-directional connection between a user-facing application and any agentic backend" | src: https://docs.ag-ui.com/introduction | type: official
- [C3] 发起方 CopilotKit："was born from CopilotKit's initial partnership with LangChain and CrewAI"；2025年5月推出 | src: https://github.com/ag-ui-protocol/ag-ui + https://www.copilotkit.ai/learning/mcp-vs-a2a-vs-ag-ui ("AG-UI was created by CopilotKit (May 2025) and is developed in the open under the MIT license") | type: official
- [C4] 治理：归 ag-ui-protocol GitHub org / CopilotKit，README 提及 "AG-UI Working Group"；不在 Linux Foundation/AAIF——aaif.io 托管项目仅 MCP、goose、AGENTS.md、agentgateway、A2A、Agent Router，无 AG-UI | src: https://aaif.io/projects | type: official
- [C5] 事件数：README 原句 "emit events compatible with one of AG-UI's ~16 standard event types" | src: https://github.com/ag-ui-protocol/ag-ui | type: official
- [C6] 文档事件页分类更细：Lifecycle 5、Text 4、ToolCall 5、State 3(STATE_SNAPSHOT/STATE_DELTA/MESSAGES_SNAPSHOT)、Activity 2、Reasoning 7、Subagent 3、Special(RAW/CUSTOM) 2、draft META_EVENT；STATE_DELTA 用 RFC 6902 JSON Patch | src: https://docs.ag-ui.com/concepts/events | type: official
- [C7] 弃用：5 个 THINKING_* 事件被 REASONING_* 取代，"will be removed in version 1.0.0" | src: https://docs.ag-ui.com/concepts/events | type: official
- [C8] 传输无关："Works with any event transport (SSE, WebSockets, webhooks, etc.)"；HttpAgent 支持 "HTTP SSE" 与 "HTTP binary protocol"(protobuf) | src: https://github.com/ag-ui-protocol/ag-ui + https://docs.ag-ui.com/concepts/architecture | type: official
- [C9] 核心抽象：run(input: RunAgentInput) -> Observable<BaseEvent>；HttpAgent=POST RunAgentInput{threadId,runId,messages,tools,state,context}→BaseEvent 流；每 run 须 RUN_STARTED 开头、RUN_FINISHED/RUN_ERROR 结尾 | src: https://docs.ag-ui.com/concepts/architecture | type: official
- [C10] 版本：npm @ag-ui/core 1.0.0 发布于 2026-09-17（包创建于 2025-04-30）；docs 页本身不标 spec 版本 | src: https://registry.npmjs.org/@ag-ui/core | type: official
- [C11] 鉴权：spec 未定义 ∅；架构页无 OAuth/API key 字段，仅有 "Secure Proxy: Backend services that provide additional capabilities and act as a secure proxy" | src: https://docs.ag-ui.com/concepts/architecture | type: official
- [C12] 框架集成：partnership=LangChain/LangGraph、CrewAI；1st-party=Microsoft Agent Framework、Google ADK、AWS Strands、Mastra、Pydantic AI、Agno、LlamaIndex、AG2；community=Claude Agent SDK、Langroid；in-progress=OpenAI Agent SDK、AWS Bedrock Agents、Cloudflare Agents | src: https://github.com/ag-ui-protocol/ag-ui | type: official
- [C13] SDK：官方 TS(@ag-ui/core|client|encoder)+Python；社区 Kotlin/Go/Dart/Java/Rust/Ruby/C++/.NET；客户端 CopilotKit、terminal、Slack/Teams Channels SDK、React Native | src: https://github.com/ag-ui-protocol/ag-ui | type: official
- [C14] AG-UI "Other" 集成列有 A2A、Amazon Bedrock AgentCore、Oracle Agent Spec、MCP Apps(generative UI)；A2UI 可经 AG-UI middleware 承载 | src: https://github.com/ag-ui-protocol/ag-ui + https://developers.googleblog.com/a2ui-v0-9-generative-ui/ | type: official
- [C15] MCP-UI 作者：Ido Salomon，合作者 Liad Yosef："`mcp-ui` is a project by Ido Salomon, in collaboration with Liad Yosef"；Apache-2.0 | src: https://github.com/MCP-UI-Org/mcp-ui | type: official
- [C16] MCP-UI 已并入官方标准："MCP-UI is now standardized into MCP Apps!"；"MCP Apps is the official standard for interactive UI in MCP"；mcp-ui 包成为兼容实现+社区 playground，另有 Legacy MCP-UI Adapter | src: https://mcpui.dev/ | type: official
- [C17] MCP Apps=官方 MCP 扩展 SEP-1865，仓 modelcontextprotocol/ext-apps；spec 版本 2026-01-26 标 "Stable"，draft 版开发中 | src: https://github.com/modelcontextprotocol/ext-apps | type: official
- [C18] MCP Apps 是 OpenAI+Anthropic+MCP-UI 三方协作："we announced a collaboration with Anthropic and MCP-UI to extend the Apps SDK to all MCP developers through MCP Apps"(2025-12-09) | src: https://openai.com/index/agentic-ai-foundation/ | type: official
- [C19] 协议面：tool 经 `_meta.ui.resourceUri` 指向 `ui://` 资源，MIME `text/html;profile=mcp-app`；host 用 resources/read 取 HTML | src: https://github.com/MCP-UI-Org/mcp-ui + https://modelcontextprotocol.io/extensions/apps | type: official
- [C20] app↔host 通信：postMessage 上的 JSON-RPC MCP 方言，"most are new with a ui/ method name prefix"(ui/initialize、ui/notifications/tool-result、ui/message、ui/update-model-context)，共享 tools/call；"The transport is postMessage instead of stdio or HTTP" | src: https://modelcontextprotocol.io/extensions/apps | type: official
- [C21] 安全模型："MCP Apps run in a sandboxed iframe controlled by the host"；_meta.ui 可含 permissions 与 csp | src: https://modelcontextprotocol.io/extensions/apps | type: official
- [C22] SDK：@modelcontextprotocol/ext-apps(+/react、/app-bridge、/server)；host 侧推荐 @mcp-ui/client；另有 Ruby mcp_ui_server、Python mcp-ui-server | src: https://modelcontextprotocol.io/extensions/apps + https://mcpui.dev/ | type: official
- [C23] 已支持 host："Claude, Claude Desktop, VS Code GitHub Copilot, Microsoft 365 Copilot, Goose, Postman, MCPJam, Archestra.AI" | src: https://modelcontextprotocol.io/extensions/apps | type: official
- [C24] ChatGPT 亦实现 MCP Apps 标准："ChatGPT supports the MCP Apps open standard for embedded app UIs"；兼容别名 `_meta["openai/outputTemplate"]`↔`_meta.ui.resourceUri`，window.openai.*(callTool/toolOutput/setWidgetState/requestCheckout)=ChatGPT 专属扩展；"OpenAI helped shape the MCP Apps standard from ChatGPT Apps" | src: https://developers.openai.com/apps-sdk/mcp-apps-in-chatgpt | type: official
- [C25] OpenAI Apps SDK：2025-10-06 发布 preview，"open standard built on the Model Context Protocol (MCP)… We've made the Apps SDK open source"；widget 以 iframe 渲染进 ChatGPT；2025-11-13 起 Business/Enterprise/Edu 可用 | src: https://openai.com/index/introducing-apps-in-chatgpt/ | type: official
- [C26] Google A2UI 确实存在：Google Developers Blog 2025-12-15 公布，"A2UI is an Apache 2 licensed project"，格式当时 v0.8；现 a2ui.org "v0.9.1 current, v1.0 candidate" | src: https://developers.googleblog.com/en/introducing-a2ui-an-open-project-for-agent-driven-interfaces/ + https://a2ui.org/ | type: official
- [C27] A2UI 定位：声明式 JSON UI 消息(createSurface/surfaceUpdate/dataModelUpdate/beginRendering)，"declarative data format, not executable code"，客户端 catalog 渲染；renderers Lit/Angular/Flutter；"created by Google with contributions from CopilotKit" | src: https://a2ui.org/ + Google blog | type: official
- [C28] A2UI↔邻居关系："The JSON payload can be sent to the client over A2A, AG UI, and potentially other transports"；与 AG-UI 互补：AG-UI=双向运行时连接，A2UI=UI 数据格式；v0.9 起也可走 MCP/WS/REST | src: https://developers.googleblog.com/en/introducing-a2ui-an-open-project-for-agent-driven-interfaces/ | type: official

## conflicts
- AG-UI license：repo LICENSE 文件为 "MIT License (c) 2025"，CopilotKit 对比文写 "under the MIT license"；但 docs.copilotkit.ai/ag-ui 页脚徽章写 "Open source · Apache 2.0 · ag-ui-protocol/ag-ui"。LICENSE 文件为准，徽章疑有误。
- AG-UI 事件数：README "~16 standard event types" vs docs events 页现列 8 类 31+ 个（reasoning/subagent/activity 为后加）。非真矛盾，属版本演进，但 "~16" 已过时。

## gaps
- AG-UI spec 文档自身版本号未在 docs 页标注；1.0.0 是 npm 包版本（deprecated 事件承诺在 1.0.0 移除——刚发布 8 天，未核实是否真删）。
- MCP-UI 各包版本号、MCP Apps spec 是否有 SEP 编号之外的语义版本（仅见 2026-01-26 日期版）。
- AG-UI Working Group 章程/成员未见正式文档（README 仅一行提及）。
- A2UI 治理：是否计划捐基金会未见声明（仅 "open-source project… engage with the community"）。
- developers.openai.com/apps-sdk 根路径疑似已并入 /plugins 文档（skills+MCP+UI 打包），未确认重定向。

## leads
- OpenAI 开发者文档已把 apps 归入 "plugins"（skills+MCP server+optional UI），L3 正在向 MCP Apps 标准收敛。
- AAIF(aaif.io) 现托管 A2A、agentgateway、Agent Router——对 L2 行治理列有用。
- AG-UI 把 MCP Apps/A2UI/A2A 都列为可集成 payload，三层协议呈正交堆叠。
