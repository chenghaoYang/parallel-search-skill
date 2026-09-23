# LLM 推理 API 请求协议对照：五个源头协议 × 下游兼容层（截至 2026-09-23）

> LLM API 请求协议分几类、差在哪、兼容层缺什么多什么。先读 §0、§1，查字段看 §2–§3，踩坑看 §4。表头 [n] 为该列默认来源；❓ 未查到，∅ 官方未写，（二手）= 社区报告。

## 0. 一屏看懂

1. **两代协议**：一代「无状态消息列表」——Chat Completions（CC）、Anthropic Messages、Gemini generateContent；二代「可选服务端状态 + 类型化条目 + 语义流事件」——OpenAI Responses、Gemini Interactions。OpenAI 称 "Responses is recommended for all new projects"，Assistants API 已于 2026-08-26 下线 [1]；Gemini Interactions 2026-06 GA，generateContent 被称为 legacy [2]；Anthropic Messages 仍无状态 [3]。
2. **Q1 DeepSeek：确实不同，性质是「兼容子集 + 私有扩展」**。有 Responses：`POST https://api.deepseek.com/responses`（无 `/v1`，2026-07-31 起）[4][5]；不存状态，`previous_response_id`/`store` 等被 "silently ignored" [4]；推理以明文 reasoning item 返回，不支持 `encrypted_content`/`summary` [4][5]。旧模型名 deepseek-chat/reasoner 按公告于 2026-07-24 停用 [6]。
3. **Q2 智谱：有 Anthropic 端点，无字段级兼容说明**，只写"某些场景下…仍存在差异" [7]。官方写明的多是 Coding Plan 场景的服务端改写：Claude 模型名映射成 GLM [8]、关闭思考转 low [9]、内置看图与联网搜索 [10][11]；标准 API 下 GLM-5.3 传 disabled 则报错 [12]。社区另报告 system 角色 422、count_tokens 为 0 等（§3.3）。
4. **Responses 兼容 ≠ 有状态**：`previous_response_id` 在智谱、Qwen、方舟可用；在 DeepSeek 被忽略，在 Kimi 恒为 null，在 OpenRouter 直接 400（§3）。
5. **推理回传是头号迁移坑**：各家载体和规则不同（§2.2、§3.2），Gemini 3 函数调用时漏回签名、DeepSeek 带工具漏回 `reasoning_content` 都直接 400 [13][14]。
6. **采样参数在被收回**：Claude Opus 4.7+ 等传非默认 `temperature`/`top_p`/`top_k` 即 400 [15]；Gemini 2026-07-21 起弃用三者 [16]；GPT-6 在 effort ≠ none 时要求去掉 temperature/top_p [17]。
7. **"不支持"按场景两极**：静默忽略（DeepSeek Responses 未支持参数、Anthropic 兼容层、MiniMax 多数参数）vs 报错（Kimi 固定采样参数、DeepSeek 思考模式强制 tool_choice、MiniMax 温度越界、OpenRouter 状态字段）。不报错 ≠ 生效。
8. **用量口径不同**：OpenAI 的 prompt 计数含缓存，Anthropic 不含，DeepSeek 拆成 hit/miss（§2.3、§3.2）。

## 1. Taxonomy

| 代 | 家族 | 对话单元 | 服务端状态 | 流式 | 兼容实现 |
|---|---|---|---|---|---|
| 一 | CC | `messages[]`，工具调用挂在 assistant 消息 | 无 | `data:` 块 + `[DONE]` | 6 家国内厂商、源头厂兼容层、OpenRouter |
| 一 | Messages | 顶层 `system` + 类型化 content blocks | 无 | 类型化事件 | 6 家国内厂商、网关、自托管、Bedrock |
| 一 | generateContent | `contents[].parts[]` | 无 | 每块完整响应 | 未见第三方 |
| 二 | Responses | `input[]` items | 可选，默认存 | 语义事件 | 6 家国内厂商、网关、自托管；开放规范 Open Responses [18] |
| 二 | Interactions | `input` / `steps` | 可选，默认存 | 语义事件 + `[DONE]` | 未见第三方 |

- 二代的共同形状：扁平函数工具、以 `call_id` 关联的调用/结果条目、`store` 默认 true、`previous_*_id` 续接、background 异步、带 `queued`/`incomplete` 等状态。一代内部的对话结构主要差在切分粒度：整条消息 / 类型化块 / parts。
- 下游厂商多同时暴露 CC、Messages、Responses：兼容性按**端点**判断。
- 维度 D1–D12：接入、形状、多模态、工具、状态、推理、输出与采样、流式、停止与用量、缓存、兼容度、错误。

