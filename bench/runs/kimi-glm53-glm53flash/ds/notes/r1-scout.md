# r1-scout
question: LLM API 请求协议生态里，跨厂商/跨协议适配时用户实际会踩的坑，以及本网格没列进去的重要实体或维度。
checked: https://openrouter.ai/docs/features/provider-routing, https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/, https://raw.githubusercontent.com/ollama/ollama/main/docs/api/openai-compatibility.mdx, https://docs.litellm.ai/docs/completion/drop_params, https://console.groq.com/docs/openai, https://docs.together.ai/docs/openai-api-compatibility, https://docs.fireworks.ai/tools-sdks/openai-compatibility, https://ai.google.dev/gemini-api/docs/openai, https://docs.anthropic.com/en/api/errors, https://docs.anthropic.com/en/api/messages, https://platform.openai.com/docs/guides/responses-vs-chat-completions, https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml

## claims
- [C1] OpenRouter 在 chat completions 请求体接受非标准 provider 路由对象：order/allow_fallbacks/require_parameters/data_collection/zdr/only/ignore/quantizations/sort/max_price | src: https://openrouter.ai/docs/features/provider-routing | quote: "You can customize how your requests are routed using the provider object in the request body for Chat Completions." | type: official
- [C2] OpenRouter 默认下不支持某参数的 provider 仍收到请求并静默忽略参数；require_parameters=true 才排除 | src: https://openrouter.ai/docs/features/provider-routing | quote: "can still receive the request, but will ignore unknown parameters" | type: official
- [C3] vLLM 支持 batch 端点 /v1/chat/completions/batch 与 Responses API /v1/responses | src: https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/ | quote: "Chat Completions batch API (/v1/chat/completions/batch)" | type: official
- [C4] Ollama 只实现 OpenAI API 子集；Responses 仅非状态版（无 previous_response_id/conversation） | src: https://raw.githubusercontent.com/ollama/ollama/main/docs/api/openai-compatibility.mdx | quote: "Ollama supports a subset of the OpenAI API." "there is no `previous_response_id` or `conversation` support" | type: official
- [C5] LiteLLM 默认对目标模型不支持的参数抛异常 | src: https://docs.litellm.ai/docs/completion/drop_params | quote: "LiteLLM raises an exception if you send a parameter to a model that doesn't support it." | type: official
- [C6] LiteLLM drop_params=True 改为静默丢弃；additional_drop_params 支持嵌套如 tools[*].input_examples | src: https://docs.litellm.ai/docs/completion/drop_params | quote: "LiteLLM will drop the unsupported parameter instead of raising an exception." | type: official
- [C7] Groq：logprobs/logit_bias/top_logprobs/messages[].name 即 400；n 必须=1 | src: https://console.groq.com/docs/openai | quote: "The following fields are currently not supported and will result in a 400 error (yikes) if they are supplied" "If N is supplied, it must be equal to 1." | type: official
- [C8] Together 模型 ID 带命名空间，OpenAI 模型串返回 404 | src: https://docs.together.ai/docs/openai-api-compatibility | quote: "OpenAI model strings like gpt-4o or text-embedding-3-large return a 404." | type: official
- [C9] Together 的 cached_tokens 位置按模型不同（嵌套 details 或顶层平铺），单形状客户端静默读到 0 | src: https://docs.together.ai/docs/openai-api-compatibility | quote: "A client configured for only one shape will return 0 for all others (with no error message)." | type: official
- [C10] Together 思维链在 assistant message 的 reasoning 或 reasoning_content 字段，字段名随模型 | src: https://docs.together.ai/docs/openai-api-compatibility | quote: "return the chain of thought in a reasoning or reasoning_content field on the assistant message" | type: official
- [C11] Fireworks 默认把超上下文的 max_tokens 自动调小；context_length_exceeded_behavior:"error" 才像 OpenAI 报错 | src: https://docs.fireworks.ai/tools-sdks/openai-compatibility | quote: "max_tokens will be adjusted lower accordingly. OpenAI returns an invalid request error" | type: official
- [C12] Fireworks 流式在最后 chunk（带 finish_reason）返回 usage，无需 stream_options | src: https://docs.fireworks.ai/tools-sdks/openai-compatibility | quote: "the usage field is returned in the very last chunk on the response" | type: official
- [C13] OpenAI finish_reason 枚举：stop/length/tool_calls/content_filter/function_call（后者 deprecated） | src: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml | quote: "`tool_calls` if the model called a tool, or `function_call` (deprecated) if the model called a function." | type: official
- [C14] OpenAI 流式 usage 需 stream_options:{"include_usage":true}，在 data:[DONE] 前独立 chunk 下发 | src: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml | quote: "If set, an additional chunk will be streamed before the `data: [DONE]` message." | type: official
- [C15] OpenAI chat 的 max_tokens 已弃用，改 max_completion_tokens | src: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml | quote: "This value is now deprecated in favor of `max_completion_tokens`, and is" | type: official
- [C16] Responses API 用 max_output_tokens；移除 n，只剩单次生成 | src: https://platform.openai.com/docs/guides/responses-vs-chat-completions | quote: "In Responses, we've removed this param, leaving only one generation." | type: official
- [C17] Responses：函数定义内嵌 tag；省略 strict 先试 strict，不兼容回退非 strict | src: https://platform.openai.com/docs/guides/responses-vs-chat-completions | quote: "if the schema cannot be made compatible, Responses falls back to non-strict" | type: official
- [C18] previous_response_id 不继承上一响应顶层 instructions；链上先前输入仍按 input 计费 | src: https://platform.openai.com/docs/guides/responses-vs-chat-completions | quote: "previous_response_id does not carry over the previous response's top-level instructions" | type: official
- [C19] Responses 默认存储，ZDR 需 store:false | src: https://platform.openai.com/docs/guides/responses-vs-chat-completions | quote: "Responses are stored by default." | type: official
- [C20] Anthropic 错误恒为 {error:{type,message}}+request_id；含 529 overloaded_error | src: https://docs.anthropic.com/en/api/errors | quote: "a top-level error object that always includes a type and message value" | type: official
- [C21] Anthropic SSE 下 200 之后仍可能出错，须按 error 事件处理 | src: https://docs.anthropic.com/en/api/errors | quote: "an error can occur after the API returns a 200 response." | type: official
- [C22] Anthropic stop_reason 7 值：end_turn/max_tokens/stop_sequence/tool_use/pause_turn/refusal/model_context_window_exceeded | src: https://docs.anthropic.com/en/api/messages | quote: "StopReason = \"end_turn\" or \"max_tokens\" or \"stop_sequence\" or 4 more" | type: official
- [C23] Anthropic 工具定义字段是 input_schema（非 OpenAI function.parameters） | src: https://docs.anthropic.com/en/api/messages | quote: "Tool object{ type, input_schema, name, 7 more }" | type: official
- [C24] Gemini 兼容层 reasoning_effort 映射各家 thinking；Gemini 2.5 Pro/3 系无法关闭思考 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Reasoning cannot be turned off for Gemini 2.5 Pro or 3 models." | type: official

