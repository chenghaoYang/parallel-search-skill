# r1-google-gencontent
question: Google Gemini API 官方 generateContent / streamGenerateContent 的请求与响应协议长什么样？
checked: https://ai.google.dev/api/generate-content, https://ai.google.dev/api, https://ai.google.dev/api/all-methods, https://ai.google.dev/gemini-api/docs/openai, https://ai.google.dev/gemini-api/docs/function-calling, https://ai.google.dev/gemini-api/docs/generate-content/text-generation

## claims
- [C1] D1 POST 路径见 quote；model=models/*。reference 2026-09-22 UTC。 | src: https://ai.google.dev/api/generate-content | quote: "post https://generativelanguage.googleapis.com/v1beta/{model=models/*}:generateContent" | type: official
- [C2] D1 base https://generativelanguage.googleapis.com。all-methods 2026-09-22 UTC。 | src: https://ai.google.dev/api/all-methods | quote: "https://generativelanguage.googleapis.com" | type: official
- [C3] D7 流式是独立 POST streamGenerateContent，不是 body 开关。 | src: https://ai.google.dev/api/generate-content | quote: "post https://generativelanguage.googleapis.com/v1beta/{model=models/*}:streamGenerateContent" | type: official
- [C4] D1 总览：必须带 header x-goog-api-key。2026-09-04 UTC。 | src: https://ai.google.dev/api | quote: "All requests to the Gemini API must include a x-goog-api-key header with your API key." | type: official
- [C5] D1 reference shell 用 query `key`。 | src: https://ai.google.dev/api/generate-content | quote: "generateContent?key=$GEMINI_API_KEY" | type: official
- [C6] D2 多轮 contents 含历史和最新请求（客户端放进同一请求）。 | src: https://ai.google.dev/api/generate-content | quote: "this is a repeated field that contains the conversation history and the latest request." | type: official
- [C7] D2 SDK chat 每轮把全量历史发给 generateContent。 | src: https://ai.google.dev/gemini-api/docs/generate-content/text-generation | quote: "the full conversation history is sent to the model with each follow-up turn." | type: official
- [C8] D3 role 只能 user 或 model。 | src: https://ai.google.dev/api/generate-content | quote: "Must be either 'user' or 'model'." | type: official
- [C9] D3 parts 互斥：text、inlineData、functionCall、functionResponse、fileData、executableCode、codeExecutionResult、toolCall、toolResponse；另有 thought、thoughtSignature。inlineData={mimeType, base64 data}。 | src: https://ai.google.dev/api/generate-content | quote: "At most one of the fields will be set in a response" | type: official
- [C10] D4 systemInstruction 与 contents 同级，类型 Content，仅文本。 | src: https://ai.google.dev/api/generate-content | quote: "Currently, text only." | type: official
- [C11] D5 tools[].functionDeclarations；模型不执行函数。 | src: https://ai.google.dev/api/generate-content | quote: "The model or system does not execute the function." | type: official
- [C12] D5 下一轮 FunctionResponse；reference 写 role "function"。 | src: https://ai.google.dev/api/generate-content | quote: "Content.role \"function\" generation context for the next model turn." | type: official
- [C13] D5 FunctionResponse.response 必填 JSON；FunctionCall 字段 id、name、args。 | src: https://ai.google.dev/api/generate-content | quote: "Required. The function response in JSON object format." | type: official
- [C14] D6 generationConfig 含 maxOutputTokens、temperature、topP。 | src: https://ai.google.dev/api/generate-content | quote: "\"maxOutputTokens\": integer, \"temperature\": number, \"topP\": number" | type: official
- [C15] D6 thinkingConfig：includeThoughts、thinkingBudget、thinkingLevel。 | src: https://ai.google.dev/api/generate-content | quote: "The number of thoughts tokens that the model should generate." | type: official
- [C16] D6 ThinkingLevel：THINKING_LEVEL_UNSPECIFIED、MINIMAL、LOW、MEDIUM、HIGH。Gemini 3+；更早模型 error。 | src: https://ai.google.dev/api/generate-content | quote: "Recommended for Gemini 3 or later models. Use with earlier models results in an error." | type: official
- [C17] D7 成功 body 是一串 GenerateContentResponse。 | src: https://ai.google.dev/api/generate-content | quote: "a stream of GenerateContentResponse instances." | type: official
- [C18] D7 总览称 SSE。 | src: https://ai.google.dev/api | quote: "Uses Server-Sent Events (SSE) to push chunks of the response to you as they are generated." | type: official
- [C19] D7 指南在该方法加 alt=sse。 | src: https://ai.google.dev/gemini-api/docs/generate-content/text-generation | quote: "streamGenerateContent?alt=sse" | type: official
- [C20] D8 candidates[].content 为 Content。 | src: https://ai.google.dev/api/generate-content | quote: "Output only. Generated content returned from the model." | type: official
- [C21] D8 finishReason 枚举：FINISH_REASON_UNSPECIFIED, STOP, MAX_TOKENS, SAFETY, RECITATION, LANGUAGE, OTHER, BLOCKLIST, PROHIBITED_CONTENT, SPII, MALFORMED_FUNCTION_CALL, IMAGE_SAFETY, IMAGE_PROHIBITED_CONTENT, IMAGE_OTHER, NO_IMAGE, IMAGE_RECITATION, UNEXPECTED_TOOL_CALL, TOO_MANY_TOOL_CALLS, MISSING_THOUGHT_SIGNATURE, MALFORMED_RESPONSE, ESCALATION。 | src: https://ai.google.dev/api/generate-content | quote: "Defines the reason why the model stopped generating tokens." | type: official
- [C22] D8 usageMetadata 字段见 quote；另有 *TokensDetails、serviceTier。 | src: https://ai.google.dev/api/generate-content | quote: "\"promptTokenCount\": integer, \"cachedContentTokenCount\": integer, \"candidatesTokenCount\": integer, \"toolUsePromptTokenCount\": integer, \"thoughtsTokenCount\": integer, \"totalTokenCount\": integer" | type: official
- [C23] D9 responseMimeType 未标废弃，取值见 quote。 | src: https://ai.google.dev/api/generate-content | quote: "`text/plain`: (default) Text output. `application/json`: JSON response in the response candidates. `text/x.enum`: ENUM as a string response" | type: official
- [C24] D9 responseSchema 标 deprecated，且要兼容的 responseMimeType。同页 shell 仍发 response_schema。 | src: https://ai.google.dev/api/generate-content | quote: "This item is deprecated!" | type: official
- [C25] D9 _responseJsonSchema 标 deprecated，但是 JSON Schema 替代。 | src: https://ai.google.dev/api/generate-content | quote: "This is an alternative to `responseSchema` that accepts [JSON Schema](https://json-schema.org/)." | type: official
- [C26] D9 responseJsonSchema 说明自指为内部字段；JSON 表示三字段都在。 | src: https://ai.google.dev/api/generate-content | quote: "Optional. An internal detail. Use `responseJsonSchema` rather than this field." | type: official
- [C27] D10 兼容页 2026-09-02 UTC：两套协议，未用 OpenAI 库应直接调 Gemini API。 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "If you aren't already using the OpenAI libraries, we recommend that you call the Gemini API directly." | type: official
- [C28] D10 POST /v1beta/openai/chat/completions，Authorization Bearer，body 用 messages。 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions" | type: official
- [C29] D10 兼容流式是 body "stream": true，不是 :streamGenerateContent。 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "\"stream\": true" | type: official
- [C30] D10 图片未列参数会静默忽略（支持 prompt、model、n、size、response_format）。 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Any other parameters not listed here or in the extra_body section will be silently ignored by the compatibility layer." | type: official

## conflicts
- 鉴权：https://ai.google.dev/api（2026-09-04）"must include a x-goog-api-key header" vs generate-content（2026-09-22）"generateContent?key=$GEMINI_API_KEY"。
- role： "Must be either 'user' or 'model'." vs "Content.role \"function\"" vs function-calling 指南 "Role: genai.RoleUser"。
- D9：responseSchema "This item is deprecated!"，shell 仍 "response_schema"；_responseJsonSchema 废弃但 "accepts JSON Schema"；responseJsonSchema "Use responseJsonSchema rather than this field." 未裁决。
- 大小写：JSON 为 responseMimeType；shell 为 response_mime_type、system_instruction。

## gaps
- 无原句说明省略 alt=sse 是否 JSON 数组，也无 data: 行格式。
- 无 chat.completions 总禁用字段表；ignore 句只覆盖图片参数。
- 文本指南无日期。未核 v1 是否与 v1beta 并列。

## leads
- Interactions 为 Recommended（previous_interaction_id）。结构化输出（2026-09-17）用 response_format.schema。Bidi 不支持 responseMimeType/responseSchema/responseJsonSchema。Vertex未查。
