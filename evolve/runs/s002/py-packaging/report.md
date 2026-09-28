# Python 包管理怎么选：uv、pip、Poetry、PDM、pixi

> 新项目在 uv、pip、Poetry、PDM、pixi 里怎么选。只写有官方原句的事实。调研日 2026-09-24。先读第 0 节，字段在第 2 节。版本号尚未反证。

## 0. 一屏看懂

- 三层，不是同一条安装命令。pip 只管已有环境里的包。uv、Poetry、PDM 编辑 `[project]`。pixi 编辑 `[workspace]`（或 `[tool.pixi.*]`），主源是 conda channel。[3][11][13][23][29]
- 只装包：pip。纯 Python、要同时管锁和解释器：uv。依赖组已在 `[tool.poetry]`：留 Poetry。项目锁就要 `pylock.toml`：PDM 的 `lock.format=pylock`。要 conda 包：pixi。
- 项目锁各写各的：`uv.lock`（页上写其他工具不能用）、`poetry.lock`、默认 `pdm.lock`、`pixi.lock`。`pylock.toml` 是 PEP 751 的交换格式，状态 Final（决议 2025-03-31），文件名还有 `pylock.<name>.toml`。[1][7][16][20][28]
- 疑点 D1：uv 和 pip 的文档都有 pylock，但都不是项目锁。uv 导出给 `uv pip`（`uv pip sync pylock.toml`），项目命令仍写 `uv.lock`。pip 的 `pip lock` 与 `pip install -r` 标 EXPERIMENTAL，产物只保证当前平台。[1][2][8][9]
- 疑点 D2：Poetry 2.0 公告写 respects the `project` section（PEP 621），并写 `tool.poetry.dependencies` is not deprecated。只有主依赖能放进 `[project]`，其他组仍必须在 `[tool.poetry]`。[13][15]
- 解释器：uv 下载并写 `.python-version`；Poetry 用 `poetry env use`（另有 2.1.0 的 `poetry python install`）；PDM 写 `.pdm-python`；pixi 的 python 是 conda 包；pip 只用 `--python`。[4][12][18][19][23][30]
- 默认后端：`uv_build`、`poetry.core.masonry.api`、`pdm.backend`（该页写不支持 poetry-core）、pixi 的 `pixi-build-python`。[5][14][25][31]
- 私有源不要照搬 `--extra-index-url`。uv 默认 `first-index`。Poetry 用 `priority`：`primary`、`supplemental`、`explicit`。pip 才是 `--index-url` 加 `--extra-index-url`。[8][27][32]

## 1. Taxonomy

轴是「项目真相放在哪一层」：它决定锁、成员表、构建后端归不归这个工具管。

| 家族 | 真相 | 谁 | 后果 |
|---|---|---|---|
| 安装器 | 调用者给的需求文件 | pip | pylock 只是需求格式 |
| PyPI 项目管理器 | `[project]` + 自家锁 | uv、Poetry、PDM | 锁文件名仍然不同 |
| conda 工作区 | `channels` 与 `platforms` | pixi | Python 是 conda 包；PyPI 结果写进 `pixi.lock`（`kind: pypi`）[28][29] |

列的含义见第 2 节表头。conda、hatch、pip-tools、pipenv 见第 5 节。

## 2. 对照矩阵

### 锁与元数据

| | 项目锁 | pylock.toml | 人编辑的表 |
|---|---|---|---|
| uv | `uv.lock`（universal，勿手改）[1] | 写：`uv export -o pylock.toml`、`uv pip compile -o pylock.toml`。读：`uv pip sync pylock.toml`、`uv pip install -r pylock.toml`。0.6.15 称 preliminary [1][2][6] | `[project]`、`[dependency-groups]`、`[tool.uv.sources]` [3] |
| pip | 无 [11] | `pip lock` 默认 `pylock.toml`，EXPERIMENTAL。`pip install -r` 亦标 experimental。写 25.1，读 26.1 [8][9][10] | 不管 `[project]` [11] |
| Poetry | `poetry.lock`；`poetry lock` 默认 `--no-update`，重算 `--regenerate` [13][16] | 不能替换 `poetry.lock`。导出要 poetry-plugin-export ≥1.10.0（公告 2.3.0）。无读取原句 [17] | `[project]`；组仍在 `[tool.poetry]`。`name` 标 Deprecated [13][14][15] |
| PDM | `pdm.lock`；`lock.format`=`pdm`\|`pylock`（`PDM_LOCK_FORMAT`）[20][21] | 设为 `pylock` 后 `pdm lock` 写 `pylock.toml`。另有 `pdm export -f pylock`（页标 Added in 2.24.0）[20] | `[project]`、`[dependency-groups]`、`[tool.pdm]` [23] |
| pixi | `pixi.lock`；不向前兼容。version 见第 5 节 [28] | ∅ | `pixi.toml` 或 `[tool.pixi.*]`，前者优先 [29] |

