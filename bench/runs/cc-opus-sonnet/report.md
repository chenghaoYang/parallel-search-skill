# LLM API 请求协议对照：Chat Completions / Responses / Messages / generateContent 与下游兼容实现

> 回答：四个参照协议差在哪；下游厂商「兼容 X」时实际偏差；换协议会踩的坑。截至 2026-09-23，只依据官方文档，字段名保留原文。§0 结论，§2 查字段，§3 查厂商。❓＝未查到，∅＝官方没写。

## 0. 一屏看懂

1. **形状**：Chat Completions＝`messages`→`choices[].message`；Responses＝`input` item 数组→`output` item 数组，推理、工具调用、工具结果都是独立 item；Messages＝`content` block 数组，只有 user/assistant，`system` 在顶层；generateContent＝`contents[].parts[]`，角色 `user`/`model` [1][10][20]。
2. **定位**：OpenAI「Chat Completions 仍受支持，新项目推荐 Responses」，Assistants API 已于 2026-08-26 下线 [2]；Google 称 generateContent 为 legacy（仍完全支持），推荐新项目用 2026-06 GA 的 Interactions API（服务端状态）[23]；Responses 家族已有厂商中立规范 Open Responses（2026-01-15）[9][26]。
3. **「兼容 Responses」≠ 有服务端状态**：OpenAI 缺省 `store:true`、可用 `previous_response_id`；DeepSeek、Kimi、MiniMax、OpenRouter、Ollama 的 Responses 都不支持 `previous_response_id`，历史要自己回传；智谱默认 `store=false`；Qwen、方舟默认存储，上文分别留 7 天、默认 3 天（§3.2）。
4. **推理内容是跨协议最大的坑**：OpenAI Chat 不返回推理文本；Responses 给 `reasoning` item；Anthropic 的 `thinking` 带 `signature`，须原样按序回传，否则 400；Gemini 缺签名返回 `MISSING_THOUGHT_SIGNATURE`；国内厂商多用非标准 `reasoning_content`，MiniMax 默认把思考用 `<think>` 标签混进 `content`（§3）[5][10][20][57]。
5. **Q1 DeepSeek**：不是另一种协议，是三个兼容入口各带方言。Chat 入口：`reasoning_content`、`prompt_cache_hit/miss_tokens`、`response_format` 无 `json_schema`，strict、前缀续写、FIM 走 `/beta`。Responses 入口（2026-08-13，官方称专为 Codex 适配）：无状态，`store` 恒 false，`previous_response_id`/`conversation` 不支持；推理给明文 `reasoning_text`，没有 `summary`/`encrypted_content`；托管工具全部忽略，custom 工具只认 `apply_patch`；不支持的参数静默忽略。Anthropic 入口见 §3.3 [27][29][30][31][32]。
6. **Q2 智谱**：Anthropic 兼容端点 `https://open.bigmodel.cn/api/anthropic` 没有字段级文档：`count_tokens`、`anthropic-beta`、`cache_control`、`stop_sequences`、`top_k`、`metadata`、`stop_reason` 均 ∅，官方只写「某些场景下…仍存在差异」。能证实的只有：搜索、看图走服务端内置 MCP／`image_analysis`；effort 折成 high/max 两档；模型靠客户端 `ANTHROPIC_DEFAULT_*_MODEL` 指定（§3.3）[37][38][40][41]。
7. **兼容层以静默忽略为主**：Anthropic/Gemini 的 OpenAI 兼容层、DeepSeek Responses、MiniMax 都直接忽略不支持的字段；少数报 400，如 DeepSeek 思考模式的 `tool_choice:"required"`、Kimi 的 `prompt_cache_breakpoint` [19][25][27][29][47]。
8. **参数合法性越来越看模型**：Opus 4.6 之后发布的 Claude 模型，`temperature` 只接受 1.0、`top_p` 只接受 ≥0.99、`top_k` 任何值都 400；4.6+ 禁预填，4.7+ 禁 `thinking.type:"enabled"`；Kimi 旗舰模型的采样参数固定 [10][15][18][46]。

## 1. Taxonomy

