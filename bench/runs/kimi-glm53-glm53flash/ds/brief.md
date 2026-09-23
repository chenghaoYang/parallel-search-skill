# brief

任务：产出一份帮用户了解 LLM 时代各家模型 API「请求协议」差异的对照文档。

读者：会直接用 REST/SDK 调 LLM API、写过或要写跨厂商适配层的开发者。

几分钟内要建立的认知：
1. 四大主流协议（OpenAI Chat Completions、OpenAI Responses、Anthropic Messages、Google generateContent）在请求形状、消息表示、工具调用、流式、状态管理上的核心差异。
2. 下游厂商宣称「兼容 X」时实际差在哪（字段不支持、参数被忽略、行为不同）。
3. 跨协议迁移/适配要踩的坑。

范围内：端点与 body 字段、认证 header、消息/角色表示、工具调用表示、流式事件协议、结构化输出、推理(thinking)表示、状态与缓存、版本/弃用；各家官方兼容端点的偏差。
范围外：定价与计费、模型质量评测、内部 gRPC、纯 SDK 封装细节（只在坑层面提）。

种子词：chat completions；Responses；messages；generateContent。

用户点名疑点（成稿必须给结论）：
1. DeepSeek 官方 API 协议与 OpenAI 官方 docs 的具体不同（哪些字段不支持/被忽略/新增/行为不同，/responses 端点状态）。
2. 智谱（GLM）的 messages/anthropic 兼容端点对比 Anthropic 官方 Messages 的不同。
3. 「其他用户需要知道的问题」：迁移坑、兼容层偏差、版本风险。

完成标准：taxonomy + 四主流对照矩阵 + 下游适配差异表 + 坑清单 + 未决与置信度；len(report.md) ≤ 20000 字符。
