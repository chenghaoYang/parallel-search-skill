# r1-cn-b

question: (A) 阿里云通义千问 / DashScope（百炼）API 的上下文缓存机制，(B) OpenRouter 网关如何处理上游厂商的 prompt caching。10个维度对比。

checked: help.aliyun.com/zh/model-studio/context-cache, www.alibabacloud.com/help/zh/model-studio/context-cache, help.aliyun.com/zh/model-studio/model-pricing, help.aliyun.com/zh/model-studio/qwen-api-via-dashscope, openrouter.ai/docs/guides/best-practices/prompt-caching, openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/, www.layer3labs.io/guides/openrouter-pricing, iqilian.com/learn/openrouter-api-jifei/, openrouter.ai/pricing

## claims

### 通义千问/DashScope

- [C1] D1 显式缓存需手动声明（cache_control: ephemeral），隐式缓存自动开启 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "显式缓存需要主动为指定内容创建缓存"、"隐式缓存功能自动开启，无需修改代码" | type: official
- [C2] D2 最小可缓存长度 1,024 tokens | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "最少需要 1024 个 Token 的相同前缀" | type: official
- [C3] D3 粒度为 content block 级，显式缓存marker 与后续内容间隔不超过 20 个 content blocks | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "向后前缀匹配范围不超过20个content block" | type: official
- [C4] D4 命中读取计费：显式缓存 10%，隐式缓存 20% | src: https://help.aliyun.com/zh/model-studio/model-pricing | quote: "显式缓存...命中按 10% 计费"、"隐式缓存...按输入 Token 标准单价的 20% 计费" | type: official
- [C5] D5 写入计费：显式缓存创建 125%，隐式缓存包含于正常计费 | src: https://help.aliyun.com/zh/model-studio/model-pricing | quote: "显式缓存创建按标准输入单价的 125% 计费" | type: official
- [C6] D6 TTL：显式缓存 5 分钟（命中时重置），隐式缓存系统定期清理 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "显式缓存有效期为 5 分钟"、"隐式缓存系统会定期清理" | type: official
- [C7] D7 命中确认字段：cached_tokens、cache_creation_input_tokens | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "usage.prompt_tokens_details (cached_tokens, cache_creation_input_tokens)" | type: official
- [C8] D8 显式缓存失效条件：content blocks 间隔超 20、TTL 内无命中则过期；隐式缓存系统定期清理 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "向后前缀匹配范围不超过20个content block"、"有效期为 5 分钟" | type: official
- [C9] D9 适用模型：Qwen Flash (qwen3.8-flash, qwen3.7-flash)、Qwen Max/Plus、DeepSeek、Kimi、GLM 等 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "Qwen Max/Plus/Flash...DeepSeek...Kimi...GLM" | type: official
- [C10] D10 存储介质/隔离：账户级隔离（同一账户内不同模型间也隔离） | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "无论隐式还是显式缓存，数据都在账号级别隔离，不会共享。缓存数据存在模型间隔离" | type: official

### OpenRouter

- [C11] D1 OpenRouter 完全依赖上游厂商缓存支持，自身无独立缓存决策，通过 sticky routing 路由到同一端点维持缓存 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "After a cached request, OpenRouter routes subsequent requests to the same provider endpoint" | type: official
- [C12] D4/D5 OpenRouter 在网关层不加价，原样转发上游的缓存读取折扣和写入费用 | src: https://iqilian.com/learn/openrouter-api-jifei/ | quote: "OpenRouter...平台不对模型调用加价" | type: secondary
- [C13] D6 OpenRouter 遵循上游 TTL，默认 5 分钟，文档指出由上游提供商决定 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Anthropic's default is 5 minutes, with a 1-hour option for longer sessions" | type: official
- [C14] D7 OpenRouter 响应中保留上游缓存字段：cached_tokens、cache_write_tokens（在 usage.prompt_tokens_details 中） | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "usage object includes prompt_tokens_details showing cached_tokens: tokens read from cache, cache_write_tokens: tokens written to cache" | type: official
- [C15] D9 OpenRouter 列出支持缓存的上游：Anthropic Claude（require explicit cache_control）、Google Gemini 2.5（implicit）、OpenAI（automatic）、DeepSeek（automatic）等 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Anthropic Claude...Google Gemini 2.5...OpenAI...DeepSeek" | type: official
- [C16] D8/D2/D3/D10 ∅ 未提及 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | note: OpenRouter 文档未单独说明网关层的失效条件、最小长度、粒度、存储隔离，这些由上游提供商决定 | type: official

## conflicts
- 无

## gaps
- OpenRouter 文档未明确说明是否在 session_id 之外还有其他网关层缓存管理机制
- DashScope 隐式缓存的具体 TTL 数值（文档说「定期清理」但无明确周期）
- DashScope 是否支持 Anthropic 兼容的 cache_control 字段或仅支持自有 API 格式

## leads
- OpenRouter 的 sticky routing session_id 机制对缓存命中至关重要，需要理解 10 分钟会话过期的影响
- DashScope 的隐式缓存成本结构（20% 读取、无写入费用）与显式缓存（125% 写入、10% 读取）的选择需根据使用模式判断
- 两者都支持多模型调用，但隔离策略不同（DashScope 账户级+模型级，OpenRouter 上游依赖）
