# r1-anthropic
question: Anthropic Claude API 的 prompt caching（cache_control breakpoints）机制，在以下 10 个维度上分别是什么？
checked: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching,https://claude.com/blog/token-saving-updates,https://www.anthropic.com/news/token-saving-updates

## claims
- [C1] Anthropic 支持自动缓存模式（automatic caching）：在请求顶级添加单个 `cache_control` 字段，系统自动在最后一个可缓存块上放置断点，会话增长时自动向前移动。不需要在每个块上手动插入。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Add a single cache_control field at the request's top level. The system automatically places the cache breakpoint on the last cacheable block and moves it forward as conversations grow." | type: official
- [C2] Anthropic 也支持显式缓存断点（explicit cache breakpoints）：在单个内容块上放置 cache_control，对不同频率变化的部分实现细粒度控制。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Place cache_control directly on individual content blocks to cache different sections that change at different frequencies." | type: official
- [C3] 最小可缓存长度因模型而异：Claude Fable 5.1、Mythos 5.1、Opus 5.5、Opus 5：512 tokens；Claude Sonnet 5、Opus 4.8、Sonnet 4.6：1,024 tokens；Claude Opus 4.7：2,048 tokens；Claude Opus 4.6、4.5、Haiku 4.5：4,096 tokens。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "512 tokens for Claude Opus 5.5, Fable 5.1, Mythos 5.1 ... 1,024 tokens for Claude Sonnet 5, Opus 4.8 ... 2,048-4,096 tokens for older models" | type: official
- [C4] 最多能在单个请求中放置 4 个 cache_control 断点。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "You can define up to 4 cache breakpoints if you want to cache different sections that change at different frequencies" | type: official
- [C5] 缓存读取成本自 2026-09-01 起为 0.1x base input tokens（大多数模型）或 0.025x base input tokens（Claude Fable 5.1、Claude Mythos 5.1），相对原价打 10% 或 2.5% 折扣。| src: https://www.anthropic.com/news/token-saving-updates | quote: "the cache read rate is model-dependent: it is 0.1 of the base input rate on most Claude models and 0.025 on Claude Fable 5.1 and Claude Mythos 5.1" (via WebSearch) | type: official
- [C6] 缓存写入成本：5 分钟 TTL 为 1.25x base input tokens；1 小时 TTL 为 2x base input tokens。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Cache writes cost 1.25x base input (5m) or 2x base input (1h)" | type: official
- [C7] 缓存 TTL 有两个选项：默认 5 分钟（类型 ephemeral），可选 1 小时（需设置 ttl: "1h"，成本为 2x）。无需特殊 beta header 即可使用 1 小时 TTL。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "5-minute TTL (default): {\"type\": \"ephemeral\"} ... 1-hour TTL: {\"type\": \"ephemeral\", \"ttl\": \"1h\"} (2x base input price)" | type: official
- [C8] TTL 从请求开始时刻计算，不是从响应完成时刻计算。缓存续命机制：在 TTL 内重新使用相同前缀会自动续期（免费）。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Lifetime measured from request start, not response end ... cache refreshed free when reused" | type: official
- [C9] 响应中用于追踪缓存命中的字段名：cache_read_input_tokens（从缓存读取的 token 数）、cache_creation_input_tokens（写入缓存的 token 数）、input_tokens（最后一个断点后的 token 数）。总输入 token = cache_read_input_tokens + cache_creation_input_tokens + input_tokens。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "cache_read_input_tokens: Tokens read from cache ... cache_creation_input_tokens: Tokens written to cache ... input_tokens: Tokens after last breakpoint" | type: official
- [C10] 缓存失效条件：Tool definitions 改动、System prompt 改动（某些新模型可通过添加系统消息而不失效）、Images/documents 添加或移除、tool_choice 参数改动、Speed 设置改动、Effort 设置改动、Thinking parameters 改动。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Changes that invalidate the cache: Tools array modifications ... System prompt changes ... Images/documents additions ... Tool choice parameter changes ... Thinking configuration or effort settings" | type: official
- [C11] Anthropic Claude 缓存适用于所有活跃模型：Claude Fable 5.1、Claude Mythos 5.1、Claude Fable 5、Claude Mythos 5、Claude Opus 5.5、Claude Opus 5、Claude Opus 4.8、Claude Sonnet 5、Claude Sonnet 4.6、Claude Haiku 4.5 等。官方文档明确说"prompt caching is supported on all active Claude models"。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "prompt caching is supported on all active Claude models" | type: official
- [C12] 缓存隔离范围：缓存按 workspace 隔离（在 Claude API、AWS、Microsoft Foundry 平台上）。不同组织不会共享缓存，即使提示完全相同。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Caches are isolated per workspace on Claude API, AWS, and Microsoft Foundry. Different organizations never share caches, even with identical prompts." | type: official
- [C13] 缓存存储介质：KV（key-value）缓存表示和缓存内容的加密哈希仅保存在内存中，不持久化存储。| src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "KV cache representations and cryptographic hashes of cached content are held in memory only and are not stored at rest" (via WebSearch) | type: official

## conflicts

## gaps
- 是否支持跨不同 API key 或不同用户的缓存共享（只查到不跨组织共享，未查到同组织内不同 API key 的隔离规则）
- 缓存 TTL 续命的具体机制细节（是否重新计时、是否可以多次续期）
- 自动缓存功能的确切发布时间（WebSearch 提到"February 2026"，但未从官方文档直接确认）
- 旧模型（已停用的 Opus 4.1、Opus 4、Sonnet 4、Haiku 3.5）是否仍支持缓存功能
- lookback window 限制（最多回溯 20 块）是否对所有模型一致

## leads
- 自动缓存（simplied prompt caching）在 2026 年 2 月推出，相比手动断点管理大幅降低开发复杂度
- 缓存读取定价在 2026 年 9 月优化到 0.1x-0.025x，显著降低缓存使用成本
- 新模型支持 mid-conversation 系统消息添加而不失效缓存（需要特定 beta header），改善了缓存续命灵活性
