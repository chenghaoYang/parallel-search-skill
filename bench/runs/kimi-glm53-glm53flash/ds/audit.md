# audit of ds/report.md（2026-09-23）
方法：读全文 + 14 份笔记（r1-*×6, r2-*×6, r3-*×2），抽 47 条具体主张逐条对笔记原句；编号连续性与内部引用用 grep 机械核验。未改 report.md，未做新调研。

## 逐条判定

### §0
- supported | `store` 默认 true（服务端状态仅 Responses）[1] | r1-openai-responses C10（"Defaults to true when omitted."） | 无需改
- supported | Anthropic 弃用 temperature/top_p/top_k（新模型 400）、转 thinking:{type:"adaptive"} [6][9] | r1-anthropic-messages C24/C28 | 无需改
- supported | DeepSeek「64K/无 FC」旧差异已过时 [22][27] | r1-deepseek C24（1M/384K）+C11（V3.2 起 thinking 可 FC） | 无需改

### §2.1
- supported | 必填 `anthropic-version: 2023-06-01` [11][12] | r1-anthropic-messages C20/C21 | 无需改
- supported | Gemini `x-goog-api-key`（或 `?key=`）[14][21] | r2-google-interactions C3/C4 + r1-google-gc C15 | 无需改（R1 gap 已由 r2 补上）
- supported | Responses 2025-03-11 发布 [5] | r1-openai-responses C26（changelog Mar 11, 2025） | 无需改

### §2.2
- supported | Gemini role 仅 user/model（无 assistant）[14] | r1-google-gc C5 | 无需改
- supported | Anthropic 相邻同 role 自动合并 [6] | r1-anthropic-messages C2 | 无需改
- supported | Chat file 内容块仅 PDF [2] | r1-openai-chat C25 | 无需改

### §2.3
- supported | Responses 扁平 function 工具、strict 省略即试不兼容回退 [1][3] | r1-openai-responses C7/C30 + r1-scout C17 | 无需改
- supported | `disable_parallel_tool_use` 在 tool_choice 内 [6] | r1-anthropic-messages C12 | 无需改
- weak | Gemini 结果经 **user role** functionResponse 回传 [14] | r1-google-gc gaps 明示「functionResponse 回传轮 role…页未开或 404」，仅字段名有据（C11） | 删「user role」或标注为推断
- weak | Responses tool_choice「同类枚举+每工具开关」[1] | 笔记仅 C2 证 tool_choice 字段存在，枚举值与每工具开关无主张 | 补 spec 原句或删「每工具开关」
- weak | Gemini `toolConfig.functionCallingConfig`（mode ANY…）[14] | toolConfig 字段有据（r1-google-gc C3）；mode 枚举仅 gaps 注释见 "FunctionCallingConfigMode.ANY" | 标注仅 ANY 有据，其余枚举值未取证

### §2.4
- supported | Anthropic 手动 cache_control（ttl 5m/1h）、断点 ≤4 槽、usage 分 cache_creation/read [6][8] | r1-anthropic-messages C14/C15/C16（≤4 槽避开了「5 断点」旧说，正确） | 无需改
- supported | ZDR 强制 store:false [1][3] | r2-openai-verify C12 | 无需改
- supported | Gemini implicit 默认开（3.x Flash 最小 4096）+ 显式 `cachedContents` [15] | r1-google-gc C12/C13 | 无需改
- supported | OpenAI implicit 默认开（前缀 ≥1,024 tokens）[1][4] | r1-openai-chat C13 | 建议补限定「GPT-5.6+」（笔记原句绑定该代模型）

### §2.5
- weak | Responses 终止 response.completed（**无 [DONE]**）[3] | 笔记仅有事件名（r1-openai-responses C13），无「不发 [DONE]」原句；「不发 [DONE]」原句只存在于智谱面（r3-zhipu-coding C8） | 删「无 [DONE]」或标推断
- supported | Anthropic 200 后仍可能 error 事件 [7][13] | r1-scout C21（errors 页） | 无需改
- supported | stop_reason 7 值：end_turn/max_tokens/stop_sequence/tool_use/pause_turn/refusal/model_context_window_exceeded [6] | r1-anthropic-messages C19 + r1-scout C22 | 无需改
- supported | Responses typed events 60+ 种、带 sequence_number [1][3] | r1-openai-responses C14 | 无需改

### §2.6
- supported | `max_output_tokens` min 16、含 reasoning [1] | r1-openai-responses C16 | 无需改
- supported | chat `seed` 已参数级弃用 [1] | r2-openai-verify C1（spec 行 37643 deprecated:true） | 无需改
- supported | reasoning item 须放回 input；encrypted_content 默认填充 [1][3] | r2-openai-verify C9/C10（R1 冲突已由 r2 裁决为「默认填充」） | 无需改
- supported | budget_tokens≥1024；4.6+ 弃用（4.7+ 400）、转 adaptive [6][9] | r1-anthropic-messages C26/C28/C29 | 无需改
- supported | Gemini responseMimeType+responseSchema 已标弃用、迁移目标 Interactions response_format [14][20] | r1-google-gc C19 + r2-google-interactions C20/C21 | 无需改
- supported | Responses `text.format` 同三值 [3] | r1-openai-responses C19（三值出自 spec=[1]，C20=[3] 仅映射句） | 建议改标 [1][3]
- supported | GPT-5.4 起 chat+工具仅 effort=none [2][3] | r1-openai-chat C11 / r1-openai-responses C28 | 无需改

