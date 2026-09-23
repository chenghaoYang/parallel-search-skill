# r1-ark
question: 火山引擎方舟（Volcengine Ark，豆包 Doubao 模型）的 API 协议：Chat API（OpenAI 兼容 /api/v3/chat/completions）与 Responses API（/api/v3/responses）的端点与字段，相对 OpenAI 官方 Chat Completions / Responses 有何差异？是否提供 Anthropic 兼容端点？
checked: https://www.volcengine.com/docs/82379/1494384, https://www.volcengine.com/docs/82379/1569618, https://www.volcengine.com/docs/82379/1298459, https://www.volcengine.com/docs/82379/1449737, https://www.volcengine.com/docs/82379/1956279, https://www.volcengine.com/docs/82379/1398933, https://www.volcengine.com/docs/82379/1528789, https://www.volcengine.com/docs/82379/1529329, https://www.volcengine.com/docs/82379/1396491, https://www.volcengine.com/docs/82379/1585128, https://www.volcengine.com/docs/82379/1330626, https://www.volcengine.com/docs/82379/2678892, https://www.volcengine.com/docs/82379/2615186, https://www.volcengine.com/docs/82379/1783709, https://www.volcengine.com/docs/82379/2160841, https://www.volcengine.com/docs/82379/2655179, https://www.volcengine.com/docs/82379/1928261, https://docs.byteplus.com/en/docs/ModelArk/1298459, https://docs.byteplus.com/en/docs/ModelArk/2160841

## claims
- [C1] D1 Chat 端点（2026-09-22） | src: https://www.volcengine.com/docs/82379/1494384 | quote: "POST https://ark.cn-beijing.volces.com/api/v3/chat/completions" | type: official
- [C2] D1 Responses 端点（2026-09-22） | src: https://www.volcengine.com/docs/82379/1569618 | quote: "POST https://ark.cn-beijing.volces.com/api/v3/responses" | type: official
- [C3] D1 Bearer API Key（2026-06-23） | src: https://www.volcengine.com/docs/82379/1298459 | quote: "Authorization: Bearer $ARK_API_KEY" | type: official
- [C4] D1 model 填 Model ID，多应用推荐 Endpoint ID | src: https://www.volcengine.com/docs/82379/1494384 | quote: "多个应用及精细管理场景，推荐使用推理接入点 ID 调用" | type: official
- [C5] D1 BytePlus 国际站（2026-09-18） | src: https://docs.byteplus.com/en/docs/ModelArk/1298459 | quote: "Data plane API: https://ark.ap-southeast.bytepluses.com/api/v3" | type: official
- [C6] D6 Chat thinking.type：enabled/disabled/auto | src: https://www.volcengine.com/docs/82379/1494384 | quote: "auto：自动思考模式，模型根据问题自主判断是否需要思考，简单题目直接回答。" | type: official
- [C7] D6 Chat reasoning_effort / Responses reasoning.effort：none/minimal/low/medium/high/xhigh/max | src: https://www.volcengine.com/docs/82379/1449737 | quote: "所有支持该字段的模型均接受全部 7 档取值，部分取值将按表中规则自动映射至等效档位。" | type: official
- [C8] D6 Chat 思考在 reasoning_content，Seed 2.1 等默认只给摘要 | src: https://www.volcengine.com/docs/82379/1449737 | quote: "不会输出模型原始的思考内容，会返回模型思考内容摘要（choices.message.reasoning_content）" | type: official
- [C9] D6 Responses 推理项（type=reasoning）默认给 summary 与 encrypted_content | src: https://www.volcengine.com/docs/82379/1956279 | quote: "会返回模型思考内容摘要字段 summary、思考内容加密原文字段 encrypted_content。" | type: official
- [C10] D5 previous_response_id 并入上一轮输入与回答 | src: https://www.volcengine.com/docs/82379/1569618 | quote: "会引入上一轮请求的输入和回答内容，本次请求的输入 tokens 会相应增加。" | type: official
- [C11] D5 store 标“默认值 true”；flex 时只能 false | src: https://www.volcengine.com/docs/82379/1569618 | quote: "当 service_tier 为 flex 时，本字段只能设置为 false。" | type: official
- [C12] D5 expire_at 管 store 与 caching，默认 +259200 秒，最多 7 天 | src: https://www.volcengine.com/docs/82379/1569618 | quote: "对 store（上下文存储）和 caching（上下文缓存）都生效。默认值：创建时刻+259200" | type: official
- [C13] D5 caching{type: enabled|disabled(默认), prefix: bool} | src: https://www.volcengine.com/docs/82379/1569618 | quote: "不可与 instructions 字段、tools（除自定义函数 Function Calling 外）字段一起使用。" | type: official
- [C14] D5 Session 缓存=Responses 存储+previous_response_id | src: https://www.volcengine.com/docs/82379/1398933 | quote: "通过调用 previous_response_id 在多轮对话等场景中使用缓存输入并降低推理成本。" | type: official
- [C15] D5 旧 POST /api/v3/context/create：mode session|common_prefix，ttl 默认 86400，使用即续期 | src: https://www.volcengine.com/docs/82379/1528789 | quote: "信息在创建后即开始计时，每次使用则重置为0。" | type: official
- [C16] D5 Context API 教程页标“（已下线）”（2026-09-22） | src: https://www.volcengine.com/docs/82379/1396491 | quote: "Responses API：推荐，支持更多模型，更灵活使用" | type: official
- [C17] D4 Chat 无内置工具/云部署 MCP | src: https://www.volcengine.com/docs/82379/1585128 | quote: "Chat API 当前不支持使用方舟大模型内置工具（联网搜索、图像处理、私域知识库搜索）、云部署 MCP等能力" | type: official
- [C18] D4 Chat tools.type 仅 function；tool_choice none/auto/required/指定函数 | src: https://www.volcengine.com/docs/82379/1494384 | quote: "required：模型必须调用一个或多个工具。" | type: official
- [C19] D4 Responses tool_choice.type：function/web_search/image_process/mcp/knowledge_search/doubao_app | src: https://www.volcengine.com/docs/82379/1569618 | quote: "指定要调用的工具类型，用于精确路由到对应工具。" | type: official
- [C20] D7 Chat 支持 max_completion_tokens（含思维链） | src: https://www.volcengine.com/docs/82379/1494384 | quote: "不可与 max_tokens 字段同时设置。" | type: official
- [C21] D7 logprobs/top_logprobs：思考模型不支持 | src: https://www.volcengine.com/docs/82379/1494384 | quote: "深度思考能力模型不支持该字段。其中，deepseek-v4-1-flash-260910、deepseek-v4-pro-ga-260813、deepseek-v4-flash-ga-260731 支持该字段。" | type: official
- [C22] D7 response_format text/json_schema/json_object | src: https://www.volcengine.com/docs/82379/1494384 | quote: "该能力尚在 beta 阶段，请谨慎在生产环境使用。" | type: official
- [C23] D11 非 OpenAI 字段（如 thinking）走 extra_body | src: https://www.volcengine.com/docs/82379/1330626 | quote: "传入OpenAI SDK中不支持的字段，可以通过 extra_body 字典传入" | type: official
- [C24] D9 Chat usage.prompt_tokens_details.cached_tokens；completion_tokens_details.reasoning_tokens | src: https://www.volcengine.com/docs/82379/1494384 | quote: "缓存命中的输入内容（含文本、音频等所有类型）所消耗的 token 总数" | type: official
- [C25] D9 Chat finish_reason：stop/length/content_filter/tool_calls | src: https://www.volcengine.com/docs/82379/1494384 | quote: "content_filter：模型输出被内容审核拦截。" | type: official
- [C26] D9 Responses usage.input_tokens_details.cached_tokens、output_tokens_details.reasoning_tokens、tool_usage | src: https://www.volcengine.com/docs/82379/1956279 | quote: "为原始思考内容的 tokens，计费仍然按原始思考内容 token 计算。" | type: official
- [C27] D10 隐式缓存（Chat/Responses/Batch）；显式仅 Responses，二者互斥 | src: https://www.volcengine.com/docs/82379/1398933 | quote: "隐式缓存：自动启用，用户无需额外配置，且无法关闭" | type: official
- [C28] D10 命中看 cached_tokens；隐式默认 ≥1024 tokens | src: https://www.volcengine.com/docs/82379/1398933 | quote: "大于 0 表示命中；等于 0 表示未命中。" | type: official
- [C29] Anthropic 兼容 base URL（2026-09-13） | src: https://www.volcengine.com/docs/82379/2160841 | quote: "ANTHROPIC_BASE_URL：https://ark.cn-beijing.volces.com/api/compatible" | type: official
- [C30] Coding Plan：Anthropic /api/coding，OpenAI /api/coding/v3（2026-09-23） | src: https://www.volcengine.com/docs/82379/1928261 | quote: "兼容 Anthropic 接口协议工具：https://ark.cn-beijing.volces.com/api/coding" | type: official

## conflicts
- encrypted_content 无效：1494384 "回传 encrypted_content 内容需有效，篡改或无法还原时返回错误：Invalid signature。" vs 2678892（2026-09-09）"将兼容无法解析的 encrypted_content、signature 内容输入，不会直接报错。"
- 1494384 同页：max_completion_tokens "取值范围：[1, 65536]" vs "deepseek-v4-1-flash-260910 模型该字段默认值 128k。"
- logprobs：2678892 "DeepSeek V4 正式版系列、GLM-5.2 将支持 logprobs、top_logprobs 传入和输出。" vs C21 只列 DeepSeek
- 1529329 同页："model：暂时不支持直接通过Model ID 调用模型。" vs "您需要调用的模型的 ID （Model ID）"

## gaps
- 数字 ID 指 https://www.volcengine.com/docs/82379/<ID>
- Chat 参数表未列 n/seed/user/store/metadata/modalities/audio/prediction/prompt_cache_key，无"不支持"明文
- Responses 参数表未列 parallel_tool_calls/truncation/user/background/conversation/top_logprobs/stream_options
- include 枚举、incomplete_details.reason、Messages stop_reason 未列；Endpoint ID 格式未核；支持列表(1449737)无模型标 thinking auto
- 页面 JS 渲染，WebFetch 只见导航；正文取自 www.volcengine.com/api/doc/getDocDetail 的 MDContent 与 BytePlus 内嵌数据

## leads
- Agent Plan：/api/plan、/api/plan/v3（2160841）；BytePlus Anthropic：https://ark.ap-southeast.bytepluses.com/api/compatible
- Messages（2655179）：POST /api/compatible/v1/messages；thinking.type 含 adaptive；服务端工具仅 web_search_20250305
- Access Key 鉴权须 Endpoint ID（1298459）；隐式缓存 Header X-Prompt-Cache-Id（2615186）；Responses status 4 值（1783709）；Chat 接受 role=developer（2678892）
