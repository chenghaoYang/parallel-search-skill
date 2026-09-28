# Python 包/项目管理工具对比：uv · pip · Poetry · PDM · pixi

> 截至 2026-09，均来自官方文档/changelog。读法：§0 结论 → §1 选家族 → §2/§3 细节 → §4 坑。

## 0. 一屏看懂

- **PEP 751（pylock.toml）已 Final**（2025-03-31）[1]，但目前各工具只把它当**交换格式**而非唯一锁：uv 0.6.15+ 可导出也可安装[2]，pip 25.1+ 有实验性 `pip lock`、26.1+ 可 `pip install -r pylock.toml`[3][4]，PDM 2.24+ 可导出、2.25+ 可选它当主锁格式（实验性、官方称将成默认）[5]，Poetry 2.3+ 只能经插件导出、不能替代 poetry.lock[6]。
- **Poetry 2.0（2025-01）起支持标准 `[project]` 表**（PEP 621）并废弃一批 `tool.poetry` 字段；官方建议依赖写 `project.dependencies`，但 dependency groups、相对 path 依赖等仍须 `[tool.poetry]`[7][8]。
- **先选生态再选工具**：PyPI 系（uv、Poetry、PDM、pip）只装 Python 包；conda 系（pixi、conda）能装 CUDA、编译器等任意二进制依赖[9]。
- **再选层**：pip 官方自定为纯安装器，「不打算管整个工作流」[10]；uv/Poetry/PDM/pixi 是项目管理器（建环境、锁、跑、发布）；conda 是环境层。
- **新项目默认选 uv**：一个工具覆盖装解释器、锁、workspace、构建发布；代价是主锁 uv.lock 为私有格式（可导出 pylock.toml）[11][12]。
- **要 GPU/系统级依赖或对接 conda 生态选 pixi**；只部署应用、想钉死版本，pip + pylock.toml/requirements.txt 已够。
- **monorepo**：uv、PDM（2.28 实验性）、pixi 有真 workspace；Poetry 只有 path deps + groups 变通（issue #6850），pip 没有此概念[13][14]。

## 1. Taxonomy

两条分类轴解释几乎所有差异：

- **轴 A 生态**：PyPA 系解析 PyPI wheel 进 `.venv`；conda 系从 channel 解析二进制包进 prefix 环境，Python 解释器本身也是个 conda 包[15]。
- **轴 B 定位层**：安装器（只管装包）→ 项目管理器（pyproject/锁/任务/发布）→ 环境/解释器层（conda、pyenv、uv python）。

| 家族 | 成员 | 一句话 |
|---|---|---|
| PyPA 项目管理器 | uv、Poetry、PDM | pyproject.toml + 私有锁 + venv + build/publish |
| PyPA 安装器 | pip | 无项目概念；锁是新增的实验能力 |
| conda 项目管理器 | pixi | pixi.toml 或 pyproject.toml `[tool.pixi]`，锁 conda+PyPI |
| conda 环境层 | conda（mamba 同族） | environment.yml，不管项目 |
| 配套 | hatch（env+后端）、pyenv（解释器）、pipx/uvx（应用）、twine | 与上面互补而非竞争 |

## 2. 对照矩阵

### 2a. 项目模型

| 工具 | 元数据表 | workspace/monorepo | Python 版本 | 构建/发布 |
|---|---|---|---|---|
| uv | 标准 `[project]` + `[tool.uv]` | `[tool.uv.workspace]` members/exclude + `tool.uv.sources` `workspace=true`；全 workspace 共享一把 uv.lock 和一个 requires-python[13] | `uv python install` 自动下载托管 CPython/PyPy；`.python-version` 逐层上溯[16] | `uv_build` 为 init 默认后端但仅纯 Python；`uv build`/`uv publish`[17] |
| pip | 无 | — | 不管；`--python` 只指向已有解释器/venv[18] | — |
| Poetry | 2.0+ `[project]` 与 `[tool.poetry]` 并存：project 管构建元数据，tool.poetry 仅富化锁定、存 groups/package-mode 等[7] | 无内建 workspace（#2270 open）；变通 = path 依赖 + groups（#6850）[14] | 不装解释器，配合 pyenv；`poetry env use` 切换[19] | `poetry-core` 后端；`poetry build`/`publish`（publish 不自动 build）[20] |
| PDM | `[project]`（PEP 621，自 1.0 即标准） | `[tool.pdm.workspace]`（2.28 实验）：成员是 root 的隐式 editable 依赖、共享 root 锁[21] | `pdm python install`（python-build-standalone，2.13+）[22] | `pdm-backend` 默认（2.5 起）；`pdm publish` 支持 OIDC[23] |
| pixi | `pixi.toml` 或 pyproject.toml `[tool.pixi]`；`[project]` 字段自动映射（requires-python→conda python 依赖，dependencies→pypi-dependencies）[24] | feature/`[environments]` 组合出多环境 + solve-group[25] | python 是 conda-forge 依赖，随环境装；各 environment 可不同版本[15] | `pixi build`（preview）经 pixi-build-python/rattler-build 产 .conda[26] |
| conda | environment.yml | — | python 是 conda 包 | conda-build / rattler-build |

