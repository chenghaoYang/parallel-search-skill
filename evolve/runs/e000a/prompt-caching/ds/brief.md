# Brief：各家大模型 API 的 prompt caching 对比

## 读者与目标
读者：正在多家模型 API 之间选型/接入的工程师，关心成本和延迟。要在 5 分钟内看懂：
谁自动缓存、谁要手动改代码、命中后怎么算钱、缓存能活多久、怎么确认命中、什么操作会打掉缓存。

## 范围内
核心四家（必须深入）：
- OpenAI Prompt Caching
- Anthropic `cache_control`（Claude）
- Google Gemini context caching（显式 CachedContent + 隐式 implicit caching）
- DeepSeek 上下文硬盘缓存（Context Caching on Disk）

第二梯队（至少给出关键事实，不要求同等深度）：
- Moonshot Kimi API context caching
- 智谱 GLM（open.bigmodel.cn）
- 阿里通义千问 / DashScope（上下文缓存）
- OpenRouter（网关，透传/归一化各家缓存的方式）

可选变体层（时间允许再做，属于 P2）：Azure OpenAI、AWS Bedrock（Claude）、Google Vertex AI（Gemini）在缓存行为上与「原厂」API 的差异。

## 范围外
微调缓存、embedding 缓存、HTTP/CDN 缓存、自建推理框架（vLLM/SGLang 等）的 KV cache 复用（除非作为 taxonomy 引言里一句话的背景概念）、价格计算器工具、仅控制台可见但无 API 对应的设置。

## 用户点名的疑点（成稿必须给出明确结论）
1. 「OpenAI 和 DeepSeek 是自动缓存、不用改代码，Anthropic 必须手动打 cache_control 断点——现在还是这样吗？」→ 对四家（+第二梯队）逐一给出当前真实机制，标出与「传言」不符的地方。
2. 命中之后各家怎么计费（折扣比例、写入是否额外收费、是否分档计价）。
3. 缓存能活多久（默认 TTL、能否延长/自定义）。
4. 怎么确认命中了（响应里具体哪个字段）。
5. 哪些改动会让缓存失效。

## 完成标准
- `report.md` ≤ 9000 字符（含来源节），可多次收束重写。
- 建立 taxonomy（分类轴 + 家族 + 正交维度清单），后续矩阵按此排列。
- 至少覆盖 8 个实体：OpenAI、Anthropic、Gemini、DeepSeek、Kimi、智谱、通义千问、OpenRouter。
- 5 个用户疑点在正文（多为「0. 一屏看懂」或对照矩阵）中有明确结论，而不是「因供应商而异」这种空话。
- 每个具体事实可追到笔记里的 `[C#]`/URL；没来源的进「未决」节，不进正文。

## 种子词
OpenAI prompt caching；Anthropic cache_control；Gemini context caching / implicit caching；
DeepSeek 上下文硬盘缓存 / context caching on disk；Kimi context caching；智谱 GLM 缓存；
通义千问 / DashScope 上下文缓存；OpenRouter prompt caching。
