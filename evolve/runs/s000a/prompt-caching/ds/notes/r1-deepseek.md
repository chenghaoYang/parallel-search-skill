# r1-deepseek
question: DeepSeek 官方 API 的上下文缓存（硬盘/KV cache）是否自动发生、要不要改请求；缓存介质、门槛、寿命、命中/未命中计费、命中观测字段、失效条件、适用模型。
checked: https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/zh-cn/guides/kv_cache, https://api-docs.deepseek.com/quick_start/pricing, https://api-docs.deepseek.com/zh-cn/quick_start/pricing, https://api-docs.deepseek.com/news/news0802, https://api-docs.deepseek.com/zh-cn/news/news0802, https://api-docs.deepseek.com/api/create-chat-completion, https://api-docs.deepseek.com/quick_start/rate_limit, https://api-docs.deepseek.com/guides/responses_api

## claims
- [C1] D1 触发：上下文硬盘缓存对所有用户默认开启，无需改代码 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "The DeepSeek API Context Caching on Disk Technology is enabled by default for all users, allowing them to benefit without needing to modify their code." | type: official
- [C2] D1 中文页同义表述 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "DeepSeek API 上下文硬盘缓存技术对所有用户默认开启，用户无需修改代码即可享用。" | type: official
- [C3] D1 无请求级开关：Responses API 明确不支持 prompt_cache_key / prompt_cache_retention，缓存全自动管理 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Not supported. Context caching is managed automatically, see Context Caching" | type: official
- [C4] D1 Chat Completions 请求体 schema 无任何缓存开关字段；唯一与缓存相关的请求参数是 user_id（用于隔离） | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "user_id can be used for KVCache isolation for privacy management." | type: official
- [C5] D2 介质：硬盘；官方英文新闻称缓存在分布式磁盘阵列 | src: https://api-docs.deepseek.com/news/news0802 | quote: "caches content that is expected to be reused on a distributed disk array" | type: official
- [C6] D2 中文页：分布式硬盘阵列 | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "把预计未来会重复使用的内容，缓存在分布式的硬盘阵列中" | type: official
- [C7] D2/D7 命中边界：只认从第 0 个 token 开始的相同前缀，中间重复不命中；前缀改动即失效 | src: https://api-docs.deepseek.com/news/news0802 | quote: "only requests with identical prefixes (starting from the 0th token) will be considered duplicates. Partial matches in the middle of the input will not trigger a cache hit." | type: official
- [C8] D2 命中需完整匹配已落盘的"缓存前缀单元"；落盘时机三种：请求结束位置（输入/输出末尾各一单元）、检测到公共前缀、按固定 token 间隔截取 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "A subsequent request can only hit the cache if it fully matches a cache prefix unit." | type: official
- [C9] D3 门槛：64 tokens 为一个存储单元，不足 64 tokens 不缓存 | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "缓存系统以 64 tokens 为一个存储单元，不足 64 tokens 的内容不会被缓存" | type: official
- [C10] D4 寿命：不再使用后自动清空，一般几小时到几天；构建秒级；尽力而为不保证 100% 命中 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Cache construction takes seconds. Once the cache is no longer in use, it will be automatically cleared, usually within a few hours to a few days." | type: official
- [C11] D4 "硬盘"字样仍出现在当前官方页（标题 Context Caching on Disk / 上下文硬盘缓存；正文 hard disk cache / 硬盘缓存） | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Each user request will trigger the construction of a hard disk cache." | type: official
- [C12] D5 当前美元价（每 1M tokens）：deepseek-flash 命中 $0.003(闲)/$0.006(峰)，未命中 $0.15/$0.3；deepseek-v4-pro 命中 $0.022/$0.044，未命中 $0.66/$1.32 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "Off-peak rates are half of the peak rates." | type: official
- [C13] D5 当前人民币价（每百万 tokens）：flash 命中 0.02元(闲)/0.04元(峰)，未命中 1元/2元；v4-pro 命中 0.15元/0.30元，未命中 4.5元/9.0元 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "空闲时段价格为高峰时段价格的一半。" | type: official
- [C14] D5 峰谷时段：英 UTC 01:00-04:00、06:00-10:00 周一至五为高峰；中 北京时间周一至五 9:00-12:00、14:00-18:00 高峰（两版等价） | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "北京时间周一至周五（不含中国法定节假日）9:00 - 12:00、14:00 - 18:00 为高峰时段" | type: official
- [C15] D6 命中观测：usage.prompt_cache_hit_tokens / prompt_cache_miss_tokens | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "prompt_cache_hit_tokens: The number of tokens in the input of this request that resulted in a cache hit." | type: official
- [C16] D6 schema 细节：usage.prompt_tokens_details.cached_tokens 等于 hit；prompt_tokens = hit + miss | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Number of tokens in the prompt that hit the context cache. Same as `prompt_cache_hit_tokens`." | type: official
- [C17] D6 Responses API 中命中数为 usage.input_tokens_details.cached_tokens | src: https://api-docs.deepseek.com/guides/responses_api | quote: "input_tokens_details.cached_tokens is the number of tokens hitting the context cache" | type: official
- [C18] D7 缓存只匹配输入前缀，输出仍实时推理生成、受 temperature 等影响 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "The hard disk cache only matches the prefix part of the user's input. The output is still generated through computation and inference, and it is influenced by parameters such as temperature" | type: official
- [C19] D7 隔离即失效维度：每用户缓存独立；传不同 user_id 走不同 KVCache 命名空间 | src: https://api-docs.deepseek.com/quick_start/rate_limit | quote: "KVCache Isolation: `user_id` is used to isolate KVCache for users on your business side for privacy management" | type: official
- [C20] D8 范围：服务对所有用户开放；当前 model 枚举为 deepseek-flash、deepseek-v4-pro，定价页两者均有命中/未命中输入价行 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Possible values: [`deepseek-flash`, `deepseek-v4-pro`]" | type: official
- [C21] D8 新闻表述为全量上线 | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "硬盘缓存服务已经全面上线，用户无需修改代码，无需更换接口，硬盘缓存服务将自动运行" | type: official
- [C22] 版本/日期：定价页标 MODEL VERSION DeepSeek-V4.1-Flash 与 DeepSeek-V4-Pro-0813；各页面均无可见"最后更新"日期 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "DeepSeek-V4.1-Flash DeepSeek-V4-Pro-0813" | type: official

