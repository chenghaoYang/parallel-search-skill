# r2-gemini-interactions
question: Gemini Interactions API(2026-06 GA)D2–D10请求/响应形状;补generateContent D9缺口;裁决D2角色冲突。
checked: https://ai.google.dev/gemini-api/docs/interactions-overview, https://ai.google.dev/api/interactions-api, https://ai.google.dev/api/generate-content, https://ai.google.dev/gemini-api/docs/function-calling, https://github.com/googleapis/googleapis/blob/master/google/ai/generativelanguage/v1beta/content.proto

## claims
- [C1] D2 model/agent二选一必填 | src: https://ai.google.dev/api/interactions-api | quote: "Required if `agent` is not provided." | type: official
- [C2] D2 input=Content/array(Content)/array(Step)/string,必填 | src: https://ai.google.dev/api/interactions-api | quote: "input Content or array ( Content ) or array ( Step ) or string (required)" | type: official
- [C3] D2 system_instruction仅字符串 | src: https://ai.google.dev/api/interactions-api | quote: "system_instruction string (optional) System instruction for the interaction." | type: official
- [C4] D2 Content用type区分5种,无role字段;角色改由Step.type承担 | src: https://ai.google.dev/api/interactions-api | quote: "type object (required) No description provided. Always set to \"text\" ." | type: official
- [C5] D4 status枚举8值,含requires_action/incomplete/budget_exceeded(deprecated)等 | src: https://ai.google.dev/api/interactions-api | quote: "status enum (string) (optional) Required. Output only. The status of the interaction." | type: official
- [C6] D4 steps是输出容器 | src: https://ai.google.dev/api/interactions-api | quote: "steps array ( Step ) (optional) Output only. The steps that make up the interaction" | type: official
- [C7] D5 Function工具声明是扁平对象,不嵌套functionDeclarations[] | src: https://ai.google.dev/api/interactions-api | quote: "parameters object (optional) The JSON Schema for the function's parameters." | type: official
- [C8] D5 FunctionCallStep字段id/name/arguments,type固定function_call | src: https://ai.google.dev/api/interactions-api | quote: "id string (required) Required. A unique ID for this specific tool call." | type: official
- [C9] D5 FunctionResultStep用call_id配对id,type固定function_result | src: https://ai.google.dev/api/interactions-api | quote: "call_id string (required) Required. ID to match the ID from the function call block." | type: official
- [C10] D6 thinking_level四档minimal/low/medium/high,thinking_summaries两值auto/none | src: https://ai.google.dev/api/interactions-api | quote: "thinking_level ThinkingLevel (optional) The level of thought tokens that the model should generate." | type: official
- [C11] D6 ThoughtStep=signature+summary(摘要非全文) | src: https://ai.google.dev/api/interactions-api | quote: "signature string (optional) A signature hash for backend validation. summary array (ThoughtSummaryContent)" | type: official
- [C12] D7 response_format取代Gen的responseSchema | src: https://ai.google.dev/api/interactions-api | quote: "response_format ResponseFormat or array ( ResponseFormat ) (optional) Enforces that the generated response is a JSON object" | type: official
- [C13] D7 TextResponseFormat.schema仅在mime_type=application/json时生效 | src: https://ai.google.dev/api/interactions-api | quote: "schema object (optional) The JSON schema that the output should conform to. Only applicable when mime_type is application/json." | type: official
- [C14] D8 stream为Input only字段 | src: https://ai.google.dev/api/interactions-api | quote: "stream boolean (optional) Input only. Whether the interaction will be streamed." | type: official
- [C15] D8 SSE用event_type判别,7种含step.start/step.delta/step.stop/interaction.* | src: https://ai.google.dev/api/interactions-api | quote: "event_type object (required) No description provided. Always set to \"step.start\" ." | type: official
- [C16] D8 流结束标志=interaction.completed事件;每个SSE事件带event_id供断线重连 | src: https://ai.google.dev/api/interactions-api | quote: "Partial completed interaction resource emitted at the end of the stream." | type: official
- [C17] D9 generation_config只有9字段(不含temperature/top_p/top_k/candidate_count,全页0命中) | src: https://ai.google.dev/api/interactions-api | quote: "generation_config GenerationConfig (optional) Model Configuration Configuration parameters for the model interaction." | type: official
- [C18] D9 max_output_tokens原句 | src: https://ai.google.dev/api/interactions-api | quote: "max_output_tokens integer (optional) The maximum number of tokens to include in the response." | type: official
- [C19] D9 seed原句(措辞与Gen不同) | src: https://ai.google.dev/api/interactions-api | quote: "seed integer (optional) Seed used in decoding for reproducibility." | type: official
- [C20] D10 usage为独立Usage对象,6个total_*字段+按modality拆分数组 | src: https://ai.google.dev/api/interactions-api | quote: "usage Usage (optional) Output only. Statistics on the interaction request's token usage." | type: official
- [C21] 附 store默认true,可store=false关闭;留存期付费55天/免费1天 | src: https://ai.google.dev/gemini-api/docs/interactions-overview | quote: "By default, the API stores all Interaction objects ( store=true )" | type: official
- [C22] 附 background字段,Input only,后台运行 | src: https://ai.google.dev/api/interactions-api | quote: "background boolean (optional) Input only. Whether to run the model interaction in the background." | type: official
- [C23] GGL-Gen D9 candidateCount原句 | src: https://ai.google.dev/api/generate-content | quote: "candidateCount integer Optional. Number of generated responses to return. If unset, this will default to 1." | type: official
- [C24] GGL-Gen D9 maxOutputTokens原句 | src: https://ai.google.dev/api/generate-content | quote: "maxOutputTokens integer Optional. The maximum number of tokens to include in a response candidate." | type: official
- [C25] GGL-Gen D9 topP原句 | src: https://ai.google.dev/api/generate-content | quote: "topP number Optional. The maximum cumulative probability of tokens to consider when sampling." | type: official
- [C26] GGL-Gen D9 topK原句 | src: https://ai.google.dev/api/generate-content | quote: "topK integer Optional. The maximum number of tokens to consider when sampling." | type: official
- [C27] GGL-Gen D9 seed原句 | src: https://ai.google.dev/api/generate-content | quote: "seed integer Optional. Seed used in decoding. If not set, the request uses a randomly generated seed." | type: official
- [C28] GGL-Gen D2 role字段限定user/model | src: https://ai.google.dev/api/generate-content | quote: "role string Optional. The producer of the content. Must be either 'user' or 'model'." | type: official
- [C29] GGL-Gen D2 同页functionDeclarations称FunctionResponse用Content.role"function" | src: https://ai.google.dev/api/generate-content | quote: "The next conversation turn may contain a FunctionResponse with the Content.role \"function\" generation context for the next model turn." | type: official

