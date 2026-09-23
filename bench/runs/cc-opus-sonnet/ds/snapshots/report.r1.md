# LLM API 请求协议对照：Chat Completions / Responses / Messages / generateContent 与下游兼容实现

> 回答：四个参照协议差在哪；下游厂商「兼容 X」时实际偏差；换协议会踩的坑。截至 2026-09-23，只依据官方文档，字段名保留原文。§0 结论，§2 查字段，§3 查厂商。❓＝未查到，∅＝官方没有该项。

## 0. 一屏看懂

1. **四种形状**：Chat Completions＝`messages`→`choices[].message`；Responses＝`input` item 数组→`output` item 数组，推理、工具调用、工具结果都是独立 item；Messages＝`content` block 数组，只有 user/assistant，`system` 在顶层；generateContent＝`contents[].parts[]`，角色只有 `user`/`model`，参数集中在 `generationConfig` [1][2][9][19]。
2. **状态**：Chat、Messages、generateContent 每轮都要客户端回传全量历史；Responses 默认 `store:true`，可用 `previous_response_id` 或 `conversation` 让服务端接续 [1][3]。Google 的 Interactions API（2026-06 GA，`previous_interaction_id`）被官方推荐给新项目，generateContent 被称为 legacy 但仍完全支持 [22]。
3. **官方定位**：OpenAI「Chat Completions 仍受支持，新项目推荐 Responses」；Assistants API 已于 2026-08-26 下线 [2]。
4. **跨协议最大的坑是推理内容**：OpenAI Chat 不返回推理文本；Responses 返回 `reasoning` item（含 `encrypted_content`）；Anthropic 的 `thinking` block 带 `signature`，须原样按原顺序回传，否则 400；Gemini 缺 `thoughtSignature` 会得到 `MISSING_THOUGHT_SIGNATURE`；国内厂商用非标准字段 `reasoning_content`，回传规则各家不同（§3）[5][9][19]。
5. **Q1 DeepSeek**：主协议是 Chat Completions 形状加一套方言：`reasoning_content`、`prompt_cache_hit/miss_tokens`、多出两个 `finish_reason`、`response_format` 没有 `json_schema`、`strict` 与前缀续写要走 `/beta`。2026-08-13 起同一 base_url 原生支持 Responses API，但 `developer` 被当作 `user`、`parallel_tool_calls` 被忽略。Anthropic 兼容端点把 `claude-*` 模型名静默映射成自家模型（opus→`deepseek-v4-pro`）[24][26][27][28]。
6. **Q2 智谱**：Anthropic 兼容端点 `https://open.bigmodel.cn/api/anthropic`，官方只写「某些场景下智谱与 Claude 接口仍存在差异」，**没有字段级支持表**（DeepSeek、Kimi、Qwen 都给了）。能确认的只在接入层：用 Claude Code 的 `ANTHROPIC_DEFAULT_*_MODEL` 把档位指到 GLM 模型、effort 五档折成两档、`[1m]` 后缀开 1M 上下文 [34][35]。
7. **「兼容」≠ 等价**：不支持的字段多数被**静默忽略**（Anthropic 的 OpenAI 兼容层忽略 `response_format`、`strict`、`reasoning_effort`；Gemini 兼容层忽略未列参数），少数直接 400（DeepSeek 思考模式下 `tool_choice:"required"`）[18][23][24]。
8. **参数是否合法越来越取决于模型而不是协议**：Anthropic 对 Opus 4.6 之后发布的模型弃用 `temperature/top_p/top_k`，4.6+ 不支持预填，4.7+ 不支持 `thinking.type:"enabled"`；Kimi 现役旗舰固定 `temperature=1.0`，传别的值报错 [9][14][17][42]。

## 1. Taxonomy

分类轴：**A1 形状谱系**（决定字段名与嵌套）、**A2 状态在哪端**（决定要不要回传历史和推理）、**A3 实体角色**（参照协议／参照厂商自家兼容层／第三方模型厂／网关与自托管／开放规范）。

| 家族 | 参照 | 为什么是一类 | 状态 | 本文涉及的兼容实现 |
|---|---|---|---|---|
| Chat | OpenAI `/v1/chat/completions` | 一条条 message，工具调用挂在 assistant message 上 | 无状态 | DeepSeek、智谱 v4、Kimi、Qwen、火山方舟、vLLM、Anthropic/Gemini 自家兼容层 |
| Items | OpenAI `/v1/responses` | 输入输出都是带 `type` 的 item，推理与工具是一等对象 | 可选服务端状态 | DeepSeek、智谱、Kimi、Qwen、vLLM、llama.cpp、OpenRouter/Ollama（仅无状态）；Open Responses 规范 |
| Blocks | Anthropic `/v1/messages` | 内容是 typed block，`tool_use`/`tool_result`/`thinking` 都是 block | 无状态 | DeepSeek、智谱、Kimi、Qwen、MiniMax、火山方舟、SGLang、llama.cpp、Bedrock |
| Parts | Gemini `:generateContent` | `contents/parts`，配置集中在 `generationConfig` | 无状态＋缓存资源 | Vertex AI 同形 |

维度（§2 的表按此排）：D1 端点鉴权｜D2 输入结构｜D3 历史谁保存｜D4 输出容器｜D5 工具声明/调用/回传｜D6 推理控制与回传｜D7 JSON 约束｜D8 流式分帧与结束｜D9 生成参数｜D10 停止原因/用量/缓存｜D11 厂商暴露哪些协议入口｜D12 不支持的字段是忽略还是报错。

## 2. 对照矩阵（四个参照协议）

**D1–D4 端点、输入、状态、输出**

| | Chat Completions | Responses | Anthropic Messages | Gemini generateContent |
|---|---|---|---|---|
| 端点 | `POST https://api.openai.com/v1/chat/completions` [1] | `POST /v1/responses`；另有 GET/DELETE/cancel/input_items、`/conversations` [1] | `POST https://api.anthropic.com/v1/messages`；`count_tokens`、`batches` [10] | `POST …/v1beta/models/{model}:generateContent`；v1＝稳定，v1beta＝新特性 [19] |
| 鉴权/版本 | `Authorization: Bearer`；可选 `OpenAI-Organization`/`OpenAI-Project` [7] | 同左 | `anthropic-version: 2023-06-01` 必填；`Authorization: Bearer` 为主，`x-api-key` 为旧版回退 [10][11] | `x-goog-api-key` 头或 `?key=`；Vertex 用 OAuth [19][20] |
| 对话字段 | `messages[]` | `input`（字符串或 item 数组）＋`instructions` | `messages[]`＋顶层 `system` | `contents[]`＋`systemInstruction`（仅文本） |
| 角色 | developer/system/user/assistant/tool（function 已弃用） | user/system/developer/assistant | 仅 user/assistant；连续同角色会被合并 [9] | `user`/`model` ⚔§5 |
| 多模态块 | `text`/`image_url`/`input_audio`/`file` | `input_text`/`input_image`/`input_file` | `image`/`document`，可引用 Files API 的 `file_id` | `inlineData`/`fileData` |
| 服务端状态 | `store` 仅供蒸馏/评测，默认 false [1] | `store` 缺省 true，至少保留 30 天；`previous_response_id` 与 `conversation` 互斥且不继承 `instructions`；Conversation 不受 30 天 TTL 限制 [1][3] | 官方称 stateless [9] | 无；可引用 `cachedContents` 资源 [19] |
| 输出容器 | `choices[].message{content,refusal,tool_calls,annotations,audio}` | `output[]` items；`status`：completed/failed/in_progress/cancelled/queued/incomplete；`output_text` 只是 SDK 便捷属性 [1] | `content[]` blocks；`id`（msg_…）；拒答＝`stop_reason:"refusal"` [9] | `candidates[].content.parts`；`promptFeedback.blockReason` |
| 多候选 | `n`（1–128） | ∅ | ∅ | `candidateCount` ❓ |

**D5 工具调用**

