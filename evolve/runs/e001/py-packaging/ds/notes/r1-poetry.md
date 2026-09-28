# r1-poetry
question: Poetry（1.x → 2.x）在 10 个维度上，官方文档/changelog 是怎么说的？
checked: https://python-poetry.org/blog/announcing-poetry-2.0.0/,https://python-poetry.org/docs/main/pyproject/,https://python-poetry.org/docs/dependency-specification/,https://python-poetry.org/docs/managing-environments/,https://python-poetry.org/docs/repositories/,https://python-poetry.org/docs/managing-dependencies/,https://github.com/python-poetry/poetry/releases,https://python-poetry.org/docs/main/repositories/

## claims

### D1: Scope/Ecosystem
- [C1] Poetry 默认发布和包发现都面向 PyPI，其他源须在项目 pyproject.toml 中配置。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "By default, if you have not configured any primary source, Poetry is configured to use the Python ecosystem's canonical package index PyPI." | type: official
- [C2] Poetry 支持私有仓库发现和发布，但非 PyPI 的源需在项目中显式配置。 | src: https://python-poetry.org/docs/main/repositories/ | quote: "Poetry supports the use of PyPI and private repositories for discovery of packages as well as for publishing your projects." | type: official

### D2: pyproject.toml 标准化 - **关键问题**
- [C3] Poetry 2.0 加入了对 [project] 表的支持，符合 PEP 621。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Poetry 2.0 added support for the project section in the pyproject.toml file according to PEP 621." | type: official
- [C4] Poetry 2.0 中许多 [tool.poetry] 字段现已废弃，推荐改用 [project] 等效字段。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "many fields in the `tool.poetry` section are deprecated in favor of their counterparts in the `project` section." | type: official
- [C5] [project] 表包含标准字段：name, version, description, license, readme, requires-python, authors, keywords, classifiers, urls, dependencies, optional-dependencies，遵循 PyPA spec。 | src: https://python-poetry.org/docs/main/pyproject/ | quote: "This section follows the PyPA specification and includes: name, version, description, license, readme, requires-python, authors/maintainers, keywords, classifiers, urls, scripts/gui-scripts, dependencies/optional-dependencies." | type: official
- [C6] [tool.poetry] 保留的 Poetry 专有字段包括：package-mode, packages, exclude/include, scripts（含文件类型脚本）, extras, plugins, requires-poetry, requires-plugins, build-constraints，以及 groups（依赖分组）。 | src: https://python-poetry.org/docs/main/pyproject/ | quote: "Poetry-Specific: package-mode, packages, exclude/include, scripts (including file-type scripts), extras, plugins, requires-poetry, requires-plugins, build-constraints." | type: official
- [C7] 项目可同时在 [project.dependencies] 和 [tool.poetry.dependencies] 中声明，二者组合使用可结合标准和专有特性。 | src: https://python-poetry.org/docs/main/pyproject/ | quote: "You can use project.dependencies and add additional information in tool.poetry.dependencies if you need Poetry specific features." | type: official
- [C8] [project] 中的依赖遵循 PEP 508 字符串格式，[tool.poetry.dependencies] 使用 TOML 表格式。 | src: https://python-poetry.org/docs/dependency-specification/ | quote: "While dependencies in `tool.poetry.dependencies` are specified using toml tables, dependencies in `project.dependencies` are specified as strings according to PEP 508." | type: official

### D3: 锁文件
- [C9] poetry.lock 是 Poetry 原生格式（非 PEP 751 标准）。 | src: https://python-poetry.org/blog/announcing-poetry-2.3.0/ | quote: "Poetry is not yet able to replace poetry.lock with pylock.toml." | type: official
- [C10] Poetry 2.3.0+ 可导出 PEP 751 的 pylock.toml 格式，需 poetry-plugin-export >= 1.10.0。 | src: https://python-poetry.org/blog/announcing-poetry-2.3.0/ | quote: "Poetry now provides all necessary information for poetry-plugin-export to export pylock.toml files. Exporting pylock.toml requires at least Poetry 2.3.0 and poetry-plugin-export 1.10.0." | type: official
- [C11] Poetry 2.0 lock 文件现包含每个包的结果分组和标记，支持禁用重新解析时的快速安装。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Lock files now include resulting groups and markers for each package in lock files, enabling faster installations when re-resolution is disabled." | type: official

