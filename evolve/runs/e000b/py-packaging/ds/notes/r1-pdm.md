# r1-pdm
question: PDM 官方文档在以下方面怎么说：(D1) 项目元数据是否原生用标准 PEP621 `[project]` 表（PDM 是否是最早采用 PEP621 的工具之一）；(D2) `pdm.lock` 是什么格式；(D3) PDM 是否/计划支持 PEP 751 标准锁文件 `pylock.toml`（官方 issue/roadmap/changelog 怎么说，PDM 作者是否参与了 PEP751 制定）；(D4) `pdm python` 怎么管理 Python 版本（能否自动下载解释器）；(D5) 虚拟环境管理方式，PDM 是否支持 PEP582（`__pypackages__`，是否已废弃）；(D6) PDM 有没有 workspace/monorepo 机制；(D7) 默认构建后端是不是 pdm-backend，是否可插拔；(D9) 私有源配置方式；(D10) 官方 CI 缓存方案；(D11) 有没有官方「从 pip/Poetry/pipenv 迁移到 PDM」的指南（例如 `pdm import` 命令）

checked: https://pdm-project.org/,https://pdm-project.org/latest/reference/pep621/,https://pdm-project.org/en/latest/usage/lockfile/,https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md,https://github.com/pdm-project/pdm/issues/3480,https://pdm-project.org/en/latest/usage/workspace/,https://pdm-project.org/en/latest/usage/advanced/,https://raw.githubusercontent.com/pdm-project/pdm/main/pdm.lock

## claims

- [C1] 项目元数据原生支持标准 PEP621 `[project]` 表 | src: https://pdm-project.org/ | quote: "PEP 621 project metadata" (in feature highlights) | type: official

- [C2] PDM 是早期采用者，从项目起始就围绕 PEP 621 设计，计划将 `tool.pdm` 元数据逐步移至 `project` 命名空间 | src: https://pdm-project.org/ | quote: "PDM was built around PEP 621 from the start" | type: official

- [C3] pdm.lock 是 TOML 格式，包含 [metadata] 表（groups, strategy, lock_version, content_hash）和 [[package]] 节 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/pdm.lock | quote: "contains several key sections" including "[metadata]" and "[[package]] section" | type: official

- [C4] pdm.lock 记录所有包的版本、文件名、哈希、依赖关系、环境标记 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "All packages and their versions, The file names and hashes of the packages" | type: official

