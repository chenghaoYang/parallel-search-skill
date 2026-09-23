# r3-minimax-responses
question: MiniMax Responses 兼容端点（POST /v1/responses）的状态与推理表示；Anthropic 兼容端的鉴权 header 与模型名要求
checked: https://platform.minimax.io/docs/api-reference/responses-create, https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json, https://platform.minimax.io/docs/api-reference/text-chat-anthropic, https://platform.minimax.io/docs/api-reference/text/api/openapi-chat-anthropic.json, https://platform.minimax.io/docs/api-reference/text-anthropic-api

## claims
- [C1] Responses 端 `store` 只是响应字段（"Whether the response is persisted"），不是请求参数；CreateResponseReq 的 14 个属性里没有 store，示例响应里给的是 `"store": false` | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "store": {"type": "boolean", "description": "Whether the response is persisted"} | type: official
- [C2] 没有 previous_response_id / 独立 conversation 参数；多轮靠 input 直接传完整历史数组 | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "Conversation content. Supports either a simple text or a full conversation history array" | type: official
- [C3] output 里的推理表示为 type="reasoning" 的 OutputItem，含 summary 数组和 content 数组（content 元素 type="reasoning_text" + text 明文），未见 encrypted_content 属性 | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "Reasoning output (only returned when reasoning is enabled)" | type: official
- [C4] input 侧 InputItem.type 枚举含 "reasoning"，summary 字段描述为"仅当 type 为 reasoning 时"的推理片段数组，结构上支持把推理项回传，但没有强制性"必须回传"的原句 | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "Reasoning segment array (only when `type` is `reasoning`)" | type: official
- [C5] reasoning 控制字段：M3 默认 none(关闭)，effort 设为 minimal/low/medium/high 只是开关 Adaptive Thinking，不真正调节推理深度；M2.x 不能关闭推理 | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "For MiniMax-M3, the default is `none`, which disables reasoning. Set `effort` to a non-`none` value...to enable Adaptive Thinking, but this does not tune MiniMax-M3's reasoning depth. For M2.x models, reasoning cannot be disabled." | type: official
- [C6] tools 只支持一种类型 function，没有 OpenAI 官方 Responses API 里的内置/服务端工具类型 | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "type": {"type": "string", "enum": ["function"], "description": "Tool type"} | type: official
- [C7] tool_choice 只支持 none/auto 两个值 | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "Tool selection strategy: `none` means no tool will be called; `auto` lets the model decide whether to call tools" | type: official
- [C8] usage 里的缓存/推理 token 字段：input_tokens_details.cached_tokens、output_tokens_details.reasoning_tokens | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "Prompt cache hit tokens" / "Tokens consumed by reasoning (only counted when reasoning is enabled)" | type: official
- [C9] Responses 端 temperature 范围是 (0,1]，默认 1——与 OpenAI/Anthropic 兼容端的 [0,2] 不同 | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "Sampling temperature, range (0, 1]" | type: official
- [C10] stream 只是布尔开关，OpenAPI 里该端点 responses 对象只写了 200/application-json 一种，没有单独的流式事件 schema，全文没有具体 SSE 事件名或 [DONE] | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "Set to `true` to enable SSE streaming response" | type: official
- [C11] Anthropic 兼容端鉴权：Authorization: Bearer 方式，若 Authorization 与 x-api-key 同时出现，Authorization 优先 | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "Bearer API Key auth. Send Authorization: Bearer <API_KEY>. If Authorization and x-api-key are both present, Authorization takes precedence." | type: official
- [C12] 同时也支持 x-api-key header，但该 scheme 自己的描述反过来推荐用 Authorization: Bearer | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "Anthropic-compatible API Key auth. Send x-api-key: <API_KEY>. Authorization: Bearer <API_KEY> is recommended." | type: official
- [C13] model 字段是严格枚举，只接受 8 个 MiniMax-* 名字（M3/M2.7/M2.7-highspeed/M2.5/M2.5-highspeed/M2.1/M2.1-highspeed/M2），不接受 claude-* 名称 | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "enum": ["MiniMax-M3","MiniMax-M2.7","MiniMax-M2.7-highspeed","MiniMax-M2.5","MiniMax-M2.5-highspeed","MiniMax-M2.1","MiniMax-M2.1-highspeed","MiniMax-M2"] | type: official
- [C14][更正r2] cache_control 其实在 OpenAPI 参考页（非 r2 查的 guide 页）里正式定义，system 文本块/消息内容块/tool 定义都可挂 cache_control，取值固定 {"type":"ephemeral"} | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "Prompt cache marker." | type: official
- [C15][更正r2] signature 字段也正式定义在 thinking 内容块里，与 thinking 文本同级 | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "Signature for echoed thinking content. Return unchanged in later turns." | type: official

## conflicts
- MiniMax 自家三套协议 temperature 范围不一致：Responses 端 (0,1]默认1（C9），而 Chat Completions 兼容端与 Anthropic 兼容端都是 [0,2]默认1（见 r2-minimax.md C8/C26）。同一批模型，三套接口温度上限不同。
- r2-minimax.md 基于 text-anthropic-api guide 页判断 cache_control/signature 未文档化（gap/conflict），但本轮打开的 OpenAPI 参考页（text-chat-anthropic 的 json）明确定义了两者（C14/C15）——是文档分层的问题，不是真不支持。

## gaps
- 全文（含 openapi-responses.json）没有 "encrypted_content"，无法确认 MiniMax 是否提供加密推理选项。
- 没找到强制性原句要求"必须把 reasoning item 原样回传"，Responses 端多轮回传推理项只是结构上可行（C4），不像 Anthropic/Chat Completions 两端那样有明文"must preserve"式规定。
- 没有整句列出 Responses 端不支持/忽略哪些字段；previous_response_id、conversation、background、include、logprobs、seed 的缺失是靠 CreateResponseReq 属性列表里没有这些键推断的，不是官方点名说"忽略"。
- 未找到 Responses 端具体 SSE 事件类型名（如 response.created/response.output_text.delta）或 [DONE] 终止符的原句。

## leads
- Responses 端有 prompt_cache_key 请求字段（"Prompt cache routing identifier"），三套协议的 prompt caching 设计值得单独一轮统一核对。
- Anthropic 兼容内容块枚举里多了一个官方 Anthropic 规范没有的 "mid_conv_system" 类型（"System instructions inserted mid-conversation"）。
- Anthropic 兼容的 OpenAPI 定义了 StreamEvent schema，Responses 端 OpenAPI 没有等价 schema——两端流式事件文档完整度不对等。
