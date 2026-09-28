# r1-openrouter
question: OpenRouter 在 prompt caching 上是透传上游字段、自己做网关缓存，还是两者都有？把 D1–D8 用一手原句填满。
checked: https://openrouter.ai/docs/guides/best-practices/prompt-caching, https://openrouter.ai/docs/features/prompt-caching, https://openrouter.ai/docs/guides/features/response-caching, https://openrouter.ai/docs/guides/guides/usage-accounting, https://openrouter.ai/docs/guides/features/zdr, https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request, https://openrouter.ai/docs/api/api-reference/generations/get-request-&-usage-metadata-for-a-generation

页未见日期。OpenAPI 1.0.0。base https://openrouter.ai/api/v1。

## claims
- [C1] D1 两者都有且分开：上游持有 prompt cache；OpenRouter 另做请求级 response cache。 | src: https://openrouter.ai/docs/guides/features/response-caching | quote: "Provider caching is separate from OpenRouter response caching and the two can be used together." | type: official
- [C2] D1 prompt cache 在 provider 内；OpenRouter 缓存发生在请求到达 provider 之前。 | src: https://openrouter.ai/docs/guides/features/response-caching | quote: "provider caching operates within the provider's infrastructure." | type: official
- [C3] D1 隐式 prompt 缓存在供应商机房内存，不是 OpenRouter。 | src: https://openrouter.ai/docs/guides/features/zdr | quote: "in an in-memory cache in the provider's datacenter" | type: official
- [C4] D1/D3 非纯透传：按 provider 在两种断点标记间转换。Bedrock 把顶层字段改成 trailing breakpoint。 | src: https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request | quote: "On Amazon Bedrock, OpenRouter translates the top-level field into a trailing cache breakpoint" | type: official
- [C5] D1/D4 OpenRouter 专有的是 sticky routing，把后续请求钉到同一 provider endpoint，不是自己存 prompt 前缀。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "route your subsequent requests to the same provider endpoint after a cached request." | type: official
- [C6] D2 多数上游自动开；Alibaba 与 Anthropic 要调用方按消息启用。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "some (see Alibaba and Anthropic below) require you to enable it on a per-message basis." | type: official
- [C7] D2 `cache_control.type=ephemeral`；`ttl` 枚举 `5m`|`1h`。顶层自动断点，块级为显式断点，可转成 OpenAI 原生格式。 | src: https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request | quote: "OpenRouter converts them to the provider's native format." | type: official
- [C8] D2 粘性键：body `session_id`（≤256）优先于 `x-session-id`；否则 `prompt_cache_key`。`provider.order` 不用 sticky。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "falls back to the OpenAI-style `prompt_cache_key` request field as the sticky routing key." | type: official
- [C9] D2 GPT-5.6+：根字段 `prompt_cache_options`（`mode` 仅 `explicit`，`ttl` 如 `30m`）与块字段 `prompt_cache_breakpoint.mode=explicit`。 | src: https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request | quote: "Only supported by OpenAI GPT-5.6 and newer." | type: official
- [C10] D2 整响应缓存（另一产品，默认关）：header `X-OpenRouter-Cache`、`X-OpenRouter-Cache-TTL`、`X-OpenRouter-Cache-Clear`；preset `cache_enabled`、`cache_ttl_seconds`。 | src: https://openrouter.ai/docs/guides/features/response-caching | quote: "If neither header nor preset is set, caching is off" | type: official
- [C11] D3 Anthropic：显式最多四个断点，在 text 块；顶层则打在最后可缓存块。短于下限不缓存。页列 4096（Opus 4.8–4.5、Haiku 4.5）、2048（Haiku 3.5）、1024（Sonnet 4.6/4.5、Opus 4.1/4、Sonnet 4）。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Prompts shorter than these minimums will not be cached." | type: official
- [C12] D3 OpenAI 自动，最小 1024。显式断点在 text/`input_text`，该块及之前为前缀。`cache_control.ttl` 去 OpenAI 被丢弃；`prompt_cache_breakpoint` 到 Anthropic/Google 变成默认 5 分钟。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "There is a minimum prompt size of 1024 tokens." | type: official
- [C13] D3 Gemini 2.5+ 隐式不要求断点。显式只用最后一个 `cache_control`；系统指令不可变，动态尾巴须放到后续 user。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "OpenRouter will use only the last breakpoint for Gemini caching" | type: official
- [C14] D4 粘性 provider 不可用则 next-best。闲置 10 分钟过期；报错不更新粘性。无 `session_id` 仅在 cache hit 后才粘；默认键=首条 system/developer + 首条非 system 的哈希。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Sticky sessions expire after 10 minutes of inactivity." | type: official
- [C15] D4/D5 Anthropic 默认 5 分钟，`ttl:"1h"` 可延到 1 小时。Gemini 隐式 TTL 平均 3–5 分钟；显式写入 TTL 5 分钟且不刷新。Alibaba 写入 5 分钟。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "the cache expires after 5 minutes, but you can extend this to 1 hour" | type: official
- [C16] D5/D6 非统一价。Anthropic 写 1.25（1h 为 2x）、读 0.1。OpenAI 读 0.25x 或 0.50x；GPT-5.6 前写入免费，之后写 1.25x。显式前缀最短 30 分钟。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "charge cache writes at 1.25x the price of the original input pricing, even with automatic caching" | type: official
- [C17] D5/D6 读倍率：Google 0.25、DeepSeek 0.1（写入=输入价）、Grok/Moonshot 0.25、Groq 0.5、Alibaba 写 1.25 读 0.1。Grok/Moonshot/Groq 写入 no cost。Gemini 隐式无写入/存储费。Z.AI 写入与 storage 限时免费，读约 0.2x。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "export const GOOGLE_CACHE_READ_MULTIPLIER = '0.25';" | type: official
- [C18] D5/D6 response cache 默认 TTL 300 秒（1–86400）。命中免费，用量为 0。键按 API key 隔离。 | src: https://openrouter.ai/docs/guides/features/response-caching | quote: "Cache hits are free." | type: official
- [C19] D7 Chat：`usage.prompt_tokens_details.cached_tokens`（>0 为命中）、`cache_write_tokens`。Responses：`usage.input_tokens_details`。usage 每次都返回；`usage.include` 已废弃。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "When this is greater than zero, you're benefiting from cached content." | type: official
- [C20] D7 OpenAPI：`cache_write_tokens` 仅显式缓存且有写入定价时返回。generation 另有 `native_tokens_cached`。 | src: https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request | quote: "Only returned for models with explicit caching and cache write pricing." | type: official
- [C21] D7 response cache 用 `X-OpenRouter-Cache-Status: HIT|MISS`，不是 `cached_tokens`。命中时 token 为 0。 | src: https://openrouter.ai/docs/guides/features/response-caching | quote: "X-OpenRouter-Cache-Status: HIT" | type: official
- [C22] D8 分节：OpenAI 自动（显式仅 GPT-5.6+）；Grok、Moonshot、DeepSeek、Z.AI 自动；Groq 目前 Kimi K2；Anthropic cache_control（含 Vertex/Azure/Bedrock）；Gemini 2.5+ 隐式。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Currently available on Kimi K2 models." | type: official
- [C23] D8 Alibaba 显式模型见 quote；快照 qwen3.5-plus-02-15 不支持。response cache 全模型，端点仅 chat、responses、messages、embeddings。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "available on `deepseek/deepseek-v3.2`, `qwen/qwen3-max`, `qwen/qwen-plus`, `qwen/qwen3.6-plus`, `qwen/qwen3-coder-plus`, and `qwen/qwen3-coder-flash`." | type: official

