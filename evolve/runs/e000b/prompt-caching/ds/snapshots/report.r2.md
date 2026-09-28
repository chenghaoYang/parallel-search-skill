# 大模型 API Prompt Caching 横向对比

> 截至 2026-09-24,基于各厂商官方文档与 API Reference。先看「一屏看懂」建立框架,第2节查具体数字,第4节是踩坑提醒,第5节是仍未确认的细节。

## 0. 一屏看懂

1. **"自动 vs 手动"是光谱不是二选一,且格局没有变化**:OpenAI(全系列)、DeepSeek、Kimi、智谱、Gemini(implicit)、Qwen(implicit)默认零改动;Anthropic 至少要在请求顶层加 1 个 `cache_control`——即使 2025-03-13 上线的"Automatic Caching"也没有免掉这一步,只是不用逐块标记[2]。反过来 OpenAI GPT-5.6+ 新增了*可选*的手动断点(`prompt_cache_breakpoint`),但默认行为仍是零改动全自动[1]。
2. **命中折扣普遍在"原价10%左右",但基准不同**:Anthropic 多数模型0.1x(部分模型低至0.025x)[2];Gemini 两种模式都是0.1x[3];OpenAI 新款(GPT-5.6+)0.1x、旧款0.5x[1];Kimi K3 0.1x、K2.6 0.17x[5];DeepSeek 因架构升级价格本身很低,命中价约为原价的2%左右[4];智谱约0.5x[6];DashScope 显式0.1x/隐式约0.2x[7]。
3. **写入是否收费看厂商也看模型代际**:Anthropic、Kimi、DashScope(显式)明确收写入费(1.25x起,长TTL更贵);OpenAI 只有 GPT-5.6+ 才开始收1.25x写入费,更早版本依然免费[1];DeepSeek、智谱写入不加价[4][6]。
4. **TTL 思路两极**:DeepSeek 用磁盘做介质,官方原话是"尽力而为、不保证命中率",只说"数小时到数天"不给精确数字、不可配置[4];其余厂商是分钟/小时级精确时长,默认5-30分钟,要更长(1小时)通常要多付钱;Gemini explicit 缓存反而可自定义 TTL 或到期时间戳,未见文档写明上限[3]。
5. **确认命中看 usage 字段,但形状不同**:多数厂商一个字段搞定(`cached_tokens` 或类似命名)[1][3][4][5][6];Anthropic 是三个独立字段,要自己相加还原总输入 token 数[2]。
6. **失效的核心规则是"前缀精确匹配、整体失效"**:断点前内容任何字节变化——包括自动填充的时间戳——都会让之后全部缓存失效而非部分失效,查到的厂商里这条一致[1][2][4][5]。
7. **国内厂商分两派**:智谱、Kimi 走 OpenAI 式全自动;DashScope 两种模式都给,显式模式参数形状(`cache_control: {type: "ephemeral"}`)几乎照搬 Anthropic[6][7]。
8. **OpenRouter 不生产缓存**:官方 FAQ 原句"no markup on inference pricing"——照抄上游折扣价,自己只加一层"粘性路由"把后续请求送回同一上游节点提升命中率,10分钟无活动后失效,且只在"上游缓存价比常规价低"时才启用[8]。
9. **同一厂商换个云托管,家族可能会变**:Anthropic 原生 API 和 Vertex AI 上的 Claude 都要手动 `cache_control`;但 AWS 官方文档明确 Bedrock 上的 Claude 多了一条不需要 `cache_control` 的 Implicit Prompt Caching 通道,计费和 TTL 与原生相同[9]——这是本文档查到唯一的"手动变自动"例外。

## 1. Taxonomy

分类轴:**谁触发缓存、状态放请求里还是独立资源**,分三家族:

| 家族 | 定义 | 成员 |
|---|---|---|
| F1 全自动隐式 | 不改请求结构,够长自动命中,可选参数只是调优 | OpenAI、DeepSeek、Kimi(默认)、智谱GLM、Gemini implicit、Qwen implicit |
| F2 请求内显式断点 | content block(或请求顶层)放 `cache_control` 类标记随请求发送,无独立资源 ID | Anthropic、Qwen explicit |
| F3 独立缓存对象 | 先调用 API 建资源拿 ID,后续引用,有独立生命周期、可显式删除 | Gemini explicit(CachedContent) |

OpenRouter 不是第四家族,是**网关层**:继承上游模型的 F1/F2/F3,叠加"粘性路由"。云托管入口(Bedrock/Vertex/Azure)也可能让同一母协议横跨家族,见结论9和第3节。

维度:触发方式与代码改动、最小可缓存长度、命中价、写入费、TTL、命中确认字段(矩阵按此排列)。

## 2. 对照矩阵

