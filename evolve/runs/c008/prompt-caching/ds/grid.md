# grid v1（R1 收束后）

## 分类轴（v1，不变）
缓存以什么 API 形态暴露：
- **A 隐式自动**：服务端按前缀自动存取，零字段（OpenAI 默认、DeepSeek、智谱、Gemini implicit、Qwen implicit、Kimi implicit）
- **B 请求级标记**：请求内放断点/开关字段（Anthropic 顶层 auto + 逐块 explicit、Qwen explicit、OpenAI GPT-5.6+ explicit、Kimi Anthropic 端点）
- **C 独立缓存资源**：create 一个 cache 对象再引用，付存储费（仅 Gemini explicit CachedContent；旧 Kimi /v1/caching 已下线）
- **D 网关翻译**：OpenRouter 互译 cache_control↔prompt_cache_breakpoint，缓存在上游

## 维度
D1 机制与启用 / D2 门槛与范围 / D3 TTL / D4 计费 / D5 命中字段 / D6 匹配与失效 / D7 断点与对象管理 / D8 隔离

## 状态网格
| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 |
|---|---|---|---|---|---|---|---|---|
| OpenAI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Anthropic | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini explicit | ✅ | ⚠(当前页未列最小值) | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠(仅Vertex) |
| Gemini implicit | ✅ | ✅(门槛上调过⚔) | ❓(未公布) | ✅ | ✅ | ✅ | — | ⚠(仅Vertex) |
| DeepSeek | ✅ | ⚠(64token为2024口径⚔) | ✅ | ✅ | ✅ | ✅ | ✅(无API) | ✅ |
| Kimi | ✅ | ❓(块大小未公开) | ✅ | ✅ | ✅ | ✅ | ✅(无CRUD) | ✅ |
| 智谱 | ✅ | ✅(定价页列不支持型号) | ∅(6页未见) | ✅(命中价+存储费列) | ✅ | ✅ | — | ∅ |
| 通义千问 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| OpenRouter | ✅(prompt缓存在上游;另有Response Caching) | ✅ | ✅(不译TTL) | ✅ | ✅ | ✅(粘性路由) | ✅ | — |
| Bedrock | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | — |
| Azure OpenAI | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | — |
| Vertex | ✅(implicit可关) | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ |

## 冲突/缺口待 R2
- ⚔ Kimi：指南称 k2.6/k2.7 不支持 Cache Write，定价页却列其命中价 → 反证/解读
- ⚔ DeepSeek 64-token 单元为 2024 口径，SWA 后数值未公布 → 记为时效差异
- ⚔ Gemini implicit 门槛上调过（1024→2048 Flash）；折扣 75%→90% → 带日期写
- ❓ 智谱 TTL/隔离；Gemini implicit TTL；Kimi 块大小 — 官方未写，记 ∅
- 边界主张待反证：「Anthropic 仍非默认开」「OpenAI 全自动默认开」「Kimi 无显式缓存对象 API」
