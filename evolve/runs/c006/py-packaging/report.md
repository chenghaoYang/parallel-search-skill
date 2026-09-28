# Python 包管理工具横评：uv / pip / Poetry / PDM / pixi

> 回答：五个工具差在哪、新项目怎么选。事实截至 2026-09，版本号随文标注。先读 §0 结论，再按场景查 §2 矩阵。

## 0. 一屏看懂

- **选型二分法**：纯 PyPI 项目默认选 uv；有非 Python 依赖（CUDA、GDAL、编译器、R/C++ 库）选 pixi（conda 生态）。pip 是装包基线，Poetry/PDM 是同层替代。
- **Q1·PEP 751（pylock.toml）已 Final（2025-03-31）**，但生态只到「能导出/能安装」：uv 0.6.15+ 可导出并用 `uv pip sync` 安装 [4][5]；pip 25.1 实验性 `pip lock` 生成、26.1 起 `-r pylock.toml` 消费（仍标实验）[2][3]；PDM 2.25+ 可把它当主锁文件（实验，计划未来默认）[22]；Poetry 仅经插件导出 [15][21]；pixi 不支持 [52]。
- **uv 的项目主锁仍是 uv.lock**，pylock.toml 只在 `uv pip`/`uv run --with-requirements` 层面可消费 [4][46]。
- **Q2·Poetry 2 起用标准 `[project]`（PEP 621）** 且 `poetry new` 默认生成；但 `[tool.poetry.dependencies]` 未废弃，非标准特性仍需它 [16]。
- **workspace**：uv 成熟、pixi 有、PDM 2.28 起实验；Poetry 无正式支持（issue 自 2020 挂起）[20]；pip 无。
- **装 Python**：uv、pixi（解释器即 conda 包）、PDM 2.13+ 都行；Poetry 2.1+ 实验性；pip 不管 [7][24][18]。
- **新坑高发区**：私有源认证机制互不通用；CI 应缓存包缓存而非 `.venv`。

## 1. Taxonomy

三根分类轴解释矩阵里大部分差异：① 生态（纯 PyPI vs conda 跨语言）；② 职责边界（只装包 → 管项目+环境 → 管解释器）；③ PEP 标准采用度（621/735/751 各自到导出/消费/主锁哪一层）。

| 家族 | 成员 | 划分依据 |
|---|---|---|
| 安装器 | pip | 只管「把包装进环境」；官方自述环境/解释器/project 均非其 scope [43] |
| PyPI 项目管理器 | uv、Poetry、PDM | pyproject 声明 + 锁文件 + venv 一条龙 |
| conda 系 | pixi | 锁跨语言依赖；PyPI 依赖由内嵌 uv 库解析 [32] |

## 2. 对照矩阵

### 2.1 声明与锁（D1/D2）

| 工具 | 依赖声明 | 项目锁文件 | PEP 751 层级 |
|---|---|---|---|
| uv | `[project]`(PEP621)+`[dependency-groups]`(PEP735) [6] | `uv.lock` TOML，universal 跨平台 [uv1] | 导出+安装 ✅（0.6.15）；主锁 ❌ [4][46] |
| pip | 无项目声明（requirements.txt 自有格式；可消费 PEP735）[2] | 无；`pip lock`→pylock.toml（25.1 实验，仅对当前 Python/平台有效）[3] | 消费 `-r pylock.toml`（26.1 实验）[2] |
| Poetry | `[project]`（2.0+ 默认）或 `[tool.poetry]` 并存 [16] | `poetry.lock`（专有，lock-version 2.1）[15] | 仅 `poetry-plugin-export` 导出（2.3+）[15][21] |
| PDM | `[project]` + PEP735 groups [24] | `pdm.lock`（默认）或 `pylock.toml` [22] | 导出/消费/主锁 ✅（2.25 实验）[22] |
| pixi | `[dependencies]`(conda)+`[pypi-dependencies]`；或 `[tool.pixi.*]` [31] | `pixi.lock` YAML v6，跨平台，同锁 conda+PyPI [30] | 未支持（issue open）[52] |

### 2.2 能力（D3–D6）

