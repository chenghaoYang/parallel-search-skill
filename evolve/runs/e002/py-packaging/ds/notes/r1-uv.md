# r1-uv
question: uv在锁文件、workspace/monorepo、Python版本管理、构建后端、依赖解析与速度、私有源配置、全局工具运行、迁移路径、生态定位这9个维度上的官方说法？特别是PEP 751支持状态（导出 vs 原生使用）。
checked: https://docs.astral.sh/uv/, https://docs.astral.sh/uv/guides/projects/, https://github.com/astral-sh/uv, https://docs.astral.sh/uv/concepts/lockfile/, https://docs.astral.sh/uv/guides/tools/, https://docs.astral.sh/uv/concepts/resolution/, https://docs.astral.sh/uv/concepts/projects/workspaces/, https://docs.astral.sh/uv/guides/install-python/, https://docs.astral.sh/uv/concepts/build-backend/, https://docs.astral.sh/uv/concepts/indexes/, https://docs.astral.sh/uv/guides/migration/, https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md

## claims

- [C1] uv的原生锁文件格式是`uv.lock`（TOML格式，跨平台单文件），由`uv lock`命令生成 | src: https://docs.astral.sh/uv/guides/projects/ | quote: "uv.lock is a cross-platform lockfile that contains exact information about your project's dependencies" | type: official

- [C2] uv可导出lockfile到pylock.toml格式，`uv export`命令支持alternate format输出 | src: https://docs.astral.sh/uv/reference/cli/ | quote: "Export the project's lockfile to an alternate format" | type: official

- [C3] 从v0.12.11 (2026-09-08)起，uv在导出pylock.toml时生成缺失的artifact hashes以符合PEP 751规范，作为preview feature | src: https://github.com/astral-sh/uv/releases/tag/0.12.11 | quote: "Generate missing artifact hashes when exporting pylock.toml files to ensure they conform to PEP 751 ([#20146])" | type: official | version: 0.12.11

- [C4] 从v0.12.0 (2026-07-28)起，uv可读取和验证pylock.toml文件（拒绝无效的pylock.toml文件和artifacts），支持PEP 751规范 | src: https://github.com/astral-sh/uv/releases/tag/0.12.0 | quote: "Reject invalid pylock.toml files and artifacts...uv now validates additional requirements from the pylock.toml specification" | type: official | version: 0.12.0

- [C5] uv workspace中所有member共享单个lockfile，每个member有自己的pyproject.toml | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "In a workspace, each package defines its own pyproject.toml, but the workspace shares a single lockfile" | type: official

- [C6] workspace members通过`[tool.uv.sources]`配置互相依赖，使用`workspace = true` | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "Members can depend on each other through tool.uv.sources with workspace = true" | type: official

- [C7] uv支持`uv python install`命令独立下载和管理Python版本（不依赖系统Python），使用Astral的python-build-standalone分发版 | src: https://docs.astral.sh/uv/guides/install-python/ | quote: "uv can also install and manage Python versions...uv will automatically download Python versions when they are required" | type: official

- [C8] uv支持`uv python pin`命令固定项目的Python版本 | src: https://docs.astral.sh/uv/reference/cli/ | quote: "uv python pin" (列于CLI命令列表) | type: official

- [C9] uv提供原生build backend `uv_build`，与uv深度集成，性能优秀；pure Python项目默认选择 | src: https://docs.astral.sh/uv/concepts/build-backend/ | quote: "uv provides a native build backend (uv_build) that integrates tightly with uv to improve performance and user experience" | type: official

- [C10] `uv init`默认生成使用`uv_build`的packaged project结构（src/layout + [build-system]声明），取代之前的unpackaged layout | src: https://github.com/astral-sh/uv/releases/tag/0.12.0 | quote: "Projects created with uv init now declare a build system...Now, uv init example defines a [build-system] using uv_build" | type: official | version: 0.12.0

- [C11] uv用Rust实现 | src: https://github.com/astral-sh/uv | quote: "An extremely fast Python package and project manager, written in Rust" | type: official

- [C12] 官方声称uv比pip快10-100倍，基于warm cache benchmark | src: https://github.com/astral-sh/uv | quote: "10-100x faster than pip" | type: official

- [C13] uv的Git实现基于Cargo（Rust package manager），用于依赖解析 | src: https://github.com/astral-sh/uv | quote: "uv's Git implementation is based on Cargo" | type: official

- [C14] `[[tool.uv.index]]`表格配置私有源，支持name和url字段，按定义顺序优先级递减 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "Indexes are prioritized in the order in which they're defined, such that the first index listed in the configuration file is the first index consulted" | type: official

- [C15] 私有源认证支持三种方式：环境变量(UV_INDEX_<NAME>_USERNAME等)、URL内嵌凭证、netrc/keyring自动发现 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "set variables like UV_INDEX_INTERNAL_PROXY_USERNAME...Include credentials directly in the URL...uv automatically discovers credentials from netrc and keyring systems" | type: official

- [C16] `uvx`和`uv tool run`等价，都在隔离环境中运行Python工具；不同于`uv pip install`，工具模块不对当前环境暴露 | src: https://docs.astral.sh/uv/guides/tools/ | quote: "This is exactly equivalent to: uv tool run ruff...uv installs tools into temporary, isolated environments" | type: official

- [C17] 官方仅提供"Migrate from pip to uv projects"迁移指南，未提供Poetry迁移指南；其他工具迁移指南标记为"not yet available" | src: https://docs.astral.sh/uv/guides/migration/ | quote: "Migrate from pip to uv projects is the only migration guide currently documented. Other guides...are not yet available" | type: official

- [C18] 官方声称uv可替代pip、pip-tools、pipx、poetry、pyenv、twine、virtualenv等工具 | src: https://docs.astral.sh/uv/ | quote: "A single tool to replace pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more" | type: official

## conflicts

## gaps
- uv是否将pylock.toml作为默认/可选的原生lockfile格式（即`uv lock`直接生成pylock.toml），还是仅支持`uv export`导出到该格式？文档未明确说明uv.lock和pylock.toml的互操作性或切换机制
- `uv python pin`的确切功能、命令语法、是否支持按项目固定版本（.python-version文件）或全局固定

## leads
- 0.12.11版本preview feature中的pylock.toml hashes生成表明uv正在完善PEP 751支持，后续可能提升pylock.toml地位
- uv的workspace + shared lockfile模型与Cargo类似，可作为monorepo最佳实践对标
