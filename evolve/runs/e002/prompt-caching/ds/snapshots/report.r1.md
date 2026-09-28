# 大模型 API 的 Prompt Caching（上下文缓存）全家对比

> 回答一个问题：调用不同厂商模型 API 时，「让重复上下文更便宜/更快」这件事，各家在触发方式、计费、存活时间上差在哪。截至 2026-09-24，覆盖 OpenAI、Anthropic、Gemini、DeepSeek、Kimi、智谱 GLM、通义千问（DashScope）、OpenRouter 8 家。先看第 0 节，再查第 2 节矩阵，第 4 节是踩坑清单。

## 0. 一屏看懂
- **「自动/手动」和「便宜/贵」是两条独立的轴**：触发要不要改代码，与「首次写入（cache miss）是否比不缓存更贵」互不绑定。DeepSeek、Gemini implicit、通义千问隐式缓存是「零改动+零溢价」；OpenAI、Anthropic、Kimi、通义千问 explicit 是「触发方式不同但写入普遍溢价」——即使 OpenAI 的自动缓存，首次写入也要多付 1.25x[1]。
- **OpenAI、DeepSeek 确实自动、不用改代码**：OpenAI「enabled by default for supported OpenAI models」[1]，DeepSeek「without needing to modify their code」[11]。但 OpenAI 命中打 9 折（0.1x）的同时首次写入要多付 1.25x[1]；DeepSeek 写入完全不加价[12]。
- **Anthropic 不再是纯手动**：官方新增自动缓存——请求顶层加 1 个 `cache_control` 字段，系统自动把断点放在最新可缓存内容上并随对话推进；传统的逐段手动断点（最多 4 个）仍保留供精细控制[3]。即「至少加一个字段」，比 OpenAI/DeepSeek 多一步，但远比「每段手动」轻松，且此变化未见于旧版印象，本节结论建议以 R2 复核结果为准（见第 5 节）。
- **命中折扣没有统一数字**：多数厂商命中打 0.1x，但 Anthropic 最新两款模型是 0.025x（自 2026-09-01）[4]；通义千问 explicit 0.1x、implicit 反而是 0.2x（更贵)[20]；智谱 GLM 约 0.5x，是本次调研里折扣最小的一家[17]。
- **TTL 差异很大**：OpenAI 新模型固定 30 分钟[1]；Anthropic/Kimi 都是 5 分钟起、多付钱换 1 小时[3][15]；DeepSeek 用「数小时到数天」的模糊区间，强调缓存放磁盘阵列而非内存[12]；智谱 GLM 官方未给数字[17]。
- **通义千问同时有两条路径、价格结构相反**：explicit 多付 25% 写入费换 10% 读取价；implicit 不收写入费但读取价是 20%——本质是「多一道手续换更大折扣」的取舍[20]。
- **OpenRouter 不产生自己的缓存，靠 sticky routing 路由到同一上游节点维持命中，并原样转发上游的缓存字段**[22][23]。

## 1. Taxonomy
轴 A——触发要不要改代码：零改动自动命中（OpenAI 基础层/DeepSeek/Gemini implicit/通义千问隐式/Kimi/智谱）｜至少声明一处（Anthropic 顶层字段/Gemini·通义千问 explicit/OpenAI 可选显式断点）。
轴 B——写入/未命中是否有溢价：无溢价（DeepSeek/Gemini implicit/通义千问隐式/智谱现阶段）｜有溢价（OpenAI/Anthropic/Kimi/Gemini·通义千问 explicit）。
两轴组合解释了大部分计费差异；粒度/断点数、失效条件因差异较小且技术化，放进第 3、4 节而非矩阵列。矩阵维度：触发方式、最小长度、命中价、写入价、TTL、命中字段、适用范围、存储/隔离。

## 2. 对照矩阵（命中价/写入价为相对未缓存输入价的倍数；❓缺口 ∅官方未给 ⚔平台间冲突 ⚠仅二手）

