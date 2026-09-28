# r1-kimi-zhipu

question: (A) Moonshot Kimi API 的 Context Caching 现在的机制是什么？(B) 智谱 GLM API 的缓存现在的机制是什么？

checked: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api, https://platform.kimi.ai/docs/pricing/chat-k3, https://platform.kimi.ai/docs/api/chat, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8

## claims

### Moonshot Kimi

- [C1] Kimi API Context Caching 自动触发，无需显式创建 cache_id。当 prompt_cache_options 为空时，系统默认使用 5 分钟 TTL，或可通过参数指定 TTL | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "when prompt_cache_options is omitted, the system uses the 5m TTL by default" | type: official

- [C2] Kimi K3 触发缓存的最少 token 数是 256。如果前一个请求的 prompt tokens 少于 256，则请求不会被缓存 | src: https://platform.kimi.ai/docs/api/chat | quote: "A new request can hit the prefix cache only when the previous request's prompt tokens exceed 256" | type: official

- [C3] Kimi K3 缓存折扣：缓存输入价格 $0.30/百万 tokens，非缓存输入 $3.00/百万 tokens，相当于 90% 的折扣 | src: https://platform.kimi.ai/docs/pricing/chat-k3 | quote: "cached inputs cost just $0.30 per million tokens versus $3.00 for uncached input—a 90% savings on repeated content" | type: official

- [C4] Kimi 缓存写入费用：5 分钟 TTL 和 1 小时 TTL 的缓存写入都是 $6.00/百万 tokens，缓存命中时无额外写入费用 | src: https://platform.kimi.ai/docs/pricing/chat-k3 | quote: "cache writes are billed separately per TTL tier (5min / 1h); cached input is billed at the cache-hit price only, with no additional cache write charge" | type: official

- [C5] Kimi TTL 选项为 5 分钟和 1 小时。缓存条目在至少 5 分钟不活动后自动过期，不支持手动清除 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "cached prefixes expire automatically after at least 5 minutes of inactivity. Manual cache clearing is not supported" | type: official

- [C6] Kimi 响应 usage 字段分别报告缓存 token、写入 token 和非缓存输入 token，允许开发者跟踪缓存命中效率 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "Track performance via API response usage fields, which separately report cached tokens, write tokens, and uncached input tokens" | type: official

- [C7] Kimi 缓存失效条件：仅当前缀完全匹配时才命中；前缀内的任何改动会导致缓存从该点开始失效。改变 tool_choice 不会失效缓存，但改变 reasoning_effort 级别会导致缓存失效 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "any change within the prefix invalidates the cache from that point onward. Changing tool_choice does not invalidate the prefix cache. However, switching reasoning effort levels invalidates prefix-cache hits" | type: official

- [C8] Kimi 不存在独立的缓存管理 API。缓存通过 prompt_cache_options 参数（Chat Completions/Responses API）或 cache_control（Messages API）隐式管理，无 POST /v1/caching 等显式创建接口 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "Specify TTL by passing prompt_cache_options with your desired duration (Chat Completions/Responses APIs) or cache_control (Messages API)" | type: official

### 智谱 GLM

- [C9] 智谱 GLM API 实现隐式上下文缓存，自动识别重复内容，无需手动配置 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "隐式缓存，智能识别重复的上下文内容，无需手动配置" | type: official

- [C10] 智谱 GLM 触发缓存的最少 token 数：重复前缀内容必须足够长，建议 500 tokens 以上 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "重复的前缀内容必须足够长（建议 500 Token 以上）" | type: official

- [C11] 智谱 GLM 缓存折扣：缓存 token 通常按标准费率的 50% 计费。示例显示缓存可降低整体成本 24% | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "Cached tokens receive discounted pricing—typically 50% of standard rates. In the provided example, context caching reduced costs by 24%" | type: official

- [C12] 智谱 GLM 响应中，缓存命中的 token 数通过 usage.prompt_tokens_details.cached_tokens 字段显示 | src: https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8 | quote: "cached_tokens: type number, description: 命中的缓存 Token 数量" | type: official

- [C13] 智谱 GLM 缓存以异步方式生效，在初始请求之后稍等片刻可提高后续缓存命中率 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "Caching is asynchronously effective; results improve when waiting briefly between initial and subsequent requests" | type: official

- [C14] 智谱 GLM 不存在独立的缓存管理 API。缓存功能隐式整合在聊天补全 API 中，无显式的创建/删除/查询缓存对象的端点 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "The current implementation appears to be integrated into the standard chat completions endpoint" | type: secondary

## conflicts

- Moonshot Kimi 在 2024 年历史上曾提供过显式 cache_id 管理机制（POST /v1/caching），但当前（2026）文档只显示隐式自动缓存，无需手动创建 cache 对象。这是重要的机制变化，但官方文档未明确说明版本变更时间。

## gaps

- **Kimi storage**: 文档未明确描述缓存的物理存储方式
- **Kimi scope**: 未明确说明缓存是按 API key 隔离、按账户隔离还是跨账户共享
- **Zhipu TTL**: 文档未明确指定缓存的具体存活时长（是否有 TTL，多久过期）
- **Zhipu storage**: 文档未明确描述存储方式
- **Zhipu invalidate**: 文档未明确列举哪些前缀改动会导致缓存失效
- **Zhipu scope**: 文档未明确说明缓存隔离范围

## leads

- Moonshot Kimi 显式 cache_id 机制是否在某个版本中被弃用：建议查阅平台 changelog（https://platform.kimi.ai/docs/platform-changelog）确认机制变更时间
- 智谱 GLM 缓存的 TTL 和过期机制可能需要查看技术博客或开发者论坛的实际案例
- 两个平台关于按账户隔离的说明需要在 API 密钥管理和认证文档中确认