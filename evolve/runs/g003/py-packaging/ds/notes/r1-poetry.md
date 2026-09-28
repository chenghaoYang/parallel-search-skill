# r1-poetry
question: Poetry 2 是否改用标准 [project] 表？[tool.poetry] 还剩什么？以及 Poetry 的锁文件、workspace、Python 版本、构建后端、环境、迁移、CI 缓存、私有源、依赖分组的官方字段名和命令。
checked: https://python-poetry.org/blog/announcing-poetry-2.0.0/, https://python-poetry.org/history/, https://python-poetry.org/docs/pyproject/, https://python-poetry.org/docs/basic-usage/, https://python-poetry.org/docs/dependency-specification/, https://python-poetry.org/docs/managing-dependencies/, https://python-poetry.org/docs/faq/, https://python-poetry.org/docs/repositories/, https://python-poetry.org/docs/configuration/, https://python-poetry.org/docs/cli/, https://python-poetry.org/docs/libraries/, https://python-poetry.org/docs/pre-commit-hooks/, https://python-poetry.org/blog/announcing-poetry-2.1.0/, https://python-poetry.org/blog/announcing-poetry-2.2.0/, https://python-poetry.org/blog/announcing-poetry-2.3.0/, https://raw.githubusercontent.com/python-poetry/poetry/2.0.0/src/poetry/layouts/layout.py

