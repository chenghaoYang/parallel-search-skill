# LLM 请求协议：谱系，以及「兼容」改了什么

> 回答四套种子协议差在哪，DeepSeek 的 response 相对 OpenAI 文档差在哪，智谱的 message 相对 Anthropic 差在哪。截至 2026-09-23。先读第 0 节；第 2 节是四套种子；第 3 节是适配层，外加 Google 后来写的 Interactions。

## 0. 一屏看懂

1. 先看两件事：下一轮历史放在哪，以及一条内容是字符串还是带 `type` 的块。Chat Completions 重放 `messages[]`。Responses 可以改走 `previous_response_id`。Messages 也重放消息，但系统指令在顶层 `system`，工具结果是 user 内容里的 `tool_result`。generateContent 重放 `contents[].parts[]`，系统指令在 `systemInstruction`，角色是 `user` / `model`。
2. OpenAI 仍支持 Chat Completions，新项目推荐 Responses。换的不是只改 URL：长度字段变为 `max_output_tokens`，JSON 从 `response_format` 改到 `text.format`，工具结果是 `function_call_output`，不是 `role=tool`。[4][6]
3. DeepSeek 两套都有：`POST https://api.deepseek.com/chat/completions` 与 `POST /responses`，无 `/v1`，Bearer，自称兼容 OpenAI/Anthropic。Responses **不存会话**，`previous_response_id` 与 `store` 被静默忽略。Chat 的 `response_format` 只有 `text`/`json_object`；`json_schema` 在 Responses 的 `text.format`。思维是 Chat 的 `reasoning_content` 或 Responses 的 `reasoning` item；有 `tools` 不回传 `reasoning_content` 会 400。`finish_reason` 多 `insufficient_system_resource`、`aborted`。`developer` 在 Responses 里当成 `user`。Chat 思考模式里 `tool_choice` 的 `required`/具名会 400；Responses 写明 Supported。penalty 在 Chat 参考是全局失效，思考页写成仅思考模式（第 5 节）。[21][22][23][24]
4. 智谱 Messages 有路径 `POST https://open.bigmodel.cn/api/anthropic/v1/messages`（示例头 `x-api-key`），承认与 Claude 有差异，但 sitemap 236 条里没有字段页：块类型、`stop_reason`、事件名都是官方未写。能逐字段看的是 Chat：`POST https://open.bigmodel.cn/api/paas/v4/chat/completions`。公开了 Messages 差异清单的是 MiniMax：`POST https://api.minimax.cn/anthropic/v1/messages`，`tool_choice` 仅 `auto`/`none`，忽略 `top_k`、`stop_sequences`、`mcp_servers`、`context_management`、`container`。[27][29][39][40][41][49]
5. 适配层最常踩的是思维旁路，不是 URL。DeepSeek 有工具时必须回传 `reasoning_content`。百炼禁止把它拼进 `content`，`preserve_thinking` 默认 false。Moonshot 要求每一轮 assistant 的 `reasoning_content` 原样留在 `messages`。智谱 Chat 的 `clear_thinking` 默认 true，要保留必须原样透传。[24][29][34][36]
6. 「换成 base_url 就能用」只在文档的总述里成立。Moonshot 把 `temperature` 等固定，传入其他值会报错，并在末条 assistant 上使用 `partial`。百炼的 `enable_thinking` 在 HTTP body 顶层（Python SDK 走 `extra_body`），Qwen 不支持 `tool_choice=required`。智谱 Chat 的 `tool_choice` 文档写默认且仅 `auto`。[29][34][37][38]
7. Google 在 generateContent 之外又写了 Interactions：`POST /v1beta/interactions` 与 `/v1/interactions`，用 `previous_interaction_id` 取历史，工具结果是 `function_result`，流式是同一 URL 的 `"stream": true`。总览写 2026-06 起 GA 并推荐新项目；参考页 2026-09-22 仍标 Beta；一份 md 写生产应继续用 generateContent。三句话并存，见第 5 节。OpenAI 形状的旁路仍是 `/v1beta/openai/chat/completions`。[18][42][43][44]

