# r1-gemini-generatecontent
question: Gemini API generateContent 在 D1–D10 的官方规格；Vertex AI 同名接口端点/鉴权差异；Interactions API 是否存在。
checked: [GC]=ai.google.dev/api/generate-content, [FC]=ai.google.dev/gemini-api/docs/function-calling, [TH]=ai.google.dev/gemini-api/docs/thinking, [CACHE]=ai.google.dev/gemini-api/docs/caching, [APICACHE]=ai.google.dev/api/caching, [IOV]=ai.google.dev/gemini-api/docs/interactions-overview, [APIVER]=ai.google.dev/gemini-api/docs/api-versions, [VGC]=docs.cloud.google.com/vertex-ai/.../generateContent, [VINF]=docs.cloud.google.com/vertex-ai/.../model-reference/inference

## claims
- [C1] D1端点v1beta | src: https://ai.google.dev/api/generate-content | quote: "post https://generativelanguage.googleapis.com/v1beta/{model=models/*}:generateContent" | type: official
- [C2] D1鉴权query key参数 | src: https://ai.google.dev/api/generate-content | quote: "generateContent?key=$GEMINI_API_KEY" | type: official
- [C3] D1鉴权header(guide页示范,参考页本身未示范) | src: https://ai.google.dev/gemini-api/docs/function-calling | quote: "-H \"x-goog-api-key: $GEMINI_API_KEY \"" | type: official
- [C4] D1 v1=GA稳定版,v1beta=在研特性,SDK默认v1beta | src: https://ai.google.dev/gemini-api/docs/api-versions | quote: "v1: Stable version of the API. ... v1beta: ... early features and capabilities" | type: official
- [C5] D1 Vertex端点用{service-endpoint}占位符 | src: https://docs.cloud.google.com/vertex-ai/ (generateContent REST 参考，工人未给全路径) | quote: "post https://{service-endpoint}/v1/{model}:generateContent" | type: official
- [C6] D1 Vertex用OAuth,scope=cloud-platform | src: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference | quote: "scopes=[\"https://www.googleapis.com/auth/cloud-platform\"]" | type: official
- [C7] D2 role只能user/model | src: https://ai.google.dev/api/generate-content | quote: "Must be either 'user' or 'model'." | type: official
- [C8] D2 systemInstruction仅文本 | src: https://ai.google.dev/api/generate-content | quote: "Developer set system instruction(s). Currently, text only." | type: official
- [C9] D2 Part互斥类型:text/inlineData/functionCall/functionResponse/fileData/executableCode/codeExecutionResult;另有thought/thoughtSignature | src: https://ai.google.dev/api/generate-content | quote: "A Part can only contain one of the accepted types in Part.data." | type: official
- [C10] D3 cachedContent为可选请求字段,引用外部缓存资源 | src: https://ai.google.dev/api/generate-content | quote: "Format: cachedContents/{cachedContent}" | type: official
- [C11] D3 显式缓存POST /v1beta/cachedContents,ttl/expireTime互斥 | src: https://ai.google.dev/api/caching | quote: "A duration in seconds ... ending with 's'. Example: \"3.5s\"" | type: official
- [C12] D3 隐式缓存2.5+默认开,最小token:3.x系列4096/2.5系列2048 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models." | type: official
- [C13] D4顶层字段:candidates/promptFeedback/usageMetadata/modelVersion/responseId/modelStatus | src: https://ai.google.dev/api/generate-content | quote: "responseId is used to identify each response." | type: official
- [C14] D4 Candidate含citationMetadata(复述归因信息) | src: https://ai.google.dev/api/generate-content | quote: "Output only. Citation information for model-generated candidate." | type: official
- [C15] D4 blockReason枚举6项 | src: https://ai.google.dev/api/generate-content | quote: "BLOCK_REASON_UNSPECIFIED / SAFETY / OTHER / BLOCKLIST / PROHIBITED_CONTENT / IMAGE_SAFETY" | type: official
- [C16] D5 parameters用OpenAPI Schema,parametersJsonSchema与其互斥 | src: https://ai.google.dev/api/generate-content | quote: "This field is mutually exclusive with parameters." | type: official
- [C17] D5 mode枚举AUTO/ANY/NONE/VALIDATED默认AUTO;allowedFunctionNames仅ANY/VALIDATED时生效 | src: https://ai.google.dev/api/caching | quote: "This should only be set when the Mode is ANY or VALIDATED." | type: official
- [C18] D5 FunctionCall{id?,name,args}/FunctionResponse{id?,name,response,parts[]},id用于配对 | src: https://ai.google.dev/api/generate-content | quote: "return the response with the matching id" | type: official
- [C19] D5内置工具(页面现状):googleSearchRetrieval/codeExecution/googleSearch/computerUse/urlContext/fileSearch/mcpServers/googleMaps | src: https://ai.google.dev/api/generate-content | quote: "interacting directly with the computer" | type: official
- [C20] D6 thinkingConfig{includeThoughts,thinkingBudget,thinkingLevel} | src: https://ai.google.dev/api/generate-content | quote: "An error will be returned if this field is set for models that don't support thinking." | type: official
- [C21] D6 thinkingLevel 5枚举,推荐Gemini3+,老模型用会报错 | src: https://ai.google.dev/api/generate-content | quote: "Use with earlier models results in an error." | type: official
- [C22] D6 generateContent无独立thought block,签名挂在任意part上 | src: https://ai.google.dev/gemini-api/docs/thinking | quote: "signatures are metadata that can be attached to any part, such as living inside functionCall parts" | type: official
- [C23] D6 finishReason专设MISSING_THOUGHT_SIGNATURE | src: https://ai.google.dev/api/generate-content | quote: "Request has at least one thought signature missing." | type: official
- [C24] D7 responseSchema已deprecated,是OpenAPI子集 | src: https://ai.google.dev/api/generate-content | quote: "This item is deprecated! ... a subset of the OpenAPI schema" | type: official
- [C25] D7 responseJsonSchema与responseSchema互斥,需设responseMimeType | src: https://ai.google.dev/api/generate-content | quote: "responseSchema must be omitted, but responseMimeType is required" | type: official
- [C26] D7 responseMimeType支持text/plain(默认)/application/json/text/x.enum | src: https://ai.google.dev/api/generate-content | quote: "text/plain: (default) Text output. application/json: JSON response" | type: official
- [C27] D8流式端点streamGenerateContent | src: https://ai.google.dev/api/generate-content | quote: "post .../v1beta/{model=models/*}:streamGenerateContent" | type: official
- [C28] D8每个chunk是完整GenerateContentResponse(未见结束哨兵说明) | src: https://ai.google.dev/api/generate-content | quote: "the response body contains a stream of GenerateContentResponse instances" | type: official
- [C29] D9 temperature范围[0.0,2.0],均Optional | src: https://ai.google.dev/api/generate-content | quote: "Values can range from [0.0, 2.0]." | type: official
- [C30] D9 stopSequences最多5条 | src: https://ai.google.dev/api/generate-content | quote: "character sequences (up to 5) that will stop output generation" | type: official
- [C31] D9 logprobs范围[0,20] | src: https://ai.google.dev/api/generate-content | quote: "The number must be in the range of [0, 20]." | type: official
- [C32] D9 safetySettings每HarmCategory最多一条 | src: https://ai.google.dev/api/generate-content | quote: "not be more than one setting for each SafetyCategory type" | type: official
- [C33] D10 finishReason19项:STOP/MAX_TOKENS/SAFETY/RECITATION/LANGUAGE/OTHER/BLOCKLIST/PROHIBITED_CONTENT/SPII/MALFORMED_FUNCTION_CALL/IMAGE_SAFETY系列4项/NO_IMAGE/UNEXPECTED_TOOL_CALL/TOO_MANY_TOOL_CALLS/MISSING_THOUGHT_SIGNATURE/MALFORMED_RESPONSE/ESCALATION | src: https://ai.google.dev/api/generate-content | quote: "Natural stop point of the model or provided stop sequence." | type: official
- [C34] D10 usageMetadata含promptTokenCount/cachedContentTokenCount/candidatesTokenCount/toolUsePromptTokenCount/thoughtsTokenCount/totalTokenCount | src: https://ai.google.dev/api/generate-content | quote: "prompt + thoughts + response candidates" | type: official
- [C35] 附Interactions API存在,2026-06起GA,端点为/v1beta/interactions | src: https://ai.google.dev/gemini-api/docs/interactions-overview | quote: "As of June 2026, it is Generally Available and recommended for all new projects." | type: official
- [C36] 附状态字段previous_interaction_id,配合store=true/false控制留存 | src: https://ai.google.dev/gemini-api/docs/interactions-overview | quote: "using the previous_interaction_id parameter to continue the conversation" | type: official

## conflicts
- 同页矛盾:Content.role定义"Must be either 'user' or 'model'",但functionDeclarations说明写FunctionResponse应带"Content.role \"function\""。均见 [GC]。
- GA表述歧义:"it is Generally Available ... While it is now considered legacy, the original generateContent API remains fully supported."中"it"指代不清。src同C35。

## gaps
- thinkingBudget具体数值范围/每模型上限未给数字;thinking guide页当前示例是Interactions API的thinking_level非generateContent。
- 显式缓存(cachedContents)最小token门槛数字未找到(隐式缓存门槛已有,见C12)。
- 流式响应无专门结束哨兵字段的文字说明。

## leads
- function-calling/thinking/structured-output三个guide页默认示例是Interactions API风格,非generateContent,易被误认。
- cloud.google.com已301到docs.cloud.google.com,品牌显示"Gemini Enterprise Agent Platform",疑Vertex AI更名。
- Vertex的cachedContent是全路径"projects/{p}/locations/{l}/cachedContents/{id}",比Gemini API短格式多一层。
