# r2-google
question: Google 官方文档如何描述自己对 MCP、A2A、两条 ACP、AG-UI 的支持，以及 Google 自己发布的相邻协议原名（尤其 A2UI 用一句话做什么、接哪两端）。
checked: https://adk.dev/mcp/, https://adk.dev/a2a/, https://adk.dev/integrations/, https://a2ui.org/, https://a2ui.org/concepts/transports/, https://docs.cloud.google.com/agent-builder/agent-engine/develop/a2a, https://developers.googleblog.com/en/gemini-cli-is-now-integrated-into-zed/, https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/acp-mode.md, https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade

## claims
- [C1] MCP=支持。Google ADK 官方文档（域名为 adk.dev，google.github.io/adk-docs 重定向至此）：ADK agent 可作 MCP client 调外部 MCP server，也可把 ADK tools 暴露为 MCP server | src: https://adk.dev/mcp/ | quote: "An ADK agent can act as an MCP client and use tools provided by external MCP servers." | type: official
- [C2] MCP=支持。Gemini CLI 也支持 MCP server，Google Developers Blog（2025-08-27）称其 "extensible by default through emerging standards like MCP" | src: https://developers.googleblog.com/en/gemini-cli-is-now-integrated-into-zed/ | quote: "Gemini CLI was built to be extensible by default through emerging standards like MCP" | type: official
- [C3] A2A=支持。ADK 文档有 A2A 专节，可构建用 A2A 协议协作的多智能体系统（exposing/consuming 双向 quickstart，Python/Go/Java） | src: https://adk.dev/a2a/ | quote: "With Agent Development Kit (ADK), you can build complex multi-agent systems where different agents need to collaborate and interact using Agent2Agent (A2A) Protocol!" | type: official
- [C4] A2A=支持。Google Cloud 博客（2025-08-01）宣布整套工具链：ADK 原生支持、Agent Engine/Cloud Run/GKE 部署、Agentspace（现 Gemini Enterprise）、AI Agent Marketplace 售卖；同文宣布 A2A v0.3（gRPC、签名 security card） | src: https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade | quote: "we are announcing a comprehensive suite of tools that will empower developers to build, deploy, evaluate, and sell Agent2Agent (A2A) agents with Google Cloud." | type: official
- [C5] A2A 起源（Google 官方口径）：Google 2025-04 宣布 A2A，2025-06 捐给 Linux Foundation | src: https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade | quote: "We announced the A2A protocol in April to lead the industry toward interoperable agent systems, and in June, we advanced that commitment by contributing it to the Linux Foundation." | type: official
- [C6] A2A=支持。Gemini Enterprise Agent Platform 官方文档列有 "Use an Agent2Agent agent" 指南（页面 Last updated 2026-09-22 UTC） | src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/use-an-a2a-agent | quote: "Use an Agent2Agent agent with Agent Platform Runtime." | type: official
- [C7] ACP（Zed 的 Agent Client Protocol）=支持。Gemini CLI 有 ACP mode（`gemini --acp`），JSON-RPC 2.0 over stdio，面向 IDE/编辑器集成；Gemini CLI 是 ACP-compatible agent，已进 ACP Agent Registry | src: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/acp-mode.md | quote: "ACP (Agent Client Protocol) mode is a special operational mode of Gemini CLI designed for programmatic control, primarily for IDE and other developer tool integrations." | type: official
- [C8] ACP（Zed）=支持。Google 官方博客 2025-08-27 宣布 Gemini CLI 集成进 Zed 编辑器（ACP 为底层机制，博文本身未写 "ACP" 字样） | src: https://developers.googleblog.com/en/gemini-cli-is-now-integrated-into-zed/ | quote: "Starting today, Gemini CLI is integrated with Zed, bringing Gemini's models directly into Zed's Rust-based environment." | type: official
- [C9] AG-UI=支持（目录级）。ADK 官方 integrations 目录收 AG-UI 条目（/integrations/ag-ui/），定位为给 agent 建交互聊天 UI | src: https://adk.dev/integrations/ | quote: "AG-UI — Build interactive chat UIs with streaming, state sync, and agentic actions" | type: official
- [C10] A2UI 全称+一句话：全称 Agent-to-UI protocol（ADK 目录原称 "the Agent-to-UI protocol"，https://adk.dev/integrations/）；官网标题 "A Protocol for Agent-Driven Interfaces"；一句话：让 AI agent 生成在客户端原生渲染的富交互 UI 而不执行任意代码。同页自述 "A2UI is Apache 2.0 licensed, created by Google with contributions from CopilotKit and the open source community"（满足 a2ui.org 作为 Google 关系来源的条件） | src: https://a2ui.org/ | quote: "A2UI enables AI agents to generate rich, interactive user interfaces that render natively across web, mobile, and desktop—without executing arbitrary code." | type: official
- [C11] A2UI 两端：agent 端生成 A2UI 消息，经 transport 送到 client 端 renderer 用原生组件渲染；用户操作以 action 消息回传 agent；协议 transport-agnostic | src: https://a2ui.org/concepts/transports/ | quote: "Transports deliver A2UI messages from agents to clients. A2UI is transport-agnostic: use any method that can send JSON." | type: official
- [C12] A2UI 与 AG-UI/A2A 的官方关系：AG-UI 是 A2UI 的 Stable 传输方式之一（另有 A2A extension，specification/v0.8-a2a-extension/）；同页 "CopilotKit is AG-UI's creator and primary consumer." | src: https://a2ui.org/concepts/transports/ | quote: "AG-UI translates A2UI messages to AG-UI events and handles transport and state sync automatically." | type: official

## conflicts
- 无实质冲突。域名注意：ADK 官方文档现用 adk.dev（google.github.io/adk-docs 301 到 adk.dev）；Gemini CLI 官方 repo 在 github.com/google-gemini 组织下，不在简报列举的 github.com/google，但属 Google 产品官方仓库。

## gaps
- 第二条 ACP（IBM/BeeAI 的 Agent Communication Protocol）：未找到任何 Google 官方文档提及或声称支持；二手来源称其 2025-08 并入 A2A（见 leads）。格子按 "未写" 处理。
- AG-UI 在 Google 侧仅见 ADK integrations 目录条目；/integrations/ag-ui/ 详情页未打开，支持级别（官方/社区贡献）未核实。
- 未逐页核对 ai.google.dev 是否有 Gemini API 级 MCP/A2A 专页；ADK 与 Gemini CLI 层面证据已足够填格。
- A2UI 的 "Agent-to-UI" 全称在 a2ui.org 首页未拼出，仅见于 ADK 目录页与二手资料。

## leads
- IBM ACP 已于 2025-08 并入 A2A（github.com/i-am-bee/acp 已归档，IBM/LF 公告）——写 vendors 表时注意 "两条 ACP" 语义。
- Google 另有相邻协议 AP2（Agent Payments Protocol，agent 支付），cloud blog 提及，超出本轮范围。
- A2UI 版本线：v0.9.1 为当前 production，v1.0 candidate 增 client-to-server RPC（actionResponse）；A2UI Composer 托管在 ag-ui.com 域。