## 2. 源头协议对照矩阵

### 2.1 接入、形状、工具（D1–D4）
| | CC [19] | Responses [20] | Messages [21] | generateContent [22] | Interactions [23] |
|---|---|---|---|---|---|
| 端点 | `POST /v1/chat/completions` | `POST /v1/responses` | `POST /v1/messages` | `POST /v1beta/models/{model}:generateContent`（模型在 URL） | `POST /v1beta/interactions`（另有 v1）；body 放 `model` 或 `agent` |
| 鉴权 | Bearer [24] | 同左 | Bearer（`x-api-key` 为旧式回退）+ 必填 `anthropic-version` [25][26] | `x-goog-api-key` [27] | 同左 |
| 容器/角色/系统指令 | `messages`：developer/system/user/assistant/tool；o1 起 developer 取代 system | `input`（字符串或 items；无 tool 角色）+ 顶层 `instructions` [1] | `messages` 仅 user/assistant（连续同角色合并）+ 顶层 `system` | `contents` 仅 user/model + `systemInstruction` | `input` + 顶层 `system_instruction`；无状态多轮回传上轮 `steps` [28] |
| 多模态 | `image_url`/`input_audio`/`file` | `input_image`/`input_file` | `image`/`document`（base64/url/file） | `inlineData`/`fileData` | type=image/audio/document/video [29] |
| 工具定义 | `{type:"function",function:{name,parameters,strict}}`；另有 `custom` | 扁平 `{type:"function",name,parameters,strict}`，省略 strict 即尝试严格 [1] | `{name,input_schema,strict?}` | `functionDeclarations[]`：OpenAPI 子集或 `parametersJsonSchema` [30] | 扁平 `{type:"function",name,description,parameters}` [29] |
| 调用 → 回传 | `tool_calls[]{id,function.arguments}`（字符串）→ `{role:"tool",tool_call_id}` | `function_call{call_id,arguments}` → `function_call_output{call_id,output}` [1] | `tool_use{id,input}`（对象）→ user 内 `tool_result{tool_use_id}`，须紧跟且排最前 [31] | `functionCall{id,args}`（对象）→ `functionResponse{id,response}`，role 用 user [30] | `function_call` step（status `requires_action`）→ `function_result{call_id,result,is_error}` |
| tool_choice | none/auto/required/指定/`allowed_tools` | 同左，指定写成扁平 `{type:"function",name}` [32] | auto/any/tool/none + `disable_parallel_tool_use` | `mode`：AUTO/ANY/NONE/VALIDATED [33] | ❓ |
| 内置工具 | `web_search_options` | web_search、file_search、code_interpreter、MCP 等 [1] | 带日期版本号，如 `web_search_20260318` [34] | googleSearch、codeExecution 等 | google_search、code_execution、mcp_server 等 |

### 2.2 状态、推理、输出（D5–D7、D10）
| | CC [19] | Responses [20] | Messages [21] | generateContent [22] | Interactions [23] |
|---|---|---|---|---|---|
| 历史 | 客户端管理 [1] | `store` 默认 true [1]；`previous_response_id` 与 `conversation` 互斥 [32]；默认存 30 天 [35] | 无状态 [3] | 无状态 [29] | `store` 默认 true；`previous_interaction_id`（tools 等每轮重传）；付费留存 55 天、免费 1 天 [2] |
| 缓存 | 自动，GPT-5.6+ ≥ 1,024 tokens [36] | 同左；官方内测称缓存利用率比 CC 高 40–80% [1] | 显式 `cache_control`（5m/1h，≤ 4 断点）；顶层即自动 [37] | 隐式 + 显式 `cachedContents` [38] | 仅隐式 [39] |
| 推理控制 | `reasoning_effort`：none/minimal/low/medium/high/xhigh/max | `reasoning.effort`，同 7 档 | `thinking.type`：enabled/disabled/adaptive + `output_config.effort`；4.7+ 用 `budget_tokens` 报 400 [40] | `thinkingConfig{thinkingLevel,thinkingBudget,includeThoughts}` | `thinking_level` + `thinking_summaries` |
| 推理返回 | 不返回，只计 `reasoning_tokens` [41] | reasoning item，默认带 `encrypted_content` [41] | `thinking{thinking,signature}` / `redacted_thinking` | `thought:true` 摘要 part + `thoughtSignature` [42] | thought step 带 `signature`/`summary` [43] |
| 推理回传 | — | 手动管理状态时须放回 reasoning items | 工具循环中 "complete and unmodified" 回传 [15] | Gemini 3 函数调用缺签名 → 400 [13] | 有状态免管；无状态须原样回传 [43] |
| 结构化输出 | `response_format{type:"json_schema",...}` | `text.format` [1] | `output_config.format`（已 GA）[44] | `responseFormat.text{mimeType,schema}`（`responseSchema` 已 deprecated） | 顶层 `response_format`，删 `response_mime_type` [28] |
| 长度/采样 | `max_completion_tokens`（`max_tokens` 弃用）；temperature 0–2，`stop` ≤ 4 | `max_output_tokens`，含推理 token [32] | `max_tokens` **必填** [45] | `maxOutputTokens`；temperature [0,2]（已弃用，见 §0） | `max_output_tokens` |

