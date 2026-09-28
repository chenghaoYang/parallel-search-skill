# r1-deepseek
question: DeepSeek 官方上下文缓存（含「硬盘缓存」这一说法是否成立）：要不要改代码、缓存存在哪、门槛、命中字段、命中/未命中价格、TTL、失效、哪些模型。
checked: https://api-docs.deepseek.com/zh-cn/guides/kv_cache, https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/zh-cn/quick_start/pricing, https://api-docs.deepseek.com/quick_start/pricing, https://api-docs.deepseek.com/zh-cn/news/news0802, https://api-docs.deepseek.com/news/news0802, https://api-docs.deepseek.com/zh-cn/updates/, https://api-docs.deepseek.com/zh-cn/quick_start/rate_limit, https://api-docs.deepseek.com/api/create-chat-completion/, https://api-docs.deepseek.com/zh-cn/api/create-completion/, https://api-docs.deepseek.com/api/create-response/, https://api-docs.deepseek.com/zh-cn/api/create-response/, https://api-docs.deepseek.com/zh-cn/guides/responses_api, https://api-docs.deepseek.com/guides/responses_api, https://api-docs.deepseek.com/guides/anthropic_api, https://api-docs.deepseek.com/zh-cn/guides/anthropic_api, https://api-docs.deepseek.com/zh-cn/news/news260910, https://api-docs.deepseek.com/news/news260910

## claims
- [C1] D1：标题即「上下文硬盘缓存」；默认开启，不用改代码。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "DeepSeek API 上下文硬盘缓存技术对所有用户默认开启，用户无需修改代码即可享用。" | type: official
- [C2] D1：每个请求都构建硬盘缓存。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "用户的每一个请求都会触发硬盘缓存的构建。" | type: official
- [C3] D2：英文写 hard disk cache。 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Each user request will trigger the construction of a hard disk cache." | type: official
- [C4] D2：命中前提是前缀已写入硬盘缓存。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "缓存命中的前提是相应前缀已被“落盘”（写入硬盘缓存）。" | type: official
- [C5] D2：2024 公告写分布式硬盘阵列。 | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "把预计未来会重复使用的内容，缓存在分布式的硬盘阵列中。" | type: official
- [C6] D2/D3：须完整匹配缓存前缀单元。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "后续请求只有在完整匹配缓存前缀单元时，才能命中缓存。" | type: official
- [C8] D2：长输入按未写明数字的固定 token 间隔截取前缀单元。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "系统会以一定的 token 数量为间隔，截取缓存前缀单元" | type: official
- [C9] D3：2024 英文公告以 64 tokens 为存储单元，不足不缓存。 | src: https://api-docs.deepseek.com/news/news0802 | quote: "The cache system uses 64 tokens as a storage unit; content less than 64 tokens will not be cached." | type: official
- [C10] D4：usage 字段为 prompt_cache_hit_tokens 与 prompt_cache_miss_tokens。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "prompt_cache_hit_tokens：本次请求的输入中，缓存命中的 tokens 数" | type: official
- [C11] D4：Chat POST /chat/completions：prompt_tokens = hit + miss。 | src: https://api-docs.deepseek.com/api/create-chat-completion/ | quote: "It equals prompt_cache_hit_tokens + prompt_cache_miss_tokens." | type: official
- [C12] D4：prompt_tokens_details.cached_tokens 与 hit 相同。 | src: https://api-docs.deepseek.com/api/create-chat-completion/ | quote: "Number of tokens in the prompt that hit the context cache. Same as prompt_cache_hit_tokens." | type: official
- [C13] D9：FIM POST /completions 的 base_url 为 https://api.deepseek.com/beta。同页 usage 含 prompt_cache_hit_tokens。 | src: https://api-docs.deepseek.com/zh-cn/api/create-completion/ | quote: "用户需要设置 base_url=\"https://api.deepseek.com/beta\" 来使用此功能。" | type: official
- [C14] D4：Responses 命中字段是 input_tokens_details.cached_tokens。该页无 prompt_cache 字符串。 | src: https://api-docs.deepseek.com/api/create-response/ | quote: "Number of input tokens that hit the context cache. See Context Caching." | type: official
- [C15] D1/D8：不支持 prompt_cache_key / prompt_cache_retention，缓存自动管理。 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "prompt_cache_key / prompt_cache_retention Not supported. Context caching is managed automatically" | type: official
- [C16] D5：英文 cache hit /1M：flash 空闲 $0.003 高峰 $0.006；pro 空闲 $0.022 高峰 $0.044。 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "1M INPUT TOKENS (CACHE HIT) OFF-PEAK $0.003 $0.022 PEAK $0.006 $0.044" | type: official
- [C17] D5：中文缓存命中/百万：flash 空闲 0.02元 高峰 0.04元；pro 空闲 0.15元 高峰 0.30元。 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "百万tokens输入（缓存命中）空闲时段 0.02元 0.15元 高峰时段 0.04元 0.30元" | type: official
- [C18] D6：英文 cache miss /1M：flash $0.15/$0.3；pro $0.66/$1.32。定价页无存储费或 cache write 行。 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "1M INPUT TOKENS (CACHE MISS) OFF-PEAK $0.15 $0.66 PEAK $0.3 $1.32" | type: official
- [C19] D6：中文缓存未命中/百万：flash 空闲 1元 高峰 2元；pro 空闲 4.5元 高峰 9.0元。 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "百万tokens输入（缓存未命中）空闲时段 1元 4.5元 高峰时段 2元 9.0元" | type: official
- [C20] D5/D6：空闲为高峰一半。英文高峰 UTC 工作日 01:00–04:00 与 06:00–10:00。 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday, excluding Chinese public holidays." | type: official
- [C21] D5/D6：中文高峰为北京时间工作日 9:00–12:00、14:00–18:00；周末与中国法定节假日全天空闲。 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "北京时间周一至周五（不含中国法定节假日）9:00 - 12:00、14:00 - 18:00 为高峰时段" | type: official
- [C22] D6：英文公告写 storage is free，与 $0.014 命中价同一句。 | src: https://api-docs.deepseek.com/news/news0802 | quote: "storage usage for the cache is free." | type: official
- [C23] D7：不用后自动清空，一般为几个小时到几天。无整数小时 TTL。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "缓存不再使用后会自动被清空，时间一般为几个小时到几天" | type: official
- [C24] D7：英文指南同义。 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "usually within a few hours to a few days." | type: official
- [C25] D8：尽力而为，不保证 100% 命中。输出仍推理，受 temperature 影响。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "缓存系统是“尽力而为”，不保证 100% 缓存命中" | type: official
- [C26] D8：例二前两次不命中。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "在上例中，前两次请求不会命中缓存。" | type: official
- [C27] D8：user_id 用于 KVCache 隔离，不是开启缓存的参数。 | src: https://api-docs.deepseek.com/zh-cn/quick_start/rate_limit | quote: "user_id 用于我们对您业务侧用户进行 KVCache 隔离，以进行隐私管理" | type: official
- [C29] D9：deepseek-flash（DeepSeek-V4.1-Flash）与 deepseek-v4-pro（DeepSeek-V4-Pro-0813）两列都有命中/未命中价。 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "模型名请使用 deepseek-flash。" | type: official
- [C30] D9：OpenAI BASE URL 为 https://api.deepseek.com。同页另有 Anthropic BASE URL。 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "BASE URL (OpenAI Format) https://api.deepseek.com" | type: official
- [C31] D9：旧名 deepseek-v4-flash 与 deepseek-v4-flash-vision-exp 由 V4.1-Flash 按 Flash 价提供。 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "请求将由 DeepSeek-V4.1-Flash 模型提供服务，并按 Flash 价格计费。" | type: official
- [C32] D1/D9：Anthropic cache_control 为 Ignored；该页无 prompt_cache。 | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "cache_control Ignored" | type: official
- [C33] D9：changelog 最早相关条为 2024-08-02。 | src: https://api-docs.deepseek.com/zh-cn/updates/ | quote: "DeepSeek API 创新采用硬盘缓存，价格再降一个数量级" | type: official