## conflicts
- Gemini 同页：隐式「no manual setup or additional cache_control」「No cache write or storage costs」，TTL「3-5 minutes」；后文却要求 cache_control，写入含 5 分钟存储，TTL「does not update」。https://openrouter.ai/docs/guides/best-practices/prompt-caching
- 同页：FLASH `'1024'`、PRO `'4096'`，又写「typically have a 4096 token minimum」。
- `cache_write_tokens`：usage/OpenAPI「explicit caching and cache write pricing」vs prompt caching 页首次建缓存即出现（含 GPT-5.6 自动写）。https://openrouter.ai/docs/guides/guides/usage-accounting
- `cache_discount`：prompt caching 称在 response body；ChatUsage 无此字段。generation 有 `data.cache_discount`：「Discount applied due to caching」。https://openrouter.ai/docs/api/api-reference/generations/get-request-&-usage-metadata-for-a-generation

## gaps
- DeepSeek/Grok/Moonshot/Groq 最小 token 未写。OpenAI 0.25x vs 0.50x 未点名。Gemini 显式型号未列。
- Messages 的 cache_read_input_tokens 未核对。Anthropic 单独 storage SKU 未写。sticky 10 分钟与上游 TTL 谁先 miss 未写。

## leads
- ZDR 端点字段 `supports_implicit_caching`：https://openrouter.ai/docs/guides/features/zdr
