# 四家大模型 API 的 prompt caching

> 不改代码会不会缓存、命中后怎么付钱、能活多久、看哪个字段、改什么会失效。截至 2026-09-24 的官方页。Kimi、智谱、通义、OpenRouter 本轮不进矩阵。

## 0. 一屏看懂

OpenAI 支持的模型默认开启 prompt caching。DeepSeek 的标题是「上下文硬盘缓存」，并写默认开启、无需修改代码。Gemini implicit 写明不用做任何事。

Anthropic 在 2026-02-19 起可以只在请求顶层放一个 `cache_control`，断点落到最后一块并随请求移动。另一页写：没有 `cache_control` 字段（自动或显式断点）就不缓存。thinking 小节又写 even without explicit cache_control markers。两句未裁完，这里不下「必须传 / 可以完全不传」。

付钱分三套。gpt-5.6+：写入 1.25×，其后读取 0.1×；更早模型无额外写费。Anthropic：5 分钟写 1.25×，1 小时写 2×；读取一般为 base 的 10%，Fable 5.1 与 Mythos 5.1 为 2.5%，Opus 5.5 为 5%。DeepSeek 现行价目只有命中价和未命中价。

寿命：Anthropic 默认 5 分钟（可改 1 小时），只在内存。OpenAI gpt-5.6+ 的 `ttl` 只有 `30m`，同站还有 `in_memory` 与 `24h`，和参考页冲突，见 §5。Gemini explicit 的 `ttl` 默认 1 小时，页上写无上下限，存储按 TTL 计。DeepSeek 写几个小时到几天，在硬盘上。命中只看当次 usage（§2）。

## 1. Taxonomy

轴 A 是控制点：默认就缓存（OpenAI 支持模型、Gemini implicit、DeepSeek）；请求里要有缓存字段（Anthropic 的 `cache_control`）；先创建资源（Gemini explicit：`POST https://generativelanguage.googleapis.com/v1beta/cachedContents`，再用 `cachedContent` = `cachedContents/{id}`）。

轴 B 是钱：写溢价加读折扣（OpenAI gpt-5.6+、Anthropic）；只分命中/未命中（DeepSeek，以及无额外写费的更早 OpenAI）；读折扣加按 TTL 存储（Gemini explicit）；implicit 是否承诺折扣未裁（一页写 no cost saving guarantee，另一页写命中就返利，§5）。

轴 C 是介质：OpenAI 是单机上的前缀 KV，不跨组织、不跨区域；Anthropic 写 held in memory only；DeepSeek 是硬盘，命中前要落盘；Gemini explicit 是带 `ttl` 的命名对象。

| 家族 | 谁 | 差别 |
|---|---|---|
| 默认前缀，命中/未命中分价 | DeepSeek；OpenAI 更早模型 | 请求可以不提缓存 |
| 写溢价 + 短 TTL 读折扣 | OpenAI gpt-5.6+；Anthropic | 第一次更贵，紧接着复用更便宜 |
| 隐式前缀，折扣承诺未裁 | Gemini implicit | 零改动；两页对是否省钱不一致，见 §5 |
| 命名资源 + 存储时长 | Gemini explicit | 先创建再引用 |

OpenAI 同页还有「没放显式断点则本请求不缓存」。和「默认开启」是否分属两种 mode，摘录没绑小节名，所以它跨着前两行，见 §5。

## 2. 对照矩阵

### 触发、单位、门槛

| 实体 | D1 | D2 | D3 |
|---|---|---|---|
| OpenAI | 默认开 [1]。gpt-5.6+ Responses 默认一个隐式断点 [2]。没放显式断点则不缓存也不写 [1] | 前缀 KV，不是原文 [1]。gpt-5.6+ 断点不按 token block 取整 [2] | gpt-5.6+ 最少 1024；隐藏系统 token 不计；更早模型随请求变 [1] |
| Anthropic | 顶层一个 `cache_control`，断点在最后一块并移动 [6]；2026-02-19 [8]。无该字段则不缓存 [7]，与 [6] 冲突 | `tools`→`system`→`messages`，含断点块；20-block lookback [6] | 短于门槛也不缓存 [6]。512：Fable 5.1、Mythos 5.1、Opus 5.5、Opus 5、Fable 5、Mythos 5。1024：Opus 4.8、Sonnet 5、Sonnet 4.6、Sonnet 4.5、Opus 4.1。2048：Mythos Preview、Opus 4.7 [6] |
| Gemini implicit | 2.5 及更新默认开 [10] | 短时间相似前缀 [10] | 2.5 Flash/Pro 2048；3.8/3.7/3.6/3.5 Flash 与 3.1 Pro Preview 4096 [10] |
| Gemini explicit | 手动创建，页上写有 cost saving guarantee [10] | prompt 前缀 [10] | ❓ 只说因模型而异 |
| DeepSeek | 默认开，无需改代码；每个请求都建硬盘缓存 [16] | 须完整匹配已落盘的前缀单元 [16][17] | ⚔ 现行无数字 [16]。2024-08-02 仍写 64 token [20] |

