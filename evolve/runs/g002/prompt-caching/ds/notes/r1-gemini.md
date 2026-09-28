# r1-gemini
question: Gemini API 官方的 implicit caching 与 explicit context caching 各是什么：要不要改代码、缓存单位、门槛、命中字段、读价/写价/存储价、TTL、失效、哪些模型。两条机制分开写。
checked: https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/caching?lang=python, https://ai.google.dev/api/caching, https://ai.google.dev/api/generate-content, https://ai.google.dev/gemini-api/docs/pricing, https://ai.google.dev/gemini-api/docs/changelog, https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/

## claims
- [C1] D1 两套机制。generateContent 页 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The Gemini API offers two different caching mechanisms" | type: official
- [C2] implicit D1 不用改请求。页 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "There is nothing you need to do in order to enable this." | type: official
- [C3] implicit 模型：2.5 及更新。页 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "enabled by default for all Gemini 2.5 and newer models." | type: official
- [C4] implicit D9 不保证省钱。页 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "no cost saving guarantee" | type: official
- [C5] implicit D2 相似前缀、短时间。页 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "requests with similar prefix in a short amount of time" | type: official
- [C6] implicit D3 Gemini 3.8 Flash 4096。页 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Gemini 3.8 Flash | 4,096" | type: official
- [C7] implicit D3 Gemini 3.7 Flash 4096 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Gemini 3.7 Flash | 4,096" | type: official
- [C8] implicit D3 Gemini 3.6 Flash 4096 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Gemini 3.6 Flash | 4,096" | type: official
- [C9] implicit D3 Gemini 3.5 Flash 4096 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Gemini 3.5 Flash | 4,096" | type: official
- [C10] implicit D3 Gemini 3.1 Pro Preview 4096 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Gemini 3.1 Pro Preview | 4,096" | type: official
- [C11] implicit D3 Gemini 2.5 Flash 2048 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Gemini 2.5 Flash | 2,048" | type: official
- [C12] implicit D3 Gemini 2.5 Pro 2048 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Gemini 2.5 Pro | 2,048" | type: official
- [C13] implicit D4 generateContent 指南只写 usage_metadata。页 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "cache hits in the response object's `usage_metadata` field." | type: official
- [C14] implicit D4 Interactions 页 2026-09-02：usage.total_cached_tokens | src: https://ai.google.dev/gemini-api/docs/caching | quote: "`usage.total_cached_tokens` (Python and JavaScript) field." | type: official
- [C15] Interactions 不支持 explicit。页 2026-09-02 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Explicit caching (manually creating and managing cache objects) is not supported in the Interactions API." | type: official
- [C16] 博客 2025-05-08 implicit D5：75% | src: https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/ | quote: "providing the same 75% token discount." | type: official
- [C17] 博客同日 implicit D4：cached_content_token_count | src: https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/ | quote: "see `cached_content_token_count` in the usage metadata" | type: official
- [C18] 博客同日旧门槛 | src: https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/ | quote: "2.5 Flash to 1024 tokens and 2.5 Pro to 2048 tokens." | type: official
- [C19] explicit D1 手动且保证省钱。页 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "manually enabled on most models, cost saving guarantee" | type: official
- [C20] explicit 创建 POST，路径在 v1beta。API 2026-09-11 | src: https://ai.google.dev/api/caching | quote: "post `https://generativelanguage.googleapis.com/v1beta/cachedContents`" | type: official
- [C22] explicit D8 字段 ttl（Duration，与 expireTime 互斥）。API 2026-09-11 | src: https://ai.google.dev/api/caching | quote: "`ttl` `string ( Duration format)`" | type: official
- [C23] explicit D8 默认 1 小时。指南 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "If not set, the TTL defaults to 1 hour." | type: official
- [C24] explicit D8 无上下限。指南 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "There are no minimum or maximum bounds on the TTL." | type: official
- [C25] explicit 引用字段 cachedContent | src: https://ai.google.dev/api/generate-content | quote: "Format: `cachedContents/{cachedContent}`" | type: official
- [C26] explicit D2 是 prompt 前缀。指南 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Cached content is a prefix to the prompt." | type: official
- [C27] explicit D9 到期自动删。指南 2026-09-11 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "before the tokens are automatically deleted." | type: official
- [C28] D4 API 字段 cachedContentTokenCount，未写只计哪一种 | src: https://ai.google.dev/api/generate-content | quote: "Number of tokens in the cached part of the prompt (the cached content)" | type: official
- [C29] explicit D5 后续请求降价 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "billed at a reduced rate when included in subsequent prompts." | type: official
- [C30] explicit D7 按 TTL 收存储 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "billed based on the TTL duration of cached token count." | type: official
- [C31] 定价 2026-09-23 不拆机制。gemini-2.5-flash 首表缓存价含存储 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.03 (text / image / video) $0.1 (audio) $1.00 / 1,000,000 tokens per hour (storage price)" | type: official
- [C32] gemini-2.5-pro 首块 ≤200k 缓存读价。>200k 与存储在相邻行 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.125, prompts <= 200k tokens" | type: official
- [C33] gemini-3.1-pro-preview 首块 ≤200k 缓存读价 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.20, prompts <= 200k tokens" | type: official
- [C34] gemini-3.8-flash 首块付费缓存读价至 2026-12-31 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.075 through December 31, 2026." | type: official
- [C35] 博客 2025-05-08：explicit 当时支持 2.5 与 2.0 | src: https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/ | quote: "supports our Gemini 2.5 and 2.0 models." | type: official

## conflicts
- 门槛：博客 2025-05-08「2.5 Flash to 1024 tokens and 2.5 Pro to 2048 tokens」vs 现行表「Gemini 2.5 Flash | 2,048」「Gemini 2.5 Pro | 2,048」。
- 折扣：博客「the same 75% token discount」vs 定价页不写 75%。2.5 Flash 输入「$0.30 (text / image / video)」，缓存「$0.03」。该格未声明属于哪套。
- 命中字段：`usage_metadata` / `cachedContentTokenCount` / `usage.total_cached_tokens` / `cached_content_token_count`。
- 免费与付费：指南「Context caching is a paid feature」；2.5 Flash 免费档「Not available」；3.8 Flash 首块免费档「Free of charge」。
- 存储是否含 implicit：explicit 节按 TTL 计存储；implicit 节不提。定价格把 storage price 写进同一 Context caching price。

## gaps
- D6 写价：caching、pricing、changelog、博客均无「创建按标准输入价」原句。
- explicit D3：只说 minimum varies by model，无分模型数字。implicit 表未声明也约束 explicit。
- implicit D8/D9：无用户 TTL、无过期秒数。不能写成无存储费。
- 2.5 Flash-Lite 有缓存价但不在最低 token 表。定价多块无档名，只引第一块。2.5 Pro/3.1 Pro 的 >200k 与 $4.50 storage 在相邻行，未并进 quote。
- changelog pattern cach 仅 2024-06-18 与 2025-04-16，无 implicit。最早 implicit 日期是博客 2025-05-08。

## leads
- Vertex：https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview
