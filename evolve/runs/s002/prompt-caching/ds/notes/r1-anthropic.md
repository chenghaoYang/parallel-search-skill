# r1-anthropic
question: Anthropic Claude API 的 prompt caching 是否仍要调用方在内容块上放 cache_control；断点、TTL、写入/读取计价、命中字段、失效规则的当前原文。
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/api/messages, https://platform.claude.com/docs/en/release-notes/overview, https://platform.claude.com/docs/en/about-claude/pricing

## claims
- [C1] D1: 启用缓存仅两种路径且都含 `cache_control`——顶层字段（automatic caching）或块级断点；无零 `cache_control` 的隐式缓存 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "There are two ways to enable prompt caching:" | type: official
- [C2] D1: automatic caching＝顶层 `cache_control` 字段，系统自动把断点放到最后可缓存块并随会话前移 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Add a single `cache_control` field at the top level of your request." | type: official
- [C3] D1: explicit 方式＝把 `cache_control` 放在单个 content block 上 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Place `cache_control` directly on individual content blocks for fine-grained control over exactly what gets cached." | type: official
- [C4] D1: Messages 请求体 schema 中确有顶层 `cache_control` 参数（API reference）| src: https://platform.claude.com/docs/en/api/messages | quote: "Top-level cache control automatically applies a cache_control marker to the last cacheable block in the request." | type: official
- [C5] D1: `type` 枚举仅 `"ephemeral"` | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Currently, \"ephemeral\" is the only supported cache type" | type: official
- [C6] D1: 断点上限 4 个 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "You can define up to 4 cache breakpoints" | type: official
- [C7] D1: automatic caching 于 2026-02-19 上线（release notes），免去手动断点管理 | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "the system automatically caches the last cacheable block, moving the cache point forward as conversations grow. No manual breakpoint management required." | type: official
- [C8] D2: 缓存前缀顺序 tools→system→messages，含到标记块为止的全部内容 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "the entire prompt: `tools`, `system`, and `messages` (in that order), up to and including the block designated with `cache_control`" | type: official
- [C9] D2: 写入只在断点（条目为截至该块前缀的 hash）；读取回查先前写入，窗口 20 blocks | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Marking a block with `cache_control` writes exactly one cache entry: a hash of the prefix ending at that block." | type: official
- [C10] D3: 最小可缓存长度按模型分档，512 档含 Fable 5.1/Mythos 5.1/Opus 5.5/Opus 5/Fable 5/Mythos 5 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "512 tokens for Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Opus 5, Claude Fable 5, and Claude Mythos 5" | type: official
- [C11] D3: 其余档：2048 Mythos Preview/Opus 4.7/Haiku 3.5；4096 Opus 4.6/4.5、Haiku 4.5；1024 Opus 4.8、Sonnet 5/4.6/4.5、Opus 4.1/4、Sonnet 4；低于门槛不缓存且无报错 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "1,024 tokens for Claude Opus 4.8, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5" | type: official
- [C13] D4: 默认 TTL 5 分钟，每次命中免费刷新 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used." | type: official
- [C14] D4: `ttl` 枚举 `"5m"`/`"1h"`，默认 `"5m"`；生命周期从写/读请求开始时刻计 | src: https://platform.claude.com/docs/en/api/messages | quote: "ttl: optional \"5m\" or \"1h\"" | type: official
- [C15] D5: 5 分钟缓存写入＝1.25x base input | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "5-minute cache write | 1.25x base input price" | type: official
- [C16] D5: 1 小时缓存写入＝2x base input | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "1-hour cache write | 2x base input price" | type: official
- [C17] D5: 读取标准 0.1x base input；例外 Fable 5.1/Mythos 5.1 为 0.025x、Opus 5.5 为 0.05x | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "0.1x base input price (0.025x on Claude Fable 5.1 and Claude Mythos 5.1; 0.05x on Claude Opus 5.5)" | type: official
- [C18] D6: 命中字段 `usage.cache_creation_input_tokens`（写入）与 `usage.cache_read_input_tokens`（读取）| src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "cache_creation_input_tokens: Number of tokens written to the cache when creating a new entry. cache_read_input_tokens: Number of tokens retrieved from the cache for this request." | type: official
- [C19] D6: 1h 写入有独立细分 `usage.cache_creation.ephemeral_1h_input_tokens`（另有 `ephemeral_5m_input_tokens`）| src: https://platform.claude.com/docs/en/api/messages | quote: "ephemeral_1h_input_tokens: number" | type: official
- [C20] D7: 失效沿 tools→system→messages 层级向下传播 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Changes at each level invalidate that level and all subsequent levels." | type: official
- [C21] D7: 修改工具定义使整个缓存失效；`tool_choice` 或图片增删同样失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Modifying tool definitions (names, descriptions, parameters) invalidates the entire cache" | type: official
- [C22] D7: 命中要求前缀 100% 一致（含文本与图像，至标记块）| src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache hits require 100% identical prompt segments, including all text and images up to and including the block marked with cache control." | type: official
- [C23] D8: 可缓存：tools 定义、system 块、messages 的 text（user/assistant）、user 轮图片与文档、tool_use 与 tool_result | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Tool use and tool results: Content blocks in the `messages.content` array, in both user and assistant turns" | type: official
- [C24] D8: thinking 块不能打 `cache_control`，但可随先前 assistant turns 一起被缓存，读取时计 input tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Thinking blocks cannot be cached directly with `cache_control`." | type: official
- [C25] D9: automatic 与 explicit 均支持全部 active Claude 模型 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching (both automatic and explicit) is supported on all active Claude models" | type: official
- [C26] D9: 已 GA，不再需要 beta header；2024-12-17 changelog 列入无需 beta header 的功能 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching no longer requires the beta prefix." | type: official
- [C27] D9: automatic caching 唯一平台例外为旧版 Bedrock 集成（Opus 4.6 及更早），顶层 `cache_control` 返回 400 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Automatic caching is available on every platform except the legacy Amazon Bedrock (Opus 4.6 and earlier) integration." | type: official
- [C28] D9: 命中非保证：Batches 中命中为 best-effort；并发时条目在首个响应开始后才可用 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "cache hits are provided on a best-effort basis" | type: official

## conflicts
- automatic caching 范围：2026-02-19 注记称 "Available on the Claude API and Microsoft Foundry (preview)"，当前指南称 "available on every platform except the legacy Amazon Bedrock (Opus 4.6 and earlier) integration"——疑为发布后扩大，未核实各平台上架时间。
- thinking 章节 "This caching behavior occurs even without explicit `cache_control` markers" 指 thinking 块随已启用缓存的请求内容被缓存/失效，并非零打点缓存。

## gaps
- 无逐字句写「完全不带 cache_control 绝不缓存」；依据为指南仅列两种均含 cache_control 的启用路径。
- Bedrock implicit caching 仅在 AWS 文档，本轮未打开。

## leads
- Bedrock 独立文档：https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html（minimums/失败行为/usage 字段名以 AWS 为准）。
- Cache diagnostics（beta）：`diagnostics.previous_message_id` 返回 `cache_miss_reason` 定位前缀分歧。
