# 各家大模型 API 的 Prompt Caching 对照

> 对比 OpenAI、Anthropic、Gemini、DeepSeek、Kimi、智谱、通义千问及 OpenRouter 的上下文缓存。截至 2026-09。先读 §0 拿结论，选型查 §2 矩阵，接线排障查 §4。

## 0. 一屏看懂

1. **「OpenAI/DeepSeek 自动、Anthropic 必须手动打断点」已过时。** Anthropic 2026-02-19 起支持 automatic caching：请求顶层放一个 `cache_control` 即可，系统自动把断点打到最后一个可缓存块并随对话前移 [7]；反向地，OpenAI 自 GPT-5.6（2026-07）起新增显式断点 `prompt_cache_breakpoint`（每请求 ≤4 个）并首次对缓存写收费 1.25× [1][4]。Anthropic 的 opt-in 字段仍非默认开启，「完全不改代码」的只有 DeepSeek、智谱、Gemini implicit、通义隐式和 OpenAI 默认模式 [6][14][21][22][9]。
2. **计费分三家**：纯读折扣（DeepSeek 命中价≈未命中的 1/50、智谱约 50%、Gemini implicit 10%、通义隐式 20%）；写溢价+读折扣（Anthropic 写 1.25×(5m)/2×(1h)、读 0.1×；GPT-5.6 写 1.25×；通义显式写 125%、读 10%；Kimi k3 写 ¥20–40/1M）；存储按时计费（Gemini explicit $0.5–4.5/1M tok·h）[6][11][15][19][20][21][22]。
3. **TTL 从 5 分钟到数天**：Anthropic 默认 5m、可选 1h，命中免费续期；OpenAI 5.6+ 固定 30m（命中刷新），旧模型 `prompt_cache_retention` 可选 24h；DeepSeek「数小时到数天」不保活；Gemini explicit 默认 1h 且可 PATCH 任意 TTL；智谱未写；通义隐式不定期清理 [1][6][9][12][14][22]。
4. **确认命中看 usage 字段，各家名不同**：OpenAI `usage.*_tokens_details.cached_tokens`+`cache_write_tokens`；Anthropic `cache_read_input_tokens`/`cache_creation_input_tokens`；DeepSeek `prompt_cache_hit_tokens`；Gemini `usageMetadata.cachedContentTokenCount`；OpenRouter 另有 `cache_discount` 金额 [1][6][9][14][17][24]。
5. **两家已有官方 miss 诊断**：OpenAI `prompt_cache_diagnostics`（5.6+，2026-09 GA）与 Anthropic `diagnostics`/`cache_miss_reason`（2026-09-23 GA）能直接回答「为什么没命中」[3][7]。
6. **失效规则高度一致：前缀逐 token 相同。** 通则是「前缀中任何一处变化，其后全部不可复用」；Anthropic 明确 tools→system→messages 层级失效，改 tool 定义全失效；OpenAI 的 tools/effort/verbosity 均参与前缀匹配 [1][6][19][22]。
7. **OpenRouter 做断点互译但不译 TTL**：`cache_control`↔`prompt_cache_breakpoint` 按上游改写，TTL 语义不保证；sticky routing 把会话粘在同一上游 endpoint 保命中（10 分钟空闲过期）[24]。

## 1. Taxonomy

**轴 A：谁来决定缓存位置**（解释机制差异）
- **A 隐式自动前缀**：不传任何字段，provider 侧按前缀命中——DeepSeek、智谱、Gemini implicit、通义隐式、OpenAI 默认模式。零接入成本但命中不保证。
- **B opt-in 字段 + 自动落断点**：给一个开关/标记但不指位置——Anthropic automatic caching（顶层 `cache_control`）、Kimi（默认自动，`prompt_cache_options.ttl` 选 5m/1h）。
- **C 手动断点**：在块上打标记，位置即写入点——Anthropic explicit（≤4）、GPT-5.6 explicit、通义显式（`cache_control` ephemeral ≤4）。
- **D 托管缓存对象**：先 POST 创建再按名引用——Gemini explicit `cachedContents`（Beta）、Kimi 已下线的 `/v1/caching`。

**轴 B：计费模型**（解释价格差异）：纯读折扣（A 类全体）→ 写溢价+读折扣（Anthropic、GPT-5.6+、通义显式、Kimi k3）→ 存储按时计费（Gemini explicit）。

**维度**：D1 机制与字段名｜D2 最小门槛｜D3 计费｜D4 TTL 与续期｜D5 命中确认字段｜D6 失效条件｜D7 模型范围。

## 2. 对照矩阵

### 机制 / 门槛 / TTL / 命中字段

