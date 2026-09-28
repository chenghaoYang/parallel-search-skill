# r2-verify-openai-ttl

question: (a) OpenAI GPT-5.6+ 的 explicit cache 模式（prompt_cache_options.mode="explicit"）是不是一个可选项，默认路径依然是零代码自动缓存？(b) 文档里出现的"30分钟 TTL"和"2026-05-29 起默认改为 24h retention"这两个数字，是同一个 TTL 的新旧数值，还是两个不同概念（例如一个是"缓存可复用多久"的 reuse 窗口，另一个是"数据保留多久用于安全/滥用监测"的 retention 政策，两者并存不冲突）？

checked: https://developers.openai.com/api/docs/guides/prompt-caching, https://developers.openai.com/api/docs/api-reference/chat/create, https://developers.openai.com/docs/changelog

## claims

- [C1] prompt_cache_options 参数整体是可选的，两个字段（mode、ttl）都非必需 | src: https://developers.openai.com/api/docs/api-reference/chat/create | quote: "Neither field is required. The entire prompt_cache_options parameter itself is optional." | type: official

- [C2] mode 字段默认值为 "implicit"，explicit 是可选的 | src: https://developers.openai.com/api/docs/api-reference/chat/create | quote: "mode (optional): Controls whether OpenAI automatically creates an implicit cache breakpoint. Default: \"implicit\"" | type: official

- [C3] 默认情况下（不设置参数）系统自动采用 implicit mode，OpenAI 自动创建缓存断点 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Implicit mode: OpenAI places a breakpoint at the end of the latest eligible message automatically" | type: official

- [C4] prompt_cache_options.ttl 支持唯一值 "30m"，也是默认值；GPT-5.6+ 模型使用此参数 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Use prompt_cache_options.ttl to control the minimum cache lifetime. The only supported value, \"30m\", is also the default." | type: official

- [C5] 30分钟 TTL 的含义：缓存前缀在最后一次写入或复用后保持可复用的最小时间 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse, though OpenAI may retain it longer." | type: official

- [C6] prompt_cache_retention 是较早模型使用的参数，支持 "in_memory" 或 "24h" 两个值 | src: https://developers.openai.com/api/docs/api-reference/chat/create | quote: "prompt_cache_retention parameter... accepts \"in_memory\" or \"24h\" values" | type: official

- [C7] 2026-05-29 前：prompt_cache_retention 对于未启用 ZDR 的组织默认为 "in_memory" | src: https://developers.openai.com/docs/changelog | quote: "May 29, 2026 - For organizations without ZDR enabled, prompt_cache_retention now defaults to 24h instead of in_memory" | type: official

- [C8] 2026-05-29 改动：prompt_cache_retention 默认改为 "24h"（针对较早模型，与 GPT-5.6+ 的 30m TTL 是不同的参数）| src: https://developers.openai.com/docs/changelog | quote: "For organizations without ZDR enabled, prompt_cache_retention now defaults to 24h instead of in_memory, enabling extended prompt caching by default." | type: official

- [C9] prompt_cache_retention 和 prompt_cache_options.ttl 是两个独立的、不相交的参数，分别用于不同的目的 | src: https://developers.openai.com/api/docs/api-reference/chat/create | quote: "This field expresses a maximum retention policy, while prompt_cache_options.ttl expresses a minimum cache lifetime. The two fields are independent and do not interact." | type: official

- [C10] prompt_cache_retention (24h) 表达最大保留政策；prompt_cache_options.ttl (30m) 表达最小缓存生命周期 | src: https://developers.openai.com/api/docs/api-reference/chat/create | quote: "prompt_cache_retention... maximum retention policy... prompt_cache_options.ttl... minimum cache lifetime" | type: official

## conflicts

none

## gaps

- 官方文档中没有明确说明 prompt_cache_retention 是否为"滥用监测"或其他合规目的的保留。仅说明是"extended prompt caching"的保留政策。

## leads

- prompt_cache_retention 已对 gpt-5.5+ 系列为 deprecated，建议新实现使用 prompt_cache_options；但较早模型仍然需要此参数
- explicit mode 下可以指定最多 4 个显式断点，不设置时请求不会使用 prompt caching；implicit mode 下系统自动创建
