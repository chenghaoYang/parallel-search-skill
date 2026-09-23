# LLM API 请求协议对照：Chat Completions · Responses · Messages · generateContent

> 本文回答：四大主流 LLM API 请求协议差在哪；「兼容 OpenAI/Anthropic」的下游厂实际差在哪；迁移与适配的坑。全部事实取自各厂官方文档（抓取于 2026-09-23），每条带 [n] 溯源。读法：§0 五分钟建立认知 → §2 查矩阵 → §3 看兼容差异 → §4 避坑。

## 0. 一屏看懂

1. 请求形状分四家族：**A** OpenAI Chat Completions（messages 数组、无状态、delta chunk + `data: [DONE]`，事实标准）；**B** OpenAI Responses（input items、typed events、可选服务端状态）；**C** Anthropic Messages（content blocks、max_tokens 必填）；**D** Google generateContent（RPC 路径 `:generateContent`、contents/parts）。
2. 「兼容 OpenAI」= 兼容 Chat Completions 的**子集**，不是全量、也不是 Responses。Responses 谱系在下游只有 stateless 子集（vLLM、Ollama）或专门适配（DeepSeek 为 Codex 提供，无服务端状态）[22][29][30]。
3. system 的位置是第一道分水岭：OpenAI 放 messages 里的 `system`/`developer` role [1]；Anthropic 是顶层 `system` 参数（无 system role）[10]；Google 是顶层 `systemInstruction` [18]；Responses 另有顶层 `instructions`，且 `previous_response_id` 不继承它 [3]。
4. 工具调用三套词汇表：OpenAI `tools[].function.parameters` + `tool_calls`/`role:"tool"`+`tool_call_id`；Anthropic `input_schema` + `tool_use`/`tool_result` 块（结果在 user 消息内）；Google `functionDeclarations` + `functionCall`/`functionResponse` parts（回传用 user role）[1][10][18]。
5. token 上限四种名字：`max_completion_tokens`（chat，旧 `max_tokens` 弃用）/ `max_output_tokens`（Responses，含 reasoning）/ `max_tokens`（Anthropic，必填）/ `generationConfig.maxOutputTokens`（Google）[2][10][18]。
6. 只有 Responses 有服务端状态（`previous_response_id`，`store` 默认 true）[2]；缓存四家都有但触发不同：OpenAI 全自动前缀缓存 [4]、Anthropic 手动 `cache_control`（显式断点上限 4 槽）[12]、Google 显式 `cachedContents`+默认 implicit [19]、DeepSeek 磁盘缓存默认开 [27]。
7. 【点名疑点①结论】DeepSeek ≠ OpenAI 即插即用：请求形状兼容，但参数语义、默认值、枚举、流式细节有实质差异（§3.1 逐项表）；网传「64K 上下文 / 不支持 function calling / json_output 受限」等旧差异已全部过时（现为 1M 上下文、V3.2 起 thinking 也能调工具）[21][23][24]。
8. 最大时效风险：Anthropic 已弃用 `temperature/top_p/top_k`（新模型 400）并转向 `thinking:{type:"adaptive"}` [10][13]；Google 推出 Interactions API、参考页把 `responseSchema` 标弃用 [18]——两大官方协议面正在换血，适配层要盯 changelog。

## 1. Taxonomy

分类轴：**请求形状谱系 + 状态放哪端**（请求 body 继承自谁、对话状态在客户端还是服务端）。厂商普遍「一厂多协议面」（DeepSeek 同时提供 chat/responses/anthropic 三张脸；Google 自有+OpenAI 兼容），所以按协议面而非厂商归类。

| 家族 | 协议面 | 一句特征 |
|---|---|---|
| A. Chat Completions 谱系 | openai-chat（参照）、deepseek-chat、google-openai、qwen/moonshot/xai/mistral、groq/together/fireworks、vllm、ollama、openrouter | messages 数组、无状态、`choices[].delta` 流、`[DONE]` 结尾 |
| B. Responses 谱系 | openai-responses（参照）、deepseek-responses、vllm/ollama 的 /responses | typed input/output items、typed events、可选服务端状态 |
| C. Anthropic Messages 谱系 | anthropic-messages（参照）、zhipu-anthropic、deepseek-anthropic | content blocks、`max_tokens` 必填、命名 SSE 事件 |
| D. Google 自有谱系 | google-gc（generateContent）、google-interactions（新） | RPC 风格路径、`contents[].parts[]`、camelCase |

