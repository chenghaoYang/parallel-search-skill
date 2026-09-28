# grid v1（R1 收束后）

## 分类轴（家族划分依据，R1 后确认成立，不换轴）
- **轴 A：解决问题的层级** — (a) 底层安装器；(b) PyPI 全生命周期项目管理器；(c) 跨语言环境管理器。
  R1 观察到的加强证据：(b) 阵营正在向下吃 (a) 的功能——uv 已完整自带 Python 版本管理/venv/构建；
  PDM 已成熟自带 Python 版本管理；Poetry 2.1.0 才实验性加入 `poetry python install`（最晚）。
  (c) 阵营的 pixi 正在向上吃 (b) 的功能——原生 workspace、可选 pyproject.toml 支持，比 conda 更像项目管理器。
- **轴 B：实现世代** — 新一代 Rust（uv、pixi，均标榜比前代快 10-100x）vs 老一代 Python/C++（pip、Poetry、PDM、conda）。
  conda 内部也有世代分层：libmamba（C++，23.10.0 起默认，提速 50-80%）vs classic solver（Python，仍可选）。

## 对照矩阵（R1 收束状态）
| 实体 | C1定位 | C2 [project]表 | C3锁文件+PEP751 | C4 workspace | C5 Python版本 | C6构建后端 | C7解析器/非PyPI依赖 | C8 venv | C9私有源 | C10 CI缓存 | C11迁移 | C12成熟度 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pip | ✅ | ✅ 不读，只用[build-system] | ✅ PEP751 Final 2025-03-31；25.1 `pip lock`写(实验/单平台)；**26.1 `install -r pylock.toml`读(官方NEWS.rst确认)**；26.2 增强 | ✅ ∅无 | ✅ ∅无（需pyenv等） | ✅ 默认setuptools legacy | ✅ 20.3起backtracking，仅PyPI | ✅ ∅不建venv | ✅ index-url/keyring/netrc/token | ✅ setup-python cache:pip | ∅官方未写(预期内，pip是基线) | ✅ 2008，v26.2.1，PyPA |
| uv | ✅ | ✅ 标准[project]，[tool.uv]扩展 | ✅ uv.lock(私有)为主；PEP751 **preview**：v0.12.11导出补hash、v0.12.17校验读取，非默认格式 | ✅ [tool.uv.workspace]，共享uv.lock | ✅ `uv python install`，python-build-standalone | ✅ 默认uv_build，可换6种 | ✅ resolution，平台特定/通用可选，不装conda包 | ✅ 默认.venv | ✅ keyring-provider+sources表 | ✅ 官方setup-uv Action，细粒度glob缓存 | ✅ 官方仅pip→uv；rye已弃用迁至uv | ✅ Astral，v0.12.18，**Astral 2026-03被OpenAI收购(二手)** |
| Poetry | ✅ | ✅ **2.0.0(2025-01-05)起支持[project]**，[tool.poetry]保留分组等 | ✅ poetry.lock v2.0(私有)为主；**2.3.0+可经plugin导出pylock.toml**(导出only) | ✅ 无原生，靠path dep+插件 | ✅ 依赖pyenv/系统；2.1.0实验性`poetry python install` | ✅ poetry-core | ✅ PubGrub，NP-complete | ✅ virtualenvs.in-project | ✅ tool.poetry.source+token/http-basic | ✅ **官方确认无Action/无CI指南**，仅cache-dir路径配置(R2核实) | ✅ `poetry init`向导；无官方→uv工具 | ✅ 2016，v2.1.0，需py3.10+ |
| PDM | ✅ | ✅ 从一开始就标准[project] | ✅ pdm.lock(私有)为主；**v2.26+支持导出pylock(opt-in)，v2.29+尊重依赖组** | ✅ [tool.pdm.workspace]**实验性v2.28+** | ✅ `pdm python install`，python-build-standalone | ✅ 默认pdm-backend，可自由换 | ✅ 聚焦大型二进制发行版 | ✅ 默认venv；PEP582降级为非默认(未废弃) | ✅ keyring/pdm config/证书 | ✅ **官方`pdm-project/setup-pdm` Action**，cache:true按pdm.lock计算key(R2核实，R1的404是路径变了) | ✅ `pdm import`(Pipenv/Poetry/Flit/pip/setuptools) | ✅ 2019，v2.29.2，pdm-project组织 |
| pixi | ✅ conda生态之上的Cargo式工具 | ✅ [tool.pixi.project]，pyproject.toml模式下映射标准字段(实验性v0.18+) | ✅ pixi.lock=rattler-lock-v6(多平台单文件)；**PEP751路线图中：issue #3474(设计)+#3889(导出,已分配@wolfv)，未发布(R2核实非沉默)** | ✅ 原生[workspace.dependencies]，v0.48+ | ✅ 经conda channel装Python，无独立版本管理器 | ✅ pyproject模式默认hatchling | ✅ rattler(Rust,resolvo CDCL)，比conda快10x；conda+PyPI混装 | ✅ .pixi/envs/ | ✅ Bearer/Conda Token/Basic+keyring | ✅ 官方setup-pixi Action，lock哈希缓存 | ✅ `pixi init --import env.yml`；conda-lock可转pixi.toml | ✅ 2023-06，v0.81.0，prefix.dev |
| conda | ✅ 跨语言环境管理器(任意语言) | ✅ environment.yml，不读[project] | ✅ **R1"原生多平台"说法已订正**：`conda export`默认单平台，需重复`--platform`才多平台(R2核实官方文档)；conda-lock 加分类/pyproject解析等增值功能，非唯一多平台方案；conda-lock 对PEP751**确认真沉默**(已定向搜索issues/releases) | ✅ ∅无，靠pixi/uv或分项目 | ✅ `conda create -n env python=3.x` | ✅ conda-build独立于PEP517/518 | ✅ libmamba默认(23.10.0起，+50~80%)，支持CUDA等二进制 | ✅ `conda create/activate` | ✅ token+.condarc；**Anaconda现行官方ToS：200+员工/合同工组织需付费Business license(R2核实，替换2020年二手源)** | ✅ setup-miniconda，缓存~/conda_pkgs_dir | ✅ mamba为独立C++实现非合并；conda-lock可导出至pixi | ✅ 2012，v26.7.2，Anaconda Inc+conda-forge |

