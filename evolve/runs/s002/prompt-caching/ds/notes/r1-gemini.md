# r1-gemini
question: Gemini API 的 implicit caching 与 explicit context caching 是两套机制还是一套？各自如何触发、门槛、TTL、计费、命中字段、失效条件（grid 行「Gemini 隐式」「Gemini 显式」D1–D9）
checked: https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/api/caching, https://ai.google.dev/api/generate-content, https://ai.google.dev/gemini-api/docs/pricing

## claims
- [C1] 【隐式】【显式】官方确认是两套机制：implicit（2.5+ 自动开、不保证省钱）与 explicit（多数模型手动开、保证省钱） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The Gemini API offers two different caching mechanisms:" | type: official
- [C2] 【隐式】D1 全自动：默认开启、无需改请求、命中自动让利 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models. We automatically pass on cost savings if your request hits caches. There is nothing you need to do in order to enable this." | type: official
- [C3] 【隐式】D1 在 Interactions API 中 stateful/stateless 均支持 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "It is supported for both stateful (using `previous_interaction_id`) and stateless conversation modes." | type: official
- [C4] 【显式】D1 创建端点：REST `POST https://generativelanguage.googleapis.com/v1beta/cachedContents`（SDK `client.caches.create`），Beta | src: https://ai.google.dev/api/caching | quote: "post `https://generativelanguage.googleapis.com/v1beta/cachedContents`" | type: official
- [C5] 【显式】D1 请求内引用字段：`cachedContent`（Python `cached_content`），值形如 `cachedContents/{id}` | src: https://ai.google.dev/api/generate-content | quote: "Optional. The name of the content cached to use as context to serve the prediction. Format: `cachedContents/{cachedContent}`" | type: official
- [C6] 【隐式】D3 最小输入 token 按模型分档：Gemini 3.8/3.7/3.6/3.5 Flash 与 3.1 Pro Preview=4,096；Gemini 2.5 Flash 与 2.5 Pro=2,048 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The minimum input token count for context caching is listed in the following table for each model" | type: official
- [C7] 【显式】D3 最小 token 按模型而异（当前页未给逐模型数值表），上限=模型上限 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The *minimum* input token count for context caching varies by model. The *maximum* is the same as the maximum for the given model." | type: official
- [C8] 【显式】D4 TTL 不设默认 1 小时；TTL 无最小/最大界限；可设 `ttl`（Duration 如 "300s"）或 `expireTime` | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "If not set, the TTL defaults to 1 hour." | type: official
- [C9] 【显式】D4 TTL 上下限 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "There are no minimum or maximum bounds on the TTL." | type: official
- [C10] 【显式】D4 `ttl` 字段格式 | src: https://ai.google.dev/api/caching | quote: "A duration in seconds with up to nine fractional digits, ending with '`s`'. Example: `\"3.5s\"`." | type: official
- [C11] 【隐式】D5 命中自动按折扣让利，页面未给隐式单价数字 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "We automatically pass on cost savings if your request hits caches." | type: official
- [C12] 【显式】D5 计费=缓存 token 减价读取 + 按 TTL 计存储费 + 非缓存输入/输出照常 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "**Cache token count:** The number of input tokens cached, billed at a reduced rate when included in subsequent prompts." | type: official
- [C13] 【显式】D5 存储按时长计 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "**Storage duration:** The amount of time cached tokens are stored (TTL), billed based on the TTL duration of cached token count." | type: official
- [C14] 【显式】D5 单价例：Gemini 2.5 Flash Standard 读取 $0.03/1M（文/图/视频）、$0.1/1M（音频），存储 $1.00/1,000,000 tokens/小时；2.5 Pro $0.125/1M（≤200k）+存储 $4.50/1M tok/小时 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.03 (text / image / video)   $0.1 (audio)   $1.00 / 1,000,000 tokens per hour (storage price)" | type: official
- [C15] 【隐式】【显式】D6 命中字段：`usageMetadata.cachedContentTokenCount`；`promptTokenCount` 含缓存部分；`cacheTokensDetails[]` 按模态细分 | src: https://ai.google.dev/api/generate-content | quote: "Number of tokens in the cached part of the prompt (the cached content)" | type: official
- [C16] 【隐式】D6 Interactions API 中字段名为 `usage.total_cached_tokens`（Python/JS） | src: https://ai.google.dev/gemini-api/docs/caching | quote: "You can see the number of tokens which were cache hits in the response object's `usage.total_cached_tokens` (Python and JavaScript) field." | type: official
- [C17] 【显式】D6 缓存在 create/get/list 与 GenerateContent 的 `usage_metadata` 均回传 token 数 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The number of cached tokens is returned in the `usage_metadata` from the create, get, and list operations of the cache service, and also in `GenerateContent` when using the cache." | type: official
- [C18] 【显式】D7 只可更新过期时间（PATCH `v1beta/{cachedContent.name=cachedContents/*}`）；DELETE `v1beta/{name=cachedContents/*}` 手动删除 | src: https://ai.google.dev/api/caching | quote: "Updates CachedContent resource (only expiration is updatable)." | type: official
- [C19] 【显式】D7 除 ttl/expire_time 外不可改 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "You can set a new `ttl` or `expire_time` for a cache. Changing anything else about the cache isn't supported." | type: official
- [C20] 【隐式】D7 命中率靠前缀匹配+时间邻近：公共大内容放开头、相似前缀的请求短时间内发送 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Try putting large and common contents at the beginning of your prompt" | type: official
- [C21] 【显式】D8 可缓存 `contents[]`、`tools[]`、`toolConfig`、`systemInstruction`（文本） | src: https://ai.google.dev/api/caching | quote: "Optional. Input only. Immutable. Developer set system instruction. Currently text only." | type: official
- [C22] 【显式】D8 tools 可入缓存 | src: https://ai.google.dev/api/caching | quote: "Optional. Input only. Immutable. A list of `Tools` the model may use to generate the next response" | type: official
- [C23] 【显式】D8 视频/PDF 经 Files API 上传后放入 `contents` 缓存（官方示例含 mp4 与 PDF） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Repetitive analysis of lengthy video files" | type: official
- [C24] 【隐式】D9 支持面=全部 Gemini 2.5 及更新模型；命中不保证（"no cost saving guarantee"） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Implicit caching (automatically enabled on Gemini 2.5 and newer models, no cost saving guarantee)" | type: official
- [C25] 【显式】D9 多数模型可手动开；TTL 内命中是契约式的（"cost saving guarantee"）；缓存绑定创建时的模型 | src: https://ai.google.dev/api/caching | quote: "Cached content can be only used with model it was created for." | type: official
- [C26] 【显式】D9 Beta 状态 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Explicit context caching is currently in Beta. Endpoints and SDK methods are available under `v1beta`." | type: official
- [C27] 【隐式】【显式】Interactions API 只支持隐式缓存 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "The **Interactions API** only supports implicit caching. Explicit caching (manually creating and managing cache objects) is not supported in the Interactions API." | type: official
- [C28] 【显式】缓存是前缀：`cachedContent` 作为 prompt 前缀，模型不区分缓存与普通输入 token | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "The model doesn't make any distinction between cached tokens and regular input tokens. Cached content is a prefix to the prompt." | type: official

