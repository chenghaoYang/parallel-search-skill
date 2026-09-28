# r1-scout
question: 在 pip / uv / Poetry / PDM / pixi 已有专员的前提下，范围内还有哪些用户会踩的坑、网格没列的实体或维度？conda 是否必须与 pixi 分行？
checked: https://github.com/astral-sh/rye, https://hatch.pypa.io/latest/, https://hatch.pypa.io/latest/config/build/, https://pip-tools.readthedocs.io/en/latest/, https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html, https://packaging.python.org/en/latest/specifications/dependency-groups/, https://packaging.python.org/en/latest/specifications/pylock-toml/, https://packaging.python.org/en/latest/discussions/pip-vs-conda/ (404), https://github.com/conda/conda-lock, https://mamba.readthedocs.io/en/latest/, https://packaging.python.org/en/latest/specifications/externally-managed-environments/, https://pip.pypa.io/en/stable/cli/pip_install/, https://pip.pypa.io/en/stable/cli/pip_lock/, https://pip.pypa.io/en/stable/topics/caching/, https://packaging.python.org/en/latest/key_projects/

## claims
- [C1] conda 的环境清单文件是 environment.yml，`conda create --file environment.yml` 创建环境 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "Creating an environment from an environment.yml file" | type: official
- [C2] conda 自 26.5 起原生支持多平台 lockfile，可直接消费 conda-lock.yaml 与 pixi.lock（conda export 生成 / conda create --file 使用） | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "Lockfile support is available in conda 26.5 and later. ... Conda supports `conda-lock.yaml` and `pixi.lock` natively" | type: official
- [C3] conda 的 @EXPLICIT spec 文件（`conda list --explicit`）是单平台的 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "Explicit spec files are usually limited to a single platform, but lockfiles can support multiple platforms." | type: official
- [C4] conda-lock 是 conda 组织下的独立工具，对每个目标平台各做一次 solve 生成统一锁文件，安装时跳过 solver；默认输出文件名为 conda-lock.yml | src: https://github.com/conda/conda-lock | quote: "performing a conda solve for each platform you desire a lockfile for ... the conda solver *not* being invoked when installing the packages from the generated lockfile" | type: official
- [C5] conda 官方警告 pip 混装顺序：先 conda 装尽量多再用 pip；pip 用过后 conda 不感知变更，建议重建环境 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "Issues may arise when using pip and conda together. ... Once pip has been used, conda will be unaware of the changes." | type: official
- [C6] pip-tools = pip-compile + pip-sync；pip-compile 从 pyproject.toml/requirements.in 编译出钉死版本的 requirements.txt，但需对每个 Python 环境单独编译（跨环境不通用） | src: https://pip-tools.readthedocs.io/en/latest/ | quote: "users must execute `pip-compile` **on each Python environment separately** to generate a `requirements.txt` valid for each said environment" | type: official
- [C7] Hatch 官方自述是 project manager，且自带构建后端 hatchling（PEP 517/660）——两个角色都有 | src: https://hatch.pypa.io/latest/ , https://hatch.pypa.io/latest/config/build/ | quote: "Hatch is a modern, extensible Python project manager." / "Hatchling is a standards-compliant build backend and is a dependency of Hatch itself." | type: official
- [C8] Rye 仓库 2026-02-05 被归档（read-only），README 明示停止开发并指向 uv | src: https://github.com/astral-sh/rye | quote: "Rye is no longer developed. We encourage all users to use uv, the successor project from the same maintainers" | type: official
- [C9] mamba 是 conda 的 drop-in 替代（C++/libmamba），micromamba 官方定位适合 CI | src: https://mamba.readthedocs.io/en/latest/ | quote: "fully compatible with `conda` packages and supports most of conda's commands. ... `micromamba` is especially well fitted for the CI use-case" | type: official
- [C10] pip 官方文档把 --extra-index-url 找私有包标为不安全（dependency confusion）；pip 对所有索引无优先级、按版本选最优 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "Using the `--extra-index-url` option to search for packages which are not in the main repository (for example, private packages) is unsafe. This is a class of security issue known as dependency confusion" / "There is no priority in the locations that are searched." | type: official
- [C11] PEP 735 dependency-groups（pyproject.toml 的 [dependency-groups] 表）2024-10 批准；不进构建元数据；pip 26.x 已支持 `pip install --group` | src: https://packaging.python.org/en/latest/specifications/dependency-groups/ , https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "October 2024: This specification was approved through PEP 735" / "Install a named dependency-group from a \"pyproject.toml\" file" | type: official
- [C12] PEP 751 pylock.toml 是标准锁文件格式（2025-04 批准，2026-03 修订文件名优先级）；pip 26.x 有实验性 `pip lock` 命令输出 pylock.toml，`pip install -r` 可实验性读 pylock.toml | src: https://packaging.python.org/en/latest/specifications/pylock-toml/ , https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "April 2025: Initial version, approved via PEP 751." / "EXPERIMENTAL - Lock packages and their dependencies" | type: official
- [C13] pip lock 生成的锁只保证当前 Python 版本与平台有效（非通用锁） | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The generated lock file is only guaranteed to be valid for the current python version and platform." | type: official
- [C14] PEP 668 EXTERNALLY-MANAGED 标记文件使 pip 等安装器在系统解释器上报错退出，覆盖开关为 --break-system-packages（2022-06 批准） | src: https://packaging.python.org/en/latest/specifications/externally-managed-environments/ | quote: "the installer should exit with an error message ... The installer should have a way for the user to override these rules, such as a command-line flag `--break-system-packages`" | type: official
- [C15] pip 缓存默认路径因 OS 而异：Linux ~/.cache/pip、macOS ~/Library/Caches/pip、Windows %LocalAppData%\\pip\\Cache；23.3 起 HTTP 缓存改为 http-v2 | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "You can use `pip cache dir` to get the cache directory ... Changed in version 23.3: A new cache format is now used, stored in a directory called `http-v2`" | type: official

