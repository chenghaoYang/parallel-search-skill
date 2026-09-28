# r1-gemini
question: Google Gemini API 的缓存机制是什么样的？官方文档区分「显式 context caching（CachedContent 资源）」和「implicit caching（隐式/自动缓存）」两种，这两种分别怎么用、怎么计费？
checked: https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs, https://ai.google.dev/gemini-api/docs/models/gemini

## claims
- [C1] 隐式缓存在 Gemini 2.5+ 所有模型上默认启用 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models" | type: official
- [C2] 隐式缓存不需要代码改动，自动生效 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "This automatic feature works with both stateful and stateless conversation modes without requiring manual configuration" | type: official
- [C3] Gemini 2.5 Flash/Pro 隐式缓存最小可缓存长度 2,048 tokens | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Gemini 2.5 Flash and Pro: 2,048 tokens minimum" | type: official
- [C4] Gemini 3.8/3.7/3.6/3.5 Flash 隐式缓存最小可缓存长度 4,096 tokens | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Gemini 3.8, 3.7, 3.6, and 3.5 Flash: 4,096 tokens minimum" | type: official
- [C5] 隐式缓存命中后自动打折，系统自动传递省费 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "automatically pass[es] on cost savings if your request hits caches" | type: official
- [C6] 通过响应中的 usage.total_cached_tokens 字段查看隐式缓存命中 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "You can track cache effectiveness by checking the `usage.total_cached_tokens` field in API responses" | type: official
- [C7] Interactions API 仅支持隐式缓存 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "The Interactions API only supports implicit caching; explicit cache management requires the generateContent API instead" | type: official
- [C8] 显式缓存（CachedContent）需使用 generateContent API 而非 Interactions API | src: https://ai.google.dev/gemini-api/docs/caching | quote: "explicit cache management (creating and managing cache objects directly), you'll need to use the generateContent API instead" | type: official
- [C9] 隐式缓存可在有状态和无状态对话模式下工作 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "works with both stateful and stateless conversation modes" | type: official
- [C10] 最大化缓存命中的优化建议：大内容放在前面，短时间内发送相似请求 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Position large, frequently-used content at the beginning of prompts and send similar requests within short timeframes" | type: official

## conflicts
None identified in documentation fetched.

## gaps
- D2（显式缓存）：cachedContents.create API 的具体参数结构（systemInstruction、displayName 等字段）
- D3（显式缓存）：CachedContent 是否有最小可缓存长度限制
- D4：两种模式的确切折扣比例（百分比）
- D5：显式缓存的存储费用（是否按小时计费、费率）
- D6（显式缓存）：CachedContent 默认/最大 TTL（官方文档未明确说明有效期）
- D6（隐式缓存）：隐式缓存内容在多长时间内保留（文档建议「短时间内」但无明确数值）
- D7：具体哪些改动会导致缓存失效（system prompt/tools/图片/顺序中哪些会破坏命中）
- D8：usageMetadata 中是否有其他字段（如 cacheCreationTokens、cacheReadTokens）表示缓存写入/命中
- D9（显式缓存）：CachedContent 资源支持哪些模型
- D10：缓存存储位置（内存/磁盘/分布式）

## leads
- Vertex AI 上 Gemini 的缓存计费是否与 ai.google.dev 一致（可能存在差异）
- Gemini 3.1 Pro Preview 是否支持隐式缓存（文档列出最小 4,096 tokens 但未明确说默认启用）
- 显式 CachedContent 缓存是否可以跨请求/跨用户复用（需查看资源隔离政策）