### 2.3 流式、停止、用量、错误（D8、D9、D12）
| | CC [19] | Responses [20] | Messages [21] | generateContent [22] | Interactions [23] |
|---|---|---|---|---|---|
| 流式 | `chat.completion.chunk`，`data: [DONE]` 结束；`include_usage` 末块带 usage [46] | 语义事件 + `sequence_number`；文档未见 `[DONE]`，Open Responses 规范要求 `[DONE]` [18] | `message_start`…`message_stop`；已移除 `[DONE]` [47][26] | `?alt=sse`，每块完整响应，未写结束标记 | 同端点 `"stream":true` [29]；`interaction.*`/`step.*` 事件，尾 `[DONE]` [48]；可按 `last_event_id` 续流 [23] |
| 停止 | `finish_reason`：stop/length/tool_calls/content_filter/function_call | `status` + `incomplete_details.reason` | `stop_reason`：end_turn/max_tokens/stop_sequence/tool_use/pause_turn/refusal/model_context_window_exceeded | `finishReason`：STOP/MAX_TOKENS/SAFETY/MISSING_THOUGHT_SIGNATURE 等 | `status`：in_progress/requires_action/completed/failed/cancelled/incomplete/queued |
| 用量 | `prompt_tokens`（含 cached）/`completion_tokens` [46] | `input_tokens`/`output_tokens` + cached/reasoning 明细 | `input_tokens`（不含缓存）+ `cache_creation/read_input_tokens` [37] | `promptTokenCount`/`thoughtsTokenCount` 等，total 含 thoughts | `total_input/output/thought/cached_tokens` |
| 错误 | `{"error":{message,type,param,code}}` [49] | `response.error{code,message}` | `{type:"error",error:{type,message}}`；529 `overloaded_error` [50] | `{error:{code,message,status}}`；429 `RESOURCE_EXHAUSTED` [51] | `{"error":{code,message}}`；流式 `event: error` [48] |

## 3. 变体与适配层

