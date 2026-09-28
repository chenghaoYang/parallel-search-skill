# 各家大模型 API 的 Prompt Caching 对比

> 回答：要不要改代码、命中怎么计费、缓存活多久、怎么确认命中、什么会让缓存失效。截至 2026-09-25，以官方文档为准；[n] 见文末来源。

## 0. 一屏看懂

- **机制三派**：全自动（OpenAI、DeepSeek、智谱、Gemini implicit、Qwen 隐式、Kimi）；请求内断点标记（Anthropic、Qwen 显式、OpenAI/Azure GPT-5.6+ explicit、Kimi 的 Anthropic 端点）；独立缓存对象（仅 Gemini explicit CachedContent，先 create 再引用、付存储费）[1][3][4][7][8][9]。
- **「Anthropic 必须逐 block 打 cache_control」已过时一半**：2026-02-19 起有 automatic caching——请求顶层加一个 `cache_control` 字段即可，系统自动移动断点。但缓存仍非默认开启：不加字段=不缓存。OpenAI/DeepSeek/智谱/Gemini/Qwen 隐式才真正零改动 [2][5]。
- **计费两派**：写收费+读便宜（Anthropic 写 1.25×/2×、读 0.1×；Qwen 显式写 +25%、读省 90%；Kimi K3 写 5m=原价/1h=2×、读 1/10；OpenAI GPT-5.6+ 写 1.25×/读 0.1×）vs 无写费只给读折扣（OpenAI 旧模型读 0.1–0.5×；DeepSeek 命中 1/30–1/50；智谱约 5 折；Gemini/Qwen 隐式读约 0.1–0.2×）。Gemini explicit 另收存储费 $0.5–4.5/1M tok·hr；智谱定价页也有"缓存存储"列（限时免费）[1][2][3][5][7][8][9]。
- **TTL 两派**：固定窗口、命中免费续期（Anthropic 5m/可 1h；Kimi 5m/1h；Qwen 显式 5m；OpenAI GPT-5.6+ 30m 滑动；Bedrock 5m/1h）vs 不透明闲置清除（DeepSeek「几小时到几天」；智谱、Gemini implicit 未公布）[1][2][4][5][8][11]。
- **确认命中看 usage**：OpenAI 系 `…details.cached_tokens`（5.6+ 另有 `cache_write_tokens`）；Anthropic 系 `cache_read_input_tokens`/`cache_creation_input_tokens`；Gemini `cachedContentTokenCount`；DeepSeek 另有 `prompt_cache_hit_tokens`/`prompt_cache_miss_tokens`；OpenRouter 归一成 `cached_tokens`+`cache_discount` [1][2][3][5][6][10]。
- **失效共性**：全部按「从第 0 个 token 起的最长前缀匹配」，改 system/tools/中段任何内容即击穿其后全部；阿里 Session 更严——字符级精确匹配 [5][8]。
- **OpenRouter 的 prompt 缓存在上游**：它只做 `cache_control`↔`prompt_cache_breakpoint` 互译+粘性路由，推理价格=上游透传无加价；手动 `provider.order` 关粘性即 miss。另有自建 Response Caching（edge 存响应、`X-OpenRouter-Cache` 头族、默认 300s），属另一功能 [10][12]。

## 1. Taxonomy

分类轴 = **缓存以什么 API 形态暴露**：

| 家族 | 定义 | 成员 |
|---|---|---|
| A 隐式自动 | 服务端按前缀自动存取，请求无需字段 | OpenAI、DeepSeek、智谱、Gemini implicit、Qwen 隐式、Kimi、Azure OpenAI、Bedrock Nova |
| B 请求级标记 | 请求里放断点/开关字段，控制写位置与 TTL | Anthropic（顶层 auto + 逐块）、Qwen 显式 `cache_control`、OpenAI/Azure GPT-5.6+ `prompt_cache_breakpoint`、Bedrock `cachePoint`、Kimi Anthropic 端点 |
| C 独立缓存资源 | 先 `POST /cachedContents` 建对象再按名引用，付存储费 | 仅 Gemini explicit（旧 Kimi `/v1/caching` 已下线，实测 404） |
| D 网关翻译 | prompt 缓存在上游，做标记互译+路由 | OpenRouter |

