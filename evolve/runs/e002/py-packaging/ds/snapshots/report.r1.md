# Python 包/项目管理工具怎么选（2026-09）

> 覆盖 uv、pip(+pip-tools)、Poetry、PDM、conda、pixi。截至 2026-09-24，基于各项目官方文档/changelog。R1 草稿，Poetry workspace/解析器、PDM 全局工具、CI 缓存待 R2 补证。

## 0. 一屏看懂

1. **PEP 751 `pylock.toml` 已是标准（2025-03-31 Final），但没有一个主流工具把它当默认锁文件**：uv 能读/导出（仍标 preview）[7]，pip 的 `pip lock`/`pip install -r pylock.toml` 都是 experimental 且无稳定时间表 [9][10]，PDM 可选切换为主格式但仍 opt-in [25]，Poetry 只是一个未排期的开放 issue [24]，conda/pixi 未提及。**新项目该继续用各工具自己的原生锁文件**（`uv.lock`/`poetry.lock`/`pdm.lock`），把 pylock.toml 当「跨工具交换格式」而非日常锁文件。
2. **Poetry 2.0（2025-01-05）确实改用了标准 `[project]` 表**，但 `[tool.poetry.*]` 没有退休：标准字段给通用元数据，`[tool.poetry]` 继续承载 Poetry 专属能力（私有源、path/git 依赖增强）[19][21]。
3. **只有 uv、PDM、pixi 有原生 workspace/monorepo（多包共享一把锁）**；Poetry 目前只有 `path` 依赖，不是真正 workspace；pip 完全没有这个概念，得自己拼 `-e`。
4. **只有 uv、PDM、pixi 能帮你下载/管理 Python 解释器本身**；pip、Poetry 都要求 Python 已经装好（Poetry 官方建议配 pyenv）；conda/pixi 把 Python 当普通包，装环境即装解释器。
5. **conda 系（conda/pixi）和 PyPI 系是两套不同的构建标准**：PyPI 系都遵守 PEP 517/518（可插拔构建后端）；conda 包用 `meta.yaml`/`conda-build`，官方文档不提 PEP 517。pixi 是唯一原生桥接两者的工具（`[pypi-dependencies]` 内嵌 uv 解析器）[41]。
6. **新项目速记**：纯 PyPI、要快、要一体化 → uv；已在 Poetry 生态、看重发布/私有源成熟度 → Poetry（等 workspace 补齐前多包项目仍需权衡）；需要严格可插拔构建后端或已有 PDM 投入 → PDM；需要非 Python 二进制依赖（CUDA/MKL/编译库）或多语言环境 → conda/pixi，新项目优先 pixi（原生锁文件+workspace，conda 无原生锁文件标准）。
7. **别再学 `pip freeze > requirements.txt`当锁文件**：pip 官方明确说这不是锁文件，也不做求解 [11]。
8. **PDM 曾经主推 PEP 582（`__pypackages__`，免 venv）**，但该 PEP 已被 Python 指导委员会拒绝，PDM 自 v2.5.0 起把它从宣传重点移除，现为实验性可选项，官方推荐改用 venv [29][30]——网上老教程如果讲 PEP 582，已经过时。

## 1. Taxonomy

**分类轴**：A = 包生态基座（PyPI/wheel 单一 vs 桥接 conda-forge 二进制生态）；B = 工具定位（all-in-one 项目管理器 vs 单一功能 point tool）。

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| PyPI 一体化项目管理器 | uv, Poetry, PDM | 自带锁文件 + venv 管理 + `pyproject.toml` 驱动全生命周期 |
| PyPI 传统组合工具 | pip(+pip-tools) | 无项目级锁文件/venv 概念，靠组合 venv/pyenv/pipx |
| conda 生态环境管理器 | conda, pixi | 装 conda channel 二进制包，能装非 Python 依赖；pixi 额外原生桥接 PyPI |

**维度**：D1 锁文件（含 PEP 751 支持）；D2 workspace/monorepo；D3 Python 版本管理；D4 构建后端；D5 解析器与速度；D6 私有源；D7 全局工具运行；D8 迁移路径；D9 生态定位。

## 2. 对照矩阵

