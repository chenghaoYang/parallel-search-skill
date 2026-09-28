# Python 包管理怎么选

> 新项目在 uv、pip、Poetry、PDM、pixi/conda 之间怎么选。截至 2026-09-24。先看第 0 节，字段以第 2 节为准。

## 0. 一屏看懂

1. 先选层：pip 只往已有环境装包；uv、Poetry、PDM 拥有清单、锁和虚拟环境；pixi 拥有前缀环境，Python 是其中的包。
2. 标准锁的文件名是 `pylock.toml` 或 `pylock.<name>.toml`（PEP 751 为 Final，正典在 PyPA 规范）[1][2]。默认锁不能互换：`uv.lock`（专有且跨平台）[10]、`poetry.lock` [23]、`pdm.lock` [34]、`pixi.lock` [43]。
3. 多包一把锁：uv 的 `members`，全仓一个 `uv.lock` [13]。Poetry 没有这套键 [25]。
4. 解释器：pip 不管 [6]。uv 用 `python install` / `pin`（`.python-version`）[14]。PDM 用 `pdm use` 与 `pdm python install` [36]。pixi 把 `requires-python` 收成依赖 [46]。
5. 纯 Python、要跨平台锁 → uv [17]。要 conda 包 → pixi（无 base 环境）[52]。只装进现成环境 → pip。
6. pip/uv 的 pylock、Poetry 2 的 `[project]`：做到哪一步见第 2 节；小版本号见第 5 节，这里不写死。

## 1. Taxonomy

轴 1（拥有哪一层）：安装器 pip；项目经理 uv、Poetry、PDM；环境经理 pixi（conda 未收束）。用来解释谁管解释器、谁有项目锁。

轴 2（靠不靠 PEP 621 / PEP 751）：同族的锁也不能互换，所以不并成一家。

维度：lock 锁与 pylock；meta 依赖表；workspace 多包是否一把锁；pyver 谁装解释器；backend 默认构建后端；index 私有源；cicache 缓存路径；migrate 迁入。

## 2. 对照矩阵

### lock 与 meta

| | 锁 / pylock | 依赖写在哪 |
|---|---|---|
| pip | 无自有锁。实验性 `pip lock` 实现 PEP 751，`-o` 默认 `pylock.toml`；只保证当前 Python 与平台 [3][4]。`pip install -r` 接受 requirements.txt 或 pylock.toml [5] | 不管「项目」。`--group` 安装 pyproject 的 dependency-group [5][6] |
| uv | 项目锁只认 `uv.lock`。`uv export --format pylock.toml`；`uv pip` 可用 pylock。0.6 changelog 称 preliminary [10][11][12]。`--locked` 过期即失败，`--frozen` 不检查 [19][21] | `project.dependencies`、`optional-dependencies`、`dependency-groups`（PEP 735）、`tool.uv.sources` [17] |
| Poetry | `poetry.lock`。`poetry lock` 默认 `--no-update`，重写 `--regenerate` [23][24]。`pylock.toml` 只导出，经 poetry-plugin-export [32][33]。install 能否直接读：未写 | 2.0 尊重 `[project]`；`tool.poetry.dependencies` 不弃用；组仍在 `tool.poetry`。两表都写时，构建用 project，锁定用 tool.poetry 补充 [24][25] |
| PDM | 默认格式 `pdm`、文件 `pdm.lock`；另一格式 `pylock`、文件 `pylock.toml`。`-L` 或 `PDM_LOCKFILE` 换文件。文档写可导出 pylock.toml [34] | `[project]`（PEP 621/631/639）[35]。开发依赖 `[dependency-groups]`，不进发行元数据 [37] |
| pixi | `pixi.lock`；PyPI 的 uv 解析写进该锁 [43][44]。pylock 未见实现，#3474 在讨论导出 [53] | `pixi.toml` 或 `pyproject.toml`。conda：`[tool.pixi.dependencies]`；PyPI：`[tool.pixi.pypi-dependencies]` 或 `[project.dependencies]`。同名包 conda 优先 [45][46][47] |
| conda | ⚔ 第 5 节 | ❓ |

### workspace、pyver、backend

