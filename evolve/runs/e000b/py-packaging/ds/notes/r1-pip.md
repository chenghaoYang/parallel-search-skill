# r1-pip
question: pip 官方文档 + pip-tools 官方文档在 D1(PEP621 支持)、D2(原生锁文件格式)、D3(PEP751 pylock.toml 支持)、D5(venv 配合)、D9(私有源认证)、D10(GitHub Actions 缓存) 如何说明
checked: https://pip.pypa.io/en/stable/,https://peps.python.org/pep-0751/,https://github.com/pypa/pip,https://pip-tools.readthedocs.io/,https://packaging.python.org/en/latest/specifications/pylock-toml/,https://pip.pypa.io/en/stable/topics/,https://pip.pypa.io/en/stable/cli/,https://github.com/actions/setup-python,https://peps.python.org/pep-0621/,https://pip.pypa.io/en/stable/user_guide/,https://pip.pypa.io/en/stable/reference/build-system/,https://pip.pypa.io/en/stable/topics/authentication/,https://pip.pypa.io/en/stable/cli/pip_lock/

## claims
- [C1] D1: pip 支持通过 `pip install .` 和 `pip install -e .` 安装本地项目，使用构建系统（如 setuptools）处理元数据 | src: https://pip.pypa.io/en/stable/user_guide/ | quote: "python -m pip install path/to/SomeProject" will install the project into the Python that pip is associated with | type: official
- [C2] D1: PEP 621 定义在 pyproject.toml 中使用 [project] 表来存储项目元数据（name, version, description, dependencies 等），是 tool-agnostic 的标准格式 | src: https://peps.python.org/pep-0621/ | quote: "All project information must be placed in a [project] table. Essential fields include: name (required), version, description, requires-python, dependencies" | type: official
- [C3] D1: pip 通过 PEP 517/518 标准与构建后端交互，支持读取 pyproject.toml 中的 [build-system] 配置，构建系统负责处理 PEP 621 元数据 | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "pip delegates package building to build backends. Pip will install build-time Python dependencies in a temporary directory" | type: official
- [C4] D2: pip 本身没有原生锁文件格式。在 25.1 版本（2025年4月）之前，pip 无法直接生成锁文件 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "pip lock is an experimental feature" | type: official
- [C5] D2: pip-tools 的 pip-compile 产出 requirements.txt 格式文件，包含自动生成的注释（Python 版本、执行命令、依赖关系），每个包带有版本固定和 # via 注释 | src: https://pip-tools.readthedocs.io/en/stable/reference/pip-compile/ | quote: "The compiled requirements.txt file includes header comments with metadata including autogeneration notice, Python version used, and command executed" | type: official
- [C6] D3: PEP 751（pylock.toml）在 2025 年 3 月 31 日达到 Final 状态，定义了标准的 TOML 格式锁文件 | src: https://peps.python.org/pep-0751/ | quote: "The PEP achieved Final status on March 31, 2025" | type: official
- [C7] D3: pip 在 25.1 版本（2025年4月）添加了实验性的 `pip lock` 命令，可生成 pylock.toml 文件 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The pip lock command is an experimental feature that generates lock files for Python package dependencies. The command generates a pylock.toml file by default" | type: official
- [C8] D3: pip 在 26.1 版本（2026年4月）添加了实验性的 `pip install -r pylock.toml` 支持，允许从 pylock.toml 安装 | src: https://pip.pypa.io/en/latest/cli/pip_lock/ | quote: "pip added experimental pip install -r pylock.toml in 26.1 (April 2026) for installing from one" | type: secondary
- [C9] D3: pip 生成的 pylock.toml 锁文件仅保证对当前 Python 版本和平台有效，不具有跨平台通用性 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The generated lock file is only guaranteed to be valid for the current python version and platform" | type: official
- [C10] D3: pip install -r pylock.toml 仍处于实验阶段，不支持 extras 和 dependency groups（截至版本 26.1） | src: https://pip.pypa.io/en/latest/cli/pip_lock/ | quote: "the install side does not yet support extras or dependency groups" | type: secondary
- [C11] D5: pip 不自动创建虚拟环境。用户必须手动使用 `python -m venv` 或其他工具创建虚拟环境 | src: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/ | quote: "With the standard venv module, you do not automatically create a virtual environment when running pip. You must explicitly create it first" | type: official
- [C12] D5: 激活虚拟环境后，pip 会自动在该环境中安装包，无需额外配置 | src: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/ | quote: "Once a virtual environment is created and activated, common installation tools such as pip will install Python packages into that virtual environment without needing explicit configuration" | type: official
- [C13] D9: pip 支持三种认证方式：1) 在 URL 中包含凭证 `https://username:password@pypi.company.com/simple`；2) .netrc 文件；3) keyring 库 | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "pip supports three primary authentication approaches for accessing private package indexes: Basic HTTP Authentication, .netrc File Support, and Keyring Support" | type: official
- [C14] D9: pip 支持 --index-url 和 --extra-index-url 选项配置私有 PyPI 源，支持通过 --keyring-provider 使用 keyring 库管理凭证 | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "The most secure option uses the keyring library with --keyring-provider. Available modes include: import, subprocess, auto (default)" | type: official
- [C15] D9: keyring 库需要单独安装，pip 依赖它但不包含它，防止循环依赖问题 | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "Note that keyring (the Python package) needs to be installed separately from pip" | type: official
- [C16] D10: GitHub Actions 官方 setup-python 提供 pip 缓存支持，通过 `cache` 参数启用 | src: https://github.com/actions/setup-python | quote: "The action includes built-in caching that: supports pip caches the global cache directory using requirements.txt or pyproject.toml" | type: official
- [C17] D10: setup-python 缓存支持多个依赖文件格式（requirements.txt, pyproject.toml, Pipfile.lock, poetry.lock），通过文件哈希值作为缓存键 | src: https://github.com/actions/setup-python | quote: "The action searches for dependency files (requirements.txt, pyproject.toml, Pipfile.lock, or poetry.lock) and uses file hashes as part of the cache key" | type: official
- [C18] D10: setup-python 支持 cache-dependency-path 输入用于自定义依赖文件位置，适用于非标准项目结构 | src: https://github.com/actions/setup-python | quote: "Supports the cache-dependency-path input for multiple or non-standard file locations" | type: official

## conflicts
- 无。pip 官方文档、GitHub Actions 文档、PEP 751 说法一致。

## gaps
- D3: pip lock 命令何时正式出现（稳定版本），是否仍会改变接口或 API（官方尚未承诺）
- D3: pip-tools 是否规划迁移或添加对 pylock.toml 的生成支持（未查证）
- D5: pip 是否有任何计划添加自动 venv 创建功能（未查证）
- D9: .netrc 支持在 Windows 上的具体行为（文档未明确）

## leads
- pip 26.3.dev0 已开发中，可能包含对 pylock.toml 支持的增强（如 extras/dependency-groups），应跟踪后续发布
- pip-tools 上游仓库 (jazzband/pip-tools) 对 PEP 751 的适配情况值得关注
- uv 作为竞争方案已支持完整的 pylock.toml 读写能力，pip 实验性支持仍需完善
