# LLM 请求协议：四套谱系，以及「兼容」改了什么

> 回答：Chat Completions、Responses、Messages、generateContent 在请求/响应上差在哪；DeepSeek 的 response 相对 OpenAI 官方文档差在哪；智谱的 message 相对 Anthropic 官方差在哪。截至 2026-09-23 的官方文档。先读第 0 节，第 2 节只比四个官方谱系，第 3 节只看适配层多出来或删掉的字段。

## 0. 一屏看懂

1. 先看两件事：下一轮历史放在哪，以及一条内容是字符串还是带 `type` 的块。Chat Completions 重放 `messages[]`。Responses 可以改走 `previous_response_id`。Messages 也重放消息，但系统指令在顶层 `system`，工具结果是 user 内容里的 `tool_result`。generateContent 重放 `contents[].parts[]`，系统指令在 `systemInstruction`，角色是 `user` / `model`。
2. OpenAI 仍支持 Chat Completions，新项目推荐 Responses。换的不是只改 URL：长度字段变为 `max_output_tokens`，JSON 从 `response_format` 改到 `text.format`，工具结果是 `function_call_output`，不是 `role=tool`。[4][6]
3. DeepSeek 两套都有：`POST https://api.deepseek.com/chat/completions` 与 `POST /responses`，路径不带 `/v1`，Bearer。它自称兼容 OpenAI/Anthropic。相对 OpenAI 文档，写明的差别是：Responses **不在服务端存会话**，`previous_response_id`、`store` 等不支持的参数静默忽略；Chat 的 `response_format` 只有 `text` 与 `json_object`（没有 `json_schema`；schema 在 Responses 的 `text.format`）；思维在 Chat 的 `reasoning_content` 或 Responses 的 `reasoning` item；带 `tools` 却不回传 `reasoning_content` 会 400；`finish_reason` 多了 `insufficient_system_resource` 与 `aborted`；penalty 参数不再生效。`developer` 在 Responses 里当成 `user`。[20][21][22][23][24]
4. 智谱的 Messages 路径是 `POST https://open.bigmodel.cn/api/anthropic/v1/messages`，示例头只有 `x-api-key`，没写 `anthropic-version`。原文承认与 Claude「仍存在差异」，但没有差异清单，也没有这份端点的字段表。能逐字段引用的是另一条协议：`POST https://open.bigmodel.cn/api/paas/v4/chat/completions`（Bearer），形状是 Chat，不是 Anthropic 的 `stop_reason` / `tool_result`。[27][28][29]
5. 适配层最常踩的是思维旁路，不是 URL。DeepSeek 有工具时必须回传 `reasoning_content`。百炼禁止把它拼进 `content`，`preserve_thinking` 默认 false。Moonshot 要求每一轮 assistant 的 `reasoning_content` 原样留在 `messages`。智谱 Chat 的 `clear_thinking` 默认 true，要保留必须原样透传。[24][29][34][36]
6. 「换成 base_url 就能用」只在文档的总述里成立。Moonshot 把 `temperature` 等固定，传入其他值会报错，并在末条 assistant 上使用 `partial`。百炼的 `enable_thinking` 在 HTTP body 顶层（Python SDK 走 `extra_body`），Qwen 不支持 `tool_choice=required`。智谱 Chat 的 `tool_choice` 文档写默认且仅 `auto`。[29][34][37][38]
7. Gemini 原生不是 Chat。另外挂了一条 `POST /v1beta/openai/chat/completions`（Bearer，`stream: true`）。官方建议还没用 OpenAI 库的调用方直接调 Gemini API。`responseSchema` 已标 deprecated，替代字段在文档里互相指向，见第 5 节。[16][18]

## 1. Taxonomy

分类轴：历史接在客户端还是服务端 id 上；内容是纯字符串还是带类型的块。同形不等于同一状态机：DeepSeek 的 `/responses` 用了 Responses 的字段名，但写明不存会话。

