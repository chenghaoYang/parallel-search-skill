# Audit Report: report.md vs research notes

checked: /private/tmp/ps-arena/evolve/e001/py-packaging/ds/report.md
notes_dir: /private/tmp/ps-arena/evolve/e001/py-packaging/ds/notes/

## Claim Verification (30 assertions)

### §0 一屏看懂

1. **supported** | "PEP 751（`pylock.toml`）已定稿为 Final（2025-03-31）" | [C6-r1-uv, C5-r1-pip] | 两份笔记都明确记录了Final状态和日期
2. **supported** | "pip 支持最完整——`pip lock` 生成(25.1，2025-04-26)" | [C4-r1-pip] | 官方文档支持，版本号和日期准确
3. **supported** | "`pip install -r pylock.toml` 消费(26.1，2026-04-26)" | [C1-r2-pip-pylock-install] | 官方新闻说明，版本日期准确
4. **weak** | "uv(0.12.0+，2026-07-28) 和 Poetry(2.3.0+) 只支持**导出**成它" | [C7-r1-uv, C8-r1-uv, C10-r1-poetry] | §0说"只支持导出"，但笔记r1-uv [C8]同时说"uv支持从pylock.toml导入（pip install/sync）"，§3也说"可导入"；表述有歧义，应改为"主力仍是各自的uv.lock/poetry.lock"
5. **supported** | "Poetry(2.3.0+) 只支持导出" | [C10-r1-poetry] | 官方发布公告明确支持，需poetry-plugin-export>=1.10
6. **supported** | "PDM 可以把它设为替代锁格式（仍"实验性"）" | [C3-r1-pdm, C4-r1-pdm] | 笔记完整记录了`pdm config lock.format pylock`命令
7. **supported** | "conda/pixi 官方文档未提及" | [C8-r1-conda, gap-r1-pixi] | 笔记明确标记为gap，无PEP751相关官方表述
8. **supported** | "原生 workspace 三家有，两家没有：uv、PDM(2.28+，实验性)、pixi" | [C19-r1-uv, C9-r1-pdm, C15-r1-pixi] | 三份笔记都支持，版本号2.28.0(2026-06-23)准确
9. **supported** | "uv 把"装 Python 解释器"内置了" | [C13-14-r1-uv] | 官方CLI文档明确列出`uv python install/pin`命令
10. **supported** | "PDM 有 `pdm python install`" | [C6-r1-pdm] | 官方文档支持

### §2 对照矩阵

11. **supported** | "解析器-uv: PubGrub(自研，Rust)" | [C11-r1-uv] | 官方文档明确说明
12. **supported** | "解析器-pip: 'New resolver'(20.3+，回溯)" | [C8-r1-pip] | 笔记引用NEWS.rst，版本号准确
13. **supported** | "解析器-Poetry: Mixology(PubGrub 的 Python 实现)" | [C12-r1-poetry] | 笔记明确标注为official来源
14. **supported** | "解析器-PDM: resolvelib(回溯)" | [C5-r1-pdm] | 笔记标注为official，包含backtracking策略说明
15. **supported** | "解析器-pixi: resolvo(conda 侧)+uv 的 PubGrub(PyPI 侧)" | [C8-r1-pixi] | 笔记详细描述双解析器架构，官方文档引用
16. **supported** | "解析器-conda: libmamba(23.10+ 默认)" | [C10-r1-conda] | 明确标注23.10.0为默认，附带日期2023-10-30
17. **supported** | "锁文件-uv: `uv.lock`(TOML，PubGrub 解析结果)" | [C5-r1-uv] | 官方文档对uv.lock格式和跨平台特性的说明
18. **supported** | "锁文件-Poetry: `poetry.lock`(专有格式)" | [C9-r1-poetry] | 笔记明确标注为非PEP751标准
19. **supported** | "锁文件-PDM: `pdm.lock`(默认格式)" | [C3-r1-pdm] | 默认格式说明准确
20. **supported** | "构建后端-uv: `uv_build`(PEP517，0.12+ 新项目默认)" | [C18-r1-uv] | CHANGELOG明确指出v0.12.0时改为默认

