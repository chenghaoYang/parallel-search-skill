# Python 包管理怎么选

> 新项目在 uv、pip、Poetry、PDM、pixi/conda 之间怎么选。截至 2026-09-24。先看第 0 节，字段以第 2 节为准。

## 0. 一屏看懂

1. 先选层：pip 只装包；uv、Poetry、PDM 管清单、锁和虚拟环境；pixi 与 conda 管整个前缀，Python 只是其中一个包。
2. 标准文件名是 `pylock.toml`（或 `pylock.<name>.toml`，PEP 751 Final）[1][2]。日常锁仍各用各的：`uv.lock`、`poetry.lock`、`pdm.lock`、`pixi.lock` [10][23][34][43]。
3. pip 能写也能装 pylock，但命令页仍是 EXPERIMENTAL，且只保证当前 Python 与平台 [3]。uv 的项目锁仍是专有的 `uv.lock`（别的工具不能用）；pylock 只用于导出和 `uv pip` [10]。
4. Poetry 2.0 使用 `[project]`（PEP 621）。`tool.poetry.dependencies` 不弃用；依赖组不能放进 `[project]` [24][25]。哪些键已 Deprecated，见第 2 节。
5. 多包一把锁：uv 的 `members` [13]；PDM 2.28.0 起实验性 `[tool.pdm.workspace].members` [38]；Poetry 没有 [25]。pixi 的 `[workspace]` 必填的是 `channels` 和 `platforms` [44]。
6. 纯 Python 要跨平台锁 → uv [17]。要 conda 包 → pixi，或 conda 26.5+ [59][52]。只装进现成环境 → pip [3]。

## 1. Taxonomy

轴 1（拥有哪一层）：安装器 pip；项目经理 uv、Poetry、PDM；环境经理 pixi、conda。

轴 2（靠不靠 PEP 621 / PEP 751）：同族锁也不互换。pip 的实验锁就是 pylock；uv、Poetry 只导出 pylock；PDM 可把锁切到 pylock；conda/pixi 用另一套。

维度：lock、meta、workspace（多包是否一把锁）、pyver、backend、index、cicache、migrate。

## 2. 对照矩阵

### lock 与 meta

| | 锁 / pylock | 依赖写在哪 |
|---|---|---|
| pip | `pip lock` 仍 EXPERIMENTAL，默认 `pylock.toml`，仅当前 Python/平台；`-r` 也标 experimental [3] | `--group` 装 dependency-group；不管项目 [5][6] |
| uv | 只认 `uv.lock`。`uv export --format pylock.toml`；`uv pip` 可读。pylock 表达不了全部能力 [10][11]。`--locked` 失败，`--frozen` 不检查 [19][21] | `project.dependencies`、`optional-dependencies`、`dependency-groups`、`tool.uv.sources` [17] |
| Poetry | `poetry.lock`。`poetry lock` 默认 `--no-update`，`--regenerate` 重写 [24]。2.3.0（2026-01-18）起插件导出 pylock；install 只提 poetry.lock [32][27] | 主依赖可进 `[project]`；`^`/`~` 不支持 [25] |
| PDM | 默认 `pdm.lock`。`pdm config lock.format pylock`（2.25.0，experimental，将来默认）[34] | `[project]`；开发组 `[dependency-groups]` [35][37] |
| pixi | `pixi.lock`（含 uv 解出的 PyPI）[43][44]。无 pylock [53] | `[tool.pixi.dependencies]`；PyPI 用 `[tool.pixi.pypi-dependencies]` 或 `[project.dependencies]`。同名 conda 优先 [46][47] |
| conda | 26.5+：`conda export --file conda-lock.yaml`，`conda create --file` 装回。可读 `conda-lock.yaml` 与 `pixi.lock`。无 `conda lock` [59] | `environment.yml`（channels、dependencies、`pip:`）[59] |

### workspace、pyver、backend

| | 多包 | Python | 构建 |
|---|---|---|---|
| pip | 不在范围内 [6] | 不装解释器 [6] | 默认隔离；`--no-build-isolation`。无 build-system 时回退 `setuptools.build_meta:__legacy__` [7] |
| uv | `members` 必填；依赖 `workspace = true`。`uv lock` 锁整仓 [13] | `uv python install`；`uv python pin` → `.python-version` [14] | `uv_build`（仅纯 Python）；`uv init` 默认 [15][16] |
| Poetry | ∅。path 依赖 [25] | 日常 `poetry env use` [26]。正文写不会替你装解释器 [23]；另有实验性 `poetry python install`（2.1.0）[27] | `poetry.core.masonry.api`；`poetry-core>=2.0.0,<3.0.0` [23] |
| PDM | `[tool.pdm.workspace].members`，2.28.0，experimental [38] | `pdm use` → `.pdm-python`；`pdm python install` [36] | 不强制。默认 `pdm-backend` [39] |
| pixi | 必填 `channels`、`platforms` [44]。多包是 path 依赖，无 `members`；`pixi-build` 为 preview [63] | `requires-python` 变成依赖 [46] | sdist 在 conda 环境构建 [44]。后端示例 `pixi-build-python` [64] |
| conda | 无成员表。`conda create --prefix ./envs` [59] | `python=3.9` 这种 conda 包 [59] | 不是 PEP 517 后端。solver 自 23.9 起默认 libmamba [65] |

