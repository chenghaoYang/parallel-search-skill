# Python 项目该用哪套包管理

> 新项目如何在 uv、pip、Poetry、PDM、pixi 里选。材料日期 2026-09-24。两问的边界在第 0 节，未定稿在第 5 节。

## 0. 一屏看懂

1. 先分家族，再比命令。pip 不管解释器，也不管整个 project [18]。uv、Poetry、PDM 管 pyproject 和自己的锁。pixi 同时基于 conda 与 PyPI，并写明不是 drop-in [53][59]。
2. 日常锁是 `uv.lock`、`poetry.lock`、`pdm.lock`、`pixi.lock`，彼此不能当同一个文件用 [1][30][40][51]。`pylock.toml` 是交换格式。谁能读、谁能写见第 3 节。这里不写「已经支持」。
3. Poetry 2.0 尊重 `[project]`，但 `tool.poetry.dependencies` 不弃用，FAQ 仍允许只有 `tools.poetry`（页面原文拼写）[24][25]。不是「只能写标准表」。
4. 纯 PyPI、要锁和 `.venv`：uv 或 PDM。仓库已是 Poetry 就留 `poetry.lock`。要 conda 里的本机库用 pixi，不要用 pip 去补。
5. 多包只看到 uv 的 `[tool.uv.workspace].members` 和 PDM 的 `[tool.pdm.workspace].members` [3][41]。Poetry 没有这一页。没有一条通用迁移命令，入口在 D10。

## 1. Taxonomy

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| PyPI 安装器 | pip | 只往当前解释器装包，不拥有项目文件 |
| PyPI 项目管理器 | uv、Poetry、PDM | 以 pyproject 为项目，自写锁、自管环境。分界是锁的名字，以及 PEP 621 是否唯一写法 |
| conda/prefix 工作区 | pixi | 求解的是 channel；PyPI 是第二套依赖；Python 是 channel 里的包 |

D1 元数据。D2 锁范围。D3 成员。D4 Python。D5 构建。D6 环境。D7 依赖组。D8 私有源。D9 缓存。D10 迁入。

## 2. 对照矩阵

- **D1** uv/PDM：`[project]`（`uv add`→`project.dependencies`；库 `[tool.pdm] distribution=true`）[1][7][38][39]。Poetry：`[project]` 或 `[tool.poetry]`，有 project 段则 `project.name` 必填 [24][29]。pip 只读 `pyproject.toml`/`setup.py`，不搜目录 [19]。pixi：`pixi.toml` 或 `tool.pixi` [48][49]。
- **D3** uv `[tool.uv.workspace].members` + `workspace = true`，一个锁 [3]。PDM `[tool.pdm.workspace].members` [41]。pip 不管 project [18]。Poetry ∅。pixi 的 `platforms` 都进锁；多包 members ❓ [49]。
- **D4** `uv python pin`/`install`，`project.requires-python` [4][6]。`pdm use`→`.pdm-python`，`pdm python install`，认 `.python-version` [39]。Poetry `env use` 与 `poetry python install` [37][27]。pip `--python` 只换已有解释器 [20]。pixi：conda `[dependencies]` 的 python [49][52]。
- **D5** uv：v0.12 前应用默认无；`--build-backend` 为 `hatchling`、`uv_build`、`flit-core`、`pdm-backend`、`setuptools`、`maturin`、`scikit-build-core` [5]。Poetry `poetry.core.masonry.api` [35]。PDM `pdm.backend`；同页称 poetry-core 不读 PEP 621 [42]。pip 不构建，无 sdist 命令 [21][18]。pixi `pixi-build-python`；Poetry 迁移页仍写不能构建发布 [54][58]。
- **D6** uv `.venv` / `UV_PROJECT_ENVIRONMENT` [6]。Poetry `{cache-dir}/virtualenvs`（`POETRY_VIRTUALENVS_PATH`），已有 `.venv` 会用 [31]。PDM `.venv`（`venv.in_project` 默认真），PEP 582 已拒 [43][44]。pip 装进绑定的 Python [60]。pixi `.pixi/envs` [52]。
- **D7** uv `[dependency-groups]`，`--dev`→`dev` 且默认同步 [7][8]。Poetry 隐式 `main`：`[dependency-groups]` 或 `[tool.poetry.group.<name>.dependencies]` [32]。PDM `[dependency-groups]`（`-d`→`dev`），extras=`[project.optional-dependencies]` [45]。pip 读 Dependency Groups，`pip lock --group` [19]。pixi 收成同名 feature 的 `pypi-dependencies`；默认含 default feature，除非 `no-default-feature = true` [50][49]。
- **D8** uv `[[tool.uv.index]]`、`UV_INDEX`、`UV_INDEX_<NAME>_USERNAME`/`_PASSWORD` [9]。pip `PIP_INDEX_URL` 默认 `https://pypi.org/simple`；`--extra-index-url` 不安全 [17]。Poetry `[[tool.poetry.source]]`，`priority`=`primary`|`supplemental`|`explicit`（primary 关隐式 PyPI），`POETRY_HTTP_BASIC_<NAME>_USERNAME`/`_PASSWORD`，`source` 不能进 `[project]` [34]。PDM `[[tool.pdm.source]]`，`type`=`index`|`find_links`，`name=pypi` 换默认，keyring `pdm-pypi-<name>` [46]。pixi：带主机名的 channel URL，`channel-priority` 默认 `strict`；单包 `index` [49]。
- **D9** `UV_CACHE_DIR`（否则 `$XDG_CACHE_HOME/uv` 或 `~/.cache/uv`）[10c]。`PIP_CACHE_DIR`（`~/.cache/pip`，macOS `~/Library/Caches/pip`）[22]。`POETRY_CACHE_DIR`（macOS `~/Library/Caches/pypoetry`，Unix `~/.cache/pypoetry`）[31]。`PDM_CACHE_DIR` 默认 `~/.cache/pdm` [43]。`PIXI_CACHE_DIR` 否则 `RATTLER_CACHE_DIR` [55]。
- **D10** uv：`uv add -r requirements.in -c requirements.txt`，其他指南还没有 [10][11]。pip 无 migrate [15]。Poetry 手改 `[project]`；`poetry config --migrate` 只迁配置改名 [25]。`pdm import`：Pipfile、Poetry、Flit、requirements.txt、setup.py [39]。`pixi init --import`；`pixi import` 仅 `conda-env` 与 `pypi-txt` [57][56]。
- **D2 范围** `uv.lock` universal、跨平台，且其他工具不能用 [1][2]。`pip lock` 只保证当前 Python 与平台 [15]。pixi 对每个 platform 求解 [49]。Poetry/PDM 是否跨平台：无原句。