## conflicts
- 命中单价跨版本不一致：news0802（上线公告）写命中 $0.014/百万 tokens、未命中 $0.14（中文页 0.1元/1元），quote: "For cache hits, DeepSeek charges $0.014 per million tokens"（https://api-docs.deepseek.com/news/news0802）；当前 pricing 页 flash 命中 $0.003–$0.006、未命中 $0.15–$0.30（https://api-docs.deepseek.com/quick_start/pricing）。news0802 自身注明 "The API price has been updated. For details, please refer to Models & Pricing"，属旧价而非真冲突。

## gaps
- 无固定 TTL 小时数或"永久"承诺；官方只给"几个小时到几天"自动清空 + best-effort，且 prompt_cache_retention 不支持（无请求级留存控制）。
- kv_cache 指南未逐模型列举适用范围；旧模型名 deepseek-chat / deepseek-reasoner 是否仍享缓存未说明（当前枚举只剩 flash / v4-pro）。
- Anthropic 格式端点（https://api.deepseek.com/anthropic）响应中缓存命中字段名未在已取页面确认。
- 指南/定价/新闻页均无可见更新日期，仅模型版本号含日期（0813）。

## leads
- user_id 可按业务侧终端用户做 KVCache 隔离（隐私 + 调度隔离），rate_limit 页有 OpenAI/Anthropic SDK 用法。
- news0802 称 DeepSeek 可能是全球首家大范围用硬盘缓存的厂商，依托 MLA 压缩 KV cache 落低成本硬盘。
- 闲时半价 + 命中价叠加是成本模型要点；Responses API/Anthropic API 均为同一自动缓存。