PEP 751 必填 `lock-version`=`"1.0"`、`created-by`、`[[packages]]`。该页自称历史文档。[7]

### workspace、解释器、构建后端

| | 成员 | 解释器 | build-backend |
|---|---|---|---|
| uv | `[tool.uv.workspace].members` 必填；`{ workspace = true }` [35] | `uv python pin` → `.python-version`；`uv python install` [4] | `uv_build`；`--build-backend` 还可选 hatchling、flit-core、pdm-backend、setuptools、maturin、scikit-build-core [5] |
| pip | ∅ | `--python` 指向已有解释器或 venv [12] | 项目自己的 PEP 517 backend；`--no-build-isolation` [36] |
| Poetry | ∅。path：`develop = true`。`project.dependencies` 只收绝对路径 [15] | `poetry env use`；`poetry python install`（Introduced in 2.1.0）[18][19] | `poetry.core.masonry.api` [14] |
| PDM | `[tool.pdm.workspace].members`（Added in 2.28.0）。lock/sync 在根目录 [24] | `pdm use` → `.pdm-python`；`pdm python install`（2.13.0）[23][33] | `pdm.backend`。页上写不支持 poetry-core [25] |
| pixi | `[workspace]` 的 `channels`、`platforms`、`name` [29] | conda 依赖 `python = "3.11.*"`；会读 `requires-python` [29][30] | `[package.build.backend].name`，如 `pixi-build-python` [31] |

git/path：uv 用 `[tool.uv.sources]`；Poetry 用 `path`/`git`；PDM 用 `file:///${PROJECT_ROOT}` 与 `git+url@rev`。[3][15][37]

### 迁移、缓存、私有源

| | 迁入 | 缓存 | 私有源 |
|---|---|---|---|
| uv | `uv add -r` 与 `-c`。Poetry/PDM 指南写明还没写 [38] | `UV_CACHE_DIR`（否则 `$HOME/.cache/uv`）。setup-uv：`enable-cache: true`；`uv cache prune --ci` [26][39] | `[[tool.uv.index]]` `url`；`default` / `explicit`。`UV_INDEX_<NAME>_PASSWORD` 不进锁 [27] |
| pip | `pip lock -r requirements.txt -o pylock.toml` [8] | `PIP_CACHE_DIR` [40] | `PIP_INDEX_URL` 默认 `https://pypi.org/simple`；`PIP_EXTRA_INDEX_URL`；`.netrc` 或 keyring [8][41] |
| Poetry | `poetry check` 列出废弃字段 [14] | `POETRY_CACHE_DIR`；`poetry install --only main --no-root --no-directory` [42] | `[[tool.poetry.source]]` 的 `priority`；`POETRY_HTTP_BASIC_<NAME>_PASSWORD` [32] |
| PDM | `pdm import -f pipfile\|poetry\|flit\|setuppy\|requirements` [23] | `PDM_CACHE_DIR`；setup-pdm 的 `cache` 默认 false [22][43] | `[[tool.pdm.source]]`；`name="pypi"` 替换默认源；keyring `pdm-pypi-<name>` [22] |
| pixi | `pixi init --import environment.yml`（也有 `--format=conda-env` / `pypi-txt`）[44] | `PIXI_CACHE_DIR`；有锁时 setup-pixi 按锁哈希缓存 [45][46] | `channels` 写 URL；`pixi auth login <HOST>`；PyPI 用 `index-url` [29][47] |

## 3. 变体与适配层

对照 PEP 751：uv、Poetry 的项目锁不变，pylock 只是 `uv pip` 或 poetry-plugin-export 的出口。pip 的锁就是 pylock，且只承诺当前平台。PDM 的 `lock.format=pylock` 把项目锁写成 `pylock.toml`（默认 `pdm`）。pixi 写入 `pixi.lock`。[1][8][17][21][29]

## 4. 用户需要知道的坑

| 现象 | 处理 |
|---|---|
| 有 pylock 时 `uv sync` 仍看 `uv.lock` | 交给 pip 才 `uv export -o pylock.toml` [1] |
| `pip lock` 只保证当前平台，且标 EXPERIMENTAL；PEP 已是 Final | 多平台 CI 不要单靠这一份 [7][8] |
| Poetry 2 只改 `[project]`，组依赖变了 | 组留在 `[tool.poetry]`；该键只 enrich 锁定 [15] |
| 私有源装到公共同名包，或设了密码仍像缺包 | uv 默认 `first-index`；Poetry 对该源用 `priority="explicit"`。密码变量的中缀是源的 `name`：`UV_INDEX_<NAME>_PASSWORD`、`POETRY_HTTP_BASIC_<NAME>_PASSWORD`、keyring `pdm-pypi-<name>`。uv 不把凭据写入锁 [22][27][32] |
| 三家 CI 缓存默认不同 | setup-uv 写 `enable-cache: true`；有 `pixi.lock` 时 setup-pixi 按哈希缓存；setup-pdm 的 `cache` 默认 false [39][43][45] |
| pixi 升级后拒绝锁 | 文档示例仍是 `version: 6`；0.68.0（2026-05-07）起为 v7，且不向前兼容 [28][48] |