## conflicts
- D3：现行中英指南无 “64”（检索 has64=false），只要求完整匹配缓存前缀单元。同页写 Sliding Window Attention，「与之前有所不同」（https://api-docs.deepseek.com/zh-cn/guides/kv_cache）。2024 公告仍写 64-token 单元、不足不缓存（https://api-docs.deepseek.com/news/news0802）。
- D8：公告「从第 0 个 token 开始相同」vs 指南例二前两次不命中、公共前缀在第三次才命中。
- D5/D6：公告命中 0.1元/$0.014、未命中 1元/$0.14，同页写价格已调整。现行价为 C16–C19。存储免费与旧单价绑在一起；现行定价页未再写存储免费。
- D5 中英数字：flash 命中空闲 0.02元 vs $0.003；pro 0.15元 vs $0.022。未给汇率。高峰窗北京时间与 UTC 差 8 小时，对齐，不作冲突。
- 介质：指南/2024 公告写硬盘、hard disk、disk array。2026-09-10 新闻写 KV Cache「对 SSD 的需求减少到 1/8」（https://api-docs.deepseek.com/zh-cn/news/news260910）。未说明是否取代 API 硬盘缓存。

## gaps
- 「固定 token 间隔」无具体 token 数；不能把 64 当成现行门槛。
- TTL 无整数小时，只有「几个小时到几天」。
- 无删除缓存 API。Responses 未见 miss 字段。Anthropic 页未写 usage 缓存字段。
- 中文调价「2026 年 9 月 10 日 12:00」未写时区。英文页：“New pricing takes effect at 04:00 UTC on Sept 10, 2026.”（https://api-docs.deepseek.com/news/news260910）。

## leads
- V4.1 新闻：KV Cache 相对上一代 SSD 需求为 1/8，是模型体积不是 API TTL。
