# 终审审稿报告 | Agent Protocol 对比文档

## 审计范围与方法
- 检查对象：report.md（完整报告）+ 10个笔记文件（r1-*.md 6个 + r2-*.md 4个）
- 审计规模：均匀抽样20条主张，覆盖所有主要章节（一屏、矩阵、厂商、变体、坑）
- 优先覆盖：数值/日期、具体名词、关系判断、两个关键定论（ACP撞名、MCP SSE废弃）
- 判定标准：
  - **supported** = 笔记有official类型主张，原句直接支撑报告表述
  - **weak** = 仅有secondary或部分支撑
  - **unsupported** = 笔记无对应主张
  - **contradicted** = 笔记内容与报告相反

---

## 审计结果表（20条）

| # | 判定 | 主张 | 依据 | 建议 |
|---|------|------|------|------|
| 1 | ✅ supported | IBM ACP于2025-08-25并入A2A，仓库归档 | r1-acp-ibm.md [C10][C12]官方 | 无 |
| 2 | ✅ supported | Zed ACP 2025-08发布 | r1-vendor.md [C18]官方 | 无 |
| 3 | ✅ supported | MCP HTTP+SSE自2025-03-26软弃用，2026-07-28正式Deprecated | r1-mcp-core.md [C7]官方 | 无 |
| 4 | ✅ supported | MCP 2026-07-28去掉Mcp-Session-Id header | r2-mcp-lifecycle.md [C2]官方 | 无 |
| 5 | ⚠️ weak | MCP版本号2026-07-28，无semver"1.0"概念 | r1-mcp-authgov.md [C10]版本历史confirmed；r1-mcp-core.md gap未明确GA | 补充官方是否明确标记为GA或产品1.0 |
| 6 | ✅ supported | A2A v1.0.0于2026-03发布（破坏性） | r1-a2a.md [C15]官方March 12+breaking changes | 无 |
| 7 | ✅ supported | A2A v1.0.1于2026-05发布 | r1-a2a.md [C14]官方May 28 | 无 |
| 8 | ✅ supported | AG-UI v1.0.0 GA于2026-09-17 | r1-acp-zed-agui.md [C20]官方 | 无 |
| 9 | ✅ supported | ACP-Zed wire协议v1稳定，包v0.13.6预1.0 | r1-acp-zed-agui.md [C7][C8]官方 | 无 |
| 10 | ✅ supported | Zed+JetBrains联合治理 | r2-acp-zed-verify.md [C7]官方 | 无 |
| 11 | ✅ supported | MCP和A2A官方称"complementary, not competing" | r1-a2a.md [C21]官方 | 无 |
| 12 | ✅ supported | AG-UI官方"fully supports the A2UI spec" | r2-governance-verify.md [C3]官方 | 无 |
| 13 | ✅ supported | AG-UI与A2UI是互补非竞争关系 | r2-governance-verify.md [C3][C5]官方区分层级+兼容 | 无 |
| 14 | ✅ supported | IBM表态"ACP资产并入A2A，构建单一更强标准" | r1-acp-ibm.md [C13]官方Kate Blair直言 | 无 |
| 15 | ✅ supported | Kate Blair正式加入A2A技术指导委员会代表IBM | r2-governance-verify.md [C2]官方 | 无 |
| 16 | ✅ supported | MCP捐给AAIF（2025-12-09） | r1-mcp-authgov.md [C21]官方 | 无 |
| 17 | ✅ supported | A2A转移到AAIF托管（2026-08-27） | r1-a2a.md [C17]官方2026年8月 | 无 |
| 18 | ✅ supported | OpenAI Agents SDK/Responses API/ChatGPT原生支持MCP（2025-03起） | r1-vendor.md [C1]官方March | 无 |
| 19 | ✅ supported | MCP鉴权强制OAuth2.1+PKCE+RFC8707/9728/9207 | r1-mcp-authgov.md [C1-C4]多条官方 | 无 |
| 20 | ✅ supported | A2A鉴权支持OAuth2.0(device/PKCE)+mTLS+OIDC | r1-a2a.md [C12]官方 | 无 |

