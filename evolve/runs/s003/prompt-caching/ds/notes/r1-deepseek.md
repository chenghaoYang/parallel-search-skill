# r1-deepseek
question: DeepSeek 官方 API 的上下文缓存 / 硬盘缓存现在是否自动生效、怎么计费、能活多久、用哪个字段确认命中、什么改动会失效。
checked: https://api-docs.deepseek.com/zh-cn/guides/kv_cache, https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/zh-cn/quick_start/pricing, https://api-docs.deepseek.com/quick_start/pricing, https://api-docs.deepseek.com/zh-cn/news/news0802, https://api-docs.deepseek.com/news/news0802, https://api-docs.deepseek.com/api/create-chat-completion, https://api-docs.deepseek.com/quick_start/rate_limit, https://api-docs.deepseek.com/guides/anthropic_api

## claims
- [C1] D1：缓存对所有用户默认开启、无需改代码，现行指南仍如此表述 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "DeepSeek API 上下文硬盘缓存技术对所有用户默认开启，用户无需修改代码即可享用。" | type: official
- [C2] D1：英文指南同义表述 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "The DeepSeek API Context Caching on Disk Technology is enabled by default for all users, allowing them to benefit without needing to modify their code." | type: official
- [C3] D1/D4：每个请求自动触发缓存构建并按实际命中计费（2024-08 公告） | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "用户的每一个请求都会触发硬盘缓存的构建……硬盘缓存服务将自动运行，系统自动按照实际命中情况计费。" | type: official
- [C4] D1：不存在需传参的手动缓存——Anthropic 兼容端点中 tools/text/tool_use/tool_result 的 cache_control 全部标记 Ignored | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "cache_control | Ignored" | type: official
- [C5] D2：官方术语为「上下文硬盘缓存 / Context Caching on Disk」，缓存介质是分布式硬盘阵列 | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "把预计未来会重复使用的内容，缓存在分布式的硬盘阵列中。" | type: official
- [C6] D2/D3：现行指南的缓存单位是「缓存前缀单元」，命中需完整匹配该单元（SWA 机制下与旧机制不同） | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "受 Sliding Window Attention 机制的影响，缓存前缀的存取与判别与之前有所不同。每条缓存前缀是一个独立的完整单元。后续请求只有在完整匹配**缓存前缀单元**时，才能命中缓存。" | type: official
- [C7] D3：前缀单元落盘时机之一：用户输入结束位置与模型输出结束位置各产生一个单元 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "每次请求的**用户输入结束位置**与**模型输出结束位置**，会产生两个**缓存前缀单元**。" | type: official
- [C8] D3：落盘时机之二/三：跨请求公共前缀检测落盘；长输入输出按固定 token 间隔截取单元 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "当系统检测到多次请求之间存在公共前缀时，会将该公共前缀作为一个独立的**缓存前缀单元**进行落盘。" | type: official
- [C9] D3/D7：只有从第 0 个 token 开始相同的前缀才算重复，中间开始的重复不能命中 | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "只有当两个请求的前缀内容相同时（从第 0 个 token 开始相同），才算重复。中间开始的重复不能被缓存命中。" | type: official
- [C10] D3：2024-08 公告给出最小单元 64 tokens，不足不缓存（现行指南未复述此数字） | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "缓存系统以 64 tokens 为一个存储单元，不足 64 tokens 的内容不会被缓存" | type: official
- [C11] D4：deepseek-flash 输入缓存命中 空闲 0.02 元/高峰 0.04 元，未命中 空闲 1 元/高峰 2 元（每百万 tokens，人民币） | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "百万tokens输入（缓存命中）空闲时段 0.02元……高峰时段 0.04元……百万tokens输入（缓存未命中）空闲时段 1元……高峰时段 2元" | type: official
- [C12] D4：deepseek-v4-pro 输入缓存命中 空闲 0.15 元/高峰 0.30 元，未命中 空闲 4.5 元/高峰 9.0 元（每百万 tokens，人民币） | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "百万tokens输入（缓存命中）空闲时段 ……0.15元 高峰时段 ……0.30元 百万tokens输入（缓存未命中）空闲时段 ……4.5元 高峰时段 ……9.0元" | type: official
- [C13] D4：英文价目（USD/1M）：flash 命中 $0.003–0.006、未命中 $0.15–0.3；v4-pro 命中 $0.022–0.044、未命中 $0.66–1.32 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "1M INPUT TOKENS (CACHE HIT) OFF-PEAK $0.003 $0.022 PEAK $0.006 $0.044 1M INPUT TOKENS (CACHE MISS) OFF-PEAK $0.15 $0.66 PEAK $0.3 $1.32" | type: official
- [C14] D4：高峰=北京时间周一至周五 9:00-12:00、14:00-18:00（不含法定节假日），空闲半价；输出无缓存价 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "空闲时段价格为高峰时段价格的一半。北京时间周一至周五（不含中国法定节假日）9:00 - 12:00、14:00 - 18:00 为高峰时段" | type: official
- [C15] D5：官方只给模糊 TTL——不用后自动清空，几小时到几天；构建耗时秒级 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "缓存构建耗时为秒级。缓存不再使用后会自动被清空，时间一般为几个小时到几天" | type: official
- [C16] D5：英文版同义 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Once the cache is no longer in use, it will be automatically cleared, usually within a few hours to a few days." | type: official
- [C17] D6：命中观测字段 usage.prompt_cache_hit_tokens / prompt_cache_miss_tokens | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "prompt_cache_hit_tokens：本次请求的输入中，缓存命中的 tokens 数；prompt_cache_miss_tokens：本次请求的输入中，缓存未命中的 tokens 数" | type: official
- [C18] D6：API reference 另给出 usage.prompt_tokens_details.cached_tokens，与 hit 字段同值；prompt_tokens = hit + miss | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "cached_tokens integer Number of tokens in the prompt that hit the context cache. Same as `prompt_cache_hit_tokens`." | type: official
- [C19] D7：缓存仅匹配输入前缀，输出仍实时推理，temperature 等仍引入随机性 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "硬盘缓存只匹配到用户输入的前缀部分，输出仍然是通过计算推理得到的，仍然受到 temperature 等参数的影响" | type: official
- [C20] D7：缓存是尽力而为，不保证 100% 命中 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "The cache system works on a "best-effort" basis and does not guarantee a 100% cache hit rate." | type: official
- [C21] D8：账号间缓存隔离（2024-08 公告） | src: https://api-docs.deepseek.com/zh-cn/news/news0802 | quote: "每个用户的缓存是独立的，逻辑上相互不可见，从底层确保用户数据的安全和隐私。" | type: official
- [C22] D8：现行文档新增 user_id 级 KVCache 隔离——同账号不同 user_id 的缓存互相隔离 | src: https://api-docs.deepseek.com/quick_start/rate_limit | quote: "KVCache Isolation: `user_id` is used to isolate KVCache for users on your business side for privacy management" | type: official
- [C23] D8：价格页对 deepseek-flash 与 deepseek-v4-pro 均列缓存命中/未命中价，即两模型都覆盖；chat API 模型枚举仅这两个 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Possible values: [`deepseek-flash`, `deepseek-v4-pro`]" | type: official

