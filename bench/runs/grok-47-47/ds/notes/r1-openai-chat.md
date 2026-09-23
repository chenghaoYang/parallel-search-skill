# r1-openai-chat
question: OpenAI 官方 Chat Completions 当前的请求与响应协议到底长什么样？
checked: https://platform.openai.com/docs/api-reference/chat, https://platform.openai.com/docs/api-reference/chat.md, https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml, https://developers.openai.com/api/reference/resources/chat.md, https://developers.openai.com/api/reference/overview.md, https://developers.openai.com/api/reference/resources/chat/subresources/completions/streaming-events.md, https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/retrieve.md, https://developers.openai.com/api/docs/guides/migrate-to-responses.md, https://developers.openai.com/api/docs/deprecations.md

## claims
- [C1] D1 POST `/chat/completions`。无页眉日期；OpenAPI 2.3.0。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "**post** `/chat/completions`" | type: official
- [C2] D1 base `https://api.openai.com/v1`。 | src: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml | quote: "curl https://api.openai.com/v1/chat/completions" | type: official
- [C3] D1 Bearer；可选 `OpenAI-Organization`、`OpenAI-Project`。`openai-version` 现为 `2020-10-01`。 | src: https://developers.openai.com/api/reference/overview.md | quote: "Authorization: Bearer OPENAI_API_KEY_OR_ACCESS_TOKEN" | type: official
- [C5] D2 `messages`＝本次对话至今。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "A list of messages comprising the conversation so far." | type: official
- [C6] D2 客户端重放累积 `messages`。 | src: https://developers.openai.com/api/docs/guides/migrate-to-responses.md | quote: "send the accumulated `messages` array on each request." | type: official
- [C7] D2 无续写用对话 id。 | src: https://developers.openai.com/api/docs/guides/migrate-to-responses.md | quote: "conversation state must be managed manually." | type: official
- [C8] D2 id 是 `completion_id`；GET 仅 `store: true`。 | src: https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/retrieve.md | quote: "the `store` parameter set to `true` will be returned." | type: official
- [C9] D2 OpenAPI `store.default` false，用于蒸馏/evals。 | src: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml | quote: "model distillation or evals products." | type: official
- [C10] D3 role：`developer` `system` `user` `assistant` `tool` `function`。delta 无 function。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "in this case `developer`." | type: official
- [C11] D3 `content` 为 string 或数组；developer/system/tool 仅 `text`。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "only type `text` is supported." | type: official
- [C12] D3 user `type`：`text` `image_url` `input_audio` `file`；assistant 另有 `refusal`。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Always `input_audio`." | type: official
- [C13] D4 `developer` 替换 o1 及更新模型上的旧 `system`。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "`developer` messages replace the previous `system` messages." | type: official
- [C14] D4 `system` 仍在，但 o1 及更新模型应改用 `developer`。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "use `developer` messages for this purpose instead." | type: official
- [C15] D5 `type: "function"` 的 `name`/`parameters` 在嵌套 `function`。省略 parameters＝空参数。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Omitting `parameters` defines a function with an empty parameter list." | type: official
- [C16] D5 `tool_choice`：`none` `auto` `required` 或 `{"type":"function","function":{"name":"my_function"}}`。默认 none/auto。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "`none` is the default when no tools are present." | type: official
- [C17] D5 结果为 `role: "tool"` + `tool_call_id`。回传 `tool_calls[].function.{name,arguments}`。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Tool call that this message is responding to." | type: official
- [C18] D6 `max_completion_tokens` 含可见输出与 reasoning tokens。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "including visible output tokens and reasoning tokens." | type: official
- [C19] D6 `max_tokens` 已弃用，不兼容 o-series。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "not compatible with o-series models." | type: official
- [C20] D6 `temperature` 0–2；schema `default: 1`（渲染页未写默认）。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "between 0 and 2." | type: official
- [C21] D6 `reasoning_effort`：none minimal low medium high xhigh max。组件 default medium。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`." | type: official
- [C22] D6 GPT-5.4 起非 `none` 不能 tool calling。 | src: https://developers.openai.com/api/docs/guides/migrate-to-responses.md | quote: "`reasoning_effort` values other than `none`." | type: official
- [C23] D7 `stream: true` 为 SSE；`choices[].delta`；`object`=`chat.completion.chunk`。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "using server-sent events." | type: official
- [C24] D7 流以 `data: [DONE]` 结束（`include_usage` 句；events 页未单列该行）。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "before the `data: [DONE]` message." | type: official
- [C25] D8 `choices[].message`，`role`=`assistant`，`object`=`chat.completion`。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "always `chat.completion`." | type: official
- [C26] D8 `finish_reason`：stop length tool_calls content_filter function_call。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "`function_call` (deprecated) if the model called a function." | type: official
- [C27] D8 `usage.prompt_tokens` / `completion_tokens` / `total_tokens`；另有 `reasoning_tokens`。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Number of tokens in the prompt." | type: official
- [C28] D9 `response_format.type`：text json_schema json_object。子字段 name description schema strict。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "json_schema: object { name, description, schema, strict }" | type: official
- [C29] D9 `json_object` 须 system 或 user 要求才出 JSON。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "without a system or user message instructing it to do so." | type: official
- [C30] D10 新项目建议 Responses；该句无 legacy。 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "trying Responses to take advantage of the latest OpenAI platform features." | type: official
- [C31] D10 仍受支持；Responses 为其演进。 | src: https://developers.openai.com/api/docs/guides/migrate-to-responses.md | quote: "Chat Completions remains supported, Responses is recommended for all new projects." | type: official
- [C32] D10 2022-06-03 legacy 列表无本端点；只作 `/v1/edits` 替代（2024-01-04）。 | src: https://developers.openai.com/api/docs/deprecations.md | quote: "models and endpoints that no longer receive updates." | type: official

## conflicts
- store：OpenAPI 2.3.0 `default: false`（yaml “evals products.”）对上迁移指南 “stored by default for new accounts.”（https://developers.openai.com/api/docs/guides/migrate-to-responses.md）。未裁决。
- 同页 tools：“only `function` is supported” 对上 “custom tools” 与 “Always `custom`”（https://developers.openai.com/api/reference/resources/chat.md）。

## gaps
- platform.openai.com/docs/api-reference/chat 为 403；`.md` 实为 API Overview。md 无更新日期。
- events 页与示例无单独 `data: [DONE]` 行。渲染页未写 temperature 默认。未见把本端点标成 legacy 的原句。

## leads
- 已存 completion：GET/POST（只改 metadata）/DELETE `/{completion_id}`，GET `.../messages`。
- 弃用形仍在：`functions`、`function_call`、`role: "function"`。另有 `verbosity`、`web_search_options`。
