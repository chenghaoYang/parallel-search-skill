# r1-scout-cn
question: 为下一轮定位 Kimi（月之暗面 Moonshot）、智谱、通义千问（DashScope/百炼）、OpenRouter 的官方缓存文档 URL，并判断各自更像「自动前缀 / 显式断点 / 命名资源 / 网关透传」中的哪一类。只做定位，不把细节填进成稿。
checked: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api, https://platform.kimi.com/docs/api/chat, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://help.aliyun.com/zh/model-studio/context-cache, https://openrouter.ai/docs/guides/best-practices/prompt-caching, https://platform.minimax.cn/docs/api-reference/text-prompt-caching, https://docs.volcengine.com/docs/82379/1398933, https://www.volcengine.com/docs/82379/1398933

## claims
- [C1] Kimi 更像自动前缀：按 messages 开头连续 token 的最长匹配前缀命中，不是用户标断点。 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "前缀指请求 messages 中从开头连续的 token 序列；缓存按最长匹配前缀计算，匹配成功即为命中。" | type: official
- [C2] Chat/Responses 的 `prompt_cache_options.mode` 仅 `implicit`；`ttl` 仅 `5m`/`1h`；省略则默认 `5m` 写入。主机 `https://api.moonshot.cn`，端点 `POST /v1/chat/completions`。 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "`prompt_cache_options.mode` 当前仅支持 `implicit`，`ttl` 支持 `5m` 和 `1h`。" | type: official
- [C3] 不是显式断点：content 里出现 `prompt_cache_breakpoint` 会被 HTTP 400 拒绝。用量字段 `usage.prompt_tokens_details.cached_tokens` 与 `cache_write_tokens`。 | src: https://platform.kimi.com/docs/api/chat | quote: "暂不支持显式缓存断点：`content` 中出现 `prompt_cache_breakpoint` 时请求会被拒绝（HTTP 400）。" | type: official
- [C4] Anthropic 兼容路径只用顶层 `cache_control`（`type`/`ttl`）；消息体内同名标记被忽略，仍不是逐块断点。另有 `prompt_cache_key`（会话亲和），不是单独创建的缓存资源。 | src: https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api | quote: "`cache_control` 只在请求顶层生效，消息体内的同名标记会被忽略。" | type: official
- [C5] 智谱更像自动前缀（页内称隐式缓存、无需手动配置）。命中字段 `usage.prompt_tokens_details.cached_tokens`。示例主机 `https://open.bigmodel.cn`，端点 `POST /api/paas/v4/chat/completions`。 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "自动缓存识别：隐式缓存，智能识别重复的上下文内容，无需手动配置" | type: official
- [C6] 通义/百炼主文档同时写两种模式，互斥：隐式=自动前缀且无法关闭；显式=在 content 上放 `cache_control`（`type` 仅 `ephemeral`）。更像「自动前缀 + 显式断点」，不是单一类。 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "显式缓存、隐式缓存两者互斥，单个请求只能应用其中一种模式。" | type: official
- [C7] 隐式原文：自动识别公共前缀，无需配置且无法关闭，命中率不确定。显式以每个 `cache_control` 为终点向前回溯。用量：`cache_creation_input_tokens`、`cached_tokens`；Anthropic 兼容为 `cache_creation_input_tokens` / `cache_read_input_tokens`。 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "隐式缓存：此为自动模式，无需额外配置，且无法关闭" | type: official
- [C8] 该页示例 base URL 是 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（DashScope 为同主机 `/api/v1`，Anthropic 为 `/apps/anthropic`）。同页未见 `dashscope.aliyuncs.com`。Responses API 另点名 Session 缓存，未在本页展开。 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "Responses API 另有 Session 缓存配置。" | type: official
- [C9] OpenRouter 的 prompt caching 更像网关透传：多数供应商自动缓存；Alibaba 与 Anthropic 要按消息开。字段：`cache_control`、`prompt_cache_breakpoint`、`prompt_cache_options`、`session_id` / header `x-session-id`、`prompt_cache_key`；用量 `prompt_tokens_details.cached_tokens` 与 `cache_write_tokens`。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Most providers automatically enable prompt caching, but note that some (see Alibaba and Anthropic below) require you to enable it on a per-message basis." | type: official
- [C10] OpenRouter 把阿里显式缓存写成必须加断点：`cache_control: { "type": "ephemeral" }`，并称 5-minute TTL。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Alibaba prompt caching requires explicit cache breakpoints." | type: official
- [C11] OpenRouter 把 Moonshot 写成完全自动、且 cache write 无费用。 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Prompt caching with Moonshot AI is automated and does not require any additional configuration." | type: official
- [C12] 火山方舟不是第五类：隐式=自动前缀且不可关；显式=前缀缓存或 Session 缓存，用 `caching`（`type`=`enabled`，前缀另加 `prefix`: true）加 `previous_response_id`，服务端生成 ID 作 Key（靠近命名资源）。页内更新 2026.09.22 16:52:16。示例主机 `https://ark.cn-beijing.volces.com/api/v3`。 | src: https://docs.volcengine.com/docs/82379/1398933 | quote: "用户创建缓存时，方舟将信息处理为可直接用于模型推理的 Tokens 存入缓存，并生成 ID 作为 Key。" | type: official
- [C13] 火山：请求走显式缓存时隐式不生效。隐式命中看 `usage.prompt_tokens_details.cached_tokens`。 | src: https://docs.volcengine.com/docs/82379/1398933 | quote: "当请求使用显式缓存时，隐式缓存不生效。" | type: official
- [C14] MiniMax 不是第五类：OpenAI/默认路径是被动自动前缀；Anthropic 兼容另有主动缓存，字段 `cache_control`。用量：`prompt_tokens_details.cached_tokens` 或 `cache_read_input_tokens`。国内示例主机 `https://api.minimax.cn`（`/v1` 与 `/anthropic`）。 | src: https://platform.minimax.cn/docs/api-reference/text-prompt-caching | quote: "自动缓存：被动缓存，自动识别重复的上下文内容，无需更改接口调用方式" | type: official

