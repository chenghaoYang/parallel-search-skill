# audit-b：§3 变体与适配层、§4 坑、§5 未决与置信度
格式：判定 | 主张原文（从成稿摘，前缀为位置） | 依据 | 建议改法（supported 写 —）
说明：（二手）条目如果来自 secondary 主张、正文已标二手、原句能支撑，也记 supported。回原页核对 6 次（智谱对话补全、betmoar#67、MiniMax openapi-responses.json、DeepSeek anthropic_api、Kimi messages、GLM-5#74）；GLM-5#74 页面没显示回复者身份，沿用笔记。
（二手）标注核对：§3.3 的 6 处（二手）都对应 r2-zhipu-anthropic 的 secondary 主张（C8/C9、C11、C12、C14、C16、C17）；§3–§5 没有发现用了 secondary 来源却没标二手的地方。

## §3.1 协议面
supported | §3.1 DeepSeek·CC/Messages：「`https://api.deepseek.com` [51]」「`…/anthropic` [51]」 | r1-deepseek [C1] | —
supported | §3.1 DeepSeek·Responses：「`POST /responses`；状态字段被忽略 [4]」 | r1-deepseek [C6]（[4]："Unsupported parameters are silently ignored and do not cause errors"）；路径原句在 [C5]，src 是 [5] create-response，格内只标了 [4] | —
supported | §3.1 智谱·CC：「`open.bigmodel.cn/api/paas/v4`、`api.z.ai/api/paas/v4` [52][53]」 | r1-zhipu [C10][C11]；另见 r1-zhipu conflicts：Z.ai glm-5.3 页 Model API 表把 OpenAI 协议写成 https://api.z.ai/api/coding/paas/v4，正文没提示 | —
supported | §3.1 智谱·CC：「Coding Plan 另用 `/api/coding/paas/v4` [54]」 | r1-zhipu [C13] | —
supported | §3.1 智谱·Messages：「两站 `…/api/anthropic` [7][55]」 | r1-zhipu [C1][C4] | —
supported | §3.1 智谱·Responses：「`open.bigmodel.cn/api/v1/responses`：默认 `store=false`，开启后 id 存 7 天，流式无 `[DONE]` [56]」 | r2-cn-responses [C1][C2][C3] | —
supported | §3.1 智谱·Responses：「Z.ai 为 `api.z.ai/api/v1` [57]」 | r2-cn-responses [C7]（出自 devpack 快速开始页；该笔记 gaps：Z.ai 无 Responses 参考页，状态支持未证实） | —
supported | §3.1 Kimi·CC/Messages：「`api.moonshot.cn/v1` [58]」「`…/anthropic` [59]」 | r1-moonshot-minimax [C1][C2] | —
supported | §3.1 Kimi·Responses：「`/v1/responses`：`store` 恒 false，`previous_response_id`、`encrypted_content` 恒 null [60]」 | r2-cn-responses [C9][C10][C12]（原句都是"固定为 `false`/`null`"，说的是响应字段）；路径原句在 [C8]，src 是 guide/codex-kimi | —
supported | §3.1 MiniMax·Messages：「`…/anthropic`」（格内无 [n]） | r1-moonshot-minimax [C18]（src 就是 [61]；这一格和表头都没标来源） | —
supported | §3.1 MiniMax·Responses：「`/v1/responses`：仅生成与 `input_tokens` 估算」 | r2-cn-responses [C17]；原页核对 [62]：只定义了 POST /v1/responses 和 POST /v1/responses/input_tokens | —
weak | §3.1 MiniMax·Responses：「推理默认关 [62][63]」 | r2-cn-responses [C18] 的原句只有 "Reasoning output (only returned when reasoning is enabled)"，没有默认值；原页核对 [62]："For MiniMax-M3, the default is `none`, which disables reasoning."，只说 M3 | 改为"M3 推理默认关（reasoning.effort 默认 none）"，并把这句原句补进笔记
supported | §3.1 Qwen·CC：「`{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；旧 `dashscope.aliyuncs.com` 自 2026-09-30 不再加新特性 [64][65]」 | r1-qwen [C1][C3] | —
supported | §3.1 Qwen·Messages/Responses：「`…/apps/anthropic` [66]」「`/compatible-mode/v1/responses` [67]：`store` 默认 true，id 存 7 天 [68]」 | r1-qwen [C5][C4][C21][C20] | —
supported | §3.1 方舟·CC/Messages：「`ark.cn-beijing.volces.com/api/v3` [69]」「`…/api/compatible`；Coding Plan `/api/coding` [70][71]」 | r1-ark [C1][C29][C30] | —
weak | §3.1 方舟·Responses：「`store` + `expire_at`（默认 3 天，≤ 7 天）[72]」 | r1-ark [C12] 的原句"默认值：创建时刻+259200"支撑默认 3 天；"最多 7 天"只写在主张文字里，原句里没有 | 补 7 天上限的原句；补不到就删掉"≤ 7 天"

## §3.2 CC 端点差异
supported | §3.2 DeepSeek·推理：「默认开（effort high）；`reasoning_content` [13]」 | r1-deepseek [C10][C11] | —
supported | §3.2 DeepSeek·推理回传：「无工具可不传；带工具不回传 → 400 [13]」 | r1-deepseek [C12][C13] | —
supported | §3.2 DeepSeek·工具：「思考中 `required`/指定 → 400 [73]」 | r1-deepseek [C19] | —
supported | §3.2 DeepSeek·输出/采样：「仅 text/json_object；思考中 temperature 等无效 [73][13]」 | r1-deepseek [C18][C14] | —
supported | §3.2 DeepSeek·私有字段：「`prompt_cache_hit/miss_tokens`；finish_reason 多 `insufficient_system_resource`、`aborted` [73]」 | r1-deepseek [C20][C21] | —
supported | §3.2 智谱·推理：「`thinking.type`（GLM-5.3 传 disabled 报错）[74]」 | r1-zhipu [C14] | —
weak | §3.2 智谱·推理：「effort 仅 low/high/max [75]」 | r1-zhipu [C15] 的原句限定了"对于 `GLM-5.3` `GLM-5.3-FLASH` 模型"；原页核对，同一段还写了 GLM-5.2 传 none/minimal 会放弃思考、low/medium 映射成 high、xhigh 映射成 max | 改为"GLM-5.3 系 effort 仅 low/high/max"
weak | §3.2 智谱·推理回传：「`clear_thinking` 默认丢弃历史推理 [75]」 | r1-zhipu [C16] 支撑参考页默认值 True；但同一笔记 [C17]（[76]）："该能力在 Coding Plan 端点默认开启、标准 API 端点默认关闭。" | 限定为"标准 API 端点"，并补"Coding Plan 端点默认保留 [76]"
supported | §3.2 智谱·推理回传：「带工具须回传 [76]」 | r1-zhipu [C18] | —
supported | §3.2 智谱·工具：「tool_choice 仅 auto；内置 web_search [75]」 | r1-zhipu [C20][C19] | —
supported | §3.2 智谱·输出：「仅 text/json_object [75]」 | r1-zhipu [C22]；原页核对：枚举只有 text、json_object（原页句子写"取值收敛为三种"却只列了两种，是原页自己的笔误） | —
supported | §3.2 智谱·私有字段：「中途异常经 finish_reason（`sensitive`/`network_error`）报告 [79][77]」 | r1-zhipu [C25][C26] | —
weak | §3.2 Kimi·推理回传：「原样回传含 `reasoning_content` 的消息 [80]」 | r1-moonshot-minimax [C9] 的主张只针对 K3；[C10] 对 k2.x 只要求"单轮任务内（一次工具调用循环中产生的多步推理）应保留上下文中所有的思考内容" | 改为"K3 须原样回传；k2.x 只在单次工具循环内保留"
supported | §3.2 Kimi·工具：「k2.6/k2.7-code 不支持 `required` [81]」 | r1-moonshot-minimax [C8] | —
supported | §3.2 Kimi·输出/采样：「temperature/top_p/n 固定，改值报错 [81]」 | r1-moonshot-minimax [C6][C7] | —
supported | §3.2 MiniMax·推理：「`reasoning_split=true` → `reasoning_details`，否则 `<think>` 在 content [83]」 | r1-moonshot-minimax [C26] | —
supported | §3.2 MiniMax·输出/采样：「`n` 仅 1；忽略 penalty [83]」 | r1-moonshot-minimax [C29][C28] | —
supported | §3.2 MiniMax·工具：「❓」 | r3-cn-gaps gaps（text-openai-api 和 M3 工具指南都没提 tool_choice） | —
weak | §3.2 Qwen·推理回传：「`preserve_thinking`（多数默认 false）开启时须完整回传 [84]」 | r3-cn-gaps [C4] 支撑"须完整回传"；[C2] 原句"默认值为false（qwen3.8-max/qwen3.8-flash 默认值为true）"，[C3] 只列了 4 个支持型号，其中 2 个默认 true，说"多数"没有依据 | 改为"默认 false（qwen3.8-max/flash 默认 true；只有列出的型号支持）"
supported | §3.2 Qwen·工具：「不支持 `required`；`parallel_tool_calls` 默认 false [64]」 | r1-qwen [C23][C18] | —
supported | §3.2 Qwen·输出：「`max_tokens` 只限回答，`max_completion_tokens` 含思维链 [64]」 | r1-qwen [C24] | —
supported | §3.2 Qwen·缓存：「隐式 + 显式 `cache_control`；cached 计入 prompt [85]」 | r1-qwen [C27][C28][C30] | —
supported | §3.2 方舟·推理：「`thinking.type` 含 auto [69]；部分模型只给摘要 [86]」 | r1-ark [C6][C8] | —
supported | §3.2 方舟·推理回传：「Responses 推理项带 `encrypted_content` [87]」 | r1-ark [C9] | —
supported | §3.2 方舟·工具：「Chat 无内置工具 [88]」 | r1-ark [C17] | —
weak | §3.2 方舟·输出：「思考模型无 logprobs [69]」 | r1-ark [C21] 原句："深度思考能力模型不支持该字段。其中，deepseek-v4-1-flash-260910、deepseek-v4-pro-ga-260813、deepseek-v4-flash-ga-260731 支持该字段。"；该笔记 conflicts 还记了 GLM-5.2 将支持 | 改为"思考模型一般不支持 logprobs（DeepSeek V4 系列例外）"
weak | §3.2 方舟·缓存：「隐式与显式 `caching` 互斥 [89]」 | r1-ark [C27]："二者互斥"只写在主张文字里，原句只有"隐式缓存：自动启用，用户无需额外配置，且无法关闭" | 补"互斥"的原句；补不到就删掉或标 ❓

## §3.3 Anthropic 兼容端点
supported | §3.3 DeepSeek·模型名：「`claude-opus*` → deepseek-v4-pro」 | r1-deepseek [C26] | —
supported | §3.3 DeepSeek·thinking：「支持，`budget_tokens` 忽略」 | r1-deepseek [C28] | —
contradicted | §3.3 DeepSeek·tool_choice：「auto/any/tool」 | r1-deepseek [C29] 的原句只有 "Supported (disable_parallel_tool_use is ignored)"；原页核对 [90]，tool_choice 表里还有 none 一行，标 "Fully Supported"。这一格和 Kimi 列的 auto/any/none 并排，读者会以为 DeepSeek 不支持 none | 改为"auto/any/tool/none（disable_parallel_tool_use 忽略）"，笔记 C29 一并改正
supported | §3.3 DeepSeek·缓存：「`cache_control` Ignored」 | r1-deepseek [C30] | —
supported | §3.3 DeepSeek·内容/工具：「image 支持；document、redacted_thinking 等 Not Supported」 | r3-cn-gaps [C11]；r1-deepseek [C31]（原句只有 document 一行；原页核对，redacted_thinking 一行也是 Not Supported） | —
supported | §3.3 DeepSeek·其他：「`anthropic-version`/`anthropic-beta` 忽略」 | r1-deepseek [C27]；原页核对，anthropic-beta 是 "Ignored for `/messages`; required (`files-api-2025-04-14`) for Files API endpoints" | —
supported | §3.3 智谱·字段表：「**无** [7]」 | r1-zhipu [C2] 与 gaps；r2-zhipu-anthropic gaps | —
weak | §3.3 智谱·模型名：「服务端映射到 GLM：BigModel 默认 GLM-4.7，Z.ai 默认 GLM-5.3-Flash [8][92]」 | r2-zhipu-anthropic [C1][C3] 的原句给的是 `ANTHROPIC_DEFAULT_OPUS_MODEL`（只是 Opus 槽），Sonnet/Haiku 槽没查到；该笔记 conflicts 还记了 [8] 页另写"使用最新 GLM-5.2 模型" | 改为"Opus 槽默认映射 GLM-4.7（BigModel）/ GLM-5.3-Flash（Z.ai）"
weak | §3.3 智谱·thinking：「读 `thinking.type`/`output_config.effort`，关闭 → low [9]」 | r1-zhipu [C8][C9]、r2-zhipu-anthropic [C4] 都出自 coding-plan/latest-model 的 Claude Code 一节；r2-zhipu-anthropic conflicts："按量 key 调 /api/anthropic 适用哪条没写" | 格内加"（Coding Plan / Claude Code）"，按量 key 的情况标 ❓
supported | §3.3 智谱·tool_choice：「∅」 | r2-zhipu-anthropic gaps（官方文档和二手报告里都没有） | —
supported | §3.3 智谱·缓存：「隐式命中，不返回 `cache_creation_input_tokens`（二手）[93]」 | r2-zhipu-anthropic [C14]（secondary，已标二手） | —
weak | §3.3 智谱·内容/工具：「服务端内置 `image_analysis`、联网搜索 [10][11]」 | r2-zhipu-anthropic [C5][C6] 原句的前提是"在 Claude Code 中使用 GLM Coding Plan 时"；该笔记 gaps：按量 key 走 /api/anthropic 时有没有内置工具，文档没写 | 格内加"（Coding Plan + Claude Code）"
supported | §3.3 智谱·内容/工具：「URL 图片被拒（二手）[95]」 | r2-zhipu-anthropic [C17]（secondary，已标二手；报告对象是 Z.ai、glm-5.3-flash） | —
unsupported | §3.3 智谱·内容/工具：「返回自有 `server_tool_use` 块，回灌官方 API 会 400（二手）[96]」 | r2-zhipu-anthropic [C11]（secondary）只支撑前半句，"回灌会 400"笔记里没有；原页核对有这句："API Error: 400 messages.799.content.1.server_tool_use.id: String should match pattern '^srvtoolu_[a-zA-Z0-9_]+$'" | 正文可以保留；把这句原句补进笔记
weak | §3.3 智谱·其他：「`messages` 含 system → 422，zai-org 成员称系有意为之（二手）[97]」 | r2-zhipu-anthropic [C8][C9]（secondary，已标二手）；C9 记的回复者身份是 CONTRIBUTOR，不是 zai-org 成员 | 把"zai-org 成员"改成"仓库贡献者（CONTRIBUTOR）"
supported | §3.3 智谱·其他：「`message_start.usage` 恒 0（二手）[98]」 | r2-zhipu-anthropic [C12]（secondary，已标二手；报告对象是 api.z.ai、glm-5.3） | —
weak | §3.3 智谱·其他：「count_tokens 返回 0（二手）[99]」 | r2-zhipu-anthropic [C16] 原句限定了 "Z.AI's … count_tokens … for `glm-5.3`" | 注明"Z.ai、glm-5.3"；其他二手条目也建议标上站点（#74、#411 是 open.bigmodel.cn；#139、#67、PR3704、PR613 是 Z.ai）
supported | §3.3 Kimi·thinking：「thinking 块连 `signature` 回传」 | r1-moonshot-minimax [C17] | —
supported | §3.3 Kimi·tool_choice：「auto/any/none」 | r1-moonshot-minimax [C15]；原页核对 [59]："`auto`（默认）：模型自行决定；`any`：强制调用任意工具；`none`：不调用工具。" | —
supported | §3.3 Kimi·缓存/内容：「只认顶层 `cache_control`」「无 document」 | r1-moonshot-minimax [C14][C16]；原页核对，内容块只有 text、image、thinking、tool_use、tool_result | —
supported | §3.3 MiniMax·thinking：「M3 默认关（`adaptive` 开），M2.x 不可关」 | r1-moonshot-minimax [C24] | —
supported | §3.3 MiniMax·tool_choice：「⚔ 见 §5」 | r1-moonshot-minimax conflicts；r2-cn-responses conflicts | —
supported | §3.3 MiniMax·缓存/内容：「显式 5 分钟 [94]」「M2.x 仅 text + 工具」 | r1-moonshot-minimax [C32][C23] | —
supported | §3.3 MiniMax·其他：「忽略 top_k、stop_sequences；temperature [0,2]，越界报错」 | r1-moonshot-minimax [C21][C22] | —

## §3.4 源头兼容层、网关、托管
supported | §3.4 Gemini 兼容层：「`…/v1beta/openai/`（beta）[100]」 | r2-origin-compat [C1][C2] | —
supported | §3.4 Gemini 兼容层：「`reasoning_effort` 映射到 thinking、与 thinking_level 互斥；签名在 `tool_calls[].extra_content.google.thought_signature` [12]」 | r2-origin-compat [C3][C5]（src 是 [100]，格内只标了 [12]）、[C8]（[12]） | —
supported | §3.4 Anthropic 兼容层：「`https://api.anthropic.com/v1/`，官方称非生产方案 [101]」 | r2-origin-compat [C14][C15]（原句带 "for most use cases"） | —
supported | §3.4 Anthropic 兼容层：「思考经 `extra_body` 开启且不返回；`reasoning_effort`/`strict`/`response_format` 忽略；temperature > 1 截断」 | r2-origin-compat [C16][C17][C19]；r1-scout [C6][C9] | —
supported | §3.4 OpenRouter：「CC（归一化）+ `/api/v1/responses` + `/api/v1/messages` [102][103]」「Responses 带 `store:true`/`previous_response_id` → 400 [104]」 | r2-hosting [C1][C4][C3] | —
supported | §3.4 自托管：「vLLM：`/v1/responses`、`/v1/messages` [105]；Ollama：`/v1/responses`（仅无状态）[106]」 | r2-hosting [C9][C11] | —
supported | §3.4 自托管：「Ollama 的 tool_choice 不完全支持 [107]；llama.cpp 的 Responses 转成 CC 实现，Messages 不承诺兼容 [108]」 | r2-hosting [C10][C13][C14] | —
supported | §3.4 Bedrock：「新 `bedrock-mantle.{region}.api.aws/anthropic/v1/messages`（原生形状 + SSE）[109]」 | r2-hosting [C15] | —
weak | §3.4 Bedrock：「旧 InvokeModel/Converse：event-stream，body `anthropic_version:"bedrock-2023-05-31"` [110]」 | r2-hosting [C16] 支撑两者都用 event-stream；[C17] 的 anthropic_version 只是 InvokeModel 的 body 字段；同一笔记 leads 说 Converse 用的是归一化信封 | 改为"旧 InvokeModel/Converse：event-stream；InvokeModel 的 body 带 anthropic_version"
supported | §3.4 Vertex：「model 在 URL」「body `anthropic_version:"vertex-2023-10-16"` [111]」 | r2-hosting [C18] | —

