# log

## R0

观察：读者要分清 MCP、A2A、两种 ACP、AG-UI 各管哪条边，并要结论回答「两个 ACP 是否同一物」「MCP SSE 是否废弃」，以及 OpenAI / Anthropic / Google / 微软的官方支持、自家变体、鉴权、版本、治理、选型。

决策：taxonomy v0 用「通信边」做分类轴，第二轴用「线上对象的生命周期」。网格是 5 个协议 × 9 个维度，厂商采用另表。R1 按来源边界拆开，不派「把整题再查一遍」的工人。

spawn：0

结果：`brief.md`、`grid.md` 已写。未检索。

## R1

观察：6 份笔记都回来了（lint：130 条主张，全部 official，无缺 src/quote）。协议九列没有 ❓；Q-acp 可以下结论（两个全称、两条边，文档站互不点名）；Q-sse 可以下结论（HTTP+SSE 自 2025-03-26 deprecated，现行 HTTP 叫 Streamable HTTP），但移除日期是 ⚔。厂商 24 格和 4 个近邻全是 ❓。分类轴仍用通信边：它解释了矩阵里的主要差异。v0→v1 只把 F2 从「A2A 与 IBM ACP 并列」改成「A2A 现行，IBM ACP 为归档前身，欢迎页与对比页 ⚔」。

spawn：6（r1-mcp、r1-a2a、r1-acp-ibm、r1-acp-zed、r1-agui、r1-scout）。无失败，无重派。

结果：`report.md` 8996 字符（预算 9000）。快照 `snapshots/report.r1.md`。网格 ✅ 33、⚔ 13、❓ 36、∅ 2，resolved 35/84。来源节去掉标题才卡进预算。MCP 许可证 MIT 对 Apache-2.0 留在笔记，没进成稿。scout 的主张没有写入正文。

R1 观察：点名的两个疑点已经能用一手原句回答；剩下的大块 ❓ 是四家厂商和它们的自家变体。协议格子上的 ⚔ 已写进第 5 节，不改变「用哪条边」的选择。→ 动作：只派厂商核验，每人一家，顺手核这家的变体（OpenAI 的 Agentic Commerce Protocol、Google 的 AP2/UCP、微软的 Activity Protocol）。ANP、NLIP、LangChain Agent Protocol 先不派。→ 预计 spawn：4
