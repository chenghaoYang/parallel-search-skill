# r1-gemini
question: Gemini API 的 explicit context caching 与 implicit caching 现在各怎么工作（是否两套并存、怎么开、计费、TTL、命中字段、失效）
checked: https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/api/caching, https://ai.google.dev/pricing, https://ai.google.dev/gemini-api/docs/changelog, https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/, https://raw.githubusercontent.com/googleapis/googleapis/master/google/ai/generativelanguage/v1beta/generative_service.proto

## claims
- [C1] 隐式：对 Gemini 2.5+ 模型默认开启、零代码改动；Interactions API 的 stateful（previous_interaction_id）与 stateless 均支持 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models. It is supported for both stateful (using `previous_interaction_id`) and stateless conversation modes." | type: official
- [C2] 隐式：无节省保证；命中=共享公共前缀；技巧=公共大内容放开头+短时间窗发相似前缀请求 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Implicit caching (automatically enabled on Gemini 2.5 and newer models, no cost saving guarantee)" | type: official
- [C3] 隐式：最小输入 token 门槛——Gemini 3.8/3.7/3.6/3.5 Flash 与 3.1 Pro Preview=4,096；2.5 Flash/Pro=2,048（页更新于 2026-09-02） | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Gemini 3.8 Flash 4,096 ... Gemini 2.5 Flash 2,048 Gemini 2.5 Pro 2,048" | type: official
- [C4] 隐式：Interactions API 命中数看响应 `usage.total_cached_tokens`（Python/JS） | src: https://ai.google.dev/gemini-api/docs/caching | quote: "You can see the number of tokens which were cache hits in the response object's `usage.total_cached_tokens` (Python and JavaScript) field." | type: official
- [C5] 隐式：generateContent 命中数在响应 `usage_metadata`；字段 `cached_content_token_count`（JSON `cachedContentTokenCount`）="prompt 中被缓存部分的 token 数"（googleapis v1beta proto） | src: https://raw.githubusercontent.com/googleapis/googleapis/master/google/ai/generativelanguage/v1beta/generative_service.proto | quote: "// Number of tokens in the cached part of the prompt (the cached content) int32 cached_content_token_count = 4;" | type: official
- [C6] 隐式：命中自动按缓存价计费，发布口径 "75% token discount" | src: https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/ | quote: "We will dynamically pass cost savings back to you, providing the same 75% token discount." | type: official
- [C7] 隐式：2025-05-08 起对 Gemini 2.5 模型推出 | src: https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/ | quote: "MAY 8, 2025 ... Today, we are rolling out the highly requested feature in the Gemini API: implicit caching." | type: official
- [C8] 显式：Interactions API 不支持，须用 generateContent API | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Explicit caching (manually creating and managing cache objects) is not supported in the Interactions API." | type: official
- [C9] 显式：先建缓存资源 `cachedContents`——REST `POST /v1beta/cachedContents`（SDK `client.caches.create`），资源名 `cachedContents/{id}`，必填 model=`models/{model}` | src: https://ai.google.dev/api/caching | quote: "post `https://generativelanguage.googleapis.com/v1beta/cachedContents`" | type: official
- [C10] 显式：后续请求在 generateContent 用 `cachedContent`/`cached_content` 字段引用缓存名 | src: https://raw.githubusercontent.com/googleapis/googleapis/master/google/ai/generativelanguage/v1beta/generative_service.proto | quote: "// The name of the content cached to use as context to serve the prediction. Format: `cachedContents/{cachedContent}` optional string cached_content = 9" | type: official
- [C11] 显式：TTL 默认 1 小时；可设 ttl 或 expireTime；无上下限 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "If not set, the TTL defaults to 1 hour... There are no minimum or maximum bounds on the TTL." | type: official
- [C12] 显式：失效——到期 token 自动删除；PATCH 只能改 ttl/expireTime；DELETE 手动删除 | src: https://ai.google.dev/api/caching | quote: "Updates CachedContent resource (only expiration is updatable)... delete `https://generativelanguage.googleapis.com/v1beta/{name=cachedContents/*}`" | type: official
- [C13] 显式：计费=缓存 token 按减价率计入后续请求 + 存储按 TTL 时长（token·小时）+ 非缓存输入/输出正常计 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "billed at a reduced rate when included in subsequent prompts. Storage duration ... billed based on the TTL duration of cached token count." | type: official
- [C14] 显式：现价例——2.5 Flash 缓存读 $0.03/1M+存储 $1.00/1M tokens/时；2.5 Pro $0.125(≤200k)+$4.50；3.8 Flash $0.075+$0.50（至 2026-12-31） | src: https://ai.google.dev/pricing | quote: "$0.03 (text / image / video)   $0.1 (audio)   $1.00 / 1,000,000 tokens per hour (storage price)" | type: official
- [C15] 显式：最小 token 随模型而变、最大=模型上下文上限（阈值表在 implicit 节下，见 gaps） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The minimum input token count for context caching varies by model. The maximum is the same as the maximum for the given model." | type: official
- [C16] 显式：命中/缓存 token 数在 cache create/get/list 的 `usage_metadata`（`totalTokenCount`）及 generateContent 响应中返回 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The number of cached tokens is returned in the `usage_metadata` from the create, get, and list operations ... and also in `GenerateContent`" | type: official
- [C17] 显式：隔离/边界——只能用于创建它的模型；内容不可读回，仅元数据可取 | src: https://ai.google.dev/api/caching | quote: "Cached content can be only used with model it was created for." | type: official
- [C18] 显式：缓存内容=prompt 前缀，模型不区分缓存与普通 token；无特殊速率限制，缓存 token 计入限额 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The model doesn't make any distinction between cached tokens and regular input tokens. Cached content is a prefix to the prompt." | type: official
- [C19] 显式：仍为 Beta（v1beta），所在文档标 Legacy；OpenAI 兼容库经 `extra_body.cached_content` 用 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Explicit context caching is currently in Beta. Endpoints and SDK methods are available under `v1beta`." | type: official
- [C20] 显式：沿革——2024-06-18 "Added support for context caching"；2025-04-16 "Launched context caching for Gemini 2.0 Flash" | src: https://ai.google.dev/gemini-api/docs/changelog | quote: "April 16, 2025 Launched context caching for Gemini 2.0 Flash." | type: official
- [C21] 两套并存于 generateContent API：implicit 自动无保证 / explicit 手动有保证 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Implicit caching (automatically enabled on Gemini 2.5 and newer models, no cost saving guarantee) Explicit caching (can be manually enabled on most models, cost saving guarantee)" | type: official
- [C22] 覆盖：定价页把 "Access to Context caching" 列为 Paid 权益；免费层 caching 栏因模型而异（3.8 Flash "Free of charge"，2.5 Pro/Flash "Not available"） | src: https://ai.google.dev/pricing | quote: "check_circleAccess to Context caching" | type: official

