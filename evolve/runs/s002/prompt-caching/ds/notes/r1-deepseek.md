# r1-deepseek
question: DeepSeek API 的上下文硬盘缓存 / context caching 是否自动发生、要不要改代码；命中与未命中怎么计价；缓存能保留多久；响应里哪个字段证明命中；什么改动会失效。
checked: https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/zh-cn/guides/kv_cache, https://api-docs.deepseek.com/quick_start/pricing, https://api-docs.deepseek.com/zh-cn/quick_start/pricing, https://api-docs.deepseek.com/news/news0802, https://api-docs.deepseek.com/api/create-chat-completion, https://api-docs.deepseek.com/guides/anthropic_api

## claims
- [C1] D1：硬盘缓存对所有用户默认开启，无需修改代码 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "The DeepSeek API Context Caching on Disk Technology is enabled by default for all users, allowing them to benefit without needing to modify their code." | type: official
- [C2] D1：每请求自动触发硬盘缓存构建，按实际命中计费；无需代码或接口变更 | src: https://api-docs.deepseek.com/news/news0802 | quote: "The disk caching service is now available for all users, requiring no code or interface changes. The cache service runs automatically, and billing is based on actual cache hits." | type: official
- [C3] D1 反证：Anthropic 格式请求里的 cache_control 字段被 Ignored（tools/text/tool_use/tool_result 同），不存在需手动开的缓存开关 | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "| cache_control | Ignored |" | type: official
- [C4] D1：chat/completions 请求体中唯一涉缓存的参数是可选 user_id，仅用于隔离而非开启 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "user_id can be used for KVCache isolation for privacy management." | type: official
- [C5] D2：命中键是从第 0 个 token 开始的输入前缀；中间重复不命中 | src: https://api-docs.deepseek.com/news/news0802 | quote: "only requests with identical prefixes (starting from the 0th token) will be considered duplicates. Partial matches in the middle of the input will not trigger a cache hit." | type: official
- [C6] D2：缓存单元为独立完整的「缓存前缀单元」，须完整匹配该单元才命中（受 Sliding Window Attention 影响） | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "每条缓存前缀是一个独立的完整单元。后续请求只有在完整匹配缓存前缀单元时，才能命中缓存。" | type: official
- [C7] D2：落盘时机三种——请求结束位置（用户输入结束+模型输出结束各一单元）、公共前缀检测、长输入/输出按固定 token 间隔截取 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Persistence at request boundaries... Common prefix detection persistence... Persistence at fixed token intervals" | type: official
- [C8] D2：缓存只匹配输入前缀；输出仍实时推理，受 temperature 等参数影响有随机性 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "The hard disk cache only matches the prefix part of the user's input." | type: official
- [C9] D3：最小单元 64 tokens，不足不缓存 | src: https://api-docs.deepseek.com/news/news0802 | quote: "The cache system uses 64 tokens as a storage unit; content less than 64 tokens will not be cached." | type: official
- [C10] D4：无固定 TTL；不再使用后自动清空，通常几小时到几天；构建耗时秒级 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Cache construction takes seconds. Once the cache is no longer in use, it will be automatically cleared, usually within a few hours to a few days." | type: official
- [C11] D5：deepseek-flash（DeepSeek-V4.1-Flash）USD 输入价：命中 $0.003 空闲/$0.006 高峰每 1M；未命中 $0.15/$0.30；输出 $0.6/$1.2 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "1M INPUT TOKENS (CACHE HIT) OFF-PEAK $0.003 $0.022 PEAK $0.006 $0.044" | type: official
- [C12] D5：deepseek-v4-pro（DeepSeek-V4-Pro-0813）USD 输入价：命中 $0.022/$0.044；未命中 $0.66/$1.32；输出 $1.98/$3.96 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "1M INPUT TOKENS (CACHE MISS) OFF-PEAK $0.15 $0.66 PEAK $0.3 $1.32" | type: official
- [C13] D5：中文页 CNY 价：flash 命中 0.02元/0.04元、未命中 1元/2元；v4-pro 命中 0.15元/0.30元、未命中 4.5元/9.0元 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "空闲时段 0.02元 0.15元 高峰时段 0.04元 0.30元" | type: official
- [C14] D5：高峰为 UTC 01:00-04:00 与 06:00-10:00 周一至周五（不含中国法定节假日），空闲价为高峰一半 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday, excluding Chinese public holidays." | type: official
- [C15] D5：无单独 cache write 溢价/存储费 | src: https://api-docs.deepseek.com/news/news0802 | quote: "The service has no additional fees beyond the $0.014 per million tokens for cache hits, and storage usage for the cache is free." | type: official
- [C16] D6：usage 新增 prompt_cache_hit_tokens 与 prompt_cache_miss_tokens | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "prompt_cache_hit_tokens：本次请求的输入中，缓存命中的 tokens 数" | type: official
- [C17] D6：另有 usage.prompt_tokens_details.cached_tokens（等价 hit 数）；prompt_tokens = hit + miss | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "cached_tokens integer Number of tokens in the prompt that hit the context cache. Same as prompt_cache_hit_tokens." | type: official
- [C18] D8：多轮对话第二轮 = 相同 system + 首轮 user + assistant 回复 + 新 user，可完整复用首轮缓存单元 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "the second request can fully reuse the cache prefix unit from the first request, which will count as a 'cache hit.'" | type: official
- [C19] D7：A+B 后接 A+C 不命中；系统把公共前缀 A 落盘后，第三轮 A+D 才命中 A | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "第二轮请求无法命中缓存，因为 A + C 不能完整匹配第一轮的缓存前缀单元（A + B）。" | type: official
- [C20] D9：缓存为尽力而为，不保证 100% 命中 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "The cache system works on a \"best-effort\" basis and does not guarantee a 100% cache hit rate." | type: official
- [C21] D9：当前模型仅 deepseek-flash 与 deepseek-v4-pro，定价表两者均有命中/未命中档 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Possible values: [deepseek-flash, deepseek-v4-pro]" | type: official

## conflicts
- 公告 news0802（2024-08）引旧价命中 $0.014/M、未命中 $0.14/M，与现价不符；该页自注 "The API price has been updated. For details, please refer to Models & Pricing"，应以定价页为准。
- USD 与 CNY 价非精确汇率换算（flash miss $0.15 vs 1元），系两币种各自官方价，照抄未换算。
- 简报所列 deepseek-chat / deepseek-reasoner 当前文档已无踪影，枚举只有 deepseek-flash / deepseek-v4-pro；旧名是否仍接受未写明。

## gaps
- 无显式 TTL 小时数/配置项；仅「不再使用后几小时到几天自动清空」（kv_cache 中英页、news0802 均无精确时长）。
- 无失效条件清单小节；可确认失效路径：前缀不完整匹配、<64 tokens、闲置清除、user_id 隔离；无 flush API。
- Responses API 对应字段名未在一手页核实；文档页未显示更新日期。

## leads
- user_id 做 KVCache 隔离会拉低跨终端用户命中率，是调优点。
- 官方称 128K 高重复输入首 token 延迟 13s→500ms；不优化平均省 50%+。
