# r1-uv
question: uv（Astral）作为 Python 项目管理工具，在清单、锁文件、workspace、CPython、构建后端、依赖组、迁入、CI 缓存、私有源上的官方做法是什么？特别是 uv.lock 和 PEP 751 pylock.toml 的关系。
checked: https://docs.astral.sh/uv/concepts/projects/layout/, https://docs.astral.sh/uv/concepts/projects/init/, https://docs.astral.sh/uv/concepts/projects/config/, https://docs.astral.sh/uv/concepts/projects/dependencies/, https://docs.astral.sh/uv/concepts/projects/workspaces/, https://docs.astral.sh/uv/concepts/projects/build/, https://docs.astral.sh/uv/concepts/python-versions/, https://docs.astral.sh/uv/concepts/resolution/, https://docs.astral.sh/uv/concepts/indexes/, https://docs.astral.sh/uv/concepts/cache/, https://docs.astral.sh/uv/guides/package/, https://docs.astral.sh/uv/guides/migration/, https://docs.astral.sh/uv/guides/migration/pip-to-project/, https://docs.astral.sh/uv/guides/integration/github/, https://github.com/astral-sh/uv/releases/tag/0.6.15

## claims
- [C1] D1：清单是 `pyproject.toml` 的 `[project]`（最小含 name、version）。页 2026-07-21。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "A minimal project definition includes a name and version" | type: official
- [C2] D1：`project.dependencies` 遵循 PEP 621。页 2026-08-14。 | src: https://docs.astral.sh/uv/concepts/projects/dependencies/ | quote: "the table follows the PEP 621 standard." | type: official
- [C3] D1：`uv init` 默认是应用，模板含 `[project]`、`[project.scripts]`、`[build-system]`。页 2026-09-22。 | src: https://docs.astral.sh/uv/concepts/projects/init/ | quote: "Applications are the default target for uv init" | type: official
- [C4] D2：锁文件名 `uv.lock`，位于 `pyproject.toml` 旁。页 2026-07-21。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv creates a uv.lock file next to the pyproject.toml." | type: official
- [C5] D2：`uv.lock` 不是 pylock，其他工具不能用。页 2026-07-21。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "The uv.lock format is specific to uv and not usable by other tools." | type: official
- [C6] D2：项目接口默认锁仍是 `uv.lock`。页 2026-07-21。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv will continue to use the uv.lock format within the project interface." | type: official
- [C7] D2：导出 pylock 的命令是 `uv export -o pylock.toml`。页 2026-07-21。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "run: uv export -o pylock.toml" | type: official
- [C8] D2：从需求生成 pylock：`uv pip compile requirements.in -o pylock.toml`。页 2026-07-21。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "run: uv pip compile requirements.in -o pylock.toml" | type: official
- [C9] D2：安装 pylock：`uv pip sync pylock.toml` 或 `uv pip install -r pylock.toml`。页 2026-07-21。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv pip sync pylock.toml or uv pip install -r pylock.toml" | type: official
- [C10] D2：该能力自 0.6.15，称 preliminary support。 | src: https://github.com/astral-sh/uv/releases/tag/0.6.15 | quote: "preliminary support for the pylock.toml file format, as standardized in PEP 751." | type: official
- [C11] D2：`uv.lock` 默认跨平台。页 2026-07-21。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv.lock is a universal or cross-platform lockfile" | type: official
- [C12] D2：锁记录一个分发文件 hash。页 2026-08-14。 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "uv selects a single hash to record in the lockfile." | type: official
- [C13] D3：`[tool.uv.workspace]` 的 `members` 必填，`exclude` 可选。页 2026-09-22。 | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "the members (required) and exclude (optional) keys" | type: official
- [C14] D3：成员依赖用 `tool.uv.sources` 的 `workspace = true`。页 2026-09-22。 | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "The workspace = true key-value pair in the tool.uv.sources table" | type: official
- [C15] D3：一个 workspace 一把锁。页 2026-09-22。 | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "the workspace shares a single lockfile" | type: official
- [C16] D4：可下载安装 CPython，以及 PyPy、Pyodide。页 2026-07-25。 | src: https://docs.astral.sh/uv/concepts/python-versions/ | quote: "downloading and installing CPython, PyPy, and Pyodide distributions." | type: official
- [C17] D4：解释器钉在 `.python-version`，命令 `uv python pin`。页 2026-07-25。 | src: https://docs.astral.sh/uv/concepts/python-versions/ | quote: "uv python pin command." | type: official
- [C18] D4：除非 `.python-version` 或 `--python`，否则用满足 `requires-python` 的第一个解释器。页 2026-07-25。 | src: https://docs.astral.sh/uv/concepts/python-versions/ | quote: "via a .python-version file or the --python flag." | type: official
- [C19] D5：默认 `build-backend` 是 `uv_build`。页 2026-09-22。 | src: https://docs.astral.sh/uv/concepts/projects/init/ | quote: "build-backend = \"uv_build\"" | type: official
- [C20] D5：可换成 hatchling、flit-core、pdm-backend、setuptools、maturin、scikit-build-core。页 2026-09-22。 | src: https://docs.astral.sh/uv/concepts/projects/init/ | quote: "hatchling, uv_build, flit-core, pdm-backend, setuptools, maturin, or scikit-build-core." | type: official
- [C21] D5：有 `uv build` 与 `uv publish`。页 2026-09-02。 | src: https://docs.astral.sh/uv/guides/package/ | quote: "uv build and uploading them to a registry with uv publish." | type: official
- [C22] D6：可选依赖是 `[project.optional-dependencies]`。 | src: https://docs.astral.sh/uv/concepts/projects/dependencies/ | quote: "Optional dependencies are specified in [project.optional-dependencies]" | type: official
- [C23] D6：开发依赖表是 `[dependency-groups]`（PEP 735）。页 2026-08-14。 | src: https://docs.astral.sh/uv/concepts/projects/dependencies/ | quote: "the [dependency-groups] table (as defined in PEP 735)" | type: official
- [C24] D6：默认索引是 PyPI。页 2026-08-14。 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "By default, uv uses the Python Package Index (PyPI)" | type: official
- [C25] D7：requirements 迁入命令是 `uv add -r requirements.in -c requirements.txt`。页 2026-07-23。 | src: https://docs.astral.sh/uv/guides/migration/pip-to-project/ | quote: "$ uv add -r requirements.in -c requirements.txt" | type: official
- [C26] D7：从其他项目管理工具迁移的指南尚未提供。页 2025-07-02。 | src: https://docs.astral.sh/uv/guides/migration/ | quote: "migrating from another project management tool, or from pip to uv pip are not yet available." | type: official
- [C27] D8：缓存目录可用 `UV_CACHE_DIR`（或 `--cache-dir` / `tool.uv.cache-dir`）。页 2026-08-25。 | src: https://docs.astral.sh/uv/concepts/cache/ | quote: "specified via --cache-dir, UV_CACHE_DIR, or tool.uv.cache-dir." | type: official
- [C28] D8：官方 Action 是 `astral-sh/setup-uv`。页 2026-09-22。 | src: https://docs.astral.sh/uv/guides/integration/github/ | quote: "the official astral-sh/setup-uv action" | type: official
- [C29] D9：私有索引写 `[[tool.uv.index]]`，必填 `url`。 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "via the [[tool.uv.index]] configuration option" | type: official
- [C30] D9：凭证变量是 `UV_INDEX_<NAME>_USERNAME` 与 `UV_INDEX_<NAME>_PASSWORD`。 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "UV_INDEX_INTERNAL_PROXY_USERNAME and UV_INDEX_INTERNAL_PROXY_PASSWORD" | type: official
- [C31] D9：凭证不会写入 `uv.lock`。 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "credentials are never stored in the uv.lock file" | type: official

## conflicts
- layout 与 0.6.15 写 “could be installed by other tools, and vice versa”，同段又给出当前 `uv pip sync` / `uv pip install -r`。src: https://docs.astral.sh/uv/concepts/projects/layout/ , https://github.com/astral-sh/uv/releases/tag/0.6.15
- package（2026-09-02）写 uv init 默认含 `[build-system]`；init（2026-09-22）写 v0.12 前应用默认没有。src: https://docs.astral.sh/uv/guides/package/ , https://docs.astral.sh/uv/concepts/projects/init/

## gaps
- Poetry、Pipfile、conda 无 uv 命令原句。查过 migration 与 pip-to-project。不写成“不支持”。
- `uv.lock` 的 hash 键名未核对。`uv sync` 是否读 pylock 未另写。0.6.15 页只有 “22 Apr”，未逐条翻更早 changelog。

## leads
- PEP 751 留给 pip 工人。另：enable-cache、`$HOME/.cache/uv`、`uv cache prune --ci`、Git/URL/path。