### D4: 依赖解析算法
- [C12] Poetry 使用 Mixology（PubGrub 算法的 Python 实现）进行版本求解。 | src: https://github.com/sdispater/mixology | quote: "A generic dependency-resolution library written in pure Python" based on PubGrub | type: official
- [C13] Poetry 包含"详尽的依赖解析器"，能在存在解决方案时找到，存在冲突时提供详细说明。 | src: https://python-poetry.org/docs/managing-dependencies/ | quote: "Poetry comes with an exhaustive dependency resolver" | type: official

### D5: Python 版本管理
- [C14] 使用 `poetry env use` 命令指定项目使用的 Python 版本。 | src: https://python-poetry.org/docs/managing-environments/ | quote: "Use `poetry env use` to specify which Python version to use: `poetry env use python3.7`, `poetry env use 3.7`, `poetry env use /full/path/to/python`" | type: official
- [C15] Poetry 与 pyenv 集成，若使用 pyenv 管理 Python 版本，Poetry 会自动识别 shell 中的活跃 Python。 | src: https://python-poetry.org/docs/managing-environments/ | quote: "If you use tools like pyenv to manage Python versions, Poetry automatically recognizes your shell's active Python version for environment creation." | type: official
- [C16] Poetry **无内置 Python 解释器安装能力**，依赖外部工具如 pyenv。 | src: https://python-poetry.org/docs/managing-environments/ | quote: "Poetry makes project environment isolation one of its core features" but requires external tools like pyenv for Python installation | type: official

### D6: 构建后端
- [C17] Poetry 默认构建后端是 poetry-core，build-backend 值为 `poetry.core.masonry.api`，遵循 PEP 517。 | src: https://python-poetry.org/docs/main/pyproject/ | quote: "[build-system] requires = [\"poetry-core>=1.0.0\"] build-backend = \"poetry.core.masonry.api\"" | type: official
- [C18] Poetry 1.x 使用已弃用的 `poetry.masonry.api` 后端，2.x 需迁移到 poetry-core。 | src: https://python-poetry.org/docs/main/pyproject/ | quote: "For existing projects, the build-system section must be changed from `build-backend = \"poetry.masonry.api\"` to `build-backend = \"poetry.core.masonry.api\"`." | type: official

### D7: Workspace/Monorepo
- [C19] Poetry **无原生 workspace 概念**，依赖分组通过 `[tool.poetry.group.{name}]` 或 PEP 735 `[dependency-groups]` 管理。 | src: https://python-poetry.org/docs/managing-dependencies/ | quote: "You can organize dependencies using either PEP 735's `[dependency-groups]` or Poetry's `[tool.poetry.group.<name>]` format." | type: official
- [C20] 官方推荐多包协同做法是路径依赖（path dependencies）+ `develop = true`，用于本地开发。 | src: https://python-poetry.org/docs/dependency-specification/ | quote: "Path dependencies are intended for local development. my-package = { path = \"../my-package/\", develop = true }" | type: official
- [C21] Poetry 2.0 修复了从 fork monorepos 安装多个依赖时的竞态条件问题。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Fixed an issue where installing multiple dependencies from forked monorepos failed sporadically due to a race condition." | type: official
- [C22] 社区提供了 poetry-workspace-plugin 等第三方插件以补充 monorepo 功能。 | src: https://pypi.org/project/poetry-workspace-plugin/ | quote: "Multi project workspace plugin for Poetry" | type: secondary

