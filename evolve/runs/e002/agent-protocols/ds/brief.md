# Brief（R0）

## 任务
产出一份文档，帮读者理清 "agent 时代" 各种「协议」分别管什么、有什么不同，建立可快速查阅的 taxonomy + 对照矩阵。

## 读者
正在评估要不要 / 怎么在自己的 agent 系统里接入某个协议的工程师。已经听过这些名字、看过零散博客，但分不清谁管什么、谁包含谁。5 分钟内要能回答：「我现在的问题该用哪个协议」「这几个名字是不是在说同一件事」。

## 完成标准
- 4 个种子协议（MCP / A2A / ACP-IBM / ACP-Zed）+ AG-UI 各自「管什么」讲清楚，一句话可复述。
- 对照矩阵：同一组维度横向比较全部实体。
- 大厂矩阵：OpenAI / Anthropic / Google / Microsoft 各自支持哪些协议、有没有自家变体/框架。
- 用户点名疑点必须有明确结论（即便结论是「官方未写」）：
  1. IBM 的 Agent Communication Protocol 和 Zed 的 Agent Client Protocol 是不是一回事？
  2. MCP 的 SSE 传输是否已废弃？官方原话是什么？
- 覆盖鉴权、版本治理、governance body、选型建议。
- 字符预算 9000（硬上限，含来源节）。

## 范围内
MCP、A2A、ACP-IBM、ACP-Zed、AG-UI 五个协议的官方规范/文档；四大厂（OpenAI/Anthropic/Google/Microsoft）对这些协议的官方支持声明；IBM、Zed Industries、Linux Foundation、CopilotKit 等治理方的官方页面；鉴权机制、版本号规则、治理模式。

## 范围外
具体框架内部实现细节（LangChain/LlamaIndex 等，除非直接是某协议的官方 SDK）；协议的完整消息示例代码；未正式发布的传闻/路线图猜测；与本 5 个协议无直接关系的旧协议历史（LSP 只作为 ACP-Zed 的类比对象简要提及，不展开）。

## 种子词
MCP (Model Context Protocol)、A2A (Agent2Agent)、ACP、AG-UI。

## 参数
rounds=3, workers=6（每轮上限）, budget=9000 chars, dir=./ds, 最终文档同时写 ./report.md。