| 工具 | workspace | 装解释器 | 构建后端 | 项目环境 |
|---|---|---|---|---|
| uv | `[tool.uv.workspace]` members/exclude，单锁、成员 editable [6ws] | `uv python install`（python-build-standalone，默认自动）[7] | `uv_build`（仅纯 Python；扩展换 hatchling）[8] | `.venv`，`uv sync/run` 自动建 [uv1] |
| pip | — | — | 委托 PEP 517 后端（`pip wheel`，无 sdist 命令）[43] | 自管 `python -m venv`；`--python` 可指他处 [51] |
| Poetry | ∅ 正式支持；path deps+`develop=true` 代替 [20] | 2.1+ `poetry python install`（实验，Standalone Builds）[18] | `poetry-core`（2.1 起 build 与后端解耦）[15] | `{cache-dir}/virtualenvs` 或项目内 `.venv` [19] |
| PDM | `[tool.pdm.workspace]`（2.28 实验），root 单锁 [23] | `pdm python install`（2.13+）[24] | `pdm-backend`（可独立用）[27] | 默认项目内 `.venv`；PEP 582 `__pypackages__` opt-in [25] |
| pixi | 一 workspace 多 `[package]`，path 依赖 [33b] | Python 是 conda 包，版本由 `requires-python` 读出 [31t] | `pixi-build-*` 产 conda 包 [33] | `.pixi/envs/`，共享缓存硬链去重 [34] |

### 2.3 迁移 / CI / 私有源（D7–D9）

| 工具 | 官方迁移 | CI 缓存 | 私有源与认证 |
|---|---|---|---|
| uv | 官方仅「pip→uv」指南 [13]；`uv add -r`；第三方 `migrate-to-uv` 覆盖 Poetry/Pipenv/pip-tools 且保 pin [14] | `setup-uv` `enable-cache`（默认 auto）；或缓存 `UV_CACHE_DIR`+`prune --ci` [11][12] | `[[tool.uv.index]]` first-match；凭据链 URL→netrc→`uv auth`(preview)→keyring(subprocess，默认关)[9][10] |
| pip | — | `setup-python` `cache:'pip'`；本地 HTTP+wheel 缓存 [42][44] | `--index-url`/`--extra-index-url`；URL 内嵌/netrc/keyring（`--keyring-provider`）[41] |
| Poetry | `poetry init`；无官方导入器；`poetry check`+`config --migrate` 助迁 2.0 [19][15] | 官方仅仓库自用 composite action（缓存 cache-dir，键含 lock hash）[15b] | `[[tool.poetry.source]]` primary/supplemental/explicit；`http-basic`/keyring/env [17] |
| PDM | `pdm import`：Pipfile/poetry/flit/requirements.txt/setup.py 五源 [24] | `setup-pdm@v4` `cache`+`cache-dependency-path`（默认 pdm.lock）[28] | `[[tool.pdm.source]]`；env 展开/keyring 插件 [26] |
| pixi | `pixi import`：conda-env / pypi-txt [35]；可反向导出 env.yml [40] | `setup-pixi` 有 lock 即默认缓存环境（lock hash 作键）[36] | `pixi auth login`（OIDC/bearer/basic/S3→keychain）；PyPI 侧 `[pypi-options]` index-url+keyring/netrc [37][38] |

## 3. 变体与适配层

- **uv ≠ pip clone**：drop-in 仅覆盖常见 pip/pip-tools 工作流，pre-release 与 index 优先级更严格 [47]；uv 建的 venv 不含 pip（拒绝 seed/shim）[50]。
- **pixi↔uv**：pixi 把 uv 当 Rust 库解析 PyPI 依赖（不装 uv 工具）；同名包 conda 依赖优先 [32]。
- **PDM use_uv**：实验性拿 uv 当 resolver/installer；私有源凭据不传给 uv 是已知缺陷 [pdm-uv]。
- **Hatch**：1.17（2026-05）起可为环境生成 pylock.toml——「Hatch 无锁文件」已过期 [45]。

## 4. 用户需要知道的坑

1. **私有源认证不通用**：uv 故意不把凭据写进 pyproject/uv.lock——`uv add` 剥离 URL 内嵌凭据，之后 sync 401，要用 netrc/keyring/`uv auth` [48][10]（direct-URL 依赖的凭据例外，会持久化）；Poetry 走 `http-basic`+keyring [17]；GAR 场景 uv 需 `authenticate = "always"` [8gar]。
2. **CI 缓存对象搞错**：缓存包缓存（wheel/HTTP），不要缓存 `.venv`（恢复后 `uv venv` 拒绝覆盖，二手）[16c][11]；`setup-uv` `enable-cache:auto` 在 release/PR-target 等事件不缓存；`prune-cache` 删预编译 wheel 会触发重下 [12][49]。
3. **pip-tools→uv 不等于 `uv add -r`**：它把 `requests==2.31.0` 剥成 `requests`；保 pin 用 `migrate-to-uv` 或 `uv pip compile`（二手）[14][caktus]。
4. **conda→pixi**：无 base 环境（`pixi global`≈pipx）；默认 strict channel priority，混 channel 会报 "excluded" [40]。
5. **Poetry 2 迁移**：`poetry export`、`poetry shell` 2.0 起拆进插件 [15]。

## 5. 未决与置信度

