# 大模型 API Prompt Caching 横向对比

> 截至 2026-09-24。回答:OpenAI/Anthropic/Gemini/DeepSeek/Kimi/智谱/通义千问/OpenRouter 的上下文缓存机制有什么不同。先看「一屏看懂」建立框架,再查第 2 节矩阵对具体数字,第 4 节是踩坑提醒。

## 0. 一屏看懂

1. **"自动 vs 手动"是光谱,不是二选一**:OpenAI、DeepSeek、Kimi、智谱、Gemini(隐式模式)默认不改代码就能命中缓存;Anthropic 的机制本质是"在请求里放 cache_control",即使它的"Automatic Caching"选项也只是省去逐块标记、仍要在请求顶层加参数——不是零改动。(⚠ OpenAI 新版是否新增了可选手动断点模式待复核,见第5节)
2. **命中折扣差异大**:Anthropic 多数模型命中价是原价 10%(部分模型低至 2.5%);DeepSeek 命中价接近于零成本;OpenAI 传统上 50% 折扣;Kimi 约 84–90%[2][3][4][5]。
3. **只有 Anthropic 和 Kimi 对"写入缓存"明确额外收费**:Anthropic 5 分钟档 1.25x、1 小时档 2x 基础输入价;Kimi 同理分层;OpenAI 传统模式、DeepSeek、智谱写入不加价[2][4][5]。
4. **TTL 思路不同**:DeepSeek 用磁盘做介质,官方说法是"数小时到数天"、不可配置;其余厂商普遍分钟级(5 分钟默认),要更长需显式选 1 小时档并多付费(Anthropic、Kimi、DashScope 显式模式)[2][4][6]。
5. **怎么确认命中**:多数厂商在 `usage`/`prompt_tokens_details` 下放一个 `cached_tokens` 字段;Anthropic 是三个独立字段需自己求和[1][2][4]。
6. **失效的核心规则是"前缀精确匹配、整体失效"**:断点之前的内容——包括时间戳、工具定义顺序——发生任何变化,缓存立刻整体失效,不是部分失效[1][2][5]。
7. **国内厂商分两派**:智谱、Kimi 走 OpenAI 式全自动路线;通义千问/DashScope 同时提供两种模式,显式模式参数形状(`cache_control: {type: "ephemeral"}`)几乎照搬 Anthropic[4][6]。
8. **OpenRouter 不生产缓存,只做两件事**:透传上游厂商各自的缓存机制和计费,并加一层"粘性路由"把后续请求送回同一节点以提高命中率[7]。

## 1. Taxonomy

分类轴:**谁触发缓存、状态放哪端**,分三家族:

| 家族 | 定义 | 成员 |
|---|---|---|
| F1 全自动隐式 | 不改请求结构,够长自动命中,可选参数只是调优 | OpenAI、DeepSeek、Kimi(默认)、智谱GLM、Gemini implicit(2.5+默认)、Qwen implicit |
| F2 请求内显式断点 | content block 上放 `cache_control` 类标记随请求发送,无独立资源 ID | Anthropic、Qwen explicit |
| F3 独立缓存对象 | 先调用 API 建资源拿 ID,后续引用,有独立生命周期 | Gemini explicit(CachedContent) |

OpenRouter 不是第四家族,是**网关层**:继承上游模型的 F1/F2/F3,叠加"粘性路由"。

维度:D1/D2 触发方式与代码改动、D3 最小可缓存长度、D4 命中折扣、D5 写入费、D6 TTL、D8 命中确认字段(矩阵按此排列)。

## 2. 对照矩阵

