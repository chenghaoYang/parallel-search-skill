# 审计报告：Prompt Caching 报告事实支撑核查

## 抽查清单与判定

| 判定 | 主张原文（摘自 report.md） | 依据（笔记文件+[Cn]或 URL） | 建议改法 |
|------|--------------------------|----------------------------|--------|
| supported | OpenAI Chat Completions 支持 prompt_cache_options 参数、三个端点都支持、但官方 caching 指南页只讲 Responses/Agents | r2-openai-gaps.md [C1][C3] | 无 |
| supported | Anthropic 2026-02-19 上线「自动缓存」 | r2-verify-anthropic.md [C4] | 无 |
| supported | Anthropic「仍需显式加 cache_control 字段，不是不加任何参数就全自动」 | r2-verify-anthropic.md [C2] | 无 |
| supported | OpenAI 1.25x 写入溢价对 implicit/explicit 都适用 | r2-openai-gaps.md [C2] | 无 |
| supported | Anthropic Fable5.1/Mythos5.1 自 2026-09-01 起命中折扣为 0.025x | r1-anthropic.md [C5] | 无 |
| supported | Anthropic 多数模型命中折扣 0.1x | r1-anthropic.md [C5] | 无 |
| supported | 通义千问 explicit 0.1x、implicit 0.2x（更贵） | r1-cn-b.md [C4] | 无 |
| supported | 智谱 GLM 约 0.5x 折扣 | r1-cn-a.md [C14] | 无 |
| supported | DeepSeek 写入完全不加价 | r1-deepseek.md [C6] | 无 |
| supported | OpenAI 新模型固定 30 分钟 TTL | r1-openai.md [C10] | 无 |
| supported | Anthropic/Kimi 5 分钟起、多付钱换 1 小时 | r1-anthropic.md [C6]、r1-cn-a.md [C5] | 无 |
| supported | DeepSeek 数小时到数天 TTL | r1-deepseek.md [C7-C8] | 无 |
| supported | 通义千问隐式缓存「无固定有效期，按使用频率清理」 | r2-ttl-gaps.md [C1] | 无 |
| supported | 智谱 GLM 官方未给 TTL（二轮核查确认已查证） | r2-ttl-gaps.md gap | 无 |
| supported | OpenRouter 官方文档未明确声称「不对缓存加价」 | r2-openrouter-kimi.md [C2] | 无 |
| weak | OpenRouter 有些数字比直连贵（如 OpenAI 读取 0.25x-0.5x vs 0.1x） | r2-openrouter-kimi.md [C1]（仅有表格数据，缺"比直连贵"说法） | 建议改为"根据 OpenRouter 官方表，OpenAI 缓存读取为 0.25x-0.5x，高于官方 0.1x 的直连价"或标注为"需确认是 OpenRouter 加成还是模型版本差异" |
| supported | OpenAI 命中价 0.1x | r1-openai.md [C7] | 无 |
| supported | OpenAI 写入价 1.25x | r1-openai.md [C8] | 无 |
| supported | OpenAI TTL 30 分钟 | r1-openai.md [C10] | 无 |
| supported | OpenAI cached_tokens/cache_write_tokens 字段 | r1-openai.md [C13-C14] | 无 |
| supported | Anthropic 命中价 0.1x（多数）/0.025x（Fable5.1/Mythos5.1） | r1-anthropic.md [C5] | 无 |
| supported | Anthropic 写入价 1.25x(5min)/2x(1h) | r1-anthropic.md [C6] | 无 |
| supported | Anthropic TTL 5 分钟/1 小时 | r1-anthropic.md [C7] | 无 |
| supported | Anthropic cache_read/creation_input_tokens 字段 | r1-anthropic.md [C9] | 无 |
| supported | Gemini explicit 命中价 0.1x | r1-gemini.md [C7] | 无 |
| supported | Gemini implicit 命中价官方未给% | r1-gemini.md [C8]、r2-ttl-gaps.md [C3] | 无 |
| supported | Gemini explicit 存储费 $0.5/M/h(2027 起 $1) | r1-gemini.md [C9] | 无 |
| supported | DeepSeek 命中价 0.1x | r1-deepseek.md [C5] | 无 |
| supported | DeepSeek 写入价不加价 | r1-deepseek.md [C6] | 无 |
| supported | DeepSeek TTL 数小时~数天 | r1-deepseek.md [C7] | 无 |
| supported | Kimi 命中价 0.1x | r1-cn-a.md [C4] | 无 |
| supported | Kimi 写入价 $3/M(5min)或$6/M(1h) | r1-cn-a.md [C5] | 无 |
| supported | Kimi TTL 5 分钟/1 小时 | r1-cn-a.md [C6] | 无 |
| supported | 智谱 GLM 命中价 ~0.5x | r1-cn-a.md [C14] | 无 |
| supported | 通义千问 explicit 命中价 0.1x | r1-cn-b.md [C4] | 无 |
| supported | 通义千问 implicit 命中价 0.2x | r1-cn-b.md [C4] | 无 |
| supported | 通义千问 explicit 写入价 1.25x | r1-cn-b.md [C5] | 无 |
| supported | 通义千问 implicit 写入价不加价 | r1-cn-b.md [C5] | 无 |
| supported | OpenRouter 给分供应商倍率表 | r2-openrouter-kimi.md [C1] | 无 |
| supported | OpenRouter 没有「不加价」承诺 | r2-openrouter-kimi.md [C2] | 无 |
| weak | 通义千问 ≠ 托管在它上面的第三方模型自家 API（文档明确说走阿里云自己的实现与计费） | r1-cn-b.md 提到支持这些模型但未明确说"≠原厂实现"；WebFetch 阿里云文档也未直接说明 | 建议补充：笔记中应明确注明"通义千问平台上的 DeepSeek/Kimi/GLM 缓存采用阿里云自己的实现与计费规则，与这些厂商自家 API 的缓存功能不同"或引用相关官方声明 |
| supported | cached_tokens 字段 | r1-openai.md [C13]、r1-cn-a.md [C17] 等多处 | 无 |
| supported | cache_read_input_tokens 字段 | r1-anthropic.md [C9]、r1-cn-a.md [C7] | 无 |
| supported | cache_creation_input_tokens 字段 | r1-anthropic.md [C9]、r1-cn-b.md [C7] | 无 |
| supported | prompt_cache_hit_tokens 字段 | r1-deepseek.md [C9] | 无 |
| supported | usageMetadata.total_cached_tokens 字段 | r1-gemini.md [C14] | 无 |

