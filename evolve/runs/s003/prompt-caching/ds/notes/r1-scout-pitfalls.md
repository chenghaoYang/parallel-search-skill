# r1-scout-pitfalls
question: OpenAI、Anthropic、Gemini、DeepSeek 官方文档里，用户最容易踩错的缓存坑，以及现有网格没有的维度。
checked: https://developers.openai.com/api/docs/guides/prompt-caching (redirected from https://platform.openai.com/docs/guides/prompt-caching), https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching.md (canonical https://platform.claude.com/docs/en/build-with-claude/prompt-caching), https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/news/news0802

## claims
- [C1] OpenAI GPT-5.6+ 隐式模式把断点写在最新 eligible 消息末尾，共享前缀但后缀不同的请求复用不到较短前缀 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "If requests share a long prefix but have different suffixes, caching the first complete request implicitly-only does not make the shorter shared prefix reusable." | type: official
- [C2] OpenAI 的默认缓存保留档位由组织 ZDR 状态决定 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Organizations without Zero Data Retention enabled default to `24h`. Organizations with Zero Data Retention enabled default to `in_memory`." | type: official
- [C3] OpenAI 缓存驻留单机、org 与区域处理边界间不共享，且同 org 内建议用 prompt_cache_key 防跨用户命中探测 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "separate keys help prevent cache-hit probing across users: submitting candidate prompts and observing cache hits to learn whether matching content was previously cached" | type: official
- [C4] OpenAI 早期模型的 cached_tokens 报数要扣除隐藏系统 token 并向下取整到 128 倍数 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Reported `cached_tokens` is calculated by subtracting the hidden system tokens from the last matched breakpoint, then rounding down to the nearest multiple of 128." | type: official
- [C5] Anthropic 缓存 TTL 从写/读请求的开始时刻计，生成耗时计入 TTL | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The lifetime is measured from the start of the request that writes or reads the cache entry, not from the end of its response. Time spent generating a response counts against the lifetime" | type: official
- [C6] Anthropic 的 20-block lookback 只找先前请求在断点写过的条目，断点打在每请求都变的块上永不命中 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The lookback does not find stable content behind your breakpoint and cache it. It finds entries that prior requests already wrote, and writes happen only at breakpoints." | type: official
- [C7] Anthropic usage.input_tokens 只计最后断点之后的 token，总输入须三字段相加 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The `input_tokens` field represents only the tokens that come **after the last cache breakpoint** in your request, not all the input tokens you sent." | type: official
- [C8] Anthropic Batches API 里缓存命中只是 best-effort；max_tokens:0 预热请求在 batch 中被拒 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "because asynchronous batch requests can be processed concurrently and in any order, cache hits are provided on a best-effort basis" | type: official
- [C9] Gemini Interactions API 只支持隐式缓存，显式缓存要用旧版 generateContent API | src: https://ai.google.dev/gemini-api/docs/caching | quote: "The Interactions API only supports implicit caching. Explicit caching (manually creating and managing cache objects) is not supported in the Interactions API." | type: official
- [C10] Gemini 隐式缓存不保证命中/省钱 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "Implicit caching (automatically enabled on Gemini 2.5 and newer models, no cost saving guarantee)" | type: official
- [C11] Gemini 显式缓存独有一个计费维度：按 token 数 × TTL 时长收存储费，TTL 无上下限（默认 1 小时） | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "billed based on the TTL duration of cached token count. There are no minimum or maximum bounds on the TTL." | type: official
- [C12] Gemini 显式缓存创建后只能改 ttl/expire_time，内容不可读回 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "You can set a new `ttl` or `expire_time` for a cache. Changing anything else about the cache isn't supported." | type: official
- [C13] DeepSeek 命中要求"完整匹配一个已持久化的 cache prefix unit"；共享前缀要等系统检测持久化后才可命中（官方例：A+B 后接 A+C miss，第三请求 A+D 才命中 A） | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "A subsequent request can only hit the cache if it **fully matches** a **cache prefix unit**." | type: official
- [C14] DeepSeek 只认从第 0 个 token 起的相同前缀，中段匹配无效 | src: https://api-docs.deepseek.com/news/news0802 | quote: "only requests with identical prefixes (starting from the 0th token) will be considered duplicates. Partial matches in the middle of the input will not trigger a cache hit." | type: official
- [C15] DeepSeek 缓存以 64 token 为存储单元，不足 64 token 不缓存 | src: https://api-docs.deepseek.com/news/news0802 | quote: "The cache system uses 64 tokens as a storage unit; content less than 64 tokens will not be cached." | type: official
- [C16] DeepSeek 缓存按"每用户"隔离 | src: https://api-docs.deepseek.com/news/news0802 | quote: "Each user's cache is isolated and logically invisible to others, ensuring data privacy and security." | type: official

