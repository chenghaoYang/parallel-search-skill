# r1-anthropic
question: Anthropic Claude Messages API 的 prompt caching（cache_control）机制是什么样的？是否必须手动打断点？
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://claude.com/blog/prompt-caching, https://claude.com/pricing, https://platform.claude.com/docs/en/manage-claude/data-residency

## claims
- [C1] Anthropic 支持两种 cache_control 实现方式：自动缓存（在请求顶级添加 cache_control，系统自动应用缓存断点到最后一个可缓存块）和显式缓存断点（在单个内容块上放置 cache_control） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Two Implementation Methods: 1. Automatic Caching - Add cache_control at the request top level; the system automatically manages cache breakpoints 2. Explicit Cache Breakpoints - Place cache_control on individual content blocks" | type: official

- [C2] cache_control 参数格式：5分钟缓存 `{"type": "ephemeral"}`，1小时缓存 `{"type": "ephemeral", "ttl": "1h"}` | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "cache_control at the request top level; the system automatically manages cache breakpoints. 5-minute cache (default) cache_control: {\"type\": \"ephemeral\"}. 1-hour cache (2x base input token price) cache_control: {\"type\": \"ephemeral\", \"ttl\": \"1h\"}" | type: official

- [C3] 最多支持 4 个缓存断点（cache_control 参数）在一个提示中 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "You can define up to 4 cache breakpoints (using cache_control parameters) in your prompt" | type: official

- [C4] cache_control 必须放在稳定内容（系统提示、工具定义等），不能放在有时间戳或每次请求变化的内容上 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Breakpoint on unchanging content - don't mark blocks with timestamps or per-request data" | type: official

- [C5] Claude Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Fable 5：最小可缓存长度 512 tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "512 tokens: Claude Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Fable 5" | type: official

- [C6] Opus 4.8, Sonnet 5/4.6/4.5：最小可缓存长度 1,024 tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "1,024 tokens: Opus 4.8, Sonnet 5/4.6/4.5" | type: official

- [C7] Mythos Preview, Opus 4.7, Haiku 3.5：最小可缓存长度 2,048 tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "2,048 tokens: Mythos Preview, Opus 4.7, Haiku 3.5" | type: official

- [C8] Opus 4.6/4.5, Haiku 4.5：最小可缓存长度 4,096 tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "4,096 tokens: Opus 4.6/4.5, Haiku 4.5" | type: official

- [C9] 缓存命中后的读取折扣：大多数模型为基础输入价格的 0.1x（10%） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache reads: 0.1x base input token price (varies by model)" | type: official

- [C10] Claude Fable 5.1/Mythos 5.1 缓存读取折扣：0.025x（2.5%） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Claude Fable 5.1/Mythos 5.1: 0.025x" | type: official

- [C11] Claude Opus 5.5 缓存读取折扣：0.05x（5%），即 $0.20/MTok（基础 $4/MTok） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Claude Opus 5.5: 0.05x. Example for Claude Opus 5.5: Cache read $0.20/MTok" | type: official

- [C12] 5分钟缓存写入成本：基础输入价格的 1.25x（增加 25%） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "5-minute cache writes: 1.25x base input token price" | type: official

- [C13] 1小时缓存写入成本：基础输入价格的 2x（增加 100%） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "1-hour cache writes: 2x base input token price" | type: official

- [C14] Claude Opus 5.5 缓存成本示例：基础输入 $4/MTok，5分钟缓存写入 $5/MTok，1小时缓存写入 $8/MTok，缓存读取 $0.20/MTok | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Example for Claude Opus 5.5: Base input $4/MTok, 5m cache write $5/MTok, 1h cache write $8/MTok, Cache read $0.20/MTok" | type: official

- [C15] 缓存默认 TTL：5 分钟（从请求开始计时，非响应结束），可选 1 小时（成本为 2x 写入价格） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Default: 5 minutes from request start. Extended: 1 hour at 2x write cost" | type: official

- [C16] 缓存在 TTL 内被重用时无额外成本，响应生成时间计入 TTL 倒计时 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Cache refreshes at no additional cost when reused within TTL. Response generation time counts against TTL" | type: official

