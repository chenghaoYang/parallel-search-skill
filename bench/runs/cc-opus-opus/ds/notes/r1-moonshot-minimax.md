# r1-moonshot-minimax
question: 月之暗面 Kimi 开放平台与 MiniMax 开放平台各自提供哪些协议端点（OpenAI 兼容、Anthropic 兼容），兼容层相对参考协议（OpenAI Chat Completions / Anthropic Messages 官方）的差异：支持/忽略/报错的字段、推理字段、工具调用、缓存、采样参数范围。
checked: https://platform.kimi.com/docs/api/overview, https://platform.kimi.ai/docs/api/overview, https://platform.kimi.com/docs/api/chat, https://platform.kimi.com/docs/api/messages, https://platform.kimi.com/docs/api/models-overview, https://platform.minimax.io/docs/api-reference/text-anthropic-api, https://platform.minimax.io/docs/api-reference/text-openai-api, https://platform.minimax.io/docs/guides/text-m3-function-call，其余见各 claim src

## claims
- [C1] MS D1 国内 OpenAI：https://api.moonshot.cn/v1 | src: https://platform.kimi.com/docs/api/overview | quote: "OpenAI Chat Completions `https://api.moonshot.cn/v1`" | type: official
- [C2] MS D1 国内 Anthropic：https://api.moonshot.cn/anthropic | src: https://platform.kimi.com/docs/api/messages | quote: "只需把 base URL 指向 `https://api.moonshot.cn/anthropic`" | type: official
- [C3] MS D1 国际 OpenAI：https://api.moonshot.ai/v1 | src: https://platform.kimi.ai/docs/api/overview | quote: "OpenAI Chat Completions `https://api.moonshot.ai/v1`" | type: official
- [C4] MS D1 国际 Anthropic：https://api.moonshot.ai/anthropic | src: https://platform.kimi.ai/docs/api/messages | quote: "point the base URL at `https://api.moonshot.ai/anthropic`" | type: official
- [C5] MS D11 私有扩展 thinking（extra_body）与 assistant 消息 partial | src: https://platform.kimi.com/docs/api/overview | quote: "`thinking` 参数需要通过 SDK 的 `extra_body` 传递；`partial` 是写在 messages 中 assistant 消息上的字段" | type: official
- [C6] MS D7 k2.6 temperature 固定（k3/k2.7-code 固定 1.0） | src: https://platform.kimi.com/docs/api/models-overview | quote: "思考模式固定 `1.0`，非思考模式固定 `0.6`，传入其他值报错" | type: official
- [C7] MS D7 top_p 0.95、n 1、penalty 0 均固定，改值报错 | src: https://platform.kimi.com/docs/api/models-overview | quote: "传入其他值会报错，建议不要显式传入" | type: official
- [C8] MS D11 tool_choice=required 仅 k3 可用 | src: https://platform.kimi.com/docs/api/models-overview | quote: "`kimi-k2.6` 与 `kimi-k2.7-code` 不支持 `required`，传入会报错" | type: official
- [C9] MS D6 K3 须原样回传 reasoning_content | src: https://platform.kimi.com/docs/guide/use-thinking-models | quote: "多轮对话和工具调用必须把 API 返回的完整 assistant message 原样回传到 `messages`（包括 `reasoning_content`）" | type: official
- [C10] MS D6 k2.x 单次工具循环内须回传全部 reasoning_content | src: https://platform.kimi.com/docs/guide/use-thinking-models | quote: "单轮任务内（一次工具调用循环中产生的多步推理）应保留上下文中所有的思考内容" | type: official
- [C11] MS D4 $web_search 即将下线 | src: https://platform.kimi.com/docs/guide/use-web-search | quote: "`$web_search` 内置联网搜索工具即将下线。新接入请改用搜索与网页抓取接口" | type: official
- [C12] MS D10 自动前缀缓存 | src: https://platform.kimi.com/docs/api/chat | quote: "Kimi API 会对重复的请求前缀自动启用上下文缓存" | type: official
- [C13] MS D10 usage.prompt_tokens_details.cached_tokens/cache_write_tokens | src: https://platform.kimi.com/docs/api/chat | quote: "`cached_tokens`、`cache_write_tokens` 与未缓存部分互斥" | type: official
- [C14] MS D10 Anthropic 层只认顶层 cache_control | src: https://platform.kimi.com/docs/api/messages | quote: "仅顶层传入时生效，`messages` 消息体内的 `cache_control` 标记会被忽略" | type: official
- [C15] MS D11 Anthropic 层 tool_choice 仅 auto/any/none | src: https://platform.kimi.com/docs/api/messages | quote: "`any`：强制调用任意工具；`none`：不调用工具" | type: official
- [C16] MS D11 Anthropic 层内容块（无 document） | src: https://platform.kimi.com/docs/api/messages | quote: "内容块数组（text / image / thinking / tool_use / tool_result）" | type: official
- [C17] MS D6 Anthropic 层 thinking 块连 signature 回传 | src: https://platform.kimi.com/docs/api/messages | quote: "请把响应中的 thinking 块（含 `signature`）原样放回 assistant 消息中" | type: official
- [C18] MM D1 Anthropic：国际 .io、国内 .cn | src: https://platform.minimax.io/docs/guides/text-m3-function-call | quote: "For international users, use `https://api.minimax.io/anthropic`; for users in China, use `https://api.minimax.cn/anthropic`" | type: official
- [C19] MM D1 OpenAI：国际 .io/v1、国内 .cn/v1 | src: https://platform.minimax.io/docs/guides/text-m3-function-call | quote: "For international users, use `https://api.minimax.io/v1`; for users in China, use `https://api.minimax.cn/v1`" | type: official
- [C20] MM D1 官方推荐 Anthropic SDK | src: https://platform.minimax.io/docs/api-reference/api-overview | quote: "the Anthropic SDK (Recommended), or the OpenAI SDK" | type: official
- [C21] MM D11 Anthropic 层忽略参数 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "(such as `top_k`, `stop_sequences`, `mcp_servers`, `context_management`, `container`) will be ignored" | type: official
- [C22] MM D7 Anthropic 层 temperature [0,2]，越界报错 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "range is [0, 2], values outside this range will return an error" | type: official
- [C23] MM D11 内容块按模型分 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "`MiniMax-M3` supports text, image, video, tool use, tool result, and thinking blocks. The M2.7, M2.5, M2.1, and M2 series support text and tool-call content blocks only" | type: official
- [C24] MM D6 Anthropic 层 M3 默认不思考，M2.x 不可关 | src: https://platform.minimax.io/docs/api-reference/text-anthropic-api | quote: "Thinking is off by default for MiniMax-M3 and can be enabled with `adaptive`. Thinking cannot be disabled for M2.x models." | type: official
- [C25] MM D6 OpenAI 层 M3 默认思考 | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "If `thinking` is omitted, thinking is on by default" | type: official
- [C26] MM D6 reasoning_split 决定思考出现位置 | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "when `true`, thinking is exposed through `reasoning_content` and `reasoning_details`; when `false`, native Chat Completions responses keep thinking inside the `content` field with `<think>...</think>` tags" | type: official
- [C27] MM D6 须回传完整 response_message | src: https://platform.minimax.io/docs/guides/text-m3-function-call | quote: "the entire `response_message` — including the `reasoning_details` field — must be preserved in the message history" | type: official
- [C28] MM D11 OpenAI 层忽略 penalty/logit_bias | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "(such as `presence_penalty`, `frequency_penalty`, `logit_bias`, etc.) will be ignored" | type: official
- [C29] MM D11 OpenAI 层 n 仅 1 | src: https://platform.minimax.io/docs/api-reference/text-openai-api | quote: "The `n` parameter only supports value 1" | type: official
- [C30] MM D4 服务端 web_search（Beta） | src: https://platform.minimax.io/docs/guides/server-tools | quote: "uses the versioned type identifier `web_search_20250305`" | type: official
- [C31] MM D10 被动自动缓存 | src: https://platform.minimax.io/docs/api-reference/text-prompt-caching | quote: "Passive caching that automatically identifies repeated context content without changing API call methods" | type: official
- [C32] MM D10 显式 cache_control 寿命 5 分钟 | src: https://platform.minimax.io/docs/api-reference/anthropic-api-compatible-cache | quote: "Cached content has a lifetime of 5 minutes." | type: official

## conflicts
- MM tool_choice：https://platform.minimax.io/docs/api-reference/text-anthropic-api "Fully supported" vs https://platform.minimax.io/docs/api-reference/text-chat-anthropic "Only auto and none are supported."
- MM M3：https://github.com/MiniMax-AI/MiniMax-M3 "M3 supports three reasoning modes through the `thinking` parameter" vs text-anthropic-api "For MiniMax-M3, `adaptive` is equivalent to thinking on."
- MS k3：https://platform.kimi.com/docs/guide/claude-code-kimi "默认开启，可关闭" vs https://platform.kimi.com/docs/api/models-overview "K3 始终进行推理思考"

## gaps
- MS Anthropic 层采样参数/映射：无原句
- 两家 tool call id 格式：无原句
- MM OpenAI 层 tool_choice/stop：无原句
- api.minimaxi.com 现状、M3 显式缓存：无原句；页面无更新日期

## leads
- 两家均有 OpenAI Responses 兼容 /v1/responses
- kimi-k2-thinking 已于 2026年5月下线（changelog）
