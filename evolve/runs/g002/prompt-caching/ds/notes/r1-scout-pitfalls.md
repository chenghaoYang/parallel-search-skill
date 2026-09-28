# r1-scout-pitfalls
question: 在 OpenAI、Anthropic、Gemini、DeepSeek 的官方缓存文档里，找出网格没单列、但调用方很容易踩坑的规则（确认命中的方法、看似无关却会让前缀失效的改动、路由/组织/并发限制）。只产出线索，不填成稿。
checked: https://developers.openai.com/api/docs/guides/prompt-caching, https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/api/rate-limits, https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics.md, https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/api/caching, https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/quick_start/rate_limit, https://api-docs.deepseek.com/news/news0802

## claims
- [C1] OpenAI 缓存不跨组织，也不能跨区域处理边界复用。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Caches are not shared across organizations and cannot be reused across regional processing boundaries." | type: official
- [C2] 缓存态在单机上；同前缀超过 15 次/分钟会溢出路由。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cached states live on individual machines, where traffic above 15 requests per minute can lead to overflow routing." | type: official
- [C3] GPT-5.6 及之后 prompt_cache_key 不再用来优化路由。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "On GPT-5.6 and later, OpenAI handles cache routing automatically; the key is not needed to optimize caching." | type: official
- [C4] 改 tools 的名字、描述、schema 或顺序会改变 OpenAI 可缓存前缀。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Changes tool names, descriptions, schemas, ordering, or tool-specific instructions." | type: official
- [C5] OpenAI 渲染进缓存的上下文含图片、文档和受支持音频。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "OpenAI caches the model's full rendered context including OpenAI-provided instructions, developer messages, tool definitions, and conversation history containing text, images, documents, and supported audio." | type: official
- [C6] Claude API、AWS 上的 Claude Platform、Foundry 按 workspace 隔离；Bedrock 与 Google Cloud 只按组织。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Caches are also isolated per workspace within an organization on the Claude API, Claude Platform on AWS, and Microsoft Foundry; Bedrock and Google Cloud use organization-level isolation only." | type: official
- [C7] Anthropic 按 tools、system、messages 的顺序引用整段前缀。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching references the entire prompt: tools, system, and messages (in that order), up to and including the block designated with cache_control." | type: official
- [C8] 改 tool_choice，或任意位置增减图片，会使 Anthropic 缓存失效。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Changes to tool_choice or the presence/absence of images anywhere in the prompt will invalidate the cache, requiring a new cache entry to be created." | type: official
- [C9] tool_use 的 JSON 键序不稳（如 Swift、Go）会破坏 Anthropic 缓存。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Verify that the keys in your tool_use content blocks have stable ordering as some languages (for example, Swift, Go) randomize key order during JSON conversion, breaking caches" | type: official
- [C10] Anthropic 缓存要等第一条响应开始后，并行请求才能命中。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "For concurrent requests, note that a cache entry only becomes available after the first response begins." | type: official
- [C11] 多数 Claude 模型只有未缓存输入计入 ITPM。 | src: https://platform.claude.com/docs/en/api/rate-limits | quote: "For most Claude models, only uncached input tokens count toward your ITPM rate limits." | type: official
- [C12] DeepSeek 的 user_id 用于隔离业务侧用户的 KVCache。 | src: https://api-docs.deepseek.com/quick_start/rate_limit | quote: "user_id is used to isolate KVCache for users on your business side for privacy management" | type: official
- [C13] DeepSeek 必须完整匹配已落盘的缓存前缀单元才命中。 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "A subsequent request can only hit the cache if it fully matches a cache prefix unit." | type: official
- [C14] Gemini 显式缓存只能用于创建它的那个 model。 | src: https://ai.google.dev/api/caching | quote: "Cached content can be only used with model it was created for." | type: official
- [C15] 诊断比较失败不一定是前缀变了：可能没带 beta header、换了 workspace，或隔太久。 | src: https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics | quote: "Typically the previous request did not carry the beta header, it came from a different workspace, or too much time has passed since it was sent." | type: official

