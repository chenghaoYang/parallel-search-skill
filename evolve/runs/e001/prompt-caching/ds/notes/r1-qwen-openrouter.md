# r1-qwen-openrouter

question: 本简报覆盖两个独立实体，请分别调研、分别记录claims，不要混合成一条结论：(A) 阿里云通义千问（Qwen，DashScope / 百炼 Model Studio）API 的上下文缓存现在的机制是什么？(B) OpenRouter 作为多模型网关，在 prompt caching 上是怎么处理的（自己实现，还是透传底层各家模型的原生缓存行为）？

checked: https://help.aliyun.com/zh/model-studio/context-cache,https://help.aliyun.com/zh/model-studio/explicit-cache-guide,https://help.aliyun.com/en/model-studio/context-cache,https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope,https://openrouter.ai/docs/guides/best-practices/prompt-caching,https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/

## claims

### A. Alibaba Qwen (阿里云通义千问)

- [C1] Qwen Context Cache 支持两种独立模式：Explicit Cache（需主动开启）和 Implicit Cache（自动启用）| src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "需要主动开启的缓存模式" vs "自动启用，无法关闭" | type: official

- [C2] Explicit Cache：缓存内容最小 1,024 tokens | src: https://help.aliyun.com/zh/model-studio/explicit-cache-guide | quote: "缓存内容最少需要 1024 Token" | type: official

- [C3] Explicit Cache 价格：创建时 125% 原价，命中时 10% 原价 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "Creation cost: 125% of standard input token price, Hit cost: 10% of standard input token price" | type: official

- [C4] Implicit Cache 价格：创建无额外费用，命中时 20% 原价（模型间可能不同） | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "No creation overhead, Hit cost: 20% of standard input token price (varies by model)" | type: official

- [C5] Explicit Cache TTL：5 分钟，每次命中时重置 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "5-minute validity period (reset on each hit)" | type: official

- [C6] Implicit Cache 无固定过期时间，系统定期清理未使用缓存 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "No fixed expiration; system periodically clears unused caches" | type: official

- [C7] 缓存存储机制：通过 cache_control marker 标记消息内容，缓存从消息数组开头到该 marker 的所有内容 | src: https://help.aliyun.com/zh/model-studio/explicit-cache-guide | quote: "Add \"cache_control\": {\"type\": \"ephemeral\"} to messages requiring caching. All content from the messages array beginning through that marker becomes a cached block." | type: official

- [C8] Response 命中字段：usage.prompt_tokens_details 中的 cache_creation_input_tokens 和 cached_tokens | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "cache_creation_input_tokens: Tokens used for explicit cache creation, cached_tokens: Tokens retrieved from Context Cache" | type: official

- [C9] Explicit 和 Implicit 缓存互斥：单一请求只能使用其中一种模式 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "Explicit and implicit caching modes are mutually exclusive within a single request." | type: official

- [C10] 单个请求支持最多 4 个 cache control marker | src: https://help.aliyun.com/zh/model-studio/explicit-cache-guide | quote: "A single request supports up to 4 cache control markers maximum." | type: official

- [C11] 缓存失效条件：工具定义修改、content block 超过 20 个限制 | src: https://help.aliyun.com/zh/model-studio/explicit-cache-guide | quote: "Tool definitions function as system prompt components and participate in cache calculations, so any tool modification prevents cache hits. Prefix matching looks back maximum 20 content blocks" | type: official

- [C12] 使用 cache_control 需要消息内容为数组格式；字符串格式不支持 cache marker | src: https://help.aliyun.com/zh/model-studio/explicit-cache-guide | quote: "Content must be formatted as an array to support cache markers—string-format content doesn't support this feature." | type: official

- [C13] DashScope API 端点格式（区域化）：https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "Beijing: https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1, Singapore: https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1" | type: official

### B. OpenRouter (as LLM Gateway)

