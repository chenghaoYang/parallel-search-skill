# 各家大模型 API 的上下文缓存

> 回答：要不要改请求、命中怎么计费、能活多久、看哪个字段、什么改动会打穿。OpenAI 指南 Last-Modified 2026-09-23，Gemini 定价页 2026-09-23。Kimi、智谱、通义、OpenRouter 本轮不写进结论。

## 0. 一屏看懂

1. 「OpenAI 和 DeepSeek 不用改代码」仍然成立：两边都写了默认开启 [1][12]。「Anthropic 不用改代码」不成立。现行文档的两种启用方式都要带 `cache_control` [5]。块级断点是不是唯一写法，现行页和 2025-08 快照不一致，不在本屏下结论（第 5 节）。
2. Gemini 是两套，不要并成一句。implicit：2.5 及更新模型默认开，不保证省钱 [8]。explicit：先 `POST /v1beta/cachedContents`，推理请求填 `cachedContent`，存储按时间计费 [8][9]。
3. 命中后不是统一折扣。DeepSeek 分命中价和未命中价，闲时再减半，没有写入费和存储费 [13][14]。Anthropic 写入 1.25×（1 小时档 2×），读取多数 0.1×，个别新模型更低 [5]。OpenAI 旧模型没有写入费，cached 列倍数因模型而异；GPT-5.6 的 1.25×/0.1× 复核前不当全线价格 [1][2]。Gemini implicit 没写百分比 [8]。
4. 寿命对不上。Anthropic 默认 5 分钟，用到就免费续 [5]。OpenAI 更早模型 `in_memory` 大约 5–10 分钟不活跃、最长 1 小时；无 ZDR 默认 `"24h"` [1][3]。GPT-5.6+ 的 `ttl` 只接受 `"30m"` [1]。Gemini explicit 默认 1 小时，延长要 PATCH [8][9]。DeepSeek 没有 TTL 字段，闲置后通常几小时到几天，best-effort [12]。Gemini implicit 的 TTL 官方没写。
5. 确认命中只看响应里的 usage，字段名见第 2 节。Anthropic 的 `input_tokens` 不含缓存前缀，两个 cache 字段都是 0 才是没缓存 [5]。
6. 会打穿缓存的，都是「从开头算的那一段变了」：模型名、工具定义或顺序、断点前的文本和图片。DeepSeek 还多一条：必须完整对上一个已经落盘的前缀单元，中间相同不算 [12][15]。

## 1. Taxonomy

分类轴：边界由谁划定，缓存以什么形态存在。一家可以占两格。这一轴同时解释「要不要改代码」和「有没有一笔存储费」。

| 家族 | 为什么算一类 | 已核实 |
|---|---|---|
| I 隐式前缀 | 服务端自己匹配前缀，请求可以不带缓存字段 | OpenAI 默认、DeepSeek、Gemini implicit |
| II 请求内标记 | 不放标记就不写缓存。标记可以在请求顶层，也可以在内容块上 | Anthropic；OpenAI 仅 GPT-5.6+ 可选 |
| III 独立资源 | 先创建带名字和 TTL 的对象，推理时引用。内容不能改，存储另计 | Gemini `CachedContent` |
| IV 网关 | 自己不定义语义，跟着上游走 | OpenRouter，未摘录 |



## 2. 对照矩阵

### 触发与前缀

