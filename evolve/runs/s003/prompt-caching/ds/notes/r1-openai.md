# r1-openai
question: OpenAI 官方 API 的 prompt caching 现在怎么工作（自动还是要改请求、计费、TTL、怎么看命中、什么会失效）。
checked: https://developers.openai.com/api/docs/guides/prompt-caching, https://developers.openai.com/api/docs/pricing, https://developers.openai.com/api/reference/resources/chat（platform.openai.com 同名页 301 至此）

## claims
- [C1] D1 默认：对受支持模型默认开启，不改请求体即生效 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Prompt caching is enabled by default for supported OpenAI models." | type: official
- [C2] D1 可选字段 prompt_cache_key（string），取代 user 字段 | src: https://developers.openai.com/api/reference/resources/chat | quote: "Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field." | type: official
- [C3] D1 可选对象 prompt_cache_options {mode, ttl, prewarm}，仅 gpt-5.6+；默认自动放一个隐式 breakpoint | src: https://developers.openai.com/api/reference/resources/chat | quote: "Supported for `gpt-5.6` and later models. By default, OpenAI automatically chooses one implicit cache breakpoint." | type: official
- [C4] D1 mode 枚举 "implicit"|"explicit"，默认 implicit；explicit 且无任何 breakpoint 时该请求不缓存 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "When no explicit breakpoints are placed, the request does not use prompt caching or create cache writes." | type: official
- [C5] D1 prompt_cache_retention 枚举 "in_memory"|"24h"，API ref 已标 Deprecated | src: https://developers.openai.com/api/reference/resources/chat | quote: "Deprecated. Use `prompt_cache_options.ttl` instead." | type: official
- [C6] D1 内容块级 prompt_cache_breakpoint {mode:"explicit"} 标记前缀终点 | src: https://developers.openai.com/api/reference/resources/chat | quote: "Marks the exact end of a reusable prompt prefix. The breakpoint inherits its TTL from the request's `prompt_cache_options.ttl`" | type: official
- [C7] D2 缓存单元是前缀 KV tensor；渲染上下文含隐藏系统指令、developer 消息、工具定义、文本/图像/文档/音频历史 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "The prompt cache stores key-value (KV) tensors, not the tokens themselves." | type: official
- [C8] D2/D3 命中要求渲染前缀完整匹配；breakpoint 前的任何内容或相关设置变更使其后前缀不可命中 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cache reuse requires the entire rendered prefix to match." | type: official
- [C9] D2 5.6+ 隐式 breakpoint 在最新 eligible 消息末尾；更早模型按模型相关间隔；显式每请求至多 4 个写入 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "When `prompt_cache_options.mode` is `implicit`, OpenAI places a breakpoint at the end of the latest eligible message." | type: official
- [C10] D3 命中门槛：5.6+ 最低 1,024 可见 input token，隐藏系统 token 不计；更早模型随请求设置（tools/images/schema/reasoning/verbosity）变化 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later and varies by request settings for earlier models." | type: official
- [C11] D3 命中依赖路由到持有缓存的单机：哈希初始 token + prompt_cache_key，单 key 建议约 15 rpm 总量 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cached states live on individual machines, where traffic above 15 requests per minute can lead to overflow routing." | type: official
- [C12] D4 5.6+ 倍率：write 1.25×、read 0.1× uncached input；write 非叠加费 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "cache writes cost 1.25× the standard, uncached input-token rate. [...] subsequent reads cost only 0.1× that rate." | type: official
- [C13] D4 更早模型按各自 cached-input 价、无 write 加价；折扣最高 90% | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Pay the model's reduced cached-input rate for reused tokens, discounted up to 90%." | type: official
- [C14] D4 价目（Standard/1M tok）：gpt-5.6-sol $4.00/cached $0.40/write $5.00；gpt-5.1 $1.25/$0.125/write "-"；gpt-5-pro、o1-pro 等 cached 列为 "-" | src: https://developers.openai.com/api/docs/pricing | quote: "| gpt-5.6-sol | $4.00 | $0.40 | $5.00 | $20.00 | [...] | gpt-5.1 | $1.25 | $0.125 | - | $10.00 |" | type: official
- [C15] D4 cached token 仍计入 TPM 限速 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Yes. Cached input tokens still count toward tokens-per-minute limits." | type: official
- [C16] D5 5.6+ TTL：prompt_cache_options.ttl 唯一值且默认 "30m"，自最近写入/复用起至少 30 分钟可复用 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "The only supported value, `30m`, is also the default. A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse" | type: official
- [C17] D5 更早模型：in_memory 不活跃 5–10 分钟至多 1 小时；24h 典型约 30 分钟至多 24 小时；复用刷新存活且不再收 write 费 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "`in_memory`: Entries typically remain active for around 5 to 10 minutes of inactivity, up to one hour." | type: official
- [C18] D5/D8 默认保留按 ZDR 分：无 ZDR 默认 "24h"，有 ZDR 默认 "in_memory"；gpt-5.5/5.5-pro 仅支持 "24h" | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Organizations _without_ Zero Data Retention enabled default to `24h`. Organizations _with_ Zero Data Retention enabled default to `in_memory`." | type: official
- [C19] D6 Responses 观测字段 usage.input_tokens_details.cached_tokens 与 .cache_write_tokens | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Track `usage.input_tokens_details.cached_tokens`, `usage.input_tokens_details.cache_write_tokens`" | type: official
- [C20] D6 Chat Completions 字段 usage.prompt_tokens_details.cached_tokens / .cache_write_tokens | src: https://developers.openai.com/api/reference/resources/chat | quote: "`cache_write_tokens: optional number` The unadjusted number of prompt tokens written to cache. `cached_tokens: optional number` Cached tokens present in the prompt." | type: official
- [C21] D6 官方监控：Prompt Caching Dashboard + Diagnostics 工具；更早模型上报值减隐藏 token 后向下取整 128 倍数 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "rounding down to the nearest multiple of 128" | type: official
- [C22] D7 点名影响前缀的设置：model、tools、parallel_tool_calls、text.format、reasoning.effort、text.verbosity、context_management | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "`tools` | Changes tool names, descriptions, schemas, ordering, or tool-specific instructions." | type: official
- [C23] D7 不能手动清缓存；compaction 与延长已有消息亦降低复用 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "No. Manual cache clearing is not currently available. Cache entries expire according to the model's cache lifetime and retention settings." | type: official
- [C24] D8 缓存按组织隔离、不能跨 regional processing 边界复用 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Caches are not shared across organizations and cannot be reused across regional processing boundaries." | type: official
- [C25] D8 不同 prompt_cache_key 隔离计费归属、防跨用户 cache-hit 探测；Agents API 行为同 Responses | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "separate keys help prevent cache-hit probing across users" | type: official

## conflicts
- prompt_cache_retention：API ref 标 "Deprecated. Use `prompt_cache_options.ttl` instead" 且称 "For `gpt-5.5`, `gpt-5.5-pro`, and future models, only `24h` is supported"（api/reference/resources/chat）；指南仍把它列为 earlier models 的现行 TTL 控制（api/docs/guides/prompt-caching 表 "Cache lifetime control" 行）。"future models" 措辞与 5.6 改用 ttl 不自洽。

## gaps
- ZDR 组织能否显式选 "24h"：页面只说默认值不同并让 "Verify the available retention policies"，未明说禁用。
- changelog/launch 公告被 SSRF 拦：2024-10-01 上线条目、prompt_cache_options/explicit breakpoint 引入版本未取原文。
- 页面无更新日期；Responses create 参考页未抓到（prewarm 仅见于指南示例）。
- pre-5.6 无 explicit mode；能否彻底关闭缓存未说明。

## leads
- Prompt Cache Diagnostics 专页 https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics
- openai.com/index/api-prompt-caching（2024-10-01 发布稿，被拦；二手摘要称上线即自动、当时折扣 50%）
- compaction、tool search defer_loading、configuration_update 的缓存交互在各专题页