## §4 坑
weak | §4.1：「CC/Responses 的 `arguments` 是字符串，且 "the model does not always generate valid JSON" [18]」 | r1-openai-chat [C9] 出自 CC 参考页 chat.md，只能支撑 CC；r1-openai-responses 里没有"Responses 的 arguments 是字符串"的原句 | 把原句限定到 CC；Responses 部分补来源
supported | §4.2：「迁入 Gemini 可填占位签名跳过校验，并行调用的 FC/FR 交错排列会 400 [12]」 | r1-scout [C3]；r2-origin-compat [C10] | —
supported | §4.2：「Anthropic 须原样回传 [15]」 | r1-anthropic-messages [C20]；r1-scout [C4]（原文语境是工具轮） | —
supported | §4.3：「OpenAI strict 要求所有字段 required 且 `additionalProperties:false` [112]；Gemini 是 OpenAPI 3.0 子集 [21]」 | r1-scout [C14][C15][C16] | —
supported | §4.4：「Anthropic 要求 `^[a-zA-Z0-9_-]+$` [20]」 | r1-scout [C12] | —
supported | §4.5：「GPT-5.4 起 CC 的工具调用只能配 `reasoning_effort: none` [1]」 | r1-openai-chat [C10] | —
supported | §4.5：「Claude 4.6+ 预填 → 400 [3]」 | r1-anthropic-messages [C7] | —
weak | §4.6：「Qwen、方舟的 `max_completion_tokens` 含思维链 [64][69]」 | Qwen 部分由 r1-qwen [C24] 支撑；方舟部分，r1-ark [C20] 的"含思维链"只写在主张文字里，原句是"不可与 max_tokens 字段同时设置。" | 补方舟的原句，或者只写 Qwen
supported | §4.6：「DeepSeek 默认 8K（思考 64K）[73]」 | r1-deepseek [C17] | —
supported | §4.7：「DeepSeek 等待时发 `: keep-alive` 注释 [113]，OpenRouter 也有 comment [102]」 | r1-deepseek [C24]；r2-hosting [C2] | —
supported | §4.8：「订阅过智谱 Coding Plan 的账号暂只能用 OpenAI 协议调模型 API [114]」 | r1-zhipu [C6] | —

