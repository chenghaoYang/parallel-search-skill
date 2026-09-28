# 各家 Prompt Caching 怎么不一样

> 截至 2026-09-24。回答：要不要改请求、字段原名、命中计费、TTL、用哪个 usage 字段确认、什么改动会 miss。先读第 0 节再查表。Kimi、智谱、通义本轮无专职工人笔记。

## 0. 一屏看懂

1. DeepSeek 仍自动：默认开启，不用改代码，每个请求都建硬盘缓存。Chat 看 `prompt_cache_hit_tokens`。人民币价目 Flash 命中=未命中的 1/50，V4 Pro=1/30。不用后一般留几小时到几天。[13][14][15]
2. OpenAI 支持的模型仍默认开启，不必为了打开缓存而加字段。[1]
3. Anthropic 仍要 `cache_control`（没有则 nothing is cached）。顶层一个即可，断点自动前移；`type` 只有 `ephemeral`；beta 前缀已不需要。thinking 见第 5 节。[5][8]
4. Anthropic：5 分钟写 1.25×、1 小时写 2×、读 0.1×（Fable/Mythos 5.1 为 0.025×，Opus 5.5 为 0.05×）。OpenAI 5.6+ 写 1.25×，读 “0.1× that rate”，基数没拆开。[1][5]
5. Gemini 两套并存。隐式 2.5+ 默认开、不保证省钱。显式要先 `POST /v1beta/cachedContents`，默认 TTL 1 小时并按 TTL 收存储。[9][10]
6. OpenRouter 前缀在上游：断点会改写；粘性用 `session_id` 或 `prompt_cache_key`。整响应缓存默认关，看 `X-OpenRouter-Cache-Status`，命中免费。[16][17][24]
7. 共同失效条件：从开头起的整段前缀必须一致。前缀任一处变化，后面的稳定内容也进不了旧条目。[1][5][13]
8. Kimi、智谱、通义：无结论。

## 1. Taxonomy

分类轴：**不传任何缓存字段时，会不会产生 cache read？**

| 家族 | 为什么是一类 | 成员 |
|---|---|---|
| F1 自动前缀 | 不传字段也会读；边界由服务端放在前缀上 | OpenAI 默认、DeepSeek、Gemini 隐式 |
| F2 请求内声明 | 零字段则不缓存；可只放顶层，断点由服务端前移 | Anthropic |
| F3 缓存对象 | 先创建资源，生成请求只引用名字 | Gemini 显式 `cachedContents` |
| F4 网关 | 前缀在上游；网关另做粘性和整响应缓存 | OpenRouter |

GPT-5.6+ 另有可选显式断点，默认仍是 F1。Anthropic 的 automatic 仍要顶层 `cache_control`，不是 F1。维度 D1–D8 即下面各表的列。

## 2. 对照矩阵

### 开关与字段

| 实体 | D1 零字段会不会读 | D2 请求字段 |
|---|---|---|
| OpenAI | 默认开启 [1]。仅 `mode=explicit` 且无 explicit breakpoint 时，该请求不用 prompt caching [2] | `prompt_cache_key`（取代 `user`）[3]；`prompt_cache_retention`=`in_memory`\|`24h` [2]；`prompt_cache_options.ttl` 默认且只支持 `30m` [2]；`prompt_cache_breakpoint.mode=explicit`，不按 token block 取整 [2] |
| Anthropic | 无 `cache_control` 则 nothing is cached [8]。⚔ §5 | 顶层或内容块。`type`=`ephemeral`；`ttl`=`5m`\|`1h`；最多 4 断点；可标 tools、system [5][6] |
| Gemini 隐式 | 2.5+ 默认开，“nothing you need to do” [9] | 无缓存字段。有状态可传 `previous_interaction_id` [9] |
| Gemini 显式 | 先缓存再引用。Beta [10] | `POST https://generativelanguage.googleapis.com/v1beta/cachedContents` [10]；`cachedContent`=`cachedContents/{id}` [25] |
| DeepSeek | 默认开启，无需改代码；每个请求都构建硬盘缓存 [13] | 无缓存开关。`user_id` 隔离 KVCache [15]。`https://api.deepseek.com` [19] `POST /chat/completions` [15] |
| OpenRouter | 上游 prompt cache 与网关 response cache 分开，可同时用 [17] | 断点转成上游格式；Bedrock 上顶层字段变成 trailing breakpoint [24]。粘性：`session_id` 优先于 `x-session-id`，否则 `prompt_cache_key` [16]。响应缓存默认关：`X-OpenRouter-Cache` [17] |
| Kimi / 智谱 / 通义 | ❓ | ❓ |

