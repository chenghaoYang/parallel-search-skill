# r1-uv
question: uv（Astral）8 个维度现状：D1 定位/项目文件；D2 uv.lock 与 PEP 751 pylock.toml（命令/版本）；D3 元数据表；D4 workspace；D5 Python 版本管理；D6 构建后端；D7 环境模型；D8 迁移/CI/私有源
checked: https://docs.astral.sh/uv/, https://docs.astral.sh/uv/concepts/projects/, https://docs.astral.sh/uv/concepts/projects/layout/, https://docs.astral.sh/uv/concepts/projects/config/, https://docs.astral.sh/uv/concepts/projects/sync/, https://docs.astral.sh/uv/concepts/projects/workspaces/, https://docs.astral.sh/uv/concepts/projects/export/, https://docs.astral.sh/uv/concepts/python-versions/, https://docs.astral.sh/uv/concepts/build-backend/, https://docs.astral.sh/uv/concepts/indexes/, https://docs.astral.sh/uv/concepts/preview/, https://docs.astral.sh/uv/pip/environments/, https://docs.astral.sh/uv/guides/package/, https://docs.astral.sh/uv/guides/migration/pip-to-project/, https://docs.astral.sh/uv/guides/integration/github/, https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md, https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.6.x.md (+0.5.x–0.11.x), https://api.github.com/repos/astral-sh/uv/releases/tags/0.6.15

