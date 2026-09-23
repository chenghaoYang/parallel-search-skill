# r1-zhipu
question: 智谱 BigModel 开放平台（docs.bigmodel.cn / open.bigmodel.cn）与 Z.ai（docs.z.ai）的 API 协议：(1) 其 OpenAI 风格 /api/paas/v4/chat/completions 与 OpenAI 官方 Chat Completions 的差异；(2) 其 Anthropic 兼容端点（Messages）与 Anthropic 官方 Messages API 的差异。
checked: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction, https://docs.bigmodel.cn/api-reference/模型-api/对话补全, https://docs.bigmodel.cn/cn/api/introduction, https://docs.bigmodel.cn/cn/api/api-code, https://docs.bigmodel.cn/cn/guide/capabilities/thinking, https://docs.bigmodel.cn/cn/guide/capabilities/thinking-mode, https://docs.bigmodel.cn/cn/guide/capabilities/streaming, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3, https://docs.bigmodel.cn/cn/coding-plan/quick-start, https://docs.bigmodel.cn/cn/coding-plan/faq, https://docs.bigmodel.cn/cn/coding-plan/latest-model, https://docs.bigmodel.cn/llms-full.txt, https://docs.z.ai/api-reference/introduction, https://docs.z.ai/api-reference/llm/chat-completion, https://docs.z.ai/api-reference/api-code, https://docs.z.ai/guides/llm/glm-5.3, https://docs.z.ai/llms-full.txt, https://docs.z.ai/guides/develop/claude/introduction

## claims
- [C1] Anthropic 端点 POST /api/anthropic/v1/messages，示例用 x-api-key 头 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: “curl https://open.bigmodel.cn/api/anthropic/v1/messages --header "x-api-key: YOUR_API_KEY"” | type: official
- [C2] 兼容页只有笼统声明，无字段清单 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "某些场景下智谱与 Claude 接口仍存在差异，但不影响整体兼容性。" | type: official
- [C3] key 在平台通用 API Keys 页创建 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "在 API Keys 管理页面创建 API Key" | type: official
- [C4] Z.ai 的 Anthropic base URL（Model API 表） | src: https://docs.z.ai/guides/llm/glm-5.3 | quote: "Anthropic Message Protocol | https://api.z.ai/api/anthropic" | type: official
- [C5] Coding Plan 与通用 Anthropic 端点是同一 URL | src: https://docs.bigmodel.cn/cn/coding-plan/quick-start | quote: "Anthropic Message 协议 | https://open.bigmodel.cn/api/anthropic" | type: official
- [C6] 订阅过 Coding Plan 的账号暂时只能用 OpenAI 协议调模型 API（Z.ai 同） | src: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3 | quote: "如果您有订阅过 GLM Coding Plan（含已过期），那么暂时您只能通过 OpenAI Chat Completion 协议调用模型 API" | type: official
- [C7] 套餐额度只在指定工具内可用 | src: https://docs.bigmodel.cn/cn/coding-plan/faq | quote: "在除规定工具外调用 API，不可享用 Coding 套餐的额度。" | type: official
- [C8] Claude Code 的 thinking 关闭值映射为 low 档，请求照常进行 | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "thinking.type 为 false、disabled、none、off | low | 继续请求；仍会轻量思考" | type: official
- [C9] 映射读取 Anthropic 侧 output_config.effort | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "Claude Code 使用 `thinking.type`、`output_config.effort`" | type: official
- [C10] BigModel 通用端点 | src: https://docs.bigmodel.cn/cn/api/introduction | quote: "智谱开放平台的通用 API 端点： https://open.bigmodel.cn/api/paas/v4" | type: official
- [C11] Z.ai 通用端点 | src: https://docs.z.ai/api-reference/introduction | quote: "Z.ai Platform's general API endpoint is as follows: https://api.z.ai/api/paas/v4" | type: official
- [C12] 鉴权 Authorization: Bearer <API Key> | src: https://docs.bigmodel.cn/cn/api/introduction | quote: "开放平台 API 使用标准的 HTTP Bearer 进行身份验证。" | type: official
- [C13] Coding Plan 的 OpenAI 端点另为 /api/coding/paas/v4 | src: https://docs.bigmodel.cn/cn/coding-plan/quick-start | quote: "OpenAI Chat Completion 协议 | https://open.bigmodel.cn/api/coding/paas/v4" | type: official
- [C14] 私有 thinking.type（enabled/disabled）；GLM-5.3 传 disabled 会报错 | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking | quote: "GLM-5.3 GLM-5.3-FLASH 不再支持关闭思考（API 请求中 thinking.type 传 disabled 将会报错）" | type: official
- [C15] reasoning_effort：GLM-5.3 只支持 low/high/max 三档 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "对于 `GLM-5.3` `GLM-5.3-FLASH` 模型，仅支持 low / high / max 档位。" | type: official
- [C16] clear_thinking 默认 true（丢弃历史轮 reasoning_content） | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "默认为 `True`。用于控制是否清除历史对话轮次（`previous turns`）中的 `reasoning_content`。" | type: official
- [C17] 保留式思考默认值随端点不同 | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking-mode | quote: "该能力在 Coding Plan 端点默认开启、标准 API 端点默认关闭。" | type: official
- [C18] 配合工具时须把 reasoning_content 随工具结果回传 | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking-mode | quote: "必须显式保留 Reasoning content，并在返回工具结果时一并返回" | type: official
- [C19] tools 支持 function、retrieval、web_search | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "支持函数调用、知识库检索和网络搜索。" | type: official
- [C20] tool_choice 只支持 auto | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "默认`auto`且仅支持`auto`。" | type: official
- [C21] 私有 tool_stream，流式返回工具参数 | src: https://docs.z.ai/api-reference/llm/chat-completion | quote: "Whether to enable streaming response for Function Calls. Default value is false." | type: official
- [C22] response_format.type 只有 text 和 json_object | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "取值收敛为三种：`text`（普通文本输出）、`json_object`（`JSON` 格式输出）。" | type: official
- [C23] 流式以 data: [DONE] 结束 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "流式输出结束时会返回 `data: [DONE]` 消息。" | type: official
- [C24] usage 只在最后一个 chunk 返回 | src: https://docs.bigmodel.cn/cn/guide/capabilities/streaming | quote: "`usage`: 令牌使用统计（仅在最后一个chunk中出现）" | type: official
- [C25] 流式中途失败时不返回错误码，改在 finish_reason 报告 | src: https://docs.bigmodel.cn/cn/api/api-code | quote: "如果 API 在推理过程中异常终止，不会返回上述错误码，而是在响应体的 `finish_reason` 参数中返回异常原因" | type: official
- [C26] finish_reason 有私有值 sensitive、network_error、model_context_window_exceeded | src: https://docs.z.ai/api-reference/llm/chat-completion | quote: "`sensitive`, `model_context_window_exceeded` or `network_error`." | type: official
- [C27] 缓存命中量报告在 cached_tokens 字段 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "响应字段 `usage.prompt_tokens_details.cached_tokens`" | type: official
- [C28] 错误体 error.code（字符串业务码）+ error.message | src: https://docs.bigmodel.cn/cn/api/api-code | quote: “{"error":{"code":"1001","message":"Header 中未收到 Authentication 参数，无法进行身份验证"}}” | type: official
- [C29] 1261（Prompt 超长）、1301（内容安全）对应 HTTP 400 | src: https://docs.bigmodel.cn/cn/api/api-code | quote: "1261 | 400 | Prompt 超长 | 1301 | 400 | 系统检测到输入或生成内容可能包含不安全或敏感内容" | type: official

