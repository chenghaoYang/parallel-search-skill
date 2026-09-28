# r1-anthropic
question: Anthropic 官方现在的 prompt caching：是否仍必须在请求里打 cache_control 断点，还是已经有不用改代码的自动缓存；以及断点、门槛、命中字段、读写倍率、TTL、失效、模型和端点。
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/about-claude/pricing, https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages, https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching, https://platform.claude.com/docs/en/release-notes/overview, https://docs.claude.com/en/docs/build-with-claude/prompt-caching

## claims
- [C1] D1：没有 `cache_control` 就不缓存，并按普通 input 计价。 | src: https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages | quote: "if a request has no cache_control field (automatic or an explicit breakpoint), nothing is cached and every request pays the regular input token price" | type: official
- [C2] D1：自动缓存仍要在请求体顶层放一个 `cache_control`，断点打在最后一个可缓存块。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "add a single `cache_control` field at the top level of your request body. The system automatically applies the cache breakpoint to the last cacheable block." | type: official
- [C3] D1：断点随每个请求移到最后一个可缓存块。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "automatically moves to the last cacheable block in each request" | type: official
- [C4] D1：2026-02-19 发布该顶层自动缓存。 | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "We've launched automatic caching for the Messages API." | type: official
- [C5] D1：无 prompt caching 的请求不会得到 server-tool 自动断点。 | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching | quote: "Requests without prompt caching do not receive the automatic breakpoint." | type: official
- [C7] D2：缓存的是含断点块在内的前缀，顺序 `tools`、`system`、`messages`。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "`tools`, `system`, and `messages` (in that order), up to and including the block designated with `cache_control`." | type: official
- [C8] D2：自动缓存与显式断点共用 20-block lookback。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "the 20-block lookback window all apply the same as with explicit breakpoints." | type: official
- [C9] D3：短于门槛即使有 `cache_control` 也不缓存。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Shorter prompts cannot be cached, even if marked with `cache_control`." | type: official
- [C10] D4：`cache_creation_input_tokens` 与 `cache_read_input_tokens` 都为 0 就是没缓存。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "if both `cache_creation_input_tokens` and `cache_read_input_tokens` are 0, the prompt was not cached" | type: official
- [C11] D3：512 tokens：Fable 5.1、Mythos 5.1、Opus 5.5、Opus 5、Fable 5、Mythos 5。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "512 tokens for Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Opus 5, Claude Fable 5, and Claude Mythos 5" | type: official
- [C12] D3：Mythos Preview 与 Opus 4.7 的门槛是 2,048 tokens。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "2,048 tokens for Claude Mythos Preview and Claude Opus 4.7" | type: official
- [C13] D3：1,024 tokens：Opus 4.8、Sonnet 5、Sonnet 4.6、Sonnet 4.5、Opus 4.1。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "1,024 tokens for Claude Opus 4.8, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.1" | type: official
- [C14] D4：`input_tokens` 是最后一个断点之后的 token。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "tokens after the last cache breakpoint" | type: official
- [C15] D4：`cache_creation_input_tokens` 等于 `cache_creation` 对象各项之和。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "the current `cache_creation_input_tokens` field equals the sum of the values in the `cache_creation` object." | type: official
- [C16] D5：读价为 base input 的 10%；Fable 5.1 与 Mythos 5.1 为 2.5%；Opus 5.5 为 5%。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "10% of base input token price, or 2.5% on Claude Fable 5.1 and Claude Mythos 5.1, and 5% on Claude Opus 5.5" | type: official
- [C19] D6：5 分钟写入是 base input 的 1.25 倍。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "5-minute cache write tokens are 1.25 times the base input tokens price" | type: official
- [C20] D6：1 小时写入是 base input 的 2 倍。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "1-hour cache write tokens are 2 times the base input tokens price" | type: official
- [C21] D7：自动缓存默认 5 分钟；可指定 1 小时，写价 2x base input。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "By default, automatic caching uses a 5-minute TTL. You can specify a 1-hour TTL at 2x the base input token price" | type: official
- [C22] D7：每次使用缓存内容都会刷新，原句为 no additional cost。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The cache is refreshed for no additional cost each time the cached content is used." | type: official
- [C23] D7：寿命从写出或读出该条目的请求开始时算，不是从响应结束时算。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "measured from the start of the request that writes or reads the cache entry, not from the end of its response." | type: official
- [C24] D6：缓存表示只在内存，不落盘。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "held in memory only and are not stored at rest." | type: official
- [C25] D7：2025-08-13 起 1 小时缓存不再需要 beta header。 | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "The 1-hour cache duration for prompt caching no longer requires a beta header." | type: official
- [C26] D8：`tools` → `system` → `messages`，改一层则该层及之后失效。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Changes at each level invalidate that level and all subsequent levels." | type: official
- [C27] D8：命中要求 prompt 片段 100% 相同。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache hits require 100% identical prompt segments" | type: official
- [C29] D9：自动与显式都支持所有 active Claude models。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching (both automatic and explicit) is supported on all active Claude models." | type: official
- [C30] D9：可与 Batches API 同用，命中是 best-effort。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "cache hits are provided on a best-effort basis." | type: official
- [C31] D9：现行 FAQ 写 prompt caching 不再需要 beta 前缀。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching no longer requires the beta prefix." | type: official

## conflicts
- FAQ："Cached prefixes automatically expire after a minimum of 5 minutes of inactivity." 同页还有 1 小时 TTL，且寿命从请求开始算。刷新写 "no additional cost"，定价列名是 "Cache hits and refreshes"。未裁决。src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- "This caching behavior occurs even without explicit cache_control markers." 与 C1 冲突。该句在 thinking 小节。src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- 功能页写 prompt caching "is ZDR eligible"；2026-09-01 notes 写 Fable 5.1 / Mythos 5.1 默认不能 ZDR。src: https://platform.claude.com/docs/en/release-notes/overview

## gaps
- 同页还有未单独引用的门槛：4,096（Opus 4.6、Opus 4.5、Haiku 4.5）、2,048（Haiku 3.5），以及最多 4 个断点。
- 示例端点 `https://api.anthropic.com/v1/messages`；字段在 `usage` / 流式 `message_start`。未见单独存储单价。未打开 API schema。1h beta 上线日早于 2025-08-13，notes 里没有。

## leads
- 旧版 Bedrock（Opus 4.6 及更早）对顶层 `cache_control` 返回 400。预热用 `max_tokens: 0` 加显式断点。

