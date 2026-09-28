# brief: 各家大模型 API 的 prompt caching 差异

读者：要在多家 LLM API 之间做选型/接线的开发者。目标：5 分钟建立「自动 vs 手动缓存」的家族认知，再按矩阵查计费、TTL、命中确认、失效条件。

## 用户点名的疑点（成稿必须有结论）
1. 「OpenAI 和 DeepSeek 是自动缓存、不用改代码；Anthropic 必须手动打 cache_control 断点」——截至 2026-09 还是否成立？（注意 Gemini 已加 implicit caching，OpenAI 是否有 manual 端点变化）
2. 命中之后各家怎么计费（写溢价/读折扣/存储费）？
3. 缓存能活多久（TTL、是否续期）？
4. 怎么确认命中了（usage 字段/响应标志）？
5. 哪些改动会让缓存失效（前缀匹配规则、排序、tool 定义变化等）？

## 范围内
OpenAI、Anthropic、Gemini（explicit context caching + implicit）、DeepSeek、Kimi(Moonshot)、智谱 GLM、通义千问/DashScope、OpenRouter（网关层）。

## 范围外
本地推理框架（vLLM/SGLang 的 prefix cache）、Embedding/批处理缓存、各云托管变体（Bedrock/Vertex/Azure）只在 leads 出现时入 §3 简述。

## 参数
rounds=3, workers=6, budget=9000, dir=./ds

## 完成标准
- 每个实体 × 每个维度有格状态；核心 4 家关键格 ✅ 或 ∅
- 5 条疑点全部有带 [n] 的结论
- 终稿 ≤9000 字符
