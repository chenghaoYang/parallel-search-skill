# grid: 协议 × 维度 (taxonomy v1)

v0→v1：分类轴不变（连接哪两端），新增 F5 agent↔交易家族 + 「缩写撞名」问题升级为核心内容。
新增实体行：ACP-Commerce（OpenAI/Stripe）、AGNTCY-ACP（撞名表用）；周边实体（A2UI/MCP Apps/AP2/UCP/UTCP/ANP/WebMCP/NLWeb/NLIP）不进主矩阵，进「协议汤」表。

## 网格（主矩阵 5 行）

| 实体 | D1 两端 | D2 治理 | D3 传输 | D4 抽象 | D5 鉴权 | D6 版本 | D7 发现 | D8 大厂 | D9 vs MCP | D10 场景 |
|---|---|---|---|---|---|---|---|---|---|---|
| MCP | ✅ host/client↔server | ✅ Anthropic→AAIF | ✅ stdio/StreamableHTTP | ✅ tools/res/prompts | ✅ OAuth2.1 OPTIONAL | ✅ 2026-07-28 | ✅ discover+Registry | ✅ | — | ✅ |
| A2A | ✅ client↔remote agent | ✅ Google→LF→AAIF | ✅ RPC/gRPC/REST | ✅ Task/Message/Artifact | ✅ 5 schemes 带外 | ✅ v1.0.1 | ✅ agent-card.json | ✅ | ✅ 互补 | ✅ |
| ACP-Zed | ✅ editor↔agent | ✅ Zed/Apache | ✅ JSON-RPC/stdio | ✅ session/prompt | ✅ authenticate/authMethods(agent/terminal) | ✅ v1/v2草案 | ∅ | ⚠ Gemini CLI参考实现 | — | ✅ |
| ACP-IBM | ✅ agent↔agent | ✅ IBM→LF→并入A2A | ⚠ HTTP/REST | ⚠ run/agent | ❓ | ✅ 归档2025-08 | ⚠ | ⚠ | ✅ 并入A2A | ✅ BeeAI→AgentStack |
| AG-UI | ✅ backend↔UI | ✅ CopilotKit/MIT | ✅ 传输无关 | ✅ 31事件/run | ✅ spec明文不定义凭据 | ✅ spec 1.0 | ∅ | ⚠ | ✅ 互补 | ✅ |

## 大厂立场子表

| 厂商 | MCP | A2A | AG-UI | 自家 |
|---|---|---|---|---|
| Anthropic | ✅ 发起/捐AAIF | ⚠ webinar互补表态，无产品支持 | ⚠ quickstart示例 | — |
| OpenAI | ✅ SDK+Apps | ∅ 未见 | ∅ 走MCP Apps | ✅ ACP商务/AGENTS.md |
| Google | ✅ Cloud/ADK/Gemini | ✅ 发起 | ✅ ADK集成 | ✅ A2UI/AP2/UCP |
| Microsoft | ✅ Studio/Foundry/Win ODR | ✅ Foundry head | ✅ Agent Framework | ✅ NLWeb |

## 疑点判定
- Q1 两个 ACP 是否一回事 → ✅ 不是；实际 4 个缩写撞车（IBM/Zed/OpenAI-Stripe/AGNTCY），IBM 与 AGNTCY 两家已归档
- Q2 MCP SSE 废弃 → ✅ HTTP+SSE 传输 deprecated since 2025-03-26；SSE 格式仍在 Streamable HTTP 内部使用
