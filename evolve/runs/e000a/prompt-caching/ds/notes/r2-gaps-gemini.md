# r2-gaps-gemini
question: Gemini 隐式缓存（implicit caching）的存活时间/TTL 和失效条件是什么？官方文档有没有明确说明？哪些改动会导致 cache miss（如 model 版本变化、system_instruction 变化、请求间隔等）？

checked: https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/api/caching, https://ai.google.dev/gemini-api/docs/optimization, https://ai.google.dev/gemini-api/docs/caching.md.txt, https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/, https://discuss.ai.google.dev/t/have-anyone-checked-out-the-implicit-caching-for-gemini-api-caches-hits-are-inconsistent-for-me/82666, https://huggingface.co/arshjaved/gemini-docs/blob/main/text_content/docs_caching_eeebb99e.txt

## claims
- [C1] 官方 Google 回应明确说隐式缓存的 TTL 无法定义且没有保证 | src: https://discuss.ai.google.dev/t/have-anyone-checked-out-the-implicit-caching-for-gemini-api-caches-hits-are-inconsistent-for-me/82666 | quote: "For implicit context caching we cannot define the TTL and also there is no guarantee TTL time for implicit context caching" | type: official

- [C2] 隐式缓存失效条件之一：系统提示中的动态内容（如时间戳）变化会导致缓存失效 | src: https://discuss.ai.google.dev/t/have-anyone-checked-out-the-implicit-caching-for-gemini-api-caches-hits-are-inconsistent-for-me/82666 | quote: "including timestamps in the system prompt caused cache misses since the content changed with each request" | type: official

- [C3] 隐式缓存自动启用于所有 Gemini 2.5 及更新版本模型 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models" | type: official

- [C4] 隐式缓存需要最少 token 数量才能触发：Gemini 2.5 Flash/Pro 需 2,048 个；Gemini 3.x Flash 需 4,096 个 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Gemini 2.5 Flash/Pro: 2,048 tokens minimum" | type: official

- [C5] ai.google.dev 主页面、generate-content 页面、caching.md.txt 均未记载隐式缓存具体 TTL 数值 | src: https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/gemini-api/docs/caching.md.txt | quote: "The documentation doesn't specify an automatic expiration time for implicit caching" | type: official

- [C6] Google 官方建议隐式缓存用户改用显式缓存以获得 TTL 保证 | src: https://discuss.ai.google.dev/t/have-anyone-checked-out-the-implicit-caching-for-gemini-api-caches-hits-are-inconsistent-for-me/82666 | quote: "Users requiring guaranteed cache behavior should use explicit caching instead" | type: official

## conflicts
- WebSearch 结果显示第三方教程声称隐式缓存 TTL 为"5 分钟"或"24 小时"（来源：theneuralbase.com, aifreeapi.com），但这些非官方文档来源与 Google 官方论坛回应"无法定义 TTL、无保证"的说法矛盾；未找到官方确认这些数值。

## gaps
- 官方文档（ai.google.dev、Google Cloud Blog、Google Cloud Docs）均未发布隐式缓存的具体 TTL 数值、计时方式（LRU vs 绝对时间）或重置机制
- 隐式缓存的完整失效条件清单不完整（已知：系统提示动态变化导致失效；未知：model 版本变化、请求间隔时长、其他参数改变是否导致失效）
- 缓存后续每次命中是否重置 TTL 计时器的官方说明缺失

## leads
- Google Cloud 官方 Vertex AI 文档可能有补充信息，但需完整页面（https://docs.cloud.google.com/vertex-ai/... 因重定向未完全获取）
- discuss.ai.google.dev 论坛可能有更多工程师回应澄清细节（已查的帖子聚焦于一个用户案例）
