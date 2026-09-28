# r1-scout-pitfalls
question: 四家 prompt caching 改变「自动/手动、TTL、计费」的官方变更与失效/计费坑
checked: https://developers.openai.com/api/docs/changelog, https://developers.openai.com/api/docs/guides/prompt-caching, https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/release-notes/overview, https://platform.claude.com/docs/en/manage-claude/api-and-data-retention, https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/changelog, https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/, https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/news/news0802, https://api-docs.deepseek.com/quick_start/pricing

## claims
- [C1] OpenAI 2025-11-13：extended prompt cache retention 上线，最长 24h（KV 张量溢出到 GPU 本地存储） | src: https://developers.openai.com/api/docs/changelog | quote: "Extended prompt cache retention keeps cached prefixes active for longer, up to a maximum of 24 hours." | type: official
- [C2] OpenAI 2026-05-29：无 ZDR 组织 prompt_cache_retention 默认改 24h；ZDR 组织默认 in_memory | src: https://developers.openai.com/api/docs/changelog | quote: "For organizations without ZDR enabled, `prompt_cache_retention` now defaults to `24h` instead of `in_memory`" | type: official
- [C3] OpenAI 2026-04-24（GPT-5.5）：只支持 extended caching | src: https://developers.openai.com/api/docs/changelog | quote: "Caching for GPT-5.5 only works with extended prompt caching. In-memory prompt caching is not supported." | type: official
- [C4] OpenAI GPT-5.6+ 新增缓存写计费：写 1.25×、读 0.1×；TTL 改为 prompt_cache_options.ttl，唯一值 "30m" | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "For GPT-5.6 and later, cache writes cost 1.25× the standard, uncached input-token rate." | type: official
- [C5] OpenAI 路由坑：缓存驻留单机，>15 rpm 会溢出路由；跨组织、跨区域不共享 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "traffic above 15 requests per minute can lead to overflow routing" | type: official
- [C6] OpenAI：cached tokens 仍计入 TPM 限流 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cached input tokens still count toward tokens-per-minute limits." | type: official
- [C7] Anthropic 2026-02-19：automatic caching 上线（顶部单个 cache_control，自动移动断点） | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "We've launched **automatic caching** for the Messages API." | type: official
- [C8] Anthropic 2025-08-13：1 小时缓存不再需要 beta header | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "The 1-hour cache duration for prompt caching no longer requires a beta header." | type: official
- [C9] Anthropic 2026-09-01：Fable/Mythos 5.1 缓存读降到 0.025×（Opus 5.5 为 0.05×，其余 0.1×） | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "0.025x the base input price, compared with 0.1x on other models" | type: official
- [C10] Anthropic：TTL 从请求开始计时，长流式生成吃掉 5 分钟窗口 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The lifetime is measured from the start of the request that writes or reads the cache entry, not from the end of its response." | type: official
- [C11] Anthropic 并发坑：首个响应开始前缓存不可用，并行请求须等首响应 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "a cache entry only becomes available after the first response begins." | type: official
- [C12] Anthropic 隔离粒度：API/AWS/Foundry 为 workspace 级，Bedrock/GCP 为 org 级 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching uses workspace-level isolation." | type: official
- [C13] Anthropic：缓存命中不计入限流 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "cache hits are not deducted against your rate limit" | type: official
- [C14] Anthropic：低于最小缓存长度的请求静默不缓存、不报错 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "processed without caching, and no error is returned" | type: official
- [C15] Anthropic：prompt caching 在 ZDR 下可用（KV 仅内存驻留） | src: https://platform.claude.com/docs/en/manage-claude/api-and-data-retention | quote: "KV cache representations and cryptographic hashes are held in memory for the cache TTL and promptly deleted after expiry." | type: official
- [C16] Gemini 2025-05-08 官方博客：implicit caching 上线，75% 折扣自动返还 | src: https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/ | quote: "implicit caching directly passes cache cost savings to developers without the need to create an explicit cache." | type: official
- [C17] Gemini 文档（2026-09-02 更新）：implicit caching 对 2.5+ 默认开启；最小 token 2.5 系 2048、3.x 系 4096 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models." | type: official
- [C18] Gemini：Interactions API 只支持 implicit caching | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Explicit caching (manually creating and managing cache objects) is not supported in the Interactions API." | type: official
- [C19] DeepSeek：Sliding Window Attention 使前缀匹配规则变更；命中须完全匹配 cache prefix unit | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Due to the Sliding Window Attention mechanism, the storage and matching of cached prefixes differs from before." | type: official
- [C20] DeepSeek：best-effort 不保证命中；闲置缓存数小时到数天清除 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "The cache system works on a \"best-effort\" basis and does not guarantee a 100% cache hit rate." | type: official
## conflicts
- DeepSeek：2024-08 公告（https://api-docs.deepseek.com/news/news0802）写 "The cache system uses 64 tokens as a storage unit"、命中 $0.014/MTok；现行 kv_cache 指南改为「完全匹配 cache prefix unit」、不提 64-token 粒度，定价页 hit $0.003–0.044。
- Gemini：2025-05-08 博客称最小请求量降到 1,024（2.5 Flash）/2,048（2.5 Pro）；现行文档 2.5 均 2,048——阈值上调过。
- OpenAI 指南同页并存 "cache writes cost 1.25×"（GPT-5.6+）与旧模型 "No additional cache-write charge"——按代际区分，易误读。

