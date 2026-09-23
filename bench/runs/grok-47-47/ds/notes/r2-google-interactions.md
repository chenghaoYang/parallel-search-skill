# r2-google-interactions
question: Gemini Interactions API 是不是与 generateContent 不同的请求协议？结构化输出现在官方让调用方用哪个字段？
checked: https://ai.google.dev/api/interactions-api https://ai.google.dev/api/interactions-api-v1 https://ai.google.dev/gemini-api/docs/interactions-overview https://ai.google.dev/gemini-api/docs/function-calling https://ai.google.dev/gemini-api/docs/streaming https://ai.google.dev/gemini-api/docs/structured-output https://ai.google.dev/gemini-api/docs/migrate-to-interactions https://ai.google.dev/api/generate-content https://ai.google.dev/gemini-api/docs/interactions.md.txt https://ai.google.dev/gemini-api/docs/interactions/function-calling.md.txt

## claims
- [C1] D1 2026-09-22 beta reference：创建是 POST `/v1beta/interactions`，不是 `:generateContent`。 | src: https://ai.google.dev/api/interactions-api | quote: "post https://generativelanguage.googleapis.com/v1beta/interactions Creates a new interaction." | type: official
- [C2] D1 2026-09-21 v1 reference：另有 POST `/v1/interactions`。 | src: https://ai.google.dev/api/interactions-api-v1 | quote: "post https://generativelanguage.googleapis.com/v1/interactions Creates a new interaction." | type: official
- [C3] D1 2026-09-22：该页自称 beta，端点在 `/v1beta/`。 | src: https://ai.google.dev/api/interactions-api | quote: "You are viewing the beta version of the Interactions API. Endpoints are under `/v1beta/`." | type: official
- [C4] D1 2026-09-17 curl 头；下一行 Content-Type: application/json。reference 无必须 header 句。 | src: https://ai.google.dev/gemini-api/docs/function-calling | quote: "-H \"x-goog-api-key: $GEMINI_API_KEY\"" | type: official
- [C5] D2 2026-09-21：可选 `previous_interaction_id`。 | src: https://ai.google.dev/api/interactions-api-v1 | quote: "previous_interaction_id string (optional) The ID of the previous interaction, if any." | type: official
- [C6] D2 2026-09-17：服务端用该 id 取历史。下一行是 resend the entire chat history. | src: https://ai.google.dev/gemini-api/docs/interactions-overview | quote: "uses this ID to retrieve the conversation history, saving you from having to" | type: official
- [C7] D2 2026-09-17 store=false 后不能再用 previous_interaction_id。下一行 for subsequent turns。 | src: https://ai.google.dev/gemini-api/docs/interactions-overview | quote: "`store=false` is incompatible with" | type: official
- [C8] D2 2026-09-17 无状态要重放 input。 | src: https://ai.google.dev/gemini-api/docs/function-calling | quote: "In stateless mode, you must pass the full history of the conversation in the `input` field of each subsequent request." | type: official
- [C9] D5 2026-09-21：函数参数是 JSON Schema。同段 type 原行 Always set to "function"。 | src: https://ai.google.dev/api/interactions-api-v1 | quote: "parameters object (optional) The JSON Schema for the function's parameters." | type: official
- [C10] D5 2026-09-21：工具结果 step 的 type 是 `function_result`。v1/v1beta reference 全文无 `functionResponse`。 | src: https://ai.google.dev/api/interactions-api-v1 | quote: "Always set to `\"function_result\"`." | type: official
- [C11] D5 2026-09-17 指南：结果放在 `function_result` 步的 `result`。 | src: https://ai.google.dev/gemini-api/docs/function-calling | quote: "include it as one or more content blocks in the `result` field of the `function_result` step." | type: official
- [C12] D7 2026-09-22：流式是同一创建请求的 `stream` 布尔，不是另一个方法名。 | src: https://ai.google.dev/api/interactions-api | quote: "stream boolean (optional) Input only. Whether the interaction will be streamed." | type: official
- [C13] D7 2026-09-17 结束行；上一行 event: done。页首链接前有 stream: true … using。 | src: https://ai.google.dev/gemini-api/docs/streaming | quote: "data: [DONE]" | type: official
- [C14] D7 2026-09-17 迁移：同端点 body stream，generateContent 另打 :streamGenerateContent。 | src: https://ai.google.dev/gemini-api/docs/migrate-to-interactions | quote: "the Interactions API uses the same endpoint with `\"stream\": true` in the request body, whereas the `generateContent` API required calling a dedicated endpoint (`:streamGenerateContent`)." | type: official
- [C15] D8 2026-09-21 status：in_progress, requires_action, completed, failed, cancelled, incomplete（hitting max_tokens）。无 finishReason。 | src: https://ai.google.dev/api/interactions-api-v1 | quote: "Required. Output only. The status of the interaction." | type: official
- [C16] D8 2026-09-22 样例 step type=model_output；文本行 Required. The text content. | src: https://ai.google.dev/api/interactions-api | quote: "\"type\": \"model_output\"" | type: official
- [C17] D8 2026-09-22 usage.total_input_tokens。同段还有 total_output_tokens、total_thought_tokens、total_tokens、total_tool_use_tokens；上一行 total_cached_tokens。 | src: https://ai.google.dev/api/interactions-api | quote: "total_input_tokens integer (optional) Number of tokens in the prompt (context)." | type: official
- [C18] D9 Interactions 2026-09-21：顶层 response_format 用 JSON schema 约束输出。 | src: https://ai.google.dev/api/interactions-api-v1 | quote: "Enforces that the generated response is a JSON object that complies with the JSON schema specified in this field." | type: official
- [C19] D9 指南 2026-09-17（/json-mode 301 到此）：schema 在 schema；同行有 type text 与 mime_type application/json。样例 interactions.create。 | src: https://ai.google.dev/gemini-api/docs/structured-output | quote: "The schema should be provided in the `schema` field." | type: official
- [C21] D9 迁移 2026-09-17：generateContent 仍用 response_mime_type 与 response_schema。 | src: https://ai.google.dev/gemini-api/docs/migrate-to-interactions | quote: "using the `response_mime_type` and `response_schema` fields nested inside the `config` (or `generationConfig`) object." | type: official
- [C22] D9 generateContent ref 2026-09-22：responseSchema 下 (deprecated)，警告 This item is deprecated。样例仍有 response_schema。 | src: https://ai.google.dev/api/generate-content | quote: "Optional. Output schema of the generated candidate text." | type: official
- [C23] D9 同页 responseJsonSchema 自称内部细节并自指。 | src: https://ai.google.dev/api/generate-content | quote: "Optional. An internal detail. Use `responseJsonSchema` rather than this field." | type: official
- [C24] D10 2026-09-17 GA 且 recommended for all，下一行 new projects。不是 :generateContent。 | src: https://ai.google.dev/gemini-api/docs/interactions-overview | quote: "As of June 2026, it is Generally Available and recommended for all" | type: official

