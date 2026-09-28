# Grid v1 — 实体 × 维度（R1 收束后）

## 分类轴（沿用）
「交互的两端是谁」→ 五家族；新增第二轴：线上协议 vs 负载格式/约定。
- L1 agent↔工具/数据：MCP（+官方扩展 MCP Apps）
- L2 agent↔agent：A2A、IBM-ACP(并入A2A)、AGNTCY ACP(疑弃)、ANP、AITP
- L3 agent↔界面/人：AG-UI(运行时事件流)；MCP Apps、A2UI=负载格式（骑在 L1/L2/L3 协议上）
- L4 应用/IDE↔agent：Zed ACP
- L5 agent↔支付/商业：ACP-commerce、UCP、AP2、x402
- 周边非协议：AGENTS.md（约定文件）、WebMCP（浏览器提案）、NLWeb（微软，端点即 MCP server）、MCP Registry（目录服务）

## 矩阵状态

| 实体 | D1层 | D2治理 | D3传输 | D4抽象 | D5版本 | D6鉴权 | D7大厂 | D8生态 |
|---|---|---|---|---|---|---|---|---|
| MCP | ✅ | ✅Anthropic→AAIF | ✅stdio/Streamable HTTP | ✅ | ✅2026-07-28 | ✅OAuth2.1可选 | ✅四家全支持 | ✅registry preview |
| A2A | ✅ | ✅Google→LF→AAIF | ✅3 bindings | ✅AgentCard/Task/Msg/Artifact | ✅v1.0.0 | ✅5种scheme | ✅G/MS/AWS | ✅150+组织 |
| IBM ACP | ✅ | ✅并入A2A 2025-08-29 | ✅REST | ✅ | ✅archived | — | ✅ | — |
| Zed ACP | ✅ | ✅agentclientprotocol org | ✅JSON-RPC/stdio+HTTP/WS | ✅session/* | ✅v1稳定 | ✅authMethods | ✅多家agent | ✅40+ |
| OpenAI/Stripe ACP | ✅ | ✅OpenAI+Stripe | ✅REST | ✅checkout_sessions/Delegate Payment | ✅2026-04-17 beta | ✅Bearer+签名 | ✅ChatGPT | ✅Stripe PSP |
| AGNTCY ACP | ✅ | ✅AGNTCY(LF Projects) | ✅REST/OpenAPI | ✅threads/runs | ⚠0.2.3 疑弃 | ❓ | ❓ | ⚠ |
| AG-UI | ✅ | ✅CopilotKit(非AAIF) | ✅传输无关 SSE/WS | ✅事件流 ~31类 | ✅npm 1.0.0 | ∅未定义 | ⚠框架集成多 | ✅ |
| MCP Apps/MCP-UI | ✅ | ✅MCP官方扩展SEP-1865 | ✅ui://资源+postMessage | ✅ | ✅2026-01-26 stable | ✅沙箱iframe | ✅OAI+Anthropic共建 | ✅ |
| A2UI | ✅ | ✅Google | ✅负载格式(非wire) | ✅声明式JSON UI | ✅v0.9.1 | — | ✅Google | ⚠ |
| AP2 | ✅ | ✅Google→FIDO TWG | ✅A2A/MCP扩展 | ⚠mandates细节未取 | ✅v0.2 | ❓ | ✅60+伙伴 | ⚠ |
| x402 | ✅ | ✅Coinbase→LF x402 Fdn | ✅HTTP 402 | ✅pay-and-retry | ✅2026-07-14 operational | ❓ | ✅40成员含Visa/MC | ✅ |
| UCP | ⚠ | ✅Google+Shopify 2026-01 | ⚠ | ⚠全链路 | ⚠ | ❓ | ✅20+背书 | ⚠ |
| AGENTS.md | ✅ | ✅OpenAI→AAIF | ✅Markdown约定 | — | ✅2025-08 | — | ✅60k+项目 | ✅ |
| WebMCP | ✅ | ✅W3C CG(Edge+Chrome) | ✅浏览器JS API | ✅registerTool | ✅draft/Chrome146 preview | ❓ | ✅MS+Google | ⚠ |
| NLWeb | ✅ | ✅Microsoft | ✅即MCP server | ⚠ | ⚠ | — | ✅MS | ⚠ |
| ANP / AITP | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ | ❓ | ⚠ | ⚠ |

## 大厂反向矩阵 ✅ 已填（r1-vendors）
- OpenAI: MCP✅(Responses/ChatGPT/Codex)、A2A❌(SDK不内置)、ACP-commerce发起、Apps SDK→MCP Apps、AGENTS.md发起
- Anthropic: MCP发起、Claude Integrations/API connector、MCP Apps共建；A2A/AG-UI 无表态(∅)
- Google: A2A发起、MCP✅(Gemini API/GenAI SDK/ADK/Cloud托管)、AP2/A2UI/UCP自家系
- Microsoft: MCP✅(全家桶+Steering Committee)、A2A✅(Foundry/Copilot Studio+TSC)、NLWeb、WebMCP 联合提案

## 待 R2 处理
- ⚔ AG-UI license（LICENSE=MIT vs docs 徽章 Apache）→ 以 LICENSE 为准，写进坑
- ⚠→✅ 需一手：UCP 传输/抽象（developers.googleblog under-the-hood 页）；AP2 核心抽象(mandates)
- ❓ AGNTCY ACP 是否有正式废弃声明（边界主张「事实上弃用」需反证）
- ❓ x402 鉴权/支付机制细节（签名方案）
- 边界主张待反证：「OpenAI 产品层无 A2A」「AG-UI 未入 AAIF」「Anthropic 无 A2A/AG-UI 表态」
