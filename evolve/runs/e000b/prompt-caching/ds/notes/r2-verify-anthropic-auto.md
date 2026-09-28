# r2-verify-anthropic-auto
question: Anthropic 官方文档提到的「Automatic Caching」（自动缓存）模式，到底比「Explicit Cache Breakpoints」（显式断点）省了多少改动？是不是真的存在，具体怎么用？
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://claude.com/blog/token-saving-updates

## claims
- [C1] Automatic Caching 确实存在，官方于 2025 年 3 月 13 日正式推出 | src: https://claude.com/blog/token-saving-updates | quote: "The updates were announced on **March 13, 2025**" | type: official
- [C2] Automatic Caching 需要在请求顶层添加单个 cache_control 字段 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Add a single `cache_control` field at the **top level** of your request" | type: official
- [C3] Automatic Caching 的系统自动将缓存断点应用于最后可缓存块 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The system automatically applies the cache breakpoint to the **last cacheable block**" | type: official
- [C4] Automatic Caching 中缓存断点在多轮对话中自动前移 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The breakpoint moves forward automatically as conversations grow" | type: official
- [C5] 完全不加 cache_control 字段则不会进行任何缓存 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching is an optional feature that requires explicit enablement" | type: official
- [C6] Automatic Caching 与 Explicit Breakpoints 对比表显示 Automatic 只需单个顶层字段，Explicit 需在各内容块上标记 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Automatic Caching: Single top-level `cache_control` / Explicit Breakpoints: `cache_control` on specific blocks" | type: official
- [C7] Automatic Caching 支持 Claude Opus 5.5, 5, Sonnet 5, Haiku 4.5 等所有现役 Claude 模型 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, 5...Claude Haiku 4.5" | type: official
- [C8] Automatic Caching 支持 Claude API、Amazon Bedrock（除旧版本）、Google Cloud Vertex AI、Microsoft Foundry、AWS 上的 Claude Platform | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Claude API ✓ / Amazon Bedrock ✓ / Google Cloud (Vertex AI) ✓" | type: official
- [C9] Automatic Caching 只使用 4 个可用缓存断点槽中的 1 个 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Max breakpoints: 1 (uses 1 of 4 available slots)" | type: official
- [C10] 2025 年 3 月 13 日发布时官方说"最小代码改动" | src: https://claude.com/blog/token-saving-updates | quote: ""available today to all Anthropic API customers" with "minimal code changes" required" | type: official

## conflicts
- [无冲突] 两个官方文档对 Automatic Caching 的描述一致：platform.claude.com/docs 详细说明了机制，claude.com/blog 说明了发布日期和"最小改动"的说法

## gaps
- 官方文档未明确对比 OpenAI、DeepSeek 等其他厂商的缓存机制
- 官方文档未明确说明 Automatic Caching 在 Google Cloud Vertex AI 上的具体行为是否与 Anthropic API 完全一致
- 官方文档中 cache_control 字段的 JSON 格式示例显示 `{"type": "ephemeral"}` 或 `{"type": "ephemeral", "ttl": "1h"}`，但未明确说明在 Python SDK 中是否必须用字典、还是支持其他语法糖

## leads
- AWS Bedrock 是否真的支持 Automatic Caching（C8 说"✓"，但之前 grid 中 Bedrock 旧版本有限制），需 AWS 官方文档确认
- 该功能在 Google Cloud Vertex AI 上的具体可用性和定价是否与原生 Anthropic API 一致
