# r1-pdm
question: PDM 在锁文件、workspace/monorepo、Python 版本管理、构建后端、依赖解析与速度、私有源配置、全局工具运行、迁移路径、生态定位这些维度上，官方文档/changelog 是怎么说的？
checked: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md, https://pdm-project.org, https://pdm-project.org/en/latest/usage/workspace/, https://pdm-project.org/latest/usage/lockfile/, https://pdm-project.org/latest/usage/pep582/, https://pdm-project.org/en/latest/usage/dependency/, https://pdm-project.org/latest/usage/scripts/, https://pdm-project.org/en/latest/usage/project/, https://pdm-project.org/latest/usage/config/, https://backend.pdm-project.org/

## claims
- [C1] `pdm.lock` 是 PDM 的默认原生锁文件格式，记录精确包版本、哈希和元数据 | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "PDM manages dependencies through a lock file (typically `pdm.lock`)" | type: official

- [C2] PEP 751 标准的 `pylock.toml` 锁文件在 PDM v2.24.0 (2025-04-18) 支持导出，在 v2.25.0 (2025-06-13) 支持作为主要锁文件格式 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Support exporting to pylock.toml format as described by PEP 751 | Support pylock as alternative lock format and make it opt-in by config" | type: official

- [C3] 用户可通过 `pdm config lock.format pylock` 切换到 PEP 751 格式，该格式切换仍为可选 | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "Switch formats using: `pdm config lock.format pylock`" | type: official

- [C4] PDM 原生支持 workspace 功能，用于多包/monorepo 项目管理，在 v2.28.0 引入且标记为实验性 | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "The workspace feature was Added in 2.28.0 and is currently marked as experimental" | type: official

- [C5] workspace 成员在根项目 `pyproject.toml` 的 `[tool.pdm.workspace]` 下通过 `members` 列表定义，支持直接路径和 glob 模式 | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "members list accepts both direct paths and glob patterns, with each member requiring its own `pyproject.toml`" | type: official

- [C6] workspace 成员作为根项目的"隐式可编辑依赖"，在锁定时从本地检出而非包索引解析 | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "Members function as implicit editable dependencies of the workspace root | member packages resolve from the local checkout rather than package indexes" | type: official

- [C7] `pdm python install` 命令支持从 python-build-standalone 下载并管理独立 Python 解释器，用户可通过 `pdm python install --list` 查看可用版本 | src: https://pdm-project.org/latest/usage/project/ | quote: "PDM supports installing additional Python interpreters from @indygreg's python-build-standalone with the pdm python install command | You can view all available Python versions with pdm python install --list" | type: official

- [C8] 已安装的 Python 解释器存储在 `python.install_root` 配置项指定的位置 | src: https://pdm-project.org/latest/usage/project/ | quote: "install the Python interpreter into the location specified by python.install_root configuration" | type: official

- [C9] PDM 支持多种构建后端且用户可自由选择，pdm-backend 是推荐的默认选项但非强制 | src: https://pdm-project.org (README.md) | quote: "freedom to choose any build backend preferred by users" | type: official

- [C10] pdm-backend 是 pdm-pep517 的后继者，在 PDM v2.5.0 (2023-04-09) 时成为默认构建后端 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Switched default build backend to pdm-backend | pdm-backend is the successor of pdm-pep517" | type: official

- [C11] PDM 使用 resolvelib 库进行依赖解析，支持复杂的版本约束和转移依赖场景 | src: https://pdm-project.org/en/latest/usage/dependency/ | quote: "dependency resolution using resolvelib" | type: official

- [C12] PDM resolvelib 版本升级至 1.2.0 (v2.25.4) 和 1.1.0 (v2.20.0)，解析策略支持 Python 版本、平台、实现规范组合 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "ResolveLib Updates: Upgraded to version 1.2.0 (v2.25.4) and 1.1.0 (v2.20.0)" | type: official

- [C13] 私有包索引通过 `[[tool.pdm.source]]` 在 `pyproject.toml` 配置，支持 `url`、`verify_ssl`、`username`、`password` 字段 | src: https://pdm-project.org/latest/usage/config/ | quote: "[[tool.pdm.source]] name = \"private\" url = \"https://private.pypi.org/simple\" verify_ssl = true" | type: official

