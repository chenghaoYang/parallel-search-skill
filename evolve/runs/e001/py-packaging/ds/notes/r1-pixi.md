# r1-pixi
question: pixi在10个维度上的官方文档说法：定位/生态范围、清单标准、锁文件、解析器、Python版本管理、构建后端、Workspace/monorepo、私有源认证、CI缓存、迁移路径
checked: https://pixi.prefix.dev/latest/, https://pixi.prefix.dev/latest/reference/pixi_manifest/, https://pixi.prefix.dev/latest/python/pyproject_toml/, https://pixi.prefix.dev/latest/workspace/lock_file/, https://pixi.prefix.dev/latest/concepts/conda_pypi/, https://pixi.prefix.dev/latest/deployment/authentication/, https://pixi.prefix.dev/latest/switching_from/poetry/, https://pixi.prefix.dev/latest/build/workspace_dependencies/, https://github.com/prefix-dev/pixi, https://prefix.dev/blog/pypi_support_in_pixi

## claims

- [C1] D1-定位：pixi 是"a fast, modern, and reproducible package manager for developers" 管理任何编程语言的依赖 | src: https://pixi.prefix.dev/latest/ | quote: "Pixi is a fast, modern, and reproducible package manager for developers of all backgrounds" | type: official

- [C2] D1-生态范围：pixi 管理 conda 和 PyPI 两个生态的包，"defaults to the biggest Conda package repository, conda-forge, which contains over 30,000 packages" | src: https://pixi.prefix.dev/latest/ | quote: "defaults to the biggest Conda package repository, conda-forge, which contains over 30,000 packages" | type: official

- [C3] D1-技术基础：pixi 基于 conda 生态，"powered by Rattler, described as Everything conda but built in Rust" | src: https://pixi.prefix.dev/latest/ | quote: "powered by Rattler, Everything conda but built in Rust" | type: official

- [C4] D2-清单文件：支持 pixi.toml 或 pyproject.toml，后者用 [tool.pixi] 前缀 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "The pixi.toml is the workspace manifest... pyproject.toml file... need to prepend the tables with tool.pixi" | type: official

- [C5] D2-pyproject.toml详情：不建议非Python项目使用 pyproject.toml，"We don't advise to use the pyproject.toml file for anything else than Python projects" | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "We don't advise to use the pyproject.toml file for anything else than Python projects, the pixi.toml is better suited" | type: official

- [C6] D3-锁文件格式：pixi.lock 包含环境定义和包元数据，"contains two main sections: Environments listing packages... Package definitions with metadata" | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "pixi.lock file contains two main sections: Environments listing packages for different platforms, Package definitions with metadata" | type: official

- [C7] D3-同时锁定：pixi.lock 同时锁定 conda 和 PyPI 包，"all packages in the manifest file are in the lock file... for both conda and pypi packages" | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "All packages in the manifest file are in the lock file... versions... compatible with the requirements... both conda and pypi packages" | type: official

- [C8] D4-双解析器架构：pixi 先用 resolvo 解决 conda 依赖，再用 uv 的 PubGrub 解决 PyPI | src: https://pixi.prefix.dev/latest/concepts/conda_pypi/ | quote: "resolution process follows three sequential steps: Resolve conda dependencies using the resolvo solver... Resolve remaining PyPI dependencies using uv library's PubGrub solver" | type: official

- [C9] D4-uv集成方式：pixi 不安装 uv 工具，而是作为库集成，"both tools are built in Rust, it is used as a library" | src: https://prefix.dev/blog/pypi_support_in_pixi | quote: "Pixi doesn't install uv (the tool) itself: because both tools are built in Rust, it is used as a library" | type: official

- [C10] D4-conda优先策略：同时声明 conda 和 PyPI 时优先装 conda 包，"Pixi will install the conda package (and not the PyPI package) if both are available" | src: https://pixi.prefix.dev/latest/concepts/conda_pypi/ | quote: "Pixi will install the conda package (and not the PyPI package) if both are available and specified as dependencies" | type: official

- [C11] D5-Python版本管理：作为 conda 包在依赖中声明，自动从 requires-python 字段转换 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "Pixi recognizes the requires-python field and automatically converts it into a Python dependency" | type: official

- [C12] D5-多版本支持：通过 feature 定义多个 Python 版本 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "Create flexible setups by defining features... [feature.name]... composing environments" | type: official

- [C13] D6-构建后端：支持 PEP 517/518，使用 pixi-build-python 后端 | src: https://pixi.prefix.dev/latest/build/backends/pixi-build-python/ | quote: "requires a PEP 517/518 compliant Python project with pyproject.toml" | type: official

- [C14] D6-默认构建系统：无 [build-system] 时默认用 setuptools，"Pixi will fall back to uv's default, which is equivalent to requires = setuptools >= 40.8.0" | src: https://pixi.prefix.dev/latest/build/backends/pixi-build-python/ | quote: "If the pyproject.toml file does not contain any [build-system] section, Pixi will fall back to uv's default, equivalent to setuptools" | type: official

