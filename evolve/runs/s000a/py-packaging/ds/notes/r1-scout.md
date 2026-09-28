# r1-scout
question: 在 uv/pip/Poetry/PDM/pixi 这五者之外，2026 年选型还会被哪些官方工具或标准改写，以及官方文档已经点名的坑有哪些？
checked: hatch.pypa.io/latest/, hatch.pypa.io/latest/environment/, github.com/astral-sh/rye, github.com/jazzband/pip-tools, github.com/pypa/pipenv, pipenv.pypa.io/en/latest/commands.html, pipenv.pypa.io/en/latest/changelog.html, peps.python.org/pep-0735/, peps.python.org/pep-0668/, peps.python.org/pep-0751/, github.com/conda/conda-lock, mamba.readthedocs.io/en/latest/, docs.astral.sh/uv/guides/integration/github/, docs.astral.sh/uv/concepts/indexes/, pixi.prefix.dev/latest/, docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html

## claims
- [C1] Hatch 不是单纯构建后端：自我定位项目经理（"a modern, extensible Python project manager"），且能通过 `hatch env lock` / `locked = true` 生成 PEP 751 的 pylock.toml（页更新 2026-04-23）。 | src: https://hatch.pypa.io/latest/environment/ | quote: "Hatch can generate PEP 751 lockfiles (`pylock.toml`) for environments." | type: official
- [C2] Rye 已死：仓库 2026-02-05 被归档为只读，官方要求迁移到 uv。 | src: https://github.com/astral-sh/rye | quote: "Rye is no longer developed. We encourage all users to use uv ... no further updates are planned, including security updates." | type: official
- [C3] pip-tools（Jazzband 而非 PyPA 维护）的锁产物仍是 requirements.txt，由 pyproject.toml/setup.cfg/setup.py/requirements.in 编译。 | src: https://github.com/jazzband/pip-tools | quote: "The `pip-compile` command lets you compile a `requirements.txt` file from your dependencies, specified in either `pyproject.toml`, `setup.cfg`, `setup.py`, or `requirements.in`." | type: official
- [C4] pip-compile 的 requirements.txt 是单环境产物，官方要求每个目标环境各编译一次（官方点名的坑）。 | src: https://github.com/jazzband/pip-tools | quote: "users must execute `pip-compile` **on each Python environment separately** to generate a `requirements.txt` valid for each said environment." | type: official
- [C5] Pipenv 仍在 PyPA 下活跃维护（changelog 至 2026.8.0，2026-08-20），锁文件名 Pipfile.lock；`pipenv sync` 是官方推荐的生产安装命令。 | src: https://pipenv.pypa.io/en/latest/commands.html | quote: "`pipenv sync` is the recommended command because it guarantees that no modifications will be made to your lock file." | type: official
- [C6] Pipenv 自 2026.0.0（2025-12-10）支持 PEP 751：pylock.toml 存在时优先于 Pipfile.lock；写需 `[pipenv] use_pylock = true`。 | src: https://pipenv.pypa.io/en/latest/changelog.html | quote: "When both a Pipfile.lock and a pylock.toml file exist, Pipenv will prioritize the pylock.toml file. Writing: Add `use_pylock = true` to the `[pipenv]` section" | type: official
- [C7] PEP 735（Final，2024-10-10）定义 pyproject.toml 顶层 `[dependency-groups]` 表——足以成为新分类维度。 | src: https://peps.python.org/pep-0735/ | quote: "This PEP defines a new section (table) in `pyproject.toml` files named `dependency-groups`." | type: official
- [C8] PEP 735 明确 dependency-groups 不是锁文件载体，只是锁文件生成器的输入。 | src: https://peps.python.org/pep-0735/ | quote: "Dependency Groups are not an appropriate place to store lockfiles, as they lack many of the necessary features." | type: official
- [C9] PEP 668（Final）EXTERNALLY-MANAGED 标记让 pip 在系统解释器上拒绝安装，覆盖开关 `--break-system-packages`。 | src: https://peps.python.org/pep-0668/ | quote: "The installer should have a way for the user to override these rules, such as a command-line flag `--break-system-packages`." | type: official
- [C10] PEP 751（Final，2025-03-31）：锁文件名 `pylock.toml` 或 `pylock.<name>.toml`，`lock-version = "1.0"`，安装时无需再跑解析器。 | src: https://peps.python.org/pep-0751/ | quote: "Installers consuming the file should be able to calculate what to install without the need for dependency resolution at install-time." | type: official
- [C11] conda ≥26.5 原生支持锁文件，且能直接读 pixi.lock——conda 生态锁文件已互通。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "Conda supports `conda-lock.yaml` and `pixi.lock` natively, and these lockfile types can be used to exactly recreate environments" | type: official
- [C12] 凭证进锁文件是因工具而异的坑：conda-lock 默认把私有 channel 的 basic auth 留在锁文件里（需 `--strip-auth`）。 | src: https://github.com/conda/conda-lock | quote: "By default `conda-lock` will leave basic auth credentials for private conda channels in the lock file." | type: official
- [C13] uv 官方保证凭证绝不写入 uv.lock，但安装时仍需能访问带认证 URL。 | src: https://docs.astral.sh/uv/concepts/indexes/ | quote: "credentials are *never* stored in the `uv.lock` file; as such, uv *must* have access to the authenticated URL at installation time." | type: official
- [C14] uv CI 缓存坑：缓存 UV_CACHE_DIR 而非 venv，cache key 用 hashFiles('uv.lock')，结尾 `uv cache prune --ci`；用 `uv pip` 时 key 换成 requirements.txt。 | src: https://docs.astral.sh/uv/guides/integration/github/ | quote: "If using `uv pip`, use `requirements.txt` instead of `uv.lock` in the cache key." | type: official
- [C15] conda 环境 ≠ venv 的官方证据：conda env 必须先 activate，不激活直接调可执行文件「一般不会工作」；pip 只能在 conda 装完后用。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "calling any executable in an environment without first activating that environment will likely not work." | type: official

