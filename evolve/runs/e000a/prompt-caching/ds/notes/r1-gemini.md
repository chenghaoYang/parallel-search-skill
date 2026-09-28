# r1-gemini
question: Google Gemini API 的 context caching 在当前（2026年）的现状——显式 CachedContent（create/get/list/delete）与隐式 implicit caching 两条路径分别怎么触发、门槛、计费、TTL、命中确认字段、失效条件、支持范围。
checked: https://ai.google.dev/gemini-api/docs/caching,https://ai.google.dev/api/caching,https://ai.google.dev/gemini-api/docs/generate-content/caching,https://ai.google.dev/gemini-api/docs/optimization,https://ai.google.dev/gemini-api/docs/pricing,https://ai.google.dev/gemini-api/docs/tokens,https://ai.google.dev/gemini-api/docs/interactions/caching

## claims
- [C1] 隐式缓存默认对所有 Gemini 2.5 及更新模型启用，无需配置 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models." | type: official
- [C2] 显式缓存通过 POST 至 https://generativelanguage.googleapis.com/v1beta/cachedContents 端点创建 | src: https://ai.google.dev/api/caching | quote: "POST https://generativelanguage.googleapis.com/v1beta/cachedContents" | type: official
- [C3] 显式缓存 create 端点必需参数：model（格式 models/{model}，如 gemini-3.8-flash） | src: https://ai.google.dev/api/caching | quote: "model - Format: models/{model} (e.g., gemini-3.8-flash)" | type: official
- [C4] 显式缓存支持 API 操作：cachedContents.create、cachedContents.list、cachedContents.get、cachedContents.patch（仅更新 TTL）、cachedContents.delete | src: https://ai.google.dev/api/caching | quote: "cachedContents.create, cachedContents.list, cachedContents.get, cachedContents.patch, cachedContents.delete" | type: official
- [C5] 显式缓存 create 可选参数：contents、system_instruction、tools、displayName（最多128字符）、toolConfig | src: https://ai.google.dev/api/caching | quote: "displayName - User-friendly identifier (max 128 characters)" | type: official
- [C6] 显式缓存 TTL 设置：支持 ttl（时长格式如"3.5s"）或 expireTime（RFC 3339 UTC 时间戳），二者互斥 | src: https://ai.google.dev/api/caching | quote: "ttl - Time-to-live duration (e.g., \"3.5s\"), expireTime - UTC timestamp in RFC 3339 format, mutually exclusive" | type: official
- [C7] 显式缓存默认 TTL 为 1 小时 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "If not set, the TTL defaults to 1 hour." | type: official
- [C8] Gemini 3.8/3.7/3.6/3.5 Flash 和 3.1 Pro Preview 隐式缓存最小 token 门槛：4,096 | src: https://ai.google.dev/gemini-api/docs/caching.md.txt | quote: "Gemini 3.8, 3.7, 3.6, 3.5 Flash & 3.1 Pro Preview: 4,096 tokens" | type: official
- [C9] Gemini 2.5 Flash 和 Pro 隐式缓存最小 token 门槛：2,048 | src: https://ai.google.dev/gemini-api/docs/caching.md.txt | quote: "Gemini 2.5 Flash & Pro: 2,048 tokens" | type: official
- [C10] 显式缓存最小 token 门槛与隐式相同，因模型而异（Gemini 3.x Flash 4,096；Gemini 2.5 2,048） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Minimum Token Requirements: Vary by model; maximums match the model's standard limits" | type: official
- [C11] 缓存命中计费：90% 折扣（相比标准输入 token 价格）| src: https://ai.google.dev/gemini-api/docs/optimization | quote: "90% discount + Prorated token storage" | type: official
- [C12] Gemini 3.8 Flash 缓存定价示例：标准输入 $0.75/M token，缓存输入 $0.075/M token（90% 折扣）| src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Standard input: $0.75 per 1M tokens, Cached input: $0.075 per 1M tokens (90% off)" | type: official
- [C13] 显式缓存存储费用：2026年12月31日前 $0.50/M token/小时；2027年1月1日起 $1.00/M token/小时 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Through December 31, 2026: $0.50 per 1M tokens per hour, Starting January 1, 2027: $1.00 per 1M tokens per hour" | type: official
- [C14] 隐式缓存命中确认字段：response 中的 usage.total_cached_tokens | src: https://ai.google.dev/gemini-api/docs/interactions/caching | quote: "You can track cached token performance through the usage.total_cached_tokens field in response objects." | type: official
- [C15] 显式缓存 UsageMetadata 字段：totalTokenCount（缓存内容消耗的总 token 数）| src: https://ai.google.dev/api/caching | quote: "Total number of tokens that the cached content consumes." | type: official
- [C16] 隐式缓存是 Interactions API 的唯一支持方式；显式缓存需用 generateContent API | src: https://ai.google.dev/gemini-api/docs/interactions/caching | quote: "The Interactions API only supports implicit caching; developers needing explicit cache management must use the generateContent API instead." | type: official
- [C17] 显式缓存机制：缓存内容作为提示词的前缀来使用 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Cached content functions as a prompt prefix" | type: official
- [C18] 隐式缓存优化建议：将大型且常用的内容放在提示词开头，并在短时间内发送相似请求 | src: https://ai.google.dev/gemini-api/docs/caching.md.txt | quote: "Try putting large and common contents at the beginning of your prompt, Try to send requests with similar prefix in a short amount of time" | type: official
- [C19] 显式缓存创建计费：按标准输入 token 价格计费创建，加上基于 TTL 的存储费用 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "you're billed for the input tokens used to create the cache at the standard input token price, and for explicit caching, there are also storage costs based on how long caches are stored." | type: secondary
- [C20] 显式缓存只能用于创建该缓存的特定模型 | src: https://ai.google.dev/api/caching | quote: "Cached content works only with the specific model it was created for" | type: official

## conflicts
- 隐式缓存 TTL 不明确：文档未指定隐式缓存的默认或最大存活时间；显式缓存明确为 1 小时默认 | src1: https://ai.google.dev/gemini-api/docs/interactions/caching | src2: https://ai.google.dev/gemini-api/docs/generate-content/caching

## gaps
- D8 失效条件具体细节：文档未明确列举哪些改动（模型版本变更、system_instruction 修改、tools 变更等）会导致 miss
- D9 存储介质与作用域：未说明缓存是否跨 API key/项目共享，是否有地域限制

## leads
- Vertex AI 变体：文档搜索中出现 cloud.google.com/vertex-ai 的 CachedContent API，似乎与 ai.google.dev 有相同概念但实现可能不同，值得检查差异
