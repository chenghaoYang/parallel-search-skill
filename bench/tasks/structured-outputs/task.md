产出文档 帮用户搞清楚各家大模型 API 的「保证 JSON / 结构化输出」能力有什么不同

seed keywords: OpenAI Structured Outputs (strict json_schema). Anthropic structured outputs / strict tool use. Gemini responseSchema / responseJsonSchema. DeepSeek JSON Output

some user aware variation: 听说 OpenAI 的 strict 模式是 100% 保证输出符合 schema、连 allOf 都支持——是真的吗？还有人说 Anthropic 到现在都没有正式的结构化输出、只能拿 tool use 硬凑；Gemini 的 responseSchema 是不是不支持 $ref、字段顺序还得靠 propertyOrdering 手写


起码先这 4 家，然后 xAI Grok、Mistral 这些 OpenAI 兼容 API 在结构化输出上有什么不同


以及其他用户需要知道的问题（流式下能不能用、和 function calling 的关系、字段顺序和必需字段各家怎么规定、哪些 JSON Schema 关键字各家不支持）


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长
