# r1-kimi
question: Kimi（Moonshot AI）API 的 context caching 机制是什么样的？是全自动隐式缓存，还是需要先创建一个独立的缓存对象（类似 Gemini 的 CachedContent）再引用？
checked: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api, https://platform.kimi.ai/docs/api/chat, https://platform.kimi.ai/docs/pricing/chat

## claims
- [C1] Kimi 实现全自动隐式缓存（F1 家族），仅需在请求中加 prompt_cache_options 参数 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "automatically writes the request prefix to the cache" | type: official
- [C2] prompt_cache_options 包含两个字段：mode（仅支持 "implicit"）和 ttl（"5m" 或 "1h"） | src: https://platform.kimi.ai/docs/api/chat | quote: "mode: Accepts only \"implicit\"... ttl: Accepts \"5m\" or \"1h\"" | type: official
- [C3] 不需要创建独立缓存对象，无缓存 ID 或 resource name 概念 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "no cache ID, TTL, or extra parameter is required" | type: official
- [C4] 默认启用缓存写入 5m 缓存层（当 prompt_cache_options 被 omitted 时） | src: https://platform.kimi.ai/docs/api/chat | quote: "When omitted, cache write is enabled by default (5m tier)" | type: official
- [C5] 最小可缓存长度 256 tokens | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "A new request can hit the prefix cache only when the previous request's prompt tokens exceed 256" | type: official
- [C6] K3 系列命中计费 $0.30 / MTok，相对于 $3.00 / MTok 原价约 90% 折扣 | src: https://platform.kimi.ai/docs/pricing/chat | quote: "Cached Input (hit): $0.30 per 1M tokens... Standard Input: $3.00" | type: official
- [C7] K2.6 系列命中计费 $0.16 / MTok（cache hit），相对于 $0.95 / MTok 原价约 84% 折扣 | src: https://platform.kimi.ai/docs/pricing/chat | quote: "$0.16 (cache hit) / $0.95 (miss)" | type: official
- [C8] 写入计费：K3 系列 5m 缓存 $3.00 / MTok，1h 缓存 $6.00 / MTok | src: https://platform.kimi.ai/docs/pricing/chat | quote: "Cache Write (5min TTL): $3.00 per 1M tokens... Cache Write (1h TTL): $6.00 per 1M tokens" | type: official
- [C9] K2.7-code 系列 cache write 计费 $3.00 / MTok | src: https://platform.kimi.ai/docs/pricing/chat | quote: "For Kimi K2.7 Code: Cache Write $3.00 / MTok" | type: official
- [C10] 写入计费是指将请求前缀写入缓存的成本，首次写入时计费（非存储费） | src: https://platform.kimi.ai/docs/pricing/chat | quote: "Cache Write refers to the cost of writing request prefixes into the context cache" | type: official
- [C11] TTL 有两个独立层级：5 分钟（默认）和 1 小时 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "Two cache durations are available: 5 minutes (default)... 1 hour" | type: official
- [C12] 缓存命中后 TTL 重置为原始值（自动续期） | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "Cache entries reset to their original TTL upon cache hits" | type: official
- [C13] 前缀任何地方改变就会导致缓存 miss（前缀匹配） | src: https://platform.kimi.ai/docs/guide/use-dynamic-tool-loading | quote: "context caching works by prefix matching where only the leading portion of the current request that is identical to a previous request can hit the cache, and any change within the prefix invalidates the cache" | type: official
- [C14] 系统提示或工具定义的早期改变会失效缓存，但末尾追加新工具不会破坏已有缓存 | src: https://platform.kimi.ai/docs/guide/use-dynamic-tool-loading | quote: "Modifications to tools or system prompts in the early part of your message sequence will invalidate cache hits, while appending new tools at the end preserves the existing cache" | type: official
- [C15] 响应中 prompt_tokens_details 包含 cached_tokens（缓存命中的 token 数）字段表示缓存命中 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "Usage reports include prompt_tokens_details showing: cached_tokens: tokens from cache (read)" | type: official
- [C16] 响应中另有 cache_write_tokens 字段表示本次写入缓存的 token 数 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "cache_write_tokens: tokens written to cache" | type: official
- [C17] 支持模型包括 kimi-k3, kimi-k2.6, kimi-k2.7-code | src: https://platform.kimi.ai/docs/pricing/chat | quote: "K3 Series... K2 Series... kimi-k2.6... kimi-k2.7-code" | type: official
- [C18] 缓存数据按组织隔离，组织间不共享 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "Cache isolation: Separate per organization; never shared across orgs" | type: official
- [C19] 切换模型后之前的缓存不再命中，需要重新填充 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "After switching models, the context cache built earlier no longer hits on the new model" | type: official
- [C20] 稳定内容（系统提示、工具定义、参考资料、代码库）应放在请求前方，动态内容放在末尾以优化缓存 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "Put stable system prompts, tool definitions, reference material, and codebases at the front of the request while placing per-request user questions, tool results, and task state at the end" | type: official

## conflicts

## gaps
- D2 详细代码示例（JSON 请求体格式）
- D3 最小长度是否因模型而异
- D5 是否可禁用缓存写入
- D6 能否自定义 TTL 为其他值
- D7 图片、文件等非文本内容改变是否导致失效
- D10 缓存具体存储位置（内存/磁盘/分布式）

## leads
- Kimi K3 2026 年 7 月新发布，缓存机制可能还在迭代；需确认其他新模型（如 K2.8）是否支持缓存
- 与 Anthropic Claude 的请求内显式断点模式对比：Kimi 采用纯参数式自动缓存，更接近 OpenAI 隐式策略
- Kimi 独特之处：写入费用按 TTL 分层（5m vs 1h），鼓励长期缓存的用户付更多写入费
