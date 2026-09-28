# r2-openai-scope
question: 只划定两处冲突的主语范围，不重写 OpenAI 缓存总览。要填的格子：OpenAI 的 D1 与 D7。
checked: https://developers.openai.com/api/docs/guides/prompt-caching.md, https://developers.openai.com/api/reference/resources/responses/methods/create.md, https://developers.openai.com/api/docs/guides/your-data.md

## claims
- [C1] D1 第一句在 “Why prompt caching matters”，不提 `prompt_cache_options` 或 mode。三页缓存段无更新日期。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Prompt caching is enabled by default for supported OpenAI models." | type: official
- [C2] D1 第二句在 h2 “How caching works” / h3 “GPT-5.6 and later” 的粗体 “Explicit mode:” 列表，不是全页默认。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "When no explicit breakpoints are placed, the request does not use prompt caching or create cache writes." | type: official
- [C3] 同一 h3、Explicit mode 列表之前同时有 implicit 与 explicit。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Both implicit and explicit caching are supported, where explicit caching gives you more control over which context is written to cache." | type: official
- [C4] 含 C2 的列表有 `mode` 与 `explicit`，该子弹无 `implicit`。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Set `prompt_cache_options.mode` to `explicit` to use only developer-selected breakpoints and mark each desired breakpoint by adding `prompt_cache_breakpoint: { "mode": "explicit" }` to a supported content block inside an input message." | type: official
- [C5] 同一 h3 后半 “Implicit mode:” 才写 `mode`=`implicit` 会放断点。`implicit` 与 C2 同 h3、不同列表。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "When `prompt_cache_options.mode` is `implicit`, OpenAI places a breakpoint at the end of the latest eligible message." | type: official
- [C6] 下一 h3 “Earlier models” 只有 implicit，不走 C2。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Only implicit caching is supported." | type: official
- [C7] 不传 `prompt_cache_options` 仍缓存的原句不在指南，在 create：对象 optional，默认一个 implicit breakpoint。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "By default, OpenAI automatically chooses one implicit cache breakpoint." | type: official
- [C8] 该对象只写明支持 `gpt-5.6` 及以后；设 `mode`=`explicit` 才关掉 implicit breakpoint。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "Options for prompt caching. Supported for `gpt-5.6` and later models." | type: official
- [C9] `prompt_cache_options.mode` 默认 `implicit`。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "Controls whether OpenAI automatically creates an implicit cache breakpoint. Defaults to `implicit`." | type: official
- [C10] 参考页 “无显式断点则不缓存” 紧跟 `explicit` 说明，不覆盖默认 implicit。下一句无 “or create cache writes”。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "If there are no explicit breakpoints, the request does not use prompt caching." | type: official
- [C11] C10 的上一句把主语限定为 explicit。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "With `explicit`, OpenAI does not create an implicit breakpoint and writes up to the latest four explicit breakpoints." | type: official
- [C12] D7 “only supported value, `30m`” 的参数是 `prompt_cache_options.ttl`，h3 是 Cache lifetime 下 “GPT-5.6 and later”，不是 retention。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Use `prompt_cache_options.ttl` to control the minimum cache lifetime. The only supported value, `30m`, is also the default." | type: official
- [C13] 指南把 `prompt_cache_retention` 放在 Cache lifetime 的 h3 “Earlier models”。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Use `prompt_cache_retention`, with supported values that depend on the model:" | type: official
- [C14] 差异表 Cache lifetime control：GPT-5.6+ 列是 `prompt_cache_options.ttl`；GPT-5.5 and GPT-5.5 Pro 与 Other earlier models 列是 `prompt_cache_retention`。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "Cache lifetime control" | type: official
- [C15] 同行 Supported retention values：5.6+ 为 `"30m"`，5.5/5.5 Pro 为 `"24h"` only，其他更早模型为 `"in_memory"` or `"24h"`。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "`"24h"` only" | type: official
- [C16] “only `24h`” 在请求参数 `prompt_cache_retention` 正文，不在 `ttl`。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "For `gpt-5.5`, `gpt-5.5-pro`, and future models, only `24h` is supported." | type: official
- [C17] 该字段把 `24h` 说成 extended prompt caching 的最大保留，不是 ttl 枚举。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "Set to `24h` to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours." | type: official
- [C18] 两字段独立：retention 是 maximum，ttl 是 minimum。 | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "This field expresses a maximum retention policy, while `prompt_cache_options.ttl` expresses a minimum cache lifetime. The two fields are independent and do not interact." | type: official
- [C19] `ttl` 自身只有 `30m`。同字段还写 “Deprecated. Use `prompt_cache_options.ttl` instead.” | src: https://developers.openai.com/api/reference/resources/responses/methods/create.md | quote: "Defaults to `30m`, which is currently the only supported value." | type: official
- [C20] your-data 的 `/v1/chat/completions` 与 `/v1/responses` 都把 `prompt_cache_retention`=`in_memory` 的报错限于 `gpt-5.5` 与 `gpt-5.5-pro`。 | src: https://developers.openai.com/api/docs/guides/your-data.md | quote: "For `gpt-5.5` and `gpt-5.5-pro`, setting `prompt_cache_retention` to `in_memory` returns an error." | type: official
- [C21] 同条把 `prompt_cache_options.ttl` 限于 GPT-5.6+，并声明它不是 24 小时 application-state 上限。 | src: https://developers.openai.com/api/docs/guides/your-data.md | quote: "For GPT-5.6 models and later model families, `prompt_cache_options.ttl` controls the minimum cache lifetime, not this maximum application-state retention period." | type: official
- [C22] “all queries use extended…” 只在 #### `/v1/responses`，原句不点任一参数名；条件是未开 Zero Data Retention。 | src: https://developers.openai.com/api/docs/guides/your-data.md | quote: "When Zero Data Retention is not enabled for an organization, all queries use extended prompt caching for all supported models." | type: official
- [C23] 同页 24 小时是 GPU-local 到期上限（chat 与 responses 都有），不是 ttl 取值。 | src: https://developers.openai.com/api/docs/guides/your-data.md | quote: "This data is stored on the local GPU machines and is not retained after the 24-hour expiration." | type: official
- [C24] 指南未开 ZDR 则默认 `24h`，主语是同时支持 `in_memory` 与 `24h` 的 retention，不是 ttl。 | src: https://developers.openai.com/api/docs/guides/prompt-caching.md | quote: "For models that support both `in_memory` and `24h`, the default depends on your organization's data retention policy:" | type: official

