# r2-ci-cache
question: uv、pip、Poetry、PDM、conda、pixi 在 CI（尤其 GitHub Actions）里，官方文档/官方 action 推荐缓存什么路径/文件来加速依赖安装？
checked: https://github.com/astral-sh/setup-uv, https://github.com/actions/setup-python, https://github.com/pdm-project/setup-pdm, https://github.com/conda-incubator/setup-miniconda, https://github.com/prefix-dev/setup-pixi, https://docs.astral.sh/uv/guides/integration/github/, https://docs.astral.sh/uv/concepts/cache/

## claims
- [C1] uv 官方 action `astral-sh/setup-uv` 有内置缓存选项 `enable-cache`，值为 true/false/auto（GitHub 托管 runner 默认启用，自托管 runner 禁用） | src: https://github.com/astral-sh/setup-uv | quote: "Enable the GitHub Actions cache for uv: true, false, or auto (enabled on GitHub-hosted runners except for release, tag push, pull_request_target, and workflow_run events; disabled on self-hosted runners)" | type: official
- [C2] uv 缓存基于依赖文件的哈希值（uv.lock 或 requirements.txt），cache key 示例为 `key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}` | src: https://docs.astral.sh/uv/guides/integration/github/ | quote: "key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}" | type: official
- [C3] uv 官方建议在 CI 最后运行 `uv cache prune --ci` 来最小化缓存大小 | src: https://docs.astral.sh/uv/guides/integration/github/ | quote: "uv cache prune --ci removes all pre-built wheels and unzipped source distributions from the cache, but retains any wheels that were built from source" | type: official
- [C4] uv 缓存存储目录为：Unix 上 `$XDG_CACHE_HOME/uv` 或 `$HOME/.cache/uv`，Windows 上 `%LOCALAPPDATA%\uv\cache` | src: https://docs.astral.sh/uv/concepts/cache/ | quote: "$XDG_CACHE_HOME/uv or $HOME/.cache/uv on Unix, %LOCALAPPDATA%\uv\cache on Windows" | type: official
- [C5] pip 官方 action `actions/setup-python` 支持 `cache: 'pip'` 参数来启用内置缓存 | src: https://github.com/actions/setup-python | quote: "cache: 'pip' # caching pip dependencies" | type: official
- [C6] `cache: 'pip'` 缓存 pip 的全局 cache 目录 | src: https://github.com/actions/setup-python | quote: "For pip, the action will cache the global cache directory" | type: official
- [C7] pip 缓存基于 requirements.txt 或 pyproject.toml 的哈希值作为缓存 key | src: https://github.com/actions/setup-python | quote: "The action searches for dependency files automatically: For pip: requirements.txt or pyproject.toml" | type: official
- [C8] Poetry 官方 action `actions/setup-python` 支持 `cache: 'poetry'` 参数来启用内置缓存 | src: https://github.com/actions/setup-python | quote: "cache: 'poetry'" | type: official
- [C9] `cache: 'poetry'` 缓存的是 virtualenv 目录（为每个找到的 Poetry 项目各缓存一个） | src: https://github.com/actions/setup-python | quote: "For poetry, the action will cache virtualenv directories -- one for each poetry project found" | type: official
- [C10] Poetry 缓存基于 poetry.lock 文件的哈希值作为缓存 key | src: https://github.com/actions/setup-python | quote: "For poetry: poetry.lock" | type: official
- [C11] PDM 官方 action `pdm-project/setup-pdm` 支持 `cache: true` 参数来启用内置缓存 | src: https://github.com/pdm-project/setup-pdm | quote: "cache: true" | type: official
- [C12] PDM 缓存默认使用 `./pdm.lock` 文件来计算缓存 key | src: https://github.com/pdm-project/setup-pdm | quote: "The default path to calculate the cache key is ./pdm.lock" | type: official
- [C13] PDM 缓存支持通过 `cache-dependency-path` 指定自定义路径或 glob 模式（如 `**/pdm.lock`）| src: https://github.com/pdm-project/setup-pdm | quote: "You can specify a list by using line breaks to separate entries across multiple lock files" and "Glob patterns such as **/pdm.lock to match files across directories" | type: official
- [C14] conda 官方 action `conda-incubator/setup-miniconda` 推荐缓存路径为 `~/conda_pkgs_dir`（conda 包缓存目录） | src: https://github.com/conda-incubator/setup-miniconda | quote: "If you want to enable package caching for conda you can use the cache action using ~/conda_pkgs_dir as path for conda packages" | type: official
- [C15] conda 缓存必须设置 `use-only-tar-bz2: true` 才能正常工作 | src: https://github.com/conda-incubator/setup-miniconda | quote: "use-only-tar-bz2: true # IMPORTANT: This needs to be set for caching to work properly!" | type: official
- [C16] conda 也可以缓存整个环境目录 `${{ env.CONDA }}/envs` | src: https://github.com/conda-incubator/setup-miniconda | quote: "path: ${{ env.CONDA }}/envs" | type: official
- [C17] conda Windows runner 在 `D:` drive 上解压缓存会更快 | src: https://github.com/conda-incubator/setup-miniconda | quote: "GitHub hosted Windows runners are currently faster during cache decompression when configuring the package directories on the D: drive" | type: official
- [C18] pixi 官方 action `prefix-dev/setup-pixi` 如果存在 `pixi.lock` 文件则默认启用项目环境缓存 | src: https://github.com/prefix-dev/setup-pixi | quote: "The action supports caching of the project and global pixi environments. By default, project environment caching is enabled if a pixi.lock file is present" | type: official
- [C19] pixi 缓存基于 pixi.lock 文件的哈希值来跳过重装 | src: https://github.com/prefix-dev/setup-pixi | quote: "The system generates a hash from the lock file and stores the cached environment to skip reinstallation on subsequent runs" | type: official
- [C20] pixi 全局环境缓存默认禁用，可通过 `global-cache: true` 启用 | src: https://github.com/prefix-dev/setup-pixi | quote: "Global environment caching is disabled by default but can be activated by setting global-cache: true" | type: official
- [C21] pixi 全局缓存因为缺乏 lockfile，月末会过期以防止过期 | src: https://github.com/prefix-dev/setup-pixi | quote: "the cache will expire at the end of every month to ensure it does not go stale" | type: official
- [C22] pixi 缓存可通过 `cache-key` 和 `global-cache-key` 自定义，cache key 格式为 `<cache-key><conda-arch>-<hash>` 和 `<global-cache-key><conda-arch>-<YYYY-MM>-<hash>` | src: https://github.com/prefix-dev/setup-pixi | quote: "cache-key><conda-arch>-<hash>" and "<global-cache-key><conda-arch>-<YYYY-MM>-<hash>" | type: official
- [C23] pixi 支持 `cache-write` 参数来限制缓存保存条件（如只在 main 分支 push 时保存），以避免超过 GitHub 10GB 缓存限制 | src: https://github.com/prefix-dev/setup-pixi | quote: "To avoid exceeding GitHub's 10 GB cache limit, you can restrict saving to specific conditions (like pushes to main branch) using the cache-write parameter" | type: official
- [C24] uv 缓存包括注册表依赖、直接 URL 依赖、Git 依赖、本地依赖、扁平索引文件、从源构建的 wheels 和下载的 pre-built wheels | src: https://docs.astral.sh/uv/concepts/cache/ | quote: "Registry dependencies, Direct URL dependencies, cached by URL and HTTP headers, Git dependencies, cached by fully-resolved commit hash, Local dependencies, cached by file modification times, Flat index files, cached by filename" | type: official
- [C25] uv 可通过环境变量 `UV_CACHE_DIR` 手动指定缓存目录 | src: https://docs.astral.sh/uv/guides/integration/github/ | quote: "Alternatively, you can manage the cache manually using the actions/cache action by setting a constant location for the uv cache directory using the UV_CACHE_DIR environment variable" | type: official

## conflicts
None identified.

## gaps
- 缺少官方 pip 文档中是否有专门的 CI 缓存建议页（仅从 setup-python action README 中找到了缓存支持）
- 缺少确认是否存在名称为 "poetry-plugin-cache" 的官方 Poetry 插件（WebSearch 未找到该名称的插件）
- 未找到 PDM 官网本身的 GitHub Actions 集成文档，仅从 setup-pdm action README 获取信息
- 缺少确认 Poetry 官方文档中是否有专门的 CI 缓存集成章节

## leads
- Poetry 官方文档中未找到专门的 CI/GitHub Actions 集成指南，仅 setup-python action README 提供缓存支持
- 没有名为 "poetry-plugin-cache" 的官方插件，但存在 poetry-plugin-export-packages 等相关缓存优化插件
