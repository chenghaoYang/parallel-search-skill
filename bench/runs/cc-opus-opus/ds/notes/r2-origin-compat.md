# r2-origin-compat
question: 两家源头厂商自己提供的 OpenAI Chat Completions 兼容层——(a) Google Gemini 的 OpenAI 兼容层，(b) Anthropic 的 OpenAI SDK 兼容层——各自的接入方式、推理/思考怎么映射、工具调用差异、哪些 OpenAI 字段不支持/忽略、官方定位（是否仅供测试/beta）？
checked: https://ai.google.dev/gemini-api/docs/openai, https://ai.google.dev/gemini-api/docs/thought-signatures, https://ai.google.dev/gemini-api/docs/thinking, https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures, https://ai.google.dev/gemini-api/docs/function-calling, https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk.md

## claims
- [C1] GG 接入：base_url 如下 + Gemini key（页更新 2026-09-02） | src: https://ai.google.dev/gemini-api/docs/openai | quote: "base_url="https://generativelanguage.googleapis.com/v1beta/openai/"" | type: official
- [C2] GG 定位：beta | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Support for the OpenAI libraries is still in beta" | type: official
- [C3] GG 映射：minimal/low/medium/high → 3.1 Pro 为 low/low/medium/high；3.1 Flash-Lite、3 Flash 同名；2.5 为 budget 1,024/1,024/8,192/24,576 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "they map to OpenAI's reasoning efforts" | type: official
- [C4] GG：none 只能关 2.5 的思考 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "set reasoning_effort to "none" for 2.5 models. Reasoning cannot be turned off for Gemini 2.5 Pro or 3 models." | type: official
- [C5] GG：reasoning_effort 与 thinking_level/budget 互斥 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "reasoning_effort and thinking_level/thinking_budget overlap functionality, so they can't be used at the same time." | type: official
- [C6] GG：摘要靠 extra_body.google.thinking_config.include_thoughts（REST 顶层键即 extra_body，Python 双层） | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Gemini thinking models also produce thought summaries. You can use the extra_body field to include Gemini fields in your request." | type: official
- [C7] GG：extra_body 的 Chat 项只有 cached_content、thinking_config | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Corresponds to Gemini's general content cache." | type: official
- [C8] GG 签名位置：tool_calls[].extra_content.google.thought_signature（页更新 2026-09-04） | src: https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures | quote: ""extra_content": { "google": { "thought_signature": "<Signature A>"" | type: official
- [C9] GG：Gemini 3 函数调用不回传签名报 4xx | src: https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures | quote: "When using Gemini 3 models, you must pass back thought signatures during function calling, otherwise you will get a validation error (4xx status code)." | type: official
- [C10] GG 并行：签名只在 FC1；FC/FR 交错回传报 400 | src: https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures | quote: "If you have them interleaved as "FC1 + signature, FR1, FC2, FR2" the API will return a 400 error." | type: official
- [C11] GG 图像端点：其余参数静默忽略 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Any other parameters not listed here or in the extra_body section will be silently ignored" | type: official
- [C12] GG 有 embeddings 端点 | src: https://ai.google.dev/gemini-api/docs/openai | quote: "curl "https://generativelanguage.googleapis.com/v1beta/openai/embeddings"" | type: official
- [C13] GG 结构化输出可用（parse） | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Gemini models can output JSON objects in any structure you define." | type: official
- [C14] AN 接入：base_url 如下 + Claude key | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "base_url="https://api.anthropic.com/v1/"" | type: official
- [C15] AN 定位：用于测试，非生产方案 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "primarily intended to test and compare model capabilities, and is not considered a long-term or production-ready solution for most use cases." | type: official
- [C16] AN 思考：extra_body={"thinking":{"type":"enabled","budget_tokens":2000}} 开启，不返回思考过程 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "the OpenAI SDK doesn't return Claude's detailed thought process." | type: official
- [C17] AN：reasoning_effort 被忽略 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "`reasoning_effort` | Ignored" | type: official
- [C18] AN：n 只能为 1 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "Must be exactly 1" | type: official
- [C19] AN：response_format 被忽略 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "Ignored. For JSON output, use Structured Outputs" | type: official
- [C20] AN：stop 只认非空白序列 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "All non-whitespace stop sequences work" | type: official
- [C21] AN：parallel_tool_calls 完整支持 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "`parallel_tool_calls` | Fully supported" | type: official
- [C22] AN：音频输入被忽略并剥离 | src: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk | quote: "Audio input is not supported; it will be ignored and stripped from input" | type: official

## conflicts
- GG openai 页主示例 base_url 为 ".../v1beta/openai/"，extra_body 示例却写 "base_url="https://generativelanguage.googleapis.com/v1beta/""
- AN 称 "manually configured extended thinking is a legacy mode"，唯一示例却用 "type: "enabled", budget_tokens: 2000"

## gaps
- GG：chat 无不支持参数清单，长度/采样参数处理未写；未提 Responses API；摘要字段未写
- GG：映射表没列 gemini-3.8-flash（thinking 页写它只有 low, medium, high）
- GG：openai 页的签名链接现跳到 /docs/thinking（无 OpenAI 小节）
- AN：没给 adaptive 思考写法；没说 chat 以外端点能否用；页面无更新日期

## leads
- GG 认 service_tier=flex/priority（AN 忽略）；Batch 不兼容文件上传下载；有 /v1/videos
- AN：usage.*_details 恒为空；多 workspace key 需 anthropic-workspace-id；Claude 5 默认思考
- GG：占位签名 skip_thought_signature_validator 可跳过校验
