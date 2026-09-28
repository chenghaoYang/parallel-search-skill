# Grid（更新于 R2 收束后）

## 分类轴（taxonomy backbone，R1-R2 确认成立）
按「协议连接的两端是谁」分族——能解释两个 ACP 撞名却不同类：IBM ACP 和 A2A 同属「Agent 对等面」（IBM ACP 已于 2025-08-27 并入 A2A），Zed ACP 和 AG-UI 同属「宿主应用面」。

| 族 | 连接两端 | 成员 |
|---|---|---|
| 工具/上下文面 | agent ↔ 工具、数据源 | MCP |
| Agent 对等面 | agent ↔ 另一个（可能跨厂商/跨框架）agent，任务委派 | A2A, ACP-IBM（已并入 A2A，历史实体）|
| 宿主应用面 | agent ↔ 承载它的宿主应用/UI/编辑器 | AG-UI（面向 web/app UI）, ACP-Zed（面向编辑器宿主，类比 LSP）|

## 维度
D1 定位层｜D2 传输/消息格式｜D3 鉴权模型｜D4 状态归属｜D5 治理与归属｜D6 版本与成熟度｜D7 采用者/参考实现｜D8 与其他协议关系

## 状态网格：协议本身
✅ 有一手来源+原文摘录 | ⚠ 只有二手 | ⚔ 冲突 | ❓ 缺口 | ∅ 官方未写

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 |
|---|---|---|---|---|---|---|---|---|
| MCP | ✅ | ✅ | ✅ | ✅ | ✅（AAIF, 2025-12-09 创始项目）| ✅ | ✅ | ✅ |
| A2A | ✅ | ✅ | ✅ | ✅ | ✅（LF 独立项目→2026-08-27 并入 AAIF）| ✅ | ✅ | ✅ |
| ACP-IBM | ✅ | ⚠（技术细节二手）| ⚠ | ⚠ | ✅ | ✅（已归档）| ❓ | ✅ |
| ACP-Zed | ✅ | ✅ | ✅ | ❓（不影响正文结论）| ✅ | ✅ | ✅ | ✅ |
| AG-UI | ✅ | ✅ | ✅ | ✅ | ⚠（无正式治理委员会文档，但已知 CopilotKit 主导）| ✅ | ✅ | ✅ |

## 疑点专项格（已解决）
| 疑点 | 结论 |
|---|---|
| IBM ACP vs Zed ACP 是否同一回事 | 不是同一回事，纯属撞名；两边官方文档互不提及；IBM 版已于 2025-08-27 归档并入 A2A |
| MCP SSE 传输是否已废弃 | 2025-03-26 版起用 Streamable HTTP 替换独立的 HTTP+SSE transport（deprecated，仅保留向后兼容）；2026-07-28 现行版标准传输只剩 stdio/Streamable HTTP |

## 大厂支持矩阵（R2 后，已核实）
| 厂商 | MCP | A2A | ACP-Zed | AG-UI | 自家变体 |
|---|---|---|---|---|---|
| OpenAI | ✅ | ❓已查证未提及 | ❓已查证未提及 | ❓已查证未提及 | AGENTS.md（非协议，文件约定，AAIF 创始项目）|
| Anthropic | ✅ 发起方 | ⚠仅联合 webinar，无正式声明 | ⚠Zed 建适配器，非原生 | ⚠仅对方集成页确认 | 无 |
| Google | ❓终审降级（原 ✅ 引用错误来源，AG-UI 页不涉及 MCP）| ✅ 发起方 | ✅ 官方确认（Gemini CLI 原生 --acp）| ✅ | A2UI：独立协议，与 AG-UI 互补 |
| Microsoft | ✅ | ✅ 原生 | ✅ Copilot CLI 原生（2026-01-28 public preview）；VS Code 本体讨论中 | ✅ 原生 | NLWeb（非协议，构建于 MCP 之上）|

## R3 结果（已完成）
Microsoft × ACP-Zed 的 ⚔ 已解决：issue #222 是功能请求，2026-01-30 以 "completed" 关闭（非"未实现"），Copilot CLI 的 ACP 支持已于 2026-01-28 正式进入 public preview（`copilot --acp`）。文档与 issue 不矛盾，是上一轮工人误读 issue 关闭状态。大厂矩阵 20 格现在全部是"查证过的明确结论"，无遗留冲突或缺口，转入终审。

## 不再追的低价值缺口（写入未决，不专门派工）
- ACP-IBM 技术细节仅二手：协议已死超一年，无实用价值
- ACP-Zed D4 状态归属未明确：不影响任何正文结论
- AGNTCY（Cisco/LF，65+ 公司）：基础设施层，与本文协议互补不竞争，篇幅原因不展开
- Goose（Block，AAIF 项目）：agent 框架/runtime，非协议，不收录