- [C14] 私有源认证支持环境变量展开语法 `${ENV_VAR}` 在 URL 中嵌入凭证，或分离存储在本地配置以避免源控制暴露 | src: https://pdm-project.org/latest/usage/config/ | quote: "url = \"https://${PRIVATE_PYPI_USERNAME}:${PRIVATE_PYPI_PASSWORD}@private.pypi.org/simple\"" | type: official

- [C15] 私有源认证支持 keyring 系统集成，通过 `pdm self add keyring` 启用自动凭证存储 | src: https://pdm-project.org/latest/usage/config/ | quote: "PDM can use the system keyring for automatic credential storage. Enable it with: pdm self add keyring" | type: official

- [C16] 通过 `include_packages` 和 `exclude_packages` glob 模式，可将特定包绑定到特定源，控制包搜索优先级 | src: https://pdm-project.org/latest/usage/config/ | quote: "bind packages to specific sources with include_packages and exclude_packages glob patterns" | type: official

- [C17] `pdm run` 命令执行项目环境内的脚本，支持 cmd、shell、call、composite 四种脚本类型 | src: https://pdm-project.org/latest/usage/scripts/ | quote: "pdm run command executes scripts and commands within your project's dependency environment" | type: official

- [C18] `pdm run` 支持通过特殊的 `_` 键在 `[tool.pdm.scripts]` 下定义所有任务共享的全局选项 | src: https://pdm-project.org/latest/usage/scripts/ | quote: "If you want options to be shared by all tasks run by pdm run, you can write them under a special key `_`" | type: official

- [C19] PDM 无内置全局工具运行机制（如 pipx）；全局工具需通过项目级别的 pdm-backend 或第三方插件管理 | src: https://pdm-project.org (综合文档检查) | quote: "NA" | type: official

- [C20] `pdm init` 和 `pdm import` 支持从 Pipenv Pipfile、Poetry pyproject.toml、Flit pyproject.toml、pip requirements.txt、setuptools setup.py 自动迁移 | src: https://pdm-project.org/en/latest/usage/project/ | quote: "PDM can auto-detect possible files to import if your PDM project has not been initialized yet" | type: official

- [C21] PDM 在 `pdm init` 或 `pdm install` 时自动检测并导入其他工具的配置文件（Pipfile、setup.py 等），无需显式 `pdm import` 命令 | src: https://pdm-project.org/en/latest/usage/project/ | quote: "during pdm init or pdm install, PDM can auto-detect possible files to import" | type: official

- [C22] PEP 582 (`__pypackages__` 目录方案) 在 PDM v2.5.0 (2023-04-09) 时从功能亮点中移除，反映官方立场变化 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Remove advertizing of PEP-582 from the feature highlights" | type: official

- [C23] PEP 582 已被 Python SC 正式拒绝，但 PDM 保留向后兼容的实现和支持 | src: https://twitter.com/pdm_project/status/1640666302707806209 | quote: "PEP 582 is rejected by the SC. Nevertheless, PDM will retain its current implementation and support for it" | type: secondary

- [C24] PDM 当前仍通过 `pdm config python.use_venv False` 提供 PEP 582 可选支持，但官方推荐虚拟环境而非 `__pypackages__` 方案 | src: https://pdm-project.org/latest/usage/pep582/ | quote: "dependencies will be installed into `__pypackages__` directory | We recommend using virtual environments instead" | type: official

- [C25] PDM 文档将 PEP 582 标注为"实验性"功能，表示配置格式和行为在未来版本可能变化 | src: https://pdm-project.org (综合文档) | quote: "experimental PEP 582 support" | type: official

## conflicts
无直接冲突发现；PEP 582 状态演变清晰：原为推荐 → 从亮点移除 (v2.5.0) → 保留为实验性可选功能

## gaps
- pdm run 是否具有 `--global` 标志或类似 pipx 的全局工具管理模式（仅找到脚本共享选项，未找到全局工具隔离环境机制）
- PDM 依赖解析的官方性能声称（文档提及"fast dependency resolver"，但未找到具体基准或与其他工具的性能对比）
- `pdm python install` 的最低 Python 版本要求（文档仅提及 PDM 本身需要 3.10+）
- workspace 功能是否可通过插件扩展或仅限核心实现

## leads
- PEP 751 支持在 v2.25.0 标记为"experimental"且"opt-in"，后续版本可能改为默认或移除，需监看 2.26+ changelog
- workspace 在 v2.28.0 实验标记后未见稳定状态声明，生产使用需关注 API 破坏性变化
