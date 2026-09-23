# r2-zhipu-messages
question: 智谱官方有没有 Anthropic Messages 兼容端点（/api/anthropic/v1/messages）的字段表？有的话，header、system、content block、tools、stream 事件、stop_reason、max_tokens 的原名是什么；没有的话，用新页面证明「官方没写」。
checked: https://docs.bigmodel.cn/sitemap.xml, https://docs.bigmodel.cn/llms.txt, https://docs.bigmodel.cn/llms-full.txt, https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3, https://docs.bigmodel.cn/cn/guide/models/text/glm-5.2, https://docs.bigmodel.cn/cn/coding-plan/tool/others, https://docs.bigmodel.cn/cn/guide/develop/others, https://docs.bigmodel.cn/cn/guide/develop/http/introduction, https://docs.bigmodel.cn/cn/coding-plan/quick-start, https://docs.bigmodel.cn/cn/coding-plan/faq, https://docs.bigmodel.cn/cn/coding-plan/latest-model, https://docs.bigmodel.cn/cn/coding-plan/usage-notes, https://docs.bigmodel.cn/cn/guide/develop/droid, https://docs.bigmodel.cn/cn/coding-plan/tool/goose, https://docs.bigmodel.cn/cn/coding-plan/tool/claude-for-ide, https://docs.bigmodel.cn/cn/coding-plan/tool/opencode, https://docs.bigmodel.cn/cn/coding-plan/tool/crush, https://docs.bigmodel.cn/cn/coding-plan/tool/roo, https://docs.bigmodel.cn/cn/coding-plan/tool/kilo, https://docs.bigmodel.cn/cn/coding-plan/tool/pi, https://docs.bigmodel.cn/cn/coding-plan/tool/openclaw, https://docs.bigmodel.cn/cn/coding-plan/tool/cursor, https://docs.bigmodel.cn/cn/faq/api-code, https://docs.bigmodel.cn/cn/faq/api-issues, https://docs.bigmodel.cn/cn/guide/capabilities/streaming, https://docs.bigmodel.cn/cn/guide/start/concept-param, https://docs.bigmodel.cn/cn/guide/start/migrate-to-glm-new, https://docs.bigmodel.cn/cn/update/new-releases, https://docs.bigmodel.cn/en/guide/develop/claude/introduction, https://docs.bigmodel.cn/api-reference/模型-api/anthropic, https://docs.bigmodel.cn/cn/guide/develop/claude/messages

## claims
- [C1] sitemap 共 236 条；含 claude 的只有兼容介绍（lastmod 2026-09-23），没有 Messages 字段页。 | src: https://docs.bigmodel.cn/sitemap.xml | quote: "<loc>https://docs.bigmodel.cn/cn/guide/develop/claude/introduction</loc>" | type: official
- [C2] llms.txt 只挂「Claude API 兼容」到 introduction.md。 | src: https://docs.bigmodel.cn/llms.txt | quote: "- [Claude API 兼容](https://docs.bigmodel.cn/cn/guide/develop/claude/introduction.md)" | type: official
- [C3] GLM-5.3 协议名是 Anthropic Message 协议，Base URL 无路径 /v1/messages，无字段表。 | src: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3 | quote: "Anthropic Message 协议" | type: official
- [C4] 该页接口文档链到对话补全。 | src: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3 | quote: "了解如何调用 API" | type: official
- [C5] 订过 Coding Plan 时，「模型 API」暂时只能走 Chat Completion。 | src: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3 | quote: "暂时您只能通过 OpenAI Chat Completion 协议调用模型 API" | type: official
- [C6] 快速开始只给协议与 Base URL。 | src: https://docs.bigmodel.cn/cn/coding-plan/quick-start | quote: "Anthropic Message 协议" | type: official
- [C7] FAQ 只规定 Claude Code 的 Base URL。 | src: https://docs.bigmodel.cn/cn/coding-plan/faq | quote: "Claude Code 中 Base URL 是：`https://open.bigmodel.cn/api/anthropic` 。" | type: official
- [C8] Claude Code / Goose 被标为 Anthropic 兼容，仍只有 base URL。 | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "Claude Code / Goose（**Anthropic 兼容**）" | type: official
- [C9] Claude Code 侧原名是 thinking.type、output_config.effort；同表还有 reasoning_effort。取值：thinking.type 为 true、enabled、adaptive、false、disabled、none、off；reasoning_effort 为 minimal、light、low、medium、high、xhigh、max、ultra。不是 system/tools/stop_reason。 | src: https://docs.bigmodel.cn/cn/coding-plan/latest-model | quote: "Claude Code 使用 `thinking.type`、`output_config.effort`；Codex 使用 `reasoning.effort`。" | type: official
- [C10] Goose 的 Anthropic 配置项只有 Base URL、API Key、Model。 | src: https://docs.bigmodel.cn/cn/coding-plan/tool/goose | quote: "Base URL: 输入 API 地址 `https://open.bigmodel.cn/api/anthropic` 。" | type: official
- [C11] Droid Anthropic 配置是客户端 settings 原名 displayName、model、baseUrl、apiKey、provider、maxOutputTokens；provider 值为 anthropic。不是 Messages body。 | src: https://docs.bigmodel.cn/cn/coding-plan/tool/droid | quote: "maxOutputTokens" | type: official
- [C12] 流式页事件原名是 Chat SSE：stream、choices[0].delta.content、choices[0].delta.reasoning_content、choices[0].finish_reason、usage。示例主机路径是 /api/paas/v4/chat/completions。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/streaming | quote: "`choices[0].finish_reason`: 完成原因（仅在最后一个chunk中出现）" | type: official
- [C13] 错误码页流式异常原名 finish_reason；1001 文案是 Authentication。未点名 /api/anthropic。 | src: https://docs.bigmodel.cn/cn/faq/api-code | quote: "而是在响应体的 `finish_reason` 参数中返回异常原因" | type: official
- [C14] 核心参数表有 max_tokens、stream、thinking、reasoning_effort，与 do_sample 同表，全文无 /api/anthropic。glm-5.3：默认 max_tokens 65536，最大 131072。 | src: https://docs.bigmodel.cn/cn/guide/start/concept-param | quote: "限制单次调用生成的最大 token 数。" | type: official
- [C15] 通用 HTTP 头原名是 Content-Type 与 Authorization: Bearer，端点是 /api/paas/v4/。 | src: https://docs.bigmodel.cn/cn/guide/develop/http/introduction | quote: "Authorization: Bearer YOUR_API_KEY" | type: official
- [C16] 迁移清单原名属于 Chat：tool_stream、delta.tool_calls、delta.reasoning_content、delta.content、max_tokens；调用是 client.chat.completions.create。 | src: https://docs.bigmodel.cn/cn/guide/start/migrate-to-glm-new | quote: "支持工具调用过程的流式输出（`tool_stream=true`）" | type: official
- [C17] 英文 Claude 介绍页不存在。 | src: https://docs.bigmodel.cn/en/guide/develop/claude/introduction | quote: "The requested page could not be found." | type: official

## conflicts
- 模型 API 与 Coding 工具对 Anthropic 是否可用打架，未裁决。A（GLM-5.3「模型 API」）: "暂时您只能通过 OpenAI Chat Completion 协议调用模型 API" https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3 ；B（切换模型）: "Claude Code / Goose（**Anthropic 兼容**）" 且地址为 https://open.bigmodel.cn/api/anthropic https://docs.bigmodel.cn/cn/coding-plan/latest-model
- 接入表不一致，与 Messages 字段无关。https://docs.bigmodel.cn/cn/guide/develop/others 只有 Anthropic Message 与 `https://open.bigmodel.cn/api/coding/paas/v4`；https://docs.bigmodel.cn/cn/coding-plan/tool/others 另有 "OpenAI Response 协议" 与 `https://open.bigmodel.cn/api/v1`。

## gaps
- 官方未发布 Messages 字段表。D2 header、D3 system、D4 content block、D5 tools、D6 stream 事件、D7 stop_reason、D8 max_tokens、D9 都没有 Messages 原名。
- llms-full.txt 236 篇无 stop_reason、anthropic-version、anthropic-beta、content_block_start。x-api-key 与 /v1/messages 只在上轮 introduction，不重写 D1/D10。
- 无字段表的新页：glm-5.3、glm-5.2、coding-plan/tool/others、guide/develop/others、http/introduction、coding-plan/quick-start、coding-plan/faq、coding-plan/latest-model、coding-plan/usage-notes、guide/develop/droid、tool/goose、tool/claude-for-ide、tool/opencode、tool/crush、tool/roo、tool/kilo、tool/pi、tool/openclaw、tool/cursor、faq/api-code、faq/api-issues、capabilities/streaming、concept-param、migrate-to-glm-new、update/new-releases、sitemap.xml、llms.txt、llms-full.txt。域名均为 https://docs.bigmodel.cn/ 。
- HTTP 404：/en/guide/develop/claude/introduction 、/api-reference/模型-api/anthropic 、/cn/guide/develop/claude/messages 、/docs.json 。
- 禁止填进 D2–D9：Authorization、Authentication、maxOutputTokens、choices[0].finish_reason、tool_stream、delta.tool_calls、核心参数表的 max_tokens（未绑定 Messages）。

## leads
- 缓存页示例 prompt 内嵌「知识库」写了 Bearer 与 finish_reason，不是字段表：https://docs.bigmodel.cn/cn/guide/capabilities/cache
- managed-agents 的 user.custom_tool_result / agent.tool_use 不是 Messages content block。
- maxOutputTokens 131072 与概念页最大 max_tokens 131072 同数不同名。
