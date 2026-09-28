# r1-deepseek
question: DeepSeek API 的「上下文硬盘缓存」（Context Caching on Disk）现在的机制是什么？
checked: https://api-docs.deepseek.com/guides/kv_cache/,https://api-docs.deepseek.com/news/news0802/,https://api-docs.deepseek.com/quick_start/pricing/,https://api-docs.deepseek.com/api/create-chat-completion/,https://api-docs.deepseek.com/quick_start/rate_limit/,https://api-docs.deepseek.com/updates/

## claims
- [C1] trigger: 自动启用，无需代码改动 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "The caching mechanism automatically activates without requiring code modifications." | type: official
- [C2] min_len: 最小缓存长度为 64 tokens，更短内容不被缓存 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "The cache system uses 64 tokens as a storage unit; content less than 64 tokens will not be cached." | type: official
- [C3] discount (价格方案1-旧): cache hit 价格 $0.014/百万 tokens，相对 cache miss（约 $0.14/百万）打 1 折 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "For cache hits, DeepSeek charges $0.014 per million tokens, slashing API costs by up to 90%." | date: 2024-08-02 | type: official
- [C4] discount (价格方案2-新): Flash model cache hit $0.003–0.006/百万 tokens，cache miss $0.15–0.3/百万；V4-Pro cache hit $0.022–0.044/百万，cache miss $0.66–1.32/百万 | src: https://api-docs.deepseek.com/quick_start/pricing/ | quote: "Cache hit input: $0.003–$0.006... Cache miss input: $0.15–$0.3... Cache hit input: $0.022–$0.044... Cache miss input: $0.66–$1.32" | date: 2026 | type: official
- [C5] discount: 无单独的缓存"写入"费用，缓存构建成本已含在整体定价中 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "cache construction... Cache hit occurs when... fully matches a previously persisted cache prefix unit" | type: official
- [C6] ttl: 缓存未使用时自动清除，官方未给具体时长，仅说"hours to days" | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "cached data is automatically cleared within hours to days of disuse" | type: official
- [C7] ttl: 不保证缓存持久性，运行在"best-effort"基础上 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "operates on a best-effort basis without guaranteeing 100% cache hits" | type: official
- [C8] storage: 硬盘而非内存的原因——MLA 架构显著减小 KV cache 大小，使其可存储在低成本硬盘上 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "significantly reduces the size of the context KV cache, making it feasible to store cached content on affordable disk hardware rather than expensive GPU memory" | type: official
- [C9] storage: DeepSeek 声称是全球首个在 API 服务中实现大规模硬盘缓存的大语言模型提供商 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "the first large language model provider globally to implement extensive disk caching in API services" | type: official
- [C10] confirm: response usage 对象包含两个字段跟踪缓存命中：prompt_cache_hit_tokens 和 prompt_cache_miss_tokens | src: https://api-docs.deepseek.com/api/create-chat-completion/ | quote: "prompt_cache_hit_tokens: tokens from input that hit the cache... prompt_cache_miss_tokens: tokens that didn't hit the cache" | type: official
- [C11] invalidate: 缓存命中基于完全前缀匹配，部分匹配不触发缓存，暗示前缀任何改动都会失效 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "A cache hit occurs only when a subsequent request fully matches a previously persisted cache prefix unit" | type: official
- [C12] invalidate: 仅输入前缀被缓存，输出不缓存，仍通过计算和推理生成 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "The hard disk cache only matches the prefix part of the user's input. The output is still generated through computation and inference" | type: official
- [C13] scope: 缓存按 user_id 隔离，不同 user_id 拥有独立的 KVCache 存储 | src: https://api-docs.deepseek.com/quick_start/rate_limit/ | quote: "KVCache Privacy: Separates cache storage between users" | type: official
- [C14] scope: 各用户的缓存在逻辑上相互隔离且不可见，确保隐私和安全 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "Each user's cache remains logically separate... ensuring data privacy and security" | type: official
- [C15] api: 无单独的缓存管理/查询 API，缓存自动管理 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "Unused cache entries are automatically cleared after a period" | type: official
- [C16] api: 缓存性能仅能通过 response 的 usage 字段中的 prompt_cache_hit_tokens 和 prompt_cache_miss_tokens 字段观测 | src: https://api-docs.deepseek.com/api/create-chat-completion/ | quote: "API response includes two usage metrics... prompt_cache_hit_tokens and prompt_cache_miss_tokens" | type: official
- [C17] 缓存应用于多轮对话、重复数据分析、代码分析和 few-shot 学习等场景 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "Multi-turn conversations... Repeated data analysis on the same documents... Code analysis with recurring repository references... Few-shot learning scenarios" | type: official
- [C18] 性能示例：128K token 输入在高参考密度下，首 token 延迟从 13 秒降至 500ms | src: https://api-docs.deepseek.com/news/news0802/ | quote: "First token latency improved from 13 seconds to 500 milliseconds for a 128K prompt with high reference density" | type: official

## conflicts
- [CONF1] 缓存命中价格存在不同版本：硬盘缓存公告（2024-08-02）声称统一价格 $0.014/百万 tokens，但 2026 年定价页面区分 Flash ($0.003–0.006) 和 V4-Pro ($0.022–0.044)。两个数字均为官方，表明价格已调整。
  - 源1: https://api-docs.deepseek.com/news/news0802/ | quote: "$0.014 per million tokens"
  - 源2: https://api-docs.deepseek.com/quick_start/pricing/ | quote: "Cache hit input: $0.003–$0.006... Cache hit input: $0.022–$0.044"

## gaps
- 前缀的哪些具体改动（字符级、token 级、结构级）会导致缓存失效，官方文档未明确说明
- API key 级别的缓存隔离策略未明确：缓存按 user_id 隔离，但未说明不同 API key 的缓存是否可跨账户共享
- 缓存 TTL 具体时长（如 hours 范围内的小时数、days 范围内的天数）未给出，仅说"hours to days"
- 是否存在缓存大小限制（单个前缀、单个用户、账户级别）的官方规范未找到
- 缓存构造延迟（从首次请求到缓存可用的时间）未在文档中量化

## leads
- MLA 架构在 KV cache 大小压缩中的具体效率数据（相对标准 Transformer 的压缩比）可进一步调研
- DeepSeek V4.1-Flash（2026-09-10 发布）定价是否再次调整，与本笔记中 2026 定价页面的对应关系需确认
- Chat Prefix Completion API 和缓存机制的交互方式（是否共用相同的缓存后端）可进一步查证
