# r2-google-interactions
question: Google 新的 Interactions API（v1beta/interactions）是什么、与 generateContent 的关系（继任/并行）、responseSchema 标弃用后的替代是什么？
checked: https://ai.google.dev/api/interactions-api, https://ai.google.dev/gemini-api/docs/interactions-overview, https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026, https://ai.google.dev/gemini-api/docs/migrate-to-interactions, https://ai.google.dev/gemini-api/docs/api-key, https://ai.google.dev/api

## claims
- [C1] CreateInteraction 端点 POST /v1beta/interactions | src: https://ai.google.dev/api/interactions-api | quote: "https://generativelanguage.googleapis.com/v1beta/interactions Creates a new interaction." | type: official
- [C2] 参考页为 beta，另有稳定版 v1 | src: https://ai.google.dev/api/interactions-api | quote: "Beta: You are viewing the beta version of the Interactions API. Endpoints are under /v1beta/. The stable v1 version is also available." | type: official
- [C3] 认证用 x-goog-api-key header，官方 REST 示例即打 POST /v1beta/interactions | src: https://ai.google.dev/gemini-api/docs/api-key | quote: "curl \"https://generativelanguage.googleapis.com/v1beta/interactions\" … -H \"x-goog-api-key: YOUR_API_KEY\"" | type: official
- [C4] 所有请求必须带 x-goog-api-key（补 R1 gap） | src: https://ai.google.dev/api | quote: "All requests to the Gemini API must include a x-goog-api-key header with your API key." | type: official
- [C5] 顶层必填 input（不再是 contents）：Content、Content 数组、Step 数组或 string | src: https://ai.google.dev/api/interactions-api | quote: "input Content or array (Content) or array (Step) or string (required) The inputs for the interaction (common to both Model and Agent)." | type: official
- [C6] 顶层 generation_config 与 agent_config 二选一，前者仅限 model 模式 | src: https://ai.google.dev/api/interactions-api | quote: "Configuration parameters for the model interaction. Alternative to `agent_config`. Only applicable when `model` is set." | type: official
- [C7] 顶层布尔 stream/store/background（流式/存储请求响应/后台运行） | src: https://ai.google.dev/api/interactions-api | quote: "store boolean (optional) Input only. Whether to store the response and request for later retrieval." | type: official
- [C8] system 处理：顶层字符串 system_instruction，不再有 role=system contents part | src: https://ai.google.dev/api/interactions-api | quote: "system_instruction string (optional) System instruction for the interaction." | type: official
- [C9] server-side 状态：默认存储，previous_interaction_id 续接，store=false 关闭 | src: https://ai.google.dev/gemini-api/docs/interactions-overview | quote: "You can opt into stateless behavior by setting store=false." | type: official
- [C10] 响应不再用 contents/parts：May 2026 新 schema 以 steps 取代 outputs | src: https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026 | quote: "The new schema replaces the outputs array with a steps array." | type: official
- [C11] Content 为类型化块联合（AudioContent/DocumentContent/ImageContent…），无 role/parts | src: https://ai.google.dev/api/interactions-api | quote: "Content The content of the response. Possible Types AudioContent An audio content block." | type: official
- [C12] 旧响应有顶层 "role":"model"；当前参考页全页无 role 字段，新示例仅 SDK 便捷属性 output_text | src: https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026 | quote: "// Response { \"id\": \"int_123\", \"role\": \"model\", \"outputs\": [...] }" | type: official
- [C13] function calling：顶层 tools 数组传声明 | src: https://ai.google.dev/api/interactions-api | quote: "tools array (Tool) (optional) A list of tool declarations the model may call during interaction." | type: official
- [C14] 工具调用为 Step，判别串含 function_call/thought/model_output/user_input；function_call 步含 id/name/arguments | src: https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026 | quote: "{ \"type\": \"function_call\", \"id\": \"fc_1\", \"name\": \"get_weather\", \"arguments\": { \"location\": \"Boston\" }" | type: official
- [C17] D8 替代物：顶层 response_format（ResponseFormat 或数组） | src: https://ai.google.dev/api/interactions-api | quote: "response_format … (optional) Enforces that the generated response is a JSON object that complies with the JSON schema specified in this field." | type: official
- [C18] schema 放 TextResponseFormat.schema，需 mime_type=application/json，type 恒为 "text" | src: https://ai.google.dev/api/interactions-api | quote: "schema object (optional) The JSON schema that the output should conform to. Only applicable when mime_type is application/json." | type: official
- [C19] breaking change：response_format 收编输出格式控制并移除 response_mime_type | src: https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026 | quote: "A new polymorphic response_format consolidates all output format controls and removes response_mime_type." | type: official
- [C20] 官方映射：gc 的 response_mime_type+response_schema → Interactions 顶层 response_format | src: https://ai.google.dev/gemini-api/docs/migrate-to-interactions | quote: "In generateContent, you configure output format using the response_mime_type and response_schema fields." | type: official
- [C21] 迁移后写法 response_format=[{"type":"text","mime_type":"application/json","schema":…}] | src: https://ai.google.dev/gemini-api/docs/migrate-to-interactions | quote: "In the Interactions API, output format controls move to a top-level response_format array." | type: official
- [C22] D9：思考量由 generation_config.thinking_level 控制，枚举 minimal/low/medium/high，无 thinkingBudget | src: https://ai.google.dev/api/interactions-api | quote: "thinking_level ThinkingLevel (optional) The level of thought tokens that the model should generate." | type: official
- [C23] 思考摘要开关 thinking_summaries，枚举 auto/none | src: https://ai.google.dev/api/interactions-api | quote: "Whether to include thought summaries in the response. Possible values auto … none" | type: official
- [C24] 签名：thought 步带 signature；流式有 ThoughtSignatureDelta.signature | src: https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026 | quote: "{ \"type\": \"thought\", \"signature\": \"abc123...\" }" | type: official
- [C25] D11：Interactions API 2026-06 GA、推荐所有新项目；generateContent 称 legacy 但完全受支持 | src: https://ai.google.dev/gemini-api/docs/interactions-overview | quote: "As of June 2026, it is Generally Available and recommended for all new projects. While it is now considered legacy, the original generateContent API remains fully supported." | type: official
- [C26] 后续新特性只上 Interactions API | src: https://ai.google.dev/gemini-api/docs/interactions-overview | quote: "Going forward, all new models, multimodal capabilities, tools, and agentic features will launch on the Interactions API." | type: official
- [C27] 参考首页列 CreateInteraction 为 (Recommended)，与 generateContent 并存 | src: https://ai.google.dev/api | quote: "Interactions (CreateInteraction) (Recommended): The recommended standard primitive for building with Gemini." | type: official
- [C29] 破坏性变更页标题含 May 2026；流式事件改名 interaction.start→interaction.created、content.*→step.* | src: https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026 | quote: "interaction.start → interaction.created content.start → step.start" | type: official

## conflicts
- R1 记录 /api/generate-content 把 responseSchema 标 "This item is deprecated!" 且未指替代；migrate-to-interactions 页却映射 response_schema → Interactions response_format[].schema。不直接矛盾（前者讲 gc 内部无替代、后者讲跨 API 迁移），但 gc 参考页未交叉引用迁移目标。
- interactions-overview 称 Interactions API "Generally Available"（June 2026），其 API 参考页仍标 "Beta … /v1beta/"（另有 stable v1）。GA 与 beta 横幅并存，未裁决。

## gaps
- generateContent 端点下线时间表：已查页只说 "remains fully supported"/"considered legacy"，无截止日期；Deprecations 页未读。
- 现行 schema 无 role 字段系全页零出现推断，未见"role 已移除"官方原句。
- v1（stable）参考页未单独抓取。

## leads
- migrate-to-interactions 页含 thinking/tools/caching 全字段迁移映射表，可复用于其他格子。
- overview 称多轮经 server-side state 有 "Lower cost with higher cache hit rates"，与 R1"显式缓存不支持于 Interactions"并读，缓存语义已重构。
- 导航新增 Agents 子树（Credentials/Hooks/Environments）及 Triggers、Webhooks、File Search API。
