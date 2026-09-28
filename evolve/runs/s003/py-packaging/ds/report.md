# Python 项目该用哪套包管理工具

> 回答 pip、uv、Poetry、PDM、pixi 差在哪一层，以及两件用户点名的事：PEP 751 的 `pylock.toml`，Poetry 2 的 `[project]`。conda 本体这轮不写进正文（§5）。截至 2026-09-24。先读 §0，字段名在 §2。

## 0. 一屏看懂

1. 先看它管不管项目。pip 文档把「管解释器」和「管整个项目」放在职责外 [5]。uv 用 `pyproject.toml` 加上自己的 `uv.lock` [8]。pixi 的工作单位是一份 manifest、`pixi.lock` 和 `.pixi` 目录 [43]。
2. **pip 和 uv 都已经能碰 `pylock.toml`，主锁却不是同一个文件。** 规范文件名是 `pylock.toml` 或 `pylock.<名>.toml` [4]。pip 25.1（2025-04-26）起实验性 `pip lock`，默认写出 `pylock.toml` [1][2]；26.1（2026-04-26）起 `pip install -r pylock.toml` 可读，仍标 experimental [1][3]。uv 自 0.6.15 起 preliminary：`uv export -o pylock.toml`，以及 `uv pip compile` / `uv pip sync` / `uv pip install -r` [9][8]。uv 项目的主锁仍是 `uv.lock`，`uv add -r` 拒绝 pylock.toml [8][10]。
3. **Poetry 2 已支持标准 `[project]`，私有表还在。** 2.0.0（2025-01-05）起尊重 PEP 621 的 `project` 段 [21]。许多 `[tool.poetry]` 元数据字段弃用，改指 `project.*`；`tool.poetry.dependencies` 不弃用，因为还有 `source`、相对路径、`^` / `~` [21]。FAQ：只写旧段，或使用 `project` 段，两种都可以 [26]。主锁仍是 `poetry.lock`。2.3.0（2026-01-18）起由 poetry-plugin-export ≥1.10.0 导出 pylock，官方写明还不能取代 `poetry.lock` [23]。
4. 跨平台要看锁本身。`uv.lock` 是 universal / cross-platform，格式只属于 uv [8]。`poetry.lock` 是 platform-agnostic [25]。`pip lock` 只保证当前 Python 和当前平台 [2]。
5. 谁准备解释器：uv 默认下载 Astral 的 python-build-standalone（`uv python install`，`python-preference` 默认 `managed`）[12]。PDM 2.13.0 起有 `pdm python install`，路径记在 `.pdm-python` [37][33]。pixi 把 Python 写成 conda 依赖 `[dependencies] python = "…"`；要用 `[pypi-dependencies]` 时必须显式有 python [39]。pip 用 `--python` 指向已经存在的解释器或 venv [47]。
6. 构建：pip 是 PEP 517 前端，自己不是后端 [6]。`uv init` 默认 `build-backend = "uv_build"`，uv_build 目前只支持纯 Python [13][14]。Poetry 的值是 `poetry.core.masonry.api` [22]。PDM 默认 `pdm.backend` [34]。pixi 把项目当 PyPI path 依赖安装时读 `[build-system]`；`pixi init --format pyproject` 默认 hatchling [40]。
7. 新项目按家族选。只往现成环境装 PyPI：`python -m pip install`，可重复安装用 pin 过的 requirements，或实验性 pylock [3][2]。PyPI 项目要锁、同步、并由工具下载解释器：uv 的 `uv sync` / `uv run`，或 PDM（`pdm install` 会补锁，`pdm sync` 只读锁）[20][28]。人已经在 Poetry 里：留在 Poetry 2，元数据放 `[project]`，富依赖语法继续放 `tool.poetry.dependencies` [21]。要 conda 频道和非 Python 包：pixi，没有 base 环境，`conda install` 对应 `pixi add` [43]。

## 1. Taxonomy

