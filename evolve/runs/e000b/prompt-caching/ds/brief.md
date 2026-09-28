# brief：大模型 API prompt caching 横向对比

## 任务
产出一份文档，帮用户搞清楚各家大模型 API 的 prompt caching（上下文缓存）有什么不同。读者 5 分钟内建立认知框架，再按需查细节。

## 范围内
- 核心 4 家（用户点名）：OpenAI、Anthropic（Claude）、Google Gemini、DeepSeek
- 国内其他厂：Kimi（Moonshot）、智谱（GLM / BigModel）、通义千问（Qwen / DashScope）
- 网关：OpenRouter（以及它对上游厂商缓存的透传/自建方式，如有其他重要网关，作为 lead 追加）
- 每家的：触发方式（自动/手动）、计费（写入价/命中价/折扣比例）、TTL（缓存能活多久）、失效条件（什么改动会 miss）、怎么确认命中（响应字段）、支持的模型范围、缓存存储方式
- 平台变体/适配层（如 Anthropic via AWS Bedrock / Google Vertex，OpenAI via Azure）——只在与母协议有实质差异时才展开，作为「变体与适配层」一节，不作为独立主行

## 范围外
- 非 API 的产品内缓存（如 ChatGPT 网页版、Claude.ai 网页版的对话记忆机制）
- 向量数据库 / RAG 检索缓存（语义缓存 semantic cache 这类第三方方案），除非某官方 API 文档本身用这个词描述其功能
- embedding 缓存、微调（fine-tuning）价格
- 自建反向代理/本地 LLM 推理框架（如 vLLM）的 prefix caching 实现细节，除非用于解释某云厂商底层机制

## 读者
懂 API 开发的用户，可能在多个 provider 间选型或写兼容层代码，需要能落地的具体参数名/字段名/数值，而不是泛泛而谈「缓存能省钱」。

## 用户点名的疑点（成稿必须给结论）
1. "OpenAI 和 DeepSeek 是自动缓存、不用改代码，Anthropic 必须手动打 cache_control 断点"——现在还是这样吗？（含 Gemini 的 implicit caching 是否也变成自动，因为这直接反驳「只有 OpenAI/DeepSeek 自动」的印象）
2. 命中之后各家怎么计费（折扣比例、写入是否额外收费、和基础 input 价的关系）
3. 缓存能活多久，各家是否一样（默认 TTL、是否可配置/续期）
4. 怎么确认命中了（响应里看哪个字段）
5. 哪些改动会让缓存失效（前缀匹配规则的边界：system prompt、工具定义、图片、消息顺序变化等）
6. 国内厂（Kimi/智谱/Qwen）和 OpenRouter 在缓存机制上与上述 4 家的异同

## 种子词
OpenAI prompt caching; Anthropic cache_control; Gemini context caching / implicit caching; DeepSeek 上下文硬盘缓存; Kimi context caching; 智谱 GLM 缓存; 通义千问 DashScope 缓存; OpenRouter prompt caching

## 完成标准
- taxonomy：分类轴能解释「谁自动/谁手动/谁要建独立缓存对象」这三分法，且矩阵覆盖 8 个实体 × 核心维度
- 每个用户点名疑点在「0. 一屏看懂」有明确结论
- 正文事实可追溯到 notes 里的一手来源；成稿 ≤ 9000 字符
- 终审抽查 ≥ 20 条具体主张对照笔记核实
