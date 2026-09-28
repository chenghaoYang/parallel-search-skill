# r1-openai
question: OpenAI API 的 prompt caching（提示词缓存）机制、计费、TTL、命中确认字段、失效条件。
checked: https://developers.openai.com/api/docs/guides/prompt-caching, https://developers.openai.com/api/docs/pricing, https://developers.openai.com/api/docs/changelog, https://raw.githubusercontent.com/openai/openai-python/main/src/openai/types/completion_usage.py

## claims
- [C1] 机制=自动前缀 KV 缓存，默认开启，无需启用参数 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Prompt caching is enabled by default for supported OpenAI models." | type: official
- [C2] 缓存内容是 KV 张量而非 token；按渲染后的前缀匹配 | src: 同上 | quote: "The prompt cache stores key-value (KV) tensors, not the tokens themselves." | type: official
- [C3] 命中要求完整渲染前缀一致 | src: 同上 | quote: "Cache reuse requires the entire rendered prefix to match." | type: official
- [C4] 最小可缓存前缀：GPT-5.6+ 为 1,024 tokens；更早模型随请求设置变化 | src: 同上 | quote: "The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later and varies by request settings for earlier models." | type: official
- [C5] OpenAI 隐藏 system 内容不计入最小长度 | src: 同上 | quote: "Tokens in the OpenAI-provided hidden system content do not count toward this minimum." | type: official
- [C6] 更早模型只有隐式缓存，breakpoint 按模型相关间隔放置 | src: 同上 | quote: "OpenAI places implicit breakpoints at model-dependent intervals , counted from the beginning of the hidden OpenAI system message." | type: official
- [C7] GPT-5.6+ 支持 explicit 模式：在内容块加 prompt_cache_breakpoint，每请求最多 4 次 cache write | src: 同上 | quote: "Each request can create up to four cache writes." | type: official
- [C8] 命中计费：按模型 cached-input 费率，最高折扣 90% | src: 同上 | quote: "Pay the model’s reduced cached-input rate for reused tokens, discounted up to 90%." | type: official
- [C9] GPT-5.6+ 写缓存收费 1.25× 输入价，读 0.1×；更早模型无写入费 | src: 同上 | quote: "cache writes cost 1.25× the standard, uncached input-token rate" / "subsequent reads cost only 0.1× that rate" / 表格行 "No additional cache-write charge" | type: official
- [C10] 三种费率互斥，不是叠加费 | src: 同上 | quote: "Cache-write pricing is not an additive fee: input tokens use the uncached-input, cached-input, or cache-write rate." | type: official
- [C11] 价格例：gpt-5 cached $0.125 vs input $1.25（90% off）；gpt-4o $1.25 vs $2.50（50%）；o1 $7.50 vs $15（50%）；o3 $0.50；gpt-5.6-sol cache write $5.00 | src: https://developers.openai.com/api/docs/pricing | quote: "| gpt-5 | $1.25 | $0.125 |" / "| gpt-4o | $2.50 | $1.25 |" / "| o1 | $15.00 | $7.50 |" | type: official
- [C12] TTL（GPT-5.6+）：prompt_cache_options.ttl 仅支持 "30m" 且为默认 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse, though OpenAI may retain it longer." | type: official
- [C13] TTL（更早模型）：prompt_cache_retention=in_memory 约 5–10 分钟不活跃即失效、至多 1 小时 | src: 同上 | quote: "in_memory : Entries typically remain active for around 5 to 10 minutes of inactivity, up to one hour." | type: official
- [C14] TTL（更早模型）：prompt_cache_retention=24h 通常约 30 分钟、至多 24 小时 | src: 同上 | quote: "24h : Extended retention typically keeps entries available for around 30 minutes and can retain them for up to 24 hours." | type: official
- [C15] 默认 retention 依 ZDR：无 ZDR 默认 24h；有 ZDR 默认 in_memory（限同时支持两者的模型） | src: 同上 | quote: "Organizations without Zero Data Retention enabled default to 24h ." | type: official
- [C16] 命中复用刷新生命周期且不再收写入费 | src: 同上 | quote: "reusing the prefix refreshes its lifetime without another cache-write charge" | type: official
- [C17] 命中确认字段（Responses）：usage.input_tokens_details.cached_tokens 与 cache_write_tokens | src: 同上 | quote: "Track usage.input_tokens_details.cached_tokens , usage.input_tokens_details.cache_write_tokens" | type: official
- [C18] 命中确认字段（Chat Completions）：usage.prompt_tokens_details.cached_tokens / cache_write_tokens | src: https://raw.githubusercontent.com/openai/openai-python/main/src/openai/types/completion_usage.py | quote: "cached_tokens: Optional[int] = None\n    \"\"\"Cached tokens present in the prompt.\"\"\"" | type: official
- [C19] 更早模型 cached_tokens 口径：减去隐藏 system tokens 后向下取整到 128 的倍数 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "subtracting the hidden system tokens from the last matched breakpoint, then rounding down to the nearest multiple of 128" | type: official
- [C20] 失效/miss：缓存在单机本地，>15 rpm 会触发 overflow routing 导致 miss | src: 同上 | quote: "A request can reuse a cached prefix only if it reaches a machine holding a matching entry that has not expired." | type: official
- [C21] 缓存不跨组织、不跨区域处理边界共享 | src: 同上 | quote: "Caches are not shared across organizations and cannot be reused across regional processing boundaries ." | type: official
- [C22] 失效条件（设置变更）：model、tools、parallel_tool_calls、text.format、reasoning.effort、text.verbosity、context_management(compaction) 任一变化即破坏前缀 | src: 同上 | quote: "A different model can use different weights and caching behavior." | type: official
- [C23] prompt_cache_key 仅影响路由不保证命中；GPT-5.6+ 上只用于分账 | src: 同上 | quote: "Keys influence routing; they do not pin requests to a machine or guarantee a cache hit." | type: official
- [C24] 结构性 miss：implicit→explicit 切换不命中隐式前缀；把新内容并入同一条消息会使旧断点落在消息内部；初始连续 developer 块之后的 developer 消息不是隐式查找边界 | src: 同上 | quote: "request 2 checks only the explicit breakpoints in its own input, so it will not reuse that saved implicit prefix from request 1" | type: official
- [C25] 无需改代码；可选参数：prompt_cache_key、prompt_cache_retention（旧模型）、prompt_cache_options.mode/ttl/prewarm、prompt_cache_breakpoint（GPT-5.6+） | src: 同上 | quote: "enabled by default" + 示例 "prompt_cache_options" : { "mode" : "implicit" , "ttl" : "30m" } | type: official
- [C26] 可缓存内容：隐藏 instructions、developer 消息、工具定义、含 text/images/documents/supported audio 的会话历史 | src: 同上 | quote: "OpenAI caches the model’s full rendered context including OpenAI-provided instructions, developer messages , tool definitions , and conversation history containing text , images , documents , and supported audio ." | type: official
- [C27] 覆盖模型：pricing 页为 gpt-4o(-mini)、o1、o3、o3-mini、o4-mini、gpt-4.1、gpt-5/5.1/5.2/5.4/5.5/5.6/6 系、gpt-realtime-2.1 均列出 cached-input 价；24h retention 支持列表含 gpt-5.5, gpt-5.5-pro, gpt-5.4, gpt-5.2, gpt-5.1 系, gpt-5, gpt-5-codex, gpt-4.1 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "supported by gpt-5.5 , gpt-5.5-pro , gpt-5.4 , gpt-5.2 , gpt-5.1-codex-max , gpt-5.1 , gpt-5.1-codex , gpt-5.1-codex-mini , gpt-5.1-chat-latest , gpt-5 , gpt-5-codex , and gpt-4.1" | type: official
- [C28] GPT-5.5 只支持 extended(24h) 缓存，不支持 in_memory | src: https://developers.openai.com/api/docs/changelog | quote: "Caching for GPT-5.5 only works with extended prompt caching. In-memory prompt caching is not supported." | type: official
- [C29] 上线时间：2024-10-01 DevDay | src: 同上 | quote: "Prompt caching : Discounts and faster processing times on recently seen input tokens." | type: official
- [C30] 24h extended retention 2025-11-13 发布，KV 张量卸载到 GPU-local 存储 | src: 同上 | quote: "Extended prompt cache retention keeps cached prefixes active for longer, up to a maximum of 24 hours." | type: official
- [C31] 2026-05-29 起非 ZDR 组织 prompt_cache_retention 默认改为 24h | src: 同上 | quote: "prompt_cache_retention now defaults to 24h instead of in_memory" | type: official
- [C32] GPT-5.6（2026-07-09）引入 explicit 缓存控制；Prompt Cache Diagnostics 2026-09-08 GA | src: 同上 | quote: "GPT-5.6 adds Programmatic Tool Calling , explicit prompt caching controls" | type: official
- [C33] 命中 token 仍计入 TPM 限流；不能手动清缓存 | src: https://developers.openai.com/api/docs/guides/prompt-caching | quote: "Cached input tokens still count toward tokens-per-minute limits." / "Manual cache clearing is not currently available." | type: official
- [C34] prewarm（GPT-5.6+，prompt_cache_options.prewarm=true）按 cache-write 价计费 | src: 同上 | quote: "Tokens written to the cache during a prewarm request are billed at the standard cache-write rate." | type: official

