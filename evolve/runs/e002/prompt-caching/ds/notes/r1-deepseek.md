# r1-deepseek
question: DeepSeek API 的「上下文硬盘缓存」机制在 D1-D10 十个维度上各是什么？
checked: https://api-docs.deepseek.com/guides/kv_cache/, https://api-docs.deepseek.com/news/news0802/, https://api-docs.deepseek.com/quick_start/pricing/, https://api-docs.deepseek.com/api/create-chat-completion/, https://api-docs.deepseek.com/quick_start/token_usage/

## claims
- [C1] D1 触发方式：全自动、不用改代码、不用加任何参数 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "Context Caching is enabled by default for all users, allowing them to benefit without needing to modify their code." | type: official
- [C2] D2 最小可缓存长度：64 tokens | src: https://api-docs.deepseek.com/news/news0802/ | quote: "The cache system uses 64 tokens as a storage unit; content less than 64 tokens will not be cached." | type: official
- [C3] D3 粒度/断点：前缀级（cache prefix units），在请求边界、公共前缀检测、固定间隔处触发 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "These units are persisted at three key moments: request boundaries (after user input and model output), when common prefixes are detected across requests, and at fixed intervals for lengthy inputs." | type: official
- [C4] D3 粒度进一步说明：只有完全匹配前缀的后续请求才能命中缓存 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "A subsequent request can only hit the cache if it fully matches a cache prefix unit." | type: official
- [C5] D4 命中读取计费：每百万 token $0.014（原价 $0.14 未缓存），降价 90% | src: https://api-docs.deepseek.com/news/news0802/ | quote: "The service charges $0.014 per million tokens for cache hits, representing up to 90% savings compared to standard pricing of $0.14 per million tokens." | type: official
- [C6] D5 写入/存储计费：不额外收费 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "Cache storage incurs no additional fees." | type: official
- [C7] D6 TTL：hours to days（几小时到几天），未使用的缓存自动清除 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "The system automatically clears unused caches within hours to days." | type: official
- [C8] D6 硬盘持久化特色：分布式硬盘阵列存储，相比业界常见的内存态缓存提供更长的持久性 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "DeepSeek innovatively adopted context disk caching technology, unlike the industry's common reliance on expensive memory for minute-level caching." | type: official
- [C9] D7 命中确认字段：prompt_cache_hit_tokens（缓存命中 token 数） | src: https://api-docs.deepseek.com/api/create-chat-completion/ | quote: "Number of tokens in the prompt that hits the context cache." | type: official
- [C10] D7 未命中字段：prompt_cache_miss_tokens（缓存未命中 token 数） | src: https://api-docs.deepseek.com/api/create-chat-completion/ | quote: "Number of tokens in the prompt that misses the context cache." | type: official
- [C11] D8 失效条件：不完全匹配请求前缀、长时间不用（hours to days）后自动清除 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "A subsequent request can only hit the cache if it fully matches a cache prefix unit." + "The system automatically clears unused caches within hours to days." | type: official
- [C12] D8 生成过程不缓存：输出仍通过计算和推理生成，受温度等参数影响 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "The output is still generated through computation and inference, and it is influenced by parameters such as temperature." | type: official
- [C13] D9 适用模型：deepseek-flash（DeepSeek-V4.1-Flash）支持 | src: https://api-docs.deepseek.com/quick_start/pricing/ | quote: "Flash model input tokens cost $0.003-$0.30 per million (cache hits to misses)" | type: official
- [C14] D9 适用模型：deepseek-v4-pro（DeepSeek-V4-Pro-0813）支持 | src: https://api-docs.deepseek.com/quick_start/pricing/ | quote: "Pro ranges from $0.022-$1.32 per million." | type: official
- [C15] D10 存储介质：分布式硬盘阵列（distributed disk array） | src: https://api-docs.deepseek.com/news/news0802/ | quote: "The technology caches content that is expected to be reused on a distributed disk array." | type: official
- [C16] D10 隔离机制：逻辑隔离，每用户缓存独立、用户间不共享 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "Each user's cache remains logically isolated from others, with automatic deletion of unused entries within hours to days." | type: official

## conflicts
无

## gaps
- D6 TTL 具体机制：官方未说明是否采用 TTL 概念还是基于使用频率的清除机制
- D9 是否所有新模型都支持（如 R1, V3 等）
- D10 是否有地域限制或跨地域的缓存共享策略

## leads
- DeepSeek 官方强调硬盘持久化相比业界内存缓存提供更长持久性和更低成本（由 MLA 架构的低冗余 KV cache 压缩技术支撑）
- 文档未提及缓存的显式手动清除或更新机制