状态图例：✅ 有一手来源+原文 | ⚠ 需核实/仅二手/存疑 | ❓ 缺口 | ∅ 官方未写(已定向查过，属预期)

## 用户点名疑点（R1 后结论）
| 疑点 | 结论 |
|---|---|
| PEP 751/pylock.toml 是否定稿 + uv/pip 支持度 | ✅ **PEP751 已 Final（2025-03-31）**。pip：25.1 实验性生成(单平台)，26.1 实验性安装读取（**读取这条仅二手，R2 核实**）。uv：**preview** 阶段可导出+校验读取（v0.12.11/v0.12.17），primary 仍是 uv.lock。两者均未把 pylock.toml 设为默认/唯一格式。 |
| Poetry 2.0 是否改用标准 [project] 表 | ✅ **是**。2.0.0（2025-01-05）起遵循 PEP 621 `[project]` 表；`[tool.poetry]` 保留 dependency groups 等 Poetry 专属功能；渐进式、向后兼容、无自动迁移命令。 |

## R2 计划（3 workers，narrower，点名格子/主张）
1. r2-pip-pylock-verify — 核实 pip 表格 C3 里"⚠仅二手"的 `pip install -r pylock.toml`（pip 26.1）主张，改用 pip 官方 NEWS.rst/changelog。
2. r2-ci-cache-poetry-pdm — 补 Poetry C10、PDM C10 两个 ⚠ 格子的官方 CI 缓存证据。
3. r2-conda-verify — 核实 conda C3（"conda export 支持多平台锁文件"是否真实，官方原文）、conda/pixi/conda-lock 对 PEP751 的官方沉默是否属实（C3 pixi、C3 conda-lock）、conda C9 Anaconda 现行商业条款原文（而非 2020 年二手回顾）。

## R2 收束结果（全部 3 项核验完成，全部 official，全部有明确结论）
1. **pip pylock 安装侧：confirmed official，且比预期更丰富。** pip 26.1（2026-04-26）NEWS.rst 官方确认
   `pip install -r pylock.toml`（experimental）；pip 26.2（2026-07-29）进一步支持 `--uploaded-prior-to`、`--only-final`
   与 `-r pylock.toml` 配合。C3 从 ⚠ 升级为 ✅，时间线完整：25.1 生成→26.1 安装→26.2 增强。
2. **CI 缓存：Poetry 确认官方无方案；PDM 反转为官方有方案。** Poetry 官方文档只给 cache-dir 路径配置，无 CI/Action 指南，
   无官方 Action（社区 snok/install-poetry 非官方）——C10 定为 ∅（官方确认未写）。PDM 官方文档明确推荐
   `pdm-project/setup-pdm` Action，`cache: true` 默认按 pdm.lock 算 key，支持 glob——C10 升级为 ✅，R1 的 404 只是路径变了。
3. **conda 多平台锁文件：R1 主张有误，已订正。** 官方文档明确 `conda export` 默认单平台，需重复 `--platform` 参数
   才能产出多平台文件（如 `--platform linux-64 --platform osx-64 --platform win-64`）；不是"文件名叫 conda-lock.yaml
   就自动多平台"。订正为：conda 原生**可以**做多平台锁定（显式重复 flag），conda-lock 的价值在别处（依赖分类、
   pyproject.toml 解析、导出到 pixi.toml 等），不是"conda 完全做不到多平台"。C3 从 ⚠ 改为 ✅（訂正版）。
4. **pixi 对 PEP751 不是沉默，是在推进中。** 官方 issue #3474（"PEP751 support"，needs-design）+ #3889
   （"Support export to pylock.toml"，已分配给核心维护者 @wolfv）。pixi 这格从"未见支持"改为"路线图中，未发布"。
5. **conda-lock 对 PEP751 确认真沉默**（已定向搜索 issues/releases/CHANGELOG，无结果）——从推测的 ∅ 变成定向核实过的 ∅。
6. **Anaconda 商业条款：拿到现行官方原文。** anaconda.com 官方 ToS："Users within organizations with 200+
   employees/contractors (including Affiliates) require a paid Business license"——替换掉 2020 年二手回顾来源，C9 升级为 ✅。

grid 状态更新：⚠ 6 个格子全部清零，无一降级为 ❓/⚔，全部确认或订正为 ✅/∅。79 格中 ✅74 ∅5，resolved 79/79 (100%)。

## 观察 → 下一步（R2 后）
观察：R2 三个核验全部拿到明确的一手结论（confirmed / corrected / confirmed-absent），grid 无残留 ⚠/❓/⚔，
上一轮几乎把所有薄弱点都解决了。→ 动作：不再需要扩展型 spawn，进入终审——派 1 个审稿工人，只读 report.md + notes/，
抽查 ≥20 条具体主张核对是否与笔记原句一致，尤其是本轮改动过的几条（pip 26.x 时间线、PDM setup-pdm、
conda --platform、pixi issue 号）。预计 spawn：1（这是 R3，也是最后一轮）。
