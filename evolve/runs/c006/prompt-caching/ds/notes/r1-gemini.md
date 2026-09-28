# r1-gemini
question: Google Gemini API 的显式 context caching（CachedContent）与隐式 implicit caching：机制、计费、TTL、命中确认字段、失效条件
checked: https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/api/caching, https://ai.google.dev/api/generate-content, https://ai.google.dev/gemini-api/docs/pricing, https://ai.google.dev/gemini-api/docs/optimization, https://ai.google.dev/gemini-api/docs/changelog, https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/

## claims

### 显式 explicit (CachedContent)
- [C1] 显式缓存 = 先建 CachedContent 资源再按 name 引用；Python: `client.caches.create(model=..., config=types.CreateCachedContentConfig(..., ttl="300s"))`，请求里 `GenerateContentConfig(cached_content=cache.name)` | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "you can pass some content to the model once, cache the input tokens, and then refer to the cached tokens for subsequent requests" | type: official
- [C2] REST 端点 `POST https://generativelanguage.googleapis.com/v1beta/cachedContents` 创建缓存（body 为 CachedContent），generateContent 请求里传 `"cachedContent": "$CACHE_NAME"` | src: https://ai.google.dev/api/caching | quote: "post /generativelanguage.googleapis.com /v1beta /cachedContents" | type: official
- [C3] 显式缓存仍是 Beta，走 v1beta | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Explicit context caching is currently in Beta. Endpoints and SDK methods are available under v1beta." | type: official
- [C4] TTL 默认 1 小时，可自定，无上下界 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "If not set, the TTL defaults to 1 hour. ... billed based on the TTL duration of cached token count. There are no minimum or maximum bounds on the TTL." | type: official
- [C5] 过期字段是 expireTime 与 ttl 二选一 union；`cachedContents.patch` 只能改过期时间 | src: https://ai.google.dev/api/caching | quote: "Updates CachedContent resource (only expiration is updatable)." | type: official
- [C6] `cachedContents.delete` 可手动删缓存 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The caching service provides a delete operation for manually removing content from the cache." | type: official
- [C7] 缓存对象除过期外全部不可变：contents/tools/systemInstruction/toolConfig/model/displayName 均标 Immutable；改任何内容须新建缓存 | src: https://ai.google.dev/api/caching | quote: "Required. Immutable. The name of the Model to use for cached content Format: models/{model}" | type: official
- [C8] 缓存只能用于创建时指定的模型 | src: https://ai.google.dev/api/caching | quote: "Cached content can be only used with model it was created for." | type: official
- [C9] 计费=缓存 token 按折扣价计 + 存储按时长计 + 非缓存输入/输出照常 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Cache token count: The number of input tokens cached, billed at a reduced rate when included in subsequent prompts. Storage duration: The amount of time cached tokens are stored (TTL), billed based on the TTL duration of cached token count." | type: official
- [C10] 存储价（每 1M tokens/小时）：2.5 Pro $4.50；2.5 Flash/Flash-Lite $1.00；3.8/3.7/3.6 Flash $0.50（至 2026-12-31，之后 $1.00）；3.5 Flash 等 $1.00；3.1 Pro Preview $4.50 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$4.50 / 1,000,000 tokens per hour (storage price)" | type: official
- [C11] 命中读取价 "Context caching price"：2.5 Pro $0.125（≤200k）/$0.25（>200k）；2.5 Flash $0.03（audio $0.1）；2.5 Flash-Lite $0.01；3.1 Pro Preview $0.20/$0.40；3 Flash Preview $0.05 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.125, prompts <= 200k tokens" | type: official
- [C12] 命中确认字段：generateContent 响应 `usageMetadata.cachedContentTokenCount`（Py: `usage_metadata.cached_content_token_count`）；缓存 token 数也在 cache create/get/list 的 usage_metadata 返回 | src: https://ai.google.dev/api/generate-content | quote: "cachedContentTokenCount integer. Number of tokens in the cached part of the prompt (the cached content)" | type: official
- [C13] 显式缓存支持多模态内容（官方示例缓存视频文件 mp4、PDF） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "generate content using a cached system instruction and video file" | type: official
- [C14] 显式缓存无特殊 rate limit；cached tokens 计入 token 上限；"Cached content is a prefix to the prompt" | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "There are no special rate or usage limits on context caching; the standard rate limits for GenerateContent apply, and token limits include cached tokens." | type: official
- [C15] 显式 caching 最早 2024-06-18 上线（Gemini 1.5 时代）；2025-04-16 扩展到 Gemini 2.0 Flash | src: https://ai.google.dev/gemini-api/docs/changelog | quote: "June 18, 2024 API updates: Added support for context caching." | type: official