比较维度（§2 各表按此排）：D1 端点与请求形状｜D2 消息与角色｜D3 工具调用｜D4 状态与缓存｜D5 流式协议｜D6 认证｜D7 采样与控制参数｜D8 结构化输出｜D9 推理/思考｜D10 多模态输入｜D11 版本与稳定性。

## 2. 对照矩阵（四主流）

### 2.1 端点 · 认证 · 版本（D1/D6/D11）

| | OpenAI Chat | OpenAI Responses | Anthropic Messages | Gemini generateContent |
|---|---|---|---|---|
| 端点 | `POST /v1/chat/completions` [1] | `POST /v1/responses`（另有 /responses/{id}、/input_items、/input_tokens、/compact）[2] | `POST /v1/messages` [10] | `POST /v1beta/models/{model}:generateContent`；流式 `:streamGenerateContent?alt=sse` [18] |
| 认证 | `Authorization: Bearer` [1] | 同左 [2] | `x-api-key` + **必填** `anthropic-version: 2023-06-01` [15][16] | `?key=`（或 OAuth）[18] |
| 版本机制 | URL 无版本段，看 deprecations 页 | 同左；changelog 月更（2025-03-11 发布 Responses）[9] | `anthropic-version` 头 + `anthropic-beta` 头（`feature-name-YYYY-MM-DD`，可逗号合并）[16] | `v1beta` 路径段；v1 政策未取到 ⚠ |

顶层字段（原样）：chat = messages/model/service_tier/modalities/temperature/top_p/response_format/max_tokens/max_completion_tokens/n/seed/frequency_penalty/presence_penalty/logprobs/store/stop/stream_options/tool_choice/parallel_tool_calls… [2]；Responses = model/input/instructions/max_output_tokens/store/stream/tools/tool_choice/reasoning/text/previous_response_id/conversation/prompt_cache_key/truncation(弃用)/context_management… [2]；Anthropic = model/max_tokens/messages/system/tools/tool_choice/temperature/top_p/top_k/stop_sequences/stream/thinking/metadata [10]；Google = contents/systemInstruction/tools/toolConfig/generationConfig/safetySettings/cachedContent [18]。

### 2.2 消息与角色（D2）

| | Chat | Responses | Anthropic | Gemini |
|---|---|---|---|---|
| role 枚举 | developer/system/user/assistant/tool（o1 起 developer 取代 system）[1] | input item role：user/assistant/system/developer [2] | 仅 user/assistant；相邻同 role 自动合并 [10] | 仅 user/model（无 assistant）[18] |
| system | messages 内 role | 顶层 `instructions` 或 input 内 system [2][3] | 顶层 `system`（无 system role）[10] | 顶层 `systemInstruction`（仅文本）[18] |
| content 形状 | string 或块数组 | string（=user 文本）或 item 数组 [2] | string 或块数组 [10] | **无字符串简写**，Part 的 data 互斥 [18] |
| 输入块类型 | text/image_url/input_audio/file（file 仅 PDF）[1][8] | input_text/input_image/input_file/input_audio [2] | text/image/document/search_result/thinking/redacted_thinking/tool_use/tool_result [10] | text/inlineData/fileData/functionCall/functionResponse（另有 thought、server-side toolCall 等）[18] |

### 2.3 工具调用（D3）