| 实体 | D1 机制 | D2 门槛 | D4 TTL·续期 | D5 命中字段 |
|---|---|---|---|---|
| OpenAI ≤5.5 | 自动，默认开 [1] | 随请求设置变；命中 128 递增 [1][5] | `prompt_cache_retention`: in_memory 5–10m / 24h（非 ZDR 默认 24h）[1] | `usage.*_tokens_details.cached_tokens` [1] |
| OpenAI 5.6+ | +`prompt_cache_options.mode/ttl/prewarm`、`prompt_cache_breakpoint` ≤4 [4] | 1,024 visible tok [1] | 30m，命中刷新 [1] | 同上 +`cache_write_tokens` +诊断 [1][3] |
| Anthropic | 顶层 `cache_control` 自动断点，或块级 ≤4 显式断点（ephemeral）[6] | 512–4,096 按模型分档；不足静默跳过 [6] | 默认 5m，`"ttl":"1h"`；命中免费续期 [6] | `cache_creation_input_tokens`/`cache_read_input_tokens` +`cache_miss_reason` [6][7] |
| Gemini implicit | 默认开，无开关 [9] | 2.5 系 2,048；3.x Flash/3.1 Pro 4,096 [9] | 未文档化（Vertex 侧 ≤24h）[9][13] | `usageMetadata.cachedContentTokenCount` [9] |
| Gemini explicit | POST `/v1beta/cachedContents` 建对象，`cachedContent` 引用（Beta）[9][10] | 官方仅「varies by model」 [9] | 默认 1h，无上下界，可 PATCH ttl/expire_time [9] | 同上 [10] |
| DeepSeek | 全自动落盘，零改动 [14][16] | 64 tok 单元（2024 公告值）[16] | 不用则清，约数小时~数天；best-effort [14] | `prompt_cache_hit_tokens`/`_miss_tokens` [17] |
| Kimi | 隐式自动；可选 `prompt_cache_options`（ttl 5m/1h）[19] | 未公布（按块存储）[19] | 5m 或 1h，写入时锁定，命中按原档续期 [19] | `cached_tokens`（各端点位置略异）[19] |
| 智谱 | 隐式自动，无开关 [21] | 建议 ≥500 tok（非硬性）[21] | 官方未写 ∅ | `usage.prompt_tokens_details.cached_tokens` [21] |
| 通义·隐式 | 自动开启且无法关闭 [22] | 1,024（百炼部署 GLM/MiniMax 512）[22] | 不确定，定期清理 [22] | `cached_tokens` [22] |
| 通义·显式 | message 上 `cache_control` ephemeral ≤4 [22][23] | 1,024 [22] | 5m，每次命中重置 5m [22] | 同上 +`cache_creation_input_tokens` [22] |
| OpenRouter | 透传+断点互译；Anthropic/Vertex/Azure/Bedrock 可用顶层 cache_control [24] | 随上游 [24] | 随上游，TTL 不互译 [24] | `usage` 缓存字段 +`cache_discount` [24][25] |

### 计费（读=命中输入价；写=建缓存价）

| 实体 | 写价 | 读价 | 存储/其他 |
|---|---|---|---|
| OpenAI ≤5.5 | 免费 [24] | 输入价 50%–10%（4o 50%、4.1 25%、5 系 10%）[2] | pro 系与 Batch(pre-5) 无缓存价 [2] |
| OpenAI 5.6+ | 1.25× [1] | 0.1× [1] | cached tok 仍计 TPM [1] |
| Anthropic | 5m=1.25×；1h=2× [6] | 0.1×（Fable/Mythos 5.1 0.025×、Opus 5.5 0.05×）[6] | — |
| Gemini implicit | 免费 [9] | 输入价 10%（如 2.5 Flash $0.03/1M）[11] | — |
| Gemini explicit | =输入价+5m 存储折算（OpenRouter 口径）[24] | 同 implicit 表 [11] | $0.5–4.5/1M tok·h 按模型 [11] |
| DeepSeek | 免费 [16] | 峰 $0.006 / 谷 $0.003（flash）；v4-pro 页面价 $0.044 但 2026-09-14 起路由到 Flash 按 Flash 价 [15][18] | 存储免费 [16] |
| Kimi | k3：5m 档 ¥20、1h 档 ¥40/1M；k2 系免写费 [20] | k3 ¥2、k2.7-code ¥1.30、k2.6 ¥1.10/1M [20] | 命中续期不另收费 [19] |
| 智谱 | 免费 [21] | 约标准价 50%（限标准计费，资源包/ Coding Plan 除外）[21] | — |
| 通义·隐式 | 免费（按输入价 100%）[22] | 20%（例外：deepseek-v4.1-flash/kimi-k3 10%、部分 GLM 25%）[22] | — |
| 通义·显式 | 125%（仅新增部分）[22] | 10% [22] | — |
| OpenRouter | 透传上游 [24] | 透传；BYOK 抽同价 5% [24][25] | `usage.cost_details.upstream_inference_cost` 仅 BYOK [25] |

## 3. 变体与适配层

- **OpenRouter 互译**：`prompt_cache_breakpoint` 路由到 Anthropic/Google 时转默认 5m `cache_control`，TTL 不翻译；Gemini 显式只取最后一个断点；Responses API 不暴露块级 `cache_control` [24]。sticky routing 按 账户×模型×会话 粘滞（`session_id`/`prompt_cache_key` 可做 key），10 分钟无活动过期；手动 `provider.order` 会禁用粘滞 [24]。
- **托管差异**：Anthropic automatic caching 在旧版 Bedrock 集成（Opus 4.6 及更早）不可用，顶层字段返回 400 [6]；Vertex AI implicit 对全部项目默认开、缓存 ≤24h 删除 [13]；Azure OpenAI 有平行文档、默认值略异（未逐项核验）。
- **Kimi 旧显式缓存**：`POST /v1/caching` 建缓存对象、`role:"cache"` 引用，仅 moonshot-v1 系可用；现行官方文档索引已删此端点（二手）[19]。

