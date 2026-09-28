# r2-kimi
question: Kimi / Moonshot 官方 API 现在的上下文缓存怎么触发、边界、门槛、TTL、计费、观测字段、失效条件、哪些接口和模型可用。Chat/Responses 与 Anthropic 兼容接口若规则不同，分开记。
checked: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api ; https://platform.kimi.com/docs/api/chat.md ; /api/responses.md ; /api/messages.md ; /docs/pricing/chat ; /pricing/batch.md ; /docs/models.md ; /docs/changelog/index.md ; /docs/openapi.json ; https://platform.kimi.com/blog/posts/context-caching ; https://api.moonshot.cn/v1/caching (probe)
注：D1触发 D2边界 D3门槛 D4TTL D5计费 D6观测 D7失效 D8接口/模型（按简报顺序假定）；文档页均无发布日期，检索日 2026-09-24。G=guide页 C=chat R=responses M=messages P=pricing。

## claims
- [C1] platform.moonshot.cn 整站 301 至 platform.kimi.com（含 /docs 旧链） | src: https://platform.moonshot.cn/docs | quote: "301 https://platform.kimi.com/docs" | type: official（实测）
- [C2][D1/D2] 现行为隐式前缀缓存：messages 开头连续 token 序列按最长匹配前缀命中 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "缓存按最长匹配前缀计算，匹配成功即为命中" | type: official
- [C3][D1] Chat/Responses 不传 prompt_cache_options 即默认按 5m 档自动写入并计费；mode 仅 implicit | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "不传 prompt_cache_options 时，系统默认使用 5m TTL：满足命中条件的前缀会自动写入并尝试复用，账单上会产生相应的缓存写入费用" | type: official
- [C4][D4] TTL 仅 5m、1h 两档且相互独立 | src: https://platform.kimi.com/docs/api/chat.md | quote: "仅支持 5m、1h 两档（默认 5m），两档缓存相互独立" | type: official
- [C5][D4] TTL 首次写入锁定不可改写；命中按原 TTL 免费续期；完全过期后才能用新 TTL 重写 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "缓存条目的 TTL 在首次写入时锁定，不能改写：相同前缀命中后按原 TTL 免费续期" | type: official
- [C6][D2] 前缀任一处变化则其后内容不可复用；稳定内容置前、动态内容置后 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "前缀中任何一处发生变化，该位置之后的内容都无法复用" | type: official
- [C7][D2] 缓存按组织（org）隔离：同组织共享、跨组织不共享 | src: https://platform.kimi.com/docs/api/chat.md | quote: "缓存以组织（org）为粒度隔离，组织之间不共享缓存" | type: official
- [C8][D7] 不支持手动清除；前缀超过所选 TTL 无活动即自动过期 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "缓存不支持手动清除；缓存前缀无活动超过所选 TTL 后自动过期" | type: official
- [C9][D7] Chat/Responses 无显式断点：content 含 prompt_cache_breakpoint 即 HTTP 400 | src: https://platform.kimi.com/docs/api/chat.md | quote: "content 中出现 prompt_cache_breakpoint 时请求会被拒绝（HTTP 400）" | type: official
- [C10][D1] Chat/Responses 另有 prompt_cache_key（session/task id）提升命中率；Kimi Code Plan 必填 | src: https://platform.kimi.com/docs/api/chat.md | quote: "对于 Coding Agent，通常是代表单个会话的 session id 或 task id" | type: official
- [C11][D8] Anthropic Messages 用顶层 cache_control={type:ephemeral,ttl:5m|1h} 写入；省略则只读 5m 档不写入不收费 | src: https://platform.kimi.com/docs/api/messages.md | quote: "不传时本次请求只尝试读取缓存（5m 档），不写入缓存，不产生缓存写入费用" | type: official
- [C12][D8] Messages 消息体内同名 cache_control 标记被忽略，仅顶层生效 | src: https://platform.kimi.com/docs/api/messages.md | quote: "messages 消息体内的 cache_control 标记会被忽略" | type: official
- [C13][D5] kimi-k3 缓存价每 1M：未命中 ¥20、Cache Write 5m ¥20、1h ¥40、命中 ¥2 | src: https://platform.kimi.com/docs/pricing/chat | quote: "[\"kimi-k3\", \"1M tokens\", \"¥20.00\", \"¥40.00\", \"¥2.00\", \"¥20.00\", \"¥100.00\"]" | type: official
- [C14][D5] 缓存命中价为未命中价 1/10（kimi-k3 例）；Cache Write 现单独列为计费项 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "缓存命中价格仅为未命中价格的 1/10" | type: official
- [C15][D5] K2 系列价表仅命中/未命中两列无 Cache Write 列：k2.7-code ¥1.30/¥6.50、highspeed ¥2.60/¥13.00、k2.6 ¥1.10/¥6.50 | src: https://platform.kimi.com/docs/pricing/chat | quote: "[\"kimi-k2.7-code\", \"1M tokens\", \"¥1.30\", \"¥6.50\", \"¥27.00\", \"262,144 tokens\"]" | type: official
- [C16][D5] 计费逻辑仅声明 K3 缓存写入按 TTL 档单独计费 | src: https://platform.kimi.com/docs/pricing/chat | quote: "对于 K3 系列模型，缓存写入按 TTL 档位（5min / 1h）单独计费" | type: official
- [C17][D5] Batch 亦列命中价：k2.7-code(Batch) ¥0.78、k2.6(Batch) ¥0.66 每 1M | src: https://platform.kimi.com/docs/pricing/batch.md | quote: "[\"kimi-k2.7-code（Batch）\", \"1M tokens\", \"¥0.78\", \"¥3.90\", \"¥16.20\"]" | type: official
- [C18][D6] Chat 观测：usage.prompt_tokens_details.cached_tokens（读）/cache_write_tokens（写）+顶层 usage.cached_tokens；三者互斥和为 prompt_tokens | src: https://platform.kimi.com/docs/api/chat.md | quote: "cached_tokens、cache_write_tokens 与未缓存部分互斥，三者之和等于 prompt_tokens" | type: official
- [C19][D6] Responses 观测：usage.input_tokens_details.cached_tokens/cache_write_tokens；响应顶层回显实际应用的 prompt_cache_options（Chat 不回显） | src: https://platform.kimi.com/docs/api/responses.md | quote: "响应顶层会回显服务端实际应用的 prompt_cache_options，以其返回为准" | type: official
- [C20][D6] Messages 观测：cache_read_input_tokens、cache_creation_input_tokens、cache_creation.ephemeral_5m/1h_input_tokens；input_tokens 不含缓存读写 | src: https://platform.kimi.com/docs/api/messages.md | quote: "总输入 = input_tokens + cache_read_input_tokens + cache_creation_input_tokens" | type: official
- [C21][D6] Chat 流式须 stream_options.include_usage=true 才在最后 chunk 出缓存明细 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "需要设置 stream_options.include_usage=true，完整的缓存读写明细才会出现在最后一个 chunk 的 usage 字段中" | type: official
- [C22][D7] Messages 的 output_config.effort 切换档位破坏前缀缓存命中 | src: https://platform.kimi.com/docs/api/messages.md | quote: "切换档位会破坏前缀缓存命中，建议在会话开始前确定" | type: official
- [C23][D6] Messages 的 metadata.user_id 稳定 ID 用于提高缓存命中率 | src: https://platform.kimi.com/docs/api/messages.md | quote: "标识终端用户或会话的稳定 ID，用于提高缓存命中率与滥用检测" | type: official
- [C24][D8] 现行模型：kimi-k3（1M ctx）、kimi-k2.7-code/-highspeed、kimi-k2.6（256k）；moonshot-v1 全系 2026-08-31 下线 | src: https://platform.kimi.com/docs/models.md | quote: "moonshot-v1 系列模型（含 moonshot-v1-auto 及 -vision-preview 版本）已于 2026 年 8 月 31 日下线" | type: official
- [C25][D8] Responses API 当前仅支持 kimi-k3；Anthropic Messages 请求模型枚举亦仅 kimi-k3 | src: https://platform.kimi.com/docs/api/responses.md | quote: "本接口当前支持 kimi-k3" | type: official
- [C26][D8] Anthropic 兼容端点 base URL：https://api.moonshot.cn/anthropic（POST /anthropic/v1/messages） | src: https://platform.kimi.com/docs/api/messages.md | quote: "只需把 base URL 指向 https://api.moonshot.cn/anthropic" | type: official
- [C27][D8] 现行 OpenAPI 无 /v1/caching；实测 POST 返 404 url.not_found（对照 chat/completions 401）；旧文档页 /docs/api/caching、/docs/pricing/caching 软 404 | src: https://api.moonshot.cn/v1/caching | quote: "\"error\":\"url.not_found\",\"message\":\"没找到对象\" ... \"url\":\"/v1/caching\"" | type: official（实测 2026-09-24）
- [C28] 2024-07-01 公测博客为旧显式资源型 API：POST /v1/caching 建 cache、role="cache" 引用、ttl 秒级、dry_run 可选 | src: https://platform.kimi.com/blog/posts/context-caching | quote: "你可以直接使用 role=\"cache\"来引用一段已经创建好的 cache" | type: official（2024-07-01）
- [C29] 旧 API 计费：创建 24元/M token、存储 10元/M/分钟、调用 0.02元/次；公测仅 Tier5 | src: https://platform.kimi.com/blog/posts/context-caching | quote: "按照 Cache 中 Tokens 按实际量计费。24元/M token" | type: official（2024-07-01）
- [C30] 时间线：2024-07 公测→2024-11 全量且续期免创建费→2025-10 下线手动 Cache 展示 | src: https://platform.kimi.com/docs/changelog/index.md | quote: "Context Caching 功能放开给全量用户，Cache 续期不再收取创建费用" | type: official

## conflicts
- 2024-07-01 官方公测博客的显式资源型缓存（POST /v1/caching、role="cache"、存储 10元/M/分钟、调用 0.02元/次）与现行文档/OpenAPI 不符；实测端点已 404，旧文档页软 404。无官方 deprecation 公告原文，按现行文档应视为已下线。

## gaps
- 最小可缓存前缀长度/门槛未量化（仅"满足命中条件的前缀"）；token 边界要求未说明。
- K2 系列缓存写入是否单独计费未写明（价表无 Cache Write 列，计费逻辑只提 K3）。
- "Cache Write 单独计费"上线日期未见 changelog 条目；文档页均无发布时间。
- Messages/Responses 模型枚举仅 kimi-k3，K2 能否走这两接口未明说。
- 缓存容量上限、每 org 条目数、前缀是否跨模型共享未说明。

## leads
- https://platform.kimi.com/docs/llms-full.txt 与 /docs/openapi.json 可机器校验全量字段。
- 旧显式缓存 API 考古：platform.kimi.com/blog/posts/enhance-kimi-api-bot-with-context-caching。