| 家族 | 历史怎么接 | 系统指令 | 工具结果 | 流式结束 |
|---|---|---|---|---|
| Chat Completions | 客户端重放 `messages` | `messages` 里的 `system` / `developer` | `role=tool` | SSE，`data: [DONE]` |
| Responses | 本次 `input`，或 `previous_response_id` / `conversation` | 顶层 `instructions` | `type=function_call_output` | SSE（OpenAI 事件全名未逐条摘句） |
| Messages | 客户端重放完整 `messages` | 顶层 `system` | user 消息里的 `tool_result` | SSE，`event: message_stop` |
| generateContent | 客户端重放 `contents` | `systemInstruction` | `functionResponse` part | 另一个方法 `:streamGenerateContent` |

适配层不单列家族。它声明自己模仿上面某一行，再加厂商字段（最常见的是 `reasoning_content`）。

## 2. 对照矩阵

只列四个官方谱系。空着的枚举表示笔记里没有逐字原句，不补。

### 端点、历史、系统指令

| | 端点与鉴权 | 历史 | 系统指令 | 输入角色 |
|---|---|---|---|---|
| Chat Completions | `POST https://api.openai.com/v1/chat/completions`，`Authorization: Bearer` [1][2][3] | 每轮发送累积的 `messages`；没有用来续写的对话 id。可选 `store`（默认值两处文档冲突，见第 5 节）[1][4] | o1 及更新模型用 `developer` 替代旧 `system`；`system` 仍在 [1] | 参考按角色分节，含 `developer`；工具结果是单独一类消息 [1] |
| Responses | 迁移指南：`post /v1/chat/completions` 改为 `post /v1/responses`。同样 Bearer [3][4] | 不传 id 时单次请求无状态，历史放进本次参数。`previous_response_id` 指向上一则。`conversation` 的 items 会前置到本次 input [6][7] | `instructions`：插入上下文的 system（或 developer）消息 [6] | `input` 的 string 等于 `user` 文本。message role：`user` `assistant` `system` `developer` [6] |
| Messages | `POST https://api.anthropic.com/v1/messages`。必填 `anthropic-version: 2023-06-01`。`Authorization` 在未设置 `x-api-key` 时为必需 [8][9][10] | 无服务端历史，每次发送完整对话 [8][11] | 顶层 `system`：string 或 text block 数组。同页散文写没有 `system` role，schema 又列出该 role（第 5 节）[8] | `content` 为 string 或 block 数组；block 含 `tool_result` [8] |
| generateContent | `POST https://generativelanguage.googleapis.com/v1beta/{model=models/*}:generateContent`。总览要求头 `x-goog-api-key`；参考 shell 用 `?key=`（第 5 节）[16][17] | `contents` 重复字段，装历史和最新一轮；SDK 每轮发送全量历史 [16][19] | 与 `contents` 同级的 `systemInstruction`，目前仅文本 [16] | role 只能 `user` 或 `model`。parts 里 text、inlineData、functionCall、functionResponse 等互斥 [16] |

### 工具、长度、流、正文、JSON