轴 A 是解析生态：PyPI 的 simple index，或 conda 频道。轴 B 是管到哪一层：安装器、项目（元数据 + 锁 + 虚拟环境）、prefix（含非 Python 依赖）。轴 C 只解释家族内部差异：PEP 621 `[project]`、PEP 517 `build-backend`、PEP 751 `pylock.toml`。PyPI 项目管理器的权威锁仍是各自的文件；pylock 是导出或实验入口。

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| PyPI 安装器 | pip | 往已有环境装包，不拥有项目生命周期 [5] |
| PyPI 项目管理器 | uv、Poetry、PDM | 读 pyproject、写锁、同步环境，索引是 PyPI |
| prefix | pixi | 环境在 `.pixi`；conda 包与 PyPI 包可以同时出现，PyPI 解析走内嵌的 uv [43][39] |

| 维度 | 这一列回答什么 |
|---|---|
| D1 锁 | 文件名、命令、是否 pylock、是否跨平台 |
| D2 元数据 | `[project]` 还是私有表；dev 依赖写哪 |
| D3 workspace | 多包时的配置键；pixi 里这个词指什么 |
| D4 Python | 谁安装解释器，版本钉在哪 |
| D5 后端 | 默认 `build-backend`；工具是不是前端 |
| D6 来源 | 默认索引或频道 |
| D7 私有源 | 字段名与凭据放哪 |
| D8 CI | 缓存目录或官方 action |
| D9 迁移 | 官方迁入路径 |
| D10 命令 | 每天的安装 / 同步命令 |

## 2. 对照矩阵

conda 整行仍是 ❓，不进表。

### D1 锁

| | 主文件与命令 | pylock.toml | 跨平台 |
|---|---|---|---|
| pip | 实验性 `pip lock`，默认输出 `pylock.toml`（25.1 起）[1][2] | 26.1 起 `-r pylock.toml`，仍 experimental [1][3] | 只保证当前 Python 与平台 [2] |
| uv | `uv.lock`，入库，不可手改 [8] | 0.6.15 起 export 与 `uv pip`；`uv add -r` 拒绝 [9][10] | universal / cross-platform [8] |
| Poetry | `poetry.lock`；2.0 起 `poetry lock` 默认 `--no-update` [24][21] | 2.3.0 起插件导出，不取代主锁 [23] | platform-agnostic [25] |
| PDM | 默认 `pdm.lock`；键 `lock.format`，环境变量 `PDM_LOCK_FORMAT` [28] | 2.25.0 起 opt-in 才改主格式；`pdm export -f pylock` 文档标 Added in 2.24.0。文档写未来版本才会把 pylock 当默认 [28][29] | ❓ |
| pixi | `pixi.lock`（页内示例 `version: 6`），不可手改；`--locked` / `PIXI_LOCKED` [38] | ❓ | ❓（manifest 有 `platforms`，锁是否多平台未见单独原句） |

### D2 元数据

| | 依赖写在哪 | dev / 分组 |
|---|---|---|
| pip | 不解析 `[project]`；本地目录的元数据由构建后端生成。目录要有 `pyproject.toml` 或 `setup.py` [3] | `--group` 读 `[dependency-groups]`（25.1 起）[3] |
| uv | `[project].dependencies` 与 `optional-dependencies`；来源表 `tool.uv.sources` [8][19] | `[dependency-groups]`；名为 `dev` 的组默认会 sync [19][20] |
| Poetry | `[project]` 或仍用 `[tool.poetry]`。`requires-python` 在 `[project]`；`tool.poetry.dependencies.python` 必须是它的子集 [21][22] | `[tool.poetry.group.*]`；2.2.0 起同时支持 PEP 735 [23] |
| PDM | `[project]`，规范写明 PEP 621 / 631 / 639 [30] | `[dependency-groups]` [30] |
| pixi | `pixi.toml` 的 `[workspace]`，或 `pyproject.toml` 中表名加前缀 `tool.pixi` [39] | `[project].dependencies` 映射成 `[pypi-dependencies]`；`[dependency-groups]` 映射成同名 feature。同名时 conda 依赖盖过 PyPI [40] |

