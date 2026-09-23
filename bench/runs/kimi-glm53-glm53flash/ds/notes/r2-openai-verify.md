# r2-openai-verify
question: 核验 seed ⚔、parallel_tool_calls ⚔、encrypted_content ⚔ 与两缺口（错误对象形状、chat prompt_cache_key）。
checked: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml, https://developers.openai.com/api/docs/guides/function-calling, https://developers.openai.com/api/docs/guides/responses-vs-chat-completions, https://platform.openai.com/docs/deprecations, https://developers.openai.com/api/docs/guides/error-codes, https://platform.openai.com/docs/api-reference/chat/create, https://developers.openai.com/api/docs/guides/prompt-caching

## claims
- [C1] 判定①：master openapi.yaml CreateChatCompletionRequest.seed 带 deprecated:true（行 37643，2026-09-23 抓取），x-oaiMeta.beta=true | src: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml | quote: "This feature is in Beta. If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result." | type: official
- [C2] 仅 chat completions seed 弃用；CreateCompletionRequest.seed 与微调 seed 无弃用标记 | src: 同上 | quote: "If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result." | type: official
- [C3] deprecations 页只覆盖模型/端点退役（2026-09-23 打开，最新条目 2026-09-11，全文无 seed）| src: https://platform.openai.com/docs/deprecations | quote: "We use the term \"deprecation\" to refer to the process of retiring a model or endpoint." | type: official
- [C4] chat/create 文档页 system_fingerprint 仍引用 seed 参数 | src: https://platform.openai.com/docs/api-reference/chat/create | quote: "Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made that might impact determinism." | type: official
- [C5] 判定②：ParallelToolCalls schema（行 49939）default:true | src: openapi.yaml 同上 | quote: "Whether to enable [parallel function calling](https://developers.openai.com/api/docs/guides/function-calling#parallel-function-calling) during tool use."（default: true）| type: official
- [C6] Responses create 与 Response schema 的 parallel_tool_calls 亦 default:true（行 ~40560/~62059）| src: openapi.yaml 同上 | quote: "Whether to allow the model to run tool calls in parallel."（default: true）| type: official
- [C7] 判定②：function-calling 指南只写关闭方式、无默认值 | src: https://developers.openai.com/api/docs/guides/function-calling | quote: "The model may choose to call multiple functions in a single turn. You can prevent this by setting parallel_tool_calls to false, which ensures exactly zero or one tool is called." | type: official
- [C8] 指南补充：GPT-5 起并行调用限制 | src: 同上 | quote: "On supported models beginning with GPT-5, functions can be called in parallel when built-in tools are also available. Built-in tools cannot be included in a parallel function-call batch." | type: official
- [C9] 判定③：迁移指南 ZDR 段称每项默认含 encrypted_content | src: https://developers.openai.com/api/docs/guides/responses-vs-chat-completions | quote: "Preserve and replay every returned reasoning item. Each item includes encrypted_content by default when you create a response." | type: official
- [C10] 当前 spec ReasoningItem.encrypted_content 与指南一致：默认填充 | src: openapi.yaml 同上 | quote: "The encrypted content of the reasoning item. This is populated by default for reasoning items returned by `POST /v1/responses` and WebSocket `response.create` requests." | type: official
- [C11] spec 内 include 枚举仍留旧 opt-in 措辞，与 C10 并存 | src: openapi.yaml 同上 | quote: "Includes an encrypted version of reasoning tokens in reasoning item outputs. This enables reasoning items to be used in multi-turn conversations when using the Responses API statelessly" | type: official
- [C12] 迁移指南：ZDR 组织强制 store:false | src: 同上 | quote: "For ZDR organizations, OpenAI enforces store: false automatically." | type: official
- [C13] 错误码指南确认 error.code/error.type 及层级 | src: https://developers.openai.com/api/docs/guides/error-codes | quote: "For billing-related errors, inspect error.code to identify the specific cause. The broader error.type can still be insufficient_quota." | type: official
- [C14] 错误码指南确认 error.param | src: 同上 | quote: "as an invalid_request_error with error.param set to service_tier when a request selects or resolves to a service tier that is not allowed for the project." | type: official
- [C15] 缺口④：spec ErrorResponse={error:Error}；Error 必含 type/message/param/code（param、code 可空 string），另有可选 misalignment；Realtime 错误对象同形（多 event_id）| src: openapi.yaml 同上 | quote: "The type of error (e.g., \"invalid_request_error\", \"server_error\")." | type: official
- [C16] 缺口⑤：chat completions 经 allOf CreateModelResponseProperties→ModelResponseProperties 继承 prompt_cache_key（行 49235）| src: openapi.yaml 同上 | quote: "Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field." | type: official
- [C17] prompt-caching 指南：GPT-5.6 前靠 prompt_cache_key 优化缓存路由 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "On models before GPT-5.6, prompt_cache_key is important for optimizing cache hit rates. Use a stable key for requests that share a reusable prefix to help route them to the same cache." | type: official
- [C18] 指南：GPT-5.6+ prompt_cache_key 仅用于分账户统计 | src: 同上 | quote: "On GPT-5.6 and later, use prompt_cache_key when you want to maintain separate cache accounting for customers, users, or workspaces within your application." | type: official
- [C19] spec user 字段标弃用并指向 prompt_cache_key | src: openapi.yaml 同上 | quote: "This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations." | type: official

## conflicts
- ① seed ⚔：非真冲突、非版本差异。spec 参数级 deprecated:true 仍有效（C1，行号与 R1 一致）；deprecations 页按声明只列"model or endpoint"退役（C3），不列参数级弃用。当前口径：chat completions seed 已弃用（仍标 Beta、无退役日期）；legacy /v1/completions 与微调 seed 未弃用（C2）。
- ② parallel_tool_calls ⚔：以 spec 为准——两处均 default:true（C5/C6，R1 行 49944 现仍 default:true）。指南只写可设 false（C7），属省略非矛盾。当前口径：默认开启；GPT-5 起内置工具不可入并行批次（C8）。
- ③ encrypted_content ⚔：迁移指南与当前 spec 一致——"populated by default"（C9/C10）。R1"仅 include 才有"出自 include 枚举旧措辞（C11），仍并存于同一文件，属 spec 内部新旧表述共存。当前口径：默认返回 encrypted_content；include 参数仍在但描述未更新。

## gaps
- api-reference chat/create 请求参数段为纯客户端渲染（curl 仅 9.8KB 空壳；FetchURL 文本缺请求参数段），未取到页面上 seed 的"Deprecated"渲染原句；判定以 spec + system_fingerprint 交叉引用（C4）支撑。
- seed 弃用标记加入时间无法定位：仓库顶层已无 changelog.md，未查 git 提交历史。

## leads
- CreateChatCompletionRequest 的 system_fingerprint 同标 deprecated:true（行 ~37978）；user、function_call、prompt_cache_retention 亦弃用，可作参数弃用面盘点。
- GPT-5.6+ 新缓存参数 prompt_cache_options.mode/ttl/prewarm、prompt_cache_breakpoint 与 spec 对齐未核。
- openai-python SDK 侧 seed 弃用标注未核验。