## conflicts
- max_tokens 超上下文：OpenAI 语义报错（Fireworks 文档自述 "OpenAI returns an invalid request error in this situation"），Fireworks 默认静默 truncate，行为相反。
- 流式 usage：OpenAI 需 include_usage 且独立 chunk 在 [DONE] 前；Fireworks 默认放 finish_reason chunk；Together 称 usage 恒在。三者互斥。

## gaps
- OpenAI→Anthropic 迁移页 404；system/max_tokens 必填/prefill 无原句。
- Gemini role 映射、function schema 转换、错误形状未取得（重定向循环+正文过长）。
- OpenAI 错误对象 {message,type,param,code} schema 原句未取。
- tool_call id 跨厂商对比仅碎片；Mistral/xAI/Cohere/MiniMax 兼容页未打开。

## leads
- 多协议服务端：Fireworks 有 Anthropic /v1/messages 兼容+chat_template_kwargs；Ollama 有 anthropic-compatibility.mdx；SGLang 同服暴露 /v1/*、/v1/messages、原生 /generate。
- batch 分裂：vLLM 原生 batch；Together 明确 OpenAI-shaped batches.* 不支持。
- OpenAI Assistants API 已于 2026-08-26 sunset；Gemini 兼容层仍标 beta（2026-09 版）。
- vLLM extra_body 非标参数与 --api-key 不护 /invocations；Together 对 service_tier/store/metadata/prediction 接受但忽略、错误 type/code 自家取值；Responses 另将 response_format→text.format。
- OpenRouter x-anthropic-beta 透传（interleaved-thinking-2025-05-14 等）；:nitro/:floor slug 与 service tier 端点不被基础 slug 匹配。
- 未入网格实体：Mistral、xAI（双兼容）、Cohere v2、MiniMax、NVIDIA NIM；LiteLLM allowed_openai_params。
