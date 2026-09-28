# 日志

参数：rounds=3 workers=6 budget=9000 dir=./ds worker-model=swe-2-shim。检索：web_search 找页，web_fetch 取原句。无 pplx-safe。

## R0

观察：用户要的是选择框架，不是五个工具的说明书。种子是 uv、pip、Poetry、PDM、pixi/conda。点名疑点是 PEP 751（uv 与 pip 是否都支持 pylock.toml）和 Poetry 2 是否改用 `[project]`。

决策：taxonomy v0 用两根轴——项目真相在哪一层（安装器 / PyPI 项目管理器 / conda 求解器），依赖宇宙（仅 PyPI 系 / conda channel±PyPI）。九个正交维度见 grid.md。conda 先占行不进 R1 正文。

R1 计划：按来源站拆 5 个实体工人（uv、pip、Poetry、PDM、pixi），外加 1 个 scout（坑、以及 hatch/rye/pip-tools/pipenv/conda/mamba 是否该升格）。预计 spawn：6。

## R1

spawn：6（uv、pip、Poetry、PDM、pixi、scout）。全部返回。lint：154 条主张全是 official；pip C13 无原句（workspace 检索 0 命中）；pdm/pixi/poetry/scout/uv 五份笔记超过 8000 字，收束时只用了能对上原句的句子。

taxonomy：v0 保留。轴 1（项目真相在安装器 / pyproject / conda workspace）解释了锁文件名、元数据表、构建后端。没有改轴。

网格：五行里 pip、Poetry 的 workspace 为 ∅；pixi lock 为 ⚔（示例 version 6 vs changelog v7）；conda 整行仍是 ❓。scout 的 hatch / pip-tools / pipenv / rye / mamba 只进 leads，不进成稿。

成稿：从头重写 `ds/report.md`，8986 字（预算 9000）。来源节只保留 URL，标题会把篇幅顶过预算。快照 `snapshots/report.r1.md`，并复制到仓库根 `report.md`。roundstat：✅ 42，⚔ 1，❓ 9，∅ 2，resolved 44/54。

新增：五家的锁文件名、pylock 读/写命令、`[project]` 与 `[tool.poetry]` 的分工、workspace 键、解释器命令、build-backend 字符串、迁入命令、缓存变量、私有源键。
压掉：scout 升格建议、笔记里原句没有「实验性 / preview」的转述、PEP 751 的字段长清单、重复的散文。

R1 观察：第 0 节已经写了 D1（uv/pip 都有 pylock，但都不是项目锁；pip 标 EXPERIMENTAL）和 D2（Poetry 2.0 读 `[project]`，且未废弃 `tool.poetry.dependencies`），以及「PDM 不支持 poetry-core」。这些是时间边界或否定，笔记里还没有用更晚的 changelog 找过反例。conda 行是种子里的空行。pixi 锁版本是唯一的 ⚔。hatch/pipenv/pip-tools 在范围内，但 9000 字再加三行会挤掉核心矩阵，这轮不升格。

→ 动作：三份反证（uv、pip、Poetry，Poetry 顺带核 poetry-core 是否已能读 PEP 621），一份 conda 定向填格，一份 pixi 只核锁版本和有没有 pylock 反例。

→ 预计 spawn：5。
