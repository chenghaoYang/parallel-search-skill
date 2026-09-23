# r3-conflicts
question: 裁决三处下游兼容层的冲突/缺口：①百炼 tools×stream；②xAI penalties/stop；③Moonshot 的 responses/anthropic 兼容面入口。
checked: https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope, https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions, https://docs.x.ai/developers/rest-api-reference/inference/responses, https://docs.x.ai/developers/model-capabilities/text/reasoning, https://docs.x.ai/developers/rest-api-reference/inference/chat-completions, https://platform.kimi.com/docs/guide/start-guide, https://platform.kimi.com/docs/api/responses, https://platform.kimi.com/docs/api/messages （均抓取 2026-09-23；直访 /api/responses、/api/messages 为 404 壳；help.aliyun.com/zh/model-studio/function-calling 实为 Assistant API 页，与本问无关未引）

## claims
- [C1] 百炼迁移页 tools 行（2026-09-23 仍）载禁令且限定模型：仅 qwen-turbo/plus/max 支持工具，tools 与 stream=True 暂不可同用 | src: https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope | quote: "当前支持的模型包括qwen-turbo、qwen-plus和qwen-max。说明tools暂时无法与stream=True同时使用。" | type: official
- [C2] 百炼 API 参考页（2026-09-23）新增 tool_stream 参数：boolean 可选，默认 false，仅在 stream=true 时生效 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "tool_stream boolean （可选）默认值为 false仅在stream=true时生效" | type: official
- [C3] 百炼 API 参考页明确 tools+stream 已可用：普通工具参数开 stream=true 即流式输出；仅复杂工具（参数类型 array/object）受 tool_stream 控制 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "普通工具参数只要开启stream=true就会流式输出。复杂工具是指工具定义中某些参数类型为array或object。" | type: official
- [C4] tool_stream 为非 OpenAI 标准参数（SDK 需 extra_body={"tool_stream": true}）；适用 Qwen 系，GLM 支持列表 glm-4.6/4.7/5/5.1（阿里云直供） | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 extra_body 对象中。" | type: official
- [C5] 百炼 API 参考页完整收录 tool_choice（默认 auto，含 none/required/指定函数）与 parallel_tool_calls（默认 false），全文无 tools×stream 禁令（grep 计 0） | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "tool_choice string 或 object（可选）默认值为 auto" | type: official
- [C6] xAI responses 参考页（2026-09-23）presence_penalty 标端点级不支持 | src: https://docs.x.ai/developers/rest-api-reference/inference/responses | quote: "(NOT SUPPORTED in Responses API) Positive values penalize new tokens based on whether they appear in the text so far" | type: official
- [C7] xAI responses 参考页 frequency_penalty 同标端点级不支持 | src: https://docs.x.ai/developers/rest-api-reference/inference/responses | quote: "(NOT SUPPORTED in Responses API) Positive values penalize new tokens based on their existing frequency in the text so far" | type: official
- [C8] xAI reasoning 页：三个参数对 reasoning models 全禁，传入即报错 | src: https://docs.x.ai/developers/model-capabilities/text/reasoning | quote: "presencePenalty, frequencyPenalty, and stop cannot be used with reasoning models. Requests that include them return an error." | type: official
- [C9] xAI chat completions 页 stop 字段仍在，带模型级限制标注 | src: https://docs.x.ai/developers/rest-api-reference/inference/chat-completions | quote: "(Not supported by reasoning models) Up to 4 sequences where the API will stop generating further tokens." | type: official
- [C10] xAI chat 页 frequency_penalty 仍在，限非 reasoning 模型，取值 [-2.0, 2.0] | src: https://docs.x.ai/developers/rest-api-reference/inference/chat-completions | quote: "(Not supported by reasoning models) Number between -2.0 and 2.0." | type: official
- [C11] xAI chat 页 presence_penalty 仍在，额外排除 grok-3 | src: https://docs.x.ai/developers/rest-api-reference/inference/chat-completions | quote: "(Not supported by `grok-3` and reasoning models) Number between -2.0 and 2.0." | type: official
- [C12] Moonshot start-guide 总声明双格式兼容 | src: https://platform.kimi.com/docs/guide/start-guide | quote: "Kimi API 提供了与 Kimi 大模型交互的能力，兼容 OpenAI 与 Anthropic API 格式。" | type: official
- [C13] start-guide 卡片列 Responses API 入口（href /api/responses，OpenAI 兼容面） | src: https://platform.kimi.com/docs/guide/start-guide | quote: "Responses APIOpenAI 兼容格式，生成文本/JSON 输出或调用函数工具。" | type: official
- [C14] start-guide 卡片列 Messages API 入口（href /api/messages，Anthropic 兼容面，适配 Claude Code） | src: https://platform.kimi.com/docs/guide/start-guide | quote: "Messages APIAnthropic 兼容格式，适合 Anthropic SDK、Claude Code 等工具接入。" | type: official
- [C15] Responses 面实际入口（canonical 确认，卡片 href 需加 /docs 前缀） | src: https://platform.kimi.com/docs/api/responses | quote: "创建一次模型响应。传入文本或图片，生成文本或 JSON 输出；也可以让模型调用你定义的函数工具，或使用服务端执行的联网搜索。" | type: official
- [C16] Anthropic/Messages 面实际入口（canonical 确认，页带 dateModified 2026-09-18T06:47:05.398Z） | src: https://platform.kimi.com/docs/api/messages | quote: "以 Anthropic Messages API 兼容的格式调用 Kimi 模型，支持流式输出、工具调用、图片输入、思考与结构化输出。" | type: official

