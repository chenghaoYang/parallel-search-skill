# r2-openrouter-billing
question: OpenRouter 对上游厂商的 prompt caching，计费上是原价透传还是会加价？「粘性路由」（sticky routing）是所有上游模型都有，还是只对特定厂商生效？
checked: https://openrouter.ai/docs/faq, https://openrouter.ai/docs/guides/best-practices/prompt-caching, https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/

## claims
- [C1] OpenRouter 在推理计费上不加价，透传上游价格 | src: https://openrouter.ai/docs/faq | quote: "We pass through the pricing of the underlying providers; there is no markup on inference pricing" | type: official
- [C2] OpenRouter 在 credit 购买时收取 Stripe 手续费 5.5%，但推理价格无加价 | src: https://openrouter.ai/docs/faq | quote: "however we do charge a fee when purchasing credits" | type: official
- [C3] Sticky routing 不是对所有上游都无条件激活，而是有条件的自动激活 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "only activates when the provider's cache read pricing is cheaper than regular prompt pricing" | type: official
- [C4] Sticky routing 应用于 OpenRouter 的 70+ 提供商 | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "Sticky routing applies across OpenRouter's 70+ providers" | type: official
- [C5] Sticky sessions 10分钟无活动后失效，每次成功请求重置计时器 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Sticky sessions expire after 10 minutes of inactivity. Each successful request resets the timer." | type: official
- [C6] 如果 sticky provider 返回错误，缓存不更新，允许下次请求重新路由 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "If the sticky provider returns an error, the cache is not updated, allowing the next request to be re-routed." | type: official
- [C7] 用户手动指定 provider.order 时会覆盖 sticky routing | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "if you set provider.order yourself, your order wins over sticky routing" | type: official
- [C8] Sticky provider 不可用时自动 fallback 到下一个可用提供商 | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "when that sticky provider becomes unavailable, OpenRouter falls back to the next available provider" | type: official
- [C9] OpenRouter 不自己做缓存，只路由请求到上游提供商实现缓存 | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "OpenRouter does not cache content itself. Instead, it routes your subsequent requests to the same provider endpoint to help upstream providers maximize their cache hits." | type: official
- [C10] 缓存位置在各上游 endpoint，不同 endpoint 无法访问彼此的缓存 | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "Caches are provider-specific: they reside on the endpoint where initially written and cannot be accessed by other provider endpoints." | type: official

## conflicts
- 无

## gaps
- Sticky routing 是否对 OpenAI、DeepSeek、Gemini、Anthropic 等全部上游都生效，还是有厂商不支持（文档说"70+ providers"但未逐一列举哪些厂商满足"cache read pricing < regular pricing"条件）
- OpenRouter 自身的网络路由层是否有任何缓存机制（文档明确说不做内容缓存，但未说是否有其他形式的优化）

## leads
- AWS Bedrock Claude 隐式缓存（未在 R1 深入验证）
- Vertex AI Gemini/Claude 缓存价格是否与原生一致（需确认是否也是透传）
- Azure OpenAI 缓存是否与原生一致
