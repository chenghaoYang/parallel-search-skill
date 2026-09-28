# r1-scout
question: Python 包管理选型坑：迁移坑（Poetry 1.x→2.x、requirements.txt→uv/PDM、pipenv 状态、rye→uv）、CI 缓存坑、私有源/依赖混淆坑、漏网实体一句话定位
checked: https://python-poetry.org/blog/announcing-poetry-2.0.0/, https://python-poetry.org/docs/repositories/, https://docs.astral.sh/uv/concepts/indexes/, https://docs.astral.sh/uv/guides/integration/github/, https://docs.astral.sh/uv/concepts/cache/, https://docs.astral.sh/uv/guides/migration/pip-to-project/, https://github.com/astral-sh/rye, https://github.com/astral-sh/setup-uv, https://github.com/pypa/pipenv, https://pypi.org/project/pipenv/, https://hatch.pypa.io/latest/, https://github.com/pyenv/pyenv, https://pipx.pypa.io/stable/, https://github.com/python-poetry/poetry-plugin-export, https://github.com/conda-forge/miniforge, https://mamba.readthedocs.io/en/latest/, https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows, https://pdm-project.org/latest/, https://pdm-project.org/latest/reference/cli/, https://github.com/pdm-project/setup-pdm, https://github.com/prefix-dev/setup-pixi

