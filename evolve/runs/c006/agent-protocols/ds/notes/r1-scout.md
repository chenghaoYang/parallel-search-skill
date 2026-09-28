# r1-scout
question: 除 MCP、A2A、IBM ACP、Zed ACP、AG-UI 之外还有哪些用户会混淆/需要知道的协议或事实坑（产 leads + 少量 claim）
checked: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http, https://github.com/agntcy/docs/blob/d7d5db4e/docs/syntactic/connect.md, https://github.com/agntcy/acp-spec, https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/, https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation, https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol, https://a2ui.org/, https://modelcontextprotocol.io/extensions/apps/overview, https://mcpui.dev/, https://docs.copilotkit.ai/ag-ui/introduction, https://docs.stripe.com/agentic-commerce/acp, https://agentnetworkprotocol.com/en/specs/, https://github.com/agent-network-protocol/AgentNetworkProtocol, https://github.com/universal-tool-calling-protocol/utcp-specification, https://arxiv.org/abs/2410.11905, https://developers.google.com/merchant/ucp, https://shopify.engineering/UCP, https://docs.cdp.coinbase.com/x402/welcome.md, https://github.com/nlweb-ai/NLWeb, https://agents.md/, https://openai.com/index/agentic-ai-foundation/

## claims
- [C1] 第三个 ACP = Agentic Commerce Protocol，OpenAI+Stripe 共同维护的 beta 开放标准（Apache 2.0），连接买家、AI agent 与商家完成购买 | src: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol | quote: "The Agentic Commerce Protocol (ACP) is an interaction model and open standard for connecting buyers, their AI agents, and businesses to complete purchases seamlessly." "The specification is maintained by OpenAI and Stripe and is currently in `beta`." | type: official
- [C2] 第四个 ACP = Agent Connect Protocol，AGNTCY（Cisco 发起、已捐 Linux Foundation 的 Internet of Agents 项目）的 agent 调用协议 | src: https://github.com/agntcy/docs/blob/d7d5db4e/docs/syntactic/connect.md | quote: "We call it the Agent Connect Protocol (ACP). The current specification of the ACP can be found at https://spec.acp.agntcy.org/." | type: official
- [C3] MCP 的「SSE 废弃」精确含义：被废弃的是 2024-11-05 版引入的 HTTP+SSE transport，自 2025-03-26 起 deprecated，由 Streamable HTTP 取代；SSE 作为机制仍在（Streamable HTTP 响应仍可选 SSE stream）| src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "The HTTP+SSE transport from protocol version 2024-11-05 has been deprecated since protocol version `2025-03-26`" / "The server answers each request with either a single JSON object or a Server-Sent Events (SSE) stream scoped to that request" | type: official
- [C4] MCP spec 用日期版号（2024-11-05 / 2025-03-26 / 2025-06-18 / 2025-11-25 / 2026-07-28），请求须带 `MCP-Protocol-Version` header；2026-07-28 版又改了 Streamable HTTP（移除 GET stream 端点与协议级 session）| src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "Every POST request to the MCP endpoint MUST include an `MCP-Protocol-Version` header. For example: `MCP-Protocol-Version: 2026-07-28`" / "Revision 2026-07-28 changed the behavior of Streamable HTTP... Removal of the GET stream endpoint. Removal of protocol-level sessions." | type: official
- [C5] IBM 的 ACP（Agent Communication Protocol，BeeAI）已于 2025-08-29 宣布并入 Linux Foundation 下的 A2A，ACP 停止独立开发 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "ACP is officially merging with the A2A under the Linux Foundation... the ACP team will be winding down active development" | type: official
- [C6] 治理事实：2025-12-09 Linux Foundation 成立 Agentic AI Foundation (AAIF)，创始项目 = Anthropic 的 MCP、Block 的 goose、OpenAI 的 AGENTS.md；A2A 则在 LF 另一处（2025-06 捐入）| src: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | quote: "founding contributions of three leading projects... Anthropic's Model Context Protocol (MCP), Block's goose, and OpenAI's AGENTS.md" | type: official
- [C7] AGENTS.md 不是通信协议而是仓库根的 Markdown 约定文件（"README for agents"），现由 AAIF 托管 | src: https://agents.md/ | quote: "AGENTS.md is now stewarded by the Agentic AI Foundation under the Linux Foundation." | type: official
- [C8] Google AP2 = Agent Payments Protocol（2025-09-16 发布，60+ 机构），作为 A2A/MCP 的扩展做 agent 支付，VC+Intent/Cart Mandate | src: https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol | quote: "The protocol can be used as an extension of the Agent2Agent (A2A) protocol and Model Context Protocol (MCP)." | type: official
- [C9] A2UI = Google 的声明式 agent 生成 UI 协议（Apache 2.0，CopilotKit 参与），JSON 消息走 AG-UI/A2A 等 transport，客户端用自有组件渲染 | src: https://a2ui.org/ | quote: "A2UI enables AI agents to generate rich, interactive user interfaces that render natively across web, mobile, and desktop—without executing arbitrary code." | type: official
- [C10] MCP Apps 是官方 MCP 扩展（ext-apps），让 MCP server 返回 sandboxed iframe 交互 UI（`ui://` resource + `_meta.ui.resourceUri`），它统一了此前 MCP-UI 与 OpenAI Apps SDK 两套不兼容方案 | src: https://modelcontextprotocol.io/extensions/apps/overview | quote: "MCP Apps is an extension to the core MCP specification... MCP Apps let servers return interactive HTML interfaces (data visualizations, forms, dashboards) that render directly in the chat." | type: official
- [C11] AG-UI/MCP/A2A 在 CopilotKit 文档中是分层互补关系：MCP=agent↔工具数据，A2A=agent↔agent，AG-UI=agent↔用户界面 | src: https://docs.copilotkit.ai/ag-ui/introduction | quote: "Agent ↔ Tools & Data | MCP (Model Context Protocol)... Agent ↔ User Interaction | AG-UI... Agent ↔ Agent | A2A" | type: official
- [C12] ANP (Agent Network Protocol) 自称"Agentic Web 时代的 HTTP"，基于 W3C DID (did:wba) 的分层协议族，含身份/发现/IM/支付；v1.1 已发布 | src: https://github.com/agent-network-protocol/AgentNetworkProtocol | quote: "ANP aims to become the HTTP of the Agentic Web era: a protocol suite for agent identity, naming, discovery, negotiation, secure messaging" | type: official
- [C13] UTCP (Universal Tool Calling Protocol) 定位"说明书而非中间人"：agent 直调原生端点（HTTP/CLI/gRPC/MCP…），无需 wrapper server；有 UTCP vs MCP 官方对比表 | src: https://github.com/universal-tool-calling-protocol/utcp-specification | quote: "UTCP is a lightweight, secure, and scalable standard that enables AI agents and applications to discover and call tools directly using their native protocols - no wrapper servers required" | type: official
- [C14] UCP (Universal Commerce Protocol) = Google×Shopify 2026 共建的 agentic commerce 开放标准，transport 支持 REST/A2A/MCP，含 ECP (Embedded Commerce Protocol) 子协议 | src: https://developers.google.com/merchant/ucp | quote: "UCP is fully compatible with protocols such as AP2, A2A, and MCP. It supports transport REST API and MCP binding." | type: official
- [C15] x402 = Coinbase 的 HTTP 402 支付协议（stablecoin、机器付费），可跑在 HTTP/MCP/A2A transport 上；Google AP2 有 A2A x402 扩展 | src: https://github.com/coinbase/x402/blob/main/specs/x402-specification-v2.md | quote: "x402 is an open payment standard that enables clients to pay for external resources... transport layers: HTTP, MCP, A2A" | type: official
- [C16] NLWeb = 微软开源项目，让网站提供自然语言端点，每个 NLWeb 实例同时是 MCP server（"NLWeb is to MCP/A2A what HTML is to HTTP"）| src: https://github.com/nlweb-ai/NLWeb | quote: "Every NLWeb instance also acts as an MCP server (and soon A2A) and supports a core method, `ask`" | type: official
- [C17] Agora = 学术 meta-protocol（arXiv 2410.11905）：高频通信用结构化例程、低频用自然语言、中间用 LLM 写的例程，protocol document 以 SHA1 hash 标识 | src: https://arxiv.org/abs/2410.11905 | quote: "We introduce Agora, a meta protocol that leverages existing communication standards to make LLM-powered agents solve complex problems efficiently." | type: official

