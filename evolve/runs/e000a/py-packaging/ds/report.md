# Python 包管理/项目管理工具怎么选（2026-09）

> 对比 pip、uv、Poetry、PDM、pixi、conda 在锁文件、workspace、Python 版本管理、构建后端上的现状，帮你几分钟内建立认知、决定新项目选谁。截至 2026-09-24。先看「一屏看懂」，字段名/命令查第 2 节矩阵。

## 0. 一屏看懂

1. **PEP 751（`pylock.toml`）已是正式标准**（2025-03-31 Final）。pip 支持最完整：25.1 起能生成（`pip lock`，单平台），**26.1 起能安装读取**（`pip install -r pylock.toml`），26.2 进一步增强（`--uploaded-prior-to`、`--only-final`），均已被官方 NEWS.rst 确认 [2][3][38]。uv 仍在 preview 阶段（导出+校验，0.12.11+/0.12.17+）[9]。Poetry/PDM 只能"导出"到它，各自主格式不变 [18][23]。pixi 未发布但有两个在推进的官方 issue（设计+导出）[42][43]。conda 生态没有动作。**没有工具把它设为默认/唯一锁文件格式。**
2. **Poetry 2.0（2025-01-05）已改用标准 `[project]` 表**（PEP 621），`[tool.poetry]` 只保留依赖分组等专属配置，迁移渐进、向后兼容，无一键迁移命令 [16][17]。
3. 六个工具分两大阵营：pip/uv/Poetry/PDM 只管 **PyPI 生态**；pixi/conda 是**跨语言环境管理器**，能装 CUDA、编译库等非 Python 依赖，但要走 conda channel。先看你是否需要非 Python 二进制依赖。
4. 新一代工具（uv、pixi）都是 Rust 实现，比上一代快一个数量级（uv 号称比 pip 快 10-100x；pixi 号称比 conda 快 10x）[8][32]。
5. 选型经验法则：纯 Python/PyPI 项目 → **uv**（唯一同时替代 pip+pyenv+venv 且自带 workspace 的工具）；已有 Poetry/PDM 团队习惯 → 无需迁移；需要 conda 二进制生态（科学计算/CUDA）→ 新项目用 **pixi**，存量/重度 conda-forge 依赖用 **conda**。
6. `[project]` 表已成事实起点：uv、PDM 从一开始就用，Poetry 2.0 补齐；pip 不需要它，pixi 用 `[tool.pixi.project]` 包一层。
7. Workspace 能力集中在新一代：uv、PDM(实验性 v2.28+)、pixi 有原生 workspace；Poetry、conda 没有。
8. **CI 缓存官方投入不对等**：uv、pixi、PDM 都有官方维护的 GitHub Action（`setup-uv`/`setup-pixi`/`setup-pdm`）；**Poetry 官方没有**，只给了缓存目录路径 [39][40]。conda 免费层还有个容易忽略的坑：**官方条款写明 200+ 员工/合同工的组织需付费 Business license** [44]。

## 1. Taxonomy

**轴 A：解决什么层的问题**

| 家族 | 成员 | 共同点 |
|---|---|---|
| (a) 底层安装器 | pip | 只装包，不管项目生命周期/Python 版本/venv |
| (b) PyPI 项目管理器 | uv、Poetry、PDM | 管依赖+锁+venv+构建；新一代还管 Python 版本自身；只认 PyPI/wheel |
| (c) 跨语言环境管理器 | pixi、conda | 经 conda channel 装任意语言/二进制；pixi 正向 (b) 靠拢(加了workspace、可选pyproject.toml) |

**轴 B：实现世代**——Rust 新一代（uv、pixi）速度碾压；老一代（pip、Poetry、PDM、conda）更慢。conda 内部也已用 C++ 的 libmamba 替换 Python 写的 classic solver（23.10.0 起默认，提速 50-80%）。

**维度清单**：[project]表遵循 · 锁文件+PEP751 · workspace · Python版本管理 · 默认构建后端 · 解析器/非PyPI依赖 · venv位置 · 私有源认证 · CI缓存 · 迁移路径 · 背景。下表按此展开。

## 2. 对照矩阵