维度：D1 启用方式｜D2 最小前缀门槛｜D3 TTL｜D4 计费｜D5 命中字段｜D6 匹配/失效｜D7 断点/对象管理｜D8 隔离。

## 2. 对照矩阵

**D1+D2+D7 机制·门槛·管理**

| 厂商 | 默认开 | 启用方式 | 最小前缀 | 断点/对象 |
|---|---|---|---|---|
| OpenAI | 是 | 零字段；GPT-5.6+ 可加 `prompt_cache_options{mode,ttl,prewarm}`+`prompt_cache_breakpoint` | 1,024 tok（5.6+；旧模型随设置变） | 每请求≤4 写；lookup 最多 80 断点 [1] |
| Anthropic | 否 | 顶层 `cache_control`(auto) 或逐块 `{"type":"ephemeral"}` | 512–4,096 按模型（Opus5.5=512、Sonnet系=1024、Haiku4.5=4096） | ≤4 断点；每断点 20-block lookback 读旧写 [2] |
| Gemini implicit | 是 | 零配置（2.5+ 默认开；Vertex 可 PATCH `cacheConfig disableCache:true` 项目级关闭，AI Studio 侧未见开关） | 2,048–6,144 按模型（2.5 Flash/Pro=2048；3.x Flash=4096，Vertex 部分 6,144） | 无 [3][11] |
| Gemini explicit | — | `POST /v1beta/cachedContents`，请求里 `cachedContent` 引用 | 当前页未列（旧版 1024/2048） | list/get/patch/delete；patch 只改过期 [3] |
| DeepSeek | 是 | 零字段（Anthropic 端点 `cache_control` 标 Ignored） | 按固定 token 间隔切分（数值未公布；2024 公告为 64） | 无管理 API [4][5] |
| Kimi | 是 | 隐式；`prompt_cache_options{mode,ttl}`；Anthropic 端点顶层 `cache_control` 控写 | 块大小未公开 | 无对象 CRUD；不可手动清 [7] |
| 智谱 | 是 | 零配置隐式 | 建议重复前缀 ≥500 tok | 无；部分型号不支持（GLM-4-AirX、GLM-Z1 系）[9] |
| 通义千问 | 隐式是 | 隐式不可关；显式在 messages 打 `cache_control`；Responses 另有 Session 缓存（`x-dashscope-session-cache` 头） | 隐式 1024（百炼上第三方 GLM/MiniMax 512） | 显式≤4 标记、仅 ephemeral [8] |
| OpenRouter | — | `cache_control`/`prompt_cache_breakpoint` 互译；TTL 不翻译 | 透传上游门槛 | Anthropic≤4；Gemini 只用最后一个 [10] |

**D3+D4 生命周期·计费**（倍数=相对该模型 input 原价）