| 实体 | D1 锁文件 | D2 Workspace | D3 Python版本 | D4 构建后端 |
|---|---|---|---|---|
| **uv** | `uv.lock`(TOML,跨平台单文件)[1]；pylock.toml 读0.12.0+/导出+hash 0.12.11+，preview[7] | `[tool.uv.workspace]`，member 共享单锁[1] | `uv python install/pin`，用 python-build-standalone 自动下载[2] | 默认 `uv_build`（`uv init`起自带）[3] |
| **pip** | 无原生锁；`pip freeze`≠锁文件[11]；`pip lock`(v25.1,exp)/`pip install -r pylock.toml`(v26.1,exp)输出/读取 pylock.toml[9][10] | 无概念，靠 `-e` 手工编排 | 官方明确「不管理 Python 版本」，`--python`只选目标环境[12] | 无默认后端，按 PEP 517/518 委托项目声明的后端[15] |
| **Poetry** | `poetry.lock`，`poetry install`时自动生成[20] | 未见原生支持，仅 `path`依赖(`file://`,不可移植)[21]；R2待确认是否有路线图 | 不下载解释器，`poetry env use`从已装版本里选，官方建议外部配 pyenv[22] | `poetry-core`（`poetry.core.masonry.api`）[20] |
| **PDM** | `pdm.lock`默认[25]；pylock 导出 v2.24.0、可选设为主格式(`pdm config lock.format pylock`) v2.25.0，opt-in[25][30] | 原生 `[tool.pdm.workspace]`，v2.28.0，**标记 experimental**，member 为隐式可编辑依赖[26] | `pdm python install`，同样用 python-build-standalone[27] | `pdm-backend`（pdm-pep517 后继，v2.5.0起默认），可换成任意后端[30] |
| **conda** | `environment.yml`不锁 build string/难跨平台；`conda list --explicit`精确但单平台；26.5+ 支持读 `conda-lock.yaml`/`pixi.lock`[31] | 官方概念页不含 workspace/monorepo[32] | `conda create -n env python=3.x`，Python 即普通包，多版本靠多环境[33] | 不是 PEP 517 体系；`conda-build`+`meta.yaml`[34] |
| **pixi** | `pixi.lock`(YAML)单文件锁多平台+多环境，`install/run/add`自动更新[39] | 原生 `[environments]`+`[feature]`组合[40] | conda-forge 渠道装解释器，`python="3.12.*"`精确指定[41] | `pixi-build`(preview)，多后端(python/rust/cmake)；PyPI 依赖内嵌 uv resolver[41] |

| 实体 | D5 解析/速度 | D6 私有源 | D7 全局工具 | D8 迁移 | D9 定位 |
|---|---|---|---|---|---|
| **uv** | Rust；Git 实现基于 Cargo；官方称比 pip 快 10-100x(warm cache)[8] | `[[tool.uv.index]]`，env var/URL内嵌/netrc/keyring[4] | `uvx`=`uv tool run`，隔离环境，pipx等价[5] | 官方仅有「pip→uv」指南，Poetry 等「暂未提供」[6] | 官方称可替代 pip/pip-tools/pipx/poetry/pyenv/twine/virtualenv[8] |
| **pip** | v20.3 起回溯算法；官方明说「优先正确性而非速度」，复杂树可能极慢[13] | `--index-url`/`--extra-index-url`；3种认证：URL内嵌/`.netrc`/keyring[14] | 自身无隔离；官方指向 PyPA 同门 pipx[18] | 无迁移指南；`pip lock`可从 requirements/pyproject 生成 pylock.toml[9] | 「the package installer for Python」，PyPA 维护，PEP 参照实现之一[22] |
| **Poetry** | R2 待补（未找到实现细节/官方速度说法） | `[[tool.poetry.source]]`，`priority`分级；`http-basic`/`pypi-token`认证[23] | 无 uvx 等价，`poetry run`要求项目内[20] | 未见独立迁移指南（R2 待确认） | 「dependency management and packaging made easy」[20] |
| **PDM** | `resolvelib`，版本持续升级，无官方速度基准[30] | `[[tool.pdm.source]]`，支持 env var 插值 URL、`pdm self add keyring`[28] | 未找到官方 pipx 等价机制（R1证据弱，R2 复核） | `pdm init/import` 自动识别 Pipfile/Poetry/Flit/pip/setuptools 并导入[27] | 强调后端自由选择、标准兼容 |
| **conda** | 23.10.0 起默认 `libmamba` solver 替代经典 solver；26.5.0 起插件化`BaseSolver`[35] | `.condarc`，可全局/环境级配置 channel[36] | `conda run -n env <cmd>` 免激活执行[31] | 官方guidance：能用 conda 装的先用 conda，再用 pip；避免混改，出问题重建环境[31] | 跨语言二进制包管理器，覆盖 CUDA/MKL 等；conda/conda-forge/mamba 联合，NumFOCUS 赞助[37] |
| **pixi** | Rust `rattler`库；有性能优化记录，无 vs conda classic 的量化对比[41] | conda 私有 channel(URL/prefix.dev/Quetz)+ PyPI 私有 index(`index=`字段)分开配，`pixi auth login`统一登录(token/OAuth/basic/S3)[41][42] | `pixi global install`，官方明确类比 pipx[43] | 官方同时提供「from conda/mamba」和「from Poetry」迁移指南，是 6 者中最全的[42] | 「built on the foundation of the conda ecosystem」，workspace-centric 而非只做环境[41] |

## 3. 变体与适配层