## conflicts
- OpenRouter 官方写 Moonshot「Cache writes: no cost」且「Prompt caching with Moonshot AI is automated and does not require any additional configuration.」（https://openrouter.ai/docs/guides/best-practices/prompt-caching）。Kimi 官方写省略 `prompt_cache_options` 时默认 `5m` 写入，「账单上会产生相应的缓存写入费用」，且 mode 只能是 `implicit`（https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api）。不裁决哪边是当前计费。
- OpenRouter 写「Alibaba prompt caching requires explicit cache breakpoints.」（同上）。百炼写隐式「无需额外配置，且无法关闭」，显式才要 `cache_control`，且两种互斥（https://help.aliyun.com/zh/model-studio/context-cache）。网关文档只覆盖显式路径，与平台「隐式默认开」不一致。

## gaps
- 智谱缓存指南全文未见 `cache_control`、`prompt_cache_options` 或单独创建缓存的接口；未再打开第二页，不能写成「产品不支持显式/命名缓存」。
- OpenRouter prompt-caching 页未写 API host。未 fetch quickstart / API reference。搜索摘要指向 `POST https://openrouter.ai/api/v1/chat/completions`，不能当已核对主张。
- 简报优先的 platform.moonshot.cn 与英文 platform.kimi.ai 未打开。已打开的中文主文档在 platform.kimi.com，示例主机是 api.moonshot.cn。英文站是否改用 api.moonshot.ai 未核。
- 百川 `https://platform.baichuan-ai.com/docs/api` fetch 失败。搜索摘录的参数表未见缓存字段，不能断言「不支持」。
- 硅基流动：docs.siliconflow.com 检索无 prompt-caching 专页；chat completions 搜索摘录的 usage 只有 prompt/completion/total tokens。价目页 `https://www.siliconflow.cn/pricing` 摘要有「缓存价格」列，未打开。Prefix Completion（`extra_body.prefix`）是补全前缀，不是 prompt cache。
- 通义 Session 缓存只在 context-cache 页被点名，未打开 `https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api`。
- 火山旧页 `https://www.volcengine.com/docs/82379/1396491`（搜索标题含 Context API「待下线」）未打开。
- Kimi / 智谱 / 百炼 / OpenRouter / MiniMax 已打开页未见文内更新日期。

## leads
- Kimi：自动前缀。主文档 https://platform.kimi.com/docs/guide/use-context-caching-feature-of-kimi-api ；字段表 https://platform.kimi.com/docs/api/chat 。主机 api.moonshot.cn。字段 `prompt_cache_options.mode=implicit`、`ttl`、`prompt_cache_key`、`cached_tokens`、`cache_write_tokens`；Anthropic 仅顶层 `cache_control`。不像其余三类：断点会被 400，无独立 cache 资源 ID，不是网关。
- 智谱：自动前缀。https://docs.bigmodel.cn/cn/guide/capabilities/cache 。主机 open.bigmodel.cn，`/api/paas/v4/chat/completions`。字段 `usage.prompt_tokens_details.cached_tokens`。不像其余三类：页内写无需手动配置，无断点、无 cache 名、无网关路由。
- 通义：双模式，不要收成一类。主文档 https://help.aliyun.com/zh/model-studio/context-cache （搜索镜像 https://docs.bailian.console.aliyun.com/zh/model-studio/context-cache 未另开）。隐式=自动前缀；显式=断点 `cache_control.type=ephemeral`。示例主机 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。R2 另开 Responses Session 缓存，可能靠近命名/会话资源，先别并进断点。
- OpenRouter：网关透传。https://openrouter.ai/docs/guides/best-practices/prompt-caching 。透传自动前缀或 `cache_control` / `prompt_cache_breakpoint`，外加 sticky `session_id`。不是自有前缀缓存。另页 Response Caching（搜索见 https://openrouter.ai/docs/guides/features/response-caching ，header `X-OpenRouter-Cache`）是整段响应缓存，不要和 prompt caching 混。
- 火山豆包：同家族，不建议加行。隐式=自动前缀；显式前缀/Session=命名资源（`previous_response_id` + `caching`）。https://www.volcengine.com/docs/82379/1398933 （打开后在 docs.volcengine.com 同路径）。主机 ark.cn-beijing.volces.com。
- MiniMax：同家族，不建议加行。被动=自动前缀；Anthropic=显式断点。https://platform.minimax.cn/docs/api-reference/text-prompt-caching 与同站 `/docs/api-reference/anthropic-api-compatible-cache`（后者未打开，对比表已在前页）。
- 百川、硅基流动：未见与四类都不同的机制专页，不建议加行。百川 API 页未打开成功；硅基流动无机制专页。