| | Chat | Responses | Messages | generateContent |
|---|---|---|---|---|
| 声明 | `{type:"function",function:{name,description,parameters,strict}}` | `{type:"function",name,description,parameters,strict}`；省略 strict 时尽量严格 [1][2] | `{name,description,input_schema,strict}` | `functionDeclarations[{name,description,parameters｜parametersJsonSchema}]` |
| 选择 | `tool_choice` none/auto/required/指定；`parallel_tool_calls` 默认 true | 同左 | `tool_choice` auto/any/tool/none；`disable_parallel_tool_use` | `functionCallingConfig.mode` AUTO/ANY/NONE/VALIDATED＋`allowedFunctionNames` |
| 调用 | `tool_calls[{id,function{name,arguments}}]`，arguments 是 JSON 字符串 | `function_call{call_id,name,arguments}` item | `tool_use{id,name,input}`，input 是对象 | `functionCall{id?,name,args}`，args 是对象 |
| 回传 | `role:"tool"`＋`tool_call_id` [8] | `function_call_output{call_id,output}` | user 消息里的 `tool_result{tool_use_id,content,is_error}`，且必须排在最前 [13] | `functionResponse{id?,name,response}` |
| 内置工具 | `web_search_options` | 16 类：web_search、file_search、code_interpreter、computer、image_generation、mcp、shell、apply_patch… | 带日期版本的类型名：`web_search_20260209`、`code_execution_20260521`、`bash_20250124`… | googleSearch、codeExecution、urlContext、fileSearch、googleMaps、computerUse、mcpServers |

**D6 推理 · D7 结构化输出 · D9 生成参数**

| | Chat | Responses | Messages | generateContent |
|---|---|---|---|---|
| 推理控制 | `reasoning_effort`：none/minimal/low/medium/high/xhigh/max | `reasoning{effort,summary}`，summary＝auto/concise/detailed | `thinking{type:"enabled",budget_tokens≥1024}` 或 `{type:"adaptive"}`＋`output_config.effort` [9] | `thinkingConfig{thinkingBudget｜thinkingLevel,includeThoughts}`；`thinkingLevel` 用于 Gemini 3+ |
| 推理返回 | 不返回文本，只计 `reasoning_tokens` [5] | `reasoning` item（summary、`encrypted_content`） | `thinking`（默认 summarized）＋`signature`；`redacted_thinking` | `thought` part；`thoughtSignature` 可挂在任意 part |
| 回传要求 | — | 用 `previous_response_id` 或回传 reasoning item ⚔§5 | 原样原序回传，改动即 400 [9] | 回传签名，缺失返回 `MISSING_THOUGHT_SIGNATURE` [19] |
| JSON 约束 | `response_format{type:"json_schema",json_schema{…,strict}}`；`json_object` 须在提示里要求 JSON | `text.format`（替代 response_format）；`text.verbosity` [2] | `output_config.format`（已 GA，无需 beta 头）；工具 `strict:true` [16] | `responseMimeType:"application/json"`＋`responseJsonSchema`（`responseSchema` 已弃用） |
| max tokens | `max_completion_tokens`（`max_tokens` 已弃用，且不兼容 o 系列） | `max_output_tokens` | `max_tokens` **必填** | `maxOutputTokens` ❓ |
| temperature | 0–2 | 0–2 | 0–1 | 0–2 |
| 其他 | top_p、stop≤4、seed（已标 deprecated）、n、penalties、logit_bias、logprobs；无 top_k | 无 stop/n/seed [1] | top_p、top_k、`stop_sequences`；无 seed/n | topP/topK ❓、`stopSequences`≤5、logprobs 0–20、`safetySettings` |

**D8 流式 · D10 停止与用量**

