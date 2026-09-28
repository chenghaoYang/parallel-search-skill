# r2-poetry
question: Poetry 2 的 [project] 表到底取代了哪些键，pylock.toml 能不能被 install 直接读，以及「不替用户装 Python」和 poetry python install 是否同时成立？
checked: https://python-poetry.org/blog/announcing-poetry-2.0.0/, https://python-poetry.org/docs/pyproject/, https://python-poetry.org/docs/dependency-specification/, https://python-poetry.org/docs/basic-usage/, https://python-poetry.org/docs/cli/, https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md, https://github.com/python-poetry/poetry-plugin-export

## claims
- [C1] Poetry 2.0 支持按 PEP 621 使用 [project] 表 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Poetry 2.0 respects the `project` section in the `pyproject.toml` as originally specified in PEP 621" | type: official
- [C2] [project] 可替换 tool.poetry 中许多字段 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "You can replace many fields in the `tool.poetry` section with their counterparts in the `project` section" | type: official
- [C3] tool.poetry.dependencies 未被废弃（支持 project.dependencies 没有的特性） | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "tool.poetry.dependencies is not deprecated because it supports features that are not supported by project.dependencies." | type: official
- [C4] tool.poetry.name 被 project.name 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "**Deprecated**: Use `project.name` instead." | type: official
- [C5] tool.poetry.description 被 project.description 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "**Deprecated**: Use `project.description` instead." | type: official
- [C6] tool.poetry.license 被 project.license 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "**Deprecated**: Use `project.license` instead." | type: official
- [C7] tool.poetry.authors 被 project.authors 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "**Deprecated**: Use `project.authors` instead." | type: official
- [C8] tool.poetry.maintainers 被 project.maintainers 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "**Deprecated**: Use `project.maintainers` instead." | type: official
- [C9] tool.poetry.homepage 被 project.urls 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "### homepage ... **Deprecated**: Use `project.urls` instead." | type: official
- [C10] tool.poetry.repository 被 project.urls 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "### repository ... **Deprecated**: Use `project.urls` instead." | type: official
- [C11] tool.poetry.documentation 被 project.urls 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "### documentation ... **Deprecated**: Use `project.urls` instead." | type: official
- [C12] tool.poetry.keywords 被 project.keywords 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "**Deprecated**: Use `project.keywords` instead." | type: official
- [C13] tool.poetry.scripts 被 project.scripts 取代（仅 console/gui；file 类型仍用 tool.poetry.scripts） | src: https://python-poetry.org/docs/pyproject/ | quote: "**Deprecated**: Use `project.scripts` instead for `console` and `gui` scripts. Use `[tool.poetry.scripts]` only for scripts of type `file`." | type: official
- [C14] tool.poetry.extras 被 project.optional-dependencies 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "**Deprecated**: Use `project.optional-dependencies` instead." | type: official
- [C15] tool.poetry.plugins 被 project.entry-points 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "**Deprecated**: Use `project.entry-points` instead." | type: official
- [C16] tool.poetry.urls 被 project.urls 取代 | src: https://python-poetry.org/docs/pyproject/ | quote: "### urls ... **Deprecated**: Use `project.urls` instead." | type: official
- [C17] tool.poetry.version / readme / classifiers 未标 Deprecated，仅建议优先用 project 对应键 | src: https://python-poetry.org/docs/pyproject/ | quote: "prefer `project.version` over this setting" | type: official
- [C18] project 表只能声明 main 依赖，依赖组仍须写在 tool.poetry | src: https://python-poetry.org/docs/dependency-specification/ | quote: "Only main dependencies can be specified in the `project` section. Other Dependency groups must still be specified in the `tool.poetry` section." | type: official
- [C19] caret/tilde 约束在 project.dependencies 中不受支持 | src: https://python-poetry.org/docs/dependency-specification/ | quote: "Not supported in `project.dependencies`." | type: official
- [C20] changelog 2.3.0（2026-01-18）只声明经插件「导出」pylock.toml | src: https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md | quote: "## [2.3.0] - 2026-01-18 ... **Add support for exporting `pylock.toml` files with `poetry-plugin-export`**" | type: official
- [C21] poetry-plugin-export 的 --format 支持 pylock.toml（导出） | src: https://github.com/python-poetry/poetry-plugin-export | quote: "`--format (-f)`: The format to export to (default: `requirements.txt`). Additionally, `constraints.txt` and `pylock.toml` are supported." | type: official
- [C22] poetry install 文档只提读取 poetry.lock，未提 pylock.toml | src: https://python-poetry.org/docs/cli/ | quote: "If there is a `poetry.lock` file in the current directory, it will use the exact versions from there instead of resolving them." | type: official
- [C23] 基础用法页仍写 Poetry 不替你装 Python 解释器 | src: https://python-poetry.org/docs/basic-usage/ | quote: "Poetry will not install a Python interpreter for you." | type: official
- [C24] poetry python 命令组为实验特性、2.1.0 引入 | src: https://python-poetry.org/docs/cli/ | quote: "This is an experimental feature, and can change behaviour in upcoming releases. *Introduced in 2.1.0*" | type: official
- [C25] poetry python install 从 Python Standalone Builds 安装指定版本 | src: https://python-poetry.org/docs/cli/ | quote: "The `python install` command installs the specified Python version from the Python Standalone Builds project." | type: official

## conflicts
- docs/basic-usage 仍称 "Poetry will not install a Python interpreter for you"，而 docs/cli 的 `poetry python install`（Introduced in 2.1.0，experimental）会从 Python Standalone Builds 安装解释器。两句在同一版文档（2.5）并存，官方未说明何者优先。

## gaps
- 无任何官方页面声明 `poetry install` / `poetry lock` 能直接读取 pylock.toml；cli 页 install/lock 节仅提 poetry.lock，changelog 2.3.0 只提经 poetry-plugin-export 导出。

## leads
- PEP 751（pylock 标准）与 poetry-plugin-export 版本要求值得另查。
- dep-spec 页提到 installer.re-resolve=false「became the default behavior in Poetry 2.3」。