| 实体 | 触发 | 最小长度 | 命中价 | 写入价 | TTL | 命中字段 | 适用范围 | 存储/隔离 |
|---|---|---|---|---|---|---|---|---|
| OpenAI[1][2] | 默认自动；可选最多3显式断点 | 1024 token（新模型），早期因设置而异 | 0.1x | 1.25x | 30分钟（新模型）；早期5–10分钟~1h或~30分钟~24h | cached_tokens/cache_write_tokens | Responses/Agents确认；Chat Completions未明确❓ | 独立机器，不跨组织/区域 |
| Anthropic[3][4] | 顶层1字段自动放置；或最多4手动断点 | 512~4096按模型 | 0.1x（多数）/0.025x（Fable5.1/Mythos5.1） | 1.25x(5min)/2x(1h) | 5分钟默认/1h可选，命中免费续期 | cache_read/creation_input_tokens | 所有在售模型 | 按workspace隔离，纯内存 |
| Gemini[5-8] | explicit需create()；implicit(2.5+)零改动 | explicit 1024–4096；implicit 2048–4096 | explicit 0.1x(官方$数字)；implicit仅"让利"无%⚔ | explicit $0.5/M/h(2027起$1)；implicit官方未提⚔ | explicit默认1h可调；implicit官方未给⚔ | usageMetadata.total_cached_tokens | explicit"多数模型"；implicit全2.5+；Interactions仅implicit | 按key/项目隔离 |
| DeepSeek[11-14] | 默认自动 | 64 token | 0.1x | 不加价 | 数小时~数天，闲置自动清 | prompt_cache_hit/miss_tokens | 仅点名flash/v4-pro❓ | 分布式硬盘阵列，逐用户隔离 |
| Kimi[15][16] | 默认自动(前一请求需>256token) | 256 token | 0.1x | $3/M(5min)或$6/M(1h) | 5分钟/1h，到期自动清不可手动清 | cached_tokens(Chat)/cache_read(Messages) | K3/K2.7-code/K2.6 | 官方未披露∅ |
| 智谱GLM[17][18] | 隐式自动 | 建议500+ | ~0.5x | 存储限时免费 | 官方未给∅ | cached_tokens | GLM-5.3系/5.2/4.5-Flash等 | 官方未披露∅ |
| 通义千问[19-21] | explicit需声明；implicit零改动 | 1024 token | explicit0.1x；implicit0.2x | explicit1.25x；implicit不加价 | explicit5分钟命中重置；implicit"定期清理"无数字❓ | cached_tokens/cache_creation | Qwen系+百炼托管的DeepSeek/Kimi/GLM(≠原厂API,见§3) | 账户级隔离，模型间不共享 |
| OpenRouter[22][23] | 不自建，sticky routing路由同一上游节点 | 网关层∅由上游决定 | 二手:不加价转发⚠ | 二手:不加价转发⚠ | 随上游(如转述Anthropic 5min/1h) | 保留上游字段cached_tokens等 | 官方列出Anthropic/Gemini/OpenAI/DeepSeek | 网关层∅取决于上游 |

## 3. 变体与适配层
**通义千问 ≠ 托管在它上面的第三方模型自家 API**：百炼把 DeepSeek/Kimi/GLM 列为「支持缓存的模型」，走的是阿里云自己的实现与计费（矩阵里的"通义千问"行），与这些厂商自家 API 的缓存行为是两套规则，不要混用。
**OpenRouter 是纯网关**：缓存能力=上游能力，它自己只加了 sticky routing（同会话路由到同一上游节点）和字段转发；要判断某模型的缓存细节，看上游文档而非 OpenRouter 定价页。
**Gemini explicit/implicit 分裂影响可预测性**：Interactions API 仅支持 implicit；explicit 有官方承诺的$数字节省，implicit 只说"自动让利"，无数字承诺。

