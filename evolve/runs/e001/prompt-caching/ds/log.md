# log

## R0
框架：8 实体（OpenAI / Anthropic / Gemini / DeepSeek / Kimi / 智谱 / 通义千问 / OpenRouter）× 9 维度（trigger/min_len/discount/ttl/storage/confirm/invalidate/scope/api）。分类轴假设：自动隐式 / 显式声明式 / 网关透传。写了 brief.md、grid.md v0。
外层参数：rounds=3, workers=6, budget=9000, dir=./ds，工人 subagent_type=research-worker（模型由外层固定），无 pplx-safe，工人用 WebSearch+WebFetch。

计划 R1：6 个工人按来源边界拆（6 个 worker-job 覆盖 8 个实体，Kimi+智谱 合并一个工人、通义千问+OpenRouter 合并一个工人，因为 workers 上限=6 < 实体数=8；其余 4 家一家一个工人）。每份简报要求同时填 9 个维度里能查到的部分，不单独派 scout——「confirm / invalidate」两个「坑」维度已经内建在每份简报里。

## R1 结果（6/6 完成，129 条主张，official 126/secondary 3，5 处冲突，28 gap，18 leads；lint：仅 r1-qwen-openrouter.md 8114 字符略超 8000 上限，2 条主张缺 quote，不影响使用）

观察：
1. 核心格子（trigger/discount/ttl/confirm）8 实体里 6 个（openai/anthropic/gemini/deepseek/kimi/qwen）已 ✅，Zhipu 缺 ttl（核心缺口），OpenRouter 核心已填。
2. **与常识相反、影响最大**：r1-anthropic 笔记 C2 称 2026-02-19 上线「自动缓存」，但同一笔记 C29 又说「无独立缓存管理 API，仅通过请求中 cache_control 参数控制」——两条并置有矛盾嫌疑，直接关系到用户点名疑点#1 的结论，必须核验原文精确语义再写入「一屏看懂」。
3. r1-openai 笔记称 GPT-5.6+ 出现可选 explicit 模式（prompt_cache_options.mode），且 TTL 出现两个不同数字（30 分钟 vs 2026-05-29 起默认 24h retention）未分清是否同一概念——同样关系到用户疑点#1，需消歧。
4. r1-gemini 的 discount（90% 折扣）主要来源是 cloud.google.com 的 Vertex AI blog，不是 ai.google.dev 的 Gemini Developer API 定价页，两者计费规则历史上可能不同，这是核心格子，需要用 ai.google.dev 交叉验证。
5. r1-kimi-zhipu 里 Zhipu 的 discount 数字（50%）明显低于其余厂商（普遍 ~90%），且 ttl/storage/invalidate/scope 全部是 gap，ttl 是核心格子必须补。
6. deepseek 的价格「冲突」实为新旧定价页时间先后（2024-08 vs 2026），不需要新调研，收束时按时间顺序写清楚即可。kimi 的「显式 cache_id → 自动」也是版本变化而非真冲突，当前文档（2026）就是现状结论，弃用时间点未知，写进未决即可，不单独派工。qwen/openrouter/kimi 的非核心格子（scope/api/storage）gap 不影响完成标准，不派工，直接记 ❓ 进未决。

决策：R2 派 4 个窄口径工人（核验 2 + 补缺 2），比 R1 更少更窄：
- r2-verify-anthropic-automatic：精确核验「自动缓存」是否等于零代码
- r2-verify-openai-ttl：核验 explicit 模式是否可选、30min 与 24h 两个 TTL 数字是否同一概念
- r2-gemini-pricing：用 ai.google.dev（非 Vertex）交叉验证折扣比例，顺带补存储费 gap
- r2-zhipu-gapfill：补 ttl（核心），核实 50% 折扣数字，顺带补 storage/invalidate/scope

预计 spawn：4

（说明：R1 后没有单独写 report.r1.md 快照——R1 刚收完就发现 anthropic/openai 的核心矛盾和 zhipu 的核心缺口，直接决定 R2 定向核验更划算，避免「写一版马上因核验结果整段重写」的浪费。R1 的收束动作（lint、grid 更新、taxonomy 检查、观察→决策）都做了，只是没经过 report.md 这一步；完整 report.md 在 R2 数据到齐后首次写出，等同于 R1+R2 合并收束。）

## R2 结果（4/4 完成，30 条主张全为 official，0 条缺来源，3 处冲突，9 gap，6 leads）

lint：4 份笔记全部 claims 有 src+quote，无超长笔记。

观察：
1. Anthropic 核验结论：确认"自动缓存"仍需加 `cache_control` 字段，只是自动选断点位置——用户疑点#1 的答案是"现在仍然成立，Anthropic 仍是唯一声明式默认"。
2. OpenAI 核验结论：默认仍是零代码 implicit；30分钟(`prompt_cache_options.ttl`) 和 24小时(`prompt_cache_retention`) 是两个独立不相交参数，不矛盾。
3. Gemini 核验结论：ai.google.dev 定价页数字与 Vertex blog 数学上一致（均 90% off），非真冲突，只是措辞来源不同；补上了 explicit 存储费具体数值。
4. Zhipu 核验结论：ttl/storage/invalidate/scope 二次确认官方未写（∅，非漏查）；discount 存在真实冲突（指南 50% vs 定价表实测 71~75%off），以定价表为准。
5. grid.md 核心格子（trigger/discount/ttl/confirm）8 实体 × 4 = 32 格已全部 ✅/∅/⚔(已给结论)，无遗留 ❓，达成 brief.md 完成标准。
6. taxonomy 换轴：v0 的「自动/显式/网关」三分不能解释"Gemini/Qwen 默认还是自动、但又有 explicit"，改成主轴「零配置默认是否缓存」二分（A自动默认/B声明式默认）+ 副轴「是否额外提供可选显式资源」，网关单列一类（转发 A 或 B，非独立机制）。改动记于 grid.md v1。

决策：核心格子已全部解决，不再派新一轮数据收集工人；R3 用于终审——按 converge.md 标准派 1 个审稿工人抽查 report.md 里 ≥20 条具体主张 + 做自洽检查。预计 spawn：1（审稿）。

## 收束（R1+R2 合并，首次写 report.md）
roundstat：report.md / snapshots/report.r2.md 均 6786 字符（budget 9000，余量 2214）；grid ✅58 ⚠6 ⚔1 ❓4 ∅3，resolved 61/72 (85%)。剩余 ⚠/❓/∅ 全部是非核心格子（storage/scope 等），已在第 5 节「未决」交代。

## R3 终审（1 个审稿工人，见 audit.md）
抽查 34 条具体主张：supported 34 / weak 0 / unsupported 0 / contradicted 0。自洽检查（一屏看懂↔矩阵↔坑↔未决逐条对照）：0 处不一致。倍数/百分比换算（0.1x=90%off 等 7 处）全部正确。10 个来源编号对应的域名全部核实无误。结论：不需要改动 report.md 正文，直接定稿。

## 终稿
report.md（ds/ 与仓库根目录 ./report.md 均已写入）：6786 字符，budget 9000，占用 75%。grid 核心格子（trigger/discount/ttl/confirm）8×4=32 格全部 ✅/∅/⚔(已给结论)。用户点名的 6 个疑点在「一屏看懂」逐条给出结论。流程：R1(6 工人数据铺开) → R2(4 工人核验冲突+补核心缺口) → 收束写第一版报告 → R3(1 工人终审) → 收束定稿，共 11 次 spawn。
