# 各家大模型 API 的上下文缓存

> 回答：要不要改请求、命中后怎么计费、能活多久、看哪个字段、什么改动会打穿。厂商页抓取日 2026-09-24；OpenAI 指南 Last-Modified 2026-09-23，Gemini 定价页 2026-09-23。价格是每 1M tokens。

## 0. 一屏看懂

1. OpenAI 和 DeepSeek 仍是默认缓存，请求可以不带缓存字段 [1][11]。Anthropic 要放 `cache_control` 才会缓存；完全不放时，server tools 也不会自动写缓存 [25]。2026-02-19 起这个字段可以只放在顶层，断点会挪到最后一个可缓存块；块上打点仍然有效 [4][6]。2025-08 那种「只能在块上打点」是旧文档 [24]。
2. 智谱是隐式缓存，不用配置 [18]。百炼的隐式缓存默认开而且不能关；显式缓存要在 content 里加 `cache_control`，两种互斥 [21]。Kimi 的 Chat/Responses 不传 `prompt_cache_options` 也会按 5 分钟档写入，并且计写入费 [14]。Kimi 的 Anthropic 兼容接口相反：不传顶层 `cache_control` 只读 5 分钟缓存，不写入、不收写入费 [16]。
3. OpenRouter 自己不存缓存。它把后续请求粘回同一个上游；`session_id` 或头 `x-session-id` 的粘性 10 分钟无请求就过期，这不是缓存 TTL [23]。`cache_control` 和 `prompt_cache_breakpoint` 会互译，TTL 丢掉不译 [23]。
4. 账单分三种，单价在第 2 节。只降低命中输入价：DeepSeek、OpenAI 旧模型、百炼隐式、智谱。写入加价、读取打折：Anthropic、OpenAI 5.6+、百炼显式、Kimi K3。按时间收存储费：Gemini 显式；智谱的存储栏是限时免费 [19]。
5. 寿命对不上：Anthropic 默认 5 分钟且命中续期；OpenAI 5.6+ 为 30 分钟，复用刷新且不再收写入费；Kimi 的 `5m`/`1h` 首次锁定；Gemini 显式默认 1 小时。DeepSeek、百炼隐式、智谱、Gemini 隐式没有固定小时数 [1][4][7][11][14][21]。
6. 确认命中要看 usage 里的缓存字段，不要只看 `input_tokens`。Anthropic 和 Kimi Messages 的 `input_tokens` 都不含缓存读写 [4][16]。字段名在第 2 节。
7. 从开头算的前缀变了就会 miss：模型、工具定义或顺序、断点前的文本和图片。百炼显式要等那一次响应结束，缓存才建好 [21]。DeepSeek 还要完整对上一个已经落盘的前缀单元，并且不保证命中 [11]。

## 1. Taxonomy

分类轴：边界由谁划定，缓存以什么形态存在。一家可以占两格。这一轴解释要不要改代码，以及有没有存储费。

| 家族 | 判据 | 成员 |
|---|---|---|
| I 隐式前缀 | 可以不带缓存字段，服务端自己匹配前缀 | OpenAI 默认、DeepSeek、Gemini implicit、智谱、百炼隐式、Kimi Chat 默认 |
| II 请求内标记 | 请求里要出现标记才按你的断点写缓存 | Anthropic 顶层或块级；百炼显式；Kimi 的 Messages 顶层；OpenAI 仅 5.6+ 可选 |
| III 独立资源 | 先创建带 TTL 的对象再引用，存储另计 | Gemini `CachedContent`。Kimi 2024 年的 `POST /v1/caching` 已不在现行接口里 |
| IV 网关 | 不定义缓存语义，只做路由和字段互译 | OpenRouter |

## 2. 对照矩阵

### 触发、门槛、寿命

| | 不改请求时 | 字段 | 门槛 | 寿命 |
|---|---|---|---|---|
| OpenAI | 会缓存 [1] | 5.6+：`ttl` 只接受 `"30m"`，可选 `prompt_cache_breakpoint`。更早：`prompt_cache_retention`=`in_memory`\|`24h`（Deprecated）[1][3] | 5.6+：1024。更早 varies [1] | 30 分钟；复用刷新且不再收写入费。`in_memory` 约 5–10 分钟不活跃；无 ZDR 默认 `24h` [1][3] |
| Anthropic | 要有 `cache_control` [4] | 顶层或块上 `{type:ephemeral,ttl:5m\|1h}`，最多 4 个 [4][5] | 512–4096，不够就跳过 [4] | 默认 5 分钟，命中免费续。1 小时档不用 beta header [4][6] |
| Gemini 隐式 | 2.5+ 默认开 [7] | 无 | 2048；列出的 3.x 为 4096 [7] | ∅ |
| Gemini 显式 | 先创建 [8] | `POST /v1beta/cachedContents`，字段 `cachedContent` [7] | 只写 varies | 默认 1 小时。PATCH 只改过期时间 [7][8] |
| DeepSeek | 会 [11] | 无开关。`user_id` 只隔离 | 见第 5 节 | 无字段。闲置数小时到数天，best-effort [11] |
| Kimi | Chat 不传也按 5m 写入计费。Messages 不传只读、不写 [14][16] | Chat 只接受 `prompt_cache_options.ttl`=`5m`\|`1h`。块级断点 400。Messages 只认顶层 `cache_control` [15][16] | ∅ | 两档独立，首次锁定，命中按原 TTL 续 [14] |
| 智谱 | 会 [18] | 无 | 建议 ≥500 [18] | 有时限，无数字 [20] |
| 百炼隐式 | 会，不能关 [21] | 无 | 1024；GLM/MiniMax 512 [21] | 不定，不保证命中 [21] |
| 百炼显式 | 不会 | `cache_control.type=ephemeral`，≤4，回看 20 块 [21] | 1024 | 5 分钟，命中重置。响应结束后才创建 [21] |
| OpenRouter | 随上游。点名 Anthropic 与阿里要自己打标记 [23] | `cache_control` ↔ `prompt_cache_breakpoint`，TTL 不译 [23] | 随上游 | 缓存 TTL 属上游。粘性路由 10 分钟 [23] |

