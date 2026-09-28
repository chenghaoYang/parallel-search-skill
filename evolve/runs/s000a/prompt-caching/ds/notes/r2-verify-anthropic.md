# r2-verify-anthropic
question: Anthropic 现行官方文档里，启用 prompt caching 是否仍然必须在请求中出现 cache_control；顶层 cache_control 会不会自动移动断点；完全不传该字段时官方有没有写「不会缓存」。并与 2025-08 快照对照，判断是版本差异还是现行页自相矛盾。
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/api/messages/create, https://platform.claude.com/docs/en/release-notes/overview, https://web.archive.org/web/20250803210544/https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching

## claims
- [C1] 现行指南把启用写成两种方式：automatic（顶层 `cache_control` 字段）与 explicit（块级 `cache_control`），两条路径都要求该字段出现 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Automatic caching: Add a single `cache_control` field at the top level of your request." | type: official
- [C2] 顶层 `cache_control` 会让断点自动落在最后一个可缓存块并随对话前移（D4 成立） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The cache breakpoint automatically moves to the last cacheable block in each request, so you don't need to update any `cache_control` markers as the conversation grows." | type: official
- [C3] Messages API reference 把 `cache_control` 列为顶层 body 参数（optional CacheControlEphemeral or null），语义同自动断点 | src: https://platform.claude.com/docs/en/api/messages/create | quote: "Top-level cache control automatically applies a cache_control marker to the last cacheable block in the request." | type: official
- [C4] 现行 FAQ 仍要求至少一个 `cache_control`（顶层或块级）才启用缓存 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Alternatively, include at least one `cache_control` breakpoint on individual content blocks" | type: official
- [C5] `cache_control` 内 `ttl` 枚举为 "5m"/"1h"，默认 5m（API reference，块级与顶层同型） | src: https://platform.claude.com/docs/en/api/messages/create | quote: "ttl: optional "5m" or "1h"" | type: official
- [C6] release notes 记载 automatic caching（顶层 `cache_control`）上线日为 2026-02-19，Claude API 与 Microsoft Foundry (preview) | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "February 19, 2026 ... We've launched automatic caching for the Messages API. Add a single `cache_control` field to your request body" | type: official
- [C7] release notes 记载 1 小时缓存于 2025-08-13 起不再需要 beta header（旧快照之后 10 天） | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "The 1-hour cache duration for prompt caching no longer requires a beta header." | type: official
- [C8] 2025-08-03 快照：当时启用缓存要求「至少一个 `cache_control` breakpoint」，只有块级断点一种写法，无顶层字段 | src: https://web.archive.org/web/20250803210544/https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching | quote: "To enable prompt caching, include at least one `cache_control` breakpoint in your API request." | type: official
- [C9] 2025-08-03 快照：1h 缓存当时是 beta，须带 header `extended-cache-ttl-2025-04-11` 并在 `cache_control` 里写 `ttl` | src: https://web.archive.org/web/20250803210544/https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching | quote: "add `extended-cache-ttl-2025-04-11` as a beta header to your request, and then include `ttl` in the `cache_control` definition" | type: official
- [C10] automatic caching 边缘情况：末块已有不同 TTL 的 `cache_control`、或 4 个显式断点已满，API 返回 400 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "If the last block has an explicit `cache_control` with a different TTL, the API returns a 400 error." | type: official
- [C11] automatic caching 末块不合格时系统向前找最近合格块，找不到则跳过缓存 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "If the last block is not eligible as an automatic cache breakpoint target, the system silently walks backward to find the nearest eligible block. If none is found, caching is skipped." | type: official
- [C12] 顶层 `cache_control` 在 legacy Amazon Bedrock（Opus 4.6 及更早）上返回 400，属平台例外而非矛盾 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "the API returns a 400 error for a top-level `cache_control` field" | type: official
- [C13] 现行页最接近「不缓存」的明文只针对低于最小 token 数的请求，不针对缺省 `cache_control` 字段 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Any requests to cache fewer than this number of tokens will be processed without caching, and no error is returned." | type: official
- [C14] 现行页承认 server tools（如 web search）可产生用户未请求的 `ephemeral_5m_input_tokens` 写入，即无 `cache_control` 也可能有缓存写 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "If you see `ephemeral_5m_input_tokens` writes you didn't request while using server tools such as web search" | type: official
- [C15] thinking blocks 不能标 `cache_control` 但可随其他内容被缓存，说明「无标记块也可进入缓存」 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "This caching behavior occurs even without explicit `cache_control` markers" | type: official
- [C16] 计费倍数与旧说一致（5m 写 1.25×、1h 写 2×、读 0.1×），但现行页新增按模型例外：Fable 5.1/Mythos 5.1 读 0.025×、Opus 5.5 读 0.05× | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache read tokens are 0.1 times the base input tokens price (see the table footnote for per-model exceptions)" | type: official

## conflicts
- 无（现行页内部自洽；与 2025-08-03 快照的差异全部由版本演进解释：1h 去 beta header 见 C7/2025-08-13，顶层 automatic caching 见 C6/2026-02-19）

## gaps
- 现行指南与 API reference 均未直写「完全不带 `cache_control` 的请求不会被缓存」；只有 C1/C4 的 opt-in 框架隐含此意，且 C14 显示 server tools 可绕过用户字段产生缓存写。
- API reference 对顶层 `cache_control` 仅标 optional，未写省略时行为。
- 未打开 tool-use-with-prompt-caching 页核实 server tool 自动缓存是否在任何 `cache_control` 缺席时仍发生。

## leads
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching#server-tool-results-are-cached-automatically — 直接关乎「不传字段是否仍有缓存写」。
- cache diagnostics 公测（`diagnostics.previous_message_id` + `cache_miss_reason`，release notes 2026-05-13）可实证断点行为。
- 现行页新增旧快照没有的机制：20-block lookback、pre-warming（`max_tokens: 0`）、workspace 级缓存隔离。