| 厂商 | TTL | 写价 | 读价 | 存储费 |
|---|---|---|---|---|
| OpenAI | 5.6+：30m 滑动（写/复用刷新）；旧模型 in_memory 5–10min≤1h；非 ZDR 默认 24h 档 | 5.6+：1.25×；旧模型免费 | 5.6+：0.1×；旧模型 0.1–0.5× | 无 [1] |
| Anthropic | 默认 5m，`"ttl":"1h"` 延长；命中免费刷新；长 TTL 须排短 TTL 前 | 5m=1.25×；1h=2× | 0.1×（Fable5.1/Mythos5.1=0.025×，Opus5.5=0.05×） | 无 [2] |
| Gemini implicit | 未公布（OpenRouter 实测口径：均 3–5min、读不刷新） | 无 | 0.1× | 无 [3][10] |
| Gemini explicit | 默认 1h，无上下限（Vertex ≥1min） | 输入按原价 | 0.1×（Vertex：2.5+ 90% 折扣、2.0 75%） | $4.50(2.5 Pro)/$1.00(2.5F)/1M tok·hr [3][11] |
| DeepSeek | 闲置自动清除，「通常几小时到几天」 | 无 | 命中=miss 的 1/50（flash）、1/30（v4-pro）；峰谷半价 | 无 [4] |
| Kimi | 5m/1h 两档，默认 5m，命中续期 | K3：5m=1×、1h=2×；K2 见 §5⚔ | 1/10 | 无 [7] |
| 智谱 | 未公布 | 无 | 逐模型命中价≈5 折（GLM-5.3 ¥2/M）；仅标准 API 计费 | 有「存储费」列，限时免费 [9] |
| 通义千问 | 显式 5m 命中重置；隐式不定期清理 | 显式=+25%；隐式无 | 显式省 90%；隐式 20% 价 | 无 [8] |
| OpenRouter | 不翻译 TTL；粘性会话 10min 无活动过期 | 上游透传 | 上游透传，推理无加价 | 上游透传 [10] |

**D5+D8 命中确认·隔离**

| 厂商 | usage 字段 | 隔离 |
|---|---|---|
| OpenAI | Responses `input_tokens_details.cached_tokens`/`cache_write_tokens`；CC `prompt_tokens_details.*` | 不跨 org/region；`prompt_cache_key` 分隔用户防 probing [1] |
| Anthropic | `cache_read_input_tokens`、`cache_creation_input_tokens`+`cache_creation{5m,1h}` 细分 | org 隔离；Claude API/Claude Platform on AWS/Foundry 到 workspace 级；Bedrock/GCP 仅 org 级 [2] |
| Gemini | `usageMetadata.cachedContentTokenCount`（两机制同字段） | Vertex：project 级+VPC-SC；AI Studio 侧未写 [3][11] |
| DeepSeek | `prompt_cache_hit_tokens`/`prompt_cache_miss_tokens` | 用户间隔离；`user_id` 可再分 [5][6] |
| Kimi/智谱/Qwen | `prompt_tokens_details.cached_tokens`（Qwen 的 Anthropic 端点为 `cache_read_input_tokens`） | Kimi org 内共享；Qwen 账号+模型隔离；智谱未写 [7][8][9] |
| OpenRouter | 归一 `cached_tokens`/`cache_write_tokens`+`cache_discount`；GET /generation 有 `native_tokens_cached` | 粘性键=首条 system+首条非 system 消息哈希；可传 `session_id`(≤256字符)/`prompt_cache_key` [10] |

## 3. 变体与适配层

