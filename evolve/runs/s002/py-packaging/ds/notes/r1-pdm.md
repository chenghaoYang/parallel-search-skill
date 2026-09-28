# r1-pdm
question: PDM 官方文档里，锁文件（含是否读写 pylock.toml）、[project] 表、workspace/monorepo、Python 版本、构建后端、依赖来源、从 Poetry/flit/pipenv 迁移、CI 缓存、私有源分别用什么原名？
checked: https://pdm-project.org/en/latest/usage/lockfile/, https://pdm-project.org/en/latest/usage/config/, https://pdm-project.org/en/latest/usage/dependency/, https://pdm-project.org/en/latest/usage/workspace/, https://pdm-project.org/en/latest/usage/advanced/, https://pdm-project.org/en/latest/usage/project/, https://pdm-project.org/en/latest/usage/venv/, https://pdm-project.org/en/latest/reference/pep621/, https://pdm-project.org/en/latest/reference/build/, https://pdm-project.org/en/latest/reference/configuration/, https://github.com/pdm-project/setup-pdm, https://api.github.com/repos/pdm-project/pdm/releases (tags 2.13.0/2.23.0/2.24.0/2.25.x/2.28.0/2.29.0), https://raw.githubusercontent.com/pdm-project/pdm/main/src/pdm/formats/__init__.py

文档版本：en/latest，页面内提示标注至 2.29.x（如 "Changed in 2.28.1"、"Added in 2.26.9"）。

## claims

### lock（锁文件）
- [C1] 默认锁文件 `pdm.lock`；备选 PEP 751 格式 `pylock.toml`，默认格式仍是 `pdm` | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "PDM supports two lock file formats: `pdm`(default file name is `pdm.lock`) and `pylock`(default file name is `pylock.toml`). The default format is `pdm`." | type: official
- [C2] 写：`pdm lock` 创建/覆盖；`pdm install`、`pdm add` 也会自动生成锁文件 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "the `pdm install` and `pdm add` commands will also automatically create the `pdm.lock` file." | type: official
- [C3] 写 pylock（方式一，原生格式）：`pdm config lock.format pylock` 后 `pdm lock` 产出 `pylock.toml`；config 键 `lock.format`（可用 `pdm`/`pylock`，env `PDM_LOCK_FORMAT`，可 `--local` 项目级） | src: https://pdm-project.org/en/latest/reference/configuration/ | quote: "`lock.format` | The format of the lock file, can be `pdm` or `pylock` | `pdm` | Yes | `PDM_LOCK_FORMAT`" | type: official
- [C4] pylock 原生格式起点 = 2.25.0 | src: https://api.github.com/repos/pdm-project/pdm/releases/tags/2.25.0 | quote: "Support pylock as alternative lock format and make it opt-in by config." | type: official
- [C5] 写 pylock（方式二，导出转换）：`pdm export -f pylock -o pylock.toml`，起点 2.24.0 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "Added in 2.24.0. Additionally, PDM supports exporting to `pylock.toml` format as defined by PEP 751" | type: official
- [C6] 读：把 `lock.format` 设为 `pylock` 后 PDM 以 pylock.toml 为项目锁文件解析；release notes 多处确认解析行为 | src: https://api.github.com/repos/pdm-project/pdm/releases/tags/2.25.3 | quote: "Extract `dependency-groups` and `extras` markers from `marker` value when parsing pylock.toml." | type: official
- [C7] 指定其他锁文件：`-L/--lockfile` 选项或 `PDM_LOCKFILE` env；`--frozen-lockfile` 只禁止写锁文件、不禁止解析 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "You can specify another lock file with the `-L/--lockfile` option or the `PDM_LOCKFILE` environment variable" | type: official
- [C8] 原生 pdm 格式特有元数据字段：`metadata.groups`（锁定的依赖组）、`metadata.strategy`（锁策略）；锁策略 flag：`cross_platform`、`static_urls`、`direct_minimal_versions`、`inherit_metadata` | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "The native `pdm.lock` format records the locked set in `metadata.groups`." | type: official