### 计费与观测

| | 写入 | 命中 | 存储 | 字段 |
|---|---|---|---|---|
| OpenAI 5.6+ | 1.25×。gpt-5.6-sol：输入 $4、写 $5、cached $0.40 [1][2] | 0.1× [1] | 无 | `cached_tokens`、`cache_write_tokens`（Responses 在 `input_tokens_details`，Chat 在 `prompt_tokens_details`）[3] |
| OpenAI 更早 | 无，写入列为 `-` [2] | 按模型。gpt-5：$1.25→$0.125 [2] | 无 | 同上。缓存 token 仍计 TPM [1] |
| Anthropic | 5m 1.25×，1h 2× [4] | 多数 0.1×；Fable/Mythos 5.1 为 0.025×；Opus 5.5 为 0.05× [4] | 无 | `cache_read_input_tokens`、`cache_creation_input_tokens`。命中不计 rate limit [4] |
| Gemini 隐式 | 未写 | 不保证，无百分比 [7] | 未与显式拆开 | `cachedContentTokenCount`；Interactions 用 `total_cached_tokens` [7][10] |
| Gemini 显式 | 按缓存价 | 2.5 Flash 文本 $0.03；2.5 Pro ≤200k $0.125 [9] | /1M token/小时：Flash $1，Pro $4.50，3.x Flash $0.50 [9] | 同上 |
| DeepSeek | 无 | flash 命中 $0.003/$0.006、未命中 $0.15/$0.30；v4-pro $0.022/$0.044 对 $0.66/$1.32。闲时减半 [12] | 无 | `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens` [11] |
| Kimi | K3：5 分钟写入 ¥20，1 小时 ¥40 [17] | K3 命中 ¥2、未命中 ¥20。K2 无写入列，k2.7-code 命中 ¥1.30、未命中 ¥6.50 [14][17] | 无 | `cached_tokens`、`cache_write_tokens`。流式要 `include_usage` [15] |
| 智谱 | 存储现免费 [19] | GLM-5.3：输入 8 元、命中 2 元。指南另写通常 50%，见第 5 节 [19] | 限时免费 [19] | `prompt_tokens_details.cached_tokens` [18] |
| 百炼隐式 | 100% 输入价 [21] | 多数 20%；kimi-k3 与 deepseek-v4.1-flash 为 10% [21] | 没写 | `cached_tokens`；Anthropic 兼容为 `cache_read_input_tokens` [21] |
| 百炼显式 | 125% [21] | 10%（部分 qwen3.8 除外）[21] | 没写 | `cache_creation_input_tokens`、`cached_tokens` [21] |
| OpenRouter | 没写网关加价 | 报上游命中。其转述的倍数不要覆盖厂商页 [23] | — | `cached_tokens`、`cache_write_tokens` [23] |

### 失效与隔离

| | 会 miss / 跟谁隔离 |
|---|---|
| OpenAI | 断点前改 model、tools 顺序或 schema、`reasoning.effort`、`text.verbosity`。不能手删。同一前缀约 >15 次/分钟换机器。不跨组织 [1] |
| Anthropic | 断点前 100% 相同，含图片。改 tool 定义会打掉其后的 system 和 messages。workspace 隔离。旧 Bedrock 拒绝顶层字段，400 [4] |
| DeepSeek | 前缀一改就 miss，输出仍现算。`user_id` 分 KVCache。模型 `deepseek-flash`、`deepseek-v4-pro` [11] |
| Kimi | 前缀一处变化，其后不可复用。按组织隔离。Messages 换 `effort` 会 miss。Responses/Messages 文档只写 `kimi-k3` [14][16] |
| 百炼 | 显式 5 分钟没打到就清；离标记超过 20 个 content 块不命中。tools 并进 system，要逐字节一致。按账号且按模型隔离 [21]。Session：头 `x-dashscope-session-cache: enable`，响应 id 7 天 [22] |
| 智谱 | 格式细差降低命中。作用域没写。中英对「相同 / highly similar」不一致 [20] |

## 3. 变体与适配层

