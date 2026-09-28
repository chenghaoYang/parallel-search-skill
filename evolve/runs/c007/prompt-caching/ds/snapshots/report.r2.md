# 各家大模型 API 的 Prompt Caching 对照

> 对比 8 家 LLM API/网关的上下文缓存，截至 2026-09。§0 结论、§2 矩阵、§4 排障。

## 0. 一屏看懂

1. **「OpenAI/DeepSeek 自动、Anthropic 必须手动打断点」已过时。** Anthropic 2026-02-19 起有 automatic caching：顶层放一个 `cache_control` 即可，自动落断点随对话前移 [7]；反向，GPT-5.6（2026-07）新增显式断点 `prompt_cache_breakpoint`（≤4）并首次对写收费 1.25× [1][4]。真正零改代码的是 DeepSeek、智谱、Gemini implicit、通义隐式和 OpenAI 默认模式 [6][14][21][22][9]。
2. **计费分三家**：纯读折扣（DeepSeek 命中≈未命中 1/50、Gemini implicit 10%、通义隐式 20%、智谱 20–50%）；写溢价+读折扣（Anthropic 写 1.25×/2× 读 0.1×；GPT-5.6 写 1.25×；通义显式写 125% 读 10%；Kimi k3 写 ¥20–40）；存储按时计费（Gemini explicit $0.5–4.5/1M·h，智谱限时免费）[6][11][15][20][22][26]。
3. **TTL 5m~数天**：Anthropic 5m/1h 命中免费续；OpenAI 5.6+ 30m 命中刷新，旧模型可选 24h；DeepSeek「数小时~数天」不保活；Gemini explicit 默认 1h 可 PATCH；智谱/通义隐式未写明 [1][6][9][14][22]。
4. **命中看 usage 字段**：OpenAI `usage.*_tokens_details.cached_tokens`+`cache_write_tokens`；Anthropic `cache_read_input_tokens`；DeepSeek `prompt_cache_hit_tokens`；Gemini `usageMetadata.cachedContentTokenCount`；OpenRouter 另给 `cache_discount` [1][6][9][17][24]。
5. **两家有官方 miss 诊断**：OpenAI `prompt_cache_diagnostics`（5.6+）、Anthropic `diagnostics`/`cache_miss_reason`（2026-09-23 GA）直接回答「为什么没命中」[3][7]。
6. **失效规则共识：前缀逐 token 相同**，一处变化其后全失效；Anthropic 为 tools→system→messages 层级失效；OpenAI 的 tools/effort/verbosity 均参与匹配 [1][6][19][22]。
7. **OpenRouter 做断点互译但不译 TTL**：`cache_control`↔`prompt_cache_breakpoint` 按上游改写；sticky routing 粘滞同一上游（10m 空闲过期）[24]。

## 1. Taxonomy

**轴 A：谁决定缓存位置**
- **A 隐式自动前缀**：不传字段，provider 按前缀命中——DeepSeek、智谱、Gemini implicit、通义隐式、OpenAI 默认。零接入但命中不保证。
- **B opt-in 字段+自动落断点**——Anthropic automatic（顶层 `cache_control`）、Kimi（`prompt_cache_options.ttl` 选档）。
- **C 手动断点**：块上标记即写入点——Anthropic explicit、GPT-5.6 explicit、通义显式（各 ≤4）。
- **D 托管缓存对象**：先 POST 创建再按名引用——Gemini explicit `cachedContents`（Beta）；Kimi 旧 `/v1/caching` 已下线。

**轴 B：计费模型**：纯读折扣（A 类全体）→ 写溢价+读折扣（Anthropic、GPT-5.6+、通义显式、Kimi k3）→ 存储按时计费（Gemini explicit；智谱限时免费）。

**维度**：D1 机制与字段名｜D2 最小门槛｜D3 计费｜D4 TTL 与续期｜D5 命中确认字段｜D6 失效条件｜D7 模型范围。

## 2. 对照矩阵

### 机制 / 门槛 / TTL / 命中字段