## 1. Taxonomy

分类轴：历史接在客户端还是服务端 id 上；内容是纯字符串还是带类型的块。同形不等于同一状态机：DeepSeek 的 `/responses` 用了 Responses 的字段名，但写明不存会话。

| 家族 | 历史怎么接 | 系统指令 | 工具结果 | 流式结束 |
|---|---|---|---|---|
| Chat Completions | 客户端重放 `messages` | `messages` 里的 `system` / `developer` | `role=tool` | SSE，`data: [DONE]` |
| Responses | 本次 `input`，或 `previous_response_id` / `conversation` | 顶层 `instructions` | `type=function_call_output` | SSE（OpenAI 事件全名未逐条摘句） |
| Messages | 客户端重放完整 `messages` | 顶层 `system` | user 消息里的 `tool_result` | SSE，`event: message_stop` |
| generateContent | 客户端重放 `contents` | `systemInstruction` | `functionResponse` part | 另一个方法 `:streamGenerateContent` |
| Interactions | `previous_interaction_id`，或 `store=false` 时重放 `input` | 未单列（本轮不展开） | `type=function_result` | 同一 POST，`stream: true`；指南有 `data: [DONE]` |

适配层不单列家族。同形不等于会存状态：DeepSeek `/responses` 静默忽略 `previous_response_id`。最常见的厂商附加字段是 `reasoning_content`。

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
| generateContent | `tools[].functionDeclarations`。下一轮 `functionResponse`（`response` 为 JSON）。`FunctionCall` 有 `id` `name` `args`。另有 role `"function"`，与 user/model 冲突 [16] | `generationConfig`：`maxOutputTokens` `temperature` `topP`。`thinkingConfig.thinkingLevel`：`MINIMAL` `LOW` `MEDIUM` `HIGH`（Gemini 3+）[16] | 独立 `:streamGenerateContent`，不是 body 开关。总览称 SSE；指南加 `alt=sse` [16][17][19] | `candidates[].content`。`usageMetadata` 用 `promptTokenCount`、`candidatesTokenCount`、`thoughtsTokenCount`、`totalTokenCount`。`finishReason` 含 `STOP`、`MAX_TOKENS`、`MISSING_THOUGHT_SIGNATURE` [16] | `responseMimeType`：`text/plain`、`application/json`、`text/x.enum`。schema 字段见第 5 节 [16] |

Chat 与 Responses 的关系：Chat Completions remains supported, Responses is recommended for all new projects。弃用列表没有把 Chat Completions 划成 legacy。[4][5]

## 3. 变体与适配层

官方兼容层也算适配，不是新谱系。

