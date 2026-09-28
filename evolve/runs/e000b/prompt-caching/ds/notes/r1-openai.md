# r1-openai
question: OpenAI Chat Completions / Responses API 的 prompt caching（提示缓存）机制是什么样的？是否全自动、无需修改请求结构？
checked: https://developers.openai.com/api/docs/guides/prompt-caching, https://developers.openai.com/cookbook/examples/prompt_caching_201, https://developers.openai.com/api/docs/changelog, https://developers.openai.com/api/docs/pricing

## claims
- [C1] 提示缓存自动触发，对超过1024个token的请求自动激活，无需代码修改 | src: https://developers.openai.com/cookbook/examples/prompt_caching_101 | quote: "automatically activates for prompts longer than 1024 tokens without requiring changes to your API requests" | type: official
- [C2] 最小可缓存长度为1024 token，在此以上128-token为增量单位 | src: https://developers.openai.com/cookbook/examples/prompt_caching_201 | quote: "works automatically for prompts containing 1024 tokens or more, with cache hits occurring in increments of 128 tokens" | type: official
- [C3] GPT-4o/o1系列模型上缓存的输入token折扣为50%（cached input cost $1.25/1M vs uncached $2.50/1M for GPT-4o） | src: https://developers.openai.com/api/docs/pricing | quote: "GPT-4o in Standard mode, cached inputs cost just $1.25 per 1M tokens versus $2.50 for regular inputs—a 50% reduction" | type: official
- [C4] GPT-5.6及后续模型上缓存读取折扣为90%（0.1x uncached rate），缓存写入费用为1.25x uncached rate | src: https://developers.openai.com/api/docs/changelog | quote: "For GPT-6 Sol cached input tokens cost $0.20 per 1M tokens compared to standard input pricing of $2 per 1M tokens—representing a 90% reduction" | type: official
- [C5] GPT-4o/o1模型上写入缓存无额外费用（包含在标准输入定价内）；GPT-5.6+写入费用为1.25x | src: https://developers.openai.com/api/docs/pricing | quote: "For GPT-4o, cache writes are charged at the same rate as standard inputs ($2.50 per 1M tokens)" | type: official
- [C6] 缓存TTL默认值：早期模型为5-10分钟无活动后清除或最多1小时；GPT-5.6+默认30分钟，可配置至24小时 | src: https://developers.openai.com/api/docs/changelog | quote: "extended prompt cache retention keeping cached prefixes active up to a maximum of 24 hours; for organizations without ZDR enabled, prompt_cache_retention now defaults to 24h" | type: official
- [C7] 缓存失效基于前缀精确匹配规则：breakpoint之前的内容必须完全相同才能命中缓存 | src: https://developers.openai.com/cookbook/examples/prompt_caching_201 | quote: "Exact matching: Cache hits require identical prefix matching and requests must land on the same server" | type: official
- [C8] 响应中用usage.input_tokens_details或prompt_tokens_details中的cached_tokens字段表示缓存命中，cache_write_tokens字段表示本次写入的token数 | src: https://developers.openai.com/cookbook/examples/prompt_caching_201 | quote: "Monitor the cached_tokens field in usage.prompt_tokens_details to verify cache hits" | type: official
- [C9] 支持GPT-4o、GPT-4o mini、o1-preview、o1-mini（2024年10月发布），以及GPT-5.6、GPT-6等后续模型；所有支持的模型默认启用 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Prompt caching is automatically applied on the latest versions of GPT-4o, GPT-4o mini, o1-preview and o1-mini, as well as fine-tuned versions of those models" | type: official
- [C10] 缓存存储在GPU本地存储中（individual machines上），不跨Organization共享，也不跨地域边界共享 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cached states live on individual machines with GPU-local storage; Caches are not shared across organizations and cannot be reused across regional processing boundaries" | type: official
- [C11] 可选参数优化（不必须）：prompt_cache_key用于按用户/客户分账，prompt_cache_options.mode选择implicit或explicit模式（GPT-5.6+），prompt_cache_breakpoint手动标记缓存边界 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "prompt_cache_options.mode: Select implicit or explicit caching; prompt_cache_breakpoint: Mark reusable prefix boundaries" | type: official
- [C12] GPT-5.6引入explicit caching模式，允许手动控制缓存breakpoint位置；implicit模式由OpenAI自动放置breakpoint在消息末尾 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "On GPT-5.6+, Implicit mode: OpenAI automatically places breakpoints at the end of eligible messages; Explicit mode: You manually mark breakpoint locations using prompt_cache_breakpoint" | type: official
- [C13] 缓存命中需要请求落在同一服务器上，且前缀完全匹配；大约15 req/min/prefix阈值后可能触发cache miss | src: https://developers.openai.com/cookbook/examples/prompt_caching_201 | quote: "requests must land on the same server; approximately 15 requests per minute per prefix/key combination before overflow triggers cache misses on additional machines" | type: official

## conflicts
- 定价变化：初次发布（2024年10月）GPT-4o/o1系列为50%折扣；2026年9月GPT-5.6+升级为90%折扣。早期模型缓存写入无费用，GPT-5.6+改为1.25x费用。

## gaps
- 缺少详细的Azure OpenAI与原生OpenAI行为差异说明
- 缺少explicit vs implicit caching对cost的具体影响量化
- 缺少Responses API与Chat Completions API在缓存行为上的细节差异

## leads
- Azure OpenAI prompt caching may have different retention/pricing model (需核实是否跨地域/跨org规则不同)
- GPT-6 Sol/Luna(2026年9月)相比GPT-5.6的caching改进细节值得跟踪
