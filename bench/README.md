# bench

当前这一轮：任务 `tasks/api-protocol/task.md`，方法 `arms.json`，结果 `results.md`。

- 跑一个方法：`python3 run_arm.py <arm> --force`
- 盲评：`python3 judge.py <arm> ... --passes 2`
- 汇总：`python3 summarize.py`
- 看进行中的 Claude Code 方法：`python3 progress.py <arm>`

第一版（pplx 1 路 vs 4 路）的说明在 `archive/2026-09-23/bench-v1/任务说明.md`。原始 json 仍在 `bench/runs/pplx-scale-*`。
不要再跑已删除的 `run_expand.py`。