- Dependabot/Renovate 对 pylock.toml 支持状态未核实（仅有 2025 年中 tracking issue）。
- 「uv 主锁不能是 pylock」依据 issue #12584（无 arbitrary graph entrypoints），文档无直接否定句 [46]。
- pixi.lock 为 YAML 是间接证据，未见逐字声明 [30]；pip requirements-file-format 页未提 pylock.toml（文档滞后，以 changelog 为准）[2]。pixi 不支持 PEP 751 已经反证：issue #3474/#3889 仍 open、代码库无 pylock 命中（截至 v0.81.0，2026-09-15）[52]。
- PDM workspace、Poetry `poetry python`、`uv auth`、pip `pip lock`/`-r pylock.toml` 均标 experimental/preview，接口可能变。

## 来源

[1] https://peps.python.org/pep-0751/
[2] https://pip.pypa.io/en/stable/news/
[3] https://pip.pypa.io/en/stable/cli/pip_lock/
[4] https://docs.astral.sh/uv/concepts/projects/export/
[5] https://github.com/astral-sh/uv/blob/main/changelogs/0.6.x.md
[6] https://docs.astral.sh/uv/concepts/projects/dependencies/
[6ws] https://docs.astral.sh/uv/concepts/projects/workspaces/
[uv1] https://docs.astral.sh/uv/concepts/projects/layout/
[7] https://docs.astral.sh/uv/concepts/python-versions/
[8] https://docs.astral.sh/uv/concepts/build-backend/
[8gar] https://github.com/astral-sh/uv/issues/12716
[9] https://docs.astral.sh/uv/concepts/indexes/
[10] https://docs.astral.sh/uv/concepts/authentication/http/
[11] https://docs.astral.sh/uv/guides/integration/github/
[12] https://github.com/astral-sh/setup-uv
[13] https://docs.astral.sh/uv/guides/migration/
[14] https://github.com/mkniewallner/migrate-to-uv
[15] https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md
[15b] https://raw.githubusercontent.com/python-poetry/poetry/main/.github/actions/poetry-install/action.yaml
[16] https://python-poetry.org/blog/announcing-poetry-2.0.0/
[16c] https://github.com/derekslinz/meta-data-mcp/blob/0cd9cedb74632107e9d3e4ab541cca2411901eb1/.github/workflows/ci.yml
[17] https://python-poetry.org/docs/repositories/
[18] https://python-poetry.org/docs/cli/
[19] https://python-poetry.org/docs/basic-usage/
[20] https://github.com/python-poetry/poetry/issues/2270
[21] https://github.com/python-poetry/poetry/issues/10356
[22] https://pdm-project.org/en/latest/usage/lockfile/
[23] https://pdm-project.org/en/latest/usage/workspace/
[24] https://pdm-project.org/en/latest/usage/project/
[25] https://pdm-project.org/en/latest/usage/venv/
[26] https://pdm-project.org/en/latest/usage/config/
[27] https://backend.pdm-project.org/
[28] https://github.com/pdm-project/setup-pdm
[30] https://pixi.prefix.dev/latest/workspace/lock_file/
[31] https://pixi.prefix.dev/latest/python/pyproject_toml/
[31t] https://pixi.prefix.dev/latest/python/tutorial/
[32] https://pixi.prefix.dev/latest/concepts/conda_pypi/
[33] https://pixi.prefix.dev/latest/build/backends/
[33b] https://pixi.prefix.dev/latest/build/workspace/
[34] https://pixi.prefix.dev/latest/workspace/environment/
[35] https://pixi.prefix.dev/latest/tutorials/import/
[36] https://pixi.prefix.dev/latest/integration/ci/github_actions/
[37] https://pixi.prefix.dev/latest/deployment/authentication/
[38] https://pixi.prefix.dev/latest/reference/pixi_manifest/
[40] https://pixi.prefix.dev/latest/switching_from/conda/
[41] https://pip.pypa.io/en/stable/topics/authentication/
[42] https://pip.pypa.io/en/stable/topics/caching/
[43] https://pip.pypa.io/en/stable/topics/workflow/
[44] https://github.com/actions/setup-python
[45] https://hatch.pypa.io/dev/history/hatch/
[46] https://github.com/astral-sh/uv/issues/12584
[47] https://github.com/astral-sh/uv/blob/8ee34679/docs/pip/compatibility.md
[48] https://github.com/astral-sh/uv/issues/11708
[49] https://github.com/astral-sh/setup-uv/issues/745
[50] https://github.com/astral-sh/uv/issues/12604
[51] https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
[52] https://github.com/prefix-dev/pixi/issues/3474
[pdm-uv] https://github.com/pdm-project/pdm/issues/3553
[caktus] https://www.caktusgroup.com/blog/2025/08/25/migrate-pip-tools-to-uv/