| | Chat | Responses | Messages | generateContent |
|---|---|---|---|---|
| 开启 | `stream:true` | `stream:true` | `stream:true` | `:streamGenerateContent?alt=sse` |
| 分帧 | `chat.completion.chunk`，`choices[].delta` | 带 `event:` 的语义事件：`response.created`→`response.output_text.delta`/`response.function_call_arguments.delta`→`response.completed` [4] | `message_start`→`content_block_start/delta/stop`（`text_delta`/`input_json_delta`/`thinking_delta`/`signature_delta`）→`message_delta`→`message_stop`，穿插 `ping` [12] | 每块都是完整 `GenerateContentResponse` |
| 结束 | `data: [DONE]` | `response.completed` ⚔§5 | `message_stop`；2023-06-01 版起没有 `[DONE]` [11] | 无哨兵说明 |
| 流式用量 | `stream_options.include_usage` 在 `[DONE]` 前多发一个 usage chunk | ❓ | `message_delta.usage` 是累计值 | ❓ |
| 停止原因 | `finish_reason`：stop/length/tool_calls/content_filter/function_call(弃用) | `incomplete_details.reason`：max_output_tokens/max_messages/content_filter/steered | `stop_reason`：end_turn/max_tokens/stop_sequence/tool_use/pause_turn/refusal/model_context_window_exceeded | `finishReason` 19 项，含 SAFETY、RECITATION、MALFORMED_FUNCTION_CALL、MISSING_THOUGHT_SIGNATURE |
| 用量字段 | `prompt_tokens`/`completion_tokens`；`prompt_tokens_details.cached_tokens`；`completion_tokens_details.reasoning_tokens` | `input_tokens`/`output_tokens`；`input_tokens_details.cached_tokens`；`output_tokens_details.reasoning_tokens` | `input_tokens` **不含**缓存；另有 `cache_creation_input_tokens`、`cache_read_input_tokens`，三者相加才是总输入 [15] | `promptTokenCount`/`candidatesTokenCount`/`thoughtsTokenCount`/`cachedContentTokenCount`/`toolUsePromptTokenCount` |
| 缓存 | 自动前缀缓存（GPT-5.6+ 至少 1,024 tokens）；`prompt_cache_key`；`prompt_cache_retention` 已弃用→`prompt_cache_options.ttl`（in_memory/24h）[6] | 同左 | 显式 `cache_control{type:"ephemeral",ttl:"5m"/"1h"}`，最多 4 个断点，最小 512–4096 tokens 视模型；所谓自动缓存也要在顶层加一个 `cache_control` [15] | 隐式缓存（2.5+ 默认开，最小 2048/4096）＋显式 `cachedContents` [21] |

## 3. 变体与适配层

**D11 协议入口**（✅＝官方有该入口）

| 厂商 | Chat 兼容 | Responses 兼容 | Anthropic 兼容 | 备注 |
|---|---|---|---|---|
| DeepSeek | `https://api.deepseek.com`（`/beta` 开 strict/前缀续写/FIM） | ✅ 同 base_url（2026-08-13） | `…/anthropic` | 模型 `deepseek-v4-pro`/`deepseek-flash`；`deepseek-chat/reasoner` 2026-07-24 停用 [24][28] |
| 智谱 | `open.bigmodel.cn/api/paas/v4`（z.ai：`api.z.ai/api/paas/v4`） | ✅ `…/api/v1` | `…/api/anthropic` | Coding Plan 的 Chat 走 `/api/coding/paas/v4` [33][37] |
| Kimi | `api.moonshot.cn/v1`（.ai 同构） | ✅ `/v1/responses` | `…/anthropic` | [39] |
| Qwen/百炼 | `dashscope.aliyuncs.com/compatible-mode/v1`（多地域） | ✅ `…/compatible-mode/v1/responses` | `…/apps/anthropic`，只有 `/v1/messages`，没有 `/v1/models` | 原生 `/api/v1/services/aigc/text-generation/generation` [44][45][46] |
| MiniMax | ❓ | ❓ | `api.minimax.io/anthropic` | M2.x 思考不可关 [51] |
| 火山方舟 | `/api/v3`（Coding 页写 `/api/coding/v3` ⚔） | ❓ | `/api/compatible` | [52] |

**Q1：DeepSeek 相对 OpenAI 官方**

| 差异点 | DeepSeek |
|---|---|
| 推理 | 思考默认开启、默认 high；`reasoning_effort` 只有 none/low/high/max，minimal/medium/xhigh 被静默映射；返回 `reasoning_content` [24][25] |
| 推理回传 | 带 tools 的轮次必须回传 `reasoning_content`，否则 400；不带 tools 时不需要，传了也被忽略 [25] |
| 思考模式限制 | `temperature`、penalties 静默无效；`tool_choice` 为 required/指定函数 → 400 [24][25] |
| 参数 | 仍用 `max_tokens`（1–393216，默认 8K 非思考/64K 思考）；`frequency/presence_penalty` 已弃用、传了不生效；`response_format` 只有 text/json_object [24] |
| 用量 | 另给 `prompt_cache_hit_tokens`/`prompt_cache_miss_tokens`，`cached_tokens`＝hit；硬盘缓存默认对所有用户开启 [24][31] |
| 其他 | `finish_reason` 多 `insufficient_system_resource`、`aborted`；流式 usage 跟在最后一个内容 chunk 上，不单发；strict 工具要 `/beta` [24][29] |
| 专有 | 前缀续写（末条 assistant `prefix:true`，`/beta`）；FIM（`POST /completions`，`/beta`，上限 4K）[30][32] |
| Responses | `developer` 当 `user`；`parallel_tool_calls` 忽略（恒并行）；流式无 `[DONE]`；其余字段 ❓ [26] |
| Anthropic 兼容 | `anthropic-version` 忽略，`anthropic-beta` 对 /messages 忽略；`document` 不支持；`cache_control` 全忽略；`thinking` 支持但 `budget_tokens` 忽略；`disable_parallel_tool_use`、`mcp_servers`、`top_k` 忽略；`claude-opus*`→v4-pro，`sonnet*/haiku*`→flash [27] |

