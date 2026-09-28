# Log

## R0
框架定型：5 实体（MCP、A2A、ACP-IBM、ACP-Zed、AG-UI）× 10 维度 + 厂商支持矩阵。分类轴：按管辖层分 3 家族（模型↔工具 / agent↔agent / agent↔客户端UI）。
参数：rounds=3, workers=6, budget=9000, dir=./ds。

## R1
扩展：6 工人并行（mcp-core, mcp-authgov, a2a, acp-ibm, acp-zed-agui, vendor）。spawn 数 6。
收束：notes_lint 显示 131 claims（official 116/secondary 15），0 缺 src/quote，5 conflicts（实为版本演进非真冲突），24 gaps，16 leads。3 份笔记超 8000 字符但未超工具硬限。
taxonomy：分类轴成立未换，新增"治理成熟度梯度"作为家族解释力佐证。
两个用户疑点均已定论：ACP 撞名(IBM版已并入A2A归档；Zed版独立存活)；MCP SSE 已于2025-03-26软弃用/2026-07-28正式Deprecated。
report.md 首版 9895 字符超预算，经5轮压缩(删冗词、表格化、合并单元格)降到 8995/9000。
grid 状态：✅44 ⚠12 ❓5 ⚔0，resolved 72%。
R1观察 → 下一步：
- 关键但仅⚠的格子：ACP-Zed(D5鉴权/D7治理定性，仅rywalker.com二手)、AG-UI(D2核心事件列表，仅copilotkit二手) → 需一手核验
- 与常识/高影响的意外主张：MCP 2026-07-28"取消initialize握手趋于无状态" → changelog原句已引用，但需查lifecycle页确认"无状态"程度，避免过度解读
- 核心❓格子：ACP-IBM鉴权机制缺失；厂商矩阵中OpenAI×A2A、Anthropic×A2A、三家×AG-UI均为"未查到声明" → 需站内定向搜索确认是否穷尽
- 治理关系需一手佐证：MCP/A2A同属AAIF但"各自独立维护"表述来自secondary(pebblous.ai)非modelcontextprotocol.io/a2a-protocol.org官方原文
- Google A2UI vs AG-UI关系仅二手(levelup.gitconnected.com)
决策：R2 派 4 个窄工人（较R1的6个更少更聚焦），只打上述格子，不重新铺开。预计 spawn：4。

## R2
扩展：4 工人并行（mcp-lifecycle, acp-zed-verify, governance-verify, vendor-gaps）。spawn 数 4（累计10）。
收束：37 claims 全 official，0 secondary；1处小的src/quote缺失(vendor-gaps三条为搜索结果描述而非页面原句，可接受，均为"确认没找到"类结论)；2 conflicts(均为"官方未细化"而非真矛盾)。
关键结果：
- 确认：MCP 2026-07-28 协议级完全无状态(移除Mcp-Session-Id header,原句级证据)。
- **纠正**：ACP-Zed 治理并非R1二手来源所说"Zed单独主导",一手来源(agentclientprotocol.com/community/governance)证实为Zed+JetBrains联合治理,且官方声明目标是过渡到独立基金会。
- **纠正**：AG-UI与Google A2UI并非"疑似竞品",一手来源(Google官方博客+docs.ag-ui.com)证实为互补关系(UI组件规范 vs 传输协议)。
- 新增：IBM的Kate Blair正式加入A2A技术指导委员会(强化"真整合"证据)；OpenAI/Anthropic虽不在A2A早期合作伙伴名单但都是AAIF白金创始成员；Anthropic在AG-UI集成列表中(Claude Managed Agents/SDK)；OpenAI确认未在AG-UI集成列表。
report.md 重写：从R1的8995字符调整为9000字符（新增大量确认内容，靠删除章节间重复表述—IBM ACP archived/AG-UI-A2UI relationship 分别只在一处完整展开—维持预算）。
grid更新后：✅48 ⚠10 ❓2 ∅1，resolved 80%（较R1的72%提升）。
R2观察 → 下一步：
剩余缺口(ACP-IBM鉴权/VS Code信息来源/AAIF分级定义/OpenAI A2A发版计划)均为：(a)已死协议的次要细节，或(b)不影响taxonomy和核心结论的旁支，继续调研边际收益低于成本。核心格子(taxonomy、两个用户疑点、对照矩阵主要维度)已✅/∅为主。
决策：不再开R3扩展，进入终审。派1个审稿工人抽查≥20条具体主张。预计 spawn：1。

## 终审
spawn 数 1（累计11）。audit.md：抽查20条主张，覆盖各章节+两个用户疑点定论。结果：supported 19/20 (95%)，weak 1/20，unsupported 0，contradicted 0。
唯一weak点(MCP是否官方称"1.0/GA")：报告D10行已用"称production-grade，未称1.0"准确反映该不确定性，无需修改。
结论：report.md 无需改动，9000/9000字符，直接定稿。

## 最终状态
report.md（根目录，9000字符）与 ds/snapshots/report.r2.md 一致，即为终稿。
总计：2轮扩展(R1=6工人,R2=4工人)+1次终审(1工人)=11次spawn。grid resolved 49/61(80%)，剩余❓/⚠均为已死协议细节或不影响taxonomy的旁支，已在报告第6节"未决与置信度"如实列出。
两个用户点名疑点均有明确结论：ACP撞名(IBM版已死并入A2A/Zed版独立存活)；MCP SSE废弃(2025-03-26软弃用→2026-07-28正式Deprecated→迁移Streamable HTTP)。