## conflicts
- 隐式最小 token：官方博客（2025-05-08）"we reduced the minimum request size for 2.5 Flash to 1024 tokens and 2.5 Pro to 2048 tokens"（https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/）vs 当前文档表（2026-09-02 更新）"Gemini 2.5 Flash 2,048"（https://ai.google.dev/gemini-api/docs/caching）——门槛后被上调。
- 折扣口径：博客 "the same 75% token discount" vs 现价表隐含缓存读价≈输入价 1/10（2.5 Flash $0.03 vs $0.30；3.8 Flash $0.075 vs $0.75，https://ai.google.dev/pricing），约 90% off。
- 显式支持模型：博客（2025-05）"supports our Gemini 2.5 and 2.0 models" vs 现文档 "manually enabled on most models"——范围已扩大但无逐模型清单。

## gaps
- 隐式 TTL/失效：两页均无隐式缓存存活期、失效或手动清除语义，已通读全文确认。
- 隐式是否收存储费、免费层是否生效：定价页未区分隐式/显式的 storage 与免费层口径。
- 显式跨 API key/项目隔离：文档只说绑定模型且不可读回。
- 显式各模型最小 token 具体数值：阈值表位于 implicit 节标题下。

## leads
- Vertex AI 版 context caching（语义、折扣、TTL 与 Developer API 不同，勿混入主张）：https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview
- Interactions API 概览（previous_interaction_id 细节）：https://ai.google.dev/gemini-api/docs/interactions-overview