### 字段与价格

| 实体 | D4 命中字段 | D5 读 | D6 写与存储 |
|---|---|---|---|
| OpenAI | Responses：`input_tokens_details.cached_tokens`、`cache_write_tokens` [2]。Chat：`cache_write_tokens` 为未调整 prompt token [3] | gpt-5.6+ 为 0.1× [1]。更早为 model-dependent；gpt-5.5-pro 定价格为 `-` [5]，⚔ | 5.6+ 写 1.25×；更早无额外写费 [1] |
| Anthropic | 两字段都为 0 即没缓存：`cache_read_input_tokens`、`cache_creation_input_tokens`。`input_tokens` 在最后断点之后 [6] | 10%；Fable/Mythos 5.1 为 2.5%；Opus 5.5 为 5% [6] | 5 分钟 1.25×，1 小时 2×；只在内存 [6] |
| Gemini | ⚔ `usage_metadata` [10]、`usage.total_cached_tokens` [11]、`cached_content_token_count` [15]、`cachedContentTokenCount` [13] | implicit 不承诺 [10]；博客写 75% [15]。explicit 为 reduced rate [10]。价目不拆机制 [14] | explicit 按 TTL 收存储 [10]。implicit 写价/存储 ❓ |
| DeepSeek | `prompt_cache_hit_tokens` 与 `prompt_cache_miss_tokens`；`cached_tokens` 等于 hit [16][21]。Responses：`input_tokens_details.cached_tokens` [22] | 命中/百万，空闲·高峰：flash $0.003·$0.006，pro $0.022·$0.044 [18]；中文 0.02·0.04 元与 0.15·0.30 元 [19] | 未命中：flash $0.15·$0.30，pro $0.66·$1.32 [18]；中文 1·2 元与 4.5·9.0 元 [19]。无 write/存储行 |

DeepSeek 高峰：北京时间工作日 9:00–12:00、14:00–18:00（不含法定节假日），空闲为一半；模型列 deepseek-flash、deepseek-v4-pro [19]。Gemini 价目不标机制：2.5 Flash 文本输入 $0.30、缓存 $0.03、存储 $1 / 1,000,000 tokens / hour；2.5 Pro ≤200k 缓存读 $0.125；3.1 Pro Preview 同档 $0.20；3.8 Flash 付费读 $0.075 至 2026-12-31 [14]。

### 寿命、失效、端点、隔离

| 实体 | D7 TTL | D8 失效 | D9 / D10 |
|---|---|---|---|
| OpenAI | `ttl` 只有 `30m` [1]。`in_memory` 闲置约 5–10 分钟至 1 小时；`24h` 通常约 30 分钟、最长 24 小时 [1]。与 [2][4] 冲突，见 §5。不能手清 [1] | 断点前一变，其后前缀不能命中 [1]。细则见 §4 | 更早模型只有隐式；Agents 同 Responses [1]。Chat 选项只有 `mode`、`ttl` [3]；Responses 另有 `prewarm`、`comparison_response_id` [2]。不跨组织/区域；高于 15 RPM 溢出；5.6+ 的 `prompt_cache_key` 不优化路由 [1] |
| Anthropic | 默认 5 分钟，可 1 小时 [6]。2025-08-13 起 1 小时不要 beta header [8]。从请求开始算 [6]。刷新句见 §5 | 改一层，该层及之后失效；须 100% 相同 [6]。细则见 §4 | 所有 active 模型；不再要 beta 前缀；Batches 为 best-effort [6]。没开缓存则无 server-tool 自动断点 [9]。并发等第一条响应开始 [6]。API / AWS Claude Platform / Foundry 按 workspace；Bedrock 与 Google Cloud 按组织 [6] |
| Gemini implicit | ❓ | ❓ | Interactions 只有 implicit [11]。隔离 ❓ |
| Gemini explicit | 默认 1 小时；`ttl` 与 `expireTime` 互斥；无上下限 [10][12] | 到期删除 [10]。只能用于创建它的 model [12] | 端点在 v1beta [12]。隔离 ❓ |
| DeepSeek | 几小时到几天 [16][17] | 尽力而为；例二前两次不命中 [16] | BASE `https://api.deepseek.com` [18]。`cache_control` Ignored [24]。不支持 `prompt_cache_key` / `prompt_cache_retention` [23]。`user_id` 隔离业务用户 KV，不是开关 [27]；不传是否共享：没写 |

## 3. 变体与适配层

Chat 与 Responses 的差别在 `prompt_cache_options` 的字段，不在默认开关 [2][3]。`prompt_cache_retention=in_memory` 对 gpt-5.5 与 gpt-5.5-pro 报错 [4]。Anthropic 顶层自动断点与块上显式断点共用 lookback 和写价档 [6]。Gemini Interactions 不能建 cache 对象 [11]。DeepSeek 忽略 `cache_control`，Responses 也不吃 OpenAI 的两个缓存参数 [24][23]。

