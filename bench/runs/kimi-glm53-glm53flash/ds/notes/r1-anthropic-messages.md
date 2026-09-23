# r1-anthropic-messages
question: Anthropic Messages API（POST /v1/messages）官方规范中，请求协议各维度的事实是什么？
checked: https://docs.claude.com/en/api/messages.md, https://docs.claude.com/en/api/versioning.md, https://docs.claude.com/en/api/beta-headers.md, https://docs.claude.com/en/docs/build-with-claude/streaming.md, https://docs.claude.com/en/docs/build-with-claude/prompt-caching.md, https://docs.claude.com/en/docs/build-with-claude/extended-thinking.md, https://docs.claude.com/en/docs/build-with-claude/vision.md, https://docs.claude.com/en/docs/about-claude/models/overview.md, https://docs.claude.com/en/docs/build-with-claude/structured-outputs.md

## claims
- [C1] 端点 POST /v1/messages；可单次或无状态多轮 | src: https://docs.claude.com/en/api/messages | quote: "The Messages API can be used for either single queries or stateless multi-turn conversations." | type: official
- [C2] messages[] 每项 {role, content}，相邻同 role 回合合并 | src: https://docs.claude.com/en/api/messages | quote: "Consecutive `user` or `assistant` turns in your request will be combined into a single turn." | type: official
- [C3] 无 "system" role，system 为顶层参数 | src: https://docs.claude.com/en/api/messages | quote: "you can use the top-level `system` parameter — there is no `\"system\"` role for input messages" | type: official
- [C4] content 为 string 或块数组 | src: https://docs.claude.com/en/api/messages | quote: "either a single `string` or an array of content blocks" | type: official
- [C5] 输入块类型：text/image/document/search_result/thinking/redacted_thinking/tool_use/tool_result | src: https://docs.claude.com/en/api/messages | quote: "`content: string or array of ContentBlockParam`" | type: official
- [C6] 顶层含 stream: optional boolean、stop_sequences: optional array of string | src: https://docs.claude.com/en/api/messages | quote: "- `stream: optional boolean`" | type: official
- [C7] max_tokens 必填且上限随模型；=0 可预热缓存不生成 | src: https://docs.claude.com/en/api/messages | quote: "Different models have different maximum values for this parameter." | type: official
- [C8] 工具定义 name/description/input_schema（JSON Schema 2020-12） | src: https://docs.claude.com/en/api/messages | quote: "`input_schema`: [JSON schema](https://json-schema.org/draft/2020-12) for the tool `input` shape" | type: official
- [C9] 带 tools 时模型返回 tool_use 块，结果经 tool_result 回传 | src: https://docs.claude.com/en/api/messages | quote: "the model may return `tool_use` content blocks" | type: official
- [C10] tool_result 字段 tool_use_id/content/is_error(optional boolean) | src: https://docs.claude.com/en/api/messages | quote: "- `tool_use_id: string` … - `is_error: optional boolean`" | type: official
- [C11] tool_choice 四型 auto/any/tool/none | src: https://docs.claude.com/en/api/messages | quote: "The model can use a specific tool, any available tool, decide by itself, or not use tools at all." | type: official
- [C12] 字段为 disable_parallel_tool_use（默认 false） | src: https://docs.claude.com/en/api/messages | quote: "If set to `true`, the model will output at most one tool use." | type: official
- [C13] 工具入参以 input_json_delta.partial_json 分片并聚合 | src: https://docs.claude.com/en/docs/build-with-claude/streaming | quote: "accumulate the string deltas and parse the JSON once you receive a `content_block_stop` event" | type: official
- [C14] cache_control={"type":"ephemeral"}，ttl "5m"/"1h" 默认 5m | src: https://docs.claude.com/en/api/messages | quote: "- `ttl: optional \"5m\" or \"1h\"` … Defaults to `5m`." | type: official
- [C15] 显式缓存断点上限 4 个槽位 | src: https://docs.claude.com/en/docs/build-with-claude/prompt-caching | quote: "the automatic cache breakpoint uses one of the 4 available breakpoint slots." | type: official
- [C16] usage 求和：input_tokens+cache_creation_input_tokens+cache_read_input_tokens | src: https://docs.claude.com/en/api/messages | quote: "the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`" | type: official
- [C17] SSE 命名事件 message_start→content_block_start/delta/stop→message_delta→message_stop，可含 ping | src: https://docs.claude.com/en/docs/build-with-claude/streaming | quote: "Each event uses an SSE event name (for example, `event: message_stop`)" | type: official
- [C18] delta 类型 text_delta/input_json_delta/thinking_delta/signature_delta | src: https://docs.claude.com/en/docs/build-with-claude/streaming | quote: "you'll receive thinking content through `thinking_delta` events." | type: official
- [C19] stop_reason：end_turn/max_tokens/stop_sequence/tool_use/pause_turn/refusal/model_context_window_exceeded；流式 message_start 中 null | src: https://docs.claude.com/en/api/messages | quote: "it is null in the `message_start` event and non-null otherwise" | type: official
- [C20] 必带 anthropic-version 头（现值 2023-06-01，版本史仅 2023-01-01/2023-06-01），SDK 自动处理 | src: https://docs.claude.com/en/api/versioning | quote: "you must send an `anthropic-version` request header" | type: official
- [C21] 认证 x-api-key；base URL api.anthropic.com | src: https://docs.claude.com/en/api/beta-headers | quote: "curl https://api.anthropic.com/v1/messages \ -H \"x-api-key: $ANTHROPIC_API_KEY\"" | type: official
- [C22] beta 机制：anthropic-beta 头，命名 feature-name-YYYY-MM-DD，可逗号合并 | src: https://docs.claude.com/en/api/beta-headers | quote: "typically follow the pattern `feature-name-YYYY-MM-DD`" | type: official
- [C23] temperature 默认 1.0 范围 0.0–1.0 | src: https://docs.claude.com/en/api/messages | quote: "Defaults to `1.0`. Ranges from `0.0` to `1.0`." | type: official
- [C24] temperature/top_p/top_k 已弃用：Opus 4.6 后模型不接受，越界值 400 | src: https://docs.claude.com/en/api/messages | quote: "Models released after Claude Opus 4.6 do not support setting temperature." | type: official
- [C25] 结构化输出 output_config.format+type:"json_schema"；无 response_format；工具 strict:true；原 output_format 免 beta 头 | src: https://docs.claude.com/en/docs/build-with-claude/structured-outputs | quote: "Include the `output_config.format` parameter in your API request with `type: \"json_schema\"`" | type: official
- [C26] thinking:{"type":"enabled","budget_tokens":N}；min 1024 且 <max_tokens（interleaved 例外可超） | src: https://docs.claude.com/en/docs/build-with-claude/extended-thinking | quote: "**Minimum of 1,024 tokens.** The API rejects smaller values." | type: official
- [C27] ≤4.5 模型 interleaved thinking 需 beta 头 interleaved-thinking-2025-05-14 | src: https://docs.claude.com/en/docs/build-with-claude/extended-thinking | quote: "add the `interleaved-thinking-2025-05-14` beta header to your API request." | type: official
- [C28] 手动扩展思考 4.6 弃用、4.7+ 拒绝 400；新推 thinking:{type:"adaptive"} | src: https://docs.claude.com/en/docs/build-with-claude/extended-thinking | quote: "reject requests that use it, returning a 400 error." | type: official
- [C29] thinking 块须原样按序回传（signature），改动 400 | src: https://docs.claude.com/en/api/messages | quote: "Thinking blocks must be passed back unmodified and in their original order" | type: official
- [C30] image source 三型 base64/url/file(file_id)；JPEG/PNG/GIF/WebP | src: https://docs.claude.com/en/api/messages | quote: "source: Base64ImageSource or URLImageSource or FileImageSource" | type: official
- [C31] document 块 PDF media_type application/pdf | src: https://docs.claude.com/en/api/messages | quote: "- `media_type: \"application/pdf\"`" | type: official
- [C32] 当前模型仅文本+图片输入、文本输出（audio 无官方支持记载） | src: https://docs.claude.com/en/docs/about-claude/models/overview | quote: "text and image input, text output" | type: official

## conflicts
- 简报预期"5 个断点"；官方现写 4 个 slots（prompt-caching 页），D4 以官方 4 为准。
- 简报视 temperature/top_p/top_k、thinking{enabled} 为现行参数；官方已标弃用/按模型拒绝（C24/C28）。
- 简报字段名 disable_parallel_tools，实际为 tool_choice 内 disable_parallel_tool_use（C12）。

## gaps
- logprobs/n：参数全集导出中无此二参数；无 absence 原句，仅 C6 间接支撑。
- audio 不支持无明示原句，仅 C32 间接；usage 累计、20 图上限未摘录。

## leads
- docs 域名已迁 platform.claude.com（docs.claude.com 跳转），对比智谱兼容层以此为准。
- 新协议面：tool_choice type:"none"、thinking adaptive、automatic caching、file_id source、service_tier、pause_turn、output-300k beta。
