# brief：各家大模型 API 的 prompt caching 对比

## 任务
帮用户（在多家 LLM API 之间做成本/延迟优化的开发者）快速建立「谁自动谁手动、命中后怎么计费、缓存能活多久、怎么确认命中、什么会让缓存失效」的完整认知，并给出可比对照表。

## 读者与完成标准
读者已经在写调用 OpenAI/Anthropic/Gemini/DeepSeek 之一的代码，想知道换厂商或加新厂商时缓存行为有什么不同。5 分钟内应该能带走：
1. 8 家的「自动 vs 手动」结论（含最新版本是否变化）。
2. 命中折扣、写入是否溢价、TTL 的对照数字。
3. 每家怎么在 response 里确认命中。
4. 通用的「什么改动会打掉缓存」清单。
5. OpenRouter 这类网关是自己实现缓存还是透传底层厂商行为。

## 范围内
OpenAI、Anthropic（Claude）、Google Gemini、DeepSeek、Moonshot Kimi、智谱 GLM（Zhipu BigModel）、阿里通义千问（DashScope / 百炼）、OpenRouter。均以官方文档/API reference/pricing 页为准，取最新版本；页面标注的更新日期/版本号要记录（时效性）。

## 范围外
本地 embedding 缓存、语义缓存（如 GPTCache 这类第三方库）、向量数据库缓存、微调后的模型、除以上 8 家外的其他网关（Azure OpenAI、AWS Bedrock 等）——除非工人在 leads 里报告它们与本任务高度相关，否则不展开。

## 种子词
OpenAI prompt caching；Anthropic cache_control；Gemini context caching / implicit caching；DeepSeek 上下文硬盘缓存。

## 用户点名的疑点（成稿必须给出明确结论）
1. 「OpenAI 和 DeepSeek 是自动缓存、不用改代码，Anthropic 必须手动打 cache_control 断点——现在还是这样吗？」→ 需要现状结论，并交代 Gemini（隐式+显式并存）、Kimi/智谱/通义千问的自动化程度是否也变过。
2. 命中之后各家怎么计费（折扣比例、写入是否溢价）。
3. 缓存能活多久（TTL），是否可延长。
4. 国内其他厂（Kimi、智谱、通义千问）和 OpenRouter 这类网关在缓存上有什么不同。
5. 怎么确认命中了（response/usage 里的具体字段）。
6. 哪些改动会让缓存失效。

## 完成标准
- `grid.md` 里所有「核心格子」（触发方式、计费折扣、TTL、确认命中字段）为 ✅ 或 ∅，不遗留 ❓。
- 用户点名的 6 个疑点在 `report.md` 第 0 节各有一句明确结论。
- `report.md` ≤ 9000 字符，同时写入 `<repo>/report.md`。
