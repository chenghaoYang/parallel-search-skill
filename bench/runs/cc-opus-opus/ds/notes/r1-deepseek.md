# r1-deepseek
question: DeepSeek 官方 API（api-docs.deepseek.com）实现了哪些协议（OpenAI Chat Completions 兼容？Anthropic Messages 兼容？有没有 OpenAI Responses API /v1/responses？），各自与参考协议（OpenAI 官方 / Anthropic 官方）相比，哪些字段支持/忽略/报错，推理内容怎么返回与回传？
checked: https://api-docs.deepseek.com/, https://api-docs.deepseek.com/quick_start/pricing, https://api-docs.deepseek.com/updates, https://api-docs.deepseek.com/guides/responses_api, https://api-docs.deepseek.com/api/create-response, https://api-docs.deepseek.com/guides/thinking_mode, https://api-docs.deepseek.com/api/create-chat-completion, https://api-docs.deepseek.com/guides/tool_calls, https://api-docs.deepseek.com/guides/chat_prefix_completion, https://api-docs.deepseek.com/guides/fim_completion, https://api-docs.deepseek.com/guides/kv_cache, https://api-docs.deepseek.com/quick_start/rate_limit, https://api-docs.deepseek.com/quick_start/error_codes, https://api-docs.deepseek.com/guides/anthropic_api, zh-cn 同名页, /guides/reasoning_model（已下线）, 3 个存档页

## claims
- [C1] 两个 base_url；示例用 Bearer | src: https://api-docs.deepseek.com/ | quote: "base_url (OpenAI) | https://api.deepseek.com | base_url (Anthropic) | https://api.deepseek.com/anthropic" | type: official
- [C2] 2026-09 模型版本 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "MODEL VERSION | DeepSeek-V4.1-Flash | DeepSeek-V4-Pro-0813" | type: official
- [C3] 2026-04-24 公告，过渡期指向 V4-Flash 非思考/思考 | src: https://api-docs.deepseek.com/updates | quote: "deepseek-chat and deepseek-reasoner, will be discontinued in three months (2026-07-24)" | type: official
- [C4] 有 Responses API（2026-07-31 起） | src: https://api-docs.deepseek.com/guides/responses_api | quote: "our API now supports the Responses API format, with the base_url being https://api.deepseek.com" | type: official
- [C5] 端点无 /v1 | src: https://api-docs.deepseek.com/api/create-response | quote: "POST /responses" | type: official
- [C6] previous_response_id/conversation/store 等十余项不支持 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Unsupported parameters are silently ignored and do not cause errors" | type: official
- [C7] Responses reasoning 参数 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "effort supported; summary accepted but no summary is generated" | type: official
- [C8] 回传 reasoning item 仅明文 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "summary and encrypted_content are not supported" | type: official
- [C9] 输出 reasoning_text 明文 | src: https://api-docs.deepseek.com/api/create-response | quote: "the chain-of-thought is returned as a reasoning item before the message item" | type: official
- [C10] 思考默认开（thinking.type / reasoning_effort=none 关） | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "Thinking mode is enabled by default, with the default effort being high" | type: official
- [C11] message 与 delta 均有 reasoning_content | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "returned via the reasoning_content parameter, at the same level as content" | type: official
- [C12] 无 tools | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "reasoning_content does not need to be passed back; even if passed to the API, it will be ignored" | type: official
- [C13] 有 tools | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "If your code does not correctly pass back reasoning_content, the API will return a 400 error." | type: official
- [C14] 思考模式 temperature/penalty | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "setting these parameters will not trigger an error but will also have no effect" | type: official
- [C15] top_p 仅思考生效（0.95–1.0） | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "In non-thinking mode it is fixed at 1.0 and your value is ignored." | type: official
- [C16] Chat 全模式 penalty 已 deprecated | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "This parameter is no longer supported." | type: official
- [C17] max_tokens | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "between 1 and 384K (393216). When not set, the default is 8K in non-thinking mode, 64K in thinking mode (128K with reasoning_effort set to max)" | type: official
- [C18] response_format 无 json_schema | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Must be one of text or json_object." | type: official
- [C19] 思考模式 tool_choice | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "required and named tool choices are not supported in thinking mode; the API returns a 400 error" | type: official
- [C20] usage 私有字段 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "It equals prompt_cache_hit_tokens + prompt_cache_miss_tokens." | type: official
- [C21] finish_reason 私有值 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "[stop, length, content_filter, tool_calls, insufficient_system_resource, aborted]" | type: official
- [C22] include_usage（stream_options 无 stream:true 则 400） | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "no separate usage-only chunk is emitted" | type: official
- [C23] 硬盘缓存 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Context Caching on Disk Technology is enabled by default for all users" | type: official
- [C24] keep-alive（非流式为空行） | src: https://api-docs.deepseek.com/quick_start/rate_limit | quote: "Continuously return SSE keep-alive comments (: keep-alive)" | type: official
- [C25] 错误码（另有 400/401/429/500/503） | src: https://api-docs.deepseek.com/quick_start/error_codes | quote: "402 - Insufficient Balance | Cause: You have run out of balance." | type: official
- [C26] Anthropic 映射（haiku/sonnet/未知名→flash） | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "Models starting with claude-opus are mapped to deepseek-v4-pro" | type: official
- [C27] anthropic-beta（anthropic-version 亦 Ignored） | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "Ignored for /messages; required (files-api-2025-04-14) for Files API endpoints" | type: official
- [C28] thinking（top_k/container/mcp_servers/service_tier Ignored） | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "Supported (budget_tokens is ignored)" | type: official
- [C29] tool_choice auto/any/tool | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "Supported (disable_parallel_tool_use is ignored)" | type: official
- [C30] cache_control（citations、is_error 同） | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "cache_control | Ignored" | type: official
- [C31] document/search_result/redacted_thinking/mcp_*/container_upload 均 Not Supported | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "array, type = "document" |  | Not Supported" | type: official

## conflicts
- 回传（版本）：旧 https://web.archive.org/web/20250728201007/https://api-docs.deepseek.com/guides/reasoning_model "if the reasoning_content field is included in the sequence of input messages, the API will return a 400 error" vs 现行 C12/C13。
- logprobs（版本）：同旧页 "Setting logprobs、top_logprobs will trigger an error." vs 现行 reference 无此限制。
- 限流（版本）：旧 https://web.archive.org/web/20251215152232/https://api-docs.deepseek.com/quick_start/rate_limit "DeepSeek API does NOT constrain user's rate limit." vs 现行 https://api-docs.deepseek.com/quick_start/rate_limit "when the concurrency limit is exceeded, you will receive an HTTP 429 error code"（flash 2500/v4-pro 500）。

## gaps
- Chat 未列 n、seed、logit_bias、parallel_tool_calls、max_completion_tokens。
- Responses/Anthropic 下思考+强制 tool_choice、reasoning/thinking 回传规则、signature 未说明。
- /v1 现行不提；2025-12-01 存档首页称 "you can also use https://api.deepseek.com/v1"。

## leads
- Responses：custom 仅 apply_patch；内置工具忽略；流式无 [DONE]。
- strict/Prefix Completion/FIM 需 base_url https://api.deepseek.com/beta；FIM 4K、仅非思考。
- Responses text.format 支持 json_schema（Chat 不支持）。
