# r1-uv
question: Astral 官方文档里，uv 怎样做项目元数据、锁文件（含 PEP 751 pylock.toml 的读和写）、workspace、Python 版本、构建后端、虚拟环境、依赖组、私有 index、CI 缓存和从 Poetry/pip 迁入？
checked: https://docs.astral.sh/uv/concepts/projects/layout/, https://docs.astral.sh/uv/concepts/projects/export/, https://docs.astral.sh/uv/pip/compile/, https://docs.astral.sh/uv/concepts/projects/sync/, https://docs.astral.sh/uv/concepts/resolution/, https://docs.astral.sh/uv/concepts/projects/workspaces/, https://docs.astral.sh/uv/concepts/python-versions/, https://docs.astral.sh/uv/concepts/projects/init/, https://docs.astral.sh/uv/concepts/build-backend/, https://docs.astral.sh/uv/concepts/projects/config/, https://docs.astral.sh/uv/concepts/projects/dependencies/, https://docs.astral.sh/uv/concepts/indexes/, https://docs.astral.sh/uv/concepts/cache/, https://docs.astral.sh/uv/guides/integration/github/, https://docs.astral.sh/uv/guides/migration/, https://docs.astral.sh/uv/guides/migration/pip-to-project/, https://github.com/astral-sh/uv/releases/tag/0.6.15