| | Chat | Responses | Anthropic | Gemini |
|---|---|---|---|---|
| 定义 | `tools[].function{name,description,parameters,strict}`，默认非 strict [1][7] | 扁平 `{type:"function",name,parameters,strict}`（无 function 包裹层）；省略 strict 先试 strict、不兼容自动回退 [2][3]；另有内置工具 web_search/file_search/computer/code_interpreter/mcp… [2] | `tools[]{name,description,input_schema}`（JSON Schema 2020-12）[10] | `tools[].functionDeclarations{name,description,parameters(OpenAPI)或 parametersJsonSchema}` [18] |
| 模型发起 | assistant `tool_calls[]{id,type:"function",function{name,arguments}}` [1] | `function_call` item `{call_id,name,arguments}` [3] | assistant 内 `tool_use` 块 `{id,name,input}` [10] | parts 内 `functionCall{id?,name,args}`（现支持可选 id）[18] |
| 结果回传 | `role:"tool"` + `tool_call_id` [1] | `function_call_output` item `{call_id,output}` [3] | **user 消息内** `tool_result` 块 `{tool_use_id,content,is_error}` [10] | **user role** `functionResponse{id?,name,response}`（键名自定）[18] |
| tool_choice | none/auto/required/{type:"function"}（无工具默认 none、有则 auto）[1] | 同类枚举 + 每工具独立开关 [2] | auto/any/tool/none；`disable_parallel_tool_use` 在 tool_choice 内 [10] | `toolConfig.functionCallingConfig`（mode: ANY…）[18] |
| 流式聚合 | `delta.tool_calls[].index` 分片拼接 [1] | `response.function_call_arguments.delta/.done` 事件 [3] | `input_json_delta.partial_json` 分片，`content_block_stop` 后再 parse [11] | functionCall part 整体出现 [18] |

### 2.4 状态与缓存（D4）

| | Chat | Responses | Anthropic | Gemini |
|---|---|---|---|---|
| 状态 | 无状态，每次全量 messages [3] | 三选：`previous_response_id`／把 output items 放回 input／Conversations API；`store` 默认 true（≥30 天）；ZDR 须 store:false [2][3] | 无状态（单查或无状态多轮）[10] | 无状态 [18] |
| 缓存 | implicit prompt caching 默认开、无需字段；前缀下限 1,024 tokens（GPT-5.6+）[4] | 同左 + `prompt_cache_key` [2] | 手动 `cache_control{"type":"ephemeral"}`，ttl 5m/1h；显式断点上限 4 槽；usage 分 `cache_creation_input_tokens`/`cache_read_input_tokens` [12][10] | implicit 默认开（3.x Flash 最小 4096 tokens）+ 显式 `cachedContents`（generateContent 面）[19] |

### 2.5 流式协议（D5）

| | Chat | Responses | Anthropic | Gemini |
|---|---|---|---|---|
| 载体 | `chat.completion.chunk`，增量为 `choices[].delta` [1] | typed events（spec 60+ 种，带 `sequence_number`）：response.created → output_item.added → output_text.delta → response.completed 等 [2][3] | 命名事件 message_start → content_block_start → content_block_delta → content_block_stop → message_delta → message_stop（+ping）[11] | `:streamGenerateContent?alt=sse`，每个 chunk 是完整 GenerateContentResponse（candidates）[18] |
| 增量类型 | content/tool_calls/role | output_text.delta / function_call_arguments.delta / reasoning_summary_text.delta 等 [2] | text_delta / input_json_delta / thinking_delta / signature_delta [11] | parts 内 text/functionCall 增量 [18] |
| 终止 | `data: [DONE]`；`include_usage` 时独立 usage chunk 在其前 [1][2] | `response.completed` 事件（无 [DONE]）[3] | `message_stop` 事件（无 [DONE]）；**200 之后仍可能 error 事件** [11][35] | 流自然结束；终止原句未取到 ⚠ |
| 结束原因 | finish_reason：stop/length/tool_calls/content_filter（function_call 已弃用）[1] | response.status/incomplete（含 reason）[2] | stop_reason：end_turn/max_tokens/stop_sequence/tool_use/pause_turn/refusal/model_context_window_exceeded [10] | finishReason（含 SAFETY 等）[18] |

### 2.6 采样 · 结构化输出 · 推理 · 多模态（D7–D10）

