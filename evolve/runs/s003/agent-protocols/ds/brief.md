# R0 brief

读者：要在 agent 系统里选型、对接的工程师。听说过 MCP、A2A、ACP、AG-UI，但分不清各自管哪条边界。

成稿要让他在几分钟内建立的认知：

1. 这几个协议不是同一层的替代品，而是不同边界上的接口。
2. 用户点名的两个疑点有明确结论：两个 ACP 是不是一回事；MCP 的 SSE 传输是否已废弃。
3. OpenAI、Anthropic、Google、微软各自官方支持哪些、有没有自家变体。
4. 鉴权、版本、治理、怎么选，能对着表做决定，而不是读一篇编年史。

## 范围内

- MCP（Model Context Protocol）
- A2A（Agent2Agent）
- ACP 的两个同名不同物：IBM Agent Communication Protocol；Zed Agent Client Protocol
- AG-UI
- 上面每个协议的：边界、核心对象、传输、状态/任务、发现、鉴权、版本与弃用、治理、和相邻协议的关系
- 四家大厂的官方支持与自家变体（协议层，不是产品功能清单）
- scout 找到、且会改变选型认知的相邻协议（例如容易和 AG-UI 混淆的 UI 协议）。进网格后再调研，不进成稿堆背景

## 范围外

- SDK 教程、逐步实现、性能基准、价格、prompt 技巧
- 未改变「这是哪一层」认知的小众协议编目
- 非官方博客里的传闻，除非用来定位一手来源

## 种子词

MCP (Model Context Protocol). A2A (Agent2Agent). ACP. AG-UI.

## 用户点名的疑点（成稿必须给结论）

1. 网上说的 ACP 有两个：IBM 的 Agent Communication Protocol，和 Zed 的 Agent Client Protocol。是不是一回事？
2. 有人说 MCP 的 SSE 传输已经废弃了。是否属实？从哪一版起、现行规范怎么写？
3. OpenAI、Anthropic、Google、微软各自支持哪些协议、有没有自家变体？

## 完成标准

- 工作目录 `./ds`。成稿 `./ds/report.md`，并复制到 `./report.md`。
- 字符上限 `len ≤ 9000`（含来源节）。每轮从头重写，不许越改越长。
- 扩展轮上限 3（R1 铺开，R2、R3 只打缺口和边界主张）。单轮工人 ≤ 6。
- 每个具体事实能追到笔记主张。疑点哪怕结论是「官方没写」也要写明查过什么。
- 至少两轮扩展之后才终审。最后一步是收束，不是扩展。

## 参数

- rounds 3 / workers 6 / budget 9000 / dir ./ds
- 工人模型 `swe-2-shim`。没有 pplx-safe。检索只用 web_search + web_fetch。
- 截至日期以来源页面上的版本号为准；任务日 2026-09-24。