## claims
- [C1] D2 起点 2.0.0（2025-01-05）。history 只此处有该条。 | src: https://python-poetry.org/history/ | quote: "2.0.0 - 2025-01-05" | type: official
- [C2] D2 Added：PEP 621 `[project]`。 | src: https://python-poetry.org/history/ | quote: "Add support for the project section in the pyproject.toml file according to PEP 621" | type: official
- [C3] D2 `tool.poetry.dependencies` 不废弃，可与 `project.dependencies` 并存。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "tool.poetry.dependencies is not deprecated" | type: official
- [C4] D2 2.0 前依赖必须在 tool.poetry.dependencies；之后建议 project.dependencies。并存时 project 做元数据，tool 只补充锁定。可 dynamic 后只写 tool。 | src: https://python-poetry.org/docs/dependency-specification/ | quote: "Prior Poetry 2.0, dependencies had to be declared in the tool.poetry.dependencies section" | type: official
- [C5] D2 仅 tool.poetry 的旧配置 >=2.0.0 仍可用（FAQ 原文 tools.poetry）。 | src: https://python-poetry.org/docs/faq/ | quote: "support both tools.poetry section only configuration as well using the project section" | type: official
- [C6] D2 文档 2.5：`poetry new` 示例默认 `[project]`。 | src: https://python-poetry.org/docs/basic-usage/ | quote: "[project] name = \"poetry-demo\" version = \"0.1.0\"" | type: official
- [C7] D2 标签 2.0.0 的 POETRY_DEFAULT 以 [project] 开头，并留 tool.poetry packages 与 group.dev。 | src: https://raw.githubusercontent.com/python-poetry/poetry/2.0.0/src/poetry/layouts/layout.py | quote: "[project]" | type: official
- [C8] D2 tool.poetry.name 废弃。name/version 可在任一段。仍用 package-mode（默认 package）、packages、include/exclude、requires-poetry、requires-plugins、build-constraints、依赖与 group。poetry check 警告废弃字段。 | src: https://python-poetry.org/docs/pyproject/ | quote: "Deprecated: Use project.name instead." | type: official
- [C9] D1 不能用 pylock.toml 替换 poetry.lock。2.3.0（2026-01-18）起 plugin-export >=1.10.0 可导出。 | src: https://python-poetry.org/blog/announcing-poetry-2.3.0/ | quote: "not yet able to replace poetry.lock with pylock.toml" | type: official
- [C10] D1 poetry install 把精确版本写入 poetry.lock。 | src: https://python-poetry.org/docs/basic-usage/ | quote: "to the poetry.lock file" | type: official
- [C11] D3 上列 pyproject/cli/managing-dependencies/repositories 无 workspace 成员表。cli 检索 workspace 零命中。monorepo 只指 pyproject 不在根。 | src: https://python-poetry.org/docs/pre-commit-hooks/ | quote: "monorepo setup or if the pyproject.toml file is not in the root directory" | type: official
- [C12] D4 约束在 [project] requires-python。锁定上界可写 tool.poetry.dependencies 的 python；两边都有时锁定用后者且须为子集。 | src: https://python-poetry.org/docs/pyproject/ | quote: "use the information in tool.poetry.dependencies for locking" | type: official
- [C13] D4 `poetry install` 不装解释器。 | src: https://python-poetry.org/docs/basic-usage/ | quote: "Poetry will not install a Python interpreter for you." | type: official
- [C14] D4 2.1.0（2025-02-15）起实验命令 `poetry python install <PYTHON_VERSION>`（Standalone Builds）；`--implementation` 为 cpython 或 pypy。 | src: https://python-poetry.org/docs/cli/ | quote: "installs the specified Python version from the Python Standalone Builds project." | type: official
- [C15] D5 backend 都是 `poetry.core.masonry.api`。libraries 与 new 示例 requires=`poetry-core>=2.0.0,<3.0.0`。 | src: https://python-poetry.org/docs/libraries/ | quote: "build-backend = \"poetry.core.masonry.api\"" | type: official
- [C16] D5 pyproject 页仍写 poetry-core>=1.0.0，backend 同为 poetry.core.masonry.api。new/init 会自动加该段。 | src: https://python-poetry.org/docs/pyproject/ | quote: "poetry-core>=1.0.0" | type: official
- [C17] D5 2.1.0 起 poetry build 遵守 [build-system]（例 maturin）。无该段则警告并仍用 poetry-core。2.3.0 仍将改回 setuptools 标为 upcoming。 | src: https://python-poetry.org/blog/announcing-poetry-2.1.0/ | quote: "built-in poetry-core backend by default" | type: official
- [C18] D6 默认 {cache-dir}/virtualenvs；已有 .venv 则用之。键 virtualenvs.in-project，默认 None，变量 POETRY_VIRTUALENVS_IN_PROJECT；true 时用项目根 .venv。 | src: https://python-poetry.org/docs/configuration/ | quote: "folder named .venv" | type: official
- [C19] D6 `poetry config --local` 写入 poetry.toml（与 pyproject 分开）。全局 config.toml。环境变量优先。 | src: https://python-poetry.org/docs/configuration/ | quote: "stored in the poetry.toml file, which is separate from pyproject.toml." | type: official
- [C20] D7 CLI 无 requirements.txt，无 pip/requirements 导入命令。2.0 起 export 不默认安装，在 poetry-plugin-export。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "poetry-plugin-export is not included anymore in the default Poetry installation" | type: official
- [C21] D7 poetry config --migrate 只迁 config，不改 pyproject。 | src: https://python-poetry.org/docs/configuration/ | quote: "migrate explicit set options" | type: official
- [C22] D8 键 cache-dir，变量 POETRY_CACHE_DIR。macOS ~/Library/Caches/pypoetry；Windows %LOCALAPPDATA%\\pypoetry；Linux ~/.cache/pypoetry（或 $XDG_CACHE_HOME/pypoetry）。 | src: https://python-poetry.org/docs/configuration/ | quote: "POETRY_CACHE_DIR" | type: official
- [C23] D8 CI：`poetry install --no-directory`。FAQ：先复制 pyproject.toml 与 poetry.lock，再 `poetry install --only main --no-root --no-directory`。 | src: https://python-poetry.org/docs/cli/ | quote: "mainly useful for caching in CI or when building Docker images." | type: official
- [C24] D9 表 [[tool.poetry.source]]（name、url、priority）。缺省 priority=primary 并禁用隐式 PyPI。原词 primary、supplemental、explicit（后两者 Introduced in 1.5.0）。 | src: https://python-poetry.org/docs/repositories/ | quote: "priority is undefined, the source is considered a primary source" | type: official
- [C25] D9 包级键 source 在 tool.poetry.dependencies，不能写进 [project]。凭证 poetry config http-basic.<name> 或 POETRY_HTTP_BASIC_<NAME>_USERNAME/_PASSWORD。 | src: https://python-poetry.org/docs/dependency-specification/ | quote: "not possible to define source dependencies in the project section" | type: official
- [C26] D10 隐式组名 main。其它组 `[tool.poetry.group.<group>.dependencies]`，或 2.2.0（2025-09-14）起 `[dependency-groups]`（PEP 735）。 | src: https://python-poetry.org/docs/managing-dependencies/ | quote: "are part of an implicit main group" | type: official
- [C27] D10 默认安装全部非 optional 组。只装运行时 `poetry install --only main`。加组 `poetry add --group`。optional 键 optional=true，用 `--with`。 | src: https://python-poetry.org/docs/managing-dependencies/ | quote: "dependencies across all non-optional groups will be installed" | type: official
## conflicts
- D5 requires：pyproject 页 poetry-core>=1.0.0（C16）；libraries 与 new 示例 poetry-core>=2.0.0,<3.0.0（C15）。backend 都是 poetry.core.masonry.api。
- D10：dependency-specification：“Other Dependency groups must still be specified in the tool.poetry section.”；managing-dependencies 与 2.2.0 允许 [dependency-groups]。两页都是文档 2.5。
- D4：basic-usage 说 install 不装解释器（C13）；cli 自 2.1.0 另有实验 poetry python install（C14）。

## gaps
- 无自动改写 pyproject 到 [project] 的命令。CLI 无 requirements 导入。
- workspace 上列页无成员表，未扫完全站。default/secondary priority 是否仍可解析未核。
- 无 build-system 是否已在 2.4/2.5 改回 setuptools：2.3.0 仍标 upcoming。poetry init 无单独示例。

## leads
- 2.0.0 捆绑 poetry-core 2.0.0；export/shell 拆到插件。PEP 735 建议 requires-poetry >=2.3.0。未对照 uv/PDM/pip。
