# LLM 推理 API 请求协议对照：四大源头协议 × 下游兼容层（截至 2026-09-23）

> 回答：主流 LLM API 请求协议分几类、在哪些维度不同、国内厂商的兼容层差在哪。先读 §0 结论和 §1 分类；查字段看 §2–§3；踩坑看 §4。字段名保留原文；[n] 见文末来源；❓ = 未查到，∅ = 官方未写。

## 0. 一屏看懂

1. **四个家族，看两件事就能分**：对话单元是什么（CC 的 `messages[]` / Responses 的 `input[]` items / Anthropic 的 content blocks / Gemini 的 `contents[].parts[]`），以及历史存在哪一端（只有 Responses 可选服务端保存）。见 §1。
2. **两家源头厂在换代**：OpenAI 写明 "Responses is recommended for all new projects"，Chat Completions 继续支持，Assistants API 已于 2026-08-26 下线 [1]；Google 把 generateContent 标为 Legacy，新开发推荐 Interactions API [2]；Anthropic Messages 仍无状态、未换代 [3]。
3. **Q1 DeepSeek：确实不同，性质是「兼容子集 + 私有扩展」**。2026-07-31 起支持 Responses 格式，端点 `POST https://api.deepseek.com/responses`（无 `/v1`）[4][5]；不保存状态，不支持的参数 "silently ignored"（含 `previous_response_id`、`conversation`、`store`）[4]；推理以明文 reasoning item 返回，不支持 `encrypted_content`、`summary` [4][5]。Chat 兼容层的私有点见 §3.2。
4. **Q2 智谱：有 Anthropic 端点，没有字段级兼容说明**。官方只写"某些场景下智谱与 Claude 接口仍存在差异，但不影响整体兼容性" [6]；DeepSeek、Kimi、MiniMax 则公开了支持/忽略清单 [7][8][9]。已写明的差异见 §3.3。
5. **推理内容回传是头号迁移坑**：各协议载体和规则都不同；Gemini 3 漏回 `thoughtSignature`、DeepSeek 带工具时漏回 `reasoning_content`，都直接 400 [10][11]。见 §2.4、§3.2。
6. **采样参数正在被收回**：Claude Opus 4.7+、Sonnet 5 等传非默认 `temperature`/`top_p`/`top_k` 即 400 [12]；Gemini 2026-07-21 起弃用这三个参数 [13]；Kimi 固定取值，传其他值报错 [14]。
7. **"不支持"的处理两极**：静默忽略（DeepSeek、Anthropic 的 OpenAI 兼容层、MiniMax 多数参数）[4][15][9] vs 直接报错（Kimi 固定参数、MiniMax 温度越界）[14][9]。换家不报错 ≠ 参数生效。
8. **用量口径不能直接比**：OpenAI `cached_tokens` 含在 `prompt_tokens` 内 [16]；Anthropic `input_tokens` 不含缓存读写 [17]；DeepSeek `prompt_tokens` = `prompt_cache_hit_tokens` + `prompt_cache_miss_tokens` [18]。

## 1. Taxonomy

| 家族 | 对话单元 | 状态 | 源头 | 兼容实现（本次查到） |
|---|---|---|---|---|
| **CC** Chat Completions | `messages[]{role,content}`，工具调用挂在 assistant 消息上 | 无状态 | OpenAI | 6 家国内厂商、Anthropic 兼容层 |
| **R** Responses | `input[]` items（message / function_call / reasoning…） | 可选服务端（`store`、`previous_response_id`） | OpenAI；Open Responses 开放规范 [19] | DeepSeek（无状态子集）、Qwen、方舟；Kimi/MiniMax/智谱 ❓ |
| **M** Messages | 顶层 `system` + user/assistant，content blocks（tool_use / tool_result / thinking） | 无状态 | Anthropic | 6 家国内厂商 |
| **G** Gemini | `contents[]{role: user/model, parts[]}` | generateContent 无状态；Interactions ❓ | Google | 6 家文档中未见 |

