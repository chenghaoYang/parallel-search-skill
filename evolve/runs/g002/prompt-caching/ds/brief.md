# R0 brief

读者：已经在调一家或多家大模型 API、听过「有的自动缓存、有的要打 cache_control」的工程师。不是论文读者。要在几分钟内知道该改不改请求、命中后怎么付钱、缓存能活多久、怎么确认命中、改哪一下会失效。

成稿：`ds/report.md`，并同时写到仓库根 `report.md`。字符上限 9000（含来源节）。截至日期写进文首。层次按收束骨架：一屏看懂 → taxonomy → 对照矩阵 → 变体与适配层 → 坑 → 未决。

## 范围内

- OpenAI prompt caching
- Anthropic prompt caching / `cache_control`
- Gemini：implicit caching 与 explicit context caching（两行，同一厂商两种机制）
- DeepSeek 上下文缓存（含硬盘缓存说法）
- 国内：Kimi（Moonshot）、智谱、通义千问（DashScope / 百炼，以官方文档站为准）
- 网关：OpenRouter 相对上游的差异
- 用户点名的疑点必须在「一屏看懂」有结论：
  1. 现在是否仍是「OpenAI 与 DeepSeek 自动缓存、不用改代码；Anthropic 必须手动打 `cache_control` 断点」？
  2. 命中之后各家怎么计费（读价、写价、存储价）？
  3. 缓存能活多久（TTL、能否指定、过期行为）？
  4. 怎么确认命中了？
  5. 哪些改动会让缓存失效？

## 范围外

- 自建 vLLM / KV cache 推理服务内部实现
- 微调、batch API 的计价全表（只在它改变缓存规则时才记）
- 把每一家的全部模型单价抄成价目表（只记相对 input 的缓存倍率或官方写明的规则）
- 未点名的国内厂商，除非 scout 证明它的机制不属于已有家族、值得单独一行

## 种子词

OpenAI prompt caching. Anthropic cache_control. Gemini context caching / implicit caching. DeepSeek 上下文硬盘缓存. Kimi 上下文缓存. 智谱 prompt cache. 通义千问 context cache. OpenRouter prompt caching.

## 完成标准

- 网格里上述实体 × 维度，核心四家（OpenAI、Anthropic、Gemini 两行、DeepSeek）的 D1–D9 都是 ✅、⚠、⚔ 或 ∅，没有静默留 ❓。
- 用户五条疑点都有结论；其中否定、强制、时间边界类主张经过反证后才进「一屏看懂」。
- 成稿有 taxonomy（先家族后细节），不是厂商百科的拼接。
- 每个具体事实能追到笔记主张和 URL。
- `len(report) ≤ 9000`，且后一轮快照不得长过前一轮而不删内容（新增必须换掉更低价值的句子）。
