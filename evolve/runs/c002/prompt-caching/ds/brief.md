# brief: 各家大模型 API prompt caching 对比

## 读者与目标
用 LLM API 的开发者。5 分钟内弄清：各家缓存机制属于哪一类、要不要改代码、命中怎么计费、能活多久、怎么确认命中、什么操作会让缓存失效。成稿 ≤9000 字符。

## 范围内
- OpenAI prompt caching（自动）
- Anthropic prompt caching（cache_control）
- Gemini：implicit caching + explicit context caching（cachedContents）
- DeepSeek context caching（硬盘缓存）
- Kimi/Moonshot、智谱 GLM、通义千问 Qwen/DashScope
- OpenRouter 等网关如何透传/归一化缓存

## 范围外
- 本地推理框架（vLLM/SGLang 的 prefix cache）除非作为对照一句话提及
- 各家模型能力、价格全貌（只写与缓存相关的计费项）

## 用户点名疑点（成稿必须给结论）
1. "OpenAI/DeepSeek 自动、Anthropic 手动 cache_control" 现在还成立吗？（Gemini 已加 implicit caching，Anthropic 是否有自动模式？）
2. 命中后各家怎么计费（读折扣、写溢价、存储费）？
3. 缓存 TTL 各多久？
4. 怎么确认命中了（usage 字段名）？
5. 哪些改动会让缓存失效？

## 完成标准
- 矩阵每格 ✅ 或写明 ∅/❓
- 三条家族分类轴成立：自动前缀 / 显式断点 / 显式缓存对象
