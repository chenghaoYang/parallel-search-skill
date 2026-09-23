# r2-ark
question: 火山方舟（Volcengine Ark，豆包）对外有哪些协议入口，各自相对参照协议（OpenAI Chat Completions / Responses、Anthropic Messages）的偏差是什么？
checked: https://docs.volcengine.com/docs/ark/integrate-third-party-tools, https://docs.volcengine.com/docs/ark/coding-plan-personal-get-started, https://docs.volcengine.com/docs/ark/coding-plan-personal-plan-overview, https://docs.volcengine.com/docs/ark/deep-thinking, https://docs.volcengine.com/docs/ark/chat-api, https://docs.volcengine.com/docs/ark/messages-api, https://docs.volcengine.com/docs/ark/context-cache, https://docs.volcengine.com/docs/ark/structured-output-beta, https://docs.volcengine.com/docs/ark/function-calling, https://docs.volcengine.com/docs/ark/responses-api-text-generation

## claims
- [C1] 按量付费 OpenAI 兼容 base URL | src: https://docs.volcengine.com/docs/ark/integrate-third-party-tools | quote: "兼容 OpenAI 接口协议​https://ark.cn-beijing.volces.com/api/v3" | type: official
- [C2] 按量付费 Anthropic 兼容 base URL | src: https://docs.volcengine.com/docs/ark/integrate-third-party-tools | quote: "兼容 Anthropic 接口协议​https://ark.cn-beijing.volces.com/api/compatible​Claude Code" | type: official
- [C3] Anthropic Messages 完整 endpoint 含 /v1/messages | src: https://docs.volcengine.com/docs/ark/messages-api | quote: "POST https://ark.cn-beijing.volces.com/api/compatible/v1/messages" | type: official
- [C4 ⚔] Coding Plan 专用 OpenAI 兼容 base，与 C1 不同网关 | src: https://docs.volcengine.com/docs/ark/coding-plan-personal-get-started | quote: "兼容 OpenAI 接口协议工具： https://ark.cn-beijing.volces.com/api/coding/v3" | type: official
- [C5 ⚔] Coding Plan 专用 Anthropic 兼容 base，与 C2 不同网关 | src: https://docs.volcengine.com/docs/ark/coding-plan-personal-get-started | quote: "兼容 Anthropic 接口协议工具： https://ark.cn-beijing.volces.com/api/coding" | type: official
- [C6 ⚔裁决] 官方明确误用 /api/v3 不计入 Coding Plan 额度、额外收费 | src: https://docs.volcengine.com/docs/ark/coding-plan-personal-get-started | quote: "请勿使用 https://ark.cn-beijing.volces.com/api/v3：该 Base URL 不会消耗您的 Coding Plan 额度，而是会产生额外费用。" | type: official
- [C8] OpenAI 兼容鉴权用标准 Bearer | src: https://docs.volcengine.com/docs/ark/chat-api | quote: "-H \"Authorization: Bearer $ARK_API_KEY\"" | type: official
- [C9] Anthropic 兼容用 x-api-key，示例无 anthropic-version | src: https://docs.volcengine.com/docs/ark/messages-api | quote: "-H \"x-api-key: $ARK_API_KEY\"" | type: official
- [C10] Responses API 端点 /api/v3/responses | src: https://docs.volcengine.com/docs/ark/context-cache | quote: "curl https://ark.cn-beijing.volces.com/api/v3/responses" | type: official
- [C11] store 默认 true，可关闭 | src: https://docs.volcengine.com/docs/ark/responses-api-text-generation | quote: "默认开启存储功能，支持通过设置\"store\": true 启用 / \"store\": false 关闭。" | type: official
- [C12] previous_response_id 链式串联历史轮次 | src: https://docs.volcengine.com/docs/ark/responses-api-text-generation | quote: "previous_response_id 指代的 item + 本轮新输入 item。通过链表的形式串联之前轮次的对话" | type: official
- [C14] Chat API thinking.type：enabled/disabled/auto | src: https://docs.volcengine.com/docs/ark/deep-thinking | quote: "enabled：强制开启深度思考能力...disabled：强制关闭...auto：模型自行判断是否需要进行深度思考。" | type: official
- [C15 ⚔] Anthropic 兼容 thinking.type：disabled/enabled/**adaptive**，非 auto | src: https://docs.volcengine.com/docs/ark/messages-api | quote: "disabled：关闭深度思考。enabled：开启深度思考。adaptive：由模型自动决定是否开启深度思考。" | type: official
- [C16] reasoning_content 位于 choices.message，另有加密思考字段 | src: https://docs.volcengine.com/docs/ark/deep-thinking | quote: "会返回模型思考内容摘要（choices.message.reasoning_content）、思考内容加密原文（choices.message.encrypted_content）" | type: official
- [C17] 回传规则：encrypted_content 优先级高于 reasoning_content | src: https://docs.volcengine.com/docs/ark/deep-thinking | quote: "encrypted_content 字段优先级高，会忽略 reasoning_content 中的内容" | type: official
- [C18] 仅回传 reasoning_content 缺 encrypted_content 会降低 agent 推理效果 | src: https://docs.volcengine.com/docs/ark/deep-thinking | quote: "如果没有回传 encrypted_content 字段，将导致模型推理效果下降。" | type: official
- [C19] reasoning_effort/output_config.effort 共享七档 | src: https://docs.volcengine.com/docs/ark/chat-api | quote: "none：关闭思考。minimal：关闭思考，直接回答...max：最高程度思考" | type: official
- [C20] 思维链 token 计入 usage.completion_tokens_details.reasoning_tokens | src: https://docs.volcengine.com/docs/ark/chat-api | quote: "reasoning_tokens integer | 思维链 Token 数" | type: official
- [C21] response_format.type 三值，含 json_schema | src: https://docs.volcengine.com/docs/ark/chat-api | quote: "回答格式类型。可选值：text、json_schema、json_object。" | type: official
- [C22] json_schema 仍为 beta，官方建议生产谨慎使用 | src: https://docs.volcengine.com/docs/ark/structured-output-beta | quote: "该能力尚在 beta 阶段...服务可用性可能随访问情况产生波动，请谨慎在生产环境使用。" | type: official
- [C23] json_schema.strict 默认 false | src: https://docs.volcengine.com/docs/ark/chat-api | quote: "strict boolean 默认值 false | 严格模式...true：模型将始终严格遵循 schema 字段中定义的格式。" | type: official
- [C24] Chat API tool_choice：none/auto/required+指定函数 | src: https://docs.volcengine.com/docs/ark/chat-api | quote: "none：模型不会调用工具...auto：模型可以选择生成消息或调用工具...required：模型必须调用一个或多个工具。" | type: official
- [C25] parallel_tool_calls 默认 true | src: https://docs.volcengine.com/docs/ark/function-calling | quote: "parallel_tool_calls: true（默认值）：模型在单次请求中可以返回多个待调用的工具。" | type: official
- [C26] Anthropic 兼容 tool_choice：auto/any/none/tool+disable_parallel_tool_use | src: https://docs.volcengine.com/docs/ark/messages-api | quote: "取值固定为 auto...any...none...tool" | type: official
- [C27] 隐式缓存自动开启且不可关闭 | src: https://docs.volcengine.com/docs/ark/context-cache | quote: "隐式缓存：自动启用...且无法关闭...系统会自动识别请求中的公共前缀并进行缓存。" | type: official
- [C28] 显式缓存分前缀缓存/Session 缓存两类 | src: https://docs.volcengine.com/docs/ark/context-cache | quote: "当前显式缓存支持 Session 缓存和前缀缓存两种类型。" | type: official
- [C29] 前缀缓存首轮需 store:true 且 caching={enabled,prefix:true} | src: https://docs.volcengine.com/docs/ark/context-cache | quote: "需设置 \"store\": true（默认 true）、\"caching\": {\"type\": \"enabled\", \"prefix\": true}" | type: official
- [C30] 前缀缓存失效常见因输入<256 token 或 stream=true | src: https://docs.volcengine.com/docs/ark/context-cache | quote: "输入 Tokens 小于 256；三是请求中设置了 stream=true" | type: official
- [C31] 缓存命中字段路径 usage.prompt_tokens_details.cached_tokens | src: https://docs.volcengine.com/docs/ark/chat-api | quote: "cached_tokens integer | 缓存命中 Token 数 *usage.prompt_tokens_details.cached_tokens" | type: official
- [C32] 隐式缓存命中判定 cached_tokens>0 | src: https://docs.volcengine.com/docs/ark/context-cache | quote: "命中：cached_tokens > 0​未命中：cached_tokens = 0" | type: official
- [C33] Anthropic 兼容 usage 用 cache_creation_input_tokens 恒为 0 | src: https://docs.volcengine.com/docs/ark/messages-api | quote: "创建缓存计费的tokens数，当前暂不支持该计费方式，因此该字段返回为0。" | type: official
- [C34] Anthropic 兼容 model 须为方舟 Model ID/Endpoint ID，非 claude-* | src: https://docs.volcengine.com/docs/ark/messages-api | quote: "开通模型服务并查询 Model ID...可改传 Endpoint ID（在线推理接入点的 ID）" | type: official
- [C35] Anthropic 兼容 Messages 为无状态接口，需传完整历史 | src: https://docs.volcengine.com/docs/ark/messages-api | quote: "本接口为无状态接口，多轮对话时每次请求都需传入完整的消息历史。" | type: official

## conflicts
- thinking.type 取值方舟内部不一致：Chat API 用 auto（C14），Anthropic 兼容 Messages API 用 adaptive（C15）。未见互相说明是否等价，不裁决。
- R1 的 ⚔已裁：/api/coding(/v3) 与 /api/v3、/api/compatible 是平行独立网关，专供 Coding Plan 计费（C6, official），ZCode 页 /api/coding/v3 即此网关，非另一套体系，不算冲突。

## gaps
- Anthropic 兼容层是否支持 anthropic-version/beta header：官方示例未展示，未见"不支持"声明。
- 原生 Anthropic thinking.budget_tokens 未见于 messages-api 页，无法判断忽略/报错（未抓 Anthropic 官方页对照）。
- Coding Plan 是否有独立 /api/coding/v3/responses 未直接验证。
- messages-api 页未提及 Anthropic 原生 cache_control 缓存块字段。

## leads
- Codex CLI 用 wire_api="responses"，base_url 仍为按量付费 /api/v3（非 /api/coding/v3），见 integrate-third-party-tools（official）。
- 二手搜索提示第三个 base https://ark.cn-beijing.volces.com/api/plan（Agent Plan），仅 Perplexity 摘要，未一手核实。
- messages-api 响应新增 service_status.model_fallback.{fallback_triggered,original_model}，为原生 Anthropic 所无的方舟扩展字段。
- glm-5-3-flash-260828 等模型 thinking 不支持 disabled，模型级差异表需单列。