| | Chat | Responses | Anthropic | Gemini |
|---|---|---|---|---|
| max tokens | `max_completion_tokens`（旧 `max_tokens` 弃用、不兼容 o 系；含 reasoning）[2] | `max_output_tokens`（min 16，含 reasoning）[2] | `max_tokens` **必填**，上限随模型；=0 可只预热缓存 [10] | `generationConfig.maxOutputTokens` [18] |
| 采样 | temperature 0–2 默认 1；top_p 0–1；penalties −2..2；stop ≤4；n 1–128；seed（spec 已标 deprecated ⚔）[2] | 同左（无 n）[2] | temperature 0–1 默认 1；top_p/top_k；**三者已弃用**（Opus 4.6 后模型拒绝）[10] | temperature 0–2；stopSequences ≤5；candidateCount；seed [18] |
| 结构化输出 | `response_format`: text/json_object/json_schema（strict:true 仅 JSON Schema 子集）[2][6] | `text.format` 同三值（response_format 的对应物）[3] | `output_config.format{type:"json_schema"}` + 工具 `strict:true`（GA，旧 beta 头过渡；无 response_format）[14] | `responseMimeType:"application/json"` + `responseSchema`（OpenAPI 子集）——两者参考页已标 deprecated ⚔ [18] |
| 推理控制 | `reasoning_effort`（none…max）；GPT-5.4 起 chat 工具调用仅 effort=none [1][3] | `reasoning{effort,summary,context}`；reasoning item 须放回 input；`include:["reasoning.encrypted_content"]` 支持无状态多轮 [2][3] | `thinking{type:"enabled",budget_tokens≥1024}` → thinking 块（**须原样按序回传**，signature 改动 400）；4.6 起手动 enabled 弃用、4.7+ 400，转 `adaptive` [10][13] | `thinkingConfig{thinkingBudget,includeThoughts,thinkingLevel(3+)}`；thought part + `thoughtSignature` 可回传 [18] |
| 多模态输入 | image_url{url,detail}/input_audio{data,format:wav\|mp3}/file 仅 PDF [1][8] | input_image{image_url\|file_id,detail}/input_file{file_id\|file_data\|file_url}/input_audio [2] | image source base64\|url\|file_id（JPEG/PNG/GIF/WebP）+document(PDF)；模型现状仅文本+图片输入 [10][17] | inlineData{mimeType,data}/fileData{mimeType,fileUri}（音频/PDF）[18] |

## 3. 变体与适配层

### 3.1 DeepSeek vs OpenAI Chat Completions（点名疑点①）

请求形状基本同 chat completions（messages/tools/SSE/[DONE] 均同名），差异逐项：

| 差异点 | DeepSeek 官方 | OpenAI 官方 docs |
|---|---|---|
| base_url | `https://api.deepseek.com`（**无 /v1**；`/beta` 仅 FIM/strict）[21] | `https://api.openai.com/v1/…` |
| 模型名 | `deepseek-flash`、`deepseek-v4-pro`；deepseek-chat/reasoner 已于 2026-07-24 停用 [21][24] | gpt-…/o-… 系 |
| response_format | 仅 `text\|json_object`（无 json_schema）；但其 /responses 面 `text.format` 全支持 [21][22] | text/json_object/json_schema |
| temperature | thinking 模式**无效且不报错**；top_p 仅 thinking 生效（0.95–1.0），非 thinking 固定 1.0 [23] | 0–2 生效 |
| penalties | presence/frequency_penalty 弃用、传了不生效 [21] | −2..2 生效 |
| max_tokens 默认 | 非思考 8K / 思考 64K（effort=max 128K）；范围 1–384K；上下文 1M [21][26] | 模型相关，另有 max_completion_tokens |
| 工具 | thinking 模式不支持 `tool_choice` required/具名函数（400）；**带 tools 时历史 `reasoning_content` 必须全量回传否则 400** [21][23] | reasoning 传递走 reasoning item；tool_choice 全枚举 |
| 响应扩展 | `reasoning_content` 与 content 同级（流式 delta 同名）[23] | 无此字段 |
| finish_reason | 新增 `insufficient_system_resource`、`aborted` [21] | stop/length/tool_calls/content_filter |
| 流式 usage | `include_usage` 时 usage **搭在最后内容 chunk**（无独立 usage chunk）；未开 stream 传 stream_options → 400 [21] | 独立 usage chunk 在 [DONE] 前 |
| 并列协议面 | `/responses`（存在，为 Codex 适配，stateless：不支持 previous_response_id/conversation/store）[22]；`/anthropic`（/messages 面，细节 R2 查） | — |

### 3.2 厂商自家的 OpenAI 兼容面

- **Google**：`base_url=https://generativelanguage.googleapis.com/v1beta/openai/` + Bearer；`reasoning_effort` 与各家 thinking 配置有官方映射；Gemini 2.5 Pro/3 系**无法关闭思考** [20]。
- **DeepSeek /responses**：见上表末行；支持模型范围官方页打架（pricing 标两模型均支持 vs 指南只列 deepseek-flash）⚔ [22][26]。

### 3.3 聚合层与服务端兼容层（OpenAI 形状，差异在边角）

