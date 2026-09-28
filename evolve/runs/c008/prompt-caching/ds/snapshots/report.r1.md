# 各家大模型 API 的 Prompt Caching 对比

> 回答：要不要改代码、命中怎么计费、缓存活多久、怎么确认命中、什么会让缓存失效。截至 2026-09-25，以官方文档为准；[n] 见文末来源。

## 0. 一屏看懂

- **机制三派**：全自动（OpenAI、DeepSeek、智谱、Gemini implicit、Qwen 隐式、Kimi）；请求内断点标记（Anthropic、Qwen 显式、OpenAI GPT-5.6+ explicit）；独立缓存对象（仅 Gemini explicit CachedContent，先 create 再引用、付存储费）[1][3][4][5][8][9]。
- **「Anthropic 必须逐 block 打 cache_control」已过时一半**：2026-02-19 起有 automatic caching——请求顶层加一个 `cache_control` 字段即可，系统自动移动断点。但缓存仍非默认开启：不加字段=不缓存。OpenAI/DeepSeek 才是零改动 [2][5]。
- **计费两派**：写收费+读便宜（Anthropic 写 1.25×/2×、读 0.1×；Qwen 显式写 125%/读 10%；Kimi 写 5m=原价/1h=2×、读 1/10；OpenAI GPT-5.6+ 写 1.25×/读 0.1×）vs 无写费只给读折扣（OpenAI 旧模型读 0.1–0.5×；DeepSeek 命中 1/30–1/50；智谱约 5 折；Gemini/Qwen 隐式读约 0.1–0.2×）。Gemini explicit 另收存储费 $0.5–4.5/1M tok·hr [1][2][3][5][7][8][9]。
- **TTL 两派**：固定窗口、命中免费续期（Anthropic 5m/可 1h；Kimi 5m/1h；Qwen 显式 5m；OpenAI GPT-5.6+ 30m 滑动）vs 不透明闲置清除（DeepSeek「几小时到几天」；智谱、Gemini implicit 未公布）[1][2][4][5][8]。
- **确认命中看 usage**：OpenAI 系 `…details.cached_tokens`；Anthropic 系 `cache_read_input_tokens`/`cache_creation_input_tokens`；Gemini `cachedContentTokenCount`；DeepSeek 另有 `prompt_cache_hit_tokens`/`prompt_cache_miss_tokens` [1][2][3][5][6]。
- **失效共性**：全部按「从第 0 个 token 起的最长前缀匹配」，改 system/tools/任何中段内容都会击穿其后所有内容；唯一例外是阿里 Session 缓存（整段精确匹配）[5][8]。
- **OpenRouter 不自建缓存**：做 `cache_control`↔`prompt_cache_breakpoint` 双向翻译+粘性路由，价格=上游透传无加价；手动 `provider.order` 会关掉粘性路由导致 miss [10]。

## 1. Taxonomy

分类轴 = **缓存以什么 API 形态暴露**：

| 家族 | 定义 | 成员 |
|---|---|---|
| A 隐式自动 | 服务端按前缀自动存取，请求无需任何字段 | OpenAI（默认）、DeepSeek、智谱、Gemini implicit、Qwen 隐式、Kimi |
| B 请求级标记 | 请求里放断点/开关字段，控制写位置与 TTL | Anthropic（顶层 auto + 逐块 explicit）、Qwen 显式 `cache_control`、OpenAI GPT-5.6+ `prompt_cache_breakpoint`、Kimi 的 Anthropic 端点顶层 `cache_control` |
| C 独立缓存资源 | 先 `POST /cachedContents` 建对象再按名引用，付存储费 | 仅 Gemini explicit（旧 Kimi `/v1/caching` 已随平台迁移下线） |
| D 网关翻译 | 自身不缓存，互译标记+路由保命中 | OpenRouter |

维度：D1 启用方式｜D2 最小前缀门槛｜D3 TTL｜D4 计费｜D5 命中字段｜D6 匹配/失效｜D7 断点/对象管理｜D8 隔离。

## 2. 对照矩阵

**D1+D2+D7 机制·门槛·管理**

