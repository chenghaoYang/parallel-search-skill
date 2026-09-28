# Log

## R0
观察：任务给定核心四家（OpenAI/Anthropic/Gemini/DeepSeek）+ 第二梯队（Kimi/智谱/通义千问/OpenRouter），用户点名 5 个疑点。
决策：taxonomy 按「缓存声明方式」分四类家族（全自动隐式/显式缓存对象/手动断点/网关透传），11 个正交维度。
动作：写 brief.md、grid.md v0。不 spawn。
下一步：R1，6 个工人 = 4 个核心实体深挖 + 2 个 scout（国内第二梯队 + 网关/跨厂坑）。

## R1 收束
观察：6/6 工人成功，134 条主张（129 official/5 secondary），0 条缺 src/quote，6 条 conflicts 大多是「表述深度不同」非真矛盾。核心发现：Anthropic 2026-02-19 已上线自动缓存（推翻「必须手动」传言），OpenAI GPT-5.6+ 反而新增了可选显式断点；Kimi 是三家国产里唯一纯手动的一家。
决策：taxonomy v0 的四分互斥轴不成立（多数实体双轨并存），换成「双轨/纯自动/纯手动/透传」四类，Kimi 归纯手动、DeepSeek+智谱归纯自动。D8(失效条件)从矩阵移到 report 第4节「坑」，避免重复。
动作：grid.md 重写为 v1（76% 格子 ✅），report.md 从头写（6876/9000 字符），snapshot r1，roundstat 记录。
字数轨迹：0 → 6876（首次写稿，无「增长」可比）。
下一步：R2，3 个工人（比 R1 更少更窄），只打定向缺口——Anthropic beta header现状+存储介质；Gemini隐式TTL+失效条件；Kimi官方命中字段名+智谱/通义千问隐式TTL。

## R2 收束
观察：3/3 工人成功，17条新主张全部official，0缺src/quote。关键结果：Anthropic确认完全GA无需beta header（修正了R1一条引用错位的弱主张）；Gemini隐式缓存TTL官方论坛明确回复"无法定义、不保证"；智谱隐式TTL同样确认官方未写(∅)；通义千问隐式TTL="无固定期限定期清理"；Kimi命中字段从二手升级为官方确认。意外发现：通义千问/阿里云百炼会代理DeepSeek/Kimi/GLM/MiniMax等第三方模型且走自己的缓存规则，补进report第1/3/4节。
决策：taxonomy不变（R2未推翻v1的四类划分）。5个用户点名疑点全部拿到一手结论（含"官方明确不保证"这类确定性答案）。剩余❓集中在P2细节（Kimi门槛/模型列表、智谱D9/D11、Gemini跨key/地域、DeepSeek推理模型支持），不影响核心结论。
动作：report.md重写v2(6876→7839字符，+963，因为在解决真缺口而非注水)，grid.md→v2，snapshot r2。
下一步：判定核心格子已✅/∅、且本轮新增主张(17)远少于R1(134)——满足停止判据，不再开R3定向扩展，直接进终审：派1个审稿工人抽查≥20条主张。

## 终审
派1个审稿工人，抽查report.md第0-5节共45条具体主张（远超≥20的要求），逐条对照9份笔记的[C#]判定。
结果：45条全部supported，0条weak/unsupported/contradicted。5条最高影响力主张（Anthropic自动缓存+GA无header、OpenAI新增显式breakpoint、Kimi纯手动、Gemini隐式TTL不保证的官方原话、智谱0.25x折扣换算）逐条确认成立。
决策：不需要任何修正性编辑，report.md v2（7839/9000字符）即为终稿。
状态：完成。dir=ds/，最终文档同步在 ds/report.md 与仓库根目录 report.md。
