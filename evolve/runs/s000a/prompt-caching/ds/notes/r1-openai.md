# r1-openai
question: OpenAI 官方 API 的 prompt caching 现在如何触发、如何划定前缀、门槛与 TTL、怎么计费、响应里如何看见命中、什么改动会失效、哪些模型可用以及缓存跟谁隔离。
checked: https://developers.openai.com/api/docs/guides/prompt-caching.md, https://developers.openai.com/api/docs/pricing.md, https://developers.openai.com/api/reference/resources/responses/methods/create.md, https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml

## claims
- [C1] D1: 默认开启、无需改代码（"自动缓存"说法仍成立） | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Prompt caching is enabled by default for supported OpenAI models." | type: official
- [C2] D1: 首请求写前缀，后续请求往回找最长匹配断点 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "look for the longest matching cached prefix available, working backward through eligible breakpoints until they find a match" | type: official
- [C3] D1: 缓存在单机，路由=隐藏 system 后前缀哈希(含 tools)+prompt_cache_key；同前缀 >15 req/min 溢出 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cached states live on individual machines, where traffic above 15 requests per minute can lead to overflow routing." | type: official
- [C4] D2: 前缀边界单位是 cache breakpoint；范围=完整渲染上下文（隐藏指令、developer 消息、tools、历史、图片/文件/音频） | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "OpenAI caches the model's full rendered context including OpenAI-provided instructions" | type: official
- [C5] D2: GPT-5.6+ 隐式断点在最新合格消息末尾（user/连续 tool response 末尾/初始 developer 块末尾）；GPT-5.5 为固定 2,048-token 间隔，更早模型为模型相关间隔 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "OpenAI places a breakpoint at the end of the latest eligible message." | type: official
- [C6] D2: 显式断点=内容块加 prompt_cache_breakpoint:{"mode":"explicit"}，每请求最多 4 次写入；explicit-only 无断点则不缓存 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "Marks the exact end of a reusable prompt prefix. The breakpoint inherits its TTL from the request's `prompt_cache_options.ttl`" | type: official
- [C7] D3: 最小可缓存前缀 GPT-5.6+ =1,024 可见输入 token（隐藏 token 不计入），更早模型随请求设置变化；旧模型上报值取整到 128 倍数 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later and varies by request settings for earlier models." | type: official
- [C8] D4: GPT-5.6+ 用 prompt_cache_options.ttl，唯一值 "30m" 即默认；最近写入或复用后≥30 分钟且复用免费刷新寿命 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "The only supported value, `30m`, is also the default." | type: official
- [C9] D4: 更早模型用 prompt_cache_retention: "in_memory"≈5–10 分钟不活跃(最长1h)；"24h"通常~30分钟、最长24h | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Entries typically remain active for around 5 to 10 minutes of inactivity, up to one hour." | type: official
- [C10] D4: retention 默认随组织 ZDR：无 ZDR→"24h"，有 ZDR→"in_memory" | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "Organizations without ZDR enabled default to `24h`." | type: official
- [C11] D5: GPT-5.6+ 写缓存 1.25×、读命中 0.1× 未缓存输入价，非附加费(三价取一)；更早模型无 cache-write 费、按各模型 cached-input 价；命中 token 仍计 TPM 限速 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "cache writes cost 1.25× the standard, uncached input-token rate" 与 "subsequent reads cost only 0.1× that rate" | type: official
- [C12] D5: 定价页实价(Standard/短上下文,$/1M): gpt-5.6-sol $4.00/$0.40cached/$5.00write; gpt-5 $1.25/$0.125; gpt-4.1 $2.00/$0.50; gpt-4o $2.50/$1.25 — 倍数因模型而异 | src: https://developers.openai.com/api/docs/pricing | quote: "| gpt-5.6-sol | $4.00 | $0.40 | $5.00 | $20.00 |" | type: official
- [C14] D6: Responses 响应 usage.input_tokens_details.{cached_tokens,cache_write_tokens} | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "`cached_tokens` The number of tokens that were retrieved from the cache." | type: official
- [C15] D6: Chat Completions 响应 usage.prompt_tokens_details.{cached_tokens,cache_write_tokens} | src: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml | quote: "cached_tokens: ... description: Cached tokens present in the prompt." | type: official
- [C16] D6: 响应可带 prompt_cache_diagnostics（cache_hit/cache_miss+cache_missed_tokens），reason 枚举 9 值（model_changed、tools_changed、context_compacted、service_tier_changed 等）；另有 Caching Dashboard | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "The reason prompt cache reuse did not occur." | type: official
- [C17] D7: 失效面=断点前内容或相关设置变化：model、tools(名/schema/顺序)、parallel_tool_calls、text.format、reasoning.effort、text.verbosity、context_management(compaction) | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "If content or a relevant setting changes before a breakpoint, the prefix after that change cannot match the existing cache entry." | type: official
- [C18] D7: 结构失效：隐式→explicit-only 不复用旧隐式前缀；加长同一消息使旧端点失配；不能手动清缓存 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Manual cache clearing is not currently available." | type: official
- [C19] D8: 缓存不跨组织、不跨 regional processing 边界 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Caches are not shared across organizations and cannot be reused across regional processing boundaries." | type: official
- [C20] D8: GPT-5.6+ 的 prompt_cache_key 仅用于分账与防 cache-hit probing；旧模型上用于路由优化 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "You can use separate keys to maintain separate cache accounting for customers or users within your application." | type: official
- [C21] 字段: prompt_cache_key 存在(Responses/Chat 共用 schema ModelResponseProperties)，取代 user 字段 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "Replaces the `user` field." | type: official
- [C22] 字段: prompt_cache_retention 存在(Deprecated)，枚举 "in_memory"|"24h"；gpt-5.5/pro 及更新仅 "24h" | src: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml | quote: "Deprecated. Use `prompt_cache_options.ttl` instead." | type: official
- [C23] 字段: prompt_cache_options={mode,ttl,prewarm,comparison_response_id} 仅 gpt-5.6+；mode 默认 implicit | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "Supported for `gpt-5.6` and later models." | type: official
- [C24] 模型面: 24h 扩展保留支持 gpt-5.5/pro, gpt-5.4, gpt-5.2, gpt-5.1 系列, gpt-5, gpt-5-codex, gpt-4.1 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Extended retention is supported by `gpt-5.5`, `gpt-5.5-pro`, `gpt-5.4`, `gpt-5.2`" | type: official
- [C25] 模型面: 定价表 cached input 列 "-" 者无缓存价：gpt-5.5-pro、gpt-5-pro、o1-pro、o3-pro、gpt-4-turbo、gpt-3.5 等 | src: https://developers.openai.com/api/docs/pricing | quote: "| gpt-5-pro | $15.00 | - | - | $120.00 |" | type: official
- [C26] 版本: 指南页 HTTP Last-Modified 2026-09-23；openai-openapi openapi.yaml 最近提交 2026-09-23 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "last-modified: Wed, 23 Sep 2026 19:52:33 GMT" | type: official

## conflicts
- lookup 边界口径不一：指南写 implicit 查 "first 2 and latest 50 explicit breakpoints, the implicit breakpoint, up to 20 earlier eligible message endings"；reference 写 "up to the latest 80 breakpoints in the conversation"（https://developers.openai.com/api/reference/resources/responses/methods/create）
- prompt_cache_retention 地位矛盾：reference/spec 标 "Deprecated. Use `prompt_cache_options.ttl` instead."，但 ttl 仅限 gpt-5.6+，旧模型寿命控制仍只有它。

## gaps
- pre-5.6 各模型最小可缓存长度无公开数值表，官方仅写 "varies by request settings"。
- 指南/定价页正文无 Updated 日期，仅 HTTP Last-Modified 与 spec 提交日期。
- Chat Completions 是否回传 prompt_cache_diagnostics 未核实。

## leads
- Azure OpenAI prompt caching 差异（按 brief 不展开）。
- prompt_cache_options.prewarm=true 只写缓存不生成（降 TTFT）。
- diagnostics 指南见 developers.openai.com/api/docs/guides/prompt-caching/diagnostics.md。
