# grid v1 — 实体 × 维度

## 分类轴
轴 A「谁决定缓存位置」：A 零字段隐式自动（DeepSeek/智谱/Gemini implicit/通义隐式/OpenAI 默认）｜B opt-in 字段+自动落断点（Anthropic automatic、Kimi）｜C 手动断点（Anthropic explicit/GPT-5.6 explicit/通义显式）｜D 托管缓存对象（Gemini explicit、Kimi 旧 /v1/caching 已下线）。
轴 B「计费」：纯读折扣（A 类全部）｜写溢价+读折扣（Anthropic、GPT-5.6、通义显式、Kimi k3）｜存储按时计费（Gemini explicit）。

## 网格（v1 收束后）
| 实体 | D1 机制 | D2 门槛 | D3 计费 | D4 TTL | D5 命中字段 | D6 失效 | D7 模型 |
|---|---|---|---|---|---|---|---|
| OpenAI ≤5.5 | ✅ 自动默认开 | ✅ varies/128递增 | ✅ 读0.1x-0.5x无写费 | ✅ in_memory 5-10m/24h | ✅ cached_tokens | ✅ 前缀+tools等 | ✅ 4o+ |
| OpenAI 5.6+ | ✅ +显式breakpoint≤4 | ✅ 1024 | ✅ 写1.25x读0.1x | ✅ 30m可ttl | ✅ +cache_write_tokens+诊断 | ✅ | ✅ 5.6+ |
| Anthropic | ✅ automatic顶层cc/显式≤4块 | ✅ 512-4096分档 | ✅ 写1.25x/2x读0.1x(例外0.025/0.05x) | ✅ 5m默认/1h，命中续 | ✅ cache_creation/read_input_tokens+miss_reason | ✅ tools→system→messages层级 | ✅ 全现役 |
| Gemini implicit | ✅ 默认开 | ✅ 2048/4096分档 | ✅ 读=输入10% | ⚠ 未文档化(Vertex≤24h) | ✅ cachedContentTokenCount | ✅ 公共前缀 | ✅ 2.5+ |
| Gemini explicit | ✅ CachedContent对象 | ⚠ varies by model | ✅ 存储$0.5-4.5/1M·h+读10% | ✅ 默认1h无界可PATCH | ✅ 同上 | ✅ 不可变快照绑模型 | ✅ Beta most |
| DeepSeek | ✅ 全自动 | ⚠ 64tok(2024公告) | ✅ hit≈miss1/50峰谷价 | ✅ 数小时~数天 | ✅ prompt_cache_hit_tokens | ✅ 0号token起整单元 | ✅ flash/v4-pro |
| Kimi | ✅ 隐式+prompt_cache_options | ∅ 未公布 | ✅ k3写¥20/40,读¥2；k2读折扣无写费 | ✅ 5m/1h锁定续期 | ✅ cached_tokens | ✅ 前缀/org隔离 | ✅ k3写,k2读 |
| 智谱 | ✅ 隐式无开关 | ✅ 建议500+ | ✅ 命中≈50% | ∅ 未写 | ✅ cached_tokens | ✅ 长前缀 | ∅ 未写 |
| 通义隐式 | ✅ 自动无法关闭 | ✅ 1024(部分512) | ✅ 写免费读20% | ✅ 不定期清理 | ✅ cached_tokens | ✅ 不保证100% | ✅ 按地域清单 |
| 通义显式 | ✅ cache_control≤4 | ✅ 1024 | ✅ 写125%读10% | ✅ 5m命中重置 | ✅ +cache_creation | ✅ 最长前缀/tools参与 | ⚠ 清单指回主页 |
| OpenRouter | ✅ 断点互译TTL不译 | ✅ 随上游 | ✅ 透传+BYOK5% | ✅ 随上游 | ✅ usage+cache_discount | ✅ sticky 10min | ✅ 上游清单 |

⚔ 已裁决：OpenRouter 页 Gemini 门槛 1024/4096 vs 官方 2048/2048（2026-09-11 更新）→ 矩阵用官方；Gemini 2.5 Flash 门槛 1024→2048、折扣 75%→90% 为历史漂移，记 §5。
