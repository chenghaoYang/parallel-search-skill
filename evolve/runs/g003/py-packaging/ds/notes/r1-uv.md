# r1-uv
question: uv 官方文档里，锁文件、项目表、workspace、Python 版本、构建后端、环境、迁移、CI 缓存、私有源、依赖分组各自的字段名和命令是什么？特别是：uv 对 PEP 751 pylock.toml 是生成、安装，还是两者，从哪个版本、用哪条命令？
checked: https://docs.astral.sh/uv/concepts/projects/layout/, https://docs.astral.sh/uv/concepts/projects/sync/, https://docs.astral.sh/uv/concepts/projects/export/, https://docs.astral.sh/uv/pip/compile/, https://docs.astral.sh/uv/concepts/resolution/, https://github.com/astral-sh/uv/releases/tag/0.6.15, https://docs.astral.sh/uv/concepts/projects/dependencies/, https://docs.astral.sh/uv/concepts/projects/workspaces/, https://docs.astral.sh/uv/reference/settings/, https://docs.astral.sh/uv/concepts/projects/init/, https://docs.astral.sh/uv/concepts/python-versions/, https://docs.astral.sh/uv/concepts/build-backend/, https://docs.astral.sh/uv/concepts/projects/build/, https://docs.astral.sh/uv/concepts/cache/, https://docs.astral.sh/uv/guides/integration/github/, https://docs.astral.sh/uv/concepts/indexes/, https://docs.astral.sh/uv/guides/migration/, https://docs.astral.sh/uv/guides/migration/pip-to-project/

