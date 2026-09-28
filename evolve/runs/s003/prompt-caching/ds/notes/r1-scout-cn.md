# r1-scout-cn
question: Kimi（月之暗面/Moonshot）、智谱（GLM/BigModel）、通义千问（DashScope/百炼）、OpenRouter 有没有官方的上下文缓存 / prompt caching 文档，各属于哪一类控制方式。
checked: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://help.aliyun.com/zh/model-studio/context-cache, https://openrouter.ai/docs/features/prompt-caching, https://platform.kimi.com/blog/posts/context-caching, https://platform.kimi.com/docs/llms.txt

## claims
- [C1] Kimi 当前上下文缓存为自动前缀匹配；不传 prompt_cache_options 时默认 5m TTL 自动写入并复用 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "不传 `prompt_cache_options` 时，系统默认使用 `5m` TTL：满足命中条件的前缀会自动写入并尝试复用" | type: official
- [C2] Kimi prompt_cache_options.mode 仅支持 implicit，ttl 支持 5m/1h | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "`prompt_cache_options.mode` 当前仅支持 `implicit`，`ttl` 支持 `5m` 和 `1h`。" | type: official
- [C3] Kimi 的 Anthropic Messages 兼容端点用顶层 cache_control（type ephemeral, ttl 5m/1h）控制写入，消息体内同名标记被忽略 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "`cache_control` 只在请求顶层生效，消息体内的同名标记会被忽略。" | type: official
- [C4] Moonshot 旧版显式 Context Caching（2024-07-01 公测，moonshot-v1）：POST https://api.moonshot.cn/v1/caching 创建命名 cache，chat 请求用 role="cache" + cache_id 引用 | src: https://platform.kimi.com/blog/posts/context-caching | quote: "你可以直接使用 `role=\"cache\"`来引用一段已经创建好的 cache" | type: official
- [C5] 智谱 BigModel 上下文缓存为隐式缓存，无需手动配置 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "**自动缓存识别**：隐式缓存，智能识别重复的上下文内容，无需手动配置" | type: official
- [C6] 智谱缓存命中量经响应字段 usage.prompt_tokens_details.cached_tokens 返回 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "透明化计费**：详细显示缓存命中的 Token 数量，响应字段 `usage.prompt_tokens_details.cached_tokens`" | type: official
- [C7] 智谱缓存触发建议重复前缀 500 Token 以上 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "要触发上下文缓存，重复的前缀内容必须足够长（建议 500 Token 以上）" | type: official
- [C8] 百炼上下文缓存分显式/隐式两种模式且互斥，单请求只能用一种 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "显式缓存、隐式缓存两者互斥，单个请求只能应用其中一种模式。" | type: official
- [C9] 百炼显式缓存在 messages 的 content 块上加 cache_control ephemeral 标记，最多 4 个、向前回溯 20 块 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "在 messages 中加入`\"cache_control\": {\"type\": \"ephemeral\"}`标记，系统将以每个`cache_control`标记位置为终点，向前回溯最多 20 个 `content` 块" | type: official
- [C10] 百炼显式缓存仅支持 ephemeral、5 分钟有效期、最小 1024 Token | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "仅支持将 `type` 设置为 `ephemeral`，有效期为 5 分钟。" | type: official
- [C11] 百炼隐式缓存自动开启且无法关闭，命中通常按输入单价 20% 计费 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "此为自动模式，无需额外配置，且无法关闭" | type: official
- [C12] OpenRouter 多数上游自动开启缓存，Alibaba/Anthropic 等需 per-message cache_control；OpenRouter 做透传 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Most providers automatically enable prompt caching, but note that some (see Alibaba and Anthropic below) require you to enable it on a per-message basis." | type: official
- [C13] OpenRouter 在 provider 间转换断点标记：cache_control↔prompt_cache_breakpoint，ttl 不翻译 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "a text block marked with Anthropic-style `cache_control` gets a `prompt_cache_breakpoint` when routed to a supporting OpenAI model" | type: official
- [C14] OpenRouter 用 provider sticky routing + session_id/x-session-id header 保持同 provider 以提高命中率 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "OpenRouter uses **provider sticky routing** to route your subsequent requests to the same provider endpoint after a cached request." | type: official

## conflicts
- 无明显冲突。注意差异点：Kimi 的 Anthropic 兼容端点只接受顶层 cache_control（非 Anthropic 的逐块断点），与百炼逐块 cache_control 不同——是同名字段在不同家的不同语义，非来源冲突。

## gaps
- Moonshot 旧版 /v1/caching 命名缓存是否仍可用：仅见于 2024-07-01 公测博客（platform.kimi.com/blog/posts/context-caching，发表日期 2024年07月01日）；当前 docs llms.txt 索引中无 caching 端点页，疑似被 implicit 模式取代，未找到 deprecation 公告。
- Kimi api-reference 中 prompt_cache_key 参数（搜索摘要提及 platform.moonshot.cn/docs/api-reference）未打开核实。
- 智谱是否存在显式/断点模式：本次只读了 cache 指南一页，未见 cache_control；未检索其他页面。
- 百炼 Responses API 的 Session 缓存是独立配置（页内提及，未打开）：https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api#example-session-cache-title

## leads
- Kimi/Moonshot | 自动前缀 | https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | prompt_cache_options.mode 仅 implicit，默认 5m TTL 自动写入；Anthropic 端点另有顶层 cache_control 开关
- Kimi/Moonshot | 命名缓存资源（旧，2024 公测，状态待核实） | https://platform.kimi.com/blog/posts/context-caching | POST /v1/caching 返回 cache id，chat 用 role="cache" + "cache_id=...;reset_ttl=..." 引用
- 智谱 BigModel | 自动前缀 | https://docs.bigmodel.cn/cn/guide/capabilities/cache | 页面自称"隐式缓存…无需手动配置"，命中看 usage.prompt_tokens_details.cached_tokens（英文镜像 docs.z.ai/guides/capabilities/cache）
- 阿里百炼/DashScope | 请求内断点 | https://help.aliyun.com/zh/model-studio/context-cache | content 块上加 "cache_control": {"type": "ephemeral"}，≤4 标记，TTL 5min
- 阿里百炼/DashScope | 自动前缀 | https://help.aliyun.com/zh/model-studio/context-cache | 隐式缓存"无需额外配置，且无法关闭"，min 1024 token
- OpenRouter | 网关透传 | https://openrouter.ai/docs/features/prompt-caching | 透传/转换上游 cache_control 与 prompt_cache_breakpoint，外加 sticky routing 和 session_id/x-session-id
