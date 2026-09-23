# r1-qwen
question: 阿里云百炼（DashScope / Model Studio）OpenAI 兼容模式的请求与响应，相对它自己文档所声称的 Chat Completions 兼容，多了或改了哪些字段？
checked: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions, https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope, https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions, https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope

## claims
- [C1] D1 北京 SDK base_url 含 compatible-mode/v1（last-modified 2026-09-22）。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1" | type: official
- [C2] D1 北京 HTTP 为 POST 同一路径加 /chat/completions。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" | type: official
- [C3] D1 SDK 的 Base URL 不含 /chat/completions。 | src: https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope | quote: "不含 /chat/completions 的地址" | type: official
- [C4] D1 另有新加坡、弗吉尼亚 us-east-1、法兰克福、东京、香港，路径同为 /compatible-mode/v1。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1" | type: official
- [C5] D1 鉴权为 Authorization: Bearer $DASHSCOPE_API_KEY。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "Authorization: Bearer $DASHSCOPE_API_KEY" | type: official
- [C6] D1 API Key 按地域绑定，跨地域 HTTP 401、invalid_api_key。 | src: https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope | quote: "必须使用在同一地域创建的 API Key" | type: official
- [C7] D2 messages 必选，按对话顺序排列。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "按对话顺序排列。" | type: official
- [C8] D2 回放 tool_calls（id、type=function、name、arguments、index）；有 tool_calls 时 content 可空。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "由上一轮模型响应的 tool_calls 字段获得。" | type: official
- [C9] D2 Tool Message：role=tool，content 为字符串，tool_call_id 必选。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "固定为 tool。" | type: official
- [C10] D2 思考回放字段是 assistant.reasoning_content，禁止拼进 content。preserve_thinking 默认 false，放 extra_body。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "不支持将 reasoning_content 拼接到 content 字段中回传。" | type: official
- [C11] D3 role 固定 system、user、assistant、tool。user content 为 string，或多模态/缓存 array。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "系统消息的角色，固定为 system。" | type: official
- [C12] D3 array 的 type：text、image_url、input_audio、video、video_url。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "输入文本时需设为 text。" | type: official
- [C13] D4 System Message 可选，一般在 messages 首位。QVQ 设置不生效。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "QVQ 模型设置 System Message 不会生效。" | type: official
- [C14] D5 tools[].type 仅 function；name、description、parameters（JSON Schema）。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "当前仅支持设为 function。" | type: official
- [C15] D5 tool_choice 默认 auto，另有 none、required、指定 function。Qwen 暂不支持 required；思考模式不能强制指定工具。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "Qwen 系列模型暂不支持 required" | type: official
- [C16] D5 parallel_tool_calls 默认 false。tool_stream 默认 false，仅 stream=true，放 extra_body。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "仅在 stream=true 时生效。" | type: official
- [C17] D6 max_tokens 即将废弃，改用 max_completion_tokens（思维链+回答）。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "新接入请使用 max_completion_tokens。" | type: official
- [C18] D6 enable_thinking 非标准：Python 放 extra_body，HTTP 放 body 顶层。开启后走 reasoning_content。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "放在请求体（body）的顶层即可" | type: official
- [C19] D6 thinking_budget 为思考最大 Token，只写 extra_body。MiniMax-M3 用 thinking.type=adaptive 或 disabled。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "思考过程的最大 Token 数。" | type: official
- [C20] D6 reasoning_effort 被写成 OpenAI 标准参数，SDK 直传，不放 extra_body。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "reasoning_effort 是 OpenAI 标准参数。" | type: official
- [C21] D7 stream 默认 false。include_usage 默认 false，仅 stream=true；为 true 时最后一块 choices 为空。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "choices 在最后一个 chunk 中为空数组。" | type: official
- [C22] D7 delta.reasoning_content 为增量思维链；message.reasoning_content 为全文。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "增量思维链内容。" | type: official
- [C23] D8 message：content、reasoning_content、role=assistant、tool_calls。function_call 废弃且固定 null。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "该值固定为 null，请参考 tool_calls 参数。" | type: official
- [C24] D8 非流式 finish_reason：stop、length、tool_calls。流式再加 null。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "需要调用工具而结束为 tool_calls。" | type: official
- [C25] D8 usage 有 prompt_tokens、completion_tokens、total_tokens；reasoning_tokens 属 text_tokens；另有 cached_tokens。cache_type=ephemeral。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "reasoning_tokens 是 text_tokens 中对应思考过程的子集" | type: official
- [C26] D9 response_format 默认 {"type":"text"}，另有 json_object 与 json_schema。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "{\"type\": \"json_object\"}" | type: official
- [C27] D10 非标准、Python 放 extra_body：top_k、repetition_penalty、vl_high_resolution_images、enable_thinking、thinking、preserve_thinking、thinking_budget、tool_stream、enable_code_interpreter、enable_search、search_options、skill、clear_thinking。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "该参数非 OpenAI 标准参数。" | type: official
- [C28] D10 头 X-DashScope-DataInspection 为 '{"input":"cip","output":"cip"}'。service_tier 与 system_fingerprint 固定 null。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "{\"input\":\"cip\",\"output\":\"cip\"}" | type: official
- [C29] D10 Qwen-Audio 不支持 OpenAI 兼容，只支持 DashScope。 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "仅支持 DashScope 协议。" | type: official

## conflicts
- 弗吉尼亚：Chat "{WorkspaceId}.us-east-1.maas.aliyuncs.com"；概览 "dashscope-us.aliyuncs.com/compatible-mode/v1"。src: checked 的中文 Chat 页与中文概览页
- 英概览北京："Beijing: https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"。中文页与该页迁移段为 cn-beijing。src: https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope
- 概览 "tools 暂时无法与 stream=True 同时使用。"；"仅 messages[0] 中支持 role 为 system"；finish_reason 只写 null、stop、length；指纹 "返回为空字符串。" Chat 页 tool_stream "仅在 stream=true 时生效。"，有 role=tool，非流式 finish_reason 含 tool_calls，指纹 "该参数当前固定为 null。" src: checked 的两篇中文页

## gaps
- 无 frequency_penalty、logit_bias、user 的不支持原句。写明不支持的是 Qwen-Audio、required、思考模式强制工具、Node.js 护栏头。
- thinking_budget 未写 HTTP 位置；写明 body 顶层的只有 enable_thinking、use_multichannel。
- 更新日期只在 meta last-modified。英文页无该 meta。

## leads
- Anthropic：https://help.aliyun.com/zh/model-studio/anthropic-api-messages
- DashScope 总览：https://help.aliyun.com/zh/model-studio/qwen-api-reference/
- Responses：https://help.aliyun.com/zh/model-studio/openai-compatible-responses/
