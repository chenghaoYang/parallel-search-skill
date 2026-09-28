# r1-gemini
question: Gemini Developer API 的 implicit caching 与 explicit context caching 是不是两套机制？分别填 D1–D8。
checked: https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/api/caching, https://ai.google.dev/api/generate-content, https://ai.google.dev/gemini-api/docs/pricing, https://ai.google.dev/gemini-api/docs/tokens, https://ai.google.dev/gemini-api/docs/billing

## claims
- [C1] 两套并存，未写合并或弃用。隐式: D1 默认开且无成本保证。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Implicit caching (automatically enabled on Gemini 2.5 and newer models, no cost saving guarantee)" | type: official
- [C2] 显式: D1 可手动启用且 cost saving guarantee。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Explicit caching (can be manually enabled on most models, cost saving guarantee)" | type: official
- [C3] 显式: D1/D8 Beta，端点与 SDK 在 v1beta。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Explicit context caching is currently in Beta." | type: official
- [C4] 隐式: D1/D8 Interactions 只支持隐式，显式对象不支持。页 2026-09-02。 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "The Interactions API only supports implicit caching." | type: official
- [C5] 隐式: D1/D2 2.5 及更新默认开启，无需请求字段。页 2026-09-02。 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "There is nothing you need to do in order to enable this." | type: official
- [C6] 隐式: D3 最低 token，页 2026-09-02 表：3.8/3.7/3.6/3.5 Flash 与 3.1 Pro Preview 4,096；2.5 Flash 与 2.5 Pro 2,048。 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "The minimum input token count for context caching is listed in the following table for each model" | type: official
- [C9] 隐式: D6 命中才自动转节省。页 2026-09-02。 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "We automatically pass on cost savings if your request hits caches." | type: official
- [C10] 隐式: D7 Interactions 字段 usage.total_cached_tokens。页 2026-09-02。tokens 页 2026-09-23 同名字段。 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "usage.total_cached_tokens (Python and JavaScript) field." | type: official
- [C11] 隐式: D7 generateContent 只写 usage_metadata，未点名子字段。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "cache hits in the response object's usage_metadata field." | type: official
- [C12] 显式: D1/D2 先缓存再引用。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "pass some content to the model once, cache the input tokens, and then refer to the cached tokens" | type: official
- [C13] 显式: D2 POST https://generativelanguage.googleapis.com/v1beta/cachedContents。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "https://generativelanguage.googleapis.com/v1beta/cachedContents?key=$GEMINI_API_KEY" | type: official
- [C14] 显式: D2 方法 cachedContents.create。页 2026-09-11。 | src: https://ai.google.dev/api/caching | quote: "Method: cachedContents.create" | type: official
- [C15] 显式: D2 字段 cachedContent，格式 cachedContents/{cachedContent}。页 2026-09-23。 | src: https://ai.google.dev/api/generate-content | quote: "Format: cachedContents/{cachedContent}" | type: official
- [C17] 显式: D8 generateContent base：post https://generativelanguage.googleapis.com/v1beta/{model=models/*}:generateContent。页 2026-09-23。 | src: https://ai.google.dev/api/generate-content | quote: "post https://generativelanguage.googleapis.com/v1beta/{model=models/*}:generateContent" | type: official
- [C18] 显式: D2 资源名格式 cachedContents/{id}。页 2026-09-11。 | src: https://ai.google.dev/api/caching | quote: "Format: cachedContents/{id}" | type: official
- [C19] 显式: D2/D5 ttl 仅输入。页 2026-09-11。 | src: https://ai.google.dev/api/caching | quote: "Input only. New TTL for this resource, input only." | type: official
- [C20] 显式: D5 未设 TTL 默认 1 小时。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "If not set, the TTL defaults to 1 hour." | type: official
- [C21] 显式: D4 只能改 ttl 或 expire_time。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Changing anything else about the cache isn't supported." | type: official
- [C23] 显式: D4 只能用于创建时的模型。页 2026-09-11。 | src: https://ai.google.dev/api/caching | quote: "Cached content can be only used with model it was created for." | type: official
- [C24] 显式: D3/D4 tools 为 Input only 且 Immutable。页 2026-09-11。 | src: https://ai.google.dev/api/caching | quote: "Optional. Input only. Immutable. A list of Tools the model may use to generate the next response" | type: official
- [C25] 显式: D3 缓存内容是提示前缀。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Cached content is a prefix to the prompt." | type: official
- [C26] 显式: D3 最低 token 随模型变，该节无数字。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The minimum input token count for context caching varies by model." | type: official
- [C27] 显式: D6 缓存输入按降低费率。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "billed at a reduced rate when included in subsequent prompts." | type: official
- [C28] 显式: D6 存储按 TTL 时长 × 缓存 token。页 2026-09-11。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "billed based on the TTL duration of cached token count." | type: official
- [C29] 显式: D7 usageMetadata.cachedContentTokenCount。页 2026-09-23。 | src: https://ai.google.dev/api/generate-content | quote: "Number of tokens in the cached part of the prompt (the cached content)" | type: official
- [C31] 价目未标隐式或显式（2026-09-23）。2.5-pro Standard 付费缓存 $0.125（<=200k）、$0.25（>200k），存储 $4.50 / 1,000,000 tokens per hour。 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.125, prompts <= 200k tokens $0.25, prompts > 200k $4.50 / 1,000,000 tokens per hour (storage price)" | type: official
- [C32] 价目未区分机制（2026-09-23）。3.8-flash 付费缓存 $0.075 至 2026-12-31，其后 $0.15。 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.075 through December 31, 2026. $0.15 starting January 1, 2027." | type: official
- [C33] 账单 FAQ（2026-09-20）计价含 Cached token storage duration，未点名机制。 | src: https://ai.google.dev/gemini-api/docs/billing | quote: "Cached token storage duration" | type: official
- [C34] 隐式: D2 有状态用 previous_interaction_id，也支持无状态。页 2026-09-02。 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "stateful (using previous_interaction_id) and stateless conversation modes." | type: official
- [C35] 隐式: D3 大而稳定内容放提示开头。页 2026-09-02。 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Try putting large and common contents at the beginning of your prompt" | type: official

