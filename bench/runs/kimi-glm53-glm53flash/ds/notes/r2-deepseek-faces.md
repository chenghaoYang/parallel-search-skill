# r2-deepseek-faces
question: DeepSeek 的 /anthropic 兼容面官方事实，及 /responses 支持模型范围、strict 是否须 /beta 两处冲突的裁决。
checked: https://api-docs.deepseek.com/guides/anthropic_api/, https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/, https://api-docs.deepseek.com/guides/responses_api/, https://api-docs.deepseek.com/quick_start/pricing/, https://api-docs.deepseek.com/api/create-chat-completion/, https://api-docs.deepseek.com/guides/tool_calls/, https://api-docs.deepseek.com/updates, https://api-docs.deepseek.com/

## claims
- [C1] 官方 Anthropic 指南为 guides/anthropic_api「Using the Anthropic API」，base_url=https://api.deepseek.com/anthropic | src: https://api-docs.deepseek.com/guides/anthropic_api/ | quote: "our API has added support for the Anthropic API format, with the base_url being https://api.deepseek.com/anthropic." | type: official
- [C2] pricing 页：BASE URL (Anthropic Format)=https://api.deepseek.com/anthropic，Anthropic API 两模型均 ✓✓ | src: https://api-docs.deepseek.com/quick_start/pricing/ | quote: "BASE URL (Anthropic Format)https://api.deepseek.com/anthropic"（同表功能行 "Anthropic API✓✓"） | type: official
- [C3] 鉴权：x-api-key 完全支持；anthropic-version 忽略 | src: https://api-docs.deepseek.com/guides/anthropic_api/ | quote: "anthropic-versionIgnoredx-api-keyFully Supported" | type: official
- [C4] anthropic-beta 对 /messages 忽略；Files API 端点须值 files-api-2025-04-14 | src: https://api-docs.deepseek.com/guides/anthropic_api/ | quote: "Ignored for /messages; required (files-api-2025-04-14) for Files API endpoints" | type: official
- [C5] Claude Code 官方接入页：ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic + ANTHROPIC_AUTH_TOKEN=<DeepSeek key> | src: https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/ | quote: "simply configure the following environment variables to point to the DeepSeek Anthropic API" | type: official
- [C6] 模型映射：claude-opus*→deepseek-v4-pro，按 V4 Pro 价计费 | src: https://api-docs.deepseek.com/guides/anthropic_api/ | quote: "The claude-opus mapping points to deepseek-v4-pro, which is billed at the V4 Pro price." | type: official
- [C7] claude-haiku*/claude-sonnet*→deepseek-flash；未知名自动映射 deepseek-flash | src: https://api-docs.deepseek.com/guides/anthropic_api/ | quote: "Models starting with claude-haiku or claude-sonnet are mapped to deepseek-flash" | type: official
- [C8] thinking 支持（budget_tokens 忽略）；output_config 仅 effort；top_k 忽略 | src: https://api-docs.deepseek.com/guides/anthropic_api/ | quote: "thinkingSupported (budget_tokens is ignored)output_configOnly effort is supportedtop_kIgnored" | type: official
- [C9] temperature 全支持（0.0–2.0）；top_p 仅 thinking 生效（下限 0.95，非 thinking 固定 1.0） | src: https://api-docs.deepseek.com/guides/anthropic_api/ | quote: "top_pOnly takes effect in thinking mode (with a lower bound of 0.95); in non-thinking mode it is fixed at 1.0" | type: official
- [C10] tools 子字段 name/input_schema/description 全支持、cache_control 忽略；tool_choice none/auto/any/tool 均支持（disable_parallel_tool_use 忽略） | src: https://api-docs.deepseek.com/guides/anthropic_api/ | quote: "autoSupported (disable_parallel_tool_use is ignored)" | type: official
- [C11] 消息块支持：text、image（source.type=base64[jpeg/png/gif/webp]/url/file）、thinking、tool_use、tool_result、server_tool_use、web_search_tool_result | src: https://api-docs.deepseek.com/guides/anthropic_api/ | quote: "Supported. source.type can be base64 (media types: jpeg, png, gif, webp), url, or file" | type: official
- [C12] 消息块不支持：document、search_result、redacted_thinking、code_execution_tool_result、mcp_tool_use、mcp_tool_result、container_upload | src: https://api-docs.deepseek.com/guides/anthropic_api/ | quote: "array, type = \"document\"  Not Supported"（同表后续各行同标 Not Supported） | type: official
- [C13] 冲突①A：pricing 功能表 Responses API 两列均 ✓ | src: https://api-docs.deepseek.com/quick_start/pricing/ | quote: "Responses API✓✓Anthropic API✓✓" | type: official
- [C14] 冲突①B：responses 指南 model 行只列 flash 并转引 pricing | src: https://api-docs.deepseek.com/guides/responses_api/ | quote: "modelSupported. deepseek-flash, see Models & Pricing" | type: official
- [C15] updates 2026-08-13（V4-Pro GA 条目）：原生支持 Responses API；2026-07-31 条目：V4-Flash 原生支持 | src: https://api-docs.deepseek.com/updates | quote: "The DeepSeek API now natively supports the OpenAI Responses API format and is specifically adapted for Codex." | type: official
- [C16] 冲突②A：reference 将 strict 列为 /chat/completions 普通字段，默认 false，自标 Beta 并转引 Tool Calls Guide | src: https://api-docs.deepseek.com/api/create-chat-completion/ | quote: "strict booleanDefault value: false … This is a Beta feature, for more details please refer to Tool Calls Guide" | type: official
- [C17] 冲突②B：tool_calls 指南给出启用条件：base_url=…/beta 且函数内 strict:true | src: https://api-docs.deepseek.com/guides/tool_calls/ | quote: "Use base_url=\"https://api.deepseek.com/beta\" to enable Beta features" | type: official
- [C18] /responses 顶层不支持：previous_response_id、conversation、store、background、metadata、include、prompt、truncation、service_tier、safety_identifier、prompt_cache_key(_retention)、context_management、stream_options | src: https://api-docs.deepseek.com/guides/responses_api/ | quote: "storeNot supported. The response always carries store: falsebackgroundNot supportedmetadataNot supported" | type: official
- [C19] /responses 未支持参数静默忽略、不报错 | src: https://api-docs.deepseek.com/guides/responses_api/ | quote: "Unsupported parameters are silently ignored and do not cause errors, so existing Responses API clients can connect without modification." | type: official
- [C20] parallel_tool_calls/max_tool_calls 被 Ignored（并行恒开） | src: https://api-docs.deepseek.com/guides/responses_api/ | quote: "parallel_tool_callsIgnored (parallel tool calling is always enabled)" | type: official
- [C21] /responses tools：仅 function；custom 仅 apply_patch（其余名 400）；web_search/file_search/code_interpreter/computer_use/mcp 忽略 | src: https://api-docs.deepseek.com/guides/responses_api/ | quote: "customOnly {\"type\": \"custom\", \"name\": \"apply_patch\"} is supported (for Codex compatibility); other names return a 400 error" | type: official
- [C22] reasoning 仅 effort（summary 接受但不生成）；text.format 完全支持（verbosity 无效） | src: https://api-docs.deepseek.com/guides/responses_api/ | quote: "textPartially supported. format fully supported; verbosity accepted but has no effect" | type: official
- [C23] /responses 图像输入仅 deepseek-flash，限额与格式同 Chat Completions；流式以 response.completed/incomplete/failed 结束、无 data: [DONE] | src: https://api-docs.deepseek.com/guides/responses_api/ | quote: "The Responses API accepts images with the deepseek-flash model. The same image limits and supported formats as Chat Completions apply." | type: official

