# r1-moonshot
question: Moonshot（Kimi 开放平台）官方 Chat Completions 兼容协议的端点与字段，文档写明相对 OpenAI 多了或少了什么？
checked: https://platform.kimi.com/docs/api/chat, https://platform.kimi.ai/docs/api/chat, https://platform.kimi.com/docs/api/overview, https://platform.kimi.ai/docs/api/overview, https://platform.kimi.com/docs/api/models-overview, https://platform.kimi.ai/docs/api/models-overview, https://platform.kimi.com/docs/llms.txt, https://platform.kimi.com/docs/guide/use-kimi-vision-model, https://platform.kimi.com/docs/guide/use-kimi-api-for-file-based-qa, https://platform.moonshot.cn/docs/api/chat

## claims
- [C1] D1 中国区根 `https://api.moonshot.cn`；base_url `https://api.moonshot.cn/v1` + `/chat/completions`。端点表 POST `/v1/chat/completions`。OpenAPI 3.1.0，info.version 1.0.0。moonshot.cn 该路径跳到 kimi.com。 | src: https://platform.kimi.com/docs/api/overview | quote: "| `/v1/chat/completions`                | POST   | OpenAI    |" | type: official
- [C2] D1 国际站根 `https://api.moonshot.ai`，base_url `https://api.moonshot.ai/v1`，同一 POST 路径。 | src: https://platform.kimi.ai/docs/api/overview | quote: "OpenAI Chat Completions | `https://api.moonshot.ai/v1`" | type: official
- [C3] D1 鉴权 `Authorization: Bearer $MOONSHOT_API_KEY`（bearerAuth 令牌即该 Key）。示例另带 `Content-Type: application/json`。可选头 `X-Msh-Request-Nonce` 非鉴权。 | src: https://platform.kimi.com/docs/api/overview | quote: "Authorization: Bearer $MOONSHOT_API_KEY" | type: official
- [C4] D2 无状态；多轮把上一轮 assistant 与工具结果原样追加进 messages。 | src: https://platform.kimi.com/docs/api/chat | quote: "需在每次请求时把前一轮的 assistant 回复（以及工具执行结果，如适用）原样追加到 `messages` 数组中再发送。" | type: official
- [C5] D2 思考回放原句：丢掉 `reasoning_content` 可能丢上下文。K3 FAQ 同样要求回传完整 assistant message。 | src: https://platform.kimi.com/docs/api/chat | quote: "请务必将每一轮 assistant 消息的 `reasoning_content` 原样保留在 `messages` 中" | type: official
- [C6] D3 role 仅 system、user、assistant、tool；标准消息 content 不得为空。content 为 string，或 type 为 text / image_url / video_url 的对象数组。 | src: https://platform.kimi.com/docs/api/chat | quote: "role 支持 system、user、assistant、tool 其一，content 不得为空。" | type: official
- [C7] D3/D10 url 支持 base64，或 `ms://<file_id>`（视觉页：ms=moonshot storage）。公网 URL 图片不支持；SVG 拒绝，当 XML 文本。 | src: https://platform.kimi.com/docs/api/chat | quote: "文件引用：`ms://<file_id>`" | type: official
- [C8] D3/D10 前缀字段名 `partial`（bool，默认 false），只在末条 assistant，非顶层。length 截断可用同一前缀续写。 | src: https://platform.kimi.com/docs/api/overview | quote: "`partial` 是写在 messages 中 assistant 消息上的字段（`\"partial\": true`），不是顶层请求参数。" | type: official
- [C9] D4 role 含 system。json_object 须在 system 或 user prompt 写明字段。file-extract 后把正文（非 file id）放进 system；pdf、doc、txt。 | src: https://platform.kimi.com/docs/guide/use-kimi-api-for-file-based-qa | quote: "请将文件内容放置在 prompt 中，而不是文件的 `file_id`。" | type: official
- [C10] D4/D10 仅 kimi-k3：`{"role":"system","tools":[...]}` 可插在任意位置动态加载工具，该消息不含 content，只影响后续。 | src: https://platform.kimi.com/docs/api/chat | quote: "且不包含 content 字段。" | type: official
- [C11] D5 tools[] type=function；必填 name、parameters（MFJS）；strict 默认 true。name 正则见 quote。 | src: https://platform.kimi.com/docs/api/chat | quote: "函数名称。必须符合正则表达式：^[a-zA-Z_][a-zA-Z0-9-_]{0,127}$" | type: official
- [C12] D5 tool_choice：auto（默认）/none/required，或 {type:function,function:{name}}。k2 不支持 required 见 conflicts。 | src: https://platform.kimi.com/docs/api/chat | quote: "`required`：强制调用工具" | type: official
- [C13] D5 工具结果消息 `role="tool"`，`tool_call_id` 必须等于 tool_calls[].id。`finish_reason` 为 `"tool_calls"` 时 message 含 id、type=function、function.name、function.arguments（JSON 字符串）。 | src: https://platform.kimi.com/docs/api/chat | quote: "`tool_call_id` 必须与请求中的 `id` 对应" | type: official
- [C14] D6 `max_tokens` 已弃用，改 `max_completion_tokens`（输出长度，非输入+输出）。K3 默认 131072，最大 1048576。触顶 `"length"`，否则 `"stop"`；超窗 `invalid_request_error`。`stop` 最多 5 条、每条 ≤32 字节。 | src: https://platform.kimi.com/docs/api/chat | quote: "Kimi K3 默认为 131072，最大可设置为 1048576。" | type: official
- [C15] D6 temperature 不可改：k3 与 k2.7-code 固定 1.0；k2.6 思考 1.0 / 非思考 0.6。top_p=0.95，n=1，presence/frequency_penalty=0。 | src: https://platform.kimi.com/docs/api/models-overview | quote: "思考模式固定 `1.0`，非思考模式固定 `0.6`，传入其他值报错" | type: official
- [C16] D7 `stream` 默认 false。true 时 SSE，增量在 `delta.content`；finish_reason 非 null 即结束。结束行 `data: [DONE]`。object=`chat.completion.chunk`。 | src: https://platform.kimi.com/docs/api/chat | quote: "模型会以 Server-Sent Events (SSE) 格式逐段返回生成的内容。" | type: official
- [C17] D7 stream_options.include_usage 默认 false。true 时在 data: [DONE] 前多一 chunk，usage 为整次统计，choices 为空；其余 usage 为 null。 | src: https://platform.kimi.com/docs/api/chat | quote: "将在 data: [DONE] 消息之前额外发送一个 chunk。" | type: official
- [C18] D8 object=`chat.completion`。`choices[].message.role` 仅 assistant；content string|null；可有 tool_calls、reasoning_content。finish_reason 枚举 stop、length、tool_calls；流式还可 null，仅最后 chunk。 | src: https://platform.kimi.com/docs/api/chat | quote: "finish reason 将为 \"length\"；否则为 \"stop\"。" | type: official
- [C19] D8 usage：prompt_tokens、completion_tokens、total_tokens、cached_tokens，及 prompt_tokens_details.cached_tokens、cache_write_tokens。与未缓存部分互斥且和=prompt_tokens。流式明细仅最后 chunk，需 include_usage=true。 | src: https://platform.kimi.com/docs/api/chat | quote: "三者之和等于 prompt_tokens" | type: official
- [C20] D9 response_format.type：text（默认）、json_object、json_schema。json_schema 要 name+schema；strict 默认 true（MFJS）。 | src: https://platform.kimi.com/docs/api/chat | quote: "默认值为 {\"type\": \"text\"}，即纯文本输出。" | type: official
- [C21] D9 混用禁令原句。引导 JSON 可用 Structured Output，或单独 partial 并预填 `{`。 | src: https://platform.kimi.com/docs/api/chat | quote: "请勿将 Partial Mode 与 `response_format={\"type\": \"json_object\"}` 混用" | type: official
- [C22] D10 概述：相对 OpenAI 兼容接口，thinking 走 extra_body，partial 在 assistant 上。同页又说只换 base_url 与 Key。模型页：OpenAI SDK 无原生 thinking。 | src: https://platform.kimi.com/docs/api/overview | quote: "部分参数为 Kimi 专有扩展：`thinking` 参数需要通过 SDK 的 `extra_body` 传递" | type: official
- [C23] D10 K3 顶层 reasoning_effort=low|high|max，默认 max。FAQ：OpenAI 的该字段切到 kimi-k3「不需要」改。K2.x 用 thinking.type=enabled|disabled、keep=all|null；k2.7-code 不能 disabled。 | src: https://platform.kimi.com/docs/api/models-overview | quote: "K3 支持顶层 `reasoning_effort`，可选值为 `\"low\"` / `\"high\"` / `\"max\"`，默认 `\"max\"`。" | type: official
- [C24] D10 `prompt_cache_breakpoint` 在 content 中则 HTTP 400。另有 prompt_cache_options.mode=`implicit`、ttl=`5m`|`1h`；prompt_cache_key；prediction.type=`content`；safety_identifier；logprobs；top_logprobs 0–20。 | src: https://platform.kimi.com/docs/api/chat | quote: "`content` 中出现 `prompt_cache_breakpoint` 时请求会被拒绝（HTTP 400）。" | type: official
- [C25] D10 视觉不支持 URL 图片，仅 base64 与文件 ID。Body≤100M。图 jpeg/png/gif/webp/bmp/heic/heif；视频 mp4/mpeg/mov/avi/x-flv/mpg/webm/wmv/3gpp。 | src: https://platform.kimi.com/docs/guide/use-kimi-vision-model | quote: "URL 格式的图片：不支持，目前仅支持使用 base64 编码的图片内容和通过文件 ID 上传的图片/视频" | type: official

