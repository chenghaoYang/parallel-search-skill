# 大模型 API 的 prompt caching 对照

> 默认要不要改请求、命中怎么计费、能活多久、看哪个字段算命中。截至 2026-09-24。Kimi、智谱、通义见第 5 节。

## 0. 一屏看懂

1. **OpenAI、DeepSeek、Gemini 隐式都不改请求就可能命中**（均默认开启）[1][6][9]。DeepSeek 会忽略 `cache_control` [8]。
2. **「Anthropic 必须逐块打点」已过时。** 2026-02-19 起顶层一次 `cache_control` 就会自动前移断点 [3][5]。块级仍在，最多 4 个，`type` 仅 `ephemeral` [3]。零标记见第 5 节。
3. **OpenAI 的自动不是没有开关。** 默认 implicit。gpt-5.6+ 若 `mode=explicit` 且没有 `prompt_cache_breakpoint`，这次请求不缓存 [1][22]。
4. **账单分三族。** 写溢价+读折扣：Anthropic，以及 OpenAI GPT-5.6+。无写费、只分命中/未命中：GPT-5.5 及更早，DeepSeek 定价页也只有这两档。读折扣+存储费：Gemini 显式。隐式只写会让利，倍率 ∅。
5. **TTL 不能套用。** Anthropic 默认 5 分钟且命中刷新。OpenAI GPT-5.6+ 至少 30 分钟。Gemini 显式默认 1 小时。DeepSeek 无固定时长，闲置后通常几小时到几天。隐式页没写。
6. **没报错不等于命中。** 只看命中表。Chat 与 Responses、generateContent 与 Interactions 路径不同。
7. **前缀必须整段一致。** DeepSeek 还要求对齐整块已落盘单元：`A+B` 之后的 `A+C` 不命中 [7]。OpenAI 不能手动清缓存 [1]。
8. **同名不是同一产品。** Gemini 隐式不保证省钱；显式在 TTL 内保证，但是 Beta，除过期时间外不能改 [9]。OpenRouter 上免费的是 `X-OpenRouter-Cache` 整段响应 [13]。

## 1. Taxonomy

分类轴：**默认路径要不要放缓存标记。** 它决定改不改代码，决定不了价钱（GPT-5.6+ 零标记仍收 1.25× 写费）。

| 家族 | 默认路径 | 成员 | 为什么是一类 |
|---|---|---|---|
| F-自动 | 不改请求就可能命中 | OpenAI（默认 implicit）、DeepSeek、Gemini 隐式 | 调用方定不了断点位置 |
| F-标记 | 写出的启用方式都带标记 | Anthropic | 标记决定写入哪一段 |
| F-资源 | 先创建对象，请求只引用名字 | Gemini 显式 | 独立 TTL，创建后不能改内容 |
| F-网关 | 缓存在上游 | OpenRouter | 差异在转译和路由 |

`mode=explicit` 是 OpenAI 的开关，不是新家族。列 D1–D9：触发、键、门槛、TTL、计费、命中字段、失效、范围、模型与保证。

## 2. 对照矩阵

❓ 无原句。∅ 查过但页上没有。⚠ 只有过期公告。

### 触发与键

| 实体 | D1 | D2 |
|---|---|---|
| OpenAI | 默认开。可选 `prompt_cache_key`、弃用的 `prompt_cache_retention`、`prompt_cache_options`（gpt-5.6+；Responses 列出 `mode`/`ttl`/`prewarm`/`comparison_response_id`）、`prompt_cache_breakpoint`。implicit：自动 1+最多 3 显式；explicit：不自动放、最多 4 [1][2][22] | 同组织同区域：负载+前缀哈希+`prompt_cache_key`。5.6+ 路由自动，key 只分账 [1] |
| Anthropic | 顶层 `cache_control`，或标在 content block。顶层打到最后一个可缓存块 [3][4] | `tools`→`system`→`messages`，直到标记块。一断点一条哈希；读取回看 20 block [3] |
| Gemini 隐式 | 2.5+ 默认开。Interactions 有状态/无状态都支持 [9][10] | ❓ 只建议公共内容放开头并短时间重发 |
| Gemini 显式 | `POST /v1beta/cachedContents`；请求字段 `cachedContent`=`cachedContents/{id}` [14][15] | 具名资源作前缀，绑定创建时的模型 [9][14] |
| DeepSeek | 默认开。`cache_control` 忽略。`user_id` 只隔离 KV [6][8][16] | 从第 0 token 起的输入前缀；中间重复不算；单元须整段匹配。输出不缓存 [6][11] |
| OpenRouter | 多数上游自动。顶层 `cache_control`：Anthropic、Vertex、Azure、Bedrock。`cache_control`↔`prompt_cache_breakpoint`，TTL 不互译。粘性键 `session_id` / `x-session-id`，否则 `prompt_cache_key` [12] | 在供应商侧 [13] |

