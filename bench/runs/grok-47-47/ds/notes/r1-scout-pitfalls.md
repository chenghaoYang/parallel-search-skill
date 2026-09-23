# r1-scout-pitfalls
question: 在 Chat Completions、Responses、Messages、generateContent 之间迁移客户端时，官方文档写明的、最容易把请求打坏的协议差异有哪些？
checked: https://platform.claude.com/docs/en/build-with-claude/thinking, https://platform.claude.com/docs/en/build-with-claude/extended-thinking, https://platform.claude.com/docs/en/build-with-claude/streaming, https://platform.claude.com/docs/en/api/messages, https://developers.openai.com/api/docs/guides/reasoning, https://developers.openai.com/api/docs/guides/streaming-responses, https://developers.openai.com/api/docs/guides/migrate-to-responses, https://developers.openai.com/api/docs/guides/function-calling, https://developers.openai.com/api/reference/resources/responses/methods/create, https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures, https://ai.google.dev/gemini-api/docs/function-calling, https://ai.google.dev/gemini-api/docs/openai, https://ai.google.dev/gemini-api/docs/text-generation, https://ai.google.dev/api/generate-content

## claims
- [C1] thinking 块改序/改文 → 400 | src: https://platform.claude.com/docs/en/api/messages | quote: "a modified block results in a 400 invalid_request_error." | type: official
- [C2] 工具回合必须回传 thinking；普通跨回合可省 | src: https://platform.claude.com/docs/en/build-with-claude/thinking | quote: "Required: within a tool-use turn, pass thinking blocks back." | type: official
- [C3] 流式签名在 signature_delta，早于 content_block_stop | src: https://platform.claude.com/docs/en/build-with-claude/streaming | quote: "a special signature_delta event is sent just before the content_block_stop event." | type: official
- [C4] thinking.type=enabled 在 Claude 4.7+ → 400 | src: https://platform.claude.com/docs/en/build-with-claude/extended-thinking | quote: "reject requests that use it, returning a 400 error." | type: official
- [C5] 手动交错思考要 header interleaved-thinking-2025-05-14 | src: https://platform.claude.com/docs/en/build-with-claude/extended-thinking | quote: "add the interleaved-thinking-2025-05-14 beta header to your API request." | type: official
- [C6] display=updates 缺 thinking-display-updates-2026-08-18 → 400 | src: https://platform.claude.com/docs/en/build-with-claude/thinking | quote: "requires the beta header thinking-display-updates-2026-08-18." | type: official
- [C7] 手动思考不能 tool_choice any/tool | src: https://platform.claude.com/docs/en/build-with-claude/thinking | quote: "tool_choice: {\"type\": \"any\"} or tool_choice: {\"type\": \"tool\", \"name\": \"...\"} results in an error" | type: official
- [C8] messages 无 system 角色，用顶层 system | src: https://platform.claude.com/docs/en/api/messages | quote: "there is no \"system\" role for input messages in the Messages API." | type: official
- [C9] 工具结果是 user 里的 tool_result.tool_use_id，不是 role=tool | src: https://platform.claude.com/docs/en/api/messages | quote: "return the following back to the model in a subsequent user message" | type: official
- [C10] tool_use 流是 partial_json，最终 input 才是 object | src: https://platform.claude.com/docs/en/build-with-claude/streaming | quote: "the deltas are partial JSON strings, whereas the final tool_use.input is always an object." | type: official
- [C11] SSE 以 message_stop 结束，不是 content_block_stop | src: https://platform.claude.com/docs/en/build-with-claude/streaming | quote: "A final message_stop event." | type: official
- [C12] Responses 函数调用须连 reasoning items 回传 | src: https://developers.openai.com/api/docs/guides/reasoning | quote: "pass back any reasoning items returned with the last function call" | type: official
- [C13] store:false 时 reasoning 默认带 encrypted_content | src: https://developers.openai.com/api/docs/guides/reasoning | quote: "include an encrypted_content property by default." | type: official
- [C14] 回传用 call_id，不是 function_call.id | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "linked to the call with call_id" | type: official
- [C15] arguments 是 JSON 字符串 | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "A JSON string of the arguments to pass to the function." | type: official
- [C16] tools：Chat Completions 外包 function；Responses name 与 type 同级 | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "function definitions are externally tagged. In Responses, they are internally tagged." | type: official
- [C17] response_format 在 Responses 改为 text.format | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "have moved from response_format to text.format" | type: official
- [C18] 长度字段是 max_output_tokens，含 reasoning tokens | src: https://developers.openai.com/api/reference/resources/responses/methods/create | quote: "including visible output tokens and reasoning tokens." | type: official
- [C19] Chat Completions 流是 delta chunk；Responses 是 typed event，完成看 response.completed | src: https://developers.openai.com/api/docs/guides/streaming-responses | quote: "response.completed" | type: official
- [C20] Gemini 3 函数调用不回传 thought signatures → 4xx（2026-09-04） | src: https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures | quote: "otherwise you will get a validation error (4xx status code)." | type: official
- [C21] 并行 functionCall 的签名只在第一段 | src: https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures | quote: "attached only to the first functionCall part." | type: official
- [C22] 并行结果交错成 FC,FR,FC,FR → 400 | src: https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures | quote: "the API will return a 400 error." | type: official
- [C23] contents.role 只能 user 或 model | src: https://ai.google.dev/api/generate-content | quote: "Must be either 'user' or 'model'." | type: official
- [C24] functionResponse.name 必填；id 须对齐 functionCall.id | src: https://ai.google.dev/api/generate-content | quote: "match the corresponding function call id." | type: official
- [C25] 系统提示是 systemInstruction，不是 role=system | src: https://ai.google.dev/api/generate-content | quote: "Developer set system instruction(s). Currently, text only." | type: official
- [C26] 流式方法是 :streamGenerateContent，SSE 用 alt=sse；页内无 [DONE] | src: https://ai.google.dev/api/generate-content | quote: "{model=models/*}:streamGenerateContent" | type: official
- [C27] 现行函数指南是 Interactions：须原样重放 thought 与 function_call（2026-09-17） | src: https://ai.google.dev/gemini-api/docs/function-calling | quote: "including thought and function_call steps exactly as received." | type: official

