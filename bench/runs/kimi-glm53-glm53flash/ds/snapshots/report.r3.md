# LLM API 请求协议对照：Chat Completions · Responses · Messages · generateContent

> 回答：四大主流协议差在哪；「兼容 OpenAI/Anthropic」的下游厂实际差在哪；迁移与适配的坑。事实取自各厂官方文档（2026-09-23 快照），带 [n] 溯源。

## 0. 一屏看懂

1. 四家族：**A** OpenAI Chat Completions（messages 数组、无状态、delta+`[DONE]`，事实标准）；**B** Responses（typed items/events、可选服务端状态）；**C** Anthropic Messages（content blocks、max_tokens 必填）；**D** Google 自有（RPC 路径、contents/parts）。
2. 「兼容 OpenAI」= 兼容 Chat Completions 的**子集**，不是全量、更不是 Responses；Responses 谱系下游刚起步（xAI 设 primary [40][41]、DeepSeek stateless [23]、vLLM/Ollama 子集 [49][50]）。
3. system 位置是第一道分水岭：OpenAI 在 messages 内 role [2]；Anthropic 顶层 `system`（无 system role）[6]；Google 顶层 `systemInstruction` [14]；Responses 另有顶层 `instructions`（previous_response_id 不继承）[3]。
4. 工具调用三套词汇：`tools[].function.parameters`+`tool_calls`+`role:"tool"`；`input_schema`+`tool_use`/`tool_result` 块（结果在 user 侧）；`functionDeclarations`+`functionCall`/`functionResponse` [2][6][14]。
5. 命名与状态：token 上限四种名字——`max_completion_tokens`（chat，旧名弃用）/`max_output_tokens`（Responses）/`max_tokens`（Anthropic 必填）/`maxOutputTokens`（Google）[1][6][14]；服务端状态目前仅 Responses（`store` 默认 true）[1]，Interactions 已跟进；缓存触发四家不同 [4][8][15]。
6. 【点名疑点①】DeepSeek ≠ OpenAI 即插即用：请求形状兼容，但参数语义/默认值/枚举/流式实质有差（§3.2）；「64K/无 FC」旧差异已过时 [22][27]。
7. 【点名疑点②】智谱 /api/anthropic 承诺「SDK 三处改动即用」；已知实质差异：thinking 同名不同义（无 budget_tokens、力度走 reasoning_effort，GLM-5.3 关思考报错）、缓存全自动、工具/流式逐项零文档 [29][30][31]。
8. 2026 下半年协议面在换血：Anthropic 弃用 `temperature/top_p/top_k`（新模型 400）、转 `thinking:{type:"adaptive"}` [6][9]；Google Interactions GA 并将 generateContent 转 legacy，改 `response_format`、引入服务端状态 [18][19]。

## 1. Taxonomy

分类轴：**请求形状谱系 + 状态放哪端**。厂商普遍「一厂多协议面」，故按协议面而非厂商归类。

| 家族 | 协议面 | 一句特征 |
|---|---|---|
| A. Chat Completions | openai-chat（参照）、deepseek-chat、google-openai、qwen、moonshot、mistral、groq/together/fireworks、vllm、ollama、openrouter | messages 数组、无状态、`choices[].delta`、`[DONE]` |
| B. Responses | openai-responses（参照）、xai-responses（primary）、deepseek/zhipu/kimi 的 responses 面、vllm/ollama 子集 | typed items、typed events、可选服务端状态 |
| C. Anthropic Messages | anthropic-messages（参照）、zhipu/deepseek/qwen/kimi 的 anthropic 面 | content blocks、`max_tokens` 必填、命名 SSE 事件 |
| D. Google 自有 | google-gc（legacy）、google-interactions（GA 推荐） | RPC 路径、camelCase；Interactions 向 B 收敛 |

维度：D1 端点｜D2 消息与角色｜D3 工具调用｜D4 状态与缓存｜D5 流式｜D6 认证｜D7 采样｜D8 结构化输出｜D9 推理｜D10 多模态｜D11 版本。

## 2. 对照矩阵

### 2.1 端点 · 认证 · 版本（D1/D6/D11）

