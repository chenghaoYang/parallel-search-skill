# 大模型 API Prompt Caching 全景对比

> 回答：谁自动缓存/谁要手动声明、命中后怎么计费、能活多久、怎么确认命中、什么操作会打掉缓存。截至 2026-09，均为官方文档一手信息。

## 0. 一屏看懂

1. **传言已过时**：Anthropic 2026-02-19 上线了自动缓存（顶层 `cache_control` 自动套用到最后可缓存块），手动断点仍可用于精细控制，二者可并存、合计每请求≤4个断点[4][6]。反而是 OpenAI 在 GPT-5.6+ 新增了「可选显式」`prompt_cache_breakpoint`，早期模型仍纯隐式[1]。
2. **现状是「自动兜底+手动可选」双轨制占多数**：OpenAI(5.6+)、Anthropic、Gemini、通义千问都双轨；DeepSeek、智谱纯自动无手动接口；**Kimi 反而是纯手动**，必须传参才缓存[15]；OpenRouter 自己不缓存，只透传上游语义。
3. **命中折扣收敛在「1折」（省90%）**：OpenAI/Anthropic(多数模型)/Gemini/DeepSeek/Kimi/通义千问(显式) 都是 0.1x[1][4][7][12][15][17]；智谱是例外，官方绝对价格换算约 0.25x（省75%，非坊间说的五折）[16]；通义千问隐式命中只打 2 折[17]。
4. **真正差异在写入怎么算**：DeepSeek/Kimi 建缓存不加价[12][15]；OpenAI/Anthropic/通义千问(显式) 写入加价 1.25x（Anthropic 选 1 小时 TTL 还要 2x）[1][5][17]；Gemini 显式缓存反而按小时收独立存储费，2027 年起还要涨价[10]。
5. **TTL 从 5 分钟到数天不等**：Anthropic/通义千问(显式) 默认 5 分钟；OpenAI 默认≥30分钟、2026-05后非ZDR组织默认24小时；Gemini 显式默认1小时；DeepSeek 硬盘缓存能放数小时到数天[1][4][7][12]。
6. **命中确认字段各家路径不同**，都在 usage/响应体里，没有统一标准，见第2节表。
7. **网关不能替你抹平差异**：OpenRouter 路由到 Anthropic/通义千问的请求仍要自己加 `cache_control`，路由到 OpenAI 的仍要自己判断用不用 `prompt_cache_breakpoint`[19]。

## 1. Taxonomy

分类轴：**谁负责触发、要不要改代码**。
- **双轨**（自动兜底+手动/显式可选）：OpenAI(仅5.6+)、Anthropic、Gemini、通义千问——目前主流。
- **纯自动**（无手动接口）：DeepSeek、智谱GLM。
- **纯手动**（无自动路径）：Kimi。
- **透传**（自身无缓存语义）：OpenRouter。

维度：D1触发方式｜D2最小门槛｜D4命中折扣｜D5写入/存储成本｜D6 TTL｜D7命中确认字段｜D10显式资源对象。失效条件(D8)见第4节，避免重复。

## 2. 对照矩阵

| 实体 | 分类 | 触发方式 | 最小门槛 |
|---|---|---|---|
| OpenAI | 双轨 | 隐式默认；GPT-5.6+可选`prompt_cache_breakpoint`显式标记[1] | 1024 tok（GPT-5.6+）[1] |
| Anthropic | 双轨 | 顶层`cache_control`自动套用末尾块；也可手动在content block打断点，合计≤4个[4] | 512/1024/2048/4096 tok，按模型分档[4] |
| Gemini | 双轨 | 隐式：2.5+默认开；显式：generateContent创建`cachedContents`再引用[7][8] | 2048(2.5)/4096(3.x) tok[7] |
| DeepSeek | 纯自动 | 完全隐式，前缀匹配，无参数[12] | 64 tok[13] |
| Kimi | 纯手动 | 须传`prompt_cache_options`(Chat/Responses)或`cache_control`(Messages)[15] | 未注明 |
| 智谱GLM | 纯自动 | 隐式，≥512 tok公共前缀自动触发[16] | 512 tok[16] |
| 通义千问 | 双轨 | 隐式默认开；显式须传`cache_control:{type:ephemeral}`[17] | 1024 tok，两模式相同[17] |
| OpenRouter | 透传 | 跟随上游：Anthropic/通义千问仍需显式`cache_control`，OpenAI仍需`prompt_cache_breakpoint`，其余自动[19] | 取决于上游 |

| 实体 | 命中折扣(D4) | 写入/存储成本(D5) | 默认/可选TTL(D6) | 命中确认字段(D7) |
|---|---|---|---|---|
| OpenAI | 0.1x[1] | 1.25x标准输入价[1] | ≥30分钟；2026-05后非ZDR组织默认24h[1][2] | `usage.prompt_tokens_details.cached_tokens`/`cache_write_tokens`[3] |
| Anthropic | 0.1x（多数）/0.05x(Opus5.5)/0.025x(Fable5.1/Mythos5.1)[5] | 5m TTL:1.25x；1h TTL:2x[5] | 5分钟默认，1小时可选(`cache_control.ttl`)[4] | `usage.cache_read_input_tokens`/`cache_creation_input_tokens`[4] |
| Gemini | 0.1x，隐式显式一致[10] | 显式=标准输入价+$0.5~1.0/M token/小时存储费(2027起涨)[10] | 显式默认1小时(可设`ttl`/`expireTime`)；隐式∅未文档化[9] | 隐式`usage.total_cached_tokens`；显式`usageMetadata.totalTokenCount`[8][11] |
| DeepSeek | 0.1x（$0.014 vs $0.14/M）[13] | 未见加价，按命中计费[13] | 数小时至数天，自动清理未用条目[13] | `prompt_cache_hit_tokens`/`prompt_cache_miss_tokens`[14] |
| Kimi | 0.1x（$0.30 vs $3.00/M，kimi-k3）[15] | 按标准价写入，2次命中回本[15] | 5分钟或1小时二选一[15] | `usage.prompt_tokens_details.cached_tokens`（二手）[15] |
| 智谱GLM | ≈0.25x（2元 vs 8元/M，GLM-5.3）[16] | 无独立写入价；另计存储费(元/M/小时)[16] | ∅未文档化 | `usage.prompt_tokens_details.cached_tokens`[16] |
| 通义千问 | 隐式0.2x／显式0.1x[17] | 显式创建=1.25x标准价；隐式未注明[17] | 显式5分钟，命中即重置；隐式∅未文档化 | `cached_tokens`(usage)[17][18] |
| OpenRouter | 0.1x–0.5x，取决上游[20] | 取决上游 | 取决上游 | `usage.prompt_tokens_details.cached_tokens`[19] |

## 3. 变体与适配层

| 变体 | 与原生差异 |
|---|---|
| Azure OpenAI（vs OpenAI） | 无「扩展保留」，纯内存缓存5-10分钟自动清、最长1小时；断点仅Standard PAYG支持，PTU-M不支持；同前缀+`prompt_cache_key`超约15次/分钟可能miss[21] |
| AWS Bedrock·Claude（vs Anthropic） | 新增Implicit(全自动)与Explicit(checkpoint)两种；"简化缓存管理"自动回溯约20个content block，门槛与原生同档[22] |
| AWS Bedrock·GPT-5.6（vs OpenAI） | 参数与计价（写1.25x/读90%off）与原生一致[22] |
| Google Vertex AI（vs AI Studio） | 仅有线索指向"隐式默认启用"，未核实，见第5节 |

## 4. 用户需要知道的坑

1. **改一个字就从头计价**：前缀里任何变化——system prompt、工具定义顺序/描述、多模态内容增删、`tool_choice`/`reasoning.effort`/`verbosity`等采样参数——都会让该断点之后全部miss；Anthropic 还有 tools→system→messages 层级失效，上层改动连累下层[4]。→ 稳定内容（system/工具/参考资料）放最前，易变内容（当轮用户输入）放最后[4][15][19]。
2. **"看不出像改prompt"的参数也会打掉缓存**：OpenAI 改 `text.format`(Structured Outputs)、`reasoning.effort`、`text.verbosity` 会重写隐藏前缀指令，导致miss[1]。
3. **断点数有硬上限**：Anthropic、通义千问显式模式都限每请求≤4个缓存标记，超出报错或不生效[4][17]。
4. **折扣价不等于总更便宜**：命中率低时，写入加价（如Anthropic 1h TTL的2x）可能不划算，需按"命中≥N次才回本"估算[5][15]。
5. **高并发会把自己缓存挤掉**：Azure明确写同前缀+`prompt_cache_key`超约15次/分钟可能miss（多机路由）；经网关(OpenRouter)要用`session_id`做粘性路由，否则可能转发到无缓存节点[21][20]。
6. **"自动"≠免费预热**：DeepSeek/智谱/Kimi等命中依赖后续确实发相同前缀请求；智谱即使自动触发也会额外按小时收独立存储费[16]。
7. **同模型在不同云上行为可能不同**：legacy Bedrock上的旧版Claude(Opus 4.6及更早)不支持自动缓存，只能用显式断点；Azure的PTU-M部署完全不支持缓存断点[4][21]。

## 5. 未决与置信度

- Gemini/智谱/通义千问的**隐式缓存TTL**官方均未写明（仅显式路径给了数字），标∅，不确定该维度会不会随负载变化。
- Kimi 的命中字段名来自第三方GitHub提案文档，非Kimi官方页面直接确认，标（二手）。
- Google Vertex AI 的Gemini缓存参数是否与ai.google.dev完全一致，仅有线索、未核实。
- Anthropic 是否仍需要beta header才能用prompt caching：现有笔记未见明确一手引用，只确认"所有active模型默认支持"。
- DeepSeek 推理模型（如R1系列）是否支持缓存、智谱GLM隐式缓存的确切失效规则：官方文档未提及。

## 来源
[1] OpenAI Prompt Caching指南 — https://developers.openai.com/api/docs/guides/prompt-caching
[2] OpenAI API Changelog — https://developers.openai.com/api/docs/changelog
[3] OpenAI Chat API Reference — https://developers.openai.com/docs/api-reference/chat
[4] Anthropic Prompt Caching指南 — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[5] Anthropic Pricing — https://platform.claude.com/docs/en/about-claude/pricing
[6] Anthropic Release Notes — https://platform.claude.com/docs/en/release-notes/overview
[7] Gemini Caching指南 — https://ai.google.dev/gemini-api/docs/caching
[8] Gemini Caching API Reference — https://ai.google.dev/api/caching
[9] Gemini Interactions Caching — https://ai.google.dev/gemini-api/docs/interactions/caching
[10] Gemini Pricing — https://ai.google.dev/gemini-api/docs/pricing
[11] Gemini Generate-content Caching — https://ai.google.dev/gemini-api/docs/generate-content/caching
[12] DeepSeek KV Cache指南 — https://api-docs.deepseek.com/guides/kv_cache/
[13] DeepSeek发布公告(0802) — https://api-docs.deepseek.com/news/news0802/
[14] DeepSeek Chat Completion API — https://api-docs.deepseek.com/api/create-chat-completion/
[15] Kimi Context Caching指南 — https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api
[16] 智谱 Cache文档 — https://docs.bigmodel.cn/cn/guide/capabilities/cache
[17] 阿里云百炼 Context Cache(英) — https://www.alibabacloud.com/help/en/model-studio/context-cache
[18] 阿里云百炼 Context Cache(中) — https://www.alibabacloud.com/help/zh/model-studio/context-cache
[19] OpenRouter Prompt Caching最佳实践 — https://openrouter.ai/docs/guides/best-practices/prompt-caching
[20] OpenRouter Sticky Routing — https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/
[21] Azure OpenAI Prompt Caching指南 — https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching
[22] AWS Bedrock Prompt Caching指南 — https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
