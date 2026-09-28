---
name: search-evolution-review
description: 查看 parallel-search-skill 的 deep-search 进化或 bench 跑次，区分成稿、执行失败和盲评完成，解释候选对在位者的证据。用于进度、失败排查、候选取舍依据和评测维护；不代替业务调研用的 deep-search，也不自动开始进化循环。
---

# Deep-search 进化与跑次维护

命令从仓库根运行。先读 [evolve/README.md](../../../evolve/README.md)、[program.md](../../../evolve/program.md) 与本次相关的 `evolve/journal.md` 条目；读取 `evolve/config.json`、`INCUMBENT`、`results.tsv` 和 git 状态确定当前臂与候选。旧 README 的模型、任务数和示例门槛不能覆盖实际跑次配置与同臂 A/A 决策。

`skills/deep-search/` 是被测产品，`evolve/candidates/*/skill/` 是候选副本；`.agents/skills/` 服务仓库维护，不装入被测技能。维护请求不等于授权程序中的 LOOP FOREVER、建分支、初始化结果表、启动模型或采用候选。

## 查进度，不重跑

已有实验号时：

```bash
python3 evolve/status.py EXP
```

它读取 arena 的 transcript、notes 与 snapshots。`PS_ARENA` 是 arena 基目录，evolve 脚本会再拼 `/evolve`；优先从目标 `meta.json` 的 `arena` 字段定位。无输出可能是 arena 不在这台机器或已移除，回看仓库 `evolve/runs/EXP/`，不能说“实验不存在”。

`status.py` 的 `done` 仅表示产物 `meta.json` 存在，`live` 只是还没该文件，都不是进程或成功判定。对目标任务读 `meta.json` 中的 `status`、`returncode`、`is_error`、`mech.chars` 与实际 `report.md`；error/timeout 也可能有稿，保留并如实报告。若需要确认仍在跑，再核对该任务真实进程和日志时间，不根据 spawns/字数单独判断。

bench 的 Claude Code 臂用 `python3 bench/progress.py ARM_ID`；旧比较表用 `python3 bench/summarize.py`（固定读历史 bench 的 arms 与 judge 目录，不能替代 evolve 的候选对打）。

## 判断是否完成盲评

优先读 `evolve/runs/EXP/summary.json` 与 `judge/<task>/*.json`，核对：

- `vs` 是用户要比较的同一组在位者运行，arm、模型、任务和预算一致；不同臂的评审不是同一把尺。
- `tasks` 和各任务判决覆盖完整；score 只平均有分数的任务，缺判任务可能没进入分母。不能把部分正分写成通过。
- 判决保留两种展示顺序及该臂配置的 passes；`suspect` 不计分。按判决 `x`/`y` 还原方向，不凭文件顺序或历史 A/B 标签猜候选胜负。
- 取舍依据是该臂的 A/A 噪声与当前 journal 决策，同时看失败状态、长度与成本。`INCUMBENT`、results 和 journal 记录采纳，正 score 本身不是 KEEP。

需要重算已有判决汇总时才用：

```bash
python3 evolve/evaluate.py report EXP --vs BASELINE1,BASELINE2 --tasks TASK1,TASK2
```

`report` 不请求模型，但会重新计算机械指标并覆盖 `summary.json`，所以纯状态查询直接读已有文件。它的手写参数解析不支持普通 `--help`；参数查 `evaluate.py` 文件顶部 usage。`judge` 会调用模型补缺判，`run/all` 会删除并重建所列任务的输出和 arena；它们不能用来“刷新进度”。

## 修复或提案边界

外部限流、余额、网关失败与候选质量分开报告。恢复必须对应用户授权，先看 journal 的当前并发经验与哪些任务缺稿；不要为了诊断试跑模型或调整另一项目的限流配置。不要重跑有用的失败稿来掩盖原状态。

进入用户授权的进化任务时才按 program 派提案者；候选只改自己的 skill 副本，一个假设对应现有证据中的一个失分点。固定评测文件与 bench 在该进化轮中不改；`bench/tasks/*/golden.json` 和 `answers.md` 不向提案者开放，留出不用于选候选。脚本可以产出机械指标，不需要 agent 阅读隐藏答案。

交付说明实验号、arm、成稿/预期任务数、成功执行/失败数、有效判决覆盖、比较对象，以及实际采纳记录；缺少的证据直接点明。普通维护用相关静态检查或已有只读工具验证，不运行整轮 bench 来证明文档修改。
