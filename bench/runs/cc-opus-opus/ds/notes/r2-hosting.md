# r2-hosting
question: 常见网关、自托管推理服务器、云托管各自暴露哪些协议面（OpenAI Chat Completions / OpenAI Responses / Anthropic Messages / 私有原生），以及每个实体最关键的 1–2 条协议差异？
checked: https://openrouter.ai/docs/api_reference/overview, https://openrouter.ai/docs/api_reference/responses/overview, https://openrouter.ai/docs/guides/best-practices/reasoning-tokens, https://openrouter.ai/docs/llms.txt, https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-a-message, https://docs.litellm.ai/docs/anthropic_unified/, https://docs.litellm.ai/docs/response_api, https://docs.litellm.ai/docs/reasoning_content, https://docs.vllm.ai/en/latest/serving/online_serving/, https://docs.ollama.com/api/anthropic-compatibility, https://docs.ollama.com/api/openai-compatibility, https://docs.sglang.io/docs/basic_usage/anthropic_api, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md, https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock, https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy, https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html, https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai, https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/use-claude, https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle

## claims
- [C1] OpenRouter Chat 端点统一成 OpenAI Chat 形状 | src: https://openrouter.ai/docs/api_reference/overview | quote: "OpenRouter normalizes the schema across models and providers to comply with the OpenAI Chat API." | type: official
- [C2] OpenRouter SSE 流含须忽略的 comment | src: https://openrouter.ai/docs/api_reference/overview | quote: "The SSE stream will occasionally contain a “comment” payload, which you should ignore" | type: official
- [C3] OpenRouter /api/v1/responses 仅无状态 | src: https://openrouter.ai/docs/api_reference/responses/overview | quote: "Requests that set store: true or a non-null previous_response_id are rejected with a 400 error." | type: official
- [C4] OpenRouter 有 Anthropic 格式 POST /api/v1/messages | src: https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-a-message | quote: "Creates a message using the Anthropic Messages API format." | type: official
- [C5] OpenRouter 统一 reasoning 参数（effort/max_tokens） | src: https://openrouter.ai/docs/guides/best-practices/reasoning-tokens | quote: "OpenRouter normalizes the different ways of customizing the amount of reasoning tokens that the model will use" | type: official
- [C6] LiteLLM /v1/messages 以 Anthropic 格式调所有 provider | src: https://docs.litellm.ai/docs/anthropic_unified/ | quote: "Use LiteLLM to call all your LLM APIs in the Anthropic v1/messages format." | type: official
- [C7] LiteLLM /responses 对非 Responses 模型桥接 /chat/completions | src: https://docs.litellm.ai/docs/response_api | quote: "LiteLLM allows you to call non-Responses API models via a bridge to LiteLLM's /chat/completions endpoint." | type: official
- [C8] LiteLLM 思考+工具须回传 thinking_blocks | src: https://docs.litellm.ai/docs/reasoning_content | quote: "you must include thinking_blocks from the previous assistant response when sending tool results back." | type: official
- [C9] vLLM 有 Responses 与 Messages（2026-09-16） | src: https://docs.vllm.ai/en/latest/serving/online_serving/ | quote: "Responses API (/v1/responses, /v1/responses/{response_id}, /v1/responses/{response_id}/cancel) … Anthropic messages API (/v1/messages, /v1/messages/count_tokens)" | type: official
- [C10] Ollama /v1/messages 有流式，tool_choice 不全 | src: https://docs.ollama.com/api/anthropic-compatibility | quote: "Compatible models support messages, streaming, and function calling. Tool-choice controls, deferred tools, and hosted web search are not fully supported." | type: official
- [C11] Ollama /v1/responses 自 v0.13.3，仅无状态 | src: https://docs.ollama.com/api/openai-compatibility | quote: "Added in Ollama v0.13.3 … Only the non-stateful flavor is supported" | type: official
- [C12] SGLang /v1/messages 有流式/工具/count_tokens | src: https://docs.sglang.io/docs/basic_usage/anthropic_api | quote: "supports both non-streaming and streaming responses, tool use, and a count_tokens route." | type: official
- [C13] llama.cpp /v1/responses 由转换成 Chat 请求实现 | src: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | quote: "This endpoint works by converting Responses request into Chat Completions request." | type: official
- [C14] llama.cpp /v1/messages 走 SSE，不承诺兼容 | src: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | quote: "Streaming is supported via Server-Sent Events. While no strong claims of compatibility with the Anthropic API spec are made" | type: official
- [C15] Bedrock 新端点：Messages 形状+SSE（Opus 4.7+） | src: https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock | quote: "The endpoint follows the pattern https://bedrock-mantle.{region}.api.aws/anthropic/v1/messages. Unlike the InvokeModel-based integration, this endpoint uses standard SSE streaming and the same request body shape as Anthropic's first-party API." | type: official
- [C16] Bedrock 旧集成：event-stream（≤Opus 4.6） | src: https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy | quote: "the InvokeModel and Converse APIs with ARN-versioned model identifiers and AWS event-stream encoding" | type: official
- [C17] Bedrock InvokeModel body 版本字段 | src: https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy | quote: ""anthropic_version": "bedrock-2023-05-31"," | type: official
- [C18] Vertex：model 在 URL，anthropic_version 放 body | src: https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai | quote: "model is not passed in the request body. Instead, it is specified in the Google Cloud endpoint URL. … anthropic_version is passed in the request body (rather than as a header), and must be set to the value vertex-2023-10-16." | type: official
- [C19] Vertex 流式用 :streamRawPredict（2026-09-22） | src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/use-claude | quote: "publishers/anthropic/models/MODEL:streamRawPredict" | type: official
- [C20] Azure v1 免 api-version（2026-05-13） | src: https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle | quote: "append /openai/v1 to the endpoint address. api-version is no longer a required parameter with the v1 GA API." | type: official

## conflicts
- Ollama 同页：事件表勾 "[x] `error`"，Not supported 表列 "Server-sent errors | `error` events during streaming"。https://docs.ollama.com/api/anthropic-compatibility

## gaps
- D11 缺：vLLM、LiteLLM、Azure。
- OpenRouter Responses 未见 Beta；llms.txt："Beta.Responses … Deprecated alias of responses"。

## leads
- 有原句未列：OpenRouter native_finish_reason；SGLang 缺 --tool-call-parser 则工具调用回纯文本；Converse 归一信封；Bedrock 新端点 x-api-key/SigV4。
- llama.cpp 工具需 --jinja（现默认开启）；Azure 推荐 Responses。