### §3 PEP 621/751适配表

21. **supported** | "PEP 751 pip采用最彻底：`pip lock`生成+`pip install -r pylock.toml`消费" | [C4-r1-pip, C1-r2-pip-pylock-install] | 两份笔记完整覆盖生成(25.1/2025-04-26)和消费(26.1/2026-04-26)
22. **weak** | "uv仅 `uv export --format pylock.toml`...可导入但非原生生成" | [C7-r1-uv, C8-r1-uv] | §0说"只支持导出"与§3的"可导入"之间存在矛盾，笔记中r1-uv [C8]明确说"支持从pylock.toml导入"；建议§0改为"主力仍是uv.lock"而非强调"只导出"
23. **supported** | "Poetry 2.3.0+ 仅导出，需 poetry-plugin-export≥1.10" | [C10-r1-poetry] | 笔记明确列出版本和插件要求
24. **supported** | "PDM 可设为默认锁格式，仍'实验性'" | [C3-r1-pdm] | 笔记记录`pdm config lock.format pylock`切换命令
25. **supported** | "Poetry 2.0 起支持标准[project]表" | [C3-r1-poetry] | 笔记完整记录PEP621支持情况

### §4 用户需要知道的坑

26. **supported** | "PDM 的 `pdm import` 官方支持读 5 种旧工具迁移" | [C13-r1-pdm] | 笔记列举：Pipenv/Poetry/Flit/pip/setuptools
27. **supported** | "uv 官方迁移文档仅'pip → uv projects'完成" | [C31-32-r1-uv] | 笔记明确指出其他迁移排在GitHub #5200，未发布
28. **supported** | "pixi 官方明确不支持私有 PyPI 仓库认证" | [C19-r1-pixi] | 官方文档原句："Currently, pixi doesn't support private PyPI repositories"
29. **supported** | "pip 官方文档给了 `pip cache dir` 命令" | [C24-r1-pip] | 笔记完整记录查询缓存目录的方法
30. **supported** | "PDM(`pdm-project/setup-pdm`，以 pdm.lock 算缓存 key)" | [C12-r1-pdm] | 笔记记录setup-pdm的cache功能启用方法

---

## 自洽性检查（Internal Consistency）

### 核心问题：D3(锁文件/PEP751) 一致性

#### 问题1：uv 关于 PEP 751 的矛盾表述

**甲处原文（§0第2点）**
> uv(0.12.0+，2026-07-28) 和 Poetry(2.3.0+) 只支持**导出**成它，主力仍是各自的 `uv.lock`/`poetry.lock`

**乙处原文（§3 PEP 751适配表-uv行）**
> uv（仅 `uv export --format pylock.toml`，0.12.0/2026-07-28 起校验支持，**可导入但非原生生成**，主力仍 uv.lock）

**笔记支撑**
- r1-uv.md [C8]: "uv支持从pylock.toml导入（pip install/sync），但uv.lock更强大"（type: official）
- r1-uv.md conflict记录: "uv.lock vs pylock.toml定位不同：issue #12584(2025-03-31)表示pylock.toml无法完全替代uv.lock功能，因此uv采用export/import模式而非完全迁移"（type: official）

**不一致处**：§0强调"只支持导出"，§3和笔记同时提及"可导入"。笔记中的official来源更完整地说明了uv的export/import双向支持。

**建议改法**：§0改为"uv(0.12.0+，2026-07-28)可导出pylock.toml并支持导入，但主力仍是uv.lock"

---

#### 问题2：D2(清单标准/PEP 621) 一致性检查

**§0第3点原文**
> Poetry 2.0 起才有标准 `[project]` 表，核心元数据改用 PEP 621 `[project]`，旧 `[tool.poetry]` 字段多数 deprecated；但 source/group/package-mode 等 Poetry 专有能力还留在 `[tool.poetry]`，没有消失。

**§3 PEP 621表中 Poetry行**
> Poetry 2.0 起支持，旧字段部分 deprecated，但 source/group/package-mode 等专有能力仍在 `[tool.poetry]`

