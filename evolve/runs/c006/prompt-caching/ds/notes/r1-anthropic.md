# r1-anthropic
question: Anthropic Messages API 的 prompt caching（cache_control 断点）机制、计费、TTL、命中确认字段、失效条件
checked: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/about-claude/pricing, https://platform.claude.com/docs/en/api/messages, https://platform.claude.com/docs/en/release-notes/api
（注：docs.anthropic.com 已 301 至 platform.claude.com）

## claims
- [C1] 手动断点机制：在 content block 上加 `"cache_control": {"type": "ephemeral"}`；ephemeral 是唯一缓存类型 | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Currently, "ephemeral" is the only supported cache type, which by default has a 5-minute lifetime." | type: official
- [C2] 断点上限 4 个 | src: 同上 | quote: "You can define up to 4 cache breakpoints if you want to:" | type: official
- [C3] 自动缓存（automatic caching）：请求体顶层加一个 `cache_control` 字段，系统自动把断点放到最后一个可缓存 block 并随对话前移 | src: 同上 | quote: "Add a single `cache_control` field at the top level of your request. The system automatically applies the cache breakpoint to the last cacheable block and moves it forward as conversations grow." | type: official
- [C4] 自动断点占 4 个槽位之一；已有 4 个显式断点则 API 返回 400；lookback window 20 blocks | src: 同上 | quote: "When used together, the automatic cache breakpoint uses one of the 4 available breakpoint slots." + "If 4 explicit block-level breakpoints already exist, the API returns a 400 error" + "The lookback window is 20 blocks." | type: official
- [C5] automatic caching 于 2026-02-19 上线（changelog） | src: https://platform.claude.com/docs/en/release-notes/api | quote: "We've launched **automatic caching** for the Messages API. Add a single `cache_control` field to your request body and the system automatically caches the last cacheable block" | type: official
- [C6] TTL：默认 5 分钟，可用 `"ttl": "1h"` 选 1 小时；命中时免费刷新；TTL 从写/读请求开始计时而非响应结束；长 TTL 断点必须排在短 TTL 之前 | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used." + "The lifetime is measured from the start of the request that writes or reads the cache entry" + "Cache entries with longer TTL must appear before shorter TTLs" | type: official
- [C7] API schema：`cache_control` = CacheControlEphemeral，`type: "ephemeral"`，`ttl` 枚举 `"5m"|"1h"` 默认 5m；顶层 cache_control 亦同型 | src: https://platform.claude.com/docs/en/api/messages | quote: "ttl: optional \"5m\" or \"1h\" — The time-to-live for the cache control breakpoint... Defaults to `5m`." + "Top-level cache control automatically applies a cache_control marker to the last cacheable block" | type: official
- [C8] 计费倍数：5m 写入 1.25×，1h 写入 2×，读取 0.1× base input | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "5-minute cache write | 1.25x base input price" + "1-hour cache write | 2x base input price" + "Cache read (hit) | 0.1x base input price" | type: official
- [C9] 读取折扣例外：Claude Fable 5.1 / Mythos 5.1 为 0.025×，Claude Opus 5.5 为 0.05× | src: 同上 | quote: "Cache hits and refreshes on Claude Fable 5.1 and Claude Mythos 5.1 are priced at 0.025x the base input price." + "Cache hits and refreshes on Claude Opus 5.5 are priced at 0.05x" | type: official
- [C10] 最小可缓存长度按模型分档：512（Fable 5.1/Mythos 5.1/Opus 5.5/Opus 5/Fable 5/Mythos 5）、2048（Mythos Preview/Opus 4.7）、4096（Opus 4.6/Opus 4.5）、1024（Opus 4.8/Sonnet 5/Sonnet 4.6/Sonnet 4.5/Opus 4.1/Opus 4/Sonnet 4）、4096（Haiku 4.5）、2048（Haiku 3.5）；不足则静默不缓存、不报错 | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "the minimum cacheable prompt length is: 512 tokens for Claude Fable 5.1... 2,048 tokens for Claude Haiku 3.5" + "Shorter prompts cannot be cached... no error is returned." | type: official
- [C11] 命中确认字段（usage 内）：`cache_creation_input_tokens`（写入）、`cache_read_input_tokens`（命中读取）、`input_tokens`（未缓存部分） | src: 同上 | quote: "`cache_creation_input_tokens`: Number of tokens written to the cache when creating a new entry." + "`cache_read_input_tokens`: Number of tokens retrieved from the cache for this request." | type: official
- [C12] `usage.cache_creation` 对象细分 TTL：`ephemeral_5m_input_tokens` / `ephemeral_1h_input_tokens`；与 cache_creation_input_tokens 相等；total_input = read + creation + input_tokens | src: 同上 | quote: "the current `cache_creation_input_tokens` field equals the sum of the values in the `cache_creation` object." | type: official
- [C13] 未缓存判定：两字段均为 0 则未缓存 | src: 同上 | quote: "if both `cache_creation_input_tokens` and `cache_read_input_tokens` are 0, the prompt was not cached" | type: official
- [C14] 失效层级：tools → system → messages，某层改动使该层及之后全部失效 | src: 同上 | quote: "the cache follows the hierarchy: `tools` → `system` → `messages`. Changes at each level invalidate that level and all subsequent levels." | type: official
- [C15] 具体失效项：改工具定义全失效；web search/citations/speed 开关使 system+messages 失效；tool_choice、增删 image 使 messages 失效；thinking/effort 参数视模型而定 | src: 同上 | quote: "Modifying tool definitions (names, descriptions, parameters) invalidates the entire cache" + "Changes to `tool_choice` or the presence/absence of images anywhere in the prompt will invalidate the cache" | type: official
- [C16] 无需 beta header：页面未提及 prompt-caching 任何 beta header；1h TTL 自 2025-08-13 起不需 beta | src: https://platform.claude.com/docs/en/release-notes/api | quote: "The 1-hour cache duration for prompt caching no longer requires a beta header." (Aug 13, 2025) | type: official
- [C17] 支持范围："Prompt caching (both automatic and explicit) is supported on all active Claude models." | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: 同左 | type: official
- [C18] 可缓存 block：tools 数组、system 数组、messages 的 text/image/document/tool_use/tool_result（image 仅 user turn）；thinking block 不能直接打 cache_control（但随前轮 assistant turn 一起被缓存，读取时计 input tokens）；空 text block、citations 子 block 不可直接缓存 | src: 同上 | quote: "This includes: Tools... System messages... Text messages... Images & Documents... Tool use and tool results" + "Thinking blocks cannot be cached directly with `cache_control`." + "Empty text blocks cannot be cached." | type: official
- [C19] 预热：`max_tokens: 0` 可只写缓存不生成响应 | src: https://platform.claude.com/docs/en/api/messages | quote: "Set to `0` to populate the prompt cache without generating a response." | type: official
- [C20] 2025-05-01 起 cache_control 必须打在 tool_result / document.source 的父 content block 上（打在内部末块会自动上移，打在其他内块报 validation error） | src: https://platform.claude.com/docs/en/release-notes/api | quote: "Cache control must now be specified directly in the parent `content` block of `tool_result` and `document.source`." | type: official

## conflicts
- 未发现一手来源间冲突。注意：旧资料常写单一最小值 1024 tokens，现行文档已按模型分 512/1024/2048/4096 四档（见 C10），属文档更新而非来源冲突。

## gaps
- prompt caching 最初 beta 上线（2024-08）与 GA（2024-12）的确切日期：release-notes/api 页在 2025-04 前被截断，未取到原句。
- usage 对象在 API reference 的响应 schema 段被截断，字段定义引自 prompt-caching 文档页（已是一手）。

## leads
- 自动缓存（顶层 cache_control）在 legacy Amazon Bedrock（Opus 4.6 及更早）集成上返回 400，只能用显式断点。
- 另有 "cache diagnostics" 功能：beta header `cache-diagnosis-2026-04-07`，2026-09-23 已 GA。
- 缓存写入/读取可与 Batch API 50% 折扣、data residency 1.1× 叠加（pricing 页 "These multipliers stack with other pricing modifiers"）。
