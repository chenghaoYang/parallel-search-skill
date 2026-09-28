# Log

## R0
观察：任务给了 4 个种子词 + 2 个用户点名疑点 + 4 家大厂支持矩阵。选定分类轴「协议连接的两端是谁」，可直接解释两个 ACP 为何撞名却不是一回事。
决策：taxonomy v0 = 3 族 5 实体 8 维度，见 grid.md。
下一步：R1 spawn 6（5 实体 + 1 scout）。

## R1 扩展（spawn 6/6 完成）
结果：MCP/A2A/ACP-IBM/ACP-Zed/AG-UI 各自 D1-D8 基本填满（94 条主张，87 official / 7 secondary，7 处 conflict 均已在笔记内自洽解释，非真冲突）。两个用户疑点都拿到一手来源结论：SSE 确认在 2025-03-26 被 Streamable HTTP 替换（deprecated，向后兼容保留）；两个 ACP 确认互不相关，IBM 版已 2025-08-27 归档并入 A2A。scout 额外发现 A2UI（Google）、AAIF（MCP 治理方）、AGNTCY（基础设施层）三个网格外实体。

## R1 收束
taxonomy 校验：分类轴「连接两端是谁」被数据证实成立（IBM ACP 归入 Agent 对等面且已并入 A2A，与轴的预测一致），不换轴。report.md v1 写入，7759 字符（budget 9000，余量 1241）。grid.md 按实际证据更新状态（核心 5 实体 8 维度基本 ✅，仅 ACP-IBM 的 D2/D3/D4 二手、ACP-Zed D4 缺口、AG-UI D5 二手；大厂矩阵 8 格 ❓/⚠ 待核实）。

观察：核心 taxonomy 和两个用户疑点已经有一手来源结论，但大厂支持矩阵里"未见官方表态"和"对方单方面公告"两类格子（OpenAI×A2A、Anthropic×ACP-Zed/AG-UI、Google×ACP-Zed/A2UI、Microsoft×ACP-Zed）需要从厂商自己的一手来源核实，且 AAIF 的确切治理关系（精确日期、与 Linux Foundation 整体的关系）未核实，这条影响「谁在治理」这一用户明确要求的问题。
动作：R2 定向简报 5 个（openai/anthropic/google/microsoft 各一 + governance 一个），每个都点名 grid.md 里要解决的具体格子。
预计 spawn：5

## R2 扩展（spawn 5/5 完成）
结果：41 条新主张（37 official/4 secondary）。重大更新：MCP 和 A2A 现已同属 AAIF（Linux Foundation directed fund）治理，精确日期核实（AAIF 成立 2025-12-09，A2A 并入 2026-08-27）；Google A2UI 确认为独立协议（非 AG-UI 别名）；Anthropic 对 A2A/ACP-Zed/AG-UI 均无一手确认（现有"支持"是对方单方面公告或适配器）；OpenAI 确认未提及 A2A/ACP-Zed/AG-UI；Microsoft 在 ACP-Zed 上出现一条真实冲突（GitHub Copilot CLI 文档称 public preview 但关联 issue 显示未实现）。

## R2 收束
report.md 整篇重写（不是追加），纳入治理更新和大厂矩阵精确化；先写到 9086 字符超预算，删除 1 条正文未引用的孤立来源 [31] 和 1 处引用错误后压到 8942（budget 9000，余量 58）。grid.md 用新的核实结果整体替换旧的 R1 草稿表格，避免新旧矩阵并存造成状态误判。taxonomy 未变（分类轴仍成立）。

观察：大厂矩阵 20 格里只剩 1 个真实冲突（⚔ Microsoft×ACP-Zed），其余 ❓/⚠ 都是"查证过官方渠道、结论就是没有"，不是缺口。核心 taxonomy、两个用户疑点、治理关系都已有多个一手来源交叉确认，置信度高。继续大规模扩查边际价值低，且会撑爆本就吃紧的字符预算。
动作：R3 只派 1 个工人专门核实这个冲突（GitHub Copilot CLI issue #222 与 public preview 文档是否矛盾、真实原因），随后直接进入终审（审稿工人抽查 ≥20 条主张），不再新开缺口。
预计 spawn：1（R3）+ 1（终审）

## R3 扩展（spawn 1/1 完成）+ 收束
结果：唯一剩余冲突解决——GitHub Copilot CLI 的 issue #222 是功能请求，2026-01-30 以"completed"关闭（功能已交付），不是"未实现"；ACP 支持已于 2026-01-28 正式 public preview。上一轮工人把"issue 已关闭"误读成"未实现"。
report.md 更新：Microsoft×ACP-Zed 从 ⚔ 改为 ✅（保留 VS Code 本体仍讨论中的准确区分），同步精简了几处冗余措辞腾出空间。写入后 9077 字符超预算，压缩到 8900（budget 9000，余量 100）。grid.md 大厂矩阵 20 格全部转为明确结论，无遗留 ❓/⚔。

观察：三轮扩展后，taxonomy 稳定、两个用户疑点有多源交叉确认、治理关系精确到日期、大厂矩阵无遗留冲突，只剩几条低价值二手来源（ACP-IBM 技术细节，协议已死）和不影响结论的缺口（ACP-Zed 状态归属、A2UI 端点规范）。rounds 参数（3）已用满，且上一轮改动的格子数量已经很少，符合"转终审"的触发条件。
动作：终审——派 1 个审稿工人，只给它 report.md 和 notes/，抽查 ≥20 条具体主张，产出 audit.md 判定；根据结果做最后一次不搜索的修订。
预计 spawn：1（终审）

## 终审（spawn 1/1 完成）
审稿工人抽查 report.md 正文 36 条具体主张，对照全部 12 份笔记：34 条 supported、2 条 weak（Anthropic×A2A、Anthropic×AG-UI，已经用 ⚠ 恰当标注，无需改）、1 条 unsupported（Google×MCP 标了 ✅，但引用的 [15] 其实是 AG-UI 集成页，不涉及 MCP）、0 条 contradicted。audit.md 已写入 ds/audit.md。

修订（不做新调研）：Google×MCP 从 ✅ 降级为 ❓，替换错误引用，同步改了「一屏看懂」里对应的大厂支持总结句；ACP-IBM 治理列的日期从"2025-08"统一为精确的"2025-08-27"。改完重新量字数：8997 字符（budget 9000，余量 3）。grid.md、log.md 同步更新，report.md 复制到仓库根目录 ./report.md。

## 收尾
三轮扩展（6+5+1=12 个工人）+ 1 个终审工人，共 13 次 spawn。两个用户点名疑点、四大厂支持矩阵、鉴权/治理/版本横切问题均已给出有一手来源支撑的结论；仅剩的开放项（A2UI 端点规范细节、VS Code/Copilot Chat 对 ACP-Zed 的时间表、ACP-IBM 二手鉴权细节、Google×MCP 未查到声明）已在 report.md 第 5 节列出，不影响核心结论。流程结束。
