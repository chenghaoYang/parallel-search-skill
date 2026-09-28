# r2-zhipu
question: 智谱 GLM 官方上下文/prompt 缓存的 D1–D10。若存在与隐式缓存不同的显式或命名缓存，分开写主张，不要并成一句。
checked: https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://docs.bigmodel.cn/cn/guide/capabilities/cache.md, https://docs.bigmodel.cn/cn/guide/start/pricing, https://docs.bigmodel.cn/cn/best-practice/latency-optimization, https://docs.bigmodel.cn/cn/guide/capabilities/thinking-mode, https://docs.bigmodel.cn/cn/coding-plan/overview, https://docs.bigmodel.cn/cn/guide/develop/responses/introduction, https://docs.bigmodel.cn/cn/guide/models/text/glm-z1, https://docs.bigmodel.cn/cn/guide/models/sound-and-video/glm-realtime, https://docs.bigmodel.cn/cn/update/new-releases.md, https://docs.bigmodel.cn/api-reference/模型-api/对话补全, https://docs.bigmodel.cn/openapi/openapi.json, https://docs.bigmodel.cn/openapi/openapi-en.json, https://docs.bigmodel.cn/openapi/openapi-responses.json, https://docs.bigmodel.cn/llms.txt

## claims
- [C1] D1 隐式：官方把上下文缓存写成自动识别、无需手动配置。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "自动缓存识别：隐式缓存，智能识别重复的上下文内容，无需手动配置" | type: official
- [C2] D1/D3：触发靠足够长的重复前缀；建议 500 Token 以上，两三句短系统提示词通常不命中。这是建议不是硬下限。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "要触发上下文缓存，重复的前缀内容必须足够长（建议 500 Token 以上），两三句话的短系统提示词通常无法命中。" | type: official
- [C3] D1：示例要求系统提示词完全一致、只改用户问题；第一次请求注释为建立缓存且 cached_tokens 为 0。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "系统提示词保持完全一致，只有用户问题变化。" | type: official
- [C4] D1/D9：该示例为 POST `https://open.bigmodel.cn/api/paas/v4/chat/completions`，`model` 为 `glm-5.3`。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "curl --location 'https://open.bigmodel.cn/api/paas/v4/chat/completions'" | type: official
- [C5] D2 隐式：匹配对象是输入消息里与先前请求相同的内容，不是命名 cache id。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "上下文缓存通过对输入的消息内容进行计算并识别出与之前请求中相同内容。" | type: official
- [C6] D2：稳定内容放前部；后部变化不影响前面固定内容复用。 | src: https://docs.bigmodel.cn/cn/best-practice/latency-optimization | quote: "前半部分在多次请求中保持稳定，更容易被缓存复用；后半部分虽然每次变化，但不会影响前面固定内容的复用效果。" | type: official
- [C7] D4 对话补全：命中字段 `usage.prompt_tokens_details.cached_tokens`，类型 number，描述为命中缓存 Token 数。未见单独 miss/write 字段。 | src: https://docs.bigmodel.cn/openapi/openapi.json | quote: "命中的缓存 `Token` 数量" | type: official
- [C8] D4 示例：一次响应 `prompt_tokens` 1075、`cached_tokens` 1024。文档未把 1024 写成块大小。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "\"prompt_tokens\": 1075" | type: official
- [C9] D5/D6 标准 API 公式含四项：未命中输入、缓存命中、输出、缓存存储。无单独「缓存写入」项。 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "调用费用 = 未命中缓存的输入费用 + 缓存命中费用 + 输出费用 + 缓存存储费用" | type: official
- [C10] D5 能力页：新内容与输出按标准价；命中「通常为标准价格的 50%」。示例用 0.01 与 0.005 元/1K。该段声明不含资源包和 Coding Plan。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "缓存命中 Token：按优惠价格计费（通常为标准价格的 50%）" | type: official
- [C11] D5/D6/D9 定价表（元/百万 Tokens）：GLM-5.3 输入 8、输出 28、缓存存储限时免费、缓存命中 2、上下文 1M、文本。存储列单位是元/百万 Tokens/小时。 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "GLM-5.3 | 1M | 8 | 28 | 限时免费 | 2 | 文本" | type: official
- [C12] D5 同表另有命中价（非 50% 或另档）：GLM-5.3-Flash 0.23（输入 0.8）、FlashX 0.57（输入 2）；GLM-5.2 命中 2；GLM-5.1 为 1.3（输入 [0,32K)）与 2（≥32K）；GLM-5-Turbo 1.2/1.8；GLM-5 1/1.5；GLM-4.7 为 0.4、0.6、0.8；GLM-4.5-Air 0.16/0.16/0.24；GLM-4.7-FlashX 0.1；GLM-4-Plus 2.5（输入 5）；GLM-4-Air-250414 0.25；GLM-4-Long 0.5；GLM-4-FlashX-250414 0.05；GLM-5V-Turbo 1.2/1.8；GLM-4.6V 0.2/0.4；GLM-4.6V-FlashX 0.03；GLM-4.5V 0.4/0.8；GLM-4V-Plus-0111 2。GLM-4.7-Flash、GLM-4.6V-Flash 命中列为免费。 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "GLM-4.7 | 输入 [0, 32K)，输出 [0, 0.2K) | 2 | 8 | 限时免费 | 0.4" | type: official
- [C13] D6：缓存存储当前限时免费，免费期后标准价本页不展示。 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "缓存存储当前限时免费。本页暂不展示免费期结束后的标准价格，后续如有调整，以页面最新信息为准。" | type: official
- [C14] D5 Coding Plan（与标准 API 分开）：积分含「缓存命中 Token × Cached Input 抵扣系数」。表内 GLM-5.3 为 Input 6.9、Cached Input 1.7、Output 24；GLM-5.3-Flash 为 2.3 / 0.56 / 8。 | src: https://docs.bigmodel.cn/cn/coding-plan/overview | quote: "模型消耗积分数=（输入 Token × Input 抵扣系数 + 缓存命中 Token × Cached Input 抵扣系数 + 输出 Token × Output 抵扣系数） / 10000" | type: official
- [C15] D5 能力页计费说明范围：仅标准 API，不含资源包与 GLM Coding Plan。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "仅适用于标准 API 计费，不包括资源包和 GLM Coding Plan 套餐。" | type: official
- [C16] D8：改时间戳、随机编号、临时说明或段落顺序可能降低命中，不是写成立即失效的规则。 | src: https://docs.bigmodel.cn/cn/best-practice/latency-optimization | quote: "即使只是增加时间戳、随机编号、临时说明，或者调整段落顺序，也可能降低缓存命中效果。" | type: official
- [C17] D8：保留式思考要求原样回传 reasoning content，重排或修改会影响缓存命中。Coding Plan 端点默认开，标准 API 默认关，用 `clear_thinking: False` 开启。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking-mode | quote: "所有连续的 reasoning content 必须与模型在原始请求期间生成的序列完全一致，不要重新排序或修改这些 content，否则会降低效果并影响缓存命中。" | type: official
- [C18] D1/D7 仅出现在缓存文档示例的 system 字符串内，不是独立规格小节：长前缀自动缓存，且异步生效。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "缓存为异步生效，首次请求后稍等片刻再发起后续请求效果更好。" | type: official
- [C19] D9：对话补全 OpenAPI server 为 `https://open.bigmodel.cn/api/`，路径 `/paas/v4/chat/completions`。`ChatCompletionTextRequest` 属性有 model、messages、thinking、user_id 等，没有 cache_control、prompt_cache_key、ttl。 | src: https://docs.bigmodel.cn/openapi/openapi.json | quote: "终端用户的唯一标识符。" | type: official
- [C20] D9 定价表「缓存命中」列为「不支持」的行：GLM-4-AirX、GLM-4-Assistant、GLM-Z1-Air、GLM-Z1-AirX、GLM-Z1-FlashX、GLM-4-Flash-250414、GLM-Z1-Flash、GLM-OCR、GLM-4V-Flash、GLM-4.1V-Thinking-FlashX、GLM-4.1V-Thinking-Flash。与「免费」不是同一格。 | src: https://docs.bigmodel.cn/cn/guide/start/pricing | quote: "GLM-4-AirX | 8K | 10 | 10 | 限时免费 | 不支持" | type: official
- [C21] 命名参数（不同于隐式、也不是 cache_control）：Response 创建请求有可选字符串 `prompt_cache_key`，说明只写集群路由以提高命中率。端点描述为 `https://open.bigmodel.cn/api/v1`，路径 `/v1/responses`。 | src: https://docs.bigmodel.cn/openapi/openapi-responses.json | quote: "用于集群路由，以提高缓存命中率。" | type: official
- [C22] D4 Response：命中在 `usage.input_tokens_details.cached_tokens`，描述为「缓存 tokens。」与对话补全字段名不同。 | src: https://docs.bigmodel.cn/openapi/openapi-responses.json | quote: "缓存 tokens。" | type: official
- [C23] D4/D9 问答 Agent SSE：`usage.prompt_tokens_details.cached_tokens` 描述「缓存命中 Token 数」，且 Token 用量仅 done 事件。路径 `/zrag/agent/chat`。 | src: https://docs.bigmodel.cn/openapi/openapi.json | quote: "缓存命中 Token 数" | type: official
- [C24] 另一接口，不要并进对话隐式缓存：Realtime `wss://open.bigmodel.cn/api/paas/v4/realtime` 的 `input_token_details.cached_tokens` 为「使用缓存令牌的数量」，但 usage 写明暂时都返回 0、计费计算仍在规划。 | src: https://docs.bigmodel.cn/cn/guide/models/sound-and-video/glm-realtime | quote: "暂时都返回 0, 实际计算规划开发中" | type: official
- [C25] `previous_response_id` 的 7 天是已存储 Response 的多轮有效期（须 store=true），不是上下文缓存 TTL。 | src: https://docs.bigmodel.cn/openapi/openapi-responses.json | quote: "上一轮 `id`，用于多轮。须 `store=true`，有效期 7 天。" | type: official

