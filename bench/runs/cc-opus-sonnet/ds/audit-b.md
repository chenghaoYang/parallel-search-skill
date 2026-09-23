# audit-b：report.md §3/§4/§5 + §0(3,5,6) 抽查

范围：§3.1–3.4 四张表、§3 末尾「其他」、§4、§5、§0 第 3/5/6 条。
方法：对照 notes/ 指定文件；对高风险/具体数字项另用 WebFetch 回原页核对（标注「WebFetch复核」）。

## §0-3（"兼容 Responses ≠ 服务端状态"）

supported | DeepSeek、Kimi、OpenRouter、Ollama 的 Responses 都无状态 | r2-deepseek-responses.md[C3][C4][C5]; r2-kimi-responses.md[C1][C2][C3]; r1-scout.md[C8][C12] | —
weak | （同句）MiniMax 的 Responses 都无状态 | r3-minimax-responses.md[C1][C2]（只证"无 store 请求参数+无 previous_response_id"，无"stateless"原句直接断言）| 改写为"无 previous_response_id/conversation，历史靠 input 全量传"，去掉"无状态"定性
supported | 智谱默认 store=false；Qwen、方舟默认存储，分别留 7 天、默认 3 天 | r2-zhipu-anthropic.md[C15]; r3-qwen-responses.md[C1][C2]; r3-ark-responses.md[C12] | —

## §0-5（Q1 DeepSeek）

supported | DeepSeek Responses 入口无状态，store 恒 false，previous_response_id/conversation 不支持 | r2-deepseek-responses.md[C3][C4][C5] | —
supported | DeepSeek 推理给明文 reasoning_text，没有 summary/encrypted_content | r2-deepseek-responses.md[C8][C23] | —
supported | DeepSeek 托管工具全部忽略，custom 工具只认 apply_patch | r2-deepseek-responses.md[C9][C10] | —

## §0-6（Q2 智谱）

supported | 智谱 count_tokens/anthropic-beta/cache_control/stop_sequences/top_k/metadata/stop_reason 均 ∅ | r2-zhipu-anthropic.md gaps | —
supported | 智谱官方只写「某些场景下…仍存在差异」 | r1-zhipu.md[C25]; r2-zhipu-anthropic.md[C8] | —
supported | 智谱搜索、看图走服务端内置 MCP／image_analysis | r2-zhipu-anthropic.md[C1][C2] | —
supported | 智谱 effort 折成 high/max 两档 | r2-zhipu-anthropic.md[C3] | —
supported | 智谱模型靠客户端 ANTHROPIC_DEFAULT_*_MODEL 指定 | r1-zhipu.md[C26] | —

## §3.1（入口）

supported | DeepSeek: deepseek-v4-pro/deepseek-flash；deepseek-chat/reasoner 2026-07-24 停用 | r1-deepseek.md[C4][C5]（WebFetch 复核 updates 页日期一致） | —
weak | DeepSeek 行尾只引 [27][30][32]，但 "…/anthropic" 列出自 guides/anthropic_api | r1-deepseek.md[C1]（src=guides/anthropic_api）| 行尾补 [31]
weak | 智谱行尾只引 [36][39]，但 "…/api/anthropic" 列出自 guide/develop/claude/introduction | r1-zhipu.md[C3]（src=cn/guide/develop/claude/introduction；WebFetch 复核 [36][39] 两页均未提 anthropic） | 行尾补 [37]
weak | Qwen "另有 DashScope 原生协议" 引用 [48][49][50] | r1-qwen.md[C3]（src=qwen-api-via-dashscope，该 URL 未出现在来源节任何编号下） | 来源节补一个新编号指向该页

## §3.2（Responses 兼容）

supported | DeepSeek instructions 变成首条 system 消息 | r2-deepseek-responses.md[C6] | —
supported | Kimi store 固定 false，previous_response_id/conversation 固定 null | r2-kimi-responses.md[C1][C2][C3] | —
supported | Kimi prompt_cache_breakpoint → 400；图片只收 data URL | r2-kimi-responses.md[C11][C14] | —
supported | 智谱 previous_response_id 须 store=true，有效 7 天 | r2-zhipu-anthropic.md[C16] | —
supported | 智谱 effort 7 档折成不思考/high/max（Responses 端） | r2-zhipu-anthropic.md[C10]（WebFetch 复核原页一致，另确认事件名 response.reasoning_text.delta） | —
supported | Qwen previous_response_id 有效 7 天 | r3-qwen-responses.md[C2] | —
supported | 方舟 previous_response_id 默认存 3 天，expire_at 最长 7 天 | r3-ark-responses.md[C12] | —
supported | MiniMax temperature (0,1]，与其 Chat/Anthropic 端 [0,2] 不同 | r3-minimax-responses.md[C9] 及 conflicts 段 | —

## §3.3（Anthropic 兼容）