**Q2：智谱相对 Anthropic 官方（及其原生 v4）**

| 差异点 | 智谱 |
|---|---|
| Anthropic 兼容 | 端点 `/api/anthropic/v1/messages`，示例用 `x-api-key`；字段级支持表 ∅；Claude Code 档位默认映射 GLM-4.7，升级后 sonnet/opus→`glm-5.2[1m]`；effort low/medium/high→GLM high，xhigh/max→GLM max [34][35] |
| 原生 v4 | `thinking{type}`＋`clear_thinking`（false＝保留思考，须原样回传）；`tool_choice` 只支持 auto；`tool_stream` 流式工具调用；`response_format` 无 json_schema；temperature [0,1]；`stop` 最多 4 个；`finish_reason` 多 `sensitive`/`network_error`/`model_context_window_exceeded` [33] |
| Responses | 官方自述差异：默认 `store=false`、流式结束不发 `[DONE]`、未提供 cancel [36] |

**Kimi / Qwen**

| 差异点 | Kimi | Qwen/百炼 |
|---|---|---|
| 推理 | `reasoning_content` 先于 content；k2.6 用 `thinking.type`，k3 用 `reasoning_effort`；多轮须回传完整 assistant message [41] | `enable_thinking`、`thinking_budget`；部分开源版思考只支持流式 [47] |
| 参数 | 现役旗舰 temperature/top_p/n/penalty 固定，传别的值报错；`max_tokens` 弃用→`max_completion_tokens` [38][42] | 只有 `messages[0]` 可为 system；非标准 `enable_search` [49] |
| 结构化 | text/json_object/json_schema | text/json_object/json_schema |
| 缓存 | 隐式前缀缓存；`prompt_tokens_details.cached_tokens`/`cache_write_tokens` | 隐式（不可关）＋显式 `cache_control`（5 分钟，≥1024 tokens）[48] |
| Anthropic 兼容 | `Authorization: Bearer`；`stop_reason` 无 stop_sequence/pause_turn；`output_config.effort` low/high/max；`cache_control` 只认顶层；`input_tokens` 口径与 Chat 不同 [40] | 支持 13 个参数（含 top_k、thinking、output_config）；temperature 取 [0,2)，与官方 [0,1] 不同 [45] |

**自家兼容层（用 OpenAI SDK 调 Claude / Gemini）**

| | Anthropic `https://api.anthropic.com/v1/` | Gemini `…/v1beta/openai/` |
|---|---|---|
| 定位 | 测试/对比用，官方称不是长期或生产方案 [18] | beta；不用 OpenAI 库就直接调原生 [23] |
| 忽略 | `response_format`、`strict`、`reasoning_effort`、logprobs、seed、penalties、store 等 | 未列出的参数静默忽略 |
| 推理 | `extra_body.thinking`；Claude 5 默认开启 | `reasoning_effort` 映射 thinking_level/budget；`extra_body.google.thinking_config` |
| 其他 | `n` 必须为 1；temperature>1 截断为 1；system/developer 合并成一条放最前；不支持 prompt caching；audio 被剥离 | `extra_body.google.cached_content`；Batch 不支持文件上传下载 |