| | 工具 | 长度与推理 | 流式 | 响应与用量 | JSON |
|---|---|---|---|---|---|
| Chat Completions | `type: function` 的 `parameters` 可省略，表示无参数。无 tools 时 `tool_choice` 默认 `none`。结果消息「responding to」那次调用 [1] | `max_completion_tokens` 含可见输出和 reasoning tokens。`max_tokens` 已弃用，不兼容 o-series。`temperature` 0–2。`reasoning_effort`：`none` `minimal` `low` `medium` `high` `xhigh` `max` [1] | `stream: true` 为 SSE，`choices[].delta`，`object`=`chat.completion.chunk`，在 `data: [DONE]` 前可带 usage [1] | `object`=`chat.completion`，`choices[].message`。`finish_reason` 仍含已弃用值 `function_call`。`usage` 含 prompt token 计数，另有 reasoning tokens [1] | `response_format.type`：`text` `json_object` `json_schema`。后者子字段 `name` `description` `schema` `strict`。`json_object` 仍要有消息要求模型输出 JSON [1] |
| Responses | 调用 item 的 type 恒为 `function_call`；回传恒为 `function_call_output`。另有内置 `web_search` / `web_search_2025_08_26` [6] | `max_output_tokens` 含可见输出和 reasoning tokens。`temperature` 0–2。`reasoning.effort` 与 Chat 同一组取值 [6] | `stream: true` 走 SSE [6]。事件全名没有逐条原句，见第 5 节 | 正文在 `output[]`。`status`：`completed` `failed` `in_progress` `cancelled` `queued` `incomplete`。usage 描述含 input、output、total tokens [6] | 用 `text.format`，不用 `response_format` [4] |
| Messages | `tools[].input_schema` 为 JSON Schema。`tool_result` 放在后续 **user** 消息里，不是 `role=tool` [8] | `max_tokens` 类型为 number。`thinking.type=enabled` 时 `budget_tokens` ≥1024 且小于 `max_tokens`。Opus 4.6 之后的模型不支持设置 `temperature`（与指南的型号范围冲突，见第 5 节）[8] | SSE。结束事件 `event: message_stop`。delta 的 `type` 与事件名一致 [12] | `content` 为带 `type` 的块数组，响应 `role` 恒 `assistant`。`stop_reason` 至少包括 `tool_use`。`usage` 含 `input_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens` [8] | `output_config.format`，`type: json_schema` 加 `schema`。旧的 `output_format` 已迁到这里，过渡期仍接受 [8][13] |
| generateContent | `tools[].functionDeclarations`；模型不执行函数。下一轮用 `functionResponse`（`response` 为必填 JSON）。`FunctionCall` 含 `id` `name` `args`。参考另写 role `"function"`，与「只能 user/model」冲突 [16] | 都在 `generationConfig`：`maxOutputTokens` `temperature` `topP`。`thinkingConfig`：`includeThoughts` `thinkingBudget` `thinkingLevel`（`MINIMAL` `LOW` `MEDIUM` `HIGH`；Gemini 3+，更早模型会报错）[16] | 独立 `POST ...:streamGenerateContent`，不是 body 里的 `stream`。总览称 SSE；指南加 `alt=sse`。省略 `alt=sse` 时的帧格式没有原句 [16][17][19] | `candidates[].content`。`usageMetadata`：`promptTokenCount` `cachedContentTokenCount` `candidatesTokenCount` `toolUsePromptTokenCount` `thoughtsTokenCount` `totalTokenCount`。`finishReason` 含 `STOP` `MAX_TOKENS` `SAFETY` `MALFORMED_FUNCTION_CALL` `MISSING_THOUGHT_SIGNATURE` 等 [16] | `generationConfig.responseMimeType`：`text/plain`（默认）、`application/json`、`text/x.enum`。schema 字段见第 5 节 [16] |

Chat 与 Responses 的关系：Chat Completions remains supported, Responses is recommended for all new projects。弃用列表没有把 Chat Completions 划成 legacy。[4][5]

## 3. 变体与适配层

官方兼容层也算适配，不是新谱系。

