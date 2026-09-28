# r1-gemini
question: Gemini API（ai.google.dev）implicit caching 与 explicit context caching（CachedContent）各自如何触发、边界、门槛、TTL、计费、观测命中、失效条件、可用模型
checked: https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/api/caching, https://ai.google.dev/api/generate-content, https://ai.google.dev/gemini-api/docs/pricing

## claims
- [C1] [implicit] Gemini API 确为两套机制：implicit 自动、不保证省钱；explicit 手动、保证省钱 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Implicit caching (automatically enabled on Gemini 2.5 and newer models, no cost saving guarantee)" | type: official
- [C2] [implicit] explicit 是手动启用、支持大多数模型、有成本节省保证 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Explicit caching (can be manually enabled on most models, cost saving guarantee)" | type: official
- [C3] [implicit][D1] 触发方式：默认开启，请求无需任何改动 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models. We automatically pass on cost savings if your request hits caches. There is nothing you need to do in order to enable this." | type: official
- [C4] [implicit][D8] 可用模型及最低输入 token 门槛：Gemini 2.5 Flash/Pro=2,048；Gemini 3.5/3.6/3.7/3.8 Flash 与 3.1 Pro Preview=4,096 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The minimum input token count for context caching is listed in the following table for each model" | type: official
- [C5] [implicit] 命中条件（提高命中率）：公共/静态内容放 prompt 开头；短时间发送前缀相似的请求 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Try putting large and common contents at the beginning of your prompt" | type: official
- [C6] [implicit] 命中条件补充：前缀需相近且时间接近 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Try to send requests with similar prefix in a short amount of time" | type: official
- [C7] [implicit][D6] 观测命中：generateContent API 响应对象 usage_metadata 字段（SDK 命名） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "You can see the number of tokens which were cache hits in the response object's `usage_metadata` field." | type: official
- [C8] [implicit][D6] Interactions API 侧观测字段名为 usage.total_cached_tokens（Python 和 JavaScript） | src: https://ai.google.dev/gemini-api/docs/caching | quote: "You can see the number of tokens which were cache hits in the response object's `usage.total_cached_tokens` (Python and JavaScript) field." | type: official
- [C9] [implicit] Interactions API 只支持 implicit，不支持 explicit | src: https://ai.google.dev/gemini-api/docs/caching | quote: "The Interactions API only supports implicit caching." | type: official
- [C10] [explicit][D1] 创建端点：POST https://generativelanguage.googleapis.com/v1beta/cachedContents，创建 CachedContent 资源 | src: https://ai.google.dev/api/caching | quote: "Creates CachedContent resource." | type: official
- [C11] [explicit][D1] 请求中引用字段名：GenerateContentRequest.cachedContent，格式 cachedContents/{cachedContent} | src: https://ai.google.dev/api/generate-content | quote: "Optional. The name of the content cached to use as context to serve the prediction. Format: `cachedContents/{cachedContent}`" | type: official
- [C12] [explicit] 状态为 Beta，端点与 SDK 方法在 v1beta 下 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Explicit context caching is currently in Beta. Endpoints and SDK methods are available under `v1beta`." | type: official
- [C13] [explicit][D4] 默认 TTL=1 小时；TTL 是缓存自动删除前的存续时长 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "This caching duration is called the time to live (TTL). If not set, the TTL defaults to 1 hour." | type: official
- [C14] [explicit][D4] 过期字段为互斥 union：ttl（Duration 字符串如 "300s"）或 expireTime（RFC 3339）；expireTime 输出总会返回 | src: https://ai.google.dev/api/caching | quote: "This is *always* provided on output, regardless of what was sent on input." | type: official
- [C15] [explicit][D4] 可刷新：PATCH https://generativelanguage.googleapis.com/v1beta/{cachedContent.name=cachedContents/*}，仅 expiration 可更新 | src: https://ai.google.dev/api/caching | quote: "Updates CachedContent resource (only expiration is updatable)." | type: official
- [C16] [explicit] 指南确认只能改 ttl 或 expire_time，其他不可改 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "You can set a new `ttl` or `expire_time` for a cache. Changing anything else about the cache isn't supported." | type: official
- [C17] [explicit][D4] TTL 无最小/最大界限 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "There are no minimum or maximum bounds on the TTL." | type: official
- [C18] [explicit][D8] 失效/边界：缓存只能用于创建它的模型；model 字段必填、不可变、格式 models/{model} | src: https://ai.google.dev/api/caching | quote: "Cached content can be only used with model it was created for." | type: official
- [C19] [explicit][D8] 手动删除端点：DELETE https://generativelanguage.googleapis.com/v1beta/{name=cachedContents/*}；另有 get/list（list 的 pageSize 上限 1000） | src: https://ai.google.dev/api/caching | quote: "Deletes CachedContent resource." | type: official
- [C20] [explicit][D2] 门槛：最低输入 token 数因模型而异（页面未给 explicit 具体数字）；上限=该模型本身上限 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The *minimum* input token count for context caching varies by model. The *maximum* is the same as the maximum for the given model." | type: official
- [C21] [explicit][D5] 计费结构一：缓存 token 在后续请求中按折扣价计 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The number of input tokens cached, billed at a reduced rate when included in subsequent prompts." | type: official
- [C22] [explicit][D5] 计费结构二：存储按缓存 token 数 × TTL 时长计费 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Storage duration: The amount of time cached tokens are stored (TTL), billed based on the TTL duration of cached token count." | type: official
- [C23] [explicit][D5] 具体价格（Paid tier, per 1M tokens USD）：Gemini 2.5 Flash 缓存输入 $0.03(text/image/video)、$0.1(audio)，存储 $1.00/1M tokens/小时 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.03 (text / image / video)   $0.1 (audio)   $1.00 / 1,000,000 tokens per hour (storage price)" | type: official
- [C24] [explicit][D5] 具体价格：Gemini 2.5 Pro 缓存输入 $0.125(≤200k)/$0.25(>200k)，存储 $4.50/1M tokens/小时 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.125, prompts <= 200k tokens   $0.25, prompts > 200k   $4.50 / 1,000,000 tokens per hour (storage price)" | type: official
- [C25] [explicit][D5] 具体价格：Gemini 3.x Flash 缓存输入 $0.075（至 2026-12-31，之后 $0.15），存储 $0.50/1M tokens/小时（之后 $1.00） | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.075 through December 31, 2026.   $0.15 starting January 1, 2027.   $0.50 / 1,000,000 tokens per hour (storage price)" | type: official
- [C26] [explicit][D6] 观测：create/get/list 与 GenerateContent 的 usage_metadata 均返回缓存 token 数 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The number of cached tokens is returned in the `usage_metadata` from the create, get, and list operations of the cache service, and also in `GenerateContent` when using the cache." | type: official
- [C27] [explicit][D6] REST 响应字段：usageMetadata.cachedContentTokenCount=命中部分 token 数；另有 cacheTokensDetails 按模态拆分 | src: https://ai.google.dev/api/generate-content | quote: "Number of tokens in the cached part of the prompt (the cached content)" | type: official
- [C28] [explicit] CachedContent 资源的 usageMetadata 只有 totalTokenCount（缓存总 token 数） | src: https://ai.google.dev/api/caching | quote: "Total number of tokens that the cached content consumes." | type: official
- [C29] [explicit][D7] 无特殊限额：标准 GenerateContent rate limits 适用，token 上限含缓存 token | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "There are no special rate or usage limits on context caching; the standard rate limits for `GenerateContent` apply, and token limits include cached tokens." | type: official
- [C30] [explicit] 语义边界：cached content 是 prompt 前缀，模型不区分缓存与普通输入 token | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The model doesn't make any distinction between cached tokens and regular input tokens. Cached content is a prefix to the prompt." | type: official
- [C31] [explicit] 不能读回缓存内容，只能读元数据（name/model/display_name/usage_metadata/create_time/update_time/expire_time） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "It's not possible to retrieve or view cached content, but you can retrieve cache metadata" | type: official
- [C32] [explicit] 需付费层：Paid 层特性含 "Access to Context caching"；2.5 Flash/Pro 的 Free tier 该行标 "Not available" | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Access to Context caching" | type: official
- [C33] [explicit] OpenAI 兼容库中经 extra_body 的 cached_content 属性启用 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "you can enable explicit caching using the `cached_content` property on `extra_body`" | type: official
- [C34] 页面日期：gemini-api/docs/generate-content/caching Last updated 2026-09-11 UTC | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Last updated 2026-09-11 UTC." | type: official
- [C35] 页面日期：api/caching Last updated 2026-09-11 UTC | src: https://ai.google.dev/api/caching | quote: "Last updated 2026-09-11 UTC." | type: official
- [C36] 页面日期：gemini-api/docs/pricing 与 api/generate-content Last updated 2026-09-23 UTC | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Last updated 2026-09-23 UTC." | type: official
- [C37] 页面日期：gemini-api/docs/caching（Interactions 版）Last updated 2026-09-02 UTC | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Last updated 2026-09-02 UTC." | type: official