**其他实现**：Open Responses 是 OpenAI 发布、基于 Responses API 的开源多厂商规范 [50]；OpenRouter 的 Responses 无状态，`store:true` 或 `previous_response_id` 返回 400 [54]；Ollama v0.13.3 起支持 Responses，仅无状态 [56]；llama.cpp 支持 `/v1/messages` 与 `/v1/responses` [57]；SGLang 的 `/v1/messages` base_url 不带 `/v1` [55]；xAI 的 Anthropic SDK 兼容已完全弃用，改用 Responses 或 gRPC [53]；Bedrock 的 `bedrock-mantle` 端点实现 Anthropic Messages [58]；Azure OpenAI v1 GA 起不再需要 `api-version` [59]。

## 4. 用户需要知道的坑（按踩中概率）

1. **推理回传** → 400 或多轮质量下降 → 各家规则不同（§2 D6、§3）→ 保存上一轮 assistant 的原始对象整体回传，不要只存 content。
2. **把缓存算错** → 成本/上下文估算偏差 → Anthropic 的 `input_tokens` 不含缓存读写，Kimi 的 Anthropic 端口径又与其 Chat 不同，DeepSeek 另报 hit/miss → 按各家定义换算总输入 [15][40][24]。
3. **max tokens 命名不一** → 参数被拒或被忽略 → 按 §2 D9 逐家映射；DeepSeek、智谱仍用 `max_tokens`，Kimi 已弃用它。
4. **兼容层静默忽略** → 以为 `strict`、`response_format`、`reasoning_effort` 生效其实没有 → 在响应侧做 schema 校验 [18][23]。
5. **temperature 范围不一** → 报错或行为漂移 → OpenAI/Gemini 0–2，Anthropic 0–1，智谱 [0,1]，百炼 Anthropic 端 [0,2)，Kimi 旗舰固定 1.0。
6. **流式结束判定** → 挂起或提前结束 → Chat 家族以 `data: [DONE]` 收尾，Messages 以 `message_stop`，Responses 以 `response.completed` 等事件；DeepSeek usage 在最后内容块，Kimi 每个 choice 的结束块都带 usage [43]。
7. **流式工具参数分片** → JSON 解析失败 → `delta.tool_calls`、`response.function_call_arguments.delta`、`input_json_delta` 都要拼完再解析 [8][12]。
8. **tool_choice 不齐** → 400 → 智谱只支持 auto；DeepSeek 思考模式、Kimi 部分模型不支持 required。
9. **模型代际变更** → 老代码突然 400 → Anthropic 4.6+ 禁预填、4.7+ 须改 `adaptive` [14][17]。
10. **模型名被映射** → 日志里的 `claude-*` 并非真实模型 → DeepSeek 的 Anthropic 端点在服务端重映射；智谱靠客户端 `ANTHROPIC_DEFAULT_*_MODEL` 指定 [27][35]。

## 5. 未决与置信度

- ⚔ OpenAI `reasoning.encrypted_content`：规范称「默认填充」，`include` 枚举又列为需显式选择；OpenAI Responses 流是否发 `[DONE]` 只从示例推断，智谱把「不发 `[DONE]`」列为与 OpenAI 的差异。
- ⚔ Gemini：`Content.role` 只允许 user/model，但同页函数说明写 FunctionResponse 用 `"function"`；`reasoning_effort` 映射在 ai.google.dev 是 4 档（含 minimal），Vertex 是 3 档（1K/8K/24K）。
- ⚔ Qwen：`tool_choice:"required"` 适用范围、缓存 usage 字段路径两页不一致。Kimi temperature：迁移指南写 [0,1] 可调，模型总览写固定，按后者（现役模型）。
- ❓ DeepSeek Responses 字段级支持；智谱 Anthropic 字段级行为；Interactions API 形状；MiniMax、方舟细节；Gemini `maxOutputTokens`/`topK`/`candidateCount` 原句。
- 时效：OpenAI 规范 v2.3.0（2026-09-22 提交）；DeepSeek 5 周内两次协议变更；Kimi `$web_search` 预计 2026-10-20 下线；文档里的模型已是 Claude 5、GPT-6 代。

## 来源