| 适配 | 对着谁 | 文档写明的差异 |
|---|---|---|
| DeepSeek Chat | Chat Completions | Base `https://api.deepseek.com/chat/completions`，无 `/v1`，Bearer。多轮拼接全部历史。`role`：`system` `user` `assistant` `tool`。`reasoning_content` 与 `content` 同级，仅思考模式；请求里要带它必须 `prefix=true`。无 `tools` 时该字段被忽略；有 `tools` 不回传则 400。思考模式里 `tool_choice` 的 `required` 和具名选择返回 400。`max_tokens` 1–393216，默认非思考 8K、思考 64K（`reasoning_effort=max` 时 128K）。`reasoning_effort`：`none` 关思考，`low`/`high`/`max` 开思考，默认 `high`（与另一页的 `ultra` 冲突，见第 5 节）。流以 `data: [DONE]` 结束。`finish_reason`：`stop` `length` `content_filter` `tool_calls` `insufficient_system_resource` `aborted`。用量含 `prompt_cache_hit_tokens` + `prompt_cache_miss_tokens`。`response_format` 只能 `text` 或 `json_object`。presence/frequency penalty「no longer supported」，传入不生效。模型现为 `deepseek-flash` 与 `deepseek-v4-pro`，默认思考；`deepseek-chat` / `deepseek-reasoner` 自 2026-07-24 15:59 UTC 起不可访问 [20][21][24][25][26] |
| DeepSeek Responses | Responses | `POST /responses`，「OpenAI Responses API format」，base 仍是 `https://api.deepseek.com`。**无状态：responses and conversations are not stored on the server。** 不支持的参数静默忽略，点名含 `previous_response_id`、`store`、`truncation`、`prompt_cache_key`、`stream_options`。`developer` 当作 `user`；`instructions` 插成第一条 system。`max_output_tokens` 含推理 token。流没有 `data: [DONE]`，思维与正文分事件。思维是位于 message 之前的 `reasoning` item。`output_tokens_details.reasoning_tokens` 为思维链 token。`text.format` 在 `json_schema` 时要 schema。指南把 tool 写成 Supported，与 Chat 思考模式的 400 不是同一页 [22][23] |
| 智谱 Messages | Messages | `curl https://open.bigmodel.cn/api/anthropic/v1/messages`，头 `x-api-key` 与 `content-type`。未写 `anthropic-version`。原文：「某些场景下智谱与 Claude 接口仍存在差异，但不影响整体兼容性。」无字段表，因此块类型、`tool_result`、`stop_reason`、事件名都还不能对照。Claude Code 文档改用 `ANTHROPIC_AUTH_TOKEN`，base 仍是 `https://open.bigmodel.cn/api/anthropic` [27] |
| 智谱 Chat | Chat Completions | `POST https://open.bigmodel.cn/api/paas/v4/chat/completions`，Bearer。`messages` 是本次完整上下文。角色 `system` `user` `assistant` `tool`，系统指令在 messages 里。图片块是 `image_url`。思维在 `reasoning_content`。`clear_thinking` 默认 true，保留须原样按序透传。`tool_choice` 仅 `auto`。流以 `data: [DONE]` 结束。结束字段是 `finish_reason`（含 `sensitive` `network_error`），不是 `stop_reason`。`response_format.type` 文档写「三种」，列出的只有 `text` 与 `json_object`。GLM-5.3 的 `thinking.type=disabled` 会失败，Coding Plan 却把 disabled 收成 `low`（第 5 节）。1M 上下文的模型 id 加后缀 `[1m]` [28][29][30][31][32][33] |
| 百炼 compatible-mode | Chat Completions | 北京：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`，Bearer。Key 绑定地域，跨地域 401。`role`：`system` `user` `assistant` `tool`。`role=tool` 要 `tool_call_id`。`reasoning_content` 禁止拼进 `content`；`preserve_thinking` 默认 false（`extra_body`）。`max_tokens` 即将废弃，改 `max_completion_tokens`。`enable_thinking` 在 HTTP body 顶层，Python SDK 放 `extra_body`；`thinking_budget` 只写 `extra_body`。`delta.reasoning_content` 为增量。`response_format` 含 `json_schema`。Qwen 不支持 `tool_choice=required`。Qwen-Audio 只用 DashScope，不走兼容模式。主机名中英文页不一致（第 5 节）[34][35] |
| Moonshot | Chat Completions | `https://api.moonshot.cn/v1` 与 `https://api.moonshot.ai/v1` 的 `POST /v1/chat/completions`，Bearer。无状态重放。`reasoning_content` 必须留在 `messages`。末条 assistant 的 `partial: true` 做前缀续写。`max_tokens` 弃用，改 `max_completion_tokens`。`temperature` 被固定（k3 为 1.0；k2.6 思考 1.0 / 非思考 0.6），其他值报错。`data: [DONE]`。`response_format` 含 `json_schema`。K3 的 `reasoning_effort`=`low`/`high`/`max`（默认 `max`）；K2.x 的 `thinking` 走 `extra_body`。`content` 里的 `prompt_cache_breakpoint` → 400。公网图片 URL 两页矛盾（第 5 节）[36][37][38] |
| Gemini 官方 OpenAI 层 | Chat Completions | `POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`，Bearer，body 用 `messages`，流式是 `"stream": true`，不是 `:streamGenerateContent`。未使用 OpenAI 库时，官方建议直接调 Gemini API。图片接口里未列出的参数会被静默忽略 [18] |
| Anthropic 官方 OpenAI SDK 层 | 调用方用 OpenAI SDK 打 Messages | `base_url` `https://api.anthropic.com/v1/`。不是长期生产方案。多数不支持字段静默忽略，而不是报错；`response_format` 被忽略。限流仍按 `/v1/messages` [14] |

