# evolve：deep-search 的自进化循环

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
