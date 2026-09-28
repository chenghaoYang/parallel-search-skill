# r1-openrouter
question: OpenRouter 作为网关对各上游 prompt caching 的透传/归一化行为（截至 2026-09）
checked: https://openrouter.ai/docs/features/prompt-caching, https://openrouter.ai/docs/guides/overview/auth/byok, https://openrouter.ai/docs/cookbook/administration/usage-accounting, https://openrouter.ai/docs/guides/routing/provider-selection, https://openrouter.ai/docs/llms.txt

## claims
- [C1] D1：多数上游自动启用缓存，Alibaba 与 Anthropic 需逐条消息 opt-in | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Most providers automatically enable prompt caching, but note that some (see Alibaba and Anthropic below) require you to enable it on a per-message basis." | type: official
- [C2] D1：断点标记跨上游互译 cache_control↔prompt_cache_breakpoint，TTL 不翻译 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "`prompt_cache_breakpoint` gets a default (5-minute) `cache_control` when routed to Anthropic or Google. TTLs are not translated" | type: official
- [C3] D1：Anthropic 自动缓存是 OpenRouter 侧功能——顶层 cache_control 自动置于最后可缓存块并随对话前移 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Add a single `cache_control` field at the top level of your request. The system automatically applies the cache breakpoint to the last cacheable block and advances it forward" | type: official
- [C4] D1/D7：顶层自动 cache_control 支持 Anthropic、Vertex AI、Azure、Bedrock 及 Claude Platform on AWS；Bedrock 上译为尾部断点 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "On Amazon Bedrock, OpenRouter translates the top-level field into a trailing cache breakpoint" | type: official
- [C5] D1：Anthropic 显式断点上限 4 个 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "There is a limit of four explicit breakpoints." | type: official
- [C6] D1：Responses API 不暴露 input 内 per-block cache_control，改用 prompt_cache_breakpoint（路由到 Anthropic/Google 时转默认 cache_control，无 ttl） | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Anthropic-style per-block `cache_control` inside `input` items is **not** exposed through the Responses API" | type: official
- [C7] D1：Gemini 显式缓存用 Anthropic 式断点，OpenRouter 只取最后一个；首条 system/developer 消息视为不可变整体 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "OpenRouter will use only the last breakpoint for Gemini caching across normal message content." | type: official
- [C8] D2：门槛跟随上游——OpenAI 最小 1024 tokens | src: https://openrouter.ai/docs/features/prompt-caching | quote: "There is a minimum prompt size of 1024 tokens." | type: official
- [C9] D2：Anthropic 分档 4096（Opus 4.5–4.8、Haiku 4.5）/2048（Haiku 3.5）/1024（Sonnet 4/4.5/4.6、Opus 4/4.1），不足不缓存 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Prompts shorter than these minimums will not be cached." | type: official
- [C10] D2：Gemini implicit 最小 1024（2.5 Flash）/4096（2.5 Pro）；explicit 通常 4096 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Gemini models have typically have a 4096 token minimum for cache write to occur." | type: official
- [C11] D3：Anthropic 写 1.25x（5min）/2x（1h）、读 0.1x；DeepSeek 写 1x、读 0.1x；Alibaba 写 1.25x 读 0.1x | src: https://openrouter.ai/docs/features/prompt-caching | quote: "**Cache writes (1-hour TTL)**: charged at 2x the price of the original input pricing"（页首常量 WRITE='1.25'、READ='0.1'） | type: official
- [C12] D3：OpenAI 读 0.25x 或 0.50x；GPT-5.6 起写收费 1.25x（含自动缓存），此前免费 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "GPT-5.6 and later charge cache writes at 1.25x the price of the original input pricing, even with automatic caching" | type: official
- [C13] D3/D7：Grok、Moonshot 写免费读 0.25x；Groq 读 0.5x 且仅 Kimi K2；Z.AI 读约 0.2x | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Prompt caching with Groq is automated ... Currently available on Kimi K2 models." | type: official
- [C14] D3：Gemini implicit 无写/存储费、读 0.25x；explicit 写价=输入价+5 分钟存储费 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Cache write cost = Input token price + (Cache storage price × (5 minutes / 60 minutes))" | type: official
- [C15] D3 BYOK：抽成为同模型/provider 正常价的 5%；BYOK 页未提缓存特例 | src: https://openrouter.ai/docs/guides/overview/auth/byok | quote: "**{BYOK_FEE_PERCENTAGE}% of what the same model/provider would cost normally on OpenRouter**"（常量='5'） | type: official
- [C16] D4：TTL 跟随上游不互译——Anthropic 默认 5min 可 `"ttl":"1h"`；Gemini explicit 5min 不续期、implicit 平均 3–5min；OpenAI 显式断点最低 30min | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Cache Writes have a 5 minute Time-to-Live (TTL) that does not update." | type: official
- [C17] D5：Chat Completions 报 usage.prompt_tokens_details.{cached_tokens,cache_write_tokens}；Responses 报 usage.input_tokens_details | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Cache activity is reported in `usage.input_tokens_details` (Responses) and `usage.prompt_tokens_details` (Chat Completions)" | type: official
- [C18] D5：响应体有 cache_discount，Anthropic 写可为负折扣 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "The `cache_discount` field in the response body will tell you how much the response saved on cache usage." | type: official
- [C19] D5：usage 每响应自动返回含 cost 与 cost_details.upstream_inference_cost（后者仅 BYOK 非零） | src: https://openrouter.ai/docs/cookbook/administration/usage-accounting | quote: "the `upstream_inference_cost` field is only available for BYOK (Bring Your Own Key) requests." | type: official
- [C20] D5：cache_write_tokens 仅在显式缓存+有写计费的模型返回 | src: https://openrouter.ai/docs/cookbook/administration/usage-accounting | quote: "only returned for models with explicit caching and cache write pricing" | type: official
- [C21] D6：sticky routing 把后续请求路由回同一 provider endpoint 保 cache 热，仅当读价低于普通输入价时启用 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Sticky routing only activates when the provider's cache read pricing is cheaper than regular prompt pricing" | type: official
- [C22] D6：provider 不可用则 fallback 次优；手动 provider.order 禁用 sticky；10 分钟无活动过期；sticky 报错不更新缓存、下一请求重路由 | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Sticky sessions expire after **10 minutes** of inactivity." | type: official
- [C23] D6：sticky 粒度=账户×模型×会话，默认 hash 首条 system+首条非 system 消息；session_id（body 或 x-session-id，≤256 字符）覆盖，再退化到 prompt_cache_key | src: https://openrouter.ai/docs/features/prompt-caching | quote: "If neither is set, OpenRouter falls back to the OpenAI-style `prompt_cache_key` request field as the sticky routing key." | type: official
- [C24] D6：session_id 下 sticky 在任意成功请求后即激活；无则需先观测到 cache hit | src: https://openrouter.ai/docs/features/prompt-caching | quote: "When `session_id` is set, sticky routing activates on any successful request — even before cache usage is observed" | type: official
- [C25] D7：支持上游=OpenAI、Grok、Moonshot、Groq（仅 Kimi K2）、Alibaba（deepseek-v3.2、qwen3-max、qwen-plus、qwen3.6-plus、qwen3-coder-plus、qwen3-coder-flash；快照端点不支持）、Anthropic、DeepSeek、Z.AI、Gemini（2.5+ implicit） | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Snapshot endpoints, including `qwen/qwen3.5-plus-02-15` and `qwen/qwen3.5-flash-02-23`, do not support explicit caching." | type: official

