# r1-scout
question: 网格漏了哪些实体/维度？跨协议跨厂商接入最常踩的坑有哪些？
checked: openresponses.org/specification, x.com/OpenAIDevs/status/2011862984595795974, ai.google.dev/gemini-api/docs/changelog, ai.google.dev/gemini-api/docs/interactions, ai.google.dev/gemini-api/docs/thinking, platform.minimax.io/docs/api-reference/text-anthropic-api, docs.volcengine.com/docs/ark/integrate-third-party-tools, docs.x.ai/developers/rest-api-reference/inference/legacy, openrouter.ai/docs/api_reference/responses/overview, docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/, lmsysorg.mintlify.app/docs/basic_usage/anthropic_api, docs.ollama.com/api/openai-compatibility, github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md, docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html, learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle, docs.mistral.ai/api/endpoint/chat, docs.cohere.com/changelog/v2-api-release, platform.claude.com/docs/en/build-with-claude/extended-thinking, platform.claude.com/docs/en/build-with-claude/prompt-caching, developers.openai.com/api/docs/guides/function-calling, developers.openai.com/api/docs/guides/migrate-to-responses, developers.openai.com/api/docs/changelog

## claims
- [C1] Open Responses=基于Responses API的开源多厂商规范 | src: https://openresponses.org/specification | quote: "open-source specification...multi-provider, interoperable LLM interfaces based on the OpenAI Responses API" | type: official
- [C2] OpenAI官方宣布Open Responses发布 | src: https://x.com/OpenAIDevs/status/2011862984595795974 | quote: "announcing Open Responses: an open-source spec for building multi-provider, interoperable LLM interfaces" | type: official
- [C3] Gemini Interactions API 2025-12-11上线 | src: https://ai.google.dev/gemini-api/docs/changelog | quote: "Launched the Interactions API. This API provides a unified interface for interacting with Gemini models and agents." | type: official
- [C4] Interactions API已GA(2026-06)推荐新项目,generateContent降legacy仍全支持 | src: https://ai.google.dev/gemini-api/docs/interactions | quote: "recommended for all new projects"; "generateContent API remains fully supported" | type: official
- [C5] MiniMax Anthropic兼容base URL,M2.x thinking不可关闭 | src: https://platform.minimax.io/.../text-anthropic-api | quote: "https://api.minimax.io/anthropic"; "Thinking cannot be disabled for M2.x models" | type: official
- [C6] Ark双协议各自base URL(更新2026-09-13) | src: https://docs.volcengine.com/.../integrate-third-party-tools | quote: "兼容OpenAI接口协议"/api/v3;"兼容Anthropic接口协议"/api/compatible | type: official
- [C7] xAI Anthropic SDK兼容层已完全弃用 | src: https://docs.x.ai/.../inference/legacy | quote: "Anthropic SDK compatibility is fully deprecated. Please migrate to the Responses API or gRPC" | type: official
- [C8] OpenRouter Responses无状态,拒绝store/previous_response_id | src: https://openrouter.ai/docs/api_reference/responses/overview | quote: "stateless...store: true or a non-null previous_response_id are rejected with a 400 error" | type: official
- [C10] vLLM同时支持Chat/Responses/Anthropic Messages | src: https://docs.vllm.ai/.../openai_compatible_server/ | quote: "support...Chat Completions, Responses, Embeddings API" | type: official
- [C11] SGLang /v1/messages base_url为根路径无/v1后缀 | src: https://lmsysorg.mintlify.app/.../anthropic_api | quote: "base_url is the server root without a /v1 suffix" | type: official
- [C12] Ollama Responses v0.13.3加入,仅无状态版 | src: https://docs.ollama.com/api/openai-compatibility | quote: "Added in Ollama v0.13.3"; "Only the non-stateful flavor is supported" | type: official
- [C13] llama.cpp已支持/v1/messages与/v1/responses | src: https://github.com/.../server/README.md | quote: "Anthropic Messages API compatible"; "POST /v1/responses: OpenAI-compatible Responses API" | type: official
- [C14] Bedrock的Anthropic兼容Messages端点跑在独立bedrock-mantle网关 | src: https://docs.aws.amazon.com/.../api-compatibility.html | quote: "Messages...implements the Anthropic Messages interface on the bedrock-mantle endpoint" | type: official
- [C15] Azure v1自2025-08起不再需api-version | src: https://learn.microsoft.com/.../api-version-lifecycle | quote: "Starting in August 2025...api-version is no longer a required parameter with the v1 GA API" | type: official
- [C16] Mistral独有safe_prompt字段 | src: https://docs.mistral.ai/api/endpoint/chat | quote: "inject a safety prompt before all conversations" | type: official
- [C17] Cohere v2:messages合并历史,model变必填 | src: https://docs.cohere.com/changelog/v2-api-release | quote: "chat history are combined in a single messages array" | type: official
坑：
- [C18]（原P1） Anthropic thinking:enabled在4.7+模型直接400,需转adaptive | src: https://platform.claude.com/.../extended-thinking | quote: "Claude 4.7 and later models do not support it...returning a 400 error" | type: official
- [C19]（原P2） Anthropic cache token不计入input_tokens,需相加 | src: https://platform.claude.com/.../prompt-caching | quote: "total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens" | type: official
- [C20]（原P3） Gemini thought签名无状态模式须原样回传 | src: https://ai.google.dev/gemini-api/docs/thinking | quote: "MUST always resend all thought blocks exactly as they were received...NOT remove or modify" | type: official
- [C21]（原P4） OpenAI流式tool call参数以delta事件分片需拼接 | src: https://developers.openai.com/.../function-calling | quote: "response.function_call_arguments.delta which will contain the delta of the arguments field" | type: official
- [C22]（原P5） Responses用text.format取代Chat的response_format | src: https://developers.openai.com/.../migrate-to-responses | quote: "Instead of response_format, use text.format in Responses" | type: official
- [C23]（原P6） developer角色为o1而生,但o1-preview/mini不支持system/developer | src: https://developers.openai.com/api/docs/changelog | quote: "o1-preview and o1-mini do not support system or developer messages" | type: official
- [C24]（原P7） Azure:o1系列须用max_completion_tokens,max_tokens不生效 | src: https://learn.microsoft.com/.../api-version-lifecycle | quote: "max_completion_tokens added to support o1-preview and o1-mini models. max_tokens doesn't work with the o1 series" | type: official
- [C25]（原P8） vLLM --api-key不保护/invocations等非/v1端点 | src: https://docs.vllm.ai/.../openai_compatible_server/ | quote: "not authenticated — most notably /invocations" | type: official
- [C26]（原P9） SGLang未配tool-call-parser时工具调用静默退化为原始文本 | src: https://lmsysorg.mintlify.app/.../anthropic_api | quote: "tool calls come back as raw text, and Claude Code cannot execute them" | type: official
## conflicts
- Ark Chat Completions base URL不一致:通用文档api/v3(docs.volcengine.com/docs/ark/integrate-third-party-tools) vs ZCode专用页api/coding/v3(docs.volcengine.com/docs/82379/2628972),未知是否不同网关。
- llama.cpp /v1/responses支持时间差:issue#19138仍在讨论加入,当前README已写"支持",版本未核实。

## gaps
- DeepSeek reasoning_content多轮回传报错原句未取得(guides/reasoning_model页现为quick-start内容)。
- OpenAI strict JSON Schema不支持关键字完整清单被截断未取得。
- xAI chat/completions与responses完整路径拼接未见逐字原句。
- Mistral tool_choice枚举("any"/"required")差异只有二手转述。

## leads
- Gemini Interactions API是重大缺口:2025-12上线/2026-06 GA/官方推荐新项目,generateContent降legacy,建议R2起一格深挖schema。URL: ai.google.dev/gemini-api/docs/interactions
- Bedrock Messages(Anthropic兼容)按模型版本单独开关非整个Claude家族统一支持,建议逐模型核实矩阵表。URL: docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html
- 安全提醒:域名minimax-ai.chat自称MiniMax文档站,与官方platform.minimax.io不符,疑似非官方镜像,勿引用。
- OpenRouter与Ollama的Responses都是阉割无状态版,建议单开"兼容层Responses是否真托管状态"维度。
