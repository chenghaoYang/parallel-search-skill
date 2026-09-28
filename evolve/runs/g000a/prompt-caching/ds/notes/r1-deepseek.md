# r1-deepseek
question: DeepSeek 官方 API 的上下文缓存 / 上下文硬盘缓存是否自动发生、调用方不用改请求？把 D1–D8 用一手原句填满。
checked: https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/zh-cn/guides/kv_cache, https://api-docs.deepseek.com/news/news0802, https://api-docs.deepseek.com/zh-cn/news/news0802, https://api-docs.deepseek.com/updates/, https://api-docs.deepseek.com/quick_start/pricing, https://api-docs.deepseek.com/zh-cn/quick_start/pricing, https://api-docs.deepseek.com/api/create-chat-completion, https://api-docs.deepseek.com/zh-cn/api/create-chat-completion, https://api-docs.deepseek.com/api/create-response, https://api-docs.deepseek.com/quick_start/rate_limit, https://api-docs.deepseek.com/news/news260910

## claims
- [C1] D1 现行中文指南（页未见日期）：默认开启、无需改代码；每个请求都建硬盘缓存。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "默认开启，用户无需修改代码即可享用。用户的每一个请求都会触发硬盘缓存的构建。" | type: official
- [C2] D1 英文指南（页未见日期）：默认开启。 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "enabled by default" | type: official
- [C3] D1 新闻（changelog Date: 2024-08-02）：不改代码、不换接口且自动运行；用户缓存互相不可见。 | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "无需修改代码，无需更换接口，硬盘缓存服务将自动运行。每个用户的缓存是独立的，逻辑上相互不可见" | type: official
- [C6] D2 价格页（页未见日期）OpenAI BASE URL 为 https://api.deepseek.com。 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "BASE URL (OpenAI Format) https://api.deepseek.com" | type: official
- [C7] D2 Chat 为 POST /chat/completions；示例 URL 含该 host。页未见日期。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "curl -L -X POST 'https://api.deepseek.com/chat/completions'" | type: official
- [C8] D2 Responses 为 POST /responses，服务端不存对话，多轮须重送完整 input。页未见日期。 | src: https://api-docs.deepseek.com/api/create-response | quote: "The API is stateless: responses and conversations are not stored on the server." | type: official
- [C9] D2 请求里写明与缓存有关的是 user_id，用于 KVCache 隔离。 | src: https://api-docs.deepseek.com/zh-cn/api/create-chat-completion | quote: "user_id 可用于 KVCache 缓存隔离，以进行隐私管理。" | type: official
- [C10] D2 rate limit（页未见日期）：user_id 做 KVCache 隔离。 | src: https://api-docs.deepseek.com/quick_start/rate_limit | quote: "user_id is used to isolate KVCache for users on your business side for privacy management" | type: official
- [C11] D3 新闻：只有从第 0 个 token 起前缀相同才算重复；中间重复不命中。 | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "从第 0 个 token 开始相同），才算重复。中间开始的重复不能被缓存命中。" | type: official
- [C12] D3 新闻注：存储单位 64 tokens，不足不缓存。 | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "缓存系统以 64 tokens 为一个存储单元，不足 64 tokens 的内容不会被缓存" | type: official
- [C13] D3 现行指南（页未见日期）：因 SWA 与以前不同，须完整匹配缓存前缀单元。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "受 Sliding Window Attention 机制的影响，缓存前缀的存取与判别与之前有所不同。后续请求只有在完整匹配缓存前缀单元时，才能命中缓存。" | type: official
- [C14] D3 每次请求在输入结束与输出结束各产一个缓存前缀单元。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "用户输入结束位置与模型输出结束位置，会产生两个缓存前缀单元。" | type: official
- [C15] D3 第二次请求可完整复用第一次的缓存前缀单元并计为命中。 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "fully reuse the cache prefix unit from the first request, which will count as a \"cache hit.\"" | type: official
- [C16] D3 例二：前两次请求不会命中缓存。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "在上例中，前两次请求不会命中缓存。" | type: official
- [C17] D4 A+C 不能完整匹配 A+B 的缓存前缀单元，故第二轮不命中。 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "A + C does not fully match the first round's cache prefix unit (A + B)." | type: official
- [C18] D4 缓存只匹配输入前缀；输出仍现算并受 temperature 影响。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "硬盘缓存只匹配到用户输入的前缀部分，输出仍然是通过计算推理得到的，仍然受到 temperature 等参数的影响" | type: official
- [C19] D4 尽力而为，不保证 100% 命中。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "缓存系统是“尽力而为”，不保证 100% 缓存命中" | type: official
- [C20] D5 构建为秒级；不用后自动清空，一般为几小时到几天。页未见日期。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "缓存构建耗时为秒级。缓存不再使用后会自动被清空，时间一般为几个小时到几天" | type: official
- [C21] D5 新闻写存储不收费。 | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "缓存占用存储无需付费。" | type: official
- [C22] D5 现行指南仍把命中前提写成写入硬盘缓存。 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "相应前缀已被“落盘”（写入硬盘缓存）。" | type: official
- [C23] D5 现行价格页扣费为 token 消耗量 × 模型单价。页未见日期。 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "扣减费用 = token 消耗量 × 模型单价" | type: official
- [C24] D6 英文价列序 deepseek-flash、deepseek-v4-pro，每 1M tokens。 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "CACHE HIT OFF-PEAK $0.003 $0.022 PEAK $0.006 $0.044 CACHE MISS OFF-PEAK $0.15 $0.66 PEAK $0.3 $1.32" | type: official
- [C25] D6 中文价列序同上，每百万 tokens。 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "缓存命中 空闲时段 0.02元 0.15元 高峰时段 0.04元 0.30元 缓存未命中 空闲时段 1元 4.5元 高峰时段 2元 9.0元" | type: official
- [C26] D6 空闲价为高峰一半；高峰时段见引文。 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "空闲时段价格为高峰时段价格的一半。北京时间周一至周五（不含中国法定节假日）9:00 - 12:00、14:00 - 18:00 为高峰时段" | type: official
- [C27] D6 英文新闻仍写命中 $0.014/百万 tokens，并注明价格已更新。 | src: https://api-docs.deepseek.com/news/news0802 | quote: "For cache hits, DeepSeek charges $0.014 per million tokens. Hint 1: The API price has been updated." | type: official
- [C28] D6 news260910：新价于 2026-09-10 04:00 UTC 生效。 | src: https://api-docs.deepseek.com/news/news260910 | quote: "New pricing takes effect at 04:00 UTC on Sept 10, 2026." | type: official
- [C29] D7 Chat：prompt_tokens 等于 prompt_cache_hit_tokens + prompt_cache_miss_tokens。 | src: https://api-docs.deepseek.com/zh-cn/api/create-chat-completion | quote: "该值等于 prompt_cache_hit_tokens + prompt_cache_miss_tokens" | type: official
- [C30] D7 中文释义：cached_tokens「与 prompt_cache_hit_tokens 相同」；另有 prompt_cache_miss_tokens。 | src: https://api-docs.deepseek.com/zh-cn/api/create-chat-completion | quote: "命中上下文缓存的 token 数。与 prompt_cache_hit_tokens 相同。" | type: official
- [C31] D7 Responses 命中字段为 input_tokens_details.cached_tokens。 | src: https://api-docs.deepseek.com/api/create-response | quote: "Number of input tokens that hit the context cache. See Context Caching." | type: official
- [C32] D8 Chat model 为 deepseek-flash 或 deepseek-v4-pro。 | src: https://api-docs.deepseek.com/zh-cn/api/create-chat-completion | quote: "请使用 deepseek-flash 或 deepseek-v4-pro。" | type: official
- [C33] D8 旧名 deepseek-v4-flash、deepseek-v4-flash-vision-exp 仍可调，由 V4.1-Flash 按 Flash 价服务。 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "旧模型名 deepseek-v4-flash、deepseek-v4-flash-vision-exp 仍可调用，但对应模型已下线，请求将由 DeepSeek-V4.1-Flash 模型提供服务，并按 Flash 价格计费。" | type: official
- [C34] D8 changelog Date: 2026-04-24：deepseek-chat 与 deepseek-reasoner 将于 2026-07-24 停用。 | src: https://api-docs.deepseek.com/updates/ | quote: "deepseek-chat and deepseek-reasoner, will be discontinued in three months (2026-07-24)." | type: official

