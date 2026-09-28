# 大模型 API 的 Prompt Caching（上下文缓存）横向对比

> 截至 2026-09-24，基于各家官方文档。先看「一屏看懂」建立结论，细节查第 2～4 节的表，存疑/未公开的地方都在第 5 节。

## 0. 一屏看懂

1. **"OpenAI/DeepSeek 自动、Anthropic 必须手动"——现在依然成立。** Anthropic 是四大里唯一一个不加参数就完全不缓存的：2026-02-19 新增的"自动缓存"只是省去手动挑最多 4 个断点位置，本质仍要在请求里加 1 个 `cache_control` 字段[2]。OpenAI 默认 `mode: implicit` 零参数自动生效，GPT-5.6+ 起多了个可选 explicit 模式，但那是"可选"不是"改了默认值"[1]。
2. Gemini、通义千问不是"自动 vs 手动"二选一：两家都默认自动（implicit，无法关闭），**同时**还各自提供一个要手动创建的独立缓存资源（explicit：Gemini 叫 cachedContent、Qwen 叫 explicit cache），换取更长/更确定的可用性[3][8]。
3. 命中折扣普遍在 90% 左右（降到原价 0.1x），但非统一：Anthropic 按模型分档给到 0.05x～0.025x（更便宜）[2]；智谱官方指南写"50%"，定价表实测是 71～75% off，两处口径不一致，本文按定价表算[7]。
4. 缓存能活多久差异很大：Anthropic/Kimi/Qwen(explicit) 是 5 分钟量级（可选更贵的 1 小时档）；OpenAI(GPT-5.6+) 30 分钟；Gemini(implicit)/DeepSeek 是小时到 24 小时量级自动清；Gemini(explicit) 默认 1 小时但可调；智谱官方没写 TTL[2][3][5][6][7][8]。
5. 国内三家现在都以自动隐式为主。Kimi 2024 年公开过要手动建 `cache_id` 的显式接口，2026 现行文档已看不到，大概率被自动前缀缓存取代，但官方没公布切换时间点[6]。
6. OpenRouter 不是第五种缓存机制，是转发：连 OpenAI/DeepSeek/Groq 自动生效，连 Anthropic/通义千问仍要自己按对方格式加 `cache_control`——网关不会替你补上，它统一的只是 usage 里报告命中的字段名[9]。
7. 确认命中都在 response 的 usage/usageMetadata 里，但字段名各不相同，见 2.2 表。
8. 缓存失效头号原因是"前缀不是逐字节相同"：改 system prompt/tools 定义或顺序、加减图片、改 reasoning/thinking 相关参数，几乎每家都会失效，见第 4 节。

## 1. Taxonomy

**主轴：不加任何缓存参数发一个普通请求，默认会不会缓存？**

| 家族 | 成员 | 特征 |
|---|---|---|
| A 自动默认 | OpenAI、DeepSeek、Kimi、智谱、Gemini(implicit)、通义千问(implicit) | 零配置命中前缀即打折 |
| B 声明式默认 | Anthropic | 不加 `cache_control` 完全不缓存，四大里唯一 |
| C 网关透传 | OpenRouter | 非独立机制，行为=转发到的底层是 A 还是 B |

**副轴（叠加在 A 上）：是否额外提供一个要手动创建的显式/预留缓存？** 有：Gemini（cachedContent 独立资源，按小时收存储费）、通义千问（explicit cache，创建多付 25%）、OpenAI（GPT-5.6+ 可选 explicit 断点标记，不产生独立付费资源，性质更轻）。无或已撤：DeepSeek、智谱；Kimi 历史上有过。

**维度**：trigger(自动/手动)、min_len(最小触发长度)、discount(命中折扣/写入溢价)、ttl(存活时长)、storage(存储介质/费用)、confirm(命中字段)、invalidate(失效条件)、scope(隔离范围)、api(是否有独立管理接口)。

## 2. 对照矩阵

### 2.1 触发与计费
| | 触发方式 | 最小长度 | 命中价格 | 写入/创建溢价 |
|---|---|---|---|---|
| OpenAI[1] | 自动(implicit默认)，GPT-5.6+可选explicit | 1024 tok | 0.1x（90%off） | 1.25x（GPT-5.6+） |
| Anthropic[2] | **必须加`cache_control`** | 512/1024/4096（按模型分档） | 0.1x(Sonnet 5)/0.05x(Opus 5.5)/0.025x(Fable 5.1,Mythos 5.1) | 1.25x(5m)/2x(1h) |
| Gemini[3][4] | implicit自动+explicit手动资源 | 2048或4096（按模型） | 两者均~90%off | 无写入费；explicit按小时收存储费 |
| DeepSeek[5] | 全自动 | 64 tok | 现价分档，命中比未命中低95~98% | 无 |
| Kimi[6] | 全自动 | 256 tok(K3) | 0.1x（90%off） | 两档TTL写入价相同 |
| 智谱GLM[7] | 隐式自动 | 建议500+ tok | 定价表实为0.25x(GLM-5.3)~0.29x(GLM-5.3-Flash)，指南写"50%"对不上 | 未公开 |
| 通义千问[8] | implicit自动(不可关)+explicit可选(互斥) | explicit≥1024 | implicit 0.2x/explicit 0.1x | explicit创建1.25x；implicit免费 |
| OpenRouter[9] | 透传底层 | 取决于底层 | 透传：0.1x(DeepSeek/Anthropic/Qwen)~0.5x(Groq) | 透传：Anthropic/Qwen有，OpenAI/Gemini/Grok无 |

### 2.2 TTL 与确认命中
| | 默认TTL | 可选更长档 | response 里的命中字段 |
|---|---|---|---|
| OpenAI | 复用窗口30分钟(GPT-5.6+) | 另有独立的`prompt_cache_retention`，跟是否复用无关，2026-05-29起未开ZDR组织默认24h | `usage.input_tokens_details.cached_tokens` |
| Anthropic | 5分钟，命中即刷新 | `"ttl":"1h"` | `usage.cache_read_input_tokens`/`cache_creation_input_tokens` |
| Gemini | implicit 24h自动清；explicit 1h | explicit可设`ttl`/`expireTime` | `usageMetadata.cachedContentTokenCount` |
| DeepSeek | 官方仅说"数小时到数天"，best-effort不保证 | 无 | `usage.prompt_cache_hit_tokens`/`prompt_cache_miss_tokens` |
| Kimi | 5分钟 | 1小时档 | usage按cached/write/uncached分字段报告 |
| 智谱GLM | ∅ 官方未写 | ∅ | `usage.prompt_tokens_details.cached_tokens` |
| 通义千问 | explicit 5分钟(命中刷新)；implicit无固定期 | 无 | `usage.prompt_tokens_details.cached_tokens`/`cache_creation_input_tokens` |
| OpenRouter | 官方称"最低30分钟"，实际取决于底层 | 取决于底层 | 统一为`cached_tokens`/`cache_write_tokens`/`cache_discount` |

## 3. 变体与适配层

**Gemini / 通义千问的双模式**：implicit 默认打底、不可关；explicit 要单独创建资源/加参数，换更确定的可用性和可自定义 TTL，但要多付成本（Gemini 按小时付存储费如 $0.50~1.00/M tok/h[3]；Qwen 创建多付 25%[8]）。Qwen 里 explicit 与 implicit 互斥，单次请求只能选一种[8]。

**OpenRouter 的透传边界**：它不生成新缓存策略，只做两件自己的事——① 统一 usage 字段命名，不管底层是谁都能在同一套字段里看到命中/写入 token；② 用 `session_id`（≤256字符）做 provider 粘性路由，因为两次请求若被路由到底层厂商的不同实例，缓存就不命中——这是网关特有的失效原因，模型厂商自己的 API 不会有[9][10]。OpenRouter 另有一个不相关的 "Response Caching"（`X-OpenRouter-Cache` header），是应用层整段响应缓存，跟 prompt caching 是两回事，别混淆[9]。

**OpenAI 的 explicit 模式**：和 Gemini/Qwen 不同，它不创建独立付费资源，只是把断点标记方式从"系统自动放在最后一条可缓存消息末尾"换成自己指定，默认仍是 implicit[1]。

## 4. 用户需要知道的坑

| 现象 | 原因 | 处理 |
|---|---|---|
| 换了 tools 定义/顺序，缓存全灭 | 几乎所有家都要求前缀逐字节相同；tools/system 通常排最前，改动连带后面全部失效（Anthropic 明确是`tools→system→messages`层级失效）[2] | 稳定内容（tools/system）放最前，易变内容放尾部 |
| OpenAI 上编辑了最后一条消息内容，没命中 | 官方区分"扩展/编辑已有消息"和"追加新消息"，前者不能复用[1] | 用追加新消息代替重写旧消息 |
| Kimi 改 tool_choice 没事，改 reasoning_effort 就失效 | 各家 invalidate 清单不完全一样[6] | 按各家清单逐项核对，别假设"参数变了一定全灭"或"一定没事" |
| 通过 OpenRouter 连续请求，缓存没命中 | 两次请求被路由到底层不同实例/账号[10] | 加 `session_id` 做粘性路由 |
| 通过 OpenRouter 连 Claude，以为和连 OpenAI 一样不用改代码 | OpenRouter 只转发，Anthropic/通义千问路径仍要求调用方自己加 `cache_control`[9] | 按目标模型原生要求写请求，别假设网关会替你补 |
| Qwen 加了 cache_control 但没命中 | content 必须是数组格式，字符串格式不支持缓存标记；前缀匹配最多回看 20 个 content block[8] | 检查 content 格式和 block 数 |
| 短对话怎么都不命中缓存 | 每家都有最小前缀长度门槛（64～4096 tok 不等，见 2.1 表） | 前缀不够长就别指望命中，先看自己模型的 min_len |
| 智谱缓存折扣算出来比文档说的"50%"划算很多 | 官方指南和定价表口径不一致[7] | 按定价表估算成本，别按指南文字估算 |

## 5. 未决与置信度

- **智谱**：ttl/invalidate/scope 三格官方文档（缓存指南+定价页）均未提及，已两轮定向查证，判定为未写而非漏查；discount 指南（50%）与定价表（71~75%off）口径不一致，本文采用定价表数字。
- **Kimi**：2024 年显式 `cache_id` 接口在 2026 现行文档中已消失，推断已被自动前缀缓存取代，但没找到官方 changelog 给出切换日期；storage、scope 两格官方未公开。
- **OpenRouter**：官方称缓存"最低 30 分钟"TTL，与 Anthropic 自己公布的 5 分钟默认 TTL 对不太上，可能是网关层面的粗略说法，未进一步核实原因。
- **Anthropic / Gemini / 通义千问的 API-key 级隔离范围**：三家官方文档都只说清楚了 organization/project 级隔离，未明确 API key 粒度能否共享，本文未展开。
- **DeepSeek TTL**：官方原话就是"数小时到数天"（best-effort，不保证），没有具体数字，是官方说法本身模糊，非调研遗漏。
- 本文基于 2026-09-24 公开文档，模型代号、价格、参数名可能随版本继续变化，使用前建议对照来源链接复查。

## 来源
[1] OpenAI – Prompt Caching guide — https://developers.openai.com/api/docs/guides/prompt-caching
[2] Anthropic – Prompt caching guide — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[3] Google Gemini API – Context caching / pricing — https://ai.google.dev/gemini-api/docs/caching ・ https://ai.google.dev/gemini-api/docs/pricing
[4] Google Vertex AI blog（交叉验证用，非 Gemini API 官方定价页）— https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching
[5] DeepSeek – KV Cache 硬盘缓存指南 — https://api-docs.deepseek.com/guides/kv_cache/
[6] Moonshot Kimi – Context Caching 指南 — https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api
[7] 智谱 GLM – 上下文缓存指南 / 定价 — https://docs.bigmodel.cn/cn/guide/capabilities/cache ・ https://docs.bigmodel.cn/cn/guide/start/pricing
[8] 阿里云百炼 – Context Cache — https://help.aliyun.com/zh/model-studio/context-cache
[9] OpenRouter – Prompt caching best practices — https://openrouter.ai/docs/guides/best-practices/prompt-caching
[10] OpenRouter blog – Prompt caching & sticky routing — https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/
