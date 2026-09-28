# Taxonomy grid v2

v1→v2：分类轴不变。Kimi 的 Chat 归入 I（默认写入但调用方可以不传字段），Messages 兼容接口归入 II。百炼同时有 I 和 II，且官方写明互斥。Kimi 2024 的 `POST /v1/caching` 不再算现行 III。OpenRouter 定为 IV。计费里「默认写入是否另收费」不新开维度。

| 家族 | 判据 | 成员 |
|---|---|---|
| I 隐式前缀 | 可以不带缓存字段 | OpenAI 默认、DeepSeek、Gemini implicit、智谱、百炼隐式、Kimi Chat |
| II 请求内标记 | 要出现标记才按断点写 | Anthropic、百炼显式、Kimi Messages、OpenAI 5.6+ 可选 |
| III 独立资源 | 先创建对象再引用 | Gemini explicit。Kimi 旧 `/v1/caching` 已 404 |
| IV 网关 | 只做路由和字段互译 | OpenRouter |

| 实体 | 家族 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | 笔记 |
|---|---|---|---|---|---|---|---|---|---|---|
| ★ OpenAI | I + 可选 II | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | r1-openai，r2-verify-openai |
| ★ Anthropic | II | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | r1-anthropic，r2-verify-anthropic |
| ★ Gemini implicit | I | ✅ | ✅ | ✅ | ∅ | ✅ | ✅ | ∅ | ✅ | r1-gemini |
| ★ Gemini explicit | III | ✅ | ✅ | ∅ | ✅ | ✅ | ✅ | ✅ | ✅ | r1-gemini |
| ★ DeepSeek | I | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | r3-deepseek-price。现行指南无 64，旧新闻不再当门槛 |
| ★ Kimi | I + II | ✅ | ✅ | ∅ | ✅ | ✅ | ✅ | ✅ | ✅ | r3-kimi-price。K3 表头已核对；K2 写入费 ∅ 写在 D5 注里 |
| ★ 智谱 | I | ✅ | ⚔ | ✅ | ∅ | ⚔ | ✅ | ⚠ | ∅ | r2-zhipu。D5 指南 50% 对定价页 |
| ★ 通义/百炼 | I + II | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | r2-bailian。Session TTL ∅ |
| ★ OpenRouter | IV | ✅ | ✅ | — | ✅ | ∅ | ✅ | — | ✅ | r2-openrouter。网关加价 ∅；上游转述不作厂商事实 |
| Azure OpenAI（变体） | | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | 未摘 |
| Vertex Gemini（变体） | | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | 未摘 |
| Bedrock Claude（变体） | | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | 仅 legacy 顶层 400，见 Anthropic |

OpenAI D2 只剩回看窗口个数。DeepSeek D3/D5 已按现行指南和定价页表头核对，64 token 只留在旧新闻。智谱 D2、D5 仍是中英或指南/定价页冲突。OpenRouter 的 D3/D7 用 —：门槛和失效属于上游。