## claims
- [C1] D1 项目锁 `uv.lock`，在 `pyproject.toml` 旁。页脚 2026-07-21。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv creates a `uv.lock` file next to the `pyproject.toml`." | type: official
- [C2] D1 `uv lock` 显式创建或更新该锁。页脚 2026-08-05。 | src: https://docs.astral.sh/uv/concepts/projects/sync/ | quote: "the lockfile may also be explicitly created or updated using `uv lock`:" | type: official
- [C3] D1 schema 字段名 `version`。页脚 2026-09-18。未给当前整数。 | src: https://docs.astral.sh/uv/concepts/resolution/ | quote: "The schema version is included in the `version` field of the lockfile." | type: official
- [C4] D1 同页兼容字段 `revision`。 | src: https://docs.astral.sh/uv/concepts/resolution/ | quote: "The `revision` field of the lockfile is used to track backwards compatible changes to the lockfile." | type: official
- [C5] D1 项目接口继续用 `uv.lock`，不把 pylock 当项目锁。页脚 2026-07-21。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv will continue to use the `uv.lock` format within the project interface." | type: official
- [C6] D1 导出 flag：`--format pylock.toml` 与 `--output-file`。页脚 2025-11-20。 | src: https://docs.astral.sh/uv/concepts/projects/export/ | quote: "Use `--output-file` to write to a file for any format:" | type: official
- [C7] D1 从 requirements 生成：`uv pip compile requirements.in -o pylock.toml`。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "To generate a `pylock.toml` file from a set of requirements, run: `uv pip compile requirements.in -o pylock.toml`" | type: official
- [C8] D1 安装：`uv pip sync pylock.toml` 或 `uv pip install -r pylock.toml`。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "To install from a `pylock.toml` file, run: `uv pip sync pylock.toml` or `uv pip install -r pylock.toml`" | type: official
- [C9] D1 起点 tag 0.6.15（页上 “22 Apr”，无年份）引入 preliminary support。 | src: https://github.com/astral-sh/uv/releases/tag/0.6.15 | quote: "This release includes preliminary support for the `pylock.toml` file format, as standardized in PEP 751." | type: official
- [C10] D1 同发布说明：自该版起支持下列命令。 | src: https://github.com/astral-sh/uv/releases/tag/0.6.15 | quote: "As of this release, `pylock.toml` is supported in the following commands:" | type: official
- [C11] D2 `uv add` 写入 `[project] dependencies`。页脚 2026-08-14。 | src: https://docs.astral.sh/uv/concepts/projects/dependencies/ | quote: "An entry will be added in the `project.dependencies` field:" | type: official
- [C12] D3 表 `[tool.uv.workspace]`，必填 `members`、可选 `exclude`。页脚 2026-09-22。 | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "you must specify the `members` (required) and `exclude` (optional) keys" | type: official
- [C13] D3 成员依赖键是 `tool.uv.sources` 里的 `workspace = true`。 | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "The `workspace = true` key-value pair in the `tool.uv.sources` table" | type: official
- [C14] D4 安装 CPython 的命令是 `uv python install`；默认可自动下载。页脚 2026-07-25。 | src: https://docs.astral.sh/uv/concepts/python-versions/ | quote: "By default, Python versions are automatically downloaded as needed without using `uv python install`." | type: official
- [C15] D4 `.python-version` 是默认版本请求。 | src: https://docs.astral.sh/uv/concepts/python-versions/ | quote: "The `.python-version` file can be used to create a default Python version request." | type: official
- [C16] D4 项目命令尊重 `pyproject.toml` 的 `requires-python`。 | src: https://docs.astral.sh/uv/concepts/python-versions/ | quote: "uv will respect Python requirements defined in `requires-python` in the `pyproject.toml` file during project command invocations." | type: official
- [C17] D4 workspace 对成员 `requires-python` 取交集。页脚 2026-09-22。 | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "taking the intersection of all members' `requires-python` values." | type: official
- [C18] D5 `uv init` 应用模板写入 `build-backend = "uv_build"`。页脚 2026-09-22。v0.12 前应用默认不写 build system。 | src: https://docs.astral.sh/uv/concepts/projects/init/ | quote: "build-backend = \"uv_build\"" | type: official
- [C19] D5 原生后端是 `uv_build`。页脚 2026-09-22。 | src: https://docs.astral.sh/uv/concepts/build-backend/ | quote: "also provides a native build backend (`uv_build`)" | type: official
- [C20] D5 `uv build` 是 build frontend。页脚 2026-09-15。 | src: https://docs.astral.sh/uv/concepts/projects/build/ | quote: "When using `uv build`, uv acts as a build frontend" | type: official
- [C21] D6 默认环境目录 `.venv`，在 `pyproject.toml` 旁。页脚 2026-07-21。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "in a `.venv` directory next to the `pyproject.toml`." | type: official
- [C22] D7 其他项目管理工具或 pip→`uv pip` 的指南尚未提供。页脚 2025-07-02。已有标题是 pip→项目。 | src: https://docs.astral.sh/uv/guides/migration/ | quote: "Other guides, such as migrating from another project management tool, or from pip to `uv pip` are not yet available." | type: official
- [C23] D7 标题 “Migrating from pip to a uv project”。导入：`uv add -r requirements.in`。页脚 2026-07-23。 | src: https://docs.astral.sh/uv/guides/migration/pip-to-project/ | quote: "$ uv add -r requirements.in" | type: official
- [C24] D8 缓存变量 `UV_CACHE_DIR`，以及 `--cache-dir`、`tool.uv.cache-dir`。页脚 2026-08-25。 | src: https://docs.astral.sh/uv/concepts/cache/ | quote: "The specific cache directory specified via `--cache-dir`, `UV_CACHE_DIR`, or `tool.uv.cache-dir`." | type: official
- [C25] D8 CI 用 `uv cache prune --ci`。 | src: https://docs.astral.sh/uv/concepts/cache/ | quote: "uv provides a `uv cache prune --ci` command, which removes all pre-built wheels and unzipped source distributions from the cache" | type: official
- [C26] D8 GitHub 文档建议跨 workflow 保存 uv cache。页脚 2026-09-22。 | src: https://docs.astral.sh/uv/guides/integration/github/ | quote: "It may improve CI times to store uv's cache across workflow runs." | type: official
- [C27] D9 额外索引用 `[[tool.uv.index]]`。页脚 2026-08-14。 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "add a `[[tool.uv.index]]` entry to your `pyproject.toml`:" | type: official
- [C28] D9 凭据变量 `UV_INDEX_INTERNAL_PROXY_USERNAME` 与 `UV_INDEX_INTERNAL_PROXY_PASSWORD`（name 大写）。 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "you can set the `UV_INDEX_INTERNAL_PROXY_USERNAME` and `UV_INDEX_INTERNAL_PROXY_PASSWORD` environment variables" | type: official
- [C29] D10 开发依赖表是顶层 `[dependency-groups]`（PEP 735）。页脚 2026-08-14。 | src: https://docs.astral.sh/uv/concepts/projects/dependencies/ | quote: "uv uses the `[dependency-groups]` table (as defined in PEP 735) for declaration of development dependencies." | type: official
- [C30] D10 键 `tool.uv.default-groups`；默认同步包含 `dev` 组。页脚 2026-08-14。 | src: https://docs.astral.sh/uv/concepts/projects/dependencies/ | quote: "By default, uv includes the `dev` dependency group in the environment (e.g., during `uv run` or `uv sync`)." | type: official

## conflicts
- flag 写法不同、未否定能力：layout `uv pip compile requirements.in -o pylock.toml` 与 `uv export -o pylock.toml`；0.6.15 notes `uv pip compile -o pylock.toml requirements.in`；export 页 `--format pylock.toml` 与 `--output-file`。compile 页只重复 `uv pip sync pylock.toml`。

## gaps
- 未打开 0.6.14 及更早 release。“自 0.6.15 起”只据该 tag 的 “preliminary support” / “As of this release”。搜 0.6.12–0.6.14 release 无另一次 pylock 命中，不能当反证。
- 未打开 CLI reference，未核对 `--build-backend` 枚举是否另有别名 `uv`。init 页模板名是 `uv_build`。
- resolution 未给出当前 `version` 整数。Poetry/PDM 无官方迁移命令；索引写明其他工具指南尚未提供。

## leads
- hatchling / flit-core / pdm-backend / setuptools / maturin / scikit-build-core：`uv init --build-backend` 可选；uv_build 只纯 Python。
- pip-tools：迁移指南的源工作流；`uv pip compile` 默认平台相关，`uv.lock` 始终 universal。
- 坑：`first-index` 不同于 pip；`tool.uv.dev-dependencies` 仍合并；`centralized-project-envs` 把默认环境放进缓存。