## claims
- [C1] Poetry 2.0（2025-01-05 发布）删除 `poetry shell`，推荐 `poetry env activate`；旧命令可装 poetry-plugin-shell | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "we seized the chance of a major release to remove the `poetry shell` command" | type: official
- [C2] `poetry export` 移出核心，poetry-plugin-export 不再随默认安装 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "`poetry export` is not a core feature of Poetry but is provided by `poetry-plugin-export`" | type: official
- [C3] `poetry lock` 默认变为 `--no-update`，旧行为改用 `--regenerate` | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "`poetry lock` now defaults to `--no-update` to prevent accidental updates of the lock file" | type: official
- [C4] `poetry install --sync` 废弃，改用 `poetry sync`；`installer.modern-installation=false`（pip 安装器）被移除 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Deprecate `poetry install --sync` in favor of `poetry sync`" | type: official
- [C5] `-C/--directory` 语义变了：真正切换目录；旧语义移到 `--project`/`-P` | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "The `--directory`/`-C` option now actually switches the directory instead of just setting the directory as project root" | type: official
- [C6] `virtualenvs.prefer-active-python` 被反向选项 `virtualenvs.use-poetry-python` 取代，Poetry 2.0 默认优先当前激活的 Python；配置可用 `poetry config --migrate` 迁移 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Replace `virtualenvs.prefer-active-python` by the inverse setting `virtualenvs.use-poetry-python`" | type: official
- [C7] Poetry 2.0 不再支持 Python 3.8，且读不了 Poetry <1.1 生成的 lock 文件 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "Drop support for reading lock files prior version 1.0 (created with Poetry prior 1.1)" | type: official
- [C8] `tool.poetry` 大量字段废弃改用 PEP 621 `project` 段（`tool.poetry.dependencies` 除外），`poetry check` 可列出 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "many fields in the `tool.poetry` section are deprecated in favor of their counterparts in the `project` section" | type: official
- [C9] poetry-plugin-export 提供 `export` 命令导出 requirements.txt/constraints.txt/pylock.toml；Poetry 2.0+ 可在 `[tool.poetry.requires-plugins]` 声明 | src: https://github.com/python-poetry/poetry-plugin-export | quote: "This package is a plugin that allows the export of locked packages to various formats" | type: official
- [C10] rye 仓库 2026-02-05 归档只读，"Rye is no longer developed"，无安全更新，官方指向 uv 为继任 | src: https://github.com/astral-sh/rye | quote: "While Rye will continue to be available, no further updates are planned, including security updates" | type: official
- [C11] requirements.txt→uv：`uv add -r requirements.in`；保留已锁定版本要加 `-c requirements.txt`，否则重新解析新版本 | src: https://docs.astral.sh/uv/guides/migration/pip-to-project/ | quote: "uv supports using these on `add` to preserve locked versions" | type: official
- [C12] 平台专属 requirements.txt 不能直接当 constraints（缺 markers 会冲突），需先 `uv pip compile --python-platform windows --no-strip-markers` 重新生成 | src: https://docs.astral.sh/uv/guides/migration/pip-to-project/ | quote: "you cannot just use `-c` to specify constraints from your existing platform-specific `requirements.txt` files" | type: official
- [C13] uv 不以"激活的 venv"为中心，每项目用 `.venv`；`uv run` 保证在锁定环境执行 | src: https://docs.astral.sh/uv/guides/migration/pip-to-project/ | quote: "Unlike `pip`, uv is not centered around the concept of an "active" virtual environment" | type: official
- [C14] `pdm import` 可从其他格式导入项目元数据：`pdm import [OPTIONS] filename`，支持 `-f/--format`、`-d`（dev）、`-G`（group） | src: https://pdm-project.org/latest/reference/cli/ | quote: "Import project metadata from other formats" | type: official
- [C15] pipenv 仍在维护：PyPI 最新 2026.8.0（2026-08-20），定位 "Python Development Workflow for Humans"；无任何废弃/迁移提示 | src: https://pypi.org/project/pipenv/ | quote: "Python Development Workflow for Humans." | type: official
- [C16] setup-uv `enable-cache` 默认 `auto`：GitHub-hosted runner 上默认开（release/tag push/pull_request_target/workflow_run 除外），self-hosted 默认关 | src: https://github.com/astral-sh/setup-uv | quote: "enabled on GitHub-hosted runners except for release, tag push" | type: official
- [C17] setup-uv `cache-dependency-glob` 默认含 `**/uv.lock`、`**/pyproject.toml`、`**/*requirements*.txt` 等 | src: https://github.com/astral-sh/setup-uv | quote: "Glob pattern to match files relative to the repository root to control the cache" | type: official
- [C18] 手动缓存 uv：`UV_CACHE_DIR: /tmp/.uv-cache`，key `uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}`，末尾 `uv cache prune --ci` | src: https://docs.astral.sh/uv/guides/integration/github/ | quote: "The `uv cache prune --ci` command is used to reduce the size of the cache and is optimized for CI" | type: official
- [C19] 用 `uv pip` 工作流时缓存 key 应改用 requirements.txt 而非 uv.lock | src: https://docs.astral.sh/uv/guides/integration/github/ | quote: "If using `uv pip`, use `requirements.txt` instead of `uv.lock` in the cache key" | type: official
- [C20] uv cache 默认在 `$XDG_CACHE_HOME/uv` 或 `$HOME/.cache/uv`（Windows `%LOCALAPPDATA%\uv\cache`）；内部分 wheels/sdists/git 桶且各自版本化 | src: https://docs.astral.sh/uv/concepts/cache/ | quote: "a bucket for wheels, a bucket for source distributions, a bucket for Git repositories" | type: official
- [C21] `uv cache prune --ci` 删除预构建 wheels 和解压的 sdist，保留源码构建的 wheel，官方建议 CI job 末尾运行 | src: https://docs.astral.sh/uv/concepts/cache/ | quote: "We recommend running uv cache prune --ci at the end of your continuous integration job" | type: official
- [C22] flat index 下同文件名替换的文件在缓存刷新前不会被拾取；需 `--refresh` 或 `--refresh-package` | src: https://docs.astral.sh/uv/concepts/cache/ | quote: "will not be picked up until the cache is refreshed" | type: official
- [C23] setup-pdm 内置缓存（`cache: true`），`cache-dependency-path` 默认 `./pdm.lock`；官方称 setup-python 开箱不支持 PDM 缓存 | src: https://github.com/pdm-project/setup-pdm | quote: "doesn't support caching for PDM out of the box while `setup-pdm` does" | type: official
- [C24] setup-pixi 检测到 `pixi.lock` 时默认开启项目环境缓存，用 lock 文件算 hash；`cache-write` 可限只在 main 保存以控制 10GB 上限 | src: https://github.com/prefix-dev/setup-pixi | quote: "By default, project environment caching is enabled if a `pixi.lock` file is present" | type: official
- [C25] GitHub 官方缓存文档无 Python/poetry.lock 示例，只指向 setup-python（pip/pipenv/Poetry）自动缓存；lock 文件 hash 模式仅给出 npm 例 | src: https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows | quote: "will create and restore dependency caches for you" | type: official
- [C26] uv `[[tool.uv.index]]` 的 `explicit = true`：该 index 上的包只有在 `tool.uv.sources` 显式 pin 时才从该 index 安装 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "to prevent packages from being installed from that index unless explicitly pinned to it" | type: official
- [C27] uv 默认 first-index 策略：包在首个含它的 index 上定案；`unsafe-best-match` 合并所有 index 候选但会引入依赖混淆风险 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "By default, uv will stop at the first index on which a given package is available" | type: official
- [C28] uv：内部 index 上存在的包永远从内部 index 装、绝不回 PyPI——专门防 dependency confusion（官方引用 2022-12 torchtriton 事件） | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "if a package exists on that internal index, it will _always_ be installed from that internal index, and never from PyPI" | type: official
- [C29] Poetry `priority = "explicit"` 的源只服务显式指定来源的包；官方强烈建议 source constraint 防 dependency confusion | src: https://python-poetry.org/docs/repositories/ | quote: "Explicit sources are considered only for packages that explicitly indicate their source" | type: official
- [C30] Poetry：配置 ≥1 个 primary 源后隐式 PyPI 自动禁用；supplemental 仅在更高优先级源无可用发行时搜索 | src: https://python-poetry.org/docs/repositories/ | quote: "The implicit PyPI source is disabled automatically if at least one primary source is configured" | type: official
- [C31] Hatch："a modern, extensible Python project manager"，含 build backend、环境管理、版本管理、发布 | src: https://hatch.pypa.io/latest/ | quote: "Hatch is a modern, extensible Python project manager" | type: official
- [C32] pyenv："Simple Python version management"，用 shim 切换解释器版本，明确不管 virtualenv（需 pyenv-virtualenv 插件） | src: https://github.com/pyenv/pyenv | quote: "pyenv lets you easily switch between multiple versions of Python" | type: official
- [C33] pipx：在隔离环境中安装运行 end-user Python 应用 | src: https://pipx.pypa.io/stable/ | quote: "pipx installs and runs end-user Python applications in isolated environments" | type: official
- [C34] miniforge：conda-forge 专用的最小 conda+mamba 安装器，conda-forge 为默认且唯一 channel | src: https://github.com/conda-forge/miniforge | quote: "The conda-forge channel is set as the default (and only) channel" | type: official
- [C35] mamba：快速跨平台包管理器，conda 的 drop-in 替代品，基于 libmamba C++ 库 | src: https://mamba.readthedocs.io/en/latest/ | quote: "a *drop-in* replacement for `conda`" | type: official
- [C36] PDM："a modern Python package and dependency manager supporting the latest PEP standards"，带 pnpm 式可选集中安装缓存 | src: https://pdm-project.org/latest/ | quote: "Opt-in centralized installation cache like pnpm" | type: official

