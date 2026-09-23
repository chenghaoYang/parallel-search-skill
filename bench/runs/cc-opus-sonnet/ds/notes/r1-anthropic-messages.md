# r1-anthropic-messages
question: Anthropic Messages API（POST /v1/messages）的官方规格在 D1–D10 上各是什么？
checked: base=https://platform.claude.com/docs/en/ + {api/messages, api/versioning, api/overview, api/beta-headers, api/errors, build-with-claude/streaming, agents-and-tools/tool-use/{overview,handle-tool-calls}, build-with-claude/{extended-thinking,prompt-caching,structured-outputs,files,token-counting,handling-stop-reasons,refusals-and-fallback}}（docs.claude.com 301→同路径）

## claims

D1
- [C1] Base URL：RESTful API at https://api.anthropic.com | src: https://platform.claude.com/docs/en/api/overview | quote: "The Claude API is a RESTful API at `https://api.anthropic.com`" | type: official
- [C2] anthropic-version必填,值2023-06-01(历史仅两版:2023-01-01、2023-06-01) | src: https://platform.claude.com/docs/en/api/versioning | quote: "you must send an `anthropic-version` request header" | type: official
- [C3] Authorization:Bearer 为主鉴权(除非设x-api-key);x-api-key是旧版回退,非必填 | src: https://platform.claude.com/docs/en/api/overview | quote: "Legacy fallback for `Authorization`, still supported" | type: official
- [C4] anthropic-beta 可逗号分隔多值或重复该头;命名惯例 feature-name-YYYY-MM-DD | src: https://platform.claude.com/docs/en/api/beta-headers | quote: "feature names in the header separated by commas" | type: official
- [C5] 配套端点均GA:POST /v1/messages/count_tokens、POST /v1/messages/batches、GET /v1/models | src: https://platform.claude.com/docs/en/api/overview | quote: "(`POST /v1/messages/count_tokens`)" | type: official

D2
- [C6] messages 仅 user/assistant 交替；连续同角色合并为一轮 | src: https://platform.claude.com/docs/en/api/messages | quote: "Consecutive `user` or `assistant` turns in your request will be combined into a single turn." | type: official
- [C7] 末条为 assistant 即预填，响应从该内容续写以约束输出 | src: https://platform.claude.com/docs/en/api/messages | quote: "the response content will continue immediately from the content in that message." | type: official
- [C8] Claude 4.6+ 与 Mythos Preview 不支持预填，返回 400 | src: https://platform.claude.com/docs/en/api/errors | quote: "do not support prefilling assistant messages...returns a 400 `invalid_request_error`" | type: official
- [C9] 无 system role；system 顶层参数，string 或 TextBlockParam[] | src: https://platform.claude.com/docs/en/api/messages | quote: "there is no `\"system\"` role for input messages in the Messages API" | type: official

D3
- [C10] 官方原文称 Messages API 为"无状态"多轮对话（∅ 服务端会话） | src: https://platform.claude.com/docs/en/api/messages | quote: "single queries or stateless multi-turn conversations" | type: official
- [C11] Files API 已 GA 无需 beta 头；file_id 经 document/image block 的 source 字段引用 | src: https://platform.claude.com/docs/en/build-with-claude/files | quote: "The Files API is out of beta and needs no beta header." | type: official

D4
- [C12] id 为字符串,官方声明格式/长度可能变化;type恒"message";示例"msg_013Zva2..." | src: https://platform.claude.com/docs/en/api/messages | quote: "format and length of IDs may change over time" | type: official
- [C13] stop_reason 共7值:end_turn/max_tokens/stop_sequence/tool_use/pause_turn/refusal/model_context_window_exceeded | src: https://platform.claude.com/docs/en/api/messages | quote: "we exceeded the model's context window" | type: official
- [C14] 拒答=stop_reason:"refusal"+stop_details{category,explanation}，属正常 200 | src: https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback | quote: "a normal response, not an error, with `stop_reason: \"refusal\"`" | type: official
- [C15] 顶层请求体无 n/seed 字段（∅ 多候选、∅ seed） | src: https://platform.claude.com/docs/en/api/messages | quote: "stop_sequences, stream, system, temperature, thinking, tool_choice, tools, top_k, top_p" | type: official

D5
- [C16] tools[]={name,description,input_schema}；strict:boolean 保证 schema 校验 | src: https://platform.claude.com/docs/en/api/messages | quote: "guarantees schema validation on tool names and inputs" | type: official
- [C17] tool_choice 四型 auto/any/tool/none；disable_parallel_tool_use=true 时限恰好一次调用 | src: https://platform.claude.com/docs/en/api/messages | quote: "If set to `true`, the model will output exactly one tool use." | type: official
- [C18] tool_result 须紧跟 tool_use；同一 user 消息内须排最前，文本只能在其后 | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls | quote: "tool_result blocks must come FIRST in the content array. Any text must come AFTER" | type: official
- [C19] tool_use 含 id/name/input；tool_result 含 tool_use_id(正则)、content、is_error | src: https://platform.claude.com/docs/en/api/messages | quote: "`tool_use_id: string` pattern: ^[a-zA-Z0-9_-]+$" | type: official
- [C20] 版本化工具类型名示例：bash_20250124、computer_toolset_20260801、web_search_20260209、code_execution_20260521 | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | quote: "\"type\": \"web_search_20260209\"" | type: official