| | OpenAI Chat | OpenAI Responses | Anthropic Messages | Gemini generateContent |
|---|---|---|---|---|
| 端点 | `POST /v1/chat/completions` [2] | `POST /v1/responses`（+/{id}、/input_items 等）[1] | `POST /v1/messages` [6] | `POST /v1beta/models/{model}:generateContent`；流式 `:streamGenerateContent?alt=sse` [14] |
| 认证 | `Authorization: Bearer` [2] | 同左 [1] | `x-api-key` + **必填** `anthropic-version: 2023-06-01` [11][12] | `x-goog-api-key`（或 `?key=`）[14][21] |
| 版本 | URL 无版本段；参数级弃用看 spec | 同左；changelog 月更（Responses 2025-03-11 发布）[5] | `anthropic-version` + `anthropic-beta` 头（`feature-name-YYYY-MM-DD`）[12] | `v1beta` 路径；generateContent 已标 legacy [18] |

### 2.2 消息与角色（D2）

| | Chat | Responses | Anthropic | Gemini |
|---|---|---|---|---|
| role 枚举 | developer/system/user/assistant/tool（o1+ 用 developer）[2] | user/assistant/system/developer [1] | 仅 user/assistant；相邻同 role 自动合并 [6] | 仅 user/model（无 assistant）[14] |
| system | messages 内 role | 顶层 `instructions` 或 input 内 system [1][3] | 顶层 `system` [6] | 顶层 `systemInstruction`（仅文本）[14] |
| content 形状 | string 或块数组 | string（=user 文本）或 item 数组 [1] | string 或块数组 [6] | **无字符串简写**；Part.data 互斥 [14] |
| 输入块类型 | text/image_url/input_audio/file（仅 PDF）[2] | input_text/input_image/input_file/input_audio [1] | text/image/document/search_result/thinking/tool_use/tool_result 等 [6] | text/inlineData/fileData/functionCall/functionResponse [14] |

### 2.3 工具调用（D3）

| | Chat | Responses | Anthropic | Gemini |
|---|---|---|---|---|
| 定义 | `tools[].function{name,description,parameters,strict}` [2] | 扁平 `{type:"function",name,parameters,strict}`（无 function 包裹）；strict 省略即试、不兼容回退；另有 web_search 等内置工具 [1][3] | `tools[]{name,description,input_schema}`（JSON Schema 2020-12）[6] | `functionDeclarations{name,description,parameters(OpenAPI)\|parametersJsonSchema}` [14] |
| 模型发起 | assistant `tool_calls[]{id,function{name,arguments}}` [2] | `function_call` item `{call_id,name,arguments}` [3] | `tool_use` 块 `{id,name,input}` [6] | `functionCall{id?,name,args}` [14] |
| 结果回传 | `role:"tool"` + `tool_call_id` [2] | `function_call_output` `{call_id,output}` [3] | **user 消息内** `tool_result{tool_use_id,content,is_error}` [6] | **user role** `functionResponse{id?,name,response}` [14] |
| tool_choice | none/auto/required/{type:"function"} [2] | 同类枚举+每工具开关 [1] | auto/any/tool/none；`disable_parallel_tool_use` 在 tool_choice 内 [6] | `toolConfig.functionCallingConfig`（mode ANY…）[14] |
| 流式聚合 | `delta.tool_calls[].index` 分片 [2] | `function_call_arguments.delta/.done` [3] | `input_json_delta.partial_json`，块结束后再 parse [7] | functionCall part 整体出现 [14] |

### 2.4 状态与缓存（D4）

| | Chat | Responses | Anthropic | Gemini |
|---|---|---|---|---|
| 状态 | 无状态，每次全量 messages [3] | `previous_response_id`／items 放回 input／Conversations 三选；`store` 默认 true；ZDR 强制 false [1][3] | 无状态 [6] | 无状态 [14] |
| 缓存 | implicit 默认开（前缀 ≥1,024 tokens）；`prompt_cache_key` 可选 [1][4] | 同左 [1] | 手动 `cache_control`（ttl 5m/1h），显式断点 ≤4 槽；usage 分 cache_creation/read_input_tokens [6][8] | implicit 默认开（3.x Flash 最小 4096）+ 显式 `cachedContents` [15] |

### 2.5 流式协议（D5）

| | Chat | Responses | Anthropic | Gemini |
|---|---|---|---|---|
| 载体与增量 | `chat.completion.chunk`，增量 `choices[].delta`（content/tool_calls/role）[2] | typed events（60+ 种，带 sequence_number）：response.created → output_item.added → output_text.delta → … → response.completed [1][3] | 命名事件 message_start → content_block_delta（text_delta/input_json_delta/thinking_delta/signature_delta）→ … → message_stop [7] | 每个 chunk 是完整 GenerateContentResponse（candidates）[14] |
| 终止 | `data: [DONE]`；`include_usage` 时独立 usage chunk 在其前 [1] | `response.completed`（无 [DONE]）[3] | `message_stop`；**200 后仍可能 error 事件** [7][13] | 流自然结束 ⚠ |
| 结束原因 | stop/length/tool_calls/content_filter [1] | response.status/incomplete [1] | stop_reason：end_turn/max_tokens/stop_sequence/tool_use/pause_turn/refusal 等 7 值 [6] | finishReason（含 SAFETY 等）[14] |

### 2.6 采样 · 结构化输出 · 推理 · 多模态（D7–D10）

| | Chat | Responses | Anthropic | Gemini |
|---|---|---|---|---|
| max tokens | `max_completion_tokens`（旧 `max_tokens` 弃用、不兼容 o 系）[1] | `max_output_tokens`（min 16，含 reasoning）[1] | `max_tokens` **必填**，上限随模型 [6] | `generationConfig.maxOutputTokens` [14] |
| 采样 | temperature 0–2 默认 1；top_p 0–1；penalties ±2；stop ≤4；n 1–128；**seed 已参数级弃用**[1] | 同左（无 n）[1] | temperature 0–1 默认 1；top_p/top_k；**三者已弃用**（Opus 4.6 后模型拒绝）[6] | temperature 0–2；stopSequences ≤5；candidateCount；seed [14] |
| 结构化输出 | `response_format`: text/json_object/json_schema（strict:true 仅 JSON Schema 子集）[1] | `text.format` 同三值 [3] | `output_config.format{type:"json_schema"}` + 工具 `strict:true`（GA）[10] | `responseMimeType`+`responseSchema`（已标弃用，迁移目标是 Interactions `response_format`）[14][20] |
| 推理控制 | `reasoning_effort`（none…max）；GPT-5.4 起 chat+工具仅 effort=none [2][3] | `reasoning{effort,summary,context}`；reasoning item 须放回 input；encrypted_content 默认填充 [1][3] | `thinking{type:"enabled",budget_tokens≥1024}`→thinking 块（须原样按序回传）；4.6+ 弃用（4.7+ 400），转 `adaptive` [6][9] | `thinkingConfig{thinkingBudget,includeThoughts,thinkingLevel(3+)}`；thought part+`thoughtSignature` [14] |
| 多模态输入 | image_url/input_audio/file（仅 PDF）[2] | input_image/input_file/input_audio [1] | image source base64\|url\|file_id + document(PDF) [6] | inlineData/fileData [14] |

### 2.7 Google Interactions API（D 族新面）

- 定位：2026-06 GA、新项目全推荐；generateContent 转 legacy 但仍支持；新特性只上 Interactions [18]。
- `POST /v1beta/interactions`；必带 `x-goog-api-key` [17][21]。顶层 `input`（string｜Content｜Step 数组，**不再 contents**）、`system_instruction`、`generation_config`/`agent_config`、`stream/store/background` [17]。
- **服务端状态**：默认存储、`previous_interaction_id` 续接、`store=false` 关闭（首次引入 Responses 式状态）[17][18]。
- 响应为 `steps` 数组（2026-05 起取代 outputs）；Content 为类型化块、无 role/parts；工具调用是 `function_call` Step `{type,id,name,arguments}` [19]。
- 结构化输出：顶层 `response_format[{type:"text",mime_type:"application/json",schema}]`，取代 responseMimeType+responseSchema [19][20]。思考：`thinking_level`（minimal…high）+`thinking_summaries`，thought Step 带 signature；流式事件改名 interaction.created、step.* [17][19]。

