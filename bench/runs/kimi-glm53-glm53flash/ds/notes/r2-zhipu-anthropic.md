# r2-zhipu-anthropic
question: 智谱 AI（GLM）官方提供的 Anthropic Messages 兼容端点，对比 Anthropic 官方 /v1/messages 规范，差异具体是什么？
checked: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction, https://docs.bigmodel.cn/cn/guide/develop/claude.md, https://docs.bigmodel.cn/cn/guide/develop/openai/introduction.md, https://docs.bigmodel.cn/cn/guide/capabilities/cache.md, https://docs.bigmodel.cn/cn/guide/capabilities/thinking.md, https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3.md, https://docs.bigmodel.cn/llms.txt, https://docs.z.ai/llms.txt

## claims
- [C1][D1] 兼容 base_url 为 https://open.bigmodel.cn/api/anthropic，迁移只改 key/base_url/模型名三处 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "替换您访问的 base_url 为 https://open.bigmodel.cn/api/anthropic" | type: official
- [C2][D1] 完整端点 = base_url + /v1/messages | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "curl https://open.bigmodel.cn/api/anthropic/v1/messages \" | type: official
- [C3][D1] GLM-5.3 模型页协议表同样列 Anthropic Message 协议入口 | src: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3.md | quote: "| Anthropic Message 协议      | `https://open.bigmodel.cn/api/anthropic` |" | type: official
- [C4][D2] 直连用智谱 API Key 走 x-api-key 头 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "--header \"x-api-key: YOUR_API_KEY\" \" | type: official
- [C5][D2] Claude Code 接入用 ANTHROPIC_AUTH_TOKEN + ANTHROPIC_BASE_URL 环境变量指向同端点 | src: https://docs.bigmodel.cn/cn/guide/develop/claude.md | quote: "\"ANTHROPIC_AUTH_TOKEN\": \"YOUR_API_KEY\", \"ANTHROPIC_BASE_URL\": \"https://open.bigmodel.cn/api/anthropic\"" | type: official
- [C6][D3] 官方 cURL 示例请求头仅 x-api-key 与 content-type，未含 anthropic-version | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "curl https://open.bigmodel.cn/api/anthropic/v1/messages \ --header \"x-api-key: YOUR_API_KEY\" \ --header \"content-type: application/json\"" | type: official
- [C7][D4] 调用须改用智谱模型编码；示例 Python/Java/cURL 用 glm-5.3，TypeScript 用 glm-5.2 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "model=\"glm-5.3\",  # 使用智谱模型" | type: official
- [C8][D4] Claude Code 默认服务端模型映射：界面显示 Claude 模型、实际为 GLM | src: https://docs.bigmodel.cn/cn/guide/develop/claude.md | quote: "在成功配置套餐后，默认为服务端模型映射，即您界面上看到的是 Claude 模型但实际是 GLM 模型。" | type: official
- [C9][D4] Claude Code 默认 ANTHROPIC_DEFAULT_HAIKU/SONNET/OPUS_MODEL=glm-4.7，最新配 glm-5.2[1m]，[1m] 后缀开 1M 上下文 | src: https://docs.bigmodel.cn/cn/guide/develop/claude.md | quote: "注意开启 GLM 1M 上下文需要模型后缀加上 `[1m]` 即 `glm-5.2[1m]`, 同时配置压缩窗口大小参数 `\"CLAUDE_CODE_AUTO_COMPACT_WINDOW\": \"1000000\"`" | type: official
- [C10][D5] GLM-5.3 上限：1M 上下文窗口、最大输出 128K Tokens | src: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3.md | quote: "GLM-5.3 目前仅支持处理文本模态信息，支持 1M 上下文窗口，最大输出 Tokens 为 128K。" | type: official
- [C11][D5] 模型页/兼容页代码示例 max_tokens 取 1024 或 65536，均显式携带 | src: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3.md | quote: "\"max_tokens\": 65536," | type: official
- [C12][D7] 兼容端点支持流式，示例请求体含 stream: true | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "\"max_tokens\": 1024, \"stream\": true," | type: official
- [C13][D8] GLM 侧思考参数为 thinking.type（enabled/disabled）+ reasoning_effort，非 budget_tokens | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking.md | quote: "* **`thinking.type`**: 控制深度思考模式" | type: official
- [C14][D8] GLM-5.3/GLM-5.3-FLASH 强制思考，传 disabled 报错 | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking.md | quote: "GLM-5.3 GLM-5.3-FLASH 不再支持关闭思考（API 请求中 thinking.type 传 disabled 将会报错）" | type: official
- [C15][D8] reasoning_effort 取值按模型：GLM-5.3 仅 max/high/low；GLM-5.2 另有 xhigh/medium/low/minimal/none 并自动映射 | src: https://docs.bigmodel.cn/cn/guide/capabilities/thinking.md | quote: "reasoning_effort=\"high\"  # GLM-5.3 仅支持: max, high, low；GLM-5.2 另支持 xhigh, medium, low, minimal, none 并自动映射" | type: official
- [C16][D8] Claude Code 场景由 /effort 命令映射到 GLM 实际 effort（low/medium/high→high；xhigh/max/ultra→codemax） | src: https://docs.bigmodel.cn/cn/guide/develop/claude.md | quote: "切换后，Claude Code 内部会将所选的 effort 映射到 GLM-5.2 实际生效的 effort，对应关系如下" | type: official
- [C17][D9] 智谱缓存为隐式自动缓存，无需手动配置（未提及 cache_control） | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache.md | quote: "**自动缓存识别**：隐式缓存，智能识别重复的上下文内容，无需手动配置" | type: official
- [C18][D9] 缓存命中计入 usage.prompt_tokens_details.cached_tokens（非 Anthropic 的 cache_read_input_tokens） | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache.md | quote: "详细显示缓存命中的 Token 数量，响应字段 `usage.prompt_tokens_details.cached_tokens`" | type: official
- [C19][D9] 缓存命中要求重复前缀足够长（建议 500 Token 以上） | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache.md | quote: "重复的前缀内容必须足够长（建议 500 Token 以上）" | type: official
- [C20][D10] 官方仅一句总括性差异声明，无逐项差异清单页 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "某些场景下智谱与 Claude 接口仍存在差异，但不影响整体兼容性。" | type: official
- [C21][D10] 兼容层承诺跟随 Anthropic SDK 更新 | src: https://docs.bigmodel.cn/cn/guide/develop/claude/introduction | quote: "跟随 Anthropic SDK 更新，保持最新功能支持" | type: official
- [C22][zhipu-native D1] 智谱原生 OpenAI 兼容 base_url 为 https://open.bigmodel.cn/api/paas/v4/ | src: https://docs.bigmodel.cn/cn/guide/develop/openai/introduction.md | quote: "base_url=\"https://open.bigmodel.cn/api/paas/v4/\"" | type: official
- [C23][zhipu-native D1] 官方明示 OpenAI API 兼容声明 | src: https://docs.bigmodel.cn/cn/guide/develop/openai/introduction.md | quote: "智谱提供与 OpenAI API 兼容的接口，这意味着您可以使用现有的 OpenAI SDK 代码，只需要简单修改 API 密钥和基础 URL，就能无缝切换到智谱的模型服务。" | type: official

