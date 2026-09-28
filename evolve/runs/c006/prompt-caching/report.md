# 各家大模型 API 的 prompt caching 对照

> 对比 OpenAI、Anthropic、Gemini、DeepSeek、Kimi、智谱 GLM、通义千问、OpenRouter 的上下文缓存：机制、计费、TTL、命中确认、失效条件。截至 2026-09-25，以官方文档为准。先读 §0 拿结论，细节查 §2。

## 0. 一屏看懂

1. **「OpenAI/DeepSeek 自动、Anthropic 必须手动」已过时。** Anthropic 2026-02-19 上线 automatic caching：请求顶层加一个 `cache_control` 字段，系统自动把断点放到最后一个可缓存 block [5][8]；反向地，OpenAI 在 GPT-5.6+ 引入了显式断点 `prompt_cache_breakpoint`（每请求最多 4 个 cache write）[1][3]。
2. **计费分两类**：按读写计费的（OpenAI 新模型写 1.25×、命中读 0.1×；Anthropic 写 1.25×(5m)/2×(1h)、读 0.1×）[1][6]；Gemini 显式缓存额外按 **存储时长** 收费（$0.5–4.5 / 1M tokens / 小时）[13]。
3. **TTL 差异大**：Anthropic 默认 5 分钟、可选 1h、命中免费刷新 [5]；OpenAI GPT-5.6+ 固定 30m，旧模型 `in_memory` 约 5–10 分钟、可选 `24h` 档 [1]；Gemini 显式缓存 TTL 自定、官方写明无上下限 [10]。
4. **确认命中看 usage 字段，各家字段名不同**：OpenAI `usage.*_tokens_details.cached_tokens`；Anthropic `cache_read_input_tokens`（写入看 `cache_creation_input_tokens`）；Gemini `usageMetadata.cachedContentTokenCount`；DeepSeek `prompt_cache_hit_tokens` [1][4][5][12]。
5. **最小触发门槛按模型分档**：OpenAI 1,024 tokens（GPT-5.6+，旧模型随请求设置浮动）[1]；Anthropic 512/1024/2048/4096 四档按模型 [5]；Gemini 2.5 系 2,048、3.x 系 4,096 [10]。不足门槛时 Anthropic 静默不缓存、不报错 [5]。
6. **失效的共性是前缀一致**：改模型、工具定义、参数（reasoning effort、verbosity 等）都会 miss [1][5]。Anthropic 按 tools→system→messages 层级失效——改工具定义全失效，改 tool_choice 只使 messages 段失效 [5]。

## 1. Taxonomy

**分类轴：缓存边界由谁决定。** 注意现在一家可以横跨多类，按 API 行为分档比按厂商分档准确：

| 家族 | 行为 | 成员 |
|---|---|---|
| A 隐式前缀 | 服务端按渲染前缀自动命中，客户端零改动 | OpenAI（默认）、Gemini 隐式（2.5+ 默认开）、Anthropic 顶层 `cache_control`（2026-02 起）、DeepSeek、Kimi（新版） |
| B 手动断点 | 请求里在内容块上打缓存标记 | Anthropic block 级 `cache_control`（≤4 个）、OpenAI `prompt_cache_breakpoint`（GPT-5.6+，≤4 个 write） |
| C 显式缓存对象 | 先建缓存资源拿 name/id，请求引用，按存储时长计费 | Gemini `CachedContent`（v1beta）、Kimi 旧版 context caching |
| D 网关透传 | 网关不持有缓存，差异在透传字段与路由 | OpenRouter |

维度定义：D1 机制；D2 最小可缓存 tokens；D3 计费（写入溢价/命中折扣/存储费）；D4 TTL；D5 命中确认字段；D6 失效条件；D7 代码改动量；D8 适用限制。

## 2. 对照矩阵

### 机制与门槛

