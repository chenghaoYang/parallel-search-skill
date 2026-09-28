# r1-scout
question: 2026 年选 Python 项目/环境工具时，conda、mamba、hatch、rye、pip-tools、pipenv 各自的官方页面怎么定义自己和 uv/pip/Poetry/PDM/pixi 的关系？哪些仍是新项目的独立选项，哪些已并入或不再作为默认？
checked: https://docs.conda.io/en/latest/, https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/install-packages-from-pypi.html, https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/pip-interoperability.html, https://conda.org/blog/2023-11-06-conda-23-10-0-release, https://mamba.readthedocs.io/en/latest/, https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html, https://hatch.pypa.io/latest/, https://hatch.pypa.io/latest/environment/, https://hatch.pypa.io/latest/config/environment/overview/, https://hatch.pypa.io/latest/plugins/environment/virtual/, https://github.com/astral-sh/rye, https://rye.astral.sh/guide/uv/, https://pip-tools.readthedocs.io/en/latest/, https://pipenv.pypa.io/en/latest/, https://pipenv.pypa.io/en/latest/pylock.html

## claims
- [C1] conda 自称跨语言包+依赖+环境管理器，仍是独立选项 | src: https://docs.conda.io/en/latest/ | quote: "Conda provides package, dependency, and environment management for any language." | type: official
- [C2] conda 官方推荐 Miniconda 或 Miniforge 作为发行版安装 conda | src: https://docs.conda.io/en/latest/ | quote: "We recommend the following conda distributions to install conda: Miniconda ... Miniforge" | type: official
- [C3] conda 自 23.10.0（2023-11）起默认 solver 换成基于 mamba 的 conda-libmamba-solver | src: https://conda.org/blog/2023-11-06-conda-23-10-0-release | quote: "With this 23.10.0 release we are changing the default solver of conda to conda-libmamba-solver!" | type: official
- [C4] conda 26.9+ 可用 conda-pypi channel 直接从 PyPI 装纯 Python wheel，且要求 rattler solver（与 pixi 同源） | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/install-packages-from-pypi.html | quote: "In conda version 26.9 and later, you can use the conda-pypi channel ... Rattler solver: conda config --set solver rattler" | type: official
- [C5] conda-pypi 官方明确"不是 pip 替代品"，仅公共 PyPI、仅纯 Python wheel、装时需连 PyPI；mamba/micromamba 支持"under active CEP discussion" | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/install-packages-from-pypi.html | quote: "this is not a pip replacement ... Public PyPI only. ... Pure Python wheels only. ... Support in other clients (mamba, micromamba, and so on) is under active CEP discussion." | type: official
- [C6] conda 官方建议在 conda env 里别混 pip：pip 装的包 conda 会丢失跟踪 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/install-packages-from-pypi.html | quote: "conda loses track of pip-installed packages, making future environment updates and installs unreliable" | type: official
- [C7] conda 锁文件靠独立项目 conda-lock | src: https://docs.conda.io/en/latest/ | quote: "Conda lock generates fully reproducible lock files for conda environments" | type: official
- [C8] mamba 自称"快速跨平台包管理器"，是 conda 的 drop-in 替代品，组件含 libmamba/mamba/micromamba | src: https://mamba.readthedocs.io/en/latest/ | quote: "Mamba is a fast, robust, and cross-platform package manager. ... fully compatible with conda packages and supports most of conda's commands. ... mamba: a ELF as a drop-in replacement for conda" | type: official
- [C9] mamba 官方安装指引推荐 Miniforge，并指出 conda 已内置 libmamba solver | src: https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html | quote: "conda-libmamba-solver now ships by default with Conda. Just use an up to date version of Conda to enjoy the speed improvememts." | type: official
- [C10] micromamba 官方定位尤其适合 CI | src: https://mamba.readthedocs.io/en/latest/ | quote: "micromamba is especially well fitted for the CI use-case but not limited to that!" | type: official
- [C11] hatch 自称"现代可扩展 Python 项目管理器"，覆盖 build/env/Python/测试/发布/版本管理 | src: https://hatch.pypa.io/latest/ | quote: "Hatch is a modern, extensible Python project manager." | type: official
- [C12] hatch 的 virtual 环境默认 installer 是 pip，设 installer="uv" 时由 UV 接管建环境与装依赖 | src: https://hatch.pypa.io/latest/plugins/environment/virtual/ | quote: "When set to uv, UV will be used in place of virtualenv & pip for virtual environment creation and dependency management" | type: official
- [C13] hatch 现可生成 PEP 751 锁文件 pylock.toml（locked=true、hatch env lock；默认环境名 pylock.toml，其他 pylock.<ENV>.toml）；页脚更新 2026-04/08 | src: https://hatch.pypa.io/latest/environment/ | quote: "Hatch can generate PEP 751 lockfiles (pylock.toml) for environments." | type: official
- [C14] hatch 装依赖走 pip 配置，可用 PIP_INDEX_URL 指私有源 | src: https://hatch.pypa.io/latest/config/environment/overview/ | quote: "Hatch uses pip to install dependencies so any configuration it supports Hatch does as well. For example ... PIP_INDEX_URL" | type: official
- [C15] rye 已停止开发，官方让全部用户迁往 uv；仓库 2026-02-05 归档为只读 | src: https://github.com/astral-sh/rye | quote: "Rye is no longer developed. We encourage all users to use uv, the successor project from the same maintainers ... no further updates are planned, including security updates." | type: official
- [C16] rye 生前定位=项目管理+包管理一体（装 Python/pyproject/venv/workspace） | src: https://github.com/astral-sh/rye | quote: "Rye is a comprehensive project and package management solution for Python." | type: official
- [C17] rye 锁文件名 requirements.lock（requirements.txt 兼容语法）；uv 用自有 uv.lock，需互通用 uv export | src: https://rye.astral.sh/guide/uv/ | quote: "Rye generates a lockfile named requirements.lock with a syntax compatible with pip ... uv uses its own lock file format (uv.lock). ... you can generate one with uv export" | type: official
- [C18] rye 的锁定/安装后端本来就是 uv（回退 unearth、pip-tools） | src: https://github.com/astral-sh/rye | quote: "Locking and Dependency Installation: is today implemented by using uv with a fallback to unearth and pip-tools" | type: official
- [C19] pip-tools 自称 = pip-compile + pip-sync，定位是 pip 系的锁定/同步层，不是环境或项目管理器 | src: https://pip-tools.readthedocs.io/en/latest/ | quote: "pip-tools = pip-compile + pip-sync. A set of command line tools to help you keep your pip-based packages fresh, even when you've pinned them." | type: official
- [C20] pip-compile 从 pyproject.toml/setup.cfg/setup.py/requirements.in 编译出 requirements.txt；须装在每个项目 venv 内（文档版本 v7.6.2.dev51，jazzband 维护） | src: https://pip-tools.readthedocs.io/en/latest/ | quote: "The pip-compile command lets you compile a requirements.txt file from your dependencies, specified in either pyproject.toml, setup.cfg, setup.py, or requirements.in." | type: official
- [C21] pip-tools 官方警告：requirements.txt 因环境而异，pip-compile 必须在每个目标 Python 环境分别跑 | src: https://pip-tools.readthedocs.io/en/latest/ | quote: "users must execute pip-compile on each Python environment separately to generate a requirements.txt valid for each said environment" | type: official
- [C22] pipenv 自称把 pip+virtualenv+Pipfile 合成一个工作流工具，锁文件 Pipfile.lock | src: https://pipenv.pypa.io/en/latest/ | quote: "Pipenv is a Python virtualenv management tool that combines pip, virtualenv, and Pipfile into a single unified interface ... maintaining a Pipfile for package requirements and a Pipfile.lock for deterministic builds." | type: official
- [C23] pipenv 页脚自称 production-ready；changelog 更新至 2026.8.0（2026-08-20），仍活跃维护 | src: https://pipenv.pypa.io/en/latest/pylock.html | quote: "Pipenv is a production-ready tool that aims to bring the best of all packaging worlds to the Python world." | type: official
- [C24] pipenv 已支持 PEP 751 pylock.toml，且 pylock.toml 与 Pipfile.lock 并存时优先用 pylock.toml | src: https://pipenv.pypa.io/en/latest/pylock.html | quote: "When both a Pipfile.lock and a pylock.toml file exist, Pipenv will prioritize the pylock.toml file." | type: official