| 厂商 | 默认开 | 启用方式 | 最小前缀 | 断点/对象 |
|---|---|---|---|---|
| OpenAI | 是 | 零字段；GPT-5.6+ 可加 `prompt_cache_options{mode,ttl,prewarm}`+`prompt_cache_breakpoint` | 1,024 tok（5.6+；旧模型随设置变） | 每请求≤4 写；lookup 最多 80 断点 [1] |
| Anthropic | 否 | 顶层 `cache_control`(auto) 或逐块 `{"type":"ephemeral"}` | 512–4,096 tok 按模型（Opus5.5=512，Sonnet系=1024，Haiku4.5=4096） | ≤4 断点；每断点 20-block lookback 读旧写 [2] |
| Gemini implicit | 是 | 零配置（2.5+ 默认开） | 2,048–6,144 按模型（2.5 Flash/Pro=2048；3.x Flash=4096/6144） | 无 [3] |
| Gemini explicit | — | `POST /v1beta/cachedContents`，请求里 `cachedContent` 引用 | 官方当前页未列（旧版 1024/2048） | list/get/patch/delete；patch 只改过期 [3] |
| DeepSeek | 是 | 零字段（`cache_control` 被 Ignored） | 按固定 token 间隔切分（数值未公布；2024 公告为 64） | 无管理 API [4] |
| Kimi | 是 | 隐式；`prompt_cache_options{mode:"implicit",ttl}`；Anthropic 端点顶层 `cache_control` 控写 | 块大小未公开 | 无 CRUD 端点 [7] |
| 智谱 | 是 | 零配置隐式 | 建议重复前缀 ≥500 tok | 无 [9] |
| 通义千问 | 隐式是 | 隐式不可关；显式在 messages 打 `cache_control`；Responses 另有 Session 缓存（`x-dashscope-session-cache` 头） | 隐式 1024（第三方部署 GLM/MiniMax 512） | 显式≤4 标记、仅 ephemeral [8] |
| OpenRouter | — | `cache_control`/`prompt_cache_breakpoint` 互译；TTL 不翻译 | 透传上游门槛 | Anthropic≤4；Gemini 只用最后一个 [10] |

**D3+D4 生命周期·计费**（倍数=相对该模型 input 原价）

| 厂商 | TTL | 写价 | 读价 | 存储费 |
|---|---|---|---|---|
| OpenAI | GPT-5.6+：30m 滑动（写/复用刷新）；in_memory 5–10min≤1h；非 ZDR 默认 24h 档（典型 30min≤24h） | 5.6+：1.25×；旧模型免费 | 5.6+：0.1×；旧模型 0.1–0.5× 按定价页 | 无 [1] |
| Anthropic | 默认 5m，`"ttl":"1h"` 可延长；命中免费刷新；长 TTL 须排短 TTL 前 | 5m=1.25×；1h=2× | 0.1×（Fable5.1/Mythos5.1=0.025×，Opus5.5=0.05×） | 无 [2] |
| Gemini implicit | 未公布（OpenRouter 实测称均 3–5min 且读不刷新） | 无 | 0.1×（=90% 折扣） | 无 [3][10] |
| Gemini explicit | 默认 1h，无上下限（Vertex ≥1min） | 输入按原价 | 0.1× | $4.50(2.5 Pro)/$1.00(2.5F)·/1M tok·hr [3] |
| DeepSeek | 闲置自动清除，「通常几小时到几天」 | 无 | 命中=miss 的 1/50（flash）、1/30（v4-pro）；另有峰谷半价 | 无 [4] |
| Kimi | 5m/1h 两档，默认 5m，命中续期；不可手动清 | k3：5m=1×、1h=2× | 1/10（k2.x 只见命中价，指南称其不支持写入⚔） | 无 [7] |
| 智谱 | 未公布 | 无 | 约 0.5×（仅标准 API 计费，Coding Plan 不适用） | 无 [9] |
| 通义千问 | 显式 5m 命中重置；隐式不定期清理 | 显式=125%；隐式无 | 显式 10%；隐式 20%（deepseek-v4.1-flash 10%） | 无 [8] |
| OpenRouter | 不翻译 TTL；粘性会话 10min 无活动过期 | 上游透传 | 上游透传，推理无加价 | 上游透传 [10] |

**D5+D8 命中确认·隔离**

| 厂商 | usage 字段 | 隔离 |
|---|---|---|
| OpenAI | Responses `input_tokens_details.cached_tokens`/`cache_write_tokens`；CC `prompt_tokens_details.*` | 不跨 org/region；`prompt_cache_key` 分隔用户防 probing [1] |
| Anthropic | `cache_read_input_tokens`、`cache_creation_input_tokens`+`cache_creation{5m,1h}` 细分 | org 隔离；API/AWS 平台/Fundry 到 workspace 级 [2] |
| Gemini | `usageMetadata.cachedContentTokenCount`（implicit/explicit 同字段） | Vertex：project 级+VPC-SC；AI Studio 侧未写 [3] |
| DeepSeek | `prompt_cache_hit_tokens`/`prompt_cache_miss_tokens` | 用户间隔离；`user_id` 可再分 [4][5] |
| Kimi/智谱/Qwen | `prompt_tokens_details.cached_tokens`（Qwen 的 Anthropic 端点为 `cache_read_input_tokens`） | Kimi org 内共享；Qwen 账号+模型隔离；智谱未写 [7][8][9] |
| OpenRouter | 归一为 `cached_tokens`/`cache_write_tokens`+`cache_discount`；GET /generation 有 `native_tokens_cached` | 粘性键=账户×模型×会话（`session_id`/`prompt_cache_key`）[10] |

