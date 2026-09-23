# r1-deepseek
question: DeepSeek 官方API相对OpenAI Chat Completions/Responses及Anthropic Messages的实际偏差？
checked: https://api-docs.deepseek.com/, https://api-docs.deepseek.com/api/create-chat-completion, https://api-docs.deepseek.com/guides/thinking_mode, https://api-docs.deepseek.com/guides/responses_api, https://api-docs.deepseek.com/guides/anthropic_api, https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/guides/tool_calls, https://api-docs.deepseek.com/guides/chat_prefix_completion, https://api-docs.deepseek.com/guides/fim_completion, https://api-docs.deepseek.com/guides/vision, https://api-docs.deepseek.com/updates, https://api-docs.deepseek.com/guides/reasoning_model

## claims
- [C1] Anthropic兼容base_url同域换路径:https://api.deepseek.com/anthropic | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "the base_url being https://api.deepseek.com/anthropic" | type: official
- [C2] 确有Responses API，base_url与ChatCompletions同域(不是独立主机) | src: https://api-docs.deepseek.com/guides/responses_api | quote: "the base_url being https://api.deepseek.com" | type: official
- [C3] /beta是解锁Beta功能(前缀续写/FIM/strict)的独立base_url | src: https://api-docs.deepseek.com/guides/chat_prefix_completion | quote: "base_url=\"https://api.deepseek.com/beta\" to enable the Beta feature" | type: official
- [C4] ChatCompletions的model枚举仅剩deepseek-flash/deepseek-v4-pro，旧名不在列 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Possible values: [ deepseek-flash , deepseek-v4-pro ]" | type: official
- [C5] deepseek-chat/reasoner已公告2026-07-24停用，被v4-pro/v4-flash取代 | src: https://api-docs.deepseek.com/updates | quote: "deepseek-chat and deepseek-reasoner, will be discontinued in three months (2026-07-24)" | type: official
- [C6] Responses API的developer角色被当作user；ChatCompletions无developer角色 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "developer ( developer is treated as user )" | type: official
- [C7] 图像输入两协议都支持，格式JPEG/PNG/GIF/WebP | src: https://api-docs.deepseek.com/guides/vision | quote: "Supported image formats: JPEG, PNG, GIF, and WebP." | type: official
- [C8] 硬盘缓存默认对所有用户开启，每次请求自动触发构建 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "enabled by default for all users, allowing them to benefit without needing to modify their code" | type: official
- [C9] usage含prompt_cache_hit/miss_tokens，且prompt_tokens_details.cached_tokens明确=hit_tokens | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Same as prompt_cache_hit_tokens." | type: official
- [C10] reasoning_content是OpenAI schema外多出字段，仅思考模式出现 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "For thinking mode only. The reasoning contents of the assistant message" | type: official
- [C11] finish_reason比OpenAI多两个自有值 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "insufficient_system_resource , aborted" | type: official
- [C12] frequency_penalty/presence_penalty标记deprecated，传了静默无效(未分模式) | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "no longer supported. It will not take effect if you pass it to the API." | type: official
- [C13] strict工具调用须切/beta，逐函数设strict:true，服务端校验Schema | src: https://api-docs.deepseek.com/guides/tool_calls | quote: "Use base_url=\"https://api.deepseek.com/beta\" to enable Beta features" | type: official
- [C14] 思考模式下tool_choice用required/具名工具直接400 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "required and named tool choices are not supported in thinking mode; the API returns a 400 error." | type: official
- [C15] Responses API的parallel_tool_calls字段被忽略，并行恒开启不可关 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "parallel_tool_calls Ignored (parallel tool calling is always enabled)" | type: official
- [C16] 思考模式默认开启，默认强度high，靠参数而非模型名切换 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "Thinking mode is enabled by default, with the default effort being high" | type: official
- [C17] reasoning_effort枚举none/low/high/max，旧别名minimal/medium/xhigh被静默重映射 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "minimal is accepted and mapped to low" | type: official
- [C18] 带tools时前序reasoning_content须回传并拼入上下文；不带tools则不需回传且被忽略 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "should be passed back to the API and will be concatenated" | type: official
- [C19] 工具调用轮次reasoning_content回传错误会400，非静默降级 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "If your code does not correctly pass back reasoning_content, the API will return a 400 error." | type: official
- [C20] 思考模式下temperature/presence/frequency_penalty静默无效；top_p仅思考模式生效且下限0.95 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "will not trigger an error but will also have no effect" | type: official
- [C21] response_format.type枚举只有text/json_object，未见json_schema | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Must be one of text or json_object." | type: official
- [C22] 流式usage只在最后一个内容chunk出现，不单发usage-only chunk | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "the statistics ride on the last content chunk" | type: official
- [C23] Responses API流式无data:[DONE]，靠response.completed/incomplete/failed收尾 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "there is no data: [DONE] message" | type: official
- [C24] max_tokens范围1-393216，默认非思考8K/思考64K/max效果时128K | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "default is 8K in non-thinking mode, 64K in thinking mode" | type: official
- [C25] 对话前缀续写:末条assistant消息设prefix:true且须切/beta | src: https://api-docs.deepseek.com/guides/chat_prefix_completion | quote: "set the prefix parameter of the last message to True" | type: official
- [C26] FIM补全在POST /completions非/chat/completions，须/beta，max_tokens硬顶4K | src: https://api-docs.deepseek.com/guides/fim_completion | quote: "The max tokens of FIM completion is 4K." | type: official
- [C27] anthropic-beta对/messages被忽略(Files API才需要)；anthropic-version直接忽略 | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "anthropic-beta Ignored for /messages" | type: official
- [C28] content block: document=Not Supported；cache_control在tools/text/tool_use/tool_result均Ignored | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "array, type = \"document\" Not Supported" | type: official
- [C29] Anthropic格式thinking支持但budget_tokens被忽略；output_config只认effort | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "thinking Supported ( budget_tokens is ignored )" | type: official
- [C30] tool_choice的auto/any/tool均Supported但disable_parallel_tool_use被忽略；mcp_servers/top_k均Ignored | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "disable_parallel_tool_use is ignored" | type: official
- [C31] Anthropic层静默重映射Claude模型名:claude-opus*→v4-pro，haiku*/sonnet*→flash | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "Models starting with claude-opus are mapped to deepseek-v4-pro" | type: official
- [C32] 近5周两次协议更新:08-13上线Responses API+三档思考强度；09-10模型名改deepseek-flash | src: https://api-docs.deepseek.com/updates | quote: "natively supports the OpenAI Responses API format" | type: official

## conflicts
- frequency/presence_penalty失效范围两页不一致：create-chat-completion页标全局deprecated；thinking_mode页把"无效"限定思考模式语境，均未明说非思考模式是否真生效。

## gaps
- SSE keep-alive注释/空行：已查页面均无原句，仅Perplexity综合答案提及，未采信。
- Responses API无逐字"POST /responses"路径原句，guide只给SDK写法。
- Chat Completions端parallel_tool_calls是否存在/默认值未见明文。
- developer角色传入Chat Completions报错与否未见明文。

## leads
- guide路径已变：function_calling现称/tool_calls；多轮对话现称/multi_round_chat(未开)。
- Files API(/guides/files_api)被anthropic_api/responses_api多次引用，值得单独深挖。
- updates页2026-04-24: V3.2-Speciale曾用临时base_url路径挂限时模型，是分裂先例。
