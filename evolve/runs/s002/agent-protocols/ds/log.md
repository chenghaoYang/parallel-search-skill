# 轮次日志

## R0

观察：任务是协议分层对照，不是单事实。用户疑点有两个（两份 ACP、MCP SSE）。预算 9000，轮数 3，每轮 ≤ 6 工人。

决策：taxonomy v0 以「对话两端」为分类轴，5 个实体 × D1–D9。厂商矩阵另表，R1 不填。R1 按来源边界派 5 个实体工人 + 1 个 scout。scout 只产 leads 和「坑」的一手原句，不进成稿正文。

预计 spawn：6。

## R1

spawn：6（r1-mcp、r1-a2a、r1-acp-ibm、r1-acp-zed、r1-ag-ui、r1-scout）。全部返回。lint：127 条主张，全 official，0 缺 src/quote；笔记有 5 份超过 8000 字符，收束时只采用带原句的主张。

结果：五份规范的 D1–D9 有一手原句。厂商 24 格仍是 ❓。⚔ 两处：A2A 规范站 1.0.0 对笔记里的 GitHub tag v1.0.1；IBM ACP 的合并公告对未更新的对比页。

taxonomy v0→v1：主轴「对话两端」能解释矩阵。补辅轴「工作单元」。IBM ACP 改为 A2A 的同层前身（2025-08-29 宣布停止独立开发，仓库 2025-08-27 归档），不再当成在营的第二套互操作协议。

成稿从头重写。字数 8025（预算 9000）。快照 `snapshots/report.r1.md`。为了把 SSE、两份 ACP、合并关系写进第 0 节，厂商矩阵只留在第 5 节，没有铺开。

R1 观察：用户要的厂商行全空；两份 ACP 的「是不是别名」和「2026-07-28 是否仍要求兼容旧 HTTP+SSE / SEP-2596 是否 Final」这两条边界主张还没反证。枚举名有几条摘录被截断，先不派，留给下一轮如果还影响正文。→ 动作：R2 只打厂商四行和两条反证，不重扫规范。→ 预计 spawn：6。

## R2

spawn：6（r2-openai、r2-anthropic、r2-google、r2-microsoft、r2-counter-acp、r2-counter-sse）。全部返回。lint：83 条主张（official 82 / secondary 1）；部分笔记用「同 C1」当 src，收束时只沿用能对上完整 URL 和原句的句子。

结果：厂商行从 ❓ 填成 ✅ 或 ∅。反证改了两条边界：SEP-2596 页是 Final，不是「尚未 Final」；2026-07-28 仍保留 HTTP+SSE 兼容小节，用词是 can maintain。两份 ACP 没有找到等同页。新撞车：AGNTCY Agent Connect Protocol（仓 2026-04-11 归档）、OpenAI Agentic Commerce Protocol。A2A 的 v1.0.1 有了 release 正文，和规范站 1.0.0 仍是 ⚔。

taxonomy v1→v2：ACP 缩写不构成家族。商业协议只在报告里占一行，不另开空网格。

成稿重写，不是追加。新增厂商表、四个 ACP、SSE 的 Final/can maintain。删掉的是：展开的 v2 方法、Part 四字段、JetBrains 以外的治理散文、以及摘录对不上的枚举。Zed/JetBrains 联合治理补回一句。字数 8025 → 7919（−106）。快照 `snapshots/report.r2.md`。

R2 观察：用户点名的两则疑点已有反证后的结论；厂商核心格是 ✅ 或有范围的 ∅；再挖枚举名会把正文顶长，而那些名字已在第 5 节标成摘录不完整。→ 动作：不派 R3 调研。进入终审，1 个审稿工人抽查 ≥20 条具体主张。→ 预计 spawn：1。