| | 不改请求 | 要写的字段 | 前缀划到哪 |
|---|---|---|---|
| OpenAI | 会缓存 [1] | 可选。5.6+：`prompt_cache_breakpoint`、`prompt_cache_options`。旧：`prompt_cache_retention`（Deprecated）、`prompt_cache_key` [3][4] | 完整渲染上下文，含平台自带指令；断点在最新合格消息末尾 [1] |
| Anthropic | 文档给出的启用方式都要带 `cache_control` [5] | `{"type":"ephemeral","ttl":"5m"\|"1h"}`，放顶层或放块上。块级最多 4 个；顶层自动断点占 1 个槽，已有 4 个再加顶层会 400 [5][6] | 顺序固定：`tools` → `system` → `messages`，到被标记的块为止。回看 20 个块 [5] |
| Gemini implicit | 会，2.5+ 默认开 [8] | 无 | 只要求大段公共内容放开头，并在短时间里发相似前缀。对齐算法 ∅ [8] |
| Gemini explicit | 不会 | `POST /v1beta/cachedContents`；请求字段 `cachedContent`，形如 `cachedContents/{id}`。OpenAI 兼容库用 `extra_body.cached_content` [8][9][10] | 缓存内容就是 prompt 前缀。创建后不能改内容，也不能把内容读回来 [8] |
| DeepSeek | 会。Responses API 写明不支持 `prompt_cache_key` / `prompt_cache_retention` [12][16] | 无开关。`user_id` 只做隔离 [17] | 从第 0 个 token 起，且必须完整匹配一个 cache prefix unit。落在硬盘上 [12][15] |
| Kimi、智谱、通义、OpenRouter | ❓ | ❓ | ❓ |

### 门槛与寿命

| | 短于多少不缓存 | 能活多久 |
|---|---|---|
| OpenAI | 5.6+：1024 个可见输入 token，隐藏 token 不计。更早模型官方只写 varies。旧模型上报值取整到 128 的倍数 [1] | 5.6+：`ttl` 唯一值 `"30m"`，也是默认。更早：`in_memory` 大约 5–10 分钟不活跃、最长 1 小时；无 ZDR 默认 `"24h"`，有 ZDR 默认 `in_memory` [1][3] |
| Anthropic | 按模型分档，摘录里从 512 到 4096。低于门槛不报错，只是不缓存 [5] | 默认 5 分钟，命中免费刷新。`ttl:"1h"`。更长的 TTL 必须排在更短的前面 [5][6] |
| Gemini implicit | 2.5 Flash/Pro：2048。3.5/3.6/3.7/3.8 Flash 与 3.1 Pro Preview：4096 [8] | ∅ |
| Gemini explicit | 官方只写 varies by model，数字表放在 implicit 那一节 | 默认 1 小时。`ttl`（如 `"300s"`）或 `expireTime`，无上下界。`PATCH /v1beta/{cachedContent.name}` 只能改过期时间 [8][9] |
| DeepSeek | 见第 5 节。新闻页写 64 token 一单元；现行指南只要求匹配 prefix unit [12][15] | 没有 TTL 参数。不用之后通常几小时到几天。不保证 100% 命中 [12] |

### 计费

单位是每 1M tokens。不要把一家的倍数套到另一家。

| | 写入 | 命中读取 | 存储 |
|---|---|---|---|
| OpenAI 5.6+ | 1.25× 未缓存输入价。表内一行：gpt-5.6-sol 输入 $4.00、写入 $5.00 [1][2] | 0.1×。同一行 cached $0.40 [1][2] | 无 |
| OpenAI 更早 | 无写入费 [1] | cached 列倍数不统一：gpt-5 $1.25→$0.125，gpt-4.1 $2→$0.50，gpt-4o $2.50→$1.25。`gpt-5-pro` 为 `-` [2] | 无 |
| Anthropic | 5 分钟写入 1.25×；1 小时写入 2× [5] | 多数 0.1×；Fable 5.1 与 Mythos 5.1 为 0.025×；Opus 5.5 为 0.05× [5] | 无 |
| Gemini implicit | 未写是否另收写入费 | 只写会把节省传下来，且 “no cost saving guarantee”。无百分比 [8] | 定价页没有把 implicit 和 explicit 拆开 |
| Gemini explicit | 后续请求按缓存价，笔记未摘未缓存基线 | 2.5 Flash 文本/图/视频 $0.03、音频 $0.1；2.5 Pro ≤200k $0.125、更长 $0.25；3.x Flash $0.075（2026-12-31 前，其后 $0.15）[11] | 每 1M tokens 每小时：2.5 Flash $1.00，2.5 Pro $4.50，3.x Flash $0.50（其后 $1.00）[11] |
| DeepSeek | 无单独写入价 | 闲时=峰时一半。flash 命中 $0.003/$0.006、未命中 $0.15/$0.30；v4-pro 命中 $0.022/$0.044、未命中 $0.66/$1.32（人民币见定价页，约 0.02 元起）[13][14] | 无。高峰：北京时间工作日 9:00–12:00、14:00–18:00 [14] |

