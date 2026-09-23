# r3-ark-responses
question: 方舟 Responses API（/api/v3/responses）的推理表示与不支持字段；Anthropic 端是否处理 anthropic-version / anthropic-beta / budget_tokens。
checked: https://docs.volcengine.com/docs/ark/responses-api-text-generation, https://docs.volcengine.com/docs/ark/responses-api-deep-thinking, https://docs.volcengine.com/docs/ark/responses-api-tool-calling, https://docs.volcengine.com/docs/ark/responses-api-migration, https://docs.volcengine.com/docs/ark/context-cache, https://docs.volcengine.com/docs/ark/base-url-and-authentication, https://docs.volcengine.com/docs/ark/messages-api

## claims
- [C1] Responses 输出用 output 数组，含独立 reasoning item（非 reasoning_content 字段） | src: https://docs.volcengine.com/docs/ark/responses-api-migration | quote: "\"id\":\"rs_...\",\"type\":\"reasoning\",\"summary\":[{\"type\":\"summary_text\",\"text\":\"...\"}],\"status\":\"completed\"" | type: official
- [C2] 默认开启 thinking summary，字段名为 summary + encrypted_content，不输出原始思维链 | src: https://docs.volcengine.com/docs/ark/responses-api-deep-thinking | quote: "默认会开启 thinking summary 能力，不会输出模型原始的思考内容，会返回模型思考内容摘要字段 summary、思考内容加密原文字段 encrypted_content。" | type: official
- [C3] reasoning.effort 只影响原始思考内容，不影响摘要 | src: https://docs.volcengine.com/docs/ark/responses-api-deep-thinking | quote: "reasoning.effort：仅作用于模型的原始思考内容，不适用于思考摘要。" | type: official
- [C4] 多轮回传两种方式：推荐 previous_response_id 自动带入，或手动回传完整 encrypted_content | src: https://docs.volcengine.com/docs/ark/responses-api-deep-thinking | quote: "previous_response_id（推荐）：自动获取原始思考内容并回传给模型参与推理。手动回传 encrypted_content：按接收到的完整格式回传思考内容加密原文" | type: official
- [C5] 思维链 token 计费字段为 usage.output_tokens_details.reasoning_tokens | src: https://docs.volcengine.com/docs/ark/responses-api-deep-thinking | quote: "usage.output_tokens_details.reasoning_tokens：为原始思考内容的 tokens，计费仍然按原始思考内容 token 计算。" | type: official
- [C6] 支持的内置工具：豆包助手、联网搜索、Image Process、私域知识库搜索 | src: https://docs.volcengine.com/docs/ark/responses-api-tool-calling | quote: "支持豆包搜索 Custom 版和联网内容插件两种工具...支持通过 Responses API 调用对输入图片执行画点、画线、旋转、缩放...支持通过 Responses API 调用直接获取企业私域知识库中的信息" | type: official
- [C7] 自定义函数工具类型固定为 function | src: https://docs.volcengine.com/docs/ark/responses-api-tool-calling | quote: "\"type\": \"function\"" | type: official
- [C8] 支持云部署/Remote MCP，经 Streamable HTTP 链接调用 | src: https://docs.volcengine.com/docs/ark/responses-api-tool-calling | quote: "Responses API 支持通过 Streamable HTTP 链接的 MCP 调用。适用于复杂任务...支持与自定义函数、Web Search 工具混合使用。" | type: official
- [C9] 官方列出 Responses API 不支持的（非字段级）场景，无逐字段黑名单 | src: https://docs.volcengine.com/docs/ark/responses-api-migration | quote: "不支持使用 TPM 保障包。不支持精调后模型的在线推理。不支持智能模型路由。不支持在线推理服务的模型版本切换。" | type: official
- [C10] 流式事件命名与 OpenAI Responses 风格一致：created/in_progress/output_item.added/reasoning_summary_part.added/reasoning_summary_text.delta | src: https://docs.volcengine.com/docs/ark/responses-api-deep-thinking | quote: "event: response.created​...event: response.in_progress​...event: response.output_item.added​...event: response.reasoning_summary_part.added​...event: response.reasoning_summary_text.delta" | type: official
- [C11] SDK 示例以 response.completed 事件类型判定流结束 | src: https://docs.volcengine.com/docs/ark/responses-api-deep-thinking | quote: "if event.type == \"response.completed\":" | type: official
- [C12] 存储/缓存默认 3 天，可经 expire_at 最长设至 7 天 | src: https://docs.volcengine.com/docs/ark/responses-api-text-generation | quote: "存储时长：默认存储 3 天，可通过 expire_at 字段自定义设置，最长支持 7 天。" | type: official
- [C13] expire_at 为 UTC Unix 时间戳+604800，过期后不因使用而重置 | src: https://docs.volcengine.com/docs/ark/context-cache | quote: "当前最大可存储时间为 7 天，即当前 UTC Unix 时间戳 + 604800...不会随着缓存 / 存储的使用而重置缓存生命周期。" | type: official
- [C14] 官方 Base URL/鉴权参考页只文档化 OpenAI 兼容的 Bearer 与 HMAC-SHA256，无 anthropic-version/anthropic-beta 字样 | src: https://docs.volcengine.com/docs/ark/base-url-and-authentication | quote: "Authorization: Bearer $ARK_API_KEY" | type: official
- [C15] Anthropic Messages 参考页完整文档化的 thinking 对象仅含 type 三值，未见 budget_tokens 字段 | src: https://docs.volcengine.com/docs/ark/messages-api | quote: "thinking object | 深度思考配置...type string 必选 | 思考模式...disabled：关闭深度思考。enabled：开启深度思考。adaptive：由模型自动决定是否开启深度思考。" | type: official

## conflicts
（本轮未发现新冲突；R2 已记录的 thinking.type auto/adaptive 不一致仍成立，见 r2-ark.md）

## gaps
- 未找到官方逐字段列出 Responses API 不支持/忽略哪些 OpenAI 专有字段（include、background、truncation、conversation 等）；已查 7 个页面均未出现这些英文字段名，无法判断"未实现"还是"文档未写"，也不确定未知字段是报错还是静默忽略。
- 未见 data: [DONE] 终止行；三份官方页面的流式示例（Chat/Responses/深度思考）均以具名事件（如 response.completed）收尾，无法排除额外发送 [DONE] 的可能。
- base-url-and-authentication 与 messages-api 两页均未出现 anthropic-version、anthropic-beta、thinking.budget_tokens 字样；官方既未声明支持也未声明不支持（二手 Perplexity 摘要同样确认"文档未列出该参数支持矩阵"，仅作旁证，非一手）。

## leads
- Responses API 仅 250615 及之后版本的大语言模型默认支持，具体清单在模型列表页，本轮未展开核实。
- 私域知识库搜索工具"目前仅支持旗舰版知识库"，评估工具可用性时需注意版本门槛。
- 二手信息称方舟原生思考控制语义更接近 reasoning effort 档位而非 Anthropic 的精确 token 预算模型，未一手验证，供后续追问方向。
