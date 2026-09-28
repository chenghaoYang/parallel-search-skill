# r2-openai-gaps
question: 补充两个缺口：(1) Chat Completions 端点是否支持 prompt caching；(2) 写入侧 1.25x 溢价是否仅限显式断点模式。另外核实官方 API 文档的域名。
checked: https://developers.openai.com/docs/guides/prompt-caching, https://developers.openai.com/api/docs/api-reference/chat/create

## claims
- [C1] Chat Completions POST /chat/completions 端点支持 `prompt_cache_options` 参数进行 prompt caching，支持 gpt-5.6 及更新模型 | src: https://developers.openai.com/api/docs/api-reference/chat/create | quote: "Options for prompt caching. Supported for `gpt-5.6` and later models. By default, OpenAI automatically chooses one implicit cache breakpoint." | type: official
- [C2] Prompt caching 写入成本在 GPT-5.6+ 模型下为标准费率的 1.25 倍，对 implicit 和 explicit 两种模式都适用（非仅限显式模式） | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "cache writes cost 1.25× the standard, uncached input-token rate" | type: official
- [C3] 官方 prompt caching 指南页面（https://developers.openai.com/docs/guides/prompt-caching）专注 Responses API 和 Agents API，未提及 Chat Completions 端点 | src: https://developers.openai.com/docs/guides/prompt-caching | quote: "Agents API model calls use the same prompt-caching behavior as the Responses API" (页面无 Chat Completions 相关内容) | type: official
- [C4] OpenAI 官方 API 文档域名为 developers.openai.com（确认当前状态） | src: https://developers.openai.com/api/docs/changelog | quote: "https://developers.openai.com/" | type: official

## conflicts
- C1 vs C3: Chat Completions API reference 文档化支持 prompt caching，但官方 prompt caching 指南页面未提及，造成文档一致性缺口

## gaps
- 旧版本模型（GPT-5.6 之前）的 chat completions 是否支持 prompt caching（指南仅提及 GPT-5.6+）
- Prompt caching 指南为何不覆盖 Chat Completions 端点（仅覆盖 Responses/Agents API）

## leads
- Chat Completions 的 prompt caching 支持确认来自 API reference 而非指南页，可能需要查看该指南更新日期或发布说明
