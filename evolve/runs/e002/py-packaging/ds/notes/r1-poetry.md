# r1-poetry
question: Poetry（尤其 2.x）在锁文件、workspace/monorepo、Python 版本管理、构建后端、依赖解析与速度、私有源配置、全局工具运行、迁移路径、生态定位这些维度上，官方文档/changelog 是怎么说的？
checked: https://python-poetry.org/docs/pyproject/,https://python-poetry.org/docs/managing-environments/,https://python-poetry.org/docs/repositories/,https://python-poetry.org/docs/basic-usage/,https://github.com/python-poetry/poetry/releases/tag/2.0.0,https://github.com/python-poetry/poetry/issues/10356,https://python-poetry.org/docs/dependency-specification/,https://python-poetry.org/docs/managing-dependencies/,https://python-poetry.org/,https://python-poetry.org/docs/cli/

## claims
- [C1] Poetry 2.0.0（发布 2025-01-05）新增 PEP 621 [project] 表支持 | src: https://github.com/python-poetry/poetry/releases/tag/2.0.0 | quote: "Add support for the `project` section in the `pyproject.toml` file according to PEP 621" | type: official
- [C2] 构建系统使用 `poetry-core` 实现 PEP 517，配置为 `build-backend = "poetry.core.masonry.api"` | src: https://python-poetry.org/docs/pyproject/#build-system | quote: "PEP-517 introduces a standard way to define alternative build systems to build a Python project" | type: official
- [C3] poetry.lock 文件在首次 `poetry install` 时自动生成，记录所有包的确切版本 | src: https://python-poetry.org/docs/basic-usage/#poetry-lock | quote: "When Poetry has finished installing, it writes all the packages and their exact versions that it downloaded to the `poetry.lock` file" | type: official
- [C4] Poetry 不下载或安装 Python 解释器，仅从已安装版本中选择 | src: https://python-poetry.org/docs/managing-environments/#managing-python-versions | quote: "if your project requires a newer Python than is available with your system, users should use external tools like pyenv" | type: official
- [C5] `poetry env use` 命令用于指定项目使用的 Python 版本 | src: https://python-poetry.org/docs/managing-environments/ | quote: "users can explicitly specify which Python version to use via the `env use` command" | type: official
- [C6] 路径依赖支持本地包开发（`path` 属性与 `develop=true`），但记录为 `file://` URL，不可移植 | src: https://python-poetry.org/docs/dependency-specification/#path-dependencies | quote: "Path dependencies are intended for local development. When building a wheel or sdist, Poetry records directory path dependencies as `file://` requirements" | type: official
- [C7] 私有源通过 `[[tool.poetry.source]]` 配置，字段包括 name、url、priority（primary/supplemental/explicit） | src: https://python-poetry.org/docs/repositories/ | quote: "Package sources configured as supplemental are only searched if no other (higher-priority) source yields a compatible package distribution" | type: official
- [C8] 认证方式：`poetry config http-basic.<name> <user> <pwd>` 或 `poetry config pypi-token.<name> <token>`，支持环境变量 | src: https://python-poetry.org/docs/repositories/#using-a-private-repository | quote: "poetry config http-basic.foo <username> <password>" | type: official
- [C9] Poetry 定位为"Python packaging and dependency management made easy"，提供依赖管理、环境隔离、打包、发布功能 | src: https://python-poetry.org/ | quote: "Poetry is a tool for dependency management and packaging in Python" | type: official
- [C10] Poetry 无全局工具运行命令（如 uvx/pipx），`poetry run` 需要项目 pyproject.toml | src: https://python-poetry.org/docs/cli/ | quote: "`run` command operates within a project's virtualenv context and requires an active Poetry project" | type: official
- [C11] PEP 751（pylock.toml 标准）支持在 GitHub issue #10356 中被提议但未实现，状态为开放（last updated 2026-03-10） | src: https://github.com/python-poetry/poetry/issues/10356 | quote: "Support PEP 751 (`pylock.toml` standard)" | type: official
- [C12] [project] 与 [tool.poetry] 并存时，[project.dependencies] 用于构建元数据，[tool.poetry.dependencies] 用于增强锁定 | src: https://python-poetry.org/docs/dependency-specification/ | quote: "When both are specified, `project.dependencies` are used for metadata when building the project, `tool.poetry.dependencies` is only used to enrich" | type: official
- [C13] 可选依赖推荐使用 PEP 621 的 `[project.optional-dependencies]` 而非 `[tool.poetry.extras]` | src: https://python-poetry.org/docs/pyproject/#extras | quote: "Extras Definition...in `project.optional-dependencies` (recommended modern approach)" | type: official

## conflicts
- 关于 [project] 表的向后兼容性：官方文档说明 Poetry 2.0 支持两种写法并存，但未明确说明 [tool.poetry] 何时将被完全弃用。

## gaps
- D2：是否有原生 workspace/monorepo 支持（多包共享单一锁文件）——官方文档未提及专门的 workspace 配置，仅涉及路径依赖
- D5：依赖解析器的具体实现语言/算法特点，以及官方对「Poetry 解析慢」说法的回应
- D8：从 setup.py/requirements.txt 迁移到 Poetry 的官方指南（未找到独立文档页面）
- D3：`poetry python` 命令的完整功能说明（docs/cli 章节未详细展开）

## leads
- Poetry 2.0 (2025-01-05) 是第一个完整支持 PEP 621 [project] 表的版本，实现了与标准的对齐
- PEP 751 (pylock.toml) 仍是开放提案（issue #10356），暂无支持计划，这是用户关注的互操作性缺口
- 路径依赖模式支持基础的本地开发，但不等同于原生 workspace——复杂 monorepo 场景需评估实际可行性
