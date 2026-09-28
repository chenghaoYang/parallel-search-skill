# r2-zhipu
question: 智谱 GLM 开放平台的上下文缓存是否自动、要不要改请求；前缀怎么划、有没有最短长度、TTL、命中怎么计费、响应哪个字段表示命中、什么改动会失效、哪些模型可用。
checked: https://docs.bigmodel.cn/cn/guide/capabilities/cache | https://docs.bigmodel.cn/cn/guide/start/pricing | https://docs.z.ai/guides/capabilities/cache | https://docs.z.ai/guides/overview/pricing（各页均未标注发布日期，2026-09-24 抓取）

## claims
- [C1] 自动、隐式缓存，无需改请求/手动配置 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "自动缓存识别：隐式缓存，智能识别重复的上下文内容，无需手动配置" | type: official
- [C2] 命中判定基于输入消息与前请求相同内容，复用计算结果 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "上下文缓存通过对输入的消息内容进行计算并识别出与之前请求中相同内容。当检测到重复内容时，系统会复用之前的计算结果" | type: official
- [C3] 前缀需足够长才触发：建议 ≥500 Token，短系统提示词难命中 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "要触发上下文缓存，重复的前缀内容必须足够长（建议 500 Token 以上），两三句话的短系统提示词通常无法命中" | type: official
- [C4] 命中数量字段 usage.prompt_tokens_details.cached_tokens | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "详细显示缓存命中的 Token 数量，响应字段 usage.prompt_tokens_details.cached_tokens" | type: official
- [C5] 示例响应：prompt_tokens 1075 中 cached_tokens 1024（model glm-5.3） | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: ""prompt_tokens": 1075, "prompt_tokens_details": { "cached_tokens": 1024 }" | type: official
- [C6] 命中按优惠价计费，文档称通常为标准价 50%；新内容与输出按标准价 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "缓存命中 Token：按优惠价格计费（通常为标准价格的 50%）；输出 Token：按标准价格计费" | type: official
- [C7] 缓存优惠仅适用标准 API 计费，不含资源包与 GLM Coding Plan | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "仅适用于标准 API 计费，不包括资源包和 GLM Coding Plan 套餐" | type: official
- [C8] 计费公式：调用费用 = 未命中输入费 + 缓存命中费 + 输出费 + 缓存存储费；单位元/百万 Tokens | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "调用费用 = 未命中缓存的输入费用 + 缓存命中费用 + 输出费用 + 缓存存储费用" | type: official
- [C9] GLM-5.3 定价：输入 8、输出 28、缓存命中 2 元/百万 Tokens（命中价=输入价 25%） | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "GLM-5.3 | 1M | 8 | 28 | 限时免费 | 2" | type: official
- [C10] GLM-5.3-Flash：输入 0.8、输出 2.8、命中 0.23；GLM-5.3-FlashX：2/7/0.57 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "GLM-5.3-Flash | 1M | 0.8 | 2.8 | 限时免费 | 0.23 … GLM-5.3-FlashX | 1M | 2 | 7 | 限时免费 | 0.57" | type: official
- [C11] GLM-5.2 输入 8/输出 28/命中 2；GLM-5.1 <32K 命中 1.3、≥32K 命中 2 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "GLM-5.2 | 1M | 8 | 28 | 限时免费 | 2 … GLM-5.1 | 输入长度 [0, 32K) | 6 | 24 | 限时免费 | 1.3" | type: official
- [C12] 缓存存储费当前限时免费，免费期后价格未公布 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "缓存存储当前限时免费。本页暂不展示免费期结束后的标准价格" | type: official
- [C13] 支持缓存的模型以定价页"缓存命中"列为准；不支持者含 GLM-4-AirX、GLM-4-Assistant、GLM-Z1-Air/AirX/FlashX、GLM-OCR、GLM-4V-Flash、GLM-4.1V-Thinking 系列、GLM-4-Flash-250414、GLM-Z1-Flash | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "GLM-4-AirX | 8K | 10 | 10 | 限时免费 | 不支持 … GLM-OCR | 32K | 0.2 | 0.2 | 限时免费 | 不支持" | type: official
- [C14] 其他命中价：GLM-4.7 命中 0.4–0.8（分档）、GLM-4-Long 0.5、GLM-4-Plus 2.5、GLM-4.6V 0.2/0.4 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "GLM-4.7 | 输入 [0, 32K)，输出 [0, 0.2K) | 2 | 8 | 限时免费 | 0.4" | type: official
- [C15] 英文页称支持主流模型 GLM-5、GLM-4.7、GLM-4.6、GLM-4.5 系列 | src: https://docs.z.ai/guides/capabilities/cache | quote: "Supports all mainstream models, including GLM-5, GLM-4.7, GLM-4.6, GLM-4.5 series, etc." | type: official
- [C16] 英文页：相同或高度相似内容即算重复（中文页只说"相同内容"） | src: https://docs.z.ai/guides/capabilities/cache | quote: "identifying content that is identical or highly similar to previous requests" | type: official
- [C17] TTL 存在但无具体数值：过期后重新计算 | src: https://docs.z.ai/guides/capabilities/cache | quote: "Cache has reasonable time limits, will recalculate after expiration" | type: official
- [C18] 失效条件：内容须一致；细微格式差异降低命中率；相同内容命中率最高；避免频繁变更内容 | src: https://docs.z.ai/guides/capabilities/cache | quote: "Identical content has the highest cache hit rate; Minor formatting differences may affect cache effectiveness … Avoid overly frequent content changes" | type: official
- [C19] 首个建缓存请求可能略慢 | src: https://docs.z.ai/guides/capabilities/cache | quote: "First request to establish cache may be slightly slower" | type: official
- [C20] z.ai 美元定价：GLM-5.3 输入 $1.4、Cached Input $0.26（≈18.6%）、输出 $4.4/百万 tokens；存储 Limited-time Free | src: https://docs.z.ai/guides/overview/pricing | quote: "GLM-5.3 | $1.4 | $0.26 | Limited-time Free | $4.4" | type: official
- [C21] z.ai 其他：GLM-5.3-Flash $0.15/$0.03/$0.50；GLM-4.5-Air $0.2/$0.03/$1.1 | src: https://docs.z.ai/guides/overview/pricing | quote: "GLM-5.3-Flash | $0.15 | $0.03 | Limited-time Free | $0.50" | type: official
- [C22] 英文页同述 50% 示例价（与中文页一致，为示意非实际价） | src: https://docs.z.ai/guides/capabilities/cache | quote: "Cache hit tokens: Billed at discounted prices (usually 50% of standard price)" | type: official

## conflicts
- 指南页称命中价"通常为标准价格的 50%"，但定价页实际命中价为输入价 ~18–29%（GLM-5.3: 2/8=25%；z.ai $0.26/$1.4≈18.6%）。
- 中文页明确要求重复前缀 ≥500 Token；英文页未提任何最短长度。
- 中文页命中条件是"相同内容"；英文页写 "identical or highly similar"。

## gaps
- TTL 具体时长（分钟/小时）两语版本均未公布。
- 缓存作用域（按 API Key/账号/模型隔离）未说明。
- tools 定义、多模态内容是否计入前缀未说明；无 cache_control 类显式参数文档。
- 失效仅笼统描述为内容不一致/过期，无逐条失效清单。

## leads
- https://docs.z.ai/help/faq 或含 TTL/命中率细节（搜索摘要提及，未打开）。
- 定价页"更多文本模型"折叠区还有 GLM-4.5-Air、GLM-4.7-FlashX 等命中价。
- GLM Coding Plan 下命中按更低 credit 倍数计（docs.z.ai 套餐页，未详查）。