分类轴：**A1 形状谱系**（决定字段名与嵌套）；**A2 状态在哪端**（决定客户端要回传什么）；**A3 实体角色**（参照协议／参照厂商自家兼容层／第三方模型厂／网关与自托管／开放规范）。第三方兼容端点多按 Codex、Claude Code 的需要裁剪（DeepSeek、Kimi 的 custom 工具只收 `apply_patch`；方舟为 Coding Plan 单设网关）[29][47][61]。

| 家族 | 参照 | 为什么是一类 | 状态 | 兼容实现 |
|---|---|---|---|---|
| Chat | OpenAI `/v1/chat/completions` | message 列表，工具调用挂在 assistant message 上 | 无状态（推断） | DeepSeek、智谱、Kimi、Qwen、MiniMax、方舟、vLLM、Anthropic/Gemini 自家兼容层 |
| Items | OpenAI `/v1/responses` | 输入输出都是带 `type` 的 item | 可选服务端状态 | Open Responses 规范；DeepSeek、智谱、Kimi、Qwen、MiniMax、方舟、vLLM、llama.cpp、OpenRouter、Ollama |
| Blocks | Anthropic `/v1/messages` | 内容是 typed block（`tool_use`/`tool_result`/`thinking`） | 无状态 | DeepSeek、智谱、Kimi、Qwen、MiniMax、方舟、llama.cpp、Bedrock |
| Parts | Gemini `:generateContent` | `contents/parts`，参数集中在 `generationConfig` | 无状态（推断）＋缓存资源 | Vertex AI |
| Steps | Gemini `/v1beta/interactions` | Content 没有 role，角色由 `Step.type` 表达 | 服务端状态 | — |

维度：D1 端点鉴权｜D2 输入结构｜D3 历史谁保存｜D4 输出容器｜D5 工具｜D6 推理控制与回传｜D7 JSON 约束｜D8 流式｜D9 生成参数｜D10 停止/用量/缓存｜D11 厂商暴露哪些入口｜D12 不支持字段是忽略还是报错。

## 2. 对照矩阵（参照协议）

表头 [n] 覆盖整列，格内 [n] 为其他页。

**D1–D4**

| | Chat [1] | Responses [1][2] | Messages [10][11] | generateContent [20] |
|---|---|---|---|---|
| 端点 | `POST https://api.openai.com/v1/chat/completions` | `POST /v1/responses`；GET/DELETE/cancel/input_items、`/conversations` | `POST https://api.anthropic.com/v1/messages`；`count_tokens`、`batches` | `POST …/v1beta/models/{model}:generateContent`；v1 稳定、v1beta 新特性 |
| 鉴权 | `Authorization: Bearer`；可选 `OpenAI-Organization`/`OpenAI-Project` [7] | 同左 [7] | `anthropic-version: 2023-06-01` 必填 [12]；`Authorization: Bearer`，`x-api-key` 是 legacy fallback | `x-goog-api-key` 或 `?key=` [21]；Vertex 用 OAuth |
| 角色 | developer/system/user/assistant/tool（function 弃用） | user/system/developer/assistant；另有 `instructions` | 仅 user/assistant，连续同角色合并；`system` 顶层 | `user`/`model`＋`systemInstruction` |
| 状态 | `store` 只为蒸馏/评测，默认 false | `store` 缺省 true，至少 30 天；`previous_response_id` 与 `conversation` 互斥、不继承 `instructions`；Conversation 无 30 天 TTL [3] | 官方称 stateless | 无；可引用 `cachedContents` |
| 输出 | `choices[].message{content,refusal,tool_calls,annotations,audio}`；`n` 1–128 | `output[]`；`status` completed/failed/in_progress/cancelled/queued/incomplete；无 `n` | `content[]`；拒答＝`stop_reason:"refusal"`；无 `n` | `candidates[].content.parts`；`candidateCount`；`promptFeedback.blockReason` |

**D5 工具**