| 适配 | 对着谁 | 文档写明的差异 |
|---|---|---|
| DeepSeek Chat | Chat Completions | `https://api.deepseek.com/chat/completions`，无 `/v1`。`reasoning_content` 与 `content` 同级；无 `tools` 则忽略，有 `tools` 不回传则 400；请求里携带须 `prefix=true`。思考模式 `tool_choice` 的 `required`/具名 → 400，须先关掉思考。`reasoning_effort`：`none` 关，`low`/`high`/`max` 开；`minimal`→`low`，`medium`/`xhigh`→`high`（思考页 OpenAI 列没有 `none`，见第 5 节）。`max_tokens` 默认非思考 8K、思考 64K（`max` 时 128K），上限 393216。`finish_reason` 另有 `insufficient_system_resource`、`aborted`。用量含 `prompt_cache_hit_tokens` 与 `prompt_cache_miss_tokens`。`response_format` 只有 `text`/`json_object`。penalty 全局不再支持。`deepseek-chat`/`deepseek-reasoner` 自 2026-07-24 15:59 UTC 起不可访问；现为 `deepseek-flash` 与 `deepseek-v4-pro`，默认思考 [20][21][24][26] |
| DeepSeek Responses | Responses | `POST /responses`，base `https://api.deepseek.com`。**responses and conversations are not stored。** `previous_response_id`、`store`、`truncation`、`prompt_cache_key`、`stream_options` 静默忽略。`developer` 当作 `user`。`reasoning.effort`：`none`/`low`/`high`/`max`（`none` 关思考）；`minimal`→`low`，`medium`/`xhigh`→`high`。`tool_choice` Supported：`none`/`auto`/`required`/具名，参考页没有 400。无 `data: [DONE]`。思维是 message 前的 `reasoning` item。`text.format` 支持 `json_schema`。这两页没有 penalty 参数名 [22][23] |
| 智谱 Messages | Messages | `POST https://open.bigmodel.cn/api/anthropic/v1/messages`，示例头 `x-api-key`。原文承认有差异但没有清单。sitemap 236 条里含 claude 的只有介绍页（lastmod 2026-09-23）；`/api-reference/模型-api/anthropic` 与 `/cn/guide/develop/claude/messages` 为 404。D2–D9 记为官方未写。Claude Code 页只映射 `thinking.type` 与 `output_config.effort`，不是 Messages 字段表 [27][33][49] |
| 智谱 Chat | Chat Completions | `POST https://open.bigmodel.cn/api/paas/v4/chat/completions`，Bearer。系统指令在 `messages` 的 `system`，不是顶层字段。思维在 `reasoning_content`；`clear_thinking` 默认 true。`tool_choice` 仅 `auto`。结束字段是 `finish_reason`（含 `sensitive`），不是 `stop_reason`。`response_format` 只列出 `text` 与 `json_object`。`thinking.type=disabled` 在通用 API 失败，Coding Plan 收成 `low`（第 5 节）[28][29][31][33] |
| 百炼 compatible-mode | Chat Completions | 北京 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`，Bearer，Key 绑定地域。`reasoning_content` 禁止拼进 `content`；`preserve_thinking` 默认 false。`enable_thinking` 在 HTTP body 顶层（Python 用 `extra_body`）。`max_tokens` 即将废弃，改 `max_completion_tokens`。Qwen 不支持 `tool_choice=required`。Qwen-Audio 不走兼容模式。主机名见第 5 节 [34][35] |
| Moonshot | Chat Completions | `api.moonshot.cn/v1` 与 `api.moonshot.ai/v1` 的 `POST /v1/chat/completions`。`reasoning_content` 必须留在 `messages`。末条 assistant 可 `partial: true`。`temperature` 被固定（k3 为 1.0），其他值报错。K3 的 `reasoning_effort`=`low`/`high`/`max`（默认 `max`）。`prompt_cache_breakpoint` 出现在 `content` → 400 [36][37][38] |
| MiniMax Messages | Messages | `POST https://api.minimax.cn/anthropic/v1/messages`。Bearer 与 `x-api-key` 并存时优先 Bearer。历史在 `messages`；`signature` 须原样回带。`tool_choice` 仅 `auto`/`none`。`thinking.type` 仅 `disabled`/`adaptive`（M3 的 adaptive=开启；M2.x 无法关闭）。忽略 `top_k`、`stop_sequences`、`mcp_servers`、`context_management`、`container`。image/video 仅 M3。delta 为 `text_delta`/`thinking_delta`/`signature_delta`，结束于 `message_stop`。无 JSON schema 字段。未写 `anthropic-version` 是否必填 [39][40][41] |
| Gemini Interactions | 官方另一套 | `POST https://generativelanguage.googleapis.com/v1beta/interactions` 与 `/v1/interactions`。`previous_interaction_id` 由服务端取历史；`store=false` 与该续写不兼容。结果块恒为 `function_result`，不是 `functionResponse`。`stream` 在 body 里；指南有 `data: [DONE]`。JSON 用顶层 `response_format`。是否取代 generateContent，见第 5 节 [42][43][44][46] |
| Gemini 官方 OpenAI 层 | Chat Completions | `POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`，Bearer，`messages`，`"stream": true`。未用 OpenAI 库时官方建议直接调 Gemini API。图片接口未列出的参数静默忽略 [18] |
| Anthropic 官方 OpenAI SDK 层 | 调用方用 OpenAI SDK 打 Messages | `base_url` `https://api.anthropic.com/v1/`。不是长期生产方案。多数不支持字段静默忽略，而不是报错；`response_format` 被忽略。限流仍按 `/v1/messages` [14] |

