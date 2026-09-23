# audit-a（审 §0 一屏看懂、§1 Taxonomy、§2 源头协议对照矩阵 2.1–2.3）
格式：判定 | 主张原文（从成稿摘） | 依据 | 建议改法。笔记文件都在 notes/ 下。"原页复核"指本轮 WebFetch（共 6 次，2026-09-23）。

supported | §0.1 OpenAI 称 "Responses is recommended for all new projects"，Assistants API 已于 2026-08-26 下线 [1] | r1-openai-chat.md [C13]；r1-openai-responses.md [C24]；原页复核 https://developers.openai.com/api/docs/guides/migrate-to-responses 原句 "The Assistants API was officially sunset on August 26, 2026, and is no longer available." | —
supported | §0.1 Gemini Interactions 2026-06 GA，generateContent 被称为 legacy [2] | r2-gemini-interactions.md [C1]；r1-scout.md [C1]；原页复核 https://ai.google.dev/gemini-api/docs/interactions（Last updated 2026-09-17） | —
supported | §0.1 Anthropic Messages 仍无状态 [3] | r1-anthropic-messages.md [C15] | —
supported | §0.2 有 Responses：`POST https://api.deepseek.com/responses`（无 `/v1`，2026-07-31 起）[4][5]；不存状态，`previous_response_id`/`store` 等被 "silently ignored" [4] | r1-deepseek.md [C4][C5][C6] | —
weak | §0.2 推理以明文 reasoning item 返回，不支持 `encrypted_content`/`summary` [5] | [5] 对应的 r1-deepseek.md [C9] 只能支撑"明文 reasoning item"；"summary and encrypted_content are not supported" 在 [C8]，其 src 是 [4] guides/responses_api | 引注改为 [4][5]
weak | §0.2 旧模型名 deepseek-chat/reasoner 已于 2026-07-24 停用 [6] | r1-deepseek.md [C3] 原句是将来时 "will be discontinued in three months (2026-07-24)"（2026-04-24 公告）；原页复核 https://api-docs.deepseek.com/updates：该条之后没有确认已停用的条目 | 改为"官方 2026-04-24 公告：将于 2026-07-24 停用（过渡期分别指向 deepseek-v4-flash 的非思考/思考模式）"
supported | §0.3 有 Anthropic 端点，无字段级兼容说明，只写"某些场景下…仍存在差异" [7] | r1-zhipu.md [C1][C2]（gaps：两站 llms-full.txt 全文检索 0 命中）；r2-zhipu-anthropic.md gaps | —
supported | §0.3 Claude 模型名被映射成 GLM [8]；Coding Plan 下服务端内置看图与联网搜索 [10][11] | r2-zhipu-anthropic.md [C1][C5][C6] | —
weak | §0.3 官方写明的多是服务端改写：…关闭思考被转成 low [9] | r1-zhipu.md [C8] 和 r2-zhipu-anthropic.md [C4] 都出自 coding-plan/latest-model，属于 Claude Code/Coding Plan 语境；r1-zhipu.md [C14] 写 GLM-5.3 传 disabled 会报错（标准 API）；两份笔记的 conflicts 都列了这对矛盾，并写明"按量 key 调 /api/anthropic 适用哪条没写" | 限定语"Claude Code/Coding Plan 下"不要只放在最后一项，要管住三项改写；再补半句"标准 API 下 GLM-5.3 传 disabled 会报错 [74]"
weak | §0.3 社区还报告了 system 角色 422、count_tokens 返回 0 等（§3.3） | r2-zhipu-anthropic.md [C8][C9][C16]，全部 secondary | 正文已标"社区"，可保留（低优先）；可补范围：422 见 open.bigmodel.cn，count_tokens=0 见 Z.ai + glm-5.3
supported | §0.4 `previous_response_id` 在智谱、Qwen、方舟可用；在 DeepSeek 被忽略，在 Kimi 恒为 null，在 OpenRouter 直接 400 | r2-cn-responses.md [C2][C10]；r1-qwen.md [C20]；r1-ark.md [C10]；r1-deepseek.md [C6]；r2-hosting.md [C3] | —
weak | §0.5 Gemini 3 漏回签名…直接 400 [12]（§2.2 generateContent「推理回传」格"Gemini 3 缺签名 → 400 [12]"同） | r1-gemini.md [C22] 和 r1-scout.md [C2] 的原句限定在 "the first functionCall part in any step of the current turn"；r2-origin-compat.md [C9] 限定在 "during function calling" | 改为"Gemini 3 函数调用时，当前轮漏回 functionCall 签名 → 400"；§2.2 那一格同样改
supported | §0.5 DeepSeek 带工具漏回 `reasoning_content` 都直接 400 [13] | r1-deepseek.md [C13] | —
supported | §0.6 GPT-6 在 effort ≠ none 时要求去掉 `temperature`/`top_p` [14] | r3-openai-gaps.md [C7]（Using GPT-6 页，无日期；原句还含 top_logprobs） | —
supported | §0.6 Claude Opus 4.7+ 等传非默认值即 400 [15] | r1-anthropic-messages.md [C21]；r1-scout.md [C10] | —
supported | §0.6 Gemini 2026-07-21 起弃用三者 [16] | r1-scout.md [C11]；原页复核 https://ai.google.dev/gemini-api/docs/changelog：July 21, 2026 条目原句 "The sampling parameters temperature, top_p and top_k are now deprecated." | —
weak | §0.7 "不支持"两极：静默忽略（DeepSeek、Anthropic 兼容层、MiniMax 多数参数）vs 报错（Kimi、MiniMax 温度越界、OpenRouter 状态字段） | 每个例子单独看都有出处：r1-deepseek.md [C6][C14]、r1-scout.md [C7]、r1-moonshot-minimax.md [C6][C7][C8][C21][C22][C28]、r2-hosting.md [C3]。但 DeepSeek 也会报错（r1-deepseek.md [C13][C19]：思考模式下 required/指定 tool_choice → 400），Kimi 也会忽略（r2-cn-responses.md [C15]：web_search 的 user_location 等被忽略），按厂商分两极说过头了 | 改成按场景分，例如"静默忽略（DeepSeek Responses 不支持的参数和思考模式采样参数、Anthropic 兼容层、MiniMax 多数参数）vs 报错（Kimi 固定采样参数、DeepSeek 思考模式强制 tool_choice、MiniMax 温度越界、OpenRouter 状态字段）"
supported | §0.8 OpenAI 的 prompt 计数含缓存，Anthropic 不含，DeepSeek 拆成 hit/miss | r1-scout.md [C21]；r1-anthropic-messages.md [C26]；r1-deepseek.md [C20] | —
supported | §1 CC 行：服务端状态「无」；流式「`data:` 块 + `[DONE]`」 | r1-openai-chat.md [C11][C19] | —
supported | §1 CC/Messages/Responses 三行「兼容实现」含"6 家国内厂商"及源头厂兼容层、网关、自托管、Bedrock、Vertex；要点"下游厂商多同时暴露 CC + Messages + Responses" | 六家三端点：r1-deepseek.md [C1][C4]；r1-zhipu.md [C1][C10] + r2-cn-responses.md [C1]；r1-moonshot-minimax.md [C1][C2][C18][C19] + r2-cn-responses.md [C8][C16]；r1-qwen.md [C1][C4][C5]；r1-ark.md [C1][C2][C29]。其余：r2-origin-compat.md [C1][C14]；r2-hosting.md [C1][C3][C4][C6][C7][C9]–[C18] | —
weak | §1 generateContent、Interactions 行「兼容实现」：仅 Google | 笔记里没有"只有 Google 实现"这条主张；r2-hosting.md 查过的网关、自托管、云托管都没提这两种协议。这是把"未见"写成了"没有" | 改为"调研范围内未见第三方实现"
supported | §1 Interactions 行：服务端状态「可选，默认存」；流式「语义事件 + `[DONE]`」 | r2-gemini-interactions.md [C11][C19]（[C11] 原句只有片段 "(store=true)"）；原页复核 https://ai.google.dev/gemini-api/docs/interactions 原句 "By default, the API stores all Interaction objects (`store=true`)…" | —
supported | §1 要点：二代的共同形状：扁平函数工具、以 `call_id` 关联的调用/结果条目、`store` 默认 true、`previous_*_id` 续接、background 异步、带 `queued`/`incomplete` 等状态 | Responses：r1-openai-responses.md [C6][C8][C10][C18]，r2-oa-responses-add.md [C7][C9]；Interactions：r2-gemini-interactions.md [C8][C9][C11][C12][C13][C20] | —
weak | §1 要点：一代内部只差消息切分粒度：整条消息 / 类型化块 / parts | 作者自己的归纳，没有出处；和本稿 §2 对不上：鉴权头、system 位置、工具结果角色都不同，Messages 还要求 max_tokens 必填（r1-anthropic-messages.md [C4]） | 改为"一代内部的对话结构主要差在消息切分粒度"
supported | §2.1 CC 容器/角色：`messages`：developer/system/user/assistant/tool；o1 起 developer 取代 system | r1-openai-chat.md [C3] | —
supported | §2.1 CC tool_choice：none/auto/required/指定/`allowed_tools` | r1-openai-chat.md [C8] | —
weak | §2.1 Responses：`input`（字符串或 items，角色同左）+ 顶层 `instructions` [1] | input/instructions 有 r1-openai-responses.md [C2] 支撑；但 [C4]（src 即 [19]）的角色枚举是 "One of user, assistant, system, or developer."，没有左格 CC 的 tool。"同左"这部分和笔记相反 | "角色同左"改为"角色 user/assistant/system/developer（无 tool，工具结果用 function_call_output 条目）"
supported | §2.1 Responses 工具定义：扁平 `{type:"function",name,parameters,strict}`，省略 strict 即尝试严格 [1] | r1-openai-responses.md [C6][C7] | —
supported | §2.1 Messages 鉴权：Bearer（`x-api-key` 为旧式回退）+ 必填 `anthropic-version` [24][25] | r1-anthropic-messages.md [C2][C3] | —
weak | §2.1 Messages：`messages` 仅 user/assistant（连续同角色合并）+ 顶层 `system` | r1-anthropic-messages.md [C5][C6] 能支撑；但 r1-scout.md conflicts 记了一处官方冲突：mid-conversation-system-messages 页写「You append a `{"role": "system"}` message」（Sonnet 5 不支持）。正文只取了一边，§5 也没列 | 加 ⚔ 注"另有 mid-conversation system messages，可在 messages 内追加 role:system（部分模型）"，并补进 §5 冲突清单
supported | §2.1 Messages 调用→回传：`tool_use{id,input}`（对象）→ user 内 `tool_result{tool_use_id}`，须紧跟且排最前 [30] | r1-anthropic-messages.md [C10][C11][C12] | —
supported | §2.1 generateContent 端点：`POST /v1beta/models/{model}:generateContent`（模型在 URL） | r1-gemini.md [C1]（页 2026-09-22） | —
supported | §2.1 generateContent tool_choice：`mode`：AUTO/ANY/NONE/VALIDATED [32] | r1-gemini.md [C16] | —
supported | §2.1 Interactions 端点：`POST /v1beta/interactions`（另有 v1）；body 放 `model` 或 `agent` | r2-gemini-interactions.md [C2][C4]（v1beta2 冲突 §5 已列） | —
supported | §2.1 Interactions：`input` + 顶层 `system_instruction`；无状态多轮回传上轮 `steps` [27] | r2-gemini-interactions.md [C5][C6] | —
supported | §2.1 Interactions 调用→回传：`function_call` step（status `requires_action`）→ `function_result{call_id,result,is_error}` | r2-gemini-interactions.md [C9][C20] | —
weak | §2.1 Interactions tool_choice：`generation_config.tool_choice` | r2-gemini-interactions.md [C17] 只在主张的括注里写了"另 seed、stop_sequences、tool_choice"，原句只讲 max_output_tokens | 补一条带 tool_choice 原句的笔记（低优先）
supported | §2.2 CC 推理控制：`reasoning_effort`：none/minimal/low/medium/high/xhigh/max | r1-openai-chat.md [C14] | —
supported | §2.2 CC 缓存：自动，GPT-5.6+ ≥ 1,024 tokens [35]；`prompt_cache_key` | r1-openai-chat.md [C23][C24] | —
supported | §2.2 Responses 历史：`store` 默认 true [1]；`previous_response_id` 与 `conversation` 互斥 [31]；默认存 30 天 [34] | r1-openai-responses.md [C10][C11]（conflicts 另引 conversation-state 原句 "Response objects are saved for 30 days by default."）；r2-oa-responses-add.md [C7] | —
weak | §2.2 Responses 缓存：官方称缓存利用率比 CC 高 40–80% [1] | r1-openai-responses.md [C21] 原句带 "in internal tests"；原页复核全句 "Results in lower costs due to improved cache utilization (40% to 80% improvement when compared to Chat Completions in internal tests)." | 改为"官方称内部测试中缓存利用率比 CC 提升 40–80%"
supported | §2.2 Responses 推理返回：reasoning item，默认带 `encrypted_content` [40] | r1-openai-responses.md [C12]；r1-scout.md [C5] | —
supported | §2.2 Messages 推理控制：`thinking.type`：enabled/disabled/adaptive + `output_config.effort`；4.7+ 用 `budget_tokens` 报 400 [39] | r1-anthropic-messages.md [C18][C19] | —
supported | §2.2 Messages 长度：`max_tokens` 必填 [44] | r1-anthropic-messages.md [C4] | —
supported | §2.2 generateContent 结构化输出：`responseFormat.text{mimeType,schema}`（`responseSchema` 已 deprecated） | r1-gemini.md [C23][C24] | —
weak | §2.2 generateContent 长度/采样：`maxOutputTokens`；temperature [0,2] | r1-gemini.md [C25] 能支撑取值；但 r1-scout.md [C11] 记了 2026-07-21 起弃用，r1-gemini.md conflicts 记了 Vertex 的 "aren't supported and are ignored if set"（3.6 Flash 起）。格内没提示，§5 也没列 | 格内加"（2026-07-21 起弃用 [16]）"；Vertex 忽略这条冲突补进 §5
supported | §2.2 Interactions 历史：`store` 默认 true；`previous_interaction_id`（tools 等每轮重传）；付费留存 55 天 [2] | r2-gemini-interactions.md [C11][C12]；原页复核 "Paid tier: The system retains interactions for 55 days." | —
unsupported | §2.2 Interactions 历史：…免费 1 天 [2] | 笔记里没有（r2-gemini-interactions.md [C11] 只摘了 55 天）；原页复核 https://ai.google.dev/gemini-api/docs/interactions 有 "Free tier: The system retains interactions for 1 day." | 内容属实。把原句补进笔记即可，正文不用改
supported | §2.2 Interactions 缓存：仅隐式 [38] | r2-gemini-interactions.md [C22] | —
weak | §2.2 Interactions 结构化输出：顶层 `response_format`，删 `response_mime_type` [27] | r2-gemini-interactions.md [C16] 能支撑；但同一份笔记的 conflicts 记了 interactions.openapi.json 对 response_mime_type 的描述 "This is required if response_format is set."，§5 没列 | 加 ⚔ 注"OpenAPI 仍保留 response_mime_type，并称设了 response_format 就必填"，并补进 §5
supported | §2.3 CC 流式：`chat.completion.chunk`，`data: [DONE]` 结束；`include_usage` 末块带 usage [45] | r1-openai-chat.md [C18][C19] | —
supported | §2.3 CC 错误：`{"error":{message,type,param,code}}` [48] | r1-openai-chat.md [C25] | —
supported | §2.3 Responses 流式：语义事件 + `sequence_number`；文档未见 `[DONE]`，Open Responses 规范要求 `[DONE]` [17] | r1-openai-responses.md [C17][C33] 及 gaps | —
supported | §2.3 Responses 停止：`status` + `incomplete_details.reason` | r1-openai-responses.md [C18][C19] | —
supported | §2.3 Messages 流式：`message_start`…`message_stop`；已移除 `[DONE]` [46][25] | r1-anthropic-messages.md [C23][C24] | —
supported | §2.3 Messages 错误：`{type:"error",error:{type,message}}`；529 `overloaded_error` [49] | r1-anthropic-messages.md [C28] | —
supported | §2.3 generateContent 流式：`?alt=sse`，每块完整响应，未写结束标记 | r1-gemini.md [C3][C27] 及 gaps | —
supported | §2.3 generateContent 停止：`finishReason`：STOP/MAX_TOKENS/SAFETY/MISSING_THOUGHT_SIGNATURE 等 | r1-gemini.md [C29] | —
supported | §2.3 Interactions 流式：同端点 `"stream":true` [28]；`interaction.*`/`step.*` 事件，尾 `[DONE]` | r2-gemini-interactions.md [C18][C19] | —
unsupported | §2.3 Interactions 流式：可按 `last_event_id` 续流 [47] | 笔记里没有；原页复核 [47] https://ai.google.dev/gemini-api/docs/streaming（Last updated 2026-09-17）也没有 last_event_id 或续流相关内容 | 删掉；想保留就先另找出处补进笔记
supported | §2.3 Interactions 停止：`status`：in_progress/requires_action/completed/failed/cancelled/incomplete/queued | r2-gemini-interactions.md [C20] | —
supported | （§4.5，不在本次范围，按简报例子顺手核对）GPT-5.4 起 CC 的工具调用只能配 `reasoning_effort: none` [1] | r1-openai-chat.md [C10]；原页复核原句一致 "Starting with GPT-5.4, Chat Completions does not support tool calling with `reasoning_effort` values other than `none`." | —
supported | （§4.5，不在本次范围，按简报例子顺手核对）Claude 4.6+ 预填 → 400 [3] | r1-anthropic-messages.md [C7]（conflicts：api/messages 未限定模型） | —
计数：范围内 61 条，supported 45 / weak 14 / unsupported 2 / contradicted 0；另附 §4 范围外 2 条（均 supported）；WebFetch 复核 6 次。
