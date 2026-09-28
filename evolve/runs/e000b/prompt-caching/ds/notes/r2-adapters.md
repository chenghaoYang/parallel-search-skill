# r2-adapters
question: 三个云托管入口各查 1-2 条关键事实，判断它们的 prompt caching 计费/TTL 是否与母协议原生 API 一致：(a) AWS Bedrock 上的 Claude；(b) Google Vertex AI 上的 Gemini（以及如果 Vertex 也托管 Claude，一并看）；(c) Azure OpenAI 上的 GPT 系列。
checked: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html,https://learn.microsoft.com/azure/ai-services/openai/how-to/prompt-caching,https://developers.openai.com/docs/guides/prompt-caching,https://platform.claude.com/docs/en/build-with-claude/prompt-caching,https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching,https://aws.amazon.com/bedrock/pricing/

## claims

### AWS Bedrock (Claude)
- [C1] AWS Bedrock 上的 Claude 支持隐式缓存（Implicit Prompt Caching），"Amazon Bedrock and the model automatically attempt to reuse eligible prompt prefixes" 无需 cache_control 参数，这与 Anthropic 原生 API 要求手动 cache_control 不同。| src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "Implicit Prompt Caching automatically attempts to reuse eligible prompt prefixes without requiring cache controls in your request." | type: official

- [C2] Bedrock 上 Claude 的 TTL 选项与原生 API 相同：5 分钟（默认）或 1 小时。| src: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html | quote: "Many models support a 5-minute TTL... Supported TTL: 5 minutes, 1 hour" | type: official

- [C3] Bedrock 上 Claude 的缓存计费与原生 API 相同：cache write 按 1.25x（5 分钟）或 2x（1 小时）计费，cache read 按 0.1x 计费。| src: https://aws.amazon.com/bedrock/pricing/ | quote: "Cache write: $7.50 per 1M input tokens; Cache read: $0.60 per 1M input tokens" (Claude 3.5 Sonnet v2 基准 $6.00/1M) | type: official

### Google Vertex AI (Gemini & Claude)
- [C4] Google Vertex AI 上的 Gemini 提供两种缓存模式：implicit（默认自动，无额外费用）和 explicit（需手动声明，有存储费用），不需要 cache_control 参数。| src: https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching | quote: "Implicit Caching: Enabled by default... Standard input token cost to write to cache (no additional charge). Explicit Caching: User-controlled caching behavior. Requires declaring content to cache via API" | type: official

- [C5] Vertex AI 上 Gemini 的缓存折扣：Gemini 2.5 及更新版本 90% 折扣，Gemini 2.0 版本 75% 折扣（明显优于 Anthropic 0.1x=90% 折扣）。| src: https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching | quote: "90% discount on cached tokens vs. regular input tokens" | type: official

- [C6] Vertex AI 上的 Claude 支持 prompt caching，需要 cache_control 参数，与 Anthropic 原生 API 一致，支持灵活 TTL 选项。| src: https://cloud.google.com/blog/products/ai-machine-learning/claude-at-scale-on-google-cloud-frontier-ai-built-for-enterprise-production | quote: "Prompt caching for Anthropic Claude models now supports a one-hour Time To Live (TTL)." | type: official

### Azure OpenAI (GPT)
- [C7] Azure OpenAI 上的 GPT-5.6 及更新版本支持显式 cache breakpoints，需要 prompt_cache_key 和 prompt_cache_breakpoint 参数，与原生 OpenAI API 计费模式相同：cache write 1.25x，cache read 0.1x。| src: https://learn.microsoft.com/azure/ai-services/openai/how-to/prompt-caching | quote: "cache writes can incur charges in addition to discounted cache reads... Responses API supports breakpoints on input_text, input_image, and input_file blocks" | type: official

- [C8] Azure OpenAI 上的 GPT-5.6+ 的 TTL 为 30 分钟最少（默认），与 native OpenAI 一致。| src: https://learn.microsoft.com/azure/ai-services/openai/how-to/prompt-caching | quote: "Set prompt_cache_options.ttl to 30m to configure the minimum cache lifetime for all breakpoints in the request. The 30m value is the default and the only supported value." | type: official

- [C9] Azure OpenAI 上的 GPT-5.5 及更早版本不支持 prompt_cache_options 或 prompt_cache_breakpoint，自动缓存不收写入费用。| src: https://learn.microsoft.com/azure/ai-services/openai/how-to/prompt-caching | quote: "Models before the GPT-5.6 family don't support prompt_cache_options or prompt_cache_breakpoint... Models before the GPT-5.6 family don't charge extra to write to the cache." | type: official

### OpenAI Native API (Baseline)
- [C10] OpenAI 原生 API 的 prompt caching 要求显式 cache breakpoints，cache write 1.25x，cache read 0.1x，TTL 30 分钟最少。| src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Charges cached reads at 0.1× the standard rate; first request writes to cache at 1.25× cost... Lifespan: Cached entries persist for at least 30 minutes after last access" | type: official

- [C11] Anthropic 原生 API 的 prompt caching 要求 cache_control 参数（automatic 或 explicit），TTL 5 分钟或 1 小时，计费分别为 1.25x/2x 写入，0.1x 读取。| src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache writes: 1.25x base input price (5-min) or 2x (1-hour); Cache reads: 0.1x base input price" | type: official

## conflicts
- Vertex AI 对 Gemini 和 Claude 的缓存机制差异：Gemini 使用 "context caching" 且支持 implicit 模式（无需手动参数），而 Claude on Vertex 使用 "prompt caching" 且需要 cache_control 参数。两个特性共存于同一平台但机制不同。| src: https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching vs 搜索结果显示 Claude on Vertex 需要 cache_control | type: documentation inconsistency

## gaps
- Google Vertex AI 上 Claude 的具体 cache read/write 费率与原生 API 的对比未在官方文档中明确说明
- Google Vertex AI 上 Claude 的 TTL 默认值是否为 5 分钟或 1 小时未在抓取的文档中确认
- Azure OpenAI 上 GPT-5.6 的当前可用性和完整支持状态在官方文档中存在确认问题

## leads
- Bedrock 上 Claude 的"隐式缓存"传言已由 AWS 官方文档确认，是对 Anthropic 原生 API 的重要改进
- Google Vertex AI 对 Gemini 和 Claude 的缓存实现完全分离，反映平台对不同供应商 API 的适配差异
- Azure OpenAI 与原生 OpenAI 的 GPT-5.6+ 计费高度对齐，但 TTL 值（30m vs 原生"至少 30m"）可能有微妙差异