## 4. 用户需要知道的坑

按接错就 400 或静默丢字段的概率排。

1. **思维字段不回放，或回放到错误的键。** DeepSeek：有 `tools` 却不回传 `reasoning_content` → 400；没有 `tools` 则即使回传也会被忽略，不进上下文 [24]。百炼：不要把 `reasoning_content` 拼进 `content`；默认不保留历史思维 [34]。Moonshot：丢掉 `reasoning_content` 可能丢上下文 [36]。智谱 Chat：`clear_thinking` 默认 true，保留时必须未修改、按原顺序放回 `messages` [29]。处理：把厂商的思维字段当作对话状态的一部分存下来，不要只存 `content`。
2. **工具结果的角色不能跨谱系复用。** Chat 系是 `role=tool` [21][29][34]。Messages 是 user 消息里的 `tool_result` [8]。Responses 是 `function_call_output` [6]。generateContent 是 `functionResponse` [16]。Interactions 是 `function_result` [43]。处理：按谱系转换。
3. **结束标记不同。** OpenAI Chat、DeepSeek Chat、智谱 Chat、Moonshot 以 `data: [DONE]` 结束 [1][21][32][36]。DeepSeek Responses 写明没有这行 [23]。Messages 以 `event: message_stop` 结束 [12]。Gemini 原生走 `:streamGenerateContent`，兼容层才用 `"stream": true` [16][18]。处理：按端点选解析器，不要用同一个「读到 `[DONE]`」循环打全部厂商。
4. **长度字段改名，旧名在推理模型上失效或即将废弃。** OpenAI Chat：`max_tokens` 不兼容 o-series，改 `max_completion_tokens`（含 reasoning tokens）[1]。Responses：`max_output_tokens`，同样含 reasoning tokens [6]。百炼、Moonshot 也把 `max_tokens` 标成弃用，改 `max_completion_tokens` [34][36]。Messages 仍叫 `max_tokens`，并且思考预算必须小于它 [8]。处理：按谱系填长度字段；推理 token 算在上限里面。
5. **不支持的参数有的 400，有的静默忽略。** DeepSeek Responses 忽略 `previous_response_id`，不报错，所以并没有接上上一轮 [23]。MiniMax 忽略 `top_k`、`stop_sequences`、`mcp_servers` 等 [40]。Anthropic 的 OpenAI 兼容层多数不支持字段也静默忽略 [14]。Moonshot 的非固定 `temperature` 会报错 [38]。处理：状态类字段没报错，不等于生效。
6. **`tool_choice` 子集比 OpenAI 小，思考模式更小。** 智谱 Chat 仅 `auto` [29]。百炼：Qwen 不支持 `required`，思考模式不能强制指定工具 [34]。DeepSeek Chat 思考模式：`required` 和具名选择 400 [21]。Moonshot：k2.6 与 k2.7-code 不支持 `required`（与参考页「required 强制调用」冲突，见第 5 节）[36][38]。处理：强制选工具前先看模型和思考开关，不要默认 OpenAI 的 `required` 到处可用。
7. **智谱的 Claude 兼容和 Chat 兼容是两条 base URL**（`/api/anthropic` 与 `/api/paas/v4`）。订过 Coding Plan 的说明写模型 API 只能走 Chat，与「两种协议都支持」冲突 [30]。先确认账号走哪条 URL。

