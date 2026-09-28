# parallel-search-skill

A multi-agent **deep-search skill** (vocabulary first → taxonomy → parallel expand → converge → observe → next round, hard length budget, layered deliverable) plus a **bench** that compares running it under different harnesses and models against single-shot Perplexity answers. Docs are in Chinese.

一套多 agent 深度调研 skill，**默认跑在 ZCode + GLM-5.3**（主/工人同模），调研任何领域直接 `/deep-search`：先反向生成领域词表（[vocabulary-first](https://github.com/justinatusa/vocabulary-first)：先对齐名字，再进入领域），从词表长出 taxonomy，再分轮并行扩展（一次 spawn 算一个 turn），每轮单独收束、按观察决定下一步。成稿分层交付：导读 `report.md`（长度上限、不许越改越长）+ 可选字段对照册 `atlas.md` + 可选细节页 `details/`，对标并超越 [justinatusa/llm-api-protocols](https://github.com/justinatusa/llm-api-protocols) 那套「分层、说人话、条理清晰」的成稿。外加一个 bench：同一道调研题，比较「直接调 Perplexity（换模型）」和「不同外层 + 模型调这个 skill」的效果。

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
| `skills/deep-search/` | skill 本体：`SKILL.md`（流程）、`references/`（词表 vocab、工人简报与笔记格式、收束与分层成稿骨架、各外层适配）、`agents/research-worker.md`（工人定义）、`scripts/`（`notes_lint.py`、`roundstat.py`、并行安全的 `pplx-safe`）、`CHANGELOG.md` |
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

ZCode（默认栈，GLM-5.3 主/工人同模；用户级安装后任何项目都能用）：

```bash
ln -s "$PWD/skills/deep-search" ~/.agents/skills/deep-search
```

然后 `/deep-search <调研任务>`。项目级的话把符号链接放进项目的 `.agents/skills/`（本仓库已自带）。

Claude Code（bench 对比用）：

```bash
ln -s "$PWD/skills/deep-search" ~/.claude/skills/deep-search
```

```bash
ln -s "$PWD/skills/deep-search/agents/research-worker.md" ~/.claude/agents/research-worker.md
```

然后 `/deep-search <调研任务>`。Kimi Code 用 `--skills-dir`，Grok Build 会读 `.claude/skills/`。各外层怎么派工人、怎么等一批、怎么指定工人模型，见 [references/harness.md](skills/deep-search/references/harness.md)。

成稿分层：导读 `report.md`（≤ budget）+ 可选 `atlas.md` 字段对照册 + 可选 `details/` 细节页；领域词表（vocabulary-first，来自 [justinatusa/vocabulary-first](https://github.com/justinatusa/vocabulary-first)，MIT）在 R0 反向生成、R1 起由工人对官方 glossary 核验，喂给 taxonomy、工人简报和成稿「先认识这些词」一节。

检索：工人默认通过 `scripts/pplx-safe` 调本地的 `pplx-web`（Perplexity Pro 网页会话客户端，**不在本仓库**，用 `PPLX_WEB_SCRIPT` 指向它）；没有它就用外层自带的网页搜索，再用网页抓取工具打开一手页面摘原句。

## 跑 bench

需要 `claude` CLI；Kimi Code ≥ 0.36、Grok Build、`pplx-web` 可选。`run_arm.py` 要联网（模型 API、Perplexity、各家文档站），在 Claude Code 沙箱里要关掉沙箱跑；Grok 需要代理时设 `PS_PROXY` / `PS_NO_PROXY`。

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

MIT，见 [LICENSE](LICENSE)。词表方法（vocabulary-first：seed / core lexicon / shibboleths 三件套、双向用法）来自 [justinatusa/vocabulary-first](https://github.com/justinatusa/vocabulary-first)（MIT），集成时做了多 agent 化改造。`bench/runs/` 里的成稿是各模型生成的调研文本，其中引用的官方文档版权归原作者。
