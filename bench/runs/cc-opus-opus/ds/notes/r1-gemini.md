# r1-gemini
question: Google Gemini API 原生 generateContent / streamGenerateContent 协议当前（2026）文档里各维度的具体字段，以及 Vertex AI 上同一协议的接入差异（端点/鉴权）。
checked: https://ai.google.dev/gemini-api/docs/api-versions, https://docs.cloud.google.com/gemini-enterprise-agent-platform/vertex-ai-name-changes

## claims
- [C1] 端点，模型在路径（页 2026-09-22） | src: https://ai.google.dev/api/generate-content | quote: "https://generativelanguage.googleapis.com/v1beta/{model=models/*}:generateContent" | type: official
- [C2] x-goog-api-key 头 | src: https://ai.google.dev/api | quote: "must include a x-goog-api-key header" | type: official
- [C3] 流式 ?alt=sse；示例用 ?key= | src: https://ai.google.dev/api/generate-content | quote: "streamGenerateContent?alt=sse&key=${GEMINI_API_KEY}" | type: official
- [C4] 文档标 "(Legacy)"，推荐 Interactions | src: https://ai.google.dev/gemini-api/docs/migrate-to-interactions | quote: "we recommend the Interactions API for all new development." | type: official
- [C5] Vertex（现 Agent Platform）区域主机 {L}-aiplatform.googleapis.com；global： | src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/locations | quote: "https://aiplatform.googleapis.com/v1/projects/${GOOGLE_CLOUD_PROJECT}/locations/global/publishers/google/models/${MODEL_ID}:generateContent" | type: official
- [C6] Vertex 用 OAuth Bearer | src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/locations | quote: "Authorization: Bearer $(gcloud auth print-access-token)" | type: official
- [C7] contents[]={role,parts[]} | src: https://ai.google.dev/api/generate-content | quote: "Must be either 'user' or 'model'." | type: official
- [C8] 另有 tools, toolConfig, safetySettings, systemInstruction(仅文本), generationConfig, cachedContent | src: https://ai.google.dev/api/generate-content | quote: "Currently, text only." | type: official
- [C9] functionResponse 以 role user 回传 | src: https://ai.google.dev/gemini-api/docs/generate-content/function-calling | quote: "role: 'user', parts: [{ functionResponse: function_response_part }]" | type: official
- [C10] 无状态，历史客户端自带；chats 为 SDK 侧 | src: https://ai.google.dev/gemini-api/docs/migrate-to-interactions | quote: "using the contents array or a client-side chat helper." | type: official
- [C11] Part：text, inlineData{mimeType,data}, fileData{mimeType,fileUri}, functionCall, functionResponse 等 | src: https://ai.google.dev/api/generate-content | quote: "A Part can only contain one of the accepted types in Part.data." | type: official
- [C12] Files API：POST /upload/v1beta/files | src: https://ai.google.dev/gemini-api/docs/generate-content/files | quote: "per-file maximum size of 2 GB. Files are stored for 48 hours." | type: official
- [C13] 内置工具 googleSearch, codeExecution, urlContext, fileSearch, googleMaps 等 | src: https://ai.google.dev/api/generate-content | quote: "Tool to support URL context retrieval." | type: official
- [C14] parameters 为 OpenAPI 子集 | src: https://ai.google.dev/gemini-api/docs/generate-content/function-calling | quote: "a select subset of the OpenAPI schema format." | type: official
- [C15] parametersJsonSchema 与 parameters 互斥 | src: https://ai.google.dev/api/generate-content | quote: "This field is mutually exclusive with parameters." | type: official
- [C16] functionCallingConfig{mode: AUTO/ANY/NONE/VALIDATED, allowedFunctionNames} | src: https://ai.google.dev/api/caching | quote: "If unspecified, the default value will be set to AUTO." | type: official
- [C17] functionCall.args 为对象；functionResponse{id,name,response} | src: https://ai.google.dev/api/generate-content | quote: "The function parameters and values in JSON object format." | type: official
- [C18] Gemini 3 必返 id，回传同 id | src: https://ai.google.dev/gemini-api/docs/generate-content/function-calling | quote: "Gemini 3 now always returns a unique id with every functionCall." | type: official
- [C19] thinkingConfig{includeThoughts, thinkingBudget, thinkingLevel: MINIMAL/LOW/MEDIUM/HIGH}；Level 用于旧模型报错 | src: https://ai.google.dev/api/generate-content | quote: "Use with earlier models results in an error." | type: official
- [C20] thinkingBudget：0 关，-1 动态 | src: https://ai.google.dev/gemini-api/docs/generate-content/thinking | quote: "You can disable thinking by setting thinkingBudget to 0. Setting the thinkingBudget to -1 turns on dynamic thinking" | type: official
- [C21] 思考摘要 part 带 thought:true | src: https://ai.google.dev/gemini-api/docs/generate-content/thinking | quote: "checking the thought boolean." | type: official
- [C22] Gemini 3 当前轮首个 functionCall 缺签名 | src: https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures | quote: "the request will fail with a 400 error." | type: official
- [C23] responseMimeType + responseSchema（已标 deprecated） | src: https://ai.google.dev/api/generate-content | quote: "Schemas must be a subset of the OpenAPI schema" | type: official
- [C24] 新 generationConfig.responseFormat.text{mimeType,schema} | src: https://ai.google.dev/api/generate-content | quote: "Only applicable when mimeType is APPLICATION_JSON." | type: official
- [C25] stopSequences, maxOutputTokens, topP, topK, seed, presencePenalty, frequencyPenalty；temperature | src: https://ai.google.dev/api/generate-content | quote: "Values can range from [0.0, 2.0]." | type: official
- [C26] Gemini 3 temperature | src: https://ai.google.dev/gemini-api/docs/gemini-3 | quote: "keeping the temperature parameter at its default value of 1.0." | type: official
- [C27] 流式每块是完整 GenerateContentResponse | src: https://ai.google.dev/api/generate-content | quote: "a stream of GenerateContentResponse instances." | type: official
- [C28] 响应：candidates[], promptFeedback, usageMetadata, modelVersion, responseId | src: https://ai.google.dev/api/generate-content | quote: "responseId is used to identify each response." | type: official
- [C29] finishReason 含 STOP, MAX_TOKENS, SAFETY, RECITATION, MALFORMED_FUNCTION_CALL, MISSING_THOUGHT_SIGNATURE 等 | src: https://ai.google.dev/api/generate-content | quote: "Request has at least one thought signature missing." | type: official
- [C30] blockReason：SAFETY, OTHER, BLOCKLIST, PROHIBITED_CONTENT, IMAGE_SAFETY | src: https://ai.google.dev/api/generate-content | quote: "the prompt was blocked and no candidates are returned." | type: official
- [C31] usageMetadata：promptTokenCount, cachedContentTokenCount, candidatesTokenCount, toolUsePromptTokenCount, thoughtsTokenCount, totalTokenCount | src: https://ai.google.dev/api/generate-content | quote: "(prompt + thoughts + response candidates)" | type: official
- [C32] 隐式缓存；门槛 3.x 4,096 / 2.5 2,048 | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "enabled by default for all Gemini 2.5 and newer models." | type: official
- [C33] 显式：POST v1beta/cachedContents，ttl 或 expireTime | src: https://ai.google.dev/gemini-api/docs/generate-content/caching | quote: "If not set, the TTL defaults to 1 hour." | type: official
- [C34] 错误体 {error:{code,message,status,details}}；429 RESOURCE_EXHAUSTED | src: https://ai.google.dev/gemini-api/docs/generate-content/api-errors | quote: "You've exceeded one of the API's rate limits" | type: official

## conflicts
- role：参考页 https://ai.google.dev/api/generate-content "Must be either 'user' or 'model'." vs 同页 "FunctionResponse with the Content.role "function""。
- candidateCount：参考页 "If unset, this will default to 1." vs https://ai.google.dev/gemini-api/docs/generate-content/latest-model "Remove candidate_count (unsupported in Gemini 3 and later)."
- temperature：参考页 "[0.0, 2.0]" vs https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/inference "(temperature, topP, and topK) aren't supported and are ignored if set"（3.6 Flash 起）。

## gaps
- SSE 结束标记、usageMetadata 所在 chunk 均未写明。
- 429 的 Retry-After/RetryInfo 未见原句。

## leads
- Interactions API：POST https://generativelanguage.googleapis.com/v1/interactions
- OpenAI 兼容：https://ai.google.dev/gemini-api/docs/openai
- Live API：https://ai.google.dev/api/live