## conflicts
- rye 停止开发时间两处不一致：rye.astral.sh 页顶横幅写 "Rye is no longer developed as of February 2025."（https://rye.astral.sh/guide/uv/），而 GitHub 仓库页写 "This repository was archived by the owner on Feb 5, 2026."（https://github.com/astral-sh/rye）。结论方向一致（都指向已停更），但日期差一年。

## gaps
- pip-tools 与 pipenv 官方页是否有"新项目建议改用 uv"的表述：已核对两者 index 全文与 pip-tools Deprecations 段，未见；未逐页搜 changelog。
- conda 经典 "use conda first, then pip" 原始段落（manage-environments 页）未取原句；以 C6 替代。
- hatch 的 UV 支持自哪个版本起、pylock.toml 锁定自哪个版本起：未查 changelog。
- mamba 2.x 现状（是否仍推荐新用户直接用 mamba 而非 conda+rattler）：官方页只推荐 Miniforge，无进一步对比。

## leads
- conda | 升格为网格行（已是行，可去掉 ❓）| 官方自称"package, dependency, and environment management for any language"；锁文件走 conda-lock；26.9+ 起有 conda-pypi channel + rattler solver | https://docs.conda.io/en/latest/
- mamba | 忽略（不单列，作 conda 行的生态注记）| "drop-in replacement for conda"，其 solver 已被 conda 收编为默认 | https://mamba.readthedocs.io/en/latest/
- hatch | 升格为网格行 | "modern, extensible Python project manager"，默认 pip、可选 UV 后端，新增 PEP 751 pylock.toml 锁定 | https://hatch.pypa.io/latest/
- rye | 只作为 uv 的迁移来源 | "no longer developed ... use uv, the successor project"，仓库已归档只读 | https://github.com/astral-sh/rye
- pip-tools | 升格为网格行 | pip 系的 lock 编译器（pip-compile/pip-sync），jazzband 活跃维护，与项目管理器互补而非竞争 | https://pip-tools.readthedocs.io/en/latest/
- pipenv | 升格为网格行 | 自称 production-ready、changelog 到 2026.8.0，已支持 PEP 751 pylock.toml | https://pipenv.pypa.io/en/latest/
- 坑-迁移 | rye→uv：截至 2025-07 "uv does not yet have a task runner"；[tool.rye] 需改 [tool.uv]；rye init --script ≠ uv init --script | https://rye.astral.sh/guide/uv/
- 坑-私有源 | rye 迁移：uv 不支持 index URL 里的环境变量展开（uv#5734）；conda-pypi "Public PyPI only"；hatch 走 PIP_INDEX_URL | https://rye.astral.sh/guide/uv/
- 坑-CI/离线 | micromamba 定位 CI 场景；pip-compile 须在每个目标 Python 环境分别生成 requirements.txt；conda-pypi 装包时需实时连 PyPI | https://mamba.readthedocs.io/en/latest/
- 坑-锁文件互换 | 三家锁文件互不通用：rye=requirements.lock、uv=uv.lock（需 uv export）、conda=conda-lock；PEP 751 pylock.toml 正在 hatch/pipenv 落地 | https://rye.astral.sh/guide/uv/
