# r1-pixi
question: pixi 官方文档里，锁文件、项目清单、workspace、Python 版本、构建、私有 channel/index、CI 缓存、相对 conda 的迁移，各自怎么规定？
checked: https://pixi.prefix.dev/latest/, https://pixi.prefix.dev/latest/workspace/lock_file/, https://pixi.prefix.dev/latest/python/tutorial/, https://pixi.prefix.dev/latest/python/pyproject_toml/, https://pixi.prefix.dev/latest/reference/pixi_manifest/, https://pixi.prefix.dev/latest/reference/environment_variables/, https://pixi.prefix.dev/latest/integration/ci/github_actions/, https://pixi.prefix.dev/latest/deployment/authentication/, https://pixi.prefix.dev/latest/build/backends/, https://pixi.prefix.dev/latest/switching_from/conda/, https://pixi.prefix.dev/latest/switching_from/poetry/, https://pixi.prefix.dev/latest/tutorials/import/, https://github.com/prefix-dev/pixi/issues/3474, https://github.com/prefix-dev/pixi/releases/tag/v0.66.0, https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md

## claims
- [C1] lock: 锁文件名为 `pixi.lock`（YAML，`version: 6`，向后兼容不向前）。| src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "This file is named `pixi.lock`." | type: official
- [C2] lock: 同一 `pixi.lock` 同时锁定 conda 与 PyPI，PyPI 部分由内置 uv 解析写入。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "The uv resolution is included in the lock file directly." | type: official
- [C3] lock: 不读写 `pylock.toml`（PEP 751）；官方 issue #3474「PEP751 support」仍 Open（enhancement, needs-design）。 | src: https://github.com/prefix-dev/pixi/issues/3474 | quote: "implementing export functionality to this lock file format would enhance interoperability" | type: official
- [C4] meta: 同时支持 `pixi.toml` 与 `pyproject.toml`，后者各表加 `tool.pixi` 前缀（`[workspace]`→`[tool.pixi.workspace]`）。 | src: https://pixi.prefix.dev/latest/python/tutorial/ | quote: "We support two manifest formats: `pyproject.toml` and `pixi.toml`." | type: official
- [C5] meta: conda 依赖写 `[dependencies]`/`[tool.pixi.dependencies]`；PyPI 依赖写 `[pypi-dependencies]`/`[tool.pixi.pypi-dependencies]` 或 `[project.dependencies]`（`version`/`extras`/`index`/`git`/`path`/`url`）。 | src: https://pixi.prefix.dev/latest/switching_from/poetry/ | quote: "`[tool.pixi.dependencies]` for conda, `[tool.pixi.pypi-dependencies]` or `[project.dependencies]` for PyPI dependencies" | type: official
- [C6] meta: 同名包 conda 优先；`[dependency-groups]` 与 `[project.optional-dependencies]` 自动映射为同名 feature。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "Pixi takes the conda dependencies over the pypi dependencies." | type: official
- [C7] workspace: `[workspace]` 必填 `channels` 与 `platforms`（`name` 可省默认目录名）。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "The minimally required information in the `workspace` table is:" | type: official
- [C8] workspace: 多环境：`[feature.<name>.*]` 特性 + `[environments]` 组合；字段 `features`/`solve-group`/`no-default-feature`。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "created using the features defined in the `[feature]` tables" | type: official
- [C9] workspace: 注册表 `pixi workspace register` 后可 `pixi run -w name`/`pixi shell -w name`；v0.66.0（2026-03-16）引入。 | src: https://github.com/prefix-dev/pixi/releases/tag/v0.66.0 | quote: "This release brings registered workspaces!" | type: official
- [C10] pyver: Python 是 conda 包（`pixi add python=3.8`/`[dependencies] python = ">=3.9"`）；`requires-python` 自动转成该依赖；free-threaded 用 `python-freethreading`。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "automatically adds the version to the dependencies" | type: official
- [C11] backend: PyPI sdist 在激活的 conda 环境中构建（构建依赖可取 conda 包）；`[pypi-options]` 的 `no-build`/`no-binary`/`no-build-isolation` 控制。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "it's used from the conda environment instead of the system" | type: official
- [C12] backend: 本项目作 pypi path 依赖时经 uv 用 `[build-system]`/`build-backend`，缺省回退 `setuptools.build_meta:__legacy__`。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "build and install the project if it is added as a pypi path dependency" | type: official
- [C13] backend: 自有 build backend 构建 conda 包：`[package]`+`[package.build.backend]`，官方 `pixi-build-python`/`pixi-build-cmake`/`pixi-build-rattler-build` 等，preview flag `pixi-build`，经 `pixi publish` 触发。 | src: https://pixi.prefix.dev/latest/build/backends/ | quote: "what are called build backends" | type: official
- [C14] index: conda channel 键为 `[workspace]`/`[feature.*]` 的 `channels`；私有 prefix.dev/Quetz 用含主机名 URL；`channel-priority` 默认 `strict`。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "use the url including the hostname" | type: official
- [C15] index: 凭证 `pixi auth login <HOST>`：`--token`/`--conda-token`/`--username+--password`/`--s3-*`/`--oauth`；存 keychain，回退 `~/.rattler/credentials.json`。 | src: https://pixi.prefix.dev/latest/deployment/authentication/ | quote: "Bearer tokens are sent with every request" | type: official
- [C16] index: PyPI 源键 `[pypi-options]`（可置 `[workspace.pypi-options]`/`[feature.*.pypi-options]`）：`index-url`（默认 pypi.org/simple）、`extra-index-urls`、`find-links`、`index-strategy` 等；单包可 `index` 钉源。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "options that are specific to PyPI registries" | type: official
- [C17] index: PyPI 凭证：keyring（`--pypi-keyring-provider subprocess` 或全局 `[pypi-config]`，URL 嵌 `user@`）或 `.netrc`；strict first-match。 | src: https://pixi.prefix.dev/latest/deployment/authentication/ | quote: "the uv method of authentication through the python keyring library" | type: official
- [C18] cicache: `PIXI_CACHE_DIR` 指定缓存目录，回退 `RATTLER_CACHE_DIR` → `XDG_CACHE_HOME/pixi` → `rattler::default_cache_dir`。 | src: https://pixi.prefix.dev/latest/reference/environment_variables/ | quote: "Defines the directory where pixi puts its cache." | type: official
- [C19] cicache: 官方 Action `prefix-dev/setup-pixi`：`cache: true` 按 `pixi.lock` 哈希缓存环境、命中跳过安装；另有 `global-cache`/`cache-key`/`cache-write`/`frozen`/`locked`。 | src: https://pixi.prefix.dev/latest/integration/ci/github_actions/ | quote: "use the `pixi.lock` file to generate a hash of the environment" | type: official
- [C20] migrate: `pixi import` 支持 `--format conda-env`（environment.yml，`pip:`→pypi-dependencies）与 `pypi-txt`（requirements.txt）；`--feature`/`--environment`/`--platform` 控制落点。 | src: https://pixi.prefix.dev/latest/tutorials/import/ | quote: "we support two import file formats: `conda-env` and `pypi-txt`" | type: official
- [C21] migrate: `pixi init --import environment.yml` 仅 `conda-env`；反向 `pixi workspace export conda-environment [--from-lockfile]`、`conda-explicit-spec`。 | src: https://pixi.prefix.dev/latest/tutorials/import/ | quote: "only the `conda-env` format is supported by `pixi init --import`" | type: official
- [C22] migrate: 官方对比指南 switching_from/{conda,poetry,uv}；明示无 `base` 环境。 | src: https://pixi.prefix.dev/latest/switching_from/conda/ | quote: "Pixi does not have a base environment" | type: official

