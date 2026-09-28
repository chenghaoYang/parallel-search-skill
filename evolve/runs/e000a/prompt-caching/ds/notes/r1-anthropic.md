# r1-anthropic
question: Anthropic Claude API 的 prompt caching（cache_control）机制在当前（2026年）的现状——是否仍需手动打断点、断点数量上限、门槛、计费、TTL、命中确认字段、失效条件、支持范围
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/about-claude/pricing, https://platform.claude.com/docs/en/release-notes/overview, https://platform.claude.com/docs/en/api/messages/create, https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics, https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching, https://platform.claude.com/docs/en/about-claude/models/overview

## claims
- [C1] 两种触发方式并存：自动缓存（top-level cache_control，系统自动管理断点）和显式断点（放在内容块上） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Add a single cache_control field at the top level of your request. The system automatically applies the cache breakpoint to the last cacheable block" | type: official
- [C2] 自动缓存在 2026 年 2 月 19 日推出，推翻了「必须手动打断点」的传言 | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "Automatic Caching (February 19, 2026)" | type: official
- [C3] 单次请求最多 4 个 cache_control 断点，超过时返回 400 错误 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Maximum: 4 cache breakpoints per request. If 4 explicit breakpoints exist, automatic caching returns a 400 error" | type: official
- [C4] 最小可缓存长度按模型分档：Fable 5.1/Mythos 5.1/Opus 5.5/Opus 5/Fable 5/Mythos 5 需 512 tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Claude Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Fable 5, Mythos 5: **512**" | type: official
- [C5] 最小可缓存长度：Opus 4.8/Sonnet 5/Sonnet 4.6/Sonnet 4.5/Opus 4.1/Opus 4 需 1,024 tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Claude Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5, Opus 4.1, Opus 4: **1,024**" | type: official
- [C6] 最小可缓存长度：Haiku 4.5 需 4,096 tokens、Opus 4.7 需 2,048 tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Claude Haiku 4.5: **4,096**; Claude Opus 4.7: **2,048**" | type: official
- [C7] cache_control 字段可放在 system (TextBlockParam)、messages 内容块、tools 数组最后一个工具上 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Place cache_control directly on individual content blocks for fine-grained control over exactly what gets cached" | type: official
- [C8] 缓存基于前缀匹配（prefix），非语义匹配，系统最多向后 20 个位置查找匹配缓存条目 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "The system checks **up to 20 positions** backward per breakpoint looking for matching cache entries from prior requests" | type: official
- [C9] 命中计费：0.1x base input price（标准模型）、0.025x（Fable 5.1/Mythos 5.1）、0.05x（Opus 5.5） | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "Cache hits and refreshes: 0.025x on Claude Fable 5.1 and Claude Mythos 5.1; 0.05x on Claude Opus 5.5; 0.1x on other models" | type: official
- [C10] 建缓存写入价格：5 分钟 1.25x base input price，1 小时 2x base input price | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "5-minute cache write: 1.25x base input price; 1-hour cache write: 2x base input price" | type: official
- [C11] TTL 有两档：默认 5 分钟（5m），可选 1 小时（1h）via cache_control.ttl 字段 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Default: 5-minute ephemeral cache; Extended: 1-hour cache available at 2x write cost" | type: official
- [C12] TTL 从请求开始计算，响应生成时间消耗 TTL，缓存命中时刷新并继承原 TTL | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Measured from the start of the request that writes or reads the cache entry. Response generation time counts against the lifetime" | type: official
- [C13] 响应 usage 对象字段：cache_read_input_tokens 存储从缓存读取的 token 数 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "\"cache_read_input_tokens\": 1800, // Tokens retrieved from cache" | type: official
- [C14] 响应 usage 对象字段：cache_creation_input_tokens 存储写入缓存的 token 数 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "\"cache_creation_input_tokens\": 248, // Tokens written to cache" | type: official
- [C15] 工具定义变化导致整个缓存失效，系统与消息缓存失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Tool definitions: ✘ Entire cache invalidated" | type: official
- [C16] web search/citations toggle、speed setting(fast/normal)变化导致系统和消息缓存失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Web search/citations toggle: System & message caches invalidated; Speed setting: System & message caches invalidated" | type: official
- [C17] 添加/移除 images、tool_choice 变化、thinking parameters 变化导致消息缓存失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Images (add/remove anywhere): Message cache invalidated; Tool choice changes: Message cache invalidated; Thinking parameters: Message cache invalidated" | type: official
- [C18] effort setting 变化导致消息缓存失效（部分模型同时影响 tool/system 缓存） | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Effort setting changes: Message cache invalidated" | type: official
- [C19] 消息被编辑/重新排序/删除（而非追加）导致消息缓存失效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "messages_changed: an earlier entry in messages was altered, reordered, or removed rather than appended to" | type: official
- [C20] 缓存作用域限于组织和工作区，跨 API key 共享但不跨组织/工作区 | src: https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics | quote: "Fingerprints are scoped to your organization and workspace" | type: official
- [C21] 缓存按模型隔离，不同模型无法命中同一缓存条目 | src: https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics | quote: "model_changed: The cache is per-model" | type: official
- [C22] 所有活跃 Claude 模型都支持 prompt caching，包括 Fable 5.1、Opus 5.5、Sonnet 5、Haiku 4.5 等 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching supported on: All active Claude models" | type: official
- [C23] Prompt caching 在 Claude API 中默认开启，不需要额外开通或特殊请求头 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Place cache_control directly on individual content blocks for fine-grained control over exactly what gets cached" | type: official
- [C24] 自动缓存在 Amazon Bedrock 旧版本（Opus 4.6 及更早）不可用，仅支持显式断点 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Automatic caching not available on legacy Bedrock (Opus 4.6 and earlier)—use explicit breakpoints instead" | type: official
- [C25] 缓存诊断功能（cache-diagnosis-2026-04-07 beta header）可识别 cache miss 原因 | src: https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics | quote: "Cache diagnostics closes that gap. Pass the id of your previous response, and the API compares the two requests" | type: official
- [C26] 同一请求内可混合不同 TTL，较长 TTL 需放在前面来优先生效 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Mixed TTLs: Use both in same request if longer TTL appears first" | type: official
- [C27] 服务器工具（web search/web fetch/code execution）使用时，API 自动在服务器工具结果后放置 cache breakpoint，使用默认 5 分钟 TTL | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching | quote: "the API automatically places a cache breakpoint on the server tool result before running the next iteration of the agentic loop" | type: official
- [C28] cache_control 字段格式为 {"type": "ephemeral", "ttl": "5m"} 或 {"type": "ephemeral", "ttl": "1h"}，ttl 可选默认 5m | src: https://platform.claude.com/docs/en/api/messages/create | quote: "cache_control: {\"type\": \"ephemeral\", \"ttl\": \"5m\"} // or \"1h\"" | type: official
- [C29] 建缓存的请求只收一次写入费用，后续命中请求每次收读取费用（最快一次回本） | src: https://platform.claude.com/docs/en/about-claude/pricing | quote: "A cache hit costs 10% of the standard input price, which means caching pays off after one cache read for the 5-minute duration" | type: official
- [C30] 工具缓存时 cache_control 放在工具数组最后一个工具的对象上，缓存整个工具定义前缀 | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching | quote: "Place cache_control on the last tool in your tools array. This caches the entire tool-definitions prefix" | type: official

## conflicts
- 无发现的直接冲突。不同官方文档页间对缓存机制的描述保持一致。

## gaps
- D9 存储介质（内存 vs 磁盘）：文档未明确说明缓存存储在服务端内存还是磁盘上
- D9 地域限制：无信息表明缓存是否有地域限制或需要指定数据中心
- D11 支持范围：Bedrock/Google Cloud/AWS Marketplace 上是否需要特殊配置或有功能差异（仅提及自动缓存在 Bedrock 旧版不可用）

## leads
- Cache miss reason 诊断可按类型分类（model_changed、system_changed、tools_changed、messages_changed 等），文档有详细矩阵可参考故障排查
- 缓存与 Batch API 折扣可叠加，详见 Batch processing 页
- Extended thinking 和 fast mode 会影响缓存决策，需单独查询相关页面确认交互
