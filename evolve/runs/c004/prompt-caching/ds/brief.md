# brief：各家大模型 API 的 prompt caching 对比

## 任务
产出一份对比文档，帮用户快速搞清楚各家大模型 API 的 prompt caching（上下文缓存）差异。

## 读者
要接入或已经在用多家 LLM API 的开发者/架构师，关心：要不要改代码、省多少钱、怎么确认命中、什么会失效。

## 用户点名的疑点（成稿必须有明确结论）
1. 「OpenAI 和 DeepSeek 自动缓存不用改代码、Anthropic 必须手动打 cache_control」——现在还是这样吗？（2026-09 时点）
2. 命中后各家怎么计费（折扣/写入溢价/存储费）？
3. 缓存能活多久（TTL）？

## 范围内
- 核心 4 家：OpenAI、Anthropic、Gemini（显式 context caching + 隐式 implicit caching）、DeepSeek
- 国内其他：Kimi（Moonshot）、智谱（Zhipu/GLM）、通义千问（DashScope/Qwen）
- 网关：OpenRouter（及其他聚合层如 Azure OpenAI、AWS Bedrock、Vertex 上的缓存行为，若 leads 出现）
- 横切问题：如何确认命中（usage 字段）、什么改动让缓存失效（前缀匹配、tools/system 变化、TTL）

## 范围外
- 模型能力、非缓存定价细节、私有化部署、vLLM/SGLang 推理框架层缓存（除非官方 API 直接暴露）

## 完成标准
- 每个实体 × 维度格子有状态；核心格子 ✅ 或 ∅
- 三条疑点结论都有来源支撑（或写明官方未写）
- report.md ≤ 9000 字符（len()）
- 参数：rounds=3, workers=6, budget=9000, dir=./ds