- 分法：CC/M/G 每次发全量历史，差别在切分粒度（整条消息 / 类型化块 / parts）；R 把消息、工具调用、推理拍平成 item，允许服务端续接。
- 国内厂商多**同时**暴露 CC + M（部分 + R）：兼容性按端点判断，不按厂商。
- 维度（后文表格按此排）：D1 接入 · D2 对话形状（容器、角色、system）· D3 多模态 · D4 工具 · D5 状态 · D6 推理（开关/返回/回传）· D7 输出控制与采样 · D8 流式 · D9 响应、停止原因、用量口径 · D10 缓存 · D11 兼容度（支持/忽略/报错）· D12 错误。

## 2. 源头协议对照矩阵

### 2.1 接入与对话形状（D1–D3）
| | CC | Responses | Messages | generateContent |
|---|---|---|---|---|
| 端点 | `POST /v1/chat/completions` [20] | `POST /v1/responses` [21] | `POST /v1/messages` [22] | `POST /v1beta/models/{model}:generateContent`（模型在 URL）[23] |
| 鉴权/版本 | `Authorization: Bearer` [24] | 同左 | Bearer（`x-api-key` 为 legacy fallback）+ 必填 `anthropic-version: 2023-06-01` [25][26] | `x-goog-api-key` [27]；Vertex 用 OAuth Bearer [28] |
| 容器/角色 | `messages`：developer/system/user/assistant/tool（`function` 弃用）[20][29] | `input`（字符串或 items）；user/assistant/system/developer [21] | `messages`：仅 user/assistant；连续同角色自动合并 [22] | `contents`：仅 `user`/`model` [23] |
| 系统指令 | developer 消息（o1 起取代 system）[20] | 顶层 `instructions` [1] | 顶层 `system`，无 system 角色 [22] | `systemInstruction`（仅文本）[23] |
| 多模态 | `image_url`、`input_audio`、`file` [20] | `input_image`、`input_file`（输入块无音频类型）[21] | `image`/`document`，source = base64/url/file [22] | `inlineData`、`fileData` [23] |

### 2.2 工具（D4）
| | CC | Responses | Messages | generateContent |
|---|---|---|---|---|
| 定义 | `{type:"function",function:{name,parameters,strict}}`；另有 `custom` [20] | 扁平 `{type:"function",name,parameters,strict}` [1] | `{name,input_schema,strict?}` [22] | `functionDeclarations[]`：`parameters`（OpenAPI 子集）与 `parametersJsonSchema` 二选一 [23][30] |
| 调用 | `message.tool_calls[]{id,function:{name,arguments}}`，arguments 是 JSON **字符串** [20] | item `function_call{call_id,name,arguments}` [1] | block `tool_use{id,name,input}`，input 是**对象** [31] | part `functionCall{id,name,args}`，args 是对象；Gemini 3 必返 id [23][30] |
| 回传 | `{role:"tool",tool_call_id,content}` [20] | item `function_call_output{call_id,output}` [1] | user 消息内 `tool_result{tool_use_id,content,is_error}`，须紧跟且排在 content 最前 [31] | part `functionResponse{id,name,response}`，role 用 user [30] |
| tool_choice | `none`/`auto`/`required`/指定/`allowed_tools` [20] | ❓ | `auto`/`any`/`tool`/`none` + `disable_parallel_tool_use` [22] | `mode`: AUTO/ANY/NONE/VALIDATED + `allowedFunctionNames` [32] |
| strict | 默认非严格 [1] | 省略即尝试严格 [1] | 按工具可选 [22] | — |
| 内置工具 | ❓ | web_search、file_search、code_interpreter、image_generation、remote MCP 等 [1] | 服务端工具带日期版本，如 `web_search_20260318` [33] | googleSearch、codeExecution、urlContext、fileSearch、googleMaps 等 [23] |

