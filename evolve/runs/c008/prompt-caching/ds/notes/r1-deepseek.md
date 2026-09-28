# r1-deepseek
question: DeepSeek API 的上下文硬盘缓存（context caching on disk）全部事实。
checked: https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/zh-cn/guides/kv_cache, https://api-docs.deepseek.com/quick_start/pricing, https://api-docs.deepseek.com/quick_start/rate_limit, https://api-docs.deepseek.com/api/create-chat-completion, https://api-docs.deepseek.com/guides/anthropic_api, https://api-docs.deepseek.com/, https://www.deepseek.com/en/news/context-caching/, https://api-docs.deepseek.com/sitemap.xml

## claims
- [C1] D1 自动、无需改代码：context caching on disk 对所有用户默认开启 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "enabled by default for all users, allowing them to benefit without needing to modify their code." | type: official
- [C2] D1 官方公告（2024-08-02）确认无需改代码/接口 | src: https://www.deepseek.com/en/news/context-caching/ | quote: "The disk caching service is now available for all users, requiring no code or interface changes. The cache service runs automatically, and billing is based on actual cache hits." | type: official
- [C3] D2 存储单元 64 tokens，不足不缓存（发布时口径） | src: https://www.deepseek.com/en/news/context-caching/ | quote: "The cache system uses 64 tokens as a storage unit; content less than 64 tokens will not be cached." | type: official
- [C4] D2 现行指南只说按固定 token 间隔切分 cache prefix unit，未给数值 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "the system will carve out cache prefix units at fixed token intervals" | type: official
- [C5] D2 当前在售模型 deepseek-flash（DeepSeek-V4.1-Flash）与 deepseek-v4-pro（DeepSeek-V4-Pro-0813）均有 cache hit/miss 两档输入价，即均支持缓存；缓存命中字段文档化在 POST /chat/completions 的 usage 对象 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "The prices listed below are in units of per 1M tokens." | type: official
- [C6] D3 缓存生命周期：构建秒级，闲置后自动清除，通常几小时到几天 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Cache construction takes seconds. Once the cache is no longer in use, it will be automatically cleared, usually within a few hours to a few days." | type: official
- [C7] D3 公告同口径且补充"不再保留或复用" | src: https://www.deepseek.com/en/news/context-caching/ | quote: "Unused cache entries are automatically cleared after a period, ensuring they are not retained or repurposed." | type: official
- [C8] D4 现价（每 1M tokens，美元）：deepseek-flash 命中 $0.006 峰值/$0.003 低谷 vs 未命中 $0.30/$0.15（命中=1/50）；deepseek-v4-pro 命中 $0.044/$0.022 vs 未命中 $1.32/$0.66（命中=1/30） | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "Off-peak rates are half of the peak rates." | type: official
- [C9] D4 峰谷时段定义 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday, excluding Chinese public holidays." | type: official
- [C10] D4 2024-08 发布时命中价 $0.014/M vs 未命中 $0.14/M（旧模型口径） | src: https://www.deepseek.com/en/news/context-caching/ | quote: "For cache hits, DeepSeek charges $0.014 per million tokens, slashing API costs by up to 90%" | type: official
- [C11] D5 usage 字段 prompt_cache_hit_tokens / prompt_cache_miss_tokens；另有 prompt_tokens_details.cached_tokens 与 hit 相同；prompt_tokens = hit + miss | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Number of tokens in the prompt that hits the context cache." | type: official
- [C12] D6 只认从第 0 个 token 起完全相同的前缀；中段改动不命中 | src: https://www.deepseek.com/en/news/context-caching/ | quote: "only requests with identical prefixes (starting from the 0th token) will be considered duplicates." | type: official
- [C13] D6 SWA 机制下每个缓存前缀是独立完整单元，须完整匹配 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Due to the Sliding Window Attention mechanism, the storage and matching of cached prefixes differs from before. Each cached prefix is an independent, complete unit. A subsequent request can only hit the cache if it fully matches a cache prefix unit." | type: official
- [C14] D6 三种落盘路径：请求边界（用户输入末尾+模型输出末尾各产生一个 unit）、跨请求公共前缀检测、长输入/输出按固定 token 间隔切分 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Each request will produce two cache prefix units at the end position of the user input and the end position of the model output." | type: official
- [C15] D6 缓存只管输入前缀，输出仍实时计算且受 temperature 等影响；命中为 best-effort 不保证 100% | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "The cache system works on a \"best-effort\" basis and does not guarantee a 100% cache hit rate." | type: official
- [C16] D7 无显式缓存管理 API：API reference 仅含 /chat/completions、/completions、/responses、files CRUD、/models、/user/balance；Anthropic 兼容端点中 cache_control 标注 "Ignored" | src: https://api-docs.deepseek.com/sitemap.xml | quote: "create-chat-completion, create-completion, create-response, create-file, delete-file, get-user-balance, list-files, list-models, retrieve-file" | type: official
- [C17] D8 各用户缓存隔离、互相不可见 | src: https://www.deepseek.com/en/news/context-caching/ | quote: "Each user's cache is isolated and logically invisible to others, ensuring data privacy and security." | type: official
- [C18] D8 同账号下可用 user_id 做 KVCache 隔离；格式 [a-zA-Z0-9\-_]+ 最长 512；OpenAI 端放请求体/extra_body，Anthropic 端放 metadata.user_id | src: https://api-docs.deepseek.com/quick_start/rate_limit | quote: "user_id is used to isolate KVCache for users on your business side for privacy management" | type: official

## conflicts
- 命中粒度数值：2024-08-02 公告写 "The cache system uses 64 tokens as a storage unit"；现行指南（引入 SWA 的 cache prefix unit 模型后）只写 "fixed token intervals" 不给数值，并明说存储/匹配方式 "differs from before" — 64 这个数字可能已不适用于当前机制。

## gaps
- 缓存是否覆盖 /responses、/anthropic、/completions(FIM) 各端点：文档未逐端点说明（usage 字段仅确认在 /chat/completions）。
- 现行 "fixed token intervals" 的具体数值未公布。
- 官方 FAQ（static.deepseek.com/faq）为 JS 渲染页，未能抽取内容；缓存隔离原句取自官方新闻页而非 FAQ。

## leads
- https://api-docs.deepseek.com/updates（Change Log）可查 SWA/prefix-unit 机制切换时间点。
- https://api-docs.deepseek.com/news/news0802 为缓存功能上线的 docs 侧公告镜像。
- 第三方实测（user_id 隔离 A/B 探针）: chat-deep.ai/docs/deepseek-user-id-isolation/，可作佐证但非一手。