### meta（[project] 表）
- [C9] 项目元数据按 PEP 621/631/639 写在 `pyproject.toml` 的 `[project]` 表 | src: https://pdm-project.org/en/latest/reference/pep621/ | quote: "metadata should be written under `[project]` table if not given explicitly." | type: official
- [C10] `[project].dependencies` 是 PEP 440/PEP 508 依赖字符串数组；可选依赖在 `[project.optional-dependencies]`；开发依赖在 `[dependency-groups]`（PEP 735） | src: https://pdm-project.org/en/latest/usage/dependency/ | quote: "This will result in a `pyproject.toml` as following: [dependency-groups] test = [\"pytest\"]" | type: official
- [C11] PDM 专属配置放 `[tool.pdm]`：`distribution`（true=按库处理）、动态版本 `version = { source = "file", path = ... }`、`[tool.pdm.resolution]`、`[[tool.pdm.source]]`、`[tool.pdm.workspace]`、`[tool.pdm.options]`、`ignore_package_warnings` | src: https://pdm-project.org/en/latest/usage/project/ | quote: "there is a field `distribution` under the `[tool.pdm]` table. If it is set to true, PDM will treat the project as a library." | type: official

### workspace（monorepo）
- [C12] 原生 workspace：根 `pyproject.toml` 里 `[tool.pdm.workspace]` 的 `members` 键（路径+glob），成员为隐式 editable 依赖、共享根锁文件；实验性，起点 2.28.0 | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "Added in 2.28.0. ... `[tool.pdm.workspace] members = [\"packages/foo\", \"packages/bar\", \"tools/*\"]`" | type: official
- [C13] `pdm install/lock/sync/outdated/info` 必须从 workspace 根运行；`pdm add/remove/update/run/build/publish` 可指向成员；成员间按包名互依 | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "The following commands must be run from the workspace root: - `pdm install` - `pdm lock` - `pdm sync` - `pdm outdated` - `pdm info`" | type: official
- [C14] 2.28.0 之前的手工 monorepo 做法仍在文档：根 `[dependency-groups]` 里放 `-e file:///${PROJECT_ROOT}/packages/<pkg>` editable 条目 | src: https://pdm-project.org/en/latest/usage/advanced/ | quote: "dev = [ \"-e file:///${PROJECT_ROOT}/packages/foo-core\", ...] ... All sub-packages will be installed in editable mode." | type: official

### pyver（Python 版本）
- [C15] 项目支持的 Python 范围：`[project]` 的 `requires-python`（PEP 440 specifier），锁文件按该范围跨平台解析 | src: https://pdm-project.org/en/latest/usage/project/ | quote: "The value of `requires-python` is a version specifier as defined in PEP 440" | type: official
- [C16] 钉解释器：`pdm use` 选择解释器，路径写入项目根 `.pdm-python` 文件；`PDM_PYTHON` env 可覆盖；`.pdm-python` 不应提交 | src: https://pdm-project.org/en/latest/usage/project/ | quote: "The interpreter path will be stored in `.pdm-python` and used by subsequent commands. You can also change it later with `pdm use`." | type: official
- [C17] `pdm python install/list/remove/find` 从 python-build-standalone 安装 CPython（含 `3.13t` 自由线程），装到 `python.install_root`（默认 `~/.local/share/pdm/python`）；`pdm use` 找不到解释器可自动安装 | src: https://api.github.com/repos/pdm-project/pdm/releases/tags/2.13.0 | quote: "Add command group `pdm python` to manage Python installations. And `pdm use` can automatically install the Python interpreter" | type: official
- [C18] `.python-version` 文件或 `PDM_PYTHON_VERSION` env 可指定版本（文档标注 Added in 2.23.0）；开关 `python.use_python_version`/`PDM_USE_PYTHON_VERSION` | src: https://pdm-project.org/en/latest/usage/project/ | quote: "If `.python-version` is present in the project root or `PDM_PYTHON_VERSION` env var is set, PDM will use the Python version specified in it." | type: official
- [C19] 虚拟环境是默认模式（`python.use_venv` 默认 True，默认在项目内 `.venv`，backend 可选 virtualenv/venv/conda）；否则用 PEP 582 `__pypackages__` | src: https://pdm-project.org/en/latest/usage/venv/ | quote: "PDM will create a virtualenv in `<project_root>/.venv` ... supports three backends: `virtualenv`(default), `venv`, `conda`" | type: official

