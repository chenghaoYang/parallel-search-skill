# r1-anthropic
question: Anthropic Claude API 的 prompt caching 是否仍必须由调用方在内容块上打 cache_control 断点？把 D1–D8 用一手原句填满。
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/about-claude/pricing, https://platform.claude.com/docs/en/api/messages, https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages

## claims
- [C1] D1：没有 cache_control 就不缓存。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages | quote: "if a request has no `cache_control` field (automatic or an explicit breakpoint), nothing is cached" | type: official
- [C2] D2：顶层一个 cache_control 即可，断点自动在最后可缓存块并前移。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Add a single `cache_control` field at the top level of your request. The system automatically applies the cache breakpoint to the last cacheable block and moves it forward as conversations grow." | type: official
- [C3] D2：也可把 cache_control 放在单个内容块上。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Place `cache_control` directly on individual content blocks" | type: official
- [C4] D2：type 只有 ephemeral，默认 5 分钟。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "\"ephemeral\" is the only supported cache type, which by default has a 5-minute lifetime." | type: official
- [C5] D2：ttl 为 "5m" 或 "1h"。页未见日期。 | src: https://platform.claude.com/docs/en/api/messages | quote: "ttl: optional \"5m\" or \"1h\"" | type: official
- [C6] D2：可标 tools 与 system 块。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Tools: Tool definitions in the `tools` array System messages: Content blocks in the `system` array" | type: official
- [C7] D2：最多 4 个断点。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "You can define up to 4 cache breakpoints" | type: official
- [C8] D2：不再要求 beta 前缀。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching no longer requires the beta prefix." | type: official
- [C9] D3：Fable 5.1、Mythos 5.1、Opus 5.5、Opus 5、Fable 5、Mythos 5 最小 512。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "512 tokens for Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Opus 5, Claude Fable 5, and Claude Mythos 5" | type: official
- [C10] D3：Mythos Preview、Opus 4.7 最小 2,048。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "2,048 tokens for Claude Mythos Preview and Claude Opus 4.7" | type: official
- [C11] D3：Opus 4.6、Opus 4.5 最小 4,096。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "4,096 tokens for Claude Opus 4.6 and Claude Opus 4.5" | type: official
- [C12] D3：Opus 4.8、Sonnet 5、Sonnet 4.6、Sonnet 4.5 最小 1,024。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "1,024 tokens for Claude Opus 4.8, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5" | type: official
- [C13] D3：Haiku 4.5 最小 4,096。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "4,096 tokens for Claude Haiku 4.5" | type: official
- [C14] D3：顺序为 tools、system、messages。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache prefixes are created in the following order: `tools`, `system`, then `messages`." | type: official
- [C15] D3：每个断点最多查 20 个位置。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The system checks at most 20 positions per breakpoint" | type: official
- [C16] D4：断点及之前的 block 一变，哈希就变。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "changing any block at or before the breakpoint produces a different hash on the next request." | type: official
- [C17] D4：改 tool 定义使整个 cache 失效。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Modifying tool definitions (names, descriptions, parameters) invalidates the entire cache" | type: official
- [C18] D5：默认寿命 5 分钟。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "By default, the cache has a 5-minute lifetime." | type: official
- [C19] D5：从 write 或 read 请求开始计时。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The lifetime is measured from the start of the request that writes or reads the cache entry, not from the end of its response." | type: official
- [C20] D5：另有 1 小时，加价。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Anthropic also offers a 1-hour cache duration at additional cost." | type: official
- [C21] D5：只写了首次写入与后续读取收费，没有 storage 单价。页未见日期。 | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "Cache write tokens are charged when content is first stored. Cache read tokens are charged when a subsequent request retrieves the cached content." | type: official
- [C22] D6：5 分钟写入 1.25 倍。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "5-minute cache write tokens are 1.25 times the base input tokens price" | type: official
- [C23] D6：1 小时写入 2 倍。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "1-hour cache write tokens are 2 times the base input tokens price" | type: official
- [C24] D6：读取 0.1 倍，脚注有例外。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache read tokens are 0.1 times the base input tokens price" | type: official
- [C25] D6：Fable 5.1 与 Mythos 5.1 为 0.025 倍。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache hits and refreshes on Claude Fable 5.1 and Claude Mythos 5.1 are priced at 0.025x the base input price." | type: official
- [C26] D6：Opus 5.5 为 0.05 倍。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache hits and refreshes on Claude Opus 5.5 are priced at 0.05x the base input price." | type: official
- [C27] D7：两个字段都为 0 则未缓存。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "if both `cache_creation_input_tokens` and `cache_read_input_tokens` are 0, the prompt was not cached" | type: official
- [C28] D7：1 小时写入字段是 ephemeral_1h_input_tokens。页未见日期。 | src: https://platform.claude.com/docs/en/api/messages | quote: "ephemeral_1h_input_tokens: number" | type: official
- [C29] D8：自动和显式都支持全部 active 模型。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching (both automatic and explicit) is supported on all active Claude models." | type: official
- [C30] D8：POST https://api.anthropic.com/v1/messages。页未见日期。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "curl https://api.anthropic.com/v1/messages" | type: official

## conflicts
- 同页 https://platform.claude.com/docs/en/build-with-claude/prompt-caching ：FAQ “expire after a minimum of 5 minutes of inactivity.” vs C19 的 “measured from the start of the request”。不裁决。
- thinking “without explicit `cache_control` markers”（同上）vs mid-conversation “nothing is cached”（https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages）。不裁决。

## gaps
- 四页无 Updated。未见 `prompt-caching-2024-07-31` / `extended-cache-ttl-2025-04-11` 在 /v1/messages 上是必填还是废弃。
- 无 storage 单价原句。内存句：“held in memory only and are not stored at rest”。
- 未立项：text/image/tool result 可标；Haiku 3.5 为 2,048；1,024 组后还有 Opus 4.1、Opus 4、Sonnet 4；过短不缓存；4 断点满则 400；须 100% identical；读则免费刷新。

## leads
- 旧 Bedrock（Opus 4.6 及更早）顶层 cache_control 返回 400。1h 点名 Claude API、Bedrock、Google Cloud、Foundry。
- 已开缓存时 server tool 结果自动打 5 分钟断点，写入进 ephemeral_5m_input_tokens。