## conflicts
- 隐式命中字段名两处写法不同：Interactions 缓存页写 `usage.total_cached_tokens`（https://ai.google.dev/gemini-api/docs/caching），generateContent 缓存页写 "response object's `usage_metadata` field"（https://ai.google.dev/gemini-api/docs/generate-content/caching），API ref 字段全名 `usageMetadata.cachedContentTokenCount`（https://ai.google.dev/api/generate-content）。属不同 API 表面，不算矛盾但需在 grid 注明。

## gaps
- 【隐式】D4：两页 Implicit caching 章节全文均未提 TTL/有效期（页尾 Last updated 2026-09-02 / 2026-09-11，已读全文），无法引用原句证实「隐式无 TTL」。
- 【隐式】D7：文档只给「相似前缀+短时间内」命中率建议，未定义哪些前缀变化会失效。
- 【隐式】D5：pricing 页只有一行 "Context caching price"（读价+存储价并列），未说明隐式命中是否免存储费/具体折扣率。
- 【显式】D3：当前文档未给逐模型最小 token 表（旧版文档曾有），仅 "varies by model"。
- Vertex AI（cloud.google.com）规则未查，可能有独立 TTL/计费。

## leads
- Vertex AI 有独立 context caching 文档（cloud.google.com/vertex-ai/generative-ai/docs/context-cache/*），规则与 Developer API 可能不同。
- OpenAI 兼容层可用 `extra_body` 的 `cached_content` 开显式缓存（/gemini-api/docs/openai#extra-body）。
- 显式缓存无法读回内容，只能 get/list 元数据（name, model, display_name, usage_metadata, create_time, update_time, expire_time）。
