# r1-google-gc
question: Google Gemini API 的 generateContent / streamGenerateContent（REST）官方规范中，请求协议各维度的事实是什么？
checked: https://ai.google.dev/api/generate-content, https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/function-calling, https://ai.google.dev/gemini-api/docs/thinking, https://ai.google.dev/gemini-api/docs/openai, https://ai.google.dev/gemini-api/docs/models
page-state: 参考页示例模型 gemini-3.8-flash（2026-09 现行）；caching 页更新于 2026-09-02 UTC

## claims
- [C1] D1 generateContent=POST https://generativelanguage.googleapis.com/v1beta/{model=models/*}:generateContent，model 格式 models/{model} | src: https://ai.google.dev/api/generate-content | quote: "Required. The name of the Model to use for generating the completion. Format: models/{model}." | type: official
- [C2] D1 streamGenerateContent=POST https://generativelanguage.googleapis.com/v1beta/{model=models/*}:streamGenerateContent | src: https://ai.google.dev/api/generate-content | quote: "Generates a streamed response from the model given an input GenerateContentRequest." | type: official
- [C3] D1 顶层字段：contents[] 必填 + tools[]/toolConfig/safetySettings[]/systemInstruction/generationConfig/cachedContent/serviceTier/store（无 labels） | src: https://ai.google.dev/api/generate-content | quote: "Required. The content of the current conversation with the model." | type: official
- [C4] D1 systemInstruction 顶层 Content，仅文本 | src: https://ai.google.dev/api/generate-content | quote: "Optional. Developer set system instruction(s). Currently, text only." | type: official
- [C5] D2 role 仅 user|model，无 assistant | src: https://ai.google.dev/api/generate-content | quote: "Optional. The producer of the content. Must be either 'user' or 'model'." | type: official
- [C6] D2 Part.data 互斥：text/inlineData/fileData/functionCall/functionResponse（另有 executableCode/codeExecutionResult/toolCall/toolResponse/videoMetadata）；无字符串简写 | src: https://ai.google.dev/api/generate-content | quote: "A Part can only contain one of the accepted types in Part.data." | type: official
- [C7] D9 Part 带 thought 布尔与 thoughtSignature（base64，可回传复用） | src: https://ai.google.dev/api/generate-content | quote: "Optional. An opaque signature for the thought so it can be reused in subsequent requests." | type: official
- [C8] D3 Tool.functionDeclarations；Tool 另含 googleSearch/codeExecution/computerUse/urlContext/fileSearch/mcpServers/googleMaps | src: https://ai.google.dev/api/generate-content | quote: "Optional. A list of FunctionDeclarations available to the model that can be used for function calling." | type: official
- [C9] D3 参数可用 parametersJsonSchema（JSON Schema），与 parameters（OpenAPI Schema）互斥 | src: https://ai.google.dev/api/generate-content | quote: "Optional. Describes the parameters to the function in JSON Schema format." | type: official
- [C10] D3 FunctionCall={id?,name,args}，现支持 tool call id | src: https://ai.google.dev/api/generate-content | quote: "Optional. Unique identifier of the function call. If populated, the client to execute the functionCall and return the response with the matching id." | type: official
- [C11] D3 FunctionResponse={id?,name,response(JSON对象)}，键名自定 | src: https://ai.google.dev/api/generate-content | quote: "Callers can use any keys of their choice that fit the function's syntax to return the function output, e.g. \"output\", \"result\", etc." | type: official
- [C12] D4 请求带 cachedContent 引用显式缓存 | src: https://ai.google.dev/api/generate-content | quote: "Optional. The name of the content cached to use as context to serve the prediction. Format: cachedContents/{cachedContent}" | type: official
- [C13] D4 implicit caching 默认开启；最小 token：3.x Flash 4096、2.5 Flash 2048 | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Implicit caching is enabled by default for all Gemini 2.5 and newer models." | type: official
- [C14] D4 显式缓存走 generateContent | src: https://ai.google.dev/gemini-api/docs/caching | quote: "Explicit caching (manually creating and managing cache objects) is not supported in the Interactions API. To use explicit caching, switch to the generateContent API." | type: official
- [C15] D5+D6 官方 curl 示例：:streamGenerateContent?alt=sse，key 经 ?key= 查询参数 | src: https://ai.google.dev/api/generate-content | quote: "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:streamGenerateContent?alt=sse&key=" | type: official
- [C16] D5 响应体（含流式各 chunk）为 GenerateContentResponse | src: https://ai.google.dev/api/generate-content | quote: "If successful, the response body contains an instance of GenerateContentResponse." | type: official
- [C17] D7 stopSequences≤5；temperature∈[0.0,2.0]；seed、candidateCount（默认 1）存在 | src: https://ai.google.dev/api/generate-content | quote: "Optional. The set of character sequences (up to 5) that will stop output generation." | type: official
- [C18] D8 responseMimeType：text/plain、application/json、text/x.enum；responseModalities 空=仅文本 | src: https://ai.google.dev/api/generate-content | quote: "application/json: JSON response in the response candidates. text/x.enum: ENUM as a string response in the response candidates." | type: official
- [C19] D8 responseSchema 为 OpenAPI 子集且已标 (deprecated)；_responseJsonSchema（JSON Schema）亦标 deprecated | src: https://ai.google.dev/api/generate-content | quote: "Schemas must be a subset of the OpenAPI schema and can be objects, primitives or arrays." | type: official
- [C20] D9 ThinkingConfig 含 includeThoughts/thinkingBudget/新 thinkingLevel（Gemini 3+），不支持思考的模型报错 | src: https://ai.google.dev/api/generate-content | quote: "Recommended for Gemini 3 or later models. Use with earlier models results in an error." | type: official
- [C21] D9 includeThoughts 开关 thought 返回 | src: https://ai.google.dev/api/generate-content | quote: "Indicates whether to include thoughts in the response. If true, thoughts are returned only when available." | type: official
- [C22] D10 inlineData 内联字节、fileData 为 URI 引用 | src: https://ai.google.dev/api/generate-content | quote: "URI based data." | type: official
- [C23] 附-OpenAI 兼容：官方支持 OpenAI 库/REST 访问 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Gemini models are accessible using the OpenAI libraries (Python and TypeScript / Javascript) along with the REST API, by updating three lines of code and using your Gemini API key." | type: official
- [C24] 附-OpenAI 兼容 base_url=https://generativelanguage.googleapis.com/v1beta/openai/，鉴权 Authorization: Bearer | src: https://ai.google.dev/gemini-api/docs/openai | quote: "base_url=\"https://generativelanguage.googleapis.com/v1beta/openai/\"" | type: official
- [C25] 附-OpenAI 兼容：reasoning_effort 与 Gemini reasoning 配置有映射 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Different Gemini models have different reasoning configurations, you can see how they map to OpenAI's reasoning efforts as follows:" | type: official

