# r2-zhipu-gapfill
question: 智谱 GLM API 缓存的 TTL（能存活多久）官方文档具体怎么写？另外"命中价格是标准费率的 50%"这个折扣数字是否准确？
checked: https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://docs.bigmodel.cn/cn/guide/start/pricing

## claims
- [C1] 缓存命中的 Token 按优惠价格计费，通常为标准价格的 50% | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "缓存命中的 Token 按优惠价格计费（通常为标准价格的 50%）" | type: official
- [C2] GLM-5.3 输入价格 ¥8/百万 Tokens，缓存命中 ¥2/百万 Tokens | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "GLM-5.3 | 8 | 2" | type: official
- [C3] GLM-5.3-Flash 输入价格 ¥0.8/百万 Tokens，缓存命中 ¥0.23/百万 Tokens | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "GLM-5.3-Flash | 0.8 | 0.23" | type: official
- [C4] 缓存存储当前限时免费，本页暂不展示免费期结束后的标准价格 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "缓存存储当前限时免费。本页暂不展示免费期结束后的标准价格，后续如有调整，以页面最新信息为准" | type: official
- [C5] 调用费用 = 未命中缓存的输入费用 + 缓存命中费用 + 输出费用 + 缓存存储费用 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "调用费用 = 未命中缓存的输入费用 + 缓存命中费用 + 输出费用 + 缓存存储费用" | type: official
- [C6] 要触发上下文缓存，重复的前缀内容必须足够长，建议 500 Token 以上 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "要触发上下文缓存，重复的前缀内容必须足够长（建议 500 Token 以上）" | type: official
- [C7] 缓存为异步生效，首次请求后稍等片刻再发起后续请求效果更好 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "缓存为异步生效，首次请求后稍等片刻再发起后续请求效果更好" | type: official

## conflicts
- [CF1] C1 声称缓存命中价格"通常为标准价格的 50%"（相当于价格降至 0.5x），但 C2 和 C3 的实际定价表数据显示：GLM-5.3 缓存命中为标准输入价格的 0.25 倍（2÷8），GLM-5.3-Flash 为约 0.2875 倍（0.23÷0.8），即缓存折扣远高于 50%（接近 75% 和 71%）。缓存指南页与定价表数据不一致。

## gaps
- TTL / 缓存有效期：官方文档未提及缓存能存活多久、是否有过期时间、不活动多久被清除、能否设置或延长
- storage / 存储方式：官方文档未说明缓存存储在何处、采用什么技术、是否有存储容量限制
- invalidate / 失效条件：官方文档未说明缓存如何失效、清除条件、是否支持手动清除或设置失效规则
- scope / 隔离范围：官方文档未说明缓存是否隔离（按用户、按 API key、还是系统全局）、是否支持跨会话保持或跨用户共享

## leads
- 官方文档（缓存指南和定价页）对缓存的文档完整性有限，尤其是生命周期管理和安全隔离方面无任何说明，建议直接联系智谱技术支持以获取关于 TTL、失效机制、隔离范围的详细信息
