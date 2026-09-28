# brief: 各家大模型 API prompt caching 对比

## 读者与目标
用多家 LLM API 的开发者。5 分钟内建立：谁家是自动缓存、谁家要手动打标、命中怎么计费、缓存活多久、怎么确认命中、什么改动会失效。成稿是 taxonomy + 对照矩阵，不是教程。

## 用户点名疑点（成稿必须有明确结论）
1. 「OpenAI 和 DeepSeek 自动缓存不用改代码、Anthropic 必须手动打 cache_control」——现在还是吗？
2. 命中后各家怎么计费（写溢价 / 读折扣 / 存储费）。
3. 缓存能活多久（TTL）。
4. 怎么确认命中了（usage 字段）。
5. 哪些改动会让缓存失效。

## 范围内
- 核心 4 家：OpenAI、Anthropic、Google Gemini（显式 context caching + implicit caching）、DeepSeek。
- 国内：Kimi/Moonshot、智谱 GLM、通义千问/DashScope。
- 网关：OpenRouter（透传各家的差异）。
- 相关 scope：命中确认、失效条件、隐私/隔离、模型/端点适用范围。

## 范围外
- 各家推理质量、非缓存计价细节；客户端 SDK 教程；自部署 KV cache（vLLM 等）。

## 参数
rounds=3, workers=6, budget=9000 chars（含来源节），dir=./ds，终稿同时写 ./report.md。