| 路径 | 和直连文档的差 |
|---|---|
| OpenRouter | 粘性键 `session_id` > `x-session-id` > `prompt_cache_key`。没有 `session_id` 时，先有一次命中才开始粘。手工 `provider.order` 不粘。发往 OpenAI 时丢掉 `ttl` [23] |
| OpenRouter→阿里 | 网关要求显式 `cache_control`，写入 TTL 5 分钟 [23]。百炼直连是隐式不能关 |
| Kimi `/anthropic` | base URL `https://api.moonshot.cn/anthropic`。只认顶层 `cache_control`，块级忽略 [16]。Anthropic 官方块级仍有效 [4] |
| 旧 Bedrock | 顶层 `cache_control` 返回 400，要改回块级 [4] |
| Kimi `POST /v1/caching` | 只存在于 2024-07 博客。2026-09-24 请求该 URL 返回 404 [14] |



## 4. 用户需要知道的坑

1. Anthropic、Kimi Messages、百炼的 Anthropic 兼容里，`input_tokens` 不含缓存读写，账单要把 `cache_read_*` 和 `cache_creation_*` 加回去 [4][16][21]。
2. Kimi Chat 不传字段也会收写入费 [14]。同一家的 Messages 不传则不写 [16]。
3. OpenAI 的 `prompt_cache_breakpoint` 发给 Kimi Chat 会 400 [15]。百炼显式和隐式不能出现在同一次请求 [21]。
4. 百炼显式要等这一次响应结束，缓存才存在，并发的第一批会对 miss [21]。
5. 低于门槛会成功但缓存为 0。智谱写两三句系统提示通常打不中 [18]。百炼隐式不保证命中 [21]。
6. Gemini 显式按 token×小时收存储，TTL 拉长会吃掉命中差价 [9]。隐式不保证更便宜 [7]。

## 5. 未决与置信度

- DeepSeek 现行指南不写 64 token，只要求完整匹配 cache prefix unit，间隔没有数字 [11]。64 token 只在上线新闻 [13]。美元和人民币价已按定价页表头核对。
- 智谱指南写命中通常 50%，定价页 GLM-5.3 是 2 元对 8 元（z.ai $0.26/$1.4）[18][19]。矩阵用定价页。英文写 highly similar，中文写相同 [20]。
- Kimi 的 1/10 原文是「以 kimi-k3 为例」。K2 表大约是 1/5，有没有写入费没写 [14][17]。最小 token 没写。
- OpenRouter 写阿里必须显式断点，百炼写隐式不能关。它把 Gemini 显式 TTL 写成 5 分钟，Gemini 文档是默认 1 小时。网关转述不覆盖厂商页 [7][21][23]。
- OpenAI 回看窗口：指南是前 2 加最近 50 个显式断点，reference 是最近 80 个 [1][3]。
- 已启用缓存时，server tool 会再写一笔固定 5 分钟缓存，即使用户标记的是 1 小时 [25]。Gemini 隐式的折扣、TTL、能否关闭、收不收存储费，现行文档都没写。2025-05 博客的 75% 和现行价表对不上，不采用 [26]。百炼 Session 没有自己的 TTL。

## 来源

[1] OpenAI — https://developers.openai.com/api/docs/guides/prompt-caching
[2] OpenAI pricing — https://developers.openai.com/api/docs/pricing
[3] OpenAI Responses — https://developers.openai.com/api/reference/resources/responses/methods/create
[4] Anthropic — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[5] Anthropic Messages — https://platform.claude.com/docs/en/api/messages/create
[6] Anthropic release notes — https://platform.claude.com/docs/en/release-notes/overview
[7] Gemini — https://ai.google.dev/gemini-api/docs/generate-content/caching
[8] Gemini CachedContent — https://ai.google.dev/api/caching
[9] Gemini pricing — https://ai.google.dev/gemini-api/docs/pricing
[10] Gemini Interactions — https://ai.google.dev/gemini-api/docs/caching
[11] DeepSeek — https://api-docs.deepseek.com/guides/kv_cache
[12] DeepSeek pricing — https://api-docs.deepseek.com/quick_start/pricing
[13] DeepSeek news0802 — https://api-docs.deepseek.com/news/news0802
[14] Kimi — https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api
[15] Kimi Chat — https://platform.kimi.com/docs/api/chat.md
[16] Kimi Messages — https://platform.kimi.com/docs/api/messages.md
[17] Kimi pricing — https://platform.kimi.com/docs/pricing/chat
[18] 智谱 — https://docs.bigmodel.cn/cn/guide/capabilities/cache
[19] 智谱价格 — https://docs.bigmodel.cn/cn/guide/start/pricing
[20] Z.AI — https://docs.z.ai/guides/capabilities/cache
[21] 百炼 — https://help.aliyun.com/zh/model-studio/context-cache
[22] 百炼 Responses — https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api
[23] OpenRouter — https://openrouter.ai/docs/features/prompt-caching
[24] Anthropic 2025-08-03 — https://web.archive.org/web/20250803210544/https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
[25] Anthropic server tools — https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching
[26] Gemini implicit 博客 2025-05-08 — https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/