## §5 未决与置信度
supported | §5 ❓：「MiniMax OpenAI 层的 tool_choice；Qwen 工具调用时的回传规则」 | r3-cn-gaps gaps | —
weak | §5 ❓：「各家 Responses 对未知字段忽略还是报错」 | r2-cn-responses gaps 只说智谱/Kimi/MiniMax 没写；DeepSeek 已写明（r1-deepseek [C6]："Unsupported parameters are silently ignored and do not cause errors"）；r1-qwen gaps 也记了 Qwen 的 Responses 页写明会忽略 | 把范围限定为"智谱、Kimi、MiniMax 的 Responses"
supported | §5 ∅：「智谱 Anthropic 端点无字段级文档；§3.3 的（二手）条目来自 2026-05～09 GitHub 报告」 | r1-zhipu gaps；r2-zhipu-anthropic gaps 与 [C8]–[C17]（日期 2026-05-29～09-16） | —
supported | §5 ⚔：「Interactions 端点版本（参考页 `/v1beta` + v1，迁移指南示例用 `/v1beta2`）及是否支持 temperature、safety_settings」 | r2-gemini-interactions [C2] 与 conflicts（temperature 一方是"OpenAPI/SDK 里没有这个字段"的观察，不是原句） | —
supported | §5 ⚔：「MiniMax Anthropic 层 tool_choice（同站两页矛盾，非版本差异）」 | r2-cn-responses conflicts（lastmod 06-10 vs 06-09，国内站也一样矛盾） | —
supported | §5 ⚔：「GLM-5.3 关闭思考（标准 API 报错 vs Coding Plan 转 low，按通道区分）」 | r2-zhipu-anthropic conflicts、r1-zhipu conflicts（笔记只给了语境，没有裁决；按量 key 调 /api/anthropic 的情况没写） | —
supported | §5 ⚔：「OpenAI CC `store` 默认值；Gemini `functionResponse` 的 role；方舟无效 `encrypted_content` 是否报错；Qwen3 商业版思考模式是否仅流式」 | r1-openai-chat、r1-gemini、r1-ark、r3-cn-gaps 的 conflicts（方舟那一方 2678892 用的是"将兼容"，可能是版本预告） | —
supported | §5 时效：「DeepSeek 回传规则反转过」 | r1-deepseek conflicts（存档页"included…will return a 400 error" vs 现行 [C12][C13]） | —

附注（不算判定）：§5 的 ⚔ 列表没收录笔记里和 §3 直接相关的几条冲突：Z.ai CC 端点（r1-zhipu conflicts）、MiniMax Responses 的工具类型是只有 function 还是也有 web_search（r2-cn-responses conflicts）、Qwen 的 tools 能否与 stream=True 同用（r1-qwen conflicts）、方舟 max_completion_tokens 取值范围（r1-ark conflicts）。
计数：supported 77 / weak 17 / unsupported 1 / contradicted 1（共 96 条）