### 门槛、TTL、价钱

| 实体 | D3 | D4 | D5 |
|---|---|---|---|
| OpenAI | 5.6+：1024 可见 token。更早随 tools/images/schemas/reasoning/verbosity 变 [1] | 5.6+ `ttl` 仅 `30m`，复用续期且不再收写费。更早 `in_memory`：约 5–10 分钟无活动、至多 1 小时。无 ZDR 自 2026-05-29 默认 `24h`。见第 5 节 [1][2][17] | 5.6+ 写 1.25×、读 0.1×（最高 90%）。5.5 及更早无写费。gpt-5.6-sol：$4 / $0.40 / $5 / $20（笔记：input/cached/write/output）[1] |
| Anthropic | 512：Fable 5.1、Mythos 5.1、Opus 5.5、Opus 5、Fable 5、Mythos 5。1024：Opus 4.8、Sonnet 5/4.6/4.5。不足不缓存、不报错 [3] | 默认 5 分钟；`ttl`=`5m` 或 `1h`；命中免费刷新 [3][4] | 5 分钟写 1.25×，1 小时写 2×，读 0.1×（Fable 5.1 与 Mythos 5.1 为 0.025×，Opus 5.5 为 0.05×）[18] |
| Gemini 隐式 | ❓ 有表，摘录无数字 | ∅ | ∅ 只写命中会转嫁节省 |
| Gemini 显式 | ❓ 最小值因模型而异 | 默认 1 小时；`ttl`（如 `300s`）或 `expireTime`；无上下限；只能 PATCH 过期时间 [9][14] | 降价读 + 按 TTL 存储。2.5 Flash：文/图/视频 $0.03/1M，音频 $0.1/1M，存储 $1/1M token/小时。2.5 Pro：读 $0.125/1M（≤200k），存储 $4.50 [9][19] |
| DeepSeek | ⚠ 64 token 只在 2024 公告，该页称价格已更新 [11] | 无固定 TTL；闲置后通常几小时到几天 [6] | USD/1M（flash/v4-pro）：命中空闲 $0.003/$0.022、高峰 $0.006/$0.044；未命中空闲 $0.15/$0.66、高峰 $0.30/$1.32。高峰=工作日 UTC 01:00–04:00 与 06:00–10:00，不含中国节假日；空闲为一半。人民币命中摘录：空闲 0.02/0.15 元，高峰 0.04/0.30 元 [20][21] |
| OpenRouter | 有的模型最短 1024 token [12] | 随上游：Anthropic 5 分钟可 1 小时；它写 Gemini 隐式平均 3–5 分钟（官方 ∅）；OpenAI 显式最短 30 分钟。自身 10 分钟只重置粘性路由 [12] | ❓ 摘录只钉住 Anthropic 写 1.25×、读 0.1×，以及 GPT-5.6+ 写 1.25×（自动也收） |

### 命中字段

