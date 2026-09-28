# r1-poetry
question: Poetry 2 是否改用标准 [project] 表？[tool.poetry] 还保留什么？Poetry 的锁文件、workspace、Python 版本、构建后端、虚拟环境路径、依赖组、私有源、缓存、迁移入口的官方原名是什么？
checked: https://python-poetry.org/blog/announcing-poetry-2.0.0/, https://python-poetry.org/blog/announcing-poetry-2.2.0/, https://python-poetry.org/blog/announcing-poetry-2.3.0/, https://python-poetry.org/docs/basic-usage/, https://python-poetry.org/docs/1.8/basic-usage/, https://python-poetry.org/docs/faq/, https://python-poetry.org/docs/pyproject/, https://python-poetry.org/docs/dependency-specification/, https://python-poetry.org/docs/managing-dependencies/, https://python-poetry.org/docs/repositories/, https://python-poetry.org/docs/configuration/, https://python-poetry.org/docs/cli/, https://python-poetry.org/docs/managing-environments/, https://python-poetry.org/docs/libraries/, https://raw.githubusercontent.com/python-poetry/poetry-plugin-export/master/README.md

## claims
- [C1] D1 Poetry 2.0.0（2025-01-05）尊重 PEP 621 的 [project]，可替换许多 [tool.poetry] 字段。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Poetry 2.0 respects the `project` section in the `pyproject.toml` as originally specified in PEP 621." | type: official
- [C2] D1 许多 [tool.poetry] 字段 deprecated；tool.poetry.dependencies 不弃用。poetry check 列出弃用字段。 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "`tool.poetry.dependencies` is not deprecated because it supports features that are not supported by `project.dependencies`." | type: official
- [C3] D1 FAQ（文档 2.5）：>=2.0.0 仍可只用 tools.poetry（页面拼写）或使用 project。 | src: https://python-poetry.org/docs/faq/ | quote: "support both `tools.poetry` section only configuration as well using the `project` section." | type: official
- [C4] D1 文档 2.5 的 poetry new 示例以 project.name 为准。 | src: https://python-poetry.org/docs/basic-usage/ | quote: "the same name as `project.name`" | type: official
- [C5] D1 文档 1.8 的 poetry new 以 tool.poetry.name 为准，依赖在 [tool.poetry.dependencies]，示例 python = "^3.7"。 | src: https://python-poetry.org/docs/1.8/basic-usage/ | quote: "the same name as `tool.poetry.name`" | type: official
- [C6] D1 pyproject（2.5）：package mode 的 name/version 可在 project 或 tool.poetry。有 project 段则 project.name 必填。未标 Deprecated：package-mode、packages、requires-poetry（示例 >=2.0）、requires-plugins。 | src: https://python-poetry.org/docs/pyproject/ | quote: "either in the project section or in the tool.poetry section" | type: official
- [C8] D2 锁文件名 poetry.lock；无锁时 poetry install 写入精确版本。 | src: https://python-poetry.org/docs/basic-usage/ | quote: "downloaded to the `poetry.lock` file" | type: official
- [C9] D2 Poetry 2.0+ 生成的锁至少 version 2.1。 | src: https://python-poetry.org/docs/configuration/ | quote: "lock file is at least version 2.1 (created by Poetry 2.0 or above)" | type: official
- [C10] D2 Poetry 2.3.0（2026-01-18）还不能用 pylock.toml 替换 poetry.lock。 | src: https://python-poetry.org/blog/announcing-poetry-2.3.0/ | quote: "not yet able to replace `poetry.lock` with `pylock.toml`" | type: official
- [C11] D2 导出 pylock.toml 需要 Poetry 2.3.0 与 poetry-plugin-export 1.10.0。 | src: https://python-poetry.org/blog/announcing-poetry-2.3.0/ | quote: "requires at least Poetry 2.3.0 and poetry-plugin-export 1.10.0." | type: official
- [C12] D2 export 由插件提供，Poetry 2.0 起默认不安装。 | src: https://python-poetry.org/docs/cli/ | quote: "no longer installed by default with Poetry 2.0." | type: official
- [C13] D2 插件 README 格式原句。 | src: https://raw.githubusercontent.com/python-poetry/poetry-plugin-export/master/README.md | quote: "Additionally, `constraints.txt` and `pylock.toml` are supported." | type: official
- [C14] D4 字段 project.requires-python；锁定上界用 tool.poetry.dependencies 的键 python。 | src: https://python-poetry.org/docs/pyproject/ | quote: "add it in the tool.poetry.dependencies section." | type: official
- [C15] D4 命令 env use：路径、python3.7、3.7 或 system。 | src: https://python-poetry.org/docs/managing-environments/ | quote: "the `env use` command to tell Poetry which Python version to use" | type: official
- [C16] D4 poetry python install <PYTHON_VERSION>，Introduced in 2.1.0，experimental。目录 python.installation-dir 默认 {data-dir}/python，变量 POETRY_PYTHON_INSTALLATION_DIR。 | src: https://python-poetry.org/docs/cli/ | quote: "installs the specified Python version from the Python Standalone Builds project." | type: official
- [C17] D5 build-backend 为 poetry.core.masonry.api。文档 2.5 requires 为 poetry-core>=2.0.0,<3.0.0。 | src: https://python-poetry.org/docs/libraries/ | quote: "define a build-system according to PEP 517" | type: official
- [C18] D6 virtualenvs.path 默认 {cache-dir}/virtualenvs，变量 POETRY_VIRTUALENVS_PATH。也可沿用 {project-dir}/.venv。in-project=true 时为项目根 .venv。命令 poetry env info --path。 | src: https://python-poetry.org/docs/configuration/ | quote: "use the {project-dir}/.venv directory if one already exists." | type: official
- [C19] D7 隐式组名 main。表名 [dependency-groups] 或 [tool.poetry.group.<group>.dependencies]。键 optional、include-groups、include-group。 | src: https://python-poetry.org/docs/managing-dependencies/ | quote: "part of an implicit `main` group." | type: official
- [C20] D7 Poetry 2.2.0（2025-09-14）起可用 PEP 735 组语法。 | src: https://python-poetry.org/blog/announcing-poetry-2.2.0/ | quote: "you can now also use PEP 735 syntax." | type: official
- [C21] D8 表 [[tool.poetry.source]]：name、url、priority（primary、supplemental、explicit；缺省 primary）。有 primary 则禁用隐式 PyPI。凭据 http-basic.<name>；变量 POETRY_HTTP_BASIC_<NAME>_USERNAME 与 _PASSWORD。另有 pypi-token.<name>。 | src: https://python-poetry.org/docs/repositories/ | quote: "the implicit PyPI source is disabled." | type: official
- [C22] D8 键 source 不能写在 project，只在 tool.poetry.dependencies。命令 poetry add --source。 | src: https://python-poetry.org/docs/dependency-specification/ | quote: "It is not possible to define source dependencies in the `project` section." | type: official
- [C23] D9 cache-dir，变量 POETRY_CACHE_DIR。macOS ~/Library/Caches/pypoetry；Unix ~/.cache/pypoetry；Windows %LOCALAPPDATA%\\pypoetry。 | src: https://python-poetry.org/docs/configuration/ | quote: "setting the POETRY_CACHE_DIR environment variable." | type: official
- [C24] D9 命令 poetry cache clear；--no-cache 不删除。列举 poetry cache list。 | src: https://python-poetry.org/docs/cli/ | quote: "The cache clear command removes packages from cached repositories." | type: official
- [C25] D10 迁到 project 是 FAQ 手工修改。poetry check 报弃用。poetry init 用于已有目录。poetry config --migrate 只迁 config 改名或删除。 | src: https://python-poetry.org/docs/faq/ | quote: "manual changes to your `pyproject.toml` file is unavoidable" | type: official