## conflicts
- 存储是否含隐式：billing 2026-09-20 列 "Cached token storage duration"（https://ai.google.dev/gemini-api/docs/billing），未写只对显式。显式指南 2026-09-11 写 "billed based on the TTL duration of cached token count"（https://ai.google.dev/gemini-api/docs/generate-content/caching）。隐式页无存储句。
- 免费层：pricing 2026-09-23 Paid 写 "Access to Context caching"；3.8-flash 免费 "Free of charge"，2.5-pro 免费 "Not available"（https://ai.google.dev/gemini-api/docs/pricing）。
- 隐式命中字段：Interactions 为 usage.total_cached_tokens（caching 2026-09-02）；generateContent 隐式节只写 usage_metadata（2026-09-11）。cachedContentTokenCount 未写是否含隐式（api/generate-content 2026-09-23）。

## gaps
- 隐式 D4：改模型、工具声明、字节是否 miss，无原句。
- 隐式 D5：TTL、能否延长、是否收存储，隐式专页未写。
- 隐式 D6：相对 input 的倍率未写。
- 显式 D3 最低 token 数字：explicit 节只说 varies by model；4096/2048 在隐式标题下。
- 隐式 D3 模态未写。显式 D5「TTL 无上下界」、expireTime 与 ttl 互斥原句未留。显式 D8 无完整模型表（most models；示例 gemini-3.8-flash）。
- 不能由价目断言隐式读价等于显式，或隐式也按 token-hour 收存储。2.5-flash 与 3.1-pro 单价未写入主张。

## leads
- Vertex 限额可能不同（cloud.google.com context cache）；未做矩阵。
- 2025-05-08 developers.googleblog.com 的 75% 与旧门槛，与现行价目不符。
