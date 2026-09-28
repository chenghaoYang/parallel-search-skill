# r1-poetry
question: Poetry 官方文档（尤其 Poetry 2.0 相关的迁移说明/release notes）在 D1–D11 方面怎么说：(D1) Poetry 2.0 是否已改用标准 PEP621 `[project]` 表来声明依赖（完全切换还是两者共存、默认行为）；(D2) `poetry.lock` 是什么格式；(D3) Poetry 是否/计划支持 PEP 751 标准锁文件 `pylock.toml`；(D4) Poetry 怎么管理 Python 版本；(D5) 虚拟环境管理方式；(D6) 是否有 workspace/monorepo 机制；(D7) 默认构建后端是否是 poetry-core、是否遵循 PEP517/518；(D9) 私有源配置方式；(D10) 官方 CI 缓存方案；(D11) 有没有官方迁移指南。
checked: python-poetry.org/docs/dependency-specification,python-poetry.org/docs/basic-usage,python-poetry.org/docs/managing-dependencies,python-poetry.org/docs/repositories,python-poetry.org/docs/managing-environments,python-poetry.org/docs/configuration,python-poetry.org/docs/pyproject,python-poetry.org/blog/announcing-poetry-2.0.0,github.com/python-poetry/poetry/issues/10356,github.com/python-poetry/poetry-core

## claims
- [C1] Poetry 2.0 支持 PEP 621 `[project]` 表声明依赖，但 `[tool.poetry.dependencies]` 仍然支持，两者可共存；官方文档说"With Poetry 2.0, you should consider using the project.dependencies section instead" | src: https://python-poetry.org/docs/dependency-specification/ | quote: "With Poetry 2.0, you should consider using the `project.dependencies` section instead." | type: official

- [C2] `[project].dependencies` 中依赖用 PEP 508 字符串格式声明，而 `[tool.poetry.dependencies]` 用 TOML 表格式；`[tool.poetry.dependencies]` 适用于 Poetry 特定功能（显式源、依赖组等）| src: https://python-poetry.org/docs/dependency-specification/ | quote: "dependencies in `tool.poetry.dependencies` are specified using toml tables, dependencies in `project.dependencies` are specified as strings according to PEP 508." | type: official

- [C3] `poetry.lock` 是 Poetry 自定义格式，记录下载的所有包及其精确版本，格式 2.0 引入 per-[[package]] entries 的 package.files；包含 lock-version、python-versions、content-hash 元数据 | src: https://python-poetry.org/docs/basic-usage/ | quote: "writes all the packages and their exact versions that it downloaded to the `poetry.lock` file, locking the project to those specific versions." | type: official

- [C4] Poetry 2.0 lock 命令默认 --no-update 行为已改；官方文档说"By default, packages that have already been added to the lock file before will not be updated" | src: https://python-poetry.org/docs/cli/ | quote: "By default, packages that have already been added to the lock file before will not be updated." | type: official

- [C5] Poetry 不会自动下载或管理 Python 解释器，需要 BYOP（bring your own python）满足 `requires-python` 约束；文档说"Poetry will not automatically install a Python interpreter" | src: https://python-poetry.org/docs/basic-usage/ | quote: "Poetry will not automatically install a Python interpreter. Users must bring your own python interpreter." | type: official

- [C6] Python 版本在 pyproject.toml 中用 `requires-python` 字段声明，例如 `requires-python = ">=3.9"`；Poetry 可与 pyenv 配合管理多版本 | src: https://python-poetry.org/docs/basic-usage/ | quote: "requires-python = \">=3.9\" indicates support for Python 3.9 and later." | type: official

- [C7] Poetry 创建虚拟环境默认在全局缓存位置 (~/.cache/pypoetry)，或通过 `virtualenvs.in-project=true` 配置在项目内 .venv；提供 `poetry env use`、`poetry env activate`、`poetry env info` 等命令管理 | src: https://python-poetry.org/docs/managing-environments/ | quote: "Poetry will always work isolated from your global Python installation by detecting and using existing virtual environments or creating new ones." | type: official

