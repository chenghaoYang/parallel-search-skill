# 调研日志

参数：rounds=3，workers=6，budget=9000，dir=./ds，worker-model=grok-4.7。无 pplx-safe。

## R0

观察：用户要的是边界 taxonomy，不是四个规范的说明书。点名疑点有两个：两个 ACP 是否同一协议；MCP 的 SSE 是否已废弃。大厂支持是核心格子，但和「协议自己是什么」不在同一个来源站。

决策：taxonomy v0 主轴 = 通信边界，辅轴 = 交互时态。行先只放四个种子（ACP 拆成 IBM / Zed 两行）。D8（大厂落地）不从协议官网的采用名单填。R1 按来源站拆 5 个协议工人 + 1 个 scout。厂商站留到缺口轮，避免 R1 变成「再全面查一遍」。

动作：写 brief / grid / log，不 spawn。

预计 spawn：0（R1 预计 6）。

## R1

spawn：6（r1-mcp、r1-a2a、r1-acp-ibm、r1-acp-zed、r1-agui、r1-scout）。全部返回。笔记 144 条主张，0 条缺 src/quote。六份笔记都超过 8000 字符，收束时只采用带摘录的主张。

lint：official 141 / secondary 3；conflicts 21；gaps 21；leads 21。

taxonomy：v0→v1 不换轴。主轴仍是通信边界，辅轴仍是交互时态。IBM ACP 从「并列现行标准」改成「同一家族里宣布并入 A2A 的前规范」。Zed ACP 不因缩写进这个家族。

成稿：从头重写 `ds/report.md`，8952 字（预算 9000）。快照 `snapshots/report.r1.md`。同步 `./report.md`。D8 整列空着，所以第 0 节不给大厂结论。SSE 与两个 ACP 的结论写进第 0 节，但同一节带上冲突原句；反证留到 R2，未把「SSE 这个机制已死」或「全站没有对方名字」写成定论。

网格：✅ 28，⚔ 11，❓ 5，∅ 1；resolved 29/45（64%）。五格 ❓ 全是 D8。

R1 观察：用户点名的两条疑点已有一手原句，但都是时间/排他类边界主张，还没专门找反例。D8 全空，而大厂支持是任务要求，不是边角。scout 的 leads 里，会改第 0 节的是「第三个 ACP」和「A2UI 把 AG-UI 说成传输、把自己说成载荷」。WebMCP、ANP、MCP Apps 这一轮不派。分类轴解释得了矩阵里的差异，不换轴。A2A Key Concepts 与三种绑定、AG-UI 16 与 31，笔记里已经是新旧页面并存，不必各派一个核验工人。字数 8952，下一版不得超过这一版。

R1 → 动作：两份反证（SSE；IBM ACP 是否还在独立演进）+ 四个厂商站。不派综合侦察。→ 预计 spawn：6。
