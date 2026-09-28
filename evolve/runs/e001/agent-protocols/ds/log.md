# Log

## R0
框定范围：MCP / A2A / ACP-IBM / ACP-Zed / AG-UI 五个实体 + 四大厂支持面。分类轴＝「协议连接的两端是谁」，直接解释疑点①。写 brief.md、grid.md（Grid A 实体×9维度，Grid B vendor×协议）。
计划 R1：6 workers，一实体一工人（来源边界），另加 1 scout。

## R1（6 spawn：r1-mcp, r1-a2a, r1-acp-ibm, r1-acp-zed, r1-ag-ui, r1-scout）
结果：144 claims（official 125 / secondary 19），5 conflicts（多为可编辑解释，非真冲突），25 gaps，19 leads。两个用户疑点核心事实均已有一手来源：① IBM ACP 已并入 A2A（2025-08-29 官方博客）、Zed ACP 连接对象完全不同（编辑器↔本地 agent）；② MCP SSE 传输 2025-03-26 起 deprecated、2026-07-28 正式 reclassify，替代 Streamable HTTP。scout 额外带回一个可能的「第三个 ACP」线索（AGNTCY，仅二手来源）。
收束：更新 grid.md v1；report.md 首版 5763 字符（预算 9000，留 ~3200 字符给 R2）；snapshots/report.r1.md。
观察 → 动作：Grid B（大厂支持面）全空且是用户明确要求 → 4 个 vendor 定向简报；AGNTCY 第三个 ACP 只有二手来源、且是高传播力信息 → 1 个一手来源核实简报；MCP 治理转移 LF 说法只有二手来源、治理是 taxonomy 核心列 → 1 个一手来源核实简报。预计 spawn：6。

## R2 计划
r2-openai / r2-anthropic / r2-google / r2-microsoft → 填 Grid B 四行（点名格子：Grid B 对应行全部列）
r2-agntcy-acp → 核实 grid.md「新发现」一节的第三个 ACP
r2-aaif-governance → 核实 Grid A「MCP」D2 治理转移主张（把 secondary 换成 official）+ AAIF/A2A 治理关系

## R2（6 spawn：r2-openai, r2-anthropic, r2-google, r2-microsoft, r2-agntcy-acp, r2-aaif-governance）
结果：70 claims（official 59 / secondary 11）。Grid B 四大厂行全部填上，多数 official。重大发现：AGNTCY 确有官方 "Agent Connect Protocol (ACP)"（github.com/agntcy/acp-spec），但已 2026-04-11 归档弃用——疑点①从"两个 ACP"升级为"三个，其中两个已并入/让位于 A2A"。MCP→AAIF 治理转移拿到精确日期(2025-12-09)+官方原句(Mike Krieger)。副产品：Anthropic 对 A2A 只是办过 webinar、GitHub issue 未采纳，对 ACP 明确拒绝——四大厂支持程度不对等。
收束：grid.md v2；report.md 重写，5763→6955 字符（budget 9000，余量约 2000）；snapshots/report.r2.md。taxonomy 未换轴，但补充了"agent↔agent 家族里 A2A 是唯一幸存者"的叙事，家族表加了活跃/死亡标记。
观察 → 动作：R2 notes 里有一条「影响大」的主张只有不完整二手来源支撑——"A2A 于 2026-08 作为 hosted project 加入 AAIF"（r2-aaif-governance C7 自己标注"需进一步核实"），且已经写进本版「一屏看懂」和矩阵，按规则必须先复核；AGNTCY 官方对 ACP 现状的表述在 Outshift 博客和 LF 公告之间不一致，值得再找一个更权威页面。两条都窄、都可能改变现有正文措辞（而非扩展新内容）。预计 spawn：2（远少于上一轮，因为核心内容已经扎实，只剩收尾核实）。

## R3（2 spawn：r3-aaif-a2a-date, r3-agntcy-status）
结果：10 claims（official 9 / secondary 1）。日期核实：AAIF 官方博客发布于 2026-08-17，确认 A2A 以 hosted project 身份加入（aaif.io/projects 同步列出）。AGNTCY 现状核实：acp-spec/acp-sdk 两仓库均于 2026-04-11 归档；现行官方文档（docs.agntcy.org、GitHub org profile README）的"七大组件"列表已完全不含 ACP，改列 SLIM 为"transport layer for...A2A"；但没有找到 AGNTCY 官方发布的正式弃用公告或原因说明——"让位于 A2A"是根据仓库归档+现有文档结构+一条非官方 GitHub issue 推断出来的，已在 report 里明确标注这一点，不当作官方原话呈现。
收束：report.md 重写，6955→7106 字符（budget 9000，余量约 1900），增长趋缓(+1192→+151)，说明主体内容已稳定；grid.md 90% 格子已解决(9/10 ✅，仅剩「AGNTCY 官方弃用原因」这个本质上问不出一手来源的格子，已归入未决）。snapshots/report.r3.md。
观察 → 动作：三轮扩展（R1+R2+R3=14 spawn）已覆盖 brief.md 定义的全部范围内条目，核心矩阵和两个用户疑点均为 ✅/官方来源，无剩余「高置信度缺口」值得再派工人；外层 rounds 参数(=3)已用尽。→ 进入终审阶段，不再扩展。

## 终审（1 spawn：audit-final）
audit.md：抽查 25 条主张，supported 21 / weak 2 / unsupported 1 / contradicted 0；自洽问题 2 处。核实后处理：
1. audit 指出"Anthropic MCP 矩阵标记错误"——核对 report.md 实际内容后确认是审稿工人读错列（Anthropic/MCP 格子本来就是"✅ 起源方"），**不是真问题，不改**（trust-but-verify：直接读源文件核实，未盲从审稿结论）。
2. AGNTCY "改推荐 A2A" 在 0.1 和第 3 节表格里表述过度确定（笔记明确说找不到官方弃用公告）——已改为只陈述可核实事实（仓库归档、SLIM 官方定位为"A2A 传输层"），去掉"改推荐"这个未经证实的因果断言。
3. OpenAI 对 A2A 的支持状态证据比 Anthropic 弱（笔记里在 gaps 而非 claims，未验证到官方一手声明）——矩阵单元格由 ❌ 改 ❓，「一屏看懂」第 5 条和「坑」第 3 条同步改措辞，不再把 OpenAI 和 Anthropic 的 A2A 姿态并列成同一种确定性。
收束：report.md 7106→7165 字符（budget 9000，余量约 1835）。snapshots/report.final.md。同步写入顶层 ./report.md（外层要求）。

## 结束
三轮扩展 + 一轮终审，共 15 次 spawn。两个用户点名疑点均已给出有一手来源支撑的结论（① 实际是三个撞名 ACP，两个已并入/让位于 A2A，只有 Zed 的还活着；② MCP 的 SSE 传输确认已废弃，替代方案 Streamable HTTP）。四大厂支持面矩阵、鉴权、治理、版本、选型坑均已覆盖。停止扩展。