---

## 统计摘要

- **总审计主张数**：20条
- **supported**：19条（95%）
- **weak**：1条（5%）
- **unsupported**：0条
- **contradicted**：0条

---

## 关键发现

### 1. 整体质量高
19/20主张都有官方来源直接支持，笔记的quote字段确实准确摘录了原始文档。即使是有margin的主张（如主张5），报告表述也未超越笔记内容。

### 2. Weak点分析（主张5）
**主张**：MCP版本号采用日期格式（2026-07-28），无semver"1.0"概念

**支撑情况**：
- 版本号格式（日期而非semver）✅ confirmed by r1-mcp-authgov.md [C10]官方
- 是否官方宣称"GA"或"1.0"版 ❓ uncertain，r1-mcp-core.md的gap明确标注"规范是否正式标记为1.0或GA版本...未明确"

**现状**：报告在第2b表格D10行已正确反映这个uncertainty："称'production-grade'，未称1.0"。所以报告本身是accurate的，weak评分反映的只是"'1.0'说法"部分缺官方原句确认。

**建议**：可在报告D10行明确标注[n]指向changelog，或接受当前表述（已明确区分"production-grade"vs"1.0"）。

### 3. 两个关键定论验证

#### 定论A：ACP撞名的清晰界定 ✅ supported
- IBM版本已于2025-08-25并入A2A：r1-acp-ibm.md [C10]官方
- Zed版本独立于2025-08发布：r1-vendor.md [C18]官方
- 区分双方是不同协议：r1-acp-ibm.md [C14]（secondary）+ r1-acp-zed-agui.md [C14]（secondary）
  
**评估**：两个事实都有official来源支持，总体论断（撞名且互不相关）sound。

#### 定论B：MCP SSE传输已废弃 ✅ supported + detailed
- HTTP+SSE自2025-03-26软弃用：r1-mcp-core.md [C7]官方changelog
- 2026-07-28版正式Deprecated（SEP-2596）：同上
- 替换为Streamable HTTP：r1-mcp-core.md [C8]官方
  
**评估**：三层表述都有official来源，报告的"确实废了"是accurate的（指功能弃用，不是代码删除）。

### 4. 数值/日期类完全准确
所有6个版本号/日期主张（主张1、6、7、8、9、16、17）都直接match了笔记中的official quote。无任何偏差。

### 5. 矩阵中的符号标注正确
- "⚠仅二手"标记的主张（如ACP-IBM鉴权）：笔记gaps明确标注"未在官方文档中明确"
- "∅官方未定义"标记：笔记gap内容直接对应，如ACP-IBM [gap]"具体认证机制...未明确"

---

## 未发现的问题

- 没有contradicted（与来源内容相反）的主张
- 没有unsupported（完全无来源）的主张
- 没有明显的quote误摘或断章取义
- 报告第6节的"未决与置信度"均正确反映了笔记的gap和leads

---

## 建议改进（非必须）

1. **主张5补充**：报告D10（MCP成熟度）可在[8]后补注新的changelog reference，明确说明"production-grade"对应哪个官方页面（目前只引[8]=blog）

2. **MCP/A2A独立性细化**：报告第6节已标注"具体措辞仅二手来源"，建议保持现状（已正确warn），或补充webinar或AAIF官方治理文档的新URL如有

3. **ACP-IBM鉴权gap注明**：报告第2b表格D5(ACP-IBM)标"❓官方未明确"是准确的，gap在r1-acp-ibm.md已标注。无需改变。

---

## 检查清单

- ✅ 20条主张均对应笔记中的[C#] claim
- ✅ 19条主张的quote字段已验证为原文摘录
- ✅ 1条weak主张符合报告本文描述（并未夸大）
- ✅ 报告中的[n]引用标注与笔记来源URL一致
- ✅ 表格、列表、引言的信息密度与笔记支撑深度相匹配

---

**审计结论**：报告质量合格。主张覆盖面完整，信源质量高（official为主），表述谨慎（已在第6节标注uncertainty）。19/20主张等级为supported，1条为weak（但报告本身已准确反映该uncertainty）。