| | Chat | Responses | Messages | generateContent |
|---|---|---|---|---|
| 声明 | `{type:"function",function:{name,description,parameters,strict}}` | `{type:"function",name,description,parameters,strict}`，省略 strict 时尽量严格 | `{name,description,input_schema,strict}` | `functionDeclarations[{name,description,parameters｜parametersJsonSchema}]` |
| 选择 | `tool_choice` none/auto/required/指定；`parallel_tool_calls` 默认 true | 同左 | `tool_choice` auto/any/tool/none；`disable_parallel_tool_use` | `functionCallingConfig.mode` AUTO/ANY/NONE/VALIDATED |
| 调用 | `tool_calls[{id,function{name,arguments}}]`，arguments 是 JSON 字符串 | `function_call{call_id,name,arguments}` | `tool_use{id,name,input}`，input 是对象 | `functionCall{id?,name,args}`，args 是对象 |
| 回传 | `role:"tool"`＋`tool_call_id` [8] | `function_call_output{call_id,output}` | user 消息里的 `tool_result{tool_use_id,content,is_error}`，须排在最前 [14] | `functionResponse{id?,name,response}` |
| 托管工具 | `web_search_options` | 16 类，如 web_search、file_search、mcp | 带日期版本名，如 `web_search_20260209` | googleSearch、codeExecution 等 |

**D6 推理 · D7 JSON · D9 参数**

| | Chat | Responses | Messages | generateContent |
|---|---|---|---|---|
| 推理控制 | `reasoning_effort` none/minimal/low/medium/high/xhigh/max | `reasoning{effort,summary}` | `thinking{type:"enabled",budget_tokens≥1024}` 或 `{type:"adaptive"}`＋`output_config.effort` | `thinkingConfig{thinkingBudget｜thinkingLevel,includeThoughts}` |
| 推理返回 | 不返回文本，只计 `reasoning_tokens` [5] | `reasoning` item：summary＋`encrypted_content`（无状态模式默认返回）[5] | `thinking`（默认 summarized）＋`signature`；`redacted_thinking` | `thought` part；`thoughtSignature` 可挂在任意 part |
| 回传 | — | 用 `previous_response_id` 或回传 reasoning item | 原样原序回传，改动即 400 | 缺签名 → `MISSING_THOUGHT_SIGNATURE` |
| JSON | `response_format{type:"json_schema",…,strict}`；`json_object` 需提示词要求 | `text.format`；`text.verbosity` | `output_config.format`（GA）；工具 `strict` [17] | `responseMimeType`＋`responseJsonSchema`（`responseSchema` 弃用） |
| max tokens | `max_completion_tokens`（`max_tokens` 弃用） | `max_output_tokens` | `max_tokens` 必填 | `maxOutputTokens`（可选） |
| 采样 | temperature 0–2、top_p、stop≤4、seed（弃用）、n、penalties、logit_bias；无 top_k | temperature 0–2、top_p；无 stop/n/seed | temperature 0–1、top_p、top_k、`stop_sequences`；新模型限制见 §0-8 | temperature 0–2、topP、topK、seed、`stopSequences`≤5 |

**D8 流式 · D10 停止/用量/缓存**

| | Chat | Responses | Messages | generateContent |
|---|---|---|---|---|
| 流式 | `chat.completion.chunk` 的 `choices[].delta`，以 `data: [DONE]` 结束；`stream_options.include_usage` 多发一个 usage chunk | 带 `event:` 的语义事件：`response.created`→`response.output_text.delta`→`response.completed`；无 `[DONE]` [4] | `message_start`→`content_block_start/delta/stop`→`message_delta`（usage 累计）→`message_stop`；2023-06-01 起无 `[DONE]` [12][13] | `:streamGenerateContent?alt=sse`，每块都是完整 `GenerateContentResponse` |
| 停止 | `finish_reason` stop/length/tool_calls/content_filter | `incomplete_details.reason` max_output_tokens/max_messages/content_filter/steered | `stop_reason` end_turn/max_tokens/stop_sequence/tool_use/pause_turn/refusal/model_context_window_exceeded | `finishReason` 20 项，含 SAFETY、RECITATION、MALFORMED_FUNCTION_CALL |
| 用量 | `prompt_tokens`/`completion_tokens`；`prompt_tokens_details.cached_tokens`；`completion_tokens_details.reasoning_tokens` | `input_tokens`/`output_tokens`＋同构 details | `input_tokens` 不含缓存；`cache_creation_input_tokens`＋`cache_read_input_tokens`＋`input_tokens`＝总输入 [16] | `promptTokenCount`/`candidatesTokenCount`/`thoughtsTokenCount`/`cachedContentTokenCount` |
| 缓存 | 自动前缀缓存（GPT-5.6+ ≥1,024 tokens）；`prompt_cache_key`；`prompt_cache_options.ttl` [6] | 同左 | 显式 `cache_control{type:"ephemeral",ttl:"5m"/"1h"}`，≤4 断点，最小 512–4096；「自动缓存」也要在顶层加一个 `cache_control` [16] | 隐式缓存（2.5+ 默认，最小 2048/4096）＋显式 `cachedContents` [22] |