| 实体 | 触发·改动 | 最小长度 | 命中价(相对原价) | 写入费 | TTL | 命中字段 |
|---|---|---|---|---|---|---|
| OpenAI GPT-5.6+/GPT-6 | F1默认+可选手动断点`prompt_cache_breakpoint` | 1024tok,128递增 | 0.1x | 1.25x | 固定30m(仅此值) | `usage.prompt_tokens_details.cached_tokens` |
| OpenAI GPT-5.5及更早 | F1纯自动 | 1024tok | 0.5x | 免费 | in_memory 5-10m~1h 或 24h档 | 同上 |
| Anthropic | F2,顶层1个`cache_control`(自动放置)或逐块最多4个 | 512-4096按模型 | 0.1x(部分模型0.025x-0.05x) | 1.25x(5m)/2x(1h) | 5m默认/1h可选,命中续期 | 3字段求和 |
| Gemini | F1 implicit默认 + F3 explicit需建CachedContent | 2048-4096按模型 | 两模式均0.1x | explicit $0.50/M tok/时(2026底前);implicit免费 | explicit默认1h可调;implicit系统自动 | `usage.total_cached_tokens` |
| DeepSeek | F1纯自动 | 64tok | 约0.02x | 免费 | "数小时到数天",不保证命中,不可配 | `prompt_cache_hit/miss_tokens` |
| Kimi | F1默认,mode仅含implicit | 256tok | K3:0.1x/K2.6:0.17x | 5m档=标准价;1h档=2x | 5m默认/1h可选,命中续期 | `cached_tokens`+`cache_write_tokens` |
| 智谱GLM | F1纯自动,全部GLM模型 | 500+tok | 约0.5x | ∅官方未详述 | 5min自动刷新 | `cached_tokens` |
| 通义千问 | F1 implicit + F2 explicit两选 | explicit 1024tok | explicit 0.1x/implicit约0.2x | explicit 1.25x | explicit 5min;implicit∅未给精确值 | explicit已确认;implicit∅未确认是否同名 |
| OpenRouter | 透传上游+sticky routing(条件触发) | 按上游 | 按上游,官方"no markup" | 按上游 | 按上游;sticky 10min无活动失效 | `cached_tokens` |

∅=官方定向查过、明确未给精确数字(不是没查到)。

## 3. 变体与适配层

| 云托管入口 | 与原生的关系 |
|---|---|
| AWS Bedrock(Claude) | 多一条**不需要 cache_control** 的 Implicit Prompt Caching 通道(官方原句);计费/TTL 与原生一致 |
| Google Vertex AI(Gemini) | implicit+explicit 均不需要 cache_control,2.5+系90%折扣、2.0系75% |
| Google Vertex AI(Claude) | 仍需 cache_control,与原生一致;具体费率未在官方页面查到 |
| Azure OpenAI | GPT-5.6+起与原生几乎一致(可选手动断点、1.25x写入、30m固定TTL);更早版本自动且写入免费 |

## 4. 用户需要知道的坑

- **改一个字都可能整体失效**:断点前内容任何字节变化(哪怕模板自动填充的时间戳)会让之后全部缓存失效,不是部分失效[1][2]。
- **稳定内容放最前、易变内容放最后**:多家官方指南建议 system prompt、工具定义放请求最前,用户问题放最后,否则前面一变后面全 miss[2][5]。
- **命中不是保证的**:DeepSeek 官方明确"尽力而为、不保证命中率";OpenAI 请求量太大时(约15 req/min/前缀阈值)也可能因路由到不同机器错过缓存[1][4]。
- **切换模型/版本,缓存不跟着走**:Kimi 官方明确换模型后旧缓存不再命中[5]。
- **DashScope 只查最近20个 block**:不是整个历史都会拿来比对前缀[7]。
- **Anthropic/Kimi 更长 TTL 要多付钱**:1小时档写入价接近5分钟档的2倍,不是免费续命[2][5]。
- **OpenRouter 粘性路由不是无条件的**:只有上游缓存价比常规价低时才启用,自己指定 `provider.order` 会覆盖它,上游报错也不会更新[8]。
- **Gemini explicit 缓存本身要花钱存**:按小时计费(2026年底后翻倍),不像多数厂商命中前完全免费[3]。

## 5. 未决与置信度

- Google Vertex AI 上 Claude 的具体缓存费率:本轮只确认"与原生一致"的定性说法,未找到官方费率表。
- DashScope implicit 模式的精确 TTL 数值、命中字段名是否与 explicit 相同:官方页面只说"定期清理",未给数字。
- 智谱 GLM 的写入费、精确失效触发条件:官方文档未详述。
- OpenRouter sticky routing 对 70+ 上游厂商是否逐一满足触发条件:官方只给判定规则,未给全量清单。
- OpenAI Responses API 与 Chat Completions API 的缓存行为是否有差异:未查到官方说明。

## 来源
[1] OpenAI Prompt Caching — https://developers.openai.com/api/docs/guides/prompt-caching, https://developers.openai.com/api/docs/pricing
[2] Anthropic Prompt Caching — https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://claude.com/blog/token-saving-updates
[3] Gemini Context Caching — https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/generate-content/caching, https://ai.google.dev/pricing
[4] DeepSeek Context Caching on Disk — https://api-docs.deepseek.com/guides/kv_cache/, https://api-docs.deepseek.com/news/news260910/
[5] Kimi Context Caching — https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api, https://platform.kimi.ai/docs/pricing/chat
[6] 智谱 BigModel 缓存文档 — https://docs.bigmodel.cn/cn/guide/capabilities/cache
[7] 阿里云 DashScope Context Cache — https://help.aliyun.com/zh/model-studio/context-cache
[8] OpenRouter Prompt Caching — https://openrouter.ai/docs/guides/best-practices/prompt-caching, https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/, https://openrouter.ai/docs/faq
[9] AWS Bedrock Prompt Caching — https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html, https://aws.amazon.com/bedrock/pricing/
[10] Google Cloud Vertex AI Context Caching — https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching, https://cloud.google.com/blog/products/ai-machine-learning/claude-at-scale-on-google-cloud-frontier-ai-built-for-enterprise-production
[11] Azure OpenAI Prompt Caching — https://learn.microsoft.com/azure/ai-services/openai/how-to/prompt-caching