- **托管平台同构不同名**：Bedrock Converse 用 `cachePoint` 块（Claude 走 InvokeModel 仍用 `cache_control`），Nova 默认隐式，usage 为 `cacheReadInputTokens`/`cacheWriteInputTokens`；Azure OpenAI 与 OpenAI 同机制（默认自动、≥1024、GPT-5.6+ 才有 `prompt_cache_breakpoint`/`ttl:"30m"`，旧模型传参报 400）；Vertex=Gemini 同对象模型，差异在 project 级 `cacheConfig` 开关、VPC-SC、存储计费 [11][13]。
- **Anthropic 双模式**：顶层 `cache_control`（auto，legacy Bedrock 除外，其上 400 需逐块）与逐块断点可混用，auto 占一个断点槽；`max_tokens:0` 可预热（需显式断点）[2]。
- **OpenAI 两代口径**：GPT-5.6+ 走 `prompt_cache_options.ttl`("30m")；旧模型靠 `prompt_cache_retention`("24h"，spec 已标 deprecated 但 ttl 仅 5.6+ 可用）[1]。
- **阿里三种缓存**：隐式（不可关）+显式 `cache_control`（与隐式互斥）+Session 缓存（请求头 `x-dashscope-session-cache: enable` 开启、system+user prompt 字符级精确匹配、≥1024 tok、响应 id 7 天）[8]。
- **OpenRouter 翻译规则**：`prompt_cache_breakpoint` 转 Anthropic/Google 时补默认 5m `cache_control`；发向 OpenAI 时 ttl 丢弃；Bedrock 顶层字段转尾部断点 [10]。

## 4. 用户需要知道的坑

- **前缀逐 token 相同才命中**（从第 0 token 起）：改 system、tools、消息中段任意字节，其后全部失效；阿里显式连「遗漏/新增一个空的可选字段」都失效；Anthropic 分层失效（改 tools 全灭，改 tool_choice/images 只灭 messages）[2][4][8]。
- **低于门槛静默不缓存**，不报错（Anthropic 两字段均为 0）[2]。
- **写溢价要摊回**：Anthropic 写 1.25–2×、Qwen 显式写 1.25×、Kimi K3 1h 档 2×，只命中一次未必回本；命中续期才划算 [2][7][8]。
- **并发首请求不命中**：Anthropic 缓存要等首个响应开始才可用；智谱异步生效、稍等再发后续请求 [2][9]。
- **路由**：OpenAI >15 rpm 会 overflow 掉出缓存机；`prompt_cache_key` 兼做路由/分账/隔离 [1]。OpenRouter 手动 `provider.order` 关粘性→换 provider 即 miss [10]。
- **cached tokens 仍占上下文窗口**（Gemini）、**仍计 TPM 限额**（OpenAI）[1][10]。
- **排障工具**：OpenAI Prompt Cache Diagnostics（dashboard+comparison_response_id）、Anthropic `diagnostics` 对象（报前缀分歧点）[1][2]。

## 5. 未决与置信度

- **Kimi K2 矛盾未裁决**：api/chat.md schema 称 `prompt_cache_options` 不传时默认开启写入（无 per-model 限制），指南却称 k2.6/k2.7「不支持 Cache Write」；自洽解读：K2 自动命中但无可计费写入，官方无明文 [7]。
- **官方未写（∅）**：智谱 TTL/隔离；Gemini implicit TTL；Kimi 块大小；阿里 Session 缓存定价与 TTL；DeepSeek SWA 后切分间隔（「64 token」为 2024 旧口径）。
- **时效风险**：Gemini implicit 门槛与折扣均上调过（Flash 1024→2048；75%→90%）；DeepSeek 机制经 SWA 改版；旧文流传需对日期。
- 阿里 session 页自相矛盾（"改 user 归零" vs "前缀匹配不影响"），未裁决 [8]。

## 来源

[1] OpenAI Prompt Caching guide + OpenAPI spec — https://developers.openai.com/api/docs/guides/prompt-caching
[2] Anthropic Prompt caching + Release notes — https://docs.claude.com/en/docs/build-with-claude/prompt-caching
[3] Gemini caching docs/API/pricing — https://ai.google.dev/gemini-api/docs/caching ; https://ai.google.dev/api/caching
[4] DeepSeek KV cache guide + 定价 — https://api-docs.deepseek.com/guides/kv_cache ; https://api-docs.deepseek.com/quick_start/pricing
[5] DeepSeek context caching 公告 — https://www.deepseek.com/en/news/context-caching/
[6] DeepSeek create-chat-completion — https://api-docs.deepseek.com/api/create-chat-completion
[7] Kimi context caching + api/chat — https://platform.kimi.com/docs/guide/context-caching
[8] 阿里云百炼 context-cache 等三页 — https://help.aliyun.com/zh/model-studio/context-cache
[9] 智谱 cache 指南 + 定价页 — https://docs.bigmodel.cn/cn/guide/capabilities/cache ; https://docs.bigmodel.cn/cn/guide/start/pricing
[10] OpenRouter prompt caching — https://openrouter.ai/docs/guides/best-practices/prompt-caching
[11] Vertex AI context cache overview — https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview
[12] OpenRouter Response Caching — https://openrouter.ai/docs/guides/features/response-caching
[13] Bedrock / Azure prompt caching — https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html ; https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching
