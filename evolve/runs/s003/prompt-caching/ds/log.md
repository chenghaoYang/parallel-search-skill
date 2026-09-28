# 调研日志

参数：rounds=3，workers=6，budget=9000，dir=./ds，工人模型=swe-2-shim。无 pplx-safe。主 agent 不搜网页。

## R0

观察：用户第一问是「还要不要改代码」，计费和 TTL 是第二问。Gemini 官方把隐式和显式分成两种产品，合成一行会把主轴搅乱。

决策：taxonomy v0 主轴 = 谁控制缓存边界（自动前缀 / 请求内断点 / 命名缓存资源 / 网关）。维度 D1–D8。R1 按来源站拆 4 家 + 2 个 scout。国内三家和 OpenRouter 先留 ❓，不在 R1 填进成稿。

spawn：0
