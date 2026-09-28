# r2-domestic-deepen
question: 
1. Kimi API 官方文档中，响应体中表示"缓存命中token数"的字段，官方页面自己是怎么写的？
2. 智谱 GLM 的隐式缓存有没有 TTL（存活时间）？
3. 通义千问/DashScope 的隐式缓存 TTL 是多久？支持隐式缓存的具体模型有哪些？

checked: https://platform.kimi.ai/docs/api/chat, https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://www.alibabacloud.com/help/zh/model-studio/context-cache, https://www.alibabacloud.com/help/en/model-studio/context-cache

## claims
- [C1] Kimi：API响应体中用 `usage.prompt_tokens_details.cached_tokens` 字段表示缓存命中token数 | src: https://platform.kimi.ai/docs/api/chat | quote: "Number of tokens served from the cache (cache read)" | type: official
- [C2] Kimi：同时提供 `cache_write_tokens` 字段表示本次请求写入缓存的token数 | src: https://platform.kimi.ai/docs/api/chat | quote: "Number of tokens written to the cache by this request. Billed according to the TTL tier at write time" | type: official
- [C3] Kimi：这两个字段与未缓存部分互斥且总和等于 prompt_tokens | src: https://platform.kimi.ai/docs/api/chat | quote: "cached_tokens, cache_write_tokens and the uncached remainder are mutually exclusive and sum to prompt_tokens" | type: official
- [C4] 通义千问：隐式缓存没有固定有效期，系统定期清理长期未使用的缓存数据 | src: https://www.alibabacloud.com/help/zh/model-studio/context-cache | quote: "System will periodically clean up long-term unused cache data" | type: official
- [C5] 通义千问：隐式缓存支持 Qwen Max/Plus/Flash/Coder/VL 系列模型 | src: https://www.alibabacloud.com/help/zh/model-studio/context-cache | quote: "Qwen variants including Max, Plus, Flash, Coder, and VL models" | type: official
- [C6] 通义千问：隐式缓存还支持 DeepSeek、Kimi、GLM、MiniMax 等第三方模型 | src: https://www.alibabacloud.com/help/zh/model-studio/context-cache | quote: "DeepSeek variants, Kimi models, GLM series, and MiniMax" | type: official
- [C7] 通义千问：隐式缓存在多地域可用（北京、新加坡、美国弗吉尼亚、德国法兰克福、香港、日本东京） | src: https://www.alibabacloud.com/help/zh/model-studio/context-cache | quote: "China (Beijing), Singapore, US (Virginia), Germany (Frankfurt), Hong Kong, and Japan (Tokyo)" | type: official

## conflicts
- 无

## gaps
- [G1] 智谱 GLM 的隐式缓存 TTL：官方文档（https://docs.bigmodel.cn/cn/guide/capabilities/cache）未提及缓存数据的过期时间、存活时间或清理周期，仅说明缓存命中时的计费优惠（约50%折扣），以及触发缓存需要至少500个token的重复内容。

## leads
- 智谱可能在其他页面（如FAQ、定价页、API reference）有关于缓存数据清理周期的说明，需要进一步搜索
- 通义千问隐式缓存与显式缓存的TTL差异明显（隐式无固定期限 vs 显式5分钟），可用于不同场景
