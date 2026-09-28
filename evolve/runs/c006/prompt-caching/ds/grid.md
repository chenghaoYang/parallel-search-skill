# grid v1：实体 × 维度

## 分类轴（taxonomy 骨架）
**缓存边界由谁决定**：
- A 隐式/自动前缀：客户端零改动或仅一个开关（OpenAI implicit、Gemini 隐式、Anthropic 顶层 automatic caching、DeepSeek?、Kimi 新版?）
- B 手动断点：在内容块上打标记（Anthropic block 级 cache_control、OpenAI GPT-5.6+ prompt_cache_breakpoint）
- C 显式缓存对象：先建资源拿 name/id 再引用，按存储计费（Gemini CachedContent、Kimi 旧版?）
- D 网关透传：OpenRouter

v0→v1：OpenAI 不再纯自动（GPT-5.6+ 有 explicit）；Anthropic 不再纯手动（有顶层 automatic）。分类轴仍成立，但「一家=一类」不成立——按 API 行为分档更准确。

## 维度（列）
- D1 机制类型：自动 / 手动断点 / 显式对象 / 透传
- D2 最小触发 tokens
- D3 计费：写入溢价、命中读取折扣、存储费
- D4 TTL / 生命周期
- D5 命中确认字段：usage 字段原名
- D6 失效条件
- D7 代码改动量
- D8 适用限制

## 状态
| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 |
|---|---|---|---|---|---|---|---|---|
| OpenAI | ✅ 默认隐式+5.6起可选显式断点 | ✅ 1024(5.6+)/旧模型不定 | ✅ 写1.25×读0.1×(5.6+)/旧模型读最高90%off | ✅ 30m(5.6+)/in_memory 5-10m/24h | ✅ cached_tokens+cache_write_tokens | ✅ 前缀/参数/路由 | ✅ 零改动 | ⚠ pro系存疑⚔ |
| Anthropic | ✅ block级手动+顶层automatic(2026-02) | ✅ 512/1024/2048/4096按模型 | ✅ 写1.25×(5m)/2×(1h)读0.1×(部分模型0.025/0.05×) | ✅ 5m默认/1h可选/命中免费续 | ✅ cache_creation/cache_read_input_tokens | ✅ tools→system→messages层级 | ✅ 需加字段 | ✅ 全现役模型 |
| Gemini 显式 | ✅ CachedContent对象(Beta) | ⚠ 按模型、现页未单列 | ✅ 读折扣价+存储$/Mtok/h | ✅ 默认1h可自定无上限 | ✅ cachedContentTokenCount | ✅ 对象不可变 | ✅ 需建对象 | ✅ v1beta |
| Gemini 隐式 | ✅ 2.5+默认开 | ✅ 2048/4096按模型 | ✅ 命中~90%off无存储费 | ∅ 官方未写数值 | ✅ cachedContentTokenCount/total_cached_tokens | ⚠ 仅前缀建议无清单 | ✅ 零改动 | ✅ 2.5+ |
| DeepSeek | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Kimi | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| 智谱 GLM | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| 通义千问 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| OpenRouter | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

失败记录：r1-deepseek/r1-cn/r1-openrouter 两轮均被 429 限流杀掉（r1 + r1b 各一次）。R2 再派。
