# r1-pixi
question: pixi 官方文档里，项目规格、锁文件、workspace、Python 从哪来、构建、环境目录、依赖特性、conda channel 与 PyPI 私有源、CI 缓存、从 conda/poetry 迁入，各自的文件名和字段是什么？它和 conda 是不是同一个工具？
checked: https://pixi.prefix.dev/latest/first_workspace/, https://pixi.prefix.dev/latest/reference/pixi_manifest/, https://pixi.prefix.dev/latest/python/pyproject_toml/, https://pixi.prefix.dev/latest/workspace/lock_file/, https://pixi.prefix.dev/latest/workspace/environment/, https://pixi.prefix.dev/latest/reference/environment_variables/, https://pixi.prefix.dev/latest/concepts/conda_pypi/, https://pixi.prefix.dev/latest/conda_ecosystem/, https://pixi.prefix.dev/latest/switching_from/conda/, https://pixi.prefix.dev/latest/switching_from/poetry/, https://pixi.prefix.dev/latest/tutorials/import/, https://pixi.prefix.dev/latest/reference/cli/pixi/init/, https://pixi.prefix.dev/latest/build/python/, https://pixi.prefix.dev/latest/integration/ci/github_actions/

## claims
- [C1] D1 规格文件是 pixi.toml。 | src: https://pixi.prefix.dev/latest/first_workspace/ | quote: "The `pixi.toml` file is the manifest of your Pixi workspace." | type: official
- [C2] D1 pyproject.toml 同结构，表名前加 tool.pixi。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "except that you need to prepend the tables with `tool.pixi` instead of just the table name." | type: official
- [C3] D3 私有 conda channel 用带主机名的 URL。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "To access private or public channels on prefix.dev or Quetz use the url including the hostname:" | type: official
- [C5] D3 channel-priority 默认 strict，按 channels 列表顺序只用第一个含该包的 channel。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "`strict`: **Default**, The channels are used in the order they are defined in the `channels` list." | type: official
- [C6] D3 [workspace].platforms 的每个平台都会求解并写入 pixi.lock。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "Pixi solves the dependencies for all these platforms and puts them in the lock file (`pixi.lock`)." | type: official
- [C7] D2 锁文件名 pixi.lock。 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "This file is named `pixi.lock`." | type: official
- [C8] D2 lock_file 页示例是 version: 6。 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "version: 6" | type: official
- [C9] D4 [dependencies] 装的是 conda 包。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "Add any conda package dependency that you want to install into the environment." | type: official
- [C10] D4 requires-python 变成 python 依赖。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "Pixi understands that field and automatically adds the version to the dependencies." | type: official
- [C11] D4/D8 同时基于 conda 与 PyPI。 | src: https://pixi.prefix.dev/latest/concepts/conda_pypi/ | quote: "Pixi is built on top of both the conda and PyPI ecosystems." | type: official
- [C12] D4 [pypi-dependencies] 要求先在 conda [dependencies] 安装 python。 | src: https://pixi.prefix.dev/latest/workspace/environment/ | quote: "`pixi` requires to first install `python` in the (conda)`[dependencies]` section of the `pixi.toml` file." | type: official
- [C13] D8 `pixi add --pypi` 写入的表示例表名是 [pypi-dependencies]。 | src: https://pixi.prefix.dev/latest/first_workspace/ | quote: "[pypi-dependencies]" | type: official
- [C14] D8 未设 index-url 时默认 https://pypi.org/simple。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "If this is not set the default index used is `https://pypi.org/simple`." | type: official
- [C15] D8 单个 PyPI 包可用 index 指定索引 URL。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "The index parameter allows you to specify the URL of a custom package index for the installation of a specific package." | type: official
- [C16] D5 构建后端名是 pixi-build-python，用来把 Python 包做成 Pixi 包。 | src: https://pixi.prefix.dev/latest/build/python/ | quote: "`pixi-build-python` creates a Pixi package out of a Python package." | type: official
- [C17] D6 环境目录默认 .pixi/envs。 | src: https://pixi.prefix.dev/latest/workspace/environment/ | quote: "All Pixi environments are by default located in the `.pixi/envs` directory of the workspace." | type: official
- [C19] D6 环境可改到工作区外，配置名 detached-environments。 | src: https://pixi.prefix.dev/latest/switching_from/conda/ | quote: "you can use the detached-environments feature of pixi." | type: official
- [C20] D7 未设 no-default-feature = true 时，环境隐含包含 default feature。 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "Unless `no-default-feature` is set to `true`, the default feature is implicitly included in the environment." | type: official
- [C22] D7 dependency-groups 变成同名 feature 的 pypi-dependencies。 | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "If your python project includes dependency groups, Pixi will automatically interpret them as Pixi features of the same name with the associated `pypi-dependencies`." | type: official
- [C23] D9 未设 PIXI_CACHE_DIR 时用 RATTLER_CACHE_DIR。 | src: https://pixi.prefix.dev/latest/reference/environment_variables/ | quote: "If `PIXI_CACHE_DIR` is not set, the `RATTLER_CACHE_DIR` environment variable is used." | type: official
- [C24] D9 setup-pixi 在有 pixi.lock 时默认缓存项目环境。 | src: https://pixi.prefix.dev/latest/integration/ci/github_actions/ | quote: "By default, project environment caching is enabled if a `pixi.lock` file is present." | type: official
- [C25] D9 --frozen 对应环境变量 PIXI_FROZEN。 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "It can also be controlled by the `PIXI_FROZEN` environment variable (example: `PIXI_FROZEN=true`)." | type: official
- [C26] D10 `pixi init --import` 用环境文件生成 pixi.toml 的 dependencies。 | src: https://pixi.prefix.dev/latest/reference/cli/pixi/init/ | quote: "When importing an environment, the `pixi.toml` will be created with the dependencies from the environment file." | type: official
- [C27] D10 `pixi import` 只支持 conda-env 与 pypi-txt。 | src: https://pixi.prefix.dev/latest/tutorials/import/ | quote: "At the time of writing, we support two import file formats: `conda-env` and `pypi-txt`." | type: official
- [C28] D10 从 poetry 迁入是手抄 tool.poetry.dependencies 到 tool.pixi.pypi-dependencies。 | src: https://pixi.prefix.dev/latest/switching_from/poetry/ | quote: "It's best to duplicate the dependencies, basically making an exact copy of the `tool.poetry.dependencies` into `tool.pixi.pypi-dependencies`." | type: official
- [C29] 不是 conda。生态页把 Pixi 与 conda/mamba 并列，并写 Not a drop-in replacement。 | src: https://pixi.prefix.dev/latest/conda_ecosystem/ | quote: "Not a drop-in replacement — it rethinks the workflow." | type: official

