# r2-compat-west
question: xAI（Grok）与 Mistral AI 官方 API 的协议面事实：各自与 OpenAI 的兼容度与已知偏差。
checked: docs.x.ai/developers/rest-api-reference/inference(+responses+chat-completions内嵌spec)、/developers/model-capabilities/text/*4页、/developers/tools/(function-calling|web-search)、/overview；docs.mistral.ai/resources/migration-guides、/api/endpoint/chat(内嵌spec)、/capabilities/*3页、/resources/error-glossary（均https://，2026-09-23）

## claims
- [C1] xAI D1/D11：声明 REST API 与 OpenAI 兼容；base https://api.x.ai，SDK 用 base_url https://api.x.ai/v1 | src: https://docs.x.ai/developers/rest-api-reference/inference | quote: "The xAI REST API is compatible with the OpenAI REST API." | type: official
- [C2] xAI D1 双端点：POST /v1/responses（primary）+ POST /v1/chat/completions（legacy）；/responses 有 GET/DELETE /{response_id}、POST /compact | src: https://docs.x.ai/developers/rest-api-reference/inference/responses | quote: "The Responses API is the primary interface for text generation, reasoning, and tool use." | type: official
- [C3] xAI D11：chat completions 定位 legacy 前身 | src: https://docs.x.ai/developers/rest-api-reference/inference/chat-completions | quote: "The Chat Completions API is the stateless, OpenAI-compatible predecessor of the Responses API. New integrations should use Responses" | type: official
- [C4] xAI D6：Bearer xAI API key；管理域独立 management-api.x.ai（偏差） | src: https://docs.x.ai/developers/rest-api-reference/inference | quote: "https://management-api.x.ai Authorization: Bearer <xAI Management API key>" | type: official
- [C5] xAI D1 偏差：chat 非标顶层 search_parameters（sources[].type 枚举 live_search）；非标端点 GET /v1/chat/deferred-completion/{request_id} | src: https://docs.x.ai/developers/rest-api-reference/inference/chat-completions | quote: "\"search_parameters\":{…\"description\":\"Parameters to control realtime data.\"" | type: official
- [C6] xAI D3：responses 端 tools 仅 functions+web_search，max 350 | src: https://docs.x.ai/developers/rest-api-reference/inference/responses | quote: "A max of 350 tools are supported." | type: official
- [C7] xAI D3：tool_choice 同 OpenAI chat（auto 默认/required/none/{"type":"function","function":{"name"}}）；parallel 默认开 | src: https://docs.x.ai/developers/tools/function-calling | quote: "By default, parallel function calling is enabled" | type: official
- [C8] xAI D5 偏差：流式函数调用整块单 chunk，不按 delta+index 拆 | src: https://docs.x.ai/developers/tools/function-calling | quote: "With streaming, the function call is returned in whole in a single chunk, not streamed across chunks." | type: official
- [C9] xAI D8：response_format.type=text/json_object/json_schema；工具参数恒 strict；additionalProperties 默认 false；违规 schema 400 | src: https://docs.x.ai/developers/model-capabilities/text/structured-outputs | quote: "the strict flag is implicitly always true" | type: official
- [C10] xAI D9：reasoning_effort low/medium/high（默认）/xhigh（grok-4.6+）；不可关 | src: https://docs.x.ai/developers/model-capabilities/text/reasoning | quote: "If not specified, reasoning_effort defaults to \"high\". Reasoning cannot be disabled." | type: official
- [C11] xAI D9：include:["reasoning.encrypted_content"]；grok-4.7 无条件返回；流式 delta 含非标 reasoning_content | src: https://docs.x.ai/developers/model-capabilities/text/generate-text | quote: "grok-4.7 always returns reasoning.encrypted_content on the Responses API" | type: official
- [C12] xAI D5：SSE（stream:true），chunk object=chat.completion.chunk，终止 data: [DONE]，每 chunk 带 usage（xAI 特有 text_tokens） | src: https://docs.x.ai/developers/model-capabilities/text/streaming | quote: "To enable streaming, you must set \"stream\": true in your request." | type: official
- [C13] xAI D7：chat 支持 seed（best-effort；OpenAI 已弃 seed xAI 未弃）；max_tokens 弃用改 max_completion_tokens | src: https://docs.x.ai/developers/rest-api-reference/inference/chat-completions | quote: "will make a best effort to sample deterministically, such that repeated requests with the same `seed`" | type: official
- [C14] xAI D7 偏差：responses 端 frequency_penalty/presence_penalty 标 NOT SUPPORTED；store 默认 true 存 30 天；background 等仅为 OpenResponses 兼容摆设 | src: https://docs.x.ai/developers/rest-api-reference/inference/responses | quote: "(NOT SUPPORTED in Responses API) Positive values penalize new tokens" | type: official
- [C15] xAI D7：finish_reason 含非 OpenAI 枚举 "end_turn"；web_search 参数 allowed_domains/excluded_domains max 5 | src: https://docs.x.ai/developers/rest-api-reference/inference/chat-completions | quote: "\"end_turn\" or `null` in streaming mode when the chunk is not the last." | type: official
- [C16] Mistral D1/D11：声明请求结构与 OpenAI 相同，改 base URL+模型名即可；端点 POST https://api.mistral.ai/v1/chat/completions | src: https://docs.mistral.ai/resources/migration-guides | quote: "The Mistral Chat Completions API follows the same request structure as OpenAI" | type: official
- [C17] Mistral D6：Authorization: Bearer $MISTRAL_API_KEY | src: https://docs.mistral.ai/api/endpoint/chat | quote: "-H \"Authorization: Bearer $MISTRAL_API_KEY\"" | type: official
- [C18] Mistral D3 偏差：tool_choice 枚举 auto（默认）/any（强制）/none，无 "required"；parallel_tool_calls 默认 true | src: https://docs.mistral.ai/capabilities/function_calling | quote: "\"any\": forces tool use. \"none\": prevents tool use." | type: official
- [C19] Mistral D3 偏差：tools 为 OpenAI 式 function 包裹（tools[].function），function.strict="Not supported"，type 枚举 ["function"] | src: https://docs.mistral.ai/api/endpoint/chat | quote: "\"strict\":{…\"description\":\"Not supported. Only maintained for compatibility reasons.\"}}" | type: official
- [C20] Mistral D8：json_object 须在 prompt 显式要求 JSON（OpenAI 不强制） | src: https://docs.mistral.ai/capabilities/structured_output | quote: "For JSON mode, it is essential to explicitly instruct the model in your prompt to output JSON and specify the desired format." | type: official
- [C21] Mistral D8：json_schema 模式保证按 schema 输出 | src: https://docs.mistral.ai/api/endpoint/chat | quote: "enables JSON schema mode, which guarantees the message the model generates is in JSON and follows the schema you provide." | type: official
- [C22] Mistral D7 偏差：随机种子字段名 random_seed（非 OpenAI 的 seed） | src: https://docs.mistral.ai/api/endpoint/chat | quote: "chat_completion_v1_chat_completions_post_request_random_seed" | type: official
- [C23] Mistral D5：流式 200 text/event-stream，终止 data: [DONE]（同 OpenAI）；SDK 流式方法 client.chat.stream | src: https://docs.mistral.ai/api/endpoint/chat | quote: "with the stream terminated by a data: [DONE] message." | type: official
- [C24] Mistral 错误形状 {message,type,param,code}，type 枚举 invalid_request_error/authentication_error/rate_limit_error/server_error | src: https://docs.mistral.ai/resources/error-glossary | quote: "(invalid_request_error, authentication_error, rate_limit_error, server_error)" | type: official
- [C25] Mistral D2/D10：视觉走 chat completions（image_url，URL/base64）；现行推荐 Mistral Large 3/Medium 3.1/Small 3.2/Ministral 3，无 Pixtral | src: https://docs.mistral.ai/capabilities/vision | quote: "We provide a variety of models with vision capabilities, all available via the Chat Completions API." | type: official
- [C26] Mistral D9：reasoning 线 Magistral 入 FC 模型表，但已抓页面无 reasoning_effort 类参数 | src: https://docs.mistral.ai/capabilities/function_calling | quote: "Reasoning ModelsMagistral Medium 1.2" | type: official

## conflicts
- xAI penalties/stop 三口径：responses 标 "NOT SUPPORTED"（C14）；reasoning 页称模型上报错（quote: "presencePenalty, frequencyPenalty, and stop cannot be used with reasoning models"）；chat spec 又含这些字段——模型/端点相关，未裁决。
- "compatible with the OpenAI REST API" 总声明 vs 上列偏差：官方无偏差汇总页。
- Mistral tool_choice "required" 仅见检索答案，官方页只列 auto/any/none。

## gaps
- xAI 错误对象形状（新 docs 无 error 页）；responses 流式事件名；temperature/top_p 范围原句。
- Mistral json_schema 内层 strict 语义；named-function tool_choice 形状原句；无官方偏差清单页；Pixtral 已不在 vision 页。

## leads
- xAI responses 的 background 等仅为 "OpenResponses compatibility"（呼应 r1）。
- xAI 另有面：gRPC xai_sdk、WebSocket、mTLS；内置工具 x_search/code-execution/remote-mcp。
- Mistral 自有面：/v1/conversations(beta)、agents、workflows。