| 层 | 关键差异 |
|---|---|
| OpenRouter | 请求体可带非标 `provider{order,allow_fallbacks,require_parameters,…}` 路由对象；**默认**把请求发给不支持某参数的 provider 并静默忽略该参数，`require_parameters:true` 才排除 [28] |
| vLLM | `/v1/chat/completions` + 自家 batch `/v1/chat/completions/batch` + `/v1/responses` [29] |
| Ollama | 只实现 OpenAI API **子集**；/responses 仅无状态版（无 previous_response_id/conversation）[30] |
| LiteLLM | 翻译层：目标模型不支持的参数**默认抛异常**；`drop_params=True` 改静默丢弃（可嵌套 tools[*] 级）[31] |
| Groq | logprobs/logit_bias/top_logprobs/messages[].name 传了即 **400**；n 必须 =1 [32] |
| Together | 模型 ID 带命名空间（gpt-4o 等 OpenAI 串 **404**）；思维链字段 `reasoning` 或 `reasoning_content` 随模型变；cached_tokens 位置随模型（嵌套 details 或顶层），单一形状客户端静默读 0 [33] |
| Fireworks | 超上下文的 max_tokens **默认静默调小**（OpenAI 语义是报错），`context_length_exceeded_behavior:"error"` 才对齐；流式 usage 默认在最后 chunk，无需 stream_options [34] |

## 4. 用户需要知道的坑（按踩中概率排）

1. **「兼容 OpenAI」≠ 全量兼容，且各家对不支持参数的行为三派**：静默忽略（OpenRouter 默认 [28]）／直接 400（Groq [32]、LiteLLM 默认抛错 [31]）／可配置（LiteLLM drop_params、Fireworks 截断行为）。→ 接新厂先读它的「不支持清单」，别拿 OpenAI 全参数集当契约。
2. **max_tokens 命名迁移**：chat 旧名弃用且不兼容 o 系 → `max_completion_tokens`；Responses 是 `max_output_tokens`；Anthropic `max_tokens` 必填。字段名不改必挂 [2][3][10]。
3. **reasoning 的回传义务**：Anthropic thinking 块必须原样按序回传否则 400 [10]；DeepSeek 带 tools 时历史 `reasoning_content` 必须回传否则 400 [23]；Responses 无状态多轮须 include `reasoning.encrypted_content` [2]。换协议时最容易漏的一类 400。
4. **流式终止与 usage 位置不统一**：OpenAI 系 `[DONE]` + 可选独立 usage chunk [1]；DeepSeek usage 搭最后内容 chunk [21]；Fireworks 搭 finish_reason chunk [34]；Anthropic/Google 无 [DONE]、Anthropic 200 后仍可能 error 事件 [11][35]。
5. **system 不是到处都是 role**：迁 Anthropic/Google 要把 system 消息提升为顶层参数（`system` / `systemInstruction`）；Responses 优先顶层 `instructions`，且 previous_response_id 不继承 instructions [3][10][18]。
6. **结构化输出四套字段**：response_format / text.format / output_config.format / responseMimeType+responseSchema；strict 默认值还不同（chat 默认非 strict，Responses 省略即尝试 strict）[2][3][14][18][7]。
7. **tool 结果的 role 差异**：Anthropic/Google 把工具结果放 user 侧（tool_result 块 / functionResponse part），OpenAI 用独立 `role:"tool"`；Google 回传的 role 是 user 不是 tool [1][10][18]。
8. **采样参数正在被弃用**：Anthropic temperature/top_p/top_k 弃用（Opus 4.6 后模型 400）[10]；DeepSeek thinking 模式 temperature 无效 [23]；Gemini 2.5 Pro/3 无法关思考 [20]。写死 temperature=0 的代码在新模型上会碎。
9. **max_tokens 超上下文语义相反**：OpenAI 报错，Fireworks 默认静默截断 [34]。
10. **模型字符串不通用**：Together 需命名空间 ID，OpenAI 模型串 404 [33]；各家模型枚举都是自有命名。

## 5. 未决与置信度

