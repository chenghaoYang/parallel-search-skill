# 任务简报

读者：听过 MCP、A2A、ACP、AG-UI，但分不清各自管哪一段链路的工程师或技术负责人。不是协议实现手册。

成稿要在几分钟内建立的认知：

1. 这些协议按「谁和谁说话」分成几个家族，不是一组互相替代的标准。
2. 两个都叫 ACP 的东西是不是同一个协议。
3. MCP 的 SSE 到底废了没有：废的是哪一种传输、从哪一版起、替代物是什么。
4. OpenAI、Anthropic、Google、微软各自站在哪些协议上，有没有自家变体。
5. 选型看边界、鉴权、版本和治理，不看缩写热度。

范围内：

- MCP（Model Context Protocol）、A2A（Agent2Agent）、IBM Agent Communication Protocol、Zed Agent Client Protocol、AG-UI。
- 上述四家的官方支持与自家变体。
- 鉴权、版本、治理、传输弃用、发现方式、怎么选。
- 名字容易撞车、用户会踩坑的相邻规范（是否入格由调研决定，不预写结论）。

范围外：SDK 安装教程、博客观点综述、与这些协议无关的通用网络协议全文、本地代码。

种子词：MCP、A2A、ACP、AG-UI。

用户点名的疑点（成稿第 0 节必须给结论，结论可以是「官方没写」）：

1. IBM 的 Agent Communication Protocol 和 Zed 的 Agent Client Protocol 是不是一回事？
2. MCP 的 SSE 传输是不是已经废弃？废弃的是哪一种？

完成标准：

- taxonomy 能解释矩阵里的主要差异。
- 两个疑点有一手来源结论。
- 四家大厂的支持各有格子，不靠印象。
- `len(report.md) ≤ 9000`，后一轮重写而不是在末尾追加。
- 每个具体事实能追到笔记主张。

参数：rounds=3，workers=6，budget=9000，dir=./ds，工人模型 grok-4.7。检索只用 web_search 找页、web_fetch 打开一手页。没有 pplx-safe。