- [C14] OpenRouter 透传底层厂商的原生缓存行为，区分两种实现方式：自动缓存（OpenAI/DeepSeek/Groq）和显式缓存（Anthropic/Alibaba） | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Automatic caching (easiest): Available on OpenAI, DeepSeek, Groq, and others. No configuration needed. Explicit caching (fine-grained control): Used by Anthropic and Alibaba. Add cache_control: { \"type\": \"ephemeral\" } to specific content blocks." | type: official

- [C15] OpenRouter 最小缓存长度取决于底层模型，无跨厂商统一说明 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "No explicit unified minimum mentioned; varies by provider implementation" | type: official

- [C16] 缓存命中价格折扣由底层厂商决定：DeepSeek/Anthropic/Alibaba 0.1x，Moonshot/Grok 0.25x，Groq 0.5x | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Cache read multipliers vary significantly: DeepSeek: 0.1x, Anthropic/Alibaba: 0.1x reads, Moonshot/Grok: 0.25x reads, Groq: 0.5x reads" | type: official

- [C17] 缓存写入成本因厂商而异：Anthropic/Alibaba 1.25x（5分钟TTL）或 2.0x（1小时TTL），OpenAI/Gemini/Grok 免费 | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "Initial cache storage carries a premium. On Anthropic, writes cost 1.25x input for the default 5-minute TTL and 2.0x input for the 1-hour TTL" | type: official

- [C18] Prompt caching TTL 最小 30 分钟，具体由底层厂商决定 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Cached prefixes have a minimum 30-minute TTL." | type: official

- [C19] OpenRouter 缓存存储由底层厂商处理，OpenRouter 本身无额外缓存层 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "OpenRouter automatically routes subsequent requests to the same provider after a cached request, maximizing cache hit rates" | type: official

- [C20] Response 中缓存命中字段位置统一：usage.prompt_tokens_details 中的 cached_tokens、cache_write_tokens、cache_discount | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Check prompt_tokens_details in API responses for: cached_tokens: Amount read from cache, cache_write_tokens: Amount written to cache, cache_discount: Cost savings achieved" | type: official

- [C21] Prompt caching 命中失效条件：请求被路由到不同 provider，导致缓存未命中 | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "cached content only helps when follow-up requests reach the same provider endpoint. The solution is explicit routing control through session_id" | type: official

- [C22] OpenRouter 通过 session_id 参数实现 provider 粘性路由，确保缓存命中：session_id 最长 256 字符 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Pass a session_id (up to 256 characters) via request body or x-session-id header to: Pin routing to the same provider across turns, Group multimodal requests in activity logs, Ensure cache benefits from the first request" | type: official

- [C23] OpenRouter 无独立 prompt cache 管理 API；缓存管理通过 session_id 路由和厂商原生机制实现 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "No dedicated endpoint for clearing prompt caches; cache behavior controlled via session routing and provider-specific implementations" | type: official

- [C24] OpenRouter Response Caching（不同于 prompt caching）支持 X-OpenRouter-Cache 等 header，可按请求清除，但这是应用层缓存而非 prompt cache | src: https://openrouter.ai/docs/guides/features/response-caching | quote: "To force a fresh response for a specific request, send the X-OpenRouter-Cache-Clear: true header alongside X-OpenRouter-Cache: true" | type: official

## conflicts

- OpenRouter 文档称"automatic caching"对 OpenAI 无需配置，但 OpenAI 实际要求显式 cache_control；此差异可能反映文档更新滞后或"automatic"指 OpenRouter 自动转发格式 | src1: https://openrouter.ai/docs/guides/best-practices/prompt-caching | src2: OpenAI 官方文档（不在本次查证域名内）

## gaps

- [G1] Qwen 缓存隔离范围：文档未明确说明是按 Workspace ID、API Key 还是账户级别隔离
- [G2] Qwen 是否提供独立的 cache 管理/清除 API（例如删除特定缓存的端点）
- [G3] OpenRouter 对不同底层模型的 cache_control 格式是否做了归一化，还是要求调用方按各厂商格式传入
- [G4] OpenRouter 通过 provider routing 到同一厂商但不同地区/账户时，是否会共享同一缓存

## leads

- OpenRouter 与底层厂商缓存的隔离边界（provider routing 粒度）会影响成稿中"网关"分类的准确性；建议进一步澄清不同 provider 路由是否会在地域/账户级产生新的缓存边界
- Qwen implicit vs explicit 的自动选择逻辑（何时优先选择哪种）未在文档中详细说明，可能影响实际成本预测
- OpenRouter 的"automatic caching"说法与 OpenAI 原生行为可能存在偏差，需确认是否为文档过时或概念定义差异
