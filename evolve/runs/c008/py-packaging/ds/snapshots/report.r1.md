# Python 包管理工具怎么选：uv / pip / Poetry / PDM / pixi

> 依据各工具官方文档与 changelog，截至 2026-09-25。第 0 节结论，第 2 节按维度查表，[n] 对应文末来源。

## 0. 一屏看懂

- **先分两家**：uv / pip / Poetry / PDM 装 PyPI wheel、走 PEP 标准；pixi 装 conda-forge 跨语言预编译包，Python 解释器本身也是包[35][36]。要 CUDA/系统库/多语言选 pixi，纯 Python 留 PyPI 系。
- **PEP 751（pylock.toml）已 Final**（2025-03-31 接受，文件名固定 `pylock.toml`/`pylock.<name>.toml`，为多环境设计）[1]——但**没有一家拿它当默认锁**：pip 25.1 起实验性 `pip lock`、26.1 起 `pip install -r pylock.toml`（仅保证当前平台）[2][3]；uv 0.6.15 起可导出/`uv pip` 读 pylock.toml，项目主锁仍是专有 uv.lock[5][4]；PDM 2.25 起可 `lock.format="pylock"` 实验启用[19]；Poetry 仅插件导出[16][17]；pixi 用自家 pixi.lock[29]。
- **Poetry 2 确认改用标准 [project] 表**（PEP 621，2.0.0 起）[13][14]；[tool.poetry] 只剩 package-mode、requires-poetry 等专有配置；`^x.y` caret 约束不能写进 project.dependencies[48]。
- **monorepo**：uv 原生 workspace（members glob、单一锁、成员 editable）[6]；PDM 2.28 起实验性[20]；Poetry 无官方；pixi 是「一个 manifest 多 environment」而非包 workspace[30]。
- **装 Python 谁管**：uv `uv python install`、PDM `pdm python install` 用 python-build-standalone[7][21]；Poetry 2.1 起实验 `poetry python install`[46]；pixi 自动装 conda 包解释器[36]；pip 不管，配 venv/pyenv。
- **新项目默认**：纯 Python 选 uv（速度+workspace+解释器一体）；已在 Poetry/PDM 没痛点不必迁；要非 Python 依赖选 pixi；pip 只当安装器或配 pip-tools。

## 1. Taxonomy

两轴：**①装什么包**（PyPI wheel vs conda 跨语言二进制）、**②管多宽**（只安装 vs 声明→锁→环境→构建→发布全流程）。

| 家族 | 成员 | 为什么一类 |
|---|---|---|
| PyPI 安装器 | pip（+pip-tools） | 只装包；锁是后补的实验功能 |
| PyPI 项目管理器 | uv / Poetry / PDM | 职责集相同，差异在标准采纳度与覆盖 |
| conda 工作区 | pixi（conda/mamba 为上一代） | channel 跨语言二进制，锁覆盖全平台 |

维度：D1 元数据写哪张表 / D2 锁文件格式与可移植性 / D3 多包工作区 / D4 谁装解释器 / D5 构建后端 / D6 环境放哪 / D7 官方迁移 / D8 CI 缓存 / D9 私有源 / D10 其他 PEP 采纳。

## 2. 对照矩阵

| 工具 | D1 元数据 | D2 锁文件 | D3 workspace | D4 装解释器 | D5 构建后端 | D6 环境 |
|---|---|---|---|---|---|---|
| uv | [project] PEP 621 | uv.lock：universal 跨平台、uv 专有[4]；pylock 仅导出/`uv pip`[5] | `[tool.uv.workspace]` members glob、共享锁、成员 editable[6] | `uv python install/pin`（pbs）、.python-version[7] | 自带 uv_build（0.7.19 stable，**仅纯 Python**，扩展换 hatchling）；亦可作任意后端 frontend[8] | 自动建 .venv，`uv sync` 精确同步[51] |
| pip | —（无项目概念） | `pip lock`→pylock.toml（实验、仅当前平台）[3]；官方可复现路径=requirements `==`+`--hash`+wheelhouse[41] | — | 不管 | —（PEP 517 frontend） | 靠 stdlib venv[45] |
| Poetry | 2.0 起 [project]；[tool.poetry] 存专有配置；package-mode=false 纯依赖管理[13][14] | poetry.lock（v2.1，专有）[16]；pylock 仅插件导出[17] | 无官方；path `develop=true` 仅本地开发 | 2.1 起实验 `poetry python install`（Python Standalone）；或 `poetry env use` 已装解释器[46][18] | 默认 poetry-core；2.1 起后端无关[16] | {cache-dir}/virtualenvs 或已有 .venv[47] |
| PDM | [project] PEP 621；[tool.pdm] 专有；库标 `distribution=true`[24] | pdm.lock（跨平台）默认；`lock.format="pylock"` 实验（2.25）[19][21] | 实验（2.28）：`[tool.pdm.workspace]` members glob、共享锁[20] | `pdm python install`（pbs，2.13）；路径存 .pdm-python[21][24] | 不强制（默认 pdm-backend；不支持 poetry-core）[25] | 默认 .venv；`python.use_venv=false` 切 PEP 582 `__pypackages__`[22][23] |
| pixi | pixi.toml 或 pyproject `[tool.pixi]`（TOML 1.1 语法坑）[28] | pixi.lock：全 environment×platform 一把锁，conda+PyPI 同锁[29] | feature+environments 多环境；`[workspace.dependencies]`（preview）[30][33] | 解释器=conda 包自动装[36] | pixi build→conda 包（preview）[32] | `.pixi/envs/` 每环境一目录[53] |

