# prompt-caching 任务参考答案

给人工检查者用的简明答案，对应 task.md 里用户提出的疑问。核实日期：2026-09-24。

## 1. "OpenAI 和 DeepSeek 是自动缓存、不用改代码" —— 现在还是这样吗？

**部分不准确了。** DeepSeek 仍然是纯自动（硬盘缓存对所有用户默认开启，不用改代码）。但 OpenAI 从 GPT-5.6 开始，除了原有的隐式/自动缓存之外，**新增了开发者可手动放置的显式 cache breakpoint**（一次请求最多 4 个写入点），行为上开始向 Anthropic 靠拢。GPT-5.6 之前的模型仍然只支持隐式缓存。
来源：https://developers.openai.com/api/docs/guides/prompt-caching ；https://api-docs.deepseek.com/guides/kv_cache

## 2. "Anthropic 必须手动打 cache_control 断点" —— 现在还是这样吗？

**也不完全准确了。** Anthropic 现在多了一种"自动"用法：只需在请求顶层加一次 `cache_control`，系统会自动把断点挪到最后一个可缓存块，随对话增长自动前移；如果要精细控制哪些内容块被缓存，仍然可以在具体 content block 上手动打点（最多 4 个断点）。所以手动打点不再是唯一方式，但仍然是可选项。
来源：https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching

## 3. 命中之后各家怎么计费？

- **OpenAI（GPT-5.6+）**：写入 1.25× 标准输入价，命中读取 0.1×（更早模型没有写入费，命中价按模型而定）。
- **Anthropic**：5 分钟 TTL 写入 1.25×，1 小时 TTL 写入 2×；命中读取都是 0.1×。
- **Gemini**：官方只说"自动把成本节省转嫁给你"（automatically pass on cost savings），未在缓存文档页给出统一折扣比例，需查具体模型定价页。
- **DeepSeek**：定价页会区分 CACHE HIT / CACHE MISS 两档单价（例如 deepseek-flash 峰值期 cache miss $0.3/M vs cache hit $0.006/M），还叠加了峰谷时段价差，命中价通常是未命中价的几十分之一。
- **Kimi（Moonshot）**：kimi-k3 命中读取是未命中价格的 1/10（例如 $3.00/M miss vs $0.30/M hit），写入按 5 分钟或 1 小时 TTL 分两档（$3.00 / $6.00 每 1M）。
- **通义千问（DashScope）**：显式缓存创建按标准价 125% 计费、命中 10%；隐式缓存命中按标准价约 20% 计费（不同来源模型比例略有差异）。
来源：https://developers.openai.com/api/docs/guides/prompt-caching ；https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching ；https://api-docs.deepseek.com/quick_start/pricing ；https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api ；https://help.aliyun.com/zh/model-studio/context-cache
（注意：具体价格数字变动较快，检查时建议以当天的定价页为准。）

## 4. 缓存能活多久（TTL）？

- **OpenAI**：GPT-5.6+ 默认最短 30 分钟（`prompt_cache_options.ttl`，目前只支持 `30m`）；更早模型的隐式缓存通常闲置 5–10 分钟失效，最长可留到 1 小时，也有 24 小时的扩展保留档位。
- **Anthropic**：默认 5 分钟，可选加钱换 1 小时（`"ttl": "1h"`）。
- **Gemini**：隐式缓存没有用户可配置的 TTL（系统自动管理）；显式 `CachedContent` 资源可以自己设置 TTL。
- **Kimi**：不指定 `prompt_cache_options` 时默认 5 分钟 TTL，可选 1 小时。
- **通义千问**：显式缓存有效期 5 分钟，命中后会重置计时。
来源同上。

## 5. 怎么确认命中了缓存？（各家响应字段）

- **OpenAI**：`usage.input_tokens_details.cached_tokens`（另有 `cache_write_tokens`）。
- **Anthropic**：`usage.cache_read_input_tokens` / `usage.cache_creation_input_tokens` / `usage.input_tokens`。
- **Gemini**：`usage.total_cached_tokens`（Python/JS SDK 字段名）。
- **DeepSeek**：`usage.prompt_cache_hit_tokens` / `usage.prompt_cache_miss_tokens`。
- **通义千问**：OpenAI 兼容模式看 `usage.prompt_tokens_details.cached_tokens`，Anthropic 兼容模式看 `usage.cache_read_input_tokens`。
- **OpenRouter**：`usage.prompt_tokens_details.cached_tokens`，另外响应体里有 `cache_discount` 字段直接告诉你省了多少钱。
来源：https://developers.openai.com/api/docs/guides/prompt-caching ；https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching ；https://api-docs.deepseek.com/guides/kv_cache ；https://help.aliyun.com/zh/model-studio/context-cache ；https://openrouter.ai/docs/features/prompt-caching

## 6. 哪些改动会让缓存失效？

- **OpenAI**：改 `model`、`tools`（名称/描述/schema/顺序）、`parallel_tool_calls`、`text.format`、`reasoning.effort`、`text.verbosity`、上下文压缩（compaction）都可能让前缀不再匹配；核心原则是"改动点之前的内容必须完全一致才能复用"。
- **Anthropic**：改工具定义会让整份缓存失效；开关 web search / citations、切换 speed 档位会让 system 和 message 级缓存失效；加/删图片只影响 message 块。缓存分工具→系统→消息三层，改动上层会连带下层一起失效。
- **DeepSeek**：新请求的前缀必须与已缓存的"前缀单元"完全匹配，否则算未命中（例如第一轮缓存的是 A+B，第二轮变成 A+C 就无法命中）。
来源：https://developers.openai.com/api/docs/guides/prompt-caching ；https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching ；https://api-docs.deepseek.com/guides/kv_cache

## 7. 起码 4 家之外：Kimi、通义千问、OpenRouter 等有什么不同？

- **Kimi（Moonshot）**：这次查到的文档已经改成和 OpenAI 类似的 `prompt_cache_options` 自动缓存机制（默认 5 分钟 TTL），和早期"必须先调 `/v1/caching` 显式建缓存对象"的旧模式不同——文档域名也从 moonshot.cn/moonshot.ai 重定向到了 platform.kimi.ai，看起来是做了一次品牌/API 改版。
- **通义千问（DashScope）**：一个平台提供三种缓存模式且互斥——隐式缓存（自动、不可关、命中按 ~20% 计费）、显式缓存（手动创建、5 分钟 TTL、创建 125%/命中 10%）、会话缓存（给 Responses API 用，加请求头 `x-dashscope-session-cache: enable` 即可，计费规则和显式缓存一致）。隐式缓存最小公共前缀 1024 token（阿里云上部署的智谱 GLM、MiniMax 模型是 512）。
- **OpenRouter**：把各家的缓存行为原样透传给你——大多数供应商（含 OpenAI、DeepSeek）在 OpenRouter 上是自动缓存，但 Anthropic、通义千问等仍需要你自己在消息里加 `cache_control` 才会命中；响应里统一用 `usage.prompt_tokens_details.cached_tokens` 和 `cache_discount` 字段回报命中和省下的钱。
来源：https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api ；https://help.aliyun.com/zh/model-studio/context-cache ；https://openrouter.ai/docs/features/prompt-caching

## 备注：智谱（Zhipu GLM）

本次没有直接抓到智谱官方的缓存文档页（预算内没有单独核实），只在阿里云百炼文档里看到一句旁证："智谱部署的GLM...模型为512"（指 GLM 在阿里云上的隐式缓存最小 token 门槛），这是阿里云的说法而非智谱自己的文档，检查时不要当成智谱官方结论，需要单独核实 https://docs.bigmodel.cn 上的说法。
