# r1-scout
question: 除 uv、pip、Poetry、PDM、pixi 之外，2026 年新 Python 项目选型还该不该把 conda、mamba、conda-lock、pip-tools、Hatch、Rye 当成独立选项？各家官方文档怎么定位自己？官方文档明确警告过哪些选型坑？
checked: https://rye.astral.sh/, https://rye.astral.sh/guide/uv/, https://hatch.pypa.io/latest/, https://hatch.pypa.io/latest/why/, https://hatch.pypa.io/latest/config/environment/overview/, https://hatch.pypa.io/latest/meta/faq/, https://hatch.pypa.io/1.17/plugins/locker/, https://pip-tools.readthedocs.io/en/latest/, https://pip-tools.readthedocs.io/en/latest/changelog/, https://docs.conda.io/projects/conda/en/stable/index.html, https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html, https://mamba.readthedocs.io/en/latest/, https://mamba.readthedocs.io/en/latest/user_guide/mamba.html, https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html, https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html, https://conda.github.io/conda-lock/, https://conda.github.io/conda-lock/flags/

## claims
- [C1] Rye 官方自述是完整的 Python 项目与包管理方案。 | src: https://rye.astral.sh/ | quote: "Rye is a comprehensive project and package management solution for Python." | type: official
- [C2] 官方要求改用同一维护者的后继项目 uv。 | src: https://rye.astral.sh/ | quote: "We encourage all users to use uv, the successor project from the same maintainers, which is actively maintained and much more widely used." | type: official
- [C3] Rye 仍可使用，但不再更新，包括安全更新。 | src: https://rye.astral.sh/ | quote: "While Rye will continue to be available, no further updates are planned, including security updates." | type: official
- [C4] Rye 锁文件名是 requirements.lock，语法兼容 pip 的 requirements.txt。 | src: https://rye.astral.sh/guide/uv/ | quote: "Rye generates a lockfile named requirements.lock with a syntax compatible with pip and other tools that handle requirements.txt files." | type: official
- [C5] Hatch 官方自述是现代、可扩展的 Python 项目管理器。latest 首页页脚 2025-10-17。 | src: https://hatch.pypa.io/latest/ | quote: "Hatch is a modern, extensible Python project manager." | type: official
- [C6] 构建后端是姊妹项目 Hatchling。why 页页脚 2024-10-13。 | src: https://hatch.pypa.io/latest/why/ | quote: "Hatchling, the build backend sister project, has many benefits compared to setuptools." | type: official
- [C7] latest 环境页（页脚 2026-08-10）锁文件按 PEP 751：默认 pylock.toml，其它 pylock.<ENV_NAME>.toml。 | src: https://hatch.pypa.io/latest/config/environment/overview/ | quote: "By default, lockfiles are named following the PEP 751 convention: pylock.toml for the default environment and pylock.<ENV_NAME>.toml for all others." | type: official
- [C8] 内置 pip locker 未实现 apply_lock；从 pylock 做 dep sync 需要 uv locker。 | src: https://hatch.pypa.io/latest/config/environment/overview/ | quote: "The built-in pip locker does not currently implement apply_lock, so lockfile application with dep sync requires the uv locker." | type: official
- [C9] pip-tools 官方自述是一套命令行工具，用来维持已钉住的 pip 包。文档 v7.6.2.dev51。 | src: https://pip-tools.readthedocs.io/en/latest/ | quote: "A set of command line tools to help you keep your pip-based packages fresh, even when you've pinned them." | type: official
- [C10] pip-compile 把依赖编译成 requirements.txt，输入可为 pyproject.toml、setup.cfg、setup.py 或 requirements.in。 | src: https://pip-tools.readthedocs.io/en/latest/ | quote: "The pip-compile command lets you compile a requirements.txt file from your dependencies, specified in either pyproject.toml, setup.cfg, setup.py, or requirements.in." | type: official
- [C11] 欢迎页检索无 pylock / PEP 751；quote 只证明钉死文件被写成 requirements.txt。changelog 见 gaps。 | src: https://pip-tools.readthedocs.io/en/latest/ | quote: "And it will produce your requirements.txt, with all the Django dependencies (and all underlying dependencies) pinned." | type: official
- [C12] 坑：requirements.txt 随环境而变，必须在每个目标 Python 环境分别跑 pip-compile。 | src: https://pip-tools.readthedocs.io/en/latest/ | quote: "As the resulting requirements.txt can differ for each environment, users must execute pip-compile on each Python environment separately to generate a requirements.txt valid for each said environment." | type: official
- [C13] conda 官方自述：为任何语言提供包、依赖与环境管理。 | src: https://docs.conda.io/projects/conda/en/stable/index.html | quote: "Conda provides package, dependency, and environment management for any language." | type: official
- [C14] stable 管理环境页：锁文件支持自 conda 26.5 起。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "Lockfile support is available in conda 26.5 and later." | type: official
- [C15] 同一页把“完全相同的环境”分成 explicit spec 与 lockfiles 两条路。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "There are two ways to build identical conda environments, using explicit specification files and using lockfiles." | type: official
- [C16] 坑：用过 pip 之后，conda 不知道这些改动。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "Once pip has been used, conda will be unaware of the changes." | type: official
- [C17] mamba 用户指南：会 conda 就会 mamba。 | src: https://mamba.readthedocs.io/en/latest/user_guide/mamba.html | quote: "If you already know conda, great, you already know mamba!" | type: official
- [C18] 安装文档：快速求解由 conda 默认自带的 conda-libmamba-solver 提供。 | src: https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html | quote: "conda-libmamba-solver now ships by default with Conda." | type: official
- [C19] micromamba 不需要 base 环境，也不自带默认 Python。 | src: https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html | quote: "It does not need a base environment and does not come with a default version of Python." | type: official
- [C20] 总览：micromamba 尤其适合 CI，但不仅限于 CI。 | src: https://mamba.readthedocs.io/en/latest/ | quote: "micromamba is especially well fitted for the CI use-case but not limited to that!" | type: official
- [C21] conda-lock 自述是为 conda 环境生成完全可复现锁文件的轻量库。 | src: https://conda.github.io/conda-lock/ | quote: "Conda lock is a lightweight library that can be used to generate fully reproducible lock files for conda environments." | type: official
- [C22] conda-lock 默认输出 conda-lock.yml。 | src: https://conda.github.io/conda-lock/flags/ | quote: "By default, conda-lock store its output in conda-lock.yml in the current working directory." | type: official

