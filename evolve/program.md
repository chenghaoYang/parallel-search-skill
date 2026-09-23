# autoresearch for deep-search

让 agent 自己做实验，改进 `skills/deep-search`。改编自 karpathy/autoresearch 的 `program.md`（原文在 `upstream/program.md`，MIT）。
对应关系：`train.py` → `skills/deep-search/`（唯一被改的东西）；`prepare.py` → `evaluate.py` + `mech.py` + `judge_pair.md` + `config.json` + `bench/tasks/`（固定评测，不许改）；
`val_bpb` → 盲评对打分 `score`（越高越好）；5 分钟固定预算 → 固定的外层、模型和轮数/字数上限（`config.json` 的 `dev` 臂）。

和原版的主要差别：评测有噪声（LLM 写、LLM 评），一次实验要几十分钟、花真钱，所以加了 A/A 噪声基线、两段式评测（筛选 → 确认）、
隐藏的 golden、留出任务，以及多 agent 分工（提案者并行出候选，主 agent 评测和取舍）。

## Setup

1. **Run tag**：按日期取，例如 `sep24`。分支 `autoresearch/<tag>` 必须不存在。
2. **建分支**：从 `main` 执行 `git checkout -b autoresearch/<tag>`。
3. **读 in-scope 文件**：
   - `README.md`、`bench/README.md`：仓库背景。
   - `evolve/evaluate.py`、`evolve/mech.py`、`evolve/judge_pair.md`、`evolve/config.json`：固定评测。不许改。
   - `bench/tasks/<task>/task.md`：任务原文。**不许读** `golden.json` 和 `answers.md`（隐藏的测试答案，只给评测脚本用）。
   - `skills/deep-search/**`：被改进的对象。
4. **初始化 `evolve/results.tsv`**：只写表头。基线在第一次评测后记录。
5. **确认**，然后开始。

## 实验怎么跑

一次评测 = 用候选 skill 在若干开发任务上各跑一次 `dev` 臂（Claude Code，Sonnet 主 → Haiku 工人，WebSearch + WebFetch，
`--rounds 3 --workers 6 --budget 9000`，单次上限 60 分钟、$20，超时就杀掉、按当时的 `report.md` 打分），然后和在位者（incumbent）的同题运行做盲评对打：

```
python3 evolve/evaluate.py all eNNN --skill evolve/candidates/eNNN/skill --vs <在位者的实验号，逗号分隔> --tasks <任务> > evolve/logs/eNNN.log 2>&1
```

（要联网并启动嵌套的 `claude -p`：在 Claude Code 沙箱里要关沙箱跑；Grok 评审需要代理时设 `PS_PROXY`。）

对打：每位评审（Opus、Grok）× 两种顺序，各给 `overall ∈ {候选胜, 平, 负}` 和强度 1/2，换算成候选视角的 +2…−2，取平均。
两份文档用随机的 4 位文档编号命名（文件名和第一行都有），评审按编号作答——用 A/B 命名时 Grok 会把整份判决的标签弄反；
判决里引用的错误原文如果大多出自另一份文档，这份判决重评一次，仍然对不上就标 `suspect`、不计分。
开发任务：`prompt-caching`、`agent-protocols`、`py-packaging`。留出任务：`js-runtimes`（dev 臂）、`api-protocol`（`flagship` 臂：Opus 主 → Sonnet 工人），
只用来检查是否过拟合，**永远不参与取舍**。

**可以做什么：**
- 改 `skills/deep-search/` 下的任何东西：`SKILL.md`、`references/`、`agents/research-worker.md`、`scripts/`。流程、规则、模板、格式、脚本都可以改，也可以删。

**不能做什么：**
- 改评测：`evolve/evaluate.py`、`mech.py`、`judge_pair.md`、`config.json`、`bench/`。
- 读隐藏答案：`bench/tasks/*/golden.json`、`answers.md`。
- 把领域知识写进 skill：任何任务里的产品名、厂商名、字段名、结论、「这类题要查 X」的提示。skill 必须对任意调研题都成立。
  （harness 名字——Claude Code、Kimi Code、Grok Build 等——本来就在 skill 里，不算。）
