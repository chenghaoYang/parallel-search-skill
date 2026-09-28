# r2-anthropic-scope
question: 只划定两处冲突的主语，不重写 Anthropic 缓存总览。
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages

## claims
- [C1] D1 主语 A＝整次请求 opt-in。## How it works：无 `cache_control`（顶层 automatic 或显式 breakpoint）则不缓存，整段按普通 input 价。 | src: https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#how-it-works | quote: "Prompt caching is opt-in: if a request has no cache_control field (automatic or an explicit breakpoint), nothing is cached and every request pays the regular input token price for the full conversation." | type: official
- [C2] D1 同页 ## Combining with prompt caching：只有请求带 cache_control（顶层 automatic 或 block 上的显式 breakpoint）才缓存。 | src: https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#combining-with-prompt-caching | quote: "Caching only happens when the request includes cache_control, either the top-level automatic caching field or an explicit breakpoint on a content block." | type: official
- [C3] D1 同节：中途 system 消息自己不建 cache entry；未启用 caching 就没有可保留的节省。 | src: https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#combining-with-prompt-caching | quote: "A mid-conversation system message does not create a cache entry on its own, and without caching enabled there are no savings to preserve." | type: official
- [C4] D1 主语 B 不是整段 prompt。该句在 prompt-caching 仅一处，位于 ### Caching with thinking blocks / **Cache invalidation patterns** 第 4 点。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#caching-with-thinking-blocks | quote: "This caching behavior occurs even without explicit cache_control markers" | type: official
- [C5] D1 前一句主语是早期 Opus/Sonnet 与全部 Haiku 上 thinking blocks 被剥离，不是「无标记则整段写入缓存」。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#caching-with-thinking-blocks | quote: "On earlier Opus/Sonnet models and all Haiku models, cache gets invalidated when non-tool-result user content is added, causing all previous thinking blocks to be stripped from context" | type: official
- [C6] D1 后一句仍指向 cache invalidation。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#caching-with-thinking-blocks | quote: "For more details on cache invalidation, see What invalidates the cache." | type: official
- [C7] D1 同小节近端：thinking blocks 不能直接标 `cache_control`，但会作为请求内容的一部分被缓存。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#caching-with-thinking-blocks | quote: "While thinking blocks cannot be explicitly marked with cache_control, they get cached as part of the request content when you make subsequent API calls with tool results." | type: official
- [C8] D1 automatic caching 仍要顶层 `cache_control`；系统只是把 breakpoint 放到最后一个可缓存 block。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#automatic-caching | quote: "Instead of placing cache_control on individual content blocks, add a single cache_control field at the top level of your request body." | type: official
- [C9] D1 页首第一条启用方式同样要求顶层一个 `cache_control`。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Add a single cache_control field at the top level of your request. The system automatically applies the cache breakpoint to the last cacheable block and moves it forward as conversations grow." | type: official
- [C10] D7 散文主语是 5 分钟 TTL 刷新，不是价目列。## How prompt caching works：每次使用已缓存内容，refresh 不再另收费。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#how-prompt-caching-works | quote: "By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used." | type: official
- [C11] D7 ### When to use the 1-hour cache：高于每 5 分钟使用时，5 分钟缓存 “refreshed at no additional charge”。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#1-hour-cache-duration | quote: "continue to use the 5-minute cache, because this will continue to be refreshed at no additional charge." | type: official
- [C12] D7 列名 “Cache hits and refreshes”。脚注：Fable 5.1 与 Mythos 5.1 的 hits and refreshes＝基价 0.025x（非 0，非写价）。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing | quote: "Cache hits and refreshes on Claude Fable 5.1 and Claude Mythos 5.1 are priced at 0.025x the base input price." | type: official
- [C13] D7 同列：Opus 5.5 的 hits and refreshes＝基价 0.05x。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing | quote: "Cache hits and refreshes on Claude Opus 5.5 are priced at 0.05x the base input price." | type: official
- [C14] D7 同列：其余模型标准 0.1x。未把 refresh 单独写成 0 或写价。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing | quote: "All other models use the standard 0.1x multiplier." | type: official
- [C15] D7 表下 Note 的 0.1x 子弹主语是 Cache read tokens，不是 refreshes。写价另列：5m 写 1.25x，1h 写 2x。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing | quote: "Cache read tokens are 0.1 times the base input tokens price (see the table footnote for per-model exceptions)" | type: official
- [C16] D7 breakpoint 成本节把 “cached content is used” 标成读价 10% / 2.5%（Fable 5.1、Mythos 5.1）/ 5%（Opus 5.5），与 C10 数字不同，不合并。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#understanding-cache-breakpoint-costs | quote: "When cached content is used (10% of base input token price, or 2.5% on Claude Fable 5.1 and Claude Mythos 5.1, and 5% on Claude Opus 5.5)" | type: official
- [C17] D3。### Cache limitations：Claude Haiku 4.5 最低 4,096 tokens。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#cache-limitations | quote: "4,096 tokens for Claude Haiku 4.5" | type: official
- [C18] D3。Haiku 3.5 是 2,048，不是 4,096；除 Bedrock 与 Google Cloud 外已退役。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#cache-limitations | quote: "2,048 tokens for Claude Haiku 3.5 (retired, except on Bedrock and Google Cloud)" | type: official
- [C19] D3。另一条 4,096 是 Claude Opus 4.6 与 Opus 4.5，与 Haiku 4.5 分行。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#cache-limitations | quote: "4,096 tokens for Claude Opus 4.6 and Claude Opus 4.5" | type: official
- [C20] D3。低于门槛则即使有 cache_control 也不缓存，且不报错。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching#cache-limitations | quote: "Shorter prompts cannot be cached, even if marked with cache_control. Any requests to cache fewer than this number of tokens will be processed without caching, and no error is returned." | type: official

## conflicts
- D1 不裁行为对错，只分主语。C1–C3：没有 `cache_control` 字段则 nothing is cached / regular input token price。C4 只在 Caching with thinking blocks 的 Cache invalidation patterns；前句是 thinking blocks 被剥离（C5），后句仍是 invalidation（C6），近端是 thinking 不能直接标 cache_control 但仍随请求内容缓存（C7）。同页 automatic 仍要顶层 cache_control（C8、C9）。不是「零 cache_control 时整段 prompt 自动缓存」。
- D7 不折成一个数。C10/C11：5 分钟缓存每次使用 “no additional cost” / “no additional charge”。列 “Cache hits and refreshes” 的倍率原句是 0.025x、0.05x、其余 0.1x（C12–C14），不是 0，也不是写价 1.25x/2x。Note 的 0.1x 写的是 “Cache read tokens”（C15）。C16 把使用已缓存内容写成 10%/2.5%/5%。页内未调和。

## gaps
- 两页抓取正文无 last-updated 或文档版本号。
- 未开 https://platform.claude.com/docs/en/about-claude/pricing ，不知是否把 hit 与 refresh 拆价。
- 未开 https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-and-prompt-caching ；C4 主语只据本页前后句。

## leads
- thinking 锚点页可能把 without-markers 句写得比失效列表更宽。
- about-claude/pricing 可能把 refresh 与 cache read 拆开。
- D3 同段：两 usage 字段皆 0 则未缓存，未计入 4 条上限。
