# log

## R0
- 任务：各厂 LLM API prompt caching 对比文档。rounds=3 workers=6 budget=9000 dir=./ds。
- taxonomy v0：分类轴 = 机制谱系（自动隐式 / 手动断点 / 显式对象 / 网关透传）；8 个维度 D1–D8。
- 疑点：自动 vs 手动现状、计费、TTL —— 必须给结论。
- R1 计划：按来源边界拆 6 个工人：openai / anthropic / gemini（显式+隐式）/ deepseek / cn 三家（kimi+zhipu+qwen）/ openrouter+scout 坑。

## R1
- spawn：6（openai, anthropic, gemini, deepseek, cn, openrouter-scout）
