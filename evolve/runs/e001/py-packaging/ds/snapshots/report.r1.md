# Python 包管理/项目管理工具怎么选（2026-09）

> 对比 uv、pip、Poetry、PDM、pixi、conda 六个工具在锁文件、workspace、Python 版本管理、构建后端上的官方文档说法；信息截至 2026-09-24，版本号以官方 changelog 为准。先看 §0 建立认知，再按需查 §2 矩阵和 §4 的坑。

## 0. 一屏看懂

1. **两个生态，先按这条分**：pip/Poetry/PDM/uv 只管 PyPI 包；conda/pixi 还能管非 Python 的系统/编译依赖。要装 CUDA、编译好的科学计算库，选 conda 系；纯 Python 项目，选 PyPI 原生工具。[§1]
2. **PEP 751（`pylock.toml`）已定稿为 Final（2025-03-31），但没有工具把它当"唯一默认"锁文件**：pip 25.1 用实验性 `pip lock` 命令直接产出它；uv/Poetry 只支持**导出**成它（主力仍是 `uv.lock`/`poetry.lock`）；PDM 可以把它设为替代锁格式（仍标"实验性"）；conda/pixi 官方文档未提及与它的关系。[§3]
3. **Poetry 2.0 起才有标准 `[project]` 表**：核心元数据改用 PEP 621 `[project]`，旧 `[tool.poetry]` 字段多数 deprecated；但 source/group/package-mode 等 Poetry 专有能力还留在 `[tool.poetry]`，没有消失。[§3]
4. **原生 workspace 三家有，两家没有**：uv、PDM(2.28+，实验性)、pixi 都有官方 workspace 声明并共享单一锁文件；pip 完全没有；Poetry 只能靠 path dependency 手动拼。[§2]
5. **只有 uv 把"装 Python 解释器"内置了**：`uv python install/pin` 直接下载解释器；PDM 有 `pdm python install`；Poetry 要靠外部 pyenv；pip 完全不管；conda/pixi 把 Python 当普通包装进环境。[§2]
6. **构建后端各家不同，但都是 PEP 517 后端，可以互通**：pip 默认回退 setuptools，Poetry 用 poetry-core，PDM 用 pdm-backend，uv 用自己的 uv_build（0.12+ 新项目默认）。[§2]
7. **操作细节的官方完成度差很多**：`pdm import` 官方支持从 5 种旧工具迁移，覆盖面最广；pixi 官方目前**不支持私有 PyPI 仓库认证**；Poetry、conda 官方文档都没给 CI 缓存策略。选型前建议对着 §4 核对你在意的那一条。[§4]

## 1. Taxonomy

**分类轴：这个工具的"世界"里有没有非 Python 的东西？**

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| PyPI 原生 | pip, Poetry, PDM, uv | 只装 PyPI／兼容 index 的包，围绕标准 pyproject.toml 工作 |
| conda 生态 | conda, pixi | 包可以是任意语言的编译产物；环境=系统级依赖清单，Python 只是其中一个包 |

PyPI 原生内部再分：**无内建锁**的 pip（要配 pip-tools/venv/pyenv 才等价于别家的开箱功能）vs **锁文件+解析器+多合一**的 Poetry/PDM/uv。conda 生态内部：**经典档** conda（环境=唯一单位，2012 年至今）vs **新锐档** pixi（2023 年后、Rust 重写，原生 workspace，conda+PyPI 双解析器）。

本文矩阵维度（§2）：锁文件、解析器、Python 版本管理、构建后端、workspace——回答"具体怎么做"；私有源/CI缓存/迁移路径见 §4。

## 2. 对照矩阵

