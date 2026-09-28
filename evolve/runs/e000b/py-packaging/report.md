# Python 包管理/项目管理工具怎么选（2026-09）
> 对比 uv、pip(+pip-tools)、Poetry、PDM、pixi、conda(+conda-lock) 在锁文件、workspace、Python 版本管理、构建后端上的官方文档说法，5 分钟建认知，按需查表核细节。终审版（经 34 条主张抽查核实），剩余边界见第 5 节。

## 0. 一屏看懂
- **新纯 Python 项目、要快要新**：选 **uv**。Rust 实现，原生 `[project]` 表，自带 Python 版本管理和 workspace，唯一有官方 GH Action 的一体化工具。
- **在 conda-forge 生态/需要非 Python 依赖（CUDA、编译器、C 库）**：选 **pixi**（`pixi.lock` 强制、单文件覆盖多平台多环境，还有真正的多子包 monorepo 机制[19]）或 **conda**（生态最老最广；26.5 版起实验性支持原生导出 `conda-lock.yaml`/兼容 `pixi.lock`，此前完全依赖第三方 conda-lock[18]）。
- **PEP 751（`pylock.toml`）现状**：**已定稿**（2025-03-31 Final，取代 PEP 665）[3]。规范本身支持单文件覆盖多环境，但**没有工具把它当主格式**：uv 0.6.15+ preliminary 支持导出/安装，`uv.lock` 仍是主格式[2]；pip 25.1 实验生成、26.1 实验安装但不支持 extras/dependency-groups[5]；PDM v2.25.0 opt-in 支持[11]；**Poetry 未支持**（issue #10356 无里程碑）[9]；**pixi 官方文档未提及**。conda 生态完全不在此规范讨论范围内[3]。
- **Poetry 2 的 `[project]` 表**：**没有完全切换**。推荐新项目用标准 `project.dependencies`，但显式多源、依赖组、相对路径本地依赖仍要写 `[tool.poetry.dependencies]`，两表并存[7][8]。
- **workspace/monorepo**：uv、PDM、pixi 都有正式多包机制。PDM 是 2026-06 才加的实验特性[11]；pixi 的多子包发布机制（根 `[workspace]`+子包 `[package]`+`pixi publish` 按序发布）已随 **v0.75.0**（2026-07-29）进入稳定版，当前最新稳定版 v0.81.0（2026-09-15）仍保留[19]。Poetry 只有不便携的 path dependencies[7]；pip/conda 无此概念。
- **私有源要小心默认策略不同**：pip 默认合并所有 index 选最优版本，容易被"依赖混淆"攻击；uv 默认 `first-index`（先找到哪个 index 有就用哪个，更安全），但**内部 index 缺凭证时会静默回退到公共 PyPI**，是已知安全隐患而非文档特性[20][21]。
- **Python 解释器能否自装**：uv/PDM/pixi/conda 都能自己下载解释器；**Poetry 明确不会**（BYOP）[7]；pip 不涉及。

## 1. Taxonomy
按「服务的生态位」分三族：

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| A. PyPI 专用・一体化 | uv, Poetry, PDM | 自带元数据模型+锁文件+venv(+部分Python版本)，一个命令管全流程 |
| B. PyPI 专用・拼装式 | pip (+pip-tools) | 不内置锁文件/项目模型，靠用户自拼 venv/pyenv/pip-tools |
| C. 跨语言・conda-forge | pixi, conda(+conda-lock) | 能装非 Python 二进制依赖(CUDA/编译器/C库)，不止管 wheel |

维度：D1 元数据来源｜D2 原生锁文件格式｜D3 PEP751 支持｜D4 能否自管 Python 解释器｜D5 venv 自动化程度｜D6 workspace/monorepo｜D7 默认构建后端与可插拔性｜D8 非Python依赖｜D9 私有源认证｜D10 官方CI缓存｜D11 迁移路径。

## 2. 对照矩阵

**元数据 / 锁文件 / PEP751**

| 工具 | D1 元数据 | D2 锁文件 | D3 PEP751 |
|---|---|---|---|
| uv | 原生`[project]`[1] | `uv.lock` TOML，跨平台通用[1] | preliminary，导出/compile/install均可[2] |
| pip | 委托构建后端读取[4] | 无原生（pip-tools→`requirements.txt`）[6] | `pip lock`(25.1)实验生成，`install -r pylock.toml`(26.1)实验安装，无extras[5] |
| Poetry | 混合：推荐`[project]`+保留`[tool.poetry.dependencies]`[7] | `poetry.lock`自定义TOML[7] | 不支持，issue #10356无里程碑[9] |
| PDM | 原生，PEP621起家[10] | `pdm.lock` TOML[10] | 实验opt-in，v2.25.0(2025-06)[11] |
| pixi | `pixi.toml`或`pyproject.toml`+`[tool.pixi]`[12] | `pixi.lock` YAML，单文件覆盖全平台全环境[12] | ∅ 官方未提及 |
| conda | — | `environment.yml`仅声明式；26.5+实验性原生导出`conda-lock.yaml`/兼容`pixi.lock`[18]，此前靠conda-lock[15] | — |