Poetry 继续留在 `[tool.poetry]` 的还有 `package-mode`、`packages`、`[[tool.poetry.source]]`、`requires-poetry` [22]。

### D3 workspace

| | 配置 |
|---|---|
| pip | ∅。已查 lock、install、workflow 与命令列表，未见 workspace 键 |
| uv | `[tool.uv.workspace]`：`members` 必填，`exclude` 可选。成员依赖写 `{ workspace = true }`。一份 `uv.lock`。`uv run` / `uv sync` 默认 root，`--package` 选成员 [11] |
| Poetry | ∅。pyproject 文档没有 workspace 键。多目录示例用 `-C` / `--project`，2.0 起 `-C` 会真正切换目录 [46][21] |
| PDM | 2.28.0 起实验性 `[tool.pdm.workspace].members`（路径或 glob）。成员共享根环境和一份锁；`install` / `lock` / `sync` 在根上执行 [32][31] |
| pixi | workspace = manifest + `pixi.lock` + `.pixi`。多环境用 `[feature.<name>]` 与 `[environments]`（字段 `features`、`solve-group`），最少要有 `channels` 和 `platforms` [43][39] |

### D4 Python 与 D5 构建后端

| | 解释器 | `build-backend` |
|---|---|---|
| pip | 职责外 [5]。`--python` 指向已有解释器或 venv；`--python-version` 只做兼容性检查 [47][3] | 调用 PEP 517 `build_wheel` 等钩子。仅有 `setup.py` 时回退 `setuptools.build_meta:__legacy__`。25.3 起 `--use-pep517` 恒为开 [6][1] |
| uv | `uv python install`；`uv python pin` 写 `.python-version`。关掉自动下载：`python-downloads = "manual"` 或 `--no-python-downloads` [12] | `uv init` 默认 `uv_build`，文档示例 `requires = ["uv_build>=0.12.18,<0.13"]`。纯 Python，默认模块路径 `src/<package_name>`。可用 `--build-backend` 更换 [13][14] |
| Poetry | 约束写在 `requires-python` [22]。是否会安装解释器见 §5 | `poetry.core.masonry.api`，依赖包 `poetry-core`。缺 `[build-system]` 时 2.3.0 仍回退 poetry-core，公告写未来小版本默认改为 setuptools [22][23] |
| PDM | `pdm use` 把路径写入 `.pdm-python`（不要提交）。安装根默认 `~/.local/share/pdm/python` [33][37] | 默认 `pdm.backend`（`requires = ["pdm-backend"]`）。`pdm init` 还可选 setuptools、flit、hatchling、maturin [34][33] |
| pixi | conda 包，不是另一套 CPython 发行版 [39] | 见 §0。conda 包构建是另一条 preview：`[package.build].backend`，例如 `pixi-build-cmake`，开关 `pixi-build` [39] |

pip 26.1 起不再支持用 Python 3.9 跑 pip 自己 [1]。Poetry 2.3.0 起不再支持用 Python 3.9 跑 Poetry 自己 [23]。这与项目的 `requires-python` 不是同一件事。

### D6 来源与 D7 私有源