## 3. 变体与适配层

### 3.1 一厂多协议面总表

| 厂商 | A: chat completions | B: responses | C: anthropic | 其他 |
|---|---|---|---|---|
| OpenAI | /v1/chat/completions（仍支持）[3] | /v1/responses（推荐）[1] | — | Assistants 已下线（2026-08-26）[5] |
| Google | 兼容端点 …/v1beta/openai/ [16] | — | — | generateContent（legacy）+ Interactions（GA）[18] |
| DeepSeek | /chat/completions [22] | /responses（stateless）[23] | /anthropic [24] | /beta（FIM、strict）[26] |
| 智谱 | /api/paas/v4/ [33]；coding 用 /api/coding/paas/v4 [55] | /api/v1（Responses 面）[55][56] | /api/anthropic [29] | Coding Plan 仅限指定工具 [55] |
| 百炼/Qwen | compatible-mode/v1 [34] | — | /apps/anthropic（仅 /v1/messages）[36] | 原生 DashScope 协议 |
| Moonshot | api.moonshot.cn/v1 [37] | Responses 面（/docs/api/responses）[57] | Messages 面（/docs/api/messages）[58] | — |
| xAI | /v1/chat/completions（**legacy**）[41] | /v1/responses（**primary**）[40] | — | gRPC/WS 面 [40] |
| Mistral | /v1/chat/completions（自有=兼容）[45] | — | — | /v1/conversations(β) [46] |

### 3.2 DeepSeek vs OpenAI Chat Completions（点名疑点①）

请求形状同形（messages/tools/SSE/[DONE] 同名），差异逐项：

| 差异点 | DeepSeek 官方 | OpenAI 官方 |
|---|---|---|
| base_url | `https://api.deepseek.com`（**无 /v1**；/beta 仅 FIM 与 strict）[22][26] | api.openai.com/v1/… |
| 模型名 | deepseek-flash、deepseek-v4-pro（旧 chat/reasoner 已停用）[22][27] | gpt-…/o-… |
| response_format | 仅 text\|json_object（无 json_schema）；/responses 面全支持 [22][23] | 三值全支持 |
| 参数行为 | thinking 模式 temperature 无效不报错；top_p 仅 thinking 生效（0.95–1.0）；penalties 传了不生效 [22][25] | 全参数生效 |
| max_tokens 默认 | 非思考 8K/思考 64K（effort=max 128K）；输出上限 384K、上下文 1M [22][28] | 模型相关 |
| 工具 | thinking 模式 tool_choice required/具名 400；带 tools 时历史 reasoning_content 须回传；strict 须 /beta [22][25][26] | 全枚举 |
| 响应差异 | 新增 `reasoning_content`（与 content 同级，流式 delta 同名）[25]；finish_reason 新增 `insufficient_system_resource`、`aborted` [22] | 无 |
| 流式 usage | include_usage 时 usage **搭在最后内容 chunk**（无独立 chunk）；未开 stream 传 stream_options → 400 [22] | 独立 chunk 在 [DONE] 前 |
| /responses 面 | 存在（Codex 适配）；不支持 previous_response_id/conversation/store 等，**未支持参数静默忽略**；tools 仅 function+apply_patch；并行恒开；流式以 response.completed 结束；两模型均支持 [23][27] | 服务端状态可用 |

另有 /anthropic 面：base_url `https://api.deepseek.com/anthropic`；`x-api-key` 支持、`anthropic-version`/`anthropic-beta` 忽略；模型映射 claude-opus*→v4-pro、haiku/sonnet*→flash；thinking 支持但 budget_tokens 忽略；cache_control/disable_parallel_tool_use 忽略；块不支持 document/search_result/redacted_thinking/mcp_* [24]。

### 3.3 智谱 vs Anthropic（点名疑点②）

