# r1-scout
question: prompt caching 这个范围内，还有哪些网格没列的实体或维度，以及用户最容易踩的、已有家族解释不了的坑？
checked: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html, https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching, https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching?view=foundry-classic, https://ai.google.dev/gemini-api/docs/caching, https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview, https://docs.volcengine.com/docs/82379/1398933, https://platform.minimax.io/docs/api-reference/text-prompt-caching, https://platform.minimax.io/docs/api-reference/anthropic-api-compatible-cache, https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api, https://www.alibabacloud.com/help/en/model-studio/context-cache, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://developers.openai.com/api/docs/guides/prompt-caching

## claims
- [C1] Bedrock 隐式缓存不必在请求里放 cache control。 | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "without requiring cache controls in your request." | type: official
- [C2] Bedrock 跨区域推理在高需求时增加 cache write。 | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "At times of high demand, these optimizations may lead to increased cache writes." | type: official
- [C3] Bedrock 上 Claude：Converse 用 cachePoint，InvokeModel 用 cache_control。 | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "In the Converse API, add \"ttl\": \"1h\" to your cachePoint object. In the InvokeModel API for Claude models, add \"ttl\": \"1h\" to your cache_control object." | type: official
- [C4] Bedrock Converse 的 inputTokens 只计未进缓存的输入。 | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "the inputTokens field represents only the non-cached input tokens" | type: official
- [C5] Azure：前 1024 token 差一字则 cached_tokens=0。ms.date 2026-08-11。 | src: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching | quote: "A single character difference in the first 1,024 tokens results in a cache miss, which is characterized by a cached_tokens value of 0." | type: official
- [C6] Azure GPT-5.6 断点：Responses 与 Chat Completions 的块类型不同。ms.date 2026-08-11。 | src: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching | quote: "The Responses API supports breakpoints on input_text, input_image, and input_file blocks. The Chat Completions API supports breakpoints on text, image_url, input_audio, and file blocks." | type: official
- [C7] OpenAI 缓存不能跨组织，也不能跨 regional processing boundary。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Caches are not shared across organizations and cannot be reused across regional processing boundaries." | type: official
- [C8] GPT-5.6 仅隐式时，换后缀后较短公共前缀不会复用。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "If requests share a long prefix but have different suffixes, caching the first complete request implicitly-only does not make the shorter shared prefix reusable." | type: official
- [C9] Gemini Interactions API 不支持显式缓存对象。Last updated 2026-09-02 UTC。 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Explicit caching (manually creating and managing cache objects) is not supported in the Interactions API." | type: official
- [C10] Agent Platform 显式缓存默认 TTL 60 分钟，可再延长。Last updated 2026-09-22 UTC。 | src: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview | quote: "Update a context cache's expiration time (Time to Live, or TTL) past the default 60 minutes." | type: official
- [C11] 方舟隐式不保证命中，分布式路由影响命中概率。更新 2026.09.22 16:52:16。 | src: https://docs.volcengine.com/docs/82379/1398933 | quote: "不保证命中：缓存容量有限，旧缓存可能被淘汰；分布式路由也会影响命中概率。" | type: official
- [C12] 方舟显式缓存最长 7 天，超过 expire_at 即过期且不因使用重置。页末 2026.09.22。 | src: https://docs.volcengine.com/docs/82379/1398933 | quote: "当前最大可存储时间为 7 天，即当前 UTC Unix 时间戳 + 604800。当当前时刻超过过期时刻，则存储过期；不会随着缓存 / 存储的使用而重置缓存生命周期。" | type: official
- [C13] MiniMax 把要在 Anthropic API 里显式设参数的模式与被动缓存分开。 | src: https://platform.minimax.io/docs/api-reference/text-prompt-caching | quote: "the caching mode that requires explicitly setting parameters in the Anthropic API" | type: official
- [C14] Kimi Messages 的 cache_control 只在顶层生效，体内标记被忽略，不是 F2。 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "`cache_control` is effective only at the top level; the same marker inside the messages body is ignored." | type: official
- [C15] 通义显式与隐式互斥。 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "Explicit cache and implicit cache are mutually exclusive." | type: official