通义官方写隐式与显式互斥，网格已拆两行，数字下一轮再写入。Vertex 另有 context cache 文档，未打开。

## 4. 用户需要知道的坑

前缀放在会变的内容前面。OpenAI 是断点前的内容或设置 [1]。Anthropic 的顺序锁死为 `tools`→`system`→`messages` [6]。DeepSeek 要完整匹配已经落盘的前缀单元，不是任意重叠 [16][17]。

工具和多模态算进前缀。OpenAI：tool 的名字、描述、schema、顺序，以及图片、文档、受支持音频 [1]。Anthropic：改 `tool_choice`，或任意位置增减图片，会失效；`tool_use` 的 JSON 键序不稳（文档举 Swift、Go）也会对不上 [6]。

写入不是马上全局可见。Anthropic 两个计数都是 0 即没缓存，并发要等第一条响应开始 [6]。DeepSeek 例二的前两次不命中 [16]。OpenAI 不能手清，同一前缀高于 15 次/分钟会溢到别的机器 [1]。

隔离键会拆开相同文本：OpenAI 的组织与区域 [1]，Claude API 的 workspace [6]，DeepSeek 的 `user_id` [27]。gpt-5.6+ 不要再靠 `prompt_cache_key` 去贴机器 [1]。Gemini implicit 可以有命中计数，同时不保证省钱 [10]；explicit 换模型就不能用 [12]。诊断 miss 时，Anthropic 还列举没带 header、跨 workspace、隔太久 [25]（示例 header `cache-diagnosis-2026-04-07`）。多数 Claude 模型只有未缓存输入计入 ITPM [26]。

## 5. 未决与置信度

- Anthropic D1：[7] 无 `cache_control` 字段就不缓存；[6] thinking 写 without explicit markers。未裁 markers 是否只指块级标记。
- OpenAI D1：默认开启与「无显式断点则不写缓存」同在 [1]，摘录无模式名。
- OpenAI D7：`ttl=30m` [1]；[2] 写 gpt-5.5、gpt-5.5-pro 与 future models 的 retention 只支持 `24h`；[4] 写所有查询都用 extended prompt caching，指南写未开 ZDR 的组织默认 `24h`。复用再收写费只有线索。
- Anthropic 刷新原文 no additional cost，列名却是 Cache hits and refreshes [6]。
- Gemini 折扣三处不一致 [10][11][15]。$0.30 与 $0.03 是 10%，页上没有统一比例。付费功能 vs 2.5 Flash 免费档 Not available vs 3.8 Flash 首块 Free of charge [10][14]。implicit 的 TTL、失效、写价，explicit 的分模型最低 token：无原句。博客 2.5 Flash 门槛 1024，现行表 2048，表用现行 [15][10]。
- DeepSeek 的 64 token 与 storage is free 只在 2024 公告 [20]。现行指南只说 Sliding Window Attention 之后单元变了。中英文价不换算。
- Kimi、智谱、通义隐式、通义显式、OpenRouter 仍是 ❓。主文档：`https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api`、`https://docs.bigmodel.cn/cn/guide/capabilities/cache`、`https://help.aliyun.com/zh/model-studio/context-cache`、`https://openrouter.ai/docs/guides/best-practices/prompt-caching`。OpenRouter 写 Moonshot 写入免费，Kimi 页写默认 5 分钟写入要计费，下一轮对照后再写进正文。

## 来源

[1] https://developers.openai.com/api/docs/guides/prompt-caching.md
[2] https://developers.openai.com/api/reference/resources/responses/methods/create.md
[3] https://developers.openai.com/api/reference/resources/chat.md
[4] https://developers.openai.com/api/docs/guides/your-data.md
[5] https://developers.openai.com/api/docs/pricing.md
[6] https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[7] https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages
[8] https://platform.claude.com/docs/en/release-notes/overview
[9] https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching
[10] https://ai.google.dev/gemini-api/docs/generate-content/caching
[11] https://ai.google.dev/gemini-api/docs/caching
[12] https://ai.google.dev/api/caching
[13] https://ai.google.dev/api/generate-content
[14] https://ai.google.dev/gemini-api/docs/pricing
[15] https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/
[16] https://api-docs.deepseek.com/zh-cn/guides/kv_cache
[17] https://api-docs.deepseek.com/guides/kv_cache
[18] https://api-docs.deepseek.com/quick_start/pricing
[19] https://api-docs.deepseek.com/zh-cn/quick_start/pricing
[20] https://api-docs.deepseek.com/news/news0802
[21] https://api-docs.deepseek.com/api/create-chat-completion/
[22] https://api-docs.deepseek.com/api/create-response/
[23] https://api-docs.deepseek.com/guides/responses_api
[24] https://api-docs.deepseek.com/guides/anthropic_api
[25] https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics
[26] https://platform.claude.com/docs/en/api/rate-limits
[27] https://api-docs.deepseek.com/zh-cn/quick_start/rate_limit