## conflicts
- name 是否必填，同页两句：https://pixi.prefix.dev/latest/reference/pixi_manifest/ "The minimally required information in the `workspace` table is:" 与 "If the name is not specified, the name of the directory that contains the workspace is used."
- lock 示例都是 version: 6。A conda: URL https://pixi.prefix.dev/latest/first_workspace/ 。B kind: conda https://pixi.prefix.dev/latest/workspace/lock_file/ 。
- 缓存默认：变量页 XDG_CACHE_HOME/pixi https://pixi.prefix.dev/latest/reference/environment_variables/ ；环境页 $XDG_CACHE_HOME/rattler 或 $HOME/.cache/rattler https://pixi.prefix.dev/latest/workspace/environment/ 。
- 构建：poetry 页 "We've yet to implement package building and publishing" https://pixi.prefix.dev/latest/switching_from/poetry/ ；教程已有 pixi-build-python https://pixi.prefix.dev/latest/build/python/ 。

## gaps
- 无 pylock.toml。未打开 changelog，不能确认锁是否已不是 version 6。
- 未打开 pixi_configuration，故 [cache] 与 [pypi-config] 无原句。
- 无 poetry.lock 导入。conda-first、solve-group、--format 枚举、extra-index-urls、v0.81.0 未入主张。

## leads
- conda 仍独立，未被 pixi 取代：https://pixi.prefix.dev/latest/conda_ecosystem/ 。
- mamba/micromamba 只点名：https://pixi.prefix.dev/latest/concepts/conda_pypi/ 。rattler-build 另列，不写配方：https://pixi.prefix.dev/latest/conda_ecosystem/ 。