| 对比点 | Anthropic 官方 | 智谱 /api/anthropic |
|---|---|---|
| 接入 | api.anthropic.com + `x-api-key` + 必填 `anthropic-version` [6][11] | base_url=`https://open.bigmodel.cn/api/anthropic`（+/v1/messages）；三处改动即用 Anthropic SDK；直连示例仅 x-api-key，version 必填与否无文档 [29] |
| 模型 | claude-* | glm-5.3 等；Claude Code 走**服务端映射**（界面 Claude、实际 GLM；`[1m]` 后缀开 1M 上下文）[32] |
| thinking | `thinking{type:"enabled",budget_tokens≥1024}` [6][9] | **同名不同义**：thinking.type=enabled/disabled，无 budget_tokens；力度走 reasoning_effort（GLM-5.3 仅 max/high/low）；GLM-5.3 传 disabled 报错 [30] |
| 缓存 | 手动 `cache_control` 断点（≤4 槽）；usage 分 cache_creation/read_input_tokens [6][8] | 隐式自动（无需 cache_control）；前缀建议 ≥500 token；命中看 `prompt_tokens_details.cached_tokens` [31] |
| 工具/流式 | tool_use/tool_result；命名事件流 [6][7] | **逐项零文档**，仅 stream:true 示例；差异声明仅一句："某些场景下…仍存在差异，但不影响整体兼容性" [29] |

结论：实质差异集中在 thinking 语义、缓存机制、usage 字段名；工具/流式逐项只能实测。另有 /api/v1 Responses 面，官方明示与 OpenAI 三点差异：`store` 默认 false、流式不发 `data: [DONE]`、无 cancel；另 tool_choice 仅 none/auto、text.format 仅 text\|json_object、max_output_tokens 默认 65536 [56]。

### 3.4 其他下游厂（OpenAI 形状偏差）

| 厂商 | 端点/base_url | 关键偏差 |
|---|---|---|
| 百炼/Qwen | `{WorkspaceId}….maas.aliyuncs.com/compatible-mode/v1`（旧 dashscope 域名仍可用）[34] | tool_choice `required` 暂不支持；parallel_tool_calls **默认 false**（OpenAI true）；tools×stream 已可用（普通参数 stream=true 即流式；复杂参数 array/object 需非标 tool_stream=true，迁移页旧禁令滞后）；top_k/repetition_penalty/enable_thinking 等非标参数走 extra_body；max_tokens 将废弃→max_completion_tokens；seed 默认 1234；json_object 需提示词含 "JSON"；reasoning_effort 映射 low/medium→high、xhigh→max [34][35] |
| Moonshot | `https://api.moonshot.cn/v1` [37] | kimi-k3 恒思考（reasoning_effort low/high/max，无 thinking 参数）；k2.6 用 thinking.type+keep；`reasoning_content` 先于 content 且计入 max_tokens；k2.7-code/k2.6 temperature 不可改；stop 最多 5 个；缓存自动开、显式断点 400 [37][38][39] |
| xAI | `https://api.x.ai/v1`（/responses primary、chat legacy）[40][41] | 非标顶层 `search_parameters`；responses 端 penalties 端点级不支持、reasoning 模型另禁 penalties/stop；流式函数调用**整块单 chunk**、每 chunk 带 usage；finish_reason 含自家 `end_turn`；strict 恒 true；reasoning_effort low…xhigh 且**不可关** [40][41][42][43][44] |
| Mistral | `https://api.mistral.ai/v1/chat/completions` [45] | tool_choice 用 `any`（**无 required**）；tools[].function 同形但 `strict`="Not supported"；种子叫 `random_seed`；json_object 须 prompt 明说 JSON；错误形状同 OpenAI [45][46][47] |

聚合层与服务端：OpenRouter 可在 body 放 `provider{order,require_parameters,…}`，**默认**静默忽略下游不支持的参数 [48]；vLLM/Ollama 提供 OpenAI 子集与无状态 /responses [49][50]；LiteLLM 是翻译层（默认抛错、drop_params 静默丢）[51]；Groq 对 logprobs/logit_bias/messages[].name 等直接 400 [52]；Together 模型 ID 需命名空间 [53]；Fireworks 超上下文 max_tokens 默认静默调小 [54]。