## conflicts
- ①百炼 tools×stream 裁决：当前口径=已放开。以 API 参考页（C2/C3/C5，含 tool_stream 流式工具调用规范）为准；迁移页禁令（C1）未同步=滞后页。限制已从端点级全禁收窄为参数级：普通工具参数 stream=true 即流式；复杂参数（array/object）需 tool_stream=true（Qwen 系+GLM 指定列表）。未见显式"放开"公告，放开证据即 tool_stream 参数本身。
- ②xAI penalties/stop 裁决：三口径不矛盾，可调和，无页滞后。模型维度：reasoning models 禁 presencePenalty/frequencyPenalty/stop（C8），chat spec 各字段描述内嵌同款标注（C9/C10，presence 另排 grok-3，C11）；端点维度：/v1/responses 对 penalties 整体 NOT SUPPORTED（C6/C7），与模型无关。R2 所记"三口径打架"实为端点×模型两维叠加；chat 页"仍含字段"并非滞后——字段在但描述已限定。
- ③Moonshot 无冲突：start-guide 三入口自洽；唯一小差异是卡片 href 写 /api/* 而实际 canonical 为 /docs/api/*（直访 /api/* 是 404 壳）。

## gaps
- 百炼两页"更新时间："字段存在但值为 JS 渲染，未取到具体日期；未找到明确宣布放开 tools×stream 的产品动态/公告页（pplx 检索仅得 AI 综合答案，不作来源）。
- xAI responses 页请求 schema 中未检得 stop 字段（grep 未命中，非原句证据）；其 stop 口径只能从 C8 推断为随模型禁用。
- Moonshot 两兼容面的 base_url（Anthropic 面 HTTP 前缀、Responses 面 /v1/responses 完整路径）未在两入口页 meta 原句中取到，未深挖页面正文。

## leads
- platform.kimi.com/guide/codex-kimi：官方示例"通过 Kimi Responses API 将 Codex 直连 Kimi K3"，可作 Responses 面用法样例。
- platform.kimi.com/docs/api/responses.md 等提供 markdown 原文（link rel=alternate），后续抓取可直取 .md。
- 百炼 tool_stream 的 Qwen/GLM 支持面已记，DeepSeek/Kimi/MiniMax 系（阿里云直供）是否支持流式工具调用未记，可补查。