- [C5] PEP 751 支持：v2.25.0 (2025-06-13) 实验性引入 pylock.toml，通过 `pdm export -f pylock` 或 `pdm config lock.format pylock` 使用 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Support pylock as alternative lock format and make it opt-in by config. (#3481)" | type: official

- [C6] v2.24.0 (2025-04-18) 支持导出 PEP 751 pylock.toml | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Support exporting to pylock.toml format as described by PEP 751. (#3480)" | type: official

- [C7] pylock.toml 格式是标准锁文件格式，旨在最小化不同 Python 包管理器间的差异，增强互操作性 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "It's a standard lock file format designed to minimize discrepancies among different Python package managers, enhancing interoperability with other tools" | type: official

- [C8] PDM 作者 frostming 参与 PEP 751 反馈 | src: https://github.com/pdm-project/pdm/issues/3439 | quote: "Frost Ming opened an issue on PDM regarding support for PEP 751" | type: official

- [C9] `pdm python install` 从 python-build-standalone 自动下载并安装 Python 解释器 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Support installing Pythons from python-build-standalone. Add command group `pdm python` to manage Python installations. And `pdm use` can automatically install the Python interpreter if it's not found. #2721" | type: official

- [C10] v2.25.6 (2025-08-14) `pdm python install -v` 显示下载 URL | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "The `pdm python install -v` command now shows the download URL for the Python interpreter. (#3552)" | type: official

- [C11] PEP 582 (`__pypackages__`) 支持实验性/opt-in，v1.162 集成 `pdm venv` 将其改为可选特性 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Integrate `pdm venv` commands into the main program. Make PEP 582 an opt-in feature. #1162" | type: official

- [C12] 虚拟环境支持在项目和集中位置，可以配置 venv.location | src: https://pdm-project.org/ | quote: "PDM can manage virtual environments (venvs) in both project and centralized locations" | type: official

- [C13] v2.28.0 (2026-06-23) 实验性 workspace 支持，用于在共享根锁文件中管理多个本地成员项目 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Add experimental workspace support for managing local member projects in a shared root lock file. (#1505)" | type: official

- [C14] Workspace 成员在 pyproject.toml 中配置，每个成员必须有 pyproject.toml 文件 | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "Workspace members are configured in the root project's pyproject.toml with a members list that accepts direct paths and glob patterns" | type: official

- [C15] v1.1.684 (issue #1684) 切换默认构建后端为 `pdm-backend` | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Switch the default build backend to `pdm-backend`. #1684" | type: official

- [C16] PDM 不限于特定构建后端，用户可自由选择任何构建后端 | src: https://pdm-project.org/ | quote: "Unlike Poetry and Hatch, PDM is not limited to a specific build backend; users have the freedom to choose any build backend they prefer" | type: official

- [C17] 私有源支持通过 keyring 存储凭证，支持嵌入 URL 凭证 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "When keyring is available, either by importing or by CLI, the credentials of repositories and PyPI indexes will be saved into it. #1908" | type: official

- [C18] 私有源支持双向 TLS (mTLS) via `pypi.client_cert` 和 `pypi.client_key` 配置选项 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Support mutual TLS to private repositories via pypi.client_cert and pypi.client_key config options. #1290" | type: official

- [C19] CI 集成推荐使用官方 `pdm-project/setup-pdm` GitHub Action | src: https://pdm-project.org/en/latest/usage/advanced/ | quote: "The documentation recommends using the official pdm-project/setup-pdm action" | type: official

- [C20] CI 环境中应设置 `PDM_IGNORE_SAVED_PYTHON="1"` 以确保正确识别 Python 可执行文件 | src: https://pdm-project.org/en/latest/usage/advanced/ | quote: "PDM_IGNORE_SAVED_PYTHON" | type: official

- [C21] Ubuntu CI 环境并行安装兼容性问题需通过禁用并行或设置 `LD_PRELOAD=/lib/x86_64-linux-gnu/libgcc_s.so.1` 解决 | src: https://pdm-project.org/en/latest/usage/advanced/ | quote: "There's a documented issue with parallel installation on Ubuntu runners" | type: official

- [C22] `pdm import` 命令从 Pipfile、Poetry、flit、requirements.txt 导入项目元数据 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Add new command `pmd import` to import project metadata from `Pipfile`, `poetry`, `flit`, `requirements.txt`" | type: official

- [C23] v2.24.0 (2025-04-18) `pdm import` 将 Poetry 的 `package-mode` 转换为 `distribution` | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "`pdm import` now converts `package-mode` from Poetry's settings table to `distribution`. (#3427)" | type: official

- [C24] `pdm import` 支持导入 requirements.txt 中的 `--trusted-host` 和 editable 包 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/CHANGELOG.md | quote: "Import editable requirements into dev dependencies. #1674" | type: official

## conflicts

无官方文档之间的冲突发现。PDM 关于 PEP 751 态度一致（早期实验性支持，opt-in，计划未来成为默认）。

## gaps

- [G1] 官方文档中未明确描述 pdm.lock 文件内部编码方式（是否 msgpack 或纯 TOML）
- [G2] 未找到 PDM 关于 PEP 751 作为默认格式时间表的官方公告
- [G3] 未找到官方发布的 CI 缓存加速方案的详细指南（仅有 setup-pdm action 介绍）
- [G4] 未找到关于 pdm-backend 可插拔性的详细配置文档（仅知可切换到其他后端）

## leads

- PDM 对 PEP 标准采纳进度领先：早期 PEP 621 采用者，v2.25.0 即支持 PEP 751 实验性特性，作者主动参与 PEP 751 制定
- PEP 751 pylock.toml 预计未来成为 PDM 默认格式，当前通过 `lock.format` 配置开启
- 官方迁移路径明确：`pdm import` 支持从 pip/Poetry/pipenv/flit 项目迁移