| 实体 | 机制 | 最小 tokens | 需改代码 | TTL |
|---|---|---|---|---|
| OpenAI | 默认隐式；GPT-5.6+ 可选显式断点 [1] | 1,024（5.6+）；旧模型随请求设置 [1] | 零改动；可选 `prompt_cache_key`/`prompt_cache_retention`/`prompt_cache_options` [1] | 5.6+ 固定 30m；旧模型 in_memory ~5–10min（上限 1h）或 24h 档（~30min 典型）[1] |
| Anthropic | block 级 `cache_control`（≤4 断点）+ 顶层 automatic [5] | 512/1024/2048/4096 按模型分档 [5] | 必须加字段；`max_tokens:0` 可预热 [5][7] | 默认 5m，`"ttl":"1h"` 可选；命中免费刷新；从请求起始计时 [5][7] |
| Gemini 显式 | `cachedContents` 建对象按 name 引用（Beta）[10][11] | 按模型，现页未单列 [10] | 需建对象并传 `cachedContent` | 默认 1h，`ttl`/`expireTime` 自定，无上下界 [10][11] |
| Gemini 隐式 | 2.5+ 默认开，前缀匹配 [9] | 2,048（2.5 系）/4,096（3.x 系）[10] | 零改动 [9] | ∅ 官方未写具体值 |
| DeepSeek | ❓（自动硬盘缓存，R2 核实） | ❓ | ❓ | ❓ |
| Kimi | ❓ | ❓ | ❓ | ❓ |
| 智谱 GLM | ❓ | ❓ | ❓ | ❓ |
| 通义千问 | ❓ | ❓ | ❓ | ❓ |
| OpenRouter | ❓ 透传 | ❓ | ❓ | ❓ |

### 计费

| 实体 | 写入 | 命中读取 | 存储费 |
|---|---|---|---|
| OpenAI | GPT-5.6+ 1.25× 输入价；旧模型免费 [1] | 5.6+ 0.1×；旧模型 cached-input 价（如 gpt-5 $0.125 vs $1.25，90% off）[1][2] | 无 |
| Anthropic | 5m 写 1.25×；1h 写 2× base input [6] | 0.1×；Fable/Mythos 5.1 为 0.025×、Opus 5.5 为 0.05× [6] | 无 |
| Gemini 显式 | 建缓存按输入价计 + 存储费 [10] | "Context caching price"：如 2.5 Pro $0.125、2.5 Flash $0.03 [13] | $4.50（2.5 Pro）/$1.00（2.5 Flash）/$0.50（3.x Flash，至 2026-12-31）每 1M tok/h [13] |
| Gemini 隐式 | 无 | 命中自动按 ~90% 折扣让利，不保证命中 [9][14] | 无 |
| 其余 | ❓ R2 | | |

### 命中确认与失效

| 实体 | usage 字段 | 主要失效条件 |
|---|---|---|
| OpenAI | `input_tokens_details.cached_tokens`（Responses）/ `prompt_tokens_details.cached_tokens`（Chat Completions），另有 `cache_write_tokens` [1][4] | 前缀任一变化；改 model/tools/text.format/reasoning.effort 等；>15rpm overflow 路由；不跨组织/区域 [1] |
| Anthropic | `cache_read_input_tokens`（命中）、`cache_creation_input_tokens` + `cache_creation.ephemeral_5m/1h_input_tokens`（写入）；两者皆 0 = 未缓存 [5] | tools→system→messages 层级失效；改工具定义全失效；tool_choice/images 变化使 messages 失效 [5] |
| Gemini | `usageMetadata.cachedContentTokenCount`；Interactions API 为 `usage.total_cached_tokens` [9][12] | 显式：对象不可变，改内容须新建 [11]；隐式：前缀一致（无逐条清单） |
| 其余 | ❓ R2 | |

## 3. 变体与适配层