## conflicts
- 是否替代，未裁决。overview "it is now considered legacy"；迁移 "we recommend the Interactions API for all new development"。https://ai.google.dev/gemini-api/docs/interactions.md.txt（HTML 301）"currently in Beta" / "recommended path for stable deployments"。https://ai.google.dev/gemini-api/docs/interactions/function-calling.md.txt "we recommend you continue to use the `generateContent` API."（HTML 301；现行 md 无）。beta "You are viewing the beta version"，另有 v1。
- D9 无唯一名。https://ai.google.dev/api/generate-content 2026-09-22：responseSchema "This item is deprecated!"；_responseJsonSchema deprecated 但 "alternative to `responseSchema` that accepts"；responseJsonSchema "Use `responseJsonSchema` rather than this field."；responseFormat "Allows specifying output configuration per modality"，"Only applicable when mimeType is APPLICATION_JSON."。迁移仍 response_schema；Interactions "move to a top-level `response_format` array"。指南只在 interactions.create。
- D5 同页 Go "FunctionResponse: &genai.FunctionResponse"，REST 是 function_result（https://ai.google.dev/gemini-api/docs/function-calling）。
- D10 "Custom safety settings are not supported in the Interactions API." vs "safety_settings array (SafetySetting) (optional) Safety settings for the interaction." 同段还有 Batch API、Automatic function calling (Python)、Explicit caching；not yet 与 available 换行。

## gaps
- reference 无必须 header 原句，也没说 required 的 api_version 是否还要查询参数。curl 无该参数。
- reference 有 interaction.completed "emitted at the end of the stream"，无 data: [DONE]。一条 REST 同时 ?alt=sse 与 stream true；流式指南没写 alt=sse。
- beta status 另有 queued 与 Deprecated 的 budget_exceeded，v1 没有。generateContent D9 无单一字段名。

## leads
- 旧 md.txt 未跟 HTML 301。函数指南 Go 样例仍是 generateContent。Vertex 未查。