[1] OpenAPI 规范 https://github.com/openai/openai-openapi/blob/master/openapi.yaml
[2] 迁移指南 https://developers.openai.com/api/docs/guides/migrate-to-responses
[3] 会话状态 https://developers.openai.com/api/docs/guides/conversation-state
[4] Streaming https://developers.openai.com/api/docs/guides/streaming-responses
[5] Reasoning https://developers.openai.com/api/docs/guides/reasoning
[6] 提示缓存 https://developers.openai.com/api/docs/guides/prompt-caching
[7] Auth https://developers.openai.com/api/docs/api-reference/authentication
[8] 函数调用 https://developers.openai.com/api/docs/guides/function-calling
[9] Messages https://platform.claude.com/docs/en/api/messages
[10] Overview https://platform.claude.com/docs/en/api/overview
[11] Versioning https://platform.claude.com/docs/en/api/versioning
[12] Streaming https://platform.claude.com/docs/en/build-with-claude/streaming
[13] Tool calls https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
[14] 扩展思考 https://platform.claude.com/docs/en/build-with-claude/extended-thinking
[15] 提示缓存 https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[16] 结构化输出 https://platform.claude.com/docs/en/build-with-claude/structured-outputs
[17] Errors https://platform.claude.com/docs/en/api/errors
[18] OpenAI SDK 兼容 https://platform.claude.com/docs/en/api/openai-sdk
[19] generateContent https://ai.google.dev/api/generate-content
[20] 函数调用 https://ai.google.dev/gemini-api/docs/function-calling
[21] Caching https://ai.google.dev/gemini-api/docs/caching
[22] Interactions https://ai.google.dev/gemini-api/docs/interactions-overview
[23] OpenAI 兼容 https://ai.google.dev/gemini-api/docs/openai
[24] Chat https://api-docs.deepseek.com/api/create-chat-completion
[25] 思考模式 https://api-docs.deepseek.com/guides/thinking_mode
[26] Responses https://api-docs.deepseek.com/guides/responses_api
[27] Anthropic https://api-docs.deepseek.com/guides/anthropic_api
[28] Updates https://api-docs.deepseek.com/updates
[29] Tool calls https://api-docs.deepseek.com/guides/tool_calls
[30] 前缀续写 https://api-docs.deepseek.com/guides/chat_prefix_completion
[31] KV cache https://api-docs.deepseek.com/guides/kv_cache
[32] FIM https://api-docs.deepseek.com/guides/fim_completion
[33] 智谱对话补全 https://docs.bigmodel.cn/api-reference/模型-api/对话补全
[34] Claude 兼容 https://docs.bigmodel.cn/cn/guide/develop/claude/introduction
[35] Claude Code https://docs.bigmodel.cn/cn/guide/develop/claude
[36] Responses https://docs.bigmodel.cn/cn/guide/develop/responses/introduction
[37] Coding 工具 https://docs.z.ai/devpack/tool/others
[38] Kimi Chat https://platform.kimi.com/docs/api/chat
[39] API 总览 https://platform.kimi.com/docs/api/overview
[40] Messages https://platform.kimi.com/docs/api/messages
[41] 思考模型 https://platform.kimi.com/docs/guide/use-thinking-models
[42] 模型总览 https://platform.kimi.com/docs/api/models-overview
[43] 迁移指南 https://platform.kimi.com/docs/guide/migrating-from-openai-to-kimi
[44] 百炼 Base URL https://help.aliyun.com/zh/model-studio/base-url
[45] Anthropic 兼容 https://help.aliyun.com/zh/model-studio/anthropic-api-messages
[46] Responses 兼容 https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api
[47] 深度思考 https://help.aliyun.com/zh/model-studio/deep-thinking
[48] 上下文缓存 https://help.aliyun.com/zh/model-studio/context-cache
[49] OpenAI 兼容 https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope
[50] Open Responses https://openresponses.org/specification
[51] MiniMax https://platform.minimax.io/docs/api-reference/text-anthropic-api
[52] 火山方舟 https://docs.volcengine.com/docs/ark/integrate-third-party-tools
[53] xAI https://docs.x.ai/developers/rest-api-reference/inference/legacy
[54] OpenRouter https://openrouter.ai/docs/api_reference/responses/overview
[55] SGLang https://lmsysorg.mintlify.app/docs/basic_usage/anthropic_api
[56] Ollama https://docs.ollama.com/api/openai-compatibility
[57] llama.cpp https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
[58] Bedrock https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html
[59] Azure https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle
