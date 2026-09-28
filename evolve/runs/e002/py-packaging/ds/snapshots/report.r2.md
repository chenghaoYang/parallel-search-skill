# Python 包管理工具怎么选（2026-09）

> 覆盖 uv、pip(+pip-tools)、Poetry、PDM、conda、pixi，基于官方文档/changelog，截至 2026-09-24。4 个核心维度已落实一手来源，留白见第5节。

## 0. 一屏看懂

1. **PEP 751 `pylock.toml` 已是标准（2025-03-31 Final），但没有工具把它当默认锁文件**：uv 能读(0.12.0+)/导出+hash(0.12.11+)，仍标 preview[7]；pip 的 `pip lock`(v25.1)/`pip install -r pylock.toml`(v26.1) 都是 experimental，无稳定时间表[9][10]；PDM 可选切换为主格式(`pdm config lock.format pylock`)但仍 opt-in[25]；Poetry 未实现，只是无排期的开放 issue #10356[24]；conda/pixi 未提及。**新项目继续用各自原生锁文件**，把 pylock.toml 当「导出交换格式」。
2. **Poetry 2.0（2025-01-05）确实改用标准 `[project]` 表**，但 `[tool.poetry.*]` 不会消失：`[project.dependencies]`管构建元数据，`[tool.poetry.dependencies]`继续「enrich」（私有源、path/git 等标准表达不了的信息），无弃用时间表[19][21]。
3. **workspace/monorepo：uv、PDM、pixi 原生支持；Poetry 官方 2019 年就把 monorepo 请求关闭为「not planned」(#936)，pip 完全没有这个概念**——两者都只能靠手工拼 `path`/`-e`[44]。
4. **只有 uv、PDM、pixi 能帮你下载/管理 Python 解释器本身**（都基于 python-build-standalone 或 conda-forge）；pip、Poetry 要求 Python 已装好，Poetry 官方建议外部配 pyenv[22]；conda/pixi 把 Python 当普通包。
5. **conda 系和 PyPI 系是两套构建标准**：PyPI 系遵守 PEP 517/518；conda 包用 `meta.yaml`/`conda-build`，官方文档不提 PEP 517[34]。pixi 是唯一原生桥接两者的工具（`[pypi-dependencies]`内嵌 uv resolver）[41]。
6. **全局工具隔离运行（pipx 等价物）：uv(`uvx`)、pixi(`pixi global`)有，明确对标 pipx；Poetry、PDM 都没有**——PDM 的 `--global/-g` 其实是「切到全局项目配置文件」，与隔离运行无关，容易望文生义[48]。
7. **CI 缓存对象不同，别照抄**：uv/pip/Poetry/PDM 都能用官方 action 一行开启缓存，但 Poetry 的 `cache: poetry` 缓存的是**每个项目的 virtualenv 目录**而非包缓存[53]；conda 默认不缓存，需手动指向 `~/conda_pkgs_dir` 且必须设 `use-only-tar-bz2: true`[55]；见 D10 表。
8. **新项目速记**：纯 PyPI、要快、要一体化 → uv；已在 Poetry 生态且不需要 monorepo → Poetry；需要严格可插拔构建后端或已投入 PDM → PDM（注意 workspace 目前仍 experimental）；需要非 Python 二进制依赖（CUDA/MKL/编译库）或多语言 → pixi 优先于裸 conda（原生锁文件+workspace，conda 没有）。
9. **别把 `pip freeze > requirements.txt` 当锁文件**：pip 官方明确说这不做依赖求解[11]；**PEP 582(`__pypackages__`)已过时**：曾是 PDM 卖点，被 Python SC 拒绝后 PDM 自 v2.5.0 起降级为实验性可选、推荐用 venv[29]。

## 1. Taxonomy

**分类轴**：A = 包生态基座（PyPI/wheel 单一 vs 桥接 conda-forge 二进制生态）；B = 工具定位（all-in-one 项目管理器 vs 单一功能 point tool）。

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| PyPI 一体化项目管理器 | uv, Poetry, PDM | 自带锁文件 + venv 管理 + `pyproject.toml` 驱动全生命周期 |
| PyPI 传统组合工具 | pip(+pip-tools) | 无项目级锁文件/venv 概念，靠组合 venv/pyenv/pipx |
| conda 生态环境管理器 | conda, pixi | 装 conda channel 二进制包，能装非 Python 依赖；pixi 额外原生桥接 PyPI |

**维度**：D1 锁文件(含PEP751)｜D2 workspace/monorepo｜D3 Python版本管理｜D4 构建后端｜D5 解析器与速度｜D6 私有源｜D7 全局工具运行｜D8 迁移路径｜D9 生态定位｜D10 CI 缓存。

## 2. 对照矩阵

| 实体 | D1 锁文件 | D2 Workspace | D3 Python版本 | D4 构建后端 |
|---|---|---|---|---|
| **uv** | `uv.lock`(TOML,跨平台单文件)[1]；pylock.toml 读0.12.0+/导出+hash 0.12.11+，preview[7] | `[tool.uv.workspace]`，member 共享单锁[1] | `uv python install/pin`，python-build-standalone自动下载[2] | 默认`uv_build`（`uv init`起自带）[3] |
| **pip** | 无原生锁；`freeze`≠锁文件[11]；`pip lock`(v25.1,exp)/`install -r pylock.toml`(v26.1,exp)[9][10] | 无概念，靠`-e`手工编排 | 官方明确不管理版本，`--python`只选目标环境[12] | 无默认后端，按PEP517/518委托[15] |
| **Poetry** | `poetry.lock`,`install`时自动生成[20] | **确认没有**：#936(2019)closed not planned，仅`path`依赖(`file://`不可移植)[44] | 不下载解释器，`env use`从已装版本选，建议配pyenv[22] | `poetry-core`(`poetry.core.masonry.api`)[20] |
| **PDM** | `pdm.lock`默认[25]；pylock导出v2.24.0/可选主格式v2.25.0，opt-in[25][30] | 原生`[tool.pdm.workspace]`(v2.28.0,**experimental**)，member隐式可编辑依赖[26] | `pdm python install`，同用python-build-standalone[27] | `pdm-backend`(v2.5.0起默认)，可换任意后端[30] |
| **conda** | `environment.yml`不锁build string；`--explicit`精确但单平台；26.5+支持读`conda-lock.yaml`/`pixi.lock`[31] | 概念页确认不含[32] | `create -n env python=3.x`，Python即普通包[33] | 非PEP517体系；`conda-build`+`meta.yaml`[34] |
| **pixi** | `pixi.lock`(YAML)单文件锁多平台+多环境[39] | 原生`[environments]`+`[feature]`组合[40] | conda-forge渠道装解释器，可精确指定版本[41] | `pixi-build`(preview)多后端；PyPI依赖内嵌uv resolver[41] |

| 实体 | D5 解析/速度 | D6 私有源 | D7 全局工具 | D8 迁移 | D9 定位 |
|---|---|---|---|---|---|
| **uv** | Rust,Git基于Cargo；官方称比pip快10-100x[8] | `[[tool.uv.index]]`,env var/URL/netrc/keyring[4] | `uvx`=`uv tool run`，pipx等价[5] | 官方仅「pip→uv」指南[6] | 称可替代pip/pip-tools/pipx/poetry/pyenv等[8] |
| **pip** | v20.3起回溯算法，官方明说优先正确性而非速度[13] | `--index-url`/`--extra-index-url`,3种认证[14] | 自身无隔离，指向PyPA同门pipx[18] | 无迁移指南；`pip lock`可从现有文件生成[9] | 「the package installer for Python」，PyPA维护[22] |
| **Poetry** | 未公开算法名；FAQ称「highly optimized」但复杂依赖仍慢；有`solver.min-release-age`等调优项[46][47] | `[[tool.poetry.source]]`,`priority`分级[23] | **确认没有**，`run`要求项目内[30] | **确认没有**：`init`不支持从requirements.txt/setup.py导入[46] | 「dependency management and packaging made easy」[20] |
| **PDM** | `resolvelib`，版本持续升级，无官方速度基准[30] | `[[tool.pdm.source]]`,env var插值,keyring[28] | **确认没有**：`--global`是切全局项目配置，非工具隔离；无`tool install/run`命令[48][49] | `init/import`自动识别Pipfile/Poetry/Flit/pip/setuptools[27] | 强调后端自由选择 |
| **conda** | 23.10.0起默认`libmamba`替代经典solver；26.5.0插件化`BaseSolver`[35] | `.condarc`,全局/环境级channel[36] | `conda run -n env <cmd>`免激活[31] | guidance：先conda后pip，出问题重建环境而非混改[31] | 跨语言二进制包管理器，NumFOCUS赞助[37] |
| **pixi** | Rust`rattler`库，有性能优化记录，无vs conda classic量化对比[41] | conda私有channel+PyPI私有index分开配，`pixi auth login`统一(token/OAuth/basic/S3)[41] | `pixi global install`，官方明确类比pipx[43] | 官方同时提供「from conda/mamba」和「from Poetry」指南，6者中最全[42] | 「built on conda ecosystem」，workspace-centric[41] |

**D10 CI 缓存**（GitHub Actions 官方 action，均按锁文件哈希做 cache key）：

| 实体 | 官方 action / 选项 | 缓存对象 |
|---|---|---|
| uv | `setup-uv`，`enable-cache`[50] | 全局 cache 目录，key基于`uv.lock`[51] |
| pip | `setup-python`，`cache: 'pip'`[53] | 全局 cache 目录，key基于requirements.txt |
| Poetry | `setup-python`，`cache: 'poetry'`[53] | **每个项目的 virtualenv 目录**，key基于`poetry.lock` |
| PDM | `setup-pdm`，`cache: true`[54] | key默认基于`./pdm.lock`，支持glob自定义 |
| conda | `setup-miniconda` | 需手动配`actions/cache`指向`~/conda_pkgs_dir`+`use-only-tar-bz2: true`[55] |
| pixi | `setup-pixi` | 有`pixi.lock`即自动缓存项目环境；全局缓存需另开，按月过期[56] |

## 3. 变体与适配层

| 变体 | 相对参照系差在哪 |
|---|---|
| pixi vs conda | 不是替代品，是建在 conda 生态之上：加了原生锁文件、workspace、内嵌 uv 原生装 PyPI 包，conda 本身没有这三样 |
| Poetry `[project]` vs `[tool.poetry]` | 2.0 起标准字段管元数据；`[tool.poetry]`继续管私有源/增强依赖，无强制迁移时间表 |
| PEP 751 支持 vs 各自原生锁 | 无工具将其设为默认；PDM 走得最远(可选主格式)，其余是「能读/导出」而非「默认使用」 |

## 4. 用户需要知道的坑

- **迁移**：pip/requirements.txt→uv 有官方指南[6]；Pipfile/Poetry/Flit/pip/setup.py→PDM 自动识别导入[27]；conda/mamba 或 Poetry→pixi 有专门指南，6 者最全[42]；**Poetry 反向没有官方迁移指南，`poetry init`不支持自动导入**[46]；pip 生态内部升级到锁文件工具也没有专门指南。
- **私有源认证方式不通用**：uv 用`[[tool.uv.index]]`+keyring[4]；pip 用`--index-url`+netrc/keyring[14]；Poetry 用`poetry config http-basic.*`[23]；PDM 用 URL 内嵌变量[28]；conda 用`.condarc`[36]；pixi 的 conda 源和 PyPI 源要分开配，登录走`pixi auth login`[41]——换工具不能照抄配置。
- **CI 缓存对象不同**：见上表 D10；最容易踩坑的是 Poetry（缓存的是 venv 目录而非包缓存）和 conda（默认不缓存，需手动加 `use-only-tar-bz2`）。
- **conda+pip 混用有官方风险提示**：尽量先 conda 装完再 pip 补充；出问题重建环境而非反复混改[31]。
- **PEP 582 已过时**：见一屏看懂第 9 条。

## 5. 未决与置信度

- Poetry 解析器具体算法名称、pixi 底层是否为 Resolvo：官方均未公开/未给量化速度对比，第三方提及但无法溯源，**低优先级留白**。
- 以下是查证后的明确结论、非空缺：pip 内部无「requirements.txt 升级到锁文件」官方指南（靠 `pip lock` 直接生成）；Poetry/pip 官方文档都没有独立 CI 集成章节（相关做法来自 `actions/setup-python` 通用 action README）。

## 来源

uv: [1]https://docs.astral.sh/uv/concepts/projects/workspaces [2]…/guides/install-python [3]…/concepts/build-backend [4]…/concepts/indexes [5]…/guides/tools [6]…/guides/migration [7]https://github.com/astral-sh/uv/releases [8]https://github.com/astral-sh/uv [50]https://github.com/astral-sh/setup-uv [51]https://docs.astral.sh/uv/guides/integration/github
pip: [9]https://pip.pypa.io/en/stable/cli/pip_lock [10]…/cli/pip_install [11]…/cli/pip_freeze [12]…/topics/python-option [13]…/topics/dependency-resolution [14]…/topics/authentication [15]…/reference/build-system [18]https://pipx.pypa.io/latest [53]https://github.com/actions/setup-python
Poetry: [19]https://github.com/python-poetry/poetry/releases/tag/2.0.0 [20]https://python-poetry.org/docs/pyproject [21]…/docs/dependency-specification [22]…/docs/managing-environments [23]…/docs/repositories [24]https://github.com/python-poetry/poetry/issues/10356 [44]…/issues/936 [45]…/issues/7677 [46]https://python-poetry.org/docs/faq [47]https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md
PDM: [25]https://pdm-project.org/latest/usage/lockfile [26]…/usage/workspace [27]…/usage/project [28]…/usage/config [29]…/usage/pep582 [30]https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md [48]…/src/pdm/cli/options.py [49]https://pdm-project.org/latest/reference/cli [54]https://github.com/pdm-project/setup-pdm
conda: [31]https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html [32]…/concepts/index.html [33]…/manage-python.html [34]https://docs.conda-build.io/en/latest/user-guide [35]https://github.com/conda/conda/blob/main/CHANGELOG.md [36]https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html [37]https://conda.org [55]https://github.com/conda-incubator/setup-miniconda
pixi: [39]https://raw.githubusercontent.com/prefix-dev/pixi/main/docs/workspace/lock_file.md [40]…/workspace/multi_environment.md [41]…/reference/pixi_manifest.md [42]…/switching_from/ [43]…/global_tools/introduction.md [56]https://github.com/prefix-dev/setup-pixi