### 2b. 锁文件与环境

| 工具 | 主锁文件 | pylock.toml 支持 | 环境 |
|---|---|---|---|
| uv | `uv.lock`（私有 TOML，跨平台 universal）[12] | 导出 `uv export --format pylock.toml`；安装 `uv pip sync/install -r pylock.toml`（安装侧仍是 preview 特性 `pylock`）[2][27] | 项目 `.venv` |
| pip | requirements.txt（单平台、非真锁） | `pip lock` 实验导出（25.1+）；`pip install -r pylock.toml`（26.1+）；锁只对当前 Python/平台有效[3][4] | 不管环境 |
| Poetry | `poetry.lock` | 仅导出：2.3.0+ 且 poetry-plugin-export 1.10+[6] | virtualenv；默认 `{cache-dir}/virtualenvs`，设 `virtualenvs.in-project` 用 `.venv`[28] |
| PDM | `pdm.lock`（哈希+markers，可选 static_urls） | 导出 `pdm export -f pylock`（2.24+）；`pdm config lock.format pylock` 当主锁（2.25+，实验性，官方称将成默认）[5] | 默认 `.venv`；PEP 582 `__pypackages__` 已被拒（PEP 582 Rejected），转 opt-in[29] |
| pixi | `pixi.lock`（YAML，version: 7；锁 conda+PyPI 双生态、按 env×platform 求解）[30] | 无；维护者称 conda 依赖无法用 pylock 表达，pixi.lock 仍是主锁（issue #3889）[31] | `.pixi` prefix；`[pypi-dependencies]` 由内置 uv 求解，conda-first[9] |
| conda | 26.5+ 原生支持 `conda-lock.yaml`/`pixi.lock`[32] | ∅ | prefix 环境，跨语言二进制[9] |

## 3. pylock.toml 适配层（PEP 751 生态）

- 规范本体：Final，canonical spec 在 packaging.python.org，`lock-version="1.0"`；PEP 明确**不完全替代** requirements.txt（多用途锁 vs 单用途），且落地是各工具自愿[1][33]。
- 文件名规则：`pylock.toml` 或 `pylock.<name>.toml`；`packaging` 26.1+ 内置 `packaging.pylock` 读写校验[34]。
- 其他工具：hatch 1.17.0（2026-05）`hatch env lock`/`hatch lock` 产 pylock.toml（pip locker 只产不装，装靠 uv）[36]；pipenv 实验性读写（`use_pylock=true`，两锁并存时优先 pylock）[37]；pip-tools 没有（PR #2380 关闭未合并）[34]。
- 限制：pip 的 `-r pylock.toml` 不能和 `--python-version/--platform/--abi` 同用；实验性 `pip lock` 产不出 extras/dependency-groups[35]。
- Dependabot、Renovate 均未支持 pylock（各有跟踪 issue）——纯 pylock 项目拿不到自动更新 PR[40]。

## 4. 用户需要知道的坑

1. **pylock.toml ≠ 通用主锁**。各家主锁仍是私有格式；pylock 目前定位是导出/交换。别急着删 poetry.lock/uv.lock[6][12]。
2. **锁文件互转基本不存在**：poetry.lock→uv.lock 无官方转换（uv 迁移指南只有 pip 路线，其余「尚未编写」#5200）[41]；第三方 `migrate-to-uv` 支持 Poetry/Pipenv/pip-tools/pip 且保留已锁版本，但不支持 PDM[42]。PDM 自带 `pdm import`（Pipfile/Poetry/Flit/requirements.txt/setup.py）[43]；pixi 有 `pixi init --import environment.yml`[44]。
3. **私有源凭据互不兼容**：uv 始终读 `.netrc`（另有 credentials.toml、keyring 默认关）[45]；Poetry 用 `http-basic`+keyring/auth.toml，官方警告 netrc 会冲突[46]；pixi 走 rattler credentials/keychain[47]。换工具要重配。
4. **CI 缓存按工具选 action**：`setup-uv` 的 `enable-cache`（auto）[48]、`setup-pdm` 的 `cache`+`cache-dependency-path`（默认 pdm.lock）[49]、`setup-pixi`（有 pixi.lock 自动按哈希缓存）[50]；`actions/setup-python` 的 `cache` 只认 pip/pipenv/poetry[51]。uv 默认 cache glob 未列 pylock.toml（见 §5）。
5. **Poetry `[project]` 表的两个残留限制**：只能放主依赖（groups 仍归 tool.poetry）；path 依赖在 `[project]` 里只能是绝对 `file://` URL（不可移植），相对路径仍须 `[tool.poetry]`[8]。
6. **uv workspace 是单锁单 requires-python**：成员需要不同 Python 版本/冲突依赖时不能用 workspace，只能 path 依赖[13]。
7. **pixi 装 PyPI 包是 conda-first**：同名包优先 conda 版；纯 Python 项目不必进 conda 生态[9]。

