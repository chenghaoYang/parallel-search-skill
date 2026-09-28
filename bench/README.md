# bench

任务在 `tasks/<task>/`：`task.md`（用户视角的调研题：seed keywords、半对半错的 variation、范围要求、四行元指令）、
`golden.json`（隐藏答案：claims 的 groups/hosts/source/quote，只计召回）、`answers.md`（人工核对用参考答案）。

## 任务清单（2026-09-24 起 9 题）

| 任务 | 主题 | 角色 |
|---|---|---|
| prompt-caching | 各家 LLM API prompt caching 差异 | dev |
| agent-protocols | MCP / A2A / ACP / AG-UI 等 agent 协议 | dev |
| py-packaging | uv / pip / Poetry / PDM / pixi | dev |
| llm-inference | vLLM / SGLang / TensorRT-LLM / llama.cpp | dev |
| durable-execution | Temporal / Restate / DBOS / Inngest / Hatchet | dev |
| js-runtimes | Node / Deno / Bun | 留出（dev 臂过拟合检查） |
| api-protocol | chat completions / Responses / generateContent 等 | 留出（flagship 臂） |
| kv-stores | Redis / Valkey / Dragonfly / KeyDB（license + 线程模型） | 留出 |
| structured-outputs | 各家 strict JSON schema / structured output 能力 | 留出 |

dev 集用于每次实验的对打评分；留出集只查过拟合，不参与取舍。

## 跑法

- 跑一个方法：`python3 run_arm.py <arm> --force`
- 盲评：`python3 judge.py <arm> ... --passes 2`
- 汇总：`python3 summarize.py`
- 看进行中的 Claude Code 方法：`python3 progress.py <arm>`
- evolve 循环的固定评测走 `../evolve/evaluate.py`（arm 定义在 `../evolve/config.json`：dev / flagship / grok / grok-swe2 / cc-swe2）

## golden 写法（踩过的坑）

- 针（groups 里每个元素）要短而有区分度：字段名、版本号、license 名、参数名最好；中英文同义各备一个。
- 不许用长英文原句当针——中文成稿永远命中不了。
- 裸数字（`0.1`、`10`、`7.5`）单独成组太弱，要带单位或上下文的同义写法（`0.1x`、`10 层`、`compute capability`）。
- `quote` 必须是打开 `source` 页面逐字摘的原句（≤40 词）；`hosts` 写官方域名。
- 打完用 `score.py` 对 `answers.md` 干跑一遍 recall，理想值接近 1.0。

第一版（pplx 1 路 vs 4 路）的说明在 `../archive/2026-09-23/bench-v1/任务说明.md`。原始 json 仍在 `runs/pplx-scale-*`。
不要再跑已删除的 `run_expand.py`。