**Gemini 的两个入口**

| | generateContent | Interactions [24] |
|---|---|---|
| 输入 | `contents[]{role,parts}` | `input`（字符串/Content/Step 数组）＋`system_instruction`；角色靠 `Step.type` |
| 输出与工具 | `candidates[]`；嵌套 `functionDeclarations`，`functionCall.args` | `steps[]`，`status` 含 `requires_action`；扁平函数声明，`function_call{id,name,arguments}`／`function_result{call_id}` |
| 推理/JSON/参数 | `thinkingConfig`；`responseJsonSchema`；`generationConfig` | `thinking_level`，ThoughtStep 带 `signature`；`response_format`；`generation_config`（参考页未列 temperature） |
| 流式/状态 | 完整响应块；无状态 | `step.*`/`interaction.*` 事件，以 `interaction.completed` 结束；`store` 默认 true，`previous_interaction_id`，`background` [23] |

## 3. 变体与适配层

**3.1 入口（D11）**

| 厂商 | Chat | Responses | Anthropic | 备注 |
|---|---|---|---|---|
| DeepSeek | `https://api.deepseek.com`（`/beta` 开 strict/前缀续写/FIM） | 同 base_url，`POST /responses` | `…/anthropic` | `deepseek-v4-pro`/`deepseek-flash`；`deepseek-chat/reasoner` 2026-07-24 停用 [27][30][31][32] |
| 智谱 | `open.bigmodel.cn/api/paas/v4`（z.ai 同构） | `…/api/v1` | `…/api/anthropic` | [36][37][39] |
| Kimi | `api.moonshot.cn/v1` | `/v1/responses`（仅 kimi-k3） | `…/anthropic` | [43][47] |
| Qwen/百炼 | `dashscope.aliyuncs.com/compatible-mode/v1`（多地域） | `…/compatible-mode/v1/responses` | `…/apps/anthropic`，无 `/v1/models` | 另有 DashScope 原生协议 [48][49][50][55] |
| MiniMax | `api.minimax.io/v1`（国内 `api.minimax.cn`） | `/v1/responses` | `…/anthropic`，官方标「推荐」 | [56][57] |
| 方舟 | `ark.cn-beijing.volces.com/api/v3` | `/api/v3/responses` | `/api/compatible` | Coding Plan 用 `/api/coding/v3`、`/api/coding`，误用 `/api/v3` 另计费 [60][61] |

**3.2 Items 家族：Responses 兼容**

| 实现 | 状态 | 推理表示 | 工具 | 不支持字段 |
|---|---|---|---|---|
| Open Responses 规范 | `previous_response_id` 必须加载上文，取不到报 `previous_response_not_found` | `content`/`encrypted_content`/`summary` 均可选 | 分外部托管与厂商内部托管 | 扩展 item/事件须带厂商前缀（`acme:…`），客户端须能安全忽略 [26] |
| DeepSeek | 无状态（§0-5）；`instructions` 变成首条 system | 明文 `response.reasoning_text.delta`；回传的 reasoning 并入相邻 assistant | function；custom 仅 `apply_patch`；web_search 等忽略 | 静默忽略；`include`、`background` 不支持；无 `truncation`，超长 400；`text.format` 支持 `json_schema` [29][30] |
| Kimi | `store` 固定 false，`previous_response_id`/`conversation` 固定 null | reasoning item，summary 为 `reasoning_text` | function、custom（仅 `apply_patch`）、namespace、web_search | `prompt_cache_breakpoint` → 400 [47] |
| 智谱 | `store` 默认 false；`previous_response_id` 须 `store=true`，有效 7 天 | reasoning item＋`reasoning_text` 事件；effort 7 档折成不思考/high/max | function、namespace、custom、web_search；`tool_choice` 仅 none/auto | temperature [0,1]；`error.code` 是字符串 [39] |
| 方舟 | `store` 默认 true；`previous_response_id` 默认存 3 天，`expire_at` 最长 7 天 | summary＋`encrypted_content`，不给原始思维链；多轮靠 `previous_response_id` 或回传 `encrypted_content` | function、联网搜索、Image Process、私域知识库、Remote MCP | 字段级清单 ∅ [66][67][68] |
| Qwen | `store` 默认 true；`previous_response_id` 有效 7 天 | reasoning item（summary 必选）；effort 7 档 | 联网搜索、网页抓取、代码解释器等 | 不支持 `background` 等，未列全 [50][54] |
| MiniMax | 无 `previous_response_id`/`conversation`，历史靠 `input` 全量传 | reasoning item：summary＋明文 `reasoning_text`，无 `encrypted_content`；M3 的 effort 只是开关 | 仅 function；`tool_choice` 仅 none/auto | temperature (0,1]，与其 Chat/Anthropic 端 [0,2] 不同 [58] |

