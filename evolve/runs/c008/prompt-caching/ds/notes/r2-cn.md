# r2-cn
question: 核验国内三家缓存的 3 个遗留点：(a) Kimi "不支持 Cache Write" vs K2 缓存命中价的真实语义；(b) 智谱 cache 页缺失的 TTL/隔离/支持模型在站内其他页是否存在；(c) 阿里 x-dashscope-session-cache 命中规则/TTL/计费 + 显式缓存失效条件原句。
checked: https://platform.kimi.com/docs/guide/context-caching.md, https://platform.kimi.com/docs/pricing/chat.md, https://platform.kimi.com/docs/llms.txt, https://platform.kimi.com/docs/changelog/index.md, https://platform.kimi.com/docs/guide/kimi-k2-7-code-quickstart.md, https://platform.kimi.com/docs/api/chat.md, https://platform.moonshot.ai/docs/guide/context-caching.md (301→platform.kimi.ai), https://platform.kimi.ai/docs/guide/context-caching.md, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://docs.bigmodel.cn/llms.txt, https://docs.bigmodel.cn/cn/guide/start/pricing.md, https://docs.bigmodel.cn/api-reference/模型-api/对话补全.md, https://docs.bigmodel.cn/cn/update/new-releases.md, https://docs.bigmodel.cn/cn/coding-plan/faq.md, https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses, https://help.aliyun.com/zh/model-studio/explicit-cache-best-practice

## claims

### (a) Kimi
- [C1] context-caching 指南 FAQ 唯一模型级表述：`kimi-k3` 支持 Cache Write，k2.7/k2.7-highspeed/k2.6 不支持 | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "`kimi-k3` 支持 Cache Write；`kimi-k2.7`、`kimi-k2.7-highspeed`、`kimi-k2.6` 不支持。" | type: official
- [C2] 定价页 K2 表只有"输入价格（缓存命中）/（缓存未命中）"两列，无缓存写入列；k2.6 命中价 ¥1.10、k2.7-code ¥1.30、k2.7-code-highspeed ¥2.60（/1M） | src: https://platform.kimi.com/docs/pricing/chat.md | quote: "kimi-k2.6 | 1M tokens | ¥1.10 | ¥6.50 | ¥27.00 | 262,144 tokens" | type: official
- [C3] 定价页注释把"缓存写入按 TTL 档位计费"限定在 K3 | src: https://platform.kimi.com/docs/pricing/chat.md | quote: "对于 K3 系列模型，缓存写入按 TTL 档位（5min / 1h）单独计费；缓存命中的输入仅按缓存命中价格计费" | type: official
- [C4] 定价页称缓存整体自动启用（未限定模型） | src: https://platform.kimi.com/docs/pricing/chat.md | quote: "Kimi API 对重复的请求前缀自动启用上下文缓存" | type: official
- [C5] 指南称默认按 5m 写入（未限定模型范围） | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "不传 `prompt_cache_options` 时，系统默认使用 `5m` TTL：满足命中条件的前缀会自动写入并尝试复用" | type: official
- [C6] chat.md 的 prompt_cache_options 在共享 schema，适用全部列出模型，无 per-model 限制 | src: https://platform.kimi.com/docs/api/chat.md | quote: "上下文缓存写入选项。不传时默认开启缓存写入（5m 档）：系统自动将请求前缀写入 5m 档缓存" | type: official
- [C7] 缓存按组织隔离 | src: https://platform.kimi.com/docs/api/chat.md | quote: "缓存以组织（org）为粒度隔离，组织之间不共享缓存。" | type: official
- [C8] TTL 仅 5m/1h 两档、mode 仅 implicit、不支持手动清除 | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "`prompt_cache_options.mode` 当前仅支持 `implicit`，`ttl` 支持 `5m` 和 `1h`。" | type: official
- [C9] 英文站 platform.moonshot.ai 301 重定向到 platform.kimi.ai；英文页 FAQ 与中文完全相同，未解释 K2 能否读命中 | src: https://platform.kimi.ai/docs/guide/context-caching.md | quote: "`kimi-k3` supports Cache Write; `kimi-k2.7`, `kimi-k2.7-highspeed`, and `kimi-k2.6` do not." | type: official
- [C10] changelog 无 K3-only Cache Write 或 K2 读命中说明；缓存史：2024-07 公测、2024-11 全量放开+"Cache 续期不再收取创建费用"、2025-10"下线手动 Cache 展示功能" | src: https://platform.kimi.com/docs/changelog/index.md | quote: "Context Caching 功能放开给全量用户，Cache 续期不再收取创建费用" | type: official
- [C11] 命名不一致：指南写 kimi-k2.7/kimi-k2.7-highspeed，定价页写 kimi-k2.7-code/kimi-k2.7-code-highspeed；k2.7-code quickstart 全文未提缓存 | src: https://platform.kimi.com/docs/guide/kimi-k2-7-code-quickstart.md | quote: （页面无 cache 字样） | type: official