| | 多包 | Python | 构建 |
|---|---|---|---|
| pip | 不在范围内 [6] | 不装解释器 [6] | 默认构建隔离；`--no-build-isolation`。无 build-system 但有 setup.py 时回退 `setuptools.build_meta:__legacy__` [7] |
| uv | `[tool.uv.workspace].members` 必填，`exclude` 可选；依赖写 `workspace = true`。`uv lock` 锁整仓；`uv sync` 默认根，`--package` 选成员 [13] | `uv python install`；`uv python pin` → `.python-version`；守 `requires-python` [14] | 自带 `uv_build`（仅纯 Python）。`uv init` 默认用它；`--build-backend` 可换 [15][16] |
| Poetry | ∅。本地开发用 path 依赖 [25] | `poetry env use` 选已有解释器 [26]。与 `poetry python install` 冲突，见第 5 节 | `poetry.core.masonry.api`；新项目 `poetry-core>=2.0.0,<3.0.0`。不要再把 `poetry` 本身写成 backend [23][28] |
| PDM | 成员写在根 pyproject；键名摘录未给出 ❓ [38] | `pdm use` → `.pdm-python`；`pdm python install`（python-build-standalone）[36] | 不强制。默认 `pdm-backend`（Python 3.7+）[39][36] |
| pixi | `[workspace]` 是清单根，不是成员表 ❓ [44] | `requires-python` 写入 dependencies [46] | sdist 在 conda 环境构建 [44]。与迁移页冲突，见第 5 节 |

`name` 已弃用，改 `project.name`。上界可只写在 `tool.poetry.dependencies` 的 `python` [28]。

### index、cicache、migrate

| | 私有源 | CI | 迁入 |
|---|---|---|---|
| pip | `--index-url` 默认 `https://pypi.org/simple`；`--extra-index-url`；`PIP_<UPPER_LONG_NAME>`；`--keyring-provider`=`auto`/`disabled`/`import`/`subprocess` [3][9] | `pip cache dir`。上层已有缓存才用 `--no-cache-dir` [8] | `pip lock -r` 可读 requirements.txt [3] |
| uv | `[[tool.uv.index]]`（`name`、`url`）；`explicit = true` 须 pin；`UV_INDEX_<NAME>_USERNAME`/`PASSWORD`；凭证不进 `uv.lock` [18] | `UV_CACHE_DIR` 或 `--cache-dir` / `tool.uv.cache-dir`。`uv sync --locked --all-extras --dev`；`uv cache prune --ci` [20][19] | pip/pip-tools 有指南。Poetry/PDM 指南未写（#5200）[22] |
| Poetry | `[[tool.poetry.source]]`，`priority` 摘录见 `primary`、`explicit`；`http-basic.<name>`。发布是另一套 `repositories.<name>` [29][30] | `POETRY_CACHE_DIR`。无 Actions 示例。Docker：`--only main --no-root --no-directory` [30][31] | 可只留 tool.poetry 或改用 `[project]`。`poetry check` 报弃用字段 [31][28] |
| PDM | `url`、`verify_ssl`、`username`、`password`、`type`=`index`/`find_links`；`include_packages` / `exclude_packages` [40] | 默认 `~/.cache/pdm`，`PDM_CACHE_DIR`。setup-pdm 用 `pdm.lock` 做缓存键 [41][42] | `pdm import`：Pipfile、Poetry、Flit、requirements.txt、setup.py [36] |
| pixi | channel 用带主机名的 URL；`pixi auth login`。PyPI 表 `[pypi-options]`，子键 ❓ [48][44] | `PIXI_CACHE_DIR`。setup-pixi 按 `pixi.lock` 哈希缓存 [49][50] | `pixi import`：`conda-env`、`pypi-txt`（`init --import` 仅前者）[51] |

## 3. 变体与适配层

Hatch 能生成 `pylock.toml` [54]。`pip-compile` 仍按环境产出 `requirements.txt` [55]。Pipenv 写 pylock 要 `use_pylock = true` [56]。Rye 已归档，改用 uv [57]。conda-lock 默认把 basic auth 留在锁里 [58]。

## 4. 用户需要知道的坑

1. pip 不管项目、不装 Python [6]。conda 环境不 activate 就直接跑可执行文件，一般不行 [59]。
2. `uv.lock` 不能交给别的工具 [10]。pip 生成的 pylock 只覆盖当前平台 [3]。
3. Poetry 2 仍要留 `tool.poetry.dependencies`，依赖组不能放进 `[project]` [24][25]。
4. uv 凭证不进锁，CI 要另配 [18]。conda-lock 相反，会把 basic auth 写进锁 [58]。
5. uv 缓存 `UV_CACHE_DIR`，用 `uv sync --locked` [19][20]。Poetry 只有 `POETRY_CACHE_DIR`，没有官方 Actions 示例 [30]。pixi 同名包走 conda [46]。

## 5. 未决与置信度

