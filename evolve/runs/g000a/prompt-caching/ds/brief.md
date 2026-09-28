# R0 brief

读者：要在自己的客户端或网关里接多家大模型、并搞清 prompt caching / 上下文缓存要不要改代码的工程师。
成稿要让他在几分钟内分清「自动前缀 / 请求内断点 / 显式缓存对象 / 网关中介」四类，并查到字段名、TTL、计费倍率和命中字段。

范围内：
- OpenAI、Anthropic、Gemini（隐式 + 显式 context caching）、DeepSeek
- 国内：Kimi（月之暗面）、智谱、通义千问（DashScope / 百炼）
- 网关：OpenRouter（作为网关家族的代表；其他网关只在线索里出现，不单列成稿行，除非机制独立到必须写）
- 用户点名的疑点必须有结论：
  1. OpenAI 与 DeepSeek 是否仍自动缓存、调用方不用改请求？
  2. Anthropic 是否仍必须手动打 `cache_control` 断点？
  3. 命中之后各家怎么计费（读 / 写 / 存储，相对普通 input）？
  4. 缓存能活多久？
  5. 怎么确认命中了？
  6. 哪些改动会让缓存失效？

范围外：
- 如何实现自建 KV cache、推理引擎内部 prefix cache（vLLM / SGLang）的配置
- 训练、微调、batch 折扣的完整价目（只在它改变缓存计费时写入）
- 各模型质量、延迟基准
- 非上述厂商的完整矩阵（Azure / Bedrock / Vertex 只在它们改变「同一协议在另一端」的行为时，作为变体写进第 3 节，不另开家族）

种子词：OpenAI prompt caching；Anthropic cache_control；Gemini context caching / implicit caching；DeepSeek 上下文硬盘缓存。

完成标准：
- `ds/report.md` 按 converge 骨架，`len ≤ 9000`
- 用户点名的 6 个疑点在「一屏看懂」有结论，正文有字段名和来源
- 网格核心行（OpenAI、Anthropic、Gemini 隐式、Gemini 显式、DeepSeek、Kimi、智谱、通义、OpenRouter）× 8 维均为 ✅ / ∅ / ⚔（⚔ 必须在第 5 节解释），不许静默留 ❓
- 同内容同时写到工作区根目录 `./report.md`
- 日期锚点：调研日 2026-09-24；主张必须带页面上看到的日期或版本，没有日期就在主张里注明「页未见日期」

参数：rounds=3 workers=6 budget=9000 dir=./ds worker-model=grok-4.7
检索：工人 web_search 找页，web_fetch 打开一手页。没有 pplx-safe。