### 3.1 协议面：下游暴露哪些端点
| 厂商 | CC | Messages | Responses（状态支持） |
|---|---|---|---|
| DeepSeek | `https://api.deepseek.com` [52] | `…/anthropic` [52] | `POST /responses`；状态字段被忽略 [4] |
| 智谱 | `open.bigmodel.cn/api/paas/v4`、`api.z.ai/api/paas/v4` [53][54]；Coding Plan 另用 `/api/coding/paas/v4` [55] | 两站 `…/api/anthropic` [7][56] | `open.bigmodel.cn/api/v1/responses`：默认 `store=false`，开启后 id 存 7 天，流式无 `[DONE]` [57]；Z.ai：`api.z.ai/api/v1` [58] |
| Kimi | `api.moonshot.cn/v1` [59] | `…/anthropic` [60] | `/v1/responses`：`store` 恒 false，`previous_response_id`、`encrypted_content` 恒 null [61] |
| MiniMax | `api.minimax.io/v1`、`api.minimax.cn/v1` [62] | `…/anthropic` [62] | `/v1/responses`：仅生成与 `input_tokens` 估算；M3 推理默认关 [63][64] |
| Qwen/百炼 | `{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；旧 `dashscope.aliyuncs.com` 自 2026-09-30 不再加新特性 [65][66] | `…/apps/anthropic` [67] | `/compatible-mode/v1/responses` [68]：`store` 默认 true，id 存 7 天 [69] |
| 方舟 | `ark.cn-beijing.volces.com/api/v3` [70] | `…/api/compatible`；Coding Plan `/api/coding` [71][72] | `/api/v3/responses`：`store` + `expire_at`（默认 3 天）[73] |

### 3.2 CC 端点的差异（相对 OpenAI）
| | 推理开关/返回 | 推理回传 | 工具 | 输出/采样 | 缓存与私有字段 |
|---|---|---|---|---|---|
| DeepSeek | 默认开（effort high）；`reasoning_content` [14] | 无工具可不传；带工具不回传 → 400 [14] | 思考中 `required`/指定 → 400 [74] | 仅 text/json_object；思考中 temperature 等无效 [74][14] | `prompt_cache_hit/miss_tokens`；finish_reason 多 `insufficient_system_resource`、`aborted` [74] |
| 智谱 | `thinking.type`（GLM-5.3 传 disabled 报错）[12]；GLM-5.3 系 effort 仅 low/high/max [75] | 标准端点默认丢弃历史推理（`clear_thinking`），Coding Plan 端点默认保留；带工具须回传 [75][76] | tool_choice 仅 auto；内置 web_search [75]；私有 `tool_stream` [77] | 仅 text/json_object [75] | `cached_tokens` [78]；中途异常经 finish_reason（`sensitive`/`network_error`）报告 [79][77] |
| Kimi | `thinking` 走 extra_body；`partial` 预填 [59] | K3 须原样回传 `reasoning_content`；k2.x 只在单次工具循环内保留 [80] | k2.6/k2.7-code 不支持 `required` [81] | temperature/top_p/n 固定，改值报错 [81] | `cached_tokens`/`cache_write_tokens` [82] |
| MiniMax | `reasoning_split=true` → `reasoning_details`，否则 `<think>` 在 content [83] | 保留完整消息含 `reasoning_details` [62] | ❓ | `n` 仅 1；忽略 penalty [83] | 见 §3.3 |
| Qwen | `enable_thinking`、`thinking_budget`（extra_body）[65] | `preserve_thinking` 开启时须完整回传（默认 false，qwen3.8 系默认 true）[84] | 不支持 `required`；`parallel_tool_calls` 默认 false [65] | `max_tokens` 只限回答，`max_completion_tokens` 含思维链 [65] | 隐式 + 显式 `cache_control`；cached 计入 prompt [85] |
| 方舟 | `thinking.type` 含 auto [70]；部分模型只给摘要 [86] | Responses 推理项带 `encrypted_content` [87] | Chat 无内置工具 [88] | `response_format` 含 json_schema（beta）[70] | 隐式缓存自动且不可关 [89]；Responses 另有显式 `caching` [73] |

### 3.3 Anthropic 兼容端点（Q2 展开）
| | DeepSeek [90] | 智谱（官方行为条目限 Coding Plan） | Kimi [60] | MiniMax [91] |
|---|---|---|---|---|
| 字段表 | 有 | **无** [7] | 有 | 有 |
| 模型名 | `claude-opus*` → deepseek-v4-pro | 服务端映射到 GLM：Opus 槽默认 GLM-4.7（BigModel）/ GLM-5.3-Flash（Z.ai）[8][92] | ❓ | ❓ |
| thinking | 支持，`budget_tokens` 忽略 | 读 `thinking.type`/`output_config.effort`，关闭 → low [9] | thinking 块连 `signature` 回传 | M3 默认关（`adaptive` 开），M2.x 不可关 |
| tool_choice | auto/any/tool/none | ∅ | auto/any/none | ⚔ 见 §5 |
| 缓存 | `cache_control` Ignored | 隐式命中，不返回 `cache_creation_input_tokens`（二手）[93] | 只认顶层 `cache_control` | 显式 5 分钟 [94] |
| 内容/工具 | image 支持；document、redacted_thinking 等 Not Supported | 服务端内置 `image_analysis`、联网搜索 [10][11]；URL 图片被拒（二手）[95]；Z.ai 返回自有 `server_tool_use` 块，回灌官方 API 会 400（二手）[96] | 无 document | M2.x 仅 text + 工具 |
| 其他 | `anthropic-version`/`anthropic-beta` 忽略 | `messages` 含 system → 422，仓库贡献者称系有意为之（二手）[97]；Z.ai 上 `message_start.usage` 恒 0（二手）[98]、glm-5.3 的 count_tokens 返回 0（二手）[99] | — | 忽略 top_k、stop_sequences；temperature [0,2]，越界报错 |

### 3.4 源头厂兼容层、网关、托管
| 实体 | 协议面 | 关键差异 |
|---|---|---|
| Gemini 兼容层 | `…/v1beta/openai/`（beta）[100] | `reasoning_effort` 映射到 thinking、与 thinking_level 互斥；签名在 `tool_calls[].extra_content.google.thought_signature` [13] |
| Anthropic 兼容层 | `https://api.anthropic.com/v1/`，官方称非生产用 [101] | 思考经 `extra_body` 开启且不返回；`reasoning_effort`/`strict`/`response_format` 忽略；temperature > 1 截断 |
| OpenRouter | CC（归一化）+ `/api/v1/responses` + `/api/v1/messages` [102][103] | Responses 带 `store:true`/`previous_response_id` → 400 [104] |
| 自托管 | vLLM：`/v1/responses`、`/v1/messages` [105]；Ollama：`/v1/responses`（仅无状态）[106] | Ollama 的 tool_choice 不完全支持 [107]；llama.cpp 的 Responses 转成 CC 实现，Messages 不承诺兼容 [108] |
| Bedrock | 新 `bedrock-mantle.{region}.api.aws/anthropic/v1/messages`（原生形状 + SSE）[109] | 旧 InvokeModel/Converse 用 event-stream；InvokeModel body 带 `anthropic_version:"bedrock-2023-05-31"` [110] |