### 2.3 状态与缓存（D5、D10）
| | CC | Responses | Messages | generateContent |
|---|---|---|---|---|
| 历史 | 客户端手动管理 [1]；`store:true` 只为事后检索 [20] | `store` 默认 true [1]；Response 默认存 30 天，Conversations 对象不受此 TTL [34] | 无状态，每次全量 [3] | 无状态，chat 是 SDK 侧 [2] |
| 缓存 | 自动，GPT-5.6+ 最小 1,024 tokens [35]；`prompt_cache_key`、`prompt_cache_options`、part 级 `prompt_cache_breakpoint` [20] | 同左；官方称缓存利用率比 CC 高 40–80% [1] | 显式 `cache_control{type:"ephemeral",ttl:"5m"/"1h"}`，≤ 4 断点；顶层 `cache_control` = 自动 [17] | 隐式（2.5+ 默认开）+ 显式 `cachedContents`（默认 TTL 1h）[36] |

### 2.4 推理（D6）
| | CC | Responses | Messages | generateContent |
|---|---|---|---|---|
| 控制 | `reasoning_effort`: none/minimal/low/medium/high/xhigh/max [20] | `reasoning.effort`，同 7 档 [21] | `thinking.type`: enabled/disabled/adaptive + `output_config.effort` [22]；`enabled`+`budget_tokens` 在 4.7+ 报 400 [37] | `thinkingConfig{thinkingLevel,thinkingBudget,includeThoughts}` [23] |
| 返回 | 不返回，只计 `reasoning_tokens` [38] | `reasoning` item，默认带 `encrypted_content` [38] | `thinking{thinking,signature}` / `redacted_thinking{data}` [22] | `thought:true` 摘要 part + `thoughtSignature` [39][10] |
| 回传 | — | 手动管理状态时须放回 reasoning items [21] | 工具循环中 "complete and unmodified" 回传 [12] | Gemini 3：当前轮首个 functionCall 缺签名 → 400 [10] |
| 特殊 | GPT-5.4 起 CC 的工具调用只能配 `reasoning_effort: none` [1] | — | Claude 4.6+ 不支持 assistant 预填（400）[3] | — |

### 2.5 输出控制与采样（D7）
| | CC | Responses | Messages | generateContent |
|---|---|---|---|---|
| 结构化 | `response_format{type:"json_schema",json_schema:{name,schema,strict}}` [20] | `text.format{type:"json_schema",...}` [1] | `output_config.format{type:"json_schema",schema}`，已 GA [40] | `responseMimeType`+`responseSchema`（已 deprecated）→ `responseFormat.text{mimeType,schema}` [23] |
| 长度 | `max_completion_tokens`（`max_tokens` 弃用）[20] | ❓ | `max_tokens` **必填** [41] | `maxOutputTokens` [23] |
| 采样 | ❓ | ❓ | Opus 4.7+ 等非默认值 → 400 [12] | `temperature` [0, 2] [23]；2026-07-21 起弃用 [13] |

