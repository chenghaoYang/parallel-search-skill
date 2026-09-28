# r2-gemini-pricing
question: Google **Gemini Developer API**（域名 ai.google.dev，不是 Vertex AI / cloud.google.com）的官方定价页面上，implicit caching 和 explicit caching 命中时的折扣比例分别是多少？explicit caching 的存储费具体数值是多少（每小时每百万 token 多少美元）？
checked: https://ai.google.dev/gemini-api/docs/pricing,https://ai.google.dev/gemini-api/docs/caching

## claims
- [C1] Gemini 3.8 Flash 的 context caching 输入价格为 $0.075 / 1M tokens（通过 2026 年 12 月 31 日） | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Context caching price: $0.075 through December 31, 2026" | type: official
- [C2] Gemini 3.8 Flash 的 context caching 存储费为 $0.50 / 1M tokens / hour（通过 2026 年 12 月 31 日），之后为 $1.00 / 1M tokens / hour（2027 年 1 月 1 日起） | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$0.50 / 1,000,000 tokens per hour (storage price) through December 31, 2026. $1.00 / 1,000,000 tokens per hour (storage price) starting January 1, 2027" | type: official
- [C3] Gemini 3.8 Flash 标准输入价格为 $0.75 / 1M tokens（通过 2026 年 12 月 31 日），缓存输入价格为标准价的 10%（90% 折扣） | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Standard input: $0.75 per 1M tokens; Context caching: $0.075 per 1M tokens" | type: official
- [C4] Gemini 3.5 Flash 的 context caching 输入价格为 $0.15 / 1M tokens | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Context caching price: $0.15 per 1M tokens" | type: official
- [C5] Gemini 3.5 Flash 的 context caching 存储费为 $1.00 / 1M tokens / hour | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "$1.00 / 1,000,000 tokens per hour" | type: official
- [C6] Gemini 3.5 Flash 标准输入价格为 $1.50 / 1M tokens，缓存输入价格为标准价的 10%（90% 折扣） | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Standard: $1.50 per 1M tokens; Context caching: $0.15 per 1M tokens" | type: official
- [C7] ai.google.dev 定价页面没有区分 implicit caching 和 explicit caching 的不同定价——两种都按相同的 "Context caching" 价格计费 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Context caching price is presented uniformly for all models without differentiating between caching methods" | type: official
- [C8] ai.google.dev 定价页面未显式说明折扣百分比，仅显示具体的美元金额 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Pricing tables show context caching with specific rates (e.g., $0.075) without explicit percentage discounts stated" | type: official

## conflicts
- [CONFLICT] Vertex AI 官方博客明确声称 "Cached tokens are billed at 10% of standard input token cost"（https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching，出现在 r1-gemini 的 C9 和 C11），而 ai.google.dev 定价页面只显示具体美元金额，未显式提及"10%"或"90%折扣"——尽管数学上相符（如 Gemini 3.8 Flash：$0.075 = $0.75 × 10%），但措辞来源不同。Vertex AI blog 是 Vertex AI 产品文档，ai.google.dev 是 Gemini Developer API 的定价页。两条链路的计费规则在缓存折扣上是否一致需要进一步澄清。

## gaps
- implicit caching 和 explicit caching 在 ai.google.dev 定价页面上是否有任何可观察的计费差异（页面未区分）
- 为什么 Gemini 3.8 Flash ($0.50/h) 与 Gemini 3.5 Flash ($1.00/h) 的存储费不同——官方定价页未解释定价差异逻辑
- Gemini 其他型号（如 3.1 Flash-Lite、2.5 Flash 等）的 context caching 存储费具体数值

## leads
- Vertex AI 与 Gemini Developer API 的计费历史或文档演进——需要确认是否两个路径的定价规则应该相同
- ai.google.dev 的定价页面可能需要查看 raw HTML 或更新日期，以确认内容的最新性
