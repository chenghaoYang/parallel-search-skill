# r1-deepseek
question: DeepSeek API 的「上下文硬盘缓存」（Context Caching on Disk）机制是什么样的？是否全自动、无需修改请求？
checked: https://api-docs.deepseek.com/guides/kv_cache/,https://api-docs.deepseek.com/news/news0802/,https://api-docs.deepseek.com/api/create-chat-completion/,https://api-docs.deepseek.com/quick_start/pricing/,https://api-docs.deepseek.com/news/news260910/

## claims
- [C1] 缓存触发方式为全自动、无需代码修改 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "The disk caching service is now available for all users, requiring no code or interface changes. The cache service runs automatically." | type: official
- [C2] 完全匹配前缀才能触发缓存命中（从第0个token开始） | src: https://api-docs.deepseek.com/news/news0802/ | quote: "only requests with identical prefixes (starting from the 0th token) will be considered duplicates" | type: official
- [C3] 最小缓存单位为64 tokens | src: https://api-docs.deepseek.com/news/news0802/ | quote: "The cache system uses 64 tokens as a storage unit; content less than 64 tokens will not be cached." | type: official
- [C4] V4.1-Flash 缓存命中价格离峰 $0.003/M tokens、峰值 $0.006/M tokens（September 2026起生效） | src: https://api-docs.deepseek.com/news/news260910/ | quote: "New pricing takes effect at 04:00 UTC on Sept 10, 2026." | type: official
- [C5] 缓存未命中时输入按普通价格计费 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "For cache hits, DeepSeek charges $0.014 per million tokens, slashing API costs by up to 90%." [注：旧价格，当前已更新] | type: official
- [C6] 缓存存储本身不收费 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "billing is based on actual cache hits" | type: official
- [C7] 缓存自动清理，通常几小时到几天内清空 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "caches are automatically cleared within hours to days after disuse" | type: official
- [C8] 缓存 TTL 不可配置 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "operates on a best-effort basis without guaranteed hit rates" | type: official
- [C9] 响应包含 prompt_cache_hit_tokens 和 prompt_cache_miss_tokens 字段 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "prompt_cache_hit_tokens: Tokens that matched cached prefixes" | type: official
- [C10] 支持模型：deepseek-flash 和 deepseek-v4-pro | src: https://api-docs.deepseek.com/ | quote: "Available models: deepseek-flash and deepseek-v4-pro" | type: official
- [C11] 缓存基于 MLA 架构实现，MLA 相比传统模型大幅降低 KV cache 大小 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "This innovation leverages the MLA architecture in DeepSeek V2, which reduces KV cache size" | type: official
- [C12] V4.1-Flash 的 KV cache 相比前代只需 1/4 的 HBM（主内存）和 1/8 的 SSD 存储 | src: https://api-docs.deepseek.com/news/news260910/ | quote: "Its KV cache needs only 1/4 the HBM and 1/8 the SSD storage compared to previous generations." | type: official
- [C13] 缓存在分布式磁盘阵列上，用户间隔离 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "stores repeated content on distributed disk arrays" and "User caches remain isolated" | type: official
- [C14] 多轮对话和长文档分析场景中缓存效果最好 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "Multi-round conversations benefit most" and "Long document analysis works through prefix detection" | type: official
- [C15] 缓存命中可将首 token 延迟从 13 秒降至 500ms（128K 高重复内容场景） | src: https://api-docs.deepseek.com/news/news0802/ | quote: "First-token latency sees substantial reductions with repetitive inputs...achieved latency improvement from 13 seconds down to 500 milliseconds." | type: official
- [C16] 缓存前缀在三个时点被持久化：请求边界、检测到公共前缀、长输入输出的固定间隔处 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "cache prefix units through three methods: At request boundaries...When detecting common prefixes...At fixed token intervals" | type: official
- [C17] 输出仍通过推理生成，不缓存输出、仍受温度等参数随机性影响 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "the output is still generated through computation and inference with randomness based on temperature and other parameters" | type: official

## conflicts
- 官方旧公告（August 2024）中提到缓存命中 $0.014/M tokens，但 September 2026 新闻稿中 V4.1-Flash 价格更新为 $0.003-0.006/M tokens | src1: https://api-docs.deepseek.com/news/news0802/ | src2: https://api-docs.deepseek.com/news/news260910/

## gaps
- 缓存写入是否额外收费（相对未命中输入是否有溢价）：官方未明确说明
- 具体 TTL 时间下限与上限（「几小时到几天」未有精确数字）
- 是否支持手动清缓存或强制缓存未命中
- deepseek-chat/deepseek-reasoner 等其他模型是否支持缓存
- 前缀匹配是否区分 system/user/assistant role

## leads
- V4.1-Flash 新增的 8B active / 16B output 参数配置可能与缓存大小有关，需确认是否影响缓存命中率
- GitHub issue #1655 提出过「显式缓存对象」需求，需查看是否有后续更新
- MLA 架构论文中对 KV cache 压缩比的详细说明，理解硬盘缓存为何可行的理论基础