## conflicts
- Gemini 两个官方页面对"缓存命中 token 数"字段写法不同：https://ai.google.dev/gemini-api/docs/caching 写 `usage.total_cached_tokens`（Interactions API），https://ai.google.dev/gemini-api/docs/generate-content/caching 写 `usage_metadata`。属两套 API 的字段名差异，非数值矛盾，但照搬字段名会踩空。
- Anthropic 同页措辞张力：正文写 "The cache is refreshed for no additional cost each time the cached content is used"，而定价表把 "Cache hits and refreshes" 按每百万 token 计价（如 Opus 5.5 $0.20/MTok）。"no additional cost" 指不另收写费，读仍计费，易误读为免费。

## gaps
- OpenAI：streaming 响应里 usage/cached_tokens 出现在哪个 chunk、与 Batch API 的交互，prompt-caching 页未写；your-data 页（ZDR 细节）未逐句核对。
- Anthropic：cache-diagnostics (beta) 独立页未打开；Bedrock 侧 per-model 最小长度在 AWS 文档（超出允许域名）。
- Gemini：显式缓存是否跨 API key / 项目共享、隐式缓存隔离边界，两页均未写；Batch 预测与缓存交互未查。
- DeepSeek：搜索摘要提到 `user_id` 参数可做额外缓存隔离，在 kv_cache 与 news0802 两页均未找到原句，未证实；streaming 下 usage 位置未写。

## leads
- 新维度：数据保留策略改变缓存行为 —— OpenAI 对 ZDR 组织默认 `in_memory` 而非 `24h`（https://developers.openai.com/api/docs/guides/prompt-caching）；Anthropic 写明 ZDR eligible 且 "KV (key-value) cache representations and cryptographic hashes of cached content are held in memory only and are not stored at rest"（https://platform.claude.com/docs/en/build-with-claude/prompt-caching）。
- 新维度：同 org 内缓存共享带来侧信道 —— OpenAI 文档直接建议用 `prompt_cache_key` 分隔记账以 "prevent cache-hit probing across users"（https://developers.openai.com/api/docs/guides/prompt-caching）。网格 D8 只问"是否隔离"，没问"同租户内是否需要主动分 key"。
- 新维度：预热是一等功能且四家形态互异 —— OpenAI `prompt_cache_options.prewarm`（"Tokens written to the cache during a prewarm request are billed at the standard cache-write rate"）；Anthropic `max_tokens: 0`（被 stream/thinking/structured outputs/强制 tool_choice 拒绝，且 batch 内不可用）；Gemini `caches.create` 本身就是预热；DeepSeek 无预热手段且 "Cache construction takes seconds"。
- 新维度：隔离粒度口径不同 —— Anthropic 为 workspace 级（"Bedrock and Google Cloud maintain organization-level cache isolation"）；OpenAI 为 org + 区域处理边界；DeepSeek 为 "each user's cache"；Gemini 未写明。
- 新维度：token 粒度 —— DeepSeek 64-token 存储单元（news0802）；OpenAI 早期模型报数取整 128 且不含 hidden token；Anthropic lookback 以 block 计位（连续 tool_use/tool_result 算一个位置）。
- 坑：TTL 计时口径 —— Anthropic 从请求开始计，"if a response takes 4 minutes to stream, a follow-up request ... must start within about 1 minute"；OpenAI `30m` 是"minimum cache lifetime"而非上限（"OpenAI may retain it longer"）；DeepSeek 清理"usually within a few hours to a few days"无 SLA。
- 坑：速率限额对命中的处理相反 —— OpenAI "Cached input tokens still count toward tokens-per-minute limits"；Anthropic "cache hits are not deducted against your rate limit"。
- 坑：命中单位语义 —— DeepSeek 要 fully match 已持久化 unit（前两个不同后缀请求都 miss）；OpenAI implicit 断点在最新消息末尾致 shared prefix ≠ cached prefix，且 implicit→explicit 切换会丢掉隐式写入、给已有 message 追加内容也会使断点失效；Anthropic lookback 只找写过的条目。
- 坑：并发与可用时延 —— Anthropic "a cache entry only becomes available after the first response begins"，并行首轮打不中；Batches 内命中 best-effort；Gemini 隐式 "no cost saving guarantee"。
- 坑：观测字段口径分裂 —— Anthropic `input_tokens` 只算断点后（总量 = cache_read + cache_creation + input_tokens）；Gemini 两 API 字段名不同；DeepSeek `prompt_cache_hit_tokens/prompt_cache_miss_tokens`；OpenAI 报数取整 128。
- 坑：失效面比预想宽 —— Anthropic 失效表把 web search/citations toggle、speed、thinking/effort 配置都渲染进前缀；"some languages (for example, Swift, Go) randomize key order during JSON conversion, breaking caches"；OpenAI 的 compaction、parallel_tool_calls、text.format 同样改写前缀。
- 坑：Anthropic 自动缓存边界 —— 末块已有不同 TTL 的显式 cache_control 返回 400；已用满 4 个显式断点返回 400；legacy Bedrock 集成不支持顶层 cache_control（400）。
- 新维度：存储计费 —— 只有 Gemini 显式缓存按 token×TTL 计存储费且 TTL 无上下限；且缓存不可变（只能改 ttl/expire_time、内容不可读回）。其它三家按写/读计费、TTL 固定档位。