### build（构建后端）
- [C20] 默认/首选后端 `pdm-backend`：`[build-system] requires = ["pdm-backend"]`, `build-backend = "pdm.backend"`；PDM 是 PEP 517 前端，不强制后端 | src: https://pdm-project.org/en/latest/reference/build/ | quote: "[build-system] requires = [\"pdm-backend\"] build-backend = \"pdm.backend\"" | type: official
- [C21] 文档列出的可选后端：setuptools、flit_core、hatchling、maturin；poetry-core 不支持 | src: https://pdm-project.org/en/latest/reference/build/ | quote: "poetry-core is not supported because it does not support reading PEP 621 metadata." | type: official
- [C22] 相对路径依赖的写法因后端而异：pdm-backend 用 `file:///${PROJECT_ROOT}/`，hatchling 用 `{root:uri}/` | src: https://pdm-project.org/en/latest/usage/dependency/ | quote: "If you are using `hatchling` instead of the pdm backend, the URLs would be as follows: sub-package @ {root:uri}/sub-package" | type: official

### sources（依赖来源）
- [C23] 依赖一律 PEP 508 字符串；VCS 形式 `{vcs}+{url}@{rev}`，支持 git/hg/svn/bzr；`#egg=pkg&subdirectory=...` 片段；ssh 形式 `git+ssh://` / `git+git@host:path` | src: https://pdm-project.org/en/latest/usage/dependency/ | quote: "The URL should be like: `{vcs}+{url}@{rev}`" | type: official
- [C24] path 依赖：`pdm add ./sub-package`（路径必须以 `.` 开头），写入为 `name @ file:///${PROJECT_ROOT}/...`；URL 依赖可直接给 tar.gz/whl 地址 | src: https://pdm-project.org/en/latest/usage/dependency/ | quote: "sub-package @ file:///${PROJECT_ROOT}/sub-package" | type: official
- [C25] editable（`-e`）只允许 dev 依赖组；URL 内凭据可用 `${ENV_VAR}` 展开 | src: https://pdm-project.org/en/latest/usage/dependency/ | quote: "Editable installs are only allowed in the `dev` dependency group." | type: official
- [C26] 版本锁定/覆盖：`[tool.pdm.resolution.overrides]` 表（版本号/范围/绝对 URL），或 `--override constraints.txt`（可 URL） | src: https://pdm-project.org/en/latest/usage/dependency/ | quote: "You can specify the overrides in the `pyproject.toml` file, under the `[tool.pdm.resolution.overrides]` table" | type: official

### migrate（迁移）
- [C27] `pdm import` 支持：Pipenv `Pipfile`、Poetry 的 pyproject 段、Flit 的 pyproject 段、pip `requirements.txt`、setuptools `setup.py`；`pdm init`/`pdm install` 也能自动探测并导入 | src: https://pdm-project.org/en/latest/usage/project/ | quote: "PDM provides `import` command ... it now supports: 1. Pipenv's `Pipfile` 2. Poetry's section in `pyproject.toml` 3. Flit's section ..." | type: official
- [C28] `-f/--format` 接受的格式键：`pipfile`、`poetry`、`flit`、`setuppy`、`requirements`（源码 FORMATS 注册表） | src: https://raw.githubusercontent.com/pdm-project/pdm/main/src/pdm/formats/__init__.py | quote: "FORMATS: ... {\"pipfile\": ..., \"poetry\": ..., \"flit\": ..., \"setuppy\": ..., \"requirements\": ...}" | type: official
- [C29] 2.23.0 起 `pdm import` 会把 Poetry 的 `package-mode` 转成 PDM 的 `distribution` | src: https://api.github.com/repos/pdm-project/pdm/releases/tags/2.23.0 | quote: "`pdm import` now converts `package-mode` from Poetry's settings table to `distribution`." | type: official

