# R0 brief

## 任务复述
产出一份中文对照文档，让读者快速弄清 LLM 时代主流 API 请求协议的差异：
OpenAI Chat Completions、OpenAI Responses、Anthropic Messages、Google Gemini generateContent（4 个参照协议），
以及下游模型厂/平台「兼容 X 协议」时的偏差（DeepSeek、智谱 GLM、Kimi、Qwen/百炼、MiniMax、火山方舟等），
再加上跨协议迁移/接入时用户必须知道的坑。以 taxonomy 为骨架。

## 读者
写过至少一种 LLM API 调用、要在多家模型/多种协议之间做接入、迁移、网关或 SDK 适配的工程师。
读完 5 分钟内应能回答：
1. 四个参照协议各属于哪种「形状」，状态放在哪端，差异最大的是哪几处（工具调用、推理内容、流式、用量）。
2. 某个下游厂商说「兼容 OpenAI / 兼容 Anthropic」时，实际缺什么、多什么、语义哪里不同。
3. 换协议/换厂商时最容易踩的坑和处理方法。

## 范围内
- 文本生成主调用（请求/响应/流式）、工具调用、推理/思考、结构化输出、提示缓存与用量、鉴权/端点/版本。
- 参照厂商自家的兼容层（Anthropic 的 OpenAI SDK 兼容、Gemini 的 OpenAI 兼容）。
- 下游厂商的 OpenAI 兼容 / Anthropic 兼容 / Responses 兼容端点。
- 与之直接相关的开放规范或网关（如 Open Responses、OpenRouter、vLLM/Ollama、Bedrock Converse），视 scout 结果决定深度。

## 范围外
- Realtime/Live 语音 WebSocket 协议、Embeddings、图像/视频生成端点、Batch 细节、Assistants API 历史细节（只一句话）。
- 价格、模型能力评测、SDK 语言细节。

## 种子词
chat completions、Responses、messages、Google generateContent。

## 用户点名的疑点（成稿必须给结论）
- Q1：DeepSeek 官方的「response 协议」可能和 OpenAI 官方 docs 有很多不同 —— 到底哪里不同？DeepSeek 是否提供 Responses API？
- Q2：智谱的 Messages（Anthropic 兼容）对比 Anthropic 官方有什么不同？
- Q3：至少 4 个主流协议的系统对比。
- Q4：其他下游模型厂适配有什么不同。
- Q5：其他用户需要知道的问题。

## 完成标准
- 4 个参照协议 × 核心维度的格子全部 ✅ 或 ∅。
- DeepSeek、智谱两行的核心格子 ✅/∅，Q1/Q2 在「一屏看懂」里有明确结论。
- 成稿 ≤ 20000 字符，且快照长度逐轮不增长。
- 终审抽查 ≥ 20 条主张，contradicted 全部改正。

## 参数
rounds ≤ 4；workers ≤ 10/轮；budget 20000；dir ./ds；终稿同时写 ./report.md。
