# r2-gemini-explicit
question: Google Gemini API 的显式 context caching（CachedContent 资源，用 cachedContents.create 之类的 API 建立）具体怎么计费、TTL 是多久、支持哪些模型？
checked: https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/api/caching, https://ai.google.dev/pricing

## claims
- [C1] Explicit caching 的缓存读取价格为标准输入价格的 10%，相当于 90% 的折扣 | src: https://ai.google.dev/pricing | quote: "Context caching costs $0.075 per million tokens" (vs. $0.75 standard); "cached tokens are billed at reduced rates" | type: official
- [C2] Explicit caching 按小时收存储费，费率为 $0.50 / 1,000,000 tokens per hour（至 2026 年 12 月 31 日） | src: https://ai.google.dev/pricing | quote: "$0.50 / 1,000,000 tokens per hour (storage price)" | type: official
- [C3] 2026 年 1 月 1 日起，explicit caching 存储费翻倍至 $1.00 / 1,000,000 tokens per hour | src: https://ai.google.dev/pricing | quote: "doubling to $1.00/1M tokens/hour afterward" | type: official
- [C4] Explicit CachedContent 的默认 TTL 为 1 小时 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The default time-to-live is one hour" | type: official
- [C5] Explicit caching 支持通过 ttl 或 expireTime 字段自定义缓存过期时间 | src: https://ai.google.dev/api/caching | quote: "ttl: Time-to-live duration (e.g., '300s' for 5 minutes)" and "expireTime: Specific UTC timestamp in RFC 3339 format" | type: official
- [C6] Implicit caching 对 Gemini 2.5 及更新模型默认启用，自动应用成本节省 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models" | type: official
- [C7] Implicit caching 的成本节省也遵循相同的折扣率（90% 折扣） | src: https://ai.google.dev/pricing | quote: "We automatically pass on cost savings if your request hits caches" | type: official
- [C8] Implicit caching 没有显式的 TTL 配置，由系统自动管理 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "No manual configuration is required" for implicit caching | type: official
- [C9] Explicit CachedContent 支持 Gemini 3.8 Flash, 3.7 Flash, 3.6 Flash, 3.5 Flash, 3.1 Pro Preview（最小 4,096 令牌） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Gemini 3.8, 3.7, 3.6, 3.5 Flash and 3.1 Pro Preview: 4,096 tokens minimum" | type: official
- [C10] Explicit CachedContent 支持 Gemini 2.5 Flash & Pro（最小 2,048 令牌） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Gemini 2.5 Flash & Pro: 2,048 tokens minimum" | type: official
- [C11] Batch API 对缓存输入令牌额外提供 50% 折扣（基础 90% 折扣之上） | src: https://ai.google.dev/pricing | quote: "Gemini 3.8 Flash Batch pricing shows $0.0375 versus the standard tier's $0.075 for cached input tokens—representing a 50% reduction" | type: official
- [C12] Explicit caching 通过 cachedContents 资源在 /v1beta/ 端点上操作 | src: https://ai.google.dev/api/caching | quote: "API endpoint: `/v1beta/cachedContents`" | type: official

## conflicts
- 存储费率在不同日期不同：C2 表示至 2026 年 12 月 31 日为 $0.50/hour；C3 表示 2027 年 1 月 1 日起为 $1.00/hour。两个来源都是官方定价页面，没有实际冲突，但用户需明确了解价格变化时间点。

## gaps
- Explicit caching 是否有最大 TTL 限制（generate-content/caching 页面一处提到"no minimum or maximum bounds"，但需在官方 API 参考中确认）
- Implicit caching 在缓存超时前的具体行为（是否有固定周期，或完全由系统判断）
- Explicit caching 在批量请求中是否也享受 Batch API 的额外 50% 折扣

## leads
- Vertex AI 中 Gemini caching 的计费是否与原生 API 一致（可能有平台加价）
