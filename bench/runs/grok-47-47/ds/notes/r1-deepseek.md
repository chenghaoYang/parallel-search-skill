# r1-deepseek
question: DeepSeek 官方 API 的响应（以及请求）相对 OpenAI 官方 Chat Completions / Responses 文档，字段上有哪些写明的不同？DeepSeek 有没有自己的 /responses 或 response 协议？
checked: https://api-docs.deepseek.com/, https://api-docs.deepseek.com/api/deepseek-api, https://api-docs.deepseek.com/api/create-chat-completion, https://api-docs.deepseek.com/api/create-response, https://api-docs.deepseek.com/guides/responses_api, https://api-docs.deepseek.com/guides/thinking_mode, https://api-docs.deepseek.com/guides/json_mode, https://api-docs.deepseek.com/guides/multi_round_chat, https://api-docs.deepseek.com/guides/reasoning_model, https://api-docs.deepseek.com/quick_start/pricing, https://api-docs.deepseek.com/updates, https://api-docs.deepseek.com/faq, https://api-docs.deepseek.com/sitemap.xml, https://api-docs.deepseek.com/news/news260424

## claims
- [C1] D1 base=https://api.deepseek.com/chat/completions，无 /v1。 | src: https://api-docs.deepseek.com/ | quote: "curl https://api.deepseek.com/chat/completions" | type: official
- [C2] D1 鉴权 Bearer。 | src: https://api-docs.deepseek.com/api/deepseek-api | quote: "HTTP Authorization Scheme: bearer" | type: official
- [C3] D1 有 POST /responses。 | src: https://api-docs.deepseek.com/api/create-response | quote: "/responses Creates a model response in the OpenAI Responses API format." | type: official
- [C4] D1 Responses base_url 相同。 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "with the base_url being https://api.deepseek.com." | type: official
- [C5] D2 Chat 多轮重放全部 messages。 | src: https://api-docs.deepseek.com/guides/multi_round_chat | quote: "concatenate all previous conversation history" | type: official
- [C6] D2 Responses 不保存会话。 | src: https://api-docs.deepseek.com/api/create-response | quote: "The API is stateless: responses and conversations are not stored on the server." | type: official
- [C7] D3 role 为 system/user/assistant/tool。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "The role of the messages author, in this case system." | type: official
- [C8] D3 content 可为字符串或内容部件。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Either a string, or an array of content parts" | type: official
- [C9] D3 reasoning_content 与 content 同级，仅思考模式。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "For thinking mode only. The reasoning contents of the assistant message, before the final answer." | type: official
- [C10] D3 请求 reasoning_content 须 prefix=true。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "the prefix parameter must be set to true" | type: official
- [C11] D5 无 tools 则忽略 reasoning_content。 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "If the request does not carry the tools parameter: reasoning_content does not need to be passed back; even if passed to the API, it will be ignored and will not be concatenated into the context." | type: official
- [C12] D5 有 tools 不回传则 400。 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "If your code does not correctly pass back reasoning_content, the API will return a 400 error." | type: official
- [C13] D4 Chat 接受 system。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "The contents of the system message" | type: official
- [C14] D4 developer 当作 user；instructions 作第一条 system。 | src: https://api-docs.deepseek.com/api/create-response | quote: "developer is treated as user. A system-level instruction, inserted as the first system message of the model's context." | type: official
- [C15] D5 tools 仅 function；tool 消息有 tool_call_id。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Currently, only functions are supported as a tool. Tool call that this message is responding to." | type: official
- [C16] D5 思考模式 required/具名 tool_choice 400。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "required and named tool choices are not supported in thinking mode; the API returns a 400 error." | type: official
- [C17] D6 前段为 max_tokens；末句为 temperature。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "The value must be between 1 and 384K (393216). When not set, the default is 8K in non-thinking mode, 64K in thinking mode (128K with reasoning_effort set to max). Has no effect in thinking mode." | type: official
- [C18] D6 reasoning_effort：none 关思考，默认 high。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "none disables thinking mode; low / high / max enable thinking mode. The default effort is high." | type: official
- [C19] D6 Responses：max_output_tokens 含推理 token。 | src: https://api-docs.deepseek.com/api/create-response | quote: "visible output tokens and the reasoning tokens" | type: official
- [C20] D7 Chat 以 data: [DONE] 结束。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "terminated by a data: [DONE] message" | type: official
- [C21] D7 Responses 无 [DONE]；思维与正文分事件。 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "there is no data: [DONE] message" | type: official
- [C22] D8 message 含 content、reasoning_content、tool_calls。 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "content, reasoning_content, and tool_calls" | type: official
- [C23] D8 finish_reason 含 insufficient_system_resource、aborted。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "stop, length, content_filter, tool_calls, insufficient_system_resource, aborted" | type: official
- [C24] D8 见原句。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "It equals prompt_cache_hit_tokens + prompt_cache_miss_tokens. Tokens generated by the model for reasoning." | type: official
- [C25] D8 Responses 思维是 reasoning 项，在 message 前。 | src: https://api-docs.deepseek.com/api/create-response | quote: "reasoning item before the message item" | type: official
- [C26] D8 Responses reasoning_tokens 见原句。 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "output_tokens_details.reasoning_tokens is the number of chain-of-thought tokens" | type: official
- [C27] D9 Chat 仅 json_object，无 json_schema。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Must be one of text or json_object" | type: official
- [C28] D9 Responses 支持 json_schema。 | src: https://api-docs.deepseek.com/api/create-response | quote: "Required when type is json_schema" | type: official
- [C29] D10 自称兼容 OpenAI/Anthropic。 | src: https://api-docs.deepseek.com/ | quote: "The DeepSeek API uses an API format compatible with OpenAI/Anthropic." | type: official
- [C30] D10 penalty 不再支持且不生效。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "This parameter is no longer supported. It will not take effect if you pass it to the API." | type: official
- [C31] D10 不支持项静默忽略（previous_response_id、store、truncation、prompt_cache_key、stream_options 等）。 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Unsupported parameters are silently ignored and do not cause errors" | type: official
- [C32] D10 模型为 deepseek-flash 与 deepseek-v4-pro，默认思考。 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "non-thinking and thinking (default) modes" | type: official
- [C33] D10 chat/reasoner 该日后不可访问；当时路由为非思考/思考。 | src: https://api-docs.deepseek.com/news/news260424 | quote: "inaccessible after Jul 24th, 2026, 15:59 (UTC Time). (Currently routing to deepseek-v4-flash non-thinking/thinking)." | type: official

## conflicts
- effort：页写 ultra→max；参考有 none、不写 ultra。
- 惩罚项：思考页称三者不支持且不报错；Chat 参考把 presence/frequency 写成全局 no longer supported。
- tool_choice：Chat 思考模式 required/具名 400；Responses 指南写 Supported。指南另写 apply_patch。

## gaps
- 无 /v1，勿当拒绝。Chat 未写 developer、json_schema、max_completion_tokens、user（只写了 user_id）。
- reasoning_model 即首页。thinking.type：If set to enabled, then use thinking mode.
## leads
- Anthropic：https://api-docs.deepseek.com/guides/anthropic_api。
