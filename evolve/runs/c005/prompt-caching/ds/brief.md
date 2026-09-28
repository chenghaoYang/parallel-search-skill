# brief

任务：产出一份对照文档，帮用户搞清楚各家大模型 API 的 prompt caching（上下文缓存）差异。

参数：rounds=3, workers=6, budget=9000 字符（含来源节），dir=./ds，终稿同步写 ./report.md。

读者：要在多家 LLM API 上做成本/延迟优化的开发者。读完 5 分钟内知道：各家缓存要不要改代码、命中怎么计费、能活多久、怎么确认命中、什么操作会打掉缓存。

## 范围内
- OpenAI prompt caching（platform.openai.com）
- Anthropic prompt caching / cache_control（docs.anthropic.com / docs.claude.com）
- Gemini explicit context caching + implicit caching（ai.google.dev）
- DeepSeek 上下文硬盘缓存（api-docs.deepseek.com）
- 国内：Kimi/Moonshot（platform.moonshot.cn）、智谱 GLM（bigmodel.cn）、通义千问 DashScope（help.aliyun.com）
- 网关：OpenRouter（openrouter.ai/docs），顺带留意 Bedrock/Vertex/Azure 是否有缓存透传差异

## 范围外
- 非 API 层缓存（应用层 semantic cache、langchain/gptcache 等）
- 各模型推理质量对比

## 用户点名疑点（成稿必须有明确结论）
1. 「OpenAI 和 DeepSeek 自动缓存不用改代码，Anthropic 必须手动打 cache_control」——现在还是这样吗？（注意 Gemini 已出 implicit caching，需核实现状）
2. 命中之后各家怎么计费（写入费？命中折扣多少？）
3. 缓存能活多久（TTL、续期规则）

## 完成标准
- 每个实体 × 每个维度有一手来源或明确标 ∅/❓
- 「一屏看懂」里的边界主张过反证
- len(report.md) ≤ 9000
