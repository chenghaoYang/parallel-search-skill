# r2-zhipu-anthropic
question: 智谱 /api/anthropic 相对 Anthropic 官方 Messages 的官方原句证实差异？智谱 Responses（/api/v1）相对 OpenAI Responses 完整差异清单？
checked: https://docs.bigmodel.cn/llms.txt, https://docs.z.ai/llms.txt, https://docs.bigmodel.cn/cn/coding-plan/faq, https://docs.bigmodel.cn/cn/coding-plan/mcp/search-mcp-server, https://docs.bigmodel.cn/cn/coding-plan/mcp/vision-mcp-server, https://docs.bigmodel.cn/cn/guide/develop/claude/introduction, https://docs.bigmodel.cn/cn/guide/develop/claude, https://docs.bigmodel.cn/cn/faq/api-code.md, https://docs.z.ai/api-reference/api-code.md, https://docs.bigmodel.cn/api-reference/response/创建-response.md, https://docs.bigmodel.cn/cn/coding-plan/quick-start, https://docs.z.ai/devpack/quick-start, https://github.com/zai-org/zai-coding-plugins/issues/12

## claims
### /api/anthropic
- [C1] 联网搜索由服务端内置「联网搜索 MCP」提供，非文档声称实现 Anthropic 原生 web_search 工具类型 | src: https://docs.bigmodel.cn/cn/coding-plan/mcp/search-mcp-server | quote: "在 Claude Code 中使用 GLM Coding Plan 时，模型服务端已内置联网搜索 MCP，无需安装。" | type: official
- [C2] 图片理解由服务端内置 `image_analysis` 工具提供；完整视觉工具集（8个具名工具）需另装视觉理解 MCP | src: https://docs.bigmodel.cn/cn/coding-plan/mcp/vision-mcp-server | quote: "模型服务端已内置 `image_analysis` 工具，具备图片理解能力，无需安装。" | type: official
- [C3] Claude Code `/effort` 6档在 GLM-5.2 后端只有2个实际生效值 | src: https://docs.bigmodel.cn/cn/guide/develop/claude | quote: "low, medium, high（默认值） | high；xhigh, max, ultracode | max" | type: official
- [C4] 官方命名该协议为「Anthropic Message 协议」(单数)，z.ai 用独立域名 | src: https://docs.bigmodel.cn/cn/coding-plan/quick-start | quote: "Anthropic Message 协议 | `https://open.bigmodel.cn/api/anthropic`" | type: official
- [C5] z.ai 英文命名「Anthropic Messages」，base URL 为 api.z.ai 而非 bigmodel.cn 域名 | src: https://docs.z.ai/devpack/quick-start | quote: "Anthropic Messages | `https://api.z.ai/api/anthropic`" | type: official
- [C6] 智谱/z.ai 通用错误体为 {"error":{"code":"数字","message"}}，与 Anthropic 官方 error.type 形状不同；两域名措辞一致，未注明专指 /api/anthropic | src: https://docs.bigmodel.cn/cn/faq/api-code.md | quote: "{\"error\":{\"code\":\"1001\",\"message\":\"Header 中未收到 Authentication 参数，无法进行身份验证\"}}" | type: official
- [C7]（secondary）zai-org 官方仓库issue：Anthropic兼容端点tokenizer与官方差异大，JSON多算43–49%、特殊字符多算143–149%；2026-04-15提交，0回复无官方确认 | src: https://github.com/zai-org/zai-coding-plugins/issues/12 | quote: "significant tokenization differences from Anthropic's tokenizer, causing Claude Code to hit context limits at ~80% reported usage" | type: secondary
- [C8] Claude 兼容介绍页仅给笼统差异提示，无字段级说明，链接指向 Anthropic 官方文档而非自建 schema | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "某些场景下智谱与 Claude 接口仍存在差异，但不影响整体兼容性。" | type: official

