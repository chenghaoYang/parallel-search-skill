# 简报（R0）

读者：要在 agent 系统里接线的工程师。几分钟内要能说出 MCP、A2A、两份都叫 ACP 的东西、AG-UI 各管哪一层、差在哪，以及 OpenAI / Anthropic / Google / 微软各自站在哪边。细节按表格往下查，不靠长文。

完成标准：

- 成稿有分类轴和家族，对照矩阵用官方原名（方法、对象、传输、版本号）。
- 用户点名的两个疑点有明确结论：IBM Agent Communication Protocol 与 Zed Agent Client Protocol 是不是一回事；MCP 的 SSE 传输是否已经废弃。
- 四大厂支持哪些协议、有没有自家变体，写进独立矩阵；官方没写的标 ∅，不靠传闻填。
- 鉴权、版本、治理、怎么选，各有一处可执行的说法。
- 成稿 `len()` ≤ 9000（含来源）。每轮重写，不许越改越长。
- 截至日期写进成稿抬头。每个具体事实能追到笔记主张。

范围内：上述协议的官方规范（角色、对象、传输、发现、鉴权、版本、治理、状态模型、彼此关系）；四大厂公开文档里的支持与变体；同范围内容易混名的协议（只在确认后决定是否进网格）。

范围外：某个 SDK 的安装教程、框架横评（LangGraph / CrewAI 等）、提示词技巧、自建网关的实现代码。

种子词：MCP (Model Context Protocol)、A2A (Agent2Agent)、ACP、AG-UI。

用户点名疑点（成稿必须给结论）：

1. 网上说的 ACP 有两个：IBM 的 Agent Communication Protocol，Zed 的 Agent Client Protocol。是不是一回事？
2. 有人说 MCP 的 SSE 传输已经废弃了。

工作约束：最多 3 轮扩展，每轮最多 6 个工人，预算 9000 字符。主 agent 不搜网页。没有 pplx-safe；工人用 web_search 找页、web_fetch 取原句。