**3.3 Blocks 家族：Anthropic 兼容**

| 实现 | 鉴权/模型名 | thinking | 忽略或不支持 | 缓存 |
|---|---|---|---|---|
| DeepSeek | 服务端把 `claude-opus*` 映射到 `deepseek-v4-pro`，其余到 flash | 支持，`budget_tokens` 忽略；`output_config` 只认 effort | `anthropic-version`、`anthropic-beta`、`disable_parallel_tool_use`、`mcp_servers`、`top_k` 忽略；`document` 不支持 | `cache_control` 全忽略 [31] |
| 智谱（Q2） | `x-api-key`；客户端 `ANTHROPIC_DEFAULT_*_MODEL` 指定 GLM（如 GLM-4.7、`glm-5.2[1m]`） | effort low/medium/high→high，xhigh/max→max | 字段级 ∅；联网搜索、看图由服务端内置工具提供 | ∅ [37][38][40][41] |
| Kimi | `Authorization: Bearer` | `output_config.effort` low/high/max | `stop_reason` 无 stop_sequence/pause_turn | `cache_control` 只认顶层 [44] |
| Qwen | `x-api-key` 或 `Authorization: Bearer` | 支持 `thinking` | 只列 13 个支持参数；temperature [0,2) | ❓ [49] |
| MiniMax | `Authorization: Bearer`（推荐）或 `x-api-key`；`model` 只收 `MiniMax-*` | M3 默认关、`adaptive` 开；M2.x 关不掉；thinking 块连同 `signature` 原样回传 | `top_k`、`stop_sequences`、`mcp_servers`、`context_management`、`container` 忽略；temperature [0,2]；M2.x 不收图片/视频 | `cache_control{type:"ephemeral"}` [56][59] |
| 方舟 | `x-api-key`；`model` 填方舟 Model ID/Endpoint ID | `thinking.type` disabled/enabled/adaptive | 无状态 | `cache_creation_input_tokens` 恒 0 [62] |

**3.4 Chat 家族：OpenAI 兼容**