**Python 版本 / venv / workspace / 构建后端**

| 工具 | D4 Python版本 | D5 venv | D6 workspace | D7 构建后端 |
|---|---|---|---|---|
| uv | `uv python install`自动下载[1] | 自动建`.venv`[1] | `[tool.uv.workspace]`+`members`glob[1] | `uv_build`，可换hatchling/pdm-backend/setuptools/maturin等[1] |
| pip | 不涉及 | 手动`venv`[4] | — | 委托任意PEP517后端[4] |
| Poetry | 不自动装，需自带BYOP[7] | 自动建，默认全局缓存[7] | 仅path dependencies，不便携[7] | 固定`poetry-core`[7] |
| PDM | `pdm python install`自动下载[10] | 项目/集中位置可配[10] | 实验特性，v2.28.0(2026-06)[11] | `pdm-backend`，可自由更换[10] |
| pixi | Python作为conda依赖自动装[12] | `.pixi/envs/`[13] | 根`[workspace]`+子包`[package]`，`{workspace=true}`源依赖，`pixi publish`按序发布——**稳定版功能，v0.75.0(2026-07-29)起**[19] | 无`[build-system]`默认setuptools，`init --format pyproject`默认hatchling[19] |
| conda | `python=3.x`当包装[14] | `/envs/`或`--prefix`[14] | — | — |

**非 Python 依赖 / 私有源 / CI 缓存 / 迁移**