| 实体 | D1 机制 | D2 门槛 | D4 TTL·续期 | D5 命中字段 |
|---|---|---|---|---|
| OpenAI ≤5.5 | 自动，默认开 [1] | 随请求设置变（tools/effort 等影响）[1] | `prompt_cache_retention`: in_memory 5–10m / 24h（非 ZDR 默认 24h）[1] | `usage.*_tokens_details.cached_tokens` [1] |
| OpenAI 5.6+ | +`prompt_cache_options.mode/ttl/prewarm`、`prompt_cache_breakpoint` ≤4 [4] | 1,024 visible tok [1] | 30m，命中刷新 [1] | 同上 +`cache_write_tokens`+诊断 [1][3] |
| Anthropic | 顶层 `cache_control` 自动断点，或块级显式 ≤4（ephemeral）[6] | 512–4,096 按模型分档；不足静默跳过 [6] | 默认 5m、`"ttl":"1h"`；命中免费续 [6] | `cache_creation/read_input_tokens`+`cache_miss_reason` [6][7] |
| Gemini implicit | 默认开，无开关 [9] | 2.5 系 2,048；3.x Flash/3.1 Pro 4,096（Vertex 侧 6,144）[9][31] | Gemini API 未文档化；Vertex ≤24h [9][13] | `usageMetadata.cachedContentTokenCount` [9] |
| Gemini explicit | POST `/v1beta/cachedContents` 建对象，`cachedContent` 引用（Beta）[9][10] | 官方仅「varies by model」[9] | 默认 1h 无上下界，可 PATCH ttl/expire_time [9] | 同上 [10] |
| DeepSeek | 全自动落盘，零改动 [14][16] | 64 tok 单元（2024 公告值）[16] | 不用则清，数小时~数天；best-effort [14] | `prompt_cache_hit_tokens`/`_miss_tokens` [17] |
| Kimi | 隐式自动；可选 `prompt_cache_options`（ttl 5m/1h）；显式断点被拒（400）[19][29] | >256 prompt tok（k3 页）[28] | 5m 或 1h，写入时锁定，命中按原档续期 [19] | `cached_tokens`（各端点位置略异）[19] |
| 智谱 | 隐式自动，无显式开关 [21][26] | 建议 ≥500 tok（非硬性）[21] | TTL 未写；英文站称 "reasonable time limits" [21][27] | `usage.prompt_tokens_details.cached_tokens` [21] |
| 通义·隐式 | 自动开启且无法关闭 [22] | 1,024（百炼部署 GLM/MiniMax 512）[22] | 不确定，定期清理 [22] | `cached_tokens` [22] |
| 通义·显式 | message 上 `cache_control` ephemeral ≤4；DashScope 原生 SDK 亦支持 [22][23] | 1,024 [22] | 5m，每次命中重置 [22] | 同上 +`cache_creation_input_tokens` [22] |
| OpenRouter | 透传+断点互译；Anthropic/Vertex/Azure/Bedrock 可用顶层 cache_control [24] | 随上游 [24] | 随上游，TTL 不互译 [24] | `usage` 缓存字段 +`cache_discount` [24][25] |

### 计费（读=命中输入价；写=建缓存价）

| 实体 | 写价 | 读价 | 存储/其他 |
|---|---|---|---|
| OpenAI ≤5.5 | 免费 [24] | 输入价 10%–50%（4o 50%、5 系 10%）[2][2] | pro 系与 Batch(pre-5) 无缓存价 [2] |
| OpenAI 5.6+ | 1.25× [1] | 0.1× [1] | cached tok 仍计 TPM [1] |
| Anthropic | 5m=1.25×；1h=2× [6] | 0.1×（Fable/Mythos 5.1 0.025×、Opus 5.5 0.05×）[6] | — |
| Gemini implicit | 免费 [9] | 输入价 10%（如 2.5 Flash $0.03/1M）[11] | — |
| Gemini explicit | ≈输入价+5m 存储折算（OpenRouter 口径）[24] | 同 implicit 表 [11] | $0.5–4.5/1M tok·h 按模型 [11] |
| DeepSeek | 免费 [16] | 峰 $0.006/谷 $0.003（flash）；v4-pro 9/14 起路由到 Flash 按 Flash 价 [15][18] | 存储免费 [16] |
| Kimi | k3：5m 档 ¥20、1h 档 ¥40/1M；k2 系免写费 [20] | k3 ¥2、k2.7-code ¥1.30、k2.6 ¥1.10/1M [20] | 命中续期不另收费；Messages 不传顶层 cache_control 则只读不写 [19][29] |
| 智谱 | 免费 [21] | 指南称约 50%，定价页旗舰 ~20–25%（GLM-5.3 ¥2/¥8）；限标准计费 [21][26] | 存储按 元/1M tok·h 计，限时免费 [26] |
| 通义·隐式 | 免费 [22] | 20%（例外：deepseek-v4.1-flash/kimi-k3 10%、部分 GLM 25%）[22] | — |
| 通义·显式 | 125%（仅新增部分）[22] | 10% [22] | — |
| OpenRouter | 透传上游 [24] | 透传；BYOK 抽同价 5% [24][25] | `usage.cost_details.upstream_inference_cost` 仅 BYOK [25] |

D7 模型范围：Anthropic 全现役 [6]；OpenAI gpt-4o+ [1]；Gemini implicit 2.5+、explicit 多数模型 [9]；DeepSeek `deepseek-flash`/`deepseek-v4-pro` [15]；Kimi k3 可写、k2 只读折扣 [19][20]；智谱定价页命中列即清单 [26]；通义分地域清单含第三方模型 [22]。

## 3. 变体与适配层

- **OpenRouter**：`prompt_cache_breakpoint` 路由到 Anthropic/Google 转默认 5m `cache_control`，TTL 不译；Gemini 显式只取末断点；Responses API 不暴露块级 `cache_control`；sticky routing 按账户×模型×会话粘滞（`session_id`/`prompt_cache_key` 做 key），10m 空闲过期，手动 `provider.order` 禁用 [24]。
- **托管差异**：Anthropic automatic caching 在旧版 Bedrock（Opus 4.6 及更早）不可用，顶层字段 400 [6]；Vertex implicit 全项目默认开、≤24h，explicit TTL 默认 60m 最短 1m [13][31]；DeepSeek 的 Anthropic 端点对 `cache_control` 全部标 "Ignored" [30]。
- **Kimi 旧显式缓存**：`POST /v1/caching` 建对象、`role:"cache"` 引用，仅 moonshot-v1 系；现行文档已删（二手）[19]。

