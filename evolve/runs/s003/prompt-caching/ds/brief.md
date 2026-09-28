# 简报：各家大模型 API 的 prompt caching

读者：要接或迁移多家模型 API 的工程师。几分钟内要能判断「要不要改代码、命中后怎么扣钱、缓存能活多久、怎么确认命中、什么改动会失效」，再按需查矩阵里的字段名。

截至调研日：2026-09-24。成稿字符上限 9000（`len()`，含来源节）。

## 范围内

- OpenAI prompt caching
- Anthropic `cache_control`
- Gemini：explicit context caching 与 implicit caching（两行，不合并）
- DeepSeek 上下文硬盘缓存
- 国内：Kimi（月之暗面 / Moonshot）、智谱（GLM / BigModel）、通义千问（DashScope / 百炼）
- 网关：OpenRouter，以及 scout 若发现的同类官方网关差异（只在有一手来源时写入）
- 用户点名的疑点必须在成稿给出结论（可以是「官方未写」）

## 范围外

- 自建推理引擎的 prefix / KV cache（vLLM、SGLang 等）
- 应用层自己做的缓存（Redis、SDK memo）
- 微调、batch 折扣、普通 input 价目的完整价目表（只保留与缓存读写直接相关的倍率或单价口径）
- 训练数据、模型权重缓存

## 种子词

OpenAI prompt caching. Anthropic cache_control. Gemini context caching / implicit caching. DeepSeek 上下文硬盘缓存. Kimi 上下文缓存. 智谱 上下文缓存. 通义千问 显式缓存 隐式缓存. OpenRouter prompt caching.

## 用户点名的疑点（成稿必须有结论）

1. 现在是否仍是：OpenAI 与 DeepSeek 自动缓存、不用改代码；Anthropic 必须手动打 `cache_control` 断点？
2. 命中之后各家怎么计费（读价、有没有写价/存储价、相对普通输入）？
3. 缓存能活多久（默认 TTL、能否指定、命中是否续期）？
4. Kimi、智谱、通义、OpenRouter 在缓存上和上面四家差在哪？
5. 怎么确认这次命中了（响应里的字段名）？
6. 哪些改动会让缓存失效？

## 完成标准

- Taxonomy 能解释「要不要改代码」这组差异；Gemini 的两种模式分开比。
- 四家核心行的 D1–D8 尽量是 ✅ 或 ∅（定向查过官方没有）。
- 国内三家与 OpenRouter 有结论，空着的格子进「未决」并写原因。
- 每个具体事实能追到笔记主张；边界主张（必须、只有、自动、未提及）经过反证或写明查过的范围。
- `ds/report.md` 与仓库根 `report.md` 内容一致，且 `len() ≤ 9000`。