版本号不在摘录，不进第 0 节：pip 25.1/26.1 [4]；uv 0.6.15 [12]；PDM 的 `lock.format`、2.25.0、能否 import pylock [34]；Poetry 弃用键全表、`supplemental`、install 是否读 pylock [24]。

⚔ conda 写 26.5 起可读 `conda-lock.yaml` 与 `pixi.lock` [59]，pixi 对比表仍称无锁（缺原句），其余格 ❓。Poetry 一页说不装解释器，CLI 有 `poetry python install` [23][27]。pixi 迁移页写尚未实现构建与发布 [47]；对立页待复核。PDM 自身的 Python 写成 3.10+、3.9+、≥3.8、<3.7 [60][42]。

仍空：PDM/pixi 成员键、pixi 的 `channels` 与 `index-url`、uv 的 index 枚举、Poetry 2.2 dependency-groups、`PIP_CACHE_DIR`。

## 来源

[1] https://peps.python.org/pep-0751/
[2] https://packaging.python.org/en/latest/specifications/pylock-toml/
[3] https://pip.pypa.io/en/stable/cli/pip_lock/
[4] https://pip.pypa.io/en/stable/news/
[5] https://pip.pypa.io/en/stable/cli/pip_install/
[6] https://pip.pypa.io/en/stable/topics/workflow/
[7] https://pip.pypa.io/en/stable/reference/build-system/
[8] https://pip.pypa.io/en/stable/topics/caching/
[9] https://pip.pypa.io/en/stable/topics/authentication/
[10] https://docs.astral.sh/uv/concepts/projects/layout/
[11] https://docs.astral.sh/uv/concepts/projects/export/
[12] https://github.com/astral-sh/uv/blob/main/changelogs/0.6.x.md
[13] https://docs.astral.sh/uv/concepts/projects/workspaces/
[14] https://docs.astral.sh/uv/concepts/python-versions/
[15] https://docs.astral.sh/uv/concepts/build-backend/
[16] https://docs.astral.sh/uv/concepts/projects/config/
[17] https://docs.astral.sh/uv/concepts/projects/dependencies/
[18] https://docs.astral.sh/uv/concepts/indexes/
[19] https://docs.astral.sh/uv/guides/integration/github/
[20] https://docs.astral.sh/uv/concepts/cache/
[21] https://docs.astral.sh/uv/concepts/projects/sync/
[22] https://docs.astral.sh/uv/guides/migration/pip-to-project/
[23] https://python-poetry.org/docs/basic-usage/
[24] https://python-poetry.org/blog/announcing-poetry-2.0.0/
[25] https://python-poetry.org/docs/dependency-specification/
[26] https://python-poetry.org/docs/managing-environments/
[27] https://python-poetry.org/docs/cli/
[28] https://python-poetry.org/docs/pyproject/
[29] https://python-poetry.org/docs/repositories/
[30] https://python-poetry.org/docs/configuration/
[31] https://python-poetry.org/docs/faq/
[32] https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md
[33] https://github.com/python-poetry/poetry-plugin-export
[34] https://pdm-project.org/latest/usage/lockfile/
[35] https://pdm-project.org/latest/reference/pep621/
[36] https://pdm-project.org/latest/usage/project/
[37] https://pdm-project.org/latest/usage/dependency/
[38] https://pdm-project.org/en/latest/usage/workspace/
[39] https://pdm-project.org/latest/reference/build/
[40] https://pdm-project.org/latest/usage/config/
[41] https://pdm-project.org/latest/reference/configuration/
[42] https://github.com/pdm-project/setup-pdm
[43] https://pixi.prefix.dev/latest/workspace/lock_file/
[44] https://pixi.prefix.dev/latest/reference/pixi_manifest/
[45] https://pixi.prefix.dev/latest/python/tutorial/
[46] https://pixi.prefix.dev/latest/python/pyproject_toml/
[47] https://pixi.prefix.dev/latest/switching_from/poetry/
[48] https://pixi.prefix.dev/latest/deployment/authentication/
[49] https://pixi.prefix.dev/latest/reference/environment_variables/
[50] https://pixi.prefix.dev/latest/integration/ci/github_actions/
[51] https://pixi.prefix.dev/latest/tutorials/import/
[52] https://pixi.prefix.dev/latest/switching_from/conda/
[53] https://github.com/prefix-dev/pixi/issues/3474
[54] https://hatch.pypa.io/latest/environment/
[55] https://github.com/jazzband/pip-tools
[56] https://pipenv.pypa.io/en/latest/changelog.html
[57] https://github.com/astral-sh/rye
[58] https://github.com/conda/conda-lock
[59] https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html
[60] https://pdm-project.org/latest/
