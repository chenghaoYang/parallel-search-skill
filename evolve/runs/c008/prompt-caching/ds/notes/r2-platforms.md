# r2-platforms
question: 三个托管平台（AWS Bedrock / Azure OpenAI / Vertex AI）prompt caching 各一行级事实（机制形态、上游语义、计费/字段差异）+ OpenRouter BYOK 缓存计费官方说明
checked: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html, https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching, https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview, https://ai.google.dev/gemini-api/docs/caching, https://openrouter.ai/docs/guides/best-practices/prompt-caching, https://openrouter.ai/docs/features/byok, https://openrouter.ai/docs/cookbook/administration/usage-accounting

## claims

### (a) AWS Bedrock
- [C1] Bedrock 分隐式+显式两种；显式在 Converse API 用 `cachePoint` 块（可放 `system`/`messages`/`tools`），Claude 走 InvokeModel 时沿用上游 `cache_control: {"type":"ephemeral"}` | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "Amazon Bedrock supports two types of prompt caching: Implicit Prompt Caching and Explicit Prompt Caching" + `"cachePoint" : { "type": "default", "ttl" : "5m | 1h" }` | type: official
- [C2] 显式缓存支持 Claude 全系（每 checkpoint 最小 512–4,096 token，最多 4 个）；Amazon Nova 对所有 text prompt 默认隐式缓存（部分 Nova 模型卡标注支持显式 checkpoint）；OpenAI GPT-5.6 在 Responses API 用 `prompt_cache_breakpoint` | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "Amazon Nova offers Implicit Prompt Caching for all text prompts, including `User` and `System` messages." | type: official
- [C3] TTL 默认 5 分钟、命中即刷新，较新 Claude 可选 `"ttl": "1h"`；Converse 响应 usage 新增 `cacheReadInputTokens`/`cacheWriteInputTokens`/`cacheDetails`，且 `inputTokens` 只计未缓存部分；读按 cache-read 价、写可高于标准输入价 | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "the `inputTokens` field represents only the non-cached input tokens (tokens that were not read from or written to the cache)" | type: official
- [C4] Bedrock 上 Anthropic 模型有"简化缓存管理"：只放 1 个 checkpoint，系统回溯约 20 个 content block 找最长命中前缀 | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "the system automatically checks for cache hits at previous content block boundaries, looking back up to approximately 20 content blocks from your specified breakpoint" | type: official

### (b) Azure OpenAI
- [C5] 默认自动开启（无需参数），要求 ≥1,024 token 且首 1,024 token 完全相同；命中字段与 OpenAI 相同：`prompt_tokens_details.cached_tokens`；GPT-5.6+ 另报 `cache_write_tokens` | src: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching | quote: "Cache hits show up as `cached_tokens` under `prompt_tokens_details` in the chat completions response."（ms.date 2026-08-11）| type: official
- [C6] GPT-5.6+ 增加显式 `prompt_cache_breakpoint`（Responses 和 Chat Completions 均支持）与 `prompt_cache_options.mode`（implicit/explicit）、`ttl` 仅支持 `30m`；旧模型传这些参数返回 400 | src: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching | quote: "Models before the GPT-5.6 family don't support `prompt_cache_options` or `prompt_cache_breakpoint`. Requests that include these parameters return a `400` error." | type: official
- [C7] 保留策略：in-memory 默认（无活动 5–10 分钟清除、至多 1 小时）；GPT-5.5 及更早部分模型可 `prompt_cache_retention: "24h"` 扩展至最多 24 小时；所有 GPT-4o 或更新模型支持 in-memory | src: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching | quote: "The system typically clears caches within 5 to 10 minutes of inactivity and always removes them within one hour of the cache's last use." | type: official
- [C8] 计费：cache 读按输入折扣价；GPT-5.6 之前写缓存免费，GPT-5.6+ 写可收费；PTU-M 部署不支持 breakpoint 且不暴露 `cache_write_tokens` | src: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching | quote: "Models before the GPT-5.6 family don't charge extra to write to the cache. On GPT-5.6 models and later model families, cache writes can incur charges" | type: official

### (c) Vertex AI context caching
- [C9] 双机制：implicit 默认开启（命中 90% 折扣）+ explicit `CachedContent` 资源经 Gemini Enterprise API 显式创建/按 resource name 引用/可更新删除，默认 TTL 60 分钟 | src: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview | quote: "Explicit caching: Manual caching enabled using the Gemini Enterprise API, where you explicitly declare the content you want to cache" | type: official
- [C10] 显式读折扣：Gemini 2.5+ 为 90%、Gemini 2.0 为 75%；支持 Gemini 2.5/3.x 系列（含 fine-tuned 模型） | src: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview | quote: "On Gemini 2.5 or later models, this discount is 90%; on Gemini 2.0 models, this discount is 75%." | type: official
- [C11] 计费与字段：建缓存的输入 token 按标准输入价计；显式缓存另按时长收存储费，隐式无存储费；命中数以响应 metadata 的 `cachedContentTokenCount` 返回 | src: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview | quote: "For explicit caching, there are also storage costs based on how long caches are stored. There are no storage costs for implicit caching." | type: official
- [C12] 与 Gemini API（AI Studio 侧）关系：对象模型同构（同为显式 cache 对象、generateContent 引用），AI Studio 侧 implicit 同样默认开启、命中字段 `usage.total_cached_tokens`；Vertex 侧差异在 GCP  endpoint、VPC-SC、存储计费 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models" | type: official

### (d) OpenRouter BYOK
- [C13] OpenRouter 缓存命中字段统一为 `prompt_tokens_details.cached_tokens` / `cache_write_tokens`，另有响应级 `cache_discount`；用 provider sticky routing 保缓存命中，可传 `session_id` | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "The `cache_discount` field in the response body will tell you how much the response saved on cache usage." | type: official
- [C14] BYOK 无缓存专属计费/字段说明：BYOK 页只讲 5% 手续费与免费额度，prompt-caching 页不提 BYOK；唯一官方交叉点：`upstream_inference_cost` 经 generation ID 查询时仅 BYOK 请求可用 | src: https://openrouter.ai/docs/cookbook/administration/usage-accounting | quote: "the `upstream_inference_cost` field is only available for BYOK (Bring Your Own Key) requests. For all other requests it will be 0 or null." | type: official

## conflicts
- 无实质冲突。命名差异：Bedrock Converse 用 `cachePoint`、Claude InvokeModel 用上游 `cache_control`；Azure/GPT-5.6 用 `prompt_cache_breakpoint` —— 同一断点概念三套字段名（非矛盾）。

## gaps
- AI Studio（Gemini API 开发者侧）显式缓存的存储计费单价未核实（本次只开了 implicit caching 页，generateContent caching 页未取）。
- Bedrock Nova 显式 checkpoint 的字段/最小 token 需逐模型卡确认（总表只列了 Claude 与 GPT-5.6）。
- OpenRouter BYOK 下 `cache_discount`/`cache_write_tokens` 语义是否与 credit 计费一致，官方无说明。

## leads
- Bedrock 页新增 OpenAI GPT-5.6 on Bedrock 显式缓存（`prompt_cache_breakpoint`、30min TTL、写 1.25x/读 0.1x），与 Azure 侧同构——值得成稿时对照。
- OpenRouter 支持 Anthropic `cache_control` 与 OpenAI `prompt_cache_breakpoint` 互转路由（per prompt-caching 指南）。
