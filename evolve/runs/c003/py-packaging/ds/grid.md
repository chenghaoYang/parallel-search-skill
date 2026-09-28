# grid v0

## 分类轴（taxonomy 骨架）
- A1 生态系：PyPI-only vs conda 生态（跨语言）。pixi 属 conda 生态，其余属 PyPI。
- A2 定位：纯安装器（pip）vs 全项目管理器（uv/Poetry/PDM/pixi）。
- A3 Python 运行时归谁管：工具自带下载/切换（uv、pixi、PDM?）vs 依赖外部解释器（pip、Poetry?）。

## 维度（列）
- D1 锁文件：文件名、格式、是否 PEP 751 pylock.toml、是否跨平台统一。
- D2 项目元数据：[project] (PEP 621) 还是自有表（[tool.poetry] 等）。
- D3 workspace/monorepo：是否支持、机制名（workspace members / path deps）。
- D4 Python 版本管理：能否下载/固定/切换解释器。
- D5 构建后端：默认/自带 backend。
- D6 环境与安装位置：venv/.venv、__pypackages__ (PEP 582)、conda env。
- D7 迁移：从 pip/requirements、poetry、pipenv、conda env 迁入的官方命令/插件。
- D8 CI 与缓存：官方 setup action、cache 目录/命令。
- D9 私有源：index 配置字段、凭证机制（keyring/env/auth）。
- D10 脚本/任务：内置 task runner（pixi tasks / pdm scripts / poetry run 等）。

## 网格（行=实体，格状态 ✅/⚠/⚔/❓/∅/—）

| 实体 | D1锁 | D2元数据 | D3ws | D4py | D5backend | D6env | D7迁移 | D8CI | D9私有源 | D10任务 |
|---|---|---|---|---|---|---|---|---|---|---|
| uv | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| pip | ❓ | — | — | — | — | ❓ | — | ❓ | ❓ | — |
| Poetry | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| PDM | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| pixi | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| (次要: hatch/conda-lock 等) | | | | | | | | | | |

## 横向疑点格
- X1 PEP 751 状态：定稿？pylock.toml 各工具支持度（uv/pip/PDM/Poetry/pixi）→ 由 D1 各格 + scout 汇总。
- X2 Poetry 2 [project] 表 → Poetry D2 格。