| 工具 | D7 官方迁移 | D8 CI/缓存 | D9 私有源 | D10 其他标准 |
|---|---|---|---|---|
| uv | 仅 pip→project 指南：`uv add -r req.in`，`-c` 保留已锁版本[12] | setup-uv `enable-cache`(auto)；`uv cache prune --ci`[11][10] | `[[tool.uv.index]]` default/explicit/first-match；index pin 防依赖混淆[9] | PEP 735✅（dev 组默认装）、723✅、668 `break-system-packages`[49][50] |
| pip | — | setup-python `cache:'pip'` 缓存 pip 目录（二手）[42] | `--index-url`/`--extra-index-url`；netrc/keyring[43][44] | PEP 668（23.0 起）[39]；735 `--group`（25.1）[2] |
| Poetry | 无官方 req.txt 导入；1→2 手动改 pyproject + `config --migrate`[13] | pipx 装+固定版本；cache-dir ~/Library/Caches/pypoetry 等[47] | `[[tool.poetry.source]]` primary/supplemental/explicit；配 primary 关隐式 PyPI[15] | PEP 735（2.2）[48]；723 无官方支持 |
| PDM | `pdm import` 5 格式：Pipfile/Poetry/Flit 段、req.txt、setup.py[24] | setup-pdm@v4 内置 cache（key=./pdm.lock）；集中 wheel 缓存可选[26][27] | `[[tool.pdm.source]]`+`include/exclude_packages`；keyring[27] | 735（2.20）、723（2.16）、实验 `use_uv`[21] |
| pixi | `pixi init --import environment.yml`（仅 conda-env）[37] | setup-pixi 见 pixi.lock 自动缓存[34] | 私有 channel：bearer/conda-token/basic/S3；`[pypi-options]`[38] | pypi-deps 用 uv 解析库，conda 优先[31] |

## 3. 变体与适配层

- **pip-tools**：第三方，给 pip 补「.in→全 pin requirements.txt」的锁工作流[41]。
- **poetry-plugin-export**：2.0 起 export 变插件；导 requirements.txt / pylock.toml[17]。
- **Hatch/hatchling**：PyPA 项目管理器+后端，uv_build 之外的纯 Python 后端选项[55][8]。
- **pipenv** 仍维护（2026.8.0）[54]；**pyenv** 只切解释器（shim）[56]；**pipx** 隔离装 CLI[57]。
- **conda/mamba/miniforge**：原版/C++ drop-in/conda-forge 专用安装器；pixi 是 Rust 重写、非 drop-in[35][58][59]。
- **rye**：2026-02 归档停更（含安全更新），官方指 uv 继任[40]。

## 4. 需要知道的坑

1. **私有源依赖混淆**：`--extra-index-url` 会让同名包从任意源装；uv first-match+`explicit`/index pin、Poetry `explicit`、PDM `include/exclude_packages` 才是防护（uv 引 2022 torchtriton 事件）[9][15][27]。
2. **Poetry 1→2 非无缝**：shell/export 变插件、lock 默认 --no-update、`prefer-active-python` 反转为 `use-poetry-python`、弃 3.8、读不了 <1.1 的 lock[13]。
3. **平台专属 req.txt 不能直接当 uv `-c`**（markers 冲突），先 `uv pip compile --python-platform … --no-strip-markers` 重生成[12]。
4. **PEP 668**：系统 Python 上 `pip install` 报 externally-managed 是设计行为，该用 venv/pipx，勿轻易 `--break-system-packages`[39][50]。
5. **uv 缓存不感知 flat index 同文件名替换**，要 `--refresh`；CI 末尾 `uv cache prune --ci`[10]。
6. **pixi 混装时 conda 优先**且钉住 PyPI 解，冲突加 `[constraints]`[31]。

