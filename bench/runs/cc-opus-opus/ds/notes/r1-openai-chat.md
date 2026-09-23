# r1-openai-chat
question: OpenAI 官方 Chat Completions API（POST /v1/chat/completions）当前（2026）文档里，请求/响应协议在下列各维度的具体字段名、枚举值、规则是什么？
checked: https://developers.openai.com/api/reference/resources/chat.md, https://developers.openai.com/api/reference/resources/chat/subresources/completions/streaming-events.md, https://developers.openai.com/api/reference/overview.md, https://developers.openai.com/api/reference/chat-completions/overview.md, https://developers.openai.com/api/docs/guides/migrate-to-responses.md, https://developers.openai.com/api/docs/guides/reasoning.md, https://developers.openai.com/api/docs/guides/prompt-caching.md, https://developers.openai.com/api/docs/guides/error-codes.md, https://developers.openai.com/api/docs/guides/rate-limits.md, https://developers.openai.com/api/docs/guides/streaming-responses?api-mode=chat, https://developers.openai.com/api/docs/guides/images-vision.md, https://developers.openai.com/api/docs/changelog.md, https://raw.githubusercontent.com/openai/openai-openapi/main/openapi.yaml, https://raw.githubusercontent.com/openai/openai-python/main/src/openai/types/chat/

## claims
- [C1] D1 base URL `https://api.openai.com/v1`（spec 2.3.0） | src: https://raw.githubusercontent.com/openai/openai-openapi/main/openapi.yaml | quote: "servers: - url: https://api.openai.com/v1" | type: official
- [C2] D1 Bearer 鉴权；可选 `OpenAI-Organization`/`OpenAI-Project` 头 | src: https://developers.openai.com/api/reference/overview.md | quote: "Authorization: Bearer OPENAI_API_KEY_OR_ACCESS_TOKEN" | type: official
- [C3] D2 body 必填 `model`、`messages`；role=developer/system/user/assistant/tool/function | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "With o1 models and newer, `developer` messages replace the previous `system` messages." | type: official
- [C4] D2 function 角色消息、`functions`、`function_call` 均 deprecated | src: https://raw.githubusercontent.com/openai/openai-openapi/main/openapi.yaml | quote: "Deprecated in favor of `tools`." | type: official
- [C5] D2 content=字符串或 part 数组（developer/system/tool 仅 text） | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "For developer messages, only type `text` is supported." | type: official
- [C6] D3 user part：`text`、`image_url{url,detail:auto|low|high}`、`input_audio{data,format:wav|mp3}`、`file{file_id|file_data,filename}` | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Can contain text, image, or audio inputs." | type: official
- [C7] D4 tools[]：`{type:"function",function:{name,description,parameters,strict}}` 或 `{type:"custom",custom:{name,description,format}}` | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "A custom tool that processes input using a specified format." | type: official
- [C8] D4 tool_choice：none|auto|required|`{type:"function",function:{name}}`|custom 同形|`{type:"allowed_tools",allowed_tools:{mode,tools}}` | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "`none` is the default when no tools are present. `auto` is the default if tools are present." | type: official
- [C9] D4 `tool_calls[]{id,type,function:{name,arguments}}`，arguments 是 JSON 串；回传 `{role:"tool",tool_call_id,content}` | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Note that the model does not always generate valid JSON" | type: official
- [C10] D4/D6 GPT-5.4 起工具调用只能配 effort=none | src: https://developers.openai.com/api/docs/guides/migrate-to-responses.md | quote: "Starting with GPT-5.4, Chat Completions does not support tool calling with `reasoning_effort` values other than `none`." | type: official
- [C11] D5 无状态 | src: https://developers.openai.com/api/docs/guides/migrate-to-responses.md | quote: "In Chat Completions, conversation state must be managed manually." | type: official
- [C12] D5 `store:true` 才可 `GET /chat/completions`、`GET|POST|DELETE …/{completion_id}` | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "stored with the `store` parameter set to `true`" | type: official
- [C13] D5 新项目推荐 Responses | src: https://developers.openai.com/api/docs/guides/migrate-to-responses.md | quote: "Responses is recommended for all new projects." | type: official
- [C14] D6 `reasoning_effort` | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`." | type: official
- [C15] D6 推理内容不返回（只计入 reasoning_tokens） | src: https://developers.openai.com/api/docs/guides/reasoning.md | quote: "While reasoning tokens are not visible via the API" | type: official
- [C16] D7 response_format：text|json_object|`{type:"json_schema",json_schema:{name,description,schema,strict}}` | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Setting to `{ "type": "json_object" }` enables the older JSON mode" | type: official
- [C17] D7 `max_tokens` 弃用且不兼容 o 系列，改用 `max_completion_tokens` | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "deprecated in favor of `max_completion_tokens`, and is not compatible with" | type: official
- [C18] D8 `object:"chat.completion.chunk"`；`choices[].delta{role,content,refusal,tool_calls[{index,id,type,function}]}`；+`obfuscation` | src: https://developers.openai.com/api/reference/resources/chat/subresources/completions/streaming-events.md | quote: "Each chunk has the same ID." | type: official
- [C19] D8 SSE `data:` 块，`[DONE]` 结束；include_usage 末块 choices=[] 带 usage | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "an additional chunk will be streamed before the `data: [DONE]` message" | type: official
- [C20] D9 `object:"chat.completion"`；`message{role:"assistant",content,refusal,annotations,audio,tool_calls}` | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "The object type, which is always `chat.completion`." | type: official
- [C21] D9 finish_reason：stop|length|tool_calls|content_filter|function_call | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "or `function_call` (deprecated) if the model called a function" | type: official
- [C22] D9 usage：prompt/completion/total_tokens，prompt_tokens_details{cached_tokens,cache_write_tokens}，completion_tokens_details{reasoning_tokens} | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Total number of tokens used in the request (prompt + completion)." | type: official
- [C23] D10 缓存默认自动开启；最小长度 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later" | type: official
- [C24] D10 `prompt_cache_options{mode,ttl:"30m"}`、part 级 `prompt_cache_breakpoint`、`prompt_cache_key`；`prompt_cache_retention` 弃用 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Supported for `gpt-5.6` and later models." | type: official
- [C25] D12 `{"error":{"message","type","param","code"}}` | src: https://raw.githubusercontent.com/openai/openai-openapi/main/openapi.yaml | quote: "required: - type - message - param - code" | type: official
- [C26] D12 429+`Retry-After`；x-ratelimit-{limit,remaining,reset}-{requests,tokens} | src: https://developers.openai.com/api/docs/guides/error-codes.md | quote: "A `429` response with the `rate_limit_error` type and `slow_down` code" | type: official

## conflicts
- store 默认：openapi.yaml "default: false"；migrate-to-responses.md "Chat completions are stored by default for new accounts."
- image detail：chat.md 仅 "auto" or "low" or "high"；images-vision.md "`low`, `high`, `original`, or `auto`"
- seed：chat.md "This feature is in Beta."；openapi.yaml "deprecated: true"

## gaps
- custom 工具调用的流式 delta 形状未找到
- GPT-5.6 前模型最小缓存长度无具体数

## leads
- `moderation` 参数/响应字段（2026-06-04）
- GPT-6 Astra：Chat 无工具，effort none→400
- stop、verbosity、service_tier、web_search_options、audio、prediction
