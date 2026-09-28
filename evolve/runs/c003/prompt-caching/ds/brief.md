# brief — 各家大模型 API 的 prompt caching 对比

## 任务
产出一份对照文档，帮用户快速搞清楚各家 LLM API 的 prompt caching（上下文缓存）差异。

## 读者
要用 API 的开发者/技术决策者，5 分钟内建立认知，再按需查细节。

## 用户点名的疑点（成稿必须有明确结论）
1. 「OpenAI 和 DeepSeek 是自动缓存、不用改代码，Anthropic 必须手动打 cache_control 断点」——现在还是这样吗？
2. 命中之后各家怎么计费（写溢价？读折扣？存储费？）
3. 缓存能活多久（TTL、滚动续期、可配置？）

## 范围内
- 种子实体：OpenAI、Anthropic、Google Gemini（explicit context caching + implicit caching）、DeepSeek
- 点名扩展：Kimi/Moonshot、智谱 GLM、通义千问/DashScope、OpenRouter 等网关
- 用户需要知道的：怎么确认命中（响应字段）、什么改动会让缓存失效
- 相关 scope：其他有缓存的厂（xAI、Bedrock、Azure、Together 等）作为补充行

## 范围外
- 客户端/框架层缓存（LangChain cache、语义缓存、GPTCache）
- 非 prompt 级缓存（embedding cache、response cache）
- 推理加速本身（prefix caching 内核实现细节）

## 完成标准
- 对照矩阵每格有一手来源或明确标 ❓/∅
- 三个疑点各有一句带引用的结论
- 「怎么确认命中」「什么会失效」有专门节
- report.md ≤ 9000 字符