## conflicts
- conda 文档写锁文件名为 `conda-lock.yaml`（经 conda-incubator/conda-lockfiles 插件），而 conda-lock 工具 README 写默认输出 `conda-lock.yml`（.yml 扩展名）。两处原句：C2 "Conda supports `conda-lock.yaml`" vs C4 页 "By default, `conda-lock` store its output in `conda-lock.yml`"。可能是新旧两套实现并存，需下一轮核实关系。
- pip 的私有/编译锁（requirements.txt、pip lock 输出）均非跨平台（C6、C13），与 pylock.toml 规范允许 `environments` 多标记的"通用锁"定位存在张力——pip 目前未实现多环境锁。

## gaps
- conda-lock（独立工具）与 conda-incubator/conda-lockfiles（conda 26.5 的锁插件）的关系与前景未查：只打开了 https://github.com/conda/conda-lock 和 conda 文档，未打开 https://conda-incubator.github.io/conda-lockfiles/getting-started/。
- Hatch 是否生成/支持任何锁文件未核实（首页列了环境管理但未提 lockfile）。
- Pipenv 当前维护状态与 Pipfile.lock 格式只在 PyPA key_projects 页看到一句，未开 pipenv 官方文档。
- uv/conda 的缓存目录、Poetry/PDM 的 dependency-groups 支持度未在本轮范围（各专员覆盖）。
- packaging.python.org 的 pip-vs-conda 讨论页 404（可能已迁移），pip/conda 混装原句改用 conda 官方文档。

## leads
- 实体：conda 独立行（与 pixi 分行） | 生态完全不同：environment.yml 清单、channels、@EXPLICIT 单平台 spec；conda ≥26.5 才原生支持 conda-lock.yaml/pixi.lock——与 pixi 分行但在 D1 标注"可读 pixi.lock" | https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
- 实体：conda-lock / conda-lockfiles | conda 锁生态是网格外实体且正在并入 conda 本体（26.5 插件化），conda 行 D1 绕不开它 | https://github.com/conda/conda-lock
- 实体：mamba / micromamba | conda 兼容 drop-in 替代、micromamba 主打 CI；conda 行需在 D8/D10 覆盖或注明 | https://mamba.readthedocs.io/en/latest/
- 实体：Hatch(+hatchling) | 官方自述项目管理器且自带 PEP 517/660 后端，跨轴 B 与 D5；PyPA key_projects 亦列为统一 CLI | https://hatch.pypa.io/latest/ , https://hatch.pypa.io/latest/config/build/
- 实体：Rye | 已归档（2026-02-05）、官方指向 uv → 不进网格，仅在 D9 迁移列记 rye→uv | https://github.com/astral-sh/rye
- 实体：pip-tools | 官方即"pip-compile + pip-sync"，编译产物 requirements.txt 充当锁但须每环境单独编译 → 是 pip 的锁伴侣，可在 pip 行内覆盖而非独立行 | https://pip-tools.readthedocs.io/en/latest/
- 实体：Pipenv/Pipfile.lock | PyPA key_projects 仍列活跃（pipenv v2026.8.0），有私有锁文件；网格若要穷举需评估 | https://packaging.python.org/en/latest/key_projects/
- 坑：--extra-index-url 依赖混淆 | pip 官方 Warning 点名 unsafe + "no priority in the locations that are searched"；D7 私有源列必须写各工具索引优先级策略 | https://pip.pypa.io/en/stable/cli/pip_install/
- 坑：conda 与 pip 混装 | 官方顺序纪律（先 conda 后 pip、pip 之后 conda 失感知、改动需重建环境）→ 用户高频踩坑 | https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
- 坑：PEP 668 EXTERNALLY-MANAGED | 系统 Python 直接 pip install 报错、--break-system-packages 强绕——所有 pip 系工具共同坑，十列装不下 | https://packaging.python.org/en/latest/specifications/externally-managed-environments/
- 新维度：dependency-groups（PEP 735） | 标准 dev 依赖分组表 [dependency-groups]；pip --group、pylock.toml 已纳入 → 建议加"dev 依赖分组支持"列 | https://packaging.python.org/en/latest/specifications/dependency-groups/
- 新维度：pylock.toml（PEP 751）互认 | 标准锁问世，pip 26.x 已实验性 pip lock + -r 读 pylock.toml；建议 D1 拆"私有锁/标准锁/是否跨平台"三子项 | https://packaging.python.org/en/latest/specifications/pylock-toml/ , https://pip.pypa.io/en/stable/cli/pip_lock/
- 新维度：锁是否跨平台 | pip-tools 要逐环境编译、pip lock 只保当前平台，而 uv/pixi/conda-lock 产通用锁 → D1 需要"跨平台"子列 | https://pip-tools.readthedocs.io/en/latest/ , https://pip.pypa.io/en/stable/cli/pip_lock/
- 维度/坑：editable 与 PEP 723 内联脚本 | pip -e、--requirements-from-script、pylock.toml packages.directory.editable 字段 → 跨工具 editable 行为差异可入 D10 或单列 | https://pip.pypa.io/en/stable/cli/pip_install/ , https://packaging.python.org/en/latest/specifications/pylock-toml/
- 坑：CI 缓存目录不通用 | pip 缓存路径按 OS 三分且格式随版本变（http→http-v2）→ D8 需按"工具×OS"填 | https://pip.pypa.io/en/stable/topics/caching/