### 2.6 流式、响应、用量、错误（D8、D9、D12）
| | CC | Responses | Messages | generateContent |
|---|---|---|---|---|
| 流式 | `data:` 块 `chat.completion.chunk` / `choices[].delta`，以 `data: [DONE]` 结束；`include_usage` 末块带 usage [20][16] | 语义事件 `response.created`…`response.completed`/`error`，带 `sequence_number` [21]；OpenAI 文档未见 `[DONE]`，Open Responses 规范要求 `[DONE]` [19] | `message_start`→`content_block_*`→`message_delta`→`message_stop`，另有 `ping`/`error` [42]；已移除 `[DONE]` [26] | `:streamGenerateContent?alt=sse`，每块是完整 GenerateContentResponse；无结束标记说明 [23] |
| 停止 | `finish_reason`: stop/length/tool_calls/content_filter/function_call [20] | `status` 6 值 + `incomplete_details.reason`: max_output_tokens/max_messages/content_filter/steered [21] | `stop_reason`: end_turn/max_tokens/stop_sequence/tool_use/pause_turn/refusal/model_context_window_exceeded [22] | `finishReason`: STOP/MAX_TOKENS/SAFETY/RECITATION/MALFORMED_FUNCTION_CALL/MISSING_THOUGHT_SIGNATURE 等 + `promptFeedback.blockReason` [23] |
| 用量 | `prompt_tokens`（含 cached）、`completion_tokens`，details 有 `reasoning_tokens` [20][16] | `input_tokens`/`output_tokens` + `cached_tokens`/`cache_write_tokens`/`reasoning_tokens` [21] | `input_tokens`（不含缓存）+ `cache_creation_input_tokens`/`cache_read_input_tokens` [17] | `promptTokenCount`/`candidatesTokenCount`/`thoughtsTokenCount`/`cachedContentTokenCount`，total 含 thoughts [23] |
| 错误体 | `{"error":{message,type,param,code}}` [29] | 失败时 `response.error{code,message}` [21] | `{type:"error",error:{type,message},request_id}`；529 `overloaded_error` [43] | `{error:{code,message,status,details}}`；429 `RESOURCE_EXHAUSTED` [44] |

Gemini Interactions API（新推荐协议）的字段：❓（下一轮补）。

## 3. 变体与适配层

