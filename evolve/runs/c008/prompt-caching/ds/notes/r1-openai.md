# r1-openai
question: OpenAI 官方 API 的 prompt caching 机制的全部事实（D1-D8）
checked: https://developers.openai.com/api/docs/guides/prompt-caching (301 from platform.openai.com/docs/guides/prompt-caching), https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml, https://developers.openai.com/api/docs/pricing, https://openai.com/index/prompt-caching/ (403 fail)

## claims
- [C1] 自动启用，无需请求字段：默认开启 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Prompt caching is enabled by default for supported OpenAI models." | type: official
- [C2] 缓存存 KV tensor 而非 token | src: same | quote: "The prompt cache stores key-value (KV) tensors, not the tokens themselves." | type: official
- [C3] breakpoint 模型：首个请求写入前缀，后续请求取最长匹配前缀 | src: same | quote: "The first request writes an eligible prefix to the cache and subsequent requests look for the longest matching cached prefix available, working backward through eligible breakpoints" | type: official
- [C4] 最小可缓存长度：GPT-5.6+ 为 1,024 token；更早模型随请求设置变化；OpenAI 隐藏 system 内容不计入 | src: same | quote: "The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later and varies by request settings for earlier models." | type: official
- [C5] 更早模型最小长度取决于 "tools, images, output schemas, reasoning effort, and verbosity" | src: same | quote: "the minimum cacheable input length varies with request settings, including tools, images, output schemas, reasoning effort, and verbosity" | type: official
- [C6] GPT-5.6+ 支持 implicit+explicit breakpoint（每请求最多 4 次 cache write）；GPT-5.5/5.5 Pro 仅 implicit、"Spaced at regular 2,048-token intervals"；更早模型 implicit、model-dependent intervals | src: same（model comparison 表）| quote: "Spaced at regular 2,048-token intervals." | type: official
- [C7] Chat Completions 支持：CreateChatCompletionRequest 继承 CreateModelResponseProperties，含 prompt_cache_options(ttl/mode)、prompt_cache_key、prompt_cache_retention；text/image/file/audio content part 有 prompt_cache_breakpoint 字段 | src: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml | quote: "prompt_cache_breakpoint: $ref: \"#/components/schemas/PromptCacheBreakpointParam\"" | type: official
- [C8] Responses API 请求参数：prompt_cache_options{ttl,mode,prewarm,comparison_response_id}、prompt_cache_key、prompt_cache_retention | src: same | quote: "prewarm: Prepares the prompt cache without generating output. Defaults to `false`." | type: official
- [C9] CreateEmbeddingRequest schema 中无任何 prompt_cache 字段（embedding 不缓存）| src: same | quote: "CreateEmbeddingRequest:" (no prompt_cache properties) | type: official
- [C10] Agents API 与 Responses 同机制 | src: guide | quote: "Agents API model calls use the same prompt-caching behavior as the Responses API." | type: official
- [C11] 24h extended retention 支持模型：gpt-5.5, gpt-5.5-pro, gpt-5.4, gpt-5.2, gpt-5.1 家族(含 codex 变体), gpt-5, gpt-5-codex, gpt-4.1 | src: guide 表注 | quote: "Extended retention is supported by gpt-5.5, gpt-5.5-pro, gpt-5.4, gpt-5.2, ... gpt-5-codex, and gpt-4.1." | type: official
- [C12] GPT-5.6+ TTL：prompt_cache_options.ttl 仅支持 "30m"（默认）；写/复用后 30 分钟内可复用 | src: guide | quote: "A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse, though OpenAI may retain it longer." | type: official
- [C13] in_memory 保留：空闲约 5–10 分钟，至多 1 小时 | src: guide | quote: "Entries typically remain active for around 5 to 10 minutes of inactivity, up to one hour." | type: official
- [C14] 24h 保留：典型约 30 分钟，最多 24 小时 | src: guide | quote: "Extended retention typically keeps entries available for around 30 minutes and can retain them for up to 24 hours." | type: official
- [C15] 命中刷新生命周期且不再收 write 费 | src: guide | quote: "reusing the prefix refreshes its lifetime without another cache-write charge" | type: official
- [C16] 默认 retention：非 ZDR 组织默认 24h；ZDR 组织默认 in_memory | src: guide | quote: "Organizations without Zero Data Retention enabled default to 24h. Organizations with Zero Data Retention enabled default to in_memory." | type: official
- [C17] 无手动清缓存 API | src: guide FAQ | quote: "Manual cache clearing is not currently available." | type: official
- [C18] GPT-5.6+ 计费：write 1.25× input 价，read 0.1× | src: guide | quote: "cache writes cost 1.25× the standard, uncached input-token rate ... subsequent reads cost only 0.1× that rate" | type: official
- [C19] 更早模型无 cache-write 费用，read 按模型定 cached-input 价 | src: guide 表 | quote: "No additional cache-write charge" | type: official
- [C20] cached input 折扣 "up to 90%"；pricing 页实例：gpt-5/gpt-5.1 系 $1.25/$0.125 (0.1×)；gpt-4.1 $2.00/$0.50、o3 $2.00/$0.50 (0.25×)；gpt-4o $2.50/$1.25、o1 $15/$7.50 (0.5×)；Batch/Flex 约为标准价一半 | src: https://developers.openai.com/api/docs/pricing | quote: "discounted up to 90%" (guide); pricing 表 gpt-4.1 Input $2.00 / Cached input $0.50 | type: official
- [C21] Responses 命中确认字段：usage.input_tokens_details.cached_tokens 和 cache_write_tokens（均 required）| src: openapi.yaml ResponseUsage | quote: "The number of tokens that were retrieved from the cache." / "The number of input tokens that were written to the cache." | type: official
- [C22] Chat Completions 命中字段：usage.prompt_tokens_details.cached_tokens 和 cache_write_tokens | src: openapi.yaml CompletionUsage | quote: "Cached tokens present in the prompt." / "The unadjusted number of prompt tokens written to cache." | type: official
- [C23] 更早模型 cached_tokens 上报口径：减隐藏 token 后向下取整到 128 倍数 | src: guide | quote: "Reported cached_tokens is calculated by subtracting the hidden system tokens from the last matched breakpoint, then rounding down to the nearest multiple of 128." | type: official
- [C24] 有 Prompt Caching Dashboard 与 Prompt Cache Diagnostics 工具监测命中率 | src: guide | quote: "Use the Prompt Caching Dashboard to monitor cache read hit rates and use the Prompt Cache Diagnostics tool to diagnose cache misses" | type: official
- [C25] 匹配粒度：整个渲染前缀逐 token 相同 | src: guide | quote: "Cache reuse requires the entire rendered prefix to match." | type: official
- [C26] 影响前缀/命中的设置：model, tools, parallel_tool_calls, text.format, reasoning.effort, text.verbosity, context_management | src: guide "Which settings affect the cached prefix?" 表 | quote: "Changing a request does not necessarily discard an existing cache entry. What matters is whether a subsequent request has the same prefix" | type: official
- [C27] 路由：缓存存于单机；>15 rpm 会 overflow routing；按隐藏内容后初始 token 哈希+prompt_cache_key 路由 | src: guide | quote: "Cached states live on individual machines, where traffic above 15 requests per minute can lead to overflow routing." | type: official
- [C28] 失效陷阱：扩展同一 message（A→A+B）使旧端点失效；implicit→explicit 切换丢失 implicit 前缀；compaction 改前缀 | src: guide pitfalls | quote: "The old endpoint after Content A is now inside a message, rather than at its end." | type: official
- [C29] 显式管理参数：prompt_cache_options.mode(implicit/explicit)、.ttl("30m")、.prewarm(true 时不生成输出)；内容块 prompt_cache_breakpoint{mode:"explicit"}；每请求最多 4 breakpoint write | src: openapi.yaml PromptCacheOptionsParam | quote: "Each request can write up to four breakpoints. For cache matching, OpenAI considers up to the latest 80 breakpoints" | type: official
- [C30] prompt_cache_retention 枚举 in_memory|24h，spec 标记 deprecated（改用 ttl）| src: openapi.yaml ModelResponseProperties | quote: "Deprecated. Use `prompt_cache_options.ttl` instead. ... Set to `24h` to enable extended prompt caching" | type: official
- [C31] prompt_cache_key：旧模型用于路由优化，GPT-5.6+ 用于分账；`user` 字段 deprecated、"being replaced by safety_identifier and prompt_cache_key" | src: openapi.yaml + guide | quote: "This field is being replaced by `safety_identifier` and `prompt_cache_key`." | type: official
- [C32] cached token 仍计 TPM 限额；不改输出 | src: guide FAQ | quote: "Cached input tokens still count toward tokens-per-minute limits." | type: official
- [C33] 隔离：不跨组织共享、不跨区域处理边界 | src: guide | quote: "Caches are not shared across organizations and cannot be reused across regional processing boundaries." | type: official
- [C34] prompt_cache_key 隔离同组织内不同用户，防 cache-hit probing | src: guide | quote: "separate keys help prevent cache-hit probing across users: submitting candidate prompts and observing cache hits" | type: official
- [C35] Batch 对象 usage 含 input_tokens_details.cached_tokens（batch 请求计入缓存）；定价页 Batch 档有 cached input 价 | src: openapi.yaml Batch schema | quote: "cached_tokens: ... The number of tokens that were retrieved from the cache." | type: official

