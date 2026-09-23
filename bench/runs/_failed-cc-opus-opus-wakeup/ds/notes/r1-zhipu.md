# r1-zhipu
question: 智谱（BigModel 开放平台 / Z.ai）官方提供哪些协议入口？其 Anthropic Messages 兼容接口与 Anthropic 官方相比有哪些具体差异？其原生 v4 对话接口与 OpenAI Chat Completions 相比差在哪？
checked: （.md 原文/openapi.json 拉取；页面均无更新日期）docs.bigmodel.cn: llms(-full).txt, /cn/guide/develop/{claude/introduction,claude,openai/introduction,responses/introduction}, /cn/api/introduction, /cn/coding-plan/{quick-start,tool/claude,tool/others,faq,latest-model,mcp/vision-mcp-server}, /cn/guide/capabilities/{thinking,thinking-mode,streaming,stream-tool,function-calling,cache}, /cn/guide/start/concept-param, /cn/guide/models/text/glm-5.3, /api-reference/模型-api/对话补全, /openapi/openapi.json; docs.z.ai: llms(-full).txt, /api-reference/{introduction,llm/chat-completion}, /devpack/{tool/claude,quick-start,faq,latest-model}, /guides/llm/glm-5.3, /guides/develop/openai/python, /guides/capabilities/thinking-mode, /openapi.json, /guides/develop/claude(404); github.com/zai-org/ZCode