| 实现 | 推理字段与回传 | JSON / 工具 | 参数差异 | 缓存与用量 |
|---|---|---|---|---|
| DeepSeek | `reasoning_content`；思考默认开，effort 只有 none/low/high/max；带 tools 的轮次必须回传，否则 400 | 仅 `json_object`；strict 要 `/beta`；思考模式下 `required`/指定函数 → 400 | 仍用 `max_tokens`；penalties 弃用且无效；思考模式 temperature 无效；`finish_reason` 多 `insufficient_system_resource`、`aborted` | `prompt_cache_hit/miss_tokens`（`cached_tokens`＝hit）；流式 usage 在最后内容块 [27][28][33] |
| 智谱 v4 | `reasoning_content`；`thinking.type`；`clear_thinking:false` 时须原样回传 | 仅 `json_object`；`tool_choice` 仅 auto；`tool_stream` | temperature [0,1]；`finish_reason` 多 `sensitive`、`network_error` | `cached_tokens` [36] |
| Kimi | `reasoning_content` 先于 content；须回传完整 assistant message | `json_schema`；部分模型不支持 `required` | 旗舰模型 temperature/top_p/n/penalty 固定，传别的值报错；`max_tokens` 弃用 | `cached_tokens`、`cache_write_tokens` [42][45][46] |
| Qwen | `enable_thinking`、`thinking_budget`；部分开源版思考只支持流式 | `json_schema`；非标准 `enable_search` | 只有 `messages[0]` 可为 system | 隐式不可关＋显式 `cache_control`（5 分钟，≥1024）[51][52][53] |
| MiniMax | 思考默认以 `<think>` 混在 content，`reasoning_split:true` 才拆到 `reasoning_content`/`reasoning_details`；都须完整保留回传 | 不支持弃用的 `function_call` | penalties、`logit_bias` 忽略；temperature [0,2] | ❓ [57] |
| 方舟 | `reasoning_content`（摘要）＋`encrypted_content`；回传时后者优先，缺失会降低效果 | `json_schema`（beta，`strict` 默认 false） | `thinking.type` enabled/disabled/auto；effort 7 档 | 隐式缓存不可关；显式前缀/Session 缓存 [63][64][65] |
| Anthropic 兼容层 | `extra_body.thinking`；`reasoning_effort` 忽略 | `response_format`、`strict` 忽略 | `n` 须为 1；temperature>1 截断；system/developer 合并置顶；官方称非生产方案 | 不支持 prompt caching [19] |
| Gemini 兼容层（beta） | `reasoning_effort` 映射 thinking_level/budget；`extra_body.google.thinking_config` | `response_format` 可用 | 未列出的参数静默忽略 | `extra_body.google.cached_content` [25] |

DeepSeek 另有前缀续写（`prefix:true`）与 FIM（`POST /completions`），均走 `/beta` [34][35]。其他：vLLM 有 Chat、Responses [71]；llama.cpp 的 README 称支持 `/v1/messages`、`/v1/responses` [72]；OpenRouter（传 `store:true` 或 `previous_response_id` 即 400）与 Ollama 的 Responses 都无状态 [69][70]；xAI 已弃用 Anthropic SDK 兼容 [73]；Bedrock 的 `bedrock-mantle` 端点实现 Anthropic Messages [74]。

## 4. 用户需要知道的坑（按踩中概率）

1. **推理回传** → 400 或多轮质量下降 → 回传上一轮 assistant 原始对象（含 `reasoning_content`、thinking 块、`<think>`、签名），别只存 content（§3）。
2. **以为兼容 Responses 就有服务端记忆** → 上下文丢失或 400 → 看 §3.2「状态」列。
3. **用量口径** → 成本估算偏差 → Anthropic 的 `input_tokens` 不含缓存；Kimi 的 Anthropic 端口径与其 Chat 不同；DeepSeek Chat 另报 hit/miss；方舟 Anthropic 端 `cache_creation_input_tokens` 恒 0 [16][27][44][62]。
4. **静默忽略** → 以为 `strict`、`response_format`、`top_k` 生效，其实没有 → 响应侧自己校验（§0-7）。
5. **参数名、范围、合法值不一** → 400 或行为漂移 → 按 §2 D9、§3 逐家映射；Anthropic 新模型与 Kimi 旗舰只收固定值（§0-8）[15][18]。
6. **流式收尾** → 挂起或提前结束 → 只有 Chat 家族以 `data: [DONE]` 收尾，其余看结束事件（§2 D8）。
7. **计费入口** → 走错 base URL 被另收费 → 方舟 Coding Plan 必须用 `/api/coding/*` [61]。
8. **模型名映射** → 日志里的 `claude-*` 不是实际模型 → DeepSeek 的 Anthropic 端在服务端映射；智谱、方舟、MiniMax 要客户端自己填模型 [31][38][59][62]。

## 5. 未决与置信度

- ⚔ Gemini：`Content.role` 只许 user/model，同页又写 FunctionResponse 用 `"function"`（proto 同样矛盾）；Interactions 参考页有 `safety_settings`，概览页说不支持。
- ⚔ OpenAI `encrypted_content`：指南限定无状态模式默认返回，openapi.yaml 不限条件，`store:true` 时是否返回未写。
- ⚔ Qwen 的 `tool_choice:"required"` 范围两页不一，显式缓存创建量路径两页不同（按参数页的 `cache_creation` 对象）；MiniMax 三个入口的 temperature 范围不同；Kimi 迁移指南写 temperature [0,1] 可调、模型总览写固定（按后者）；方舟 `thinking.type` 在 Chat 用 `auto`、Anthropic 端用 `adaptive`。
- ❓/∅：智谱 Anthropic 端字段级行为（官方未写）；方舟、Qwen、MiniMax 的 Responses 没有字段级「不支持」清单，流式是否发 `[DONE]` 也未写；Interactions 是否强制回传思考签名。
- 二手：GitHub issue 称智谱 Anthropic 端 token 计数偏高（JSON 多 43–49%，特殊字符多 143–149%），官方未回应。
- 时效：OpenAI 规范 2026-09-22 更新；DeepSeek 5 周内两次协议变更；Kimi `$web_search` 预计 2026-10-20 下线。

