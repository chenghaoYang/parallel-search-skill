# 各家 Prompt Caching 怎么不一样

> 截至 2026-09-24。回答六件事：要不要改请求、字段原名、命中怎么计费、能活多久、响应里看哪个字段、什么改动会 miss。先读第 0 节，再按家族查表。Kimi、智谱、通义本轮还没有专职工人笔记。

## 0. 一屏看懂

1. DeepSeek 仍是自动硬盘缓存：默认开启，不用改代码，每个请求都会构建缓存。Chat 用 `prompt_cache_hit_tokens` 看命中。Flash 命中价是未命中的 1/50，V4 Pro 是 1/30（人民币价目）。不用后一般留几小时到几天。[13][14][15]
2. OpenAI 支持的模型仍默认开启，不必为了「打开缓存」而加字段。[1]
3. Anthropic 仍要在请求里放 `cache_control`：mid-conversation 页写，完全没有该字段就 nothing is cached。不必再逐块手打——顶层一个字段，断点会自动落在最后一个可缓存块并随对话前移。`type` 只有 `ephemeral`，beta 前缀已不需要。thinking 路径是否例外见第 5 节。[5][8]
4. 写/读倍率能对上原句的：Anthropic 5 分钟写入 1.25×、1 小时写入 2×、读取 0.1× base input（Fable 5.1 与 Mythos 5.1 为 0.025×，Opus 5.5 为 0.05×）。OpenAI GPT-5.6+ 写入为未缓存 input 的 1.25×，读取写成 “0.1× that rate”；that 指未缓存价还是写入价，原句没拆开，见第 5 节。[1][5]
5. Gemini 是两套，没有合并声明。隐式：2.5 及更新默认开，不用做任何事，命中才把节省转给调用方，不保证省钱。显式：先 `POST /v1beta/cachedContents`，再在生成请求里引用；默认 TTL 1 小时，存储按 TTL 计。[9][10]
6. OpenRouter 的 prompt 前缀在上游机房，不在网关。网关会把断点标记转成上游格式，并用 `session_id` / `prompt_cache_key` 做粘性路由。另有默认关闭的整响应缓存，命中免费，看 `X-OpenRouter-Cache-Status`，不是 `cached_tokens`。[16][17]
7. 失效的共同形状：要复用的内容必须是从开头连续匹配的前缀。中间相同、或在前缀里插入时间戳，对不上整段哈希。[1][5][13]
8. Kimi、智谱、通义：整行未查，没有结论。

## 1. Taxonomy

分类轴：**不传任何缓存字段时，会不会产生 cache read？** 这一个问题分开了「不用改代码」和「必须声明」。

| 家族 | 为什么是一类 | 现在的成员 |
|---|---|---|
| F1 自动前缀 | 不传字段也会读缓存；边界由服务端放在前缀上 | OpenAI 默认路径、DeepSeek、Gemini 隐式 |
| F2 请求内声明 | 零字段则不缓存；声明可以只放顶层，断点由服务端前移 | Anthropic |
| F3 缓存对象 | 缓存是先创建的资源，生成请求只引用名字 | Gemini 显式 `cachedContents` |
| F4 网关 | 前缀缓存在上游；网关另做粘性和整响应缓存 | OpenRouter |

OpenAI GPT-5.6+ 另有可选显式断点，默认仍是 F1。Anthropic 文档里的 automatic 仍要顶层 `cache_control`，所以不是 F1。

后面的表按同一组问题排：D1 不传字段会不会读缓存；D2 字段原名；D3 最小长度和放哪；D4 什么改动 miss；D5 活多久、有没有存储费；D6 读写相对 input 的倍率；D7 响应字段；D8 哪些模型、哪条 URL。

## 2. 对照矩阵

### 开关与字段

| 实体 | D1 零字段会不会读 | D2 请求里写什么 |
|---|---|---|
| OpenAI | 默认开启 [1]。只有 `mode=explicit` 且没有任何 explicit breakpoint 时，该请求不使用 prompt caching [2] | 可选 `prompt_cache_key`（取代 `user`）[3]；`prompt_cache_retention`：`in_memory` 或 `24h` [2]；`prompt_cache_options.ttl` 默认且目前只支持 `30m` [2]；`prompt_cache_breakpoint.mode=explicit` 标前缀终点，不按 token block 取整 [2] |
| Anthropic | 无 `cache_control` 则 nothing is cached [8]。⚔ 见 §5 | 顶层一个，或打在内容块上。`type`=`ephemeral`；`ttl`=`5m` 或 `1h`；最多 4 个断点；可标 tools 与 system [5][6] |
| Gemini 隐式 | 2.5+ 默认开，“nothing you need to do” [9] | 无缓存字段。有状态对话可传 `previous_interaction_id` [9] |
| Gemini 显式 | 先缓存再引用 [10]。Beta [10] | `POST https://generativelanguage.googleapis.com/v1beta/cachedContents` [10]；生成请求字段 `cachedContent`，形如 `cachedContents/{id}` [25] |
| DeepSeek | 默认开启，无需改代码；每个请求都构建硬盘缓存 [13] | 无缓存开关。`user_id` 做 KVCache 隔离 [15]。`https://api.deepseek.com` [19]，`POST /chat/completions` [15] |
| OpenRouter | 上游 prompt cache 与网关 response cache 分开，可同时用 [17] | 断点标记转成上游原生格式；Bedrock 上顶层字段会变成 trailing breakpoint [24]。粘性键：`session_id` 优先于 `x-session-id`，否则用 `prompt_cache_key` [16]。响应缓存默认关，header `X-OpenRouter-Cache` [17] |
| Kimi / 智谱 / 通义 | ❓ | ❓ |

### 门槛、失效、寿命

| 实体 | D3 | D4 | D5 |
|---|---|---|---|
| OpenAI | GPT-5.6+ 最小 1,024 token；更早模型随请求变 [1]。缓存整段渲染结果：instructions、developer、tools、历史里的 text / images / documents / supported audio [1] | 须整段前缀匹配；断点前内容或相关设置一变，其后不能命中旧条目 [1]。换 `prompt_cache_key` 可以在 usage 里记成 miss，且可以不是物理 miss [4] | GPT-5.6+：最近一次 write 或 reuse 后至少 30 分钟，可能更久 [1]。`in_memory`：不活跃约 5–10 分钟，最长约 1 小时 [1]。`24h` 策略通常约 30 分钟、最长 24 小时 [1]。ZDR 且未指定 retention 时默认 `in_memory` [2]。⚔ 见 §5 |
| Anthropic | 最小：512（Fable 5.1、Mythos 5.1、Opus 5.5、Opus 5、Fable 5、Mythos 5）；2,048（Mythos Preview、Opus 4.7）；4,096（Opus 4.6、Opus 4.5、Haiku 4.5）；1,024（Opus 4.8、Sonnet 5、Sonnet 4.6、Sonnet 4.5）[5]。顺序 `tools` → `system` → `messages`。每个断点最多查 20 个位置 [5] | 断点及之前任一块变化，哈希就变 [5]。改 tool 的 name / description / parameters，整个 cache 失效 [5] | 默认 5 分钟，从写入或读取的请求开始计，不是从响应结束 [5]。另有 1 小时，加价 [5]。存储单价 ∅（价目只写首次写入与后续读取）[7] |
| Gemini 隐式 | 门槛按模型列表；摘录没有单元格数字，见 §5。大而稳定的内容放在提示开头 [9] | ❓ | ❓ |
| Gemini 显式 | 缓存内容是提示前缀 [10]。`tools` 创建后 Immutable [11]。最低 token 只写 “varies by model” | 创建后只能改 `ttl` 或 `expire_time` [10]。只能用于创建时的那个模型 [11] | 未设 TTL 则默认 1 小时 [10]。存储按 TTL 时长 × 缓存 token 计 [10] |
| DeepSeek | 现行：须完整匹配缓存前缀单元；输入结束与输出结束各产生一个单元 [13]。⚔ 2024-08-02 新闻仍写 64 token 一块、不足不缓存 [18] | `A+C` 对不上 `A+B` 的前缀单元就不命中 [13]。缓存只匹配输入前缀；输出仍受 temperature 影响 [13]。尽力而为，不保证 100% [13] | 不用后自动清空，一般为几小时到几天 [13]。新闻写「缓存占用存储无需付费」[18]。现行价目只有 token×单价 [14]。⚔ |
| OpenRouter | 短于上游下限的 prompt 不会被缓存；摘录未含各模型数字 [16]。Gemini 显式只用最后一个断点 [16] | 粘性会话闲置 10 分钟过期 [16] | 随上游。Anthropic 路径：默认 5 分钟，可延到 1 小时 [16]。同页 Gemini 隐式/显式互相矛盾，§5 |

### 计费与命中字段

| 实体 | D6 写 / 读 | D7 怎么确认 | D8 |
|---|---|---|---|
| OpenAI | GPT-5.6+：写 = 1.25× 未缓存 input；读 = “0.1× that rate”。写不是另加一笔，input token 走未缓存、缓存读、缓存写三选一 [1]。更早模型的读倍率 ❓ | Responses：`usage.input_tokens_details.cached_tokens`；同对象有 `cache_write_tokens` [2]。Chat：`usage.prompt_tokens_details.cached_tokens` [3] | `POST /responses` 与 `POST /chat/completions`。extended retention 名单含 `gpt-5.5`、`gpt-5.5-pro`、`gpt-5.4` 直至 `gpt-4.1` 等 [1] |
| Anthropic | 5 分钟写 1.25×，1 小时写 2×，读 0.1× [5]。Fable 5.1、Mythos 5.1 的 hit/refresh 为 0.025×；Opus 5.5 为 0.05× [5] | `cache_creation_input_tokens` 与 `cache_read_input_tokens` 都为 0 则没缓存 [5]。1 小时写入另见 `ephemeral_1h_input_tokens` [6] | 全部 active 模型，automatic 与 explicit 都支持 [5]。`POST https://api.anthropic.com/v1/messages` [5] |
| Gemini 隐式 | 命中才自动转节省；相对 input 的倍率 ❓ [9] | Interactions：`usage.total_cached_tokens` [9]。generateContent 只写 `usage_metadata`，未点名子字段 [10]。⚔ | 2.5 及更新。Interactions 只有隐式，显式对象不支持 [9] |
| Gemini 显式 | 后续按降低费率，另收存储 [10]。价目未标明属于哪一套：2.5 Pro 缓存 $0.125（≤200k）/ $0.25（>200k），存储 $4.50 / 1,000,000 tokens / hour [12]。3.8 Flash 付费缓存 $0.075 至 2026-12-31，其后 $0.15 [12] | `usageMetadata.cachedContentTokenCount`：摘录是 “tokens in the cached part of the prompt” [25] | `post …/v1beta/{model=models/*}:generateContent` [25]。完整模型枚举 ❓ |
| DeepSeek | 每百万 token，闲时为高峰一半。高峰：北京时间工作日 9:00–12:00、14:00–18:00。人民币：Flash 命中 0.02 / 0.04，未命中 1 / 2；V4 Pro 命中 0.15 / 0.30，未命中 4.5 / 9.0 [14]。美元：Flash 命中 0.003 / 0.006，未命中 0.15 / 0.3；Pro 命中 0.022 / 0.044，未命中 0.66 / 1.32 [19] | Chat：`prompt_tokens` = `prompt_cache_hit_tokens` + `prompt_cache_miss_tokens`；`cached_tokens` 与 hit 相同 [15]。Responses：`input_tokens_details.cached_tokens` [20] | `deepseek-flash` 或 `deepseek-v4-pro` [15]。`deepseek-chat` / `deepseek-reasoner` 文档写 2026-07-24 停用 [21]。v4-pro 此后是否改道 ⚔ §5 |
| OpenRouter | 页上能对上摘录的：写入可按原 input 的 1.25× 计，含自动缓存；Google 读倍率常量 `'0.25'` [16]。其余模型倍率在笔记主张里、不在摘录里，见 §5。响应缓存命中免费，用量为 0 [17] | `cached_tokens` > 0 表示吃到缓存内容 [16]。`cache_write_tokens` 只在有显式缓存且有写入定价时返回 [24]。响应缓存看 `X-OpenRouter-Cache-Status: HIT` [17] | 多数上游自动；Alibaba 与 Anthropic 要按消息打开 [16] |

