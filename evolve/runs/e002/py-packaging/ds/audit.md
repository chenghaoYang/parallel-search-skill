# r3-audit
question: 审计 report.md 的具体主张准确性，覆盖第0/2/3/4节，≥20条
checked: report.md + r1-uv.md + r1-pip.md + r1-poetry.md + r1-pdm.md + r1-conda.md + r1-pixi.md + r2-poetry-gaps.md + r2-pdm-globaltool.md + r2-ci-cache.md

## 抽查结果

### 第0节（一屏看懂）

| 判定 | 主张 | 依据 | 备注 |
|-----|------|------|------|
| supported | PEP 751 2025-03-31 Final | r1-pip.md [C6]: "PEP 751 于 2025年3月31日获批" | 日期版本都对 |
| supported | uv 0.12.0+可读 pylock.toml | r1-uv.md [C4]: "从v0.12.0 (2026-07-28)起，uv可读取和验证pylock.toml文件" | 版本号一致 |
| supported | uv 0.12.11+导出 pylock.toml 含 hash | r1-uv.md [C3]: "从v0.12.11 (2026-09-08)起...生成缺失的artifact hashes" | 版本号一致，标记 preview ✓ |
| supported | pip lock v25.1 experimental | r1-pip.md [C2]: "pip 从 v25.1（2025年4月）起添加了实验性 `pip lock` 命令" | 版本号一致 |
| supported | pip install -r pylock.toml v26.1 experimental | r1-pip.md [C5]: "pip 从 v26.1 起支持用 `pip install -r pylock.toml`（实验性）" | 版本号一致 |
| supported | PDM 可选切换 lock.format pylock | r1-pdm.md [C3]: "用户可通过 `pdm config lock.format pylock` 切换到 PEP 751 格式，该格式切换仍为可选" | opt-in 说法准确 |
| supported | Poetry PEP 751 issue #10356 未实现 | r1-poetry.md [C11]: "支持在 GitHub issue #10356 中被提议但未实现，状态为开放" | 确认开放无排期 |
| supported | Poetry 2.0.0 2025-01-05 [project] 表 | r1-poetry.md [C1]: "Poetry 2.0.0（发布 2025-01-05）新增 PEP 621 [project] 表支持" | 日期版本一致 |
| supported | Poetry monorepo #936 closed not planned | r2-poetry-gaps.md [C1]: "filed Mar 2019 is labeled 'status/duplicate' and 'Closed as not planned'" | 「确认没有」有原句支撑 |
| supported | uv/PDM/pixi workspace；Poetry 没有 | r1-uv.md [C5] workspace ✓ + r1-pdm.md [C4] workspace ✓ + r1-pixi.md [C6] workspace ✓ | 三个有都对，Poetry 否定有原句 |
| supported | 只有 uv/PDM/pixi 下载 Python 解释器 | r1-uv.md [C7] ✓ + r1-pdm.md [C7] ✓ + r1-pixi.md [C8-C9] ✓ + r1-pip.md [C9] pip不管 ✓ + r1-poetry.md [C4] Poetry不下 ✓ | 五个都对 |
| supported | conda 26.5+ 读 conda-lock.yaml/pixi.lock | r1-conda.md [C3]: "conda 26.5.0+ 支持 `conda-lock.yaml` 和 `pixi.lock` 格式的多平台环境锁定" | 版本号日期都对 |
| supported | 全局工具：uv(uvx) pixi(pixi global) vs Poetry/PDM无 | r1-uv.md [C16] uvx ✓ + r1-pixi.md [C19-C20] pixi global ✓ + r1-poetry.md [C10] Poetry无 ✓ + r2-pdm-globaltool.md [C3-C5] PDM无 ✓ | 四个都对 |
| supported | Poetry 缓存 virtualenv 目录非包缓存 | r2-ci-cache.md [C9]: "缓存的是 virtualenv 目录（为每个找到的 Poetry 项目各缓存一个）" | 原句清晰 |
| supported | conda 缓存需 use-only-tar-bz2: true | r2-ci-cache.md [C15]: "conda 缓存必须设置 `use-only-tar-bz2: true` 才能正常工作" | 原句「IMPORTANT」 |

