# r1-scout
question: 在 OpenAI / Anthropic / Gemini / DeepSeek / OpenRouter 之外，还有哪些厂商的 API 提供 prompt caching 或上下文缓存，官方文档 URL 是什么；用户最容易踩的、且网格还没列的坑或维度是什么。
checked: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching, https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html, https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview, https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api, https://www.alibabacloud.com/help/en/model-studio/context-cache, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://docs.volcengine.com/docs/82379/1398933, https://docs.x.ai/developers/advanced-api-usage/prompt-caching, https://docs.fireworks.ai/guides/prompt-caching, https://platform.minimax.cn/docs/api-reference/text-prompt-caching, https://console.groq.com/docs/prompt-caching, https://docs.mistral.ai/studio/conversations/advanced/prompt-caching

## claims
- [C1] Azure OpenAI（Microsoft Foundry）有官方 prompt caching 文档；默认启用，最低 1,024 tokens 且前 1,024 tokens 必须一致，命中体现在 prompt_tokens_details.cached_tokens（页面 ms.date 2026-08-11） | src: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching | quote: "A minimum of 1,024 tokens in length. The first 1,024 tokens in the prompt must be identical." | type: official
- [C2] Azure 在 GPT-5.6 及以后模型支持 prompt_cache_key、prompt_cache_breakpoint、prompt_cache_options（mode implicit/explicit、ttl 仅 30m）；PTU-M 部署不支持断点 | src: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching | quote: "Standard pay-as-you-go deployments support prompt cache breakpoints. Provisioned Throughput managed (PTU-M) deployments don't support prompt cache breakpoints." | type: official
- [C3] Azure prompt cache 不跨订阅共享；extended retention 最长 24 小时仅限列出的模型 | src: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching | quote: "The system doesn't share prompt caches between Azure subscriptions." | type: official
- [C4] Amazon Bedrock 官方文档同时有 Implicit 与 Explicit prompt caching；显式用 cachePoint（Converse）/ cache_control（InvokeModel），TTL 常见 5 分钟、部分模型 1 小时；不支持 batch inference | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "Prompt caching is only supported for on-demand inference endpoints. It is not supported with the batch inference API." | type: official
- [C5] Vertex AI（Gemini Enterprise Agent Platform）context caching 分 implicit（项目默认开启、命中 90% 折扣、无存储费）与 explicit（cachedContents 资源、默认 60 分钟 TTL、有存储费）（页面 Last updated 2026-09-22） | src: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview | quote: "Implicit caching: Automatic caching enabled by default... Explicit caching: Manual caching enabled using the Gemini Enterprise API" | type: official
- [C6] Kimi/Moonshot 官方文档为上下文缓存（隐式自动前缀匹配）；Chat Completions/Responses 用 prompt_cache_options（mode 仅 implicit，ttl 5m/1h），Anthropic Messages API 用顶层 cache_control；缓存按组织隔离 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "缓存按组织（org）隔离：同一组织内共享，组织之间不共享。缓存不支持手动清除" | type: official
- [C7] 智谱 BigModel 有官方「上下文缓存」文档页；隐式自动、无需配置，命中价通常为标准价 50%，建议重复前缀 >500 Token，缓存异步生效 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "自动缓存识别：隐式缓存，智能识别重复的上下文内容，无需手动配置" | type: official
- [C8] 阿里云百炼/DashScope 官方 Context Cache 页含显式（cache_control ephemeral、5 分钟、单请求≤4 个标记、创建 125%/命中 10%）与隐式（自动不可关、命中约 20%、≥1024 tokens），两种模式互斥；Responses API 另有 Session cache | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "Explicit cache and implicit cache are mutually exclusive." | type: official
- [C9] 火山引擎方舟（豆包）官方「上下文缓存」页：隐式自动不可关（默认最小 1024 tokens，部分模型 2048/8960/256）；显式仅 Responses API，分前缀缓存与 Session 缓存，经 previous_response_id 引用，expire_at 最长 7 天且存储按自然小时计费（页面更新 2026.09.22） | src: https://docs.volcengine.com/docs/82379/1398933 | quote: "当前最大可存储时间为 7 天...存储费用在缓存创建时即产生，直到该缓存被手动删除或过期后停止计费" | type: official
- [C10] xAI 官方 prompt caching 文档：自动前缀缓存，建议设 x-grok-conv-id 头（Chat Completions）或 prompt_cache_key（Responses API）提高命中 | src: https://docs.x.ai/developers/advanced-api-usage/prompt-caching | quote: "The xAI API performs prompt caching automatically. However, we recommend setting the x-grok-conv-id HTTP header to maximize your cache hit rate." | type: official
- [C11] Fireworks 官方 prompt caching 文档：默认开启、serverless 命中默认 50% 折扣；缓存是 replica-local，需 user 字段或 x-session-affinity 头做亲和；有 x-prompt-cache-isolation-key 隔离键 | src: https://docs.fireworks.ai/guides/prompt-caching | quote: "Prompt caching only works within 1 replica... you can send us a unique identifier for each user or session" | type: official
- [C12] MiniMax 官方文档：被动/自动缓存 ≥512 输入 tokens，前缀按「工具定义-系统提示词-历史对话」顺序构建；另有 Anthropic 兼容的主动缓存（cache_control、5 分钟、≤4 断点） | src: https://platform.minimax.cn/docs/api-reference/text-prompt-caching | quote: "缓存适用于包含 512 个及以上的输入 token 数量的 API 调用；缓存采用前缀匹配的方式，以「工具定义-系统提示词-历史对话内容」为顺序构建" | type: official
- [C13] Groq 官方 prompt caching 文档：全自动不可关闭、无额外费用、命中输入 50% 折扣、2 小时无使用过期；当前仅 openai/gpt-oss-20b、120b、safeguard-20b 三个模型支持 | src: https://console.groq.com/docs/prompt-caching | quote: "Prompt caching is automatically enabled and cannot be manually disabled." | type: official