| | uv | pip | Poetry | PDM | pixi | conda |
|---|---|---|---|---|---|---|
| **锁文件** | `uv.lock`(TOML，PubGrub 解析结果) | 无原生锁；`requirements.txt`+`pip freeze`/`--require-hashes`（PEP751 见§3） | `poetry.lock`(专有格式) | `pdm.lock`(默认格式) | `pixi.lock`(conda+PyPI 合一) | 无官方锁；`conda-lock`(第三方)/`conda list --explicit` |
| **解析器** | PubGrub(自研，Rust) | "New resolver"(20.3+，回溯) | Mixology(PubGrub 的 Python 实现) | resolvelib(回溯) | resolvo(conda 侧)+uv 的 PubGrub(PyPI 侧)，双解析器 | libmamba(23.10+ 默认，SAT 式)，旧版 classic(pycosat) |
| **Python 版本管理** | `uv python install/pin`，内置下载解释器 | 无，交给 venv/pyenv | `poetry env use`，需外部 pyenv | `pdm python install/use` | Python 作为 conda 包声明，随环境切换 | Python 作为 conda 包，`conda create -n env python=3.x` |
| **构建后端** | `uv_build`(PEP517，0.12+ 新项目默认) | 前端角色；无声明时退回 `setuptools.build_meta:__legacy__` | `poetry-core`(`poetry.core.masonry.api`) | `pdm-backend`(原 pdm-pep517) | `pixi-build-python`；无声明时退回 setuptools | `conda-build`+`meta.yaml`，自成体系，是否算 PEP517 后端存疑(§5) |
| **Workspace** | `[tool.uv.workspace]`，members/exclude glob，单一锁文件 | 无原生概念，只有 `-e` 可编辑安装 | 无原生概念，靠 path dependency + `develop=true` | `[tool.pdm.workspace]`(v2.28+，实验性) | `[workspace]`(2024 年从`[project]`改名)+`[workspace.dependencies]` | 无，模型是多个独立 environment |

来源：uv[2][3][5]，pip[6][7]，Poetry[8][10]，PDM[11][12]，pixi[13]，conda[15][16]

## 3. 标准适配层：PEP 621 / 751 落地程度

| 标准 | 定义什么 | 采用最彻底 | 部分/仅导出 | 不适用 |
|---|---|---|---|---|
| PEP 621 `[project]` | 项目元数据标准表 | uv、PDM（原生）；**Poetry 2.0 起**支持，旧字段部分 deprecated，但 source/group/package-mode 等专有能力仍在 `[tool.poetry]` | pip（读取但官方未细列完整度） | conda（environment.yml 走独立的 CEP 24 标准，官方未提二者关联） |
| PEP 751 `pylock.toml`（2025-03-31 定为 Final） | 标准锁文件格式 | PDM（可设为默认锁格式，仍"实验性"） | uv（仅 `uv export --format pylock.toml`，可导入但非原生生成）；Poetry（2.3.0+ 仅导出，需 poetry-plugin-export≥1.10）；pip（25.1+ `pip lock` 命令直接产出，标"实验性"） | conda/pixi（官方未提及；pixi.lock 覆盖 conda 包，超出 PEP751 范围） |

**回答两个点名疑点**：① PEP 751 已是 Final 状态的标准，但目前没有工具把 `pylock.toml` 当唯一/默认锁文件——pip 用它生成新锁、PDM 可选用、uv/Poetry 仅支持导出，各家原生锁文件都还在用。② Poetry 2.0 确实改用标准 `[project]` 表承载核心元数据，但 `[tool.poetry]` 没有消失，Poetry 的专有功能（依赖分组、source 配置等）还在那张表里，两个表通常搭配使用。[1][8][9][11]

## 4. 用户需要知道的坑

**迁移**：PDM 的 `pdm import` 官方支持读 Pipenv Pipfile、Poetry 区块、Flit 区块、pip requirements.txt、setuptools setup.py——五种里最全。pixi 有官方 Poetry→pixi 指南（含依赖语法对照：Poetry `^1.2.3` → pixi `>=1.2.3,<2.0.0`），也能 `pixi init --import env.yml` 从 conda 环境迁入。uv 官方migration文档只完成"pip → uv projects"一篇，从 Poetry/pip-tools/pyenv/virtualenv 迁移排在 GitHub #5200，还没发布。Poetry 只有 1.x→2.x 的 `poetry config --migrate`，没有官方 pip→Poetry 指南。conda 没有分步迁移文档，只说"conda 能做 pip/virtualenv 做的事"。[4][9][11][14][15]

