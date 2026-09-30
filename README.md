# parallel-search-skill

A **deep-search skill** for source-backed research: clarify the question, investigate independently useful directions, verify consequential claims, and write an answer people can actually read. Parallelism and supporting files are optional. Docs are in Chinese.

一套面向复杂问题的调研 skill。先弄清用户要理解或决定什么，再按需要并行查证；来源可靠、结论有边界，表达和结构随问题调整。可以直接 `/deep-search <调研任务>`，不强制词表、轮数或多层报告，也不依赖特定模型或检索服务。

本仓库同时保留跨模型/外层的历史 bench 和进化实验。下面的分数属于当时的版本与任务，不代表本次修订已经经过同样评测；旧指标中有固定章节和结构化笔记要求，不能直接用来评价新版的自然表达。

## 结果速览（2026-09-23，题目：LLM 时代 API 请求协议的差异）

| 方法 | Opus 评审 | Grok 评审 | 字数 | 用时 | 花费 |
|---|---|---|---|---|---|
| Claude Code，Opus 主 → Sonnet 工人 + skill | 9.0（第 1） | 9.0（第 1） | 19.7k | 83 min | $54 |
| Claude Code，Opus 主 → Opus 工人 + skill | 9.0（第 2） | 8.5（第 2） | 17.9k | 96 min | $96 |
| Kimi Code，GLM-5.3 → GLM-5.3-Flash + skill | 8.5（第 3） | 8.5（第 3） | 19.9k | 111 min | 订阅 |
| Grok Build，grok-4.7 → grok-4.7 + skill | 7.5（第 4） | 8.0（第 4） | 18.7k | 91 min | ≈$36 |
| 单次 Perplexity（8 个模型） | 3.5–5.0 | 4.0–6.0 | 31–41k | 2–3 min | 订阅 |

两个不同家族的盲评、各两遍，前四名顺序一致。细节、人工核验、外部参照（一份三层手册）、各外层踩到的坑和局限（每个方法只跑了 1 次；Perplexity 这轮配额用完，被回退到同一个模型）见 [bench/results.md](bench/results.md)。

## 目录

| 路径 | 内容 |
|---|---|
| `.agents/skills/deep-search` | 指向 `skills/deep-search/` 的符号链接，本仓内 ZCode 直接 `/deep-search` |
| `.agents/skills/search-evolution-review/` | 仓库维护技能：查看进化/bench 进度、判决与失败证据，复用已有工具，不启动评测 |
| `skills/deep-search/` | skill 本体：`SKILL.md`（核心原则）、`references/`（可选术语对齐、分工与证据笔记、整合写作、环境适配）、`agents/research-worker.md`（工人定义）、`scripts/`（`notes_lint.py`、`roundstat.py`、并行安全的 `pplx-safe`）、`CHANGELOG.md` |
| `bench/tasks/api-protocol/task.md` | bench 的任务原文 |
| `bench/arms.json` | 参赛方法（外层 × 模型），按外层微调提示词的规则，排除的方法和原因 |
| `bench/run_arm.py` | 跑一个方法：Perplexity 单次、Claude Code / Kimi Code / Grok Build + skill。在仓库外的临时目录跑，产物拷回 `bench/runs/<arm>/` |
| `bench/judge.py`、`bench/judge.md` | 盲评：匿名、打乱顺序，8 个维度打分并排名；`--judge claude`（Opus）或 `--judge grok`（换模型家族查自家偏好） |
| `bench/summarize.py`、`bench/score.py`、`bench/golden.json` | 汇总表；v1 golden（12 条官方文档事实的机械召回针） |
| `bench/progress.py`、`bench/grok_usage.py` | 看运行中的 Claude Code 方法；汇总 Grok 主 + 工人会话的 token 与花费 |
| `bench/runs/` | 每个方法的成稿 `report.md`、`meta.json`；skill 方法另有 `ds/`（brief、grid、log、每轮笔记、快照、审稿） |
| `bench/judge/` | 每遍评审的逐维分数与汇总 |
| `bench/fetch_external.py` | 重建外部参照（justinatusa/llm-api-protocols）的评审输入；原文不收进本仓库 |
| `archive/2026-09-23/` | 第一版 bench（Perplexity 1 路 vs 4 路）的说明与查询，公开资料笔记。原始检索在 `bench/runs/pplx-scale-*` |
| `evolve/` | autoresearch 式自进化循环：提案者出候选 → 同臂盲评对打在位者 → 过门槛才替换（[evolve/README.md](evolve/README.md)、[program.md](evolve/program.md)、[journal.md](evolve/journal.md)）。`runs/` 是完整证据链（transcript 不入库），`INCUMBENT` 记当前在位版本 |
| `private/` | 本地私有材料（笔记、transcript、第三方拷贝），不进版本库，公开仓库里不存在 |

