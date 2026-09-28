# r1-deepseek
question: DeepSeek API 的 context caching（硬盘缓存，Context Caching on Disk）现状（截至 2026-09）：机制/门槛/计费/TTL/命中确认/失效条件/模型范围
checked: https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/zh-cn/guides/kv_cache, https://api-docs.deepseek.com/quick_start/pricing, https://api-docs.deepseek.com/api/create-chat-completion, https://api-docs.deepseek.com/updates, https://api-docs.deepseek.com/news/news260910, https://api-docs.deepseek.com/news/news260424, https://api-docs.deepseek.com/news/news0802, https://api-docs.deepseek.com/news/news251201, https://api-docs.deepseek.com/news/news250929, https://api-docs.deepseek.com/news/news250821, https://api-docs.deepseek.com/quick_start/token_usage, https://api-docs.deepseek.com/img/v3_2_price_en.jpeg, https://api-docs.deepseek.com/img/v4-price-en.png

## claims
- [C1] 缓存全自动，默认开启，无需任何参数/代码改动 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "enabled by default for all users, allowing them to benefit without needing to modify their code" | type: official
- [C2] 「on disk」官方描述：缓存在分布式磁盘阵列上，重复部分直接拉取不重算 | src: https://api-docs.deepseek.com/news/news0802 | quote: "implemented Context Caching on Disk technology," which "caches content that is expected to be reused on a distributed disk array"; "the repeated parts are retrieved from the cache, bypassing the need for recomputation" | type: official
- [C3] 现行指南页标题即 "Context Caching on Disk"；长输入/输出按固定 token 间隔切单元落盘 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "the system will carve out cache prefix units at fixed token intervals" | type: official
- [C4] 最小缓存单元 64 tokens（2024 上线公告；现行指南页未再写数值） | src: https://api-docs.deepseek.com/news/news0802 | quote: "The cache system uses 64 tokens as a storage unit; content less than 64 tokens will not be cached." | type: official
- [C5] 命中要求从第 0 个 token 起前缀完全一致，中段部分匹配不命中 | src: https://api-docs.deepseek.com/news/news0802 | quote: "only requests with identical prefixes (starting from the 0th token) will be considered duplicates"; "Partial matches in the middle of the input will not trigger a cache hit." | type: official
- [C6] 现行指南：命中单位是「cache prefix unit」，须完整匹配；每个请求在 user input 末尾和 model output 末尾各产生一个单元；跨请求公共前缀也会持久化为独立单元 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "A subsequent request can only hit the cache if it fully matches a cache prefix unit." / "Each request will produce two cache prefix units" | type: official
- [C7] 现行价格（USD/1M tokens，peak/off-peak）：deepseek-flash hit $0.006/$0.003、miss $0.30/$0.15、output $1.20/$0.60；deepseek-v4-pro hit $0.044/$0.022、miss $1.32/$0.66、output $3.96/$1.98 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "Off-peak rates are half of the peak rates."（表格数字见正文） | type: official
- [C8] peak 时段定义 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday, excluding Chinese public holidays." | type: official
- [C9] deepseek-chat/deepseek-reasoner 已于 2026-07-24 15:59 UTC 彻底下线，此前（2026-04-24 起）路由至 deepseek-v4-flash 的 non-thinking/thinking | src: https://api-docs.deepseek.com/news/news260424 | quote: "deepseek-chat & deepseek-reasoner will be fully retired and inaccessible after Jul 24th, 2026, 15:59 (UTC Time)." "(Currently routing to deepseek-v4-flash non-thinking/thinking)." | type: official
- [C10] chat/reasoner 退役前最后可考价格（V3.2-Exp 定价，2025-09-29 起，两名同价）：hit $0.028、miss $0.28、output $0.42 /1M（原 $0.07/$0.56/$1.68） | src: https://api-docs.deepseek.com/img/v3_2_price_en.jpeg（news250929 页内价格图，已读图） | quote: 表格 "INPUT (CACHE HIT) $0.028 / INPUT (CACHE MISS) $0.28 / OUTPUT $0.42" | type: official
- [C11] 2024 上线价：hit $0.014、miss $0.14 /1M，缓存存储免费 | src: https://api-docs.deepseek.com/news/news0802 | quote: "$0.014 per million tokens," "slashing API costs by up to 90%"; "storage usage for the cache is free" | type: official
- [C12] TTL：不用即清，一般几小时到几天；best-effort 不保证命中 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Once the cache is no longer in use, it will be automatically cleared, usually within a few hours to a few days." / "The cache system works on a 'best-effort' basis and does not guarantee a 100% cache hit rate."（zh: "缓存不再使用后会自动被清空，时间一般为几个小时到几天"） | type: official
- [C13] usage 字段：prompt_cache_hit_tokens / prompt_cache_miss_tokens 均必填返回；prompt_tokens = hit + miss；另有 prompt_tokens_details.cached_tokens 等于 hit | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Number of tokens in the prompt that hits the context cache." / "It equals prompt_cache_hit_tokens + prompt_cache_miss_tokens." / "Same as `prompt_cache_hit_tokens`." | type: official
- [C14] 失效条件：前缀任何改动即 miss。例：首轮 A+B 产生单元后，A+C 不命中（未完整匹配 A+B 单元），但 A 会持久化供后续命中；输出仍实时推理，temperature 等照常生效 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "because `A + C` does not fully match the first round's cache prefix unit (`A + B`)" / "The output is still generated through computation and inference" | type: official
- [C15] 现行 model 枚举只有 deepseek-flash（DeepSeek-V4.1-Flash）和 deepseek-v4-pro（DeepSeek-V4-Pro-0813）；旧名 deepseek-v4-flash/-vision-exp 仍接受但由 V4.1-Flash 服务按 Flash 价计费 | src: https://api-docs.deepseek.com/api/create-chat-completion + /quick_start/pricing | quote: "ID of the model to use. Use deepseek-flash or deepseek-v4-pro." / "The legacy names deepseek-v4-flash and deepseek-v4-flash-vision-exp are still accepted" | type: official
- [C16] 2026-09-14 04:00 UTC 起所有 deepseek-v4-pro 请求路由到 V4.1-Flash、按 Flash 价计费，直至 V4.1-Pro 上线 | src: https://api-docs.deepseek.com/news/news260910 | quote: "all `deepseek-v4-pro` requests will route to V4.1-Flash at V4.1-Flash rates." "This will continue until V4.1-Pro launches." | type: official
- [C17] 新架构仍在用盘缓存：V4.1-Flash KV cache 只需上代 1/4 HBM、1/8 SSD | src: https://api-docs.deepseek.com/news/news260910 | quote: "1/4 the HBM" "1/8 the SSD storage" | type: official
- [C18] 功能上线时间 2024-08-02（changelog 唯一缓存条目），此后无缓存机制变更记录 | src: https://api-docs.deepseek.com/updates | quote: "The DeepSeek API has innovatively adopted hard disk caching, reducing prices by another order of magnitude." | type: official
- [C19] V4 上线时（2026-04）定价图：v4-pro hit $0.145/miss $1.74/out $3.48；v4-flash hit $0.028/miss $0.14/out $0.28，1M context | src: https://api-docs.deepseek.com/img/v4-price-en.png（news260424 页内价格图，已读图） | quote: 表格 "$0.145 / $1.74 / $3.48" 与 "$0.028 / $0.14 / $0.28" | type: official

## conflicts
- 定价页仍列 deepseek-v4-pro 自有价格（miss $1.32 peak），但 news260910 称 9/14 起 v4-pro 请求全部路由到 V4.1-Flash「at V4.1-Flash rates」——同一 model 名两处隐含价格不一致。
- 64-token 单元只见于 2024 上线公告；现行 kv_cache 指南只说 "fixed token intervals" 不给数值——属文档漂移，未必是机制变更。

## gaps
- 64-token 粒度在 V4 架构下是否仍成立：现行指南/zh 页均无数值，未再确认。
- V3.2（2025-12）至 2026-04 间 chat/reasoner 是否沿用 $0.028/$0.28/$0.42：news251201 价格也在图里（未读该图），正文仅 "Same pricing as V3.2"（指 Speciale）。
- 「fixed token intervals」具体间隔值官方未写。
- TTL 只有「几小时到几天」区间，无精确值；无保活承诺。

## leads
- FAQ（https://static.deepseek.com/faq/index.html?lang=en#/category/4）未查，可能有缓存细节。
- Anthropic 兼容端点（api.deepseek.com/anthropic）是否同样返回 cache 字段未查。