## conflicts
- 冲突①（/responses 支持模型范围）裁决：以 Models & Pricing 为准——deepseek-flash 与 deepseek-v4-pro 均支持 Responses API。依据：pricing 表 "Responses API✓✓" 覆盖两列（C13）；responses 指南 model 行 "Supported. deepseek-flash, see Models & Pricing"（C14）只举 flash 且自带转引 pricing，未声明 v4-pro 不支持；旁证 updates 2026-07-31（V4-Flash）与 2026-08-13（V4-Pro GA 原生支持，C15）。指南窄写法疑因示例统一用 flash，非能力差异。
- 冲突②（strict 是否须 /beta）裁决：两文并存、不构成矛盾——strict 是 /chat/completions 请求体普通字段（默认 false，C16），reference 自己标注 "This is a Beta feature" 并转引 Tool Calls Guide；实际启用条件以 guide 为准（C17）：须 base_url="https://api.deepseek.com/beta" 且每个函数设 strict:true。结论：字段存在于标准 schema，但启用 strict 必须 /beta base_url（"普通字段 + Beta 启用门槛"）。

## gaps
- /anthropic 完整端点路径（是否 …/anthropic/v1/messages）无逐字原句：guide 只给 base_url 与 SDK client.messages.create，兼容表提 "/messages"；已查 anthropic_api、首页、pricing，均未拼出全路径。
- anthropic_api / claude_code 页面无更新日期、版本号；Anthropic 面引入时点仅 changelog 2026-04-24（V4 系列 "available via both the OpenAI ChatCompletions interface and the Anthropic interface"）可佐证。
- thinking 输出块 signature 字段是否返回未说明（表只标 type="thinking" Supported、redacted_thinking 不支持）。

## leads
- 侧栏新增 News 页 /news/news260910（2026-09-10 V4.1-Flash 发布；V4 Pro 2026-09-14 后继续服务）未读。
- Agent Integrations 侧栏指向 deepseek-harness.github.io（官方 DeepSeek Harness agent 框架），新实体。
- /quick_start/rate_limit 未核。
