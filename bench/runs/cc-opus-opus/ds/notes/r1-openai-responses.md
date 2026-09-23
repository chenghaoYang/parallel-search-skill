# r1-openai-responses
question: OpenAI Responses API（POST /v1/responses）及配套 Conversations API 当前（2026）文档里各维度的具体字段；OpenAI 官方 Chat Completions→Responses 迁移指南列出的差异；以及 "Open Responses" 开放规范是否存在、是什么、谁实现。
checked: https://developers.openai.com/api/docs/guides/migrate-to-responses, https://developers.openai.com/api/reference/resources/responses, https://developers.openai.com/api/docs/guides/conversation-state, https://developers.openai.com/api/docs/guides/reasoning, https://developers.openai.com/api/docs/guides/compaction, https://developers.openai.com/api/docs/guides/websocket-mode, https://developers.openai.com/api/reference/overview, https://developers.openai.com/api/docs/changelog, https://www.openresponses.org/, https://www.openresponses.org/specification, https://www.openresponses.org/governance

## claims
- [C1] D1：POST https://api.openai.com/v1/responses | src: https://developers.openai.com/api/reference/resources/responses | quote: "curl https://api.openai.com/v1/responses" | type: official
- [C2] D2：input 字符串或列表；system 级指导用顶层 instructions | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "Pass a string with input or a list of messages; use instructions for system-level guidance." | type: official
- [C3] D2：Items 取代 Messages | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "A message is a type of Item, as is a function_call or function_call_output." | type: official
- [C4] D2：role 枚举 | src: https://developers.openai.com/api/reference/resources/responses | quote: "One of user, assistant, system, or developer." | type: official
- [C5] D3：输入块仅三类（image_url/file_id；file_id/file_data/file_url） | src: https://developers.openai.com/api/reference/resources/responses | quote: "ResponseInputText or ResponseInputImage or ResponseInputFile" | type: official
- [C6] D4：function 工具扁平 {type:"function",name,parameters,strict} | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "In Responses, they are internally tagged." | type: official
- [C7] D4：strict 省略即尝试严格（CC 默认非严格） | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "In Responses, omitting strict attempts strict mode" | type: official
- [C8] D4：function_call 与 function_call_output 以 call_id 关联 | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "two distinct types of Items that are correlated using a call_id" | type: official
- [C9] D4：内置工具（参考另有 computer/shell/apply_patch） | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "like web_search, image_generation, file_search, code_interpreter, remote MCP servers" | type: official
- [C10] D5：store 默认 true | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "Responses are stored by default." | type: official
- [C11] D5：Conversations API 对象无 30 天 TTL | src: https://developers.openai.com/api/docs/guides/conversation-state | quote: "Conversation objects and items in them are not subject to the 30 day TTL." | type: official
- [C12] D5/D6：encrypted_content 默认返回，include 可省 | src: https://developers.openai.com/api/docs/guides/reasoning | quote: "accepts the legacy reasoning.encrypted_content value in include for compatibility, but doesn't require it" | type: official
- [C13] D5：压缩：context_management compaction 或 POST /v1/responses/compact | src: https://developers.openai.com/api/docs/guides/compaction | quote: "No separate /responses/compact call is required in this mode." | type: official
- [C14] D6：reasoning.effort 枚举 | src: https://developers.openai.com/api/reference/resources/responses | quote: "none, minimal, low, medium, high, xhigh, and max" | type: official
- [C15] D6：reasoning item 手动管理须回传 | src: https://developers.openai.com/api/reference/resources/responses | quote: "Be sure to include these items in your input to the Responses API for subsequent turns" | type: official
- [C16] D7：text.format{type:"json_schema",name,schema,strict} | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "Instead of response_format, use text.format in Responses." | type: official
- [C17] D8：每个 SSE 事件（response.created…completed、error）带 sequence_number | src: https://developers.openai.com/api/reference/resources/responses | quote: "The sequence number of this event." | type: official
- [C18] D9：status 六值 | src: https://developers.openai.com/api/reference/resources/responses | quote: "One of completed, failed, in_progress, cancelled, queued, or incomplete." | type: official
- [C19] D9：incomplete_details.reason | src: https://developers.openai.com/api/reference/resources/responses | quote: 「"max_output_tokens" or "max_messages" or "content_filter" or "steered"」 | type: official
- [C20] D9：usage 含 cached_tokens、cache_write_tokens、reasoning_tokens | src: https://developers.openai.com/api/reference/resources/responses | quote: "The number of input tokens that were written to the cache." | type: official
- [C21] D10：迁移指南缓存原句 | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "40% to 80% improvement when compared to Chat Completions in internal tests" | type: official
- [C22] D10：prompt_cache_key；prompt_cache_retention 弃用 | src: https://developers.openai.com/api/reference/resources/responses | quote: "Deprecated. Use prompt_cache_options.ttl instead." | type: official
- [C23] D12：response.error{code,message} | src: https://developers.openai.com/api/reference/resources/responses | quote: "An error object returned when the model fails to generate a Response." | type: official
- [C24] Assistants 已下线 | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "officially sunset on August 26, 2026, and is no longer available" | type: official
- [C25] CC 继续支持 | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "While Chat Completions remains supported" | type: official
- [C26] ORS 存在；OpenAI changelog 2026-01-15 宣布 | src: https://developers.openai.com/api/docs/changelog | quote: "built on top of the original OpenAI Responses API" | type: official
- [C27] ORS 治理：TSC，个人席位；CC-BY-4.0 / Apache-2.0 | src: https://www.openresponses.org/governance | quote: "No single vendor may control a majority of Core Maintainer seats." | type: official
- [C28] ORS 首页 logo（img alt），未注明谁已实现 | src: https://www.openresponses.org/ | quote: "nvidia Vercel OpenRouter Hugging Face LM Studio Databricks Red Hat AWS Ollama OpenAI vLLM Llama Stack" | type: official
- [C29] ORS D1（spec 2026-04-24）：Authorization、Content-Type 必需 | src: https://www.openresponses.org/specification | quote: "Clients MUST send request bodies encoded as application/json" | type: official
- [C30] ORS D2 | src: https://www.openresponses.org/specification | quote: "Items are bidirectional" | type: official
- [C31] ORS D5 | src: https://www.openresponses.org/specification | quote: "the server MUST load both the input and output associated with that prior response" | type: official
- [C32] ORS D11：扩展加 slug 前缀；有 /compliance 测试 | src: https://www.openresponses.org/specification | quote: "implements this spec directly or is a proper superset of Open Responses" | type: official
- [C33] ORS D8 | src: https://www.openresponses.org/specification | quote: "The terminal event MUST be the literal string [DONE]." | type: official

## conflicts
- 保留期：参考 "stored for at least 30 days" vs conversation-state "Response objects are saved for 30 days by default."
- 音频：overview "audio, image, and text inputs" vs 迁移指南 Audio 行 "Coming soon"；输入块无 input_audio。
- WS：websocket-mode "one persistent connection to /v1/responses can run parallel conversations" vs ORS "Servers MUST NOT multiplex multiple in-flight responses over one connection"。

## gaps
- OA-R [DONE]：文档无该字样，无正面原句。

## leads
- vLLM /v1/responses 对齐 ORS（vllm issue #32850）。
- function_call_output.call_id 在参考与 openai-python 3.19.0 标 optional。