## conflicts
- GLM-5.3 关闭思考：latest-model 页写“继续请求；仍会轻量思考”，thinking 页写“thinking.type 传 disabled 将会报错”；可能是 Coding Plan 与标准 API 语境不同，未裁决。
- Z.ai GLM-5.3 页 Model API 表写“OpenAI Chat Completion Protocol | https://api.z.ai/api/coding/paas/v4”，api-reference/introduction 的通用端点是 https://api.z.ai/api/paas/v4。
- stop：Z.ai chat-completion 写“Currently, only one stop word is supported”，两站 schema 却都是 maxItems: 4。
- 错误体：Z.ai chat-completion 的 OpenAPI Error 是顶层 code（int32）；api-code 页写“a top-level error object that includes a `code` and `message`”。

## gaps
- Anthropic 端点没有字段/header 文档（Z.ai 连兼容页都没有，404）：anthropic-version（官方示例未带）、anthropic-beta、cache_control、budget_tokens、stop_sequences、top_k、metadata、tool_choice、image/document 块、流式事件、usage、错误格式都没写。查过 claude/introduction、coding-plan、devpack、glm-5.3 各页、openapi.json，两站 llms-full.txt 全文检索命中 0。
- 实测（非文档，2026-09-23）：假 key 请求两站 /api/anthropic/v1/messages 返回 401 {"error":{"message":"…","type":"1000"}}（无顶层 "type":"error"）；/api/paas/v4 返回 {"error":{"code":"1000",…}}。
- 对话补全 schema 中没有 n、seed、presence/frequency_penalty、logprobs、parallel_tool_calls、stream_options、json_schema、reasoning_tokens；所有页面都没有更新日期。

## leads
- JWT 鉴权（HS256）；do_sample=false 时忽略 temperature/top_p；temperature [0.0, 1.0]；request_id 6–64 字符、user_id 6–128 字符；max_tokens 上限 128K；缓存为隐式；1210/1211 为 400，1113 与 13xx 为 429。
- Z.ai FAQ：“API calls outside the plan are not available”；BigModel FAQ：“Claude Code 中暂不支持使用其他资源包”。
- 两站另有 OpenAI Responses 协议 /api/v1；私有响应字段 content_filter、web_search。