| | pip | uv | Poetry | PDM | pixi | conda |
|---|---|---|---|---|---|---|
| **[project]表** | 不读，只用`[build-system]`[4] | 标准，`[tool.uv]`扩展[10] | **2.0+标准**，`[tool.poetry]`保留分组[16][17] | 从始至终标准[22] | `[tool.pixi.project]`包一层，映射标准字段(实验性)[28] | 不适用，用`environment.yml` |
| **锁文件(主)** | 无官方私有锁格式(requirements.txt/`pip freeze`均未被定义为锁文件)[1] | `uv.lock`(私有)[9] | `poetry.lock` v2.0(私有) | `pdm.lock`(私有)[23] | `pixi.lock`(rattler-lock-v6,多平台单文件) | 无默认格式；`conda export --platform`(可重复)原生多平台[41]；conda-lock 加分类/pyproject解析 |
| **PEP 751支持** | 生成✓(25.1+)/安装✓(26.1+)，26.2再增强，均官方确认[3][38] | preview导出+校验(0.12.11+/17+)[9] | 仅导出(2.3.0+ via plugin)[18] | 仅导出(v2.26+,opt-in)[23] | **路线图中**：#3474设计+#3889导出(已分配)，未发布[42][43] | conda-lock 确认未提及(已定向查证)[36] |
| **Workspace** | 无 | `[tool.uv.workspace]`共享lock[10] | 无，靠path依赖+插件[20] | `[tool.pdm.workspace]`实验性v2.28+[25] | 原生`[workspace.dependencies]`[29] | 无 |
| **Python版本管理** | 无(靠pyenv) | `uv python install`自带分发[11] | 2.1.0实验性`poetry python install`[19] | `pdm python install`自带分发[23] | 经conda channel安装 | `conda create python=3.x` |
| **默认构建后端** | 默认setuptools(legacy)[4] | `uv_build`(可换6种)[9] | `poetry-core` | `pdm-backend`(可自由换) | pyproject模式默认`hatchling`[28] | `conda-build`独立于PEP517 |
| **CI官方缓存** | setup-python `cache:pip`[7] | `setup-uv`细粒度glob[13] | **官方无Action**，仅给cache-dir路径[40] | 官方`setup-pdm` Action，cache:true按pdm.lock[39] | `setup-pixi`,lock哈希缓存[31] | `setup-miniconda`[35] |
| **私有源认证** | index-url+keyring+netrc+token[6] | keyring-provider+sources表 | `tool.poetry.source`+token | keyring+证书+env var | Token/Basic+keyring[30] | `.condarc` token |

## 3. 变体与适配层：pixi/conda vs PyPI 系

pixi、conda 走 conda channel 体系（二进制预编译，含非 Python 依赖），与 PyPI/wheel 体系不直接兼容：
- **依赖范围**：conda/pixi 能把 CUDA、MKL、编译器本身纳入环境；PyPI 系只能装 wheel 里打包好的二进制。
- **解析器**：conda 用 libmamba(C++)，pixi 用 rattler(Rust)，都比 PyPI 系多一层跨语言 SAT 求解。
- **PyPI 互操作**：pixi 同项目可混装 conda 包与 PyPI 包(`[pypi-dependencies]`，conda-first)[30]；conda 原生不感知 PyPI 包。
- **锁定粒度**：conda 需要手动重复 `--platform` 才能多平台锁定[41]；pixi.lock、uv.lock 默认就是多平台/跨环境单文件，这是"新一代"工具在锁文件体验上的共同优势，不只是速度快。

## 4. 用户需要知道的坑

- **PEP 751 还不能当"通用锁文件"用**：各家支持都是导出/预览/实验级，实际锁定与安装仍走私有格式(uv.lock/poetry.lock/pdm.lock)[3][9][18][23]。
- **Poetry 1.x→2.0 不会自动重写 pyproject.toml**：`[tool.poetry]`与新`[project]`表长期共存，需手动决定字段搬家[17]。
- **Poetry 没有官方 CI 缓存方案，PDM 有**：两个"同代"工具官方投入不对等——PDM 提供 `pdm-project/setup-pdm` 官方 Action 自动按 `pdm.lock` 算缓存 key；Poetry 官方文档只给了缓存目录路径，没有 Action、没有 CI 指南[39][40]。
- **conda 免费层对大型商业组织不再免费**：官方条款写明 200+ 员工/合同工的组织需付费 Business license[44]，团队规模接近这个数字要提前确认。
- **从 pip 往其它工具迁移，官方支持并不对等**：uv 官方只写了"从 pip 迁移"，其它方向"尚未可用"；PDM 的 `pdm import` 反而覆盖 Pipenv/Poetry/Flit/pip/setuptools，是当前迁移覆盖面最广的官方工具[12][23]。
- **rye 已停止独立维护**：2024-02 Astral 接手即导向 uv，2025-08 正式弃用；还在用 rye 直接按 uv 官方迁移指南走[14]。
- **uv 背后的 Astral 已被 OpenAI 收购**（2026-03-19，二手信源）：uv 仍开源，但关注治理变化的团队应留意后续[15]。

## 5. 未决与置信度