## conflicts
- Gemini 命中字段：https://ai.google.dev/gemini-api/docs/caching （Last updated 2026-09-02 UTC）"You can see the number of tokens which were cache hits in the response object's usage.total_cached_tokens (Python and JavaScript) field." vs https://ai.google.dev/gemini-api/docs/generate-content/caching （Last updated 2026-09-11 UTC）"You can see the number of tokens which were cache hits in the response object's usage_metadata field."
- Gemini 是否保证省钱：前页 "We automatically pass on cost savings if your request hits caches."；后页 "Implicit caching (automatically enabled on Gemini 2.5 and newer models, no cost saving guarantee)"。不裁决。
- DeepSeek：https://api-docs.deepseek.com/news/news0802 "The cache system uses 64 tokens as a storage unit; content less than 64 tokens will not be cached." 本次打开的 https://api-docs.deepseek.com/guides/kv_cache 未出现 64，并写 "Due to the Sliding Window Attention mechanism, the storage and matching of cached prefixes differs from before." 不裁决 64 是否仍生效。

## gaps
- 不传 user_id 是否跨终端用户共享 KV：未写明。news0802 "Each user's cache is isolated and logically invisible to others, ensuring data privacy and security." 未定义 user 是否等于 user_id。
- 未找到 Gemini 跨 project/API key 共享的句子，也未找到 cachedContent 与请求级 systemInstruction 互斥句。
- 旧 header prompt-caching-2024-07-31 是否已取消：find 未命中 FAQ 原句。诊断示例 header 是 cache-diagnosis-2026-04-07。
- 未打开 OpenAI diagnostics 子页，面板字段与 API 是否一致未知。
- 已核、未进 C：OpenAI 同页 "Keys influence routing; they do not pin requests to a machine or guarantee a cache hit." generate-content/caching "Explicit context caching is currently in Beta. Endpoints and SDK methods are available under v1beta."

## leads
- OpenAI | 不跨组织、不跨区域处理边界；单机缓存，同前缀约超过 15 RPM 会溢出 | https://developers.openai.com/api/docs/guides/prompt-caching
- OpenAI | GPT-5.6+ 的 prompt_cache_key 不再优化路由；key 不钉机器，也不保证命中 | https://developers.openai.com/api/docs/guides/prompt-caching
- OpenAI | tools 顺序/schema，以及图片、文档、受支持音频，都在渲染前缀里 | https://developers.openai.com/api/docs/guides/prompt-caching
- Anthropic | API、Claude Platform on AWS、Foundry 按 workspace 隔离；Bedrock 与 Google Cloud 只按组织 | https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic | 前缀顺序锁死 tools → system → messages；改 tool_choice 或任意位置图片有无会失效 | https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic | tool_use JSON 键序不稳会失效；并行请求须等第一条响应开始后才能命中 | https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic | 多数模型的 cache_read 不计入 ITPM | https://platform.claude.com/docs/en/api/rate-limits
- Anthropic | 查分歧要带 beta header cache-diagnosis-2026-04-07；没带 header、跨 workspace 或隔太久并不证明前缀变了 | https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics
- Gemini | 显式 CachedContent 只能用于创建它的那个 model | https://ai.google.dev/api/caching
- Gemini | 显式缓存标 Beta，端点在 v1beta。隐式一页写命中就返利，另一页写 no cost saving guarantee；命中字段分别是 usage.total_cached_tokens 与 usage_metadata | https://ai.google.dev/gemini-api/docs/generate-content/caching
- DeepSeek | 只有完整匹配已落盘的缓存前缀单元才命中，不是任意重叠前缀 | https://api-docs.deepseek.com/guides/kv_cache
- DeepSeek | user_id 隔离业务侧 KVCache。公告写每个用户缓存互不可见，但是否等于 user_id、不传是否共享，都没写死 | https://api-docs.deepseek.com/quick_start/rate_limit
- DeepSeek | 公告仍以 64 token 为存储单元；现行指南改称 SWA 前缀单元。不裁决 | https://api-docs.deepseek.com/news/news0802
