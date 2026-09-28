# Audit of report.md claims (R3 final review)

## Audit Results

| Status | Section | Claim excerpt | Supporting notes | Judgment |
|--------|---------|----------------|------------------|----------|
| A1 | 0（一屏看懂）L5 | uv 是"速度最快" | r1-uv.md 无速度对比数据 | unsupported |
| A2 | 0 L5 | uv "自带 Python 版本管理和 workspace" | r1-uv.md [C9], [C14-17] 完整支撑 | supported |
| A3 | 0 L6 | pixi 有"真正的多子包 monorepo 机制"[19] | r2-pixi-workspace.md [C1-4]、r3-pixi-docs-check.md [C1-3] 完整支撑 | supported |
| A4 | 0 L6 | conda 26.5 版起实验性支持原生导出 `conda-lock.yaml`/兼容 `pixi.lock` [18] | r1-conda.md [C2]、r2-conda-lock-verify.md [C1-2] 支撑（措辞略有差异） | supported |
| A5 | 0 L6 | 此前完全依赖第三方 conda-lock [18] | r1-conda.md [C1], [C3] 支撑 | supported |
| A6 | 0 L7 | PEP 751 已定稿（2025-03-31 Final，取代 PEP 665）[3] | r2-pep751-spec.md [C6]："Created: 24-Jul-2024; Status: Final (as of 31-Mar-2025); Replaces: PEP 665" | supported |
| A7 | 0 L7 | uv 0.6.15+ preliminary 支持导出/安装 pylock.toml [2] | r1-uv.md [C4-7] 明确支撑 | supported |
| A8 | 0 L7 | pip 25.1 实验生成、26.1 实验安装但不支持 extras/dependency-groups [5] | r1-pip.md 笔记不完整，无原文支撑 | weak |
| A9 | 0 L7 | PDM v2.25.0 opt-in 支持 [11] | r1-pdm.md [C5]："v2.25.0 (2025-06-13) 实验性引入 pylock.toml，通过 `pdm export -f pylock` 或 `pdm config lock.format pylock` 使用" | supported |
| A10 | 0 L7 | Poetry 未支持 PEP 751（issue #10356 无里程碑）[9] | r1-poetry.md [C21]："GitHub issue #10356 开放且未分配，标记为 feature request，无里程碑或 PR" | supported |
| A11 | 0 L7 | pixi 官方文档未提及 [PEP 751] | r2-pixi-workspace.md [C5] 明确说"pixi 官方 pyproject.toml 文档未提及 PEP 751 或 pylock.toml" | supported |
| A12 | 0 L8 | Poetry 2 的 `[project]` 表没有完全切换 | r1-poetry.md [C1-2]："Poetry 2.0 支持 PEP 621 `[project]` 表声明依赖，但 `[tool.poetry.dependencies]` 仍然支持，两者可共存" | supported |
| A13 | 0 L8 | 推荐新项目用标准 `project.dependencies`，但显式多源、依赖组、相对路径本地依赖仍要写 `[tool.poetry.dependencies]` [7] | r1-poetry.md [C2], [C10] 精确支撑相对路径、显式源的限制 | supported |
| A14 | 0 L9 | PDM 是 2026-06 才加的实验特性 [11] | r1-pdm.md [C13]："v2.28.0 (2026-06-23) 实验性 workspace 支持" | supported |
| A15 | 0 L9 | pixi 多子包发布文档目前在预览路径 `/dev/`，是否已随稳定版发布待核 [19] | r3-pixi-docs-check.md [C1-3] 已核实：`/latest/` 页面存在，v0.75.0（2026-07-29）已正式发布，此说法已过时但当时准确 | supported |
| A16 | 2（矩阵）L30 | uv `uv.lock` TOML，跨平台通用 [1] | r1-uv.md [C2]："原生锁文件格式叫 uv.lock，采用 TOML 格式...across all platforms and Python markers" | supported |
| A17 | 2 L30 | pip 无原生（pip-tools→`requirements.txt`）[6] | r1-pip.md 笔记未深入，但常识相符；无直接笔记支撑 | weak |
| A18 | 2 L31 | PDM 实验 opt-in，v2.25.0(2025-06) [11] | r1-pdm.md [C5]："v2.25.0 (2025-06-13)" 支撑 | supported |
| A19 | 2 L31 | pixi `pixi.toml`或`pyproject.toml`+`[tool.pixi]` [12] | r1-pixi.md [C1-2] 完整支撑 | supported |
| A20 | 2 L32 | pixi `pixi.lock` YAML，单文件覆盖全平台全环境 [12] | r1-pixi.md [C4-5] 明确支撑 | supported |
| A21 | 2 L35 | conda 26.5+实验性原生导出`conda-lock.yaml`/兼容`pixi.lock` [18] | r1-conda.md [C2]、r2-conda-lock-verify.md [C1-3] 支撑 | supported |
| A22 | 2 L41 | uv 自动建`.venv` [1] | r1-uv.md [C11]："uv automatically creates a .venv directory alongside pyproject.toml" | supported |
| A23 | 2 L41 | uv 构建后端可换 hatchling/pdm-backend/setuptools/maturin 等 [1] | r1-uv.md [C20]："you can select a different build backend template by using --build-backend with hatchling, flit-core, pdm-backend, setuptools, maturin, or scikit-build-core" | supported |
| A24 | 2 L42 | Poetry 不自动装，需自带 BYOP [7] | r1-poetry.md [C5]："Poetry will not automatically install a Python interpreter. Users must bring your own python interpreter." | supported |
| A25 | 2 L44 | PDM workspace 实验特性，v2.28.0(2026-06) [11] | r1-pdm.md [C13]："v2.28.0 (2026-06-23) 实验性 workspace 支持" | supported |
| A26 | 2 L45 | pixi workspace 文档在`/dev/`预览路径 [19] | r3-pixi-docs-check.md 确认现已在 `/latest/`；当时（R2）在 `/dev/` 属实 | supported |
| A27 | 2 L45 | pixi 无`[build-system]`默认 setuptools，`init --format pyproject`默认 hatchling [19] | r2-pixi-workspace.md [C6]："If omitted, Pixi defaults to setuptools. Using hatchling is recommended" | supported |
| A28 | 2 L52 | uv index-strategy 默认 first-index [20] | r2-gotchas.md [C1]："Search for each package across all indexes, limiting the candidate versions to those present in the first index that contains the package" | supported |
| A29 | 2 L52 | uv index-strategy 默认 first-index，缺凭证会回退公共 PyPI [21] | r2-gotchas.md [C4]："uv silently and happily ignored my internal package index URL, gave no warning, and installs example-component from pypi" | supported |
| A30 | 2 L52 | uv 明确 wontfix 不支持读 poetry.lock/Pipfile.lock [22] | r2-gotchas.md [C5]："该issue已被标记为wontfix（不会解决）并已关闭" | supported |
| A31 | 3 L62 | PEP751 明确不覆盖 conda 等非 PyPI 生态 [3] | r2-pep751-spec.md [C5]："The specification does not mention conda or other non-PyPI package managers" | supported |
| A32 | 4 L67 | CI 缓存 key 精度不够（缺 OS 小版本号）导致装到不兼容 wheel [23] | r2-gotchas.md [C7-9]："A wheel compiled on Ubuntu 20.04 may be incompatible with Ubuntu 22.04...The cache key format includes OS type and Python version but ignores OS release" | supported |
| A33 | 4 L69 | conda 的 CI action (setup-miniconda) 不是核心团队维护 [16] | r2-pep751-spec.md [C8]、r1-conda.md [C23] 都支撑 | supported |
| A34 | 4 L69 | Poetry 无官方 CI action [7] | r2-pep751-spec.md [C7]："Multiple Poetry GitHub Actions exist; most are community-maintained rather than official Poetry project actions" | supported |

## Summary counts
- **supported**: 30
- **weak**: 2
- **unsupported**: 1
- **contradicted**: 0

## Highlights requiring correction
1. **A1 (uv 速度最快)**：正文使用了无依据的定性宣传语。建议改为"uv 在官方测试中表现较快"或删除，除非补充具体性能数据。
2. **A8 (pip 25.1/26.1 细节)**：引用 [5] 但笔记未详细记录具体版本号和功能限制，建议验证原官方文档或补充笔记。
3. **A15 (pixi workspace 时效性)**：R2 笔记正确但已过时，pixi v0.75.0（2026-07-29）已发布，`/latest/` 路径已包含 workspace 文档，建议在报告中标注"该功能已随 v0.75.0 稳定版发布"。

