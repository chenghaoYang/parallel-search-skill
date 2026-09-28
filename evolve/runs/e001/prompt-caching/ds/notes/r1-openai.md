# r1-openai
question: OpenAI API 的 Prompt Caching 现在的机制是什么？
checked: https://developers.openai.com/api/docs/guides/prompt-caching, https://developers.openai.com/api/docs/guides/prompt-caching#how-caching-works, https://developers.openai.com/api/docs/guides/prompt-caching#cache-invalidation, https://developers.openai.com/api/docs/guides/prompt-caching#checking-cache-hit, https://developers.openai.com/api/docs/guides/prompt-caching#pricing, https://developers.openai.com/api/docs/guides/prompt-caching#storage-scope, https://developers.openai.com/api/docs/guides/prompt-caching#cache-limits, https://developers.openai.com/api/docs/guides/prompt-caching#getting-started, https://developers.openai.com/api/docs/guides/prompt-caching#managing-cache-lifecycle, https://developers.openai.com/api/docs/guides/prompt-caching#troubleshooting, https://developers.openai.com/docs/changelog, https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics

## claims
- [C1] 提示词缓存默认在支持的模型上启用（无需代码改动），但GPT-5.6+可以通过`prompt_cache_options.mode`设置为explicit模式以手动控制 | src: https://developers.openai.com/api/docs/guides/prompt-caching#getting-started | quote: "Prompt caching is enabled by default for supported OpenAI models." | type: official
- [C2] GPT-5.6+触发缓存需要前缀至少1,024个可见token；更早的模型因请求设置（tools、images、schemas、reasoning effort）而异 | src: https://developers.openai.com/api/docs/guides/prompt-caching#cache-limits | quote: "1,024 visible input tokens required before caching begins." | type: official
- [C3] 缓存命中的token价格为原价的0.1倍（90%折扣）；GPT-5.6+写入缓存费用为1.25倍标准input-token价格 | src: https://developers.openai.com/api/docs/guides/prompt-caching#pricing | quote: "Cache writes cost 1.25× the standard, uncached input-token rate. Cached reads cost 0.1× the uncached input-token rate." | type: official
- [C4] GPT-5.6+缓存默认TTL为30分钟；更早的模型支持in_memory（5-10分钟，最多1小时）或24h选项，2026年5月29日后默认改为24h | src: https://developers.openai.com/api/docs/guides/prompt-caching#cache-limits | quote: "A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse." | type: official
- [C5] 缓存存储在"个别机器上"，不跨organization或regional processing boundaries | src: https://developers.openai.com/api/docs/guides/prompt-caching#storage-scope | quote: "Cached states live on individual machines. Caches are not shared across organizations and cannot be reused across regional processing boundaries." | type: official
- [C6] 查询缓存命中通过response.usage.input_tokens_details.cached_tokens字段（显示命中的token数）和cache_write_tokens字段（显示写入的token数） | src: https://developers.openai.com/api/docs/guides/prompt-caching#checking-cache-hit | quote: "cached_tokens shows the exact eligible boundary, excluding hidden tokens that were reused from cache. cache_write_tokens indicates tokens written to cache." | type: official
- [C7] 完整渲染后的前缀必须完全匹配才能复用缓存，以下改动会导致失效：模型改变、tool定义/顺序/schema改变、parallel_tool_calls改变、output format改变、reasoning.effort改变、text.verbosity改变、context_management改变、消息内容扩展 | src: https://developers.openai.com/api/docs/guides/prompt-caching#cache-invalidation | quote: "Cache reuse requires the entire rendered prefix to match. If content or a relevant setting changes before a breakpoint, the prefix cannot match." | type: official
- [C8] 缓存绑定到organization级别，不跨region；可通过`prompt_cache_key`为customers/users/workspaces维持独立的缓存计数，但不隔离缓存本身 | src: https://developers.openai.com/api/docs/guides/prompt-caching#storage-scope | quote: "prompt_cache_key to maintain separate cache accounting for customers, users, or workspaces." | type: official
- [C9] 无独立的缓存管理API；缓存完全自动和隐式，不提供手动创建/查询/删除功能，只能通过Prompt Caching Dashboard和API response的usage字段监控 | src: https://developers.openai.com/api/docs/guides/prompt-caching#managing-cache-lifecycle | quote: "Manual cache clearing is not currently available. No API to query cache status or list cached entries." | type: official
- [C10] 2026年9月8日Cache Diagnostics在Responses API for GPT-5.6+成为GA，支持通过prompt_cache_options.comparison_response_id对比前后请求缓存复用情况 | src: https://developers.openai.com/docs/changelog | quote: "Sep 8, 2026 - Prompt Cache Diagnostics became generally available in the Responses API for GPT-5.6 and later models." | type: official
- [C11] GPT-5.6+在explicit模式下使用`prompt_cache_breakpoint: {"mode": "explicit"}`在特定内容块标记缓存边界；隐式模式将breakpoint放在"最新eligible message的末尾" | src: https://developers.openai.com/api/docs/guides/prompt-caching#how-caching-works | quote: "Explicit mode lets you control exactly what gets cached. Implicit mode places a breakpoint at the end of the latest eligible message." | type: official
- [C12] 超过15 requests/minute的流量可能导致机器溢出路由，影响缓存复用概率 | src: https://developers.openai.com/api/docs/guides/prompt-caching#storage-scope | quote: "traffic above 15 requests per minute can lead to overflow routing." | type: official
- [C13] 消息扩展（在现有消息末尾添加内容而非追加新消息）会破坏缓存复用；应使用追加新消息而非重写earlier turns的方式维护缓存 | src: https://developers.openai.com/api/docs/guides/prompt-caching#troubleshooting | quote: "Extending an existing message rather than appending a new one prevents cache reuse." | type: official
- [C14] 提示词缓存优势：避免重新计算已处理过的前缀、降低成本到原价10%、加速响应（TTFT可减少80%） | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Compute-efficient: Avoid recalculating a prompt prefix. Cost savings through reduced cached-input rates up to 90%." | type: official
- [C15] 系统提示词和多模态内容（文本、图片、文档、音频）作为渲染上下文的一部分被缓存，仅在内容本身改变时失效（不因参数改变而失效） | src: https://developers.openai.com/api/docs/guides/prompt-caching#cache-invalidation | quote: "System prompts and multi-modal content are cached as part of the rendered context—they only invalidate reuse if their actual content changes." | type: official
- [C16] 2024年10月1日首次发布提示词缓存功能 | src: https://developers.openai.com/docs/changelog | quote: "October 1, 2024 - Prompt caching was initially launched." | type: official
- [C17] 2025年7月9日GPT-5.6引入explicit prompt caching控制 | src: https://developers.openai.com/docs/changelog | quote: "July 9, 2025 - GPT-5.6 introduced explicit prompt caching controls." | type: official
- [C18] 2026年5月29日：对于未启用Zero Data Retention的organization，prompt_cache_retention默认改为24h（之前为in_memory） | src: https://developers.openai.com/docs/changelog | quote: "May 29, 2026 - Default retention behavior changed. prompt_cache_retention now defaults to 24h instead of in_memory." | type: official

## conflicts
无官方文档间冲突发现。all sources align on core mechanism and pricing.

## gaps
- 缓存是否绑定specific API key或仅限organization级别（文档未明确说明API key隔离）
- prompt_cache_options.prewarm功能的具体作用和触发机制（仅提及存在，未详述）
- 较早模型（GPT-4o、o1等）的具体min_len阈值（文档仅说"variable depending on request settings"）
- Cache Diagnostics的具体reason codes完整列表（文档提及"tools_changed"、"model_changed"等示例，但未列举全部）
- 缓存是否支持跨account/team级别共享（仅提及organization，未论述multi-org scenario）

## leads
- Responses API与Chat Completions API在缓存上的行为差异（Diagnostics仅在Responses API可用）
- 如何在应用中最大化缓存命中率的最佳实践（可参考Prompt Caching 201 cookbook示例）
- 与Azure OpenAI及AWS Bedrock上的缓存实现的一致性（搜索结果提及支持但未在官方文档对比）
