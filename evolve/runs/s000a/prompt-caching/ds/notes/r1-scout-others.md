# r1-scout-others
question: Kimi（月之暗面）、智谱、通义千问（百炼/DashScope）、OpenRouter 各自的上下文缓存官方文档在哪个 URL，机制是自动前缀、请求内断点，还是先创建缓存资源？顺手记下网格未列、但会改变分类的相邻产品（豆包/火山、MiniMax、Groq、Azure OpenAI、Vertex、Bedrock）是否有官方缓存文档。
checked: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api, https://platform.kimi.com/blog/posts/context-caching, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://www.alibabacloud.com/help/en/model-studio/context-cache, https://openrouter.ai/docs/features/prompt-caching, https://console.groq.com/docs/prompt-caching, https://docs.volcengine.com/docs/82379/1398933, https://platform.minimax.io/docs/api-reference/text-prompt-caching, https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching, https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview, https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html

## claims
- [C1] Kimi 现行文档（platform.kimi.com，platform.moonshot.cn 已跳转至此）只支持隐式前缀缓存：Chat Completions/Responses 传 `prompt_cache_options`，不传时默认 5m TTL 自动写入 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "`prompt_cache_options.mode` 当前仅支持 `implicit`，`ttl` 支持 `5m` 和 `1h`" | type: official
- [C2] Kimi 的 Anthropic Messages API 用请求顶层 `cache_control` 控制缓存写入；消息体内的同名标记被忽略；缓存按 org 隔离、不可手动清除 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "`cache_control` 只在请求顶层生效，消息体内的同名标记会被忽略" | type: official
- [C3] Moonshot 旧版 Context Caching（2024-07-01 公测）是独立缓存资源：POST `https://api.moonshot.cn/v1/caching` 创建，chat 消息中用 `role="cache"` + `cache_id=...;reset_ttl=...` 引用，收创建费+存储费(按分钟)+调用费 | src: https://platform.kimi.com/blog/posts/context-caching | quote: "你可以直接使用 `role=\"cache\"`来引用一段已经创建好的 cache" | type: official
- [C4] 智谱 GLM 上下文缓存为隐式前缀缓存，无需配置；命中量在 `usage.prompt_tokens_details.cached_tokens`；命中按约标准价 50% 计费 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "自动缓存识别：隐式缓存，智能识别重复的上下文内容，无需手动配置" | type: official
- [C5] 智谱缓存需重复前缀足够长（建议 500 Token 以上），异步生效 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "要触发上下文缓存，重复的前缀内容必须足够长（建议 500 Token 以上）" | type: official
- [C6] 阿里百炼/Model Studio 同时提供显式与隐式两种上下文缓存，二者互斥 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "Explicit cache and implicit cache are mutually exclusive." | type: official
- [C7] 百炼显式缓存＝请求内断点：在 messages 的 content 块加 `"cache_control": {"type": "ephemeral"}`，单请求至多 4 个标记，从标记向前回溯至多 20 个 content 块，最小 1024 token，TTL 5 分钟且命中重置 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "The system then searches backward from each `cache_control` marker and examines up to 20 preceding `content` blocks to find a cache hit." | type: official
- [C8] 百炼隐式缓存自动开启、不可关闭、命中不保证；命中按标准输入价 20% 计费（显式命中 10%、创建 125%）；Responses API 另有 Session 缓存 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "This automatic mode requires no extra configuration and cannot be disabled" | type: official
- [C9] OpenRouter 为网关透传：多数 provider 自动缓存；Anthropic、Alibaba Qwen 需 per-message `cache_control`；有 provider sticky routing 保命中 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Most providers automatically enable prompt caching, but note that some (see Alibaba and Anthropic below) require you to enable it on a per-message basis." | type: official
- [C10] OpenRouter 在 Anthropic 式 `cache_control` 与 OpenAI 式 `prompt_cache_breakpoint` 之间互译（TTL 不互译）；sticky 会话可用 body `session_id` 或 `x-session-id` header（≤256 字符），10 分钟无活动过期 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "a text block marked with Anthropic-style `cache_control` gets a `prompt_cache_breakpoint` when routed to a supporting OpenAI model" | type: official
- [C11] Groq 为自动前缀缓存（家族 I）：无代码改动、无额外费用，命中输入 50% 折扣，数据存易失内存、不用 2 小时过期 | src: https://console.groq.com/docs/prompt-caching | quote: "Prompt caching works automatically on all your API requests with no code changes required and no additional fees." | type: official
- [C12] 火山方舟（豆包）双模式：隐式缓存自动启用且不可关闭（默认最小 1024 token）；显式缓存走 Responses API 参数 `caching: {"type":"enabled"}`（页面更新时间 2026.09.22） | src: https://docs.volcengine.com/docs/82379/1398933 | quote: "隐式缓存：自动启用，用户无需额外配置，且无法关闭，适合更关注接入便捷性、难以显式管理或固定前缀的场景" | type: official
- [C13] 火山显式缓存属"先创建再引用"资源型：首轮 `"caching": {"type":"enabled","prefix":true}` 建前缀缓存（≥256 token），后续轮次用 `previous_response_id` 引用；另支持 Session 缓存随对话更新，存储按小时计费 | src: https://docs.volcengine.com/docs/82379/1398933 | quote: "后续轮次即可通过 previous_response_id 引用缓存信息" | type: official
- [C14] MiniMax 双机制：自动缓存（≥512 input token、前缀匹配、不改请求）+ Anthropic 兼容显式 `cache_control`（5 分钟 TTL，见 /docs/api-reference/anthropic-api-compatible-cache） | src: https://platform.minimax.io/docs/api-reference/text-prompt-caching | quote: "Automatic Caching: Passive caching that automatically identifies repeated context content without changing API call methods" | type: official
- [C15] Azure OpenAI（Microsoft Foundry）：默认隐式缓存；GPT-5.6+ 支持块级 `prompt_cache_breakpoint` 与请求级 `prompt_cache_options`（mode: implicit|explicit，ttl 仅 30m）；旧模型用 `prompt_cache_retention`（in_memory|24h）（ms.date 2026-08-11） | src: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching | quote: "On GPT-5.6 models and later model families, use explicit cache breakpoints to mark the end of a reusable prompt prefix." | type: official
- [C16] Vertex AI（现归入 Gemini Enterprise Agent Platform）：隐式缓存默认开启、命中 90% 折扣；显式缓存是独立资源，API 支持 create/use/update/delete `CachedContent`、默认 TTL 60 分钟（页面 Last updated 2026-09-22） | src: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview | quote: "Explicit caching: Manual caching enabled using the Gemini Enterprise API, where you explicitly declare the content you want to cache" | type: official
- [C17] AWS Bedrock：隐式（自动、无需配置）+ 显式 cache checkpoints：Converse API 用 `cachePoint` 块、InvokeModel 用 `cache_control`，TTL 5m/1h，每模型最多 4 个 checkpoint | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "Cache checkpoints are markers that define the contiguous subsection of your prompt that you want to cache." | type: official