| 实体 | D1/D2 触发·改动 | D3 最小长度 | D4 命中价(相对原价) | D5 写入费 | D6 TTL | D8 命中字段 |
|---|---|---|---|---|---|---|
| OpenAI | F1,默认零改动;⚠新版或有可选手动断点 | 1024 tok,128递增 | 传统 50%;⚠新价待复核 | 传统免费;⚠新价待复核 | ⚠5-10min或1h;新参数待复核 | `usage.prompt_tokens_details.cached_tokens` |
| Anthropic | F2,加 `cache_control`(逐块或顶层"自动") | 512/1024/2048/4096(按模型) | 多数10%;部分模型2.5%/5% | 1.25x(5m)/2x(1h) | 5m默认/1h可选,命中续期 | `cache_read_input_tokens`+`cache_creation_input_tokens`+`input_tokens` |
| Gemini | F1 implicit默认自动 + F3 explicit需建CachedContent | implicit 2048(2.5系)/4096(3.x系) | ❓官方未给百分比 | ❓explicit存储费未查到 | ❓两模式TTL未写明确值 | `usage.total_cached_tokens`(implicit) |
| DeepSeek | F1,零改动 | 64 tok | 新价$0.003(离峰)–$0.006(峰值)/MTok | 不额外收费 | 数小时到数天,不可配置 | `prompt_cache_hit_tokens`/`_miss_tokens` |
| Kimi | F1,默认自动;`prompt_cache_options`可选调TTL | 256 tok | K3 90%(降至$0.30);K2.6 84% | 5m档=标准价;1h档=2x | 5m默认/1h可选,命中续期 | `cached_tokens`+`cache_write_tokens` |
| 智谱GLM | F1,零改动 | 500+ tok | 约50% | ❓未查到 | 5min,命中自动刷新 | `cached_tokens` |
| 通义千问 | F1 implicit(零改动)+F2 explicit(加`cache_control`) | explicit 1024 tok | explicit 10%;implicit约20% | explicit 125% | explicit 5min | ❓implicit字段名未确认 |
| OpenRouter | 透传上游F1/F2/F3 + 粘性路由 | 按上游(OpenAI起1024) | 按上游原价(如Anthropic 0.1x、Gemini 0.25x) | 按上游原价 | 按上游+粘性路由10min无活动失效 | `usage.prompt_tokens_details.cached_tokens` |

❓=本轮未查到官方数字;⚠=已查到但数字反常/需复核,见第5节。

## 3. 变体与适配层

Anthropic、Gemini 均有第三方云托管入口(AWS Bedrock、Google Vertex AI),OpenAI 有 Azure OpenAI——三者与原生 API 在缓存计费/TTL 上是否一致,R1 只查到零星二手线索(如 Bedrock 疑似提供"隐式"缓存),未经一手来源核实,本轮不下结论,见第5节。

## 4. 用户需要知道的坑

- **改一个字都可能整体失效**:断点前内容任何字节变化(哪怕是模板自动填充的时间戳)都会让之后全部缓存失效,不是部分失效[1][2]。
- **稳定内容放最前、易变内容放最后**:多家官方指南建议把 system prompt、工具定义等放请求最前,用户问题等放最后,否则前面一变后面全 miss[2][5]。
- **命中不是保证的**:DeepSeek 官方明确是"尽力而为、不保证命中率";请求量大时(OpenAI 约15 req/min/前缀阈值)也可能因路由到不同机器错过缓存[1][3]。
- **切换模型/版本,缓存不跟着走**:Kimi 官方明确换模型后旧缓存不再命中[5]。
- **DashScope 的"最近匹配窗口"有限**:官方说只检查最近20个content block,不是整个历史都比对[6]。
- **Anthropic 更长 TTL 要多付钱**:1小时档缓存写入价是基础输入价的2倍,不是免费续命[2]。

## 5. 未决与置信度

- **待复核**:OpenAI 是否在新版本引入可选手动断点 + 折扣率从50%升到90% + 写入开始收费——反常且影响本文档结论1、2,复核前不作定论。Anthropic「Automatic Caching」具体省了多少改动量也待确认。
- **Gemini explicit CachedContent 计费/TTL**:官方数字未查到,矩阵留空。
- **OpenRouter 是否在上游价格上加价**:只确认"按上游折扣比例",未查到是否叠加服务费。
- **AWS Bedrock / Google Vertex AI / Azure OpenAI 的缓存差异**:仅二手来源提及,未核实。
- **智谱GLM 写入费、通义千问隐式模式命中字段名**:官方页面未直接给出。

## 来源
[1] OpenAI Prompt Caching Guide — https://developers.openai.com/api/docs/guides/prompt-caching
[2] Claude Prompt Caching — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[3] DeepSeek Context Caching on Disk — https://api-docs.deepseek.com/guides/kv_cache/
[4] Kimi Context Caching Guide — https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api
[5] Kimi Pricing / Dynamic Tool Loading — https://platform.kimi.ai/docs/pricing/chat
[6] 阿里云 DashScope Context Cache — https://help.aliyun.com/zh/model-studio/context-cache
[7] OpenRouter Prompt Caching — https://openrouter.ai/docs/guides/best-practices/prompt-caching
[8] Gemini API Context Caching — https://ai.google.dev/gemini-api/docs/caching
[9] 智谱 BigModel 缓存文档 — https://docs.bigmodel.cn/cn/guide/capabilities/cache
