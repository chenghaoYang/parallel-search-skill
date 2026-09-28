# r1-openai
question: OpenAI 官方 API 的 prompt caching 现在是不是自动前缀缓存、调用方不用改请求？把 D1–D8 全部用一手原句填上。
checked: https://developers.openai.com/api/docs/guides/prompt-caching, https://developers.openai.com/api/docs/guides/your-data, https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics, https://developers.openai.com/api/reference/resources/responses/methods/create, https://developers.openai.com/api/reference/resources/chat, https://developers.openai.com/api/docs/pricing

## claims
- [C1] D1 支持的模型默认开启。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Prompt caching is enabled by default for supported OpenAI models." | type: official
- [C3] D1/D2 POST /responses 与 POST /chat/completions：gpt-5.6+ 的 prompt_cache_options 默认自动放一个 implicit breakpoint。页未见日期。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "By default, OpenAI automatically chooses one implicit cache breakpoint." | type: official
- [C4] D1/D2 仅 mode=explicit 时：没有 explicit breakpoint 则该请求不使用 prompt caching。默认不是这条。页未见日期。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "If there are no explicit breakpoints, the request does not use prompt caching." | type: official
- [C5] D1 更早模型只有隐式缓存。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Only implicit caching is supported." | type: official
- [C6] D1 GPT-5.6+ 不改请求时，隐式缓存整段并不能复用更短的共享前缀。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "If requests share a long prefix but have different suffixes, caching the first complete request implicitly-only does not make the shorter shared prefix reusable." | type: official
- [C7] D2 两端可选 prompt_cache_key，取代 user。页未见日期。 | src: https://developers.openai.com/api/reference/resources/chat | quote: "Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field." | type: official
- [C8] D2 两端 prompt_cache_retention 可选，枚举 in_memory 或 24h。页未见日期。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "prompt_cache_retention: optional "in_memory" or "24h" or null" | type: official
- [C9] D2/D5 prompt_cache_options.ttl 默认且目前只支持 30m。Chat create 同文。页未见日期。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "The `ttl` defaults to `30m`, which is currently the only supported value." | type: official
- [C10] D2/D3 prompt_cache_breakpoint.mode 为 explicit；边界不对齐 token block。页未见日期。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "Marks the exact end of a reusable prompt prefix. The breakpoint inherits its TTL from the request's `prompt_cache_options.ttl`; the boundary is not rounded to a token block." | type: official
- [C12] D3 最小长度：GPT-5.6+ 为 1024；更早模型随请求设置变。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later and varies by request settings for earlier models." | type: official
- [C14] D3 渲染上下文含 instructions、developer、tools，以及 text、images、documents、supported audio。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "OpenAI caches the model's full rendered context including OpenAI-provided instructions, developer messages, tool definitions, and conversation history containing text, images, documents, and supported audio." | type: official
- [C15] D4 须整段前缀匹配；断点前内容或相关设置变化则其后不能命中旧条目。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cache reuse requires the entire rendered prefix to match. If content or a relevant setting changes before a breakpoint, the prefix after that change cannot match the existing cache entry." | type: official
- [C17] D4 换 prompt_cache_key 可在 usage 里记为 cache miss，且可以不是物理 miss。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics | quote: "The supplied key changed between requests. This can be reported as a cache miss in response `usage` without a physical cache miss." | type: official
- [C20] D5 GPT-5.6+：最近一次 write 或 reuse 后至少 30 分钟可复用，可能留更久。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse, though OpenAI may retain it longer." | type: official
- [C21] D5 in_memory：不活跃约 5–10 分钟，最长约 1 小时。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Entries typically remain active for around 5 to 10 minutes of inactivity, up to one hour." | type: official
- [C22] D5 24h 策略：通常约 30 分钟可用，最长可留 24 小时。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Extended retention typically keeps entries available for around 30 minutes and can retain them for up to 24 hours." | type: official
- [C23] D5 开 ZDR 且未指定 prompt_cache_retention 时默认 in_memory。页未见日期。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "Organizations with ZDR enabled default to `in_memory` when `prompt_cache_retention` is not specified." | type: official
- [C25] D5/D6 cache-write 不是叠加费。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cache-write pricing is not an additive fee: input tokens use the uncached-input, cached-input, or cache-write rate." | type: official
- [C26] D6 GPT-5.6+：写入按未缓存 input 的 1.25×，其后读取按该费率的 0.1×。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "For GPT-5.6 and later, cache writes cost 1.25× the standard, uncached input-token rate. It is worth incurring this charge when you know a prefix will be reused, because subsequent reads cost only 0.1× that rate." | type: official
- [C29] D7 Responses：usage.input_tokens_details.cached_tokens 是从缓存取回的 token。同对象还有 cache_write_tokens。页未见日期。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "The number of tokens that were retrieved from the cache." | type: official
- [C30] D7 Chat：usage.prompt_tokens_details.cached_tokens。页未见日期。 | src: https://developers.openai.com/api/reference/resources/chat | quote: "Cached tokens present in the prompt." | type: official
- [C33] D8 extended retention 名单含 gpt-4.1 到 gpt-5.5-pro 等。页未见日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Extended retention is supported by `gpt-5.5`, `gpt-5.5-pro`, `gpt-5.4`, `gpt-5.2`, `gpt-5.1-codex-max`, `gpt-5.1`, `gpt-5.1-codex`, `gpt-5.1-codex-mini`, `gpt-5.1-chat-latest`, `gpt-5`, `gpt-5-codex`, and `gpt-4.1`." | type: official

## conflicts
- 参考：「For `gpt-5.5`, `gpt-5.5-pro`, and future models, only `24h` is supported.」src: https://developers.openai.com/api/reference/resources/responses/methods/create 。指南：「The only supported value, `30m`, is also the default.」src: https://developers.openai.com/api/docs/guides/prompt-caching 。未裁决。
- your-data：「all queries use extended prompt caching for all supported models.」src: https://developers.openai.com/api/docs/guides/your-data 。指南：「30 minutes after its most recent write or reuse」。同页又写 ttl 是 minimum，不是 24h application-state 上限。未裁决。
- 指南 extended retention 含 gpt-5.5-pro；价目该行 cached input 为 -。src: https://developers.openai.com/api/docs/pricing 。未裁决。

## gaps
- 指南正文无 “no code changes required”。temperature、top_p、seed 是否 miss 未写。更早模型无单一最小 token。
- 诊断 reason 除 key 外未逐条摘。Batch 表 gpt-4o cached input 为 -，页未解释。Realtime、POST /completions 未写。各页未见 Updated。

## leads
- 未打开：https://openai.com/index/api-prompt-caching/ （2024-10-01）、https://openai.com/index/better-prompt-caching-for-gpt-6/ （2026-09-22）。
- 未单独成条：128 取整、不跨区域、GPT-6 configuration_update、Agents 同 Responses、无额外 cache-write 费、诊断仅 Responses、价目 gpt-5.5-pro cached 为 -、Chat include_usage、Responses prewarm。
