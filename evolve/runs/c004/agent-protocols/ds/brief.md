# Brief: agent 时代的「协议」 taxonomy

## 任务
产出一份对照文档，帮读者理清 agent 生态里的各种协议分别管什么、有何不同。

## 读者
知道 MCP 这个词、被一堆缩写搞晕的工程师。5 分钟建立认知：每个协议管哪条边界、谁治理、大厂各自站哪边、怎么选。

## 范围内
- 核心四协议：MCP（Model Context Protocol）、A2A（Agent2Agent）、ACP（两个同名）、AG-UI
- 大厂支持矩阵：OpenAI、Anthropic、Google、Microsoft 各支持哪些、有无自家变体
- 横向问题：鉴权、版本/稳定性、治理、选择建议
- leads 里出现且相关的邻近协议（MCP-UI、A2UI、ANP、AGNTCY、NLWeb 等）→ 简记或进「变体与适配层」

## 范围外
- 协议实现教程、SDK 用法细节
- 模型 API 本身（Responses API 只在「变体/支持」层面提）

## 用户点名疑点（成稿必须给结论）
1. ACP 有两个（IBM Agent Communication Protocol vs Zed Agent Client Protocol），是不是一回事？→ 结论：不是，层不同；IBM 那个后来的状态（并入 A2A？）要查清。
2. MCP 的 SSE 传输是否已废弃？→ 查清 spec 版本与替代传输（Streamable HTTP）。

## 完成标准
- 对照矩阵每格有 [n] 来源；正文事实可追到 notes。
- ≤ 9000 字符（含来源节）。
- 「一屏看懂」含两条疑点结论。
- 末尾有「未决与置信度」。