## conflicts
- guide 对更早模型仍推荐 prompt_cache_retention（"prefer setting prompt_cache_retention to \"24h\""），而 OpenAPI spec 已将其标 deprecated（"Use prompt_cache_options.ttl instead"），但 ttl 仅 GPT-5.6+ 支持——两代模型文档口径交错。
- lookup 边界口径：guide 写 "The first 2 and latest 50 explicit breakpoints ... up to 20 earlier eligible message endings"，OpenAPI PromptCacheOptionsParam 写 "considers up to the latest 80 breakpoints in the conversation"——数字范围不同（请求内候选 vs 会话内考虑），未裁决。

## gaps
- 发布时间与历史起点未取到（openai.com/index/prompt-caching 403）。
- Realtime API 是否走 prompt caching 未在 guide/spec 中确认。
- Batch 文档未明示「Batch 请求自动享受缓存」原句（仅 Batch usage schema 含 cached_tokens 佐证）。
- guide 页未见更新日期。

## leads
- Prompt Cache Diagnostics 工具 + comparison_response_id 可做 miss 诊断（guide "Prompt cache diagnostics" 页）。
- 2025 前后旧版文档（platform.openai.com 存档）对 gpt-4o/o1 时代的 1,024-token 阈值说法可查 archive.org 补历史。
