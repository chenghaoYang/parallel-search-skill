# r1-zhipu
question: 智谱 GLM（BigModel/Z.ai）API 相对 OpenAI Chat Completions 与 Anthropic Messages 官方规格的偏差；重点 Q2：智谱 Anthropic 兼容层对比 Anthropic 官方有何不同
checked: docs.bigmodel.cn{/cn/guide/start/quick-start, /api-reference/模型-api/对话补全, /cn/guide/develop/claude(+/introduction), /cn/coding-plan/tool/claude, /cn/coding-plan/tool/others, /cn/guide/develop/responses/introduction, /llms.txt}; docs.z.ai{/api-reference/llm/chat-completion, /devpack/tool/claude, /devpack/tool/others, /guides/capabilities/thinking-mode, /api-reference/introduction, /llms.txt, /guides/develop/claude(404)}

## claims
### D1 base URL/鉴权/Responses
- [C1] bigmodel server=open.bigmodel.cn/api/，端点 POST /paas/v4/chat/completions | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "servers:\n  - url: https://open.bigmodel.cn/api/" | type: official
- [C2] z.ai server=api.z.ai/api，端点同为 /paas/v4/chat/completions | src: https://docs.z.ai/api-reference/llm/chat-completion | quote: "servers:\n  - url: https://api.z.ai/api" | type: official
- [C3] bigmodel Anthropic 端点实为 .../api/anthropic/v1/messages，头为 x-api-key | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "curl https://open.bigmodel.cn/api/anthropic/v1/messages --header \"x-api-key: YOUR_API_KEY\"" | type: official
- [C4] Coding Plan 三协议表(z.ai)各不同 base URL | src: https://docs.z.ai/devpack/tool/others | quote: "Anthropic Messages|`.../api/anthropic`...Chat Completions|`.../coding/paas/v4`...Responses|`.../api/v1`" | type: official
- [C5] 同表 bigmodel 版，路径同构 | src: https://docs.bigmodel.cn/cn/coding-plan/tool/others | quote: "Anthropic Message 协议...api/anthropic；...Chat Completion 协议...api/coding/paas/v4；...Response 协议...api/v1" | type: official
- [C6] Responses 端点非∅，独立 base_url 且自称与 OpenAI Responses 有差异 | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction | quote: "基址是`https://open.bigmodel.cn/api/v1`...仍有差异：默认`store=false`、流式结束不发`data:[DONE]`、未提供cancel" | type: official
- [C7] 鉴权为 Bearer API Key；4 页检索均未见"JWT"(见 gaps) | src: https://docs.bigmodel.cn/cn/guide/start/quick-start | quote: "Authorization: Bearer YOUR_API_KEY" | type: official

### D2 roles/多模态
- [C8] messages 角色 4 种互斥 schema(user/system/assistant/tool)；视觉请求另支持 image_url/video_url/file | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "enum:\n  - user"/"- system"/"- assistant"/"- tool" + "type: image_url" | type: official

### D4/D10 响应字段
- [C9] reasoning_content 仅特定模型系列返回 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "思维链内容，仅在使用`glm-4.5`系列,`glm-4.1v-thinking`系列模型时返回。" | type: official
- [C10] usage.prompt_tokens_details.cached_tokens 字段存在 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "cached_tokens:\n  description: 命中的缓存`Token`数量" | type: official
- [C11] request_id 6–64 字符，未传自动生成 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "长度要求：最少`6`个字符，最多`64`个字符...若未提供平台将自动生成" | type: official
- [C12] finish_reason 枚举(bigmodel/z.ai 文案一致)6 值 | src: https://docs.z.ai/api-reference/llm/chat-completion | quote: "Can be `stop`,`tool_calls`,`length`,`sensitive`,`model_context_window_exceeded` or `network_error`." | type: official

### D5 tools
- [C13] bigmodel 工具类型含 function/web_search/retrieval/mcp | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "工具类型，支持`web_search、retrieval、function`"(schema 另含 MCPToolSchema) | type: official
- [C14] z.ai 工具类型仅 function/retrieval/web_search，无 mcp | src: https://docs.z.ai/api-reference/llm/chat-completion | quote: "Currently, only functions are supported as a tool..."(anyOf 仅3 schema) | type: official
- [C15] tool_choice 仅字符串枚举 auto | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "默认`auto`且仅支持`auto`。" | type: official
- [C16] tool_stream 布尔默认 false，仅限特定系列 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "开启流式响应`Function Calls`，仅限`GLM-5.3``GLM-5.2`...`GLM-4.6`系列支持，默认值`false`" | type: official

### D6 thinking
- [C17] thinking.type 枚举 enabled/disabled 默认 enabled(GLM-5.3系列只能开启)；reasoning_effort 7档默认 max 仅 GLM-5.2+ | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "GLM-5.3...限制只能开启，由`reasoning_effort`控制思考强度...默认:`enabled`" | type: official
- [C18] clear_thinking 默认 true(清历史思维链)；false=Preserved Thinking 须原样回传 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "`false`：保留历史`turns`的`reasoning_content`...必须完整、未修改、按原顺序透传" | type: official
- [C19] Preserved Thinking 默认值按端点不同：Coding Plan 默认开，标准端点默认关 | src: https://docs.z.ai/guides/capabilities/thinking-mode | quote: "enabled by default on the Coding Plan endpoint and disabled by default on the standard API endpoint." | type: official
- [C20] interleaved thinking 自 GLM-4.5 起默认支持 | src: https://docs.z.ai/guides/capabilities/thinking-mode | quote: "We support interleaved thinking by default (supported since GLM-4.5)" | type: official