## conflicts
- Hatch：FAQ（https://hatch.pypa.io/latest/meta/faq/ ，页脚 2024-05-28）写 "The only caveat is that currently there is no support for re-creating an environment given a set of dependencies in a reproducible manner." 环境页（https://hatch.pypa.io/latest/config/environment/overview/ ，页脚 2026-08-10）写 "Hatch can generate PEP 751 lockfiles (pylock.toml) for environments." 未裁决哪份等于已发布版本。
- 锁文件名：C14 那页写 "Conda supports conda-lock.yaml and pixi.lock natively"。conda-lock（https://conda.github.io/conda-lock/flags/）默认 "conda-lock.yml"。mamba（https://mamba.readthedocs.io/en/latest/user_guide/mamba.html）写 "These files are named conda-lock.yml by default"。
- Rye 页眉 https://rye.astral.sh/ 与 https://rye.astral.sh/guide/uv/ 均为 "Rye is no longer developed as of February 2025." 迁移正文只写 "Rye is no longer developed."

## gaps
- 未打开 GitHub，不能写 astral-sh/rye 归档日期。
- pip-tools 无 pylock 只检索了欢迎页与 changelog，未逐页看 reference/CLI。
- 未核对 PyPI 上的 Hatch 发布版是否已包含 latest 文档的 PEP 751 锁。
- micromamba 指南抓取在 quickstart 截断，该页的 conda-lock 段未亲眼看到。
- 未核 conda-lockfiles 与 conda 26.5 原生锁是否同一格式。

## leads
- 升格：conda、Hatch 可独立成行；Rye 不升格（指向 uv）；mamba/micromamba/conda-lock 并进 conda；pip-tools 只作 pip 的钉版本层。
- conda 分发与 ToS：https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html
- conda 频道混用/ABI：https://docs.conda.io/projects/conda/user-guide/tasks/manage-channels.html
- conda-lock 的 pip 与 pyproject 输入：https://conda.github.io/conda-lock/
- mamba：勿装 base、勿留 Anaconda defaults：https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html
- Rye 迁移页写 uv 用 uv.lock，可用 uv export：https://rye.astral.sh/guide/uv/