## 3. 变体与适配层

PEP 751 页面状态 Final，同页自称历史文档。文件名 `pylock.toml` 或 `pylock.<name>.toml` [14]。

| | 项目锁 | 写出 pylock | 读 pylock |
|---|---|---|---|
| uv | 继续 `uv.lock`（有些功能写不进 pylock）[1] | `uv export -o pylock.toml`；`uv pip compile requirements.in -o pylock.toml` [1]。0.6.15 称 preliminary [12] | 仅 `uv pip sync pylock.toml` 或 `uv pip install -r pylock.toml`。同页把跨工具安装写成 future [1] |
| pip | 实验性 `pip lock` 默认即 `pylock.toml` [15][16] | changelog：实验性 `pip lock`，实现 PEP 751。版本标题不在 quote 里 [16] | `pip install -r` 接受它，页面写 experimental [17] |
| Poetry | `poetry.lock`；2.0+ 至少 lock version 2.1 [30][31]。2.3.0 还不能拿 pylock 替换 [26] | 要 Poetry ≥2.3.0 和 poetry-plugin-export ≥1.10.0。插件从 2.0 起默认不装 [26][27] | 无原句 |
| PDM | 默认 `pdm.lock`。`pdm config lock.format pylock` 改用 `pylock.toml` [40] | `pdm export -f pylock -o pylock.toml`。同页先写只支持 `requirements.txt` [40] | 格式改为 pylock 后，读写的就是该文件 [40] |
| pixi | `pixi.lock` [51] | ∅ | ∅ |

## 4. 用户需要知道的坑

1. `--extra-index-url` 装私有包：pip 写明不安全 [17]。Poetry 有 `priority = primary` 就关掉隐式 PyPI [34]。uv 把密码放在 `UV_INDEX_<NAME>_PASSWORD`，不写进项目文件 [9]。
2. pixi 加 PyPI 依赖前，conda 依赖里要先有 python [52]。不要手改 `uv.lock` [1]。CI 用 `--frozen` 或 `PIXI_FROZEN=true` [51]。
3. PDM 在没有家目录的 CI 里建缓存会权限失败，设一个可写的 `HOME`。不要提交 `.pdm-python`，建议提交 `pdm.lock` [47]。

## 5. 未决与置信度