### D7 response_format
- [C21] response_format.type 仅 text/json_object，无 json_schema | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "`type`取值收敛为三种：`text`...`json_object`..." | type: official

### D8 流式
- [C22] chat/completions 流式 SSE，结束发 data:[DONE]；Response API 流式结束不发(见C6) | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "流式输出结束时会返回`data: [DONE]`消息" | type: official

### D9 采样/限额
- [C23] temperature[0,1]两位小数，各系列默认不同(1.0/0.6/0.75)；do_sample=false 时忽略 temperature/top_p | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "`GLM-5.3`...默认值为`1.0`，`GLM-4.5`系列默认值为`0.6`，`GLM-4`系列默认值为`0.75`" | type: official
- [C24] max_tokens 上限131072；无top_k(仅top_p)；停止词参数名为 stop(非stop_sequences)最多4个 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全 | quote: "maximum: 131072" + "停止词列表...maxItems: 4" | type: official

### Anthropic 兼容（重点，Q2）
- [C25] 官方自述"某些场景仍存在差异"，未逐字段列出 thinking/tool_use/cache_control/count_tokens/anthropic-beta/stop_sequences/top_k/metadata | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "某些场景下智谱与 Claude 接口仍存在差异，但不影响整体兼容性。" | type: official
- [C26] bigmodel 默认映射 OPUS=SONNET=HAIKU=GLM-4.7；升级后 SONNET/OPUS 改 glm-5.2[1m] | src: https://docs.bigmodel.cn/cn/guide/develop/claude | quote: "ANTHROPIC_DEFAULT_OPUS_MODEL：`GLM-4.7`" + "\"ANTHROPIC_DEFAULT_SONNET_MODEL\": \"glm-5.2[1m]\"" | type: official
- [C27] z.ai 页内不一致：正文三档均写 GLM-5.3-Flash，JSON 示例 SONNET 却为 glm-5.3[1m] | src: https://docs.z.ai/devpack/tool/claude | quote: "SONNET_MODEL: GLM-5.3-Flash" vs "\"SONNET_MODEL\": \"glm-5.3[1m]\"" | type: official
- [C28] effort 映射：/effort 的 low/medium/high(默认)→GLM-5.2 high；xhigh/max/ultracode→GLM-5.2 max | src: https://docs.bigmodel.cn/cn/guide/develop/claude | quote: "low, medium, high（默认值）| high" + "xhigh, max, ultracode | max" | type: official
- [C29] 1M 上下文需模型名加[1m]并设压缩窗口参数=1000000 | src: https://docs.bigmodel.cn/cn/guide/develop/claude | quote: "模型后缀加上`[1m]`即`glm-5.2[1m]`...\"CLAUDE_CODE_AUTO_COMPACT_WINDOW\": \"1000000\"" | type: official
- [C30] 鉴权变量两页不一致：迁移页用 ANTHROPIC_API_KEY；Coding Plan 页用 ANTHROPIC_AUTH_TOKEN | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction ; /claude | quote: "export ANTHROPIC_API_KEY=..." vs "\"ANTHROPIC_AUTH_TOKEN\": \"YOUR_API_KEY\"" | type: official
- [C31] z.ai 无独立迁移导览页，/guides/develop/claude 返404，Anthropic 仅见于 devpack 工具接入文档 | src: https://docs.z.ai/guides/develop/claude ; docs.z.ai/llms.txt | quote: "The server returned HTTP 404 Not Found."(devpack索引无 Claude 条目) | type: secondary

## conflicts
- z.ai claude.md 页内矛盾：正文默认三档均为 GLM-5.3-Flash，但「Manual configuration」JSON 把 SONNET/OPUS 设为`glm-5.3[1m]`，仅 HAIKU 为`glm-5.3-flash[1m]`(C27)。未替裁决。
- bigmodel schema 含 mcp 工具类型(C13)，z.ai 同类端点写"only functions are supported as a tool"且无 MCPToolSchema(C14)；两平台官方 OpenAPI 表述不一致。

## gaps
- 官方文档均未逐字段列出 thinking/tool_use/cache_control/count_tokens/anthropic-beta/stop_sequences/top_k/metadata 支持情况，仅一句笼统声明(C25)；api-reference 下无 messages/anthropic 字段参考页。
- 未找到"旧 JWT 签名"鉴权文档(quick-start/对话补全/3个claude页/llms.txt 均无"JWT")。
- z.ai 未见面向全部 API Key 用户的 Anthropic 迁移页；不确定 /api/anthropic 是否对普通 Key 开放。
- 未见智谱侧提及 count_tokens 端点的官方文档。

## leads
- bigmodel/z.ai 均有独立 Responses 协议端点(api/v1)且自称与 OpenAI Responses 有字段差异(C6)——D1 完整表格需专列一行。
- GLM Coding Plan 限定"仅可用于官方支持的工具列表"，超范围使用可能违反条款(docs.z.ai/devpack/tool/others)，供成稿风险提示参考。