## claims
- [C1] uv 定位：官方定义为用 Rust 写的极速 Python 包与项目管理器 | src: https://docs.astral.sh/uv/ | quote: "An extremely fast Python package and project manager, written in Rust." | type: official
- [C2] 定位为单工具替代全家桶 | src: https://docs.astral.sh/uv/ | quote: "A single tool to replace `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv`, and more." | type: official
- [C3] pyproject.toml 是项目必需文件 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv requires this file to identify the root directory of a project." | type: official
- [C4] uv.lock 是 universal/cross-platform 锁文件，人类可读 TOML，应入库但不可手改；格式为 uv 私有 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "The `uv.lock` format is specific to uv and not usable by other tools." | type: official
- [C5] uv 官方说明 pylock.toml 是 PEP 751 标准化、工具无关的解析输出格式，意在替代 requirements.txt | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "`pylock.toml` is a resolution output format intended to replace `requirements.txt` ... standardized and tool-agnostic" | type: official
- [C6] uv 仅在导出目标和 `uv pip` CLI 层面支持 pylock.toml；项目接口仍用 uv.lock | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv will continue to use the `uv.lock` format within the project interface. However, uv supports `pylock.toml` as an export target and in the `uv pip` CLI." | type: official
- [C7] 导出 PEP 751 锁文件的命令为 `uv export --format pylock.toml`（配 `--output-file`）；文档原句 | src: https://docs.astral.sh/uv/concepts/projects/export/ | quote: "PEP 751 defines a TOML-based lockfile format for Python dependencies. uv can export your project's dependency lockfile to this format." | type: official
- [C8] 生成/安装命令：`uv pip compile requirements.in -o pylock.toml`；安装用 `uv pip sync pylock.toml` 或 `uv pip install -r pylock.toml` | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "To install from a `pylock.toml` file, run: `uv pip sync pylock.toml` or `uv pip install -r pylock.toml`" | type: official
- [C9] PEP 751 支持自 uv 0.6.15（发布于 2025-04-22，GitHub release API published_at）起为 "preliminary support" | src: https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.6.x.md | quote: "This release includes preliminary support for the `pylock.toml` file format, as standardized in PEP 751." | type: official
- [C10] 安装 pylock.toml 目前仍是 preview 特性 `pylock`（直接指定文件即可用但会警告；可 `preview-features = ["pylock"]` 静默） | src: https://docs.astral.sh/uv/concepts/preview/ | quote: "`pylock`: Allows installing from `pylock.toml` files." | type: official
- [C11] 元数据用标准 PEP 621 `[project]` 表；requires-python 建议必填 | src: https://docs.astral.sh/uv/concepts/projects/config/ | quote: "It is recommended to set a `requires-python` value" | type: official
- [C12] 无 build system 时 uv 只装依赖不装项目本体；`tool.uv.package` 可强制开关打包 | src: https://docs.astral.sh/uv/concepts/projects/config/ | quote: "If a build system is not defined, uv will not attempt to build or install the project itself, just its dependencies." | type: official
- [C13] workspace 用 `[tool.uv.workspace]`，`members`（必填）/`exclude` 为 glob 列表，每个匹配目录须含 pyproject.toml | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "you must specify the `members` (required) and `exclude` (optional) keys" | type: official
- [C14] 成员间依赖经 `tool.uv.sources` 声明 `workspace = true`，成员间依赖是 editable | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "Dependencies between workspace members are editable." | type: official
- [C15] 不适用 workspace 时可用 path 依赖（如 `bird-feeder = { path = "packages/bird-feeder" }`） | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "inter-package dependencies defined as path dependencies in `tool.uv.sources`" | type: official
- [C16] `uv python install` 安装托管版 CPython/PyPy | src: https://docs.astral.sh/uv/concepts/python-versions/ | quote: "uv bundles a list of downloadable CPython and PyPy distributions for macOS, Linux, and Windows." | type: official
- [C17] `.python-version` 文件提供默认版本请求，uv 向父目录逐层搜索；多版本可用 `.python-versions` | src: https://docs.astral.sh/uv/concepts/python-versions/ | quote: "uv searches for a `.python-version` file in the working directory and each of its parents." | type: official
- [C18] Python 默认自动下载（python-downloads=automatic），可 `manual` 或 `--no-python-downloads` 关闭 | src: https://docs.astral.sh/uv/concepts/python-versions/ | quote: "By default, uv will automatically download Python versions if they cannot be found on the system." | type: official
- [C19] uv 自带构建后端 `uv_build`（uv init 默认），但仅支持纯 Python | src: https://docs.astral.sh/uv/concepts/build-backend/ | quote: "currently only supports pure Python code" | type: official
- [C20] `uv build` 产出到 dist/；`uv publish` 上传（--token/UV_PUBLISH_TOKEN、attestations、publish-url） | src: https://docs.astral.sh/uv/guides/package/ | quote: "uv builds packages into source and binary distributions via `uv build`" and "uploading them to a registry with `uv publish`" | type: official
- [C21] 项目环境放 `.venv`（pyproject.toml 旁），uv run/uv sync 自动建，内置 .gitignore 排除 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "keeping the project and dependencies in a `.venv` directory next to the `pyproject.toml`" | type: official
- [C22] uv pip 默认要求虚拟环境，发现顺序 VIRTUAL_ENV → CONDA_PREFIX（支持 conda 环境）→ .venv；`--system` 装系统环境 | src: https://docs.astral.sh/uv/pip/environments/ | quote: "An activated Conda environment based on the `CONDA_PREFIX` environment variable." | type: official
- [C23] pip→uv 项目迁移：`uv init` 建 pyproject.toml，`uv add -r requirements.in -c requirements.txt` 导入并保留已锁版本 | src: https://docs.astral.sh/uv/guides/migration/pip-to-project/ | quote: "the easiest way to import requirements is with `uv add`" | type: official
- [C24] Poetry/其他迁移指南官方明确"尚未编写"，指向 issue #5200 | src: https://docs.astral.sh/uv/guides/migration/pip-to-project/ | quote: "are not yet written" | type: official
- [C25] CI：官方 action `astral-sh/setup-uv`（建议 pin 版本），`enable-cache: true` 持久化缓存；`uv cache prune --ci` 减缓存 | src: https://docs.astral.sh/uv/guides/integration/github/ | quote: "which installs uv, adds it to PATH, (optionally) persists the cache, and more" | type: official
- [C26] 私有源：`[[tool.uv.index]]`（name/url、explicit、default 等）；`--index-url`→`--default-index`，`--extra-index-url`→`--index` | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "can be configured to use other package indexes, including private indexes, via the `[[tool.uv.index]]` configuration option" | type: official
- [C27] 认证：UV_INDEX_<NAME>_USERNAME/PASSWORD、netrc、keyring、`authenticate` 键；凭据不写入 uv.lock | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "credentials are _never_ stored in the `uv.lock` file" | type: official

## conflicts
- 无硬性冲突。注意细节：preview 页称 "while `pylock.toml` support is in preview"（泛指），但其特性清单中 `pylock` 只覆盖"安装"；export/compile 页未标注 preview。0.6.15 changelog 称整体为 "preliminary support"，与现状（安装 preview、导出正常文档化）措辞略有出入。

## gaps
- `uv_build` 成为默认后端的确切版本未查（文档只述现状）。
- `uv export --format pylock.toml` 是否仍 preview-gated：export 页无 preview 标注，preview 页仅列安装——未获逐字确认。
- conda 仅限 `uv pip` 环境发现；项目工作流（uv sync）是否可用 conda 环境未见官方说明。
- setup-uv 的 enable-cache 具体缓存路径/键细节未逐字核。
- poetry → uv 一键 import（如 poetry.lock 转换）确认不存在，仅有 #5200 占位。

## leads
- `uv.toml` 独立配置文件 + PEP 723 脚本内嵌元数据（单文件脚本）未展开。
- `centralized-project-envs` preview：项目环境可存 uv 缓存而非 .venv。
- `uv pip compile` 支持 `--python-platform` 跨平台锁文件，可作 requirements.txt 替代工作流。