## conflicts
- 缓存单价：news0802（2024-08）写 "缓存命中的部分，DeepSeek 收费 0.1元 每百万 tokens"（英文 "$0.014 per million tokens"），现行价格页 flash 命中已是 0.02–0.04 元 / $0.003–0.006。公告自带脚注 "API 价格已做调整，最新价格请参考模型 & 价格页面"，属过时而非矛盾。
- 最小缓存单位：news0802 注 1 说 "缓存系统以 64 tokens 为一个存储单元"；现行 kv_cache 指南改用 "缓存前缀单元" + 三种落盘时机表述，全页无 64 tokens 字样，并明说 SWA 使 "缓存前缀的存取与判别与之前有所不同"。64-token 规则是否仍生效，官方未明确。
- news0802 称 "对所有用户均不限流、不限并发"，现行 rate_limit 页写明 flash 2500 / v4-pro 500 并发上限——佐证公告整体过时，引用其缓存细节需留意。

## gaps
- 现行指南未给最小可缓存长度数字；64 tokens 仅见 2024-08 公告（已通读 https://api-docs.deepseek.com/zh-cn/guides/kv_cache 与英文版全页确认无该字样）。
- 未逐端点说明缓存覆盖：Responses API、FIM、Anthropic 格式端点是否同样自动命中/计费，文档未写（仅 chat completions 的 usage 字段有 API reference 佐证）。
- 无精确 TTL，只有 "几个小时到几天"；模型版本升级是否清缓存、命中是否区分 thinking/non-thinking，均无说明。
- 中文/英文 kv_cache 指南均无页面日期或版本号，无法确认最近更新时间。

## leads
- user_id 参数会切分 KVCache 命名空间（rate_limit 页），多租户 SaaS 传不同 user_id 会降低跨租户命中率——可深挖。
- news0802 多处过时（价格、不限并发），引用需与现行页交叉核对。
- 128K 高重复输入首 token 延迟 13s→500ms（news0802 实测数字），可作收益佐证。
