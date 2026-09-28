# r1-openai
question: OpenAI API 的 Prompt Caching 机制，在以下 10 个维度上分别是什么？(D1–D10)
checked: https://developers.openai.com/docs/guides/prompt-caching, https://developers.openai.com/api/docs/api-reference/chat/create

## claims
- [C1] D1 触发方式：Prompt caching 在支持的模型上默认启用，不需要改代码就能获得缓存 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Prompt caching is enabled by default for supported OpenAI models" | type: official | date: 2026-09-24

- [C2] D1 触发方式：可选参数用于显式控制缓存行为（mode 和 ttl），但基础缓存无需参数 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "For GPT-5.6+, you can optionally use explicit breakpoints to control precisely where caching occurs, or rely on implicit automatic placement" | type: official

- [C3] D2 最小可缓存长度：GPT-5.6+ 需要 1024 个 visible input tokens 才能触发缓存 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "For GPT-5.6 and later, it's 1,024 visible input tokens" | type: official

- [C4] D2 最小可缓存长度：早期模型有不同的阈值，取决于工具、图像和推理努力等设置 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Earlier models have different minimums depending on request settings like tools, images, and reasoning effort" | type: official

- [C5] D3 粒度/断点：使用 implicit 模式时 OpenAI 自动创建一个隐式断点和最多三个显式断点 | src: https://developers.openai.com/docs/api-reference/chat/create | quote: "implicit mode, OpenAI creates one implicit breakpoint and writes up to the latest three explicit breakpoints" | type: official

- [C6] D3 粒度/断点：explicit 模式禁用自动断点；每个请求最多 4 次缓存写入 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Each request can create up to four cache writes" | type: official

- [C7] D4 命中读取计费：缓存命中的 tokens 按标准输入 token 费率的 0.1x 计费（90% 折扣） | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "cached reads cost 0.1× the uncached input-token rate" | type: official

- [C8] D5 写入/存储计费：建立缓存时额外收费，GPT-5.6+ 按 1.25x 标准费率计费 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "cache writes cost 1.25× the uncached input-token rate" | type: official

- [C9] D5 写入/存储计费：一次写入加一次完全复用的总成本为 1.35x，相比不缓存两次处理的 2x 更便宜 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "writing a prefix once and fully reusing it once costs 1.35× its ordinary input cost, compared with 2× for processing it twice without caching" | type: official

- [C10] D6 TTL：GPT-5.6+ 的缓存在最后一次写入或复用后 30 分钟内保持可复用状态 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse" | type: official

- [C11] D6 TTL：prompt_cache_options.ttl 参数目前仅支持 "30m" 这一个值 | src: https://developers.openai.com/docs/api-reference/chat/create | quote: "ttl (optional): Sets minimum cache lifetime, currently supporting only 30m as a value" | type: official

- [C12] D6 TTL：早期模型使用不同的保留选项，in_memory 为 5-10 分钟内非活跃，最多一小时；24h 选项保留约 30 分钟，最多 24 小时 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "in_memory: typically 5-10 minutes of inactivity, up to one hour" / "24h: typically around 30 minutes, retained for up to 24 hours" | type: official

- [C13] D7 命中确认：usage 响应对象中 prompt_tokens_details.cached_tokens 字段显示缓存中已有的 tokens 数量 | src: https://developers.openai.com/docs/api-reference/chat/create | quote: "cached_tokens: Cached tokens present in the prompt" | type: official

- [C14] D7 命中确认：usage 响应对象中 prompt_tokens_details.cache_write_tokens 字段显示本次请求写入缓存的未调整 token 数 | src: https://developers.openai.com/docs/api-reference/chat/create | quote: "cache_write_tokens: The unadjusted number of prompt tokens written to cache" | type: official

- [C15] D8 失效条件：系统 prompt 改动导致前缀重写，缓存失效 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "System Prompt Changes – Modifications to instructions rewrite the prefix" | type: official

- [C16] D8 失效条件：改动工具定义、名称、描述、顺序或 schema 会破坏匹配 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Tool Changes – Altering tool definitions, names, descriptions, ordering, or schemas breaks matching" | type: official

- [C17] D8 失效条件：图像改动导致前缀无效 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Images – Changes invalidate the prefix" | type: official

- [C18] D8 失效条件：总结、压缩或上下文截断会改变前缀，破坏缓存 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "summarization, compaction, or context truncation can change the prefix" | type: official

- [C19] D9 适用范围：Responses API 明确支持 prompt caching | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Responses API is explicitly mentioned as supporting prompt caching" | type: official

- [C20] D9 适用范围：Agents API 使用与 Responses API 相同的 prompt caching 行为 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Agents API model calls use the same prompt-caching behavior as the Responses API" | type: official

- [C21] D9 适用范围：GPT-5.6+ 支持显式断点和 TTL 控制的完整缓存功能 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "GPT-5.6 and later support explicit breakpoints and TTL control" | type: official

- [C22] D9 适用范围：早期模型仅支持隐式缓存 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Earlier models use implicit-only caching" | type: official

- [C23] D10 存储介质：缓存以 KV 张量形式存储在独立机器上，流量超过 15 req/min 可能导致溢出路由 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Cached states live on individual machines, where traffic above 15 requests per minute can lead to overflow routing" | type: official

- [C24] D10 隔离：缓存不跨组织共享 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Cached content cannot be shared across organizational boundaries" | type: official

- [C25] D10 隔离：缓存不跨区域边界共享；每个组织在其选定的处理区域内维护单独的缓存存储 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Caches are not shared across organizations and cannot be reused across regional processing boundaries" | type: official

- [C26] D10 隔离：可选的 prompt_cache_key 参数用于指导请求路由到持有匹配缓存条目的机器 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "optional prompt_cache_key parameter to direct requests toward machines with matching cache entries" | type: official

- [C27] 限制条件：缓存输入 tokens 仍然计入 tokens-per-minute 限制 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Cached input tokens still count toward tokens-per-minute limits" | type: official

## conflicts
- None detected between official OpenAI documentation sources

## gaps
- Chat Completions 端点是否官方支持 prompt caching（仅确认了 Responses API 和 Agents API）
- Batch API 是否支持 prompt caching
- Assistants API 是否支持 prompt caching
- 是否所有模型统一采用 0.1x / 1.25x 计费倍数，还是有模型差异
- 是否可续命或手动配置 TTL 超过 30 分钟

## leads
- 文档提及早期模型不同的计费结构，需查具体模型列表及其计费规则
- 提及"Prompt Caching Dashboard"用于监测性能，但文档未详述其功能
