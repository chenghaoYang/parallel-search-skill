# r3-zhipu-coding
question: 智谱 GLM Coding Plan 的 /api/v1（Responses 面）与 /api/coding/paas/v4（OpenAI 面）两个入口的官方事实。
checked: https://docs.bigmodel.cn/cn/coding-plan/quick-start, https://docs.z.ai/devpack/quick-start, https://docs.bigmodel.cn/llms.txt, https://docs.z.ai/llms.txt, https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md, https://docs.bigmodel.cn/cn/coding-plan/usage-notes.md, https://docs.bigmodel.cn/cn/coding-plan/faq.md, https://docs.bigmodel.cn/cn/coding-plan/tool/others.md, https://docs.bigmodel.cn/cn/coding-plan/tool/codex.md

## claims
- [C1] Coding Plan 端点表三行：Anthropic Message 协议=https://open.bigmodel.cn/api/anthropic、OpenAI Chat Completion 协议=https://open.bigmodel.cn/api/coding/paas/v4、OpenAI Response 协议=https://open.bigmodel.cn/api/v1 | src: https://docs.bigmodel.cn/cn/coding-plan/quick-start | quote: "Anthropic Message 协议 https://open.bigmodel.cn/api/anthropic OpenAI Chat Completion 协议 https://open.bigmodel.cn/api/coding/paas/v4 OpenAI Response 协议 https://open.bigmodel.cn/api/v1" | type: official
- [C2] Coding Plan 仅限指定工具使用（quick-start 第4步原话） | src: https://docs.bigmodel.cn/cn/coding-plan/quick-start | quote: "GLM Coding Plan 仅限在官方支持的指定工具与产品环境中使用" | type: official
- [C3] 国际站同构三入口，base 换 api.z.ai：Anthropic Messages=/api/anthropic、OpenAI Chat Completions=/api/coding/paas/v4、OpenAI Responses=/api/v1 | src: https://docs.z.ai/devpack/quick-start | quote: "Anthropic Messages https://api.z.ai/api/anthropic OpenAI Chat Completions https://api.z.ai/api/coding/paas/v4 OpenAI Responses https://api.z.ai/api/v1" | type: official
- [C4] /api/v1 基址与对话补全基址明确二分，客户端超时 7200 秒 | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md | quote: "Response API 的基址是 `https://open.bigmodel.cn/api/v1`，不是对话补全使用的 `https://open.bigmodel.cn/api/paas/v4`。请求超时为 7200 秒。" | type: official
- [C5] 接口一览共 4 条路径：POST /responses、GET /responses/{response_id}、GET /responses/{response_id}/input_items、DELETE /responses/{response_id}，Base URL https://open.bigmodel.cn/api/v1 | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md | quote: "Base URL：`https://open.bigmodel.cn/api/v1`" | type: official
- [C6] /api/v1 认证为 Authorization: Bearer + API Key | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md | quote: "curl https://open.bigmodel.cn/api/v1/responses \ --header \"Authorization: Bearer YOUR_API_KEY\"" | type: official
- [C7] 与 OpenAI Responses 的三点官方差异：store 默认 false、流式不发 data: [DONE]、无 cancel | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md | quote: "智谱 Response API 与 OpenAI Responses 在部分字段上仍有差异：默认 `store=false`、流式结束不发送 `data: [DONE]`、当前未提供 cancel。" | type: official
- [C8] 流式终止以四种终止事件为准 | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md | quote: "结束以 `response.completed` / `failed` / `incomplete` / `error` 为准，**不发送** `data: [DONE]`。" | type: official
- [C9] max_output_tokens 默认 65536、上限 131072（含思维链） | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md | quote: "max_output_tokens | integer | 65536 | 最大输出 tokens（含思维链），上限 131072" | type: official
- [C10] store 默认 false 不落库；多轮用 previous_response_id，响应 id 有效期 7 天（参数表） | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md | quote: "默认 `store=false`，响应不会落库。需要查询或续写时，创建时设置 `store=true`，下一轮传入 `previous_response_id`。" | type: official
- [C11] reasoning.effort 默认 max；none/minimal 放弃思考，low/medium→high，xhigh→max | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md | quote: "`effort` 默认 `max`。传入 `none` / `minimal` 会放弃思考；`low` / `medium` 映射为 `high`；`xhigh` 映射为 `max`。" | type: official
- [C12] tool_choice 仅 none/auto；tools 支持 function/namespace/custom/web_search（服务端执行） | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md | quote: "`tool_choice` 为 `none` 或 `auto`。另支持 `namespace`、`custom` 和由服务端执行的 `web_search`。" | type: official
- [C13] text.format.type 仅 text 或 json_object（参数表） | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md | quote: "text.format.type | string | text | `text` 或 `json_object`" | type: official
- [C14] 要求 OpenAI SDK ≥1.0.0（需支持 responses）、Python ≥3.7.1 | src: https://docs.bigmodel.cn/cn/guide/develop/responses/introduction.md | quote: "OpenAI SDK 版本不低于 1.0.0（需支持 `responses`）" | type: official
- [C15] Codex 页称 /api/v1 为「OpenAI Response 协议端点」，config.toml 要求 wire_api="responses"、base_url=/api/v1、experimental_bearer_token 填 Coding Key | src: https://docs.bigmodel.cn/cn/coding-plan/tool/codex.md | quote: "Codex 需要配置专属的 OpenAI Response 协议端点 `https://open.bigmodel.cn/api/v1`。" | type: official
- [C16] Codex models.json 声明 glm-5.3（context_window 1048576）与 glm-5-turbo（204800），均 supported_in_api | src: https://docs.bigmodel.cn/cn/coding-plan/tool/codex.md | quote: "\"context_window\": 1048576," | type: official
- [C17] Coding Key 发放：个人版在 个人编程套餐>套餐概览 新建；团队 Key 与平台其他 API Key 不通用 | src: https://docs.bigmodel.cn/cn/coding-plan/quick-start | quote: "团队套餐 Key 与平台其他 API Key 不通用，使用团队额度请务必使用团队套餐 Key" | type: official
- [C18] 套餐支持模型：所有套餐均支持 GLM-5.3、GLM-5.3-Flash | src: https://docs.bigmodel.cn/cn/coding-plan/faq.md | quote: "所有套餐均支持 `GLM-5.3`、`GLM-5.3-Flash`。" | type: official
- [C19] 套餐额度机制=每 5 小时限额+每周限额 | src: https://docs.bigmodel.cn/cn/coding-plan/faq.md | quote: "套餐采用 **每 5 小时限额 + 每周限额** 的使用机制" | type: official
- [C20] 非指定工具调用不可用套餐额度，自建应用走标准 API 按协议计费 | src: https://docs.bigmodel.cn/cn/coding-plan/faq.md | quote: "在除规定工具外调用 API，不可享用 Coding 套餐的额度。" | type: official
- [C21] 报 1113 多因 Base URL 未按工具区分：Claude Code→/api/anthropic、Cherry Studio→/api/coding/paas/v4/（带尾斜杠）、其他工具→/api/coding/paas/v4 | src: https://docs.bigmodel.cn/cn/coding-plan/faq.md | quote: "Cherry studio 配置的 Base URL 是：`https://open.bigmodel.cn/api/coding/paas/v4/` 。" | type: official
- [C22] 套餐过期后用资源包须改回标准基址 /api/paas/v4；官方称套餐权益高于资源包 | src: https://docs.bigmodel.cn/cn/coding-plan/faq.md | quote: "在其他编码工具中，请将 Base URL 设置为：`https://open.bigmodel.cn/api/paas/v4` ，即可使用资源包进行调用" | type: official
- [C23] 指定工具=18 个 Coding Agent 工具+5 个通用 Agent 工具（AutoClaw/WorkBuddy/OpenClaw/Cherry Studio/Hermes）；通用工具次级调度 | src: https://docs.bigmodel.cn/cn/coding-plan/tool/others.md | quote: "对于以下所支持的通用 Agent 工具，采用次级调度与尽力交付策略，Coding Agent 任务享有资源抢占优先权" | type: official
- [C24] 并发限制随套餐等级，原则 Max > Pro > Lite，低峰动态提升 | src: https://docs.bigmodel.cn/cn/coding-plan/usage-notes.md | quote: "速率（并发数）限制与您的套餐等级相关，平台会根据资源进行动态调整，基本原则 **Max > Pro > Lite**" | type: official
- [C25] Cline（OpenAI Compatible）示例：模型 glm-5.2 上下文窗口填 1000000，其它模型 200000 | src: https://docs.bigmodel.cn/cn/coding-plan/tool/others.md | quote: "调整 Context Window Size：根据您使用的模型调整（`glm-5.2` 为 `1000000`，其它模型为 `200000`）" | type: official

## conflicts
- 尾斜杠：FAQ 对 Cherry Studio 给 `https://open.bigmodel.cn/api/coding/paas/v4/`（C21），quick-start 与 tool/others 端点表给无尾斜杠 `.../v4`（C1）。裁决：非实质冲突——同页 FAQ 其余工具均无尾斜杠，且两页端点表逐字一致，属个别工具的书写差异，端点本体相同。
- quick-start 称"支持 Anthropic 协议和 OpenAI 协议两种接入方式"却列三个 Base URL。裁决：非冲突——OpenAI 协议族下分 Chat Completion 与 Response 两个面；佐证：Codex 页称 /api/v1 为"OpenAI Response 协议端点"（C15），z.ai 版表格同样三行（C3）。

## gaps
- /api/coding/paas/v4 与 /api/paas/v4 的差异官方只写计费/权益（C20/C22），两端点模型集合与限额数值差异无对比说明（查 FAQ、quick-start、tool/others、usage-notes）。
- /api/v1 的完整流式事件清单与错误码未取证（未打开 api-reference/response/创建-response）。
- coding Key 能否调用通用 /api/paas/v4、普通 Key 能否调用 /api/coding/paas/v4：无文档。
- 所查页面均无更新日期/版本号；仅 llms.txt 提及 2026-07-30 套餐改版通知页。

## leads
- /api/v1 基址两用：既在通用 Response API 指南（develop/responses）也在 Coding Plan 端点表；z.ai 国际站同构（api.z.ai/api/v1）。计费归属取决于 Key 与工具，无 coding 专用 responses 域。
- 2026-07-30 套餐改版通知（docs.bigmodel.cn/cn/coding-plan/notice/usage-revision.md）影响额度表述时效，终审可核。
- Codex models.json 出现 glm-5-turbo（204800 上下文），主线模型页未见过该编码，值得留意。