## conflicts
- Groq 支持模型两家文档不一致：OpenRouter 页写 "Prompt caching with Groq is automated and does not require any additional configuration. Currently available on Kimi K2 models."（https://openrouter.ai/docs/features/prompt-caching）；Groq 官方页只列 `openai/gpt-oss-20b`、`openai/gpt-oss-120b`、`openai/gpt-oss-safeguard-20b`（"Prompt caching is currently only supported for the following models"，https://console.groq.com/docs/prompt-caching）。

## gaps
- Moonshot 旧版 `/v1/caching` 资源型接口是否仍可用：现行文档页只写 implicit 模式，旧接口仅见于 2024-07 公测博客；下一轮需查 platform.kimi.com API reference 是否保留 caching 端点。
- 百炼 Responses API 的 Session 缓存（`x-dashscope-session-cache` header）只见到一句交叉引用，未取详情页。
- 中文版百炼文档 https://docs.bailian.console.aliyun.com/zh/model-studio/context-cache 未实际打开（用的英文版 alibabacloud.com/help）；火山英文站与国际站文档未查。
- Vertex 旧 URL cloud.google.com/vertex-ai/... 已 301 到 docs.cloud.google.com/gemini-enterprise-agent-platform/... 下，下一轮摘录用新路径。

## leads
- Kimi/Moonshot | I（旧另有 III /v1/caching，疑似废弃） | https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | "prompt_cache_options.mode 当前仅支持 implicit"
- 智谱 GLM | I | https://docs.bigmodel.cn/cn/guide/capabilities/cache | "隐式缓存，智能识别重复的上下文内容，无需手动配置"
- 阿里百炼/DashScope | I+II（互斥） | https://www.alibabacloud.com/help/en/model-studio/context-cache | 隐式自动不可关；显式用 cache_control ephemeral 断点
- OpenRouter | IV | https://openrouter.ai/docs/features/prompt-caching | 透传各家机制并互译 cache_control/prompt_cache_breakpoint，sticky routing
- 火山方舟/豆包 | I+III | https://docs.volcengine.com/docs/82379/1398933 | 隐式自动；显式 Responses API 建缓存后 previous_response_id 引用
- MiniMax | I+II | https://platform.minimax.io/docs/api-reference/text-prompt-caching | 自动前缀 + Anthropic 兼容 cache_control
- Groq | I | https://console.groq.com/docs/prompt-caching | "no code changes required"，仅 gpt-oss 系列
- Azure OpenAI | I+II | https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching | 默认隐式；GPT-5.6+ 有 prompt_cache_breakpoint
- Vertex AI | I+III | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview | 隐式默认开；显式为 CachedContent 资源
- AWS Bedrock | I+II | https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | 隐式自动；显式 cachePoint/cache_control 断点
