# r1-gateway-scout
question: (1) OpenRouter作为网关，如何处理/透传各家上游模型的prompt caching——它自己有没有独立的缓存计费与语义，用户在请求里要怎么声明（如果需要的话），响应里怎么体现命中。(2)跨厂商的通用「坑」线索：怎么确认缓存命中（是否有跨厂商共性/差异）、哪些改动会打掉缓存。
checked: https://openrouter.ai/docs/guides/best-practices/prompt-caching, https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/, https://developers.openai.com/api/docs/guides/prompt-caching, https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching, https://ai.google.dev/gemini-api/docs/caching, https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching, https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html, https://openrouter.ai/docs/api-reference/chat-completion

## claims
- [C1] OpenRouter不做自己的缓存，而是透传上游厂商的缓存；"OpenRouter remembers which provider served your request and routes subsequent requests to the same provider" | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "After caching is used, OpenRouter remembers which provider served your request and routes subsequent requests to the same provider" | type: official
- [C2] OpenRouter缓存计费：OpenRouter定价中cache reads成本为0.1x–0.5x（取决于厂商），不使用原厂定价 | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "Cache reads cost significantly less than fresh tokens: Anthropic Claude: 0.1x input cost for reads; 1.25x-2.0x for writes" | type: official
- [C3] OpenRouter用户声明缓存：对Anthropic和Alibaba需显式添加`cache_control: { "type": "ephemeral" }`；OpenAI需`prompt_cache_breakpoint`；其他厂商自动缓存 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Most providers (OpenAI, DeepSeek, Groq) cache automatically. Anthropic and Alibaba require explicit cache_control markers" | type: official
- [C4] OpenRouter用户声明路由：使用`session_id`（最多256字符）在请求体或`x-session-id` header里控制sticky routing | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Use session_id (max 256 characters) in request body or x-session-id header to explicitly control routing" | type: official
- [C5] OpenRouter响应体体现缓存命中：检查`usage.prompt_tokens_details.cached_tokens`（>0表示命中），以及`cache_write_tokens` | src: https://openrouter.ai/docs/api-reference/chat-completion | quote: "cached_tokens: Cached prompt tokens from prior requests; cache_write_tokens: Tokens written to cache" | type: official
- [C6] OpenAI缓存失效条件-工具改动：工具名、描述、schema或顺序改动会导致缓存prefix失效 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Changes to tool names, descriptions, schemas, ordering, or instructions invalidate the cached prefix" | type: official
- [C7] OpenAI缓存失效条件-输出格式改动：设置`text.format`（Structured Outputs）会在prefix里添加新schema指令，导致缓存失效 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Setting text.format for Structured Outputs adds new schema instructions that break cache alignment" | type: official
- [C8] OpenAI缓存失效条件-采样参数：修改`reasoning.effort`或`text.verbosity`会改写prefix中的系统指令 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Modifying reasoning.effort can rewrite hidden system instructions; adjusting text.verbosity changes output instructions" | type: official
- [C9] OpenAI缓存最小长度：GPT-5.6及更新模型最小1024token | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later" | type: official
- [C10] Anthropic缓存失效-工具定义改动：修改工具名、描述、参数会导致整个缓存失效 | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Modifying tool names, descriptions, or parameters invalidates entire cache" | type: official
- [C11] Anthropic缓存失效-多模态内容改动：添加/删除图片到prompt任何位置都会影响message缓存块 | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Adding/removing images anywhere in prompt affects message blocks" | type: official
- [C12] Anthropic缓存失效-tool_choice改动：tool_choice参数改动仅影响message缓存块 | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Changes to tool_choice parameter only affect message blocks" | type: official
- [C13] Anthropic缓存层级失效：cache失效遵循层级模型：tools → system → messages，earlier level改动会导致后续level失效 | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "cache invalidation follows a hierarchical model: tools → system → messages. Changes at each level invalidate that level and all subsequent levels" | type: official
- [C14] Anthropic缓存breakpoint位置建议：总是把cache_control放在prefix中最后一个相同块上，而不是在变化块上 | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Always place cache_control on the last block whose prefix is identical across requests" | type: official
- [C15] Gemini隐式缓存：Gemini 2.5及更新模型默认启用隐式缓存，自动优化性能和成本，无需配置 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models" | type: official
- [C16] Gemini最小缓存长度：Gemini 2.5模型最小2048token；Gemini 3.x Flash需4096token | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Gemini 2.5 models require 2,048 tokens minimum; Gemini 3.8/3.7/3.6/3.5 Flash and 3.1 Pro require 4,096 tokens" | type: official
- [C17] Gemini隐式缓存追踪：通过`usage.total_cached_tokens`字段在API响应中追踪缓存性能 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Cache performance can be tracked via the usage.total_cached_tokens field in API responses" | type: official
- [C18] 通用缓存命中确认-跨厂商共性：所有厂商都在响应usage对象中报告缓存token数，具体字段名可能不同（cached_tokens/total_cached_tokens等） | src: https://openrouter.ai/docs/api-reference/chat-completion | quote: "cached_tokens: Cached prompt tokens from prior requests" | type: official
- [C19] Azure OpenAI与原厂差异-cache保留：不支持"Extended Prompt Cache Retention"，仅支持in-memory缓存（5-10分钟活跃，最多1小时） | src: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching | quote: "The system typically clears caches within 5 to 10 minutes of inactivity and always removes them within one hour" | type: official
- [C20] Azure OpenAI与原厂差异-breakpoint支持：仅Standard pay-as-you-go部署支持prompt cache breakpoints；PTU-M部署不支持breakpoints或expose cache_write_tokens | src: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching | quote: "Standard pay-as-you-go deployments support prompt cache breakpoints. PTU-M deployments don't support prompt cache breakpoints" | type: official
- [C21] Azure OpenAI与原厂差异-高速请求：超过约15请求/分钟且共享prefix时，部分请求可能miss缓存 | src: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching | quote: "If requests for the same prefix and prompt_cache_key combination exceed approximately 15 requests per minute, some requests might miss the cache" | type: official
- [C22] Azure OpenAI缓存最小长度：首1024token必须完全相同；之后128token粒度匹配；首1024token中单个字符差异导致cache miss | src: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching | quote: "A single character difference in the first 1,024 tokens results in a cache miss" | type: official
- [C23] AWS Bedrock支持两种缓存：Implicit（自动，无需配置）和Explicit（需用户指定cache checkpoints） | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "Amazon Bedrock supports two types of prompt caching: Implicit Prompt Caching and Explicit Prompt Caching" | type: official
- [C24] AWS Bedrock缓存TTL：Claude模型支持5分钟（默认）和1小时两种TTL | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "To use the 1-hour TTL option with supported models, specify the ttl field in your cache checkpoint" | type: official
- [C25] AWS Bedrock-Claude简化缓存管理：自动在约20个content block范围内查找最长匹配前缀，用户仅需在static content末尾放一个breakpoint | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "When you enable simplified cache management, the system automatically checks for cache hits at previous content block boundaries, looking back up to approximately 20 content blocks" | type: official
- [C26] AWS Bedrock-Anthropic缓存最小长度：Claude Opus 5需512token；Claude Sonnet 5需1024token；Claude Haiku 4.5需4096token | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "Claude Opus 5 requires at least 512 tokens per cache checkpoint; Claude Sonnet 5 requires at least 1,024 tokens; Claude Haiku 4.5 requires at least 4,096 tokens" | type: official
- [C27] AWS Bedrock-OpenAI（GPT-5.6）缓存参数：使用`prompt_cache_breakpoint`标记可缓存段末尾；支持`prompt_cache_options.mode`（implicit/explicit）控制 | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "Mark the exact end of a reusable prompt prefix by adding prompt_cache_breakpoint: {mode: explicit}" | type: official
- [C28] AWS Bedrock与OpenAI原厂差异-cache write费用：GPT-5.6 on Bedrock cache writes按1.25x uncached rate计费，reads按90%折扣计费 | src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "Cache write billing: Tokens written to cache are billed at 1.25x the uncached input token rate. Cache reads are billed at a 90% discount" | type: official
- [C29] 通用最佳实践-prompt结构：将静态或频繁重用的内容放在prompt开头，动态内容放在末尾，提高exact prefix match概率 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Place stable or repeated content at the beginning of prompts and dynamic content at the end" | type: official
- [C30] 通用最佳实践-steady stream：维持相同prefix的稳定请求流，避免自动缓存清理（通常5分钟未命中则清理） | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Prompts that aren't used regularly are automatically removed from the cache" | type: official