## 4. 用户需要知道的坑（按踩中概率排）

1. **「兼容 OpenAI」≠ 全量兼容**：不支持参数的行为三派——静默忽略（OpenRouter 默认 [48]、DeepSeek /responses [23]）、400（Groq [52]、LiteLLM 默认 [51]）、静默截断（Fireworks [54]）。接新厂先读不支持清单。
2. **max_tokens 命名迁移**：chat→`max_completion_tokens`（旧名弃用）、Responses→`max_output_tokens`、Anthropic `max_tokens` 必填 [1][3][6]。
3. **reasoning 回传义务**：Anthropic thinking 块须原样按序回传 [6]；DeepSeek 带 tools 时历史 `reasoning_content` 须回传 [25]；Responses 无状态多轮须回放 reasoning item [1][3]。最易漏的一类 400。
4. **「同名不同义」参数**：Anthropic thinking{budget_tokens} vs GLM thinking.type+reasoning_effort vs DeepSeek thinking（budget_tokens 忽略）；reasoning_effort 枚举各家不同（DeepSeek none…max、GLM/Kimi 各三档、xAI low…xhigh）[6][24][30][37][40]。
5. **兼容面模型映射**：DeepSeek /anthropic claude-opus*→v4-pro、haiku/sonnet*→flash [24]；智谱 Claude Code 服务端映射 glm-4.7→glm-5.2 [32]，计费按映射后模型。
6. **流式终止与 usage 位置不统一**：[DONE]+可选独立 usage chunk（OpenAI）/ usage 搭最后内容 chunk（DeepSeek [22]）/ 搭 finish_reason chunk（Fireworks [54]）/ 无 [DONE]（Anthropic/Responses）；xAI 函数调用整块下发 [42]。
7. **system 不是到处都是 role**：迁 Anthropic/Google 要提升为顶层参数；Responses 优先 instructions（不继承）[3][6][14]。
8. **结构化输出四套字段 + strict 语义差**：response_format / text.format / output_config.format / responseMimeType+responseSchema；strict：Responses 省略即试、xAI 恒 true、Mistral 不支持 [1][3][47]。
9. **采样参数被弃用/失效**：Anthropic temperature/top_p/top_k 弃用（新模型 400）[6]；DeepSeek thinking 模式 temperature 无效 [25]；Kimi k2.7-code/k2.6 不可改 [39]；xAI、Gemini 2.5 Pro/3 思考不可关 [44][16]。写死 temperature=0 的代码会碎。
10. **默认值与边角差异**：tool_choice——Mistral 用 any 无 required [46]、Qwen 不支持 required 且 parallel_tool_calls 默认 false [35]；DeepSeek-responses 并行恒开 [23]；百炼非标参数需 extra_body [35]；Together 模型 ID 需命名空间 [53]；Fireworks 超上下文默认静默截断 [54]。

## 5. 未决与置信度

- 智谱 anthropic 端点 tools/SSE/缓存逐项行为：官方零文档（∅，只能实测）。
- 百炼 json_schema 范围两页不一；Google generateContent 下线表未给、Interactions GA 与 Beta 横幅并存；若干 ⚠ 项（Anthropic logprobs/n、Google SSE 终止原句、Kimi 面 base_url）。
- 时效：2026-09-23 快照；三家协议面都在快速演进（§0.9），兼容层要盯 changelog。