### 门槛、失效、寿命

| 实体 | D3 最小与放置 | D4 失效 | D5 寿命 / 存储 |
|---|---|---|---|
| OpenAI | 5.6+ ≥1,024；更早随请求变 [1]。含 instructions、developer、tools、text/images/documents/supported audio [1] | 整段前缀须一致；断点前一变，其后不能命中 [1]。换 `prompt_cache_key` 可显示 miss，且可以不是物理 miss [4] | 5.6+：write/reuse 后 ≥30 分钟，可能更久 [1]。in_memory 闲置约 5–10 分钟、至多约 1 小时；24h 档通常约 30 分钟、至多 24 小时 [1]。ZDR 默认 in_memory [2]。⚔ §5 |
| Anthropic | 512：Fable 5.1/Mythos 5.1/Opus 5.5/Opus 5/Fable 5/Mythos 5。2048：Mythos Preview/Opus 4.7。4096：Opus 4.6/4.5/Haiku 4.5。1024：Opus 4.8/Sonnet 5/4.6/4.5 [5]。顺序 tools→system→messages，每断点≤20 [5] | 断点及之前任一块变化则哈希变 [5]。改 tool name / description / parameters，整个 cache 失效 [5] | 默认 5 分钟，从写入或读取请求的开始计 [5]。1 小时为加价档 [5]。价目只列写入与读取，无存储单价 [7] |
| Gemini 隐式 | 稳定内容放提示开头 [9]。最低 token 表的数字不在摘录 §5 | ❓ | ❓ |
| Gemini 显式 | 是提示前缀 [10]。tools 创建后 Immutable [11]。最低 token 只写 varies by model | 只能改 `ttl` 或 `expire_time` [10]。只能用于创建时的模型 [11] | 默认 1 小时 [10]。存储按 TTL×缓存 token [10] |
| DeepSeek | 须完整匹配前缀单元；输入结束与输出结束各一个 [13]。⚔ 新闻写 64 token 一块 [18] | `A+C` 对不上 `A+B` 即 miss [13]。只匹配输入前缀；输出仍受 temperature 影响 [13]。不保证 100% [13] | 不用后清空，一般几小时到几天 [13]。新闻写存储不收费 [18]。现行价目只有 token×单价 [14] |
| OpenRouter | 短于下限不缓存；模型数字不在摘录 [16]。Gemini 显式只用最后一个断点 [16] | 粘性闲置 10 分钟过期 [16] | Anthropic 路径默认 5 分钟，可到 1 小时 [16]。Gemini 同页矛盾 §5 |

### 计费与命中字段