- **pylock：** 不能写成稳定支持。uv 同页既写 future，又写 `uv pip sync` [1]。pip 解析页仍让用户用 pip-tools 做锁 [23]，与实验性 `pip lock` 并存 [16]。PEP 要求安装时不必解析 [14]；pip 没写是否跳过。25.1 / 26.1 不在 quote 里。
- **Poetry 2：** 可以写 `[project]`，不是只能。`tool.poetry.dependencies` 不弃用 [24]。FAQ 拼成 `tools.poetry` [25]。依赖组两页不一致 [36][32]。`poetry python install` 有原句 [27]；「不安装解释器」没进 quote。
- PDM 导出页前后矛盾 [40]。2.24 / 2.25 /「Experimental、2.28.0」没进 quote。它称 poetry-core 不读 PEP 621 [42]，和 Poetry 2.0 可能不是同一年代 [24]。
- pixi 缓存默认目录两页不一致（变量页是 `RATTLER_CACHE_DIR`）[55]。多包 members ❓。Poetry/PDM 锁是否跨平台 ❓。
- conda 整行仍空。hatch、pip-tools、rye 只在 scout。导出页注 November 20, 2025；layout 冲突记录注 July 21, 2026。

## 来源

[1] https://docs.astral.sh/uv/concepts/projects/layout/
[2] https://docs.astral.sh/uv/concepts/resolution/
[3] https://docs.astral.sh/uv/concepts/projects/workspaces/
[4] https://docs.astral.sh/uv/concepts/python-versions/
[5] https://docs.astral.sh/uv/concepts/projects/init/
[6] https://docs.astral.sh/uv/concepts/projects/config/
[7] https://docs.astral.sh/uv/concepts/projects/dependencies/
[8] https://docs.astral.sh/uv/concepts/projects/sync/
[9] https://docs.astral.sh/uv/concepts/indexes/
[10] https://docs.astral.sh/uv/guides/migration/
[10c] https://docs.astral.sh/uv/concepts/cache/
[11] https://docs.astral.sh/uv/guides/migration/pip-to-project/
[12] https://github.com/astral-sh/uv/releases/tag/0.6.15
[14] https://peps.python.org/pep-0751/
[15] https://pip.pypa.io/en/stable/cli/pip_lock/
[16] https://pip.pypa.io/en/stable/news/
[17] https://pip.pypa.io/en/stable/cli/pip_install/
[18] https://pip.pypa.io/en/stable/topics/workflow/
[19] https://pip.pypa.io/en/stable/user_guide/
[20] https://pip.pypa.io/en/stable/topics/python-option/
[21] https://pip.pypa.io/en/stable/reference/build-system/
[22] https://pip.pypa.io/en/stable/topics/caching/
[23] https://pip.pypa.io/en/stable/topics/dependency-resolution/
[24] https://python-poetry.org/blog/announcing-poetry-2.0.0/
[25] https://python-poetry.org/docs/faq/
[26] https://python-poetry.org/blog/announcing-poetry-2.3.0/
[27] https://python-poetry.org/docs/cli/
[29] https://python-poetry.org/docs/pyproject/
[30] https://python-poetry.org/docs/basic-usage/
[31] https://python-poetry.org/docs/configuration/
[32] https://python-poetry.org/docs/managing-dependencies/
[34] https://python-poetry.org/docs/repositories/
[35] https://python-poetry.org/docs/libraries/
[36] https://python-poetry.org/docs/dependency-specification/
[37] https://python-poetry.org/docs/managing-environments/
[38] https://pdm-project.org/en/latest/reference/pep621/
[39] https://pdm-project.org/en/latest/usage/project/
[40] https://pdm-project.org/en/latest/usage/lockfile/
[41] https://pdm-project.org/en/latest/usage/workspace/
[42] https://pdm-project.org/en/latest/reference/build/
[43] https://pdm-project.org/en/latest/reference/configuration/
[44] https://pdm-project.org/en/latest/usage/pep582/
[45] https://pdm-project.org/en/latest/usage/dependency/
[46] https://pdm-project.org/en/latest/usage/config/
[47] https://pdm-project.org/en/latest/usage/advanced/
[48] https://pixi.prefix.dev/latest/first_workspace/
[49] https://pixi.prefix.dev/latest/reference/pixi_manifest/
[50] https://pixi.prefix.dev/latest/python/pyproject_toml/
[51] https://pixi.prefix.dev/latest/workspace/lock_file/
[52] https://pixi.prefix.dev/latest/workspace/environment/
[53] https://pixi.prefix.dev/latest/conda_ecosystem/
[54] https://pixi.prefix.dev/latest/build/python/
[55] https://pixi.prefix.dev/latest/reference/environment_variables/
[56] https://pixi.prefix.dev/latest/tutorials/import/
[57] https://pixi.prefix.dev/latest/reference/cli/pixi/init/
[58] https://pixi.prefix.dev/latest/switching_from/poetry/
[59] https://pixi.prefix.dev/latest/concepts/conda_pypi/
[60] https://pip.pypa.io/en/stable/topics/local-project-installs/