## conflicts
- 无。

## gaps
- BYOK 下缓存折扣如何计入 5% 抽成的"正常价"基数：两页均未写。
- 网关层是否另设最低门槛：页面只列上游门槛，未声明自身规则。
- 页无日期/版本标记；sticky routing 与 OpenAI explicit caching 上线时间未查 changelog。
- Anthropic :batch 同批写入不保证互见；Z.AI session affinity key；provider-selection 页称 caching beta 按模型能力自动启用。

## leads
- AWS Bedrock 原生 prompt caching（cachePoint 块、InvokeModel vs Converse）未入网格——本行只覆盖 OpenRouter 透传。
- Azure OpenAI prompt caching 未入网格；LiteLLM/Portkey/Cloudflare AI Gateway/Helicone 等同类网关透传未覆盖。
- 跨租户缓存侧信道：arXiv 2502.07776 实测 7 家 provider（含 OpenAI）全局共享缓存；OpenAI 文档称 caches 不跨 org、prompt_cache_key 做隔离计费；vLLM cache_salt（Privatemode）。
- 工具/schema 在前缀内使命中脆弱：MCP 要求 tools/list 确定性排序；GPT-5.5 起 tools 块近似原子（srcecde，二手）；Anthropic output_config schema 注入落在缓存前缀内（Medium 实测，二手）。
- arXiv 2601.06007 "Don't Break the Cache"：agentic 负载缓存失效实证。