| 工具 | D8 非Python依赖 | D9 私有源认证 | D10 CI缓存 | D11 迁移指南 |
|---|---|---|---|---|
| uv | 不支持 | URL嵌入/netrc/凭证store/keyring[1]；**index-strategy默认first-index，缺凭证会回退公共PyPI**[20][21] | `astral-sh/setup-uv`官方action[1] | 仅pip→uv；**明确wontfix不支持读poetry.lock/Pipfile.lock**(issue #1804)[22] |
| pip | 不支持 | URL嵌入/.netrc/keyring[4]；默认合并所有index选最优版本[20] | `actions/setup-python`内置cache参数[17] | — |
| Poetry | 不支持 | `source add`+`http-basic`+keyring+环境变量[7] | ∅ 确认无官方action，仅社区方案[7] | 无专门指南 |
| PDM | 不支持 | keyring自动存+URL+mTLS[10] | 官方`pdm-project/setup-pdm`[10] | `pdm import`支持Pipfile/Poetry/flit/requirements.txt[10] |
| pixi | 支持，conda-forge 3万+含CUDA/编译器[12] | OAuth/OIDC/HTTP/S3/OS原生密钥链[12] | 官方`prefix-dev/setup-pixi`，lock哈希做key[12] | 未查 |
| conda | 支持，核心卖点MKL/CUDA/编译器链[14] | token/环境变量展开/插件化认证[14] | `setup-miniconda`(incubator非core team)[16] | 无专门指南，仅pip互操作讨论[14] |

## 3. 标准化进度：谁离 PEP621/PEP751 有多远
PEP621 的`[project]`表本身没有歧义，差异在"够不够用"：PDM/uv 从一开始就够用，直接原生；Poetry 因为显式依赖源、依赖组、相对路径本地依赖这些标准表达不了的能力，两表并存，`[tool.poetry]`不会消失[7][8]。

PEP751 定位是"锁文件的 wheel 格式"：文件名固定`pylock.toml`或匹配`pylock.<name>.toml`，规范内置`environments`字段理论上支持单文件覆盖多平台多环境（PDM/Poetry/uv"尝试"支持），并**明确不覆盖 conda 等非 PyPI 生态**[3]。但现实是没有工具把它当主格式——原生锁（uv.lock/pdm.lock/poetry.lock/pixi.lock）仍是主力，pylock.toml 只是导出/交换格式；pip 是唯一"原生就是 pylock"的例外，但装的那一半还没追上 extras/dependency-groups[3][5]。

## 4. 用户需要知道的坑
- **私有源解析策略不同，默认行为有安全含义**：pip 跨所有配置的 index 合并候选版本选"最优"，历史上是依赖混淆（dependency confusion）攻击的成因之一；uv 默认`--index-strategy first-index`，只认第一个含该包的 index[20]。但**uv 忘记给内部 index 配凭证时会静默回退到公共 PyPI 装同名包，不报错不警告**，已有用户实测踩坑（issue #9429），迁移到 uv 时务必显式检查凭证配置[21]。
- **旧锁文件不能直接喂给 uv**：uv 官方对"支持直接安装 poetry.lock/Pipfile.lock"的 feature request 明确标记 **wontfix**，从 Poetry/Pipenv 迁移必须重新 `uv lock` 完整 resolve，不是文件转换[22]。
- **CI 缓存 key 精度不够会装到不兼容的 wheel**：GitHub Actions 上 Ubuntu 20.04 编译的 wheel 在 22.04 不一定能跑，若 cache key 只含 OS 类型+Python 版本、不含 OS 小版本号，跨 runner 镜像升级时会静默复用坏缓存[23]；pip 自己的缓存机制也假设构建结果确定，可能把一处环境编译的可选 C 扩展 wheel 复用到不具备编译条件的环境[24]。
- **Poetry 迁移到标准表不是免费的**：`[project].dependencies`只接受PEP508字符串和绝对路径，本地相对路径依赖、显式多源还得留在`[tool.poetry.dependencies]`，两套语法混用容易搞混哪个字段该写哪张表[7]。
- **conda 的"官方" CI action 不是核心团队维护**：`setup-miniconda`在`conda-incubator`组织下，缓存要求`use-only-tar-bz2: true`否则不生效[16]；Poetry 同样没有`python-poetry`组织下的官方 action，只有社区维护的几个替代品[7]。

## 5. 未决与置信度
终审对正文抽查 34 条具体主张：30 条 supported、2 条 weak、1 条 unsupported（已改写/删除）、0 条 contradicted。以下是仍值得注意的边界：
- **pip 25.1/26.1 的 pylock.toml 细节**（生成/安装/extras限制）证据强度为 weak——版本号和"不支持extras"这条限制本身有官方 CLI reference 支撑，但部分措辞来自 pip 最新开发文档而非稳定版文档，建议读者以自己安装的 pip 版本 `pip lock --help` 输出为准。
- **PDM workspace（v2.28.0, 2026-06-23）**来自官方 CHANGELOG，未做第二来源交叉验证，但 CHANGELOG 本身是项目一手权威记录，置信度仍较高。
- pixi 的 D11（迁移指南）R1/R2 均未覆盖，优先级低，留空。
- uv"内部 index 缺凭证回退公共 PyPI"是否已有官方修复计划（issue #12362）未确认，只确认问题存在，见第 4 节。

## 来源
[1] uv 官方文档 — https://docs.astral.sh/uv/
[2] uv 0.6.15 release notes — https://github.com/astral-sh/uv/releases/tag/0.6.15
[3] PEP 751 — https://peps.python.org/pep-0751/
[4] pip 官方文档 — https://pip.pypa.io/en/stable/
[5] pip lock CLI reference — https://pip.pypa.io/en/stable/cli/pip_lock/
[6] pip-tools 文档 — https://pip-tools.readthedocs.io/
[7] Poetry 官方文档 — https://python-poetry.org/docs/
[8] Poetry 2.0.0 发布公告 — https://python-poetry.org/blog/announcing-poetry-2.0.0/
[9] Poetry PEP751 issue #10356 — https://github.com/python-poetry/poetry/issues/10356
[10] PDM 官方文档 — https://pdm-project.org/
[11] PDM CHANGELOG — https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md
[12] pixi 官方文档 — https://pixi.prefix.dev/latest/
[13] pixi GitHub 仓库 — https://github.com/prefix-dev/pixi
[14] conda 官方文档 — https://docs.conda.io/projects/conda/en/stable/
[15] conda-lock GitHub — https://github.com/conda/conda-lock
[16] setup-miniconda README — https://github.com/conda-incubator/setup-miniconda
[17] actions/setup-python — https://github.com/actions/setup-python
[18] conda CHANGELOG（26.5.0，PR #15927/#16086）— https://github.com/conda/conda/blob/main/CHANGELOG.md
[19] pixi workspace 文档 + v0.75.0 release notes — https://pixi.prefix.dev/latest/build/workspace/ , https://github.com/prefix-dev/pixi/releases/tag/v0.75.0
[20] uv / pip 兼容性文档（index-strategy）— https://docs.astral.sh/uv/pip/compatibility/
[21] uv issue #9429（index 回退隐患）— https://github.com/astral-sh/uv/issues/9429
[22] uv issue #1804（不支持读取 poetry.lock，wontfix）— https://github.com/astral-sh/uv/issues/1804
[23] actions/setup-python issue #432（缓存 key 缺 OS 小版本号）— https://github.com/actions/setup-python/issues/432
[24] pip 缓存文档 — https://pip.pypa.io/en/stable/topics/caching/
