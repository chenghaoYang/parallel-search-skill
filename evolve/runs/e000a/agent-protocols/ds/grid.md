# Grid v1（R1 收束后）

## 分类轴（沿用 v0，R1 证据支持成立）
- **Family M（模型↔工具）**：MCP
- **Family A（agent↔agent）**：A2A、ACP-IBM（2025-08-25 起并入 A2A，历史实体）
- **Family C（agent↔客户端/UI）**：ACP-Zed、AG-UI
分类轴成立：三家族的治理成熟度也呈梯度（M/A 已基金会化，C 仍单一公司主导），解释力强，R2 不换轴。

## 主网格（实体 × 维度，R2 后）
| 实体\维度 | D1定位 | D2抽象 | D3传输 | D4状态 | D5鉴权 | D6版本 | D7治理 | D9关系 | D10成熟度 |
|---|---|---|---|---|---|---|---|---|---|
| MCP | ✅ | ✅ | ✅ | ✅(R2一手确认:协议级完全无状态) | ✅ | ✅ | ✅ | ✅ | ⚠(未称1.0/GA，用"production-grade") |
| A2A | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ACP-IBM | ✅ | ✅ | ✅ | ⚠(推断非明文) | ❓(协议已死,大概率不会再补) | ✅ | ✅ | ✅ | ✅(已停更/并入A2A) |
| ACP-Zed | ✅ | ✅ | ✅ | ⚠(客户端存线程,一手未细化) | ✅(R2一手:authenticate/methodId) | ✅ | ✅(R2**纠正**:一手证实Zed+JetBrains联合治理,非单一公司) | ✅ | ✅ |
| AG-UI | ✅ | ⚠(核心事件列表源copilotkit二手,官方页未逐条列出) | ✅ | ✅ | ✅ | ✅ | ⚠(官方GitHub Discussion,非正式治理文档) | ✅(R2**纠正**:与A2UI关系为互补非竞品,一手确认) | ✅ |

D8(厂商)见「厂商支持矩阵」。

## 厂商支持矩阵（R2 后）
| 厂商\协议 | MCP | A2A | ACP-Zed | AG-UI |
|---|---|---|---|---|
| OpenAI | ✅ | ⚠不在合作伙伴名单,但AAIF白金创始成员(治理层非产品级) | ⚠(第三方agent接入,非OpenAI官方声明) | ∅确认未在集成列表 |
| Anthropic | ✅(创造者) | ⚠同上+联合webinar | ⚠(同上) | ✅(R2一手:集成列表列Claude Managed Agents/SDK) |
| Google | ✅ | ✅(发起方) | ⚠(同上) | ✅集成方之一;另推A2UI(R2一手证实为互补非竞品) |
| Microsoft | ✅ | ✅ | ❓(仅Zed列VS Code,非MS声明) | ✅ |

## 用户疑点结论状态
- 疑点1（IBM ACP vs Zed ACP）：✅ 已定论——两个不同协议，IBM 版已死（并入A2A），Zed 版独立存活。
- 疑点2（MCP SSE 废弃）：✅ 已定论——2025-03-26 软弃用，2026-07-28 正式 Deprecated，见 changelog SEP-2596。

## R1→R2 变化
未换分类轴。R2 核实结果：
- MCP D4：从"⚠需核实无状态程度"升级为 ✅——一手确认协议级完全无状态，Mcp-Session-Id header 被整体移除，无协商握手。
- ACP-Zed D5：⚠→✅，官方 schema 定义 AuthenticateRequest/methodId。
- ACP-Zed D7：**纠正**——R1 二手来源(rywalker.com)说"Zed单独主导、非中立"，R2 一手来源(agentclientprotocol.com/community/governance)显示实为 **Zed+JetBrains 联合治理**，且官方明文"interim arrangement aims toward eventual transition to independent foundation status"。R1 的定性有误，已改用一手结论。
- AG-UI×A2UI 关系：**纠正**——R1 只有二手来源猜测"疑似竞品"，R2 一手来源(Google官方博客+docs.ag-ui.com)确认二者是互补关系：A2UI是生成式UI组件规范，AG-UI是agent↔前端传输协议，AG-UI官方"fully supports the A2UI spec"。
- 厂商矩阵：OpenAI/Anthropic 均非 A2A 早期合作伙伴名单成员，但都是现托管 A2A 的 AAIF 白金创始成员（治理层关系，非产品级声明）；Anthropic×AG-UI 从❓升级为✅（docs.ag-ui.com集成列表列出Claude Agent SDK）；OpenAI×AG-UI 从❓确认为officially absent。
- IBM 的 Kate Blair 已正式加入 A2A 技术指导委员会——补强"合并是真整合"的证据。
- 仍未一手确认："MCP/A2A在AAIF下各自完全独立维护"这句具体表述（A2A官方博客只说是"sibling projects"，未细化独立程度）。

## 决定：不再开 R3 扩展
剩余缺口（ACP-IBM鉴权机制官方从未写明/该协议已死；VS Code对ACP-Zed支持的信息来源是Zed非微软；AAIF成员分级定义）价值低、且是已死协议或次要旁支，继续派工人边际收益低。核心格子已 ✅/∅ 为主，进入终审阶段。

## Leads 汇总（暂不进正文，供R2判断是否值得追）
- AAIF 治理下 MCP/A2A"各自独立维护"的表述目前只有二手来源(pebblous.ai)，需一手确认（R2）
- Google A2UI 与 AG-UI 关系（竞争/合作）只有二手来源（R2 尝试）
- MCP 2026-07-28"去 initialize 握手"是否等于完全无状态，需查 lifecycle 页原文（R2）
- ACP-Zed 鉴权机制、治理定性目前全靠二手 rywalker.com，需查 agentclientprotocol.com 的 schema/协议页（R2）
- IBM 是否已加入 A2A 治理/指导委员会（R2 顺带查）
- OpenAI/Anthropic 对 A2A、三家对 AG-UI 到底是"没表态"还是"明确不做"，需各自站内搜索确认（R2）
- 范围外线索（本轮不追）：Agntcy(Cisco)、AGP 等协议名出现在比较文章标题中，未展开