## 5. 未决与置信度

下面还不是定论。

- 版本起点未反证：uv 0.6.15、pip 写 25.1 / 读 26.1、Poetry 2.0.0 与导出 2.3.0、PDM 页标的 2.24.0 与 2.28.0。
- 查过的页没有原句，所以不能写成「做不到」：Poetry 读取已有 pylock；pip 是否校验 `environments` / marker / 哈希；有没有 `pip sync`；pip 与 Poetry 在别的页是否后来加了 workspace。
- 文档打架：PDM 锁页既写只支持 requirements.txt，又写能导出 pylock。`.python-version` 标 Added in 2.23.0，release notes 到 2.24.0 才出现。PDM 说 poetry-core 不能读 PEP 621，Poetry 2 却用它的 backend 读 `[project]`。pixi 的 version 冲突见第 4 节。
- conda 整行是 ❓。hatch、pip-tools、pipenv、rye、mamba 还在线索里，没有进矩阵。

## 来源

[1] https://docs.astral.sh/uv/concepts/projects/layout/
[2] https://docs.astral.sh/uv/pip/compile/
[3] https://docs.astral.sh/uv/concepts/projects/dependencies/
[4] https://docs.astral.sh/uv/concepts/python-versions/
[5] https://docs.astral.sh/uv/concepts/projects/init/
[6] https://github.com/astral-sh/uv/releases/tag/0.6.15
[7] https://peps.python.org/pep-0751/
[8] https://pip.pypa.io/en/latest/cli/pip_lock/
[9] https://pip.pypa.io/en/stable/cli/pip_install/
[10] https://pip.pypa.io/en/stable/news/
[11] https://pip.pypa.io/en/stable/topics/workflow/
[12] https://pip.pypa.io/en/stable/topics/python-option/
[13] https://python-poetry.org/blog/announcing-poetry-2.0.0
[14] https://python-poetry.org/docs/pyproject/
[15] https://python-poetry.org/docs/dependency-specification/
[16] https://python-poetry.org/docs/basic-usage/
[17] https://python-poetry.org/blog/announcing-poetry-2.3.0/
[18] https://python-poetry.org/docs/managing-environments/
[19] https://python-poetry.org/docs/cli/
[20] https://pdm-project.org/en/latest/usage/lockfile/
[21] https://pdm-project.org/en/latest/reference/configuration/
[22] https://pdm-project.org/en/latest/usage/config/
[23] https://pdm-project.org/en/latest/usage/project/
[24] https://pdm-project.org/en/latest/usage/workspace/
[25] https://pdm-project.org/en/latest/reference/build/
[26] https://docs.astral.sh/uv/concepts/cache/
[27] https://docs.astral.sh/uv/concepts/indexes/
[28] https://pixi.prefix.dev/latest/workspace/lock_file/
[29] https://pixi.prefix.dev/latest/reference/pixi_manifest/
[30] https://pixi.prefix.dev/latest/python/pyproject_toml/
[31] https://pixi.prefix.dev/latest/build/backends/
[32] https://python-poetry.org/docs/repositories/
[33] https://github.com/pdm-project/pdm/releases/tag/2.13.0
[35] https://docs.astral.sh/uv/concepts/projects/workspaces/
[36] https://pip.pypa.io/en/stable/reference/build-system/
[37] https://pdm-project.org/en/latest/usage/dependency/
[38] https://docs.astral.sh/uv/guides/migration/pip-to-project/
[39] https://docs.astral.sh/uv/guides/integration/github/
[40] https://pip.pypa.io/en/stable/topics/caching/
[41] https://pip.pypa.io/en/stable/topics/authentication/
[42] https://python-poetry.org/docs/configuration/
[43] https://github.com/pdm-project/setup-pdm
[44] https://pixi.prefix.dev/latest/reference/cli/pixi/init/
[45] https://pixi.prefix.dev/latest/integration/ci/github_actions/
[46] https://pixi.prefix.dev/latest/reference/pixi_configuration/
[47] https://pixi.prefix.dev/latest/deployment/authentication/
[48] https://github.com/prefix-dev/pixi/blob/main/CHANGELOG.md