## 4. 用户需要知道的坑（按踩中概率）
1. **工具参数**：CC 的 `arguments` 是字符串，且 "the model does not always generate valid JSON" [19] → 要容错。
2. **跨家迁移历史**：推理载体互不相通；迁入 Gemini 可填占位签名跳过校验，并行调用的 FC/FR 交错排列会 400 [13]；Anthropic 须原样回传 [15]。
3. **Schema 方言**：OpenAI strict 要求所有字段 required 且 `additionalProperties:false` [111]；Gemini 是 OpenAPI 3.0 子集 [22]。
4. **工具 id**：Anthropic 要求 `^[a-zA-Z0-9_-]+$` [21]；跨家迁移历史时重写 id。
5. **模型代际规则**：GPT-5.4 起 CC 的工具调用只能配 `reasoning_effort: none` [1]；Claude 4.6+ 预填 → 400 [3]。
6. **流式解析**：`[DONE]` 有无因协议而异（§2.3、§3.1）；DeepSeek 等待时发 `: keep-alive` 注释 [112]，OpenRouter 也有 comment [102] → 解析器跳过注释行。
7. **套餐通道**：订阅过智谱 Coding Plan 的账号暂只能用 OpenAI 协议调模型 API [113]。

## 5. 未决与置信度
- ❓：MiniMax OpenAI 层的 tool_choice；Qwen 工具调用时的回传规则；智谱、Kimi、MiniMax 的 Responses 对未知字段忽略还是报错。
- ∅：智谱 Anthropic 端点无字段级文档；§3.3 的（二手）条目来自 2026-05～09 GitHub 报告，或已变。
- ⚔（文档自相矛盾，正文取可确认的一边）：Interactions 端点版本（`/v1beta`、v1、`/v1beta2` 三说）及 temperature、safety_settings、`response_mime_type` 是否支持；MiniMax Anthropic 层 tool_choice（同站两页矛盾）；OpenAI CC `store` 默认值；Gemini `functionResponse` 的 role；方舟无效 `encrypted_content` 是否报错；Qwen3 商业版思考是否仅流式；Anthropic `messages` 内能否放 `role:system`（部分模型可）；Vertex 上 Gemini 3.6 Flash 起忽略采样参数。
- 时效：规则随模型代际变化（GPT-5.4+、Claude 4.6/4.7+、Gemini 3.x）；DeepSeek 回传规则反转过。

