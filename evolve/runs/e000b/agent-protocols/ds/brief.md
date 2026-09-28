# Brief

## 任务
产出一份文档，帮读者理清「agent 时代」几种「协议」分别管什么、有什么不同，快速建立认知 + 可查细节的对照表。

## 读者
正在评估要不要接入 MCP / A2A / ACP / AG-UI 的工程师。已经听过这几个名字，但分不清各自管什么、会混淆同名的 ACP。要的是「5 分钟建立心智模型 + 需要时能查到具体字段」，不是文献综述。

## 完成标准
- 读者看完「0. 一屏看懂」就能说清 4+1 个协议各管哪一层、不会再搞混两个 ACP。
- 每个具体事实（端点、传输方式、版本号、鉴权方式）能追到一手来源。
- 用户点名的两个疑点必须有明确结论（哪怕结论是「官方未直接声明，但间接证据指向…」）。
- report.md ≤ 9000 字符（硬上限，含来源节）。

## 范围内
- 核心四个 + 1：MCP、A2A、ACP（IBM Agent Communication Protocol）、ACP（Zed Agent Client Protocol）、AG-UI。
- 各协议：管什么层、传输/消息格式、鉴权、状态归属、治理方、版本/成熟度、采用者。
- 大厂支持矩阵：OpenAI、Anthropic、Google、Microsoft 官方支持哪些协议、有没有自家变体。
- 横切问题：鉴权模型对比、版本演进（含 SSE 传输是否废弃）、谁治理/开放程度、怎么选。
- scout 阶段发现的、确实在这个 scope 里且重要的关联协议/组织（如 Agntcy、LSP 作为设计参照)，视重要性简要收录，不展开。

## 范围外
- 支付类协议（AP2、x402 等）除非被证实是本 scope 核心概念，否则只在「未决/leads」提一句。
- 具体代码教程、SDK 安装步骤、定价。
- 与协议无关的 agent 框架比较（LangChain/CrewAI 等），除非作为「采用者」出现。

## 种子词
MCP (Model Context Protocol)、A2A (Agent2Agent)、ACP、AG-UI

## 用户点名疑点（必须在正文给结论）
1. 「ACP 好像有两个：IBM 的 Agent Communication Protocol 和 Zed 的 Agent Client Protocol，是不是一回事？」
2. 「MCP 的 SSE 传输已经废弃了？」→ 需确认精确版本号、日期、替代方案叫什么。