## conflicts
- Pro 模型是否支持缓存存疑：guide 把 gpt-5.5-pro 列入 24h retention 支持名单（"supported by gpt-5.5 , gpt-5.5-pro , …"），但 pricing 页所有 pro 模型（gpt-5-pro, gpt-5.2-pro, gpt-5.4-pro, gpt-5.5-pro, o1-pro, o3-pro）cached-input 列显示 "-"（无 cached 价）。https://developers.openai.com/api/docs/guides/prompt-caching vs https://developers.openai.com/api/docs/pricing
- 版本漂移：旧版 guide（2025 年中之前）曾写「所有支持模型最小 1,024 tokens、统一约 50% 折扣」；现版改为 GPT-5.6+ 固定 1,024、更早模型"varies by request settings"、折扣"up to 90%"。旧页无法取原句（archive 被墙），仅记录漂移方向。

## gaps
- 更早模型的确切最小可缓存长度数值（只说"varies by request settings，含 tools/images/output schemas/reasoning effort/verbosity"；model comparison 页未取）
- o1-pro / o3-pro / *-pro 是否支持 prompt caching（pricing "-"）
- Batch API、Realtime API 会话内缓存的明细（changelog 显示 v1/batch 适用 retention；realtime 有 cached-input 价，但未取机制细节）
- 旧版文档原句无法核验（web.archive.org 被禁、openai.com/index/prompt-caching 连接失败）
- Assistants API 已关停（2026-08-26），缓存对照若含它需注意

## leads
- Prompt Cache Diagnostics 工具（GA 2026-09-08）+ Prompt Caching Dashboard（2026-08-20）：官方给出 miss 原因诊断，另一页 prompt-cache-diagnostics 有细节
- model comparison 页可补各模型最小可缓存长度数值
- "prompt_cache_key 防跨用户 cache-hit probing" 是容易被忽略的安全语义
