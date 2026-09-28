# log

参数：rounds=3 workers=6 budget=9000 dir=./ds worker-model=swe-2-shim。主 agent 不搜网页。没有 pplx-safe。

## R0

观察：读者要分清四条（实际五个规范对象）各管哪一段接线。点名疑点是两种 ACP 是否同一件事、MCP SSE 是否废弃、四厂支持与变体、鉴权/版本/治理/选型。
决策：taxonomy v0 分类轴 = 线上两端的角色。5 行 × 10 列。R1 按来源边界拆开，不把厂商站和协议站混在一个工人里。scout 只产 leads，不进成稿。
spawn：0
结果：写出 brief.md、grid.md。网格 50 格全是 ❓。
字数：尚无 report。

## R1

观察：5 份协议笔记 + 1 份 scout。lint：142 条主张，0 条缺 src/quote；3 份笔记超 8000 字符（a2a、mcp、acp-zed），收束时只用带原句的主张。分类轴还能解释差异。ACP-IBM 的官网横幅、GitHub 讨论和 LF 博客都写并入 A2A，仓库 2025-08-27 归档，所以它不是现行替代品。两个 ACP 的全称和两端不同，且彼此官网都没写对方。MCP 传输页把「HTTP+SSE 传输自 2025-03-26 deprecated」和「Streamable HTTP 仍可用请求级 SSE」写在一起；这与旧教程相反，且只经一名工人摘录。vendors 五格都只有协议站名单。A2A 规范站 1.0.0 与 GitHub latest v1.0.1 冲突。若干枚举名在主张里出现、原句没覆盖，成稿不写。scout 点了 A2UI、WebMCP 等，按规则不直接进成稿。
决策：taxonomy v0→v1，只把 ACP-IBM 改记为 A2A 家族的已合并前身，不换轴、不加列。成稿从头写，SSE/initialize 不进第 0 节口号。厂商支持不写成已核实。
spawn：6（r1-mcp、r1-a2a、r1-acp-ibm、r1-acp-zed、r1-agui、r1-scout）。失败重派：0。
结果：report 见 roundstat。快照 snapshots/report.r1.md。
字数：R1 是第一份快照，无「越改越长」可比。新增了五协议对照；没有上一版可删。

R1 观察：vendors 全 ⚠（用户点名，缺厂商域名）；MCP 的 SSE 弃用与删除 initialize 是高影响旧识相反项，复核前不能进一屏；A2A version 为 ⚔，且 TaskState / security scheme 原名摘录不够；Zed transport 为 ⚔；AG-UI 事件家族原名不在摘录里。scout 的 A2UI 最容易和 AG-UI 混，但先让位给厂商站。 → 动作：R2 六份窄简报，不再全面重查。1) 回页复核 MCP 传输页与 changelog 的 SSE / initialize / Mcp-Session-Id 原句。2) OpenAI 域名。3) Anthropic 域名。4) Google 域名（含它自己发布的协议名，A2UI 只在这一份里取一句话）。5) Microsoft 域名。6) A2A 规范站对 GitHub v1.0.1，并补 TaskState 与 security scheme 的原句。 → 预计 spawn：6