## conflicts
- 无（两页观测字段名不同是 API 面不同所致：generateContent 用 usage_metadata，Interactions 用 usage.total_cached_tokens，非矛盾）

## gaps
- [implicit][D4] TTL/存活期/逐出策略：官方文档未写。已查 https://ai.google.dev/gemini-api/docs/caching、https://ai.google.dev/gemini-api/docs/generate-content/caching、https://ai.google.dev/gemini-api/docs/pricing，均无 implicit 缓存时长或失效条件，仅有"短时间发送相似前缀"的建议。
- [implicit][D5] 命中折扣百分比与是否免存储费：文档只写"automatically pass on cost savings"；定价页每个模型只有一行 "Context caching price"，未区分 implicit 与 explicit 是否同价，也未写 implicit 是否收存储费。
- [explicit][D2] 每个模型的最低 token 具体数字未列出（数字表在 implicit 小节内，explicit 小节只写 varies by model）。
- [explicit] 支持 explicit 的完整模型清单未列出，仅写 "most models"（示例用了 gemini-3.8-flash、gemini-1.5-flash-001）。

## leads
- Vertex AI 的 context caching 是另一套文档与计费（同样显式 cachedContents，但存储/命中价目与 Gemini API 不同），仅线索：https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview
- Google 官方博客 implicit caching 发布文（2025-05）曾给出 75% 折扣表述，可作背景：https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/
