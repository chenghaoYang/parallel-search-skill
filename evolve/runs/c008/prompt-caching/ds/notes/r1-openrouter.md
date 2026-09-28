# r1-openrouter
question: (a) OpenRouter 对 prompt caching 的处理：cache_control 透传、计费、usage 字段、路由对命中的影响；(b) scout：其他厂商与用户易踩的坑
checked: https://openrouter.ai/docs/features/prompt-caching, https://openrouter.ai/docs/guides/best-practices/prompt-caching, https://openrouter.ai/api/v1/models, https://openrouter.ai/docs/api/api-reference/generations/get-request-&-usage-metadata-for-a-generation, https://openrouter.ai/docs/faq, https://openrouter.ai/anthropic/claude-sonnet-4.5

## claims
- [C1] OpenRouter 文档未声称自建缓存；缓存由上游 provider 提供，OpenRouter 做标记格式翻译+粘性路由（定向再取证实页面未说明缓存物理存储方）。| src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "you can enable prompt caching on supported providers and models" | type: official
- [C2] Anthropic 风格 cache_control 在 Anthropic 兼容 provider 间透传，并跨厂商翻译成 OpenAI prompt_cache_breakpoint / Bedrock 格式。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Explicit per-block `cache_control` breakpoints work across all Anthropic-compatible providers including Bedrock and Vertex." | type: official
- [C3] 双向翻译规则：cache_control→prompt_cache_breakpoint，反向则补默认 5 分钟 cache_control。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "a block marked with `prompt_cache_breakpoint` gets a default (5-minute) `cache_control` when routed to Anthropic or Google" | type: official
- [C4] TTL 不做翻译：发向 OpenAI 时 cache_control 的 ttl 被丢弃。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "TTLs are not translated — a `cache_control` `ttl` is dropped toward OpenAI" | type: official
- [C5] Bedrock 路由时顶层 cache 字段被翻译为尾部 breakpoint。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "On Amazon Bedrock, OpenRouter translates the top-level field into a trailing cache breakpoint" | type: official
- [C6] OpenAI/DeepSeek 等为自动缓存无需配置；Gemini 2.5+ 用 implicit caching；OpenAI explicit 缓存仅 GPT-5.6+ 支持。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Prompt caching with OpenAI is automated and does not require any additional configuration." | type: official
- [C7] Anthropic 自动缓存支持 Anthropic/Vertex/Azure/Bedrock 四个 provider。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "is supported on the **Anthropic**, **Google Vertex AI**, **Azure**, and **Amazon Bedrock** providers" | type: official
- [C8] D4 计费按上游倍数透传：OpenAI 读 0.25x/0.50x、写 1.25x(GPT-5.6+)；Anthropic 写 1.25x(5min)/2x(1h)、读 0.1x；DeepSeek 读 0.1x；Gemini/Grok/Moonshot 读 0.25x；Groq 读 0.5x；Alibaba 写 1.25x 读 0.1x；Z.AI 写免费(限时)读 ~0.2x。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "(depending on the model) charged at 0.25x or 0.50x the price of the original input pricing" | type: official
- [C9] OpenRouter 对推理不加价，收入靠购额手续费 5.5%(最低$0.80；crypto 5%)；缓存折扣即上游折扣透传。 | src: https://openrouter.ai/docs/faq | quote: "We pass through the pricing of the underlying providers; there is no markup on inference pricing." | type: official
- [C10] Models API 的 pricing 对象列出缓存价格字段 input_cache_read / input_cache_write / input_cache_write_1h（实测 anthropic/claude-opus-5.5）。 | src: https://openrouter.ai/api/v1/models | quote: "\"input_cache_read\": \"0.0000002\", \"input_cache_write\": \"0.000005\", \"input_cache_write_1h\": \"0.000008\"" | type: official
- [C11] D5 命中字段：Chat Completions 在 usage.prompt_tokens_details，Responses API 在 usage.input_tokens_details；字段 cached_tokens(读命中) 与 cache_write_tokens(写入)。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Cache activity is reported in `usage.input_tokens_details` (Responses) and `usage.prompt_tokens_details` (Chat Completions)" | type: official
- [C12] 响应体有 cache_discount 字段表示缓存节省金额；Anthropic 类 provider 写缓存时为负折扣、读为正折扣。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "The `cache_discount` field in the response body will tell you how much the response saved on cache usage." | type: official
- [C13] Generation API GET /api/v1/generation?id=… 返回 cache_discount("Discount applied due to caching")、native_tokens_cached("Native cached tokens as reported by provider")、native_tokens_prompt、upstream_inference_cost、total_cost。 | src: https://openrouter.ai/docs/api/api-reference/generations/get-request-&-usage-metadata-for-a-generation | quote: "cache_discount — Discount applied due to caching; native_tokens_cached — Native cached tokens as reported by provider" | type: official
- [C14] D6-8 命中依赖路由：OpenRouter 粘性路由把后续请求送回同一 provider 保缓存。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Subsequent requests for the same model are routed to the same provider, keeping your cache warm." | type: official
- [C15] 手动 provider.order 关闭粘性路由（显式顺序优先），换 provider 即缓存 miss。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Sticky routing is not used when you specify a manual provider order via `provider.order`" | type: official
- [C16] 粘性键：默认按「首条 system/developer + 首条非 system 消息」哈希识别会话；session_id(≤256字符)直接作键；否则回退 prompt_cache_key。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "identifies conversations by hashing the first system (or developer) message and the first non-system message" | type: official
- [C17] 粘性会话 10 分钟无活动过期；仅在 provider 缓存读价低于普通 prompt 价时启用；无 session_id 时须先检测到命中才激活；sticky provider 不可用时回退次优 provider(会 miss)。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Sticky sessions expire after 10 minutes of inactivity. Each successful request resets the timer." | type: official
- [C18] 最小 token 门槛：OpenAI 1024；Anthropic 按模型 4096(Opus4.5-4.8/Haiku4.5)/2048(Haiku3.5)/1024(Sonnet4系)；Gemini 1024(Flash)/4096(Pro)。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Prompts shorter than these minimums will not be cached." | type: official
- [C19] breakpoint 上限 4 个(Anthropic)；Gemini 只用最后一个 breakpoint；Responses API 不接受逐块 cache_control，需 prompt_cache_breakpoint 且不带 TTL。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "There is a limit of four explicit breakpoints." | type: official
- [C20] Gemini implicit 缓存 TTL 平均 3-5 分钟且读命中不刷新；写=input价+5分钟存储费；cached tokens 计入模型上下文上限。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "the TTL is on average 3-5 minutes, but will vary" | type: official
- [C21] 二手佐证：第三方网关 Bifrost 的修复 PR 证实 OpenRouter /v1/responses 不接受逐块 cache_control，须用 prompt_cache_breakpoint，且转 Anthropic 时超 4 个会 400。 | src: https://github.com/maximhq/bifrost/pull/6692 | quote: "OpenRouter's `/v1/responses` endpoint does not accept per-block `cache_control`; the documented equivalent is `prompt_cache_breakpoint`" | type: secondary