**笔记支撑** [r1-poetry.md]
- [C3]: "Poetry 2.0 加入了对 [project] 表的支持，符合 PEP 621"
- [C4]: "许多 [tool.poetry] 字段现已废弃"
- [C6]: "[tool.poetry] 保留的 Poetry 专有字段包括：package-mode, packages, exclude/include, scripts, extras, plugins, requires-poetry, requires-plugins, build-constraints"

**一致性**：完全一致，§0和§3的描述相同，笔记完整支撑。

---

#### 问题3：PEP 751 "Final" 日期在文中推导

**§0第2点原文**
> PEP 751（`pylock.toml`）已定稿为 Final（2025-03-31）

**§3第1行原文**
> PEP 751 `pylock.toml`（2025-03-31 定为 Final）

**§4 § 第1段原文**
> 无直接引用，但列出的版本号依赖PEP 751的该日期

**笔记支撑**
- r1-uv.md [C6]: "PEP 751状态为Final，标题...'A file format to record Python dependencies for installation reproducibility'，2025年3月31日确定" (src: https://peps.python.org/pep-0751/)
- r1-pip.md [C5]: "PEP 751 于 2025 年 3 月 31 日接纳为最终状态" (src: https://peps.python.org/pep-0751/)

**一致性**：完全一致。

---

#### 问题4：pip 版本号序列一致性

**§0第2点**
> `pip lock` 生成(25.1，2025-04-26)、`pip install -r pylock.toml` 消费(26.1，2026-04-26)

**§3 PEP 751表-pip行**
> pip（`pip lock`生成 25.1/2025-04-26 + `pip install -r pylock.toml`消费 26.1/2026-04-26，均实验性）

**§4迁移段**
> [无直接涉及pip版本的内容]

**笔记支撑**
- r1-pip.md [C4]: "pip 25.1（2025-04-26 发布）引入实验性 pip lock 命令实现 PEP 751"
- r2-pip-pylock-install.md [C1]: "pip 26.1 (2026-04-26) 添加实验性功能，支持通过 `-r pylock.toml`"

**一致性**：完全一致，版本和日期都准确。

---

#### 问题5：Workspace特性矩阵（D7）一致性

**§0第4点**
> 原生 workspace 三家有，两家没有：uv、PDM(2.28+，实验性)、pixi 都有官方 workspace 声明并共享单一锁文件；pip 完全没有；Poetry 只能靠 path dependency 手动拼。

**§2矩阵 Workspace行**
| | uv | pip | Poetry | PDM | pixi | conda |
| Workspace | `[tool.uv.workspace]`，members/exclude glob，单一锁文件 | 无原生概念，只有 `-e` 可编辑安装 | 无原生概念，靠 path dependency + `develop=true` | `[tool.pdm.workspace]`(v2.28+，实验性) | `[workspace]`(2024 年从`[project]`改名)+`[workspace.dependencies]` | 无，模型是多个独立 environment |

**笔记支撑**
- r1-uv.md [C19-21]: 有workspace机制、shared lockfile
- r1-pip.md [C14-15]: 无workspace、只有editable install
- r1-poetry.md [C19-20]: 无workspace、靠path dependency + develop=true
- r1-pdm.md [C9]: v2.28.0/实验性
- r1-pixi.md [C15]: [workspace]表是官方标准，2024年改名自[project]
- r1-conda.md [C16]: 无workspace概念

**一致性**：完全一致，所有细节都对应。

---

## 计数总结

- **supported**: 26 条
- **weak**: 2 条（主要是§0 vs §3关于uv PEP 751的矛盾表述）
- **unsupported**: 0 条
- **contradicted**: 0 条

**自洽检查**：发现 1 处主要不一致
- uv关于PEP 751导出/导入能力的表述在§0和§3之间有矛盾（§0说"只导出"，§3和笔记说"可导入"）

**其他不一致**：0 处（D2/D3/D7的其他表述在§0/§2/§3之间完全一致）

