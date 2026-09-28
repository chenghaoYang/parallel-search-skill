# r1-deepseek
question: DeepSeek API 的「上下文硬盘缓存」（Context Caching on Disk）在当前的现状——触发方式（是否全自动）、门槛、计费、TTL、命中确认字段、失效条件、支持范围
checked: https://api-docs.deepseek.com/guides/kv_cache/,https://api-docs.deepseek.com/news/news0802/,https://api-docs.deepseek.com/api/create-chat-completion/,https://api-docs.deepseek.com/quick_start/pricing/,https://api-docs.deepseek.com/quick_start/token_usage/,https://api-docs.deepseek.com/updates/,https://api-docs.deepseek.com/api/list-models/

## claims
- [C1] 触发方式全自动且无需修改请求结构 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "enabled by default for all users, allowing them to benefit without needing to modify their code" | type: official
- [C2] 最小可缓存单位为 64 tokens，低于此长度的内容不会被缓存 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "The cache system uses 64 tokens as a storage unit; content less than 64 tokens will not be cached" | type: official
- [C3] 缓存只能通过前缀匹配触发，无人工控制粒度 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "a subsequent request can only hit the cache if it fully matches a cache prefix unit" | type: official
- [C4] 缓存命中价格为 $0.014 per million tokens，相比未缓存的 $0.14/million tokens 可省 90% | src: https://api-docs.deepseek.com/news/news0802/ | quote: "For cache hits, DeepSeek charges $0.014 per million tokens, slashing API costs by up to 90%" | type: official
- [C5] 缓存命中时的延迟显著改善，128K 提示从 13 秒降至 500ms | src: https://api-docs.deepseek.com/news/news0802/ | quote: "first token latency is cut from 13s to just 500ms on lengthy prompts" | type: official
- [C6] TTL 为数小时至数天，未使用的缓存项会自动清除 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "unused cache entries are automatically cleared after hours to days" | type: official
- [C7] 响应体中 prompt_cache_hit_tokens 字段记录缓存命中的 token 数 | src: https://api-docs.deepseek.com/api/create-chat-completion/ | quote: "prompt_cache_hit_tokens: Tokens benefiting from cache" | type: official
- [C8] 响应体中 prompt_cache_miss_tokens 字段记录未命中的 token 数 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "prompt_cache_miss_tokens: tokens that weren't cached" | type: official
- [C9] 缓存失效条件为前缀不完全匹配，仅从第 0 token 起的相同前缀才能命中 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "identical prefixes (starting from the 0th token) to trigger caching" | type: official
- [C10] 硬盘缓存使用 MLA 架构实现，显著降低 KV cache 大小 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "MLA architecture, which significantly reducing the size of the context KV cache, enabling efficient storage on low-cost disks" | type: official
- [C11] 每个用户的缓存在逻辑上保持隔离，不跨 API key 共享 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "Each user's cache remains isolated" | type: official
- [C12] 缓存是完全隐式实现，无独立的 cache 资源对象或显式 API 参数 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "enabled by default for all users" | type: official
- [C13] 支持范围涵盖 deepseek-flash 和 deepseek-v4-pro 模型 | src: https://api-docs.deepseek.com/api/list-models/ | quote: "deepseek-flash and deepseek-v4-pro" models | type: official
- [C14] 缓存对输出生成无影响，温度等参数仍会引入随机性，缓存不保证 100% 命中率 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "the cache system works on a best-effort basis and does not guarantee a 100% cache hit rate" | type: official
- [C15] Context Caching on Disk 技术发布于 2024 年 8 月 2 日 | src: https://api-docs.deepseek.com/updates/ | quote: "Context Caching became available on 2024/08/02" | type: official
- [C16] 缓存不影响输出计算，输出仍需通过完整推理生成 | src: https://api-docs.deepseek.com/guides/kv_cache/ | quote: "the output is still generated through computation and inference" | type: official
- [C17] 缓存命中未明确收取额外写入费用，标准定价模式下缓存写入成本已包含 | src: https://api-docs.deepseek.com/news/news0802/ | quote: "billing is based on actual cache hits" | type: official

## conflicts
- <无>

## gaps
- D5（写入计费）：官方文档未明确说明缓存写入是否额外计费，仅提及"基于实际缓存命中计费"
- D11 的模型范围边界：未明确说明是否 R1 等推理模型也支持缓存
- 显式缓存控制：是否存在禁用缓存或人工指定缓存点的 API 参数

## leads
- 官方定价页面可能包含每个模型的详细缓存计费表，建议交叉查证 pricing 字段中是否有"cache_hit"专用价格档位
- 考虑测试 API 响应头中是否包含缓存相关的元数据（如 cache-hit 确认header）
- MLA 架构的硬盘缓存与内存缓存的性能对比未在文档中详细说明，可能需要性能测试确认