| 变体 | 相对参照系差在哪 |
|---|---|
| pixi vs conda | pixi 不是 conda 替代品，是建在 conda 生态之上的新工具：加了原生锁文件(`pixi.lock`)、workspace、以及通过内嵌 uv 原生装 PyPI 包（`[pypi-dependencies]`），conda 本身没有这三样 |
| Poetry `[project]` vs `[tool.poetry]` | 2.0 起标准字段(`[project]`)管元数据用于构建；`[tool.poetry]`不会消失，继续管私有源、增强型依赖（path/git/多约束）等标准表达不了的部分，无强制迁移时间表 |
| PEP 751 支持 vs 各自原生锁 | 没有工具把 pylock.toml 当第一公民；PDM 走得最远（可设为主格式但仍 opt-in），其余都是「能读/能导出」而非「默认使用」|

## 4. 用户需要知道的坑

- **迁移**：从 pip/requirements.txt → uv 有官方指南 [6]；从 Pipfile/Poetry/Flit/pip/setup.py → PDM，`pdm init`自动识别导入 [27]；从 conda/mamba 或 Poetry → pixi 有专门官方指南，是覆盖面最全的 [42]；Poetry 反向没有官方「从 setup.py 迁移」指南；pip 生态内部从 `requirements.txt` 升级到锁文件工具，官方也没有专门指南，只能靠 `pip lock` 直接生成。
- **私有源认证方式不通用**：uv 用 `[[tool.uv.index]]`+环境变量/keyring[4]；pip 用 `--index-url`+netrc/keyring[14]；Poetry 用 `[[tool.poetry.source]]`+`poetry config http-basic.*`[23]；PDM 用 `[[tool.pdm.source]]`+URL 内嵌变量[28]；conda 用 `.condarc` channel[36]；pixi 的 conda 源和 PyPI 源要分开配，登录用 `pixi auth login`[42]——换工具时私有源配置不能照抄。
- **conda + pip 混用有官方风险提示**：官方建议尽量先用 conda 装完，再用 pip 补纯 Python 包；出问题不要用 pip 反复修补，直接重建环境 [31]。
- **PEP 582 (`__pypackages__`) 已经过时**：曾是 PDM 卖点，现被 Python SC 拒绝，PDM 官方也降级为实验性可选、推荐用 venv [29]，看到教程讲这个要留意版本。
- **CI 缓存策略**：R1 未覆盖，待 R2 定向调研后补充。

## 5. 未决与置信度

- Poetry 是否有 workspace/monorepo 路线图：R1 只确认「文档未写」，未查 issue/RFC，**R2 待反证**。
- Poetry 依赖解析器实现细节与官方对速度的表态：**R1 空缺**。
- PDM 全局工具运行机制（pipx 等价物）：R1 证据是弱声称（无真实原文支持），**R2 待核实**。
- pixi 底层解析算法是否为 Resolvo、与 conda classic solver 的量化速度对比：官方未给数字，**低优先级空缺**。
- CI 缓存（用户点名疑点之一）：**R1 完全未覆盖**，R2 补。
- pip `pip lock`/`pip install -r pylock.toml` 何时转正：官方两处均标 experimental，**无时间表，非空缺，是明确结论**。

## 来源

uv: [1]https://docs.astral.sh/uv/concepts/projects/workspaces [2]…/guides/install-python [3]…/concepts/build-backend [4]…/concepts/indexes [5]…/guides/tools [6]…/guides/migration [7]https://github.com/astral-sh/uv/releases [8]https://github.com/astral-sh/uv
pip: [9]https://pip.pypa.io/en/stable/cli/pip_lock [10]…/cli/pip_install [11]…/cli/pip_freeze [12]…/topics/python-option [13]…/topics/dependency-resolution [14]…/topics/authentication [15]…/reference/build-system [16]https://peps.python.org/pep-0751 [17]https://pip-tools.readthedocs.io [18]https://pipx.pypa.io/latest
Poetry: [19]https://github.com/python-poetry/poetry/releases/tag/2.0.0 [20]https://python-poetry.org/docs/pyproject [21]…/docs/dependency-specification [22]…/docs/managing-environments [23]…/docs/repositories [24]https://github.com/python-poetry/poetry/issues/10356
PDM: [25]https://pdm-project.org/latest/usage/lockfile [26]…/usage/workspace [27]…/usage/project [28]…/usage/config [29]…/usage/pep582 [30]https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md
conda: [31]https://docs.conda.io/…/manage-environments.html [32]…/concepts/index.html [33]…/manage-python.html [34]https://docs.conda-build.io/en/latest/user-guide [35]https://github.com/conda/conda/blob/main/CHANGELOG.md [36]https://docs.conda.io/…/use-condarc.html [37]https://conda.org [38]https://github.com/conda/conda-lock
pixi: [39]https://raw.githubusercontent.com/prefix-dev/pixi/main/docs/workspace/lock_file.md [40]…/workspace/multi_environment.md [41]…/reference/pixi_manifest.md [42]…/switching_from/ [43]…/global_tools/introduction.md