| 实体 | D6 写 / 读 | D7 确认命中 | D8 覆盖 |
|---|---|---|---|
| OpenAI | 5.6+ 写 1.25× 未缓存 input，读 “0.1× that rate”。写不是叠加费，token 走未缓存 / 缓存读 / 缓存写三择一 [1]。更早模型读倍率 ❓ | Responses：`usage.input_tokens_details.cached_tokens`，另有 `cache_write_tokens` [2]。Chat：`usage.prompt_tokens_details.cached_tokens` [3] | `/responses` 与 `/chat/completions`。extended retention 含 gpt-5.5、gpt-5.5-pro、gpt-5.4、gpt-5.2、gpt-5.1 系列、gpt-5、gpt-4.1 等 [1] |
| Anthropic | 5 分钟写 1.25×，1 小时写 2×，读 0.1× [5]。Fable 5.1、Mythos 5.1 的 hit/refresh 0.025×；Opus 5.5 为 0.05× [5] | `cache_creation_input_tokens` 与 `cache_read_input_tokens` 都为 0 则没缓存 [5]。1 小时写入：`ephemeral_1h_input_tokens` [6] | 全部 active 模型，automatic 与 explicit 都支持 [5]。`POST https://api.anthropic.com/v1/messages` [5] |
| Gemini 隐式 | 命中才转节省；相对 input 倍率 ❓ [9] | Interactions：`usage.total_cached_tokens` [9]。generateContent 只写 `usage_metadata` [10]。⚔ | 2.5+。Interactions 只有隐式 [9] |
| Gemini 显式 | 后续降价并收存储 [10]。价目未标机制：2.5 Pro 缓存 $0.125（≤200k）/$0.25（>200k），存储 $4.50/1M tokens/hour；3.8 Flash 付费缓存 $0.075 至 2026-12-31，其后 $0.15 [12] | 摘录 “tokens in the cached part of the prompt”；笔记称 `usageMetadata.cachedContentTokenCount` [25] | `post …/v1beta/{model=models/*}:generateContent` [25]。模型全表 ❓ |
| DeepSeek | 闲=高峰×1/2。高峰：北京时间工作日 9–12、14–18。人民币/百万，闲/峰：Flash 命中 0.02/0.04、未命中 1/2；Pro 命中 0.15/0.30、未命中 4.5/9.0 [14]。美元同比例：Flash 0.003/0.006 对 0.15/0.3，Pro 0.022/0.044 对 0.66/1.32 [19] | Chat：`prompt_cache_hit_tokens`；`cached_tokens` 与之相同；`prompt_tokens`=hit+miss [15]。Responses 笔记称 `input_tokens_details.cached_tokens` [20] | `deepseek-flash` 或 `deepseek-v4-pro` [15]。`deepseek-chat`/`deepseek-reasoner` 于 2026-07-24 停用 [21]。此后 Pro 是否改道 ⚔ §5 |
| OpenRouter | 摘录：写可按原 input 的 1.25×，含自动缓存；Google 读倍率 `'0.25'` [16]。其余倍率摘录未含 §5。响应缓存命中免费 [17] | `cached_tokens`>0 即吃到缓存 [16]。`cache_write_tokens` 仅显式且有写入定价时返回 [24]。响应缓存：`X-OpenRouter-Cache-Status: HIT` [17] | 多数上游自动；Alibaba 与 Anthropic 要按消息打开 [16] |

## 3. 变体与适配层

相对直连，OpenRouter 会把断点改写成上游格式（Bedrock 上变成 trailing breakpoint）[24]，并用 `session_id` 或 `prompt_cache_key` 钉住同一 endpoint，闲置 10 分钟过期 [16]。`X-OpenRouter-Cache` 是另一个开关，默认关，命中免费 [17]。Azure / Bedrock / Vertex 本轮不写。

## 4. 用户需要知道的坑

1. 前缀里改一个字就会 miss（D4）。容易忽略的是：Anthropic 改 tool 的 name/description/parameters 会使整个 cache 失效 [5]；DeepSeek 从中间开始的重复不算命中 [18]。
2. 总 token 看不出命中。DeepSeek `prompt_tokens` 含 hit+miss [15]。Anthropic 两个缓存字段都为 0 才是没缓存 [5]。OpenAI 换 `prompt_cache_key` 可以显示 miss，却不是物理 miss [4]。
3. DeepSeek 不保证 100%，示例前两次请求不命中 [13]。Anthropic 5 分钟从请求开始计 [5]。Gemini 显式不能改内容或换模型 [10][11]。

## 5. 未决与置信度

