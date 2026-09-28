# r1-openai
question: OpenAI API的Prompt Caching机制在当前（2026年）的现状——触发方式、门槛、粒度、计费、TTL、命中确认字段、失效条件、支持范围。
checked: https://developers.openai.com/api/docs/guides/prompt-caching,https://developers.openai.com/docs/api-reference/chat,https://developers.openai.com/api/docs/changelog,https://openai.com/index/api-prompt-caching/

## claims
- [C1] 触发方式：完全自动，无需改代码。对GPT-5.6+可选择显式模式。 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Prompt caching activates automatically when requests share identical prompt prefixes." | type: official
- [C2] 最小可缓存长度（GPT-5.6+）：1024可见输入tokens，之后按128 token增量缓存 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "1,024 visible input tokens must precede a cache breakpoint" | type: official
- [C3] 隐式模式（默认）：OpenAI自动在message边界放置缓存断点；显式模式（GPT-5.6+）：开发者用prompt_cache_breakpoint标记可重用段 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Implicit: OpenAI automatically places breakpoints at message boundaries; Explicit: Developers manually mark reusable sections using prompt_cache_breakpoint" | type: official
- [C4] 命中计费（GPT-5.6+）：0.1×标准输入token费率，即90%折扣 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cached reads cost 0.1× the uncached input-token rate on GPT-5.6+" | type: official
- [C5] 写入计费（GPT-5.6+）：1.25×标准输入token费率 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cache writes cost 1.25× standard input rate" | type: official
- [C6] TTL（GPT-5.6+）：至少30分钟，默认30m，支持prompt_cache_options.ttl自定义 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "at least 30 minutes after the latest write or reuse" | type: official
- [C7] TTL（May 2026后）：organizations without Zero Data Retention默认改为24小时而非in_memory | src: https://developers.openai.com/api/docs/changelog | quote: "prompt_cache_retention now defaults to 24h instead of in_memory" | type: official
- [C8] 命中确认字段：usage.prompt_tokens_details.cached_tokens（缓存命中token数），usage.prompt_tokens_details.cache_write_tokens（新写入token数） | src: https://developers.openai.com/docs/api-reference/chat | quote: "cached_tokens: Cached tokens present in the prompt. cache_write_tokens: The unadjusted number of prompt tokens written to cache." | type: official
- [C9] 失效条件：TTL过期；或改动model、tool定义、output schema、reasoning settings | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cache entries expire after the TTL expires, or if the prefix changes due to: modified model, altered tool definitions, changed output schemas, or updated reasoning settings." | type: official
- [C10] 存储介质（早期模型）：key-value tensors；支持in_memory（~5-10分钟）或24小时选项 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Earlier models use prompt_cache_retention supporting in_memory (~5-10 minutes) or 24h" | type: official
- [C11] 存储介质（extended retention）：key-value tensors可offload到GPU存储 | src: https://developers.openai.com/api/docs/changelog | quote: "keeping cached prefixes active for longer, up to a maximum of 24 hours by offloading key/value tensors to GPU storage" | type: official
- [C12] 作用域：cache在组织级别共享，不跨组织；存储在单个机器，通过前256token的hash路由 | src: https://community.openai.com/t/prompt-caching-automatic/963981 | quote: "Prompt caching is scoped at the organization level...Caches are not shared across organizations" | type: secondary
- [C13] 显式API参数（GPT-5.6+）：prompt_cache_breakpoint（在content block上标记），prompt_cache_options.mode（设置implicit/explicit） | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "A content block can carry prompt_cache_breakpoint: { mode: \"explicit\" }" | type: official
- [C14] 支持模型范围：GPT-6系列（包括Astra、Sol、Luna）、GPT-5.6、GPT-5.5、GPT-5.4、GPT-4o及fine-tuned版本 | src: https://developers.openai.com/docs/models | quote: "GPT-6 Astra, GPT-6 Sol, GPT-6 Luna, GPT-5.6 Cyber, GPT-5.5, GPT-4o" | type: official
- [C15] 默认启用：caching对支持的模型自动启用，对隐式模式无需改代码 | src: https://community.openai.com/t/prompt-caching-automatic/963981 | quote: "Caching is automatic - you don't enable it, you don't request it. It just happens" | type: secondary
- [C16] 显式模式限制（早期模型）：GPT-5.5及更早版本仅支持隐式breakpoints，拒绝新的prompt_cache_options和prompt_cache_breakpoint字段 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Older models reject the new prompt_cache_options and prompt_cache_breakpoint fields" | type: official
- [C17] prompt_cache_key参数：用于优化早期模型的路由和cache命中，确保相同前缀的请求落到同一引擎 | src: https://community.openai.com/t/prompt-caching-automatic/963981 | quote: "A supplied prompt_cache_key can separate cache reuse between groups of requests and helps optimize cache routing" | type: secondary
- [C18] Prompt Caching仪表板（August 2026）：OpenAI发布官方仪表板，可跟踪cache命中率、cache reads per write、token分布 | src: https://developers.openai.com/api/docs/changelog | quote: "The Prompt Caching dashboard was released, allowing users to track your cache hit rate over time, cache reads per write, and the breakdown of cache-read, cache-write, and uncached tokens." | type: official

## conflicts
- [Conflict-1] 早期模型TTL：文档提到"in_memory (~5-10 minutes)"与"可配置为24小时"，但未明确指出哪些模型用哪个默认值。May 2026后只说organizations without ZDR默认24h，ZDR组织的行为未明确。

## gaps
- D3粒度：显式模式最多支持几个cache breakpoint？文档提到"up to 4 cache writes per request"但来源不确定
- D9存储作用域：是否有地域限制（例如美国/欧洲分别缓存）？
- D10资源管理：是否存在独立的cache资源对象可create/get/list/delete？文档未涉及
- 早期模型（GPT-5.5/GPT-5.4）的确切最小token数是否与GPT-5.6相同？
- 是否需要显式开通caching权限还是对所有组织默认启用？

## leads
- GPT-6 Sol/Luna（September 2026发布）缓存成本降低到90%，可能与GPT-5.6不同，建议后续跟进新模型的具体参数
- "Zero Data Retention"对caching行为的影响（TTL、存储位置）需要更详细的文档
- Azure OpenAI与标准OpenAI的caching参数是否相同？