## 来源（完整 URL = 站点前缀 + 路径）
- OpenAI 指南 `https://developers.openai.com/api/docs/guides`：[1] /migrate-to-responses · [17] /latest-model · [35] /conversation-state · [36] /prompt-caching.md · [41] /reasoning · [111] /structured-outputs
- Gemini 指南 `https://ai.google.dev/gemini-api/docs`：[2] /interactions · [13] /generate-content/thought-signatures · [16] /changelog · [28] /interactions-breaking-changes-may-2026 · [29] /migrate-to-interactions · [30] /generate-content/function-calling · [38] /generate-content/caching · [39] /caching · [42] /generate-content/thinking · [43] /thinking · [48] /streaming · [51] /generate-content/api-errors · [100] /openai
- Anthropic 指南 `https://platform.claude.com/docs/en/build-with-claude`：[3] /working-with-messages · [15] /thinking · [37] /prompt-caching · [40] /extended-thinking · [44] /structured-outputs · [47] /streaming · [109] /claude-in-amazon-bedrock · [110] /claude-on-amazon-bedrock-legacy
- DeepSeek `https://api-docs.deepseek.com`：[4] /guides/responses_api · [5] /api/create-response · [6] /updates · [14] /guides/thinking_mode · [52] / · [74] /api/create-chat-completion · [90] /guides/anthropic_api · [112] /quick_start/rate_limit
- 智谱 BigModel `https://docs.bigmodel.cn`：[7] /cn/guide/develop/claude/introduction · [8] /cn/guide/develop/claude · [9] /cn/coding-plan/latest-model · [10] /cn/coding-plan/mcp/vision-mcp-server · [11] /cn/coding-plan/mcp/search-mcp-server · [12] /cn/guide/capabilities/thinking · [53] /cn/api/introduction · [55] /cn/coding-plan/quick-start · [57] /cn/guide/develop/responses/introduction · [75] /api-reference/模型-api/对话补全 · [76] /cn/guide/capabilities/thinking-mode · [78] /cn/guide/capabilities/cache · [79] /cn/api/api-code · [113] /cn/guide/models/text/glm-5.3
- Open Responses `https://www.openresponses.org`：[18] /specification
- OpenAI 参考 `https://developers.openai.com/api/reference`：[19] /resources/chat.md · [20] /resources/responses · [24] /overview.md · [32] /resources/responses/methods/create · [46] /resources/chat/subresources/completions/streaming-events.md
- Anthropic `https://platform.claude.com/docs/en`：[21] /api/messages · [25] /api/overview · [26] /api/versioning · [31] /agents-and-tools/tool-use/handle-tool-calls · [34] /agents-and-tools/tool-use/tool-reference · [50] /api/errors · [101] /cli-sdks-libraries/libraries/openai-sdk
- Gemini 参考 `https://ai.google.dev`：[22] /api/generate-content · [23] /api/interactions-api · [27] /api · [33] /api/caching
- GitHub raw `https://raw.githubusercontent.com`：[45] /anthropics/anthropic-sdk-python/main/src/anthropic/types/message_create_params.py · [49] /openai/openai-openapi/main/openapi.yaml
- Z.ai `https://docs.z.ai`：[54] /api-reference/introduction · [56] /guides/llm/glm-5.3 · [58] /devpack/quick-start · [77] /api-reference/llm/chat-completion · [92] /devpack/tool/claude
- Kimi `https://platform.kimi.com/docs`：[59] /api/overview · [60] /api/messages · [61] /api/responses · [80] /guide/use-thinking-models · [81] /api/models-overview · [82] /api/chat
- MiniMax `https://platform.minimax.io/docs`：[62] /guides/text-m3-function-call · [63] /api-reference/text/api/openapi-responses.json · [64] /api-reference/responses-create · [83] /api-reference/text-openai-api · [91] /api-reference/text-anthropic-api · [94] /api-reference/anthropic-api-compatible-cache
- 阿里云百炼 `https://help.aliyun.com/zh/model-studio`：[65] /qwen-api-via-openai-chat-completions · [66] /regions · [67] /anthropic-api-messages · [68] /compatibility-with-openai-responses-api · [69] /qwen-api-via-openai-responses · [84] /qwen-api-via-dashscope · [85] /context-cache
- 火山方舟 `https://www.volcengine.com/docs/82379`：[70] /1494384 · [71] /2160841 · [72] /1928261 · [73] /1569618 · [86] /1449737 · [87] /1956279 · [88] /1585128 · [89] /1398933
- GitHub 社区报告（二手） `https://github.com`：[93] /zai-org/feedback/issues/411 · [95] /vybestack/llxprt-code/pull/3704 · [96] /betmoar/cc-proxy-plugin/issues/67 · [97] /zai-org/GLM-5/issues/74 · [98] /zai-org/GLM-5/issues/139 · [99] /kolega-ai/kolega-code/pull/613
- OpenRouter `https://openrouter.ai/docs`：[102] /api_reference/overview · [103] /api/api-reference/anthropic-messages/create-a-message · [104] /api_reference/responses/overview
- vLLM `https://docs.vllm.ai`：[105] /en/latest/serving/online_serving/
- Ollama `https://docs.ollama.com`：[106] /api/openai-compatibility · [107] /api/anthropic-compatibility
- llama.cpp 官方仓库 `https://github.com/ggml-org`：[108] /llama.cpp/blob/master/tools/server/README.md