- 改外层：模型、工具、参数都由 `dev` 臂固定。skill 只能在给定预算里做得更好。

**目标：在固定预算下，让盲评更偏好新版本。** 守住这些底线：成稿不超 `budget`（`len_ok` 全过）；不崩（`statuses` 全 ok）；
golden 召回不明显下降（平均降超过 0.1 要有很强的对打优势才收）；单次花费不超过在位者的 1.5 倍（除非 `score ≥ +0.5`）。

**简单性原则**（原样保留）：其他都一样时，越简单越好。加了一堆规则只换来一点点提升，不值得；删掉东西而结果不变或更好，
是简化的胜利。衡量指标是 `skill_chars`（skill 里全部 `.md` 的字符数）：它是每次运行主 agent 和工人都要读的上下文。

**第一次运行**：建立基线。当前 skill 跑两遍（`e000a`、`e000b`），再让 `e000b` 对打 `e000a`——这就是 A/A 噪声：
同一个 skill 两次运行之间的分差。之后的取舍门槛按这个噪声定（见下）。

## 输出格式

`evaluate.py` 结束时打印：

```
---
exp:          e003
vs:           e000a,e000b
score:        +0.250
task_scores:  prompt-caching:+0.500 agent-protocols:+0.000
wins:         1/2  (verdicts 16)
dims_net:     orientation:+3 taxonomy:+1 coverage:-1 doubts:+4 ...
golden:       0.792  (vs 0.750)
chars_max:    8920
len_ok:       2/2
traceable:    0.91
spawns:       11.0
lead_web:     0
cost_usd:     21.4  (vs per run 10.3)
minutes:      41.2
skill_chars:  22110
statuses:     {'ok': 2}
```

取主指标：`grep "^score:" evolve/logs/eNNN.log`。判决理由在 `evolve/runs/eNNN/judge/<task>/*.json`（`reason`、`errors_x`、`dims`）。

## 记录结果

每次实验结束写一行到 `evolve/results.tsv`（tab 分隔）：

```
exp	skill_sha	score	wins	golden	chars_max	cost_usd	minutes	status	description
```

1. 实验号（`e000a`、`e001`…）
2. `skill_sha`（评测打印的 skill 内容指纹）
3. `score`（相对当时在位者；基线写 0）
4. `wins`
5. `golden`
6. `chars_max`
7. `cost_usd`（这次实验全部运行的合计）
8. `minutes`（单次运行平均）
9. `status`：`keep`、`discard`、`crash`、`baseline`、`holdout`
10. 一句话描述这次试了什么

同时在 `evolve/journal.md` 记一段：观察 → 假设 → 结果 → 为什么收/弃 → 学到什么。提案者靠它避免重复试同一个想法。

## 实验循环

分支 `autoresearch/<tag>` 上只有被收下的改动。`evolve/INCUMBENT` 写着在位者的实验号（对打时的参照运行）。

LOOP FOREVER：

1. 看状态：当前分支和提交、`results.tsv`、`journal.md`、`INCUMBENT`。
2. **出候选（并行）**：派 2 个提案者 agent，各给一个方向（见下），各自产出 `evolve/candidates/eNNN/skill/`（在位 skill 的副本上改）
   和 `hypothesis.md`。一个候选只试一个想法。
3. **评测**：每个候选在 3 个开发任务上各跑一次，对打在位者的全部参照运行。
   （原计划先在 2 题上筛选：A/A 显示同一 skill 两次运行单题能差 1.5 分，2 题筛选基本是抛硬币，改成直接跑 3 题。）
4. **复测**：三题合并 `score` 落在 (+0.15, +0.50) 之间的候选，再把 3 题各跑一次（新实验号 `eNNNr`），两次合并重新算 `score`。
5. **收**：三题合并 `score ≥ 门槛`、`wins ≥ 2/3`、没有哪题 ≤ −0.5、底线全守住 → 把候选复制进 `skills/deep-search/`，在 `CHANGELOG.md` 记一条，
   `git commit`（「前进」分支），`INCUMBENT` 改成这个实验号。门槛：只跑一遍 3 题时 +0.50；加上复测、6 次运行合并时 +0.35（A/A 修正后是 +0.58，见 journal）。
   同一代两个候选都过门槛：收分高的；另一个在下一代和新在位者合并后重测。
   分数在 ±门槛之内、但 `skill_chars` 降了 ≥ 10%、底线全守住 → 也收（简化的胜利）。