### 隐式 implicit
- [C16] 隐式缓存对 Gemini 2.5 及更新模型默认开启，零改动；Interactions API 的有状态（previous_interaction_id）与无状态会话都支持 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models. It is supported for both stateful (using previous_interaction_id) and stateless conversation modes." | type: official
- [C17] 命中条件=公共前缀：官方建议把大的公共内容放 prompt 开头、短时间内发相似前缀请求 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Try putting large and common contents at the beginning of your prompt. Try to send requests with similar prefix in a short amount of time" | type: official
- [C18] 每模型最小触发 token：3.8/3.7/3.6/3.5 Flash 与 3.1 Pro Preview = 4,096；2.5 Flash 与 2.5 Pro = 2,048 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The minimum input token count for context caching is listed in the following table for each model" | type: official
- [C19] 命中后自动让利，不保证命中/省钱 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "We automatically pass on cost savings if your request hits caches. There is nothing you need to do in order to enable this." | type: official
- [C20] 上线日期 2025-05-08（官方博客），当时折扣为 75%，门槛 1024（2.5 Flash）/2048（2.5 Pro） | src: https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/ | quote: "MAY 8, 2025 ... providing the same 75% token discount ... we reduced the minimum request size for 2.5 Flash to 1024 tokens and 2.5 Pro to 2048 tokens" | type: official
- [C21] 现行折扣 90%：优化页写 "90% discount + Prorated token storage"；定价表隐含命中价=标准输入价 10%（2.5 Flash $0.30→$0.03；2.5 Pro $1.25→$0.125） | src: https://ai.google.dev/gemini-api/docs/optimization | quote: "90% discount + Prorated token storage" | type: official
- [C22] 隐式命中确认字段：generateContent 为 usage_metadata.cached_content_token_count；Interactions API 为 `usage.total_cached_tokens` | src: https://ai.google.dev/gemini-api/docs/caching | quote: "You can see the number of tokens which were cache hits in the response object's usage.total_cached_tokens (Python and JavaScript) field." | type: official
- [C23] 隐式无显式缓存对象、无存储费（按 C21 折扣覆盖；定价页无 implicit storage 行）；官方对比：显式 "cost saving guarantee"，隐式 "no cost saving guarantee" | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Implicit caching (automatically enabled on Gemini 2.5 and newer models, no cost saving guarantee) Explicit caching (can be manually enabled on most models, cost saving guarantee)" | type: official
- [C24] Interactions API 只支持隐式，不支持显式 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Explicit caching (manually creating and managing cache objects) is not supported in the Interactions API." | type: official

## conflicts
- 折扣力度随时间变：2025-05-08 上线博客写 "75% token discount"（https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/），现行 pricing/optimization 页隐含 90%（https://ai.google.dev/gemini-api/docs/optimization "90% discount + Prorated token storage"）。提价时间点未在 changelog 找到。
- 最小门槛随时间变：上线时 1024（Flash）/2048（Pro），现行表 2048/2048（2.5 系）。是演进不是矛盾，但填格子时应写现行值。
- 最小 token 表放在 "Implicit caching" 小节下，但措辞是 "for context caching" 通用；显式节只写 "minimum ... varies by model"，未单列显式门槛。

## gaps
- 隐式缓存在 Gemini API（ai.google.dev）侧的 TTL/存活期：官方文档只写 "short amount of time"，无具体数值（Vertex 侧写 24h 内删除，见 leads）。
- 显式+隐式能否在同一请求叠加（如引用 CachedContent 的请求其非缓存后缀是否再被隐式缓存）：文档未提及。
- 隐式命中的具体失效清单（改 tools/system_instruction/temperature/model 版本是否必失效）：文档未逐条列举，仅有前缀一致性的正向建议。
- 显式缓存文档不再单列各模型最小门槛（旧 1.5 时代 32,768 未在现页确认）。

## leads
- Vertex AI 差异（范围外）：cloud.google.com blog 2025-10-15 称 Vertex 隐式缓存 "caches always deleted within 24 hours"、2.5+ 折扣 90%/2.0 75%；docs.cloud.google.com/gemini-enterprise-agent-platform context-cache-overview 同述。
- 官方论坛线索：用户报告隐式命中对请求间隔极敏感（~10s 即不命中），非官方。
- 缓存折扣从 75%→90% 的变更时间点：可翻 pricing 页历史快照（web.archive.org）或 changelog。
