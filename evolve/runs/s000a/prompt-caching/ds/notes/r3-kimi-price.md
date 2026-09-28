# r3-kimi-price
question: Kimi 定价表 kimi-k3 行各列表头是什么？¥20/¥40/¥2/¥20 的映射？「命中=未命中 1/10」是否覆盖 K2？K2 有无缓存写入价？
checked: https://platform.kimi.com/docs/pricing/chat ; https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api

## claims
- [C1] K3 表头顺序为：模型 / 计费单位 / 缓存写入（TTL 5min）/ 缓存写入（TTL 1h）/ 输入价格（缓存命中）/ 输入价格（缓存未命中）/ 输出价格 / 上下文窗口 | src: https://platform.kimi.com/docs/pricing/chat | quote: "{ title: \"缓存写入（TTL 5min）\" },{ title: \"缓存写入（TTL 1h）\" },{ title: \"输入价格（缓存命中）\" },{ title: \"输入价格（缓存未命中）\" },{ title: \"输出价格\" }" | type: official
- [C2] kimi-k3 行按列序：¥20.00=缓存写入(TTL 5min)，¥40.00=缓存写入(TTL 1h)，¥2.00=输入(缓存命中)，¥20.00=输入(缓存未命中)，¥100.00=输出 | src: https://platform.kimi.com/docs/pricing/chat | quote: "[\"kimi-k3\", \"1M tokens\", \"¥20.00\", \"¥40.00\", \"¥2.00\", \"¥20.00\", \"¥100.00\", \"1,048,576 tokens\"]" | type: official
- [C3] 指南计费表同样给出：Cache Write（`1h`）= ¥40/1M tokens | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "| Cache Write（`1h`）  | ¥40" | type: official
- [C4] 指南计费表：Cached Input（缓存命中）= ¥2/1M tokens | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "| Cached Input（缓存命中） | ¥2" | type: official
- [C5] 指南计费表：Input（缓存未命中）= ¥20/1M tokens | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "| Input（缓存未命中）       | ¥20" | type: official
- [C6] 「命中价为未命中 1/10」原文以 kimi-k3 为例表述 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "以 `kimi-k3` 为例，缓存命中价格仅为未命中价格的 **1/10**" | type: official
- [C7] K2 表无缓存写入列，列仅为 模型/计费单位/输入价格（缓存命中）/输入价格（缓存未命中）/输出价格/上下文窗口；k2.7-code 命中 ¥1.30、未命中 ¥6.50 | src: https://platform.kimi.com/docs/pricing/chat | quote: "[\"kimi-k2.7-code\", \"1M tokens\", \"¥1.30\", \"¥6.50\", \"¥27.00\", \"262,144 tokens\"]" | type: official
- [C8] 计费逻辑称缓存写入单独计费仅针对 K3 系列 | src: https://platform.kimi.com/docs/pricing/chat | quote: "对于 K3 系列模型，缓存写入按 TTL 档位（5min / 1h）单独计费；缓存命中的输入仅按缓存命中价格计费" | type: official

## conflicts
- 指南泛称「缓存命中价格是缓存未命中价格的 1/10」，但 K2 表实际比值不符：k2.7-code ¥1.30/¥6.50=1/5，k2.6 ¥1.10/¥6.50≈1/5.9，highspeed ¥2.60/¥13.00=1/5。指南句以「以 kimi-k3 为例」限定，是否覆盖 K2 不裁决。

## gaps
- K2 是「无缓存写入费」还是「写入含在输入价内」页面未明说；K2 的 TTL 档位/写入行为未列。

## leads
- https://platform.kimi.com/docs/llms.txt ；指南页 usage 字段表（cache_write_tokens / cache_creation_input_tokens）。
