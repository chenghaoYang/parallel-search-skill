# r1-openrouter
question: OpenRouter 在 prompt caching 上是自己缓存，还是把上游（OpenAI 自动缓存、Anthropic cache_control、Gemini cache）映射出来？调用方要改什么，费用和命中字段怎么呈现。
checked: https://openrouter.ai/docs/features/prompt-caching, https://openrouter.ai/docs/guides/best-practices/prompt-caching, https://openrouter.ai/docs/guides/features/response-caching

## claims
- [C1] D1 多数供应商自动开启 prompt caching，Anthropic 与 Alibaba Qwen 需逐条消息加 cache_control | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Most providers automatically enable prompt caching, but note that some ... require you to enable it on a per-message basis." | type: official
- [C2] D1 Anthropic 两种模式：顶层 cache_control 自动缓存，或块级显式断点（上限 4 个） | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Place `cache_control` directly on individual content blocks ... There is a limit of four explicit breakpoints." | type: official
- [C3] D1 顶层 cache_control 自动缓存仅支持 Anthropic、Vertex AI、Azure、Bedrock 及 Claude Platform on AWS；Bedrock 由 OpenRouter 转译为尾部断点 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Automatic caching (top-level `cache_control`) is supported on the Anthropic, Google Vertex AI, Azure, and Amazon Bedrock providers" | type: official
- [C4] D1 块级标记是互译非透传：cache_control→OpenAI 变 prompt_cache_breakpoint，反向变 5 分钟 cache_control；TTL 不互译 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "a text block marked with Anthropic-style `cache_control` gets a `prompt_cache_breakpoint` when routed to a supporting OpenAI model ... TTLs are not translated" | type: official
- [C5] D1 OpenRouter 专有开关：session_id（body 字段或 x-session-id header，≤256 字符）作粘性路由键，缺省回退 prompt_cache_key | src: https://openrouter.ai/docs/features/prompt-caching | quote: "If neither is set, OpenRouter falls back to the OpenAI-style `prompt_cache_key` request field as the sticky routing key." | type: official
- [C6] D1 OpenAI 显式缓存（仅 GPT-5.6+）用块级 prompt_cache_breakpoint + 请求级 prompt_cache_options（mode:"explicit"、ttl） | src: https://openrouter.ai/docs/features/prompt-caching | quote: "OpenAI explicit prompt caching is only supported by OpenAI GPT-5.6 and newer." | type: official
- [C7] D5 Anthropic 价：写 1.25x（5min）/2x（1h）、读 0.1x，基准是 original input pricing（随上游 Anthropic 价） | src: https://openrouter.ai/docs/features/prompt-caching | quote: "charged at 1.25x the price of the original input pricing ... charged at 0.1x the price of the original input pricing" | type: official
- [C8] D5 OpenAI 价：GPT-5.6 前写免费，GPT-5.6+ 写 1.25x（自动缓存也收），读 0.25x/0.50x（随上游 OpenAI 价） | src: https://openrouter.ai/docs/features/prompt-caching | quote: "GPT-5.6 and later charge cache writes at 1.25x the price of the original input pricing, even with automatic caching" | type: official
- [C9] D5 Gemini 隐式无写/存储费、读 0.25x；显式写=输入价+5 分钟存储费（随上游 Google 价） | src: https://openrouter.ai/docs/features/prompt-caching | quote: "No cache write or storage costs." / "Cache write cost = Input token price + (Cache storage price × (5 minutes / 60 minutes))" | type: official
- [C10] D5 其他自动供应商（随各自上游）：Grok/Moonshot 写免费读 0.25x，Groq 写免费读 0.5x，DeepSeek 写=输入价读 0.1x，Z.AI 写暂免费读约 0.2x，Qwen 显式写 1.25x 读 0.1x | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Cache writes: no cost ... charged at 0.25x the price of the original input pricing" | type: official
- [C11] D6 归一化 usage：usage.prompt_tokens_details.cached_tokens（命中读）与 cache_write_tokens（写入）；Responses API 用 usage.input_tokens_details | src: https://openrouter.ai/docs/features/prompt-caching | quote: "cached_tokens: Number of tokens read from the cache (cache hit). ... cache_write_tokens: Number of tokens written to the cache." | type: official
- [C12] D6 响应体有 cache_discount 字段（写负折扣、读正折扣）；另见 Activity 页与 /api/v1/generation | src: https://openrouter.ai/docs/features/prompt-caching | quote: "The `cache_discount` field in the response body will tell you how much the response saved on cache usage." | type: official
- [C13] D4/D7 缓存 TTL 随上游：Anthropic 默认 5 分钟可 "ttl":"1h"；Gemini 隐式平均 3–5 分钟、显式写 5 分钟不续期；OpenAI 显式最低 30 分钟 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "the cache expires after 5 minutes, but you can extend this to 1 hour" / "the TTL is on average 3-5 minutes, but will vary" / "Cached prefixes have a minimum 30-minute TTL." | type: official
- [C14] D4 OpenRouter 自有计时器只有粘性路由（10 分钟无活动过期、成功请求重置），非缓存 TTL | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Sticky sessions expire after 10 minutes of inactivity. Each successful request resets the timer." | type: official
- [C15] prompt cache 本体在 provider 基础设施内，OpenRouter 层只做路由与格式转换 | src: https://openrouter.ai/docs/guides/features/response-caching | quote: "provider caching operates within the provider's infrastructure" | type: official
- [C16] OpenRouter 自有缓存层是 Response Caching（整响应边缘缓存）：X-OpenRouter-Cache: true 开启，命中零计费，TTL 1–86400 秒默认 300，与 prompt caching 可叠加 | src: https://openrouter.ai/docs/guides/features/response-caching | quote: "Caching operates at the OpenRouter layer before the request reaches any provider" / "Cache hits are free." | type: official
- [C17] D9 覆盖：OpenAI/Grok/Moonshot/Groq(仅 Kimi K2)/DeepSeek/Z.AI 自动；Gemini 2.5+ 隐式自动、显式只用最后一个 cache_control 断点；Anthropic 全兼容 provider；Qwen 限列名模型、快照端点不支持 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Currently available on Kimi K2 models." / "Snapshot endpoints ... do not support explicit caching." | type: official
- [C18] D9 最低缓存长度随上游模型：OpenAI 1024 tokens；Anthropic 1024–4096 按模型；Gemini 2.5 Flash 1024、Pro 4096 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "There is a minimum prompt size of 1024 tokens." / "Prompts shorter than these minimums will not be cached." | type: official
- [C19] Gemini 上游 cache 对象由 OpenRouter 代管，调用方无需建/删 cache 或管 TTL | src: https://openrouter.ai/docs/features/prompt-caching | quote: "You do not need to manually create, update, or delete caches. You do not need to manage cache names or TTL explicitly." | type: official

## conflicts
- 无冲突：两个 prompt-caching 文档 URL 正文完全相同。

## gaps
- D5 倍率基准是 "the price of the original input pricing"（OpenRouter 挂牌价），文档未正面声明缓存读写是否另加 OpenRouter markup。
- 「OpenRouter 无自有 prompt-cache 存储/TTL/写入费」无正面原句；最近似证据为 C14、C15。
- Anthropic cache_control 发回 Anthropic 时是否逐字节透传未写明；文档只描述跨供应商转译（C4）与 Bedrock 转译（C3）。
- 页面无更新日期；GPT-5.6 缓存定价变更未给生效日期。

## leads
- 已接入国产缓存：Moonshot 自动 0.25x 读、Z.AI 智谱 ~0.2x、Alibaba Qwen 显式 1.25x/0.1x、Groq 托管 Kimi K2 0.5x、DeepSeek 0.1x。
- Response Caching（C16）是 OpenRouter 真正自有缓存层，grid 若分 prompt/response 缓存应单列。
- Z.AI 命中靠 OpenRouter 发 session affinity key（账户+session_id 派生），异于标准 sticky routing。
