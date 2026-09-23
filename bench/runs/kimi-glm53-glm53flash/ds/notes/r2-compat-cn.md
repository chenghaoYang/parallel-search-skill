# r2-compat-cn
question: 百炼/DashScope（Qwen）与 Moonshot（Kimi）OpenAI 兼容模式的协议事实与差异
checked: help.aliyun.com/zh/model-studio/{compatibility-of-openai-with-dashscope, qwen-api-via-openai-chat-completions, qwen-structured-output, deep-thinking, claude-code}, platform.kimi.com/docs/guide/{use-thinking-models, start-guide}, platform.moonshot.cn/docs/api/chat （抓取 2026-09-23；moonshot.cn 文档已跳转 platform.kimi.com；页面均无显式更新日期，百炼文含 2026-07 快照）

## claims
- [C1] D1 百炼兼容 BASE_URL=业务空间专属域名，如 https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1，HTTP 端点 …/chat/completions（另有 dashscope-us/新加坡/东京）；旧域名 dashscope.aliyuncs.com 仍可用；Key 按地域绑定、跨域 401 invalid_api_key | src: https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope | quote: "POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" | type: official
- [C2] D1 兼容接口覆盖 Qwen/DeepSeek/Kimi/GLM/MiniMax；Qwen-Audio 不支持 | src: 同C1 | quote: "Qwen-Audio不支持OpenAI兼容协议，仅支持DashScope协议。" | type: official
- [C3] D3 tools 形状同 OpenAI（type:function+name/description/parameters）；tool_choice=auto/none/required/指定函数，但 Qwen 暂不支持 required | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "Qwen 系列模型暂不支持 required：非思考模式下无法保证一定调用工具" | type: official
- [C4] D3 parallel_tool_calls 默认 false（OpenAI spec default:true） | src: 同C3 | quote: "parallel_tool_calls boolean （可选）默认值为 false" | type: official
- [C5] D5 兼容模式 tools 与 stream=True 暂不可同用 | src: https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope | quote: "说明tools暂时无法与stream=True同时使用。" | type: official
- [C6] D5 流式 object=chat.completion.chunk、增量在 choices[].delta、SSE 以 data:[DONE] 终止；include_usage 时末 chunk choices=[] 带 usage | src: 同C5 | quote: "\"finish_reason\":\"stop\"…}\n\ndata: [DONE]" | type: official
- [C7] D5 迁移页返回参数 finish_reason 仅列 null/stop/length（未列 tool_calls/content_filter） | src: 同C5 | quote: "有三种情况：正在生成时为null；…stop；…length。" | type: official
- [C8] D7 迁移页参数表=model/messages/top_p/temperature/presence_penalty/n/max_tokens/seed/stream/stop/tools/stream_options/enable_search；n 仅 1-4、仅 qwen-plus、传 tools 固定 1；temperature [0,2) 且不建议 0 | src: 同C5 | quote: "当前仅支持 qwen-plus 模型，且在传入 tools 参数时固定为1。" | type: official
- [C9] D7 top_k 兼容模式可用，非 OpenAI 标准参数需 extra_body；DeepSeek/Kimi/MiniMax 系列不支持 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "DeepSeek/Kimi/MiniMax 系列均不支持 top_k 参数。该参数非 OpenAI 标准参数。" | type: official
- [C10] D7 repetition_penalty（>0，1.0=无惩罚）兼容模式可用，同需 extra_body | src: 同C9 | quote: "1.0 表示不做惩罚" | type: official
- [C11] D7 max_tokens 即将废弃→max_completion_tokens；后者=思维链+回答（同 OpenAI），max_tokens 仅限回答 | src: 同C9 | quote: "而 max_tokens 仅限制回答部分" | type: official
- [C12] D7 seed 范围 [0,2^31−1] 默认 1234；top_logprobs 上限 5（OpenAI 20） | src: 同C9 | quote: "[0,2 31 −1] … 其余模型均为 1234" | type: official
- [C13] D8 response_format 支持 text/json_object/json_schema；json_object 需提示词含 "JSON" 否则报错 | src: https://help.aliyun.com/zh/model-studio/qwen-structured-output | quote: "否则会报错：must contain the word 'json' in some form" | type: official
- [C14] D8 json_schema 模式 strict 字段推荐 true；json_schema 仅部分 Qwen3.7/3.8 系列，json_object 覆盖 Qwen 大部分模型+Kimi+GLM 等 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "是否严格遵循 schema 定义的结构。推荐设置为 true" | type: official
- [C15] D9 enable_thinking 开关混合思考；非 OpenAI 标准参数：Python SDK 走 extra_body，HTTP 可放 body 顶层 | src: 同C9 | quote: "该参数非 OpenAI 标准参数。通过 Python SDK 调用时，请放入 extra_body" | type: official
- [C16] D9 思考经 reasoning_content 返回，用量含 completion_tokens_details.reasoning_tokens（=0 即未启用） | src: https://help.aliyun.com/zh/model-studio/deep-thinking | quote: "确认用量中 reasoning_tokens 大于 0" | type: official
- [C17] D9 thinking_budget 限思维链最大 Token；适用 Kimi 阿里云直供系列，kimi-k3 不支持 | src: 同C16 | quote: "其中 kimi-k3 不支持该参数。" | type: official
- [C18] D9 preserve_thinking 控制多轮读取历史 reasoning_content，非标参数需 extra_body；限 qwen3.6-3.8 系列与百炼版 kimi-k2.6/k2.7-code 等 | src: 同C16 | quote: "preserve_thinking非 OpenAI 标准参数，…需通过extra_body传入" | type: official
- [C19] D9 模型分混合思考（可开关）与仅思考（不可关）；部分开源版仅支持流式思考，非流式报错 | src: 同C16 | quote: "…等开源版）仅支持流式输出，非流式调用会报错" | type: official
- [C20] D9 reasoning_effort 可调推理力度：DeepSeek-V4/GLM/kimi/kimi-k3 默认 high；low/medium→high、xhigh→max（枚举与 OpenAI 不同） | src: 同C9 | quote: "low 和 medium 映射为 high，xhigh 映射为 max。" | type: official
- [C21] Anthropic 兼容面：百炼有 /apps/anthropic 端点供 Claude Code（按地域 maas 域名；FAQ 表按量计费为 dashscope.aliyuncs.com/apps/anthropic），仅 /v1/messages、无 /v1/models | src: https://help.aliyun.com/zh/model-studio/claude-code | quote: "仅提供对话端点 /v1/messages，不提供模型列表端点" | type: official
- [C22] DashScope 原生接口：非标参数放 parameters（enable_thinking/incremental_output/result_format:message） | src: 同C16 | quote: "通过HTTP调用时，请将preserve_thinking放入parameters对象中。" | type: official
- [C23] D1 Kimi base_url=https://api.moonshot.cn/v1、端点 /v1/chat/completions，且"兼容 OpenAI 与 Anthropic API 格式"；模型名 kimi-k3/kimi-k2.7-code(-highspeed)/kimi-k2.6，思考开关走参数而非模型名后缀 | src: https://platform.kimi.com/docs/guide/start-guide | quote: "base_url=\"https://api.moonshot.cn/v1\"" | type: official
- [C24] D3 finish_reason="tool_calls" 时返回 tool_calls（id/function.name/function.arguments）；工具结果以 role="tool" 回传、tool_call_id 须对应；tool_choice=auto(默认)/none/required/特定函数、未提 strict | src: https://platform.moonshot.cn/docs/api/chat | quote: "tool_call_id 必须与请求中的 id 对应" | type: official
- [C25] D5 流式为 SSE（data: 行、delta 累加、finish_reason 非 null 即结束）；include_usage 的 usage 在 [DONE] 前最后 chunk | src: 同C24 | quote: "当 finish_reason 为 null 时，内容在 delta.content 中累加" | type: official
- [C26] D8 response_format 默认 text，支持 json_object 与 json_schema（Structured Output） | src: 同C24 | quote: "可启用 Structured Output，按指定的 JSON Schema 约束输出结构" | type: official
- [C27] D7 max_tokens 已弃用→max_completion_tokens（kimi-k3 默认 131072、最大 1048576）；stop 最多 5 个字符串每个≤32字节（OpenAI≤4） | src: 同C24 | quote: "已弃用，请使用 max_completion_tokens" | type: official
- [C28] D7 缓存自动开启：prompt_cache_options.mode 仅 implicit、ttl 5m/1h；无显式断点，content 含 prompt_cache_breakpoint 返回 HTTP 400 | src: 同C24 | quote: "暂不支持显式缓存断点：content 中出现 prompt_cache_breakpoint 时请求会被拒绝（HTTP 400）。" | type: official
- [C29] D9 kimi-k3 始终推理、保留式思考常开，顶层 reasoning_effort=low/high/max 默认 max、无 thinking 参数；kimi-k2.6 用 thinking.type=enabled(默认)/disabled、thinking.keep=null/all；k2.7-code 恒 enabled、keep 固定 all | src: https://platform.kimi.com/docs/guide/use-thinking-models | quote: "kimi-k3：旗舰思考模型，始终进行推理且保留式思考（Preserved Thinking）始终开启" | type: official
- [C30] D9 reasoning_content 与 content 同级、流式必先于 content；计入 max_tokens；OpenAI SDK 类型无此字段 | src: 同C29 | quote: "reasoning_content 字段一定会先于 content 字段出现" | type: official
- [C31] D7 kimi-k2.7-code/kimi-k2.6 的 temperature 不可修改、勿显式传入 | src: 同C29 | quote: "temperature 不可修改，使用默认值即可" | type: official
- [C32] D3/D5 扩展：K3 支持动态工具消息 {\"role\":\"system\",\"tools\":[...]}；Partial Mode(partial:true)；支持 prediction、logprobs/top_logprobs(0-20)、prompt_cache_key | src: https://platform.moonshot.cn/docs/api/chat | quote: "还可在任意对话位置插入 {\"role\": \"system\", \"tools\": [...]} 消息动态加载工具" | type: official

## conflicts
- 百炼 tools×stream：迁移页断言"tools暂时无法与stream=True同时使用"（C5），API 参考页却完整收录 parallel_tool_calls/tool_choice 且未重复该禁令——疑迁移页滞后。
- 百炼 json_schema 支持面：结构化输出页仅 Qwen3.7/3.8 系列列 JSON Schema、json_object 列含"Kimi"，API 参考页却给 json_schema+strict 通用说明——百炼版 Kimi 能否用 json_schema 两页口径不一。
- base_url：迁移页主推 {WorkspaceId}.maas.aliyuncs.com，deep-thinking 等页示例仍是 dashscope.aliyuncs.com/compatible-mode/v1（旧域名仍可用，属文档不同步）。

## gaps
- 百炼 tools[].function.strict（严格函数调用）无记载，仅 response_format.json_schema.strict 存在。
- 百炼流式 tool_calls 分片形状无示例；非标参数未传是否静默忽略无原文。
- Moonshot temperature/top_p/penalties 全量取值（api/chat 页折叠）未取到；其官方"与 OpenAI 差异"专页未找到。

## leads
- moonshot.cn 文档已跳 platform.kimi.com；api.kimi.com 是否并存待核。
- Moonshot 亦有 Responses API 兼容与 Anthropic Messages 兼容（Claude Code 可接）；json 校验问题指向 github.com/MoonshotAI/walle。
- 百炼上 kimi/ 前缀（月之暗面直供）kimi-k2.6 默认思考开、阿里云直供默认关；MiniMax-M3 用 thinking 参数而非 enable_thinking。