## claims
- [C1] D1：元数据文件是 pyproject.toml；紧接的最小示例是 [project] 的 name 与 version。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "Python project metadata is defined in a pyproject.toml file." | type: official
- [C2] D1：uv add 写入 project.dependencies。 | src: https://docs.astral.sh/uv/concepts/projects/dependencies/ | quote: "An entry will be added in the project.dependencies field" | type: official
- [C3] D2：锁文件名 uv.lock，位于 pyproject.toml 旁。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv creates a uv.lock file next to the pyproject.toml." | type: official
- [C4] D2：uv.lock 仅 uv 可用，勿手改。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "The uv.lock format is specific to uv and not usable by other tools." | type: official
- [C5] D2：显式更新用 uv lock。同页写 uv sync 与 uv run 会自动创建并更新。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "explicitly updated using uv lock." | type: official
- [C6] D2：uv.lock 为 universal resolution，且跨平台。同页写由 uv lock、uv sync、uv add 修改。 | src: https://docs.astral.sh/uv/concepts/resolution/ | quote: "universal resolution and is portable across platforms." | type: official
- [C7] D2：项目接口仍用 uv.lock，因部分功能无法写入 pylock.toml。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv will continue to use the uv.lock format within the project interface." | type: official
- [C8] D2 写：uv export -o pylock.toml。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "To export a uv.lock to the pylock.toml format, run: uv export -o pylock.toml" | type: official
- [C9] D2 写：uv export --format pylock.toml；落盘 flag 为 --output-file。导出页 November 20, 2025。 | src: https://docs.astral.sh/uv/concepts/projects/export/ | quote: "uv export --format pylock.toml" | type: official
- [C10] D2 写：uv pip compile requirements.in -o pylock.toml。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv pip compile requirements.in -o pylock.toml" | type: official
- [C11] D2 读：uv pip sync pylock.toml 或 uv pip install -r pylock.toml。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv pip sync pylock.toml or uv pip install -r pylock.toml" | type: official
- [C12] D2：自 0.6.15 起称 preliminary support（PEP 751）。发布页只印 22 Apr，无年份。 | src: https://github.com/astral-sh/uv/releases/tag/0.6.15 | quote: "This release includes preliminary support for the pylock.toml file format" | type: official
- [C13] D3：表 [tool.uv.workspace]；members 必填，exclude 可选，值为 glob。同页写 workspace 共用一个锁。 | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "you must specify the members (required) and exclude (optional) keys" | type: official
- [C14] D3：成员依赖在 [tool.uv.sources]，字段 workspace = true。 | src: https://docs.astral.sh/uv/concepts/projects/workspaces/ | quote: "The workspace = true key-value pair in the tool.uv.sources table" | type: official
- [C15] D4：uv python pin 写 .python-version；uv python pin --global 写用户配置。同页示例 uv python install 3.12.3，默认可自动下载。 | src: https://docs.astral.sh/uv/concepts/python-versions/ | quote: "A .python-version file can be created in the current directory with the uv python pin command." | type: official
- [C16] D4：约束字段是 project.requires-python。 | src: https://docs.astral.sh/uv/concepts/projects/config/ | quote: "in the project.requires-python field of the pyproject.toml." | type: official
- [C17] D5：v0.12 前应用默认无 build system。init 模板 build-backend 为 uv_build，requires 为 uv_build>=0.12.18,<0.13。 | src: https://docs.astral.sh/uv/concepts/projects/init/ | quote: "Prior to v0.12, uv did not define a build system for applications by default." | type: official
- [C18] D5：--build-backend 可选 hatchling、uv_build、flit-core、pdm-backend、setuptools、maturin、scikit-build-core。 | src: https://docs.astral.sh/uv/concepts/projects/init/ | quote: "--build-backend with hatchling, uv_build, flit-core, pdm-backend, setuptools, maturin, or scikit-build-core." | type: official
- [C19] D6：默认路径 .venv；环境变量 UV_PROJECT_ENVIRONMENT 可改。 | src: https://docs.astral.sh/uv/concepts/projects/config/ | quote: "configure the project virtual environment path (.venv by default)." | type: official
- [C21] D7：表名 [dependency-groups]（PEP 735）。uv add --dev 建 dev；uv add --group 建具名组。 | src: https://docs.astral.sh/uv/concepts/projects/dependencies/ | quote: "uv uses the [dependency-groups] table (as defined in PEP 735)" | type: official
- [C22] D7：dev 默认 sync。flag：--group、--only-group、--no-group、--all-groups、--no-default-groups、--dev、--only-dev、--no-dev。 | src: https://docs.astral.sh/uv/concepts/projects/sync/ | quote: "The dev group is special-cased and synced by default." | type: official
- [C23] D8：私有 index 表 [[tool.uv.index]]；另有环境变量 UV_INDEX。 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "including private indexes, via the [[tool.uv.index]] configuration option" | type: official
- [C24] D8：凭证是 UV_INDEX_<NAME>_USERNAME 与 UV_INDEX_<NAME>_PASSWORD；NAME 大写，非字母数字改下划线。示例 UV_INDEX_INTERNAL_PROXY_USERNAME / PASSWORD。 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "UV_INDEX_INTERNAL_PROXY_USERNAME and UV_INDEX_INTERNAL_PROXY_PASSWORD" | type: official
- [C25] D9：缓存由 --cache-dir、UV_CACHE_DIR 或 tool.uv.cache-dir 指定；否则 Unix $XDG_CACHE_HOME/uv 或 $HOME/.cache/uv，Windows %LOCALAPPDATA%\uv\cache。 | src: https://docs.astral.sh/uv/concepts/cache/ | quote: "via --cache-dir, UV_CACHE_DIR, or tool.uv.cache-dir." | type: official
- [C26] D9：GitHub 用 astral-sh/setup-uv 的 enable-cache: true；同页示例有 UV_CACHE_DIR 与 uv cache prune --ci。 | src: https://docs.astral.sh/uv/guides/integration/github/ | quote: "enable-cache: true" | type: official
- [C27] D10：入口是 Migration guides，只列 pip 到 uv 项目。其他项目管理工具（含 Poetry）的指南 not yet available，issue 5200。 | src: https://docs.astral.sh/uv/guides/migration/ | quote: "migrating from another project management tool" | type: official
- [C28] D10：pip 迁入命令 uv add -r requirements.in -c requirements.txt（先 uv init）。开发组用 uv add --dev -r。 | src: https://docs.astral.sh/uv/guides/migration/pip-to-project/ | quote: "uv add -r requirements.in -c requirements.txt" | type: official

## conflicts
- 写 pylock 的参数顺序：layout 为 "uv pip compile requirements.in -o pylock.toml"（https://docs.astral.sh/uv/concepts/projects/layout/，July 21, 2026）；0.6.15 为 "uv pip compile -o pylock.toml requirements.in"（https://github.com/astral-sh/uv/releases/tag/0.6.15）。未裁决。
- 同一 layout 页既写 "in the future, pylock.toml files generated by uv could be installed by other tools, and vice versa."，又写当前就能 "uv pip sync pylock.toml or uv pip install -r pylock.toml"。

## gaps
- 无 Poetry 步骤。查过 https://docs.astral.sh/uv/guides/migration/ 与 https://docs.astral.sh/uv/guides/migration/pip-to-project/ 。
- 未见 uv lock/uv sync/uv run 把 pylock.toml 当项目锁读；读只出现在 uv pip。
- 未打开 CLI reference，未核对 --build-backend 短枚举是否另有 poetry/hatch。
- 0.6.15 页只显示 22 Apr，无年份。

## leads
- centralized-project-envs 预览把环境放进缓存并留 .venv 链接；uv.lock 有 version/revision；uv_build 只支持纯 Python；旧 tool.uv.dev-dependencies 仍并入 dev 组。
