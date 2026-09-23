# r1-openai-responses
question: OpenAI Responses API（POST /v1/responses）官方规范：请求形状、事件流、与 Chat Completions 的结构差异。
checked: https://platform.openai.com/docs/guides/responses-vs-chat-completions, https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml, https://developers.openai.com/api/docs/changelog

## claims
- [C1] POST https://api.openai.com/v1/responses；body schema=CreateResponse；200 返回 JSON(Response) 或 SSE(ResponseStreamEvent)；header `Authorization: Bearer $OPENAI_API_KEY`；相关端点 GET/POST /responses/{id}(/cancel,/input_items)、POST /responses/input_tokens、POST /responses/compact | src: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml | quote: "-H \"Authorization: Bearer $OPENAI_API_KEY\"" | type: official
- [C2] body 顶层字段：model、input、instructions、max_output_tokens、store、stream、stream_options、tools、tool_choice、parallel_tool_calls、temperature、top_p、reasoning、text、include、previous_response_id、conversation、background、max_tool_calls、prompt、metadata、moderation、service_tier、prompt_cache_key、truncation(deprecated)、context_management | src: openapi.yaml | quote: "The truncation strategy to use" | type: official
- [C3] input = string（等价 user 文本）或 InputItem 数组（EasyInputMessage｜typed Item，type 判别） | src: openapi.yaml | quote: "A text input to the model, equivalent to a text input with the `user` role." | type: official
- [C4] EasyInputMessage role 枚举 user/assistant/system/developer，content 为 string 或 content-part 数组；typed InputMessage 仅 user/system/developer | src: openapi.yaml | quote: "One of `user`, `assistant`, `system`, or `developer`." | type: official
- [C5] instructions 为顶层 system/developer 消息；previous_response_id 不携带上一条的 instructions | src: openapi.yaml | quote: "the instructions from a previous response will not be carried over" | type: official
- [C6] Tool oneOf（type 判别）：function、file_search、computer、web_search（枚举 web_search｜web_search_2025_08_26）、mcp、code_interpreter、image_generation、local_shell、custom、apply_patch、tool_search、programmatic_tool_calling、namespace | src: openapi.yaml | quote: "One of `web_search` or `web_search_2025_08_26`." | type: official
- [C7] function 工具扁平：{type:"function", name, parameters, description, strict, output_schema…}，无 `function:{}` 包裹层 | src: openapi.yaml | quote: "The type of the function tool. Always `function`." | type: official
- [C8] function_call 与 function_call_output 两种 Item 用 call_id 关联；内置调用 item 枚举 web_search_call、file_search_call、code_interpreter_call | src: https://platform.openai.com/docs/guides/responses-vs-chat-completions | quote: "correlated using a call_id." | type: official
- [C9] previous_response_id 多轮用，不能与 conversation 同用 | src: openapi.yaml | quote: "Use this to create multi-turn conversations." | type: official
- [C10] store 默认 true（至少存 30 天）；ZDR 组织强制 store:false | src: openapi.yaml | quote: "Defaults to true when omitted." | type: official
- [C11] 官方状态三选：previous_response_id／output items 放回 input／Conversations API；链上先前输入仍按 input 计费 | src: migration guide | quote: "Use previous_response_id when you want OpenAI to manage prior response context." | type: official
- [C12] stream boolean 默认 false，server-sent events | src: openapi.yaml | quote: "streamed to the client as it is generated using server-sent events" | type: official
- [C13] typed events：文本监听 response.created、response.output_text.delta、response.completed、error；function 流有 response.function_call_arguments.delta/.done | src: migration guide | quote: "listen for events such as: response.created response.output_text.delta response.completed error" | type: official
- [C14] spec 全事件名 60+（各含 sequence_number）：response.created/in_progress/completed/failed/incomplete、output_item.added/done、output_text.*、content_part.*、refusal.*、reasoning_text.*、reasoning_summary_text/part.*、function_call_arguments.*、内置工具 call 事件、error | src: openapi.yaml | quote: "The type of the event. Always `response.output_text.delta`." | type: official
- [C15] 非流式 Response（object:"response"）output 为 Item 数组（reasoning + message，content[].type=output_text）；SDK 有 output_text 便捷字段（Chat 无）| src: migration guide | quote: "an array of Items labeled output." | type: official
- [C16] max_output_tokens 整型 min 16，含 reasoning tokens | src: openapi.yaml | quote: "including visible output tokens and reasoning tokens." | type: official
- [C17] temperature 默认 1（0–2）、top_p 默认 1（0–1），建议二选一 | src: openapi.yaml | quote: "We generally recommend altering this or `top_p` but not both." | type: official
- [C18] reasoning.effort 枚举 none/minimal/low/medium/high/xhigh/max 默认 medium；reasoning.summary auto/concise/detailed；reasoning.context auto/current_turn/all_turns（gpt-5.6 家族默认 all_turns）| src: openapi.yaml | quote: "Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`." | type: official
- [C19] text.format oneOf：text（默认）、json_schema、json_object；json_object 为旧 JSON mode，新模型不推荐 | src: openapi.yaml | quote: "Setting to `{ \"type\": \"json_object\" }` enables the older JSON mode" | type: official
- [C20] 对应：chat 的 response_format → Responses 的 text.format | src: migration guide | quote: "Instead of response_format, use text.format in Responses." | type: official
- [C21] reasoning item（type:"reasoning"）手动上下文须放回 input；include:["reasoning.encrypted_content"] 供 store:false/ZDR 无状态多轮 | src: openapi.yaml | quote: "Includes an encrypted version of reasoning tokens" | type: official
- [C22] ZDR 用法：store:false + 回放每个返回 reasoning item | src: migration guide | quote: "Each item includes encrypted_content by default" | type: official
- [C23] 多模态 content 类型：input_text、input_image、input_file（InputContent oneOf）+ input_audio（base64，mp3/wav）| src: openapi.yaml | quote: "The type of the input item. Always `input_audio`." | type: official
- [C24] input_image 字段 image_url/file_id/detail(high|low|auto|original)；input_file 字段 file_id/filename/file_data/file_url | src: openapi.yaml | quote: "A fully qualified URL or base64 encoded image in a data URL." | type: official
- [C25] Chat 仍支持但 Responses 为新项目推荐；Assistants API 已于 2026-08-26 sunset | src: migration guide | quote: "The Assistants API was officially sunset on August 26, 2026, and is no longer available." | type: official
- [C26] changelog（March, 2025 组 Mar 11 条）：发布 Responses API + 内置 web search/file search/computer use + Agents SDK | src: https://developers.openai.com/api/docs/changelog | quote: "Released the Responses API , a new API for creating and using agents" | type: official
- [C27] changelog 时间线：2025-08-20 Conversations API；2025-12-11 /responses/compact；2026-01-15 Open Responses 开源规范；2026-02-23 WebSocket 模式 | src: changelog | quote: "Released the Conversations API, which allows you to create and manage long-running conversations with the Responses API." | type: official
- [C28] GPT-6 Astra 工具调用须走 Responses；GPT-5.4 起 Chat 不支持 reasoning_effort≠none 工具调用 | src: migration guide | quote: "Chat Completions does not support tool calling with reasoning_effort values other than none." | type: official
- [C29] 移除 n 参数，一次仅一个生成；Responses 是 agentic loop | src: migration guide | quote: "we've removed this param, leaving only one generation." | type: official
- [C30] 函数定义 internally tagged；省略 strict 即尝试 strict，不兼容则回退非严格（返回 strict:false） | src: migration guide | quote: "In Responses, they are internally tagged." | type: official

## conflicts
- encrypted_content：guide 称 "Each item includes encrypted_content by default"（C22）；spec 把 reasoning.encrypted_content 列为需显式 include 的 additional output data（C21）。可能 spec 述机制、guide 述新默认，未裁决。
- spec 内部：EasyInputMessage 允许 assistant 角色，typed InputMessage 仅 user/system/developer。

## gaps
- docs 页面无显式更新日期；changelog 仅 month-day+年份分组（Mar 11 属 March, 2025 组）。
- tools 数组上限（maxItems）spec 未给出。

## leads
- 下游兼容矩阵重点参数：conversation、context_management、prompt、stream_options、prompt_cache_key、moderation。
- 另有 /responses/input_tokens、WebSocket 模式、Open Responses 开源规范待下游单查。
- 内置工具另有 apply_patch、local_shell、tool_search、programmatic_tool_calling、namespace。
