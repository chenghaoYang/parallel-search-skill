# grid v1（R2 收束后）

## 分类轴 v1（替换 v0；v0 的「网关透传」保留，「自动/显式/网关」三分改为按「零配置默认是否缓存」二分 + 双模可选层）
主轴：**不加任何缓存相关参数发请求，默认会不会缓存？**
- 家族 A 自动默认（6/8）：OpenAI、DeepSeek、Kimi、智谱、Gemini（implicit 部分）、通义千问（implicit 部分）——implicit 对 Gemini/Qwen 是各自默认且无法关闭的那一半。
- 家族 B 声明式默认（1/8，四大里唯一）：Anthropic——不加 `cache_control` 字段完全不缓存，2026-02-19 新增的"自动缓存"只是省去手动选断点位置，仍要加字段。
- 类别 C 网关透传：OpenRouter——不是独立第三种机制，行为=转发到的底层是 A 还是 B。

副轴（叠加在 A 之上）：**是否额外提供一个可选的显式/预留缓存模式？**
- 有：Gemini（cachedContents 独立付费资源）、通义千问（explicit cache，创建付 125%）、OpenAI（GPT-5.6+ 可选 explicit 断点标记，不创建独立付费资源）。
- 无（或已撤下）：DeepSeek、智谱；Kimi 2024 年曾有 `POST /v1/caching` 显式机制，2026 年现行文档已看不到，官方未公布切换时间。

理由：v0 的三分类无法解释「Gemini/Qwen 明明有 explicit 却默认还是自动」这类差异；换成「零配置默认」为主轴后，直接对应用户疑点#1（"现在还是这样吗"→ 是，Anthropic 仍是唯一默认不缓存的）。

## 网格（entity × 9 维度，最终状态）
| entity | trigger | min_len | discount | ttl | storage | confirm | invalidate | scope | api |
|---|---|---|---|---|---|---|---|---|---|
| openai | ✅ 自动默认+可选explicit | ✅ 1024(GPT-5.6+) | ✅ 0.1x读/1.25x写 | ✅ 30m复用窗口+独立24h retention | ✅ 单机不跨region | ✅ cached_tokens | ✅ 整前缀匹配 | ✅ 绑定org | ✅ 无独立API |
| anthropic | ✅ 声明式，须加cache_control | ✅ 512/1024/4096按模型 | ✅ 0.1x/0.05x/0.025x读,1.25x/2x写 | ✅ 5m默认/1h可选 | ❓ 未公开 | ✅ cache_read/creation_input_tokens | ✅ 层级+最多4断点 | ⚠ 不跨org，key级未写 | ✅ 无独立API |
| gemini | ✅ implicit自动+explicit手动资源并存 | ✅ 2048或4096按模型 | ✅ 均~90%off(ai.google.dev确认) | ✅ explicit默认1h可调/implicit 24h自动清 | ✅ explicit按小时收费(如$0.50~1.00/M/h) | ✅ cachedContentTokenCount | ⚠ prefix级，细粒度未写 | ✅ 绑定project/location/模型版本 | ✅ 完整CRUD |
| deepseek | ✅ 全自动 | ✅ 64 tokens | ✅ 现价分档~95-98%off | ✅(vague) 数小时到数天,best-effort | ✅ 硬盘(MLA压缩KV) | ✅ hit/miss_tokens | ✅ 全前缀匹配 | ✅ 按user_id隔离 | ✅ 无独立API |
| kimi | ✅ 全自动(2024显式机制已消失) | ✅ 256 tokens(K3) | ✅ 90%off | ✅ 默认5m/可选1h | ❓ 未公开 | ✅ 分字段报告(精确字段名未获取) | ✅ 含"改reasoning_effort失效" | ❓ 未公开 | ✅ 无独立API(旧cache_id已不可见) |
| zhipu | ✅ 隐式自动 | ✅ 建议500+ tokens | ⚔ 指南写50%，定价表实为71-75%off，以定价表为准 | ∅ 官方未写(查过guide+pricing两页) | ⚠ 存储费用项存在(限时免费)，机制未公开 | ✅ cached_tokens | ∅ 官方未写 | ∅ 官方未写 | ⚠ 无独立API(推断) |
| qwen | ✅ implicit自动(不可关)+explicit可选(互斥) | ✅ explicit最少1024 | ✅ explicit创建125%/命中10%；implicit创建免费/命中20% | ✅ explicit 5m(命中刷新)/implicit无固定期 | ⚠ marker机制，介质未写 | ✅ cache_creation/cached_tokens | ✅ 工具变更/20block回看/须数组格式 | ❓ 未公开 | ⚠ 无独立CRUD API |
| openrouter | ✅ 透传：OpenAI/DeepSeek/Groq自动，Anthropic/Qwen需显式cache_control | ✅ 取决于底层 | ✅ 透传底层折扣(0.1x~0.5x不等) | ✅(近似) 官方称"最低30分钟"，取决于底层 | ✅ 无网关层缓存，纯代理 | ✅ 统一字段cached/cache_write_tokens/cache_discount | ✅ provider路由切换会致未命中 | ✅ session_id粘性路由 | ✅ 另有独立的Response Caching(非prompt cache) |

核心格子（trigger/discount/ttl/confirm）：8×4=32 格，全部 ✅ 或 ∅/⚔(已给出可用结论)，**无遗留 ❓**——达成 brief.md 完成标准。次核心格子里 5 个 ❓（anthropic.storage、kimi.storage、kimi.scope、zhipu.api细节、qwen.scope）留给「未决」章节，不再派工验证（非核心、已查过至少一轮）。