## conflicts
- 无直接冲突。注意：智谱官方页称命中价「通常为标准价格的 50%」，而搜索结果称 GLM-5.3 命中价 2 元/M vs 输入 8 元/M（即 25%），需下一轮以 open.bigmodel.cn/pricing 核实。

## gaps
- Mistral 官方页（docs.mistral.ai/studio/conversations/advanced/prompt-caching）抓取只返回标题（疑 JS 渲染）；搜索摘要称有 prompt_cache_key、64-token 块、命中价 10%，均未证实。
- Together AI（docs.together.ai/docs/serverless/overview 的 Cached input 价格列）、SiliconFlow（docs.siliconflow.com + 官方博客称自动前缀缓存）未打开官方页确认。
- 百川、讯飞星火：搜索摘要称官方 API 文档无缓存内容，本轮未亲自打开验证。
- Kimi 早期显式缓存 API（POST /v1/caching、role=cache 消息、moonshot-v1）只见于搜索摘要，platform.kimi.com 新文档页只讲 implicit，是否仍维护未确认。
- Vertex 页缓存限制表格（最小 token 数等）渲染为空，具体数值未取到。

## leads
- Azure OpenAI | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching | 自动前缀 + 请求内断点（GPT-5.6 起） | prompt_cache_breakpoint 与 OpenAI 官方参数是否逐字段对齐？
- Amazon Bedrock | https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | 请求内断点 + 隐式（按模型分列） | 非 Anthropic/Nova 模型（如 Llama）是否也有缓存？
- Vertex AI | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview | 隐式 + 显式缓存资源（cachedContents） | 显式缓存最小 token 与存储单价？
- Kimi/Moonshot | https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | 自动前缀（implicit only，ttl 5m/1h） | 旧 /v1/caching 显式 API 现状？
- 智谱 BigModel | https://docs.bigmodel.cn/cn/guide/capabilities/cache | 自动前缀 | 命中价是否随模型变（50% vs 25%）？
- 通义/百炼 DashScope | https://www.alibabacloud.com/help/en/model-studio/context-cache | 自动前缀 + 请求内断点 + Session 缓存（Responses） | Session cache 的计费与 TTL 细节？
- 火山方舟/豆包 | https://docs.volcengine.com/docs/82379/1398933 | 自动前缀 + 显式缓存资源（previous_response_id，存 7 天） | Chat API 是否也支持显式缓存？
- xAI | https://docs.x.ai/developers/advanced-api-usage/prompt-caching | 自动前缀 + 路由亲和（x-grok-conv-id） | 缓存 TTL/逐出承诺？
- Fireworks | https://docs.fireworks.ai/guides/prompt-caching | 自动前缀 + 会话亲和头 | dedicated 共享缓存的租户隔离语义？
- MiniMax | https://platform.minimax.cn/docs/api-reference/text-prompt-caching | 自动前缀 + Anthropic 显式断点 | OpenAI 兼容接口能否用主动缓存？
- Groq | https://console.groq.com/docs/prompt-caching | 自动前缀（仅 gpt-oss 系） | 何时扩展到 Llama/Qwen 等模型？
- Mistral | https://docs.mistral.ai/studio/conversations/advanced/prompt-caching | 疑似自动前缀 + prompt_cache_key（未取到正文） | 用 Playwright/其他 UA 重取确认 64-token 粒度与 10% 价
- Together AI | https://docs.together.ai/docs/serverless/overview | 疑似自动前缀 + 按模型 cached 价（未打开） | 哪些模型有 Cached input 价格列？
- SiliconFlow | https://docs.siliconflow.com/en/api-reference/chat-completions/chat-completions | 疑似自动前缀（未打开） | 官方页是否列出 cached_tokens 与支持模型？

