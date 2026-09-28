# log

## R0
观察：任务=8+ 家 LLM API 的 prompt caching 对照；用户点名 3 个疑点（自动vs手动现状、命中计费、TTL）。
决策：taxonomy v0 按「缓存指令谁给 + 存活模型」分族；9 个维度。R1 按来源边界拆 6 个工人：
openai / anthropic / gemini(显式+隐式) / deepseek / cn(Kimi+智谱+Qwen) / openrouter+scout。
预计 spawn：6
