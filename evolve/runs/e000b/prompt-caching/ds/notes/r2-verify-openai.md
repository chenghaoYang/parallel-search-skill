# r2-verify-openai
question: 复核上一轮对 OpenAI prompt caching 的几条反常主张是否准确、原文是否真的这样写：(1)GPT-5.6/6 Sol 模型及 90% 折扣；(2)缓存写入 1.25x 费用；(3)prompt_cache_options.mode 和 prompt_cache_breakpoint 参数；(4)缓存 TTL 默认 30 分钟、可配置到 24 小时
checked: https://developers.openai.com/api/docs/guides/prompt-caching, https://developers.openai.com/api/docs/pricing, https://developers.openai.com/api/docs/models

## claims
- [C1] GPT-5.6、GPT-5.6-Sol、GPT-5.6-Luna、GPT-5.6-Terra、GPT-6-Astra、GPT-6-Sol、GPT-6-Luna 等模型确实存在于官方 API 和定价表中 | src: https://developers.openai.com/api/docs/pricing | quote: "gpt-5.6, gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna, gpt-6-astra, gpt-6-sol, gpt-6-luna 都列在定价表的标准处理层、批处理层、快速模式列表中" | type: official
- [C2] GPT-5.6+ 缓存读取折扣确为 0.1x（90% 折扣）；GPT-6-Sol 标准模式下 cached input $0.20/1M vs standard input $2.00/1M，折扣率为 0.1x | src: https://developers.openai.com/api/docs/pricing | quote: "For GPT-6-Sol cached input costs $0.20 compared to standard input $2.00—representing a 90% reduction" | type: official
- [C3] GPT-5.6+ 缓存写入费用确为 1.25x 标准输入率；GPT-6-Sol 长上下文中 cache writes $2.50/1M vs input $2.00/1M，折扣率为 1.25x | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "For GPT-5.6 and later, cache writes cost 1.25× the standard, uncached input-token rate" | type: official
- [C4] prompt_cache_options.mode 参数支持 "implicit" 和 "explicit" 两种模式；implicit 模式下 OpenAI 自动在最后一条符合条件的消息末尾放置缓存断点 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Implicit mode (default): OpenAI automatically places breakpoints at the end of the latest eligible message" | type: official
- [C5] prompt_cache_breakpoint 参数用于 explicit 模式下手动标记缓存断点位置，在内容块内使用 prompt_cache_breakpoint: { "mode": "explicit" } | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Explicit mode: Developers manually mark breakpoints using prompt_cache_breakpoint within content blocks, enabling precise control over cached sections" | type: official
- [C6] GPT-5.6+ 缓存 TTL 由 prompt_cache_options.ttl 控制，仅支持值 "30m"（30 分钟）| src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Use prompt_cache_options.ttl to control cache lifetime. The only supported value, 30m, is also the default. A cached prefix remains available for 30 minutes after its most recent write or reuse." | type: official
- [C7] GPT-4o/o1 等早期模型使用 prompt_cache_retention 参数控制缓存生命周期，支持 "in_memory"（约 5-10 分钟到 1 小时）或 "24h"（约 30 分钟起、最多 24 小时）| src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Earlier models support 'in_memory' (typically 5-10 minutes, up to one hour) and '24h' (typically 30 minutes, up to 24 hours) retention options" | type: official
- [C8] 缓存完全自动激活，无需改代码；prompt_cache_options.mode 和 prompt_cache_breakpoint 是 GPT-5.6+ 上可选的手动控制参数，不改变默认自动缓存行为 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Prompt caching is automatically applied. Both implicit and explicit caching are supported; explicit caching gives more control but is optional" | type: official

## conflicts
- [CONFLICT-1] TTL 可配置上限的说法：上一轮 C6 声称"GPT-5.6+ 默认 30 分钟，可配置至 24 小时"，但官方文档明确说明 GPT-5.6+ 的 prompt_cache_options.ttl 仅支持一个固定值 "30m"，无法配置到 24 小时。24 小时的配置能力仅存在于早期模型（GPT-5.5、GPT-4o 等）的 prompt_cache_retention 参数中。上一轮混淆了新旧模型的参数和配置选项。
  - 上一轮原文：https://developers.openai.com/api/docs/changelog (C6) "extended prompt cache retention keeping cached prefixes active up to a maximum of 24 hours; for organizations without ZDR enabled, prompt_cache_retention now defaults to 24h"
  - 实际情况：这句话说的是早期模型的 prompt_cache_retention，不是 GPT-5.6+ 的 prompt_cache_options.ttl

## gaps
- 缓存自动激活是否在所有 API 版本、所有集成方式上都生效（比如 Responses API vs Chat Completions API）
- prompt_cache_options.mode 和 prompt_cache_breakpoint 是否与缓存成本有关系（implicit vs explicit 是否影响折扣或写入费）
- 缓存写入费用 1.25x 的措施背景——为何早期模型免费、新模型收费

## leads
- GPT-6 Sol 与 GPT-5.6 的缓存实现细节是否完全相同（两者的折扣、TTL 参数名是否一致）
- Azure OpenAI 或其他云托管版本中缓存定价是否与原生保持一致