## conflicts
- Messages 同页正文 "there is no \"system\" role" vs schema role 含 system。https://platform.claude.com/docs/en/api/messages
- display 默认：Messages "Defaults to summarized" vs thinking "omitted, the default on many models"。https://platform.claude.com/docs/en/api/messages https://platform.claude.com/docs/en/build-with-claude/thinking
- thought signatures 同页混用 thoughtSignature 与 thought_signature（2026-09-04）。https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures
- 工具回传：generateContent functionResponse.name（id 可选）https://ai.google.dev/api/generate-content vs Interactions function_result.call_id https://ai.google.dev/gemini-api/docs/function-calling

## gaps
- Chat Completions 的 data: [DONE]：打开的 create 参考 .md 为 404，无原句
- Responses 收到 max_tokens、以及 Chat 的 max_completion_tokens 替换是否 400：未见到拒绝原句
- schema 列出 system 时，role=system 的实际错误文案未取到
- generateContent 流的结束条件（finishReason 或断连）参考页未写

## leads
- Interactions 的 previous_interaction_id / step.delta / function_result 应与 generateContent 分列：https://ai.google.dev/gemini-api/docs/text-generation
- 前缀一改 signature 可 400：https://platform.claude.com/docs/en/build-with-claude/thinking
- 哑签名 skip_thought_signature_validator：https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures
- GPT-6 Astra：reasoning.effort 或 reasoning_effort=none 返回 HTTP 400：https://developers.openai.com/api/docs/guides/reasoning