## claims
- [C1] 原生通用端点 | src: https://docs.bigmodel.cn/cn/api/introduction | quote: "智谱开放平台的通用 API 端点：https://open.bigmodel.cn/api/paas/v4" | type: official
- [C2] 原生鉴权 Bearer | src: https://docs.bigmodel.cn/cn/api/introduction | quote: "API 密钥需通过 HTTP 请求头的 Bearer 认证方式提供。" | type: official
- [C3] 国际站通用端点 | src: https://docs.z.ai/api-reference/introduction | quote: "Z.ai Platform's general API endpoint is as follows: https://api.z.ai/api/paas/v4" | type: official
- [C4] Anthropic 兼容 base URL | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "替换您访问的 base_url 为 https://open.bigmodel.cn/api/anthropic" | type: official
- [C5] 兼容示例走 /v1/messages + x-api-key，示例无 anthropic-version | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "curl https://open.bigmodel.cn/api/anthropic/v1/messages --header "x-api-key: YOUR_API_KEY"" | type: official
- [C6] Coding Plan（国内）：Anthropic 同址，Chat 用 coding 路径 | src: https://docs.bigmodel.cn/cn/coding-plan/quick-start | quote: "Anthropic Message 协议 | https://open.bigmodel.cn/api/anthropic | OpenAI Chat Completion 协议 | https://open.bigmodel.cn/api/coding/paas/v4 | OpenAI Response 协议 | https://open.bigmodel.cn/api/v1" | type: official
- [C7] Coding Plan（国际） | src: https://docs.z.ai/devpack/quick-start | quote: "Anthropic Messages | https://api.z.ai/api/anthropic | OpenAI Chat Completions | https://api.z.ai/api/coding/paas/v4 | OpenAI Responses | https://api.z.ai/api/v1" | type: official
- [C8] 订阅过套餐者调模型 API 暂限 Chat 协议 | src: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3 | quote: "如果您有订阅过 GLM Coding Plan（含已过期），那么暂时您只能通过 OpenAI Chat Completion 协议调用模型 API" | type: official
- [C9] Responses 兼容独立基址 | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction | quote: "Response API 的基址是 https://open.bigmodel.cn/api/v1，不是对话补全使用的 https://open.bigmodel.cn/api/paas/v4。" | type: official
- [C10] Responses 已声明差异 | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction | quote: "默认 store=false、流式结束不发送 data: [DONE]、当前未提供 cancel。" | type: official
- [C11] Claude 兼容仅有笼统差异声明 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "某些场景下智谱与 Claude 接口仍存在差异，但不影响整体兼容性。" | type: official
- [C12] OpenAI 兼容同样笼统 | src: https://docs.bigmodel.cn/cn/guide/develop/openai/introduction | quote: "某些场景下智谱与 OpenAI 接口仍存在差异，但不影响整体兼容性。" | type: official
- [C13] 套餐侧 thinking 开启类→max | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "thinking.type 未传、true、enabled、adaptive | max | 使用默认档" | type: official
- [C14] 套餐侧 disabled 不真正关思考 | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "thinking.type 为 false、disabled、none、off | low | 继续请求；仍会轻量思考" | type: official
- [C15] 识别 Anthropic output_config.effort | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "Claude Code 使用 thinking.type、output_config.effort；Codex 使用 reasoning.effort。" | type: official
- [C16] 原生：5.3 传 disabled 报错 | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking | quote: "GLM-5.3 GLM-5.3-FLASH 不再支持关闭思考（API 请求中 thinking.type 传 disabled 将会报错）" | type: official
- [C17] reasoning_effort 默认 max，5.3 三档 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "对于 GLM-5.3 GLM-5.3-FLASH 模型，仅支持 low / high / max 档位。" | type: official
- [C18] clear_thinking 默认 true | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "true（默认）：在本次请求中，系统会忽略/移除历史 turns 的 reasoning_content" | type: official
- [C19] Preserved thinking 默认值分端点 | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking-mode | quote: "该能力在 Coding Plan 端点默认开启、标准 API 端点默认关闭。" | type: official
- [C20] 工具循环须回传 reasoning | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking-mode | quote: "当您在使用“交错思考 + 工具”时，必须显式保留 Reasoning content，并在返回工具结果时一并返回" | type: official
- [C21] 流式推理字段 | src: https://docs.bigmodel.cn/cn/guide/capabilities/streaming | quote: "choices[0].delta.reasoning_content: 增量思考内容" | type: official
- [C22] 流式 usage 在末块 | src: https://docs.bigmodel.cn/cn/guide/capabilities/streaming | quote: "usage: 令牌使用统计（仅在最后一个chunk中出现）" | type: official
- [C23] tool_choice 仅 auto | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "默认auto且仅支持auto。" | type: official
- [C24] tool_stream 默认 false、限新模型 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "是否开启流式响应Function Calls，仅限GLM-5.3 GLM-5.2 GLM-5.1 GLM-5 GLM-5-Turbo GLM-4.7 GLM-4.6系列支持此参数，默认值false。" | type: official
- [C25] tools 含内置检索/搜索，≤128 函数 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "支持函数调用、知识库检索和网络搜索。使用此参数提供模型可以生成 JSON 输入的函数列表或配置其他工具。最多支持 128 个函数。" | type: official
- [C26] web_search 工具体 {type:"web_search",web_search:{search_engine}} | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "搜索引擎类型，默认为 search_std；支持search_std、search_pro、search_pro_sogou、search_pro_quark。" | type: official
- [C27] image_url.url 收 URL 或 Base64 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "图片的URL地址或Base64编码。图像大小上传限制为每张图像5M以下，且像素不超过6000*6000。" | type: official
- [C28] 5.3 纯文本/5.3-Flash 多模态 | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "GLM-5.3 为文本模型需要取消勾选 Support Images，GLM-5.3-FLASH 为多模态模型支持勾选 Support Images" | type: official
- [C29] 缓存隐式自动 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "自动缓存识别：隐式缓存，智能识别重复的上下文内容，无需手动配置" | type: official
- [C30] 缓存命中字段 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "响应字段 usage.prompt_tokens_details.cached_tokens" | type: official
- [C31] 缓存计费不含套餐 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "仅适用于标准 API 计费，不包括资源包和 GLM Coding Plan 套餐。" | type: official
- [C32] temperature | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "取值范围为 [0.0, 1.0]，限两位小数。对于GLM-5.3 GLM-5.2 GLM-5.1 GLM-5 GLM-4.7 GLM-4.6系列默认值为 1.0" | type: official
- [C33] top_p | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "取值范围为 [0.01, 1.0]，限两位小数。" 默认 0.95（同句后文）| type: official
- [C34] 独有 do_sample（默认 true） | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "当设置为 false 时，模型总是选择概率最高的词汇，生成更确定性的输出，此时 temperature 和 top_p 参数将被忽略。" | type: official
- [C35] max_tokens：glm-5.3 默认/上限 | src: https://docs.bigmodel.cn/cn/guide/start/concept-param | quote: "glm-5.3 | 65536 | 131072" | type: official
- [C36] request_id 6–64（user_id 6–128） | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "请求唯一标识符。由用户端传递，ID长度要求：最少6个字符，最多64个字符" | type: official
- [C37] Claude Code env | src: https://docs.bigmodel.cn/cn/coding-plan/tool/claude | quote: ""ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY", "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic", "API_TIMEOUT_MS": "3000000"" | type: official
- [C38] 模型映射 | src: https://docs.bigmodel.cn/cn/coding-plan/tool/claude | quote: ""ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-5.3-flash[1m]", "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5.3[1m]", "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.3[1m]"" | type: official
- [C39] 1M 上下文靠 [1m] 后缀 | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "注意开启 GLM 1M 上下文需要模型后缀加上 [1m]" | type: official