## conflicts
- 未发现实质冲突。注意点：Poetry 官方仓库文档当前只认 primary/supplemental/explicit 三种 priority（后两者标注 1.5.0 引入），旧教程里的 `secondary`/`default` 优先级写法已不在官方文档中，容易误导。

## gaps
- pip `--extra-index-url` 的 dependency confusion 风险无官方 pip 文档原句（只有 uv/Poetry 侧官方表述）。
- requirements.txt→PDM 迁移的具体坑未查到（仅确认 `pdm import` 存在，CLI 参考页未列出支持格式清单）。
- Poetry/PDM/pixi 在 GitHub Actions 手动 actions/cache 的官方推荐 key 形态未查（GitHub 文档无 Python 例）。
- pipenv 无官方"不推荐/废弃"声明；PyPA 是否另有定位建议未查。

## leads
- Poetry 2.0 迁移抓手：`poetry config --migrate`、`poetry check` 列废弃字段、`[tool.poetry.requires-plugins]` 声明插件。
- uv 私有源认证细节：401/403 停止跨 index 搜索（pytorch index 例外）；credentials 不写入 uv.lock。
- 实体补充：pyenv-virtualenv 插件；PDM PEP 582 无 venv 模式（setup-pdm `enable-pep582`）；setup-uv 文档示例 pin 到 uv 0.12.19 / action v9.0.0。
- dependency confusion 有名案例：2022-12 torchtriton（uv 官方文档引用）。
