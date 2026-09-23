# brief（R0）

## 任务复述
产出一份对照文档，帮用户理解 LLM 时代推理 API **请求协议**的差异：
1. 四个主流/源头协议：OpenAI Chat Completions、OpenAI Responses、Anthropic Messages、Google Gemini `generateContent`。
2. 下游模型厂的兼容适配差异（DeepSeek、智谱 GLM/Z.ai、Kimi、MiniMax、Qwen/百炼、豆包/方舟…）：兼容哪个协议、哪些字段支持/忽略/报错、私有扩展。
3. 其他用户需要知道的问题（跨协议迁移、网关、坑）。
骨架是 taxonomy：先分家族，再按维度比细节。

## 读者
写 LLM 应用或多模型网关的工程师，懂 HTTP/JSON/SDK。要在 5 分钟内建立：有几种协议家族、它们在哪些维度不同、兼容层通常缺什么/多什么；之后能按需查到原始字段名。

## 范围
- 内：HTTP/JSON 推理请求协议表面——接入/鉴权、对话形状、多模态块、工具调用、状态、推理(thinking)、结构化输出与长度、流式、响应/停止原因/用量、提示缓存、错误；官方原生协议 + 厂商兼容层 + 常见网关/自托管服务器的协议表面。
- 外：价格（除非体现在协议字段）、模型能力评测、Realtime/Live 语音 WebSocket（只提存在）、Embeddings/图像生成/Batch/Files（只提存在）、SDK 代码写法、Agent 框架。

## 种子词
chat completions、Responses、Messages、Gemini generateContent。

## 用户点名的疑点（成稿 §0 必须有结论）
- Q1 DeepSeek 官方"response 协议"是否与 OpenAI 官方 docs 有很多不同？（有没有 Responses API；Chat Completions 兼容层差异：reasoning_content、忽略参数、thinking+工具回传规则、Anthropic 兼容端点）
- Q2 智谱的 Messages（Anthropic 兼容）与 Anthropic 官方 Messages 有何不同？
- Q3 四个主流协议的差异与 taxonomy。
- Q4 下游模型厂适配差异（≥ 6 家）。
- Q5 其他用户需要知道的问题（坑、网关、新协议）。

## 参数
rounds 4 · workers ≤ 10/轮 · budget 20000 字符（含来源）· dir ./ds · 成稿同时写 ./report.md

## 完成标准
- 4 个核心协议 × 核心维度（D2 D4 D5 D6 D8 D9）全部 ✅ 或 ∅。
- Q1、Q2 在 §0 有结论且有一手来源。
- ≥ 6 家下游厂商有差异表。
- 终审抽查 ≥ 20 条主张，contradicted 全部改正；终稿 ≤ 20000 字符。