## conflicts
- 能力页写命中「通常为标准价格的 50%」，示例 1200 token 按 0.005 元/1K（相对假设标准价 0.01）。定价表 GLM-5.3 输入 8、命中 2（25%），GLM-4.7 短输出档输入 2、命中 0.4（20%）；GLM-4-Plus 输入 5、命中 2.5 才是 50%。未裁决哪条是当前实价。src: https://docs.bigmodel.cn/cn/guide/capabilities/cache 与 https://docs.bigmodel.cn/cn/guide/start/pricing 。quote: "缓存命中 Token：按优惠价格计费（通常为标准价格的 50%）" / "GLM-5.3 | 1M | 8 | 28 | 限时免费 | 2 | 文本"
- GLM-Z1 模型页仍有能力卡「上下文缓存 / 智能缓存机制，优化长对话性能」，同页又写系列已下线；定价表 GLM-Z1-Air、AirX、FlashX、Flash 的缓存命中均为「不支持」。src: https://docs.bigmodel.cn/cn/guide/models/text/glm-z1 与 https://docs.bigmodel.cn/cn/guide/start/pricing 。quote: "GLM-Z1 系列模型已下线" / "智能缓存机制，优化长对话性能"

## gaps
- D7：缓存指南、定价页（直接检索 cache_control、ttl、TTL、缓存写入、显式缓存、有效期、过期，只命中「缓存存储」）、对话补全 OpenAPI、`new-releases.md`（仅有架构「KV 缓存」一句，无上下文缓存上线记录）都没有 prompt 缓存 TTL 或过期原句。不能把 Response 的 7 天当成缓存 TTL。
- D3：未见硬性最少 token、块对齐（128/1024）或「超过即按块命中」的规格句。500 只是建议。
- D6：没有「缓存写入」单价原句。存储是限时免费，免费期后价格未给出，不能写成永久无存储费。
- D8：无「改某字段即作废」或按时间失效的规则；只有降低命中的建议。示例里的「异步生效」在 system 示例正文内。
- D10：`user_id` 只定义为终端用户标识，未写缓存隔离。未见跨账号/组织隔离、缓存并发上限。`prompt_cache_key` 只说明路由，未说明是否构成安全隔离。
- 显式断点：上述定价页、缓存页、对话补全请求 schema、openapi-en 未出现 `cache_control`。这不是全站「不支持显式缓存」的证明。Response 指南页检索无 cache/cached_tokens。llms.txt 无 Anthropic 专页。
- 定价表摘录未见 GLM-4.6、GLM-4.5 行，虽有模型能力卡链到缓存文档，不能据此写支持或价格。
- 各页正文未见可引用的文档更新日期。

## leads
- GLM-5.3 模型页检索摘要有 Anthropic Message base `https://open.bigmodel.cn/api/anthropic`，本轮未打开该页，未知是否接受 cache_control。
- 知识库「上下文增强」和网页阅读 `no_cache` 是别的缓存，不是 prompt cache。
- Realtime 并发表（V0–V3 为 5/10/15/20）是在途请求限制，不是 prompt 缓存隔离。
