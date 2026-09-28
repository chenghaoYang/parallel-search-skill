# r2-verify-openai
question: OpenAI 现行指南是否仍写 prompt caching 默认开启、可以不传缓存字段；GPT-5.6 及之后的写入价、读取价、TTL 的原句到底是什么；复用会不会刷新 TTL。定价页上 gpt-5.6 与至少一个更早模型的 cached/write 单元格必须出现在 quote 里。
checked: https://developers.openai.com/api/docs/guides/prompt-caching ; https://developers.openai.com/api/docs/pricing ; https://developers.openai.com/api/reference/resources/responses/methods/create (all fetched 2026-09-24)

## claims
- [C1] D1: guide still says caching is on by default, no opt-in | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Prompt caching is enabled by default for supported OpenAI models." | type: official
- [C2] D1: implicit mode needs no cache fields; breakpoints placed automatically | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Implicit mode: OpenAI chooses breakpoint locations out of the box that work well for most use cases." | type: official
- [C3] D1: API ref confirms default behavior of prompt_cache_options | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "By default, OpenAI automatically chooses one implicit cache breakpoint." | type: official
- [C4] D4: GPT-5.6+ cache-write multiplier = 1.25× uncached input rate | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "For GPT-5.6 and later, cache writes cost 1.25× the standard, uncached input-token rate." | type: official
- [C5] D4: GPT-5.6+ cache-read multiplier = 0.1× uncached input rate | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "It is worth incurring this charge when you know a prefix will be reused, because subsequent reads cost only 0.1× that rate." | type: official
- [C6] D4: cache-write is not an additive fee; each input token billed at one of three rates | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cache-write pricing is not an additive fee: input tokens use the uncached-input, cached-input, or cache-write rate." | type: official
- [C7] D4: earlier models (GPT-5.5 and older) have no cache-write charge | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cache write charge | 1.25× the uncached input-token rate | No additional cache-write charge | No additional cache-write charge" | type: official
- [C8] D4: pricing page Standard row for gpt-5.6-sol: input $4.00 / cached $0.40 / cache writes $5.00 per 1M (short context) | src: https://developers.openai.com/api/docs/pricing | quote: "gpt-5.6-sol | $4.00 | $0.40 | $5.00 | $20.00 | $8.00 | $0.80 | $10.00 | $30.00" | type: official
- [C9] D4: pricing page earlier-model rows show cached price but "-" (no fee) in cache-writes column | src: https://developers.openai.com/api/docs/pricing | quote: "gpt-5.5 (<272K context length) | $5.00 | $0.50 | - | $30.00" and "gpt-5 | $1.25 | $0.125 | - | $10.00" | type: official
- [C10] D5: TTL field is prompt_cache_options.ttl, only supported value 30m, also default | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Use `prompt_cache_options.ttl` to control the minimum cache lifetime. The only supported value, `30m`, is also the default." | type: official
- [C11] D5: reuse refreshes TTL — refresh sentence exists verbatim (resolves last round's doubt) | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "A later request can reuse a cached prefix only while its entry remains available, and reusing the prefix refreshes its lifetime without another cache-write charge." | type: official
- [C12] D5: 30-minute eligibility counted from latest write OR reuse | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse, though OpenAI may retain it longer." | type: official
- [C13] D5: API ref field spec for ttl | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "The minimum lifetime applied to every implicit and explicit cache breakpoint written by the request. Defaults to `30m`, which is currently the only supported value." | type: official
- [C14] D5: prompt_cache_retention (in_memory/24h) is the earlier-model knob, deprecated in favor of ttl | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "Deprecated. Use `prompt_cache_options.ttl` instead." | type: official
- [C15] context: min cacheable prefix for GPT-5.6+ | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later" | type: official
- [C16] date note on pricing page | src: https://developers.openai.com/api/docs/pricing | quote: "GPT-5.6 Sol's promotional pricing is available at least through November 21, 2026." | type: official

## conflicts
- 无（指南 1.25×/0.1× 与定价表 $5.00/$0.40 on $4.00 input 数值一致）

## gaps
- 两页均无 "last updated" 日期；只有 C16 的促销截止日。
- 复用刷新 TTL 的句子位于通用 "Cache lifetime" 节，未逐模型区分；更早模型的 in_memory 档只说 "5 to 10 minutes of inactivity"，是否同样由 reuse 刷新未逐字写明（仅由 inactive 一词暗示）。

## leads
- API ref 写 "considers up to the latest 80 breakpoints"，指南写 lookup boundaries 为 "first 2 and latest 50 explicit breakpoints" — 口径不同，如需精确数字另核。