OpenAI：缓存 token 仍计入 TPM [1]。Anthropic：cache hit 不扣 rate limit [5]。

### 怎么确认命中了

| 接口 | 命中 | 写入或未命中 |
|---|---|---|
| OpenAI Responses | `usage.input_tokens_details.cached_tokens` | `cache_write_tokens`。还可有 `prompt_cache_diagnostics`（`cache_miss` 的 reason 含 `model_changed`、`tools_changed`）[3] |
| OpenAI Chat | `usage.prompt_tokens_details.cached_tokens` | `cache_write_tokens` [4] |
| Anthropic | `usage.cache_read_input_tokens` | `cache_creation_input_tokens`，再拆成 `ephemeral_5m_input_tokens` 与 `ephemeral_1h_input_tokens`。总输入是三者之和 [5][6] |
| Gemini generateContent | `usageMetadata.cachedContentTokenCount` | 资源本身的 `usageMetadata.totalTokenCount` 是缓存有多大 [8][10] |
| Gemini Interactions | `usage.total_cached_tokens`。这个 API 只有 implicit [7] | — |
| DeepSeek Chat | `usage.prompt_cache_hit_tokens`（等于 `prompt_tokens_details.cached_tokens`） | `prompt_cache_miss_tokens`。`prompt_tokens` = hit + miss [12][17] |
| DeepSeek Responses | `usage.input_tokens_details.cached_tokens` [16] | |

### 什么改动会失效，缓存在谁之间

| | 会 miss | 隔离与模型 |
|---|---|---|
| OpenAI | 断点前内容，或 model、tools 名/schema/顺序、`parallel_tool_calls`、`text.format`、`reasoning.effort`、`text.verbosity`、compaction。不能手删 [1] | 不跨组织、不跨区域。同一前缀约 >15 次/分钟会溢出到别的机器。5.6+ 的 `prompt_cache_key` 只做分账 [1] |
| Anthropic | 标记块及之前 100% 相同，含图片。改 tool 定义则整段失效；改 web search/citations/speed 则 system+messages 失效；改 `tool_choice`、图片、thinking、effort 则 messages 失效 [5] | 全部现役模型，已 GA。Claude API 按 workspace。旧 Bedrock（Opus 4.6 及更早）拒绝顶层 `cache_control`（400）[5] |
| Gemini explicit | 换模型就不能用这份缓存 [9] | 绑创建时的 model。Paid 才有；2.5 的 Free 档写着 Not available。可 `DELETE` [9][11] |
| Gemini implicit | ∅ | 上表门槛里的那些模型 [8] |
| DeepSeek | 前缀有改动就 miss。输出不走缓存，仍受 temperature 影响。换 `user_id` 就是另一套缓存 [12][18] | 当前枚举 `deepseek-flash`、`deepseek-v4-pro` [17] |

## 3. 变体与适配层

笔记里写清楚的适配差异只有一条：Anthropic 顶层 `cache_control` 在 legacy Bedrock（Opus 4.6 及更早）会 400，块级断点仍然可用。1 小时 TTL 覆盖 Claude API、Bedrock（含 legacy）、Claude Platform on AWS、Google Cloud、Foundry [5]。

Azure OpenAI、Vertex、Bedrock 自己的缓存专页本轮没有摘字段。

## 4. 用户需要知道的坑