## conflicts
- D1：2.0 弃用许多 tool.poetry 字段且 2.5 模板用 project.name，FAQ 仍允许只用 tools.poetry。不裁决。https://python-poetry.org/blog/announcing-poetry-2.0.0/ https://python-poetry.org/docs/faq/
- D7：dependency-specification 要求组仍在 tool.poetry；managing-dependencies 与 2.2.0 允许 [dependency-groups]。https://python-poetry.org/docs/dependency-specification/ https://python-poetry.org/docs/managing-dependencies/
- D2：插件 README 开头仅 constraints.txt 与 requirements.txt，后文支持 pylock.toml。https://raw.githubusercontent.com/python-poetry/poetry-plugin-export/master/README.md
- D5：requires poetry-core>=2.0.0,<3.0.0（libraries）对 poetry-core>=1.0.0（pyproject PEP-517）。backend 均为 poetry.core.masonry.api。
- D4：basic usage 写不会安装解释器；CLI 有 2.1.0 experimental 的 poetry python install。

## gaps
- D3 workspace：pyproject、cli、configuration、managing-dependencies、basic-usage、repositories 与导航无此名；site:python-poetry.org/docs 检索 workspace OR monorepo 无特性页。
- D2 无 install/lock 读取 pylock.toml 的原句。
- D10 无 requirements.txt 导入命令（CLI、FAQ、basic usage 1.8/2.5）。反向是 poetry export -f requirements.txt。

## leads
- 无 [build-system] 时仍用 poetry-core，未来 minor 落到 setuptools。dev-dependencies 在 poetry-core 2.0.0 改为 group.dev.dependencies。
