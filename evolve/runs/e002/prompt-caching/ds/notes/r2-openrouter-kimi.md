# r2-openrouter-kimi
question: (1) OpenRouter official docs明确说「不对缓存命中/写入加价、原样转发上游价格」吗？(2) Kimi缓存存储介质及每请求缓存断点数上限官方文档是否提到？
checked: https://openrouter.ai/docs/guides/best-practices/prompt-caching, https://openrouter.ai/docs/features/prompt-caching, https://openrouter.ai/pricing, https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api, https://platform.kimi.ai/docs

## claims
- [C1] OpenRouter official docs详列各提供商缓存计费：Anthropic缓存写1.25x、读0.1x；DeepSeek读0.1x；Google/Moonshot/Grok读0.25x；OpenAI reads 0.25x-0.5x | src: https://openrouter.ai/docs/features/prompt-caching | quote: "Cache writes (5-minute TTL): charged at 1.25x the price" (Anthropic example) | type: official
- [C2] OpenRouter文档未明确声称「不对缓存加价」或「原样转发上游价格」，仅列出各提供商的计费倍数；未披露OpenRouter自身是否添加加成 | src: https://openrouter.ai/docs/features/prompt-caching | quote: N/A (absence of statement) | type: official
- [C3] OpenRouter pricing页面未提供缓存相关的计费细节，仅指"Prompt Caching"在Standard/Business/Enterprise方案中可用 | src: https://openrouter.ai/pricing | quote: "Prompt Caching" available in certain plans | type: official
- [C4] Kimi API缓存文档未提及存储介质（内存或磁盘） | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: N/A (not mentioned) | type: official
- [C5] Kimi缓存无手动「断点」概念，系统自动匹配前缀（longest prefix matching），TTL默认5分钟或可选1小时 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "automatically reuses the cached content" (automatic prefix matching, no manual breakpoints) | type: official
- [C6] Kimi缓存命中需前一请求prompt tokens≥256 | src: https://platform.kimi.ai/docs (API Overview) | quote: "cache entries only when previous request's prompt tokens exceed 256" | type: official

## conflicts
- OpenRouter文档在缓存计费的透明度上未直接阐述其自身的加成政策，仅罗列提供商费率，对应原问题中「不对缓存加价」的核查结论是：官方文档未见此明确声明。

## gaps
- OpenRouter官方文档是否存在其他页面（如/docs/pricing、/docs/billing、/docs/api-overview）明确说明不对缓存操作收取加成？已查三个主要页面，未找到此表述。
- Kimi缓存存储架构（内存/磁盘/混合）官方文档未涉及，是否有单独的技术架构文档、常见问题（FAQ）或架构设计文档页面？已查/docs和缓存特性页，未见。
- Kimi是否有概念上的「每请求缓存断点数上限」？文档表明缓存为自动前缀匹配，无手动断点设置，此结论基于current understanding，但未直接反证「不存在」。

## leads
- OpenRouter关于缓存无加成政策的论据仅来自iqilian.com（第三方）；官方页面未明确该声明，仅展示provider-level pricing，可能需补充查询OpenRouter客服或API文档其他部分。
- Kimi的缓存架构细节（存储位置）未在官方公开文档中披露，可能需查阅非公开技术文档或向官方咨询。