## 4. 用户需要知道的坑

按接错就 400 或静默丢字段的概率排。

1. **思维字段不回放，或回放到错误的键。** DeepSeek：有 `tools` 却不回传 `reasoning_content` → 400；没有 `tools` 则即使回传也会被忽略，不进上下文 [24]。百炼：不要把 `reasoning_content` 拼进 `content`；默认不保留历史思维 [34]。Moonshot：丢掉 `reasoning_content` 可能丢上下文 [36]。智谱 Chat：`clear_thinking` 默认 true，保留时必须未修改、按原顺序放回 `messages` [29]。处理：把厂商的思维字段当作对话状态的一部分存下来，不要只存 `content`。
2. **工具结果的角色不能跨谱系复用。** Chat 系是 `role=tool` 加 `tool_call_id`（DeepSeek、智谱 Chat、百炼、Moonshot 的文档都这样写）[21][29][34][36]。Messages 是后续 user 消息里的 `tool_result`，对的是 `tool_use` [8]。Responses 是 `function_call_output`，对的是 `function_call` [6]。generateContent 是 `functionResponse` part，`response` 为 JSON [16]。处理：网关按谱系转换，不要假设大家都认 `role=tool`。
3. **结束标记不同。** OpenAI Chat、DeepSeek Chat、智谱 Chat、Moonshot 以 `data: [DONE]` 结束 [1][21][32][36]。DeepSeek Responses 写明没有这行 [23]。Messages 以 `event: message_stop` 结束 [12]。Gemini 原生走 `:streamGenerateContent`，兼容层才用 `"stream": true` [16][18]。处理：按端点选解析器，不要用同一个「读到 `[DONE]`」循环打全部厂商。
4. **长度字段改名，旧名在推理模型上失效或即将废弃。** OpenAI Chat：`max_tokens` 不兼容 o-series，改 `max_completion_tokens`（含 reasoning tokens）[1]。Responses：`max_output_tokens`，同样含 reasoning tokens [6]。百炼、Moonshot 也把 `max_tokens` 标成弃用，改 `max_completion_tokens` [34][36]。Messages 仍叫 `max_tokens`，并且思考预算必须小于它 [8]。处理：按谱系填长度字段；推理 token 算在上限里面。
5. **不支持的参数有的 400，有的静默忽略。** DeepSeek Responses：不支持的参数不报错，其中包括 `previous_response_id`（所以看起来像接上了上一轮，其实没有）[23]。Anthropic 的 OpenAI 兼容层：多数不支持字段静默忽略 [14]。Gemini 图片兼容层：未列出的参数静默忽略 [18]。相反，Moonshot 传入非固定 `temperature` 会报错；`prompt_cache_breakpoint` 出现在 `content` 里会 400 [36][38]。处理：把「没报错」当成「可能被丢掉」，对状态类字段（`previous_response_id`、`store`）要看厂商有没有写明忽略。
6. **`tool_choice` 子集比 OpenAI 小，思考模式更小。** 智谱 Chat 仅 `auto` [29]。百炼：Qwen 不支持 `required`，思考模式不能强制指定工具 [34]。DeepSeek Chat 思考模式：`required` 和具名选择 400 [21]。Moonshot：k2.6 与 k2.7-code 不支持 `required`（与参考页「required 强制调用」冲突，见第 5 节）[36][38]。处理：强制选工具前先看模型和思考开关，不要默认 OpenAI 的 `required` 到处可用。
7. **智谱的「Claude 兼容」和「Chat 兼容」是两条 base URL。** Messages 在 `/api/anthropic`，Chat 在 `/api/paas/v4`。订过 Coding Plan（含过期）的模型说明写「暂时只能通过 OpenAI Chat Completion」，与 Coding Plan 页「两种协议都支持」冲突 [30]。处理：先确认账号走哪条 URL，不要把 Anthropic SDK 的默认 `api.anthropic.com` 只改模型名。

