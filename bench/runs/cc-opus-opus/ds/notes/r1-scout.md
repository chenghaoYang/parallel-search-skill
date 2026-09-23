# r1-scout
question: Scout——(1) 跨协议/跨厂商迁移最常踩的坑；(2) 网格未覆盖但用户应知道的实体、新协议、比较维度。
checked: https://ai.google.dev/{gemini-api/docs/interactions, api/interactions-api, gemini-api/docs/openai, gemini-api/docs/generate-content/thought-signatures, api/generate-content, gemini-api/docs/changelog}, https://developers.openai.com/api/{docs/guides/structured-outputs, docs/guides/reasoning, reference/resources/responses/methods/create, reference/resources/chat/subresources/completions/streaming-events}, https://platform.claude.com/docs/en/{cli-sdks-libraries/libraries/openai-sdk, api/messages, build-with-claude/{thinking, streaming, prompt-caching, mid-conversation-system-messages, claude-on-vertex-ai, claude-in-amazon-bedrock, claude-on-amazon-bedrock-legacy}}, https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html, https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle, https://openrouter.ai/docs/{api_reference/overview, api_reference/responses/overview, guides/best-practices/reasoning-tokens}, https://docs.litellm.ai/docs/{anthropic_unified/, response_api}, https://docs.vllm.ai/en/latest/serving/online_serving/, https://docs.sglang.io/{docs/basic_usage/anthropic_api, basic_usage/gpt_oss.html}, https://docs.ollama.com/api/{anthropic-compatibility, openai-compatibility}, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md, https://docs.x.ai/developers/rest-api-reference/inference/{legacy, responses}, https://docs.mistral.ai/{api/, capabilities/function_calling}

## claims
- [C1] Gemini generateContent 被官方称 legacy（Interactions 页，更新 2026-09-17） | src: https://ai.google.dev/gemini-api/docs/interactions | quote: "While it is now considered legacy, the original generateContent API remains fully supported." | type: official
- [C2] Gemini 3 漏回传 functionCall 的 thought_signature 即 400 | src: https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures | quote: "If you omit a thought_signature for the first functionCall part in any step of the current turn, the request will fail with a 400 error." | type: official
- [C3] 迁入别家模型的历史可填占位签名跳过校验 | src: https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures | quote: 「"context_engineering_is_the_way_to_go" or "skip_thought_signature_validator" in the thought signature field to skip validation」 | type: official
- [C4] Anthropic 工具轮须原样回传 thinking block | src: https://platform.claude.com/docs/en/build-with-claude/thinking | quote: "you must pass the thinking blocks from the assistant message back to the API, complete and unmodified." | type: official
- [C5] OpenAI Responses 的 reasoning item 带 encrypted_content 供回传 | src: https://developers.openai.com/api/docs/guides/reasoning | quote: "encrypted reasoning tokens that you can pass to future calls" | type: official
- [C6] Anthropic 的 OpenAI 兼容层忽略 strict | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "The `strict` parameter for function calling is ignored" | type: official
- [C7] 该兼容层不支持字段静默忽略（response_format、reasoning_effort、seed 标 Ignored） | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "Most unsupported fields are silently ignored rather than producing errors." | type: official
- [C8] 该兼容层把 system/developer 消息提升拼接到开头 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "System/developer messages are hoisted and concatenated to the beginning of the conversation" | type: official
- [C9] 该兼容层 temperature>1 截断为 1 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "Between 0 and 1 (inclusive). Values greater than 1 are capped at 1." | type: official
- [C10] Claude Opus 4.7+/Sonnet 5 等传非默认采样参数即 400 | src: https://platform.claude.com/docs/en/build-with-claude/thinking | quote: "non-default `temperature`, `top_p`, or `top_k` values return a 400 error on every request" | type: official
- [C11] Gemini 2026-07-21 弃用采样参数 | src: https://ai.google.dev/gemini-api/docs/changelog | quote: "The sampling parameters temperature, top_p and top_k are now deprecated." | type: official
- [C12] Anthropic tool_use.id / tool_use_id 字符集受限 | src: https://platform.claude.com/docs/en/api/messages | quote: "pattern: ^[a-zA-Z0-9_-]+$" | type: official
- [C13] Mistral 工具调用 id 须 9 位字母数字 | src: https://docs.vllm.ai/en/v0.10.2/api/vllm/entrypoints/openai/tool_parsers/mistral_tool_parser.html | quote: "Mistral Tool Call Ids must be alphanumeric with a length of 9." | type: secondary
- [C14] OpenAI strict 要求全部字段 required | src: https://developers.openai.com/api/docs/guides/structured-outputs | quote: "all fields or function parameters must be specified as `required`." | type: official
- [C15] OpenAI strict 要求 additionalProperties:false | src: https://developers.openai.com/api/docs/guides/structured-outputs | quote: "we require developers to set `additionalProperties: false` to opt into Structured Outputs." | type: official
- [C16] Gemini generateContent Schema 为 OpenAPI 3.0 子集 | src: https://ai.google.dev/api/generate-content | quote: "Represents a select subset of an OpenAPI 3.0 schema object." | type: official
- [C17] Anthropic 无 system 角色 | src: https://platform.claude.com/docs/en/api/messages | quote: 「there is no `"system"` role for input messages in the Messages API」 | type: official
- [C18] Anthropic 连续同角色会被合并 | src: https://platform.claude.com/docs/en/api/messages | quote: "Consecutive `user` or `assistant` turns in your request will be combined into a single turn." | type: official
- [C19] Anthropic 流式工具参数为 partial JSON，需拼接 | src: https://platform.claude.com/docs/en/build-with-claude/streaming | quote: "the deltas are partial JSON strings" | type: official
- [C20] Anthropic input_tokens 不含缓存部分 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "represents only the tokens that come after the last cache breakpoint" | type: official
- [C21] OpenAI cached_tokens 计在 prompt 内 | src: https://developers.openai.com/api/reference/resources/chat/subresources/completions/streaming-events | quote: "Cached tokens present in the prompt." | type: official
- [C22] xAI 的 Anthropic 兼容已弃用 | src: https://docs.x.ai/developers/rest-api-reference/inference/legacy | quote: "The Anthropic SDK compatibility is fully deprecated." | type: official

