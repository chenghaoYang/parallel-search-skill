# 怎么选 Python 包管理工具

> 给要开新项目、或从 pip / Poetry / conda 迁过来的人。第 0 节做选择，第 2–3 节查字段和命令。截至 2026-09-24，只依据官方文档。带日期的结论有没有被更晚版本改写，见第 5 节。

## 0. 一屏看懂

1. 只有 PyPI：在 uv、Poetry、PDM 里选。还要 conda 包：用 pixi。pip 把已写好的清单或锁装进已有解释器。
2. 新的纯 PyPI 项目要跨平台锁、workspace、以及工具自己下载 CPython：用 uv（`[project]`、`[dependency-groups]`、`.python-version`、一把 `uv.lock`）。
3. 标准锁 `pylock.toml` 是 PEP 751 Final（Created 24-Jul-2024）[1]。pip 25.1（2025-04-26）起实验性生成，只保证当前 Python 与平台；26.1（2026-04-26）起实验性安装 [2][3][4]。uv 自 0.6.15 可导出并安装，项目命令仍用 `uv.lock` [5][6]。命令见第 3 节。
4. Poetry 2.0.0（2025-01-05）加入 `[project]`，只含 `tools.poetry` 的配置仍可读 [7][8]。`project.dependencies` 是元数据，`tool.poetry.dependencies` 只补充锁定 [9]。权威锁仍是 `poetry.lock`；2.3.0（2026-01-18）还不能换成 pylock，导出要另装 `poetry-plugin-export` [10][11]。
5. PDM 默认跨平台 `pdm.lock`。2.24.0 起可导出 pylock；2.25.0（2025-06-13）起 `lock.format=pylock` 为 opt-in [12][13]。
6. 仓库一把锁：uv 的 `[tool.uv.workspace]` [14]；PDM 2.28.0（2026-06-23）起的 `[tool.pdm.workspace].members` [15]；pixi 的 `[workspace.dependencies]` 与 `{ workspace = true }` [16]。

## 1. Taxonomy

**包宇宙**决定锁里是 PyPI 文件还是 conda 包、私有源是 index 还是 channel、Python 是解释器还是 conda 包。**职责**决定写不写项目、有没有 workspace、CI 缓存下载目录还是环境目录。

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| PyPI 安装器 | pip | 消费清单或锁，不生成项目模板 |
| PyPI 项目管理器 | uv、Poetry、PDM | 都用 `[project]` 和自己的锁。`[tool.poetry]` 是仍可读的旧表 |
| conda 栈求解器 | pixi | conda 与 PyPI 依赖进同一把 `pixi.lock` |

conda、Hatch、pip-tools、Rye 见第 5 节。矩阵列：清单、锁、workspace、Python、构建后端、依赖组、迁移、CI、私有源。

## 2. 对照矩阵

| | 清单与 workspace | 锁 | Python、后端、依赖组 | 迁移、CI、私有源 |
|---|---|---|---|---|
| uv | `[project]`；`[tool.uv.workspace].members`；`workspace = true`；一把锁 [5][14][17] | `uv.lock`，跨平台，一个 hash [5][25] | 下载 CPython；`uv python pin` → `.python-version`，否则满足 `requires-python`。`uv_build`，可换 hatchling、flit-core、pdm-backend、setuptools、maturin、scikit-build-core。`[dependency-groups]` [17][32][34] | `uv add -r requirements.in -c requirements.txt`；其他迁移指南未提供。`UV_CACHE_DIR`；`astral-sh/setup-uv`。`[[tool.uv.index]]`；`UV_INDEX_<NAME>_USERNAME`/`_PASSWORD`；凭证不进锁 [25][44][45][46][47] |
| pip | 读项目元数据，不扫仓库里的 `requirements.txt`。已查页无 workspace [18] | 无项目锁。习惯名 `requirements.txt`。`pip lock` 只覆盖当前平台。`--hash` 打开全局校验 [4][26][27] | 不管解释器；`--python` 指向已有解释器或 venv。无 backend 时 `setuptools.build_meta:__legacy__`。`--group`（25.1）[18][35][36][37] | `pip freeze > requirements.txt`。`~/.cache/pip`，尊重 `XDG_CACHE_HOME`。`--index-url` 默认 `https://pypi.org/simple`（`PIP_INDEX_URL`）[4][18][48] |
| Poetry | `[project]` 或仅 `tools.poetry`。已打开页无 workspace；path 依赖 `develop = true`。同名字段忽略后者 [7][8][19][24] | `poetry.lock`，跨平台，含全部分组；无 hash 即报错 [10][29] | 教程：不装解释器；范围 `requires-python`。backend `poetry.core.masonry.api`。extras：`[project.optional-dependencies]` [19][28][39] | 无 import（`poetry init`）。`~/.cache/pypoetry`（`POETRY_CACHE_DIR`）。`[[tool.poetry.source]]` 的 `priority`：`primary`/`supplemental`/`explicit`。`POETRY_HTTP_BASIC_<NAME>_*` 或 `POETRY_PYPI_TOKEN_<NAME>` [29][49][50] |
| PDM | `[project]`；`pdm.toml` 放本地配置。`[tool.pdm.workspace].members`；共用根锁 [15][20][21] | `pdm.lock`（含 hashes），覆盖 `requires-python` 全部平台。`-L` / `PDM_LOCKFILE` [12] | 默认 venv；`pdm python install` 记入 `.pdm-python`（2.13.0+），2.23.0 起可读 `.python-version`。示例后端 `pdm.backend`。`[dependency-groups].dev` [13][21][40][41] | `pdm import`：Pipfile、Poetry、Flit、requirements.txt、setup.py。`pdm-project/setup-pdm@v4`；`PDM_CACHE_DIR` 默认 `~/.cache/pdm`。`[[tool.pdm.source]]`；`name="pypi"` 替换默认索引 [20][21][52][53] |
| pixi | `pixi.toml` 优先于同目录 `pyproject.toml`。`[project].dependencies` 映射为 `[pypi-dependencies]` [16][22] | `pixi.lock` 含 conda 与 PyPI，按平台分列。v7 自 0.68.0（2026-05-07）[30][31] | `requires-python` 写成 conda 的 `python`；源码包之前要有该依赖。默认 `hatchling.build`。groups 变成 feature [22] | `pixi import --format=conda-env` 或 `pypi-txt`。`PIXI_CACHE_DIR`，否则 `RATTLER_CACHE_DIR`。`prefix-dev/setup-pixi@v0.10.0`。`[pypi-options].index-url`；`RATTLER_AUTH_FILE` [16][54][56][57] |

