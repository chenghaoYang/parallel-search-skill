# r1-openai
question: OpenAI 官方现在的 prompt caching：要不要改请求、缓存单位、门槛、命中字段、读写计价、TTL、失效条件、覆盖哪些模型和端点。
checked: https://developers.openai.com/api/docs/guides/prompt-caching.md, https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics.md, https://developers.openai.com/api/docs/pricing.md, https://developers.openai.com/api/docs/guides/your-data.md, https://developers.openai.com/api/reference/resources/responses/methods/create.md, https://developers.openai.com/api/reference/resources/chat.md, https://developers.openai.com/api/reference/llms.txt, https://platform.openai.com/docs/guides/prompt-caching

## claims
- [C1] D1 支持的模型默认开启。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Prompt caching is enabled by default for supported OpenAI models." | type: official
- [C2] D1 Responses 默认自动放一个隐式 breakpoint，该选项仅 gpt-5.6+。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "Supported for `gpt-5.6` and later models. By default, OpenAI automatically chooses one implicit cache breakpoint." | type: official
- [C3] D1 Chat 的 prompt_cache_options 只有 mode 与 ttl。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "`prompt_cache_options: optional object { mode, ttl }`" | type: official
- [C4] D1 Responses 的 prompt_cache_options 还含 comparison_response_id 与 prewarm。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "`prompt_cache_options: optional object { comparison_response_id, mode, prewarm, ttl }`" | type: official
- [C5] D1 explicit 且无 breakpoint 时，该请求不使用缓存、也不写缓存。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "When no explicit breakpoints are placed, the request does not use prompt caching or create cache writes." | type: official
- [C6] D1 gpt-5.6+ 不必靠 key 优化缓存。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "On GPT-5.6 and later, OpenAI handles cache routing automatically; the key is not needed to optimize caching." | type: official
- [C7] D2 存的是前缀 KV，不是 token 原文。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "The prompt cache stores key-value (KV) tensors, not the tokens themselves." | type: official
- [C8] D2 gpt-5.6+ 的断点不按 token block 取整。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "The breakpoint inherits its TTL from the request's `prompt_cache_options.ttl`; the boundary is not rounded to a token block." | type: official
- [C9] D3 隐藏系统 token 不计入下限。gpt-5.6+ 最少 1024；更早模型随请求设置变化。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Tokens in the OpenAI-provided hidden system content do not count toward this minimum. The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later and varies by request settings for earlier models." | type: official
- [C10] D4 Responses 的命中与写入在 usage.input_tokens_details。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "`input_tokens_details: object { cache_write_tokens, cached_tokens }`" | type: official
- [C11] D4 Chat 的 cache_write_tokens 是写入缓存的未调整 prompt token 数。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "The unadjusted number of prompt tokens written to cache." | type: official
- [C12] D5 gpt-5.6+ 后续读取按未缓存 input 的 0.1× 计。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "It is worth incurring this charge when you know a prefix will be reused, because subsequent reads cost only 0.1× that rate." | type: official
- [C13] D6 gpt-5.6+ 的 cache write 为未缓存 input 的 1.25×。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "For GPT-5.6 and later, cache writes cost 1.25× the standard, uncached input-token rate." | type: official
- [C14] D6 更早模型没有额外的 cache-write 费。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "No additional cache-write charge" | type: official
- [C15] D7 ttl 唯一且默认 30m；自最近写入或复用起 30 分钟可再用，后端可留更久。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "The only supported value, `30m`, is also the default. A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse, though OpenAI may retain it longer." | type: official
- [C16] D7 24h 保留通常约 30 分钟，最长 24 小时。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "`24h`: Extended retention typically keeps entries available for around 30 minutes and can retain them for up to 24 hours." | type: official
- [C17] D7 in_memory 通常闲置 5 到 10 分钟，最长 1 小时。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "`in_memory`: Entries typically remain active for around 5 to 10 minutes of inactivity, up to one hour." | type: official
- [C18] D7 GPU 上的 KV 在 24 小时到期后不保留。 | src: https://developers.openai.com/api/docs/guides/your-data.md | quote: "This data is stored on the local GPU machines and is not retained after the 24-hour expiration." | type: official
- [C19] D7 gpt-5.5 与 gpt-5.5-pro 把 retention 设成 in_memory 会报错。 | src: https://developers.openai.com/api/docs/guides/your-data.md | quote: "For `gpt-5.5` and `gpt-5.5-pro`, setting `prompt_cache_retention` to `in_memory` returns an error." | type: official
- [C20] D8 断点前的内容或相关设置变化后，其后前缀不能命中旧条目。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "If content or a relevant setting changes before a breakpoint, the prefix after that change cannot match the existing cache entry." | type: official
- [C21] D8 缓存不跨组织，也不能跨区域处理边界复用。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Caches are not shared across organizations and cannot be reused across regional processing boundaries." | type: official
- [C22] D8 条目在单机上，高于每分钟 15 个请求会溢出路由。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Cached states live on individual machines, where traffic above 15 requests per minute can lead to overflow routing." | type: official
- [C23] D8 不能手动清除缓存。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "No. Manual cache clearing is not currently available." | type: official
- [C24] D9 更早模型只支持隐式缓存。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Only implicit caching is supported." | type: official
- [C25] D9 Agents 的模型调用与 Responses 缓存行为相同。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Agents API model calls use the same prompt-caching behavior as the Responses API." | type: official
## conflicts
- src A: https://developers.openai.com/api/reference/resources/responses/methods/create.md quote: "For `gpt-5.5`, `gpt-5.5-pro`, and future models, only `24h` is supported." src B: https://developers.openai.com/api/docs/guides/prompt-caching.md quote: "The only supported value, `30m`, is also the default."
- src A: https://developers.openai.com/api/docs/guides/your-data.md quote: "all queries use extended prompt caching for all supported models." src B: https://developers.openai.com/api/docs/guides/prompt-caching.md quote: "Organizations _without_ Zero Data Retention enabled default to `24h`."
- src A: https://developers.openai.com/api/docs/guides/prompt-caching.md quote: "Model-dependent cached-input rate" src B: https://developers.openai.com/api/docs/pricing.md quote: "| gpt-5.5-pro (<272K context length) | $30.00 | - | - | $180.00 |"

## gaps
- 发布文 https://openai.com/index/api-prompt-caching 抓取为空；未找到 changelog 最早条目。llms.txt 参考索引 cache 出现 0 次，未扫 OpenAPI。
- 指南未写 Realtime、Images、Assistants、/v1/completions。旧模型逐个最小 token 与 key 上限未见。无 prompt-cache GB·小时价。复用刷新寿命的原句未列入 claims。

## leads
- Batch 档 gpt-4o cached input 为 -。v1/prompts 不是 cache API。
- 未单列原句：cached_tokens 向下取整到 128；扩展保留含 gpt-5.5/5.5-pro/5.4/5.2/5.1 系列、gpt-5、gpt-5-codex、gpt-4.1。复用刷新寿命不再收写入费。