## conflicts
- pixi 官方对比表称 Conda 无 lockfiles（表中 Conda 列 Lockfiles=❌，https://pixi.prefix.dev/latest/），但 conda 官方文档称 "Conda supports `conda-lock.yaml` and `pixi.lock` natively"、"Lockfile support is available in conda 26.5 and later"（https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html）。pixi 文档滞后于 conda 26.5。

## gaps
- pip-compile 是否/何时输出 pylock.toml：README 未提 PEP 751，无官方表态。
- pip 本体对 PEP 751 的消费（pip install pylock.toml）状态未核实。
- Hatch `env lock` 的解析后端（是否走 uv）未写明；pipenv `use_pylock` 默认关，是否成默认未知。

## leads
- lead: PEP 725 `[external]` 表（PEP 735 正文称 "in progress"）— 可能再造一列「非 Python 依赖声明」— https://peps.python.org/pep-0735/
- lead: pipx — PEP 668 建议 EXTERNALLY-MANAGED 报错引导用户用 pipx，轴1 可能需加「应用安装器」层 — https://peps.python.org/pep-0668/
- lead: uv `--index-strategy`：默认 `first-index` 防 dependency confusion，`unsafe-best-match` 最接近 pip 但官方标注有风险 — https://docs.astral.sh/uv/concepts/indexes/
- lead: pipenv "Initiative G" 可插拔 resolver（`--resolver NAME`，2026.8.0）— 解析器后端在变成可换零件 — https://pipenv.pypa.io/en/latest/changelog.html
- lead: mamba/micromamba 属 mamba-org、C++ 重写 conda 兼容层；pipenv 文档注明 Pipfile.lock 平台相关（docs/locking.md "Multi-Platform Considerations"）— https://mamba.readthedocs.io/en/latest/