## gaps
- streaming 是否影响命中：四家均未明说。
- Gemini implicit cache 的 TTL/驻留位置/可否禁用/隔离粒度：未写。
- DeepSeek：无 TTL 字段或手动失效；观测仅 prompt_cache_hit_tokens/miss_tokens。
- Anthropic 1h TTL 的 beta header 名（extended-cache-ttl-2025-04-11）无官方原句。
- Gemini release notes 无 implicit caching 条目，日期仅博客可查。

## leads
- OpenAI | cached 计 TPM vs Anthropic 命中不计限流——「限流交互」值得单列维度 | https://developers.openai.com/api/docs/guides/prompt-caching ; https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- OpenAI | prompt_cache_key：5.6 前是路由键、之后做账目隔离；官方点名可防跨用户 cache-hit probing | https://developers.openai.com/api/docs/guides/prompt-caching
- OpenAI | implicit→explicit-only 切换或延长旧消息会静默失配；tools/effort/verbosity 等设置均影响前缀；无手动清缓存 | https://developers.openai.com/api/docs/guides/prompt-caching
- Anthropic | 预热用 max_tokens:0；断点须打在共享块而非占位 user 消息，否则键错 | https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic | 混 TTL：1h 断点须在 5m 前，按 A/B/C 三段计费；与显式断点冲突→400 | https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic | inline-tools-2026-09-15 / mid-conversation-tool-changes-2026-07-01 beta：会话中改工具不失效缓存 | https://platform.claude.com/docs/en/release-notes/overview
- Anthropic | 2026-05-13 cache diagnostics beta：diagnostics.previous_message_id 返回 cache_miss_reason | https://platform.claude.com/docs/en/release-notes/overview
- Anthropic | thinking 块缓存按模型分代；speed:"fast" 切换、Swift/Go 键序随机化均失效 | https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic | 计费坑：usage.input_tokens 只含最后一个断点之后的 token | https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- DeepSeek | 命中须全量匹配 prefix unit：A+B→A+C 不命中，等公共前缀持久化后第三请求才命中；hit 价 off-peak $0.003 | https://api-docs.deepseek.com/guides/kv_cache ; https://api-docs.deepseek.com/quick_start/pricing
- 跨家 | ZDR 语义不同：Anthropic 缓存仅内存故 ZDR 可用；OpenAI ZDR 组织拿不到 24h | https://platform.claude.com/docs/en/manage-claude/api-and-data-retention ; https://developers.openai.com/api/docs/guides/prompt-caching