## 用 skill

在已支持 skill 的环境里使用 `/deep-search <调研任务>`，或让 agent 读取 `skills/deep-search/SKILL.md`。按问题选择表达方式：一份解释清楚的回答往往比固定模板更有用；需要可复用的长文时再保存文件。

旧参数仍可用，例如：

```text
/deep-search 比较几种视频帧选择方法，重点看额外开销和适用条件 --workers 4 --rounds 3 --budget 12000 --dir ./deep-search/video-sampling
```

`workers` 是每批新派研究者的上限，`rounds` 是研究批次上限，不要求派满或跑满。`budget` 是主回答的字符上限（含引用），不是 token 或费用预算；没指定就按问题需要控制长度。`worker-model` 仅在当前环境支持时使用，否则继承环境设置。明确指定的文件路径和输出格式仍优先遵守。

本仓库的 `.agents/skills/deep-search` 已链接到 skill 本体。需要用户级安装时，按所用工具当前支持的目录安装；例如支持 `~/.agents/skills` 的环境可用：

```bash
ln -s "$PWD/skills/deep-search" ~/.agents/skills/deep-search
```

Claude Code 可使用 `~/.claude/skills/deep-search`，并按需把 `skills/deep-search/agents/research-worker.md` 链接到 `~/.claude/agents/research-worker.md`。不要覆盖已有的同名安装。

没有子 agent 时可顺序研究。默认使用环境现有搜索工具并读取原始来源。`scripts/pplx-safe` 是可选的 `pplx-web` 包装器；外部客户端不在仓库中，已配置的用户可通过 `PPLX_WEB_SCRIPT` 指定它。更多适配说明见 [harness.md](skills/deep-search/references/harness.md)。

词表、比较网格、过程日志、快照和附录只在有用时创建。需要诊断旧版 C# 笔记可运行 `notes_lint.py`；`roundstat.py <dir> --budget 12000` 检查显式字符上限，`--legacy-layout` 才启用旧版布局提示。这些脚本检查形式，不证明事实正确。离线回归测试可运行 `python3 -m unittest discover -s tests`。

## 跑 bench

需要 `claude` CLI；Kimi Code ≥ 0.36、Grok Build、`pplx-web` 可选。`run_arm.py` 要联网（模型 API、Perplexity、各家文档站），按当前环境的权限运行；Grok 需要代理时设 `PS_PROXY` / `PS_NO_PROXY`。

```bash
python3 bench/run_arm.py cc-opus-sonnet --force
```

```bash
python3 bench/judge.py cc-opus-opus cc-opus-sonnet pplx-best --passes 2 --judge claude --out my-run
```

```bash
python3 bench/summarize.py
```

## License

MIT，见 [LICENSE](LICENSE)。可选术语对齐的思路受 [justinatusa/vocabulary-first](https://github.com/justinatusa/vocabulary-first)（MIT）启发；本版不要求固定数量或分类。`bench/runs/` 里的成稿是各模型生成的调研文本，其中引用的官方文档版权归原作者。