## 3. pylock 适配层

lockers 写锁，installers 安装；PEP 要求安装时不再解析。文件名 `pylock.toml` 或 `pylock.*.toml` [1]。pip 没写读取时会跳过 resolver。

| | 写出 | 安装 | 权威锁？ |
|---|---|---|---|
| uv | `uv export -o pylock.toml`；`uv pip compile requirements.in -o pylock.toml` | `uv pip sync pylock.toml` 或 `uv pip install -r` | 否，仍是 `uv.lock` [5][6] |
| pip | `pip lock`，`-o` 默认 `pylock.toml` | `-r pylock.toml`，experimental | 只覆盖当前平台 [2][3][4] |
| Poetry | 插件 `poetry export --format pylock.toml`（≥1.10.0） | 已查页无导入 | 否 [10][11] |
| PDM | `pdm export -f pylock -o pylock.toml`，或 `lock.format=pylock` | 无 import；opt-in 后文件即 pylock | 默认否 [12][13] |
| pixi | 锁页、清单、CHANGELOG 无 pylock | 同左 | `pixi.lock` [30][31] |

## 4. 选型时会踩的坑

1. `pip lock` 只覆盖当前 Python 与平台 [4]。多平台用 `uv.lock`、`poetry.lock`、`pdm.lock`，或按平台分列的 `pixi.lock`。
2. `--extra-index-url` 被标为不安全 [38]。Poetry 源不写 `priority` 时变成 `primary`，并禁用隐式 PyPI [29]。
3. Poetry 2 默认不含 `poetry export` [11]。项目内 `.venv` 要设 `virtualenvs.in-project` [50]。
4. 只含 `[tool.poetry]` 的项目在 `>=2.0.0` 仍可读 [8]。只给锁定器用的依赖留在 `tool.poetry.dependencies` [9]。
5. pixi 把 `[project].dependencies` 装成 PyPI 依赖，排在 conda 之后；源码包要求 conda 里已有 `python`。从 Poetry 迁入要手抄 [22][55]。
6. uv 的凭证不进 `uv.lock` [25]。Poetry 写入 keyring 失败时落盘 `auth.toml` [29]。pip 的示例把 `username:password` 放进 index URL；requirements 可用 `${API_TOKEN}` [26][58]。

## 5. 未决与置信度