## 3. 变体与适配层

OpenRouter 不是某一家的别名，差在四件事：

| 差在哪 | 行为 |
|---|---|
| 断点不是原样转发 | 转成上游原生格式；Bedrock 把顶层字段译成 trailing breakpoint [24] |
| 粘性不是缓存 | 后续请求钉到同一 provider endpoint；键用 `session_id`，否则退回 `prompt_cache_key` [16] |
| 粘性寿命 | 闲置 10 分钟过期 [16] |
| 第三种缓存 | `X-OpenRouter-Cache` 默认关，命中免费 [17]。默认 TTL、按 key 隔离、命中时 token 是否为 0，摘录未含，见 §5 |

同一协议换托管方（Azure、Bedrock、Vertex）本轮只留在线索里，不写进上表。

## 4. 用户需要知道的坑

1. 前缀里插了变化的内容 → 整段对不上 → 后面的稳定文档也 miss。OpenAI 要求断点前整段渲染前缀一致 [1]。Anthropic 改断点及之前任一块，或改 tool 定义，哈希就变 [5]。DeepSeek 要求完整匹配前缀单元，从中间开始的重复不算命中 [13][18]。Gemini 隐式建议把大而稳定的内容放在提示开头 [9]。
2. 用总 input 判断「省了没有」会看错。DeepSeek 的 `prompt_tokens` 已经包含 hit 和 miss [15]。Anthropic 要两个缓存字段都为 0，才是没缓存 [5]。OpenRouter 的整响应缓存用 `X-OpenRouter-Cache-Status`，命中免费 [17]。
3. OpenAI 的 `cached_tokens=0` 可能只是 `prompt_cache_key` 变了，文档写这可以不是物理 miss [4]。
4. DeepSeek 不保证 100% 命中 [13]。温度改变的是未缓存的输出，不是把前缀匹配关掉 [13]。示例写明前两次请求不会命中，第二次要复用第一次的整个前缀单元 [13]。
5. OpenRouter 的粘性闲置 10 分钟过期 [16]。不钉住同一上游端点时，上游内存里的前缀不会跟着走 [17]。
6. Gemini 显式缓存不能改内容，只能改过期时间；换模型不能复用 [10][11]。隐式不保证省钱 [9]。
7. Anthropic 的 5 分钟从请求开始算 [5]。多轮若间隔按「响应结束之后再等 5 分钟」估计，会提前过期。
8. DeepSeek 的 Responses API 不在服务端保存 responses 和 conversations [20]。缓存仍然只匹配输入前缀 [13]。

## 5. 未决与置信度