## conflicts
- GPT-5.6 的 prompt_cache_key：Azure "This parameter improves cache matching for related requests." | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching OpenAI "On GPT-5.6 and later, OpenAI handles cache routing automatically; the key is not needed to optimize caching." | https://developers.openai.com/api/docs/guides/prompt-caching 同页 Azure 又写超过约 15 rpm "some requests might miss the cache."
- Bedrock 同页： "For GPT-5.6 models, you control caching with explicit breakpoints. For GPT-5.5 and earlier, caching is automatic." 与 "implicit (default) — Places an automatic breakpoint on the latest message and also uses any explicit breakpoints you provide." | https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
- TPM：OpenAI "Cached input tokens still count toward tokens-per-minute limits." | https://developers.openai.com/api/docs/guides/prompt-caching Bedrock 上 OpenAI 模型 "Cached input tokens read through prompt caching do not count against the input-tokens-per-minute quota." | https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html

## gaps
- 已打开页都没写「命中率接近 0」。用语是溢出、部分 miss、增加 cache write、路由影响概率、不能跨区域复用。
- 硅基流动 docs 搜索只见「前缀续写」，未打开缓存机制页。方舟旧 Context API（82379/1396491）未打开。
- 百炼 Session cache 专页、Agent Platform 限额数字、Anthropic 直连是否仍强制断点，未打开。智谱无硬性 TTL。Azure classic 与现行页同文。
- 勿由 OpenAI 的 Responses 示例推断直连没有 Chat Completions 断点。

## leads
- Azure OpenAI | 非 OpenAI 别名：GPT-5.6 起两套 API 断点块类型不同（C6）；更早模型带这些字段 400；PTU-M 无断点且关不掉；key 与直连冲突。 | 是 | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching
- Amazon Bedrock | F1 隐式加 F2 三套语法（cachePoint / cache_control / prompt_cache_breakpoint）。跨区域增加 write。批推理不支持。Nova 不单列。 | 是 | https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
- 火山方舟 | 隐式 F1 关不掉，与显式互斥。显式是 previous_response_id 会话对象：有存储费、最长 7 天（C12），命中不续期。不是 F2，也不是 cachedContents。 | 是 | https://docs.volcengine.com/docs/82379/1398933
- MiniMax | 被动 F1 与 Anthropic 主动 F2（cache_control，5 分钟，写入另收费）两套。M3 只在被动列表。 | 是 | https://platform.minimax.io/docs/api-reference/text-prompt-caching
- 维度：GPT-5.6 隐式断点在最新消息末尾 | 稳定头部不一定命中（C8）。OpenAI、Azure、Bedrock 同时出现。2026 是加上显式，不是改回纯手动。 | 是 | https://developers.openai.com/api/docs/guides/prompt-caching
- 维度：机器/区域亲和 | 无「接近 0」。OpenAI 单机且约 15 rpm 溢出、不能跨区域（C7）。Azure 同 key 约 15 rpm 部分 miss。Bedrock 跨区域增加 write（C2）。方舟路由影响概率（C11）。 | 是 | https://developers.openai.com/api/docs/guides/prompt-caching
- 维度：usage 是否含缓存 token | Bedrock inputTokens 不含读写（C4）。Kimi Messages 不含、Chat 含。百炼 Anthropic cache_read 不进 input_tokens。 | 是 | https://www.alibabacloud.com/help/en/model-studio/context-cache
- Kimi | 一眼 F1（mode 仅 implicit）。Messages 顶层 cache_control 是写入开关，不是断点。 | 是 | https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api
- 通义千问/百炼 | 一眼同时有 F1（隐式、不可关）和 F2（cache_control ephemeral）。互斥。tools 上的标记被忽略。 | 是 | https://www.alibabacloud.com/help/en/model-studio/context-cache
- 智谱 GLM | 一眼 F1：隐式、无需手动配置。 | 是 | https://docs.bigmodel.cn/cn/guide/capabilities/cache
- Gemini API 面（不新开行） | Interactions 无显式对象（C9）。Agent Platform 显式仍是缓存资源，默认 TTL 60 分钟（C10）。并入现有两行。 | 否 | https://ai.google.dev/gemini-api/docs/caching
