# r1-gemini
question: Google Gemini API 的 context caching，分「显式 explicit caching」（CachedContent / cachedContents）和「implicit caching」两种机制，在以下 10 个维度上分别是什么？
checked: https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/pricing, https://ai.google.dev/gemini-api/docs/pricing.md.txt, https://ai.google.dev/api/caching, https://ai.google.dev/gemini-api/docs/tokens, https://ai.google.dev/gemini-api/docs/interactions/caching, https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview, https://ai.google.dev/gemini-api/docs/optimization

## claims
- [C1] Explicit caching 触发方式：开发者必须调用 `cachedContents.create()` API（各 SDK 中为 `client.caches.create()`），传入 content、model、可选的 systemInstruction、toolConfig、expiration 等参数 | src: https://ai.google.dev/api/caching | quote: "cachedContents.create - Establishes a new cached content resource" | type: official
- [C2] Implicit caching 触发方式：自动启用于 Gemini 2.5 及更新型号，无需代码改动；文档表述"Implicit caching is enabled by default for all Gemini 2.5 and newer models" | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models. We automatically pass on cost savings if your request hits caches. There is nothing you need to do in order to enable this." | type: official
- [C3] Explicit caching 最小 token 阈值：因模型而异，Gemini 3.8/3.7/3.6/3.5 Flash 需 4096 token；Gemini 3 Flash Preview、2.5 Flash 需 1024 token；Gemini 3 Pro Preview、2.5 Pro 需 4096 token | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Gemini 3.8/3.7/3.6/3.5 Flash: 4,096 tokens; Gemini 2.5 Flash: 1,024 tokens; Gemini 3 Pro Preview: 4,096 tokens" | type: official
- [C4] Implicit caching 最小 token 阈值：Gemini 2.5 Flash/Pro 需 2048 token；Gemini 3.x Flash 需 4096 token | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Gemini 2.5 Flash/Pro: 2,048 tokens; Gemini 3.x Flash: 4,096 tokens" | type: official
- [C5] Explicit caching 粒度：可缓存 system instructions、file uploads（Files API）、text content、tool configurations/function definitions；缓存颗粒度为 token 级，但必须缓存整个 content 对象，不支持部分缓存 | src: https://ai.google.dev/api/caching | quote: "Contents: Media files or conversation history to cache; systemInstruction: Developer-defined behavioral guidelines; toolConfig: Function calling and retrieval settings" | type: official
- [C6] Implicit caching 粒度：与 explicit 相同，自动缓存 prompt 前缀中的所有 token，无需手动指定粒度 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "large and common contents at the beginning of your prompt" | type: official
- [C7] Explicit caching 命中读取计费：缓存命中后，输入 token 单价为标准价的 10%（90% 折扣）；例 Gemini 3.8 Flash 标准输入 $0.75/百万 token，缓存读取 $0.075/百万 token | src: https://ai.google.dev/gemini-api/docs/pricing.md.txt | quote: "Gemini 3.8 Flash... Input: $0.75/1M tokens... Context caching: $0.075/1M tokens" | type: official
- [C8] Implicit caching 命中读取计费：自动优惠传递，"we automatically pass on cost savings"，但具体折扣率在 Gemini API 文档未明确数值（Vertex AI 文档表述为 90% 折扣同等价格） | src: https://ai.google.dev/gemini-api/docs/caching | quote: "We automatically pass on cost savings if your request hits caches" | type: official
- [C9] Explicit caching 存储计费：按小时按 token 计费，$0.50/百万 token/小时（通过 2026/12/31），2027/1/1 起 $1.00/百万 token/小时；write-in cost 为标准输入 token 价格 | src: https://ai.google.dev/gemini-api/docs/pricing.md.txt | quote: "Context caching: $0.50/1M tokens/hour" | type: official
- [C10] Implicit caching 存储费用：无额外费用；Vertex AI 文档表述"There are no storage costs for implicit caching"但 Gemini API 文档未明确说明是否完全无费 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models" | type: official
- [C11] Explicit caching TTL 默认值：1 小时（"If not set, the TTL defaults to 1 hour"） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "If not set, the TTL defaults to 1 hour" | type: official
- [C12] Explicit caching TTL 自定义：支持，通过 `ttl` 参数（如 "300s"）或 `expireTime`（RFC 3339 格式）指定过期时间；也支持通过 `cachedContents.patch()` 更新过期设置 | src: https://ai.google.dev/api/caching | quote: "Expiration: Either ttl (e.g., '300s') or expireTime (RFC 3339 format); cachedContents.patch - Updates expiration settings only" | type: official
- [C13] Implicit caching TTL：Vertex AI 文档表述"Implicit caches are cleared in 24 hours or less"；Gemini API 官方文档无明确 TTL 数值 | src: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview | quote: "Implicit caches are cleared in 24 hours or less" | type: secondary
- [C14] 响应字段用于确认缓存命中：`usage.total_cached_tokens`（Python/JavaScript SDK）或 usageMetadata 中的 `total_cached_tokens` 字段显示缓存 token 数 | src: https://ai.google.dev/gemini-api/docs/tokens | quote: "total_cached_tokens" in usage field | type: official
- [C15] Explicit caching 失效条件：TTL 过期、通过 `cachedContents.delete()` 手动删除 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "You can manually delete caches using client.caches.delete() or update expiry times via client.caches.update()" | type: official
- [C16] Implicit caching 失效条件：基于 TTL 自动过期（具体时间见 C13）；文档未提及是否支持手动删除 | src: https://ai.google.dev/gemini-api/docs/caching | quote: N/A | type: official
- [C17] Explicit caching 模型支持范围："most models"（具体列表未完全列举），已验证支持 Gemini 3.8/3.7/3.6/3.5 Flash、Gemini 3/2.5 Pro/Flash Preview | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "can be manually enabled on most models" | type: official
- [C18] Implicit caching 模型支持范围：所有 Gemini 2.5 及更新版本型号（Gemini 2.5 Flash/Pro、Gemini 3.x 系列等），但 Interactions API 只支持 implicit caching，不支持 explicit caching | src: https://ai.google.dev/gemini-api/docs/interactions/caching | quote: "The Interactions API only supports implicit caching. Explicit caching (manually creating and managing cache objects) is not supported in the Interactions API" | type: official
- [C19] 缓存存储位置：Google 内部管理，隔离于 API key/project，不跨项目共享 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Each API key/project maintains separate caches; caches are not shared across projects" | type: official
- [C20] Explicit caching 和 implicit caching 在同一请求中的行为：响应中 `usage.total_cached_tokens` 统一报告所有缓存 token，不区分来源 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "the number of tokens which were cache hits in the response object's usage_metadata" | type: official