## 统计

- **supported**: 42 条
- **weak**: 2 条
- **unsupported**: 0 条
- **contradicted**: 0 条

**总计**: 44 条主张抽查

## 主要问题

### 1. OpenRouter 价格对比说明不够明确（weak）
**主张**: "表里一些数字（如 OpenAI 读取列的是 0.25x–0.5x）比该厂商官网直连价（0.1x）更贵"
**问题**: 笔记中 r2-openrouter-kimi.md [C1] 仅列出了表格数据，未做"比直连贵"的对比说明。
**建议**: 报告第 0 节和第 2 节矩阵中涉及 OpenRouter 的部分应补充说明 WebFetch 验证的结果：OpenRouter 官方确实列出 OpenAI 缓存读取为 0.25x-0.5x，但未明确说明是否含加成，仅列数据而已。或补注：官方文档中无法区分是 OpenRouter 加成还是模型版本差异。

### 2. 通义千问 ≠ 第三方模型自家 API 的说明不足（weak）
**主张**: "百炼把 DeepSeek/Kimi/GLM 列为「支持缓存的模型」，走的是阿里云自己的实现与计费"
**问题**: 笔记 r1-cn-b.md [C9] 只是列出了支持这些模型，未明确说明"采用阿里云自己实现"这个关键信息。WebFetch 查阿里云文档也未直接找到该说明。
**建议**: 若报告中此主张来自非笔记来源（如其他官方文档或逻辑推断），应在报告中明确标注。若要从笔记支撑，需补充查询或在笔记中注明该结论来自对比分析（通义千问与 DeepSeek/Kimi/GLM 的计费规则完全不同）。

## 检查过程备注

- 所有 official 类型的主张均已与笔记中的官方文档引用对应验证
- 两个 weak 主张主要是因为笔记中有相关数据，但缺少明确的对比或说明
- 未发现笔记与报告之间的直接矛盾（contradicted）
- 所有涉及日期、模型名、具体数值的主张均已核实

## checked 的 URL 清单

笔记中检查过的主要 URL：
- OpenAI: developers.openai.com/docs/guides/prompt-caching, developers.openai.com/api/docs/api-reference/chat/create
- Anthropic: platform.claude.com/docs/build-with-claude/prompt-caching, github.com/anthropics/anthropic-sdk-python/commits/a940123
- Gemini: ai.google.dev/gemini-api/docs/caching, ai.google.dev/gemini-api/docs/pricing
- DeepSeek: api-docs.deepseek.com/guides/kv_cache/, api-docs.deepseek.com/news/news0802/
- Kimi: platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api
- 智谱 GLM: docs.bigmodel.cn/cn/guide/capabilities/cache
- 通义千问: help.aliyun.com/zh/model-studio/context-cache
- OpenRouter: openrouter.ai/docs/guides/best-practices/prompt-caching, openrouter.ai/docs/features/prompt-caching
