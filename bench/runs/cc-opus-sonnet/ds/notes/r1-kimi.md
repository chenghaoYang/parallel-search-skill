# r1-kimi
question: Moonshot Kimi 开放平台 API 相对 OpenAI Chat Completions 与 Anthropic Messages 官方规格的偏差是什么？
checked: https://platform.kimi.com/docs/api/chat, https://platform.kimi.com/docs/guide/migrating-from-openai-to-kimi, https://platform.kimi.ai/docs/guide/agent-support, https://platform.kimi.com/docs/guide/use-kimi-k2-thinking-model, https://platform.kimi.com/docs/guide/use-thinking-models, https://platform.kimi.com/docs/api/caching, https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api, https://platform.kimi.com/docs/guide/use-web-search, https://platform.kimi.com/docs/api/overview, https://platform.kimi.ai/docs/api/overview, https://platform.kimi.ai/docs/guide/claude-code-kimi, https://platform.kimi.com/docs/guide/claude-code-kimi, https://platform.kimi.com/docs/api/messages, https://platform.kimi.com/docs/api/models-overview

## claims
- [C1][D1] 旧域名301跳转新域名 | src: https://platform.kimi.com/docs/api/chat | quote: "301 Moved Permanently"（实测跳转platform.kimi.com） | type: official
- [C2][D1] .cn base_url 三协议：Chat/Responses 同为 /v1，Anthropic 为 /anthropic | src: https://platform.kimi.com/docs/api/overview | quote: "https://api.moonshot.cn/v1 ... https://api.moonshot.cn/anthropic" | type: official
- [C3][D1] .ai 站同结构 base_url | src: https://platform.kimi.ai/docs/api/overview | quote: "https://api.moonshot.ai/v1 ... https://api.moonshot.ai/anthropic" | type: official
- [C4][D1] Responses兼容端点存在，非∅ | src: https://platform.kimi.com/docs/api/overview | quote: "`/v1/responses` \| POST \| OpenAI \| Responses API" | type: official
- [C5][D1] 简报 docs/api/caching 路径已失效，实跳转到 get-api-key | src: https://platform.kimi.com/docs/api/caching | quote: "curl -L 实测 → /docs/get-api-key HTTP 200" | type: official
- [C6][D2] role 仅四种 | src: https://platform.kimi.com/docs/api/chat | quote: "role 支持 system、user、assistant、tool 其一" | type: official
- [C7][D2] Partial：assistant 消息设 partial:true 续写，含续写被截断内容用途 | src: https://platform.kimi.com/docs/api/chat | quote: "\"partial\": True ... 用相同的前缀续写被截断的内容" | type: official
- [C8][D2] 多模态图片仅 base64 或 file id，无原生外链 url | src: https://platform.kimi.com/docs/api/chat | quote: "使用 base64 编码或通过 file id 指定的图片内容" | type: official
- [C9][D4/D10] usage 缓存字段+位置：cached_tokens/cache_write_tokens 在末尾 chunk | src: https://platform.kimi.com/docs/api/chat | quote: "\"cached_tokens\":12,\"prompt_tokens_details\":{\"cached_tokens\":12,\"cache_write_tokens\":0}" | type: official
- [C10][D4/D10] 缓存为隐式自动前缀匹配，非显式建缓存对象 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "缓存按最长匹配前缀计算，匹配成功即为命中" | type: official
- [C11][D4/D10] mode 仅 implicit，ttl 仅 5m/1h | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "`prompt_cache_options.mode` 当前仅支持 `implicit`，`ttl` 支持 `5m` 和 `1h`" | type: official
- [C12][D4/D10] Anthropic端 cache_control 仅顶层生效，消息体内标记被忽略；省略则只读不写 | src: https://platform.kimi.com/docs/api/messages | quote: "仅在顶层传入时生效，messages 消息体内的 cache_control 标记会被忽略" | type: official
- [C13][D5] tool_choice 枚举 auto/none/required+函数对象 | src: https://platform.kimi.com/docs/api/chat | quote: "`required`：强制调用工具；也可传入特定函数对象强制调用指定工具" | type: official
- [C14][D5] k2.6/k2.7-code 不支持 required，仅 k3 全支持 | src: https://platform.kimi.com/docs/api/models-overview | quote: "`kimi-k2.6` 与 `kimi-k2.7-code` 不支持 `required`，传入会报错" | type: official
- [C15][D5] $web_search 声明：tools 内 type=builtin_function, name=$web_search，无需参数说明 | src: https://platform.kimi.com/docs/guide/use-web-search | quote: "\"type\": \"builtin_function\" ... \"name\": \"$web_search\"" | type: official
- [C16][D5] $web_search 预计2026-10-20下线，改用 /v1/tools/search 等独立REST接口 | src: https://platform.kimi.com/docs/guide/use-web-search | quote: "即将下线...预计 2026 年 10 月 20 日下线...改用搜索与网页抓取接口" | type: official
- [C17][D6] reasoning_content 流式中先于 content 出现 | src: https://platform.kimi.com/docs/guide/use-thinking-models | quote: "`reasoning_content` 字段一定会先于 `content` 字段出现" | type: official
- [C18][D6] 多轮/工具调用须回传完整assistant message含reasoning_content（K3） | src: https://platform.kimi.com/docs/guide/use-thinking-models | quote: "必须把 API 返回的完整 assistant message 原样回传到 `messages`（包括 `reasoning_content`）" | type: official
- [C19][D6] k2.7-code保留式思考强制开启不可关 | src: https://platform.kimi.com/docs/guide/use-thinking-models | quote: "保留式思考始终开启、无法关闭" | type: official
- [C20][D6] 思考开关因模型而异：k2.6用thinking.type，k3用顶层reasoning_effort | src: https://platform.kimi.com/docs/guide/use-thinking-models | quote: "`thinking.type`：`\"enabled\"`（默认）\| `\"disabled\"`" | type: official
- [C21][D7] response_format 三态 text/json_object/json_schema(Structured Output) | src: https://platform.kimi.com/docs/api/chat | quote: "json_schema：按指定 JSON Schema 约束输出（推荐...）" | type: official
- [C22][D7] 禁止Partial与json_object混用 | src: https://platform.kimi.com/docs/api/chat | quote: "请勿将 Partial Mode 与 `response_format={\"type\": \"json_object\"}` 混用" | type: official
- [C23][D8] Kimi额外在每个choice结束块放usage(OpenAI仅整体一份) | src: https://platform.kimi.com/docs/guide/migrating-from-openai-to-kimi | quote: "还会在每个 choice 的结束数据块中放置 `usage` 信息" | type: official
- [C24][D9] 旧口径temperature[0,1] vs OpenAI[0,2]，无换算公式 | src: https://platform.kimi.com/docs/guide/migrating-from-openai-to-kimi | quote: "Kimi API 的 `temperature`...取值范围是 `[0, 1]`，而 OpenAI...是 `[0, 2]`" | type: official
- [C25][D9] temperature=0且n>1报invalid_request_error | src: https://platform.kimi.com/docs/guide/migrating-from-openai-to-kimi | quote: "大于 1 的 `n` 值，我们将返回...`invalid_request_error`" | type: official
- [C26][D9] 现役旗舰模型temperature/top_p/n/penalty全部固定不可改 | src: https://platform.kimi.com/docs/api/models-overview | quote: "`temperature` \| 固定 `1.0`...\"固定\"表示该参数不可修改：传入其他值会报错" | type: official
- [C27][D9] max_tokens弃用→max_completion_tokens，K3默认131072/上限1048576 | src: https://platform.kimi.com/docs/api/chat | quote: "已弃用，请使用 max_completion_tokens...默认为 131072，最大可设置为 1048576" | type: official
- [C28][D9] functions参数(OpenAI已弃用)Kimi不支持 | src: https://platform.kimi.com/docs/guide/migrating-from-openai-to-kimi | quote: "Kimi API 不支持使用 `functions` 参数执行函数调用" | type: official
- [C29][Anthropic兼容] 鉴权Authorization:Bearer（非x-api-key），令牌=MOONSHOT_API_KEY | src: https://platform.kimi.com/docs/api/messages | quote: "Authorization 请求头需要一个 Bearer 令牌。使用 MOONSHOT_API_KEY 作为令牌" | type: official
- [C30][Anthropic兼容] 正式schema的model枚举只列kimi-k3 | src: https://platform.kimi.com/docs/api/messages | quote: "enum: - kimi-k3 ... default: kimi-k3" | type: official
- [C31][Anthropic兼容] stop_reason枚举无stop_sequence/pause_turn，但请求仍收stop_sequences | src: https://platform.kimi.com/docs/api/messages | quote: "enum: - end_turn - max_tokens - tool_use - refusal - null" | type: official
- [C32][Anthropic兼容] 用output_config.effort/format替代原生extended-thinking块 | src: https://platform.kimi.com/docs/api/messages | quote: "effort...推理强度，支持 low、high、max" | type: official
- [C33][Anthropic兼容] input_tokens口径与Chat Completions/Responses不同 | src: https://platform.kimi.com/docs/api/messages | quote: "本页 `input_tokens` 的口径与 Chat Completions / Responses API 不同" | type: official
- [C34][Anthropic兼容] Claude Code配置用了k3/k2.7-code/k2.6三个模型名 | src: https://platform.kimi.com/docs/guide/claude-code-kimi | quote: "\"ANTHROPIC_DEFAULT_HAIKU_MODEL\": \"kimi-k2.7-code\"" | type: official

