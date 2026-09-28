# Python 包管理/项目管理工具怎么选（2026-09）
> 对比 uv、pip(+pip-tools)、Poetry、PDM、pixi、conda(+conda-lock) 在锁文件、workspace、Python 版本管理、构建后端上的官方文档说法，5 分钟建认知，按需查表核细节。R1 收束版，❓/⚔ 见第 5 节，会在后续轮次收窄。

## 0. 一屏看懂
- **新纯 Python 项目、要快要新**：选 **uv**。速度最快，原生 `[project]` 表，自带 Python 版本管理和 workspace，是唯一有官方 GH Action 的一体化工具。
- **已在 conda-forge 生态/需要非 Python 依赖（CUDA、编译器、C 库）**：选 **pixi**（`pixi.lock` 强制、人类可读、单文件覆盖多平台多环境[12]）或 **conda**（生态最老最广，但本身没有强一致锁文件，需搭配 conda-lock[15]）。
- **PEP 751（`pylock.toml`）现状**：**已定稿**，2025-03-31 转正[3]。**uv** 自 0.6.15（2025-04-22）起可导出/编译/安装 pylock.toml，标注 preliminary，`uv.lock` 仍是主格式[2]。**pip** 25.1（2025-04）加了实验性 `pip lock` 生成，26.1（2026-04）加了实验性 `pip install -r pylock.toml`，但还不支持 extras/dependency-groups[5]。**PDM** v2.24–2.25（2025-04~06）实验支持，需手动开启[11]。**Poetry** 未支持，issue #10356 未分派无里程碑[9]。**pixi** 官方文档未提及。没有一个工具把 pylock.toml 当默认格式——都是「自己的原生锁为主，pylock 为导出/互操作选项」。
- **Poetry 2 的 `[project]` 表**：**没有完全切换**。2.0.0（2025-01-05）建议新项目用标准 `project.dependencies`，但显式多源、依赖组、相对路径本地依赖这些 Poetry 专属能力仍要写在 `[tool.poetry.dependencies]`，两表并存，官方原话是"should consider using"而非强制替换[7][8]。
- **workspace/monorepo 能力差距大**：uv、PDM 有正式 workspace（PDM 的是 2026-06 才加的实验特性）；Poetry 只有不便携的 path dependencies[7]；pip/conda 无此概念；pixi 的「workspace」是否等于多子包 monorepo 待确认（见第 5 节）。
- **Python 解释器能否自装**：uv/PDM/pixi/conda 都能自己下载解释器；**Poetry 明确不会**（BYOP，需自带）[7]；pip 不涉及。

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
| uv | 原生 `[project]`[1] | `uv.lock` TOML，跨平台通用[1] | preliminary，导出/compile/install 均可[2] |
| pip | 委托构建后端读取[4] | 无原生（pip-tools→`requirements.txt`）[6] | `pip lock`(25.1)实验生成，`install -r pylock.toml`(26.1)实验安装，无 extras[5] |
| Poetry | 混合：推荐`[project]`+保留`[tool.poetry.dependencies]`[7] | `poetry.lock` 自定义TOML[7] | 不支持，issue #10356 无里程碑[9] |
| PDM | 原生，PEP621 起家[10] | `pdm.lock` TOML[10] | 实验opt-in，v2.25.0(2025-06)[11] |
| pixi | `pixi.toml`或`pyproject.toml`+`[tool.pixi]`[12] | `pixi.lock` YAML，单文件覆盖全平台全环境[12] | ∅ 官方文档未提及 |
| conda | — | `environment.yml`仅声明式；精确锁靠conda-lock[15]；「原生也能导出」待核[⚔§5] | — |

**Python 版本 / venv / workspace / 构建后端**

| 工具 | D4 Python版本 | D5 venv | D6 workspace | D7 构建后端 |
|---|---|---|---|---|
| uv | `uv python install`自动下载[1] | 自动建`.venv`[1] | `[tool.uv.workspace]`+`members` glob[1] | `uv_build`，可换hatchling/pdm-backend/setuptools/maturin等[1] |
| pip | 不涉及 | 手动`venv`[4] | — | 委托任意 PEP517 后端[4] |
| Poetry | 不自动装，需自带BYOP[7] | 自动建，默认全局缓存[7] | 仅path dependencies，不便携[7] | 固定`poetry-core`[7] |
| PDM | `pdm python install`自动下载[10] | 项目/集中位置可配[10] | 实验特性，v2.28.0(2026-06)[11] | `pdm-backend`，可自由更换[10] |
| pixi | Python作为conda依赖自动装[12] | `.pixi/envs/`[13] | 有「workspace」概念，是否=多子包待核[⚔§5] | 不强调，沿用标准PEP517 |
| conda | `python=3.x`当包装[14] | `/envs/`或`--prefix`[14] | — | — |

