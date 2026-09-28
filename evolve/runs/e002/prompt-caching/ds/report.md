# 大模型 API 的 Prompt Caching（上下文缓存）全家对比

> 回答一个问题：调用不同厂商模型 API 时，「让重复上下文更便宜/更快」这件事，各家在触发方式、计费、存活时间上差在哪。截至 2026-09-24，覆盖 OpenAI、Anthropic、Gemini、DeepSeek、Kimi、智谱 GLM、通义千问（DashScope）、OpenRouter 8 家，均已用官方一手文档核实。先看第 0 节，再查第 2 节矩阵，第 4 节是踩坑清单。

## 0. 一屏看懂
- **「自动/手动」和「便宜/贵」是两条独立的轴**：触发要不要改代码，与「首次写入（cache miss）是否比不缓存更贵」互不绑定。DeepSeek、Gemini implicit、通义千问隐式是「零改动+零溢价」；OpenAI、Anthropic、Kimi、通义千问 explicit 是「触发方式不同但写入普遍溢价」——即使 OpenAI 的自动缓存，首次写入也要多付 1.25x，且已确认对 implicit/explicit 两种模式都适用[1][2]。
- **OpenAI、DeepSeek 确实自动、不用改代码**：OpenAI「enabled by default for supported OpenAI models」[1]，Chat Completions/Responses/Agents 三个端点均确认支持（Chat Completions 靠 `prompt_cache_options` 参数，但奇怪的是官方 caching 指南页只讲了 Responses/Agents，没提 Chat Completions，属文档覆盖不一致[2]）；DeepSeek「without needing to modify their code」[11]，写入完全不加价[12]。
- **Anthropic 不再是纯手动，但也不是零改动**：2026-02-19 上线「自动缓存」——请求顶层加 1 个 `cache_control` 字段（如 `{"type":"ephemeral"}`），系统自动把断点放在最新可缓存内容上并随对话推进；官方原文明确「仍需显式加这个字段，不是不加任何参数就全自动」[3][24]。传统逐段最多 4 个手动断点依然保留，用于精细控制。这条与旧印象（必须逐段手动）不同，已用官方文档+发布记录双重核实。
- **命中折扣没有统一数字**：多数厂商命中打 0.1x，但 Anthropic 最新两款模型是 0.025x（自 2026-09-01）[4]；通义千问 explicit 0.1x、implicit 反而是 0.2x（更贵)[20]；智谱 GLM 约 0.5x，是本次调研折扣最小的一家[17]。
- **TTL 差异很大，且不是所有厂商都用"固定分钟数"这个模型**：OpenAI 新模型固定 30 分钟[1]；Anthropic/Kimi 都是 5 分钟起、多付钱换 1 小时[3][15]；DeepSeek 用「数小时到数天」，强调缓存放磁盘阵列而非内存[12]；通义千问隐式缓存官方原文是「无固定有效期，按使用频率清理」——不是没查到，是官方设计成没有固定数字[19]；智谱 GLM 官方连这句话都没有，是真的没公开[17]。
- **OpenRouter 官方给了分供应商倍率表，但没有「不加价」的保证**：openrouter.ai 自己的文档列出各上游的缓存计费倍率（如 Anthropic 写入 1.25x），但没有一句「原样转发、不加成」的声明；对比 OpenAI 自家文档给出的直连命中价 0.1x[1]，OpenRouter 官方表里 OpenAI 那一行写的是 0.25x–0.5x（本报告拿两份官方数字自行比较，OpenRouter 未解释差距来自加成还是版本口径）——用 OpenRouter 前建议直接核对它自己那张倍率表，别假设＝直连价[22][25]。

## 1. Taxonomy
轴 A——触发要不要改代码：零改动自动命中（OpenAI 基础层/DeepSeek/Gemini implicit/通义千问隐式/Kimi/智谱）｜至少声明一处（Anthropic 顶层字段/Gemini·通义千问 explicit/OpenAI 可选显式断点）。
轴 B——写入/未命中是否有溢价：无溢价（DeepSeek/Gemini implicit/通义千问隐式/智谱现阶段）｜有溢价（OpenAI/Anthropic/Kimi/Gemini·通义千问 explicit）。
两轴组合解释了大部分计费差异；粒度/断点数、失效条件因差异较小且技术化，放进第 3、4 节而非矩阵列。矩阵维度：触发方式、最小长度、命中价、写入价、TTL、命中字段、适用范围、存储/隔离。