- **OpenAI 新旧两套机制并存**：旧模型只有隐式断点（按模型相关间隔放置、写缓存免费）；GPT-5.6+ 才有 `prompt_cache_breakpoint` 显式控制、30m 固定 TTL 和 1.25× 写入费 [1][3]。`prompt_cache_key` 只影响路由、不保证命中 [1]。
- **Anthropic 两种写法可混用**：顶层 automatic 断点占 4 个显式槽位之一，已有 4 个显式断点再开顶层会报 400 [5]。legacy Amazon Bedrock（Opus 4.6 及更早）不支持顶层字段 [5 笔记 leads]。
- **Gemini 显式仍在 Beta**（v1beta），缓存对象除过期时间外全部不可变，且只能用于创建时指定的模型 [11]；Interactions API 只支持隐式 [9]。
- OpenRouter 与各上游的透传关系：R2 补。

## 4. 用户需要知道的坑

- **前缀一致是硬条件**：缓存按渲染后的完整前缀匹配，任何改动（含 tools、system、参数）都 miss；把大的公共内容放开头、短时间内发相似前缀请求是官方建议 [1][9][5]。
- **OpenAI 命中率受路由影响**：缓存存于单机，>15 rpm 触发 overflow routing 会 miss；`prompt_cache_key` 改善路由但不保证命中 [1]。
- **Anthropic 断点浪费槽位**：自动断点占 4 槽之一；层级失效意味着工具定义改动使全部缓存失效；`ttl` 从请求开始而非响应结束计时 [5]。
- **OpenAI 命中的口径**：旧模型 cached_tokens 会减隐藏 system tokens 后向下取整到 128 的倍数——看到的数比预期小不代表没命中 [1]。
- **Gemini 隐式不保证省钱**：官方写明 "no cost saving guarantee"；要确定性省钱得用显式缓存（付存储费）[10][14]。
- **OpenAI 命中 token 仍计入 TPM 限流**，且不能手动清缓存 [1]；Anthropic 可 `max_tokens:0` 预热 [7]。

## 5. 未决与置信度

- DeepSeek、Kimi、智谱、通义千问、OpenRouter 五行 ❓：两轮工人都被限流杀掉，R2 补齐。
- OpenAI `*-pro` 系是否支持缓存：guide 列 gpt-5.5-pro 进 24h 名单，pricing 页 pro 系 cached-input 均为 "-"，⚔ 未裁决。
- Gemini 隐式 TTL 官方未写数值（仅 Vertex 侧文档称 24h 内删除，属不同产品）；隐式折扣从 75%→90% 的变更时间点未找到 changelog。
- Anthropic 最小分档表系现行文档值；旧资料的单一 1024 已过时。
- 旧模型确切最小 token 数、Batch/Realtime 缓存细节未取。

## 来源

[1] OpenAI Prompt Caching 指南 — https://developers.openai.com/api/docs/guides/prompt-caching
[2] OpenAI Pricing — https://developers.openai.com/api/docs/pricing
[3] OpenAI Changelog — https://developers.openai.com/api/docs/changelog
[4] openai-python usage 类型定义 — https://raw.githubusercontent.com/openai/openai-python/main/src/openai/types/completion_usage.py
[5] Anthropic Prompt caching — https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
[6] Anthropic Pricing — https://platform.claude.com/docs/en/about-claude/pricing
[7] Anthropic Messages API — https://platform.claude.com/docs/en/api/messages
[8] Anthropic API Release notes — https://platform.claude.com/docs/en/release-notes/api
[9] Gemini API Caching（隐式） — https://ai.google.dev/gemini-api/docs/caching
[10] Gemini 显式 context caching — https://ai.google.dev/gemini-api/docs/generate-content/caching
[11] Gemini cachedContents API — https://ai.google.dev/api/caching
[12] Gemini generateContent API — https://ai.google.dev/api/generate-content
[13] Gemini Pricing — https://ai.google.dev/gemini-api/docs/pricing
[14] Gemini Optimization — https://ai.google.dev/gemini-api/docs/optimization
[15] Gemini Changelog — https://ai.google.dev/gemini-api/docs/changelog
[16] Google 博客 implicit caching 上线 — https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/