## conflicts
- 主机：kimi.com 为 `https://api.moonshot.cn/v1`；kimi.ai 为 `https://api.moonshot.ai/v1`。皆 POST `/v1/chat/completions`。
- 兼容：overview「只需将 `base_url` 和 API Key 替换为 Kimi 的配置即可迁移，无需修改其他代码。」同页又称 thinking/partial 专有。models-overview：「传入其他值会报错，建议不要显式传入。」
- tool_choice：chat「`required`：强制调用工具」；models-overview：「`kimi-k2.6` 与 `kimi-k2.7-code` 不支持 `required`，传入会报错。」
- 采样：models-overview 固定 temperature/top_p/n/penalties，又写「当 `temperature` 接近 0 时，`n` 只能为 1」。chat OpenAPI 请求体无这些字段。
- 流式 usage：示例把 usage 放在 finish_reason=stop 且 choices 非空的 chunk；stream_options 写该 chunk 的 choices 为空数组。同 chat 页。
- Message schema 仅 role/content/name/partial，正文却要 tool_call_id，并回放 reasoning_content、tool_calls。
- 图片：chat「或直接传入 URL 字符串」；视觉页「URL 格式的图片：不支持」。

## gaps
- 无 formula/公式 content type 原句。无文档日期，仅 OpenAPI 1.0.0。无「比 OpenAI 少哪些字段」清单。
- OpenAPI 未定义请求侧 tool_call_id、tool_calls、reasoning_content。max_completion_tokens 默认只点名 K3=131072。

## leads
- https://platform.kimi.com/docs/guide/use-kimi-api-to-complete-tool-calls 、/docs/guide/use-partial-mode-feature-of-kimi-api 、/docs/api/files-upload 。`$web_search` 不在 chat body。