- [C15] D7-Workspace官方概念：[workspace] 表是官方标准概念，2024年前叫 [project]，已改名 | src: https://github.com/prefix-dev/pixi/pull/3300 | quote: "Rename remaining instances of project to pixi workspace... changed section headers from [project] to [workspace]" | type: official

- [C16] D7-Workspace依赖特性：[workspace.dependencies] 用于 monorepo 共享依赖版本 | src: https://pixi.prefix.dev/latest/build/workspace_dependencies/ | quote: "packages typically share many of the same dependency versions... centralized dependency pool" | type: official

- [C17] D8-Conda认证方式：支持 OAuth/OIDC、Token、Basic Auth、S3，命令 pixi auth login | src: https://pixi.prefix.dev/latest/deployment/authentication/ | quote: "OAuth/OIDC (recommended), Token Authentication, Basic HTTP Authentication, S3 Authentication" | type: official

- [C18] D8-Conda具体命令：`pixi auth login prefix.dev` 或 `pixi auth login --token <TOKEN>` | src: https://pixi.prefix.dev/latest/deployment/authentication/ | quote: "pixi auth login prefix.dev or pixi auth login --token <TOKEN>" | type: official

- [C19] D8-PyPI认证方式：Keyring 或 .netrc 文件，不支持私有仓库 | src: https://pixi.prefix.dev/latest/deployment/authentication/ | quote: "Two methods: Keyring uses Python keyring library... .netrc file... Currently, pixi doesn't support private PyPI repositories" | type: official

- [C20] D8-凭证存储位置：Windows用Credential Manager、macOS用Keychain、Linux用GNOME Keyring，fallback ~/.rattler/credentials.json | src: https://pixi.prefix.dev/latest/deployment/authentication/ | quote: "Windows Credential Manager, macOS Keychain, Linux GNOME Keyring, fallback ~/.rattler/credentials.json" | type: official

- [C21] D9-CI缓存默认启用：setup-pixi 当 pixi.lock 存在时默认启用缓存 | src: https://github.com/marketplace/actions/setup-pixi | quote: "Project environment caching is enabled by default if a pixi.lock file is present" | type: official

- [C22] D9-缓存key格式：global-cache-key 按月过期，常规缓存基于环境hash | src: https://github.com/marketplace/actions/setup-pixi | quote: "global-cache-key expires at end of every month... full cache keys formatted as <cache-key><arch>-<hash>" | type: official

- [C23] D9-缓存自定义选项：cache-key、global-cache-key、cache-write 参数可控缓存行为 | src: https://github.com/marketplace/actions/setup-pixi | quote: "customize cache-key and global-cache-key input arguments... cache-write to restrict when cache is saved" | type: official

- [C24] D10-Conda迁移命令：`pixi init --import ./myenv.yml` 导入现有 conda 环境 | src: https://pixi.prefix.dev/latest/switching_from/poetry/ | quote: "pixi init --import ./myenv.yml should bring all dependencies from existing conda environment.yml" | type: official

- [C25] D10-Poetry迁移指南：官方提供 Poetry→Pixi 迁移文档，比较命令和配置差异 | src: https://pixi.prefix.dev/latest/switching_from/poetry/ | quote: "Migration Guide: Poetry to Pixi... Key Advantages... Essential Command Replacements" | type: official

- [C26] D10-依赖语法差异：Poetry 用 ^1.2.3 或 ~1.2.3，pixi 用 >=1.2.3 <2.0.0 | src: https://pixi.prefix.dev/latest/switching_from/poetry/ | quote: "Pixi uses different constraint operators... Instead of ^1.2.3 use semantic range notation like >=1.2.3 <2.0.0" | type: official

- [C27] D10-并行支持两种工具：可同时保留 Poetry 和 Pixi 配置以逐步迁移 | src: https://pixi.prefix.dev/latest/switching_from/poetry/ | quote: "You can support both tools simultaneously by duplicating dependencies between tool.poetry.dependencies and tool.pixi.pypi-dependencies" | type: official

- [C28] D2-PyPI选项：pyproject.toml 中标准 dependencies 字段变成 PyPI 依赖 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "The standard dependencies field becomes PyPI dependencies in Pixi" | type: official

- [C29] D2-可选依赖自动转换：pyproject.toml 的 [project.optional-dependencies] 和 [dependency-groups] 自动转为 Pixi features | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "Pixi automatically interprets both optional-dependencies and dependency-groups as Pixi features" | type: official

- [C30] D3-锁文件自动管理：pixi install/add/remove/run/shell 时自动更新锁文件 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "Pixi automatically updates the lock file when running commands like install, add, remove, run, or shell" | type: official

## conflicts
无

## gaps
- D7: 是否存在 [project] 表的兼容模式或废弃通知（仅知道已改名为 [workspace]）
- D8: PyPI 私有仓库是否有后续计划，或完整的认证支持细节
- D3: pixi.lock 与 PEP 751 pylock.toml 的标准兼容性是否明确说明

## leads
- pixi-build-python 为完整构建链的入口（涉及源包构建、conda 包生成、跨语言支持）
- Workspace 依赖（[workspace.dependencies]）是 monorepo 特性的核心，2024 后新增
- 双解析器架构（resolvo+uv）是 pixi 和 conda/Poetry 等工具的根本差异