| | 默认从哪装 | 私有源 |
|---|---|---|
| pip | `--index-url` 默认 `https://pypi.org/simple`（`PIP_INDEX_URL`）。另有 VCS、本地目录、archive [3] | `--extra-index-url` 被标为不安全（dependency confusion）：各位置没有优先级，取最佳匹配 [3]。凭据：URL 内嵌、`.netrc`、`--keyring-provider`（`PIP_KEYRING_PROVIDER`）[48] |
| uv | `[[tool.uv.index]]`。`default = true` 替换默认索引；`explicit = true` 时只能被 `tool.uv.sources` 点名。默认 `index-strategy = "first-index"` [15] | `UV_INDEX_<NAME>_USERNAME` 与 `_PASSWORD`。凭据不写进 `uv.lock` [15]。来源类型还有 git、url、path、workspace [19] |
| Poetry | `[[tool.poetry.source]]` 不写 `priority` 时视为 primary，并禁用隐式 PyPI。另有 `supplemental`、`explicit` [25] | `poetry config http-basic.<name>`，或 `POETRY_HTTP_BASIC_<NAME>_USERNAME` / `_PASSWORD` [25]。`source` 不进入 core metadata，pip 安装时会忽略 [25] |
| PDM | 命名需求、以 `.` 开头的路径、URL、VCS（`{vcs}+{url}@{rev}`）、索引 [49] | `[[tool.pdm.source]]` 字段 `name` / `url` / `verify_ssl` / `username` / `password` / `type`（`index` 或 `find_links`）。同名 `pypi` 替换默认 PyPI。密码可写 `${ENV}`，或 keyring service `pdm-pypi-<name>` [35] |
| pixi | conda 包在 `[dependencies]`，`channel-priority` 默认 `strict`。PyPI 包在 `[pypi-dependencies]`，由内嵌 uv 解析；`[pypi-options].index-url` 默认 `https://pypi.org/simple`，每个环境只能有一个 [39] | 私有频道写完整 URL。`pixi auth login` 支持 token、basic、conda-token、S3、OIDC。没有钥匙串时写到 `~/.rattler/credentials.json`。PyPI 用 keyring 或 `.netrc` [42][39] |

### D8 CI、D9 迁移、D10 命令

| | 缓存 | 迁入与每天的命令 |
|---|---|---|
| pip | 默认开启。Linux `~/.cache/pip`，macOS `~/Library/Caches/pip`，Windows `%LocalAppData%\pip\Cache`。`PIP_CACHE_DIR`。上层已有缓存时，也不要关 pip 缓存 [7] | `pip lock -r <requirements file>` 可生成 pylock。锁不完整替代 requirements 文件 [2][4]。安装：`python -m pip install`，默认不升级已装包，除非 `--upgrade` [3] |
| uv | `UV_CACHE_DIR` 或 `tool.uv.cache-dir`，默认 `$XDG_CACHE_HOME/uv`。`uv cache prune --ci`。GitHub：`astral-sh/setup-uv` 的 `enable-cache: true`，key 可含 `hashFiles('uv.lock')` [16][17] | 官方迁移只写了 pip/pip-tools → 项目：`uv add -r requirements.in -c requirements.txt`。从已有 pyproject 工作流迁入的指南写明还没有 [18]。`uv sync` 默认 exact；`uv run` 会先 lock+sync，但是 inexact [20] |
| Poetry | `cache-dir` / `POETRY_CACHE_DIR`。CI 用 `POETRY_` 前缀变量。镜像里先 `poetry install --only main --no-root --no-directory` [25][26] | `poetry check` 列出弃用字段；`poetry config --migrate` 迁配置 [21]。2.0 起 `poetry sync` 取代 `install --sync`；`poetry shell` 移到插件，改为 `poetry env activate` [21] |
| PDM | `cache_dir` 默认 `~/.cache/pdm`（`PDM_CACHE_DIR`）。action：`pdm-project/setup-pdm`，`cache: true`，`cache-dependency-path` 默认 `pdm.lock` [50][36] | `pdm import` 认 Pipfile、Poetry 段、Flit 段、`requirements.txt`、`setup.py` [33]。`pdm sync` 只读锁；`pdm install` 会写出缺失或过期的锁。提交 `pyproject.toml` 和 `pdm.lock` [28][33] |
| pixi | `prefix-dev/setup-pixi`：有 `pixi.lock` 时默认按锁哈希缓存，并执行 `pixi install --locked` [41] | `pixi init --import environment.yml`；已有项目用 `pixi import --format=conda-env` 或 `pypi-txt`。全局工具用 `pixi global install` [44][43]。`pixi run` 发现未安装会先装 [38] |

## 3. 变体与适配层

pylock 贴在各家主锁旁边。本轮没有「A 导出的 pylock 能被 B 安装」的原句，所以下表只写各自文档里的角色。