坑/新维度 leads（均来自已打开页面）：
- 坑：Bedrock 缓存不支持 batch inference；Kimi 流式需 stream_options.include_usage=true 才见缓存明细；百炼 batch（file input）调用不享受缓存折扣 →「非实时/批量路径是否适用缓存」维度。src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html ; https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api ; https://www.alibabacloud.com/help/en/model-studio/context-cache
- 坑：显式断点普遍存在「回看窗口」——Bedrock/百炼约 20 个 content block、Azure 读最多 50 个断点；并行 tool_calls 会产生大量独立消息使标记超出窗口 →「断点回看窗口/消息块计数」维度。src: https://www.alibabacloud.com/help/en/model-studio/context-cache ; https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
- 坑：缓存作用域与隔离各异——Kimi 按 org 共享、Azure 不跨订阅、Fireworks dedicated 默认共享单缓存（计时攻击风险，需 isolation key）、Groq volatile-only →「缓存隔离/共享边界」维度。src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api ; https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching ; https://docs.fireworks.ai/guides/prompt-caching
- 坑：存储费只在部分厂商存在——Vertex 显式缓存按时长收存储费、火山显式缓存按自然小时收存储费（不足 1h 按 1h），而隐式普遍免费 →「写入费 vs 存储费」维度。src: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview ; https://docs.volcengine.com/docs/82379/1398933
- 坑：一致性约束影响命中——火山显式缓存要求 thinking 各轮一致、instructions 为空、tools 只能首轮设置、启用缓存时不支持 json_schema（只支持 json_object）→「缓存×结构化输出/thinking 交互」维度。src: https://docs.volcengine.com/docs/82379/1398933
- 坑：最小前缀门槛差异极大（128~8960 tokens，Groq 128-1024 按模型、火山 glm-5-3-flash 8960、智谱建议 500+）且命中不保证；智谱明示缓存异步生效（首发请求后稍等）→「门槛+异步生效」维度。src: https://docs.volcengine.com/docs/82379/1398933 ; https://docs.bigmodel.cn/cn/guide/capabilities/cache ; https://console.groq.com/docs/prompt-caching
