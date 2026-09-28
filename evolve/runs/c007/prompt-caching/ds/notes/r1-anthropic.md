# r1-anthropic
question: Anthropic Claude API 的 prompt caching（cache_control）现状（截至 2026-09）——机制/门槛/计费/TTL/命中确认/失效/模型范围
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://claude.com/pricing, https://platform.claude.com/docs/en/release-notes/overview, https://github.com/anthropics/anthropic-sdk-python/blob/d2f6543e/src/anthropic/types/anthropic_beta_param.py

## claims

D1 机制
- [C1] 现有两种方式：automatic caching（请求体顶层放一个 cache_control 字段，系统自动把断点打到最后一个可缓存块并随对话前移）+ explicit 块级断点 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Automatic caching: Add a single `cache_control` field at the top level of your request. The system automatically applies the cache breakpoint to the last cacheable block and moves it forward as conversations grow." | type: official
- [C2] automatic caching 于 2026-02-19 上线（仍需显式加 cache_control，非默认开启） | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "We've launched **automatic caching** for the Messages API. Add a single `cache_control` field to your request body and the system automatically caches the last cacheable block ... No manual breakpoint management required." (### February 19, 2026) | type: official
- [C3] 显式块级断点最多 4 个；若已用满 4 个，顶层 automatic cache_control 会 400 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "You can define up to 4 cache breakpoints" / "If 4 explicit block-level breakpoints already exist, the API returns a 400 error (no slots left for automatic caching)." | type: official
- [C4] 缓存前缀按 tools → system → messages 顺序构建；缓存写入只发生在断点处；回看窗口 20 个块 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache prefixes are created in the following order: `tools`, `system`, then `messages`." / "Cache writes happen only at your breakpoint." / "The lookback window is 20 blocks." | type: official
- [C5] 目前唯一支持的 cache type 是 ephemeral | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Currently, \"ephemeral\" is the only supported cache type, which by default has a 5-minute lifetime." | type: official

D2 最小可缓存前缀
- [C6] 最小 token 数按模型分档：512=Fable 5.1/Mythos 5.1/Opus 5.5/Opus 5/Fable 5/Mythos 5；1024=Opus 4.8/Sonnet 5/Sonnet 4.6/Sonnet 4.5/Opus 4.1/Opus 4/Sonnet 4；2048=Mythos Preview/Opus 4.7/Haiku 3.5；4096=Opus 4.6/Opus 4.5/Haiku 4.5 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "the minimum cacheable prompt length is: * 512 tokens for Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Opus 5, Claude Fable 5, and Claude Mythos 5 * 2,048 tokens for Claude Mythos Preview and Claude Opus 4.7 * 4,096 tokens for Claude Opus 4.6 and Claude Opus 4.5 * 1,024 tokens for Claude Opus 4.8, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, ... * 4,096 tokens for Claude Haiku 4.5 * 2,048 tokens for Claude Haiku 3.5" | type: official
- [C7] 低于最小值静默不缓存、不报错 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Shorter prompts cannot be cached, even if marked with `cache_control`. Any requests to cache fewer than this number of tokens will be processed without caching, and no error is returned." | type: official
- [C8] Opus 4.8 起最小值降到 1024（2026-05-28 changelog） | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "On Claude Opus 4.8, the minimum cacheable prompt length for prompt caching is 1,024 tokens, lower than on Claude Opus 4.7." (### May 28, 2026) | type: official

D3 计费
- [C9] 乘数：5m 写=1.25x 输入价；1h 写=2x；读=0.1x；例外 Fable 5.1/Mythos 5.1 读 0.025x、Opus 5.5 读 0.05x | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "5-minute cache write tokens are 1.25 times the base input tokens price * 1-hour cache write tokens are 2 times the base input tokens price * Cache read tokens are 0.1 times the base input tokens price (see the table footnote for per-model exceptions)" | type: official
- [C10] 文档价格表（$/MTok，base输入/5m写/1h写/读）：Sonnet 4.5 3/3.75/6/0.30；Haiku 4.5 1/1.25/2/0.10；Opus 5 5/6.25/10/0.50；Opus 5.5 4/5/8/0.20；Fable 5.1 10/12.50/20/0.25 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "| Claude Opus 5 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |" | type: official
- [C11] anthropic/claude pricing 页只列 5m 价：Sonnet 5 $2/$2.50 write/$0.20 read；Haiku 4.5 $1/$1.25/$0.10；Opus 5.5 $4/$5/$0.20 | src: https://claude.com/pricing | quote: "Prompt caching pricing reflects 5-minute TTL." | type: official

D4 TTL
- [C12] 默认 5 分钟；每次命中免费续期（lifetime 从发起写/读请求的时刻起算） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used." / "The lifetime is measured from the start of the request that writes or reads the cache entry" | type: official
- [C13] 1h TTL：cache_control 里加 "ttl": "1h"；同一请求内 1h 断点必须排在 5m 断点之前 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "\"cache_control\": { \"type\": \"ephemeral\", \"ttl\": \"1h\" }" / "Cache entries with longer TTL must appear before shorter TTLs" | type: official
- [C14] 1h TTL 于 2025-08-13 去掉 beta header 转 GA；beta header 名为 extended-cache-ttl-2025-04-11（官方 SDK 枚举，日期即 2025-04-11） | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "The 1-hour cache duration for prompt caching no longer requires a beta header." (### August 13, 2025); SDK: `"extended-cache-ttl-2025-04-11"` in anthropic-sdk-python anthropic_beta_param.py | type: official

D5 命中确认
- [C15] usage 字段：cache_creation_input_tokens=写入量，cache_read_input_tokens=命中量，input_tokens 只计未缓存部分；total=三者之和 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "`cache_creation_input_tokens`: Number of tokens written to the cache when creating a new entry. * `cache_read_input_tokens`: Number of tokens retrieved from the cache for this request. * `input_tokens`: Number of input tokens which were not read from or used to create a cache" | type: official
- [C16] usage.cache_creation 子对象拆 5m/1h 写入量，其和等于 cache_creation_input_tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "\"cache_creation\": { \"ephemeral_5m_input_tokens\": 148, \"ephemeral_1h_input_tokens\": 100 } ... the current `cache_creation_input_tokens` field equals the sum of the values in the `cache_creation` object." | type: official
- [C17] cache diagnostics 2026-09-23 GA：请求带 diagnostics.previous_message_id，响应 diagnostics 字段（总是出现，未带则 null）报告 cache_miss_reason | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "Responses from `POST /v1/messages` now always include the `diagnostics` field, which is `null` when the request did not include the `diagnostics` object." (### September 23, 2026) | type: official

D6 失效规则
- [C18] 层级失效：tools→system→messages，改某层则该层及其后全部失效；命中要求前缀 100% 一致（含图片）直到断点块 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "the cache follows the hierarchy: `tools` → `system` → `messages`. Changes at each level invalidate that level and all subsequent levels." / "Cache hits require 100% identical prompt segments, including all text and images up to and including the block marked with cache control." | type: official
- [C19] 改 tool 定义（名/描述/参数）→ 整个缓存失效；tool_choice、图片增删 → 只失效 messages 层 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Modifying tool definitions (names, descriptions, parameters) invalidates the entire cache" / "Changes to `tool_choice` parameter only affect message blocks" / "Adding/removing images anywhere in the prompt affects message blocks" | type: official
- [C20] tool_use 块内 JSON key 顺序不稳定（Swift/Go）会破坏缓存 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Verify that the keys in your `tool_use` content blocks have stable ordering as some languages (for example, Swift, Go) randomize key order during JSON conversion, breaking caches" | type: official

D7 模型范围
- [C21] prompt caching（automatic 与 explicit）支持所有现役 Claude 模型 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching (both automatic and explicit) is supported on all active Claude models." | type: official
- [C22] prompt caching 本体 2024-12-17 起不再需要 beta header（beta 起于 2024-08-14） | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "The following features are now available in the Claude API without a beta header: ... [Prompt Caching]" (### December 17th, 2024) | type: official
- [C23] automatic caching 在旧版 Amazon Bedrock 集成（Opus 4.6 及更早）不可用：顶层 cache_control 返回 400 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Automatic caching is available on every platform except the legacy Amazon Bedrock (Opus 4.6 and earlier) integration. On that integration, the API returns a 400 error for a top-level `cache_control` field" | type: official

## conflicts
- 无来源冲突。pricing 页仅展示 5m TTL 价格（注明 "reflects 5-minute TTL"），1h 价格只在文档页表格出现——属覆盖范围差异，非矛盾。

## gaps
- 1h TTL beta 的「引入」条目不在 release-notes overview 中（2025-04 段只有 Ruby SDK）；日期 2025-04-11 仅从 beta header 名推断，GA 日期 2025-08-13 已确认。
- Opus 5.5 读价 0.05x 的起始日期未在 changelog 逐条核对（Fable 5.1/Mythos 5.1 的 0.025x 为 2026-09-01 条目）。
- Bedrock/Vertex 上 caching 的完整差异矩阵未查（简报只要求记 leads）。

## leads
- 旧版 Bedrock 集成（Opus 4.6 及更早）不支持顶层 cache_control / automatic caching（C23）。
- cache diagnostics（diagnostics.previous_message_id → cache_miss_reason）已于 2026-09-23 GA，是官方「为什么没命中」排障入口（C17）。
- 一批 2026 年「保缓存」特性：mid-conversation system messages（2026-05-28）、mid-conversation tool changes beta（2026-07-24）、inline tool_addition（2026-09-22）、turn-scoped system messages beta。
- prompt caching 历史：2024-08-14 beta → 2024-12-17 GA；2025-01-15 起命中自动读最长已缓存前缀。
