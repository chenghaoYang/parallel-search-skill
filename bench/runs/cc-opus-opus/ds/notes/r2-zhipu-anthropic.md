# r2-zhipu-anthropic
question: 智谱（BigModel / Z.ai）的 Anthropic 兼容端点，相对 Anthropic 官方 Messages API，有哪些可被文档或公开报告证实的行为差异？另核验一处官方文档冲突。
checked: docs.bigmodel.cn/cn/{guide/capabilities/thinking,guide/develop/claude,coding-plan/latest-model,coding-plan/mcp/{vision,search,reader}-mcp-server}, docs.z.ai/{devpack/tool/claude,devpack/latest-model,devpack/mcp/{vision,search}-mcp-server,guides/capabilities/thinking}, huggingface.co/zai-org/{GLM-5,GLM-5.1,GLM-5.2}, github.com/{zai-org/GLM-5 README,zai-org/feedback/issues/{172,182,387,411,593},zai-org/GLM-5/issues/{74,76,139},betmoar/cc-proxy-plugin/issues/67,kolega-ai/kolega-code/pull/613,vybestack/llxprt-code/pull/3704,lsm/HyperNeo/pull/2185}, +10 无关

## claims
- [C1] 【模型映射】BigModel：服务端把 Claude 模型名映射为 GLM，默认 GLM-4.7（页内 CC 2.1.140 验证） | src: https://docs.bigmodel.cn/cn/guide/develop/claude | quote: "默认为服务端模型映射，即您界面上看到的是 Claude 模型但实际是 GLM 模型。…`ANTHROPIC_DEFAULT_OPUS_MODEL`：`GLM-4.7`" | type: official
- [C2] 【超时】同页推荐 API_TIMEOUT_MS=3000000 | src: https://docs.bigmodel.cn/cn/guide/develop/claude | quote: 「"API_TIMEOUT_MS": "3000000"」 | type: official
- [C3] 【模型映射】Z.ai：默认 GLM-5.3-Flash，推荐 Opus=glm-5.3[1m]（页内 CC 2.0.14 验证） | src: https://docs.z.ai/devpack/tool/claude | quote: 「default configuration as follows: `ANTHROPIC_DEFAULT_OPUS_MODEL: GLM-5.3-Flash` … "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.3[1m]"」 | type: official
- [C4] 【思考/effort】Coding Plan 读取 thinking.type、output_config.effort；关闭思考转 low | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "Claude Code 使用 `thinking.type`、`output_config.effort`；…关闭思考配置会转换为 low，不会切换到其他模型。" | type: official
- [C5] 【图片】服务端内置 image_analysis | src: https://docs.bigmodel.cn/cn/coding-plan/mcp/vision-mcp-server | quote: "在 Claude Code 中使用 GLM Coding Plan 时，模型服务端已内置 `image_analysis` 工具…无需安装。" | type: official
- [C6] 【服务端工具】同前提下内置联网搜索 | src: https://docs.bigmodel.cn/cn/coding-plan/mcp/search-mcp-server | quote: "模型服务端已内置联网搜索 MCP，无需安装。" | type: official
- [C7] 【beta 头/工具】2026-07-22 报告（api.z.ai，glm-5.2）：带 advanced-tool-use-2025-11-20 beta 时，无 defer_loading 的工具也被延迟 | src: https://github.com/zai-org/feedback/issues/172 | quote: "Tools sent without `defer_loading` are deferred anyway." | type: secondary
- [C8] 【校验/错误】2026-05-29 报告（open.bigmodel.cn）：messages[] 含 role:"system" 即 422，错误体为 {"detail":[…]}，非 Anthropic envelope | src: https://github.com/zai-org/GLM-5/issues/74 | quote: 「422 {"detail":[{"type":"literal_error", … "msg":"Input should be 'user' or 'assistant'"」 | type: secondary
- [C9] 【校验】zai-org CONTRIBUTOR 2026-06-09 回复：有意为之 | src: https://github.com/zai-org/GLM-5/issues/74 | quote: "This is expected behavior to mitigate prompt injection attacks." | type: secondary
- [C10] 【错误】2026-09-09 报告（api.z.ai，glm-5.3）：tool pattern 含 \p{…} 即 400；错误体为 Anthropic 形状另带 code | src: https://github.com/zai-org/feedback/issues/593 | quote: 「{"type":"error","error":{"type":"invalid_request_error","code":"1210",」 | type: secondary
- [C11] 【服务端工具】2026-09-14 实测（api.z.ai，glm-5.3）：粘贴图片后端点返回自有 server_tool_use，id 为 call_ 前缀 | src: https://github.com/betmoar/cc-proxy-plugin/issues/67 | quote: 「"type": "server_tool_use", "id": "call_d88edcb2ba6d4d789afd7a0e", "name": "analyze_image"」 | type: secondary
- [C12] 【流式】2026-09-01 报告（api.z.ai，glm-5.3）：message_start.usage 恒为 0 | src: https://github.com/zai-org/GLM-5/issues/139 | quote: 「`message_start` event whose `usage` block is always `{"input_tokens": 0, "output_tokens": 0}`」 | type: secondary
- [C13] 【usage】同报告：真实计数在末尾 message_delta，带 server_tool_use、service_tier | src: https://github.com/zai-org/GLM-5/issues/139 | quote: 「final `message_delta`: `"usage":{"input_tokens":14,"output_tokens":32,"cache_read_input_tokens":0,"server_tool_use":{"web_search_requests":0},"service_tier":"standard"}`」 | type: secondary
- [C14] 【缓存】2026-08-29 报告（open.bigmodel.cn，glm-5.3-flash）：隐式缓存，无 cache_control 也命中；cache_creation 从不返回 | src: https://github.com/zai-org/feedback/issues/411 | quote: "无 `cache_control` 的完全相同请求也可隐式命中；`cache_creation_input_tokens` 从未返回过值（恒缺席/0）" | type: secondary
- [C15] 【缓存】同报告另列三项异常 | src: https://github.com/zai-org/feedback/issues/411 | quote: "append-only 紧邻轮无法命中上一轮前缀、cache_read 标签与实际耗时脱钩、system 前缀零缓存" | type: secondary
- [C16] 【count_tokens】2026-08-14 PR：Z.ai count_tokens 对 glm-5.3 返回 0 | src: https://github.com/kolega-ai/kolega-code/pull/613 | quote: "Z.AI's Anthropic-compatible `/v1/messages/count_tokens` endpoint returns `input_tokens: 0` for `glm-5.3`" | type: secondary
- [C17] 【图片】2026-09-16 PR（glm-5.3-flash）：Z.ai 拒绝 URL 来源的图片块 | src: https://github.com/vybestack/llxprt-code/pull/3704 | quote: "rejects two classes of image input with 400 [1210][图片输入格式/解析错误] … every source:{type:'url'} image block." | type: secondary