| 工具 | pylock 在该工具里的位置 |
|---|---|
| pip | 实验性的写出和读入目标；生成结果绑定当前平台 [2] |
| uv | 项目主锁仍是 `uv.lock`；pylock 用于 `uv export` 和 `uv pip` [8][9] |
| Poetry | 导出交给 poetry-plugin-export；`poetry.lock` 保留 groups 与 markers（2.0 起）[23][21] |
| PDM | 默认格式名是 `pdm`；改成 `pylock` 要设 `lock.format`。另有 `-L` / `PDM_LOCKFILE` 指向别的锁文件 [28] |
| pixi | PyPI 求解使用内嵌 uv，conda 包作为已经锁定的输入传进去 [39]。文件名是 `pixi.lock` [38] |

Poetry 还有一条适配界限：依赖上的 `source` 是 Poetry 专有字段，构建出的 core metadata 里没有它 [25]。

## 4. 用户需要知道的坑

1. **私有包不要只加 `--extra-index-url`。** pip 写明这样做不安全，因为索引之间没有优先级 [3]。uv 的默认策略叫 `first-index`，用来防止 dependency confusion [15]。Poetry 把未标 priority 的源当成 primary，从而关掉隐式 PyPI；单个依赖的 `source` 也不会传给它的依赖 [25]。
2. **标准文件名不等于通用锁。** `pip lock` 的 pylock 只覆盖当前 Python 与当前平台 [2]。跨平台的是 `uv.lock` 和 `poetry.lock` [8][25]。
3. **Poetry 2 迁表时，富依赖语法留在 `tool.poetry.dependencies`。** 三条路：只用 `project.dependencies`；在 `project` 里声明、在 `tool.poetry` 里补锁定；或把 `dependencies` 放进 `dynamic` 后继续全写在 `tool.poetry` [21]。
4. **同名 workspace 不是同一种结构。** uv / PDM 是多个包、一份锁 [11][31]。pixi 是一个 prefix 项目里的多环境 [43]。Poetry 已查页面用 `-C` 进入另一个项目目录 [21][46]。
5. **CI 里「装」和「按锁装」经常是两条命令。** PDM：`pdm sync` 不写锁，`pdm install` 会 [28]。pixi 官方 action 默认 `pixi install --locked` [41]。uv：`uv sync` 会删掉锁里没有的包，`uv run` 默认不删 [20]。pip：有上层缓存时仍保留 pip 自己的缓存 [7]。

实验性边界：pip 的 lock 读写 [1]、PDM workspace（2.28.0）[32]、Poetry 缺 build-system 时「以后改默认 setuptools」[23]，都还不是稳定契约。

## 5. 未决与置信度

- conda 整行 ❓。scout 笔记不进正文，所以还不能写 conda 与 pixi 的二选一。pixi 侧已核对：没有 base，能导入 conda-env 格式的 environment.yml [43][44]。
- 「Poetry 会不会安装 CPython」不放进 §0。basic-usage 写 “Poetry will not install a Python interpreter for you” [24]；2.3.0 公告出现子命令 `poetry python` [23]。cli 页未打开。
- pip、Poetry 的 workspace 是定向查过之后的 ∅，不是官方的否定句。
- PDM 文档写不支持 poetry-core，理由是它不读 PEP 621 [34]。Poetry 2 的后端就是 `poetry.core.masonry.api`，并且已经读 `[project]` [22][21]。两页还没对过，理由可能过时。
- PDM 自身要 Python 3.9 还是 3.10：首页与 project 页不一致 [33]。未裁决。
- 笔记里「PDM 锁跨平台」的原句只证明了 `requires-python` 的覆盖关系 [33]，正文因此标 ❓。
- 未写入正文：Hatch、pip-tools、已归档的 Rye、mamba、conda-lock 的文件扩展名、各家 pylock 能否互装、pixi 本机缓存目录、uv 的 Poetry 迁移命令（官方写明那份指南还没有 [18]）。

## 来源