- [C17] 缓存失效的改动：工具定义变化、Web 搜索/引用切换、速度设置变化（工具）、工具选择变化、图像添加/删除都会导致缓存失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Changes that invalidate cache: Tool definitions ✘, Web search/citations toggle ✓, Speed setting ✓, Tool choice ✓, Images added/removed ✓" | type: official

- [C18] 缓存基于前缀精确匹配：前缀哈希必须完全相同才能命中（时间戳等变化会破坏匹配） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The timestamp changes every request, so the prefix hash never matches" | type: official

- [C19] 响应中通过 usage 对象中的三个字段表示缓存情况：cache_read_input_tokens（从缓存读取）、cache_creation_input_tokens（新写入缓存）、input_tokens（最后一个缓存断点之后的 tokens） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "usage object includes: cache_read_input_tokens: Tokens retrieved from cache, cache_creation_input_tokens: New tokens written to cache, input_tokens: Tokens after the last cache breakpoint" | type: official

- [C20] 总输入 tokens 计算公式：total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens" | type: official

- [C21] 所有活跃的 Claude 模型都支持 prompt caching（自动和显式方式） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching (automatic and explicit) is supported on all active Claude models" | type: official

- [C22] 缓存数据存储遵循 inference_geo（us 或 global）和 workspace geo 控制，Anthropic 第一方 API 仅提供 us 数据中心，workspace geo 目前仅支持 us | src: https://platform.claude.com/docs/en/manage-claude/data-residency | quote: "Workspace geo is set when you create a workspace and can't be changed afterward. Currently, 'us' is the only available workspace geo" | type: official

- [C23] AWS Bedrock 和 Google Vertex AI 上的 Claude 支持隐式 prompt caching（无需手动 cache_control），自动尝试重用符合条件的提示前缀 | src: https://www.mager.co/blog/2026-04-29-claude-prompt-caching/ (WebSearch result) | quote: "Implicit Prompt Caching automatically attempts to reuse eligible prompt prefixes without requiring cache controls in your request" | type: secondary

- [C24] Prompt caching 激活的代价：缓存写入需要通过手动添加 cache_control 参数或在 AWS Bedrock 上使用隐式模式，对 Anthropic API 需要代码修改 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Add cache_control at the request top level" | type: official

- [C25] Claude 通过 prompt caching 可实现最高 90% 成本降低和 85% 延迟减少（针对长提示） | src: https://claude.com/blog/prompt-caching | quote: "up to '90%' cost reduction and '85%' latency reduction for long prompts" | type: official

- [C26] Prompt caching 在 Anthropic API 上 2024 年 8 月 14 日作为公测发布，2024 年 12 月 17 日正式发布（GA） | src: https://www.mager.co/blog/2026-04-29-claude-prompt-caching/ (WebSearch result) | quote: "Prompt caching was introduced by Anthropic on August 14, 2024. As of December 17, 2024, prompt caching is Generally Available on the Anthropic API" | type: secondary

## conflicts
- [CF1] Claude pricing 页面提及所有模型都支持 "tiered read/write pricing"，但官方文档详细说明了模型差异化的阈值（512/1024/2048/4096 tokens）和折扣比例（0.1x 大多数，0.025x Fable/Mythos，0.05x Opus 5.5）。这表示"统一"定价在应用层有实质性差异。 | src: https://claude.com/pricing vs https://platform.claude.com/docs/en/build-with-claude/prompt-caching

## gaps
- 缓存存储的具体数据库系统/基础设施细节（何种技术实现后端存储）
- 是否支持跨账户或跨工作区的缓存共享
- 缓存在 AWS Bedrock 和 Google Vertex AI 上是否有不同的 TTL 或价格
- 单次请求的缓存容量上限（是否有最大缓存字节数或 token 数限制）
- 缓存删除/清理的手动 API 或方法
- 不同 inference_geo（us vs global）是否影响缓存策略或位置

## leads
- AWS Bedrock 上的 Claude 2025年9月引入了"简化缓存管理"功能，可能涉及自动缓存或新的管理方式，建议验证与 Anthropic API 的功能差异
- Google Vertex AI 上 Claude 的 prompt caching 与 Anthropic API 的实现差异未详细记录，需要验证定价和 TTL 是否一致
- inference_geo 参数（Claude 4.6+模型）对缓存成本的影响：US-only 推理价格为 1.1x 倍数，但文档未明确说明这是否作用于缓存写入/读取成本