### ci（CI 缓存）
- [C30] 官方 GitHub Action `pdm-project/setup-pdm`（当前 @v4）；输入 `cache`（默认 false，"Cache PDM installation"）与 `cache-dependency-path`（默认 `pdm.lock`），支持多行/glob | src: https://github.com/pdm-project/setup-pdm | quote: "`cache` | `false` | Cache PDM installation. ... `cache-dependency-path` | `pdm.lock` | The dependency file(s) to cache." | type: official
- [C31] 官方 CI 示例装依赖用 `pdm sync -d -G testing`；CI 无 HOME 时需 `export HOME=/tmp/home` 供 PDM 建缓存目录 | src: https://pdm-project.org/en/latest/usage/advanced/ | quote: "pdm sync -d -G testing" | type: official
- [C32] 缓存目录：config `cache_dir`（默认 `~/.cache/pdm`，env `PDM_CACHE_DIR`）；`pdm config install.cache on` 开中央 wheel 缓存，位于 `$(pdm config cache_dir)/packages`，`pdm cache info` 查看，`install.cache_method` 取 `symlink`/`hardlink` | src: https://pdm-project.org/en/latest/usage/config/ | quote: "The caches are located in `$(pdm config cache_dir)/packages`. You can view the cache usage with `pdm cache info`." | type: official

### index（私有源）
- [C33] `[[tool.pdm.source]]` 数组表，键：`name`、`url`、`verify_ssl`（默认 true）、`username`、`password`、`type`（`index` 默认 / `find_links`）、`include_packages`/`exclude_packages`（glob） | src: https://pdm-project.org/en/latest/usage/config/ | quote: "[[tool.pdm.source]] name = \"private\" url = \"https://private.pypi.org/simple\" verify_ssl = true" | type: official
- [C34] 把 source 的 `name` 设为 `pypi` 即替换默认 PyPI；`[tool.pdm.resolution] respect-source-order = true` 让索引按声明顺序优先 | src: https://pdm-project.org/en/latest/usage/config/ | quote: "just set the source name to `pypi` and that source will **replace** it." | type: official
- [C35] 凭据三种方式：URL 里 `${ENV_VAR}` 展开；`pdm config pypi.<name>.username/password`（按 `name` 合并）；keyring（service 名 `pdm-pypi-<name>`，仓库为 `pdm-repository-<name>`） | src: https://pdm-project.org/en/latest/usage/config/ | quote: "The service name will be `pdm-pypi-<name>` for an index and `pdm-repository-<name>` for a repository." | type: official
- [C36] config 键 `pypi.url`、`pypi.extra.url`、`pypi.<name>.url/...`；`pypi.ignore_stored_index=true` 只用 pyproject 里的源；`repository.<name>.*` 专供 `pdm publish`，与索引不共享配置 | src: https://pdm-project.org/en/latest/reference/configuration/ | quote: "`pypi.ignore_stored_index` | Don't add the indexes from the config that is not listed in project" | type: official

## conflicts
- `.python-version`/`PDM_PYTHON_VERSION` 的起点：文档页标注 "Added in 2.23.0"（https://pdm-project.org/en/latest/usage/project/），但 2.23.0 GitHub release notes 无此条目；release notes 中最早出现 `.python-version`/`python.use_python_version` 是 2.24.0 的 bugfix（"If a `.python-version` file is found and it contains multiple lines, the file will be ignored"），说明功能存在但 release note 未记，或文档 tip 版本不准。
- 文档 en/latest 与 search 摘要称 `pdm export` "only the `requirements.txt` format is supported" 与后文 pylock 导出并存——同页先说只支持 requirements.txt 再说支持 pylock，属页面内自相矛盾（quote: "At present, only the `requirements.txt` format is supported." vs "Additionally, PDM supports exporting to `pylock.toml` format"）。

## gaps
- `pdm import` 的完整 CLI 选项表（如 `--format` 之外是否还有其他 flag）未逐一核对 CLI reference 页；格式键名已从源码 FORMATS 确认。
- `[[tool.pdm.source]]` 是否还有文档未列出的键（如 `include_packages`/`exclude_packages` 之外）未穷举。
- setup-pdm `cache` 输入缓存的具体目录（是 `cache_dir` 还是别的）README 只写 "Cache PDM installation"，未给原句。

## leads
- `use_uv`/`PDM_USE_UV`：PDM 可委托 uv 做解析与安装；workspace 在 uv 模式下生成临时 `[tool.uv.workspace]`/`[tool.uv.sources]`，不回写 pyproject。
- `pdm export` 默认导出 requirements.txt，有 pre-commit hook（pdm-export / pdm-lock-check / pdm-sync）可用于 CI 校验锁文件新鲜度；`pdm lock --check`、`--refresh`。
- 锁目标：usage/lock-targets 页支持按平台/Python 版本锁定（替代已弃用的 cross_platform 策略，弃于 2.17.0）。