- 【点名疑点②】智谱（GLM）anthropic 兼容端点 vs Anthropic 官方：R1 尚无数据 → R2 优先补。qwen/moonshot/xai/mistral 四行同样待补。
- Google `responseSchema`/`_responseJsonSchema` 参考页已标 deprecated 且未写替代；新 **Interactions API**（`v1beta/interactions`）已重构官方多份指南，2026-05 有 breaking changes 页 → R2 查这是否为 generateContent 的继任者。
- OpenAI 三处打架：`seed`（spec deprecated:true vs deprecations 页未列）；`parallel_tool_calls` 默认值（spec true vs 指南未写）；`reasoning.encrypted_content`（迁移指南称默认包含 vs spec 需显式 include）→ R2 核验。
- DeepSeek /responses 支持模型范围（pricing ✓✓ vs 指南仅 flash）；strict 工具是否必须走 /beta。
- 只有部分证据（⚠）：Google `x-goog-api-key` header 原句、SSE 终止细节、v1/v1beta 政策；OpenAI 错误对象 `{message,type,param,code}` 形状原句未取。
- 时效：全部为 2026-09-23 官方文档快照；Anthropic（采样弃用、adaptive thinking、output_config GA）与 Google（Interactions）的协议演进是最大变数；OpenAI Assistants API 已于 2026-08-26 下线 [9]。

## 来源

[1] OpenAI Chat API reference — https://platform.openai.com/docs/api-reference/chat/create
[2] OpenAI openapi.yaml（spec）— https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml
[3] OpenAI：Responses vs Chat Completions（迁移指南）— https://platform.openai.com/docs/guides/responses-vs-chat-completions
[4] OpenAI Prompt caching — https://platform.openai.com/docs/guides/prompt-caching
[5] OpenAI Reasoning — https://platform.openai.com/docs/guides/reasoning
[6] OpenAI Structured Outputs — https://platform.openai.com/docs/guides/structured-outputs
[7] OpenAI Function calling — https://platform.openai.com/docs/guides/function-calling
[8] OpenAI PDF files — https://platform.openai.com/docs/guides/pdf-files
[9] OpenAI API changelog — https://developers.openai.com/api/docs/changelog
[10] Anthropic Messages API — https://docs.claude.com/en/api/messages
[11] Anthropic Streaming — https://docs.claude.com/en/docs/build-with-claude/streaming
[12] Anthropic Prompt caching — https://docs.claude.com/en/docs/build-with-claude/prompt-caching
[13] Anthropic Extended thinking — https://docs.claude.com/en/docs/build-with-claude/extended-thinking
[14] Anthropic Structured outputs — https://docs.claude.com/en/docs/build-with-claude/structured-outputs
[15] Anthropic Versioning — https://docs.claude.com/en/api/versioning
[16] Anthropic Beta headers — https://docs.claude.com/en/api/beta-headers
[17] Anthropic Models overview — https://docs.claude.com/en/docs/about-claude/models/overview
[18] Gemini generate-content reference — https://ai.google.dev/api/generate-content
[19] Gemini Context caching — https://ai.google.dev/gemini-api/docs/caching
[20] Gemini OpenAI compatibility — https://ai.google.dev/gemini-api/docs/openai
[21] DeepSeek Create chat completion — https://api-docs.deepseek.com/api/create-chat-completion
[22] DeepSeek Responses API guide — https://api-docs.deepseek.com/guides/responses_api
[23] DeepSeek Thinking mode — https://api-docs.deepseek.com/guides/thinking_mode
[24] DeepSeek Updates/changelog — https://api-docs.deepseek.com/updates
[25] DeepSeek Vision — https://api-docs.deepseek.com/guides/vision
[26] DeepSeek Pricing/quick start — https://api-docs.deepseek.com/quick_start/pricing
[27] DeepSeek Context caching on disk — https://api-docs.deepseek.com/guides/kv_cache
[28] OpenRouter Provider routing — https://openrouter.ai/docs/features/provider-routing
[29] vLLM OpenAI-compatible server — https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/
[30] Ollama OpenAI compatibility — https://raw.githubusercontent.com/ollama/ollama/main/docs/api/openai-compatibility.mdx
[31] LiteLLM drop_params — https://docs.litellm.ai/docs/completion/drop_params
[32] Groq OpenAI compatibility — https://console.groq.com/docs/openai
[33] Together OpenAI API compatibility — https://docs.together.ai/docs/openai-api-compatibility
[34] Fireworks OpenAI compatibility — https://docs.fireworks.ai/tools-sdks/openai-compatibility
[35] Anthropic Errors — https://docs.anthropic.com/en/api/errors
