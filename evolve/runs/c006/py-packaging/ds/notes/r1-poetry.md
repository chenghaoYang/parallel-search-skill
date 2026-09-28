# r1-poetry
question: Poetry 2.x 官方文档中锁文件、依赖声明、workspace/monorepo、Python 版本管理、构建后端、虚拟环境、迁移、CI 缓存、私有源的做法（grid.md Poetry 行 D1–D9）
checked: python-poetry.org/docs/{pyproject,managing-dependencies,dependency-specification,basic-usage,managing-environments,repositories,configuration,cli,faq}, blog/announcing-poetry-2.0.0/, github CHANGELOG.md, issue #2270, raw: locker.py, action.yaml, docs/{cli,basic-usage,configuration}.md

## claims
- [C1] 锁文件 poetry.lock 记录确切版本，官方要求提交版本库 | src: https://python-poetry.org/docs/basic-usage/ | quote: "You should commit the `poetry.lock` file to your project repo" | type: official
- [C2] 当前 lock-version="2.1"，可读 >=1,<3 | src: https://raw.githubusercontent.com/python-poetry/poetry/main/src/poetry/packages/locker.py | quote: `_VERSION = "2.1"` `_READ_VERSION_RANGE = ">=1,<3"` | type: official
- [C3] 2.0.0(2025-01-05)起 `poetry lock` 默认 --no-update、旧行为 --regenerate；lock 内写 markers/groups，installer.re-resolve 2.3.0 起默认 false | src: https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md | quote: "the default behavior of `poetry lock` to `--no-update` ... `--regenerate` option" | type: official
- [C4] PEP 751 pylock.toml：2.3.0(2026-01-18)起仅经 poetry-plugin-export 导出；`poetry export` 2.0 起非内置 | src: https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md | quote: "Add support for exporting `pylock.toml` files with `poetry-plugin-export`" | type: official
- [C5] 2.0.0 新增 PEP 621 [project] 表支持 | src: https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md | quote: "Add support for the `project` section in the `pyproject.toml` file according to PEP 621" | type: official
- [C6] `poetry new` 生成的 pyproject 默认用 [project]（name/version/requires-python/dependencies） | src: https://raw.githubusercontent.com/python-poetry/poetry/main/docs/basic-usage.md | quote: "[project] name = \"poetry-demo\" ... requires-python = \">=3.9\"" | type: official
- [C7] [tool.poetry] 元数据字段多数废弃指向 [project]；dependencies 不废弃（支持非标准特性） | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "`tool.poetry.dependencies` is not deprecated because it supports features that are not supported by `project.dependencies`" | type: official
- [C8] 官方推荐标准需求改用 project.dependencies；[tool.poetry] 仍兼容；package 模式必填仅 name+version 任一表皆可 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "If you only need standard features, we recommend to replace `tool.poetry.dependencies` with `project.dependencies`." | type: official
- [C9] 依赖组支持 PEP 735 [dependency-groups] 或 [tool.poetry.group.<name>.dependencies] | src: https://python-poetry.org/docs/managing-dependencies/ | quote: "use a dependency-groups section according to PEP 735" | type: official
- [C10] monorepo 手段=path 依赖+editable `{path="../pkg/",develop=true}`；[project] 内仅绝对路径；定位本地开发、打包后变 file:// | src: https://python-poetry.org/docs/dependency-specification/ | quote: "To install directory path dependencies in editable mode, use the `develop` keyword and set it to `true`." | type: official
- [C11] 无 workspace 功能：issue #2270 2020 起 open(kind/feature) | src: https://github.com/python-poetry/poetry/issues/2270 | quote: "Support subprojects in a poetry project" | type: secondary
- [C12] Poetry 不替项目装解释器；需系统已有满足 requires-python 的 Python | src: https://raw.githubusercontent.com/python-poetry/poetry/main/docs/basic-usage.md | quote: "Poetry will not install a Python interpreter for you." | type: official
- [C13] 2.1.0 起实验性 `poetry python install/list/remove` 可装解释器(Python Standalone Builds)；installation-dir={data-dir}/python | src: https://python-poetry.org/docs/cli/ | quote: "installs the specified Python version from the Python Standalone Builds project." / "This is an experimental feature" | type: official
- [C14] `poetry env use <版本|路径>` 为项目激活/新建对应解释器 venv | src: https://raw.githubusercontent.com/python-poetry/poetry/main/docs/cli.md | quote: "The `env use` command activates or creates a new virtualenv for the current project." | type: official
- [C15] 构建后端 poetry-core：build-backend="poetry.core.masonry.api"，新项目 pin >=2.0.0,<3.0.0 | src: https://raw.githubusercontent.com/python-poetry/poetry/main/docs/basic-usage.md | quote: "requires = [\"poetry-core>=2.0.0,<3.0.0\"] build-backend = \"poetry.core.masonry.api\"" | type: official
- [C16] 2.1.0 起 `poetry build` 与 build-system 解耦 | src: https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md | quote: "Make `build` command build-system agnostic" | type: official
- [C17] virtualenvs.create 默认 true；venv 在 {cache-dir}/virtualenvs，in-project=true 则项目内 .venv | src: https://raw.githubusercontent.com/python-poetry/poetry/main/docs/configuration.md | quote: "virtualenvs.create ... **Default**: `true`" | type: official
- [C18] `poetry shell` 移入 poetry-plugin-shell；`poetry env activate` 仅打印激活命令；`poetry sync` 删未跟踪包严格对齐 lock | src: https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md | quote: "Outsource `poetry shell` into `poetry-plugin-shell`" | type: official
- [C19] 迁移官方路径：`poetry init` 交互式为已有目录建 pyproject | src: https://raw.githubusercontent.com/python-poetry/poetry/main/docs/basic-usage.md | quote: "Poetry can be used to 'initialize' a pre-populated directory." | type: official
- [C20] FAQ：>=2.0.0 双格式兼容，迁 [project] 非必须；手工修改不可避免；建议 dynamic dependencies | src: https://python-poetry.org/docs/faq/ | quote: "Poetry >=2.0.0 should seamlessly support both" | type: official
- [C21] CLI 全目录(30命令)无 import/convert，requirements.txt/Pipfile 无官方导入器 | src: https://raw.githubusercontent.com/python-poetry/poetry/main/docs/cli.md | quote: "command TOC enumerated: no import/convert command" | type: official
- [C22] 迁移辅助：`poetry check` 打印废弃字段警告；`poetry config --migrate` 迁过期配置(2.0新增) | src: https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md | quote: "Add a `--migrate` option to `poetry config` to migrate outdated configs" | type: official
- [C23] 官方 CI 缓存样例：仓库内 composite action 缓存 {cache-dir}/artifacts+/cache，键 poetry-<date>-<os>-hashFiles(pyproject.toml,poetry.lock) | src: https://raw.githubusercontent.com/python-poetry/poetry/main/.github/actions/poetry-install/action.yaml | quote: "key: poetry-<date>-${{ runner.os }}-${{ hashFiles('pyproject.toml', 'poetry.lock') }}" | type: official
- [C24] Docker/CI：先 `poetry install --no-root --no-directory` 再 COPY 源码；cache-dir 默认 ~/.cache/pypoetry(Unix)，POETRY_CACHE_DIR 覆盖 | src: https://python-poetry.org/docs/faq/ | quote: "To avoid this cache busting you can split this into two steps" | type: official
- [C25] 私有源 `poetry source add --priority=supplemental foo URL`→[[tool.poetry.source]]；优先级 primary/supplemental/explicit；任一 primary 即禁用隐式 PyPI | src: https://python-poetry.org/docs/repositories/ | quote: "poetry source add --priority=supplemental foo https://pypi.example.org/simple/" | type: official
- [C26] 认证 `poetry config http-basic.foo <user> <pass>`；env POETRY_HTTP_BASIC_FOO_{USERNAME,PASSWORD}；token POETRY_PYPI_TOKEN_FOO | src: https://python-poetry.org/docs/repositories/ | quote: "poetry config http-basic.foo <username> <password>" | type: official
- [C27] keyring.enabled 默认 true，存取系统 keyring，否则落 auth.toml | src: https://python-poetry.org/docs/repositories/ | quote: "If a system keyring is available and supported, the password is stored to and retrieved from the keyring." | type: official
- [C28] 自定义 CA/客户端证书 certificates.foo.cert/client-cert；发布私有仓 `poetry publish --repository` | src: https://python-poetry.org/docs/repositories/ | quote: "poetry config certificates.foo.cert /path/to/ca.pem" | type: official

## conflicts
- 无实质冲突。pyproject 页通用示例写 poetry-core>=1.0.0，`poetry new` 实际生成 >=2.0.0,<3.0.0（通用说明非矛盾）。

## gaps
- pylock.toml 仅可导出，未见从 pylock.toml 安装/消费的文档。
- 无 requirements.txt/Pipfile 官方导入器（已核 cli.md 全命令+FAQ 12 问）。
- workspace 无任何官方文档页，仅 issue #2270 挂起。
- FAQ 无 GitHub Actions 官方缓存 yaml；唯一官方样例是仓库自用 composite action（未发布 marketplace）。

## leads
- poetry-plugin-export 是 PEP 751 出口，Q1 横评可用。
- package-mode=false 纯依赖管理不打包（non-package mode）。
- 2.1.0 起 `poetry new` 默认 src 布局，--flat 可选。
