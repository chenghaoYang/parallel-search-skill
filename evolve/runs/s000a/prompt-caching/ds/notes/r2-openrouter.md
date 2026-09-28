# r2-openrouter
question: OpenRouter prompt caching 自建还是透传？各上游自动/需 cache_control|prompt_cache_breakpoint？标记与 TTL 互译、粘性路由字段、命中字段、网关加费、缓存寿命。
checked: https://openrouter.ai/docs/features/prompt-caching ; .../cookbook/administration/usage-accounting ; .../api/api-reference/generations/get-request-&-usage-metadata-for-a-generation ; https://console.groq.com/docs/prompt-caching （均无页面日期；fetched 2026-09-24）
SRC=https://openrouter.ai/docs/features/prompt-caching （未另注 src 的 claim 均出自此页）

## claims
- [C1] D1: 缓存本体在上游 provider；OpenRouter 只做粘性路由把后续请求送回同一 endpoint | quote: "OpenRouter uses provider sticky routing to route your subsequent requests to the same provider endpoint after a cached request." | type: official
- [C2] D2: 多数 provider 自动缓存，个别须逐条消息启用 | quote: "Most providers automatically enable prompt caching, but note that some (see Alibaba and Anthropic below) require you to enable it on a per-message basis." | type: official
- [C3] D2: 自动阵营：OpenAI（最小 1024 tokens）、Grok、Moonshot、Groq、DeepSeek、Z.AI、Gemini 2.5+ implicit | quote: "Prompt caching with OpenAI is automated and does not require any additional configuration. There is a minimum prompt size of 1024 tokens." | type: official
- [C4] D2: OpenRouter 称 Groq 缓存 "Currently available on Kimi K2 models"（与 Groq 官方冲突，见 conflicts） | quote: "Prompt caching with Groq is automated and does not require any additional configuration. Currently available on Kimi K2 models." | type: official
- [C5] D2: Anthropic 两式：顶层 cache_control 自动断点；或逐块显式断点（≤4 个） | quote: "Place `cache_control` directly on individual content blocks for fine-grained control over exactly what gets cached. There is a limit of four explicit breakpoints." | type: official
- [C6] D2: 顶层自动缓存覆盖 Anthropic/Vertex/Azure/Bedrock/Claude Platform on AWS | quote: "Automatic caching (top-level `cache_control`) is supported on the Anthropic, Google Vertex AI, Azure, and Amazon Bedrock providers, as well as Claude Platform on AWS." | type: official
- [C7] D2: Alibaba Qwen 必须显式 cache_control ephemeral，写缓存 5 分钟 TTL | quote: "Alibaba prompt caching requires explicit cache breakpoints." ; "Cache writes use a 5-minute TTL." | type: official
- [C8] D2: Alibaba 显式缓存适用 deepseek/deepseek-v3.2、qwen3-max、qwen-plus、qwen3.6-plus、qwen3-coder-plus、qwen3-coder-flash；快照端点不支持 | quote: "Snapshot endpoints, including `qwen/qwen3.5-plus-02-15` and `qwen/qwen3.5-flash-02-23`, do not support explicit caching." | type: official
- [C9] D2: Gemini 显式缓存需逐块插 cache_control，断点不限数但仅最后一个生效 | quote: "OpenRouter will use only the last breakpoint for Gemini caching across normal message content." | type: official
- [C10] D3: cache_control ↔ prompt_cache_breakpoint 双向互译 | quote: "a text block marked with Anthropic-style `cache_control` gets a `prompt_cache_breakpoint` when routed to a supporting OpenAI model, and a block marked with `prompt_cache_breakpoint` gets a default (5-minute) `cache_control` when routed to Anthropic or Google." | type: official
- [C11] D3: TTL 不互译：cache_control ttl 发往 OpenAI 被丢弃；prompt_cache_options 仅限 OpenAI | quote: "TTLs are not translated — a `cache_control` `ttl` is dropped toward OpenAI, and the request-level `prompt_cache_options` stays OpenAI-only." | type: official
- [C12] D3: prompt_cache_breakpoint 放在单个 text/input_text 块标记前缀终点；prompt_cache_options 在请求根部，mode:"explicit" 关闭 OpenAI 自动断点，ttl 如 "30m" | quote: "placed on an individual text content block (`input_text` in Responses, `text` in Chat Completions) to mark the end of a reusable prefix" | type: official
- [C13] D3: Bedrock 上顶层 cache_control 被译成尾部断点；Responses API 内 per-block cache_control 不暴露，须用 prompt_cache_breakpoint（不带 ttl） | quote: "On Amazon Bedrock, OpenRouter translates the top-level field into a trailing cache breakpoint" | type: official
- [C14] D4: 粘性键优先级：body session_id > x-session-id 头 > prompt_cache_key > 默认（首条 system/developer 消息+首条非 system 消息哈希）；session_id ≤256 字符 | quote: "If neither is set, OpenRouter falls back to the OpenAI-style `prompt_cache_key` request field as the sticky routing key." | type: official
- [C15] D4: 粘性粒度=账户×模型×会话；带 session_id 时任一成功请求即激活，不带则待首次命中后才激活；provider.order 手动排序时不启用 | quote: "Without `session_id`, sticky routing only activates after a cache hit is detected." | type: official
- [C16] D4: 粘性会话 10 分钟无活动过期，成功请求重置计时；仅当缓存读价低于普通价时启用 | quote: "Sticky sessions expire after 10 minutes of inactivity. Each successful request resets the timer." | type: official
- [C17] D5: 命中字段 usage.prompt_tokens_details.cached_tokens（Chat Completions）/ usage.input_tokens_details（Responses）；cache_write_tokens 记写入 | quote: "Cache activity is reported in `usage.input_tokens_details` (Responses) and `usage.prompt_tokens_details` (Chat Completions)" | type: official
- [C18] D5: cached_tokens>0 即命中；cache_write_tokens 仅显式缓存模型返回 | quote: "`cached_tokens`: Number of tokens read from the cache (cache hit)." ; src: https://openrouter.ai/docs/cookbook/administration/usage-accounting | type: official
- [C19] D5: /generation 元数据含 cache_discount（缓存节省额，Anthropic 写缓存可为负）与 native_tokens_cached | src: https://openrouter.ai/docs/api/api-reference/generations/get-request-&-usage-metadata-for-a-generation | quote: "cache_discount: Discount applied due to caching" | type: official
- [C20] D6/D8: 读写价均为上游倍率：Anthropic 写 5m=1.25x/1h=2x、读 0.1x；Alibaba 1.25x/0.1x；DeepSeek 写=原价读 0.1x；Gemini 读 0.25x；Groq 读 0.5x；Grok/Moonshot 0.25x；OpenAI 写 1.25x（GPT-5.6+ 自动缓存也收）、读 0.25x/0.50x | quote: "Cache writes (1-hour TTL): charged at 2x the price of the original input pricing" | type: official
- [C21] D7: Anthropic 默认 5 分钟，可 "ttl":"1h" 延至 1 小时 | quote: "By default, the cache expires after 5 minutes, but you can extend this to 1 hour by specifying `\"ttl\": \"1h\"` in the `cache_control` object." | type: official
- [C22] D7: Gemini 显式写缓存 5 分钟 TTL 不续期；implicit 平均 3–5 分钟 | quote: "Cache Writes have a 5 minute Time-to-Live (TTL) that does not update." ; "the TTL is on average 3-5 minutes, but will vary" | type: official
- [C23] D7: OpenAI 显式缓存前缀最小 30 分钟 TTL，仅 GPT-5.6+ | quote: "Cached prefixes have a minimum 30-minute TTL." ; "OpenAI explicit prompt caching is only supported by OpenAI GPT-5.6 and newer." | type: official
- [C24] D8: Anthropic 最小缓存 4096（Opus 4.5–4.8、Haiku 4.5）/2048（Haiku 3.5）/1024（Sonnet 4/4.5/4.6、Opus 4/4.1）tokens | quote: "Prompts shorter than these minimums will not be cached." | type: official
- [C25] D4: Z.AI 方向 OpenRouter 另发 session affinity key（账户+session_id 派生） | quote: "OpenRouter sends Z.AI a session affinity key with each request, derived from your account and, when provided, your `session_id`." | type: official
- [C26] Groq 官方（对照）：自动缓存、读 50% 折扣、2 小时不用过期、仅 gpt-oss-20b/120b/safeguard-20b | src: https://console.groq.com/docs/prompt-caching | quote: "All cached data automatically expires after 2 hours without use." | type: secondary

## conflicts
- Groq 支持模型：OpenRouter 写 "Currently available on Kimi K2 models"（C4）；Groq 官方 Supported Models 只列 openai/gpt-oss-20b、openai/gpt-oss-120b、openai/gpt-oss-safeguard-20b，无 Kimi K2。不裁决。

## gaps
- 网关是否另收缓存费：官方页只列上游读写倍率与 "no cost"，未声明网关层是否加费。
- 网关自身缓存 TTL：未写；页面 TTL 全为上游 TTL（Anthropic 5m/1h、Alibaba 5m、Gemini 5m 与 3–5m、OpenAI ≥30m）；10 分钟是粘性路由会话过期，非缓存本体寿命。
- 各页面未标日期。

## leads
- /generation 另有 response_cache_source_id（response 级缓存，非 prompt caching），需另查。
- Auto Router 会话粘性：/docs/guides/routing/routers/auto-router#session-stickiness
- provider.order 与粘性互斥：/docs/guides/routing/provider-selection