## conflicts
- Azure OpenAI的PTU-M部署不支持prompt_cache_breakpoint，但原生OpenAI GPT-5.6支持：[Azure](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching) vs [OpenAI](https://developers.openai.com/api/docs/guides/prompt-caching) 的部署模式差异导致功能不一致。

## gaps
- OpenRouter是否支持用户端动态指定sticky routing的provider偏好（目前文档仅说自动记住）
- OpenRouter对各厂商缓存写费用的透传/标准化处理细节
- DeepSeek官方文档中关于缓存失效条件的具体说明（目前仅知其支持自动缓存）
- Kimi/智谱/通义千问在跨厂商网关中的缓存行为差异（通常这些中文厂商文档可获得性较低）
- Google Vertex AI与原生Gemini API缓存参数命名是否完全一致

## leads
- Azure OpenAI的高速请求缓存失效（>15req/min）现象需要与其cluster routing策略关联调研；可能与load balancing导致的多endpoint问题有关
- AWS Bedrock的"simplified cache management"（自动寻找最长前缀）与OpenAI的显式breakpoint方式存在设计理念差异，值得对比研究
- Google Vertex AI文档强调"implicit caching默认启用且无存储成本"，与Azure/Bedrock的显式管理方式形成对比
- 各厂商tool/function定义改动导致缓存失效的粒度差异（是否区分名称/描述/参数/顺序）需整理对比表
- 多模态内容（图片、音频）变化时的缓存失效规则在各厂商间存在差异，需补充Bedrock/Vertex AI的具体规则