## 5. 未决与置信度

官方页之间打架、还没判的：

- OpenAI `store` 默认值：OpenAPI 写默认 false；迁移指南写新账号默认存储 [2][4]。迁移指南里「GPT-5.4 起非 `none` 的 `reasoning_effort` 不能 tool calling」只有半句原句，未写入第 2 节 [4]。
- OpenAI Chat 的 tools：同页既写只支持 `function`，又出现 custom tools [1]。
- Responses 的 `input` 同页一处写 file、一处写 audio [6]。usage 的 JSON 键名和 SSE 事件全名没有单独原句，不写入第 2 节。
- Anthropic：散文「没有 system role」对上 schema 的 `user|assistant|system`，也对上「不能是 messages 第一条」和兼容层「只支持一条起始 system」[8][11][14]。`temperature` 停用范围：参考写 Opus 4.6 之后，指南写 4.7 及以后 [8]。`tool_choice` 枚举、`stop_reason` 全表、除 `message_stop` 外的事件名，原句没覆盖全表。
- Gemini：鉴权头 `x-goog-api-key` 对上 shell 的 `?key=` [16][17]。role 只能 user/model，对上 `function` role [16]。`responseSchema` 标 deprecated，shell 仍在发；`responseJsonSchema` 的说明写成 "Use responseJsonSchema rather than this field"；`_responseJsonSchema` 又说自己是 JSON Schema 替代 [16]。省略 `alt=sse` 时是不是 JSON 数组，没有原句。未核 `v1` 与 `v1beta` 是否并列。
- DeepSeek：思考页把 OpenAI 的 `reasoning_effort` 说成 `low`/`high`/`max` 且 `ultra`→`max`；Chat/Responses 参考是 `none`/`low`/`high`/`max`，不提 `ultra` [21][24]。penalty 是「思考模式不支持」还是「全局不再支持」，两页用词不同 [21][24]。Chat 思考模式的 tool_choice 400，对上 Responses 指南的 Supported [21][23]。`max_tokens` 与 `temperature`「思考模式不生效」被摘进同一句，主语按笔记是 temperature。Chat 是否接受 `developer`、`json_schema`、`max_completion_tokens`，页面没写。
- 智谱 Messages：D2–D9 没有字段表。已查兼容介绍、`llms.txt`、OpenAPI（没有 `/anthropic` 路径）。不能把「没写 anthropic-version」写成「禁止该头」。`reasoning_content` 的 schema 写仅 glm-4.5 / glm-4.1v-thinking 返回，思考指南的 glm-5.3 示例又在读它 [29][31]。Coding Plan 与通用 API 对 `thinking.type=disabled` 的行为相反 [30][33]。两份 Claude Code 页的默认 Opus 模型一个写 GLM-4.7，一个写 GLM-5.3-Flash。
- 百炼：英文概览把北京写成 `ap-southeast-1`，中文页是 `cn-beijing`；弗吉尼亚主机两页也不同。概览写 tools 不能与 `stream=True` 同用、system 只在 `messages[0]`；Chat 专页写 `tool_stream` 可在 `stream=true` 时用，并有 `role=tool`。第 3 节采用 Chat 专页 [34][35]。
- Moonshot：总述「只换 base_url 和 Key」对上同页的 `thinking`/`partial` 和固定采样 [37][38]。`tool_choice=required` 在参考页是合法值，模型页写 k2.6 与 k2.7-code 会报错 [36][38]。图片一处写可传 URL，视觉页写不支持 [36]。

