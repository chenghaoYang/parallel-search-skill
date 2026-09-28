# Grid v1（R1 后更新）

## 分类轴（R1 验证：成立，解释了矩阵里大部分差异）

- 轴 A：包生态基座 — PyPI/wheel 单一生态，还是能桥接 conda-forge 二进制生态。
- 轴 B：工具定位 — all-in-one 项目管理器，还是单一功能 point tool。
- 新发现：pixi 是唯一原生横跨 A 两端的工具（conda 包 + `[pypi-dependencies]` 内嵌 uv resolver），需在「变体」一节单独说明，不改轴。

## 家族划分（R1 后确认，未变）

| 家族 | 成员 | 依据 |
|---|---|---|
| PyPI 一体化项目管理器 | uv, Poetry, PDM | 自带锁文件 + venv 管理 + `pyproject.toml` 驱动 |
| PyPI 传统组合工具 | pip (+pip-tools) | 无项目级锁文件/venv 概念，需组合 pyenv/pipx |
| conda 生态环境管理器 | conda, pixi | 依赖 conda channel 二进制包；pixi 是 Rust 新实现，额外原生桥接 PyPI |

## 矩阵状态（R1 后）

| 实体 | D1 锁文件 | D2 Workspace | D3 Py版本 | D4 构建后端 | D5 解析/速度 | D6 私有源 | D7 全局工具 | D8 迁移 | D9 定位 |
|---|---|---|---|---|---|---|---|---|---|
| uv | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅(仅pip→uv) | ✅ |
| pip(+pip-tools) | ✅ | — | ✅(∅原生) | ✅ | ✅ | ✅ | ✅(→pipx) | ⚠ | ✅ |
| Poetry | ✅ | ❓→R2 | ✅(∅原生下载) | ✅ | ❓→R2 | ✅ | ✅(∅) | ❓→R2 | ✅ |
| PDM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❓→R2(弱证据) | ✅ | ✅ |
| conda | ✅ | ∅ | ✅ | —(非PEP517体系) | ✅ | ✅ | ✅ | ✅ | ✅ |
| pixi | ✅ | ✅ | ✅ | ✅ | ⚠(部分) | ✅ | ✅(∅同pipx) | ✅ | ✅ |

PEP 751 / pylock.toml 子状态（用户疑点 Q1，跨实体，D1 内单列）：PEP 本身 2025-03-31 Final [16]；uv 读取 0.12.0+/导出+hash 0.12.11+，仍 preview [7]；pip `pip lock`(v25.1)/`pip install -r pylock.toml`(v26.1) 均 experimental、无稳定时间表 [9][10]；Poetry 未实现，开放 issue #10356 无排期 [24]；PDM 导出 v2.24.0/可选主格式 v2.25.0(`pdm config lock.format pylock`)，仍 opt-in [25][30]；conda/pixi 文档未提及（∅，已定向查证）。

Poetry `[project]` 表疑点（Q2）：Poetry 2.0.0(2025-01-05) 起支持 PEP 621 `[project]` [19]；与 `[tool.poetry.*]` 并存，后者用于「enrich」（如私有源、path/git 依赖等标准字段无法表达的信息）[21][20]；未设弃用时间表（冲突/未决）。

## Grid v2（R2 后，全部核心维度解决）

新增 D10 CI 缓存（用户点名，R1 缺失，R2 补齐）。

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 CI缓存 |
|---|---|---|---|---|---|---|---|---|---|---|
| uv | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pip | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠ | ✅ | ✅(经setup-python) |
| Poetry | ✅ | ∅确认(#936 closed not planned) | ✅ | ✅ | ⚠(算法名未公开) | ✅ | ∅确认(真实quote) | ∅确认(无导入/无指南) | ✅ | ⚠(无官方CI页,靠setup-python) |
| PDM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ∅确认(真实quote) | ✅ | ✅ | ✅ |
| conda | ✅ | ∅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pixi | ✅ | ✅ | ✅ | ✅ | ⚠(部分) | ✅ | ✅ | ✅ | ✅ | ✅ |

结论：4 个必答维度（D1/D2/D3/D4）在 6 个实体上全部 ✅/∅/—（无一处 ❓）。剩余弱项只是次要维度里的细节（Poetry/pixi 解析器算法名、pip 无迁移指南），优先级低。→ 触发终审条件。

## R2 目标（观察 → 下一步，已执行）

- 观察：Poetry D2（workspace）、D5（解析器/速度）、D8（迁移指南）三格薄弱或缺失，且 D2 是「没有此功能」的排他类主张，worker 自己标了不确定。
- 观察：PDM D7 的 claim（C19）quote 是伪造的 "NA"，不满足证据标准，需要真实核实。
- 观察：用户点名的「CI 缓存」维度在 R1 完全没有工人覆盖（6 个工人都按实体分工，没人管跨实体的 CI 缓存问题）。
- 决策：R2 派 3 个工人（少于 R1 的 6，聚焦缺口）：
  1. r2-poetry-gaps：反证/确认 Poetry workspace 缺失 + 解析器速度 + 迁移指南三格。
  2. r2-pdm-globaltool：真实核实 PDM 有没有 pipx 等价物。
  3. r2-ci-cache：跨实体，查 uv/pip/Poetry/PDM/conda/pixi 在 GitHub Actions 里官方推荐缓存什么路径/文件。
- 预计 spawn：3。