- OpenAI D5 ⚔。指南与参考：`prompt_cache_options.ttl` 只支持 `30m` [1][2]。同一参考又写 `gpt-5.5`、`gpt-5.5-pro` 与 future models 的 `prompt_cache_retention` 只支持 `24h`。your-data 写支持的模型都用 extended prompt caching [22]。复核前，不要按「加一个字段就留满 24 小时」去改 GPT-5.6 请求。
- OpenAI 读价的基数未拆开。原句是 writes cost 1.25× the standard uncached rate，reads cost 0.1× that rate [1]。更早模型的缓存单价 ❓。`temperature` / `top_p` 是否进入缓存键 ❓。上述页未见 Updated。
- 与「完全不用改代码」可能相反、复核前不当操作结论：GPT-5.6+ 若只做隐式缓存，共享长前缀但后缀不同时，第一次完整请求的缓存不会使更短的公共前缀变得可复用 [1]。参考写默认会自动放一个 implicit breakpoint [2]。
- Anthropic D1 ⚔。mid-conversation：没有 `cache_control`（automatic 或 explicit breakpoint）则 nothing is cached [8]。同站 prompt caching 的 thinking 小节与这句话冲突，笔记没有把 thinking 原句收成主张。5 分钟另有一处写 “minimum of 5 minutes of inactivity”，与「从请求开始计」同页并存 [5]。存储费没有单价。`prompt-caching-2024-07-31` 是否仍被 API 拒绝 ❓；能确定的是 “no longer requires the beta prefix” [5]。
- Gemini 隐式 D4、D5、读倍率 ❓。账单 FAQ 把 Cached token storage duration 列为计价项，没写只对显式 [23]；隐式页没有存储句。价目上的美元数未标注机制 [12]，所以上表不把 $0.125 / $4.50 算成隐式价格。隐式最低 token 工人称页上有表，摘录没有数字。命中字段 ⚔：Interactions 是 `usage.total_cached_tokens` [9]；generateContent 的隐式节只写 `usage_metadata` [10]；`cachedContentTokenCount` 没有写是否包含隐式 [11]。
- DeepSeek D3 ⚔：新闻「从第 0 个 token 起、64 token 一块」[18]；现行指南「受 Sliding Window Attention 影响，与以前不同，须完整匹配前缀单元」[13]，没给出间隔 token 数。正文计费采用现行价目；2024 新闻的 $0.014 同页已写价格更新 [18]。D8 ⚔：news 2026-09-10 写 v4-pro 改道 V4.1-Flash 并按 Flash 价，updates 写 9 月 14 日后 Pro 计费不变 [21]。
- OpenRouter 同一篇把 Gemini 隐式写成不必 `cache_control`、无存储费，又写成必须插 `cache_control` 且写入含 5 分钟存储 [16]。笔记里的 OpenAI 0.25×/0.50×、DeepSeek 0.1×、响应缓存默认 300 秒、按 API key 隔离，没有落在摘录里，正文不采用。
- Kimi、智谱、通义：D1–D8 全部 ❓。Azure、Bedrock、火山方舟、MiniMax 只在 scout 线索中，未核进正文。

## 来源

[1] OpenAI Prompt caching — https://developers.openai.com/api/docs/guides/prompt-caching
[2] OpenAI Responses create — https://developers.openai.com/api/reference/resources/responses/methods/create
[3] OpenAI Chat reference — https://developers.openai.com/api/reference/resources/chat
[4] OpenAI Prompt cache diagnostics — https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics
[5] Anthropic Prompt caching — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[6] Anthropic Messages API — https://platform.claude.com/docs/en/api/messages
[7] Anthropic Pricing — https://platform.claude.com/docs/en/about-claude/pricing
[8] Anthropic Mid-conversation system messages — https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages
[9] Gemini Caching — https://ai.google.dev/gemini-api/docs/caching
[10] Gemini Explicit caching — https://ai.google.dev/gemini-api/docs/generate-content/caching
[11] Gemini API cachedContents / generateContent — https://ai.google.dev/api/caching
[12] Gemini API pricing — https://ai.google.dev/gemini-api/docs/pricing
[13] DeepSeek 上下文硬盘缓存 — https://api-docs.deepseek.com/zh-cn/guides/kv_cache
[14] DeepSeek 价格（中文）— https://api-docs.deepseek.com/zh-cn/quick_start/pricing
[15] DeepSeek 创建对话补全 — https://api-docs.deepseek.com/zh-cn/api/create-chat-completion
[16] OpenRouter Prompt caching — https://openrouter.ai/docs/guides/best-practices/prompt-caching
[17] OpenRouter Response caching — https://openrouter.ai/docs/guides/features/response-caching
[18] DeepSeek 新闻 2024-08-02 — https://api-docs.deepseek.com/zh-cn/news/news0802
[19] DeepSeek Pricing (EN) — https://api-docs.deepseek.com/quick_start/pricing
[20] DeepSeek Create response — https://api-docs.deepseek.com/api/create-response
[21] DeepSeek Updates — https://api-docs.deepseek.com/updates/
[22] OpenAI Your data — https://developers.openai.com/api/docs/guides/your-data
[23] Gemini Billing — https://ai.google.dev/gemini-api/docs/billing
[24] OpenRouter Chat Completions — https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request
[25] Gemini generateContent — https://ai.google.dev/api/generate-content