**CI 缓存**：官方有现成 action 且默认带缓存的：uv(`astral-sh/setup-uv`)、pixi(`prefix-dev/setup-pixi`，pixi.lock 存在即默认启用)、PDM(`pdm-project/setup-pdm`，以 pdm.lock 算缓存 key)。pip 没有专属 action，但文档给了 `pip cache dir` 且建议保持缓存开启。Poetry、conda 官方文档都没写 CI 缓存策略；conda 常见做法是社区（非官方）的 `conda-incubator/setup-miniconda`。[2][6][11][13][18]

**私有源**：pip/uv/Poetry/PDM 都支持 `.netrc` + keyring + 环境变量令牌这套组合；uv 额外有专门的 `uv auth` CLI，索引默认按 `first-index` 策略防依赖混淆攻击。conda 走 `.condarc` 的 channel 认证（token/OAuth/Basic/S3）。**pixi 目前官方明确不支持私有 PyPI 仓库认证**（只有 keyring/.netrc，没有私有 index 机制）——项目依赖私有 PyPI 包时，这是选 pixi 前要注意的限制。[2][6][10][11][13][15]

## 5. 未决与置信度

- uv 最早支持 PEP 751 导出的版本号存在冲突（一手 CHANGELOG 与二手搜索结果对不上），核实中，不影响"uv 仅支持导出、非原生生成"这一结论。
- pip 能否直接 `install` 一份 pylock.toml（而不只是用 `pip lock` 生成），具体版本待确认。
- conda-build 是否真正实现了 PEP 517 后端接口、还是仅用 meta.yaml 模板读取 pyproject.toml 元数据，官方表述有歧义，本文采用更保守的"自成体系"表述。
- pip 对 PEP 621 `[project]` 表字段的完整支持程度，官方文档未系统列出。
- Poetry、conda 的官方 CI 缓存策略：确认为官方文档未覆盖（非本文遗漏）。

## 来源
[1] PEP 751 — https://peps.python.org/pep-0751/
[2] uv 官方文档 — https://docs.astral.sh/uv/
[3] uv CHANGELOG — https://github.com/astral-sh/uv/blob/main/CHANGELOG.md
[4] uv 迁移指南 — https://docs.astral.sh/uv/guides/migration/
[5] uv workspace/export/index concepts — https://docs.astral.sh/uv/concepts/projects/export/ , https://docs.astral.sh/uv/concepts/indexes/
[6] pip 官方文档 — https://pip.pypa.io/en/stable/
[7] pip NEWS.rst — https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst
[8] Poetry 2.0 发布公告 — https://python-poetry.org/blog/announcing-poetry-2.0.0/
[9] Poetry 2.3.0 发布公告（pylock 导出） — https://python-poetry.org/blog/announcing-poetry-2.3.0/
[10] Poetry 官方文档 — https://python-poetry.org/docs/main/pyproject/ , https://python-poetry.org/docs/main/repositories/
[11] PDM 官方文档 — https://pdm-project.org/latest/usage/lockfile/ , https://pdm-project.org/latest/reference/pep621/
[12] PDM-Backend — https://backend.pdm-project.org/
[13] pixi 官方文档 — https://pixi.prefix.dev/latest/
[14] pixi Poetry 迁移指南 — https://pixi.prefix.dev/latest/switching_from/poetry/
[15] conda 官方文档 — https://docs.conda.io , https://conda.org
[16] conda 23.10 release notes（libmamba 默认求解器） — https://docs.conda.io/projects/conda/en/23.10.x/release-notes.html
[17] conda-lock — https://github.com/conda/conda-lock
[18] CI actions — https://github.com/astral-sh/setup-uv , https://github.com/pdm-project/setup-pdm , https://github.com/marketplace/actions/setup-pixi , https://github.com/conda-incubator/setup-miniconda
