# r1-poetry
question: Poetry 2 的项目清单是否改用 PEP 621 [project]，以及 Poetry 在锁文件、workspace、CPython、构建后端、依赖组、迁入、CI、私有源上的官方做法。
checked: https://python-poetry.org/docs/basic-usage/, https://python-poetry.org/docs/pyproject/, https://python-poetry.org/docs/faq/, https://python-poetry.org/docs/dependency-specification/, https://python-poetry.org/blog/announcing-poetry-2.0.0/, https://python-poetry.org/blog/announcing-poetry-2.1.0/, https://python-poetry.org/blog/announcing-poetry-2.3.0/, https://python-poetry.org/docs/libraries/, https://python-poetry.org/docs/repositories/, https://python-poetry.org/docs/managing-dependencies/, https://python-poetry.org/docs/configuration/, https://python-poetry.org/docs/, https://python-poetry.org/docs/cli/, https://github.com/python-poetry/poetry-plugin-export, https://raw.githubusercontent.com/python-poetry/poetry-core/main/src/poetry/core/factory.py

## claims
- [C1] D1 脚手架：2.5 Basic usage 的 poetry new 示例只有 [project]（name、version、description、authors、readme、requires-python、dependencies）和 [build-system]（poetry-core>=2.0.0,<3.0.0，backend poetry.core.masonry.api），无 [tool.poetry]。 | src: https://python-poetry.org/docs/basic-usage/ | quote: "For now, it looks like this:" | type: official
- [C2] D1 旧项目：FAQ 写 Poetry >=2.0.0 仍支持仅 tools.poetry 段（原文拼写）或再用 project 段。 | src: https://python-poetry.org/docs/faq/ | quote: "Poetry >=2.0.0 should seamlessly support both tools.poetry section only configuration as well using the project section." | type: official
- [C3] D1 起点：2.0.0 公告（2025-01-05）Added 最早一条即 PEP 621；同版弃用可替代字段，不删旧表。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Add support for the project section in the pyproject.toml file according to PEP 621" | type: official
- [C4] D1 dependencies：两表并存时构建元数据用 project.dependencies，tool.poetry.dependencies 只补充锁定。2.0 不弃用后者。 | src: https://python-poetry.org/docs/dependency-specification/ | quote: "tool.poetry.dependencies is only used to enrich project.dependencies for locking." | type: official
- [C5] D1 name/version（文档）：package mode 可在任一段；有 project 段则 name 与 version 始终必填。tool.poetry.name 已弃用，仅 project 未定义时必填。动态 version 的基准在 tool.poetry，并把 version 列入 dynamic。 | src: https://python-poetry.org/docs/pyproject/ | quote: "name and version (either in the project section or in the tool.poetry section)." | type: official
- [C6] D1 name/version（代码）：文档无「后者忽略」。poetry-core 在两表同名字段都设时忽略 tool.poetry；运行时先读 project。 | src: https://raw.githubusercontent.com/python-poetry/poetry-core/main/src/poetry/core/factory.py | quote: "The latter will be ignored." | type: official
- [C7] D2 文件名 poetry.lock。无锁则写入精确版本；有锁则按锁安装。 | src: https://python-poetry.org/docs/basic-usage/ | quote: "writes all the packages and their exact versions that it downloaded to the poetry.lock file" | type: official
- [C8] D2 不是 pylock：2.3.0（2026-01-18）不能用 pylock.toml 替换 poetry.lock；导出至少要 Poetry 2.3.0 与 poetry-plugin-export 1.10.0。 | src: https://python-poetry.org/blog/announcing-poetry-2.3.0/ | quote: "Poetry is not yet able to replace poetry.lock with pylock.toml" | type: official
- [C9] D2 导出：poetry export -f requirements.txt --output requirements.txt；--format 另支持 pylock.toml。CLI 只说该命令来自插件，2.0 起默认不装。 | src: https://github.com/python-poetry/poetry-plugin-export | quote: "Additionally, constraints.txt and pylock.toml are supported." | type: official
- [C10] D2 有 hash：定不出发行链接 hash 则报错；导出可用 --without-hashes 去掉。源无 checksum 时下载 wheel 生成。 | src: https://python-poetry.org/blog/announcing-poetry-2.3.0/ | quote: "Raise an error if no hash can be determined for any distribution link of a package" | type: official
- [C11] D2 跨平台：锁是 platform-agnostic；universal locking 覆盖所声明的全部 Python 版本。锁为全部分组一份解，--without 不缩小锁。 | src: https://python-poetry.org/docs/repositories/ | quote: "Poetry’s lock file is platform-agnostic." | type: official
- [C12] D3 已打开页无 workspace 键。互依赖用 path，develop = true 才可编辑且不进发行元数据。相对路径只在 tool.poetry。库锁只作用于主项目。 | src: https://python-poetry.org/docs/libraries/ | quote: "It only has an effect on the main project." | type: official
- [C13] D4 Basic usage：不会安装解释器；范围写在 project.requires-python（示例 >=3.9）。 | src: https://python-poetry.org/docs/basic-usage/ | quote: "Poetry will not install a Python interpreter for you." | type: official
- [C14] D4 2.1.0 起实验命令 poetry python install，来自 Python Standalone Builds；--implementation 为 cpython 或 pypy。目录 python.installation-dir 默认 {data-dir}/python。 | src: https://python-poetry.org/docs/cli/ | quote: "installs the specified Python version from the Python Standalone Builds project." | type: official
- [C15] D4 两处都写时，锁定用 tool.poetry.dependencies 的 python，且须为 requires-python 的子集。 | src: https://python-poetry.org/docs/pyproject/ | quote: "use the information in tool.poetry.dependencies for locking" | type: official
- [C16] D5 默认 build-backend 为 poetry.core.masonry.api；new/init 写入该段。pyproject 示例 requires 为 poetry-core>=1.0.0；Basic usage/Libraries 为 >=2.0.0,<3.0.0。 | src: https://python-poetry.org/docs/pyproject/ | quote: "you should update it to reference poetry-core instead." | type: official
- [C17] D5 可换后端（示例 maturin）。poetry build 与 poetry publish 都在；publish 默认不构建，要 --build。无 [build-system] 时仍用 poetry-core，未来改默认 setuptools。 | src: https://python-poetry.org/docs/libraries/ | quote: "The poetry build command will then use the specified build backend" | type: official
- [C18] D6 分组表是 [dependency-groups]（PEP 735）或 [tool.poetry.group.<group>.dependencies]；主依赖属隐式 main。optional = true。extras 用 [project.optional-dependencies]，[tool.poetry.extras] 已弃用。 | src: https://python-poetry.org/docs/managing-dependencies/ | quote: "use a dependency-groups section according to PEP 735 or a tool.poetry.group.<group> section" | type: official
- [C19] D7 CLI 全文无 import。poetry init 只交互创建 pyproject（可 --dependency foo:1.0.0）。poetry export 是反向导出，2.0 起插件默认不装。无 Pipfile 导入。 | src: https://python-poetry.org/docs/cli/ | quote: "This command will help you create a pyproject.toml file interactively" | type: official
- [C20] D8 CI 点名 pipx、官方安装脚本、手动 pip，不点名 Action。示例 pipx install poetry==2.0.0；POETRY_HOME=/opt/poetry。 | src: https://python-poetry.org/docs/ | quote: "one of your top choices for use of Poetry in CI." | type: official
- [C21] D8 缓存 cache-dir：macOS ~/Library/Caches/pypoetry，Windows C:\Users\<username>\AppData\Local\pypoetry\Cache，Unix ~/.cache/pypoetry；POETRY_CACHE_DIR。virtualenvs.path 默认 {cache-dir}/virtualenvs。in-project 用 .venv。 | src: https://python-poetry.org/docs/configuration/ | quote: "Directory where virtual environments will be created." | type: official
- [C22] D9 表 [[tool.poetry.source]]，键 name、url、priority（primary、supplemental、explicit，后两者 1.5.0）。未写 priority 则当 primary 并禁用隐式 PyPI。依赖键 source 不能写在 project 段。 | src: https://python-poetry.org/docs/repositories/ | quote: "If priority is undefined, the source is considered a primary source" | type: official
- [C23] D9 凭证：poetry config http-basic.<name> 或 pypi-token.<name>；变量 POETRY_HTTP_BASIC_<NAME>_USERNAME/_PASSWORD 与 POETRY_PYPI_TOKEN_<NAME>。密码进 keyring，失败写 auth.toml。包源不进 core metadata。 | src: https://python-poetry.org/docs/repositories/ | quote: "writing the password to the auth.toml file along with the username." | type: official

## conflicts
- C13 对 C14：Basic usage 写不会安装解释器（https://python-poetry.org/docs/basic-usage/）；CLI 2.1.0 写会安装 Python Standalone Builds（https://python-poetry.org/docs/cli/）。2.1 公告称 python-build-standalone。
- requires：pyproject 示例 poetry-core>=1.0.0；Basic usage 与 Libraries 为 poetry-core>=2.0.0,<3.0.0。backend 都是 poetry.core.masonry.api。
- 依赖组：dependency-specification 写其他组必须在 tool.poetry；managing-dependencies 允许顶层 [dependency-groups]。
- 插件 README 前文只列 requirements.txt/constraints.txt，后文加上 pylock.toml。

## gaps
- D3：上述已打开页无 workspace 表；站内检索无功能页。未写成永不支持。
- D9：源名字/URL 是否写入 poetry.lock 无原句。只写不进 core metadata。
- D2/D7：无 pylock、requirements.txt、Pipfile 导入。CLI 无 import。
- D8：未点名 GitHub Action。文档无 name/version 两表并存以 project 为准的散文（见 C6）。

## leads
- 2.3.0 将 installer.re-resolve 默认改为 false。导出另有 --with-credentials。