## conflicts
- tool_choice required：chat.md通用schema未分模型列required(C13)；models-overview明确k2.6/k2.7-code不支持、传入报错(C14)。
- temperature：migrating页称[0,1]可调(C24)；models-overview页称现役三旗舰模型"固定"不可改(C26)，前者疑似未随新模型更新。
- Anthropic模型面：messages.md正式枚举只写kimi-k3(C30)；claude-code-kimi却把k2.7-code/k2.6配到同端点不同角色档(C34)。

## gaps
- agent-support（.ai域）JS渲染，.md直取为空，只有WebFetch摘要，未取得tool_choice/搜索原句。
- 未找一手页直接否定Anthropic"思考内容块"存在，只用output_config间接佐证(C32)。
- 旧版`/v1/caching`+cache_id+role:cache机制仅见pplx二手摘要引用的旧博客，未开一手页核实，未入claims。

## leads
- 旧博客提过`/v1/caching`+`cache_id`显式缓存流程，与现行隐式前缀缓存不同，疑似历史遗留API，值得核实。
- models-overview是按模型对比参数的权威页，需k2.6/k2.7-code各自finish_reason/max_tokens默认值应直接查该页。
- Kimi分.cn/.ai两套平行文档站（结构相同，域名不同），或对应中国大陆/海外账户体系。
