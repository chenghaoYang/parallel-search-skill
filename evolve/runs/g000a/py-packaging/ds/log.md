# log

## R0

观察：读者要在新项目里五选一（uv、pip、Poetry、PDM、pixi/conda），并核对两件旧说法——标准锁文件 PEP 751，以及 Poetry 2 的 `[project]` 表。还没有一手来源。

决策：taxonomy v0 用两条轴。A1 生态谱系（PyPI/PyPA vs Conda/prefix）解释锁文件和包宇宙；A2 职责宽度（安装器 vs 项目管理器 vs 解释器+系统库）解释 Python 版本管理和 workspace。十个维度正交。conda、hatch、pip-tools、rye 先不占行。

spawn：0

结果：写出 `brief.md`、`grid.md`。矩阵 50 格全是缺口。

## R1

观察：6 份笔记都是 official，lint 无缺 src/quote。笔记超过 8000 字符：uv、pip、pdm、scout（lint 只警告，未改工人原文）。

taxonomy v0→v1：轴不换。A1/A2 仍解释「包从哪来」和「管到哪一层」。「锁是否跨平台」收进 D2，不新开列。「sync 会不会删包」先不进网格（只有 scout）。新增 conda 行。hatch、pip-tools、rye 不进矩阵。

格子：uv/pip/PDM 的锁、Poetry 的元数据/锁/Python/依赖组、pixi 的构建和缓存是冲突。Poetry workspace 已查过，官方没有这一页。pixi 多包成员没摘到。conda 整行空。点名两问的版本标题（pip 25.1/26.1、PDM 2.24/2.25）没进 quote，一屏看懂只写了原句撑得住的边界。

spawn：6（r1-uv、r1-pip、r1-poetry、r1-pdm、r1-pixi、r1-scout）。全部返回，无重派。

结果：重写 `report.md`。scout 不进正文。

字数：8991（预算 9000）。相对上一轮：第一份成稿。roundstat：✅ 39，⚔ 9，❓ 11（另有分类轴里一处图例误计已改），∅ 1，resolved 40/60。

R1 观察：点名两问和 PDM 导出都是冲突或版本标题缺失；conda 是种子里的空行 → 动作：四份一手核验加一份 conda 定向，不再全面重查，不派 hatch → 预计 spawn：5