- OpenAI ⚔：`ttl` 只支持 `30m` [1][2]，同参考又写 gpt-5.5 / 5.5-pro / future 的 `prompt_cache_retention` 只支持 `24h`，your-data 写支持模型都用 extended caching [22]。读价 “0.1× that rate” 基数未拆开 [1]。更早模型单价、temperature/top_p 是否入键：❓。页无 Updated。5.6+ 只隐式时，不同后缀不能复用更短公共前缀 [1]；默认会放一个 implicit breakpoint [2]。复核前不作为「必须改请求」或「能留 24 小时」。
- Anthropic ⚔：没有 `cache_control` 则 nothing is cached [8]；thinking 小节与之冲突，笔记没有 thinking 原句主张。同页 “5 minutes of inactivity” 与「从请求开始计」并存 [5]。header `prompt-caching-2024-07-31` 是否仍拒绝 ❓；已确定不再要求 beta prefix [5]。
- Gemini 隐式 D4、D5、读倍率 ❓。账单项 Cached token storage duration 没写只对显式 [23]。$0.125 与 $4.50 未标机制，不当作隐式价 [12]。命中字段：Interactions 为 `usage.total_cached_tokens` [9]；generateContent 隐式只写 `usage_metadata` [10]。最低 token 表的数字不在摘录里。
- DeepSeek ⚔：新闻「64 token 一块、从第 0 个 token」[18]；现行指南写 Sliding Window Attention 之后须完整匹配前缀单元，未给间隔数 [13]。新闻 $0.014 同页已写价格更新，正文用现行价目 [18]。v4-pro：2026-09-10 新闻写改道 V4.1-Flash 并按 Flash 价 [26]；updates 写 9 月 14 日后 Pro 计费不变 [21]。
- OpenRouter 同页把 Gemini 隐式写成不必 `cache_control`、无存储费，又写成必须插断点且写入含 5 分钟存储 [16]。笔记里的 OpenAI 0.25×/0.50×、DeepSeek 0.1×、响应缓存 300 秒、按 API key 隔离，摘录未含，正文不采用。
- Kimi、智谱、通义整行 ❓。Azure、Bedrock、火山方舟、MiniMax 只在线索里。

## 来源

[1] OpenAI Prompt caching — https://developers.openai.com/api/docs/guides/prompt-caching
[2] OpenAI Responses create — https://developers.openai.com/api/reference/resources/responses/methods/create
[3] OpenAI Chat — https://developers.openai.com/api/reference/resources/chat
[4] OpenAI cache diagnostics — https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics
[5] Anthropic Prompt caching — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[6] Anthropic Messages — https://platform.claude.com/docs/en/api/messages
[7] Anthropic Pricing — https://platform.claude.com/docs/en/about-claude/pricing
[8] Anthropic mid-conversation — https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages
[9] Gemini Caching — https://ai.google.dev/gemini-api/docs/caching
[10] Gemini explicit caching — https://ai.google.dev/gemini-api/docs/generate-content/caching
[11] Gemini cachedContents — https://ai.google.dev/api/caching
[12] Gemini pricing — https://ai.google.dev/gemini-api/docs/pricing
[13] DeepSeek 硬盘缓存 — https://api-docs.deepseek.com/zh-cn/guides/kv_cache
[14] DeepSeek 价格 — https://api-docs.deepseek.com/zh-cn/quick_start/pricing
[15] DeepSeek Chat — https://api-docs.deepseek.com/zh-cn/api/create-chat-completion
[16] OpenRouter Prompt caching — https://openrouter.ai/docs/guides/best-practices/prompt-caching
[17] OpenRouter Response caching — https://openrouter.ai/docs/guides/features/response-caching
[18] DeepSeek 新闻 2024-08-02 — https://api-docs.deepseek.com/zh-cn/news/news0802
[19] DeepSeek Pricing EN — https://api-docs.deepseek.com/quick_start/pricing
[20] DeepSeek Responses — https://api-docs.deepseek.com/api/create-response
[21] DeepSeek Updates — https://api-docs.deepseek.com/updates/
[22] OpenAI Your data — https://developers.openai.com/api/docs/guides/your-data
[23] Gemini Billing — https://ai.google.dev/gemini-api/docs/billing
[24] OpenRouter Chat API — https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request
[25] Gemini generateContent — https://ai.google.dev/api/generate-content
[26] DeepSeek 新闻 2026-09-10 — https://api-docs.deepseek.com/news/news260910