- “For now, it looks like this:” 不能证明 `poetry new` 只有 `[project]` [28]。2.3.0 之后能否用 pylock 替换 `poetry.lock`、有无 workspace：未查。
- 教程写不安装解释器 [28]，2.1.0 起却有 `poetry python install` [49]。python 两表都写时，锁定用 `tool.poetry.dependencies`，且须落入 `requires-python` [23]。
- `[dependency-groups]` 与「其他组必须在 `tool.poetry`」冲突 [9][39]。`poetry-core` 下界兼有 `>=1.0.0` 与 `>=2.0.0,<3.0.0` [23][28]。
- 安装 pylock 时 PEP 要求不再解析 [1]，pip 只写 experimental。`PIP_CACHE_DIR`、省略 `-r`、`uv sync` 读不读 pylock：无原句。`uv init` 的 `[build-system]` 两页不一致；有 `uv build` / `uv publish` [17][33]。
- PDM 锁页先写只支持 requirements.txt，后文有 pylock [12]。Python 3.9+ 与 2.27.0 的 3.10 冲突 [13][21]。`use_venv=false` 时用 `__pypackages__` [40]。
- pixi 缓存默认是 `XDG_CACHE_HOME/pixi` 还是 `~/.cache/rattler`，两页不一致 [43][57]。锁示例 version 6，changelog 为 v7。conda、Hatch、pip-tools、Rye 只有 scout 线索。

## 来源

[1] https://peps.python.org/pep-0751/
[2] https://raw.githubusercontent.com/pypa/pip/25.1/NEWS.rst
[3] https://raw.githubusercontent.com/pypa/pip/26.1/NEWS.rst
[4] https://pip.pypa.io/en/stable/cli/pip_lock/
[5] https://docs.astral.sh/uv/concepts/projects/layout/
[6] https://github.com/astral-sh/uv/releases/tag/0.6.15
[7] https://python-poetry.org/blog/announcing-poetry-2.0.0/
[8] https://python-poetry.org/docs/faq/
[9] https://python-poetry.org/docs/dependency-specification/
[10] https://python-poetry.org/blog/announcing-poetry-2.3.0/
[11] https://github.com/python-poetry/poetry-plugin-export
[12] https://pdm-project.org/latest/usage/lockfile/
[13] https://github.com/pdm-project/pdm/blob/main/CHANGELOG.md
[14] https://docs.astral.sh/uv/concepts/projects/workspaces/
[15] https://pdm-project.org/latest/usage/workspace/
[16] https://pixi.prefix.dev/latest/reference/pixi_manifest/
[17] https://docs.astral.sh/uv/concepts/projects/init/
[18] https://pip.pypa.io/en/stable/_sources/user_guide.rst.txt
[19] https://python-poetry.org/docs/libraries/
[20] https://pdm-project.org/latest/usage/config/
[21] https://pdm-project.org/latest/usage/project/
[22] https://pixi.prefix.dev/latest/python/pyproject_toml/
[23] https://python-poetry.org/docs/pyproject/
[24] https://raw.githubusercontent.com/python-poetry/poetry-core/main/src/poetry/core/factory.py
[25] https://docs.astral.sh/uv/concepts/indexes/
[26] https://pip.pypa.io/en/stable/_sources/reference/requirements-file-format.md.txt
[27] https://pip.pypa.io/en/stable/_sources/topics/secure-installs.md.txt
[28] https://python-poetry.org/docs/basic-usage/
[29] https://python-poetry.org/docs/repositories/
[30] https://pixi.prefix.dev/latest/workspace/lock_file/
[31] https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md
[32] https://docs.astral.sh/uv/concepts/python-versions/
[33] https://docs.astral.sh/uv/guides/package/
[34] https://docs.astral.sh/uv/concepts/projects/dependencies/
[35] https://pip.pypa.io/en/stable/_sources/topics/workflow.md.txt
[36] https://pip.pypa.io/en/stable/_sources/topics/python-option.md.txt
[37] https://pip.pypa.io/en/stable/reference/build-system/
[38] https://pip.pypa.io/en/stable/_sources/cli/pip_install.rst.txt
[39] https://python-poetry.org/docs/managing-dependencies/
[40] https://pdm-project.org/latest/usage/venv/
[41] https://pdm-project.org/latest/reference/build/
[43] https://pixi.prefix.dev/latest/workspace/environment/
[44] https://docs.astral.sh/uv/guides/migration/pip-to-project/
[45] https://docs.astral.sh/uv/guides/migration/
[46] https://docs.astral.sh/uv/concepts/cache/
[47] https://docs.astral.sh/uv/guides/integration/github/
[48] https://pip.pypa.io/en/stable/topics/caching/
[49] https://python-poetry.org/docs/cli/
[50] https://python-poetry.org/docs/configuration/
[52] https://pdm-project.org/latest/usage/advanced/
[53] https://pdm-project.org/latest/reference/configuration/
[54] https://pixi.prefix.dev/latest/tutorials/import/
[55] https://raw.githubusercontent.com/prefix-dev/pixi/main/docs/switching_from/poetry.md
[56] https://pixi.prefix.dev/latest/integration/ci/github_actions/
[57] https://pixi.prefix.dev/latest/reference/environment_variables/
[58] https://pip.pypa.io/en/stable/topics/authentication/
