# r1-scout-forks
question: 除了 OpenAI、Anthropic、Google Gemini、DeepSeek、智谱、阿里云百炼、Moonshot 之外，还有哪些模型厂商官方提供了「另一套请求协议」或「对 Chat Completions / Messages / Responses / generateContent 的有损兼容」？只找值得单独加一行的。
checked: https://platform.minimax.cn/docs/api-reference/text-chat-anthropic, https://docs.x.ai/developers/rest-api-reference/inference, https://docs.x.ai/developers/model-capabilities/text/generate-text, https://docs.mistral.ai/api/endpoint/chat, https://docs.mistral.ai/studio/conversations/chat-completion, https://docs.mistral.ai/api/endpoint/beta/conversations, https://docs.mistral.ai/studio/agents/agents-api, https://docs.mistral.ai/llms.txt, https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html, https://docs.cohere.com/v2/reference/chat

## claims
- [C1] MiniMax Messages 兼容端点为 POST https://api.minimax.cn/anthropic/v1/messages（OpenAPI servers.url=https://api.minimax.cn；Bearer 或 header x-api-key）。页内无更新日期；OpenAPI info.version 1.0.0。 | src: https://platform.minimax.cn/docs/api-reference/text-chat-anthropic | quote: "使用 Anthropic API 兼容 Messages 格式调用 MiniMax 模型。" | type: official
- [C2] 该 Messages 面有损/扩展：tool_choice.type 仅 auto、none；role 枚举为 user、assistant、user_system、group、sample_message_user、sample_message_ai；请求内容块另有 video、mid_conv_system。 | src: https://platform.minimax.cn/docs/api-reference/text-chat-anthropic | quote: "工具选择策略。仅支持 auto 和 none。" | type: official
- [C3] xAI 推理基址 https://api.x.ai，同一参考页把 Responses 与 Chat Completions 都列在 Inference API 下。 | src: https://docs.x.ai/developers/rest-api-reference/inference | quote: "The xAI REST API is compatible with the OpenAI REST API." | type: official
- [C4] xAI 首选 POST https://api.x.ai/v1/responses，可传 previous_response_id；store 默认保存。同页另句：The Responses API is the preferred way of interacting with our models via API. | src: https://docs.x.ai/developers/model-capabilities/text/generate-text | quote: "The responses will be stored for 30 days, after which they will be removed." | type: official
- [C5] Mistral Chat Completions 示例打到 https://api.mistral.ai/v1/chat/completions，输入是 messages 列表。API 参考页标题为 POST /v1/chat/completions。 | src: https://docs.mistral.ai/studio/conversations/chat-completion | quote: "The Chat Completion API accepts a list of chat messages as input and generates a response." | type: official
- [C6] Mistral 另有 Beta Conversations：POST /v1/conversations，请求字段 inputs（union，含 string），再用 conversation_id 续写。H1 为 Beta Conversations Endpoints。 | src: https://docs.mistral.ai/api/endpoint/beta/conversations | quote: "Create a new conversation, using a base model or an agent and append entries." | type: official
- [C7] Bedrock 运行时分成四族：Invoke、Converse、OpenAI 的 ChatCompletions 与 Responses、以及 bedrock-mantle 上的 Anthropic Messages。 | src: https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html | quote: "Amazon Bedrock supports four families of runtime APIs, each designed for different integration patterns and use cases." | type: official
- [C8] Bedrock 的兼容按端点有损：同一模型在 bedrock-runtime 与 bedrock-mantle 上的 API 支持不必相同。页内未给出 Converse 的 REST 路径。 | src: https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html | quote: "For example, GPT OSS models support Chat Completions, Converse, and Invoke on `bedrock-runtime`, but the Responses API for those models is available only on `bedrock-mantle`." | type: official
- [C9] Cohere 原生 Chat 是 API v2：POST https://api.cohere.com/v2/chat。角色为 User、Assistant、Tool、System。响应字段是 id、finish_reason、message，不是 choices。finish_reason 允许 COMPLETE、STOP_SEQUENCE、MAX_TOKENS、TOOL_CALL、ERROR、TIMEOUT。 | src: https://docs.cohere.com/v2/reference/chat | quote: "Messages can be from `User`, `Assistant`, `Tool` and `System` roles." | type: official
- [C10] Cohere v2 另有原生 documents（同页还有 k、p、safety_mode、citation_options）。页内有 v1 到 v2 迁移指引，未见 OpenAI 兼容声明。 | src: https://docs.cohere.com/v2/reference/chat | quote: "A list of relevant documents that the model can cite to generate a more accurate reply." | type: official

## conflicts
- 无

## gaps
- Groq：4 次搜索未覆盖，未打开官方页。
- 百度千帆、阶跃星辰、腾讯混元：未搜、未开官方页。
- MiniMax 自有 /v1/text/chatcompletion_v2 与 OpenAI 兼容 /v1：只出现在搜索摘要，未打开该指南页。platform.minimaxi.com 会跨域跳到 platform.minimax.cn，已开页的 API host 只有 api.minimax.cn。
- Cohere 是否另有 OpenAI 兼容端点：已开页只有 POST /v2/chat。
- Mistral 侧栏有 OpenAI SDK compatibility，该节未打开。docs.mistral.ai/llms.txt 里的 .md 链接返回 404，未当来源。
- xAI Chat Completions 相对 OpenAI 的字段级差异：未打开 chat-completions 专页。总览列出 gRPC，未打开 grpc 参考。
- Bedrock Converse 的具体 URL 路径未在已开页出现。
- AI21 自有协议未开其官网；Bedrock 矩阵里 Jamba 仅图标显示 Invoke/Converse，图标无文字，不单列。

## leads
- MiniMax | messages | https://platform.minimax.cn/docs/api-reference/text-chat-anthropic | tool_choice 仅 auto/none，role 多 user_system、group、sample_message_user、sample_message_ai
- Mistral | 原生 conversations，另有 chat | https://docs.mistral.ai/api/endpoint/beta/conversations | 请求用 inputs 与 conversation_id，不是无状态重放 messages
- xAI | responses（兼 chat） | https://docs.x.ai/developers/model-capabilities/text/generate-text | previous_response_id，响应默认存 30 天；总览另列 gRPC
- Amazon Bedrock | 原生 Converse，兼 chat/responses/messages | https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html | bedrock-runtime 与 bedrock-mantle 支持集不一致，Responses 可只在 mantle
- Cohere | 原生 | https://docs.cohere.com/v2/reference/chat | POST /v2/chat 的 documents、p/k，finish_reason 为 COMPLETE/TOOL_CALL，响应无 choices