supported | DeepSeek 服务端把 claude-opus* 映射到 deepseek-v4-pro，其余到 flash | r1-deepseek.md[C31]（WebFetch 原页确认 haiku/sonnet→flash） | —
supported | DeepSeek budget_tokens 忽略；output_config 只认 effort | r1-deepseek.md[C29]（WebFetch 原页确认 "Only effort is supported"） | —
supported | 智谱 effort low/medium/high→high，xhigh/max→max（Claude Code /effort） | r2-zhipu-anthropic.md[C3] | —
supported | Kimi stop_reason 无 stop_sequence/pause_turn；input_tokens 口径与其 Chat 不同 | r1-kimi.md[C31][C33] | —
supported | Qwen 只列 13 个支持参数；temperature [0,2) | r1-qwen.md[C28][C29]（13 个参数逐一核对一致） | —
supported | MiniMax 鉴权 Authorization: Bearer（推荐）或 x-api-key | r3-minimax-responses.md[C11][C12] | —
supported | 方舟 cache_creation_input_tokens 恒 0 | r2-ark.md[C33] | —

## §3.4（Chat 兼容）

supported | DeepSeek 带 tools 的轮次必须回传，否则 400 | r1-deepseek.md[C18][C19] | —
supported | 智谱 clear_thinking:false 时须原样回传 | r1-zhipu.md[C18]（WebFetch 确认字段名即为 "clear_thinking"，默认 true） | —
supported | Kimi 旗舰模型 temperature/top_p/n/penalty 固定，传别的值报错 | r1-kimi.md[C26] | —
supported | MiniMax 思考默认以 <think> 混在 content，reasoning_split:true 才拆分 | r2-minimax.md[C20][C21] | —
weak | MiniMax "须回传完整 message" 系于行尾引用 [56] | r2-minimax.md[C22]（该细节 src=guides/text-m2-function-call，非 [56]=text-openai-api） | 该分句另标 guides/text-m2-function-call 对应编号
supported | 方舟 encrypted_content 优先级高于 reasoning_content，缺失降低效果 | r2-ark.md[C17][C18] | —
supported | Anthropic 兼容层 n 须为 1；不支持 prompt caching | r1-firstparty-compat.md[C11][C6] | —

## §3 末尾「其他」

supported | OpenRouter 传 store:true 或 previous_response_id 即 400 | r1-scout.md[C8] | —
supported | xAI 已弃用 Anthropic SDK 兼容 | r1-scout.md[C7] | —
weak | llama.cpp 有 /v1/messages、/v1/responses（无保留说明） | r1-scout.md[C13] 及 conflicts 段（README 写"支持"，但 issue#19138 仍在讨论加入，版本未核实） | 加限定「README 称支持，落地版本未核实」

## §4（坑）

weak | 用量口径：DeepSeek Chat 另报 hit/miss，行尾引用 [16][44][61] | r1-deepseek.md[C9]（src=api/create-chat-completion=[27]，不在 [16][44][61] 中） | 补引用 [27]
supported | 计费入口：方舟 Coding Plan 必须用 /api/coding/*（误用 /api/v3 另计费） | r2-ark.md[C6] | —
weak | 模型名映射：MiniMax 要客户端自己填模型，行尾引用 [31][38][61] | r3-minimax-responses.md[C13]（src=openapi-chat-anthropic.json=[58]，不在 [31][38][61] 中） | 补引用 [58]

## §5（未决与置信度）

supported | Qwen 的 tool_choice:"required" 范围两页不一 | r1-qwen.md conflicts 段（C10 vs C11） | —
supported | 显式缓存创建量路径两页不同（按参数页 cache_creation.cache_creation_input_tokens） | r3-qwen-responses.md conflicts 段 | —
supported | MiniMax 三个入口的 temperature 范围不同 | r3-minimax-responses.md conflicts 段 | —
supported | Kimi 迁移指南写 temperature [0,1] 可调、模型总览写固定（按后者） | r1-kimi.md conflicts 段 | —
supported | 方舟 thinking.type 在 Chat 用 auto、Anthropic 端用 adaptive | r2-ark.md conflicts 段 | —
contradicted | 二手：GitHub issue 称智谱 Anthropic 端 token 计数比官方高 43–249% | r2-zhipu-anthropic.md[C7]（原句：JSON 多算 43–49%、特殊字符多算 143–149%，无"249"这个数）；WebFetch 核对 github.com/zai-org/zai-coding-plugins/issues/12 原文确认为 "43-49%" 与 "143-149%" 两档，无 249% | 改「43–149%」，或分列「JSON 43–49%／特殊字符 143–149%」
supported | Kimi $web_search 预计 2026-10-20 下线 | r1-kimi.md[C16] | —

## 计数

supported: 41 | weak: 8 | unsupported: 0 | contradicted: 1（共 50 条）
