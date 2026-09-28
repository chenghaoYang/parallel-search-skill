# Brief：各家大模型 API 的 prompt caching 对比

## 读者与目标
开发者，正在/将要调用一家或多家大模型 API，想知道 prompt caching（上下文缓存）在各家之间的差异，
尤其是「要不要改代码」「命中后怎么计费」「缓存能活多久」。目标：5 分钟内建立整体认知 + 可查字段级细节的对照表。

## 范围内
核心四家：OpenAI、Anthropic (Claude)、Google Gemini、DeepSeek。
扩展：Moonshot Kimi、智谱 GLM、阿里云通义千问 (DashScope)、OpenRouter（网关，缓存怎么透传/计费）。
维度覆盖：触发方式、最小可缓存长度、缓存粒度/断点、命中计费、写入计费、TTL、命中确认字段、失效条件、适用模型范围、存储介质。

## 范围外
本地推理框架的 KV cache（vLLM/SGLang 等自建服务）；非 prompt caching 的其他成本优化（Batch API、fine-tuning）除非与缓存直接互动；
非官方 SDK 包装层的实现细节。

## 种子词
OpenAI prompt caching；Anthropic cache_control；Gemini context caching / implicit caching；DeepSeek 上下文硬盘缓存。

## 用户点名的疑点（成稿必须给结论）
1. OpenAI 和 DeepSeek 是否仍是「自动缓存、不用改代码」？
2. Anthropic 是否仍必须手动打 cache_control 断点——现在还是这样吗（是否有自动/长 TTL 新变化）？
3. 命中之后各家怎么计费（折扣比例、是否有写入加价）？
4. 缓存能活多久，各家 TTL 差异？

## 额外必答
怎么确认命中了（响应里的字段/怎么看）；哪些改动会让缓存失效。

## 完成标准
一张覆盖 8 个实体 × 核心维度的对照矩阵；4 条点名疑点各有明确结论（或标注官方未写 ∅）；
「确认命中」「失效条件」独立成节；成稿 ≤ 9000 字符（含来源节）。
