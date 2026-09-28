# r1-pixi
question: pixi 在清单、锁文件、workspace、Python 版本、构建后端、conda 与 PyPI 依赖、从 conda/Poetry 迁入、CI 缓存、私有 channel/index 上的官方做法是什么？
checked: https://pixi.prefix.dev/latest/reference/pixi_manifest/, https://pixi.prefix.dev/latest/python/pyproject_toml/, https://pixi.prefix.dev/latest/workspace/lock_file/, https://pixi.prefix.dev/latest/tutorials/import/, https://pixi.prefix.dev/latest/deployment/authentication/, https://pixi.prefix.dev/latest/reference/environment_variables/, https://pixi.prefix.dev/latest/workspace/environment/, https://pixi.prefix.dev/latest/integration/ci/github_actions/, https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md, https://raw.githubusercontent.com/prefix-dev/pixi/main/docs/switching_from/poetry.md

## claims
- [C1] D1：pixi.toml 与 pyproject.toml 都能当清单；后者表加 tool.pixi，如 [tool.pixi.workspace]。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "We also support the pyproject.toml file." | type: official
- [C2] D1：同目录都在时，cwd 的 pixi.toml（优先级 5）高于 pyproject.toml（4）。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "the manifest with the highest priority will be used." | type: official
- [C3] D1：[workspace] 最少含 channels、name、platforms。conda 键 [dependencies]，PyPI 键 [pypi-dependencies]。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "Add any conda package dependency" | type: official
- [C4] D1：[project].dependencies 映射为 pypi-dependencies。非 Python 项目更建议 pixi.toml。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "adds the dependencies to the workspace as [pypi-dependencies]." | type: official
- [C5] D6：[project.optional-dependencies] 与 [dependency-groups] 变成同名 feature；pixi init 为每组建 environment，共用 solve-group。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "Pixi features of the same name with the associated pypi-dependencies." | type: official
- [C6] D2：锁文件名 pixi.lock。一次写入全部 environment 与 platform；示例按 linux-64、osx-64 分列。 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "all environments and platforms listed in the manifest." | type: official
- [C7] D2：同一把锁同时覆盖 conda 与 PyPI 的版本要求。 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "for both conda and pypi packages." | type: official
- [C8] D2：uv 的 PyPI 求解直接写入 pixi.lock。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "The uv resolution is included in the lock file directly." | type: official
- [C9] D2：CHANGELOG 0.68.0（2026-05-07）把锁格式升到 v7。 | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md | quote: "This release bump the lock file version to v7." | type: official
- [C10] D3：[workspace.dependencies] 供成员用 { workspace = true } 继承；相对 path 再按成员重锚。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "inherit from per entry by writing { workspace = true }." | type: official
- [C11] D3：多成员各自用 { workspace = true } 选用共享规格。 | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/docs/build/workspace.md | quote: "each member opt in per entry with { workspace = true }." | type: official
- [C12] D6：组键 [feature.<name>] 与 [environments]，字段 features、solve-group、no-default-feature。同 solve-group 版本相同。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "the same version in all environments that have the same solve group" | type: official
- [C13] D4：requires-python 变成 conda 依赖 python，钉在 [dependencies] 或 feature/environment 的 dependencies。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "automatically adds the version to the dependencies." | type: official
- [C14] D4：装 PyPI 源码前必须先在 conda [dependencies] 安装 python。 | src: https://pixi.prefix.dev/latest/workspace/environment/ | quote: "install python in the (conda)[dependencies] section" | type: official
- [C15] D5：PyPI path 依赖用已有 [build-system] 构建。缺省用 uv 的 setuptools.build_meta:__legacy__。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "if it is added as a pypi path dependency." | type: official
- [C16] D5：pixi init --format pyproject 默认 hatchling.build。PyPI 包键是 [pypi-dependencies]，在 conda 之后安装。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "pixi init --format pyproject defaults to hatchling." | type: official
- [C17] D5：preview 的 pixi-build 用 [package].build 打成 conda 包，可与 workspace 同文件或在子目录。 | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/docs/reference/pixi_manifest.md | quote: "built into a conda package" | type: official
- [C18] D6：feature 可同时有 dependencies、pypi-dependencies、channels。环境 channel 是各 feature 的并集。 | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/docs/reference/pixi_manifest.md | quote: "union of the channels of all its features." | type: official
- [C19] D6：[pypi-options] 的 index-url、extra-index-urls。未设时默认 https://pypi.org/simple，extra-index-urls 优先。单包可写 index。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "the default index used is https://pypi.org/simple." | type: official
- [C21] D7：environment.yml 用 pixi import --format=conda-env。pip: 进 pypi-dependencies，并建 no-default-feature 环境。 | src: https://pixi.prefix.dev/latest/tutorials/import/ | quote: "two import file formats: conda-env and pypi-txt." | type: official
- [C22] D7：requirements.txt 用 pixi import --format=pypi-txt，要 --feature 或 --environment。pixi init --import 只支持 conda-env。 | src: https://pixi.prefix.dev/latest/tutorials/import/ | quote: "only the conda-env format is supported by pixi init --import." | type: official
- [C23] D7：无 Poetry 导入命令。把 tool.poetry.dependencies 抄到 tool.pixi.pypi-dependencies；python 只放 tool.pixi.dependencies。 | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/docs/switching_from/poetry.md | quote: "tool.poetry.dependencies into tool.pixi.pypi-dependencies." | type: official
- [C24] D8：缓存为 PIXI_CACHE_DIR，否则 RATTLER_CACHE_DIR，再否则已存在的 XDG_CACHE_HOME/pixi，最后 rattler 默认目录。 | src: https://pixi.prefix.dev/latest/reference/environment_variables/ | quote: "If PIXI_CACHE_DIR is not set, the RATTLER_CACHE_DIR environment variable is used" | type: official
- [C25] D8：环境页默认目录是 ~/.cache/rattler、~/Library/Caches/rattler、%LOCALAPPDATA%\\rattler；子目录 pkgs、repodata、uv-cache、http-cache。环境在 .pixi/envs。 | src: https://pixi.prefix.dev/latest/workspace/environment/ | quote: "PIXI_CACHE_DIR or RATTLER_CACHE_DIR" | type: official
- [C26] D8：Action 为 prefix-dev/setup-pixi@v0.10.0，cache: true；有 pixi.lock 则哈希并跳过安装。 | src: https://pixi.prefix.dev/latest/integration/ci/github_actions/ | quote: "caching is enabled if a pixi.lock file is present." | type: official
- [C27] D9：私有 channel 写在 channels，URL 含主机名。pixi auth login 用 --token 或 --conda-token。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "use the url including the hostname" | type: official
- [C28] D9：私有 PyPI 用 index-url 或 extra-index-urls，URL 带用户名。凭证用 keyring、$HOME/.netrc 或 NETRC。 | src: https://pixi.prefix.dev/latest/deployment/authentication/ | quote: "include your_username@ in the URL of the registry" | type: official
- [C29] D9：conda 凭证在 keyring，否则 ~/.rattler/credentials.json。RATTLER_AUTH_FILE 为唯一来源。S3 可用 AWS_ACCESS_KEY_ID 与 AWS_SECRET_ACCESS_KEY。 | src: https://pixi.prefix.dev/latest/reference/environment_variables/ | quote: "the only source of authentication data used by pixi." | type: official

## conflicts
- 锁版本：lock_file 示例 version: 6；CHANGELOG 0.68.0（2026-05-07）写 bump to v7；pixi_pack 写 version 7 or later。不裁决。
- 缓存默认路径：一页是已存在的 XDG_CACHE_HOME/pixi，另一页是 ~/.cache/rattler、~/Library/Caches/rattler、%LOCALAPPDATA%\\rattler。

## gaps
- PEP 751 / pylock.toml：lock_file、清单、CHANGELOG 全文检索为 0。
- 锁是否写入 token 或 index 密码：authentication 与 lock_file 都没写。
- 无 poetry.lock 导入命令，也无原句否认独立 CPython 安装器。

## leads
- conda 对照：无 base；pixi init 再 pixi add python。https://pixi.prefix.dev/latest/switching_from/conda/
- init --format 还有 mojoproject、pep723、conda-script。