| 实体 | 字段 |
|---|---|
| OpenAI Responses | `usage.input_tokens_details.cached_tokens`、`cache_write_tokens`。`prompt_cache_diagnostics`（2026-09-08 GA）的 miss `reason` 含 `model_changed`、`tools_changed`、`input_changed` 等 [1][2] |
| OpenAI Chat | `usage.prompt_tokens_details.cached_tokens`、`cache_write_tokens`。implicit/explicit 的断点个数写在这份 Chat 参考 [22] |
| Anthropic | `cache_read_input_tokens`、`cache_creation_input_tokens`；1h 写入另见 `cache_creation.ephemeral_1h_input_tokens` 与 `ephemeral_5m_input_tokens` [3][4] |
| Gemini generateContent | `usageMetadata.cachedContentTokenCount`（计入 `promptTokenCount`）；`cacheTokensDetails[]` 按模态 [15] |
| Gemini Interactions | `usage.total_cached_tokens`。此 API 只有隐式 [10] |
| DeepSeek | `prompt_cache_hit_tokens`、`prompt_cache_miss_tokens`；`prompt_tokens_details.cached_tokens` 等于 hit；`prompt_tokens`=hit+miss [7][16] |
| OpenRouter | `usage.prompt_tokens_details.cached_tokens` 与 `cache_write_tokens`；Responses 用 `input_tokens_details`。`cache_discount` 写为负、读为正 [12] |

### 范围、失效、保证

| 实体 | D7 失效 | D8 范围 | D9 |
|---|---|---|---|
| OpenAI | 断点前一变则后面失配。A 改成 A+B 且无显式断点则不复用。设置：`model` `tools` `parallel_tool_calls` `text.format` `reasoning.effort` `text.verbosity` `context_management`。不能手清 [1] | 隐藏 instructions、developer、工具、text/images/documents/支持的 audio。存 KV，不跨组织/区域 [1] | 不保证。同一 prefix+key 约 15 次/分钟会溢出 [1] |
| Anthropic | 改工具名/描述/参数、`tool_choice` 或图片增删则整段失效，并沿 tools→system→messages 下传。标记前须 100% 相同 [3] | 工具、system、text、图片、文档、`tool_use`/`tool_result`。thinking 不能直接打标记 [3] | 现役模型，GA，无 beta 头。Batches best-effort；并发等第一个响应开始。平台见第 5 节 [3][5] |
| Gemini 隐式 | ❓ 只有「短时间、相似前缀」的建议 | ❓ | 2.5+，不保证省钱 [9] |
| Gemini 显式 | 除过期时间外不能改，可 DELETE [9][14] | `contents`、`tools`、`toolConfig`、文本 `systemInstruction`；视频/PDF 经 Files API [9][14] | Beta `v1beta`，文档写有省钱保证。Interactions 不可用 [9][10] |
| DeepSeek | `A+B` 不能被 `A+C` 命中；公共前缀 A 落盘后，`A+D` 才命中 A。落盘：请求结束、公共前缀检测、固定间隔 [6][7] | 多轮须原样拼回 system + 上轮 user + assistant + 新 user [6] | 仅 `deepseek-flash`、`deepseek-v4-pro`。best-effort。`deepseek-chat`/`reasoner` 不在枚举 [16] |
| OpenRouter | 失效随上游；粘性路由另计 10 分钟 [12] | ❓ | 不用自己建 Gemini cache 或管 TTL。Qwen 快照端点不支持显式缓存 [12] |

## 3. 变体与适配层

转译、名单、代管和 10 分钟粘性见第 2 节。网关自己的一层：`X-OpenRouter-Cache: true` 在进供应商之前缓存整段响应，TTL 1–86400 秒、默认 300，命中免费，可与 prompt cache 叠加 [13]。Azure、Bedrock、Vertex、火山方舟是否逐字段一致，本轮不写。

## 4. 用户需要知道的坑

1. **看错字段就以为没有缓存。** 以命中表为准。DeepSeek 的 hit 有两个相等名字 [7][16]。
2. **GPT-5.6 第一笔自动写入是 1.25×。** 只有复用才是 0.1×，并续 30 分钟、不再收写费。单发长提示会更贵 [1]。
3. **explicit 却没有断点，OpenAI 整段跳过。** 要自动就留在 implicit [1]。
4. **DeepSeek 只改后半仍会 miss**，直到公共前缀被单独落盘。`user_id` 不同则 KV 隔开 [6][7][16]。
5. **改工具或点名开关会从根上失效**，不是「只改最后一条 user 就安全」[1][3]。命中也不跨机器保证：OpenAI 约 15 次/分钟/prefix+key；写成保证的只有 Gemini 显式 [1][9]。
6. **OpenRouter 的免费缓存是整段响应，10 分钟是粘性路由。** 都不是上游 prompt cache 的 TTL [12][13]。