## conflicts
- ACP (Agentic Commerce) 发起方说法不一致：Stripe docs 写 "created by Stripe, OpenAI, and Meta"（https://docs.stripe.com/agentic-commerce/acp），GitHub README 写 "maintained by OpenAI and Stripe"、agenticcommerce.dev 写 "Stripe and OpenAI developed"。
- "AP2" 同名：Google 的是 Agent **Payments** Protocol（google-agentic-commerce/ap2）；ANP 的 ANP-10 是 Agent **Payment** Protocol，也缩写 AP2（agent-network-protocol spec 索引）。两者不同 spec。

## gaps
- OpenAI Apps SDK 官方页 developers.openai.com/apps-sdk 未逐字核对（仅经 OpenAI AAIF 公告间接确认其与 MCP Apps 的关系）。
- A2A 官方「A2A ❤️ MCP」互补定位页（google.github.io/A2A 或 a2a-protocol.org）未直接打开，只有第三方转述的 Google 原句。
- "A2A" 在支付领域也指 account-to-account payments，未找一手页面佐证。

## leads
- ANP — 中国社区主导的 DID 系 agent 网络协议族，用户搜 "agent protocol" 会碰到 https://agentnetworkprotocol.com/en/specs/
- Agentic Commerce Protocol (ACP#3) — ChatGPT Instant Checkout 背后的协议，与 IBM/Zed/AGNTCY 的 ACP 同名 https://github.com/agentic-commerce-protocol/agentic-commerce-protocol
- Agent Connect Protocol (ACP#4) — AGNTCY/Cisco，Internet of Agents 套件一部分 https://github.com/agntcy/acp-spec
- AGNTCY — Cisco 等发起的 agent 互联网基础设施项目，已捐 Linux Foundation https://github.com/agntcy
- AP2 (Google) — agent 支付，A2A 扩展 https://github.com/google-agentic-commerce/ap2
- UCP — Google×Shopify 商务协议，2026 新发布，绑 A2A/MCP https://developers.google.com/merchant/ucp
- x402 — Coinbase HTTP-402 机器微支付 https://docs.cdp.coinbase.com/x402/welcome.md
- MCP Apps — 官方 MCP UI 扩展，Claude/ChatGPT/VS Code 已支持 https://modelcontextprotocol.io/extensions/apps/overview
- MCP-UI — 社区 SDK，现为 MCP Apps 的实现/试验场；历史遗留实现需 legacy adapter https://mcpui.dev/
- OpenAI Apps SDK — ChatGPT app 的既有方案，正被 MCP Apps 吸收 https://developers.openai.com/apps-sdk
- A2UI — Google 声明式 UI 协议，AG-UI 是其 transport 之一 https://a2ui.org/
- UTCP — MCP 的"直调"替代叙事 https://github.com/universal-tool-calling-protocol/utcp-specification
- Agora — 学术 meta-protocol，常见于调研文章 https://agoraprotocol.org/
- NLWeb — 微软"HTML for agentic web" https://github.com/nlweb-ai/NLWeb
- AGENTS.md — 约定文件非协议，AAIF 托管 https://agents.md/
- AAIF — MCP/AGENTS.md/goose 治理归属变化，影响"谁拥有 MCP"的回答 https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
- MCP vs A2A — 官方口径互补（tool 层 vs agent 层），非竞争；AG-UI 再补 UI 层 https://docs.copilotkit.ai/ag-ui/introduction
- Agent Skills (SKILL.md) — Anthropic 的技能文件约定，易与 AGENTS.md 混淆 https://github.com/anthropics/skills
- Open-JSON-UI — CopilotKit 生态另一声明式 UI 格式 https://github.com/CopilotKit/generative-ui
