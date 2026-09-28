# grid v1（R1 收束后）

分类轴（不变）：**协议连接哪两端**。新增第五家族「商务/支付」与「非协议约定」桶（R1 scout 发现 4 个 ACP + 一批支付协议）。

| 家族 | 实体 |
|---|---|
| 应用 ↔ 工具/数据 | MCP（+UTCP 替代叙事、MCP Apps 扩展） |
| Agent ↔ Agent | A2A（IBM ACP 已并入）、AGNTCY ACP、ANP |
| 编辑器/客户端 ↔ Agent | Zed ACP |
| 前端 UI ↔ Agent | AG-UI（A2UI 为生成式 UI 层） |
| 商务/支付 | OpenAI/Stripe ACP、AP2、UCP、x402 |
| 非 wire 协议 | AGENTS.md、Agent Skills、NLWeb（半协议） |

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 |
|---|---|---|---|---|---|---|---|---|
| MCP | ✅ | ✅(AAIF) | ✅ | ✅ | ✅(OAuth2.1子集) | ✅(2026-07-28) | ✅ | ✅ |
| A2A | ✅ | ✅(LF) | ✅ | ✅ | ✅ | ✅(v1.0.1) | ⚠(MS一手缺) | ✅ |
| ACP-IBM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅(归档) | ✅(并入A2A) | ✅ |
| ACP-Zed | ✅ | ✅ | ✅ | ✅ | ✅ | ✅(wire v1) | ⚠(Claude经adapter) | ✅ |
| AG-UI | ✅ | ✅ | ✅ | ✅ | ⚠(spec不定义) | ✅(1.0) | ✅ | ✅ |

待反证的边界主张：
- B1 AG-UI「spec 不定义 authn/authz、无 WebSocket normative binding」（否定格）→ r2-agui-neg
- B2 Zed ACP「Claude Code 经 Zed 自研 adapter、非 Anthropic 原生」「远程传输 WIP」→ r2-zed
- B3 OpenAI「暂不加入 A2A 抽象」仅单 issue 来源；「Apps SDK built on MCP」未取到一手 → r2-openai
- B4 MCP「HTTP+SSE 移除时间表」未查 deprecated registry → r2-mcp-dep
- B5 Anthropic 对其他协议无表态（否定）→ r2-zed 顺带
- B6 微软 A2A 产品级一手页缺 → r2-msft