## 3. 变体与适配层

- **Anthropic 双模式**：顶层 `cache_control`（auto，2026-02-19 起，legacy Bedrock 除外，其上返回 400 需逐块）与逐块断点可混用，auto 占一个断点槽；`max_tokens:0` 可预热（需显式断点）[2]。
- **OpenAI 两代口径**：GPT-5.6+ 走 `prompt_cache_options.ttl`("30m")/explicit breakpoint；旧模型靠 `prompt_cache_retention`("24h"，spec 已标 deprecated 但 ttl 仅 5.6+ 可用）——文档口径交错 [1]。
- **阿里三种缓存**：隐式（不可关）+显式 `cache_control`+Session 缓存（响应头开启、整段精确匹配）[8]。
- **OpenRouter 翻译规则**：`prompt_cache_breakpoint` 转 Anthropic/Google 时补默认 5m `cache_control`；发向 OpenAI 时 ttl 被丢弃；Bedrock 顶层字段转尾部断点 [10]。

## 4. 用户需要知道的坑

- **前缀逐 token 相同才命中**（从第 0 token 起）：改 system、tools、消息中段任意字节，其后全部失效；Anthropic 分层失效（改 tools 全灭，改 tool_choice/images 只灭 messages）[2][4][5]。
- **低于门槛静默不缓存**，不报错（Anthropic 两字段均为 0）[2]。
- **写溢价要摊回**：Anthropic/Qwen 显式写 1.25–2×，只命中一次未必回本；命中续期才划算 [2][8]。
- **并发首请求不命中**：Anthropic 缓存要等首个响应开始才可用 [2]；智谱异步生效、稍等再发后续请求 [9]。
- **OpenAI 路由**：>15 rpm 会 overflow routing 掉出缓存机；`prompt_cache_key` 既做路由/分账也做隔离 [1]。OpenRouter 手动 `provider.order` 关粘性→换 provider 即 miss [10]。
- **cached tokens 仍占上下文窗口和 TPM**（OpenAI/Gemini）[1][10]。
- **排障工具**：OpenAI Prompt Cache Diagnostics、Anthropic `diagnostics` 对象（报前缀分歧点，已 GA）[1][2]。

## 5. 未决与置信度

- 智谱 TTL、隔离范围、官方支持模型清单：文档未写（∅）。Kimi 缓存块大小未公开；k2.x「不能写但能命中」的指南/定价页矛盾未裁决。Gemini implicit TTL 未公布（OpenRouter 称 3–5min 为网关侧实测口径）。DeepSeek SWA 后切分间隔未公布；「64 token」为 2024 旧口径。Gemini implicit 门槛与折扣均上调过（Flash 1024→2048；75%→90%），旧文仍流传需注意日期。
- Bedrock/Azure/Vertex 原生缓存为相邻 scope，未展开。

## 来源

[1] OpenAI Prompt Caching guide + OpenAPI spec — https://developers.openai.com/api/docs/guides/prompt-caching
[2] Anthropic Prompt caching + Release notes — https://docs.claude.com/en/docs/build-with-claude/prompt-caching
[3] Gemini caching docs/API/pricing — https://ai.google.dev/gemini-api/docs/caching ; https://ai.google.dev/api/caching
[4] DeepSeek KV cache guide + 定价 — https://api-docs.deepseek.com/guides/kv_cache ; https://api-docs.deepseek.com/quick_start/pricing
[5] DeepSeek context caching 公告 — https://www.deepseek.com/en/news/context-caching/
[6] DeepSeek create-chat-completion — https://api-docs.deepseek.com/api/create-chat-completion
[7] Kimi context caching + pricing — https://platform.kimi.com/docs/guide/context-caching
[8] 阿里云百炼 context-cache + explicit-cache-best-practice — https://help.aliyun.com/zh/model-studio/context-cache
[9] 智谱 cache 指南 — https://docs.bigmodel.cn/cn/guide/capabilities/cache
[10] OpenRouter prompt caching — https://openrouter.ai/docs/guides/best-practices/prompt-caching
