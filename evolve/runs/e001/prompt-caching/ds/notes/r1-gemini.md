# r1-gemini
question: Google Gemini API 的 context caching 现在的机制是什么？注意 Gemini 可能同时存在两种模式——implicit caching（隐式/自动）和 explicit caching（显式，需要创建 cachedContent 资源）——两种都要分别记录，不要混为一谈。
checked: https://ai.google.dev/gemini-api/docs/caching,https://ai.google.dev/gemini-api/docs/generate-content/caching,https://ai.google.dev/api/caching,https://ai.google.dev/api/generate-content,https://ai.google.dev/pricing,https://ai.google.dev/gemini-api/docs/pricing,https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching

## claims
- [C1] implicit caching 在 Gemini 2.5 及更新版本默认启用，无需代码改动 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models" | type: official
- [C2] Gemini 3.8/3.7/3.6/3.5 Flash 和 3.1 Pro Preview 的 implicit caching 最小 token 数为 4,096 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Gemini 3.8, 3.7, 3.6, 3.5 Flash: 4,096 tokens" | type: official
- [C3] Gemini 2.5 Flash 和 Pro 的 implicit caching 最小 token 数为 2,048 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Gemini 2.5 Flash & Pro: 2,048 tokens" | type: official
- [C4] explicit caching 需要使用 generateContent API，通过 cachedContents.create 手动创建资源 | src: https://ai.google.dev/api/caching | quote: "Create - Establishes a new cached content resource by preprocessing input tokens" | type: official
- [C5] explicit caching 的 API 操作包括 create、list、get、patch、delete | src: https://ai.google.dev/api/caching | quote: "Create...List...Get...Patch...Delete" | type: official
- [C6] explicit caching 的 TTL 默认值为 1 小时 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Defaults to 1 hour; you can customize how long cached tokens persist" | type: official
- [C7] explicit caching 支持通过 ttl（duration）或 expireTime（absolute timestamp）两种方式设置过期时间 | src: https://discuss.ai.google.dev/t/query-gemini-2-0-flash-lite-explicit-caching-costs-and-max-ttl-limit/83445 | quote: "ttl or expire_time" | type: secondary
- [C8] implicit caching 的缓存会在 24 小时内自动清除 | src: https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching | quote: "No storage cost: Caches auto-clear within 24 hours" | type: official
- [C9] 缓存 tokens 的价格为标准输入价格的 10%（90% 折扣）—— 对 implicit 和 explicit caching 都适用 | src: https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching | quote: "Cached tokens are billed at 10% of standard input token cost" | type: official
- [C10] explicit caching 有额外的存储费用，按小时计费，与 TTL 相关 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Storage duration (TTL) — charged based on how long tokens persist" | type: official
- [C11] implicit caching 没有存储成本 | src: https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching | quote: "No storage cost: Caches auto-clear within 24 hours" | type: official
- [C12] 通过 response 的 usageMetadata 字段可以看到 cachedContentTokenCount（缓存 tokens 数） | src: https://ai.google.dev/gemini-api/docs/caching.md.txt | quote: "usage.total_cached_tokens field showing how many tokens came from cache" | type: official
- [C13] response 的 usageMetadata 对象包含 cachedContentTokenCount 字段表示从缓存中获取的 tokens 数 | src: https://discuss.ai.google.dev/t/resolved-gemini-api-context-cache-not-hit/169570 | quote: "CachedContentTokenCount: The number of tokens in the prompt that were served from the cache" | type: secondary
- [C14] 在 generateContent 请求中通过 cachedContent 字段引用已创建的 cache，格式为 cachedContents/{cachedContent} | src: https://ai.google.dev/api/generate-content | quote: "The name of the content cached to use as context to serve the prediction" | type: official
- [C15] explicit cachedContent 资源的完整名称格式为 projects/{project}/locations/{location}/cachedContents/{cachedContent} | src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/v1/projects.locations.cachedContents | quote: "The resource name of the cached content" | type: official
- [C16] explicit cachedContent 资源是独立可查询和可列出的对象，支持通过 list 方法检索所有 cache 条目（支持分页，最多 1000 项/页） | src: https://ai.google.dev/api/caching | quote: "List - Retrieves all cached content entries with pagination support (up to 1,000 items per page)" | type: official
- [C17] explicit caching 仅在 generateContent API 中支持；Interactions API 只支持 implicit caching | src: https://ai.google.dev/gemini-api/docs/caching | quote: "The Interactions API only supports implicit caching. Explicit caching is not supported in the Interactions API" | type: official
- [C18] explicit caching 当前处于 Beta 状态，使用 /v1beta/ 端点 | src: https://ai.google.dev/api/caching | quote: "The API is currently in Beta status, operating under the `/v1beta/` endpoint" | type: official
- [C19] implicit caching 无需改动现有代码，对所有 Gemini 2.5+ 的请求自动应用 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "no cost saving guarantee" 但 "cost savings are automatically applied" | type: official
- [C20] explicit cachedContent 的 patch 操作仅支持更新过期设置（TTL 或 expireTime），不能更新缓存内容本身 | src: https://ai.google.dev/api/caching | quote: "Patch - Updates only the expiration settings of existing cached content (either TTL or absolute expiration time)" | type: official
- [C21] cached content 本身是 prompt 的前缀（prefix），模型对待缓存 tokens 与普通输入 tokens 相同，无特殊区别 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Cached content is a prefix to the prompt" | type: official
- [C22] explicit cachedContent 资源绑定到创建它的模型版本，只能与该模型一起使用 | src: https://ai.google.dev/api/caching | quote: "Cached content is model-specific—it can only be used with the model for which it was created" | type: official
- [C23] 标准 API 速率限制适用于缓存请求，不存在缓存专用配额 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Standard rate limits apply; no special caching-only quotas exist" | type: official
- [C24] 要最大化 cache hit 率，应将大型常用内容放在 prompt 开头，在短时间内发送相似请求 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Try putting large and common contents at the beginning of your prompt" | type: official
- [C25] explicit caching 的 create 操作接受 model、contents、displayName、systemInstruction、ttl 等参数 | src: https://ai.google.dev/api/caching | quote: "Create...by preprocessing input tokens, contents, tools, and system instructions" | type: official
- [C26] 缓存内容的元数据（name、model、creation time、expiry）可查询，但缓存内容本身无法查看 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Cache metadata (name, model, creation time, expiry) is retrievable, but the cached content itself cannot be viewed" | type: official

## conflicts
无

## gaps
- implicit caching 的缓存命中条件的具体技术细节（例如 prefix 多大的改变会导致失效）
- explicit caching 的 storage fees 的具体数值（官方定价页面未明确显示）
- explicit cachedContent 是否可跨 API key 共享（官方未明确说明，仅提及 scope 为 project/location 级别）
- implicit caching 的命中概率具体取决于哪些因素（除了 prefix 相同外）
- explicit caching 在 generateContent API 与 Interactions API 之间的迁移路径

## leads
- Vertex AI 版本的 context caching 在 cloud.google.com 有单独的文档，可能包含额外的 scope 和企业级配置细节
- 缓存的 invalidation 条件与 "prefix" 概念相关，可能需要查看更多关于 cache alignment 或 prefix matching 的实现细节
- implicit caching 的 24 小时自动清除与 explicit caching 的可配置 TTL 形成对比，这是两种模式的关键差异
