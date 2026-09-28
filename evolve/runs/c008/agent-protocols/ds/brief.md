# Brief: agent 时代的「协议」对照文档

## 读者与目标
中文读者（开发者/架构评估者），被一堆缩写淹没：MCP、A2A、ACP、AG-UI…
5 分钟内建立认知：每个协议管哪一段（agent↔tool / agent↔agent / agent↔UI / IDE↔agent / agent↔支付），谁发起谁治理，什么传输什么抽象，大厂各支持谁，怎么选。

## 用户点名的疑点（成稿必须有明确结论）
1. 「ACP」有两个/多个：IBM Agent Communication Protocol vs Zed Agent Client Protocol，是不是一回事？→ 结论：不是；且还有 OpenAI/Stripe Agentic Commerce Protocol、AGNTCY Agent Connect Protocol 也缩写成 ACP，需一并消歧。
2. MCP 的 SSE 传输是否已废弃？→ 需在 2025-03-26 / 2025-06-18 spec changelog 里拿到原句。

## 范围内
- 种子：MCP、A2A、ACP（全部消歧）、AG-UI
- 大厂支持矩阵：OpenAI、Anthropic、Google、Microsoft（顺带 IBM、Zed、CopilotKit、Amazon 若有官方信号）
- 横向：鉴权、版本、治理、选型建议
- 邻近实体（视 leads 决定纳入深度）：MCP-UI/MCP Apps、OpenAI Apps SDK、A2UI、AP2、x402、AGNTCY、ANP、AGENTS.md、WebMCP

## 范围外
- 非协议层的东西：各 agent 框架内部 API（LangChain 等本身不是协议，只在「谁支持」格子里出现）
- 协议逐字段教程、代码示例

## 完成标准
- taxonomy 一轴：按「交互的两端是谁」分家族
- 对照矩阵：实体 × 维度（层、发起/治理、传输、核心抽象、版本、鉴权、大厂支持）
- 用户两个疑点在「一屏看懂」有结论
- len(report.md) ≤ 9000 字符

## 参数
rounds=3, workers=6, budget=9000, dir=./ds, 成稿另写 ./report.md