## conflicts
- GGL-Gen D2无法裁决,记规范级矛盾:C28/C29矛盾逐字复现在proto — src: https://github.com/googleapis/googleapis/blob/master/google/ai/generativelanguage/v1beta/content.proto | quote: "Must be either 'user' or 'model'." 同文件另一处 quote: "with the [Content.role]...\"function\" generation context"。无跑通的REST示例可裁决,只记录矛盾。
- Interactions safety冲突:https://ai.google.dev/api/interactions-api 列出请求字段 quote: "safety_settings array (SafetySetting) (optional) Safety settings for the interaction."；但 https://ai.google.dev/gemini-api/docs/interactions-overview quote: "Custom safety settings are not supported in the Interactions API." 两页相反。

## gaps
- thought signature是否必须手动回传:参考页只说"用于backend validation",无"required to resend"字样;function-calling指南泛泛提"SDKs automatically handle thought signatures"(非Interactions专属),不回传是否报错未找到原句。
- background=true后如何轮询/取回结果,request-body级文档未说明,需查/gemini-api/docs/background-execution(未抓,4次pplx-safe额度未用,直接URL已够)。
- agent_config三种类型(Antigravity/DeepResearch/Dynamic)字段未逐一摘录完。

## leads
- 简报起点URL https://ai.google.dev/api/interactions 已404,正确页是 https://ai.google.dev/api/interactions-api(从interactions-overview页内链接发现)。
- CreateInteraction还有必填query参数api_version,影响D1但超出本工人范围。
- FunctionCallStep无signature字段,但CodeExecutionCallStep/FileSearchCallStep/GoogleMapsCallStep/GoogleSearchCallStep都有,工具类型间不对称。
