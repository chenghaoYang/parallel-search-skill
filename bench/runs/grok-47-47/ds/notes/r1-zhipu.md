# r1-zhipu
question: 智谱（BigModel / 智谱 GLM）官方的 Messages 接口相对它自己文档所声称的 Anthropic 兼容，路径、header、字段有什么不同或限制？它的 OpenAI 兼容 Chat 端点路径是什么？
checked: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction, https://docs.bigmodel.cn/llms.txt, https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3, https://docs.bigmodel.cn/cn/guide/develop/openai/introduction, https://docs.bigmodel.cn/api-reference/模型-api/对话补全, https://docs.bigmodel.cn/openapi/openapi.json, https://docs.bigmodel.cn/cn/guide/develop/http/introduction, https://docs.bigmodel.cn/cn/guide/capabilities/streaming, https://docs.bigmodel.cn/cn/guide/capabilities/function-calling, https://docs.bigmodel.cn/cn/guide/capabilities/thinking, https://docs.bigmodel.cn/cn/guide/capabilities/struct-output, https://docs.bigmodel.cn/cn/coding-plan/quick-start, https://docs.bigmodel.cn/cn/guide/develop/claude, https://docs.bigmodel.cn/cn/coding-plan/tool/claude, https://docs.bigmodel.cn/cn/coding-plan/latest-model

## claims
- [C1] D1 Anthropic base_url 为 `https://open.bigmodel.cn/api/anthropic`；curl 全路径 `https://open.bigmodel.cn/api/anthropic/v1/messages`。 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "curl https://open.bigmodel.cn/api/anthropic/v1/messages" | type: official
- [C2] D1 该 curl 只写头 `x-api-key` 与 `content-type: application/json`。同页无 anthropic-version、Authorization。 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "x-api-key: YOUR_API_KEY" | type: official
- [C3] D1 通用 OpenAI Chat 全路径 `https://open.bigmodel.cn/api/paas/v4/chat/completions`，头为 Bearer。 | src: https://docs.bigmodel.cn/cn/guide/develop/http/introduction | quote: "Authorization: Bearer YOUR_API_KEY" | type: official
- [C4] D1 Coding Plan 的 OpenAI Chat base 是 `https://open.bigmodel.cn/api/coding/paas/v4`（此页未写 `/chat/completions` 全路径）。 | src: https://docs.bigmodel.cn/cn/coding-plan/quick-start | quote: "https://open.bigmodel.cn/api/coding/paas/v4" | type: official
- [C5] D1/D10 订过 Coding Plan（含过期）时，模型 API 暂时只能走 OpenAI Chat Completion。 | src: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3 | quote: "那么暂时您只能通过 OpenAI Chat Completion 协议调用模型 API，我们将在近期迭代优化。" | type: official
- [C6] D1 Claude Code 写 `ANTHROPIC_AUTH_TOKEN`，base 仍为 `https://open.bigmodel.cn/api/anthropic`。与兼容页 x-api-key / ANTHROPIC_API_KEY 不同。 | src: https://docs.bigmodel.cn/cn/coding-plan/tool/claude | quote: "ANTHROPIC_AUTH_TOKEN" | type: official
- [C7] D2 OpenAI Chat 的 messages 即本次请求的完整上下文，不是服务端会话 id 续写。 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "对话消息列表，包含当前对话的完整上下文信息。" | type: official
- [C9] D2/D6 `clear_thinking` 默认 true，会丢掉历史 reasoning_content；保留须在 messages 里原样按序透传。 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "必须在 `messages` 中完整、未修改、按原顺序透传历史 `reasoning_content`" | type: official
- [C10] D3/D4 文本四角色 system、user、assistant、tool。system 在 messages 内，无顶层 system 说明。 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "支持四种角色：`system`（系统消息，用于设定`AI`的行为和角色）、`user`（用户消息，来自用户的输入）、`assistant`（助手消息，来自`AI`的回复）、`tool`（工具消息，工具调用的结果）。" | type: official
- [C11] D3 图片理解示例的 content 类型是 `image_url`，不是 image。 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "type: image_url" | type: official
- [C12] D3/D8 思考在 `reasoning_content`，与 content 并列，不是 type=thinking。深度思考示例 model 为 glm-5.3。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking | quote: "print(response.choices[0].message.reasoning_content)" | type: official
- [C13] D5 Chat 的 tool_choice 默认且仅支持 auto。 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "默认`auto`且仅支持`auto`。" | type: official
- [C14] D5 函数结果要再送回模型。同页示例用 role tool 与 tool_call_id。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/function-calling | quote: "将函数结果返回给模型" | type: official
- [C15] D6 Chat：GLM-5.3 至 GLM-4.6 最大输出 128K。Messages 兼容页只示例 max_tokens 1024，无上限原句。 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "系列最大支持`128K`输出长度" | type: official
- [C16] D6/D10 通用 API：GLM-5.3 / GLM-5.3-FLASH 传 thinking.type=disabled 会报错。字段名 thinking.type。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking | quote: "API 请求中 thinking.type 传 disabled 将会报错" | type: official
- [C17] D6 reasoning_effort 在 thinking 开启时生效，默认 max，仅 GLM-5.2+。GLM-5.3 仅 low/high/max。模型页写 type 只支持 enabled。示例在 /paas/v4/chat/completions。 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "对于 `GLM-5.3` `GLM-5.3-FLASH` 模型，仅支持 low / high / max 档位。" | type: official
- [C18] D6/D10 Claude Code（Coding Plan）：字段为 thinking.type 与 output_config.effort；Codex 为 reasoning.effort。disabled/false/none/off 映射为 low，继续请求，仍轻量思考。 | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "Claude Code 使用 `thinking.type`、`output_config.effort`；Codex 使用 `reasoning.effort`。关闭思考配置会转换为 low，不会切换到其他模型。" | type: official
- [C19] D7 OpenAI 流式是 SSE，示例以 `data: [DONE]` 结束，不是 message_start 这类事件名。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/streaming | quote: "data: [DONE]" | type: official
- [C20] D8 终止字段是 finish_reason 不是 stop_reason。含 stop、tool_calls、length、sensitive、network_error；描述另有 model_context_window_exceeded。 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "'sensitive’表示内容被安全审核接口拦截" | type: official
- [C21] D8 usage 为 prompt_tokens、completion_tokens、total_tokens，以及 prompt_tokens_details.cached_tokens。另有 request_id、content_filter、web_search。 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "命中的缓存 `Token` 数量" | type: official
- [C22] D9 response_format.type 为 text 或 json_object；结构写在 system 消息。OpenAPI 无 json_schema。同段写「三种」但只列这两种。 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "type 取值收敛为三种：`text`（普通文本输出）、`json_object`（`JSON` 格式输出）。" | type: official
- [C23] D10 自称改 Key 与 base URL 即可兼容 Claude，但承认有差异，未列清单。 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "某些场景下智谱与 Claude 接口仍存在差异，但不影响整体兼容性。" | type: official
- [C24] D10 1M 上下文的模型 id 要加后缀 `[1m]`，例如 `glm-5.3-flash[1m]`。 | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "注意开启 GLM 1M 上下文需要模型后缀加上 `[1m]` ，即 `glm-5.3-flash[1m]`" | type: official

