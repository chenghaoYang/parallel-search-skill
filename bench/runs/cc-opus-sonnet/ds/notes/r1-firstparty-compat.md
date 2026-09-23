# r1-firstparty-compat
question: Anthropic「OpenAI SDK 兼容」与 Google「Gemini OpenAI 兼容」各自支持/忽略/不支持哪些 OpenAI 字段，官方定位是什么？
checked: https://platform.claude.com/docs/en/api/openai-sdk, https://ai.google.dev/gemini-api/docs/openai, https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate/openai/overview, https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start/openai

## claims
- [C1] base URL 为 https://api.anthropic.com/v1/ | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "base_url=\"https://api.anthropic.com/v1/\"" | type: official
- [C2] 官方定位：主要供测试/对比模型能力，非长期/生产方案 | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "not considered a long-term or production-ready solution for most use cases" | type: official
- [C3] 全部特性(PDF/citations/thinking/caching)须用原生API | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "use the native Claude API" | type: official
- [C4] tools.strict 被忽略，不保证 JSON 严格符合 schema | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "The strict parameter for function calling is ignored" | type: official
- [C5] audio 输入不支持，被忽略并从输入剥离 | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "Audio input is not supported; it will be ignored and stripped from input" | type: official
- [C6] Prompt caching 兼容层不支持，Anthropic 原生 SDK 支持 | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "Prompt caching is not supported, but it is supported in the Anthropic SDKs" | type: official
- [C7] system/developer 消息被提升，用单个换行拼成开头唯一 system 消息 | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "concatenates them together with a single newline (\n) in between them" | type: official
- [C8] 扩展思考经 extra_body 的 thinking 参数开启，非 reasoning_effort | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "extra_body={\"thinking\": {\"type\": \"enabled\", \"budget_tokens\": 2000}}" | type: official
- [C9] Claude 5 系列 thinking 默认开启，手动配置为遗留模式 | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "on Claude 5 models it is on by default; manually configured extended thinking is a legacy mode" | type: official
- [C10] temperature 取 0–1(含)，大于 1 截断为 1 | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "Between 0 and 1 (inclusive). Values greater than 1 are capped at 1." | type: official
- [C11] n 必须恰好为 1 | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "n | Must be exactly 1" | type: official
- [C12] logprobs、top_logprobs、reasoning_effort 均 Ignored | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "reasoning_effort | Ignored" | type: official
- [C13] response_format 被忽略，JSON 输出应改用原生 Structured Outputs | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "Ignored. For JSON output, use Structured Outputs with the native Claude API" | type: official
- [C14] parallel_tool_calls、stream_options 均 Fully supported | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "parallel_tool_calls | Fully supported" | type: official
- [C15] presence_penalty/frequency_penalty/seed/service_tier/metadata/prediction/logit_bias/store/user/modalities 均 Ignored | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "seed | Ignored" | type: official
- [C16] choices[]长度恒为1；usage细分/refusal/audio/logprobs/service_tier/system_fingerprint 恒空 | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "Will always have a length of 1" | type: official
- [C17] 错误格式与 OpenAI 一致但细节不等价，仅供日志/调试 | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "Only use the error messages for logging and debugging." | type: official
- [C18] 速率限制沿用 /v1/messages 标准限制 | src: https://platform.claude.com/docs/en/api/openai-sdk | quote: "Rate limits follow Anthropic's standard limits for the /v1/messages endpoint." | type: official

- [C19] base URL 为 https://generativelanguage.googleapis.com/v1beta/openai/ | src: https://ai.google.dev/gemini-api/docs/openai | quote: "base_url=\"https://generativelanguage.googleapis.com/v1beta/openai/\"" | type: official
- [C20] 未用 OpenAI 库者官方建议直接用原生 Gemini API | src: https://ai.google.dev/gemini-api/docs/openai | quote: "we recommend that you call the Gemini API directly" | type: official
- [C21] 现状：OpenAI 库支持仍 beta（页面 Last updated 2026-09-02 UTC） | src: https://ai.google.dev/gemini-api/docs/openai | quote: "still in beta while we extend feature support" | type: official
- [C22] reasoning_effort 按模型分列映射 thinking_level/thinking_budget，medium 档示例 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "medium | medium | medium | medium | 8,192" | type: official
- [C23] 仅 2.5 系列可设"none"关闭思考，2.5 Pro/3 系列不可关闭 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Reasoning cannot be turned off for Gemini 2.5 Pro or 3 models." | type: official
- [C24] extra_body.google.thinking_config 含 thinking_level、include_thoughts | src: https://ai.google.dev/gemini-api/docs/openai | quote: "\"thinking_level\": \"low\", \"include_thoughts\": True" | type: official
- [C25] extra_body.google.cached_content 对应 Gemini 通用内容缓存(Chat端点)，须包在 extra_body 里 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Corresponds to Gemini's general content cache." | type: official
- [C26] Batch 兼容支持创建/监控/查看结果，但上传下载文件不支持(需原生 genai client) | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Compatibility for upload and download is currently not supported." | type: official
- [C27] 结构化输出经 .parse + response_format=Pydantic/Zod | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Gemini models can output JSON objects in any structure you define." | type: official
- [C28] Embeddings 支持，模型 gemini-embedding-2-preview/-001 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "gemini-embedding-2-preview for multimodal embeddings" | type: official
- [C29] service_tier 缺省 standard，可设 priority 或 flex | src: https://ai.google.dev/gemini-api/docs/openai | quote: "service_tier defaults to standard, equivalent to default for OpenAI" | type: official
- [C30] 函数调用与流式响应均受支持 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "The Gemini API supports streaming responses." | type: official
- [C31] 端点含 chat/completions、embeddings、images/generations、videos、models；未列参数被静默忽略 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "silently ignored by the compatibility layer" | type: official
- [C32] 视频生成走"Sora 兼容"的 /v1/videos，模型 veo-3.1-generate-preview，长任务需轮询 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "via the Sora-compatible /v1/videos endpoint" | type: official

- [C33] 端点 {LOC}-aiplatform.googleapis.com/v1/projects/{PID}/locations/{LOC}/endpoints/openapi，仅支持 GCP OAuth token | src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start/openai | quote: "Only Google Cloud Auth is supported using the OpenAI library" | type: official
- [C34] 定位：低成本切换/对比 OpenAI 与托管模型输出/成本/可扩展性 | src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate/openai/overview | quote: "a low-cost way to switch between calling OpenAI models and Agent Platform hosted models to compare output, cost, and scalability" | type: official

## conflicts
- 档位数不同：Vertex quote: "three levels...low,medium,high...mapped...to 1K, 8K, and 24K thinking token budgets" (src: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start/openai)；ai.google.dev 四档(含minimal)分模型，quote 见C22。

## gaps
- Anthropic 原生速率限制具体数值未查（在 /api/rate-limits，超出起点范围）。
- Gemini 兼容层是否有独立 /audio(TTS/转写)端点未确认，页面只见 chat.completions 内嵌 input_audio。
- Vertex response_format 细节(json_schema 不支持完全递归、支持 additional_properties)见原句但因 Vertex 限额 1-2 条未收录。

## leads
- Anthropic 示例模型名 "claude-opus-5-5"/"claude-sonnet-4-6"，暗示 Claude 5.x 世代命名，可与"Claude 5 默认开启thinking"对照核实。
- Vertex extra_body/extra_content 专有字段远多于 thinking_config/cached_content（含 safety_settings、thought_signature 等），深挖 Vertex 行可查该页。