## 5. 未决与置信度

还没判、且会改变接法的：

- Interactions 是否取代 generateContent：总览（2026-09-17）写 2026-06 起 GA，recommended for all new projects，并称 generateContent legacy。参考（2026-09-22）写 You are viewing the beta version。`interactions.md.txt` 写 currently in Beta，生产继续用 generateContent。未裁决 [42][44]。
- generateContent 的 schema 字段收不成一个名字：`responseSchema` 标 deprecated，`responseJsonSchema` 写 "Use responseJsonSchema rather than this field"，迁移页仍写 `response_schema`。Interactions 则是顶层 `response_format` [16][43][45]。
- DeepSeek `reasoning_effort`：思考页 OpenAI 列只有 `low/high/max`；Chat API 还有 `none`（关闭）。ultra→max 只在思考页脚注，参数页没有 ultra [21][24]。penalty：思考页限思考模式且不报错；Chat 参考写不再支持 [21][24]。
- Anthropic 散文没有 system role，schema 却列了 `system` [8]。`temperature` 停用范围：Opus 4.6 之后，对上指南的 4.7 及以后 [8]。
- OpenAI `store` 默认 false（OpenAPI）对上新账号默认存储（迁移指南）[2][4]。Responses 的 usage 键名和 SSE 事件全名没有单独原句。
- 智谱：不能把「没写 anthropic-version」写成禁止该头。订过 Coding Plan 的模型页写模型 API 只能走 Chat，切换模型页仍让 Claude Code 用 `/api/anthropic` [30][33]。`thinking.type=disabled` 在通用 API 失败，在 Coding Plan 收成 `low` [30][33]。
- 百炼北京主机：中文页 `cn-beijing`，英文概览写成 `ap-southeast-1`。概览禁止 tools 与 stream 同用；Chat 专页允许 `tool_stream`。第 3 节用 Chat 专页 [34][35]。
- Moonshot：`tool_choice=required` 在参考页合法，k2.6 与 k2.7-code 传入会报错。图片一处可传 URL，视觉页不支持 [36][38]。
- MiniMax：SDK 写 tool_choice 完全支持，OpenAPI 写仅 `auto`/`none`。`max_tokens` 说明里的中断原因 `length`，对上 `stop_reason` 的 `end_turn`/`max_tokens`/`tool_use` [40][41]。

未进矩阵：百炼的 Anthropic / Responses 页、xAI Responses、Mistral Conversations、Bedrock、Cohere `/v2/chat`。MiniMax 额外 role 的枚举没有被摘录句覆盖，不写入第 3 节。

页面日期：generateContent 与 Interactions beta 参考为 2026-09-22，总览 2026-09-17，百炼 Chat 页 last-modified 2026-09-22 [16][34][42][44]。OpenAI 的 platform.openai.com 返回 403，主张来自 developers.openai.com。

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
[39] MiniMax 文本生成 — https://platform.minimaxi.com/docs/guides/text-generation
[40] MiniMax Anthropic 兼容说明 — https://platform.minimaxi.com/docs/api-reference/text-anthropic-api
[41] MiniMax Messages OpenAPI — https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json
[42] Gemini Interactions beta — https://ai.google.dev/api/interactions-api
[43] Gemini Interactions v1 — https://ai.google.dev/api/interactions-api-v1
[44] Gemini Interactions 总览 — https://ai.google.dev/gemini-api/docs/interactions-overview
[45] 迁到 Interactions — https://ai.google.dev/gemini-api/docs/migrate-to-interactions
[46] Gemini 流式 — https://ai.google.dev/gemini-api/docs/streaming
[49] 智谱 sitemap — https://docs.bigmodel.cn/sitemap.xml
