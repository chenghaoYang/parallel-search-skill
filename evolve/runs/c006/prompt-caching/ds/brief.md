# brief：各家大模型 API 的 prompt caching 对照

读者：要在多家 LLM API 之间做选择/迁移的开发者。目标：5 分钟建立「谁家缓存是什么机制、怎么计费、怎么确认命中、什么操作会失效」的认知。

## 范围内
- OpenAI prompt caching（自动）
- Anthropic cache_control（手动断点，5m/1h）
- Gemini：显式 context caching + 隐式 implicit caching
- DeepSeek 上下文硬盘缓存（自动）
- 国内：Kimi（Moonshot）、智谱 GLM、通义千问（DashScope）
- OpenRouter 网关（缓存透传/路由）
- 横向问题：怎么确认命中、哪些改动使缓存失效、计费与 TTL

## 范围外
- 响应/结果缓存（semantic cache、GPTCache 一类自建层）
- 各家的 batch/flex 折扣（与缓存无关的定价）
- 非 API 产品（网页版、IDE 插件）

## 用户点名疑点（成稿必须给结论）
1. 「OpenAI 和 DeepSeek 自动缓存不用改代码、Anthropic 必须手动打 cache_control」——现在还是吗？（注意 Gemini 隐式缓存也是自动；Anthropic 是否有变化）
2. 命中后各家怎么计费（写入溢价/读取折扣/存储费）
3. 缓存能活多久（TTL、是否可续、显式缓存对象的存活）

## 完成标准
- 矩阵每格 ✅/⚠/⚔/❓/∅ 有状态；一屏看懂每条带来源
- report.md ≤ 9000 字符；同步写到 ./report.md
- 轮次上限 3，单轮工人 ≤ 6