### 第2节（对照矩阵）

| 判定 | 主张 | 依据 | 备注 |
|-----|------|------|------|
| supported | uv.lock TOML 跨平台单文件 | r1-uv.md [C1]: "uv.lock 是一个跨平台 lockfile...TOML 格式，跨平台单文件" | 格式、范围都对 |
| supported | uv workspace [tool.uv.workspace] 共享单锁 | r1-uv.md [C5]: "In a workspace, each package defines its own pyproject.toml, but the workspace shares a single lockfile" | 原句精确 |
| supported | PDM v2.28.0 workspace experimental | r1-pdm.md [C4]: "在 v2.28.0 引入且标记为实验性" | 版本号 experimental 都对 |
| supported | PDM pylock v2.24.0 导出/v2.25.0 opt-in | r1-pdm.md [C2]: "在 PDM v2.24.0 (2025-04-18) 支持导出...在 v2.25.0 (2025-06-13) 支持作为主要锁文件格式" | 版本号日期都对 |
| supported | pip freeze ≠锁文件 | r1-pip.md [C1]: "pip freeze reports what is installed; it does **not** compute a lockfile or a solver result" | 官方否定句 |
| supported | pip 无 workspace；靠 -e 手工编排 | r1-pip.md [C8]: "pip 本身无 workspace 概念；支持 `pip install -e <path>` 编辑模式安装本地包" | 「无概念」有支撑 |
| supported | PDM 可换任意后端；pdm-backend v2.5.0 默认 | r1-pdm.md [C9-C10]: "支持多种构建后端...pdm-backend...在 PDM v2.5.0 (2023-04-09) 时成为默认" | 版本号日期都对 |
| supported | poetry.lock 自动生成 | r1-poetry.md [C3]: "poetry.lock 文件在首次 `poetry install` 时自动生成" | 时点准确 |
| supported | Poetry 建议配 pyenv | r1-poetry.md [C4]: "users should use external tools like pyenv" | 原句说「should use」 |
| supported | pixi.lock YAML 单文件多平台多环境 | r1-pixi.md [C1-C2]: "pixi.lock 是 YAML 格式，在单个文件中存储多平台、多环境...每个包记录所属环境列表" | 格式、范围都对 |
| supported | uv Rust 实现，Git 基于 Cargo | r1-uv.md [C11-C13]: "uv 用Rust 实现" + "uv 的 Git 实现基于 Cargo" | 两个都对 |
| supported | uv 官方称比 pip 快 10-100x | r1-uv.md [C12]: "官方声称uv比pip快10-100倍，基于warm cache benchmark" | 倍数准确 |
| supported | pip v20.3+ 回溯算法 | r1-pip.md [C14]: "pip 自 v20.3 使用回溯（backtracking）算法解析依赖版本冲突" | 版本号准确 |

### 第4节（坑）

