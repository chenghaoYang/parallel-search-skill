# r1-anthropic-messages
question: Anthropic 官方 Messages API（POST /v1/messages）当前（2026）文档里各维度的具体字段名、枚举值、规则是什么？
checked: 下列各 claim 的 src（.md 版，2026-09-23）及 https://platform.claude.com/docs/en/ 下 compaction、citations、vision、files、pdf-support、mcp-connector、tool-use/server-tools 页

## claims
- [C1] D1 端点；beta 用 anthropic-beta 头（逗号分隔） | src: https://platform.claude.com/docs/en/api/beta-headers | quote: "curl https://api.anthropic.com/v1/messages" | type: official
- [C2] D1 认证 Authorization: Bearer，x-api-key 为旧式回退 | src: https://platform.claude.com/docs/en/api/overview | quote: "Legacy fallback for `Authorization`, still supported" | type: official
- [C3] D1 anthropic-version 必填 | src: https://platform.claude.com/docs/en/api/versioning | quote: "you must send an `anthropic-version` request header. For example, `anthropic-version: 2023-06-01`." | type: official
- [C4] D1/D7 max_tokens 必填（model、messages 同；v1.8.0） | src: https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/main/src/anthropic/types/message_create_params.py | quote: "max_tokens: Required[int]" | type: official
- [C5] D2 system 顶层（string 或 TextBlockParam 数组）；无 system 角色 | src: https://platform.claude.com/docs/en/api/messages | quote: "you can use the top-level `system` parameter — there is no `"system"` role for input messages" | type: official
- [C6] D2 连续同角色合并；content=string 或块数组 | src: https://platform.claude.com/docs/en/api/messages | quote: "Consecutive `user` or `assistant` turns in your request will be combined into a single turn." | type: official
- [C7] D2 末条 assistant 预填 | src: https://platform.claude.com/docs/en/build-with-claude/working-with-messages | quote: "Prefilling is not supported on Claude 4.6 and later models and Claude Mythos Preview. Requests using prefill with these models return a 400 error." | type: official
- [C8] D3 image.source=base64{media_type:image/jpeg|png|gif|webp,data}|url{url}|file{file_id} | src: https://platform.claude.com/docs/en/api/messages | quote: "`source: Base64ImageSource or URLImageSource or FileImageSource`" | type: official
- [C9] D3 document.source=base64 PDF|text|content|url|file，可带 citations | src: https://platform.claude.com/docs/en/api/messages | quote: "`source: Base64PDFSource or PlainTextSource or ContentBlockSource or 2 more`" | type: official
- [C10] D4 tool_use{id,name,input}，input 为对象；tool_result{tool_use_id,content?,is_error?} | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls | quote: "`input`: An object containing the input being passed to the tool" | type: official
- [C11] D4 紧跟规则 | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls | quote: "Tool result blocks must immediately follow their corresponding tool use blocks in the message history." | type: official
- [C12] D4 最前规则 | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls | quote: "the tool_result blocks must come FIRST in the content array." | type: official
- [C13] D4 tools[]={name,description?,input_schema,strict?}；tool_choice.type=auto|any|tool|none，可加 disable_parallel_tool_use | src: https://platform.claude.com/docs/en/api/messages | quote: "The model can use a specific tool, any available tool, decide by itself, or not use tools at all." | type: official
- [C14] D4 服务端工具版本（同表 web_fetch_20250910–20260318、code_execution_20250825–20260521、mcp_toolset[mcp-client-2025-11-20]） | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference | quote: "`web_search_20260318` `web_search_20260209` `web_search_20250305` | Server" | type: official
- [C15] D5 无状态 | src: https://platform.claude.com/docs/en/build-with-claude/working-with-messages | quote: "The Messages API is stateless, which means that you always send the full conversational history" | type: official
- [C16] D5 context editing（clear_tool_uses_20250919/clear_thinking_20251015） | src: https://platform.claude.com/docs/en/build-with-claude/context-editing | quote: "use the beta header `context-management-2025-06-27`" | type: official
- [C17] D5 服务端压缩，beta compact-2026-01-12 | src: https://platform.claude.com/docs/en/build-with-claude/compaction-threshold | quote: "adding the `compact_20260112` strategy to `context_management.edits`" | type: official
- [C18] D6 thinking.type=enabled|disabled|adaptive；块 thinking{thinking,signature}、redacted_thinking{data}；output_config.effort=low|medium|high|xhigh|max | src: https://platform.claude.com/docs/en/api/messages | quote: "Must be ≥1024 and less than `max_tokens`." | type: official
- [C19] D6 enabled+budget_tokens：4.6 弃用，4.7+ 报 400 | src: https://platform.claude.com/docs/en/build-with-claude/extended-thinking | quote: "Claude 4.7 and later models do not support it and reject requests that use it, returning a 400 error." | type: official
- [C20] D6 原样回传 thinking；文本为摘要；adaptive 下 interleaved 自动；thinking 时不可预填 | src: https://platform.claude.com/docs/en/build-with-claude/thinking | quote: "you must pass the thinking blocks from the assistant message back to the API, complete and unmodified." | type: official
- [C21] D7 Opus 4.7+、Sonnet 5 等采样限制 | src: https://platform.claude.com/docs/en/build-with-claude/thinking | quote: "non-default `temperature`, `top_p`, or `top_k` values return a 400 error on every request" | type: official
- [C22] D7 结构化输出 GA：format{type:"json_schema",schema} | src: https://platform.claude.com/docs/en/build-with-claude/structured-outputs | quote: "The `output_format` parameter has moved to `output_config.format`, and beta headers are no longer required." | type: official
- [C23] D8 message_start→块→message_delta(stop_reason,累计usage)→message_stop，另 ping/error；delta: text/input_json/thinking/signature | src: https://platform.claude.com/docs/en/build-with-claude/streaming | quote: "a `content_block_start`, one or more `content_block_delta` events, and a `content_block_stop` event" | type: official
- [C24] D8 无 [DONE] | src: https://platform.claude.com/docs/en/api/versioning | quote: "Removed unnecessary `data: [DONE]` event." | type: official
- [C25] D9 stop_reason 枚举 | src: https://platform.claude.com/docs/en/api/messages | quote: "`"end_turn"` `"max_tokens"` `"stop_sequence"` `"tool_use"` `"pause_turn"` `"refusal"` `"model_context_window_exceeded"`" | type: official
- [C26] D9 input_tokens 不含缓存读写 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Number of input tokens which were not read from or used to create a cache" | type: official
- [C27] D10 cache_control{type:"ephemeral",ttl:"5m"|"1h"}；顶层 cache_control=自动缓存；最小 512–4096 tokens | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "the automatic cache breakpoint uses one of the 4 available breakpoint slots" | type: official
- [C28] D12 {type:"error",error:{type,message},request_id}；529 overloaded_error；头 request-id | src: https://platform.claude.com/docs/en/api/errors | quote: "a top-level `error` object that always includes a `type` and `message` value" | type: official

## conflicts
（路径前缀 https://platform.claude.com/docs/en/）
- display 默认：api/messages "Defaults to `summarized`." vs build-with-claude/thinking（Opus 5.5 等）"`display` defaults to `"omitted"` on these models"
- 预填：api/messages 未限定模型 "If the final message uses the `assistant` role, the response content will continue immediately from the content in that message." vs C7
- api/errors 列 "409 - `conflict_error`"、"413 - `request_too_large`"；SDK shared/error_type.py 无此二值
- model_context_window_exceeded：build-with-claude/handling-stop-reasons "currently typed only in the SDKs' `beta` namespace" vs C25

## gaps
- 未见 "temperature 与 top_p 不可同时设" 原句（现行规则 C21）
- 篇幅所限未单列：effort 默认（Opus 5.5=medium）、citations_delta、mcp_servers、compact-2026-09-04。

## leads
- OpenAI SDK 兼容页：https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk
- tool_choice any/tool 在 Opus 5.5、Fable/Mythos 5.1 一律 400（thinking 页）
