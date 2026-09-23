# r2-minimax
question: MiniMax 开放平台 API（Anthropic 兼容与 OpenAI 兼容）相对 Anthropic Messages / OpenAI Chat Completions 官方规格的偏差是什么？
checked: https://platform.minimax.io/docs/api-reference/text-anthropic-api, https://platform.minimax.io/docs/api-reference/text-openai-api, https://platform.minimax.io/docs/api-reference/responses-create, https://platform.minimax.io/docs/guides/text-m2-function-call, https://platform.minimaxi.com/docs/api-reference/text-anthropic-api, https://platform.minimax.cn/docs/api-reference/text-anthropic-api, https://platform.minimax.cn/docs/api-reference/text-openai-api

## claims
- [C1] Anthropic 兼容 base URL（国际站）| src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "export ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic" | type: official
- [C2] Anthropic 兼容 base URL（国内站）| src: https://platform.minimax.cn/docs/api-reference/text-anthropic-api | quote: "ANTHROPIC_BASE_URL=https://api.minimax.cn/anthropic" | type: official
- [C3] OpenAI 兼容 base URL（国际站）| src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "OPENAI_BASE_URL=https://api.minimax.io/v1" | type: official
- [C4] OpenAI 兼容 base URL（国内站）| src: https://platform.minimax.cn/docs/api-reference/text-openai-api | quote: "OPENAI_BASE_URL=https://api.minimax.cn/v1" | type: official
- [C5] 一手域名 minimaxi.com 302 跳转到 minimax.cn，国内文档实托管在后者 | src: https://platform.minimaxi.com/docs/api-reference/text-anthropic-api | quote: "location: https://platform.minimax.cn/docs/api-reference/text-anthropic-api" | type: official
- [C6] 侧边栏把 Anthropic SDK 页标「推荐」，OpenAI SDK 页无此标记 | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "sidebarTitle":"Anthropic SDK (Recommended)" | type: official
- [C7] 存在 OpenAI Responses API 兼容端点（POST /v1/responses），支持流式/非流式 | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "Call MiniMax models via the OpenAI Responses API compatible main endpoint. Generates model replies, supports streaming and non-streaming." | type: official
- [C8] Anthropic 兼容 temperature：[0,2]，推荐 1，完全支持 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "Range [0, 2], controls output randomness, recommended value: 1" | type: official
- [C9] Anthropic 兼容 top_p：[0,1]，M3 默认0.95/M2.x默认0.9 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "Default 0.95 for MiniMax-M3 and 0.9 for M2.x models" | type: official
- [C10] top_k/stop_sequences/mcp_servers/context_management/container 全部被忽略 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "Some Anthropic parameters (such as top_k, stop_sequences, mcp_servers, context_management, container) will be ignored" | type: official
- [C11] tool_choice 完全支持 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "Tool selection strategy" | type: official
- [C12] thinking 完全支持；M3 默认关闭可用 adaptive 开启；M2.x 不能关闭 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "Thinking is off by default for MiniMax-M3 and can be enabled with adaptive. Thinking cannot be disabled for M2.x models." | type: official
- [C13] M2.x 传 disabled 不报错但无效 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "thinking: {"type": "disabled"} is accepted but thinking remains on." | type: official
- [C14] 响应含 thinking 块时后续轮次须原样保留，尤其工具调用对话 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "preserve them unchanged in later turns, especially in tool-use conversations" | type: official
- [C15] messages 部分支持：M2.7/M2.5/M2.1/M2 只支持 text 与 tool-call，不支持图片/视频输入（M3 才支持 image/video）| src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "The M2.7, M2.5, M2.1, and M2 series support text and tool-call content blocks only; they do not support image or video input" | type: official
- [C16] type="thinking" 内容块完全支持，多轮须原样返回 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "Reasoning content. Return the block unchanged in multi-turn thinking conversations" | type: official
- [C17] function-call 指南 M3 示例中 thinking 块含十六进制 signature 字段，但 API 参考页参数表全文未出现 "signature" | src: https://platform.minimax.io/docs/guides/text-m2-function-call | quote: "signature": "cfa12f9d651953943c7a3327805..." | type: official
- [C18] OpenAI 兼容 reasoning_split 只是输出格式开关，不控制是否思考 | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "reasoning_split does not enable or disable thinking. It only controls how thinking content is returned" | type: official
- [C19] reasoning_split=true 时用 reasoning_content/reasoning_details 分离返回思考 | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "when true, thinking is exposed through reasoning_content and reasoning_details" | type: official
- [C20] 默认（reasoning_split关闭）八个模型思考内容以 <think> 标签混在 content 字段里，须完整保留 | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "the content field will contain <think> tag content, which must be preserved completely" | type: official
- [C21] Interleaved Thinking 格式（reasoning_split=True）下思考经 reasoning_details 单独提供，须完整保留 | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "provided separately via the reasoning_details field, which must also be preserved completely" | type: official
- [C22] 工具调用多轮场景要求把完整 response_message（含 tool_calls）追加到历史 | src: https://platform.minimax.io/docs/guides/text-m2-function-call | quote: "Append the full response_message object (including the tool_calls field) to the message history" | type: official
- [C23] OpenAI 兼容忽略 presence_penalty/frequency_penalty/logit_bias | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "Some OpenAI parameters (such as presence_penalty, frequency_penalty, logit_bias, etc.) will be ignored" | type: official
- [C24] 已弃用 function_call 不支持，需用 tools | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "The deprecated function_call is not supported, please use the tools parameter" | type: official
- [C25] max_tokens 为 legacy 字段，新集成用 max_completion_tokens | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "Legacy generation length limit." | type: official
- [C26] OpenAI 兼容 temperature：[0,2]，默认 1 | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "Sampling temperature. Range [0, 2], default 1." | type: official

## conflicts
- MiniMax 文档内部不一致：text-anthropic-api 参数表的 thinking 块描述全文没提 "signature"；但 text-m2-function-call 指南的真实响应示例里 thinking 块明确带 signature 字段（C16 vs C17）。是否要像 Anthropic 官方那样完整回传/校验该字段，文档未说明。

## gaps
- 三个已抓页面均无 "cache_control" 字样，无法判断 Anthropic 兼容端对 prompt caching 是支持/忽略/未文档化。
- Messages 内容块表只列 text/image/video/tool_use/tool_result/thinking 六类，无 "document"(PDF)类型，但无明确"不支持"原句，故未写成 claim。
- 未发现 web_search/code_execution/computer_use/bash 等 Anthropic 服务端工具被提及（0 命中）。
- OpenAI 兼容页无完整 usage JSON 示例，未找到 cached_tokens/prompt_tokens_details 等缓存字段原句。
- 未逐一核对 tool_choice 枚举值（auto/any/tool/none）是否与 Anthropic 官方一致。

## leads
- 导航栏除 Anthropic SDK / OpenAI SDK 外还有第三个 "AI SDK" 页面（疑似 Vercel AI SDK），未展开。
- Responses 端点还配 POST /v1/responses/input_tokens（预估输入 token），与 Anthropic 侧 count_tokens 端点对应，值得单独核对。
- 已抓页面 dateModified 集中在 2026-06-08~2026-09-01。