## conflicts
- 无官方文档间冲突。唯一张力：openrouter.ai 模型网页（JS 渲染）未在抓取中显示缓存价格行，但 models API 明确返回 input_cache_read/write 字段——视为渲染差异非矛盾。

## gaps
- OpenRouter 是否在任何路径自建/存储缓存（如自家存储层）：文档未明说，现有描述全部指向上游 provider 缓存。已定向再取一次确认页面无此表述。
- 网页版模型详情页是否展示 cache read/write 价格行：页面 JS 渲染，WebFetch 拿不到定价表；API 侧已确认字段存在。
- BYOK（自带 key）场景下缓存计费与字段是否一致：未查到专门说明。

## leads
- AWS Bedrock 原生 prompt caching（Claude/Nova，checkpoint 数与 min tokens 按模型而异）——范围内候选。
- Azure OpenAI prompt caching（自动、o 系/GPT 系）——范围内候选。
- Vertex AI Gemini explicit context caching（显式 cache 对象+存储计费）vs implicit——与 OpenRouter 路径不同，值得单列。
- xAI Grok、Moonshot、Groq、Z.AI、Alibaba Qwen 均有缓存（OR 页已列折扣）；Mistral 是否有 prompt caching 未确认，待查。
- 用户易踩的坑：前缀顺序敏感（断点前任何改动使整段失效）；tools/system 变更击穿缓存；min-token 门槛(1024/2048/4096)；TTL 不随读刷新(Gemini 5min)；写溢价>单次读节省；Anthropic 4 断点上限；provider.order/多 provider 路由导致 miss；Responses API 须用 prompt_cache_breakpoint 而非 cache_control；cached tokens 仍占上下文窗口(Gemini)；latency 收益主要是 TTFT 而非总时长。
- 未入网格的维度：缓存对输出内容无影响(纯输入侧)；与 batch 交互(Bedrock「one line 写的缓存不保证对其他 line 可见」)；缓存存储计费(Gemini)；会话粘性粒度(账户×模型×会话)；可观测性双通道(inline usage vs /generation API)；BYOK 下缓存行为。