## 4. 用户需要知道的坑

1. **tool/schema 定义在缓存前缀内**：改 tool 名/描述/参数，Anthropic 整个缓存失效、OpenAI 前缀不匹配；tool_use 块 JSON key 顺序不稳（Swift/Go）会破缓存；`tool_choice`/图片改动只影响 messages 层 [6][1]。→ 把 tools/system 放最前且保持逐字节稳定。
2. **低于最小门槛静默不缓存**（Anthropic 不报错）[6]；OpenAI <5.6 门槛随 tools/effort 等变化 [1]。→ 先查 usage 字段确认真的命中。
3. **命中不保证**：Gemini implicit、通义隐式、DeepSeek 均为 best-effort（同 prompt 也可能 miss）；OpenAI 单前缀约 15 RPM 溢出会路由到无缓存机器，`prompt_cache_key` 只提高粘性 [14][22][9][1]。
4. **TTL 与续期语义不同**：Anthropic 命中免费续 5m/1h；Kimi 命中按写入时锁定档续期；通义显式每次命中重置 5m；Gemini explicit 不会自动续、只能 PATCH；OpenAI 5.6+ 命中刷新 30m [6][19][22][9][1]。
5. **价格漂移与模型改名**：DeepSeek chat/reasoner 已退役（2026-07-24），v4-pro 请求实际按 Flash 价；Gemini 2.5 Flash 门槛 1,024→2,048、折扣 75%→90%；OpenRouter 文档的 Gemini 门槛已落后于官方 [15][18][12][9][24]。
6. **Kimi k2 系「不支持 Cache Write」但仍有命中价**——自动缓存命中享折扣、不收写费，不等于不支持缓存 [19][20]。

## 5. 未决与置信度

- 智谱 TTL/失效规则/模型清单官方未写（已 grep 原始 HTML 确认）；Kimi 最小 token 数与缓存块大小未公布；Gemini implicit 的 TTL 与可否关闭未文档化——以上按 ∅ 处理。
- DeepSeek 64-token 单元出自 2024 上线公告，现行指南只说「fixed token intervals」，V4 架构下未再确认。
- 冲突已裁决：Gemini 门槛/折扣以 2026-09-11 更新的官方页为准；DeepSeek v4-pro 定价页与 9/14 路由公告矛盾，以公告为准。
- 未逐项核验：Bedrock/Azure/LiteLLM 等托管细节；跨租户缓存时序侧信道（arXiv 2502.07776）仅二手线索；阿里显式缓存完整模型清单。

## 来源

[1] OpenAI Prompt Caching guide — https://developers.openai.com/api/docs/guides/prompt-caching
[2] OpenAI Pricing — https://developers.openai.com/api/docs/pricing
[3] OpenAI cache diagnostics — https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics
[4] OpenAI Chat Completions reference — https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
[5] OpenAI Cookbook prompt caching 201 — https://developers.openai.com/cookbook/examples/prompt_caching_201
[6] Anthropic prompt caching — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[7] Anthropic release notes — https://platform.claude.com/docs/en/release-notes/overview
[8] Claude pricing — https://claude.com/pricing
[9] Gemini context caching — https://ai.google.dev/gemini-api/docs/generate-content/caching
[10] Gemini API caching reference — https://ai.google.dev/api/caching
[11] Gemini pricing — https://ai.google.dev/gemini-api/docs/pricing
[12] Gemini implicit caching 公告 — https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/
[13] Vertex AI context caching — https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching
[14] DeepSeek KV cache 指南 — https://api-docs.deepseek.com/guides/kv_cache
[15] DeepSeek pricing — https://api-docs.deepseek.com/quick_start/pricing
[16] DeepSeek 缓存上线公告 — https://api-docs.deepseek.com/news/news0802
[17] DeepSeek API reference — https://api-docs.deepseek.com/api/create-chat-completion
[18] DeepSeek V4.1 公告 — https://api-docs.deepseek.com/news/news260910
[19] Kimi context caching — https://platform.kimi.com/docs/guide/context-caching.md
[20] Kimi pricing — https://platform.kimi.com/docs/pricing/chat.md
[21] 智谱上下文缓存 — https://docs.bigmodel.cn/cn/guide/capabilities/cache
[22] 阿里云百炼上下文缓存 — https://help.aliyun.com/zh/model-studio/context-cache
[23] 阿里云显式缓存指南 — https://help.aliyun.com/zh/model-studio/explicit-cache-guide
[24] OpenRouter prompt caching — https://openrouter.ai/docs/features/prompt-caching
[25] OpenRouter usage accounting — https://openrouter.ai/docs/cookbook/administration/usage-accounting
