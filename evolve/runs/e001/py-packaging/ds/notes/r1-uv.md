# r1-uv
question: uv（Astral 出品）在以下 10 个维度上，官方文档/changelog 是怎么说的？D1 定位/生态范围；D2 清单标准；D3 锁文件（PEP 751支持现状、版本、发布日期）；D4 解析器；D5 Python版本管理；D6 构建后端；D7 Workspace/monorepo；D8 私有源+认证；D9 CI缓存；D10 迁移路径
checked: https://peps.python.org/pep-0751/, https://docs.astral.sh/uv/, https://docs.astral.sh/uv/concepts/projects/dependencies/, https://docs.astral.sh/uv/concepts/projects/index/, https://docs.astral.sh/uv/reference/settings/, https://docs.astral.sh/uv/guides/projects, https://docs.astral.sh/uv/guides/migration/, https://github.com/astral-sh/uv/releases, https://docs.astral.sh/uv/reference/cli/, https://docs.astral.sh/uv/concepts/indexes/, https://docs.astral.sh/uv/concepts/authentication/, https://github.com/astral-sh/setup-uv, https://github.com/astral-sh/uv/issues/12584, https://github.com/astral-sh/uv/blob/main/CHANGELOG.md, https://docs.astral.sh/uv/concepts/projects/layout/, https://docs.astral.sh/uv/concepts/projects/export/, https://docs.astral.sh/uv/reference/settings/

## claims
- [C1] uv是"An extremely fast Python package and project manager"，集成了pip、pip-tools、pipx、poetry、pyenv、twine、virtualenv功能 | src: https://docs.astral.sh/uv/ | quote: "An extremely fast Python package and project manager, written in Rust" | type: official
- [C2] D1: uv管理纯PyPI包，项目管理中支持dependencies、Python版本、虚拟环境，但文档中未明确提及非Python系统依赖管理 | src: https://docs.astral.sh/uv/ | quote: "Project management...Python version installation...Workspace support" | type: official
- [C3] D2: pyproject.toml使用标准[project]表(PEP 621)和[project.dependencies] | src: https://docs.astral.sh/uv/guides/projects | quote: "The `pyproject.toml` contains metadata about your project" using standard sections | type: official
- [C4] D2: 支持[dependency-groups]表(PEP 735)用于开发依赖 | src: https://docs.astral.sh/uv/concepts/projects/dependencies/ | quote: "Development dependencies use the `[dependency-groups]` table" | type: official
- [C5] D3: uv.lock是TOML格式的跨平台锁文件 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv.lock File...This cross-platform lockfile captures exact resolved package versions" | type: official
- [C6] D3: PEP 751状态为Final，标题"A file format to record Python dependencies for installation reproducibility"，2025年3月31日确定 | src: https://peps.python.org/pep-0751/ | quote: "Status: Final...resolved on March 31, 2025" | type: official
- [C7] D3: uv支持导出到pylock.toml格式，使用`uv export --format pylock.toml`命令 | src: https://docs.astral.sh/uv/concepts/projects/export/ | quote: "uv fully supports exporting to pylock.toml format...$ uv export --format pylock.toml" | type: official
- [C8] D3: uv支持从pylock.toml导入（pip install/sync），但uv.lock更强大、包含pylock.toml无法表达的功能 | src: https://docs.astral.sh/uv/concepts/projects/export/ | quote: "the uv.lock format is more powerful and includes features that cannot be expressed in requirements.txt" | type: official
- [C9] D3: GitHub issue #12584(2025-03-31)提出PEP 751支持，目前实现为export/import模式而非完全替代uv.lock | src: https://github.com/astral-sh/uv/issues/12584 | quote: "a fully standardized format...some of uv's functionality cannot be expressed in the `pylock.toml` format" | type: official
- [C10] D3: v0.12.11增加PEP 751一致性验证，v0.12.0引入严格的pylock.toml验证（锁文件名必须为pylock.toml或变体如pylock.dev.toml） | src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: "Generate missing artifact hashes when exporting `pylock.toml` files to ensure they conform to PEP 751...Lockfile filenames must be `pylock.toml` or a single-name variant" | type: official
- [C11] D4: uv使用PubGrub依赖解析算法 | src: https://github.com/astral-sh/uv | quote: "The dependency resolver uses PubGrub" | type: official
- [C12] D5: `uv python list` - 显示可用Python版本 | src: https://docs.astral.sh/uv/reference/cli/ | quote: "uv python list — Display available Python versions" | type: official
- [C13] D5: `uv python install` - 下载并安装特定Python版本 | src: https://docs.astral.sh/uv/reference/cli/ | quote: "uv python install — Download and install specific Python versions" | type: official
- [C14] D5: `uv python pin` - 通过.python-version文件为项目设置Python版本 | src: https://docs.astral.sh/uv/reference/cli/ | quote: "uv python pin — Set a Python version for a project via `.python-version` file" | type: official
- [C15] D5: 提供uv python upgrade、find、dir、uninstall、update-shell等子命令 | src: https://docs.astral.sh/uv/reference/cli/ | quote: "uv python upgrade...uv python find...uv python dir...uv python uninstall...uv python update-shell" | type: official
- [C16] D6: 构建后端为uv_build（PEP 517），配置在[build-system]中 | src: https://docs.astral.sh/uv/guides/projects | quote: "[build-system]...specifying the build backend (e.g., `uv_build`)" | type: official
- [C17] D6: uv_build支持配置module-name、module-root、namespace、data、wheel-exclude、source-exclude、source-include等选项 | src: https://docs.astral.sh/uv/reference/settings | quote: "Build backend configuration...for customizing wheel and source distribution creation" | type: official
- [C18] D6: v0.12.0将默认构建后端改为uv_build，新项目自动使用uv_build | src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: "uv init now creates projects with the `uv_build` build system" | type: official
- [C19] D7: workspace通过[tool.uv.workspace]声明，需要指定members（必需）和exclude（可选）键 | src: https://github.com/astral-sh/uv/blob/main/docs/concepts/projects/workspaces.md | quote: "you must specify the `members` (required) and `exclude` (optional) keys, which direct the workspace to include or exclude specific directories" | type: official
- [C20] D7: workspace members使用glob模式匹配，示例：members = ["packages/*"]、exclude = ["packages/seeds"] | src: https://github.com/astral-sh/uv/blob/main/docs/concepts/projects/workspaces.md | quote: "Example Configuration...members = [\"packages/*\"]...exclude = [\"packages/seeds\"]" | type: official
- [C21] D7: workspace root既是workspace声明所在目录，也必须是workspace member，共享单一锁文件 | src: https://github.com/astral-sh/uv/blob/main/docs/concepts/projects/workspaces.md | quote: "Workspace Root: Every workspace needs a root...Shared Lockfile: The workspace maintains a single lockfile" | type: official
- [C22] D8: 通过[[tool.uv.index]]定义自定义索引 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "[[tool.uv.index]]" | type: official
- [C23] D8: 认证方式支持：环境变量(UV_INDEX_[NAME]_USERNAME/PASSWORD)、keyring、netrc自动发现 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "Environment variables — Set `UV_INDEX_[NAME]_USERNAME` and `UV_INDEX_[NAME]_PASSWORD`...credential providers — uv automatically discovers credentials from netrc and keyring systems" | type: official
- [C24] D8: 索引按定义顺序优先级查询，默认first-index策略防止依赖混淆攻击 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "Indexes are prioritized in the order in which they're defined...default to the `first-index` strategy to prevent dependency confusion attacks" | type: official
- [C25] D8: 支持通过tool.uv.sources将特定包锁定到特定索引 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "Pinning packages to specific indexes via `tool.uv.sources`" | type: official
- [C26] D8: uv auth CLI用于认证管理 | src: https://docs.astral.sh/uv/concepts/authentication/ | quote: "The `uv auth` CLI — A command-line interface for managing authentication" | type: official
- [C27] D8: 支持HTTP认证、Git认证、TLS证书 | src: https://docs.astral.sh/uv/concepts/authentication/ | quote: "HTTP authentication...Git authentication...TLS certificates — For secure connections" | type: official
- [C28] D9: astral-sh/setup-uv GitHub Action用于CI集成 | src: https://github.com/astral-sh/setup-uv | quote: "The `setup-uv` GitHub Action installs and configures the uv Python package manager for CI/CD workflows" | type: official
- [C29] D9: setup-uv支持缓存、自动版本解析、Python安装缓存、glob模式缓存键 | src: https://github.com/astral-sh/setup-uv | quote: "Cache the installed version of uv...Optional GitHub Actions cache for dependencies with configurable glob patterns...Python installation caching support" | type: official
- [C30] D9: setup-uv支持enable-cache参数和cache-dependency-glob自定义缓存模式 | src: https://github.com/astral-sh/setup-uv | quote: "`enable-cache`: Auto-detection for cache usage...`cache-dependency-glob`: Custom file patterns for cache invalidation" | type: official
- [C31] D10: 仅提供"Migrate from pip to uv projects"的官方文档 | src: https://docs.astral.sh/uv/guides/migration/ | quote: "The only completed migration guide is: **\"Migrate from pip to uv projects**\"" | type: official
- [C32] D10: 其他迁移指南（pip-tools、Poetry、virtualenv、pyenv）未完成，GitHub issue #5200跟踪进度 | src: https://docs.astral.sh/uv/guides/migration/ | quote: "Other guides, such as migrating from another project management tool, or from pip to `uv pip` are not yet available...tracked in issue #5200" | type: official
- [C33] 最新版本v0.12.18发布于2026-09-22 | src: https://github.com/astral-sh/uv/releases | quote: "Released: September 22, 2026" | type: official
- [C34] PEP 621用于标准化pyproject.toml的[project]表结构 | src: https://docs.astral.sh/uv/concepts/projects/dependencies/ | quote: "`project.dependencies`: Published dependencies following PEP 621 standards" | type: official

## conflicts
- uv.lock vs pylock.toml定位不同：issue #12584(2025-03-31)表示pylock.toml无法完全替代uv.lock功能，因此uv采用export/import模式而非完全迁移。但WebSearch提到v0.6.15(April 2025)支持PEP 751，时间上出现2个月的差异，需确认具体版本。

## gaps
- D1: 是否支持非Python系统依赖/编译依赖（如C库、system packages）未在官方文档中明确说明
- D3: uv最早支持PEP 751的版本号有矛盾：WebSearch提v0.6.15（April 2025），但CHANGELOG显示v0.12.0/v0.12.11涉及pylock.toml，需确认初始支持版本
- D9: setup-uv默认缓存路径/目录未在文档中明确列出

## leads
- 需查证uv.lock格式的完整规范文档，了解其与pylock.toml的技术差异
- PEP 751的采纳进度：Astral等工具何时完全支持为一级生成格式（而非仅export）
- uv项目迁移指南进度跟踪 (GitHub issue #5200)