改走 `[project]` 且标 Deprecated 的 `tool.poetry` 键：name、description、license、authors、maintainers、keywords、scripts（console/gui；`file` 仍留 tool.poetry）、extras、plugins；homepage、repository、documentation、urls 改 `project.urls`。`version` 只是 prefer `project.version` [28]。

### index、cicache、migrate

| | 私有源 | CI | 迁入 |
|---|---|---|---|
| pip | `--index-url` 默认 `https://pypi.org/simple`；`--extra-index-url`；`PIP_<UPPER_LONG_NAME>`；keyring `auto`/`disabled`/`import`/`subprocess` [3][9] | `pip cache dir`；有上层缓存才 `--no-cache-dir` [8] | `pip lock -r` 可读 requirements.txt [3] |
| uv | `[[tool.uv.index]]`；`explicit = true`；`UV_INDEX_<NAME>_USERNAME`/`PASSWORD`；凭证不进锁 [18] | `UV_CACHE_DIR`。`uv sync --locked`；`uv cache prune --ci` [20][19] | pip/pip-tools 有指南；Poetry/PDM 未写（#5200）[22] |
| Poetry | `[[tool.poetry.source]]`，`priority`=`primary`/`explicit`；`http-basic.<name>`。发布用 `repositories.<name>` [29][30] | `POETRY_CACHE_DIR`。Docker：`--no-root --no-directory` [30][31] | 可留 tool.poetry 或改 `[project]`。`poetry check` [31] |
| PDM | `[[tool.pdm.source]]`：`url`、`verify_ssl`、`username`、`password`、`type` [40] | `~/.cache/pdm`，`PDM_CACHE_DIR`；缓存键 `pdm.lock` [41][42] | `pdm import`：Pipfile、Poetry、Flit、requirements.txt、setup.py [36] |
| pixi | `channels`；`pixi auth login`。`index-url` 默认 pypi.org/simple；`extra-index-urls` [44][48] | `PIXI_CACHE_DIR`；setup-pixi 按锁哈希缓存 [49][50] | `pixi import`：`conda-env`、`pypi-txt` [51] |
| conda | `.condarc` `channels:`；URL 可嵌 `${USERNAME}:${PASSWORD}` [61] | `CONDA_PKGS_DIRS` 覆盖 `pkgs_dirs`。无 CI 菜谱 [61] | 无跨工具专页。`conda install --revision=REVNUM` [59] |

## 3. 变体与适配层

`pip-compile` 仍按环境产出 `requirements.txt` [55]。conda-lock 默认把 basic auth 留在锁里 [58]。

## 4. 用户需要知道的坑

1. 不 activate 就跑 conda 环境里的程序，一般不行 [59]。
2. uv 凭证不进锁 [18]；conda-lock 会把 basic auth 写进锁 [58]。缓存用 `UV_CACHE_DIR`、`CONDA_PKGS_DIRS`、`POETRY_CACHE_DIR` [20][61][30]。
3. pixi 同名包走 conda [46]。PDM 的 pylock 和 workspace 都是 experimental [34][38]。

## 5. 未决与置信度

pip 25.1/26.1 与 uv 0.6.15 不在摘录里。命令页仍是 EXPERIMENTAL；0.6 changelog 写过 preliminary [3][4][12]。

conda 指南写 “natively” [59]，conda-lockfiles 写插件必须装进 base [62]。pixi 首页 Lockfiles 行有 ❌，摘录无表头。Poetry「不装解释器」与 `poetry python install`（2.1.0，experimental）并存 [23][27]。pixi 迁移页写还没做构建发布 [47]，build 页已有 `pixi publish`，但是 preview [63][64]。

仍空：`pdm install` 能否读现成 pylock；uv 的 `default = true` 与 index-strategy；Poetry `supplemental`；`PIP_CACHE_DIR` 字面量。pixi 清单可以是 `pixi.toml` 或 `pyproject.toml` [45]。

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
[55] https://github.com/jazzband/pip-tools
[58] https://github.com/conda/conda-lock
[59] https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html
[61] https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html
[62] https://github.com/conda/conda-lockfiles
[63] https://pixi.prefix.dev/latest/build/workspace/
[64] https://pixi.prefix.dev/latest/build/backends/
[65] https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/conda-performance.html
