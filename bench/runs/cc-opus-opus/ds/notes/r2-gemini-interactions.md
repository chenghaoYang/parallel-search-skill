# r2-gemini-interactions
question: Google Gemini Interactions API（Google 现在推荐的新协议，generateContent 已标 Legacy）的请求/响应协议表面是什么？与 generateContent 的主要差异是什么？
checked: https://ai.google.dev/gemini-api/docs/interactions,https://ai.google.dev/api/interactions-api,https://ai.google.dev/api/interactions-api-v1,https://ai.google.dev/static/api/interactions.openapi.json,https://ai.google.dev/gemini-api/docs/migrate-to-interactions,https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026,https://ai.google.dev/gemini-api/docs/streaming,https://ai.google.dev/gemini-api/docs/thinking,https://ai.google.dev/gemini-api/docs/background-execution,https://ai.google.dev/gemini-api/docs/caching,https://raw.githubusercontent.com/googleapis/python-genai/main/google/genai/_gaos/types/interactions/generationconfig.py

## claims
- [C1] 2026-06 GA；generateContent 称 legacy（2026-09-17） | src: https://ai.google.dev/gemini-api/docs/interactions | quote: "As of June 2026, it is Generally Available" … "now considered legacy" | type: official
- [C2] D1 POST /v1beta/interactions（2026-09-22） | src: https://ai.google.dev/api/interactions-api | quote: "Endpoints are under /v1beta/. The stable v1 version is also available." | type: official
- [C3] D1 鉴权头 x-goog-api-key | src: https://ai.google.dev/static/api/interactions.openapi.json | quote: "Gemini API key sent as x-goog-api-key." | type: official
- [C4] D1 model 在 body；可改传 agent（deep-research-preview-04-2026 等） | src: https://ai.google.dev/api/interactions-api | quote: "Required if `model` is not provided." | type: official
- [C5] D2 容器 input（string/Content/Content[]/Step[]）；system_instruction 顶层字符串 | src: https://ai.google.dev/api/interactions-api | quote: "The inputs for the interaction (common to both Model and Agent). system_instruction string" | type: official
- [C6] D2 无状态多轮：回传 steps，新轮为 user_input step | src: https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026 | quote: "appending your new user turn as a user_input step." | type: official
- [C7] D3 块 type=text/image/audio/document/video，data 或 uri | src: https://ai.google.dev/gemini-api/docs/migrate-to-interactions | quote: "\"type\": \"image\", \"mime_type\": \"image/jpeg\", \"data\": \"...\"" | type: official
- [C8] D4 函数工具扁平：{type:"function",name,description,parameters} | src: https://ai.google.dev/gemini-api/docs/migrate-to-interactions | quote: "\"type\": \"function\", \"name\": \"get_weather\"" | type: official
- [C9] D4 function_call(id,name,arguments)；回传 function_result(call_id,result,is_error) | src: https://ai.google.dev/api/interactions-api | quote: "Required. ID to match the ID from the function call block." | type: official
- [C10] D4 内置工具 type：google_search/code_execution/url_context/google_maps/file_search/computer_use/mcp_server | src: https://ai.google.dev/api/interactions-api | quote: "Always set to \"code_execution\"." | type: official
- [C11] D5 store 默认 true；付费留存 55 天；store=false 不能 background | src: https://ai.google.dev/gemini-api/docs/interactions | quote: "(store=true)" … "retains interactions for 55 days" … "store=false is incompatible with background execution" | type: official
- [C12] D5 previous_interaction_id 只续历史，tools 等每轮重传 | src: https://ai.google.dev/gemini-api/docs/interactions | quote: "The other parameters are interaction-scoped" | type: official
- [C13] D5 background:true 立即返回 id（2026-09-17） | src: https://ai.google.dev/gemini-api/docs/background-execution | quote: "The API immediately returns an interaction ID" | type: official
- [C14] D6 thinking_level=minimal/low/medium/high；thinking_summaries=auto/none | src: https://ai.google.dev/api/interactions-api | quote: "The level of thought tokens that the model should generate." | type: official
- [C15] D6 thought step(signature,summary)；有状态免管，无状态须原样回传 | src: https://ai.google.dev/gemini-api/docs/thinking | quote: "you do not need to do anything regarding signatures" … "You MUST always resend all thought blocks" | type: official
- [C16] D7 顶层 response_format {type:"text",mime_type,schema} | src: https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026 | quote: "The API removes response_mime_type." | type: official
- [C17] D7 generation_config.max_output_tokens（另 seed、stop_sequences、tool_choice） | src: https://ai.google.dev/api/interactions-api | quote: "The maximum number of tokens to include in the response." | type: official
- [C18] D8 同端点 "stream": true | src: https://ai.google.dev/gemini-api/docs/migrate-to-interactions | quote: "uses the same endpoint with \"stream\": true" | type: official
- [C19] D8 事件 interaction.created/status_update/completed、step.start/delta/stop、error；尾 [DONE]（2026-09-17） | src: https://ai.google.dev/gemini-api/docs/streaming | quote: "event: done data: [DONE]" | type: official
- [C20] D9 status：in_progress/requires_action/completed/failed/cancelled/incomplete/queued | src: https://ai.google.dev/api/interactions-api | quote: "contains incomplete results (e.g. hitting max_tokens)." | type: official
- [C21] D9 usage：total_input/output/thought/cached/tool_use_tokens、total_tokens | src: https://ai.google.dev/api/interactions-api | quote: "\"total_input_tokens\": 7, \"total_output_tokens\": 20," | type: official
- [C22] D10 仅隐式缓存（2026-09-02） | src: https://ai.google.dev/gemini-api/docs/caching | quote: "The Interactions API only supports implicit caching." | type: official
- [C23] D12 {"error":{code,message}}，流式 event: error | src: https://ai.google.dev/gemini-api/docs/streaming | quote: "Contains an error object with a message and code." | type: official
- [C24] 2026-05：outputs→steps、多态 response_format、Api-Revision: 2026-05-20 | src: https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026 | quote: "The legacy schema will be removed on June 8, 2026." | type: official

## conflicts
- 端点：https://ai.google.dev/api/interactions-api-v1 "https://generativelanguage.googleapis.com/v1/interactions" vs https://ai.google.dev/gemini-api/docs/migrate-to-interactions "https://generativelanguage.googleapis.com/v1beta2/interactions"（C2 为 v1beta）
- 事件：https://ai.google.dev/gemini-api/docs/streaming "Signals an interaction-level status transition." vs https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026 "interaction.status_update → replaced by interaction.in_progress"
- 采样：https://ai.google.dev/gemini-api/docs/interactions "generation_config (including thinking_level, temperature, etc.)" vs OpenAPI/SDK GenerationConfig 无 temperature/top_p（观察）
- mime：C16 vs https://ai.google.dev/static/api/interactions.openapi.json response_mime_type "This is required if response_format is set."
- safety：https://ai.google.dev/gemini-api/docs/interactions "Custom safety settings are not supported" vs https://ai.google.dev/api/interactions-api "Safety settings for the interaction."

## gaps
- role：OpenAPI 无此字段。
- 迁移指南示例字段（partial_arguments、prompt_tokens）与参考不符。

## leads
- 不支持：Batch API、Python 自动函数调用、显式缓存。
- 引用改为 annotations。
