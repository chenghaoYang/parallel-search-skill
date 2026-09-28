# brief

任务：产出一份文档，帮读者理清「agent 时代」各种协议各管什么、有何不同。种子词：MCP、A2A、ACP、AG-UI。

读者：有一定工程背景的开发者/技术决策者，被各种缩写轰炸，需要 5 分钟建立认知 + 对照表 + 选型指引。

## 用户点名疑点（成稿必须给明确结论）
1. 网上说的 ACP 有两个：IBM 的 Agent Communication Protocol 和 Zed 的 Agent Client Protocol，是不是一回事？
2. 有人说 MCP 的 SSE 传输已经废弃了 —— 真的吗？

## 范围内
- 4 个种子协议 + 用户可能混淆的相关协议（变体/兼容层/同名歧义）
- 大厂支持矩阵：OpenAI、Anthropic、Google、微软各自支持哪些、有无自家变体
- 横向维度：鉴权、版本/稳定性、治理归属、怎么选

## 范围外
- 具体 SDK API 教程、如何写 server 的实操步骤
- LLM API 本身（Responses API / Messages API 不是「agent 间协议」，除非作为变体相关）

## 完成标准
- taxonomy：按「协议连接哪两端」分家族，能解释为什么这些协议不互相竞争
- 每个疑点有结论 + 来源
- 矩阵每格有 [n] 引用；字符数 ≤ 9000（含来源节）
