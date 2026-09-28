# Brief

读者：要接多家大模型 API 的工程师。几分钟内要能判断「要不要改请求、命中后怎么付钱、缓存能活多久、怎么确认命中、改哪会失效」，再按需查字段名。

成稿回答：各家 prompt caching / 上下文缓存差在哪。先建立 taxonomy（家族），再用同一组维度对照。截至调研日 2026-09-24。字符上限 9000（含来源）。

## 范围内

- 种子四家：OpenAI、Anthropic、Gemini（隐式 + 显式分开）、DeepSeek。
- 国内：Kimi（月之暗面）、智谱、通义千问（DashScope / 百炼）。
- 网关：OpenRouter。
- 用户点名疑点（成稿必须给结论）：
  1. OpenAI 与 DeepSeek 是否仍自动缓存、不用改代码；Anthropic 是否仍必须手动打 `cache_control` 断点。
  2. 命中之后各家怎么计费（写入价、读取价、相对普通 input）。
  3. 缓存能活多久（默认 TTL、能否延长、固定还是滑动）。
- 另外必答：怎么确认命中了；哪些改动会让缓存失效。

## 范围外

- 不写各家聊天产品网页版的缓存。
- 不比较模型质量、速率限制、数据训练政策（除非该政策直接改变缓存能否跨请求复用）。
- 不给出可粘贴的完整 SDK 教程；只保留决定行为的字段名、枚举、数值。
- 自建 vLLM / KV cache 不在范围内，除非官方文档把它当成该 API 的缓存语义。

## 种子词

OpenAI prompt caching. Anthropic cache_control. Gemini context caching / implicit caching. DeepSeek 上下文硬盘缓存. Kimi 上下文缓存. 智谱 prompt cache. 通义千问 context cache. OpenRouter prompt caching.

## 完成标准

- 疑点 1–3 与「命中信号 / 失效条件」各有明确结论；官方没写的写 ∅，不靠常识补。
- 进「一屏看懂」的边界主张（必须、只有、自动且不能关、自某日起）先反证再写入。
- 每个具体事实能追到笔记主张的官方 URL 与原句。
- `len(report.md) ≤ 9000`，且后一轮不得长于前一轮快照。
