# log

## R0
框架：8 实体 + Gemini 拆 explicit/implicit = 9 行；7 维度（机制/门槛/计费/TTL/命中字段/失效/模型范围）。
分类轴：自动前缀 vs 显式断点 vs 显式缓存对象；计费轴：纯读折扣 vs 写溢价 vs 存储计费。

## R1 计划（spawn 6）
- r1-openai: OpenAI prompt caching 全维度
- r1-anthropic: Anthropic cache_control 全维度（含 1h TTL、pricing）
- r1-gemini: Gemini explicit + implicit 双行
- r1-deepseek: DeepSeek 硬盘缓存
- r1-cn3: Kimi + 智谱 + 通义千问 三家
- r1-openrouter: OpenRouter 网关层 + scout（leads 找遗漏实体/坑）
R1 batch spawned at Fri Sep 25 04:42:02 CST 2026
- r1-cn3 返回：24 claims，Kimi/智谱/通义三行大体填满；冲突1（Kimi 写价 vs 命中价）；leads: 百炼 session 缓存、豆包/百度
- r1-anthropic 返回：23 claims 全 official。关键：2026-02-19 起有 automatic caching（顶层一个 cache_control 即 opt-in），beta header 已不需要；1h TTL 2025-08-13 GA；cache_miss_reason 2026-09-23 GA
- r1-openrouter 返回：25 claims。网关做断点互译/归一化，TTL 不互译，sticky routing 影响命中；leads: 跨租户时序侧信道、tools/schema 排序坑
- r1-deepseek 返回：19 claims。64-token 块粒度；deepseek-chat/reasoner 已于 2026-07-24 退役，v4-pro 路由到 V4.1-Flash
- r1-openai 返回：19 claims。仍默认自动；GPT-5.6+（2026-07）新增 prompt_cache_options/breakpoint 显式控制，cache write 1.25×；pre-5.6 prompt_cache_retention
- 待整批：r1-gemini

## R1 收束
- 6/6 工人返回，113 claims 全 official；grid 95% 填充（✅70 ⚠4 ∅3 ❓0）
- taxonomy v0→v1：轴A 由「自动vs手动」细化为四类（隐式自动/opt-in自动断点/手动断点/托管对象），因 Anthropic automatic 与 GPT-5.6 explicit 模糊了原二分
- ⚔ 裁决：Gemini 门槛/折扣以 2026-09-11 官方页为准（OpenRouter 页滞后）；DeepSeek v4-pro 价以 9/14 路由公告为准
- report.md 9037→8962（删未引用来源[8]）
- R1 观察：核心格近全填，剩余 ∅ 多为官方未写；边界主张中「智谱无TTL/开关」「Kimi无最小token」「Gemini implicit TTL未文档化」需反证后再定性
- → 动作：R2 派 2 个定向/反证工人（cn ∅ 反证 + DeepSeek/Gemini 缺口簇），不扩实体
- → 预计 spawn：2
R2 batch spawned at Fri Sep 25 04:55:26 CST 2026: r2-cn-falsify, r2-gaps

## R2 收束
- 2/2 返回；反证推翻 4 个 ∅/⚠：智谱 D7（定价页命中列=清单）、D4 部分（有存储按时计费维度、限时免费）、Kimi D2（k3 页 >256 tok）、通义显式 D7（分地域清单在主页+DashScope 原生支持）
- 新 ⚔：智谱指南「~50%」vs 定价页旗舰 ~20–25%（以定价页为准）；Vertex implicit 门槛 6,144 vs Gemini API 4,096
- 新事实：DeepSeek anthropic 端点 cache_control 全 Ignored；Kimi 显式断点 400、Messages 不传顶层 cc 只读不写
- report.md 9922→8999（压 923：删 cookbook 引用、来源标题缩写、D7 段落合并、坑条目压缩）
- R2 观察：边界主张已反证完（智谱开关/TTL、Kimi 门槛、Gemini implicit TTL 6 页查无）；grid 仅剩 ∅3 ⚠4 均为官方未写或标注存疑
- → 动作：终审，3 个核验工人按域名聚簇（openai+openrouter / anthropic+gemini / deepseek+国内三家），各 ≤10 判定项
终审批次 spawn（3 核验工人，30 判定项）at Fri Sep 25 05:09:42 CST 2026

## 终审
- 3 核验工人、30 判定项：27 confirmed、2 走样、1 not-on-page(404)
- 修正：OpenAI 断点引用改挂指南页（API ref 404）；Kimi k2 命中价 ¥1.10–2.60；Gemini 读价改「多数 10%、TTS 25%」、存储注 Priority 上限 $8.10；diagnostics 改「出 beta」
- 终稿 8906 字符 ≤ 9000，写入 ds/report.md 与 ../report.md