## 2. 对照矩阵（命中价/写入价为相对未缓存输入价的倍数；❓缺口 ∅官方未给 ⚔冲突/不确定 ⚠仅二手）

| 实体 | 触发 | 最小长度 | 命中价 | 写入价 | TTL | 命中字段 | 适用范围 | 存储/隔离 |
|---|---|---|---|---|---|---|---|---|
| OpenAI[1][2] | 默认自动；可选最多3显式断点 | 1024 token（新模型），早期因设置而异 | 0.1x | 1.25x（implicit/explicit均适用） | 30分钟（新模型）；早期5–10分钟~1h或~30分钟~24h | cached_tokens/cache_write_tokens | Responses/Agents/Chat Completions(经prompt_cache_options)均支持 | 独立机器，不跨组织/区域 |
| Anthropic[3][4][24] | 顶层1字段自动放置(2026-02-19起)；或最多4手动断点 | 512~4096按模型 | 0.1x（多数）/0.025x（Fable5.1/Mythos5.1） | 1.25x(5min)/2x(1h) | 5分钟默认/1h可选，命中免费续期 | cache_read/creation_input_tokens | 所有在售模型 | 按workspace隔离，纯内存 |
| Gemini[5-8] | explicit需create()；implicit(2.5+)零改动 | explicit 1024–4096；implicit 2048–4096 | explicit 0.1x(官方$数字)；implicit官方未给%⚔(Vertex二手同为0.1x) | explicit $0.5/M/h(2027起$1)；implicit官方未提⚔ | explicit默认1h可调；implicit官方未给⚔ | usageMetadata.total_cached_tokens | explicit"多数模型"；implicit全2.5+；Interactions仅implicit | 按key/项目隔离 |
| DeepSeek[11-14] | 默认自动 | 64 token | 0.1x | 不加价 | 数小时~数天，闲置自动清 | prompt_cache_hit/miss_tokens | 仅点名flash/v4-pro❓ | 分布式硬盘阵列，逐用户隔离 |
| Kimi[15][16] | 默认自动(前一请求需≥256token，无手动断点概念) | 256 token | 0.1x | $3/M(5min)或$6/M(1h) | 5分钟/1h，到期自动清不可手动清 | cached_tokens(Chat)/cache_read(Messages) | K3/K2.7-code/K2.6 | 官方未披露∅ |
| 智谱GLM[17][18] | 隐式自动 | 建议500+ | ~0.5x | 存储限时免费 | 官方未给∅（非漏查，二次核实仍无） | cached_tokens | GLM-5.3系/5.2/4.5-Flash等 | 官方未披露∅ |
| 通义千问[19-21] | explicit需声明；implicit零改动 | 1024 token | explicit0.1x；implicit0.2x | explicit1.25x；implicit不加价 | explicit5分钟命中重置；implicit按使用频率清理，官方原文即"无固定有效期" | cached_tokens/cache_creation | Qwen系+百炼托管的DeepSeek/Kimi/GLM(≠原厂API,见§3) | 账户级隔离，模型间不共享 |
| OpenRouter[22][25] | 不自建，sticky routing路由同一上游节点 | 网关层∅由上游决定 | 官方给分供应商倍率表，未声明"不加价"⚔ | 同上⚔ | 随上游(如转述Anthropic 5min/1h) | 保留上游字段cached_tokens等 | 官方列出Anthropic/Gemini/OpenAI/DeepSeek/Moonshot/Grok | 网关层∅取决于上游 |