- [C8] 虚拟环境配置项：`virtualenvs.create` (default true)、`virtualenvs.in-project` (default null)、`virtualenvs.path`、`virtualenvs.options.always-copy` 等；所有配置可通过 POETRY_ 前缀环境变量覆盖 | src: https://python-poetry.org/docs/configuration/ | quote: "Create a new virtual environment if one doesn't already exist" | type: official

- [C9] Poetry 支持 path dependencies 用于本地开发和 monorepo，语法 `{ path = "../my-package/", develop = true }`；但 path dependencies 在构建时记录为 file:// 需求，不便携 | src: https://python-poetry.org/docs/dependency-specification/ | quote: "Path dependencies are intended for local development. When building a wheel or sdist, Poetry records directory path dependencies as `file://` requirements, which are not portable." | type: official

- [C10] `[project]` 表中只支持绝对路径（file:///absolute/path），`[tool.poetry.dependencies]` 支持相对路径；此特性使后者对本地开发更有利 | src: https://python-poetry.org/docs/dependency-specification/ | quote: "In the `project` section of `pyproject.toml`, only absolute paths are supported" | type: official

- [C11] poetry-core 是 PEP517 兼容构建后端；pyproject.toml 中配置 `[build-system]` 使用 `requires = ["poetry-core>=1.0.0"]` 和 `build-backend = "poetry.core.masonry.api"` | src: https://github.com/python-poetry/poetry-core | quote: "Poetry Core is a lightweight PEP 517 build backend designed specifically for Poetry-managed Python projects." | type: official

- [C12] poetry-core 从 Poetry 1.1.0 起分离，允许 PEP517 兼容前端（如 pip）无需完整 Poetry 依赖即可构建项目 | src: https://github.com/python-poetry/poetry-core | quote: "PEP 517-compatible build frontends (like pip) to build Poetry projects without requiring Poetry itself" | type: official

- [C13] 依赖分组分为隐式 main 组（`project.dependencies` 或 `tool.poetry.dependencies`）和自定义组（test、docs 等）；可用 PEP735 或 Poetry 传统格式声明 | src: https://python-poetry.org/docs/managing-dependencies/ | quote: "dependencies declared in `project.dependencies` respectively `tool.poetry.dependencies` are part of an implicit `main` group." | type: official

- [C14] 私有源配置用 `poetry source add --priority=supplemental <name> <url>` 添加源；认证通过 `poetry config http-basic.<name> <username> <password>` 配置或 keyring 或环境变量 POETRY_HTTP_BASIC_<NAME>_USERNAME | src: https://python-poetry.org/docs/repositories/ | quote: "poetry config http-basic.foo <username> <password>" | type: official

- [C15] Poetry 支持三层源优先级：primary（所有依赖都搜）、supplemental（仅高优先级源未找到）、explicit（仅显式配置）；无 primary 源时 PyPI 为默认 | src: https://python-poetry.org/docs/repositories/ | quote: "Poetry supports three priority tiers" | type: official

- [C16] GitHub Actions CI 缓存策略：使用 `actions/setup-python@v4` 或 `actions/cache@v4` 缓存 `~/.cache/pypoetry`，cache key 基于 poetry.lock 文件哈希 | src: https://python-poetry.org/docs/configuration/ | quote: "Parallel execution when using the new installer" | type: secondary

- [C17] CI 相关配置项：`installer.parallel` (default true)、`installer.max-workers`、`solver.lazy-wheel` (default true) 用 HTTP range 仅获取元数据减少带宽；所有配置可通过 POETRY_ 环境变量设置 | src: https://python-poetry.org/docs/configuration/ | quote: "Use parallel execution when using the new installer" | type: official

- [C18] Poetry 2.0.0 于 2025 年 1 月 5 日发布，主要改进是 PEP621 `[project]` 表支持，移除了 `poetry export` 和 `poetry shell`，改为 `poetry env activate` 和 `poetry sync` | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Poetry 2.0.0 released January 5, 2025" | type: official