### 智谱 Responses（/api/v1）
- [C9] tool_choice 仅 none/auto 两枚举值，无 required、无强制指定具体工具 | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "`none` 不调用任何工具；`auto` 由模型判断。" | type: official
- [C10] reasoning.effort 表面 7 档，官方写明多档被合并：none/minimal 放弃思考，low/medium 映射 high，xhigh 映射 max，默认 max | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "默认 `max`。`none` / `minimal` 放弃思考；`low` / `medium` 映射为 `high`；`xhigh` 映射为 `max`。" | type: official
- [C11] tools 支持 function/namespace/custom/web_search 四类型；namespace（函数工具组）为 Zhipu 专有类型 | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "工具类型，此处为 `namespace`。" | type: official
- [C12] temperature 限定 [0.0,1.0]（两位小数），GLM-5.3 默认 1.0 | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "采样温度 `[0.0, 1.0]`，限两位小数。GLM-5.3 默认 `1.0`。" | type: official
- [C13] top_p 范围 [0.01,1.0]（两位小数），默认 0.95 | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "核采样 `[0.01, 1.0]`，限两位小数。GLM-5.3 默认 `0.95`。" | type: official
- [C14] max_output_tokens 上限 131072、默认 65536，明确含思维链 token | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "模型输出最大 tokens（含回答与思维链）。最大 `131072`，默认 `65536`。" | type: official
- [C15] store 默认 false，true 时才可查询/删除/用于多轮（完整字段 schema 独立确认 R1 结论） | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "是否保存本次响应，默认 `false`。为 `true` 时可用于查询、删除和多轮。" | type: official
- [C16] previous_response_id 要求 store=true，且有效期仅 7 天 | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "上一轮 `id`，用于多轮。须 `store=true`，有效期 7 天。" | type: official
- [C17] 流式响应结束不发 data:[DONE]（完整字段 schema 独立确认 R1 已知结论） | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "`stream=true` 时返回 SSE 事件流，不发送 `data: [DONE]`。" | type: official
- [C18] Response API 错误 code 为字符串，且与对话补全接口的数字业务码是两套独立体系 | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "Response API 错误。`error.code` 为字符串，与对话补全的数字业务码不是同一套。" | type: official
- [C19] 错误码表之一 not_implemented 明确指「接口或能力未实现」 | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "`not_implemented` | 接口或能力未实现" | type: official
- [C20] 推理内容是独立输出项类型 `reasoning`，流式阶段有专属 reasoning_text.delta/.done 事件，与回答文本增量事件分开 | src: https://docs.bigmodel.cn/api-reference/response/创建-response.md | quote: "输出类型，此处为 `reasoning`。" | type: official
- [C21] 两域名 llms.txt 均无 /api/anthropic 独立 OpenAPI 页；唯一有完整 schema 的是 Response API | src: https://docs.bigmodel.cn/llms.txt | quote: "创建 Response ... 点击 **Try it** 可试用。" | type: official

## conflicts
（无）
## gaps
- 未找到 /api/anthropic 独立 messages 字段 schema／API 参考页（两域名 llms.txt 全文索引，仅教程式介绍页，无参数表）。
- 未找到官方页面写「web_search/图片base64 block 本身不被支持」——只查到「服务端已内置替代工具」（C1/C2），不能证明原生字段被拒绝。
- count_tokens、anthropic-beta、cache_control、stop_sequences、top_k、metadata、stop_reason 七字段全文搜索未出现，应判 ∅。
- 错误码页标题为通用「智谱开放平台 API」，未特指 /api/anthropic，不能确认即代理实际返回 shape。

## leads
- GitHub issue zai-org/zai-coding-plugins#12（token 偏差43–249%）值得追踪，若官方回复可坐实 count_tokens 不兼容。
- reasoning.effort（Responses端7→2档）与 /effort（6→2档）双重折叠指向同一后端限制，可合并引用 C3+C10。
- docs.bigmodel.cn/api-reference 下「查询/删除 Response」子页本轮未抓取，可核实 R1「未提供cancel」出处。