- uv 私有源认证的具体环境变量命名（如 `UV_INDEX_*_TOKEN`）官方参考页返回 404，正文只给出机制（keyring-provider/sources 表），未逐一列举变量名。
- uv 原生构建后端 `uv_build` 的首次发布版本号/日期未查到明确官方记录。
- pixi 对 PEP 621 `[project]` 字段的逐项支持清单（哪些字段识别、哪些忽略）未逐一核实，正文只给出机制性结论。
- 各工具"解析器算法"表述多为官方营销性描述（如 PDM"简单快速"），未必对应可引用的算法名称/论文。
- "Poetry/PDM 不支持非 PyPI 二进制依赖"这一判断，直接官方证据只覆盖了 uv/pip（明确写了"仅装 PyPI wheel/sdist"）；Poetry/PDM 一侧是从其文档/CLI 设计推断的（官方没有一句话正面声明"不支持conda式依赖"），终审判定为弱证据，供参考。

## 来源
[1] pip 官方文档 — https://pip.pypa.io/en/stable/
[2] PEP 751 — https://peps.python.org/pep-0751/
[3] pip lock 命令 — https://pip.pypa.io/en/stable/cli/pip_lock/
[4] pip 构建系统参考 — https://pip.pypa.io/en/stable/reference/build-system/
[5] pip 依赖解析 — https://pip.pypa.io/en/stable/topics/dependency-resolution/
[6] pip 认证 — https://pip.pypa.io/en/stable/topics/authentication/
[7] setup-python 缓存变更日志 — https://github.blog/changelog/2021-11-23-github-actions-setup-python-now-supports-dependency-caching/
[8] uv 官方文档 — https://docs.astral.sh/uv/
[9] uv CHANGELOG — https://github.com/astral-sh/uv/blob/main/CHANGELOG.md
[10] uv workspaces — https://docs.astral.sh/uv/concepts/projects/workspaces/
[11] uv Python 版本管理 — https://docs.astral.sh/uv/guides/install-python/
[12] uv 迁移指南 — https://docs.astral.sh/uv/guides/migration/
[13] setup-uv Action — https://github.com/astral-sh/setup-uv
[14] Rye 退役 PR — https://github.com/astral-sh/rye/pull/1476
[15] Astral 被 OpenAI 收购(二手) — https://simonwillison.net/2026/mar/19/openai-acquiring-astral/
[16] Poetry 2.0.0 发布公告 — https://python-poetry.org/blog/announcing-poetry-2.0.0/
[17] Poetry pyproject 文档 — https://python-poetry.org/docs/pyproject/
[18] Poetry 2.3.0 发布公告 — https://python-poetry.org/blog/announcing-poetry-2.3.0/
[19] Poetry 2.1.0 发布公告 — https://python-poetry.org/blog/announcing-poetry-2.1.0/
[20] Poetry 依赖管理文档 — https://python-poetry.org/docs/managing-dependencies/
[21] Poetry FAQ(PubGrub) — https://python-poetry.org/docs/faq/
[22] PDM 项目文档 — https://pdm-project.org/latest/usage/project/
[23] PDM CHANGELOG — https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md
[24] PDM venv 文档(PEP582) — https://pdm-project.org/latest/usage/venv/
[25] PDM workspace 文档 — https://pdm-project.org/latest/usage/workspace/
[26] PDM GitHub — https://github.com/pdm-project/pdm
[27] pixi 官方文档 — https://pixi.prefix.dev/latest/
[28] pixi pyproject.toml 集成 — https://pixi.prefix.dev/latest/python/pyproject_toml/
[29] pixi workspace 文档 — https://pixi.prefix.dev/latest/build/workspace/
[30] pixi conda+PyPI 混装 — https://pixi.prefix.dev/latest/concepts/conda_pypi/
[31] setup-pixi Action — https://github.com/prefix-dev/setup-pixi
[32] rattler 解析器博客 — https://prefix.dev/blog/the_new_rattler_resolver
[33] conda 官方文档 — https://docs.conda.io/
[34] conda 23.10.0 发布(libmamba默认) — https://conda.org/blog/2023-11-06-conda-23-10-0-release/
[35] setup-miniconda Action — https://github.com/conda-incubator/setup-miniconda
[36] conda-lock 仓库 — https://github.com/conda/conda-lock
[37] mamba 文档 — https://mamba.readthedocs.io/
[38] pip NEWS.rst(26.1/26.2 pylock支持) — https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst
[39] setup-pdm Action — https://github.com/pdm-project/setup-pdm
[40] Poetry Configuration(cache-dir) — https://python-poetry.org/docs/configuration/
[41] conda export 命令参考(--platform) — https://docs.conda.io/projects/conda/en/latest/commands/export.html
[42] pixi issue #3474(PEP751 support) — https://github.com/prefix-dev/pixi/issues/3474
[43] pixi issue #3889(export to pylock.toml) — https://github.com/prefix-dev/pixi/issues/3889
[44] Anaconda 官方 ToS(200+员工需付费) — https://www.anaconda.com/legal/terms-of-service