## conflicts
- Anthropic system 位置：C17 vs 「You append a `{"role": "system"}` message」（mid-conversation-system-messages 页；Sonnet 5 不支持）
- Mistral tool_choice：/api/ 列 "any"|"required"；function_calling 页只列 auto/any/none

## gaps
- OpenAI Chat 流式 data: [DONE]：现行参考未见原句（仅 OpenRouter 提及）
- Anthropic max_tokens 必填：参考未标 optional，无 "required" 原句
- 空 content 报错、finish_reason↔stop_reason 映射表、图片 URL/base64：无原句
- Mistral 9 位 id：官方页未写

## leads
- Gemini Interactions：2026-06 GA，POST /v1beta/interactions；store 默认 true，付费留存 55 天；2026-05 有 schema 破坏性变更 → 新协议，应入网格
- Gemini OpenAI 兼容：…/v1beta/openai/ 存在，beta；reasoning_effort 与 thinking_level 不能同用；签名在 tool_calls[].extra_content.google.thought_signature
- Anthropic OpenAI 兼容：https://api.anthropic.com/v1/，测试用非生产；n 须为 1；不返回思考
- Bedrock：legacy InvokeModel/Converse（anthropic_version "bedrock-2023-05-31"）；新 https://bedrock-mantle.{region}.api.aws/anthropic/v1/messages（原生形状+SSE）；另有 Claude Platform on AWS
- Vertex（页称 Agent Platform）：anthropic_version "vertex-2023-10-16" 在 body，model 在 URL
- Azure v1：…/openai/v1/，免 api-version，可调 DeepSeek/Grok
- OpenRouter：归一化 Chat 形状+native_finish_reason；统一 reasoning、reasoning_details 回传；Responses Beta 无状态；有 /api/v1/messages；SSE 含 comment 需忽略
- LiteLLM：/v1/messages、/responses（可桥接 /chat/completions）
- vLLM：/v1/responses、/v1/messages；SGLang：/v1/messages，Responses 仅见 GPT-OSS 页
- Ollama：/v1/messages（无 tool_choice）；/v1/responses（v0.13.3+，仅无状态）
- llama.cpp：/v1/responses、/v1/messages（工具需 --jinja），不保证兼容
- xAI：Responses 为主接口，存 30 天
- Mistral：random_seed（非 seed）、safe_prompt、prompt_mode
- 新维度：采样参数被拒/弃用[C10][C11]；托管状态留存期
