# r1-cn-a
question: Moonshot Kimi API 与智谱 GLM（Zhipu BigModel 开放平台）API 各自的上下文缓存机制，在 D1–D10 十个维度上分别是什么？
checked: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://platform.kimi.ai/docs/pricing/chat, https://docs.bigmodel.cn/cn/guide/start/pricing

## claims
- [C1-Kimi-D1] Kimi 上下文缓存采用自动触发机制，无需手动创建缓存对象，当相同前缀在连续请求中出现时自动命中 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "Context Caching lets the server reuse your identical request prefixes" | type: official
- [C2-Kimi-D2] Kimi 要求前一个请求的 prompt tokens 超过 256 个才能触发缓存，低于 256 的请求不会被缓存 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "A new request can hit the prefix cache only when the previous request's prompt tokens exceed 256" | type: official
- [C3-Kimi-D3] Kimi 缓存粒度为前缀级别，采用最长前缀匹配 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "matches by longest prefix, and a successful match is a hit" | type: official
- [C4-Kimi-D4] Kimi K3 缓存命中读取计费为 $0.30/百万 tokens，是未缓存输入价格 $3.00/百万 tokens 的十分之一 | src: https://platform.kimi.ai/docs/pricing/chat | quote: "Cached input hits: $0.30 per million tokens... Input: $3.00 per million tokens" | type: official
- [C5-Kimi-D5] Kimi 缓存写入费用为 $3.00（5分钟 TTL）或 $6.00（1小时 TTL）每百万 tokens | src: https://platform.kimi.ai/docs/pricing/chat | quote: "Cache writes: $3.00 (5min TTL) or $6.00 (1h TTL) per million tokens" | type: official
- [C6-Kimi-D6] Kimi 缓存 TTL 有两个选项：5分钟（默认）或1小时，缓存在非活跃状态下自动过期，不支持手动清除 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "cache entries come in two time-to-live (TTL) tiers — 5min and 1h; if no TTL is specified, the 5min tier applies by default" | type: official
- [C7-Kimi-D7] Kimi Chat Completions API 缓存命中通过 usage.prompt_tokens_details.cached_tokens 字段确认，Messages API 使用 usage.cache_read_input_tokens | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "usage.prompt_tokens_details.cached_tokens (Chat Completions) or usage.cache_read_input_tokens (Messages API)" | type: official
- [C8-Kimi-D8] Kimi 缓存在 TTL 时间内处于非活跃状态后自动过期，不提供手动清除机制 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "expire automatically after it has been inactive for the selected TTL. Manual clearing isn't available." | type: official
- [C9-Kimi-D9] Kimi 支持上下文缓存的模型包括 Kimi K3、Kimi K2.7-code、Kimi K2.6 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "Kimi K3... Kimi K2.7 Code... Kimi K2.6" | type: official
- [C10-Kimi-D10] Kimi 缓存存储介质在官方文档中未披露 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "N/A" | type: official
- [C11-Zhipu-D1] 智谱 GLM 采用隐式（implicit）自动缓存机制，无需手动创建缓存对象 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "隐式缓存，智能识别重复的上下文内容" | type: official
- [C12-Zhipu-D2] 智谱 GLM 推荐缓存最小长度为 500+ tokens，短系统提示词（如几句话）通常无法触发缓存 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "sufficient length (recommended 500+ tokens)... Short system prompts like a few sentences typically won't trigger caching" | type: official
- [C13-Zhipu-D3] 智谱 GLM 缓存粒度为消息级别，稳定的系统提示独立缓存，与变量化用户查询分离 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "message-level caching where stable unchanging explanations, standards and knowledge bases in system prompts are cached separately from variable user queries" | type: official
- [C14-Zhipu-D4] 智谱 GLM 缓存命中计费约为标准价格的 50%，具体价格因模型而异 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "Cached tokens cost approximately 50% of standard rates" | type: official
- [C15-Zhipu-D5] 智谱 GLM 缓存存储当前限时免费，正式收费时按"元/百万 tokens/小时"计算 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "缓存存储（元/百万 Tokens/小时）限时免费" | type: official
- [C16-Zhipu-D6] 智谱 GLM 官方文档未明确规定缓存 TTL 或过期政策 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "N/A" | type: official
- [C17-Zhipu-D7] 智谱 GLM 缓存命中通过响应中 usage.prompt_tokens_details.cached_tokens 字段确认 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "usage.prompt_tokens_details.cached_tokens，showing exactly how many tokens were reused" | type: official
- [C18-Zhipu-D8] 智谱 GLM 官方文档未明确规定缓存失效条件，但注明缓存"异步生效"，建议请求间隔以获最佳效果 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "asynchronously effective... recommends waiting briefly between requests for optimal results" | type: official
- [C19-Zhipu-D9] 智谱 GLM 支持上下文缓存的模型包括 GLM-5.3、GLM-5.3-Flash、GLM-5.2、GLM-4.5-Flash 及所有主要 BigModel 产品线 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "All primary BigModel offerings (GLM-5.3, GLM-5.3-Flash, GLM-5.2, GLM-4.5-Flash) support context caching" | type: official
- [C20-Zhipu-D10] 智谱 GLM 缓存存储介质在官方文档中未披露 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "N/A" | type: official

## conflicts
- Kimi 与 Zhipu 对缓存最小长度的要求差异显著：Kimi 要求前一请求 prompt tokens > 256，Zhipu 推荐 500+ tokens | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api vs https://docs.bigmodel.cn/cn/guide/capabilities/cache

## gaps
- Kimi：是否支持缓存续期（TTL 刷新）；具体最小可缓存片段大小（是否有断点限制）
- Zhipu：具体 TTL 时长值；缓存过期/失效的精确条件；正式收费期间的存储费用具体数字
- 两平台：是否跨用户/API key 共享缓存内容

## leads
- Kimi 文档称缓存异步处理，建议验证其一致性保证机制
- Zhipu 缓存存储仍在免费试用期，需跟踪后续定价公布