## 4. 用户需要知道的坑
- **怎么确认命中**：认响应 usage 里的专门字段，不要靠猜。多数厂商（OpenAI/DeepSeek/Kimi Chat/智谱/通义千问）用 `cached_tokens`；Anthropic/Kimi Messages 用 `cache_read_input_tokens`+`cache_creation_input_tokens`；Gemini 用 `usageMetadata.total_cached_tokens`；DeepSeek 额外给未命中数 `prompt_cache_miss_tokens`。换厂商要重新适配监控字段。
- **什么改动会悄悄打掉缓存**：改 system prompt/instructions、改 tools（定义/顺序/schema）、加减图片或文件、改 tool_choice，是 OpenAI[1]、Anthropic[3] 等共同点名的失效原因。本质是"前缀必须逐字节匹配"，被缓存内容之前或内部的任何改动都会让后面全部重新计算。
- **自动缓存更依赖你把请求"排整齐"**：不变内容（system prompt、工具定义、长文档）放前面、易变内容（当轮用户输入）放后面，是共同的最佳实践；自动触发的厂商没有手动断点可补救，排列不好命中率直接受影响。
- **基础设施会打断命中率**：OpenRouter 命中依赖 sticky routing；OpenAI 官方提到超过15 req/min 可能触发溢出路由到无缓存的机器[1]。高并发下命中率通常低于单机测试。
- **折扣力度和存活时间是两件独立的事**：DeepSeek 折扣（0.1x）与 OpenAI 相同，但 TTL 是"数小时到数天"而非分钟级；智谱折扣最小（0.5x）但 TTL 完全未公开——不能用其一去推断另一个。

## 5. 未决与置信度
- Anthropic"自动缓存"的确切上线时间官方未直接给出，需按最新文档措辞为准，不要依赖旧的"必须手动"印象（本节为 R1 发现，R2 已派工人复核，结论见更新版本）。
- Gemini implicit caching 的折扣%、存储费、TTL 数值，Gemini API 官方文档均未给数字，仅 Vertex AI（另一产品线，二手）给出 90%/免费/≤24h，是否适用于 Gemini API 不确定。
- OpenAI Chat Completions 是否支持 prompt caching，官方指南只提 Responses/Agents API，未直接确认或排除。
- 通义千问 implicit、智谱 GLM 的 TTL 精确数值官方未给。
- Kimi、智谱 GLM 的缓存存储介质官方未披露。
- OpenRouter"不加价、原样转发"仅有第三方来源佐证，未找到官方直接声明。

## 来源
[1] OpenAI Prompt Caching guide — https://developers.openai.com/docs/guides/prompt-caching
[2] OpenAI Chat Completions API reference — https://developers.openai.com/api/docs/api-reference/chat/create
[3] Anthropic Prompt caching docs — https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
[4] Anthropic token-saving updates — https://www.anthropic.com/news/token-saving-updates
[5] Gemini context caching guide — https://ai.google.dev/gemini-api/docs/caching
[6] Gemini generate-content caching — https://ai.google.dev/gemini-api/docs/generate-content/caching
[7] Gemini API pricing — https://ai.google.dev/gemini-api/docs/pricing.md.txt
[8] Gemini caching API reference — https://ai.google.dev/api/caching
[9] Gemini Interactions API caching — https://ai.google.dev/gemini-api/docs/interactions/caching
[10] Vertex AI context cache overview（二手对照） — https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview
[11] DeepSeek Context Caching guide — https://api-docs.deepseek.com/guides/kv_cache/
[12] DeepSeek News: Context Caching on Disk — https://api-docs.deepseek.com/news/news0802/
[13] DeepSeek pricing — https://api-docs.deepseek.com/quick_start/pricing/
[14] DeepSeek create chat completion API — https://api-docs.deepseek.com/api/create-chat-completion/
[15] Kimi context caching guide — https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api
[16] Kimi pricing — https://platform.kimi.ai/docs/pricing/chat
[17] 智谱 GLM 缓存能力文档 — https://docs.bigmodel.cn/cn/guide/capabilities/cache
[18] 智谱 GLM 定价 — https://docs.bigmodel.cn/cn/guide/start/pricing
[19] 阿里云百炼 Context Cache — https://help.aliyun.com/zh/model-studio/context-cache
[20] 阿里云百炼模型定价 — https://help.aliyun.com/zh/model-studio/model-pricing
[21] 阿里云百炼 Qwen API (DashScope) — https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope
[22] OpenRouter prompt caching best practices — https://openrouter.ai/docs/guides/best-practices/prompt-caching
[23] OpenRouter blog: sticky routing — https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/
