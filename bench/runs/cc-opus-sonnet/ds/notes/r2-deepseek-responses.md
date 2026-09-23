# r2-deepseek-responses
question: DeepSeek 官方 Responses API（2026-08-13 上线）的逐字段支持情况是什么？相对 OpenAI 官方 Responses，哪些字段/事件/行为不同？
checked: https://api-docs.deepseek.com/guides/responses_api, https://api-docs.deepseek.com/zh-cn/guides/responses_api, https://api-docs.deepseek.com/updates, https://api-docs.deepseek.com/api/create-response

## claims
- [C1] 端点路径为 POST /responses | src: https://api-docs.deepseek.com/api/create-response | quote: "POST /responses" | type: official
- [C2] 端点定义："以 OpenAI Responses API 格式创建一个模型响应" | src: https://api-docs.deepseek.com/api/create-response | quote: "Creates a model response in the OpenAI Responses API format." | type: official
- [C3] API 无状态：响应/对话不在服务端保存 | src: https://api-docs.deepseek.com/api/create-response | quote: "The API is stateless: responses and conversations are not stored on the server." | type: official
- [C4] store：不支持，响应恒为 store:false | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Not supported. The response always carries store: false" | type: official
- [C5] previous_response_id 与 conversation 均不支持（同一理由） | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Not supported (stateless API)" | type: official
- [C6] instructions：支持，作为第一条 system 消息插入 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Supported. Inserted as the first system message" | type: official
- [C7] message 的 content 支持字符串及 input_text/output_text/input_image 三种内容块 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "content supports strings and input_text / output_text / input_image content parts" | type: official
- [C8] reasoning 输入项支持，明文 content 并入相邻 assistant 消息；summary、encrypted_content 不支持 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Supported. Plain-text content is merged into the adjacent assistant message; summary and encrypted_content are not supported" | type: official
- [C9] tools.custom 仅支持 apply_patch，其他 name 返回 400 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Only {\"type\": \"custom\", \"name\": \"apply_patch\"} is supported (for Codex compatibility); other names return a 400 error" | type: official
- [C10] web_search/file_search/code_interpreter/computer_use/mcp 等内置工具均被忽略 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "web_search / file_search / code_interpreter / computer_use / mcp / other built-in tools Ignored" | type: official
- [C11] tool_choice 支持 none/auto/required/指定工具 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Supported. none / auto / required / a specific tool ({\"type\": \"function\", \"name\": ...})" | type: official
- [C12] reasoning 顶层参数部分支持：effort 支持；summary 可传但不生成摘要 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Partially supported. effort supported; summary accepted but no summary is generated" | type: official
- [C13] reasoning.effort 取值 none/low/high/max；不设置则用模型默认（默认开启思考） | src: https://api-docs.deepseek.com/api/create-response | quote: "none disables thinking mode; low / high / max enable thinking mode. If not set, the model's default thinking behavior is used (enabled by default)." | type: official
- [C14] include/background/metadata/service_tier 四个参数状态同一措辞 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Not supported" | type: official
- [C15] text 顶层参数部分支持：format 完整支持；verbosity 可传但无效果 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Partially supported. format fully supported; verbosity accepted but has no effect" | type: official
- [C16] text.format 取值枚举 | src: https://api-docs.deepseek.com/api/create-response | quote: "Possible values: [text, json_object, json_schema]" | type: official
- [C17] max_output_tokens 上限含可见输出 token 与 reasoning token 之和 | src: https://api-docs.deepseek.com/api/create-response | quote: "An upper bound for the number of tokens that can be generated in the response, including both the visible output tokens and the reasoning tokens." | type: official
- [C18] temperature 范围[0.0,2.0]，思考模式下不生效 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Supported (range [0.0, 2.0]; no effect in thinking mode)" | type: official
- [C19] top_p 仅思考模式生效，下限0.95；非思考模式恒为1.0 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Supported (takes effect in thinking mode, with a lower bound of 0.95; in non-thinking mode it is fixed at 1.0)" | type: official
- [C20] truncation：不支持，超上下文窗口返回400 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Not supported. Requests exceeding the context window return a 400 error" | type: official
- [C21] prompt_cache_key/prompt_cache_retention：不支持，缓存由服务端自动管理 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Not supported. Context caching is managed automatically" | type: official
- [C22] 不支持的参数被静默忽略、不报错 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Unsupported parameters are silently ignored and do not cause errors" | type: official
- [C23] 流式事件里 reasoning 以明文增量文本传输，非加密 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "response.reasoning_text.delta / response.reasoning_text.done Incremental chain-of-thought text / the full chain-of-thought text" | type: official
- [C24] 响应 output item.type 枚举为 message/reasoning/function_call | src: https://api-docs.deepseek.com/api/create-response | quote: "Possible values: [message, reasoning, function_call] The type of the output item." | type: official
- [C25] response.status 枚举为 in_progress/completed/incomplete/failed | src: https://api-docs.deepseek.com/api/create-response | quote: "Possible values: [in_progress, completed, incomplete, failed] The status of the response." | type: official
- [C26] incomplete_details.reason 只有 max_output_tokens 或 content_filter | src: https://api-docs.deepseek.com/api/create-response | quote: "The details about why the response is incomplete. The reason field can be max_output_tokens or content_filter." | type: official
- [C27] usage.input_tokens_details.cached_tokens 存在；未见 Chat Completions 式 prompt_cache_hit_tokens 命名 | src: https://api-docs.deepseek.com/api/create-response | quote: "cached_tokens integer Number of input tokens that hit the context cache." | type: official
- [C28] usage.output_tokens_details.reasoning_tokens：模型生成的思维链 token 数 | src: https://api-docs.deepseek.com/api/create-response | quote: "reasoning_tokens integer Number of reasoning (chain-of-thought) tokens generated by the model." | type: official
- [C29] 未支持能力对应字段恒为固定值 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Fields that depend on unsupported capabilities always take fixed values (e.g. store: false, previous_response_id: null, parallel_tool_calls: true)." | type: official
- [C30] input 支持回传的 item 类型含 reasoning——多轮时客户端靠这个把上一轮明文推理塞回去 | src: https://api-docs.deepseek.com/api/create-response | quote: "Supported input item types are message / function_call / function_call_output / custom_tool_call / custom_tool_call_output / reasoning; other types are ignored." | type: official
- [C31] changelog（2026-08-13，标题 "Native support for the Responses API"）原句 | src: https://api-docs.deepseek.com/updates | quote: "The DeepSeek API now natively supports the OpenAI Responses API format and is specifically adapted for Codex." | type: official

## conflicts
- create-response 页内不一致：reasoning output item 字段表未列 summary，但示例 JSON 该 item 带 `"summary": []`（同 src）。
- EN/zh-cn 两版支持表逐行核对一致，未发现跨语言冲突。

## gaps
- guide/create-response 页均无独立更新日期，唯一锚点是 changelog 的 "Date: 2026-08-13"。
- 未查到 "prompt_cache_hit_tokens" 出现在 Responses 页面（仅见 cached_tokens），无原句可引。
- 未开 Multi-round Conversation / Thinking Mode 指南页，如有专属补充未覆盖。
- 未查 OpenAI 官方 Responses 文档，字段命名/枚举差异需主 agent 自行核对。

## leads
- reasoning 只给明文、不给 encrypted_content，是与 OpenAI 最大分歧点，命中 Q1。
- custom 工具唯一支持 apply_patch，专为 Codex 而设；Codex 集成相关格子可交叉引用。
- 旧模型 web_search_call item 传回 input 仍会被还原拼接进上下文；2026-09-10 changelog 显示 deepseek-flash 已指向 V4.1 Flash。