**非 Python 依赖 / 私有源 / CI 缓存 / 迁移**

| 工具 | D8 非Python依赖 | D9 私有源认证 | D10 CI缓存 | D11 迁移指南 |
|---|---|---|---|---|
| uv | 不支持 | URL嵌入/netrc/凭证store/keyring[1] | `astral-sh/setup-uv`官方action[1] | 仅pip→uv，Poetry/PDM缺失(issue #5200)[1] |
| pip | 不支持 | URL嵌入/.netrc/keyring[4] | `actions/setup-python`内置cache参数[17] | — |
| Poetry | 不支持 | `source add`+`http-basic`+keyring+环境变量[7] | 无官方action，仅配置项[7] | 无专门指南 |
| PDM | 不支持 | keyring自动存+URL+mTLS[10] | 官方`pdm-project/setup-pdm`[10] | `pdm import`支持Pipfile/Poetry/flit/requirements.txt[10] |
| pixi | 支持，conda-forge 3万+包含CUDA/编译器[12] | OAuth/OIDC/HTTP/S3/OS原生密钥链[12] | 官方`prefix-dev/setup-pixi`，lock哈希做key[12] | 未查 |
| conda | 支持，核心卖点MKL/CUDA/编译器链[14] | token/环境变量展开/插件化认证[14] | `setup-miniconda`(incubator，非core team)[16] | 无专门指南，仅pip互操作讨论[14] |

## 3. 标准化进度：谁离 PEP621/PEP751 有多远
PEP621 的 `[project]` 表本身没有歧义，差异在"够不够用"：PDM/uv 从一开始就够用，直接原生；Poetry 因为显式依赖源、依赖组、相对路径本地依赖这些标准表达不了的能力，两表并存，`[tool.poetry]` 不会消失[7][8]。

PEP751/`pylock.toml` 定位是"锁文件的 wheel 格式"——工具无关、可互换，但**没有工具把它当主格式**：原生锁（uv.lock/pdm.lock/poetry.lock/pixi.lock）仍是主力，pylock.toml 只是导出/交换格式；pip 是唯一"原生就是 pylock"的例外，但装的那一半还没追上 extras/dependency-groups[3][5]。conda 生态（pixi/conda）目前完全不在 PEP751 讨论范围——它们的锁文件要覆盖非 Python 的 conda 包，pylock.toml 规范不了这部分。

## 4. 用户需要知道的坑
- **Poetry 迁移到标准表不是免费的**：`[project].dependencies` 只接受 PEP508 字符串和绝对路径，本地相对路径依赖、显式多源还得留在 `[tool.poetry.dependencies]`，两套语法混用容易搞混哪个字段该写哪张表[7]。
- **pip 的 pylock 支持还不完整**：25.1 能生成、26.1 能装，但装的那条路径不支持 extras 和 dependency-groups，生产锁文件如果用了这两个特性，导出后可能装不全[5]。
- **conda 官方 CI action 不是核心团队维护**：`setup-miniconda` 在 `conda-incubator` 组织下，且缓存要求 `use-only-tar-bz2: true` 否则不生效[16]。
- **Poetry 目前没有官方 CI 缓存 action**，社区做法是自己 `actions/cache` 键 `~/.cache/pypoetry`[7]。
- 更多迁移/私有源/CI 细节待下一轮专项调研补充。

## 5. 未决与置信度
- **⚔ conda D2**：有来源称「conda 26.5+ 原生支持导出跨平台精确锁文件」，与常见认知（conda 本身无锁、靠 conda-lock）不符，疑似把 `conda env export`/`conda list --export` 旧功能误述为新特性，**未采信进第 0/2 节结论**，待核实原句与版本号。
- **❓ pixi D6**：pixi 文档「workspace」是否等于「一仓库多个可互引用子包」（类似 uv workspace），还是仅「项目清单根」的新称呼，R1 未查清。
- **⚠ 弱来源**：Poetry/conda 的 CI 缓存（D10）、迁移指南（D11）目前只有二手或间接证据，未升级为确定结论。
- PDM workspace（v2.28.0, 2026-06-23）是六者中最新加入的 workspace 能力，来自官方 CHANGELOG，待交叉验证。
- pixi 的 D7（构建后端）、D11（迁移指南）R1 未覆盖，留空。

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