1. Anthropic 的 `input_tokens` 只算最后一个断点之后的 token。对账单要把 `cache_creation_input_tokens` 和 `cache_read_input_tokens` 加回去 [5]。
2. 短请求会成功但缓存为 0：低于第 2 节门槛时，Anthropic 不报错 [5]。
3. DeepSeek 要完整等于已落盘的 prefix unit（请求结束、公共前缀或固定间隔时才写下），不保证命中 [12]。
4. OpenAI 同一前缀约 >15 次/分钟会换机器，缓存 token 仍占 TPM [1]。Anthropic 命中不占 rate limit [5]。
5. 工具顺序属于前缀。Anthropic 改 tool 定义会连带打掉 system 和 messages [5]。
6. Gemini explicit 按 token×小时收存储，TTL 过长会吃掉命中差价；implicit 看到缓存 token 也不保证更便宜 [8][11]。
7. 清除：OpenAI 不行 [1]；Gemini explicit 可 DELETE [9]；DeepSeek 只能等过期 [12]。

## 5. 未决与置信度

- Anthropic 启用方式 ⚔。现行页：顶层 `cache_control` 自动打到最后可缓存块，或至少一个块级断点 [5]。2025-08-03 快照只要求块级断点，且 1 小时 TTL 要 beta header `extended-cache-ttl-2025-04-11` [19]。现行页无 Updated 日期。已确定的是两种现行写法都要 `cache_control`。
- OpenAI 5.6 的 1.25×/0.1× 与 `"30m"` 和「旧模型无写入费」在同一份指南，不是两页对打 [1]。复核前不升成全线价格。笔记里「复用免费续 30 分钟」的原句只说 `"30m"` 是唯一默认值，续期不算已证实。
- OpenAI 回看窗口 ⚔：指南的 2+50+20 与 reference 的 latest 80 不一致 [1][3]。`prompt_cache_retention` 已 Deprecated，但 `prompt_cache_options.ttl` 只给 5.6+，旧模型仍靠它 [3][4]。
- DeepSeek：新闻页的 64 token 与 $0.014 已被该页指向定价页 [15]。64 是否仍是存储单元未决。美元数字在主张里，原句只摘了闲时减半，待复核 [13]。
- Gemini implicit 的 TTL、能否关闭、隔离、折扣百分比：官方没写。Anthropic 与 DeepSeek 正文无更新日期。
- Kimi、智谱、通义/百炼、OpenRouter，以及 Azure、Vertex、Bedrock 专页：❓。

## 来源

[1] OpenAI Prompt caching — https://developers.openai.com/api/docs/guides/prompt-caching
[2] OpenAI Pricing — https://developers.openai.com/api/docs/pricing
[3] OpenAI Create response — https://developers.openai.com/api/reference/resources/responses/methods/create
[4] openai-openapi — https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml
[5] Anthropic Prompt caching — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[6] Anthropic Create a message — https://platform.claude.com/docs/en/api/messages/create
[7] Gemini caching (Interactions) — https://ai.google.dev/gemini-api/docs/caching
[8] Gemini context caching — https://ai.google.dev/gemini-api/docs/generate-content/caching
[9] Gemini CachedContent API — https://ai.google.dev/api/caching
[10] Gemini generateContent API — https://ai.google.dev/api/generate-content
[11] Gemini pricing — https://ai.google.dev/gemini-api/docs/pricing
[12] DeepSeek Context Caching — https://api-docs.deepseek.com/guides/kv_cache
[13] DeepSeek Pricing — https://api-docs.deepseek.com/quick_start/pricing
[14] DeepSeek 模型与价格 — https://api-docs.deepseek.com/zh-cn/quick_start/pricing
[15] DeepSeek 硬盘缓存上线 — https://api-docs.deepseek.com/news/news0802
[16] DeepSeek Responses API — https://api-docs.deepseek.com/guides/responses_api
[17] DeepSeek Create Chat Completion — https://api-docs.deepseek.com/api/create-chat-completion
[18] DeepSeek Rate limit — https://api-docs.deepseek.com/quick_start/rate_limit
[19] Anthropic 指南 2025-08-03 快照 — https://web.archive.org/web/20250803210544/https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
