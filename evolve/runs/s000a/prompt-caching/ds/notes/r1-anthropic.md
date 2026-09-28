# r1-anthropic
question: Anthropic Claude 官方 API 的 prompt caching 现在是否仍必须在请求里手动放置 cache_control 断点；断点怎么放、有多少个、TTL 有哪些、读写怎么计费、响应哪个字段表示命中、什么改动会失效、哪些模型可用。
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/api/messages/create, https://web.archive.org/web/20250803210544/https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching

## claims
- [C1] D1: 缓存仍是 opt-in，必须带 cache_control；但已不止手动断点一种：可放请求顶层（自动）或放单个块上（显式） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "There are two ways to enable prompt caching" | type: official
- [C2] D1: 自动模式在顶层放一个 cache_control，系统自动把断点放到最后可缓存块并随对话前移 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Add a single `cache_control` field at the top level of your request. The system automatically applies the cache breakpoint to the last cacheable block" | type: official
- [C3] D1: FAQ：顶层字段或至少一个块级断点；不放任何 cache_control 则不启用 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Alternatively, include at least one `cache_control` breakpoint on individual content blocks" | type: official
- [C4] D1: API reference 已将 cache_control 列为 Messages 顶层 body 参数 | src: https://platform.claude.com/docs/en/api/messages/create | quote: "Top-level cache control automatically applies a cache_control marker to the last cacheable block in the request." | type: official
- [C5] D2: 缓存覆盖整段前缀，顺序固定 tools→system→messages，到被标记块为止 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache prefixes are created in the following order: `tools`, `system`, then `messages`." | type: official
- [C6] D2: 最多 4 个断点；自动断点占其中 1 槽，已有 4 个显式断点再加顶层 cache_control 返回 400 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "You can define up to 4 cache breakpoints (using `cache_control` parameters) in your prompt." | type: official
- [C7] D2: 写入只发生在断点；读取自断点向前回看 20 个块（连续 tool_use/tool_result 各算 1 位置） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The lookback window is 20 blocks." | type: official
- [C8] D2: 断点放跨请求不变的最后一个块；tools/system/text/image/document/tool_use/tool_result 可标记，thinking 块与空 text 块不可直接标记 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Place `cache_control` on the last block whose prefix is identical across the requests you want to share a cache." | type: official
- [C9] D3: 最小可缓存长度：512（Fable 5.1、Mythos 5.1、Opus 5.5、Opus 5、Fable 5、Mythos 5）；2048（Mythos Preview、Opus 4.7）；4096（Opus 4.6、Opus 4.5）；1024（Opus 4.8、Sonnet 5/4.6/4.5、Opus 4.1/4、Sonnet 4）；4096（Haiku 4.5）；2048（Haiku 3.5） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "512 tokens for Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Opus 5…" | type: official
- [C10] D3: 低于门槛静默不缓存、不报错 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Any requests to cache fewer than this number of tokens will be processed without caching, and no error is returned." | type: official
- [C11] D4: 默认 TTL 5 分钟、命中免费刷新；寿命从请求开始时刻起算（生成耗时计入） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used." | type: official
- [C12] D4: 1 小时写法 `"cache_control": {"type": "ephemeral", "ttl": "1h"}`；ttl 枚举 `"5m"`/`"1h"` 默认 5m；"ephemeral" 是唯一 cache type | src: https://platform.claude.com/docs/en/api/messages/create | quote: "ttl: optional "5m" or "1h"… Defaults to `5m`." | type: official
- [C13] D4: 可混用两种 TTL，长 TTL 断点须在短 TTL 之前；1h 缓存覆盖 Claude API/Bedrock（含 legacy）/Claude Platform on AWS/Google Cloud/Foundry | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache entries with longer TTL must appear before shorter TTLs" | type: official
- [C14] D5: 5m 写 = 1.25×、1h 写 = 2×、读/刷新 = 0.1× base input | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "5-minute cache write tokens are 1.25 times the base input tokens price… 1-hour cache write tokens are 2 times… Cache read tokens are 0.1 times" | type: official
- [C15] D5: 读价例外：Fable 5.1/Mythos 5.1 为 0.025×，Opus 5.5 为 0.05×；断点本身免费；cache hits 不扣 rate limit | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache hits and refreshes on Claude Fable 5.1 and Claude Mythos 5.1 are priced at 0.025x the base input price." | type: official
- [C16] D6: 观测字段在响应 usage（流式在 message_start）：cache_creation_input_tokens、cache_read_input_tokens、input_tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "`cache_read_input_tokens`: Number of tokens retrieved from the cache for this request." | type: official
- [C17] D6: input_tokens 只计最后断点之后的 token；总输入 = 三字段之和；两 cache 字段皆 0 即未缓存 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The `input_tokens` field represents only the tokens that come after the last cache breakpoint" | type: official
- [C18] D6: usage 内含嵌套 cache_creation 对象按 TTL 拆分 | src: https://platform.claude.com/docs/en/api/messages/create | quote: "cache_creation: CacheCreation or null — Breakdown of cached tokens by TTL — ephemeral_1h_input_tokens… ephemeral_5m_input_tokens" | type: official
- [C19] D7: 命中要求断点之前内容 100% 相同（含图片）；断点及之前任何块改动都产生新前缀 hash | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache hits require 100% identical prompt segments, including all text and images up to and including the block marked with cache control." | type: official
- [C20] D7: 失效按层级：改 tool 定义全失效；web search/citations/speed 开关→system+messages；tool_choice、图片、thinking 配置、effort→messages（tools/system 因模型而异） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "the cache follows the hierarchy: `tools` → `system` → `messages`. Changes at each level invalidate that level and all subsequent levels." | type: official
- [C22] D8: 所有现役 Claude 模型支持自动与显式两种模式 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching (both automatic and explicit) is supported on all active Claude models." | type: official
- [C23] D8: 顶层 cache_control 在 legacy Amazon Bedrock（Opus 4.6 及更早）不可用，返回 400，须用显式断点 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Automatic caching is available on every platform except the legacy Amazon Bedrock (Opus 4.6 and earlier) integration." | type: official
- [C24] D8: 已 GA 无需 beta 前缀；隔离按 workspace（Claude API/CPAWS/Foundry）或 org（Bedrock/Google Cloud） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching no longer requires the beta prefix." | type: official

## conflicts
- 旧版官方文档（Wayback 2025-08-03 快照）："To enable prompt caching, include at least one `cache_control` breakpoint in your API request."（https://web.archive.org/web/20250803210544/https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching）vs 现版："There are two ways to enable prompt caching"（https://platform.claude.com/docs/en/build-with-claude/prompt-caching）。读者"必须手动打断点"对应旧版。
- 1h TTL 旧版要求 beta header："add `extended-cache-ttl-2025-04-11` as a beta header"（同上快照）vs 现版只写 `"ttl": "1h"`，无 beta header。
- 旧版最小门槛仅 1024/2048 两档、支持模型仅限 Claude 3/4 旧型号（同上快照）vs 现版 512–4096 按模型分档且覆盖全部现役模型。

## gaps
- 现版页面未见 "Updated" 日期。
- "完全不放 cache_control 绝不缓存"无单独原话；官方表述为"two ways to enable"，两者都要求某处存在 cache_control。
- 自动缓存上线日期未找到。

## leads
- Bedrock 上 Claude 缓存有独立 AWS 文档：https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
- Cache diagnostics（beta）报告前缀分歧位置：https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics
- `inline-tools-2026-09-15` beta 可中途加工具不失效：https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages
