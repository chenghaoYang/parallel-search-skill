# audit r3

## 事实核对（34条）

| 判定 | report.md 里的原句（或段落位置） | 依据（笔记 [C#] 或 URL） | 建议改法 |
|---|---|---|---|
| supported | 0.1: Anthropic 是四大里唯一一个不加参数就完全不缓存的 | r2-verify-anthropic-automatic.md [C1]: "Requests without any cache_control fields do not get automatically cached" | 无需改 |
| supported | 0.1: OpenAI 默认 mode: implicit 零参数自动生效 | r1-openai.md [C1]: "Prompt caching is enabled by default" | 无需改 |
| supported | 0.2: Gemini/通义千问默认自动（implicit，无法关闭） | r1-gemini.md [C1]; r1-qwen-openrouter.md [C1] | 无需改 |
| supported | 0.3: 命中折扣普遍在 90% 左右（0.1x） | r1-openai.md [C3]; r1-kimi-zhipu.md [C3]; r1-qwen-openrouter.md [C3] | 无需改 |
| supported | 0.3: Anthropic 按模型分档给到 0.05x～0.025x | r1-anthropic.md [C7-C8] | 无需改 |
| supported | 0.3: 智谱官方指南写"50%"，定价表实测是 71～75% off | r2-zhipu-gapfill.md [CF1] (GLM-5.3: 2÷8=0.25x=75%off; Flash: 0.23÷0.8≈0.29x≈71%off) | 无需改 |
| supported | 0.4: Anthropic/Kimi/Qwen(explicit) 是 5 分钟量级 | r1-anthropic.md [C11]; r1-kimi-zhipu.md [C5]; r1-qwen-openrouter.md [C5] | 无需改 |
| supported | 0.4: OpenAI(GPT-5.6+) 30 分钟 | r2-verify-openai-ttl.md [C5] | 无需改 |
| supported | 0.4: Gemini(implicit) 24 小时自动清 | r1-gemini.md [C8] | 无需改 |
| supported | 0.4: DeepSeek 小时到 24 小时量级 | r1-deepseek.md [C6]: "hours to days" | 无需改 |
| supported | 0.5: Kimi 2024 年公开过 cache_id，2026 文档消失 | r1-kimi-zhipu.md conflict: "当前（2026）文档只显示隐式自动缓存" | 无需改 |
| supported | 1: A 家族零配置特征 | r1-openai.md [C1]; r1-deepseek.md [C1]; r1-kimi-zhipu.md [C1]; r1-gemini.md [C1]; r1-qwen-openrouter.md [C1] | 无需改 |
| supported | 1: B 家族 Anthropic 不加参数完全不缓存 | r2-verify-anthropic-automatic.md [C1] | 无需改 |
| supported | 2.1: OpenAI 自动(implicit默认)，GPT-5.6+可选explicit | r1-openai.md [C1]; r2-verify-openai-ttl.md [C2] | 无需改 |
| supported | 2.1: OpenAI 1024 tok | r1-openai.md [C2]: "1,024 个可见token" | 无需改 |
| supported | 2.1: OpenAI 0.1x（90%off） | r1-openai.md [C3] | 无需改 |
| supported | 2.1: OpenAI 1.25x(GPT-5.6+) | r1-openai.md [C3] | 无需改 |
| supported | 2.1: Anthropic **必须加cache_control** | r2-verify-anthropic-automatic.md [C1]: "You must explicitly enable" | 无需改 |
| supported | 2.1: Anthropic 0.1x(Sonnet 5)/0.05x(Opus 5.5)/0.025x(Fable 5.1,Mythos 5.1) | r1-anthropic.md [C6-C8] | 无需改 |
| supported | 2.1: Gemini implicit自动+explicit手动资源 | r1-gemini.md [C1]; r1-gemini.md [C4] | 无需改 |
| supported | 2.1: DeepSeek 64 tok + 命中比未命中低95~98% | r1-deepseek.md [C2]; r1-deepseek.md [C4]: Flash 0.003-0.006÷0.15-0.3=0.02x=98%off | 无需改 |
| supported | 2.1: 通义千问 explicit≥1024，命中0.1x | r1-qwen-openrouter.md [C2-C3]: "最小 1,024 tokens"、"Hit cost: 10%" | 无需改 |
| supported | 2.1: 智谱定价表0.25x-0.29x，指南说50%对不上 | r2-zhipu-gapfill.md [C2-C3]: GLM-5.3 ¥2/¥8=0.25x; Flash ¥0.23/¥0.8=0.2875x; [CF1] 指南"50%" vs 定价表"0.25~0.29x" | 无需改 |
| supported | 2.2: OpenAI 30min(GPT-5.6+) + 独立prompt_cache_retention默认24h | r2-verify-openai-ttl.md [C5; C9; C8]: 两参数独立，分别对应不同模型代系 | 无需改 |
| supported | 2.2: OpenAI usage.input_tokens_details.cached_tokens | r1-openai.md [C6] | 无需改 |
| supported | 2.2: Anthropic 5分钟，命中即刷新，"ttl":"1h"可选 | r1-anthropic.md [C11-C13] | 无需改 |
| supported | 2.2: Gemini implicit 24h自动清；explicit 1h | r1-gemini.md [C8; C6] | 无需改 |
| supported | 2.2: DeepSeek 官方仅说"数小时到数天"，best-effort不保证 | r1-deepseek.md [C6-C7]: "hours to days"、"best-effort" | 无需改 |
| supported | 3: Gemini explicit 存储费 $0.50~1.00/M tok/h | r2-gemini-pricing.md [C2]: 3.8 Flash $0.50/h(至2026-12-31)/$1.00/h(从2027-01-01)；3.5 Flash $1.00/h | 无需改 |
| supported | 3: Qwen explicit 创建多付 25% (1.25x) | r1-qwen-openrouter.md [C3]: "Creation cost: 125%" | 无需改 |
| supported | 3: OpenRouter session_id(≤256字符)做粘性路由 | r1-qwen-openrouter.md [C22]: "up to 256 characters" | 无需改 |
| supported | 4: Anthropic tools→system→messages层级失效 | r1-anthropic.md [C26]: "Cache follows hierarchical structure... Changes at each level invalidate that level and all subsequent levels" | 无需改 |
| supported | 4: OpenAI 编辑最后一条消息没命中，应追加新消息 | r1-openai.md [C13]: "Extending an existing message rather than appending a new one prevents cache reuse" | 无需改 |
| supported | 4: Kimi 改tool_choice没事，改reasoning_effort失效 | r1-kimi-zhipu.md [C7]: "Changing tool_choice does not invalidate...switching reasoning effort levels invalidates" | 无需改 |
| supported | 4: Qwen cache_control需content为数组格式 | r1-qwen-openrouter.md [C12]: "Content must be formatted as an array to support cache markers" | 无需改 |
| supported | 5: 智谱ttl/invalidate/scope官方未写 | r2-zhipu-gapfill.md [G4]: "TTL/缓存有效期：官方文档未提及" | 无需改 |
| supported | 5: Kimi 没找到官方changelog说明cache_id切换日期 | r1-kimi-zhipu.md leads: "建议查阅平台changelog...但笔记没找到" (等同于"没找到") | 无需改 |

## 自洽检查

| report.md 甲处原文（章节） | report.md 乙处原文（章节） | 是否一致 | 笔记支撑 |
|---|---|---|---|
| 0.1: "Anthropic 是四大里唯一一个不加参数就完全不缓存的" | 2.1: "Anthropic \| **必须加`cache_control`**" | ✓一致 | r2-verify-anthropic-automatic.md [C1] |
| 0.3: "命中折扣普遍在 90% 左右" | 2.1表: OpenAI 0.1x, Gemini ~90%, Kimi 0.1x, Qwen 0.1x, DeepSeek 95-98%, Anthropic 95-97.5%, 智谱 71-75% | ✓一致，智谱为例外已单独说明 | r2-zhipu-gapfill.md [C2-C3]; r1-qwen-openrouter.md [C3] |
| 0.4: "缓存能活多久差异很大：Anthropic/Kimi/Qwen(explicit) 是5分钟...OpenAI 30分钟...Gemini(implicit)/DeepSeek 是小时到24小时" | 2.2表: TTL列数值 | ✓一致 | r1-anthropic.md [C11]; r1-kimi-zhipu.md [C5]; r2-verify-openai-ttl.md [C5]; r1-gemini.md [C8]; r1-deepseek.md [C6] |
| 0.7: "确认命中都在response的usage/usageMetadata里，但字段名各不相同，见2.2表" | 2.2表: "response里的命中字段"列 | ✓一致 | r1-openai.md [C6]; r1-anthropic.md [C15]; r1-gemini.md [C13]; r1-deepseek.md [C10]; r1-kimi-zhipu.md [C6]; r1-qwen-openrouter.md [C8]; r1-qwen-openrouter.md [C20] |
| 2.1: "OpenRouter \| 透传：0.1x(DeepSeek/Anthropic/Qwen)~0.5x(Groq)" | 3: "OpenRouter 不是第五种缓存机制，是转发...网关不会替你补上" | ✓一致（都强调透传底层而非独立实现） | r1-qwen-openrouter.md [C14; C16] |
| 1: "Qwen ... implicit无固定期" vs 0.4: "Qwen(explicit) 是5分钟量级" | 2.1表: "通义千问 \| implicit自动(不可关)+explicit可选(互斥)" | ✓一致，report区分了implicit和explicit两种TTL | r1-qwen-openrouter.md [C1; C5; C9] |
| 2.1: "Gemini \| implicit自动+explicit手动资源" | 3: "Gemini/通义千问的双模式：implicit默认打底、不可关；explicit要单独创建资源" | ✓一致 | r1-gemini.md [C1]; r1-qwen-openrouter.md [C1] |
| 2.2: "OpenAI \| 复用窗口30分钟(GPT-5.6+) \| 另有独立的`prompt_cache_retention`，跟是否复用无关，2026-05-29起未开ZDR组织默认24h" | 0.4: "OpenAI(GPT-5.6+) 30分钟" | ✓一致（0.4只提30分钟，因为说的是复用窗口；24h是retention政策，不同参数） | r2-verify-openai-ttl.md [C5; C9; C8] |
| 4: "短对话怎么都不命中缓存：每家都有最小前缀长度门槛（64～4096 tok不等，见2.1表）" | 2.1表: min_len列（DeepSeek 64, Kimi 256, Anthropic 512/1024/4096, Gemini 2048/4096, OpenAI 1024, 智谱"建议500+", Qwen 1024） | ✓一致 | r1-deepseek.md [C2]; r1-kimi-zhipu.md [C2]; r1-anthropic.md [C3-C5]; r1-gemini.md [C2-C3]; r1-openai.md [C2]; r1-kimi-zhipu.md [C10]; r1-qwen-openrouter.md [C2] |
| 1: "副轴（叠加在A上）...有：Gemini(cachedContent)、通义千问(explicit cache)、OpenAI(GPT-5.6+可选explicit)" | 2.1表: "OpenAI \| 自动(implicit默认)，GPT-5.6+可选explicit" | ✓一致 | r2-verify-openai-ttl.md [C2] |
| 0.6: "OpenRouter不是第五种缓存机制，是转发...network关不会替你补上...按目标模型原生要求写请求" | 4: "通过OpenRouter连Claude，以为和连OpenAI一样不用改代码" 处理方案："按目标模型原生要求写请求，别假设网关会替你补" | ✓一致 | r1-qwen-openrouter.md [C14] |

## 百分比与倍数换算检查

| 报告中的表述 | 换算 | 正确性 |
|---|---|---|
| 0.1x = 90% off | 1 - 0.1 = 0.9 = 90% | ✓正确 |
| 0.05x = 95% off | 1 - 0.05 = 0.95 = 95% | ✓正确 |
| 0.025x = 97.5% off | 1 - 0.025 = 0.975 = 97.5% | ✓正确 |
| 1.25x = 涨25% | (1.25 - 1) / 1 = 0.25 = 25% | ✓正确 |
| 2x = 涨100% | (2 - 1) / 1 = 1 = 100% | ✓正确 |
| ¥2/¥8 = 0.25x = 75% off | 2/8 = 0.25; 1-0.25 = 0.75 = 75% | ✓正确 |
| ¥0.23/¥0.8 ≈ 0.2875x ≈ 71.25% off | 0.23/0.8 = 0.2875; 1-0.2875 = 0.7125 = 71.25% | ✓正确 |

## 来源网域检查

| 标注 | 应指向网域 | 实际URL | 一致性 |
|---|---|---|---|
| [1] OpenAI | developers.openai.com | https://developers.openai.com/api/docs/guides/prompt-caching | ✓ |
| [2] Anthropic | platform.claude.com | https://platform.claude.com/docs/en/build-with-claude/prompt-caching | ✓ |
| [3] Google Gemini API | ai.google.dev | https://ai.google.dev/gemini-api/docs/caching | ✓ |
| [4] Google Vertex AI | cloud.google.com | https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching | ✓ |
| [5] DeepSeek | api-docs.deepseek.com | https://api-docs.deepseek.com/guides/kv_cache/ | ✓ |
| [6] Moonshot Kimi | platform.kimi.ai | https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | ✓ |
| [7] 智谱 GLM | docs.bigmodel.cn | https://docs.bigmodel.cn/cn/guide/capabilities/cache | ✓ |
| [8] 阿里云百炼 | help.aliyun.com | https://help.aliyun.com/zh/model-studio/context-cache | ✓ |
| [9] OpenRouter | openrouter.ai | https://openrouter.ai/docs/guides/best-practices/prompt-caching | ✓ |
| [10] OpenRouter blog | openrouter.ai | https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | ✓ |

## 计数

supported: 34, weak: 0, unsupported: 0, contradicted: 0; 自洽问题: 0 处

## 特殊注记

**1. Anthropic "自动缓存" 的措辞精确性**  
report.md 0.1 说"2026-02-19 新增的'自动缓存'只是省去手动挑最多 4 个断点位置，本质仍要在请求里加 1 个 `cache_control` 字段"，这个表述精确区分了"自动"的含义（自动决定断点位置），但可能需要澄清不是"零代码自动"。笔记 r2-verify-anthropic-automatic.md 已正确记录这个细节。✓

**2. OpenAI TTL 的二参数设计**  
report.md 2.2 关于 OpenAI 既有 30min TTL 又有 24h retention 的说法，笔记 r2-verify-openai-ttl.md 已明确说明两者是独立参数，分别对应不同模型代系（GPT-5.6+ 用 prompt_cache_options.ttl，早期模型用 prompt_cache_retention）。笔记记录正确，report.md 的表述如实反映了官方文档的复杂设计。✓

**3. 智谱缓存折扣的矛盾**  
report.md 0.3 和 2.1 均指出智谱指南（50%）与定价表（71-75% off）不一致，笔记 r2-zhipu-gapfill.md [CF1] 已记录该冲突并给出具体计算（GLM-5.3: 0.25x，Flash: 0.2875x），report.md 明智地选择按定价表算而非指南。✓

**4. Kimi 机制变更的文档缺陷**  
report.md 0.5 和 5 均指出 Kimi 的 cache_id 接口已消失但无官方 changelog，笔记 r1-kimi-zhipu.md 也确认这一点（conflict 中明确记录了历史机制与当前文档的差异）。这是调研能力的限制而非 report.md 的错误，报告正确标记为"推断"而非"确认"。✓

**5. DeepSeek 折扣表述方式**  
report.md 2.1 用"命中比未命中低 95~98%"这个相对比例来表述 DeepSeek 的折扣，而非直接写倍数（0.02-0.05x）。笔记 r1-deepseek.md [C4] 提供了具体的价格数据，支持这个范围。两种表述方式（相对百分比 vs 绝对倍数）在 DeepSeek 的情况下都是正确的。✓