## 来源
[1] OpenAI spec — https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml
[2] OpenAI Chat ref — https://platform.openai.com/docs/api-reference/chat/create
[3] Responses vs Chat — https://platform.openai.com/docs/guides/responses-vs-chat-completions
[4] OpenAI caching — https://platform.openai.com/docs/guides/prompt-caching
[5] OpenAI changelog — https://developers.openai.com/api/docs/changelog
[6] Anthropic Messages — https://docs.claude.com/en/api/messages
[7] Anthropic stream — https://docs.claude.com/en/docs/build-with-claude/streaming
[8] Anthropic caching — https://docs.claude.com/en/docs/build-with-claude/prompt-caching
[9] Anthropic Thinking — https://docs.claude.com/en/docs/build-with-claude/extended-thinking
[10] Anthropic structured — https://docs.claude.com/en/docs/build-with-claude/structured-outputs
[11] Anthropic version — https://docs.claude.com/en/api/versioning
[12] Anthropic beta — https://docs.claude.com/en/api/beta-headers
[13] Anthropic Errors — https://docs.anthropic.com/en/api/errors
[14] Gemini generateContent — https://ai.google.dev/api/generate-content
[15] Gemini cache — https://ai.google.dev/gemini-api/docs/caching
[16] Gemini OpenAI — https://ai.google.dev/gemini-api/docs/openai
[17] Interactions ref — https://ai.google.dev/api/interactions-api
[18] Interactions overview — https://ai.google.dev/gemini-api/docs/interactions-overview
[19] Interactions breaking — https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026
[20] Migrate to interact. — https://ai.google.dev/gemini-api/docs/migrate-to-interactions
[21] Gemini API key — https://ai.google.dev/gemini-api/docs/api-key
[22] DeepSeek chat — https://api-docs.deepseek.com/api/create-chat-completion
[23] DeepSeek Responses — https://api-docs.deepseek.com/guides/responses_api
[24] DeepSeek Anthropic — https://api-docs.deepseek.com/guides/anthropic_api/
[25] DeepSeek thinking — https://api-docs.deepseek.com/guides/thinking_mode
[26] DeepSeek tools — https://api-docs.deepseek.com/guides/tool_calls
[27] DeepSeek updates — https://api-docs.deepseek.com/updates
[28] DeepSeek pricing — https://api-docs.deepseek.com/quick_start/pricing
[29] 智谱 Claude 兼容 — https://docs.bigmodel.cn/cn/guide/develop/claude/introduction
[30] 智谱 thinking — https://docs.bigmodel.cn/cn/guide/capabilities/thinking.md
[31] 智谱 cache — https://docs.bigmodel.cn/cn/guide/capabilities/cache.md
[32] 智谱 Claude Code — https://docs.bigmodel.cn/cn/guide/develop/claude.md
[33] 智谱 OpenAI — https://docs.bigmodel.cn/cn/guide/develop/openai/introduction.md
[34] 百炼兼容 — https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope
[35] 百炼 Qwen — https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions
[36] 百炼 Claude Code — https://help.aliyun.com/zh/model-studio/claude-code
[37] Kimi guide — https://platform.kimi.com/docs/guide/start-guide
[38] Kimi chat — https://platform.moonshot.cn/docs/api/chat
[39] Kimi thinking — https://platform.kimi.com/docs/guide/use-thinking-models
[40] xAI Responses — https://docs.x.ai/developers/rest-api-reference/inference/responses
[41] xAI Chat — https://docs.x.ai/developers/rest-api-reference/inference/chat-completions
[42] xAI function — https://docs.x.ai/developers/tools/function-calling
[43] xAI structured — https://docs.x.ai/developers/model-capabilities/text/structured-outputs
[44] xAI reasoning — https://docs.x.ai/developers/model-capabilities/text/reasoning
[45] Mistral chat — https://docs.mistral.ai/api/endpoint/chat
[46] Mistral function — https://docs.mistral.ai/capabilities/function_calling
[47] Mistral structured — https://docs.mistral.ai/capabilities/structured_output
[48] OpenRouter — https://openrouter.ai/docs/features/provider-routing
[49] vLLM — https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/
[50] Ollama compat — https://raw.githubusercontent.com/ollama/ollama/main/docs/api/openai-compatibility.mdx
[51] LiteLLM drop — https://docs.litellm.ai/docs/completion/drop_params
[52] Groq compat — https://console.groq.com/docs/openai
[53] Together compat — https://docs.together.ai/docs/openai-api-compatibility
[54] Fireworks compat — https://docs.fireworks.ai/tools-sdks/openai-compatibility
[55] 智谱 Coding quick-start — https://docs.bigmodel.cn/cn/coding-plan/quick-start
[56] 智谱 Responses — https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md
[57] Kimi Responses — https://platform.kimi.com/docs/api/responses
[58] Kimi Messages — https://platform.kimi.com/docs/api/messages