## conflicts
- poetry 迁移页写 "We've yet to implement package building and publishing"（https://pixi.prefix.dev/latest/switching_from/poetry/），但 manifest 已有 `[package]`/`[package.build.backend]`（preview `pixi-build`），backends 页写 "for example via `pixi publish`"（https://pixi.prefix.dev/latest/build/backends/）。poetry 页疑似过时。

## gaps
- conda-lock 导入：docs 全库与 CHANGELOG 无 "conda-lock" 字样；`pixi import` 仅 `conda-env`/`pypi-txt`。
- `pylock.toml` 无读写支持（仅 issue #3474 在议）。
- PyPI sdist 是否逐包调 PEP 517 backend：文档仅说经 uv 构建，无直白表述。
- `pixi init --format` 另有 `mojoproject|pep723|conda-script` 取值（CLI ref 页未 web_fetch 取原句）。

## leads
- `pixi init --format pep723|conda-script` 元数据写进单文件脚本（docs/reference/cli/pixi/init/）。
- 全局 `[pypi-config]`（`index-url`/`extra-index-urls`/`keyring-provider` 等）：https://pixi.prefix.dev/latest/reference/pixi_configuration/
- import 路线图 https://github.com/prefix-dev/pixi/issues/4192；prefix.dev 私有 channel 配套 `pixi upload`/`pixi publish`。
