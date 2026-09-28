# log

## R0

观察：用户疑点集中在「要不要改代码、命中怎么计费、能活多久、怎么确认命中、什么会失效」。种子词把 Gemini 拆成 implicit 与 context caching 两种说法。国内三家和 OpenRouter 是第二层。
决策：taxonomy v0 分类轴 = 缓存边界与生命周期由谁持有（F1 自动前缀 / F2 请求内断点 / F3 显式缓存对象 / F4 网关中介）。8 个正交维度 D1–D8。Gemini 先拆两行。
R1 按来源边界派 6 个工人：4 家核心文档站 + OpenRouter + 1 个 scout。国内三家留 R2。
→ 动作：spawn R1 → 预计 spawn：6