### 3.1 协议面：谁暴露哪些端点
| 厂商 | CC | Messages（Anthropic 兼容） | Responses | 备注 |
|---|---|---|---|---|
| DeepSeek | `https://api.deepseek.com` [45] | `…/anthropic` [45] | `POST /responses` [5] | deepseek-chat/reasoner 于 2026-07-24 停用 [46]；现行 V4.1-Flash、V4-Pro-0813 [47] |
| 智谱 | `open.bigmodel.cn/api/paas/v4`、`api.z.ai/api/paas/v4` [48][49]；Coding Plan 用 `/api/coding/paas/v4` [50] | `open.bigmodel.cn/api/anthropic`、`api.z.ai/api/anthropic`，套餐与按量同 URL [50][51] | ❓ | |
| Kimi | `api.moonshot.cn/v1` [52] | `api.moonshot.cn/anthropic` [8] | ❓ | |
| MiniMax | `api.minimax.io/v1`、`api.minimax.cn/v1` [53] | `api.minimax.io/anthropic`、`api.minimax.cn/anthropic`；官方推荐 Anthropic SDK [53][54] | ❓ | |
| Qwen/百炼 | `{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）；旧 `dashscope.aliyuncs.com` 自 2026-09-30 不再加新特性 [55][56] | `…/apps/anthropic`，`x-api-key` 或 Bearer [57] | `/compatible-mode/v1/responses` [58] | 原生 DashScope：`input.messages` + `parameters`，流式靠头 `X-DashScope-SSE: enable` [59] |
| 方舟 | `ark.cn-beijing.volces.com/api/v3` [60] | `…/api/compatible`；Coding Plan `/api/coding` [61][62] | `/api/v3/responses` [63] | model 可填 Model ID 或推理接入点 ID [60] |

### 3.2 兼容层差异（相对 OpenAI CC）
| | 推理开关/返回 | 推理回传 | 工具 | 结构化/采样/长度 | 缓存与私有字段 |
|---|---|---|---|---|---|
| DeepSeek | 思考默认开（effort 默认 high）；`reasoning_content` 与 content 同级 [11] | 无工具：传了也忽略；带工具：不回传 → 400 [11] | 思考模式下 `required`/指定 tool_choice → 400 [18] | `response_format` 仅 text/json_object；思考模式 temperature 等不报错也不生效 [18][11] | `prompt_cache_hit_tokens`/`_miss_tokens`；finish_reason 多 `insufficient_system_resource`、`aborted` [18] |
| 智谱 | `thinking.type`（GLM-5.3 传 disabled 报错）[64]；`reasoning_effort` 5.3 仅 low/high/max [65] | `clear_thinking` 默认 true，丢弃历史推理 [65]；带工具须回传 [66] | tool_choice 仅 `auto`；内置 web_search/retrieval [65]；私有 `tool_stream` [67] | 仅 text/json_object [65] | `cached_tokens` [68]；推理中途异常不返回错误码，改在 finish_reason（`sensitive`/`network_error` 等）报告 [69][67]；错误体为字符串业务码 [69] |
| Kimi | `thinking` 走 extra_body；assistant `partial` 预填 [52] | 须原样回传含 `reasoning_content` 的 assistant 消息 [70] | k2.6/k2.7-code 不支持 `required` [14] | temperature/top_p/n/penalty 固定，传其他值报错 [14] | 自动前缀缓存；`cached_tokens`/`cache_write_tokens` [71] |
| MiniMax | M3 默认思考；`reasoning_split=true` → `reasoning_content`/`reasoning_details`，否则 `<think>` 在 content [72] | 须保留完整 `response_message`（含 `reasoning_details`）[53] | ❓ | `n` 仅 1；忽略 penalty/logit_bias [72] | 被动自动缓存 [73] |
| Qwen | `enable_thinking`、`thinking_budget`（extra_body）；`reasoning_content` [55] | ❓ | 不支持 `required`；`parallel_tool_calls` 默认 false；私有 `enable_search` [55] | `max_tokens` 只限回答，`max_completion_tokens` 含思维链 [55] | 隐式（不可关）+ 显式 `cache_control`；`cached_tokens` 计入 prompt_tokens [74] |
| 方舟 | `thinking.type`: enabled/disabled/auto [60]；effort 7 档自动映射，部分模型只给推理摘要 [75] | Responses 推理项带 `summary` + `encrypted_content` [76] | Chat 无内置工具 [77]；Responses 有 web_search/mcp/knowledge_search 等 [63] | `response_format` 含 json_schema（beta）；思考模型不支持 logprobs [60] | 隐式缓存与 Responses 显式 `caching` 互斥 [78]；`expire_at` 默认 3 天、最多 7 天 [63] |

Responses 兼容的状态差异：OpenAI 默认存 30 天 [34]；DeepSeek 忽略 `store`/`previous_response_id` [4]；Qwen `store` 默认 true、response id 有效 7 天 [79]；方舟 `store` + `expire_at` [63]。

### 3.3 Anthropic 兼容端点对照（Q2 展开）
| | DeepSeek [7] | 智谱 | Kimi [8] | MiniMax [9] |
|---|---|---|---|---|
| 官方字段表 | 有（Supported/Ignored/Not Supported） | **无** [6] | 有（逐字段说明） | 有 |
| thinking | 支持，`budget_tokens` 忽略 | Coding Plan：Claude Code 传的 `thinking.type`/`output_config.effort` 被映射到内部档位，关闭值 → low（仍轻量思考）[80] | thinking 块连 `signature` 原样回传 | M3 默认关（`adaptive` 开），M2.x 不可关 |
| tool_choice | auto/any/tool；`disable_parallel_tool_use` 忽略 | ∅ | auto/any/none | ⚔ 见 §5 |
| cache_control | Ignored | ∅ | 仅顶层生效，消息内忽略 | 显式缓存 5 分钟 [81] |
| 内容块 | document、redacted_thinking、mcp_* 等 Not Supported | ∅ | text/image/thinking/tool_use/tool_result | M3 含 image/video/thinking；M2.x 仅 text + 工具 |
| 其他 | `anthropic-version`/`anthropic-beta` 忽略；`claude-opus*` 映射到 deepseek-v4-pro | 订阅过 Coding Plan 的账号暂只能用 OpenAI 协议调模型 API [82] | — | 忽略 top_k、stop_sequences、mcp_servers；temperature [0, 2]，越界报错 |

源头厂自己的 OpenAI 兼容层：Anthropic 把 system/developer 消息提升并拼接到开头、忽略 `strict`、temperature > 1 截断为 1、多数不支持字段静默忽略 [15]；Gemini 的 OpenAI 兼容层 ❓。

## 4. 用户需要知道的坑（按踩中概率）
1. **工具参数类型**：CC/R 的 `arguments` 是字符串，且 "the model does not always generate valid JSON" [20]；M/G 是对象 → 统一先解析并容错。
2. **跨家迁移历史**：推理载体互不相通；迁入 Gemini 可用占位签名跳过校验 [10]，Anthropic 必须原样回传 [12]。
3. **Schema 方言**：OpenAI strict 要求所有字段 required 且 `additionalProperties: false` [83]；Gemini 是 OpenAPI 3.0 子集 [23] → 维护一份 JSON Schema，按目标转换。
4. **工具 id 字符集**：Anthropic `tool_use.id` 须匹配 `^[a-zA-Z0-9_-]+$` [22]；跨家迁移历史时重写 id。
5. **长度参数语义**：Anthropic `max_tokens` 必填 [41]；Qwen、方舟的 `max_completion_tokens` 含思维链 [55][60]；DeepSeek 不设时默认 8K（思考 64K）[18]。
6. **流式解析**：CC 等 `[DONE]`；Anthropic 看 `message_stop`；DeepSeek 等待期间持续发 `: keep-alive` 注释（非流式为空行）[84] → SSE 解析器要跳过注释行。
7. **兼容层改写模型名**：DeepSeek 的 Anthropic 层把 `claude-opus*` 映射到 deepseek-v4-pro [7]；"能跑"不代表用的是你以为的模型。
8. **套餐端点**：智谱 Coding Plan 的 OpenAI 端点为 `/api/coding/paas/v4`（Anthropic 端点与按量相同）[50]；方舟 Coding Plan 用 `/api/coding`、`/api/coding/v3` [62]；智谱套餐额度只在规定工具内可用 [85]。
9. **限流语义变了**：DeepSeek 现行文档有并发上限，超限返回 429 [84]。

## 5. 未决与置信度
- ❓：Gemini Interactions 全行；Gemini 的 OpenAI 兼容层；Responses 的长度参数与 tool_choice；智谱/Kimi/MiniMax 的 Responses 兼容；网关（OpenRouter、LiteLLM）、自托管（vLLM、Ollama）、云托管（Bedrock、Vertex 上的 Claude、Azure）。
- ∅：智谱 Anthropic 端点的字段级差异（两站 llms-full.txt 检索无命中）。实测观察（非文档）：假 key 请求返回 `{"error":{"type":"1000",…}}`，不是 Anthropic 的 `type:"error"` 结构。
- ⚔（文档自相矛盾，正文取现行页）：OpenAI CC `store` 默认值（spec 写 false，迁移指南写新账号默认存储）；Gemini `functionResponse` 的 role（user vs function）；GLM-5.3 关闭思考（报错 vs Coding Plan 映射为 low）；MiniMax Anthropic 层 tool_choice（"Fully supported" vs "Only auto and none"）；方舟无效 `encrypted_content` 是否报错（2026-09-09 公告称不再报错）；Anthropic `thinking.display` 默认值；Qwen 思考模式是否仅流式。
- 时效：GPT-5.4+、Claude 4.6/4.7+、Gemini 3.x 的规则按模型代际变；DeepSeek 回传规则反转过（旧文档：回传 `reasoning_content` 即 400）。

## 来源（官方文档；完整 URL = 站点前缀 + 路径）
- OpenAI `https://developers.openai.com/api`：[1] /docs/guides/migrate-to-responses · [16] /reference/resources/chat/subresources/completions/streaming-events.md · [20] /reference/resources/chat.md · [21] /reference/resources/responses · [24] /reference/overview.md · [34] /docs/guides/conversation-state · [35] /docs/guides/prompt-caching.md · [38] /docs/guides/reasoning · [83] /docs/guides/structured-outputs
- Google Gemini API `https://ai.google.dev`：[2] /gemini-api/docs/migrate-to-interactions · [10] /gemini-api/docs/generate-content/thought-signatures · [13] /gemini-api/docs/changelog · [23] /api/generate-content · [27] /api · [30] /gemini-api/docs/generate-content/function-calling · [32] /api/caching · [36] /gemini-api/docs/generate-content/caching · [39] /gemini-api/docs/generate-content/thinking · [44] /gemini-api/docs/generate-content/api-errors
- Anthropic `https://platform.claude.com/docs/en`：[3] /build-with-claude/working-with-messages · [12] /build-with-claude/thinking · [15] /cli-sdks-libraries/libraries/openai-sdk · [17] /build-with-claude/prompt-caching · [22] /api/messages · [25] /api/overview · [26] /api/versioning · [31] /agents-and-tools/tool-use/handle-tool-calls · [33] /agents-and-tools/tool-use/tool-reference · [37] /build-with-claude/extended-thinking · [40] /build-with-claude/structured-outputs · [42] /build-with-claude/streaming · [43] /api/errors
- DeepSeek `https://api-docs.deepseek.com`：[4] /guides/responses_api · [5] /api/create-response · [7] /guides/anthropic_api · [11] /guides/thinking_mode · [18] /api/create-chat-completion · [45] / · [46] /updates · [47] /quick_start/pricing · [84] /quick_start/rate_limit
- 智谱 BigModel `https://docs.bigmodel.cn`：[6] /cn/guide/develop/claude/introduction · [48] /cn/api/introduction · [50] /cn/coding-plan/quick-start · [64] /cn/guide/capabilities/thinking · [65] /api-reference/模型-api/对话补全 · [66] /cn/guide/capabilities/thinking-mode · [68] /cn/guide/capabilities/cache · [69] /cn/api/api-code · [80] /cn/coding-plan/latest-model · [82] /cn/guide/models/text/glm-5.3 · [85] /cn/coding-plan/faq
- Kimi `https://platform.kimi.com/docs`：[8] /api/messages · [14] /api/models-overview · [52] /api/overview · [70] /guide/use-thinking-models · [71] /api/chat
- MiniMax `https://platform.minimax.io/docs`：[9] /api-reference/text-anthropic-api · [53] /guides/text-m3-function-call · [54] /api-reference/api-overview · [72] /api-reference/text-openai-api · [73] /api-reference/text-prompt-caching · [81] /api-reference/anthropic-api-compatible-cache
- Open Responses `https://www.openresponses.org`：[19] /specification
- Google Cloud `https://docs.cloud.google.com/gemini-enterprise-agent-platform`：[28] /resources/locations
- GitHub raw `https://raw.githubusercontent.com`：[29] /openai/openai-openapi/main/openapi.yaml · [41] /anthropics/anthropic-sdk-python/main/src/anthropic/types/message_create_params.py
- Z.ai `https://docs.z.ai`：[49] /api-reference/introduction · [51] /guides/llm/glm-5.3 · [67] /api-reference/llm/chat-completion
- 阿里云百炼 `https://help.aliyun.com/zh/model-studio`：[55] /qwen-api-via-openai-chat-completions · [56] /regions · [57] /anthropic-api-messages · [58] /compatibility-with-openai-responses-api · [59] /qwen-api-via-dashscope · [74] /context-cache · [79] /qwen-api-via-openai-responses
- 火山方舟 `https://www.volcengine.com/docs/82379`：[60] /1494384 · [61] /2160841 · [62] /1928261 · [63] /1569618 · [75] /1449737 · [76] /1956279 · [77] /1585128 · [78] /1398933