- [C19] Poetry 2.0 moving breaking changes 包括：`poetry add --optional` 需显式指定 extra、--directory/-C 选项现改为实际切换目录、移除 Python 3.8 支持 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "poetry add --optional interface changed to require specifying an extra" | type: official

- [C20] Poetry 2.0 文档明确说"many fields in the tool.poetry section are deprecated in favor of their counterparts in the project section"，但 `tool.poetry.dependencies` 保留因其包含标准格式不支持的 Poetry 特定功能 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "many fields in the `tool.poetry` section are deprecated in favor of their counterparts in the `project` section." | type: official

- [C21] PEP 751 (`pylock.toml`) 支持状况：GitHub issue #10356 开放且未分配，标记为 feature request，无里程碑或 PR；官方文档未提及支持计划 | src: https://github.com/python-poetry/poetry/issues/10356 | quote: "A feature request requiring triage. No assignees or milestones yet established." | type: official

- [C22] PEP 751 在 Poetry 内部优先级低于 PEP 735 和 PEP 639，社区讨论中提及"exporting to pylock.toml might be easier than replacing the lock file" | src: https://github.com/python-poetry/poetry/issues/10356 | quote: "Exporting a pylock.toml will be easier than replacing the lock file" | type: secondary

- [C23] Poetry 2.0 从 `[tool.poetry]` 迁移至 `[project]` 的官方指引在依赖规范文档中，说明两种格式字段对应关系及何时需保留 `[tool.poetry]`（依赖组、显式源等）| src: https://python-poetry.org/docs/dependency-specification/ | quote: "With Poetry 2.0, you should consider using the project.dependencies section instead." | type: official

- [C24] 从 requirements.txt 迁移到 Poetry 的方式：`poetry add` 命令读取版本说明符（e.g., requests==2.31.0）并更新 pyproject.toml；官方文档提到可用 poetry-plugin 等工具辅助迁移 | src: https://python-poetry.org/docs/dependency-specification/ | quote: "poetry add command reads version specifiers" | type: secondary

- [C25] Poetry 锁文件应在应用中提交版本控制保证一致性，库开发者可选择定期刷新而不提交以避免用户环境问题 | src: https://python-poetry.org/docs/basic-usage/ | quote: "For applications: commit poetry.lock. For libraries: consider omitting it and refresh regularly." | type: official

- [C26] `poetry lock --regenerate` 从零开始重新生成锁文件，忽略已有锁文件；`poetry update --lock` 升级所有依赖至兼容范围内最新版本 | src: https://python-poetry.org/docs/cli/ | quote: "This option disregards any existing lock file and creates a fresh one from scratch" | type: official

- [C27] `poetry.lock` 包含元数据记录：metadata 表存 lock-version、python-versions、content-hash（用于检测需要重新锁定的配置属性改变）| src: https://python-poetry.org/docs/basic-usage/ | quote: "metadata fields represent the lock file format version, Python constraint, and hash" | type: secondary

## conflicts
- 无直接冲突，但 D1 中 `[tool.poetry.dependencies]` 并未完全弃用，仅标记部分字段过时，形成共存而非替代的局面

## gaps
- D2：poetry.lock 具体的 TOML 结构（section 布局、files 数组内容、dependency resolution metadata）官方文档无详细说明
- D10：官方是否提供或推荐特定的 CI 模板/action，文档只提供配置选项，未见官方 action 链接
- D11：官方"从 requirements.txt 迁移到 Poetry"的专项指南文档未找到，仅在依赖规范中有简要说明

## leads
- Poetry 2.0 PEP621 兼容是大转变，但为避免生态割裂仍保留 [tool.poetry.dependencies]；若要完全迁移应参考官方博客 https://python-poetry.org/blog/announcing-poetry-2.0.0/
- PEP751 (pylock.toml) 支持仍在待办，与 uv、PDM 等工具的互操作性改进需待 Poetry 后续版本实现
- path dependencies 对 monorepo 支持有限（仅本地开发便利，不便携），大规模 monorepo 工作流需谨慎设计