## conflicts
- Discount rate for cache reads: Gemini API 定价文件（pricing.md.txt）明确 Gemini 3.8 Flash 缓存读取价格为 $0.075/百万 token（标准 $0.75），即 90% 折扣。但 Vertex AI 文档（cloud.google.com）明确表述"90% discount"和"pay only 10% of standard input token cost"。Gemini API 主文档（caching.md）未明确数值，只说"pass on cost savings"。这三个来源描述一致，无实质冲突，只是 Gemini API 文档因循环计算得出，Vertex AI 更直接表述。
- Implicit caching storage cost: Gemini API 文档（ai.google.dev）对 implicit caching 存储费用无明确说明；Vertex AI 文档（cloud.google.com）明确表述"There are no storage costs for implicit caching"。无法确认此差异是平台差异还是文档遗漏。

## gaps
- Implicit caching 的精确折扣率在 Gemini API 官方文档未明确数值化，只说"cost savings"；无法确认是否与 explicit caching 相同 90% 折扣。
- 无明确证据表明 Gemini 1.5、Gemini 2.0 等早期版本是否支持 explicit caching，文档只言"most models"。
- Implicit caching 是否支持手动清除或仅自动过期，文档未提及。
- 缓存失效的具体触发条件（例如 system instruction 改动、tool 定义改动、输入内容改动等具体属性）在文档中未详细列举。
- Explicit caching 与 implicit caching 在同一请求中是否冲突或如何协作的行为细节。

## leads
- Vertex AI Gemini context caching 在 TTL、storage cost（implicit 无费）、discount rate（明确 90%）上与 Gemini API 表述存在差异，需确认是两套系统的差异还是文档滞后。查看链接：https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview
- Explicit caching 在 Interactions API 中不支持的限制很重要，意味着有状态对话用户必须使用 generateContent API；该限制的持续性需关注。查看：https://ai.google.dev/gemini-api/docs/interactions/caching
- 无论 explicit 还是 implicit，缓存命中的"成本节省保证"和"自动优惠传递"在商业模式和用户可预测性上有显著差异，explicit 保证，implicit 不保证。
