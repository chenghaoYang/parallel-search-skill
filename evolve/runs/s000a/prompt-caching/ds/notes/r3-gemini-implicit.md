# r3-gemini-implicit
question: Gemini API implicit caching 命中后按什么折扣计费？收不收存储费？定价页 "Context caching price" 行是只给 explicit 还是 implicit 命中也走这行？
checked: https://ai.google.dev/gemini-api/docs/caching ; https://ai.google.dev/gemini-api/docs/generate-content/caching ; https://ai.google.dev/gemini-api/docs/pricing ; https://ai.google.dev/gemini-api/docs/changelog ; https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/

## claims
- [C1] Implicit caching 默认开启（Gemini 2.5+），命中自动返利，官方文档未写百分比。 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models. ... We automatically pass on cost savings if your request hits caches." | type: official
- [C2] 现行 generateContent 版缓存页仍标注 implicit "no cost saving guarantee"，explicit "cost saving guarantee"。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Implicit caching (automatically enabled on Gemini 2.5 and newer models, no cost saving guarantee)" | type: official
- [C3] Google 官方博客（2025-05-08，针对 Gemini 2.5 模型）写明 implicit 命中给 75% token 折扣，与 explicit 相同。 | src: https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/ | quote: "We will dynamically pass cost savings back to you, providing the same 75% token discount." | type: official
- [C4] Implicit 命中 token 数经 usage 字段返回，并按 "the lower price"（博客链接指向定价页 Context caching 价）计费——即 implicit 命中走定价表同一行。 | src: https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/ | quote: "you will start to see `cached_content_token_count` in the usage metadata which indicates how many tokens in the request were cached and therefore will be charged at the lower price" | type: official
- [C5] 定价页每个模型的 "Context caching price" 行同时含命中单价与按小时存储价（例 Gemini 3.8 Flash Standard：$0.075/1M + $0.50/1M tokens/hour），行内未区分 implicit/explicit。 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Context caching price ... $0.075 through December 31, 2026.   $0.15 starting January 1, 2027.   $0.50 / 1,000,000 tokens per hour (storage price) through December 31, 2026.   $1.00 / 1,000,000 tokens per hour (storage price) starting January 1, 2027." | type: official
- [C6] 存储费只在 explicit 计费说明（"How explicit caching reduces costs"）下出现：按 TTL 时长计费；implicit 一节无存储费表述。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Storage duration: The amount of time cached tokens are stored (TTL), billed based on the TTL duration of cached token count. There are no minimum or maximum bounds on the TTL." | type: official
- [C7] Explicit 缓存 token "billed at a reduced rate when included in subsequent prompts"，成本取决于 token 数与 TTL。 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The number of input tokens cached, billed at a reduced rate when included in subsequent prompts." | type: official

## conflicts
- 75% vs ~90%：Google 官方博客（2025-05-08，2.5 模型）写 implicit 命中 "the same 75% token discount"；现行定价表算术比例更高——如 3.8 Flash $0.075 vs input $0.75、3.1 Pro Preview $0.20 vs $2.00，即约 90% off。现行文档本身不写百分比，未裁决哪个数字对当前模型适用。

## gaps
- 现行官方文档（https://ai.google.dev/gemini-api/docs/caching 与 https://ai.google.dev/gemini-api/docs/generate-content/caching）对 implicit 命中不写任何折扣百分比；定价页（https://ai.google.dev/gemini-api/docs/pricing，全文检索无 "implicit"/"explicit"/"discount" 字样）与 changelog（https://ai.google.dev/gemini-api/docs/changelog，无 implicit caching 条目）也未写。唯一百分比来源是 2025-05-08 官方博客的 75%（针对 2.5 模型）。
- 定价页 "Context caching price" 行未标注是否覆盖 implicit 命中；"implicit 命中按该行计费" 仅由官方博客 "charged at the lower price"（链接指向定价页）间接支持。
- implicit 命中是否收 hourly storage price 无文档说明：存储价写在 "Context caching price" 行内，但计费文档只在 explicit（有 TTL 的 CachedContent）语境描述 storage 计费；implicit 无 TTL/缓存对象，推测不收但未获官方文字确认。

## leads
- Vertex AI 的 context caching 价目（cloud.google.com/vertex-ai/generative-ai/pricing）未查，如需要可另起一轮。
- usage 字段名：Interactions API 为 `usage.total_cached_tokens`；generateContent 为 `usage_metadata` / `cached_content_token_count`。