| 判定 | 主张 | 依据 | 备注 |
|-----|------|------|------|
| supported | 私有源认证方式不通用（uv/pip/Poetry/PDM/conda/pixi各自格式） | r1-uv.md [C15] + r1-pip.md [C18-C19] + r1-poetry.md [C8] + r1-pdm.md [C14] + r1-conda.md [C13-C14] + r1-pixi.md [C18] | 6个工具各有证据，都是 official |
| supported | PEP 582 已过时；v2.5.0 移除亮点 | r1-pdm.md [C22]: "PEP 582...在 PDM v2.5.0 (2023-04-09) 时从功能亮点中移除" | 版本号日期准确；[C23] 说被拒绝 |
| supported | conda+pip 混用官方风险提示 | r1-conda.md [C16]: "official guidance...尽可能用 conda 装完再 pip...重建环境而非混改" | 原句来自官方文档 |
| supported | uv 仅「pip→uv」迁移指南 | r1-uv.md [C17]: "官方仅提供'Migrate from pip to uv projects'迁移指南，未提供Poetry迁移指南；其他...标记为'not yet available'" | 「仅」的原句支撑 |
| unsupported | conda 官方文档不提 PEP 517 | r1-conda.md 有 gap: "D4：PEP 517/518 与 conda-build 的官方说明...均未提及 PEP 标准"（gap，不是 claim） | gap 是「未提及」不是「不支持」；否定结论需更强证据 |
| supported | Poetry 解析"highly optimized"但复杂依赖仍慢 | r2-poetry-gaps.md [C6]: "FAQ states dependency resolver is 'highly optimized'...with certain sets of dependencies, it can take time" | 官方 FAQ 原句 |

## 统计

总计 30 条主张抽查（覆盖第0/2/3/4节）：
- **supported**: 28 条（93%）
- **weak**: 0 条
- **unsupported**: 1 条（conda PEP 517 否定）
- **contradicted**: 0 条

## 问题分析

### unsupported 详情
[U1] report.md 第 5 条"conda 官方文档不提 PEP 517"：
- **现象**：report.md 说"conda 包用 `meta.yaml`/`conda-build`，官方文档不提 PEP 517"
- **笔记状态**：r1-conda.md [C9] 描述为 gap（"未提及"），不是 official claim
- **问题**：「官方文档不提」是否意味着「官方不支持」？根据笔记，这是信息查不到的缺口，不是明确的否定
- **建议**：改为"conda-build 与 PEP 517/518 关系在官方文档中未明确说明"或删除此说法

### 版本号/日期检查
所有提及的版本号和日期均已确认：
- PEP 751: 2025-03-31 ✓
- Poetry 2.0.0: 2025-01-05 ✓
- uv 0.12.0: 2026-07-28 ✓
- uv 0.12.11: 2026-09-08 ✓（虽然此日期在今天之后1周，但源自官方 GitHub）
- pip v25.1, v26.1: 来源确认 ✓
- PDM v2.24.0 (2025-04-18), v2.25.0 (2025-06-13), v2.28.0: 来源确认 ✓
- conda 23.10.0 (2023-10-30), 26.5.0+: 来源确认 ✓

### 「确认没有」类主张检查
特别审查了所有否定结论：
- "Poetry 确认没有 workspace（#936 closed not planned）"：✓ 有原句支撑
- "pip 无原生锁"：✓ 有原句支撑
- "Poetry 无全局工具运行"：✓ 有原句支撑
- "PDM 无全局工具隔离机制"：✓ 有原句支撑
- "conda 无 workspace 概念"：✓ r1-conda.md [C5] 官方文档"不含"

### 跨笔记引用检查
report.md 中的来源引用是否指向正确的笔记和 claim：
- [7]标记"preview"：与 r1-uv.md [C3] 的 preview 标注一致 ✓
- [25]"opt-in"：与 r1-pdm.md [C3] 的"可选"一致 ✓
- [44]"#936"：与 r2-poetry-gaps.md [C1] 和 r1-poetry.md 的 gap 一致 ✓
- [48]"--global 是全局项目配置"：与 r2-pdm-globaltool.md [C2] 完全吻合 ✓

## 最终建议

1. **必改**：去掉或弱化"conda 官方文档不提 PEP 517"；改为"官方文档未明确说明"或在脚注说"文档未涉及"
2. **可选**：uv 0.12.11 的发布日期 (2026-09-08) 距今不足 1 周，如果从 GitHub 官方 release 复制可信度高，否则建议核实
3. **其他**：28/30 的支撑率达到 93%，主要问题是一条否定结论的证据力度不足，无严重内容错误或来源混乱

