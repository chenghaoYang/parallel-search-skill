# Brief（R0）

读者：要同时接多家大模型 API 的工程师。几分钟内要能决定：要不要改请求、命中后怎么对账、缓存能活多久、响应里看哪个字段、改哪类内容会失效。

截至：调研日 2026-09-24。成稿里的数字以工人打开的官方页原句为准，不沿用记忆中的旧价。

## 成稿要建立的认知

1. 各家不在一条设计上：先按「谁划缓存边界、状态以什么形态存在」分成家族，再比字段和价格。
2. 用户点名的疑点必须有明确结论（可以是「截至某页，官方仍如此」或「官方没写」）：
   - 听说 OpenAI 和 DeepSeek 自动缓存、不用改代码；Anthropic 必须手动打 `cache_control` 断点。现在还是这样吗？
   - 命中之后各家怎么计费？
   - 缓存能活多久？
   - 怎么确认命中了？
   - 哪些改动会让缓存失效？
   - Kimi、智谱、通义千问、OpenRouter 和上面四家有什么不同？

## 范围内

- OpenAI、Anthropic、Gemini（explicit context caching 与 implicit caching 分开）、DeepSeek。
- 国内：Kimi（月之暗面）、智谱、通义千问。
- 网关：OpenRouter。
- 同范围的确认命中、失效条件、计费、TTL、最小粒度、作用域。

## 范围外

- 自建 KV / prefix cache（vLLM 等推理框架内部），除非某家官方 API 文档把用户可见行为定义为依赖它。
- 提示词怎么写才能省钱的长教程（只保留会改变命中的规则）。
- 用户没点名的厂商不做全表；scout 只记 leads。R2 起只在 leads 证明「用户接 API 时会碰到、且和四家机制不同」时才加一行。

## 种子词

OpenAI prompt caching. Anthropic cache_control. Gemini context caching / implicit caching. DeepSeek 上下文硬盘缓存. Kimi 上下文缓存. 智谱 prompt cache. 通义千问 context cache. OpenRouter prompt caching.

## 完成标准

- 九行实体 × D1–D9：每格为 ✅ / ⚠ / ⚔ / ❓ / ∅ / — 之一，核心四家加 OpenRouter 不得停在未查的 ❓。
- 六个疑点在「一屏看懂」里各有一句带 `[n]` 的结论。
- `ds/report.md` 字符数 ≤ 9000，且不是一轮比一轮更长。
- 每个具体事实能追到笔记主张的官方（或标明二手）原句。
- 终审抽查 ≥ 20 条主张后改稿，最后一步是收束。

## 参数

rounds=3，workers=6，budget=9000，dir=`./ds`，工人模型 `grok-4.7`。无 pplx-safe。检索只能 web_search 找页、web_fetch 打开一手页。
