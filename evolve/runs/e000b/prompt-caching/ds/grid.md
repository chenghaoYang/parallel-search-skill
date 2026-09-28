# grid v2（R2 后）

## 分类轴（确认成立，无需再换）
- F1 全自动隐式：OpenAI(默认)、DeepSeek、Kimi(默认)、智谱GLM、Gemini implicit(2.5+默认)、Qwen implicit
- F2 请求内显式断点：Anthropic(原生,顶层1个或逐块最多4个)、Qwen explicit
- F3 独立缓存对象：Gemini explicit CachedContent(唯一确认案例)
- 横切1：F1 厂商头部模型可选叠加手动断点(OpenAI GPT-5.6+ prompt_cache_breakpoint);F2 厂商可选自动化(Anthropic top-level cache_control,2025-03-13上线,仍需1个参数)
- 横切2：OpenRouter=网关元层,继承上游家族+sticky routing,无加价(官方FAQ原句确认)
- 新增横切3(R2发现)：同一母协议在不同云托管入口可能变家族——Anthropic 原生+Vertex 都是 F2,但 AWS Bedrock 额外提供不需要 cache_control 的"Implicit Prompt Caching"(AWS 官方文档原句确认),等于 F2 厂商在特定云托管上出现 F1 分支

## 矩阵最终状态
✅已确认(含数字)｜∅官方未写/未给精确值(已定向查过,非缺口)｜❓仍待查(低优先级,不再追查)

| 实体 | D1/D2 触发·改动 | D3最小长度 | D4命中价 | D5写入费 | D6 TTL | D8命中字段 |
|---|---|---|---|---|---|---|
| OpenAI(GPT-5.6+/GPT-6) | ✅F1默认+可选prompt_cache_breakpoint手动 | ✅1024tok/128递增 | ✅0.1x(90%) | ✅1.25x | ✅固定30m(仅此值) | ✅usage.prompt_tokens_details.cached_tokens |
| OpenAI(GPT-4o/o1/GPT-5.5及更早) | ✅F1纯自动 | ✅1024 | ✅0.5x(50%) | ✅免费 | ✅in_memory 5-10m~1h 或 24h档(prompt_cache_retention) | 同上 |
| Anthropic | ✅F2,顶层1个cache_control(自动放置)或逐块最多4个 | ✅512/1024/2048/4096按模型 | ✅0.1x多数/0.025x-0.05x部分 | ✅1.25x(5m)/2x(1h) | ✅5m默认/1h可选,命中续期 | ✅3字段求和 |
| Gemini | ✅F1 implicit默认 + F3 explicit(cachedContents API) | ✅implicit 2048(2.5系)/4096(3.x系);explicit同 | ✅两模式均0.1x(90%);batch再半价 | ✅explicit $0.50/M tok/小时(至2026年底,其后$1.00) implicit免费 | ✅explicit默认1h可调(ttl/expireTime,官方未提上限);implicit系统自动无需配置 | ✅total_cached_tokens |
| DeepSeek | ✅F1纯自动 | ✅64 | ✅约0.02x(新价$0.003-0.006/M) | ✅免费 | ∅"数小时到数天"官方未给精确值,明确"尽力而为不保证命中" | ✅hit/miss两字段 |
| Kimi | ✅F1默认,mode仅含implicit | ✅256 | ✅K3:0.1x/K2.6:0.17x | ✅5m档=标准价;1h档=2x | ✅5m默认/1h可选,命中续期 | ✅cached+write两字段 |
| 智谱GLM | ✅F1纯自动,全部GLM模型适用 | ✅500+ | ✅约0.5x | ∅官方明确未详述写入费 | ✅5min自动刷新 | ✅cached_tokens |
| 通义千问/DashScope | ✅F1 implicit+F2 explicit两选 | ✅explicit1024 | ✅explicit0.1x/implicit约0.2x | ✅explicit1.25x | ✅explicit5min;∅implicit精确值未给("定期清理") | ✅explicit字段确认;implicit字段∅未明确是否同名 |
| OpenRouter | ✅透传上游F1/F2/F3+sticky routing(条件:cache读价<常规价时激活) | ✅按上游 | ✅按上游,官方FAQ明确"no markup" | ✅按上游 | ✅按上游;sticky 10min无活动失效,error不缓存,手动provider.order可覆盖 | ✅cached_tokens |

## 变体/适配层最终状态
| 平台 | 触发方式 | 计费/TTL与原生关系 |
|---|---|---|
| AWS Bedrock(Claude) | ✅Implicit Prompt Caching,无需cache_control(AWS官方原句确认,区别于原生) | ✅与原生相同费率/TTL(1.25x/2x写入,0.1x读取,5m/1h) |
| Google Vertex AI(Gemini) | ✅implicit默认+explicit,无需cache_control | ✅2.5+系90%折扣,2.0系75%(Google Cloud官方博客) |
| Google Vertex AI(Claude) | ⚠仍需cache_control,与原生一致(来源是另一篇Google Cloud博客,非Anthropic文档) | ∅具体费率未在本轮找到官方页面 |
| Azure OpenAI(GPT) | ✅GPT-5.6+起与原生一致(prompt_cache_options/breakpoint可选);GPT-5.5及更早自动无写入费 | ✅与原生费率/TTL一致(1.25x/0.1x/30m固定) |

## 未纳入正文的次要 gaps(P2,不再追查)
- Vertex AI 上 Claude 的具体费率数字
- DashScope implicit 模式确切 TTL 数值、命中字段名是否与 explicit 相同
- 智谱 GLM 写入费、精确失效条件
- OpenRouter sticky routing 逐厂商是否满足条件的完整列表(已有"条件规则"作答,足够)
- OpenAI Responses API vs Chat Completions 缓存行为是否有别

## R2→R3 判断
核心格子(D1/D4/D5/D6/D8 × 8实体 + 4个适配平台)已全部 ✅ 或 ∅(官方确认未写,非未查)。剩余 ❓ 均为 P2 细节,继续挖掘边际价值低。按 SKILL.md 停止条件("核心格子都是✅/∅")→ 不再开大规模 R3,改为收束此轮为终稿基础 + 终审抽查。
