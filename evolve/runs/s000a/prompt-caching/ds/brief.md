# R0 brief — 各家大模型 API 的 prompt caching

## 读者与完成标准

读者是要同时接多家大模型 API 的开发者。成稿让他在几分钟内分清：缓存是自动发生、必须在请求里打点，还是要先创建一份缓存资源；命中怎么计费、能活多久、怎么确认、什么改动会打穿。

完成标准：

- 用户点名的疑点在「一屏看懂」里各有一句结论（可以是「官方没写」）。
- 对照矩阵用官方字段名，每个具体事实能追到笔记主张。
- taxonomy 的分类轴能解释矩阵里的主要差异。
- `ds/report.md` 字符数 ≤ 9000。同一份终稿写到仓库根 `report.md`。
- 截至日期以工人打开的官方页面为准（任务日 2026-09-24）。

## 用户点名、成稿必须回答

1. OpenAI 和 DeepSeek 是否仍是自动缓存、可以不改请求？Anthropic 是否仍必须手动打 `cache_control` 断点？现在还是不是这样？
2. 命中之后各家怎么计费（写入价、命中读取价、存储价，相对普通输入）？
3. 缓存能活多久（默认 TTL、命中是否续期、能否改）？
4. 怎么确认命中了（响应里的字段名）？
5. 哪些改动会让缓存失效？
6. Kimi、智谱、通义千问、OpenRouter 相对上面四家差在哪（自动还是手动、计费、寿命、观测）？

## 范围内

- 厂商官方 API 的上下文/prompt/prefix/KV 缓存（不是应用层自己做的缓存）。
- 种子四家：OpenAI、Anthropic、Gemini（隐式与显式分开）、DeepSeek。
- 用户点名的后续对象：Kimi（月之暗面）、智谱、通义千问（含百炼/DashScope，若官方是同一产品就合成一行）、OpenRouter。
- 预期变体只在它们和参照协议行为不同时写入「变体」：Azure OpenAI、Vertex AI、Amazon Bedrock 上的 Claude。不单独做全矩阵，除非证据表明差异大到会误导读者。

## 范围外

- 自建 vLLM / SGLang / TensorRT-LLM 的 prefix cache。
- 训练、batch API 的离线折扣，除非官方把它和 prompt cache 绑在同一页。
- 提示词压缩、截断、RAG 缓存等应用层技巧。
- 各家模型质量、速率限制（除非限制直接决定缓存能否用）。

## 种子词

OpenAI prompt caching；Anthropic cache_control；Gemini context caching / implicit caching；DeepSeek 上下文硬盘缓存；Kimi 上下文缓存；智谱 prompt cache；通义千问 / 百炼 context cache；OpenRouter prompt caching。

## 成稿约束

- 骨架顺序固定：一屏看懂 → Taxonomy → 对照矩阵 → 变体与适配层 → 坑 → 未决与置信度 → 来源。
- 每轮从头重写，禁止在上一版末尾追加。字符数只许持平或下降，除非本轮新填了 P0 格子。
- 主 agent 不搜网页。事实只来自 `ds/notes/`。