### (b) 智谱
- [C12] cache 指南无 TTL/隔离/模型清单；命中价约标准价 50%；建议前缀 ≥500 Token；"缓存为异步生效" | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "缓存命中 Token：按优惠价格计费（通常为标准价格的 50%）" | type: official
- [C13] cache 指南明示仅标准 API 适用 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "仅适用于标准 API 计费，不包括资源包和 GLM Coding Plan 套餐。" | type: official
- [C14] 定价页给出按模型的缓存命中价（GLM-5.3 ¥2/M、GLM-5.3-Flash ¥0.23/M 等）+ "缓存存储（元/百万 Tokens/小时）"列（限时免费）；部分型号标"不支持"（GLM-4-AirX、GLM-Z1 系列等）→ 构成事实上的支持模型清单 | src: https://docs.bigmodel.cn/cn/guide/start/pricing.md | quote: "缓存存储当前限时免费。本页暂不展示免费期结束后的标准价格" | type: official
- [C15] 计费公式含独立缓存存储费 | src: https://docs.bigmodel.cn/cn/guide/start/pricing.md | quote: "调用费用 = 未命中缓存的输入费用 + 缓存命中费用 + 输出费用 + 缓存存储费用" | type: official
- [C16] 对话补全 API ref 唯一缓存字段是 usage.prompt_tokens_details.cached_tokens | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全.md | quote: "命中的缓存 Token 数量" | type: official
- [C17] new-releases changelog 全文无上下文缓存条目（仅 GLM-5.3-Flash 架构 KV 缓存）；coding-plan/faq 无缓存字样 | src: https://docs.bigmodel.cn/cn/update/new-releases.md | quote: "计算量与 KV 缓存较 GLM-5.3 大幅降低" | type: official

### (c) 阿里
- [C18] 开启方式 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses | quote: "只需在请求头中添加 `x-dashscope-session-cache: enable`（默认值为 disable）" | type: official
- [C19] "精确匹配"=system+user prompt 共同作缓存键、字符级相等 | src: 同上 | quote: "system prompt 与 user prompt 共同构成缓存键，其中任意一项变更都会导致本轮请求不命中缓存。" | type: official
- [C20] 严格度：任意字符变更归零、追加/语义相似均不命中 | src: 同上 | quote: "system prompt 或 user prompt 的任意字符变更（包括空格和标点）都会使 `cached_tokens` 归零。" | type: official
- [C21] system prompt 前缀独立缓存，previous_response_id 不在其缓存键 | src: 同上 | quote: "仅变更 `previous_response_id` 时，system prompt 前缀部分仍然命中缓存" | type: official
- [C22] 最小可缓存 1024 Token，多轮累积超过后才创建 | src: 同上 | quote: "低于该阈值的输入不会触发缓存创建；多轮对话中累积上下文超过 1024 Token 后才会开始创建缓存。" | type: official
- [C23] 缓存本体无明确 TTL 文字；仅响应字段 ephemeral_5m_input_tokens（"5 分钟临时缓存新创建的 Token 数"）、cache_type 固定 ephemeral；响应 id 有效期 7 天 | src: 同上 | quote: "5 分钟临时缓存新创建的 Token 数" | type: official
- [C24] 页面无 Session 缓存计费说明，仅称降低"推理延迟与成本"；监控用 usage.input_tokens_details.cached_tokens | src: 同上 | quote: "无需改动业务代码即可降低多轮对话的推理延迟与成本" | type: official
- [C25] 显式缓存：content 须数组形式加 cache_control {"type":"ephemeral"}；与隐式互斥；≥1024 Token；≤4 个标记；最长前缀匹配、"前缀完全一致"、"100% 确定性命中" | src: https://help.aliyun.com/zh/model-studio/explicit-cache-best-practice | quote: "同一请求只能使用一种缓存模式" | type: official
- [C26] 显式缓存 TTL | src: 同上 | quote: "缓存有效期为 5 分钟，每次命中自动续期" | type: official
- [C27] 失效条件原句（tools） | src: 同上 | quote: "Tools 定义是 System Prompt 的一部分参与缓存计算，如果 Tools 改变则无法命中缓存" | type: official
- [C28] 失效条件原句（工具字段） | src: 同上 | quote: "不要遗漏或新增字段，即使该字段为空或可选" | type: official
- [C29] 截断粒度限制 | src: 同上 | quote: "多条 system message 会被内部合并为一个整体，也无法在中间截断"；"Qwen3.5 及之后的模型仅支持消息级别的缓存截断点" | type: official
- [C30] 显式缓存计费 | src: 同上 | quote: "首次写入缓存仅产生标准价格 25% 的额外开销，后续命中可节省 90% 成本" | type: official

## conflicts
- [K1] chat.md 共享 schema 称 prompt_cache_options "不传时默认开启缓存写入（5m 档）"且未列 per-model 限制（schema 覆盖 k3/k2.7-code/k2.6）vs 指南 FAQ "kimi-k2.7…kimi-k2.6 不支持"。最自洽解读：K2 有自动命中（故定价页有命中价）但无 K3 式可计费/可选 TTL 的 Cache Write；但无任何页面明说 K2 能读命中——裁决依据不足。
- [K2] Aliyun session 页内部矛盾：规则段 "system prompt 或 user prompt 的任意字符变更…都会使 `cached_tokens` 归零" vs 机制段 "Session 缓存基于系统提示词前缀匹配…修改 user prompt 不影响命中"。同页两说，未裁决。
- [K3] 模型命名：指南"kimi-k2.7/kimi-k2.7-highspeed" vs 定价页"kimi-k2.7-code/kimi-k2.7-code-highspeed"。

## gaps
- Kimi：K2 系列能否命中缓存（读）无官方明示；查过 context-caching(中/英)、pricing/chat、api/chat、changelog、k2.7-code-quickstart、llms.txt。
- 智谱：缓存 TTL 具体值与隔离范围仍未见文档；查过 capabilities/cache、pricing、对话补全 API ref、new-releases、coding-plan/faq、llms.txt（2026-09-25）。
- 阿里 session 缓存：无独立定价数字、无明确 TTL 文字（仅 ephemeral_5m 字段暗示 5 分钟）。

## leads
- Kimi prompt_cache_key 字段对 Kimi Code Plan 必填以提高命中率（api/chat.md）。
- 智谱"缓存存储 元/百万Tokens/小时"列暗示按小时计存储费（现限时免费），TTL 可能与此挂钩。