## 3. 变体与适配层
**通义千问 ≠ 托管在它上面的第三方模型自家 API**：百炼把 DeepSeek/Kimi/GLM 列为「支持缓存的模型」，但其参数（最小长度 1024 token、explicit TTL 5 分钟）和 DeepSeek/Kimi 自家文档给出的参数（DeepSeek 64 token、数小时到数天；Kimi 256 token）不一致（本报告对比两边官方数字得出）——可推断百炼对这些模型走的是阿里云自己的缓存实现与计费，不是调用原厂缓存系统，两套规则不要混用。
**OpenRouter 是纯网关，缓存能力≈上游能力+自己的路由和一张倍率表**：它自己只加了 sticky routing（同会话路由到同一上游节点）；它公开的倍率表数字不一定等于上游直连价（见 §0 最后一条），核价要以 OpenRouter 自己的表为准，不要假设和直连一样。
**Gemini explicit/implicit 分裂影响可预测性**：Interactions API 仅支持 implicit；explicit 有官方承诺的$数字节省，implicit 只说"自动让利"，无数字承诺。

## 4. 用户需要知道的坑
- **怎么确认命中**：认响应 usage 里的专门字段，不要靠猜。多数厂商（OpenAI/DeepSeek/Kimi Chat/智谱/通义千问）用 `cached_tokens`；Anthropic/Kimi Messages 用 `cache_read_input_tokens`+`cache_creation_input_tokens`；Gemini 用 `usageMetadata.total_cached_tokens`；DeepSeek 额外给未命中数 `prompt_cache_miss_tokens`。换厂商要重新适配监控字段。
- **什么改动会悄悄打掉缓存**：改 system prompt/instructions、改 tools（定义/顺序/schema）、加减图片或文件、改 tool_choice，是 OpenAI[1]、Anthropic[3] 等共同点名的失效原因。本质是"前缀必须逐字节匹配"，被缓存内容之前或内部的任何改动都会让后面全部重新计算。
- **通过网关（OpenRouter）调用时，命中率还取决于路由是否稳定**：sticky routing 把同一会话路由到同一上游节点，节点切换或高并发下命中会下降；同时别忘了核对网关自己的那张倍率表是否比直连贵。
- **自动缓存更依赖你把请求"排整齐"**：不变内容（system prompt、工具定义、长文档）放前面、易变内容（当轮用户输入）放后面；自动触发的厂商没有手动断点可补救，排列不好命中率直接受影响。OpenAI 官方还提到超过15 req/min 可能触发溢出路由到无缓存的机器[1]，高并发下命中率通常低于单机测试。
- **折扣力度和存活时间是两件独立的事**：DeepSeek 折扣（0.1x）与 OpenAI 相同，但 TTL 是"数小时到数天"而非分钟级；智谱折扣最小（0.5x）但 TTL 完全未公开——不能用其一去推断另一个。

## 5. 未决与置信度
- Gemini implicit caching 的折扣%、存储费、TTL 数值，Gemini API 官方文档二次核实仍未给数字，仅 Vertex AI（另一产品线，二手）给出 90%/免费/≤24h，是否适用于 Gemini API 不确定。
- 智谱 GLM 的 TTL 精确数值、Kimi/智谱的缓存存储介质，二次核实后确认官方未披露，非上一轮漏查。
- OpenRouter 的倍率表是否含加成：官方文档只给数字不给承诺，部分数字比厂商直连价更贵，可能是加成也可能是版本/口径差异，官方未解释，建议实测确认。
- Anthropic 自动缓存若完全不加 `cache_control` 字段，是否有任何缓存效果，官方文档未说明（只确认了"加了会怎样"）。
- DeepSeek 官方文档仅点名 deepseek-flash、deepseek-v4-pro 两款模型支持缓存，其余模型是否支持未列出。

## 来源
[1] OpenAI Prompt Caching guide — https://developers.openai.com/docs/guides/prompt-caching
[2] OpenAI Chat Completions API reference — https://developers.openai.com/api/docs/api-reference/chat/create
[3] Anthropic Prompt caching docs — https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
[4] Anthropic token-saving updates — https://www.anthropic.com/news/token-saving-updates
[5] Gemini context caching guide — https://ai.google.dev/gemini-api/docs/caching
[6] Gemini generate-content caching — https://ai.google.dev/gemini-api/docs/generate-content/caching
[7] Gemini API pricing — https://ai.google.dev/gemini-api/docs/pricing
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
[24] Anthropic SDK Python commit (automatic caching, 2026-02-19) — https://github.com/anthropics/anthropic-sdk-python/commits/a940123
[25] OpenRouter provider cache pricing table — https://openrouter.ai/docs/features/prompt-caching