## conflicts
- D1：订过 Coding Plan 的模型 API「只能 OpenAI Chat Completion」vs Coding Plan 仍写两种协议。quote A: "那么暂时您只能通过 OpenAI Chat Completion 协议调用模型 API，我们将在近期迭代优化。" https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3 quote B: "GLM Coding Plan 支持 Anthropic 协议和 OpenAI 协议两种接入方式" https://docs.bigmodel.cn/cn/coding-plan/quick-start
- D6：API 页称 thinking.type=disabled 失败；Claude Code 称映射为 low 并继续。quote A: "否则，请求将失败。" https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3 quote B: "继续请求；仍会轻量思考" https://docs.bigmodel.cn/cn/coding-plan/latest-model
- D8：schema 称 reasoning_content 仅 glm-4.5 与 glm-4.1v-thinking；流式页仍列 delta.reasoning_content，思考页 glm-5.3 示例也读该字段。quote A: "仅在使用 `glm-4.5` 系列, `glm-4.1v-thinking` 系列模型时返回。" https://docs.bigmodel.cn/api-reference/模型-api/对话补全 quote B: "增量思考内容" https://docs.bigmodel.cn/cn/guide/capabilities/streaming
- D10：`/cn/guide/develop/claude` 默认 Opus=GLM-4.7；`/cn/coding-plan/tool/claude` 默认 Opus=GLM-5.3-Flash。quote A: "ANTHROPIC_DEFAULT_OPUS_MODEL：GLM-4.7" quote B: "ANTHROPIC_DEFAULT_OPUS_MODEL：GLM-5.3-Flash"
- D1 鉴权：兼容页是 x-api-key；Claude Code 是 ANTHROPIC_AUTH_TOKEN。两边都无 anthropic-version。见 C2、C6。
- D9「三种」却只列 text、json_object，见 C22。

## gaps
- `/v1/messages` 无字段表。已查兼容页、llms.txt、OpenAPI 1.0.0（无 /anthropic，无 anthropic-version、message_start、stop_reason）。无原句、不写成差异：anthropic-version 是否必填；Authorization 能否替代 x-api-key；Messages 是否客户端重放；块类型 text/tool_use/tool_result/thinking/image；顶层 system；tools/input_schema/tool_choice；Messages 的 max_tokens 上限；事件名；响应的 content/stop_reason/usage；Messages 结构化输出；不支持的 beta 或块清单。
- C7–C22 只文档化 OpenAI Chat `/paas/v4/chat/completions`（Claude Code 思考映射见 Coding Plan），不是 Messages 行为。无页面更新日期。OpenAPI info.version=1.0.0。

## leads
- Managed Agents 的 agent.tool_use / user.tool_result、input_schema 不是 Messages。
- OpenAI Response base 另为 https://open.bigmodel.cn/api/v1。
- 两份 Claude Code 页的默认模型映射不一致。
