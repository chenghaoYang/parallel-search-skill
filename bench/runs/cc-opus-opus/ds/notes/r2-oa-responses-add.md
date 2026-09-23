# r2-oa-responses-add
question: Follow-up (r2): claims found but left out for space — max_output_tokens includes reasoning tokens?; tool_choice values and shape in Responses; parallel_tool_calls, max_tool_calls; previous_response_id and conversation can't be used together; truncation marked Deprecated; background mode (~10 min retention); text.verbosity; HTTP error body error.{type,code,param}
checked: https://developers.openai.com/api/reference/resources/responses/methods/create, https://developers.openai.com/api/reference/resources/responses/methods/create.md, https://developers.openai.com/api/docs/guides/function-calling, https://developers.openai.com/api/docs/guides/background, https://developers.openai.com/api/docs/guides/error-codes

## claims
- [C1] D7：max_output_tokens 是整个 response 的生成上限，可见输出和推理 token 都算在内 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens." | type: official
- [C2] D4：tool_choice 字符串取值 "none" / "auto" / "required" | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "none means the model will not call any tool and instead generates a message. auto means the model can pick between generating a message or calling one or more tools. required means the model must call one or more tools." | type: official
- [C3] D4：强制调用某个函数用扁平对象 {"type":"function","name":…}（示例里没有嵌套的 function 键） | src: https://developers.openai.com/api/docs/guides/function-calling | quote: 「Forced Function: Call exactly one specific function. tool_choice: {"type": "function", "name": "get_weather"}」 | type: official
- [C4] D4：tool_choice 另可为 allowed_tools 对象 {type:"allowed_tools", mode:"auto"/"required", tools:[…]} | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "ToolChoiceAllowed object { mode, tools, type } Constrains the tools available to the model to a pre-defined set." | type: official
- [C5] D4：parallel_tool_calls 设为 false 时，每轮只调用 0 个或 1 个工具 | src: https://developers.openai.com/api/docs/guides/function-calling | quote: "The model may choose to call multiple functions in a single turn. You can prevent this by setting parallel_tool_calls to false, which ensures exactly zero or one tool is called." | type: official
- [C6] D4：max_tool_calls 只限制内置工具调用，按所有内置工具合计，不按单个工具算 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool." | type: official
- [C7] D5：previous_response_id 不能和 conversation 一起用 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation." | type: official
- [C8] D5：HTML 参考里，请求体的 truncation（"auto"/"disabled"）字段名前有 "Deprecated" 徽标 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: 「Deprecated truncation: optional "auto" or "disabled" or null」 | type: official
- [C9] D5：background 模式下，ZDR 项目的后台请求按 store=false 运行，response 数据暂存磁盘约 10 分钟，用于异步执行和轮询 | src: https://developers.openai.com/api/docs/guides/background | quote: "Background requests from Zero Data Retention (ZDR) projects run with store=false. Response data is temporarily stored to disk for roughly 10 minutes to enable asynchronous execution and polling." | type: official
- [C10] D7：text.verbosity 取值 low / medium / high，默认 medium | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "Constrains the verbosity of the model’s response. Lower values will result in more concise responses, while higher values will result in more verbose responses. Currently supported values are low, medium, and high. The default is medium." | type: official
- [C11] D12：HTTP 错误体里有 error.code 和 error.type；计费类错误的 error.type 仍可能是 insufficient_quota | src: https://developers.openai.com/api/docs/guides/error-codes | quote: "For billing-related errors, inspect error.code to identify the specific cause. The broader error.type can still be insufficient_quota." | type: official
- [C12] D12：HTTP 错误体里有 error.param；示例中 error.type 为 invalid_request_error | src: https://developers.openai.com/api/docs/guides/error-codes | quote: "as an invalid_request_error with error.param set to service_tier when a request selects or resolves to a service tier that is not allowed for the project" | type: official

## conflicts
- 无

## gaps
- truncation 的弃用只以徽标形式出现在 HTML 参考的请求体字段上。页面没有说明原因或替代字段；同一页的 .md 版本（create.md）不显示这个徽标；Response 对象里的 truncation 字段也没有徽标。

## leads
- 根据 background 指南，开启 Modified Abuse Monitoring 的项目，若后台请求没有显式传 store=true，response 约 10 分钟后删除。
- D12 相关：流式 error 事件字段为 {code, message, param, sequence_number, type:"error"}（Responses 参考）；WebSocket 错误信封为 {type:"error", status, error{type,code,message,param}}（websocket-mode 指南）。