## 5. 未决与置信度

- poetry.lock 跨平台性官方未明示；uv.lock schema 版本、uv_build 首版、PDM 默认切 venv 的版本未确认。
- Poetry 无「不支持 monorepo」明文（仅 open issue）；pixi build/workspace.dependencies 仍 preview[32][33]。
- pip lock 仅当前平台 vs PEP 751 多环境设计：规范允许 universal，pip 实现未到[3][1]。
- setup-python 缓存行为为二手来源；「生态向 uv 集中」是趋势判断。

## 来源

[1] https://peps.python.org/pep-0751/
[2] https://pip.pypa.io/en/stable/news/
[3] https://pip.pypa.io/en/stable/cli/pip_lock/
[4] https://docs.astral.sh/uv/concepts/projects/layout/
[5] https://github.com/astral-sh/uv/releases/tag/0.6.15
[6] https://docs.astral.sh/uv/concepts/projects/workspaces/
[7] https://docs.astral.sh/uv/concepts/python-versions/
[8] https://docs.astral.sh/uv/concepts/build-backend/
[9] https://docs.astral.sh/uv/concepts/indexes/
[10] https://docs.astral.sh/uv/concepts/cache/
[11] https://github.com/astral-sh/setup-uv
[12] https://docs.astral.sh/uv/guides/migration/pip-to-project/
[13] https://python-poetry.org/blog/announcing-poetry-2.0.0/
[14] https://python-poetry.org/docs/pyproject/
[15] https://python-poetry.org/docs/repositories/
[16] Poetry changelog — https://raw.githubusercontent.com/python-poetry/poetry/main/CHANGELOG.md
[17] https://github.com/python-poetry/poetry-plugin-export
[18] https://python-poetry.org/docs/managing-environments/
[19] https://pdm-project.org/en/latest/usage/lockfile/
[20] https://pdm-project.org/en/latest/usage/workspace/
[21] PDM changelog — https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md
[22] https://pdm-project.org/en/latest/usage/venv/
[23] https://pdm-project.org/en/latest/usage/pep582/
[24] https://pdm-project.org/en/latest/usage/project/
[25] https://pdm-project.org/en/latest/reference/build/
[26] https://github.com/pdm-project/setup-pdm
[27] https://pdm-project.org/en/latest/usage/config/
[28] https://pixi.prefix.dev/latest/reference/pixi_manifest/
[29] https://pixi.prefix.dev/latest/workspace/lock_file/
[30] https://pixi.prefix.dev/latest/workspace/multi_environment/
[31] https://pixi.prefix.dev/latest/concepts/conda_pypi/
[32] https://pixi.prefix.dev/latest/build/getting_started/
[33] https://pixi.prefix.dev/latest/build/workspace_dependencies/
[34] https://github.com/prefix-dev/setup-pixi
[35] https://pixi.prefix.dev/latest/conda_ecosystem/
[36] https://pixi.prefix.dev/latest/python/tutorial/
[37] https://pixi.prefix.dev/latest/tutorials/import/
[38] https://pixi.prefix.dev/latest/deployment/authentication/
[39] https://peps.python.org/pep-0668/
[40] https://github.com/astral-sh/rye
[41] https://pip.pypa.io/en/stable/topics/repeatable-installs/
[42] https://pip.pypa.io/en/stable/topics/caching/
[43] https://pip.pypa.io/en/stable/cli/pip_install/
[44] https://pip.pypa.io/en/stable/topics/authentication/
[45] https://docs.python.org/3/library/venv.html
[46] https://python-poetry.org/docs/cli/
[47] https://python-poetry.org/docs/configuration/
[48] https://python-poetry.org/docs/dependency-specification/
[49] https://docs.astral.sh/uv/guides/scripts/
[50] https://docs.astral.sh/uv/reference/settings/
[51] https://docs.astral.sh/uv/concepts/projects/sync/
[53] https://pixi.prefix.dev/latest/workspace/environment/
[54] https://pypi.org/project/pipenv/
[55] https://hatch.pypa.io/latest/
[56] https://github.com/pyenv/pyenv
[57] https://pipx.pypa.io/stable/
[58] https://mamba.readthedocs.io/en/latest/
[59] https://github.com/conda-forge/miniforge
