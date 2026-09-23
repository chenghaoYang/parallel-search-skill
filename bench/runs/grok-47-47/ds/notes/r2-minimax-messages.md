# r2-minimax-messages
question: MiniMax 官方 Anthropic Messages 兼容接口的请求和响应，相对它自己文档所写的兼容，哪些字段被收窄或加长了？
checked: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json https://platform.minimaxi.com/docs/api-reference/text-anthropic-api https://platform.minimaxi.com/docs/guides/text-generation https://platform.minimaxi.com/docs/guides/server-tools https://platform.minimaxi.com/docs/api-reference/anthropic-api-compatible-cache

## claims
- [C1] D1 全路径 | src: https://platform.minimaxi.com/docs/guides/text-generation | quote: "curl https://api.minimax.cn/anthropic/v1/messages" | type: official
- [C2] D1 SDK base 不含 /v1/messages | src: https://platform.minimaxi.com/docs/api-reference/text-anthropic-api | quote: "export ANTHROPIC_BASE_URL=https://api.minimax.cn/anthropic" | type: official
- [C3] D1 示例头 Bearer | src: https://platform.minimaxi.com/docs/guides/text-generation | quote: "Authorization: Bearer <MINIMAX_API_KEY>" | type: official
- [C4] D1 亦可 x-api-key，并存时优先 Bearer | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "如果 Authorization 和 x-api-key 同时存在，优先使用 Authorization。" | type: official
- [C7] D2 messages=对话历史，无续写 id | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "对话历史。MiniMax-M3 支持文本、图片、视频、工具调用、工具结果和 thinking 内容块。" | type: official
- [C8] D2 须回带完整 assistant content | src: https://platform.minimaxi.com/docs/api-reference/text-anthropic-api | quote: "将完整的 `response.content`（包含 thinking/text/tool\_use 等所有块）添加到消息历史" | type: official
- [C9] D2 signature 续写须原样回带 | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "thinking 内容签名，多轮续写时需要原样回带。" | type: official
- [C10] D3 role：user、assistant、user_system、group、sample_message_user、sample_message_ai | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "消息发送方角色。MiniMax-M3 使用 user / assistant 交替消息。" | type: official
- [C11] D3 content 字符串或块。请求 type：text、image、video、tool_use、tool_result、thinking、mid_conv_system | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "image 与 video 块仅 MiniMax-M3 支持。" | type: official
- [C12] D3 响应 type 仅 text、tool_use、thinking | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "响应中不会出现 image、video、tool_result 或 mid_conv_system 块。" | type: official
- [C14] D4 system 为字符串或仅 text 块，可 cache_control | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "内容块数组格式的系统提示词。text 块可携带 cache_control。" | type: official
- [C15] D4 mid_conv_system | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "mid_conv_system：对话中途插入的系统指令" | type: official
- [C16] D4 缓存序 tools→system→messages；type 仅 ephemeral；最多 4 个断点 | src: https://platform.minimaxi.com/docs/api-reference/anthropic-api-compatible-cache | quote: "一次调用最多支持 4 个 `cache_control` 参数，若超过 4 个，只取从后向前最近的 4 个" | type: official
- [C17] D5 工具 required name+input_schema | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "工具输入参数 JSON Schema。" | type: official
- [C18] D5 tool_choice 仅 auto/none | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "工具选择策略。仅支持 auto 和 none。" | type: official
- [C19] D5 tool_result：tool_use_id；content 字符串或 text/image 数组 | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "工具执行结果，可为字符串或 text/image 内容块数组。" | type: official
- [C22] D5 Beta web_search：type web_search_20250305 + name，无 input_schema，不回传 tool_result | src: https://platform.minimaxi.com/docs/guides/server-tools | quote: "Anthropic Messages API 使用版本化类型标识 `web_search_20250305`" | type: official
- [C24] D6 required 只 model、messages。max_tokens≥1。M3 推荐 131072 上限 524288；其余推荐 65536 上限 204800 | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "MiniMax-M3 推荐值为 131072（128K），上限为 524288（512K）" | type: official
- [C25] D6 文案用 length 表示截断 | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "如果生成因 `length` 原因中断，请尝试调高此值" | type: official
- [C26] D6 temperature [0,2] 默认 1，越界报错 | src: https://platform.minimaxi.com/docs/api-reference/text-anthropic-api | quote: "推荐使用1.0，超出范围会返回错误" | type: official
- [C27] D6 top_p [0,1]；正文 M3=0.95、M2.x=0.9 | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "MiniMax-M3 默认值为 0.95，M2.x 系列模型默认值为 0.9。" | type: official
- [C28] D6 thinking.type 仅 disabled|adaptive，默认 disabled；M3 的 adaptive=开启；无 budget | src: https://platform.minimaxi.com/docs/api-reference/text-anthropic-api | quote: "对于 MiniMax-M3，`adaptive` 等同于开启 thinking。" | type: official
- [C29] D6 M2.x 忽略 disabled | src: https://platform.minimaxi.com/docs/api-reference/text-anthropic-api | quote: "对于 M2.x 模型，thinking 无法关闭；即使传入 `thinking: {"type": "disabled"}`，thinking 仍会保持开启。" | type: official
- [C30] D7 stream 默认 false，true 则分批 | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "是否使用流式传输，默认为 `false`。设置为 `true` 后，响应将分批返回" | type: official
- [C31] D7 事件 message_start、ping、content_block_start、content_block_delta、content_block_stop、message_delta、message_stop | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "`message_stop`: 消息结束" | type: official
- [C32] D7 delta 仅 text_delta、thinking_delta、signature_delta；错误 event: error | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "增量类型，例如 text_delta、thinking_delta 或 signature_delta。" | type: official
- [C33] D8 非流式 id、type=message、role=assistant、model、content、stop_reason、usage | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "对象类型，固定为 `message`" | type: official
- [C34] D8 stop_reason：end_turn、max_tokens、tool_use | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "max_tokens：达到 max_tokens 限制" | type: official
- [C35] D8 usage 四字段：input_tokens、output_tokens、cache_creation_input_tokens、cache_read_input_tokens | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "命中 prompt cache 的输入 token 数。" | type: official
- [C36] D8 流式 message 另有 stop_sequence（起始 null）与 service_tier；非流式 schema 无 | src: https://platform.minimaxi.com/docs/api-reference/text/api/openapi-chat-anthropic.json | quote: "停止序列，流式开始时为 null" | type: official
- [C37] D10 忽略 top_k、stop_sequences、mcp_servers、context_management、container | src: https://platform.minimaxi.com/docs/api-reference/text-anthropic-api | quote: "部分 Anthropic 参数（如 `top_k`、`stop_sequences`、`mcp_servers`、`context_management`、`container`）会被忽略" | type: official
- [C38] D10 messages 部分支持 | src: https://platform.minimaxi.com/docs/api-reference/text-anthropic-api | quote: "M2.7、M2.5、M2.1 和 M2 系列仅支持文本与工具调用相关内容块，不支持图片和视频输入" | type: official

## conflicts
- tool_choice：SDK「完全支持」vs OpenAPI「工具选择策略。仅支持 auto 和 none。」
- 停止名：max_tokens 说明「如果生成因 `length` 原因中断」vs stop_reason 仅 end_turn、max_tokens、tool_use。
- 响应块：OpenAPI 排除 image/video/tool_result/mid_conv_system，枚举 text/tool_use/thinking；server-tools 同路径有 server_tool_use、web_search_tool_result，usage 内 service_tier，以及 base_resp。
- top_p：正文 M2.x 默认 0.9，schema `"default": 0.95`。
- Tool 要求 input_schema；web_search 示例只有 type+name。

## gaps
- D9 无 response_format、output_config、json_schema。
- anthropic-version 是否必填无规则。额外 role 无语义。省略 max_tokens 无句子。
- delta 无 input_json_delta；schema 未列 thinking/signature 字段。无用 id 续写的句子。

## leads
- 未展开：https://platform.minimaxi.com/docs/api-reference/text-post https://platform.minimaxi.com/docs/api-reference/text-chat-openai