## conflicts
- 粒度：新闻 64 tokens 且从第 0 token 相同即重复（https://api-docs.deepseek.com/zh-cn/news/news0802 「不足 64 tokens 的内容不会被缓存」）。现行指南须完整匹配缓存前缀单元且「与之前有所不同」（https://api-docs.deepseek.com/zh-cn/guides/kv_cache ）。不裁。无第二产品名「自动前缀缓存」。
- 单价：新闻命中 $0.014 / 0.1元、未命中 $0.14 / 1元每百万，同页写价格已更新（https://api-docs.deepseek.com/news/news0802 ）。现行页为 C24–C26。不裁。
- 存储费：新闻「缓存占用存储无需付费。」现行价只有「扣减费用 = token 消耗量 × 模型单价」，无存储行。不裁。
- v4-pro 2026-09-14 后：https://api-docs.deepseek.com/news/news260910 「route to V4.1-Flash at V4.1-Flash rates」vs https://api-docs.deepseek.com/updates/ 「continue providing API services for DeepSeek V4 Pro after September 14, 2026, with the billing method remaining unchanged.」价格页仍单列 Pro。不裁。

## gaps
- 现行指南写「以一定的 token 数量为间隔」但未给数字，也未重申 64。未写换模型或改一字是否失效。
- schema 无「没有缓存开关」原句；已列字段无 cache/cache_control。
- 2026-07-24 后 deepseek-chat/reasoner 是否仍受理，现行模型表未写。现行价无按小时存储费。未打开 Anthropic cache usage。

## leads
- FIM https://api-docs.deepseek.com/api/create-completion 的 prompt_cache_* 未 web_fetch。
- https://api.deepseek.com/anthropic 的 cache usage 未打开。news260910 新价在图里。
