# r1-anthropic
question: Anthropic Claude API 的 Prompt Caching（cache_control）现在的机制是什么？
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching,https://platform.claude.com/docs/en/about-claude/pricing,https://platform.claude.com/docs/en/release-notes/overview

## claims
- [C1] trigger: 支持自动缓存（请求级别单个 cache_control 字段）和显式缓存断点（块级别 cache_control）两种方式 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Add a single `cache_control` field at the request level / Place `cache_control` directly on individual content blocks" | type: official
- [C2] trigger: 2026 年 2 月 19 日发布自动缓存功能，自动管理断点位置 | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "Automatic caching for the Messages API eliminates manual cache breakpoint management" | type: official
- [C3] min_len: 512 tokens 适用于 Claude Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Fable 5, Mythos 5 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "512 tokens: Claude Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Fable 5, Mythos 5" | type: official
- [C4] min_len: 1024 tokens 适用于 Opus 4.8, Sonnet 5, Sonnet 4.6 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "1,024 tokens: Opus 4.8, Sonnet 5, Sonnet 4.6" | type: official
- [C5] min_len: 4096 tokens 适用于 Opus 4.5, Haiku 4.5 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "4,096 tokens: Opus 4.5, Haiku 4.5" | type: official
- [C6] discount: cache read 价格为 0.1x base input（例 Sonnet 5/$0.20 per MTok） | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "Cache hits and refreshes on Claude Sonnet 5 are priced at 0.1x base input price" | type: official
- [C7] discount: Opus 5.5 cache read 价格为 0.05x base input（$0.20 per MTok） | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "Cache hits and refreshes on Claude Opus 5.5 are priced at 0.05x the base input price ($0.20 / MTok)" | type: official
- [C8] discount: Fable 5.1/Mythos 5.1 cache read 价格为 0.025x base input（$0.25 per MTok） | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "Cache hits and refreshes on Claude Fable 5.1 and Claude Mythos 5.1 are priced at 0.025x the base input price" | type: official
- [C9] discount: 5-minute cache write 倍数为 1.25x base input price | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "5-minute cache write: 1.25x base input price" | type: official
- [C10] discount: 1-hour cache write 倍数为 2x base input price | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "1-hour cache write: 2x base input price" | type: official
- [C11] ttl: 默认 TTL 为 5 分钟，无附加成本 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "5-minute (default): Automatic, no additional cost" | type: official
- [C12] ttl: 可通过 cache_control 参数 "ttl": "1h" 设置 1 小时 TTL | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "1-hour: Specified with `\"ttl\": \"1h\"`, costs 2x the base input price" | type: official
- [C13] ttl: cache hit 时自动刷新 TTL，相同时长内无额外成本 | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "Cache hits and refreshes: Reading a prompt prefix from the prompt cache, which also refreshes it / Same duration as the preceding write" | type: official
- [C14] storage: 官方文档中未明确描述缓存存储方式（内存/磁盘） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: N/A | type: official
- [C15] confirm: response.usage.cache_read_input_tokens 字段显示从缓存读取的 token 数 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "cache_read_input_tokens: Tokens read from cache" | type: official
- [C16] confirm: response.usage.cache_creation_input_tokens 字段显示写入缓存的 token 数 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "cache_creation_input_tokens: Tokens written to cache" | type: official
- [C17] invalidate: tool definitions 修改导致失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Tool definitions modified" | type: official
- [C18] invalidate: web search/citations 切换导致失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Web search/citations toggle" | type: official
- [C19] invalidate: speed setting 变更导致失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Speed setting changes" | type: official
- [C20] invalidate: images added/removed 导致失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Images added/removed" | type: official
- [C21] invalidate: thinking configuration 变更导致失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Thinking configuration changed" | type: official
- [C22] invalidate: tool_choice parameter 变更导致失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Tool choice parameter changed" | type: official
- [C23] invalidate: effort setting 变更导致失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Effort setting changed" | type: official
- [C24] invalidate: breakpoint 最多 4 个（explicit cache breakpoints） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Maximum 4 explicit breakpoints per request" | type: official
- [C25] invalidate: lookback window 为 20 blocks | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Lookback Window: 20 blocks for cache hit detection" | type: official
- [C26] invalidate: breakpoint 放置在 tools→system→messages 层级，上层变更导致下层失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache follows hierarchical structure: `tools` → `system` → `messages`. Changes at each level invalidate that level and all subsequent levels" | type: official
- [C27] scope: 缓存不跨 organization/workspace 共享 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Organization isolation: Caches don't share across organizations or workspaces" | type: official
- [C28] scope: API key 隔离范围未明确说明 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: N/A | type: official
- [C29] api: 无独立的缓存管理 API，仅通过请求中 cache_control 参数控制 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Add a single `cache_control` field / Place `cache_control` directly on individual content blocks" | type: official

## conflicts
N/A

## gaps
- [G1] 不同 API key 是否可共享缓存前缀（scope 在 API key 粒度的隔离）
- [G2] 5-minute 和 1-hour TTL 的缓存存储方式是否有区别
- [G3] 缓存是否可手动删除或清空（如果无独立 API）

## leads
- Cache diagnostics beta (May 13, 2026): `diagnostics={"previous_message_id": "msg_id"}` 可诊断缓存失效原因，需要 header: `cache-diagnosis-2026-04-07`
- Thinking blocks 现在可作为前置 assistant turns 的一部分被缓存（但不支持显式 cache_control on thinking blocks）
- Claude Opus 4.8 及之前 minimum cacheable length 更长（1024-4096 tokens），应优先使用新模型以获得 512-token 门槛
