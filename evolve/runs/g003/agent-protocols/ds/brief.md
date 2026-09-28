# R0 brief

读者：要在 agent 栈里选型的工程师。几分钟内要能回答「这几个缩写各管哪两端、能不能互换、大厂各自站在哪」。

成稿要建立的认知：

1. 用一条分类轴把协议分成几个家族，而不是按公司罗列缩写。
2. 四个种子协议各自的两端、核心对象、传输、发现、状态、鉴权、版本、治理。
3. 用户点名的两个疑点有明确结论：两个 ACP 是否同一件事；MCP 的 SSE 传输是否已废弃。
4. OpenAI、Anthropic、Google、微软各自官方支持哪些、有没有自家变体。
5. 怎么选：平面不重叠时是互补，重叠时才是替代。

## 范围内

- MCP（Model Context Protocol）
- A2A（Agent2Agent）
- ACP：IBM Agent Communication Protocol，以及 Zed Agent Client Protocol（先当两个实体，用一手来源判定是否同一协议）
- AG-UI
- 上述协议的鉴权、版本、治理、传输弃用、互操作定位
- OpenAI、Anthropic、Google、Microsoft 的官方支持与自家变体（变体必须是协议层或官方绑定层，不是一般产品功能）

## 范围外

- 某个 SDK 的安装教程、示例代码逐步讲解
- 与协议无关的 agent 框架横评（LangGraph / CrewAI / AutoGen 的编排能力本身）
- 模型质量、价格、提示词技巧

## 种子词

MCP, Model Context Protocol, A2A, Agent2Agent, ACP, Agent Communication Protocol, Agent Client Protocol, AG-UI, Agent User Interaction Protocol

## 用户点名、成稿必须给结论的疑点

1. 网上说的 ACP 有两个：IBM 的 Agent Communication Protocol，和 Zed 的 Agent Client Protocol。是不是一回事？
2. 有人说 MCP 的 SSE 传输已经废弃了。规范现在怎么写？
3. OpenAI、Anthropic、Google、微软各自支持哪些，有没有自家变体？
4. 鉴权、版本、谁在治理、怎么选。

## 完成标准

- taxonomy 的分类轴能解释矩阵里的主要差异；解释不了就换轴并记在 log。
- 疑点 1–4 在「一屏看懂」里各有一句带 `[n]` 的结论；官方没写就写 ∅，并说明查过的范围。
- 核心格子是 ✅、⚠、⚔ 或 ∅，不是沉默的 ❓。
- `ds/report.md` 字符数 ≤ 9000，且第 2 轮起不比上一轮更长。
- 最终同步一份到仓库根的 `report.md`。
- 边界主张（废弃、唯一、必须、自某版起、不支持）在写进「一屏看懂」之前要经过反证。

## 参数

- rounds 3，workers 6，budget 9000
- dir `./ds`
- 工人模型 grok-4.7；无 pplx-safe；工人用 web_search 找页、web_fetch 取原句
- 主 agent 不搜索网页