D6
- [C21] thinking.budget_tokens 下限 1024 且须 < max_tokens（交错思考例外） | src: https://platform.claude.com/docs/en/api/messages | quote: "Must be ≥1024 and less than `max_tokens`." | type: official
- [C22] 存在 type:"adaptive"；深度改由 output_config.effort 控制，值 low/medium/high/xhigh/max | src: https://platform.claude.com/docs/en/api/messages | quote: "effort: optional \"low\" or \"medium\" or \"high\" or 2 more" | type: official
- [C23] thinking.signature 须原样、原序回传，否则 400；用于验证该块确由 Claude 生成 | src: https://platform.claude.com/docs/en/api/messages | quote: "must be passed back unmodified and in their original order; a modified block results in a 400" | type: official
- [C24] redacted_thinking.data 不透明加密，多轮须原样传回 | src: https://platform.claude.com/docs/en/api/messages | quote: "Pass `redacted_thinking` blocks back to the API unchanged" | type: official
- [C25] thinking.display 默认 "summarized"，可设 "omitted"；交错思考需 interleaved-thinking-2025-05-14 beta 头 | src: https://platform.claude.com/docs/en/build-with-claude/extended-thinking | quote: "interleaved-thinking-2025-05-14` beta header to your API request" | type: official

D7
- [C26] 参数名 output_config.format（非 output_format），已 GA 无需 beta 头 | src: https://platform.claude.com/docs/en/build-with-claude/structured-outputs | quote: "has moved to `output_config.format`, and beta headers are no longer required" | type: official
- [C27] 旧头 structured-outputs-2025-11-13+output_format 过渡期仍可用，Python SDK v1.0+ 用 output_format 报 TypeError | src: https://platform.claude.com/docs/en/build-with-claude/structured-outputs | quote: "accept the old beta header...and the `output_format` request field for a transition period" | type: secondary
- [C28] 工具 strict:true 保证调用严格匹配 schema | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | quote: "ensure Claude's tool calls always match your schema exactly" | type: official

D8
- [C29] 事件序：message_start→每块 content_block_start/delta(≥1)/stop→message_delta(≥1)→message_stop，ping 穿插 | src: https://platform.claude.com/docs/en/build-with-claude/streaming | quote: "A final `message_stop` event." | type: official
- [C30] delta.type 含 text_delta/input_json_delta/thinking_delta/signature_delta；后者在 content_block_stop 前发出 | src: https://platform.claude.com/docs/en/build-with-claude/streaming | quote: "signature_delta event is sent just before the `content_block_stop` event" | type: official
- [C31] message_delta 中 usage 的 token 计数是累计值 | src: https://platform.claude.com/docs/en/build-with-claude/streaming | quote: "usage` field of the `message_delta` event are *cumulative*" | type: official
- [C32] 2023-06-01 版起移除 data: [DONE] 事件，当前格式无 [DONE] | src: https://platform.claude.com/docs/en/api/versioning | quote: "Removed unnecessary `data: [DONE]` event." | type: official

D9
- [C33] max_tokens 必填(min0)；temperature 默认1.0范围0–1、top_p(0–1)、top_k(min0) 均在 Opus4.6 后发布模型弃用 | src: https://platform.claude.com/docs/en/api/messages | quote: "Defaults to `1.0`. Ranges from `0.0` to `1.0`." | type: official

D10
- [C35] usage 含 input/output_tokens、cache_creation_input_tokens、cache_read_input_tokens、cache_creation{1h/5m}、server_tool_use | src: https://platform.claude.com/docs/en/api/messages | quote: "summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`" | type: official
- [C36] input_tokens 不含缓存读/写部分，三者相加才是总输入 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "not read from or used to create a cache" | type: official
- [C37] cache_control:{type:"ephemeral",ttl}；默认5分钟，"1h"需2倍价；最多4显式断点；最小可缓存长度按模型512–4096token | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "5-minute lifetime...define up to 4 cache breakpoints" | type: official
- [C38] 无隐式自动缓存：automatic caching 仍须顶层显式加一个 cache_control | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "add a single `cache_control` field at the top level of your request body" | type: official
- [C39] 错误体{"type":"error","error":{type,message},"request_id"}；529=overloaded_error | src: https://platform.claude.com/docs/en/api/errors | quote: "The API is temporarily overloaded." | type: official

## conflicts
- 未见跨页冲突；仅 api/messages 内一处示例 JSON 同时出现 stop_reason:"end_turn" 与非空 stop_details.category:"cyber"，疑似文档拼装疏漏。src: api/messages

## gaps
- content block 未逐类取得原句（如 search_result、mcp_tool_use/result），仅确认类型名存在。
- adaptive 思考默认深度、Claude5系列是否强制 adaptive 未核实。
- anthropic-beta 完整功能清单未取得，仅零散确认几个 beta 名。

## leads
- 模型列表已是 claude-opus-5-5/sonnet-5/fable-5-1 命名，与"今天2026-09-23"一致，引用需注意时效。
- Managed Agents 另有有状态 Sessions API（beta），与 Messages API 分属两套端点，不应混入 D3。
- Bedrock/Vertex/Foundry 在温度、prefill、thinking 支持上与直连 API 有平台差异（未深查）。