## 来源

路径接在该行前缀之后。
- **OpenAI**：[1] https://github.com/openai/openai-openapi/blob/master/openapi.yaml ；前缀 `https://developers.openai.com/api/docs`：[2] `/guides/migrate-to-responses` [3] `/guides/conversation-state` [4] `/guides/streaming-responses` [5] `/guides/reasoning` [6] `/guides/prompt-caching` [7] `/api-reference/authentication` [8] `/guides/function-calling` [9] `/changelog`
- **Anthropic** `https://platform.claude.com/docs/en`：[10] `/api/messages` [11] `/api/overview` [12] `/api/versioning` [13] `/build-with-claude/streaming` [14] `/agents-and-tools/tool-use/handle-tool-calls` [15] `/build-with-claude/extended-thinking` [16] `/build-with-claude/prompt-caching` [17] `/build-with-claude/structured-outputs` [18] `/api/errors` [19] `/api/openai-sdk`
- **Google** `https://ai.google.dev`：[20] `/api/generate-content` [21] `/gemini-api/docs/function-calling` [22] `/gemini-api/docs/caching` [23] `/gemini-api/docs/interactions-overview` [24] `/api/interactions-api` [25] `/gemini-api/docs/openai`
- **Open Responses**：[26] https://openresponses.org/specification
- **DeepSeek** `https://api-docs.deepseek.com`：[27] `/api/create-chat-completion` [28] `/guides/thinking_mode` [29] `/guides/responses_api` [30] `/api/create-response` [31] `/guides/anthropic_api` [32] `/updates` [33] `/guides/tool_calls` [34] `/guides/chat_prefix_completion` [35] `/guides/fim_completion`
- **智谱** `https://docs.bigmodel.cn`：[36] `/api-reference/模型-api/对话补全` [37] `/cn/guide/develop/claude/introduction` [38] `/cn/guide/develop/claude` [39] `/api-reference/response/创建-response.md` [40] `/cn/coding-plan/mcp/search-mcp-server` [41] `/cn/coding-plan/mcp/vision-mcp-server`
- **Kimi** `https://platform.kimi.com/docs`：[42] `/api/chat` [43] `/api/overview` [44] `/api/messages` [45] `/guide/use-thinking-models` [46] `/api/models-overview` [47] `/api/responses`
- **Qwen/百炼** `https://help.aliyun.com/zh/model-studio`：[48] `/base-url` [49] `/anthropic-api-messages` [50] `/compatibility-with-openai-responses-api` [51] `/deep-thinking` [52] `/context-cache` [53] `/compatibility-of-openai-with-dashscope` [54] `/qwen-api-via-openai-responses` [55] `/qwen-api-via-dashscope`
- **MiniMax** `https://platform.minimax.io/docs/api-reference`：[56] `/text-anthropic-api` [57] `/text-openai-api` [58] `/text/api/openapi-responses.json` [59] `/text/api/openapi-chat-anthropic.json`
- **火山方舟** `https://docs.volcengine.com/docs/ark`：[60] `/integrate-third-party-tools` [61] `/coding-plan-personal-get-started` [62] `/messages-api` [63] `/deep-thinking` [64] `/chat-api` [65] `/context-cache` [66] `/responses-api-text-generation` [67] `/responses-api-deep-thinking` [68] `/responses-api-tool-calling`
- **其他**：[69] https://openrouter.ai/docs/api_reference/responses/overview [70] https://docs.ollama.com/api/openai-compatibility [71] https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/ [72] https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md [73] https://docs.x.ai/developers/rest-api-reference/inference/legacy [74] https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html