## conflicts
- 国际 Chat 端点：docs.z.ai/guides/llm/glm-5.3 "OpenAI Chat Completion Protocol | https://api.z.ai/api/coding/paas/v4" vs docs.z.ai/api-reference/introduction "general API endpoint … https://api.z.ai/api/paas/v4"
- 5.3 关思考：/cn/guide/capabilities/thinking "传 disabled 将会报错" vs /cn/coding-plan/latest-model "disabled … | low | 继续请求"
- 默认映射：/cn/coding-plan/tool/claude "ANTHROPIC_DEFAULT_OPUS_MODEL：GLM-5.3-Flash"（同页手动配置写 glm-5.3[1m]）vs /cn/guide/develop/claude "ANTHROPIC_DEFAULT_OPUS_MODEL：GLM-4.7"
- temperature：/cn/guide/develop/openai/introduction "temperature 参数的区间为 (0,1)"、表默认 0.6 vs 对话补全 "[0.0, 1.0]"、默认 1.0
- stop：docs.z.ai chat-completion "Currently, only one stop word is supported" vs 两站 spec maxItems: 4
- reasoning_content：对话补全 "仅在使用 glm-4.5 系列, glm-4.1v-thinking 系列模型时返回" vs thinking-mode 示例用 glm-5.1 读取

## gaps
- B3 无官方字段表：tool_use/tool_result、tool_choice、image/document 块、cache_control、stop_sequences、top_k、metadata、anthropic-version/beta、server tools、SSE 事件、budget_tokens/signature 均未提；两站 llms-full grep cache_control/count_tokens/anthropic-beta/stop_sequences/top_k/budget_tokens 0 命中
- count_tokens 无文档；两站 openapi.json 无 /anthropic 路径
- Z.ai 无独立 Anthropic 兼容页
- 兼容层是否收图像、回 cache_read_input_tokens、支持 tool_stream：未写
- 原生 assistant 消息 schema 未列 reasoning_content（仅示例回传）

## leads
- zai-org/ZCode anthropic-stream-compat.ts 注释："部分 Anthropic-compatible 服务"返回无 signature 的 thinking 块、assistant 侧裸 tool_result；未点名智谱，需另核
- 同仓 official-coding-plan-gateway.ts 将 open.bigmodel.cn/api/anthropic/v1/messages 改走 zcode.z.ai 网关
- /paas/v4/tokenizer 可替代 count_tokens