## conflicts
- thinking 同名参数两侧语义冲突且兼容层翻译无文档：Anthropic 规范 thinking={type:"enabled",budget_tokens≥1024}（docs.claude.com/en/docs/build-with-claude/extended-thinking："**Minimum of 1,024 tokens.**"），GLM 侧为 thinking.type+reasoning_effort、无 budget_tokens、GLM-5.3 传 disabled 直接报错（https://docs.bigmodel.cn/cn/guide/capabilities/thinking.md，C13–C15）。兼容端点如何翻译/拒绝 budget_tokens 未说明。
- 认证表述不一：Claude 兼容直连示例用 x-api-key（C4），Claude Code 配置用 ANTHROPIC_AUTH_TOKEN（通常映射为 Authorization: Bearer，C5）；端点是否同时接受两种头无官方说明。

## gaps
- anthropic-version 是否必填/被忽略：全部智谱页均无说明（仅 C6 示例性缺席），无智谱版 versioning 页。
- tools/input_schema/tool_use/tool_result/tool_choice/disable_parallel_tool_use 在 Anthropic 端点的兼容性：无专页；function-calling/stream-tool 页只覆盖原生 chat.completions（OpenAI 风格）。
- Anthropic 端点 SSE 事件形态（message_start/content_block_delta 等是否同形）：仅有 stream:true 示例，无事件文档；智谱流式文档（capabilities/streaming）描述的是 OpenAI 风格 choices.delta/data: [DONE]。
- cache_control={type:ephemeral} 是否被接受/忽略：无文档，缓存机制仅有隐式缓存描述（C17）。
- anthropic-beta 头处理：零文档。
- max_tokens 必填性：示例均携带但无必填性文字；Anthropic 端点上限是否等于模型 128K 输出上限未说明。
- z.ai 国际站 llms.txt 索引未见 Anthropic 兼容 API 页（仅 OpenAI 风格 Chat Completion），国际端点未查证。

## leads
- GLM Coding Plan 另有双协议入口：Anthropic=/api/anthropic、OpenAI=/api/coding/paas/v4、Response=/api/v1（coding-plan/quick-start 页，未打开核验）。
- 原生 tool_stream=true（工具流式输出）与 function-calling 页可作 D6 对照线索。
- 智谱无 Anthropic 端点的 OpenAPI/API reference；逐项差异只能靠行为实测补齐（用户疑点②成稿时需标注"官方仅一句总括声明"）。
