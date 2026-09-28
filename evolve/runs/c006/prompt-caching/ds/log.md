# log

## R0 定框架
- 分类轴 v0：缓存边界由谁决定（自动前缀 / 手动断点 / 显式对象 / 网关透传）。
- 维度 D1–D8 见 grid.md。
- R1 计划：6 工人按来源边界拆——openai、anthropic、gemini（显式+隐式）、deepseek、cn 三家（kimi/zhipu/qwen）、openrouter+scout。
- spawn：6（r1-openai, r1-anthropic, r1-gemini, r1-deepseek, r1-cn, r1-openrouter）
- 待查：R1 返回后看 scout leads 是否引入新实体（xAI/Bedrock/Vertex/Azure）、各家 cached token 计费单位是否可比、Kimi 是显式对象还是自动。
- R1 返回：openai(34 claims)、anthropic(20) 成功；gemini 笔记已写但工人被 429 杀；deepseek/cn/openrouter 无笔记被 429 杀 → 重派 r1b-deepseek/r1b-cn/r1b-openrouter（累计 spawn 9），r1b 三人再次被 429 杀（无笔记）。

## R1 收束
- 网格填充 29/73（40%）；report.r1.md 6612 字符（预算 9000）。
- 关键发现：Anthropic 2026-02 起有顶层 automatic caching；OpenAI GPT-5.6+ 有显式断点+1.25× 写入费——用户疑点「现在还是这样吗」的答案已变。
- R1 观察：DeepSeek/CN/OpenRouter 五行全 ❓（限流所致，非查不到）→ 动作：R2 重派这 3 个实体工人（错开降并发风险）→ 预计 spawn：3
- 待查：OpenAI pro 系 ⚔；Gemini 隐式 TTL ∅；Kimi 新旧机制并存；OpenRouter 透传字段。
