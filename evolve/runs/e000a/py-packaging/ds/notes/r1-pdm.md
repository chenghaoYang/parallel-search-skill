# r1-pdm
question: PDM 在以下 12 个维度上现状分别是什么？
checked: https://pdm-project.org/latest/,https://github.com/pdm-project/pdm,https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md,https://raw.githubusercontent.com/pdm-project/pdm/main/README.md,https://raw.githubusercontent.com/pdm-project/pdm/main/pyproject.toml,https://pdm-project.org/latest/reference/configuration/,https://pdm-project.org/latest/usage/venv/,https://pdm-project.org/latest/usage/workspace/

## claims
- [C1] PDM 是"支持最新 PEP 标准的现代 Python 包管理器"，核心特点：快速依赖解析器（针对大型二进制发行版）、PEP 517 构建后端、PEP 621 项目元数据、灵活插件系统、Python 版本管理、集中式安装缓存（类 pnpm）。与 Poetry/Hatch 不同，PDM 不限于特定构建后端，用户可自由选择构建后端。 | src: https://github.com/pdm-project/pdm | quote: "A modern Python package and dependency manager supporting the latest PEP standards" | type: official
- [C2a] PDM 项目始终使用标准 PEP 621 `[project]` 表来定义项目元数据。`pdm init` 时添加 `name`、`version` 字段到 `[project]` 表。 | src: https://pdm-project.org/latest/usage/project/ | quote: "a name, version field to the pyproject.toml file, as well as a [build-system] table" | type: official
- [C2b] `[tool.pdm]` 表用于 PDM 特定配置，包含 `distribution` 字段（设为 true 时将项目视为库）。 | src: https://pdm-project.org/latest/usage/project/ | quote: "if it is set to true, PDM will treat the project as a library" | type: official
- [C3a] pdm.lock 格式为 TOML，用于锁定依赖版本。 | src: https://github.com/pdm-project/pdm | quote: "supports lockfiles" | type: official
- [C3b] PDM 支持 PEP 751 pylock.toml 格式。在 v2.26+ 版本实现导出功能，v2.29.0+ 尊重依赖组选择时导出到 pylock.toml。支持 pylock 作为备选锁文件格式（opt-in by config）。 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Support pylock as alternative lock format and make it opt-in by config. ([#3481]) ... Respect dependency group selection options when exporting to pylock.toml, producing a single-use lock file" | type: official
- [C4a] PDM 有原生 workspace 机制。在根 `pyproject.toml` 中通过 `[tool.pdm.workspace]` 表配置成员，使用 `members = ["packages/foo", "packages/bar", "tools/*"]` 语法，支持路径和通配符。 | src: https://pdm-project.org/latest/usage/workspace/ | quote: "[tool.pdm.workspace]members = [\"packages/foo\", \"packages/bar\", \"tools/*\"]" | type: official
- [C4b] 工作区在 v2.28.0+ 版本开始支持，标记为实验性功能。工作区成员被视为隐式可编辑依赖，成员间可按包名相互依赖。某些命令（pdm install/lock/sync）需从工作区根目录运行。 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Add experimental workspace support for managing local member projects in a shared root lock file. ([#1505])" | type: official
- [C5a] PDM 支持 `pdm python install` 命令下载并管理 Python 版本。使用 astral-sh 的 python-build-standalone 作为下载源。`pdm python install -v` 显示下载 URL，`pdm python find` 搜索已安装解释器。 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "The pdm python install -v command now shows the download URL for the Python interpreter. ([#3552])... Add pdm python find command to search for a python interpreter. ([#3389])" | type: official
- [C5b] `pdm use` 和 `pdm python install` 会考虑 requires-python（包括 pyproject.toml 中的版本要求）。 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "pdm use and pdm python install now take requires-python into account" | type: official
- [C6] 默认构建后端为 `pdm-backend`（在 PDM 项目自身 pyproject.toml 中设置为 `pdm.backend`）。PDM 允许用户自由选择任何 PEP 517 兼容的构建后端。 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/pyproject.toml | quote: "build-backend = \"pdm.backend\"" | type: official
- [C7] PDM 的依赖解析器特点：简单（simple）、快速（fast），主要针对大型二进制发行版优化。基于 PEP 标准的解析策略。 | src: https://github.com/pdm-project/pdm | quote: "Simple and fast dependency resolver, mainly for large binary distributions" | type: official
- [C8a] PDM 默认使用虚拟环境（venv），而非 PEP 582 `__pypackages__`。文档明确指出："虚拟环境被认为比 PEP 582 更成熟，生态系统支持更好"。 | src: https://pdm-project.org/latest/usage/venv/ | quote: "Compared to PEP 582, virtual environments are considered more mature and have better support in the Python ecosystem" | type: official
- [C8b] PEP 582 仍受支持但非默认。可通过 `pdm config python.use_venv false` 禁用虚拟环境模式，此时 PEP 582 模式将被使用。PEP 582 未被移除/废弃，仅是优先级下降。 | src: https://pdm-project.org/latest/usage/venv/ | quote: "PEP 582 mode will always be used" (when venv disabled) | type: official
- [C9a] PDM 支持多种认证方式：keyring（系统密钥管理）、`pdm config` 命令行配置、用户名/密码、客户端证书、SSL 验证、环境变量（PDM_PYPI_URL 等）。 | src: https://pdm-project.org/latest/reference/configuration/ | quote: "authentication (username/password), and client certificates ... Supports custom package sources and mirrors" | type: official
- [C9b] 虚拟环境默认位置由 `venv.in_project` 配置控制，默认为 True，在项目根创建 `.venv`。可配置其他位置。 | src: https://pdm-project.org/latest/reference/configuration/ | quote: "venv.in_project defaults to True, creating .venv in project root" | type: official
- [C10] CI 缓存：PDM 官方文档中的 CI/CD 指南页面返回 404，具体推荐方案待确认。pdm.lock 文件本身作为重要缓存文件，应在 CI 中版本控制。 | src: https://pdm-project.org/latest/guides/ci-cd/ | quote: "404 Not Found" | type: official
- [C11] PDM 提供 `pdm import` 命令支持从其他包管理器迁移。支持来源：Pipenv (Pipfile)、Poetry (pyproject.toml)、Flit、pip (requirements.txt)、setuptools (setup.py)。v2.29.1+ 版本对 Poetry 约束转换持续优化。 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Convert Poetry tilde constraints with fewer than three components to the bounds Poetry means... Keep importing a Poetry project when an author or maintainer entry does not fit the Name <email> pattern" | type: official
- [C12a] PDM 首发于 2019 年底（GitHub 仓库创建日期：2019-12-27）。当前主版本为 v2，最新版本为 2.29.2（2026-09-17）。 | src: https://api.github.com/repos/pdm-project/pdm | quote: "created_at: 2019-12-27T03:50:57Z" | type: official
- [C12b] PDM 项目由 pdm-project 组织维护，原始作者为 Frost Ming（GitHub @frostming）。项目高度活跃：3333+ commits 主分支、8 个开放 PR、38 个开放 issue、定期更新 CHANGELOG。 | src: https://github.com/pdm-project/pdm | quote: "Maintainer: pdm-project organization... pushed_at: 2026-09-22T00:57:57Z" | type: official
- [C12c] 项目标签包括 hacktoberfest、package-manager、packaging、pep582、pep621、python、workflow，表明对 PEP 标准的重点支持。 | src: https://api.github.com/repos/pdm-project/pdm | quote: "topics: [hacktoberfest, package-manager, packaging, pep582, pep621, python, workflow]" | type: official

## conflicts
无明显冲突。PEP 582 仍受支持但优先级下降（官方文档明确说明），而非完全废弃。

## gaps
- C10 (CI 缓存)：官方文档 /guides/ci-cd/ 页面返回 404，无法确认官方推荐的 GitHub Actions 缓存方式或具体实践指南。
- 尚未获得官方文档中关于 `pdm.lock` 具体存储格式细节（TOML schema）的页面。
- 未找到 `pdm init` 命令详细输出和默认 `[build-system]` 配置的完整参考。

## leads
- PEP 582 主题标签仍存在于项目元数据中，但已不是默认虚拟环境机制，反映了 PDM 的历史演变（原主打 PEP 582，当前已转向 venv）
- workspace 功能仍为实验性（v2.28.0+），后续迭代中可能成为稳定特性或有 API 变化
- pylock.toml (PEP 751) 支持在 v2.26+ 开始推出，表明 PDM 对新 PEP 标准的快速采用
