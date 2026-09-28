# Taxonomy grid v1

v0→v1：分类轴从「生命周期由谁持有」收成「不传任何缓存字段时，会不会产生 cache read」。原因：用户的主问题是要不要改代码；OpenAI 5.6+ 与 Anthropic 都有「自动断点 + 可选显式断点」，互斥的四家族装不下，默认路径仍能归类。

| 家族 | 判据 | 成员 |
|---|---|---|
| F1 自动前缀 | 不传缓存字段也会 cache read；边界由服务端放在前缀上 | OpenAI（默认）、DeepSeek、Gemini 隐式 |
| F2 请求内声明 | 完全不带缓存字段则不产生 cache read；字段可以只放顶层，由服务端移动断点 | Anthropic |
| F3 缓存对象 | 先创建可引用资源，再在生成请求里引用 | Gemini 显式 `cachedContents` |
| F4 网关 | 前缀缓存在上游；网关另做路由粘性和整响应缓存 | OpenRouter |

混合体不新开家族：OpenAI 5.6+ 另有 `mode=explicit`；Anthropic 的 automatic 仍要顶层 `cache_control`。

维度不变：D1 谁持有边界；D2 请求字段；D3 最小单位与放置；D4 失效；D5 寿命与存储费；D6 命中计费；D7 如何确认命中；D8 覆盖面。

| 实体 | 家族 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 |
|---|---|---|---|---|---|---|---|---|---|
| OpenAI | F1 | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ |
| Anthropic | F2 | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini 隐式 | F1 | ✅ | ✅ | ✅ | ❓ | ❓ | ❓ | ⚔ | ✅ |
| Gemini 显式 | F3 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| DeepSeek | F1 | ✅ | ✅ | ⚔ | ✅ | ⚔ | ✅ | ✅ | ⚔ |
| Kimi | ? | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| 智谱 | ? | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| 通义千问 | ? | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| OpenRouter | F4 | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ |

⚔ 位置：OpenAI D5 = `prompt_cache_options.ttl` 只写 `30m`，与 `prompt_cache_retention` 的 `24h` / your-data 的 extended 说法冲突。Anthropic D1 = thinking 与 mid-conversation 对「没有 cache_control」是否缓存冲突。Gemini 隐式 D7 = `usage.total_cached_tokens` 与 `usage_metadata` 未点名子字段。DeepSeek D3 = 2024 新闻 64 token 与现行「完整匹配前缀单元」。DeepSeek D5 = 新闻写存储不收费，现行价目无存储行。DeepSeek D8 = 2026-09-14 后 v4-pro 是否仍按 Pro 价。OpenRouter D5 = 同一页对 Gemini 隐式 TTL/存储自相矛盾。

本轮未把 scout 的 Azure / Bedrock / 方舟 / MiniMax 写入格子。