## conflicts
- D1 反例：C2 不推翻 C1。C2 只在 GPT-5.6+ 的 Explicit mode；同 h3 另有 implicit（C3、C5）；更早模型只有 implicit（C6）。create 默认 implicit breakpoint（C7、C9），无断点不缓存只跟在 explicit 后（C10、C11）。上一轮若把两句当成同一默认开关，主语错了。
- D7：上一轮把三句当成同一开关。带参原句是两个参数。`30m` = `prompt_cache_options.ttl`，GPT-5.6+，minimum（C12、C19）。`only 24h` = `prompt_cache_retention`（C16），且与 ttl independent（C18）。your-data “extended…all supported models”（C22）不点参数名；同页带参句是 C20/C21。指南表 C14/C15：5.6+ ttl/`30m`，5.5 retention/`"24h"` only。
- 未裁决：C16 的 “future models, only `24h`”（retention）对不上 C8/C19（options 仅 gpt-5.6+，ttl 仅 `30m`）和 C12/C15（5.6+ supported value `"30m"`）。同字段 “Deprecated. Use `prompt_cache_options.ttl` instead.” 与 C16 并列。C21 再把 5.6+ ttl 说成 minimum，不是 C23 的 24-hour expiration。

## gaps
- 指南无 “省略 `prompt_cache_options` 仍缓存” 的字面句；反例在 create（C7、C9）。
- C22 不能单独绑到 `prompt_cache_retention` 或 `ttl`。全页仅一次，不在 `/v1/chat/completions`。与 C17 只共享短语 “extended prompt caching”。
- 三页缓存段无更新日期/版本号。your-data 的 “As of March 1, 2023” 只讲训练，未写入主张。
- C14/C15 的 quote 是表单元格，不是完整行；列归属写在主张里，依据是同页 Summary of model differences 表。未打开这三页以外的 URL。

## leads
- 迁移列表 “Replace `prompt_cache_retention` with `prompt_cache_options.ttl`.” 只在迁到 GPT-5.6+ 一节。
- 表注 extended retention 名单含 `gpt-5.5` 与 `gpt-4.1`，挂在其他更早模型星号上。响应体复述 C16–C18，不是第三套语义。