[1] pip 新闻 — https://pip.pypa.io/en/stable/news/
[2] pip lock — https://pip.pypa.io/en/stable/cli/pip_lock/
[3] pip install — https://pip.pypa.io/en/stable/cli/pip_install/
[4] PEP 751 — https://peps.python.org/pep-0751/
[5] pip 工作流范围 — https://pip.pypa.io/en/stable/topics/workflow/
[6] pip 与构建系统 — https://pip.pypa.io/en/stable/reference/build-system/
[7] pip 缓存 — https://pip.pypa.io/en/stable/topics/caching/
[8] uv 项目布局 — https://docs.astral.sh/uv/concepts/projects/layout/
[9] uv 0.6 changelog — https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.6.x.md
[10] uv 0.7 changelog — https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.7.x.md
[11] uv workspace — https://docs.astral.sh/uv/concepts/projects/workspaces/
[12] uv Python 版本 — https://docs.astral.sh/uv/concepts/python-versions/
[13] uv 项目配置 — https://docs.astral.sh/uv/concepts/projects/config/
[14] uv 构建后端 — https://docs.astral.sh/uv/concepts/build-backend/
[15] uv 索引 — https://docs.astral.sh/uv/concepts/indexes/
[16] uv 缓存 — https://docs.astral.sh/uv/concepts/cache/
[17] uv GitHub Actions — https://docs.astral.sh/uv/guides/integration/github/
[18] uv 从 pip 迁到项目 — https://docs.astral.sh/uv/guides/migration/pip-to-project/
[19] uv 依赖 — https://docs.astral.sh/uv/concepts/projects/dependencies/
[20] uv sync — https://docs.astral.sh/uv/concepts/projects/sync/
[21] Poetry 2.0.0 公告 — https://python-poetry.org/blog/announcing-poetry-2.0.0
[22] Poetry pyproject — https://python-poetry.org/docs/pyproject/
[23] Poetry 2.3.0 公告 — https://python-poetry.org/blog/announcing-poetry-2.3.0/
[24] Poetry 基本用法 — https://python-poetry.org/docs/basic-usage/
[25] Poetry 仓库与缓存 — https://python-poetry.org/docs/repositories/
[26] Poetry FAQ — https://python-poetry.org/docs/faq/
[28] PDM 锁文件 — https://pdm-project.org/en/latest/usage/lockfile/
[29] PDM 2.25.0 — https://github.com/pdm-project/pdm/releases/tag/2.25.0
[30] PDM 与 PEP 621 — https://pdm-project.org/en/latest/reference/pep621/
[31] PDM workspace — https://pdm-project.org/en/latest/usage/workspace/
[32] PDM 2.28.0 — https://github.com/pdm-project/pdm/releases/tag/2.28.0
[33] PDM 项目 — https://pdm-project.org/en/latest/usage/project/
[34] PDM 构建 — https://pdm-project.org/en/latest/reference/build/
[35] PDM 源配置 — https://pdm-project.org/en/latest/usage/config/
[36] setup-pdm — https://github.com/pdm-project/setup-pdm
[37] PDM 2.13.0 — https://github.com/pdm-project/pdm/releases/tag/2.13.0
[38] pixi 锁文件 — https://pixi.prefix.dev/latest/workspace/lock_file/
[39] pixi manifest — https://pixi.prefix.dev/latest/reference/pixi_manifest/
[40] pixi 与 pyproject — https://pixi.prefix.dev/latest/python/pyproject_toml/
[41] pixi GitHub Actions — https://pixi.prefix.dev/latest/integration/ci/github_actions/
[42] pixi 认证 — https://pixi.prefix.dev/latest/deployment/authentication/
[43] 从 conda 换到 pixi — https://pixi.prefix.dev/latest/switching_from/conda/
[44] pixi 导入 — https://pixi.prefix.dev/latest/tutorials/import/
[46] Poetry pre-commit / monorepo — https://python-poetry.org/docs/pre-commit-hooks/
[47] pip 的 --python — https://pip.pypa.io/en/stable/topics/python-option/
[48] pip 认证 — https://pip.pypa.io/en/stable/topics/authentication/
[49] PDM 依赖来源 — https://pdm-project.org/en/latest/usage/dependency/
[50] PDM 配置参考 — https://pdm-project.org/en/latest/reference/configuration/
