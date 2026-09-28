# r1-uv
question: uv（Astral 出品）在以下 12 个维度上现状分别是什么？特别关注 PEP 751 pylock.toml 支持状态。

checked: https://docs.astral.sh/uv/, https://github.com/astral-sh/uv/blob/main/CHANGELOG.md, https://github.com/astral-sh/setup-uv, https://github.com/astral-sh/rye/pull/1476

## claims
- [C1] uv 定位："An extremely fast Python package and project manager, written in Rust"，单一工具替代 pip、pip-tools、pipx、poetry、pyenv、twine、virtualenv 等多个工具。| src: https://docs.astral.sh/uv/ | quote: "An extremely fast Python package and project manager, written in Rust" | type: official

- [C1-perf] uv 性能宣称 10-100x 快于 pip。| src: https://github.com/astral-sh/uv/blob/main/README.md | quote: "10-100x faster than pip" | type: official

- [C2] uv 项目使用标准 [project] 表（PEP 621），tool.uv 放工具特定配置（dependencies、sources、workspace 等）。| src: https://docs.astral.sh/uv/guides/projects/ | quote: "pyproject.toml contains metadata about your project" with [project] section | type: official

- [C3-pep751-v0.12.17] 自 v0.12.17（2026-09-22）起，uv 在 preview 阶段**拒绝**不符合 PEP 751 的 pylock.toml 文件，验证 wheel 文件名与包名/版本是否匹配。| src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: "Reject pylock.toml files whose wheel filenames do not match their declared package names or versions" | type: official

- [C3-pep751-v0.12.11] 自 v0.12.11（2026-09-08）起，uv 支持**生成** pylock.toml 导出时的缺失哈希值以符合 PEP 751。| src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: "Generate missing artifact hashes when exporting pylock.toml files to ensure they conform to PEP 751" | type: official

- [C3-pep751-status] PEP 751 支持目前处于 preview 阶段（非稳定功能）；uv 能**读取**pylock.toml（用于 uv pip sync），能**导出**生成 pylock.toml（通过 uv export 或 uv lock）。| src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: "preview features" section containing pylock.toml validation | type: official

- [C3-lockfile] uv 主锁文件仍为 uv.lock（TOML 格式，uv 原生格式），非 PEP 751 标准；pylock.toml 是可选/可互操作格式。| src: https://github.com/astral-sh/uv/blob/main/README.md | quote: "universal lockfile" referring to uv.lock | type: official

- [C4] uv workspace：工作区由 [tool.uv.workspace] 表定义，包含 members（glob 模式）和 exclude（可选）；所有成员共享单一 uv.lock。| src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "workspace members operate with a single uv.lock file ensuring consistent set of dependencies across the entire workspace" | type: official

- [C4-editable] workspace 成员间依赖自动作为可编辑安装（通过 workspace = true）。| src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "Dependencies between workspace members are automatically installed as editable" | type: official

- [C5-download] uv python install：自动下载并管理 Python 版本；uv 使用 Astral 的 python-build-standalone 项目作为源（因 Python 官方未提供可分发二进制）。| src: https://docs.astral.sh/uv/guides/install-python/ | quote: "uv uses distributions from the Astral python-build-standalone project" | type: official

- [C5-commands] uv 支持 uv python install、uv python list、uv python upgrade（预览）、uv python pin 等命令管理 Python 版本。| src: https://docs.astral.sh/uv/guides/install-python/ | quote: "uv python install, uv python list" | type: official

- [C5-pypy] uv 支持替代 Python 实现（如 PyPy）。| src: https://docs.astral.sh/uv/guides/install-python/ | quote: "Alternative implementations like PyPy are also supported" | type: official

- [C6] uv init 默认构建后端为 uv 的原生后端（标记为 "uv"），也可通过 --build-backend 指定 hatchling/flit-core/pdm-backend/poetry-core/setuptools/maturin/scikit-build-core。| src: https://docs.astral.sh/uv/reference/cli/ | quote: "uv (default)" build backend option | type: official

- [C6-buildsystem] uv 提供名为 "uv_build" 的原生构建后端（bundled with uv），用于构建项目包。| src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: "Use the bundled uv_build backend only when its version matches active version pins" | type: official

- [C7-resolution] uv 依赖解析过程称为 "resolution"：将需求列表转换为兼容的包版本集合；支持平台特定（默认）和通用解析。| src: https://docs.astral.sh/uv/concepts/resolution/ | quote: "Resolution is the process of taking a list of requirements and converting them to a list of package versions" | type: official

- [C7-strategy] uv 支持解析策略：默认最新版、--resolution lowest/lowest-direct 用于最小版本测试。| src: https://docs.astral.sh/uv/concepts/resolution/ | quote: "resolve the latest compatible versions" or "lowest compatible versions" | type: official

- [C7-binary] uv 主要操作 PyPI wheel 和 sdist；不原生支持 conda 或系统级二进制依赖（如 CUDA、编译库）。| src: https://docs.astral.sh/uv/concepts/resolution/ | quote: (no explicit quote on non-PyPI support) | type: official

- [C8-venv] uv 使用 Python 的 venv 模块创建虚拟环境；自动生成位置通常为项目根 .venv 目录。| src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "Creating virtual environment at: .venv" | type: official

- [C8-command] uv venv 命令可显式创建虚拟环境；uv sync/uv run 自动创建（如需）。| src: https://github.com/astral-sh/uv/blob/main/README.md | quote: (implicit from project workflow) | type: official

- [C9-keyring] uv 支持通过 keyring 库进行索引 URL 认证（via keyring-provider 配置）。| src: https://docs.astral.sh/uv/reference/settings/ | quote: "keyring-provider: Enables keyring CLI for index URL authentication" | type: official

- [C9-index-config] uv 支持 index/index-url/extra-index-url 配置以及 sources 表（用于 Git、URL、本地路径、替代注册表）。| src: https://docs.astral.sh/uv/reference/settings/ | quote: "index, index-url, extra-index-url, index-strategy" | type: official

- [C9-auth-env] uv 可能支持环境变量（需确认具体形式，docs 页面返回 404）；settings 页面提到可通过 pyproject.toml/uv.toml/环境变量/CLI 标志配置。| src: https://docs.astral.sh/uv/reference/settings/ | quote: "Settings can be configured in pyproject.toml, uv.toml, or via environment variables and CLI flags" | type: official

- [C10-action] astral-sh/setup-uv GitHub Action 缓存 uv binary、依赖文件（**/pyproject.toml、**/uv.lock、**/*.py.lock）、可选的 Python 版本。| src: https://github.com/astral-sh/setup-uv | quote: "cache the uv binary, project dependencies, Python installations" | type: official

- [C10-cache-glob] setup-uv 依赖文件 glob 模式包括 **/requirements*.txt、**/constraints*.txt、**/pyproject.toml、**/uv.lock、**/*.py.lock。| src: https://github.com/astral-sh/setup-uv | quote: "cache-dependency-glob pattern" | type: official

- [C10-disable] 某些事件（merge_group、release、tag push、pull_request_target、workflow_run）和自托管运行器默认禁用缓存。| src: https://github.com/astral-sh/setup-uv | quote: "Cache is automatically disabled for certain events" | type: official

- [C11-migration-official] uv 官方仅提供"Migrate from pip to uv projects"指南；其他工具迁移指南尚未可用，GitHub issue #5200 在跟踪。| src: https://docs.astral.sh/uv/guides/migration/ | quote: "Other guides, such as migrating from another project management tool, are not yet available" | type: official

- [C11-rye-timeline] Rye 并入 uv 的时间线：2024-02 Astral 接管 Rye 并推出 uv；2025-08 Rye 正式弃用，迁移到 uv；Astral（包括 uv）于 2026-03-19 被 OpenAI 收购。| src: https://github.com/astral-sh/rye/pull/1476, https://simonwillison.net/2026/mar/19/openai-acquiring-astral/ | quote: "Retire Rye and add a uv migration guide" (PR title) | type: secondary

- [C12-version] 当前版本 0.12.18（released 2026-09-22T23:00:51Z）；历史版本跨越 0.1.x 到 0.12.x。| src: https://api.github.com/repos/astral-sh/uv/releases | quote: "tag_name: 0.12.18, published_at: 2026-09-22" | type: official

- [C12-backing] uv 由 Astral 公司开发（创始人也开发了 Ruff 代码检查器和 ty 类型检查器）；Astral 于 2026-03-19 被 OpenAI 收购，但 uv 作为开源项目继续维护。| src: https://astral.sh/blog/, https://simonwillison.net/2026/mar/19/openai-acquiring-astral/ | quote: "uv is backed by Astral, the creators of Ruff" | type: official

- [C12-release-freq] uv 保持活跃开发，0.12.x 版本系列在 2026-09 月初至月末发布多个版本（0.12.11~0.12.18），周期数天至两周。| src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: (version sequence) | type: official

## conflicts
- (none identified at current checking depth)

## gaps
- C9：uv 是否支持特定环境变量（如 UV_INDEX_*_USERNAME、UV_INDEX_*_TOKEN）的明确文档找不到（reference/environment-variables 页面返回 404）
- C6：uv_build 后端的首个发布版本号和确切发布日期未查到
- C7：uv 是否采用 PubGrub 算法或其他特定解析算法名称无明确文档
- C8：venv 创建时的完整路径规则（包含 Python 版本标识符等）无明确文档

## leads
- PEP 751 支持：目前处于 preview 且不完整（仅验证/导出，非完全替代 uv.lock），建议 R2 追踪何时晋升为稳定功能
- uv_build 后端：官方后端存在但发布时间线不清，建议 R2 查询 GitHub issue/PR #20146、#21918 获得精确时间
- 环保变量认证：需查源码或环境变量完整列表，官方文档缺失，建议 R2 查询 docs.astral.sh 其他页面或源码注释