## conflicts
- ZP×D6 thinking.type=disabled：A https://docs.bigmodel.cn/cn/guide/capabilities/thinking "注：GLM-5.3 GLM-5.3-FLASH 不再支持关闭思考（API 请求中 thinking.type 传 disabled 将会报错），请确保开启思考。"（示例都走 /api/paas/v4/chat/completions；同页 effort 规则分"在 API 请求中"和"在 Coding Plan 请求中"两套）。B https://docs.bigmodel.cn/cn/coding-plan/latest-model "thinking.type 为 false、disabled、none、off | low | 继续请求；仍会轻量思考"（"在 Claude Code 中切换"节；前置条件"Claude Code / Goose（Anthropic 兼容）：https://open.bigmodel.cn/api/anthropic"）。语境（不裁决）：按标准 API 与 Coding Plan 通道划分，不按协议划分；按量 key 调 /api/anthropic 适用哪条没写。Z.ai 两页同构。
- 版本漂移：https://docs.bigmodel.cn/cn/guide/develop/claude 写"使用最新 GLM-5.2 模型"，https://docs.bigmodel.cn/cn/coding-plan/latest-model 写"支持最新的 GLM-5.3 和 GLM-5.3-Flash 模型"。均无更新日期。

## gaps
- 官方仍没有字段级说明（version/beta 头、stop_sequences/top_k/metadata、tool_choice、budget_tokens、document、count_tokens、流式事件、错误格式）；D3 采样参数、tool_choice 连二手报告也没有。
- 鉴权：二手复现里 x-api-key（#139）和 Bearer（#74、#593）都出现，官方没写。
- Z.ai MCP 页无"服务端已内置"一句，仅 C11、C13 旁证。
- 按量 key 走 /api/anthropic 的映射、内置工具、思考处理：没写。
- zai-org README、HF 卡无 Anthropic 兼容说明。

## leads
- feedback#387：schema 含 $ref 时报 "Network error 1234"；HyperNeo PR#2185：open.bigmodel.cn 返回 200 加错误体、流中 event: error。
- reader-mcp-server 页同写内置网页读取；docs.bigmodel.cn/cn/guide/capabilities/cache 可核 D9。