## 4. 用户需要知道的坑

1. **tool/schema 在缓存前缀内**：改 tool 名/描述/参数，Anthropic 全失效、OpenAI 前缀不匹配；tool_use 块 JSON key 顺序不稳（Swift/Go）破缓存 [6][1]。→ tools/system 放最前、逐字节稳定。
2. **低于最小门槛静默不缓存**（Anthropic 不报错）；Kimi 传显式断点直接 400 [6][29]。→ 先看 usage 确认命中。
3. **命中不保证**：Gemini implicit、通义隐式、DeepSeek 均 best-effort；OpenAI 单前缀约 15 RPM 溢出会路由到无缓存机器，`prompt_cache_key` 只提高粘性 [14][22][9][1]。
4. **TTL/续期语义各异**：Anthropic 命中免费续；Kimi 按锁定档续；通义显式命中重置 5m；Gemini explicit 只能 PATCH [6][19][22][9]。
5. **价格与模型名漂移**：DeepSeek chat/reasoner 已退役、v4-pro 按 Flash 价；Gemini 2.5 Flash 门槛 1,024→2,048、折扣 75%→90%；OpenRouter 的 Gemini 门槛已落后官方 [15][18][12][24]。
6. **网关≠上游**：OpenRouter 不译 TTL；经它打 Anthropic 仍需 opt-in 字段 [24]。

## 5. 未决与置信度

- 智谱 TTL 数值、失效规则、显式开关无官方明文（指南/API ref/兼容页已查）；「约 50%」与定价表 ~20–25% 的矛盾以定价页为准。
- Kimi 256 阈值只见于 K3 快速开始页，是否适用 k2 系未写明；缓存块大小未公布。
- Gemini implicit 存活时长官方未写（6 页反证通过）；Vertex 与 Gemini API 新模型 implicit 门槛不一致（6,144 vs 4,096）。
- DeepSeek 64-token 单元出自 2024 公告，现行指南仅说 "fixed token intervals"；anthropic 端点 usage 缓存字段未验证。
- 未逐项核验：Bedrock/Azure/LiteLLM；跨租户时序侧信道（arXiv 2502.07776）仅二手线索。

## 来源

[1] OpenAI 缓存指南 — https://developers.openai.com/api/docs/guides/prompt-caching
[2] OpenAI 定价 — https://developers.openai.com/api/docs/pricing
[3] OpenAI 缓存诊断 — https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics
[4] OpenAI CC 参考 — https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
[6] Anthropic prompt caching — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[7] Anthropic release notes — https://platform.claude.com/docs/en/release-notes/overview
[9] Gemini context caching — https://ai.google.dev/gemini-api/docs/generate-content/caching
[10] Gemini caching API 参考 — https://ai.google.dev/api/caching
[11] Gemini 定价 — https://ai.google.dev/gemini-api/docs/pricing
[12] Gemini implicit 公告 — https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/
[13] Vertex 缓存博客 — https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching
[14] DeepSeek 缓存指南 — https://api-docs.deepseek.com/guides/kv_cache
[15] DeepSeek 定价 — https://api-docs.deepseek.com/quick_start/pricing
[16] DeepSeek 缓存公告 — https://api-docs.deepseek.com/news/news0802
[17] DeepSeek API 参考 — https://api-docs.deepseek.com/api/create-chat-completion
[18] DeepSeek V4.1 公告 — https://api-docs.deepseek.com/news/news260910
[19] Kimi 缓存指南 — https://platform.kimi.com/docs/guide/context-caching.md
[20] Kimi 定价 — https://platform.kimi.com/docs/pricing/chat.md
[21] 智谱缓存指南 — https://docs.bigmodel.cn/cn/guide/capabilities/cache
[22] 阿里云百炼缓存 — https://help.aliyun.com/zh/model-studio/context-cache
[23] 阿里云显式缓存 — https://help.aliyun.com/zh/model-studio/explicit-cache-guide
[24] OpenRouter 缓存 — https://openrouter.ai/docs/features/prompt-caching
[25] OpenRouter usage — https://openrouter.ai/docs/cookbook/administration/usage-accounting
[26] 智谱定价 — https://docs.bigmodel.cn/cn/guide/start/pricing.md
[27] 智谱英文缓存指南 — https://docs.z.ai/guides/capabilities/cache.md
[28] Kimi K3 快速开始 — https://platform.kimi.com/docs/guide/kimi-k3-quickstart.md
[29] Kimi Chat API — https://platform.kimi.com/docs/api/chat.md
[30] DeepSeek Anthropic 端点 — https://api-docs.deepseek.com/guides/anthropic_api
[31] Vertex 缓存概览 — https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview
