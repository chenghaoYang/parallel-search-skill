# journal（autoresearch/sep24）

每个实验一段：观察 → 假设 → 结果 → 为什么收/弃 → 学到什么。提案者读这里，避免重复试同一个想法。

## 设置

- 被改对象：`skills/deep-search/`（起点 v1.1，skill_chars 见 e000a）。
- dev 臂：Claude Code，Sonnet 主 → Haiku 工人，WebSearch + WebFetch，`--rounds 3 --workers 6 --budget 9000`，60 分钟 / $20 上限。
- 开发任务：prompt-caching、agent-protocols、py-packaging。留出：js-runtimes（dev 臂）、api-protocol（flagship 臂）。
- 评审：Opus + Grok 盲评对打，两种顺序。

## e000a / e000b — 基线 v1.1 跑两遍（A/A）

- 6 次运行全部 ok：22–34 分钟，$6.3–9.1/次，10–13 次 spawn，成稿 6.3k–9.0k 字（两次顶到 9000 上限），主 agent 没自己上网。
- A/A 对打（e000b vs e000a，12 个判决）：agent-protocols −0.5、prompt-caching +0.5、py-packaging +0.5，合计 +0.167。
  **单题噪声约 ±0.5**，三题平均的噪声约 ±0.3。取舍门槛定为三题合并 `score ≥ +0.30`、`wins ≥ 2/3`、且没有哪题 ≤ −0.5。
- Grok 评审有明显的位置偏好（同一对文档换顺序就翻），Opus 较稳；两种顺序都跑是必要的。
- 判决里两份基线都有被点名的硬错（版本号、商业条款、缓存创建方式等），多半来自 Haiku 工人的笔记或主 agent 合并时写错——提案者的主要线索。
- golden 针第一版有过窄的英文原句（中文成稿永远命中不了），开跑前改成字段名/版本号/中英双写，主张和来源没动。改后召回 0.84–0.93，区分度不高，只当底线指标。
- 账号周用量 65% → 67%（6 次 dev 运行 ≈ 2%）。循环在周用量到 85% 时停止启动新的 Claude 运行。

## 评测修正（e001/e002 开跑前）

- 提案者 e002 发现：Grok 在 yx 顺序下有两份判决把 A/B 标签整份弄反（`errors.A` 引的原文只在 B 里）。我按原文片段逐份核对，6 份 Grok 判决里 2 份反了，Opus 的 6 份都对。
  纠正后 A/A 是 +0.67（py-packaging 单题 +1.5）——同一个 skill 两次运行的差距比预想大得多，之前「Grok 位置偏好」的判断是错的，是标签错位。
- 修正：两份文档改用随机 4 位编号命名（文件名 + 第一行），评审按编号作答；判决里引的错误原文大多出自另一份就重评，仍不对就标 suspect 不计分。
  第一次上线时 Opus 评审只有 Read/Write、看不到目录，找不到随机文件名——把两个文件名写进提示词后解决。旧判决留在 `runs/e000b/judge.v1-ab-labels/`。
- 流程随之改为：候选直接跑 3 题（不做 2 题筛选），分数在 (+0.15, 门槛) 的再复测一遍。
- 修正后的 A/A（12 份判决全部通过原文归属检查）：agent-protocols 0、prompt-caching +0.5、py-packaging +1.25，合计 **+0.58**。
  同一个 skill 的两次运行，质量差距真实存在（py-packaging 四份判决全部偏向 e000b）。门槛因此提到：一遍 3 题 +0.50；复测后 6 次合并 +0.35。
  候选总是对打 e000a、e000b 两次运行的合集，参照方的运气会被平均掉一部分。

## e001 — 终审加成稿自洽检查（收束与成稿）→ discard

- 证据：A/A 判决的 54 条错误里 23 条是成稿自相矛盾（一屏看懂/家族/坑与矩阵不一致、推导数字算错、流程计数写进正文）。
- 改动：终审除原子抽查外逐条对照矩阵、重算数字、核对 [n]；改稿以笔记原句为准。+3.4% skill_chars，不加 spawn。
- 结果（Claude dev 臂，24 判决）：+0.083；agent-protocols +0.38、prompt-caching +0.75、py-packaging **−0.88**。doubts +14、accuracy +4，但 **sourcing −15**，traceable 从 1.0 掉到 0.62。
- 解读：自洽改稿本身有用（doubts/accuracy 升），但改稿时丢了来源（成稿 URL 追不回笔记）。以后如果重试，要把「改概括时保留 [n]、来源节不许缩」写进去。

## e002 — 边界主张先反证（扩展与证据）→ keep

- 证据：A/A 判决去重后 27 条硬错，约 16 条是边界主张（否定、排他、强制、全称、时间边界），grid 里都标 ✅，从没被送去核验；六次运行里四次 R3 一个工人都没派。
- 改动：观察表那行换成「进一屏或疑点结论的边界主张先反证」；停止条件加「边界主张都已反证」；工人写否定/排他/起始版本前重取页面、查 changelog 最早条目；终审不许把没找到来源改成否定句。+6.9% skill_chars。
- 结果（Claude dev 臂，24 判决）：**+0.500**（刚好到门槛）；agent-protocols +1.13、prompt-caching 0（Opus 四票全负、Grok 四票全胜）、py-packaging +0.38。doubts +15、accuracy +9、coverage +8；orientation −7。单次 $6.8（在位 $7.7）。
- 收下，成为在位者。注意 prompt-caching 上两位评审完全相反，说明这题的优劣取决于评审看重什么。

## 切换到 Grok（用户 03:50 的要求：都用 Grok 来进化，还有 swe2，刚进化的也不要浪费）

- 之后的候选在两个 Grok 臂上评测：`grok`（grok-4.7 主 → grok-4.7 工人）、`grok-swe2`（grok-4.7 主 → swe-2 工人），评审只用 grok-4.7（两种顺序），提案者也换成 Grok（`evolve/propose.py`，沙箱里跑，读不到 golden）。
- swe-2 此前在 Grok Build 里报 `missing field output_tokens_details`：devin2api 的 usage 缺字段。加了 `bench/devin_shim.py`（本地转发、只补 usage 字段），Grok 配置里加了 `swe-2-shim` 模型。
- 不浪费：v1.1 在两个 Grok 臂上的基线（g000*/s000*）是 Grok 进度的锚点；e002 版本先在 Grok 臂上复验（跨外层确认），之后的候选都对打 Grok 臂上的在位运行。
