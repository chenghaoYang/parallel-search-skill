# evolve：deep-search 的自进化循环

## 当前 skill 与历史评测

这里保留历史实验协议，便于复查旧结果；它不是当前灵活版 skill 的通用质量评分器。JSON 字段、计算、盲评规则和已有结果均未改写。`mech.py` 与 `evaluate.py report` 只在 stderr 提醒这些指标的适用范围，stdout 格式保持不变。

- `sections` 只匹配六类旧标题；没有这些标题不代表结构差。
- `traceable` 是正文 URL 与旧 C# 笔记 `src:` 的匹配比例，不验证网页是否支持主张。自由格式笔记或未建笔记时的 0 可能只是未按旧格式评估。
- `notes.claims_ok` 只查旧 C# 行中的 URL 与 `quote:` 字段，不核实摘录。没有可解析行时仍按旧算法返回 0，不能据此判断证据质量。
- `golden` 与 `bench/score.py` 测词面命中；`sourced_recall` 还检查来源主机是否在全文出现，不能证明它支撑对应结论。
- `score` 来自指定旧任务与 rubric 的盲评，不是这些机械值的加权总分。旧 rubric 中的 taxonomy、字段级覆盖等要求适合部分原任务，不能套到所有短答。
- `lead_web`、spawn 数和快照数是过程统计；新版允许主 agent 查资料、直接回答和按需留文件，不能单凭这些值判断失败。

新一轮行为评测应单独命名协议，保存 skill、任务、rubric 和外层设置的版本，不与旧分数混排。不要为修复零分而要求新版恢复固定章节或伪造 C# 笔记。

运行旧臂前还需检查其隐含约束：`flagship` 的机械预算是 20,000 字符，但当前 `params` 为空，新版 skill 不再默认这个上限；Grok 提示仍要求整批等待。若要调整，应创建明确标记的新协议/臂，不能悄悄改变历史工作负载。本次提示修订不更改这些设置，也不启动任何模型运行。

照搬 [karpathy/autoresearch](https://github.com/karpathy/autoresearch) 的做法（原文见 `upstream/`，MIT）：
agent 改一个东西、跑固定预算的实验、看一个指标、好就留（分支前进）、不好就丢，一直循环。这里被改的是 `skills/deep-search/`，
实验是 bench 上的一次深度调研，指标是盲评对打分。

| autoresearch | 这里 |
|---|---|
| `train.py`（agent 改） | `skills/deep-search/` |
| `prepare.py`（固定） | `evaluate.py`、`mech.py`、`judge_pair.md`、`config.json`、`bench/tasks/` |
| 5 分钟固定训练预算 | 固定外层与模型（Claude Code，Sonnet 主 → Haiku 工人）+ `--rounds 3 --workers 6 --budget 9000`，单次 ≤ 60 分钟 |
| `val_bpb`（越低越好） | `score`：候选 vs 在位者的盲评对打，Opus + Grok 两位评审 × 两种顺序，+2…−2（越高越好） |
| `program.md` | `program.md`（循环规则、取舍标准、提案者简报） |
| `results.tsv` | `results.tsv` + `journal.md`（每个实验的假设与结论） |
| `analysis.ipynb` | `analysis.py` → `progress.png` |

和原版不同的地方：LLM 写 + LLM 评有噪声，所以先跑两遍基线（A/A）量噪声，再定收下的门槛；评测分筛选（2 题）和确认（3 题）两段；
golden（`bench/tasks/*/golden.json`）对提案者隐藏，只当辅助指标；留出任务（`js-runtimes`、`api-protocol`）只用来查过拟合；
多 agent：每代并行派 2 个提案者出候选，主 agent 负责评测和取舍。

## 跑

```bash
python3 evolve/evaluate.py all e001 --skill evolve/candidates/e001/skill --vs e000a,e000b --tasks prompt-caching,agent-protocols
```

```bash
uv run --with pandas --with matplotlib python evolve/analysis.py
```

要联网并启动嵌套的 `claude -p`（以及 Grok 评审），在 Claude Code 沙箱里要关沙箱跑；Grok 需要代理时设 `PS_PROXY`。

## 目录

| 路径 | 内容 |
|---|---|
| `program.md` | 循环规则（给主 agent 和提案者读） |
| `evaluate.py` | run / judge / report |
| `candidates/eNNN/` | 提案：`hypothesis.md`、`skill.diff`（完整副本 `skill/` 不进版本库） |
| `runs/eNNN/<task>/` | 每次运行的成稿、`ds/` 过程文件、`meta.json`；`runs/eNNN/judge/` 盲评判决；`summary.json` |
| `results.tsv`、`journal.md`、`INCUMBENT` | 实验记录、实验笔记、当前在位者的参照运行 |