## 5. 未决与置信度

- Anthropic：指南只写两种启用方式，都含 `cache_control`，但没有「零标记绝不缓存」。反证前不把「必须」写成已排除第三种路径。2048/4096 门槛档摘录未覆盖。2026-02-19 注记只写 Claude API 与 Foundry（preview）；现行指南写除旧版 Bedrock（Opus 4.6 及更早，顶层字段 400）外都可用。
- OpenAI：`prompt_cache_retention` 对 gpt-5.5 / pro 与 “future models” 只写支持 `24h`，指南却要 5.6+ 用 `ttl=30m`。尚未裁定 future 是否含 5.6。`24h`「通常约 30 分钟」、断点回看个数、Chat 是否含 `prewarm`，摘录都不足。
- Gemini 隐式：2026-09-02 与 09-11 两页无 TTL、无失效清单、无倍率、未写是否免存储。4096/2048 不在摘录。显式最小 token 无表。
- DeepSeek：现行指南未复述 64 token。公告上的 $0.014/1M 与「存储免费」已自指定价页。无「无写费」原句，无 flush API。人民币未命中价摘录未覆盖。
- OpenRouter：未写 markup，也无「不存 prompt cache」的否定句。读价 0.25×/0.50×、DeepSeek 0.1×、Gemini 隐式 0.25× 都不在摘录。它写的隐式 3–5 分钟与官方 ∅ 并存。
- 未进表：Kimi、智谱、通义整行是缺口。Azure、Bedrock、Vertex、火山、xAI、Fireworks、MiniMax、Groq 只确认有官方页。

置信度：第 0 节 1–3 的开关、Anthropic/OpenAI 倍率、字段名，高。DeepSeek 美元价高，64 token 低。Gemini 隐式折扣，官方没写。

## 来源

1. OpenAI 指南 — https://developers.openai.com/api/docs/guides/prompt-caching
2. Responses create — https://developers.openai.com/api/reference/resources/responses/methods/create
3. Claude 缓存 — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
4. Claude Messages — https://platform.claude.com/docs/en/api/messages
5. Claude 发布说明 — https://platform.claude.com/docs/en/release-notes/overview
6. DeepSeek KV — https://api-docs.deepseek.com/guides/kv_cache
7. DeepSeek KV 中文 — https://api-docs.deepseek.com/zh-cn/guides/kv_cache
8. DeepSeek Anthropic — https://api-docs.deepseek.com/guides/anthropic_api
9. Gemini 缓存 — https://ai.google.dev/gemini-api/docs/generate-content/caching
10. Gemini Interactions — https://ai.google.dev/gemini-api/docs/caching
11. DeepSeek 2024-08-02 — https://api-docs.deepseek.com/news/news0802
12. OpenRouter 缓存 — https://openrouter.ai/docs/features/prompt-caching
13. OpenRouter 响应缓存 — https://openrouter.ai/docs/guides/features/response-caching
14. cachedContents — https://ai.google.dev/api/caching
15. generateContent — https://ai.google.dev/api/generate-content
16. DeepSeek chat — https://api-docs.deepseek.com/api/create-chat-completion
17. OpenAI changelog — https://developers.openai.com/api/docs/changelog.md
18. Claude 定价 — https://platform.claude.com/docs/en/about-claude/pricing
19. Gemini 定价 — https://ai.google.dev/gemini-api/docs/pricing
20. DeepSeek 定价 — https://api-docs.deepseek.com/quick_start/pricing
21. DeepSeek 定价中文 — https://api-docs.deepseek.com/zh-cn/quick_start/pricing
22. Chat Completions — https://developers.openai.com/api/reference/resources/chat.md