6. **弃**：其他情况。在位 skill 不动。
7. 记 `results.tsv` 和 `journal.md`。
8. 每收下 3 个改动，或在位者已经跑过 3 代，就重跑一次在位者（新实验号，三题），把它加进 `INCUMBENT`
   ——参照运行越多，对打越不吃单次运气。

不要为了省事重用旧的对打：只拿同一个 `INCUMBENT` 集合比。

**提案方向**（每代挑两个不同的；看 `journal.md` 里哪个方向还有没试过的想法）：

- **收束与成稿**：一屏看懂、taxonomy 是否贯穿、点名疑点的结论、篇幅与压缩、终审后怎么改稿。
- **扩展与证据**：R1 怎么拆题、简报写法、工人规则和笔记格式、反常主张的复核、追问还是新派、什么时候停、花费和时间。
- **简化**：删掉没起作用的规则，合并重复说明，缩短 skill 文本而不降质量。
- **组合**：把之前分数为正但没过门槛的两个想法合在一起。
- **自由**：读证据，挑当前最大的失分点。

**提案者简报**（主 agent 填好 `<>` 后原样发出）：

```
你是 deep-search skill 自进化实验的提案者。实验号 <eNNN>，方向：<方向>。仓库根目录 <repo>，分支 autoresearch/<tag>。
先读 evolve/program.md（尤其「不能做什么」），再读 evolve/results.tsv、evolve/journal.md、skills/deep-search/ 全部文件。
证据：在位者和最近候选的运行 evolve/runs/<实验号>/<任务>/（report.md、prompt.md、ds/log.md、ds/grid.md、ds/notes/、ds/audit*.md、meta.json），
盲评判决 evolve/runs/<实验号>/judge/**.json（reason、errors_x、errors_y、dims）。不许读 bench/tasks/*/golden.json、answers.md。
要做的：
1. 从证据里找一个具体失分点或浪费（写出是哪几次运行、哪一段），提出一个可检验的假设。不要重复 journal.md 里已经弃掉的想法，除非你能说清这次有什么不同。
2. cp -R skills/deep-search evolve/candidates/<eNNN>/skill，只改这个副本。改动围绕这一个想法，越小越好；删规则也是合法的实验。
3. 不写任何领域事实或任务相关提示，skill 必须对任意调研题都成立。不改 evolve/ 和 bench/ 下的其他文件。
4. 写 evolve/candidates/<eNNN>/hypothesis.md：证据 → 假设 → 改动（文件、大意）→ 预期变好的维度/指标 → 风险。
回复 ≤ 6 行：一句话描述（会写进 results.tsv）、改了哪些文件、diff 行数、预期效果。
```

**超时**：`evaluate.py` 把单次运行卡在 60 分钟。超时的运行按当时的 `report.md` 打分（常常很差），不另作处理。

**崩溃**：候选自身的低级错误（脚本语法、路径写错）→ 修好重跑一次；想法本身跑不通 → 记 `crash`，继续。
外部故障（限流、网络、账号配额）不是候选的错：修好环境后重跑，不记成候选的结果。

**留出检查**：每收下 3 个改动、以及结束前，用当前在位者跑一次 `js-runtimes`（dev 臂），对打基线 skill 在同题的运行；
结束前再跑一次 `api-protocol`（flagship 臂），对打 bench 第二轮的 `cc-opus-sonnet` 成稿（那次用的是 v1.0）。开发任务上涨、留出任务不涨 = 过拟合信号，写进 journal。

**NEVER STOP**：循环开始以后，不要停下来问人要不要继续。人可能在睡觉，他们希望你一直干到约定的截止时间（或被手动打断）。
想法用完了就更用力地想：重读 skill 和最近的运行日志找新角度，组合之前的近似成功，试更激进的改动（重排流程、删掉整节）。
一次实验大约 1 小时，一晚能跑十来代。人醒来时应该看到 `results.tsv`、`journal.md` 和一个更好的 skill。
