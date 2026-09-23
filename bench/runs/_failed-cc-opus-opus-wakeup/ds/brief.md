# brief（R0）

## 任务复述
产出一份中文对照文档：LLM 时代主流「对话生成」API 请求协议之间的差异（请求/响应形状、状态、工具、推理、流式、缓存、用量），
以及下游模型厂商「兼容」某个协议时，与协议所有者官方文档的落差。要求建立 taxonomy，详细但能快速建立认知。

## 读者
要同时接多家模型 API、写网关/SDK/Agent 框架、或把 Claude Code / Codex 类工具接到国产模型上的开发者。
熟悉 HTTP/JSON，至少用过一家 API；不需要科普什么是 LLM。

## 成稿要让读者在 5 分钟内建立的认知
1. 四个主流协议分属几个家族、根本差异在哪（消息 vs 条目 vs 内容块 vs parts；无状态 vs 服务端状态）。
2. 按维度查到精确字段名（端点、header、字段、枚举、事件名）。
3. 下游厂商的兼容层差在哪（哪些字段被忽略、推理字段怎么回传、缓存/用量字段名）。
4. 跨协议转换、接入时最常踩的坑。

## 范围
- 内：OpenAI Chat Completions；OpenAI Responses（含 Conversations）；Anthropic Messages；Google Gemini generateContent
  （含 Vertex 变体、OpenAI 兼容层、Interactions API 若存在）。
  下游适配：DeepSeek、智谱 GLM、Moonshot Kimi、MiniMax、阿里百炼 Qwen、火山方舟 豆包。
  生态（只看「暴露哪些协议 + 入口」）：Open Responses、OpenRouter、AWS Bedrock（Converse）、Azure OpenAI、vLLM/SGLang、Ollama、xAI、Mistral。
- 外：模型能力/价格/榜单；SDK 教程；Embeddings/图像/音频/Realtime 专用 API（除非影响对话协议）；Assistants API 细节（只记弃用状态）。

## 种子词
chat completions、Responses、Messages、generateContent

## 用户点名疑点（成稿必须给结论）
- Q1 DeepSeek 官方是否提供 Responses 协议？其 API 与 OpenAI 官方文档差在哪？
- Q2 智谱的 Anthropic Messages 兼容接口与 Anthropic 官方有什么不同？
- Q3 四个主流协议的逐维差异（taxonomy + 矩阵）。
- Q4 其他下游厂商适配的差异。
- Q5 其他用户需要知道的问题（坑、时效、迁移）。

## 完成标准
- 核心 4 行 × D1–D11 ≥ 80% 为 ✅ 或 ∅；Q1、Q2 有一手来源结论。
- 成稿 ≤ 20000 字符（含来源节），每轮快照都不超；每轮重写不追加。
- 终审抽查 ≥ 20 条具体主张。

## 参数
rounds=4（上限）, workers=10/轮（上限）, budget=20000, dir=./ds, 终稿同时写 ./report.md。
工人：subagent_type=research-worker；检索 `.claude/skills/deep-search/scripts/pplx-safe search "<q>" --json --timeout 180`（≤4 次/工人）+ WebFetch 一手页。