### §2.7
- supported | steps 数组 2026-05 起取代 outputs；function_call Step {type,id,name,arguments} [19] | r2-google-interactions C10/C14 | 无需改
- weak | Content 为类型化块、**无 role/parts** [19] | r2 C11 证类型化块；gaps 自认「无 role 系全页零出现推断，未见官方原句」 | 改为「参考页已无 role 字段（观察，非官方声明）」
- supported | thinking_level（minimal…high）+ thinking_summaries；事件改名 interaction.created、step.* [17][19] | r2-google-interactions C22/C23/C29 | 无需改

### §3.1
- supported | Assistants 已下线（2026-08-26）[5] | r1-openai-responses C25 | 无需改
- weak | Mistral /v1/conversations(β) [46] | 仅 r2-compat-west leads 一行、无 quote；[46] 是 function_calling 页，出处疑为 migration-guides | 回补来源或降级为线索
- supported | Moonshot Responses 面 /docs/api/responses、Messages 面 [57][58] | r3-conflicts C13/C15/C16（canonical 加 /docs 前缀，核实过） | 无需改

### §3.2
- supported | max_tokens 默认 8K/64K（effort=max 128K）、输出上限 384K、上下文 1M [22][28] | r1-deepseek C23/C24 | 无需改
- supported | include_usage 时 usage 搭最后内容 chunk；未开 stream 传 stream_options→400 [22] | r1-deepseek C17 | 无需改
- supported | /responses 不支持 previous_response_id/store 等、未支持参数静默忽略、并行恒开、两模型均支持 [23][27] | r2-deepseek-faces C18/C19/C20 + 冲突①裁决 | 无需改
- weak | base_url `https://api.deepseek.com`（**无 /v1**）[22] | r1-deepseek gaps：「/v1 是否被拒官方只给无 /v1 示例，未明说」 | 加粗改法：改「官方示例均不带 /v1（是否拒绝未说明）」
- supported | finish_reason 新增 insufficient_system_resource、aborted [22] | r1-deepseek C32 | 无需改
- supported | /anthropic 面：映射 opus*→v4-pro、haiku/sonnet*→flash；version/beta 忽略；budget_tokens/cache_control/disable_parallel_tool_use 忽略；块不支持 document/search_result/redacted_thinking/mcp_* [24] | r2-deepseek-faces C3/C4/C6/C7/C8/C10/C12 | 无需改

### §3.3
- supported | GLM thinking.type=enabled/disabled 无 budget_tokens、力度走 reasoning_effort（5.3 仅 max/high/low）、传 disabled 报错 [30] | r2-zhipu-anthropic C13/C14/C15 | 无需改
- supported | 智谱缓存隐式自动、命中看 prompt_tokens_details.cached_tokens、前缀建议 ≥500 token [31] | r2-zhipu-anthropic C17/C18/C19 | 无需改
- supported | /api/v1 与 OpenAI 三点差异（store=false、无 [DONE]、无 cancel）+ tool_choice 仅 none/auto、text.format 仅两值、max_output_tokens 默认 65536 [56] | r3-zhipu-coding C7/C8/C9/C12/C13 | 无需改

### §3.4
- supported | 百炼 parallel_tool_calls 默认 false（OpenAI true）[34][35] | r2-compat-cn C4 | 无需改
- supported | tools×stream 已可用；复杂参数（array/object）需非标 tool_stream=true；迁移页旧禁令滞后 [34][35] | r3-conflicts C2/C3/C5 | 无需改
- supported | 百炼 seed 默认 1234；top_logprobs 上限 5 | r2-compat-cn C12 | 无需改
- supported | Kimi：stop ≤5；k3 恒思考、reasoning_effort low/high/max；k2.7-code/k2.6 temperature 不可改；缓存自动开、显式断点 400 [37][38][39] | r2-compat-cn C27/C28/C29/C31 | 无需改
- supported | xAI：strict 恒 true；流式函数调用整块单 chunk、每 chunk 带 usage；finish_reason 含 end_turn；reasoning_effort low…xhigh 不可关 [40]–[44] | r2-compat-west C8/C9/C10/C12/C15 | 无需改
- supported | Mistral：tool_choice 用 any 无 required；random_seed；strict="Not supported" [45][46][47] | r2-compat-west C18/C19/C22 | 无需改

### §4
- weak | 智谱 Claude Code「服务端映射 glm-4.7→glm-5.2」、计费按映射后模型 [32] | r2-zhipu-anthropic C9 原义是「默认映射模型=glm-4.7，最新配 glm-5.2[1m]」，非 4.7→5.2 映射；智谱侧「计费按映射后模型」笔记无据（该句仅 DeepSeek 有据 C6） | 改「默认映射模型 glm-4.7（最新配置 glm-5.2[1m]）」；计费句限定 DeepSeek
- supported | Gemini 2.5 Pro/3 思考不可关 [16] | r1-scout C24（"Reasoning cannot be turned off for Gemini 2.5 Pro or 3 models."） | 无需改

## 结构检查
- 来源节 [1]–[58] 连续完整（58 行逐条在列）✓
- 正文引用编号 = {1..58}，全部可在来源节找到，无悬空/越界编号 ✓
- ✗ §5「三家协议面都在快速演进（§0.9）」：§0 只有 1–8 条，§0.9 不存在 → 改为 §0.8

## 计数
supported 39 / weak 8 / unsupported 0 / contradicted 0（共 47 条）

## 最重要的 3 条
1. §5 引用「§0.9」指向不存在的章节（§0 仅 1–8 条）——唯一硬伤，改 §0.8。
2. §2.5「Responses 无 [DONE]」与 §2.3「Gemini functionResponse 须 user role」：笔记均无原句支撑（后者 gaps 明示未取证），建议删除断言或标注推断。
3. §4.5「智谱映射 glm-4.7→glm-5.2 + 计费按映射后模型」：笔记原义是「默认映射模型 glm-4.7、最新配 glm-5.2[1m]」，计费句对智谱无据，建议改写并限定到 DeepSeek。
