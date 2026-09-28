# r1-pixi
question: pixi 官方文档里，锁文件、清单表、workspace、Python 版本、构建/PyPI 后端、环境前缀、从 conda 或 Poetry 迁入、CI 缓存、私有 channel 与私有 PyPI、依赖分组的字段名是什么？
checked: https://pixi.prefix.dev/latest/first_workspace/, https://pixi.prefix.dev/latest/workspace/lock_file/, https://pixi.prefix.dev/latest/security/, https://pixi.prefix.dev/latest/reference/pixi_manifest/, https://pixi.prefix.dev/latest/python/pyproject_toml/, https://pixi.prefix.dev/latest/switching_from/uv/, https://pixi.prefix.dev/latest/switching_from/poetry/, https://pixi.prefix.dev/latest/build/getting_started/, https://pixi.prefix.dev/latest/tutorials/import/, https://pixi.prefix.dev/latest/reference/environment_variables/, https://pixi.prefix.dev/latest/integration/ci/github_actions/, https://pixi.prefix.dev/latest/deployment/authentication/, https://pixi.prefix.dev/latest/conda_ecosystem/, https://github.com/prefix-dev/pixi/releases/tag/v0.68.0

## claims
- [C1] D1 锁文件名 `pixi.lock`。 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "This file is named `pixi.lock`." | type: official
- [C2] D1 锁文件页示例 `version: 6`。 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "version: 6" | type: official
- [C3] D1 建议纳入版本控制，不是自动提交。 | src: https://pixi.prefix.dev/latest/security/ | quote: "Keep `pixi.lock` under version control" | type: official
- [C4] D1 允许最终不提交锁文件。 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "If you decide in the end not to commit the lock file" | type: official
- [C5] D1 uv 对照：pixi.lock 的 Format 是 YAML，不是 uv.lock 的 TOML。 | src: https://pixi.prefix.dev/latest/switching_from/uv/ | quote: "Format | TOML | YAML" | type: official
- [C6] D1 v0.68.0（2026-05-07）称锁文件升到 v7。 | src: https://github.com/prefix-dev/pixi/releases/tag/v0.68.0 | quote: "This release bump the lock file version to v7." | type: official
- [C7] D2 清单是 `pixi.toml`；pyproject 同结构，表前加 `tool.pixi`。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "the `[workspace]` table becomes `[tool.pixi.workspace]`" | type: official
- [C8] D2 conda 依赖表名 `[dependencies]`。 | src: https://pixi.prefix.dev/latest/first_workspace/ | quote: "[dependencies]" | type: official
- [C9] D2 `[project].dependencies` 当成 `[pypi-dependencies]`；`requires-python` 变成 `python`。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "adds the dependencies to the workspace as `[pypi-dependencies]`" | type: official
- [C10] D2 可直接用 pyproject：`pixi init --format pyproject`。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "you can run `pixi init --format pyproject`" | type: official
- [C11] D3 子目录含 `[package]` 的 pixi.toml，用 path 拉入。 | src: https://pixi.prefix.dev/latest/switching_from/uv/ | quote: "containing a `[package]` section" | type: official
- [C12] D3 共享池 `[workspace.dependencies]`，引用 `{ workspace = true }`。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "numpy = { workspace = true }" | type: official
- [C13] D4 Python 用 `pixi add python=3.12`，当作 conda 依赖。 | src: https://pixi.prefix.dev/latest/switching_from/uv/ | quote: "add Python as a conda dependency" | type: official
- [C14] D4 有 `[pypi-dependencies]` 时必须在 conda 依赖里写 `python`。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "When using pypi-dependencies, python is needed to resolve pypi dependencies" | type: official
- [C15] D5 作为 PyPI path 依赖时读 `[build-system]`；缺省 `setuptools.build_meta:__legacy__`。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "build-backend = \"setuptools.build_meta:__legacy__\"" | type: official
- [C16] D5 关隔离：`[pypi-options].no-build-isolation`。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "no-build-isolation = [\"detectron2\"]" | type: official
- [C17] D5 `hatchling` 建 Python 包，`pixi-build-python` 打成 conda 包。 | src: https://pixi.prefix.dev/latest/build/getting_started/ | quote: "`hatchling` creates a Python package, and `pixi-build-python` turns the Python package into a conda package." | type: official
- [C18] D6 前缀默认 `.pixi/envs`。 | src: https://pixi.prefix.dev/latest/first_workspace/ | quote: "located in the `.pixi/envs` directory in the root of your workspace." | type: official
- [C19] D6 激活变量 `CONDA_PREFIX`。 | src: https://pixi.prefix.dev/latest/reference/environment_variables/ | quote: "`CONDA_PREFIX`: The path to the environment." | type: official
- [C20] D6/D10 环境表 `[environments]`，键 `features`、`no-default-feature`。 | src: https://pixi.prefix.dev/latest/tutorials/import/ | quote: "simple-env = { features = [\"simple-env\"], no-default-feature = true }" | type: official
- [C21] D7 `pixi import --format=conda-env environment.yml`。 | src: https://pixi.prefix.dev/latest/tutorials/import/ | quote: "pixi import --format=conda-env environment.yml" | type: official
- [C22] D7 `pixi init --import` 只支持 conda-env。 | src: https://pixi.prefix.dev/latest/tutorials/import/ | quote: "only the `conda-env` format is supported by `pixi init --import`." | type: official
- [C23] D7 pip：`pixi import --format=pypi-txt`；只列这两种格式。 | src: https://pixi.prefix.dev/latest/tutorials/import/ | quote: "two import file formats: `conda-env` and `pypi-txt`." | type: official
- [C24] D7 Poetry 对照要求把依赖抄进 `tool.pixi.pypi-dependencies`。 | src: https://pixi.prefix.dev/latest/switching_from/poetry/ | quote: "into `tool.pixi.pypi-dependencies`" | type: official
- [C25] D8 缓存变量 `PIXI_CACHE_DIR`，否则 `RATTLER_CACHE_DIR`。 | src: https://pixi.prefix.dev/latest/reference/environment_variables/ | quote: "If `PIXI_CACHE_DIR` is not set, the `RATTLER_CACHE_DIR` environment variable is used." | type: official
- [C26] D8 setup-pixi 有 pixi.lock 则默认缓存项目环境。 | src: https://pixi.prefix.dev/latest/integration/ci/github_actions/ | quote: "project environment caching is enabled if a `pixi.lock` file is present." | type: official
- [C27] D9 channel 字段 `[workspace].channels`，私有 channel 用 URL。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "https://repo.prefix.dev/channel-name" | type: official
- [C28] D9 PyPI 字段 `index-url`、`extra-index-urls`。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "`index-url`: replaces the main index url. `extra-index-urls`: adds an extra index url." | type: official
- [C29] D9 凭据：`pixi auth login`，否则 `~/.rattler/credentials.json` 或 `RATTLER_AUTH_FILE`。 | src: https://pixi.prefix.dev/latest/deployment/authentication/ | quote: "located at `~/.rattler/credentials.json`" | type: official
- [C30] D9 PyPI 用 keyring 或 `.netrc`；清单 URL 可带用户名。 | src: https://pixi.prefix.dev/latest/deployment/authentication/ | quote: "https://your_username@custom-registry.com/simple" | type: official
- [C31] D10 dependency-groups 与 optional-dependencies 变成同名 feature。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "interpret them as Pixi features of the same name" | type: official
- [C32] D10 `[tool.pixi.environments]` 键 `features`、`solve-group`。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "solve-group = \"default\"" | type: official
- [C33] D10 单包 extras 字段名 `extras`。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "extras = [\"dataframe\", \"sql\"]" | type: official

## conflicts
- 锁版本：lock_file 与 first_workspace 示例 `version: 6`；v0.68.0 notes 写 "bump the lock file version to v7."
- manifest 写 no-build-isolation "can only be set per package"，下文又允许 `= true`。
- Poetry 页 "We've yet to implement package building and publishing"、目录 `./.pixi`、`[tool.pixi]`，对照 `pixi publish`、`.pixi/envs`、`[tool.pixi.workspace]`。


## gaps
- PEP 751/pylock：锁文件页全文、uv 对照、v0.68.0 notes 无导出命令。不写成全站从未提及。
- init 的 .gitignore 是否含 pixi.lock：页面未给内容；templates/gitignore raw 404。
- 未出现 pyenv；无 poetry.lock 导入命令；打开页未点名 conda-lock。
- CI 缓存环境目录，不是 PIXI_CACHE_DIR。

## leads
- conda：前缀常在 `~/miniconda3/envs/`。export conda-environment 页未打开。
- rattler：同页 "Pixi is powered by Rattler"；变量 `RATTLER_*`；rattler-build。
- conda-lock：打开页未点名。