### D8: 私有源 + 认证方式
- [C23] Poetry 支持 HTTP 基础认证：`poetry config http-basic.{repo-name} <username> <password>`。 | src: https://python-poetry.org/docs/main/repositories/ | quote: "`poetry config http-basic.foo <username> <password>` enables credential storage for specific repositories." | type: official
- [C24] Poetry 支持 PyPI API 令牌认证：`poetry config pypi-token.pypi <my-token>`。 | src: https://python-poetry.org/docs/main/repositories/ | quote: "For PyPI specifically, Poetry recommends using API tokens rather than passwords. Configure these with `poetry config pypi-token.pypi <my-token>`." | type: official
- [C25] Poetry 通过环境变量支持凭证注入：`POETRY_PYPI_TOKEN_FOO`、`POETRY_HTTP_BASIC_FOO_USERNAME`、`POETRY_HTTP_BASIC_FOO_PASSWORD`。 | src: https://python-poetry.org/docs/main/repositories/ | quote: "Credentials can be supplied via environment variables like `POETRY_PYPI_TOKEN_FOO` or `POETRY_HTTP_BASIC_FOO_USERNAME` and `POETRY_HTTP_BASIC_FOO_PASSWORD`." | type: official
- [C26] Poetry 支持客户端证书认证：`poetry config certificates.{repo-name}.client-cert /path/to/client.pem`。 | src: https://python-poetry.org/docs/main/repositories/ | quote: "`poetry config certificates.foo.client-cert /path/to/client.pem` for mutual TLS authentication." | type: official
- [C27] Poetry 优先使用系统钥匙环存储凭证，回退到 auth.toml 纯文本存储；可用 `poetry config keyring.enabled false` 禁用。 | src: https://python-poetry.org/docs/main/repositories/ | quote: "Poetry integrates with system keyrings when available, storing credentials securely. If keyring access fails, credentials fall back to the `auth.toml` file." | type: official

### D9: CI 缓存建议
- [C28] Poetry 官方文档未提供针对 GitHub Actions 等特定 CI 平台的缓存策略文档。 | src: https://python-poetry.org/docs/main/configuration/ | type: gap

### D10: 迁移路径
- [C29] Poetry 2.0 release notes 建议运行 `poetry config --migrate` 自动更新已弃用的配置字段。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Run `poetry config --migrate` to update outdated configuration settings automatically." | type: official
- [C30] Poetry 官方文档**无**专门从 pip/requirements.txt 迁移的指南，社区提供 poetry-import-plugin 等工具。 | src: https://pypi.org/project/poetry-import-plugin/ | quote: "poetry-import-plugin is a Python plugin for Poetry that simplifies importing dependencies from requirements.txt files." | type: secondary
- [C31] 1.x→2.x 主要破坏性变更：poetry export、poetry shell 移至插件；poetry lock 默认 --no-update；poetry add --optional 需指定 extra；弃用 Python 3.8。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Command Removals: poetry export/shell outsourced to plugins; poetry lock now defaults to --no-update; Optional Dependencies: poetry add --optional now requires specifying an extra; Python Support: Poetry 2.0 drops Python 3.8 support." | type: official

## conflicts
- 无。

## gaps
- D9：官方文档未明确规定 CI 缓存策略（如 GitHub Actions workflow 缓存 poetry.lock 或 .venv 的最佳实践）。
- D10：官方无 requirements.txt→Poetry 迁移指南（仅有社区教程）。

## leads
- Poetry 2.0 作为重大版本升级，彻底改变了 pyproject.toml 的规范性支持，值得关注其与 PEP 621/735 的长期协同演进。
- PEP 751 pylock.toml 标准虽支持导出，但 poetry.lock 仍为 Poetry 内部格式，可能影响跨工具互操作性。
- Mixology 依赖解析算法的性能对标 Rust PubGrub 实现，社区提议迁移以加速大型项目解析。
