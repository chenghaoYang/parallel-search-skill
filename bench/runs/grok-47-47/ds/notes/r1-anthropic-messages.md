# r1-anthropic-messages
question: Anthropic 官方 Messages API 的请求与响应协议长什么样？
checked: https://docs.anthropic.com/en/api/messages, https://platform.claude.com/docs/en/api/messages, https://platform.claude.com/docs/en/api/overview, https://platform.claude.com/docs/en/api/versioning, https://platform.claude.com/docs/en/api/beta-headers, https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk, https://platform.claude.com/docs/en/build-with-claude/working-with-messages, https://platform.claude.com/docs/en/build-with-claude/streaming, https://platform.claude.com/docs/en/build-with-claude/structured-outputs

## claims
- [C1] D1 POST `/v1/messages`。 | src: https://platform.claude.com/docs/en/api/messages | quote: "POST `/v1/messages`" | type: official
- [C2] D1 base `https://api.anthropic.com`。 | src: https://platform.claude.com/docs/en/api/overview | quote: "The Claude API is a RESTful API at `https://api.anthropic.com`" | type: official
- [C3] D1 `anthropic-version` 必填，示例 `2023-06-01`。 | src: https://platform.claude.com/docs/en/api/versioning | quote: "you must send an `anthropic-version` request header. For example, `anthropic-version: 2023-06-01`." | type: official
- [C4] D1 `Authorization` 必需，除非设置 `x-api-key`。`x-api-key` 为仍支持的 legacy fallback，表 Required=No。 | src: https://platform.claude.com/docs/en/api/overview | quote: "Yes, unless `x-api-key` is set" | type: official
- [C5] D1 示例头 Content-Type application/json。 | src: https://platform.claude.com/docs/en/api/messages | quote: "-H 'Content-Type: application/json'" | type: official
- [C6] D1 `anthropic-beta` 不是标准必填头。 | src: https://platform.claude.com/docs/en/api/beta-headers | quote: "To access beta features, include the `anthropic-beta` header in your API requests" | type: official
- [C7] D2 无服务端历史，每轮重放完整 messages。 | src: https://platform.claude.com/docs/en/build-with-claude/working-with-messages | quote: "you always send the full conversational history to the API." | type: official
- [C8] D2 reference 称 stateless multi-turn。连续同类 user/assistant turn 会合并。 | src: https://platform.claude.com/docs/en/api/messages | quote: "stateless multi-turn conversations" | type: official
- [C9] D3 schema role：`user`、`assistant`、`system`。每条须有 role 与 content。 | src: https://platform.claude.com/docs/en/api/messages | quote: "role: \"user\" or \"assistant\" or \"system\"" | type: official
- [C10] D3 content 为 string 或 block 数组；string 即单个 text block。 | src: https://platform.claude.com/docs/en/api/messages | quote: "a single `string` or an array of content blocks" | type: official
- [C11] D3 输入 block type 含 text、image、tool_use、tool_result、thinking（另有 document 等）。 | src: https://platform.claude.com/docs/en/api/messages | quote: "type: \"tool_result\"" | type: official
- [C12] D4 顶层 system 可选：string 或 TextBlockParam 数组。 | src: https://platform.claude.com/docs/en/api/messages | quote: "system: optional string or array of TextBlockParam" | type: official
- [C13] D4 同页散文：输入没有 system role。 | src: https://platform.claude.com/docs/en/api/messages | quote: "there is no `\"system\"` role for input messages in the Messages API." | type: official
- [C14] D4 system 消息不能是 messages 第一条。 | src: https://platform.claude.com/docs/en/build-with-claude/working-with-messages | quote: "A `system` message cannot be the first entry in `messages`." | type: official
- [C15] D5 tools[].name 与 input_schema（JSON Schema）。 | src: https://platform.claude.com/docs/en/api/messages | quote: "`input_schema`: [JSON schema](https://json-schema.org/draft/2020-12) for the tool `input` shape" | type: official
- [C16] D5 tool_choice.type：auto、any、tool（name）、none。 | src: https://platform.claude.com/docs/en/api/messages | quote: "decide by itself, or not use tools at all." | type: official
- [C17] D5 tool_result 放在后续 user 消息 content，不是独立 role。 | src: https://platform.claude.com/docs/en/api/messages | quote: "in a subsequent `user` message" | type: official
- [C18] D6 max_tokens 类型为 number，未标 optional。 | src: https://platform.claude.com/docs/en/api/messages | quote: "max_tokens: number" | type: official
- [C19] D6 temperature 可选；Opus 4.6 之后的模型不支持设置 temperature。 | src: https://platform.claude.com/docs/en/api/messages | quote: "Models released after Claude Opus 4.6 do not support setting temperature." | type: official
- [C20] D6 thinking.type=enabled 时 budget_tokens 须 ≥1024 且小于 max_tokens。另有 disabled、adaptive。 | src: https://platform.claude.com/docs/en/api/messages | quote: "Must be ≥1024 and less than `max_tokens`." | type: official
- [C21] D7 stream 可选，走 SSE。事件名 message_start、content_block_delta、message_delta、message_stop，另有 content_block_start、content_block_stop、ping、error。 | src: https://platform.claude.com/docs/en/build-with-claude/streaming | quote: "event: message_stop" | type: official
- [C22] D7 data.type 与 SSE 事件名一致。delta 含 text_delta、input_json_delta、thinking_delta、signature_delta。 | src: https://platform.claude.com/docs/en/build-with-claude/streaming | quote: "includes the matching event `type` in its data." | type: official
- [C23] D8 content 为 block 数组。type 恒 message，role 恒 assistant。 | src: https://platform.claude.com/docs/en/api/messages | quote: "an array of content blocks, each of which has a `type`" | type: official
- [C24] D8 stop_reason：end_turn、max_tokens、stop_sequence、tool_use、pause_turn、refusal、model_context_window_exceeded。 | src: https://platform.claude.com/docs/en/api/messages | quote: "`\"tool_use\"`: the model invoked one or more tools" | type: official
- [C25] D8 usage.input_tokens 与 usage.output_tokens。 | src: https://platform.claude.com/docs/en/api/messages | quote: "summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`." | type: official
- [C26] D9 字段是 output_config.format，type json_schema，加 schema。不是现行顶层 output_format。 | src: https://platform.claude.com/docs/en/api/messages | quote: "type: \"json_schema\"" | type: official
- [C27] D9 output_format 已迁到 output_config.format；旧字段与 beta structured-outputs-2025-11-13 过渡期仍接受。 | src: https://platform.claude.com/docs/en/build-with-claude/structured-outputs | quote: "The `output_format` parameter has moved to `output_config.format`" | type: official
- [C28] D10 无禁令句。兼容层非长期生产方案；OpenAI SDK base_url `https://api.anthropic.com/v1/`。未印兼容层 path。 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "not considered a long-term or production-ready solution for most use cases." | type: official
- [C29] D10 差异：不支持字段多半静默忽略；strict 与 response_format 忽略；有 OpenAI role tool；system 消息被抬到开头。限流按 /v1/messages。 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "Most unsupported fields are silently ignored rather than producing errors." | type: official
- [C30] D10 beta 是实验特性，可能 breaking change，从而改协议细节；标准请求可不送。 | src: https://platform.claude.com/docs/en/api/beta-headers | quote: "Have breaking changes with notice" | type: official

## conflicts
- system role：https://platform.claude.com/docs/en/api/messages 散文「there is no `"system"` role for input messages in the Messages API.」vs 同页「role: "user" or "assistant" or "system"」vs https://platform.claude.com/docs/en/build-with-claude/working-with-messages 允许中途 system vs https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk「Anthropic only supports an initial system message」。
- temperature：reference「Models released after Claude Opus 4.6 do not support setting temperature.」vs 指南「not supported on Claude 4.7 and later models and Claude Mythos Preview.」vs 兼容层「Values greater than 1 are capped at 1.」Fully supported。

## gaps
- 无 Last updated。2023-06-01 是 API version。
- 未印 required 数组；max_tokens/messages/model 只因类型行不写 optional。
- 无「禁止把 Messages 当 OpenAI」句，D10 不是 ∅。兼容层未写 POST path。
- content-type Required=Yes 只在 overview 表。stop_reason 与 image/thinking/tool_use 的 type 是分列 schema，C11/C24 的 quote 只盖住一项。

## leads
- https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages
- 同参考还有 count_tokens 与 batches。
