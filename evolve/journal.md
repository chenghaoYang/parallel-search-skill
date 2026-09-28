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

## e004 — 等待窗口只许等整批（分工纪律）→ 提案已出，待评测（勘误见下）

- **勘误**：e004 提案者的 hypothesis 声称 `lead_web` 把工人抓页误计进父会话（Grok streaming 不标 `parent_tool_use_id`）。主 agent 复核证伪：s002（swe-2 工人臂）transcript 里 242 个工具调用全部 `model: grok-4.7`，工人事件不进主会话流；主 agent 的 thinking 原文是「I need to wait for all 6 … I'm looking for documentation on OpenRouter prompt caching」随后自己发了 web_search。**`lead_web` 是对的：Grok 主 agent 真的边等边抓页**（g000a 最高 175 次、约 2.1MB 原始页面进主上下文）。12 次 Grok 运行全部 timeout/error、没有一份 audit.md，主上下文被原始页面灌爆很可能是 75 分钟走不到终审的主因之一。
- 改动（+10/−10）：SKILL.md 把「派出整批 → 收束」之间的窗口写成可执行序列（想到的缺口记 `log.md` 一行 `待查：` → 一次 wait_all 或结束回合；窗口内不开页面不取 URL 不再 spawn；想开的页面写成下一轮简报派工人）；终审写明回原页只由审稿工人做；harness.md 删掉「grok 自己抓更全/建议禁 web_fetch」的错误记述，换成「父会话输出里的抓页记录是历史行为，不要顺着 URL 再抓」。
- 待办：g003/s003（e003）跑完后，e004 在两个 Grok 臂上评测；观察 `status→ok`、`audit.md` 出现、`minutes` 下降、`lead_web` 应显著下降（提案者预期「降不多」的前提已被证伪）。

## 阻断：Grok Build 余额耗尽（2026-09-24 ~10:50）

- e003 重跑中账户返回 `402 Payment Required — Grok Build usage balance exhausted`：g003 三题全 crash（~18min、$10–19/题烧完后断供）；s003 两题 error、一题苟延。所有 grok-4.7 调用（两臂的主 agent、评审、提案者）都走这个余额，**整条 Grok 进化线暂停，等充值或额度重置**。外部故障，不记成 e003 的结果。
- 另发现一个结构性限制：Grok 的 web_fetch 走 SSRF 防护，Clash fake-ip（198.18.x.x）的域名会被拦——实测 api-docs.deepseek.com、docs.x.ai 打不开。Grok 臂在这些域名上天生少一手证据，评 verdicts 时对相关失分要留意是不是环境问题而不是 skill 的错。
- bench 扩题完成：新增 `llm-inference`（15 claims）、`durable-execution`（16）、`kv-stores`（14）、`structured-outputs`（16），quote 均经 fetch 逐字核对。接入 dev_tasks 前要先给在位者在这些题上补参照运行（Grok 臂同样等余额）。

## 新臂：cc-swe2（Claude Code 全 swe-2，绕开 Grok 余额）

- 用户指出 swe-2 已接进 Claude Code：`~/.local/bin/claude-devin` 把 ANTHROPIC_BASE_URL 指向本地 devin2api（127.0.0.1:3003），lead/工人/评审全部 swe-2-max，262k 上下文。冒烟通过（$0.14/次）。
- config.json 加臂 `cc-swe2`（`cli: claude-devin`）；evaluate.py 支持 arm 级 `cli` 覆盖；bench/judge.py 加 `claude-devin` 评审后端（swe-2-max ×2 顺序 ×2 passes）。propose.py 加 `--model swe-2-max` 走 claude-devin。
- 注意：cc-swe2 的评审是 swe-2-max，和 Grok 臂的 grok-4.7 评审不是同一把尺——跨臂分数不直接比，只看臂内对打。Claude Code harness 下 `lead_web` 的 `parent_tool_use_id` 归因是准的（不像 Grok）。
- 首批：c002 = 在位者 e002 在 cc-swe2 上的参照运行；c003/c004 = e003/e004 候选。
- **cc-swe2 并发撞限**：12 个 lead × 6 工人同开，devin2api local gate 报 `429 resource_exhausted`（537s 重置），c002–c005 首批全 crash。教训：cc-swe2 臂一次最多 ~3–4 个并发 lead，`--parallel` 要调小或分批跑。
- **人工合并（2026-09-24，用户指示停止跑批、直接打磨）**：e003（引文保全+cite 检查）、e004（等待窗口纪律）、e005（终审核验群）按证据合并进 `skills/deep-search/` → v1.3-dev，见 CHANGELOG。e005 证据最硬（e002 审稿 44 条全 supported 但盲评 ≥4 条硬错）；e004 经 transcript `model` 字段实锤；e003 取其改稿引文规则折进 e005 的改稿步。三个候选**未过盲评**，等强臂恢复后 v1.3-dev 要作为整体复验。
- bench 扩到 9 题：dev_tasks=[prompt-caching, agent-protocols, py-packaging, llm-inference, durable-execution]，holdout=[js-runtimes, api-protocol, kv-stores, structured-outputs]。**注意**：在位者在新题上还没有参照运行，恢复评测前 c002 要先补 llm-inference、durable-execution 两题；golden 针已 lint+补强（裸数字组补带单位同义词）。
- **坑：`claude -p` 有后台等待上限 600s**（`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`，默认 600000）——lead 派完后台工人结束回合，工人 10 分钟内没回来进程就自杀（rc=0、report 没写 → crash）。Claude 臂的 Haiku 工人够快没踩过；swe-2 工人慢，c003 首发两题全这样死的。已在 run_one 给 claude-code 臂统一设 `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`（无限等；evaluate.py 自己的 timeout_min 是真上限）。e005 提案者加了 `--disallowedTools Agent`，单线程不触发这个坑。