还没进矩阵、下一轮才核的范围内对象：MiniMax 的 Messages、xAI 的 Responses（是否真存 30 天）、Gemini Interactions（`previous_interaction_id`）、百炼的 Anthropic 与 Responses 兼容页。Mistral Conversations、Bedrock 四族、Cohere `/v2/chat` 是另一套原生协议，只有线索。

页面日期：Gemini generateContent 参考标 2026-09-22 UTC，API 总览 2026-09-04，OpenAI 兼容页 2026-09-02 [16][17][18]。百炼中文 Chat 页 last-modified 2026-09-22 [34]。OpenAI、Anthropic、DeepSeek、智谱、Moonshot 的已开页多数没有「最后更新」行。OpenAI 的 `platform.openai.com` 参考返回 403，主张来自 `developers.openai.com` 与官方 OpenAPI。

## 来源

[1] OpenAI Chat reference — https://developers.openai.com/api/reference/resources/chat.md
[2] OpenAI OpenAPI — https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml
[3] OpenAI API overview — https://developers.openai.com/api/reference/overview.md
[4] OpenAI migrate to Responses — https://developers.openai.com/api/docs/guides/migrate-to-responses.md
[5] OpenAI deprecations — https://developers.openai.com/api/docs/deprecations.md
[6] OpenAI Responses create — https://developers.openai.com/api/reference/resources/responses/methods/create/
[7] OpenAI conversation state — https://developers.openai.com/api/docs/guides/conversation-state
[8] Anthropic Messages — https://platform.claude.com/docs/en/api/messages
[9] Anthropic API overview — https://platform.claude.com/docs/en/api/overview
[10] Anthropic versioning — https://platform.claude.com/docs/en/api/versioning
[11] Anthropic working with messages — https://platform.claude.com/docs/en/build-with-claude/working-with-messages
[12] Anthropic streaming — https://platform.claude.com/docs/en/build-with-claude/streaming
[13] Anthropic structured outputs — https://platform.claude.com/docs/en/build-with-claude/structured-outputs
[14] Anthropic OpenAI SDK compat — https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk
[16] Gemini generateContent — https://ai.google.dev/api/generate-content
[17] Gemini API overview — https://ai.google.dev/api
[18] Gemini OpenAI compatibility — https://ai.google.dev/gemini-api/docs/openai
[19] Gemini text generation — https://ai.google.dev/gemini-api/docs/generate-content/text-generation
[20] DeepSeek 文档首页 — https://api-docs.deepseek.com/
[21] DeepSeek create chat completion — https://api-docs.deepseek.com/api/create-chat-completion
[22] DeepSeek create response — https://api-docs.deepseek.com/api/create-response
[23] DeepSeek Responses 指南 — https://api-docs.deepseek.com/guides/responses_api
[24] DeepSeek thinking mode — https://api-docs.deepseek.com/guides/thinking_mode
[25] DeepSeek multi-round — https://api-docs.deepseek.com/guides/multi_round_chat
[26] DeepSeek 2026-04-24 公告 — https://api-docs.deepseek.com/news/news260424
[27] 智谱 Claude 兼容介绍 — https://docs.bigmodel.cn/cn/guide/develop/claude/introduction
[28] 智谱 HTTP 介绍 — https://docs.bigmodel.cn/cn/guide/develop/http/introduction
[29] 智谱对话补全 — https://docs.bigmodel.cn/api-reference/模型-api/对话补全
[30] 智谱 GLM-5.3 — https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3
[31] 智谱思考 — https://docs.bigmodel.cn/cn/guide/capabilities/thinking
[32] 智谱流式 — https://docs.bigmodel.cn/cn/guide/capabilities/streaming
[33] 智谱 Coding Plan 模型 — https://docs.bigmodel.cn/cn/coding-plan/latest-model
[34] 百炼 OpenAI Chat — https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions
[35] 百炼兼容概览 — https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope
[36] Moonshot Chat — https://platform.kimi.com/docs/api/chat
[37] Moonshot 概览 — https://platform.kimi.com/docs/api/overview
[38] Moonshot 模型概览 — https://platform.kimi.com/docs/api/models-overview
