# log

## R0 框架
- taxonomy v0：分类轴 = 缓存管理形态（A 隐式自动 / B 显式断点 / C 显式缓存对象 / D 网关透传）；8 个维度 D1–D8。
- R1 计划（spawn 6，按来源边界拆）：openai / anthropic / gemini / deepseek / cn3(Kimi+智谱+通义) / openrouter+scout。

## R1 收束（spawn 6，全部成功）
- 笔记 6 份，126 主张（125 official）。grid 85% 填（60✅/5⚠/2⚔/4❓）。
- taxonomy v0→v1 不变（分类轴成立）；成稿 7488 字符。
- R1 观察：Kimi k2.x 写/命中矛盾；智谱 TTL/隔离 ∅；多条否定/边界主张未反证；Bedrock/Azure/Vertex 为相邻 scope。
- → 动作：R2 派 3 个窄工人（cn 核验 / 反证包 / 平台适配层）。

## R2 收束（spawn 3，全部成功）
- 反证结果：F1 Anthropic opt-in 确认；F3 DeepSeek cache_control=Ignored 确认；F4 Kimi 无对象 API 确认（/v1/caching 实测 404+存档证曾存在）；F2 限缩——OR prompt 缓存在上游，但 OR 另有自建 Response Caching（edge，X-OpenRouter-Cache 头族）；F5 推翻——Vertex 可 PATCH cacheConfig disableCache:true 关 implicit（AI Studio 侧未见关闭明文）。
- Kimi k2.x 冲突未裁决：api/chat.md schema 称默认开启写入（无 per-model 限制）vs 指南"不支持 Cache Write"；自洽解读=K2 自动命中但无可计费写入，进§5。
- 新料：智谱定价页有逐模型命中价+存储费列（限时免费）+不支持型号；阿里 session 缓存=system+user 字符级精确匹配/1024 门槛/无定价；阿里显式失效规则原句；Bedrock/Azure/Vertex 一行级事实齐了。
- → 动作：重写 report（补平台适配行、修正 F2/F5），字数控制在 9000 内；然后终审工人。

## R3 终审收束（spawn 1 审稿工人）
- 审计 44 行：supported 38 / weak 5 / unsupported 0 / contradicted 1。
- 已修：阿里 Session 缓存"响应头"→"请求头"（contradicted）；Anthropic 隔离写全 Claude Platform on AWS（Bedrock/GCP 仅 org）；OpenRouter 粘性键改官方口径（首两条消息哈希/session_id）；写溢价区间不再误套 Qwen；cached tokens 归属修正（窗口=Gemini、TPM=OpenAI）；diagnostics 去掉"已 GA"（仅 leads 有据）。
- 终稿 8956± 字符 ≤9000；同步写 ../report.md。停止。
