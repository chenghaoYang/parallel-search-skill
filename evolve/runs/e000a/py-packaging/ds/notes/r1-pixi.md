# r1-pixi
question: pixi（prefix.dev 出品）在以下 12 个维度上现状分别是什么？
checked: https://pixi.prefix.dev/latest/, https://github.com/prefix-dev/pixi, https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md, https://pixi.prefix.dev/latest/build/workspace/, https://pixi.prefix.dev/latest/python/pyproject_toml/, https://github.com/prefix-dev/setup-pixi, https://pixi.prefix.dev/latest/deployment/authentication/

## claims
- [C1] pixi 定位：建立在 conda 生态基础之上的跨平台、多语言包管理和工作流工具，提供如 Cargo/npm 般的开发体验，是 conda 的现代化补充而非竞争 | src: https://github.com/prefix-dev/pixi | quote: "a cross-platform, multi-language package manager and workflow tool built on the foundation of the conda ecosystem" | type: official
- [C2] pyproject.toml 支持通过 `[tool.pixi.*]` 命名空间遵循 PEP 621，pixi 理解 `requires_python` 和 `dependencies` 字段，自动转换为 PyPI 依赖 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "Pixi recognizes several standard Python project fields: requires-python, dependencies, project.optional-dependencies" | type: official
- [C3] pixi.toml 仍为首选配置方式，pyproject.toml 支持为实验性功能（v0.18.0 起引入），两种配置关系为补充而非替代 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "we don't advise to use the pyproject.toml file for anything else than Python projects; the pixi.toml is better suited for other types" | type: official
- [C4] pixi.lock 格式基于 rattler-lock-v6，是单一多平台锁文件（含 linux-64、osx-arm64、win-64 等平台），非 conda-lock 格式 | src: https://github.com/basnijholt/pixi-to-conda-lock | quote: "pixi.lock file is a single file that contains multiple platforms, with each platform getting its exact package build" | type: official
- [C5] pixi.lock 为单个多平台锁文件，不支持 PEP 751 pylock.toml，官方未见迁移计划 | src: https://peps.python.org/pep-0751/ | quote: "PEP 751 pylock.toml" | type: secondary
- [C6] pixi workspace 机制原生支持多包管理（通过 `[workspace.dependencies]` 声明共享依赖）、顶级 pixi.toml 管理多个包、共享单一 lockfile | src: https://pixi.prefix.dev/latest/build/workspace/ | quote: "A workspace is a self-contained project that defines its dependencies, tasks, and one or more environments" | type: official
- [C7] workspace 为核心特性，v0.48 起支持多包构建模式，v0.79 添加 `pixi workspace dependencies` CLI | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md | quote: "v0.79.0 - Added pixi workspace dependencies CLI command" | type: official
- [C8] Python 版本通过 conda channel（如 conda-forge）安装，pixi 仅管理依赖解析，不单独维护 Python 版本选项 | src: https://pixi.prefix.dev/latest/python/tutorial/ | quote: "requires_python field automatically interpreted as Python dependency" | type: official
- [C9] pyproject.toml 默认构建后端为 hatchling（使用 `pixi init --format pyproject` 时），pixi.toml 项目无特定默认后端 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "pixi defaults to hatchling as the build backend when using pyproject.toml" | type: official
- [C10] pixi 依赖解析器为 rattler（Rust 实现，基于 resolvo CDCL SAT 求解器），比 conda 快 10 倍、比 micromamba 快 3 倍 | src: https://prefix.dev/blog/the_new_rattler_resolver | quote: "Pixi is built on top of rattler, a modern dependency resolver written in Rust" | type: official
- [C11] 支持混合 conda 和 PyPI 依赖在同一项目，通过 `[dependencies]` 和 `[pypi-dependencies]` 字段；conda-first 解析策略 | src: https://pixi.prefix.dev/latest/concepts/conda_pypi/ | quote: "PyPI dependencies and conda dependencies can be mixed in the same Pixi project" | type: official
- [C12] 环境默认位置为 `.pixi/envs/`（项目相对路径），支持通过 PIXI_HOME 环境变量自定义全局工具位置 | src: https://pixi.prefix.dev/latest/workspace/environment/ | quote: "All Pixi environments are by default located in the .pixi/envs directory" | type: official
- [C13] pixi 支持 Bearer Token、Conda Token、Basic HTTP 认证；支持 keyring 和 JSON 文件存储凭证 | src: https://pixi.prefix.dev/latest/deployment/authentication/ | quote: "The different options are token, conda-token and username + password" | type: official
- [C14] 官方推荐 prefix-dev/setup-pixi GitHub Action 用于 CI，内置项目环境缓存（基于 pixi.lock 哈希）和全局环境缓存（月度过期） | src: https://github.com/prefix-dev/setup-pixi | quote: "project environment caching is enabled if a pixi.lock file is present, and it will use the pixi.lock file to generate a hash" | type: official
- [C15] 迁移路径：conda 项目可用 `pixi init --import ./myenv.yml`；conda-lock 项目可用 `conda-lock render-lock-spec --kind=pixi.toml` | src: https://conda.github.io/conda-lock/pixi-migration/ | quote: "conda-lock render-lock-spec --kind=pixi.toml" for pixi.toml generation | type: official
- [C16] pixi 首发于 2023-06-26（v0.0.4），当前最新版本 v0.81.0（2026-09-15），由 prefix.dev（Costanoa Ventures 投资）维护，GitHub 7.8k 星、活跃开发 | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md | quote: "v0.0.4 - 2023-06-26" and "v0.81.0 - 2026-09-15" | type: official
- [C17] PEP 621 `[project]` 表：通过 `[tool.pixi.project]` 支持（不是直接 `[project]`），pyproject.toml 中标准 PEP 621 字段如 `dependencies` 自动映射为 PyPI 依赖 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "[project] becomes [tool.pixi.project], dependencies field automatically maps to pypi-dependencies" | type: official
- [C18] 多个配置方式：pixi.toml（完整支持）、pyproject.toml（Python 项目、带 `[tool.pixi]`）、脚本级 PEP 723（v0.76 实验性支持）| src: https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md | quote: "v0.76.0 - A single Python file can now carry its own environment via PEP 723" | type: official

## conflicts
- pixi.lock 格式描述：某些文档提及"基于 conda-lock 格式"，但官方实现为独立的 rattler-lock-v6 格式，通过 pixi-to-conda-lock 工具可转换，表明格式不同但兼容 | src: https://github.com/basnijholt/pixi-to-conda-lock vs https://pixi.prefix.dev/ | quote: "pixi-to-conda-lock converts pixi.lock to conda-lock.yml" implies different formats | type: secondary

## gaps
- [G1] 是否计划支持 PEP 751 pylock.toml 锁文件格式（仅找到其他工具的支持情况）
- [G2] `[project]` 表在 pixi.toml 中的具体字段支持清单（name、version、description 等具体遵循情况）
- [G3] conda-pypi-map 映射机制的详细配置示例和版本历史
- [G4] pixi.lock 是否支持跨架构锁定（ARM/x86 混合环境）的具体情况

## leads
- pixi v0.80 引入 conda-script 实验性支持（可在脚本中嵌入依赖），可能影响未来配置方式的演进方向
- pixi workspace 特性仍标注为 preview/beta（pixi-build），应关注稳定化时间表
- Python 版本管理依赖 conda channel，与 uv 自带版本管理器不同，建议与其他工具对比时详细说明差异
