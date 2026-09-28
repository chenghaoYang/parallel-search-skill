# brief: agent 时代「协议」对照文档

## 任务复述
产出一份中文文档，帮读者理清 MCP / A2A / ACP / AG-UI 分别管什么、有何不同；
并覆盖 OpenAI / Anthropic / Google / 微软各自支持哪些协议、有无自家变体；
以及鉴权、版本、治理、选型等需要知道的问题。

## 读者
有开发背景、被一堆「协议」名词搞混的工程师。目标：5 分钟建立 taxonomy + 大厂站位认知，细节可查表。

## 范围内
- MCP (Model Context Protocol)
- A2A (Agent2Agent)
- 两个 ACP：IBM Agent Communication Protocol、Zed Agent Client Protocol
- AG-UI (CopilotKit)
- 大厂采纳/变体：OpenAI、Anthropic、Google、Microsoft
- 横向维度：连接两端、治理方、传输、鉴权、版本现状、发现机制、与 MCP 关系
- scout 发现的范围内新实体（ANP、AGNTCY、A2UI、MCP Apps 等）按价值入网格

## 范围外
- 各协议的完整 API 教程、SDK 用法
- 非协议层的东西：function calling API 本身、模型接口、记忆框架
- 小众协议除非 scout 证明用户会混

## 用户点名疑点（成稿必须有明确结论）
1. 两个 ACP（IBM Agent Communication Protocol vs Zed Agent Client Protocol）是不是一回事？
2. MCP 的 SSE 传输是否已废弃？

## 参数
rounds=3, workers=6, budget=9000 chars, dir=./ds, 成稿同时写 ./report.md
