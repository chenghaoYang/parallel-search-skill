# r3-openai-gaps
question: 补 4 个具体缺口格——OpenAI Chat Completions 的内置工具与采样参数、OpenAI Responses 的采样参数、Gemini OpenAI 兼容层的结构化输出与长度参数。
checked: https://developers.openai.com/api/reference/resources/chat.md, https://developers.openai.com/api/docs/guides/reasoning, https://developers.openai.com/api/reference/resources/responses/methods/create, https://developers.openai.com/api/docs/guides/latest-model, https://raw.githubusercontent.com/openai/openai-python/main/src/openai/types/responses/response_create_params.py, https://ai.google.dev/gemini-api/docs/openai

## claims
- [C1] CC-D4：`web_search_options.search_context_size` 取 low/medium/high，默认 medium；另有 `user_location`（type `approximate`） | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "One of `low`, `medium`, or `high`. `medium` is the default." | type: official
- [C2] CC-D7：`temperature` 取值 0–2 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "What sampling temperature to use, between 0 and 2." | type: official
- [C3] CC-D7：`top_p` 为 nucleus sampling | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "An alternative to sampling with temperature, called nucleus sampling" | type: official
- [C4] CC-D7：`n` 为每条输入生成的 choices 数 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "How many chat completion choices to generate for each input message" | type: official
- [C5] CC-D7：`stop` 最多 4 个序列 | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Up to 4 sequences where the API will stop generating further tokens." | type: official
- [C6] CC-D7：`stop` 不支持 `o3`、`o4-mini` | src: https://developers.openai.com/api/reference/resources/chat.md | quote: "Not supported with latest reasoning models `o3` and `o4-mini`." | type: official
- [C7] CC/R-D7：Using GPT-6 页（无日期）：effort 非 `none` 时去掉 `temperature`、`top_p`、`top_logprobs` | src: https://developers.openai.com/api/docs/guides/latest-model | quote: "When reasoning effort is not `none`, remove `temperature`, `top_p`, and `top_logprobs`." | type: official
- [C8] CC/R-D7：GPT-6 Astra 不支持 effort `none` | src: https://developers.openai.com/api/docs/guides/latest-model | quote: "GPT-6 Astra does not support `none`; use `low` instead." | type: official
- [C9] R-D7：Responses 创建参数有 `temperature: Optional[float]` 与 `top_p: Optional[float]`（temperature docstring） | src: https://raw.githubusercontent.com/openai/openai-python/main/src/openai/types/responses/response_create_params.py | quote: "We generally recommend altering this or `top_p` but not both." | type: official
- [C10] GG-D7：示例用 `client.beta.chat.completions.parse(..., response_format=CalendarEvent)`；页更新 2026-09-02 UTC | src: https://ai.google.dev/gemini-api/docs/openai | quote: "Gemini models can output JSON objects in any structure you define." | type: official

## conflicts
- CC `tools`（同页 https://developers.openai.com/api/reference/resources/chat.md）：函数工具 `type` 写 "The type of the tool. Currently, only `function` is supported."；另有 "The type of the custom tool. Always `custom`."

## gaps
- CC `temperature`/`top_p`/`n` 默认值页上未显示。
- 带采样参数报错还是忽略未写（GPT-6 页只说 remove）；o 系列/GPT-5.x 专句未拿到。
- Responses 参考页截断，用 SDK 代替。
- CC 其他托管工具：无明确原句。
- GG：无 `json_schema` 字面示例（只有 SDK parse）；页面未提 `max_tokens`/`max_completion_tokens`。

## leads
- GPT-6 页另有：CC 还要去 `logprobs`，Responses 去 include 的 logprobs；Sol/Luna 支持 `none`。
- Perplexity 称 Gemini 兼容层 `max_completion_tokens` 为 `max_tokens` 别名（未证实）。
