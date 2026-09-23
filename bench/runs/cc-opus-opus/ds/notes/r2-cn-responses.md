# r2-cn-responses
question: 智谱（BigModel / Z.ai）、Kimi、MiniMax 三家是否提供 OpenAI Responses 兼容端点？若有：路径、是否支持服务端状态（store、previous_response_id、conversation）、推理内容在 Responses 里怎么表示（reasoning item / summary / encrypted_content）、不支持字段是忽略还是报错？另核验一处 MiniMax 冲突。
checked: https://docs.bigmodel.cn/llms.txt, https://docs.bigmodel.cn/cn/guide/develop/responses/introduction, https://docs.bigmodel.cn/openapi/openapi-responses.json, https://docs.bigmodel.cn/sitemap.xml, https://docs.z.ai/llms-full.txt, https://platform.kimi.com/docs/llms-full.txt, https://platform.kimi.com/docs/api/responses, https://platform.kimi.ai/docs/api/responses.md, https://platform.kimi.com/docs/sitemap.xml, https://platform.minimax.io/docs/llms-full.txt, https://platform.minimax.io/docs/api-reference/responses-create, https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json, https://platform.minimax.io/docs/api-reference/text-anthropic-api.md, https://platform.minimax.io/docs/api-reference/text-chat-anthropic.md, https://platform.minimax.io/docs/sitemap.xml, https://platform.minimaxi.com/docs/api-reference/responses-create.md, https://platform.minimaxi.com/docs/api-reference/text-chat-anthropic.md

## claims
- [C1] 智谱 Responses base URL https://open.bigmodel.cn/api/v1，POST /responses | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction | quote: "Response API 的基址是 `https://open.bigmodel.cn/api/v1`，不是对话补全使用的 `https://open.bigmodel.cn/api/paas/v4`。" | type: official
- [C2] 智谱支持 store + previous_response_id，id 有效期 7 天 | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction | quote: "`store` + `previous_response_id` 由服务端拼接上下文，响应 id 有效期 7 天" | type: official
- [C3] 智谱默认 store=false；流式无 [DONE]；无 cancel | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction | quote: "默认 `store=false`、流式结束不发送 `data: [DONE]`、当前未提供 cancel。" | type: official
- [C4] 智谱 GET/DELETE /responses/{response_id} 与 GET …/input_items 需 store=true | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction | quote: "查询、列举输入项和删除都要求创建时 `store=true`。" | type: official
- [C5] 智谱推理 item：type=reasoning，content {type: reasoning_text, text} | src: https://docs.bigmodel.cn/openapi/openapi-responses.json | quote: "输出文本类型，此处为 `reasoning_text`。" | type: official
- [C6] 智谱工具 function/namespace/custom/web_search；tool_choice 仅 none/auto | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction | quote: "`tool_choice` 为 `none` 或 `auto`。另支持 `namespace`、`custom` 和由服务端执行的 `web_search`。" | type: official
- [C7] Z.ai Responses base URL https://api.z.ai/api/v1 | src: https://docs.z.ai/devpack/quick-start | quote: "OpenAI Responses | `https://api.z.ai/api/v1`" | type: official
- [C8] Kimi：POST https://api.moonshot.cn/v1/responses | src: https://platform.kimi.com/docs/guide/codex-kimi | quote: "在底层，Codex 会将请求发送到 `POST https://api.moonshot.cn/v1/responses`。" | type: official
- [C9] Kimi 请求体无 store；响应 store、background 描述为 | src: https://platform.kimi.com/docs/api/responses | quote: "固定为 `false`。" | type: official
- [C10] Kimi 请求体无 previous_response_id/conversation；响应中二者为 | src: https://platform.kimi.com/docs/api/responses | quote: "固定为 `null`。" | type: official
- [C11] Kimi 推理 item：type=reasoning，文本在 summary[].summary_text，summary 描述为 | src: https://platform.kimi.com/docs/api/responses | quote: "推理内容。" | type: official
- [C12] Kimi 推理 item 的 encrypted_content 描述为 | src: https://platform.kimi.com/docs/api/responses | quote: "固定为 `null`。" | type: official
- [C13] Kimi input 可回传 reasoning item | src: https://platform.kimi.com/docs/api/responses | quote: "回放上一轮的推理内容。`content` 优先于 `summary`。" | type: official
- [C14] Kimi 工具 | src: https://platform.kimi.com/docs/api/responses | quote: "`tools` 支持四种工具类型：`function`、`namespace`、`custom`（仅 `apply_patch`）与 `web_search`，其他类型不支持。" | type: official
- [C15] Kimi web_search 子字段：部分报错、部分忽略 | src: https://platform.kimi.com/docs/api/responses | quote: "`search_context_size`、`blocked_domains`、`filters.blocked_domains` 不支持，传入会返回 `invalid_request_error`；`user_location`、`external_web_access`、`indexed_web_access` 会被忽略。" | type: official
- [C16] MiniMax：https://api.minimax.io/v1/responses | src: https://platform.minimax.io/docs/guides/server-tools | quote: "the OpenAI Responses API endpoint is `https://api.minimax.io/v1/responses`." | type: official
- [C17] MiniMax 仅 POST /v1/responses 与 /v1/responses/input_tokens，无 GET/DELETE | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "MiniMax OpenAI Responses API compatible endpoints, supporting chat generation and token estimation" | type: official
- [C18] MiniMax 推理 item：type=reasoning、summary、content[] type=reasoning_text；M3 默认关 | src: https://platform.minimax.io/docs/api-reference/text/api/openapi-responses.json | quote: "Reasoning output (only returned when reasoning is enabled)" | type: official

## conflicts
- MM×D4 tool_choice（非版本差异：lastmod 2026-06-10 vs 06-09，国内站同样矛盾；未裁决）：https://platform.minimax.io/docs/api-reference/text-anthropic-api "`tool_choice` | Fully supported | Tool selection strategy" vs https://platform.minimax.io/docs/api-reference/text-chat-anthropic "Tool selection strategy. Only auto and none are supported."（enum auto/none）。
- MiniMax Responses 工具：https://platform.minimax.io/docs/api-reference/responses-create spec（06-08）Tool.type enum 仅 "function" vs https://platform.minimax.io/docs/guides/server-tools（09-17）"the OpenAI Responses API uses the `web_search` tool type"。

## gaps
- 三家均未说明未知顶层字段（如向 Kimi/MiniMax 传 store、previous_response_id）是忽略还是报错。
- 智谱 spec 无 conversation/include/encrypted_content/推理 summary；Z.ai 无 Responses 参考页，状态未证实。
- MiniMax 请求体无 store/previous_response_id/conversation/include；响应 store（"Whether the response is persisted"）取值未说明；无 encrypted_content。
- 页面无可见日期；sitemap lastmod：智谱 09-23、Z.ai 09-18、Kimi 09-18（2026）。

## leads
- Kimi 国际站 base https://api.moonshot.ai/v1；prompt_cache_breakpoint 直接 HTTP 400。
- MiniMax 国内 Responses 域名 https://api.minimax.cn。