## conflicts
- 参考页把 responseSchema 与 _responseJsonSchema 都标 "This item is deprecated!" 且未指明替代；与简报"responseSchema 现行"预期冲突，疑因 Interactions API 迁移。
- 简报预期顶层 labels；当前 GenerateContentRequest 字段表无 labels，全页 grep 无该词，疑已移除/移入 Interactions API。
- function-calling 指南 REST 示例已改打 v1beta/interactions，而 generateContent 的 tools/toolConfig 仍在 REST reference——两 API 并行期。

## gaps
- x-goog-api-key header、OAuth scope 官方原句未取到（api-key 页下载失败），仅 ?key= 有证（C15）。
- D5 SSE 终止方式/有无 [DONE]：reference 无原句。FunctionCallingConfigMode 枚举值仅见注释 "FunctionCallingConfigMode.ANY"。
- countTokens/cachedContents 端点、v1 vs v1beta 政策、Vertex aiplatform 差异、Blob{mimeType,data} 原句、functionResponse 回传轮 role、FunctionCall.id 适用范围：页未开或 404（/api/streaming 404）。

## leads
- 新 Interactions API（POST https://generativelanguage.googleapis.com/v1beta/interactions）：thinking/function-calling/caching 指南已围绕其重写，另有 "Interactions breaking changes (May 2026)" 页。
- Part 新增 server-side toolCall/toolResponse、mediaResolution/mediaProcessing；FunctionResponse 支持 parts[]（多模态回传）与 willContinue。
- OpenAI 兼容文档还覆盖 Batch API（OpenAI JSONL）、webhooks、flex/priority inference。