## 5. 未决与置信度

- Poetry 读 pylock.toml：只见导出证据，未见「不支持 import」的否定原句 → 记「未见支持」（未反证）。
- `uv export --format pylock.toml` 是否仍 preview-gated：export 页无标注、preview 页只列安装侧，未逐字确认。
- setup-uv 默认 `cache-dependency-glob` 是否含 pylock.toml：摘要列了 `*.py.lock` 但未复核原句。
- pixi issue #3889 开闭未确认；「各 environment 可用不同 Python 版本」仅 feature 示例暗示。
- conda 26.5 锁文件细节（生成还是只消费）未展开；conda-build 未查（⚠）。
- hatch/pipenv 的 pylock 细节为单源（官方页/PR），未经第二来源复核。
- rye 已归档停更（指向 uv）[52]；pipenv/conda-lock/mamba 仅边缘覆盖。

## 来源

[1] https://peps.python.org/pep-0751/
[2] https://github.com/astral-sh/uv/releases/tag/0.6.15
[3] https://pip.pypa.io/en/stable/news/
[4] https://pip.pypa.io/en/stable/cli/pip_lock/
[5] https://pdm-project.org/en/latest/usage/lockfile/
[6] https://python-poetry.org/blog/announcing-poetry-2.3.0/
[7] https://python-poetry.org/docs/dependency-specification/
[8] https://python-poetry.org/docs/pyproject/
[9] https://pixi.prefix.dev/latest/concepts/conda_pypi/
[10] https://pip.pypa.io/en/stable/topics/workflow/
[11] https://docs.astral.sh/uv/
[12] https://docs.astral.sh/uv/concepts/projects/layout/
[13] https://docs.astral.sh/uv/concepts/projects/workspaces/
[14] https://github.com/python-poetry/poetry/issues/2270
[15] https://pixi.prefix.dev/latest/python/tutorial/
[16] https://docs.astral.sh/uv/concepts/python-versions/
[17] https://docs.astral.sh/uv/concepts/build-backend/
[18] https://pip.pypa.io/en/stable/topics/python-option/
[19] https://python-poetry.org/docs/managing-environments/
[20] https://python-poetry.org/docs/libraries/
[21] https://pdm-project.org/latest/usage/workspace/
[22] https://pdm-project.org/en/latest/usage/project/
[23] https://pdm-project.org/latest/usage/publish/
[24] https://pixi.prefix.dev/latest/python/pyproject_toml/
[25] https://pixi.prefix.dev/latest/workspace/multi_environment/
[26] https://pixi.prefix.dev/latest/build/getting_started/
[27] https://docs.astral.sh/uv/concepts/preview/
[28] https://python-poetry.org/docs/configuration/
[29] https://pdm-project.org/en/latest/usage/pep582/
[30] https://pixi.prefix.dev/latest/workspace/lock_file/
[31] https://github.com/prefix-dev/pixi/issues/3889
[32] https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
[33] https://packaging.python.org/en/latest/specifications/pylock-toml/
[34] https://github.com/jazzband/pip-tools/pull/2380
[35] https://github.com/pypa/pip/pull/13876
[36] https://github.com/pypa/hatch/blob/master/docs/blog/posts/release-hatch-1170.md
[37] https://pipenv.pypa.io/en/stable/pylock.html
[40] https://discuss.python.org/t/community-adoption-of-pylock-toml-pep-751/89778
[41] https://docs.astral.sh/uv/guides/migration/pip-to-project/
[42] https://github.com/mkniewallner/migrate-to-uv
[43] https://pdm-project.org/en/latest/usage/project/
[44] https://pixi.prefix.dev/latest/reference/cli/pixi/init/
[45] https://docs.astral.sh/uv/concepts/authentication/http/
[46] https://python-poetry.org/docs/repositories/
[47] https://pixi.prefix.dev/latest/deployment/authentication/
[48] https://github.com/astral-sh/setup-uv
[49] https://github.com/pdm-project/setup-pdm
[50] https://pixi.prefix.dev/latest/integration/ci/github_actions/
[51] https://github.com/actions/setup-python
[52] https://github.com/astral-sh/rye
