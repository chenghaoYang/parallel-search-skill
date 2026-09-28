# r1-pip

question: pip（+ pip-tools）在锁文件、workspace/monorepo、Python 版本管理、构建后端交互、依赖解析与速度、私有源配置、全局工具运行、迁移路径、生态定位这些维度上，官方文档/changelog 是怎么说的？

checked: https://pip.pypa.io/en/stable/, https://pip.pypa.io/en/stable/cli/pip_lock/, https://pip.pypa.io/en/stable/cli/pip_freeze/, https://pip.pypa.io/en/stable/cli/pip_install/, https://pip.pypa.io/en/stable/topics/dependency-resolution/, https://pip.pypa.io/en/stable/topics/authentication/, https://pip.pypa.io/en/stable/reference/build-system/, https://pip.pypa.io/en/stable/topics/python-option/, https://peps.python.org/pep-0751/, https://pip-tools.readthedocs.io/, https://pipx.pypa.io/latest/

## claims

### D1 锁文件

- [C1] pip freeze 不生成锁文件：官方文档明确说"pip freeze reports what is installed; it does **not** compute a lockfile or a solver result"。只是快照当前安装的包，不做依赖解析。| src: https://pip.pypa.io/en/stable/cli/pip_freeze/ | quote: "pip freeze reports what is installed; it does not compute a lockfile or a solver result." | type: official

- [C2] pip 从 v25.1（2025年4月）起添加了实验性 `pip lock` 命令，生成 pylock.toml 格式的锁文件。| src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "Locks packages and their dependencies...the generated output file is **pylock.toml format** by default." | type: official

- [C3] pip lock 命令可指定输出文件（-o/--output，默认 pylock.toml），支持 -r requirements.txt 和 -e . 等多种输入源。| src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "Notable options include: -o/--output: Specifies the lock file name (defaults to `pylock.toml`)" | type: official

- [C4] pip lock 生成的锁文件有限制："The generated lock file is only guaranteed to be valid for the current python version and platform"。| src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The generated lock file is only guaranteed to be valid for the current python version and platform." | type: official

- [C5] pip 从 v26.1 起支持用 `pip install -r pylock.toml` 安装（实验性），与 requirements.txt 格式二选一。| src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "the file or URL can be in pip's requirements.txt format, or pylock.toml format. pylock.toml support is experimental." | type: official

- [C6] PEP 751 于 2025年3月31日获批，定义 pylock.toml 标准格式。| src: https://peps.python.org/pep-0751/ | quote: "PEP 751 reached its final status with a resolution dated **March 31, 2025**." | type: official

- [C7] pip-tools 的 pip-compile 生成标准 requirements.txt（含版本钉死和注释），未使用 pylock.toml 格式。| src: https://pip-tools.readthedocs.io/ | quote: "pip-compile...generates a complete dependency list with all transitive dependencies resolved and locked to specific versions...output is a standard `requirements.txt` file." | type: official

### D2 workspace/monorepo

- [C8] pip 本身无 workspace 概念；支持 `pip install -e <path>` 编辑模式安装本地包，但多包场景需手动编排。| src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "editable mode installation with `-e` for local project directories" 及搜索结果显示 monorepo 需手动按序安装各包。| type: official | secondary

### D3 Python 版本管理

- [C9] pip 不管理 Python 解释器版本。官方说："pip is a package manager used to install and manage software packages, not to manage Python interpreters."| src: https://pip.pypa.io/en/stable/topics/python-option/ | quote: "pip does not manage Python versions. Instead, it focuses on managing packages within a Python environment." | type: official

- [C10] pip 可通过 `--python` 选项（v22.3+）指向不同解释器或 venv 路径，但这是包安装的目标环境选择，非版本管理。| src: https://pip.pypa.io/en/stable/topics/python-option/ | quote: "you can use the `--python` option to specify the interpreter you want to manage. This option can take one of two values: 1. The path to a Python executable. 2. The path to a virtual environment." | type: official

### D4 构建后端

- [C11] pip 不含默认构建后端，按 PEP 517/518 规范委托给项目指定的构建后端。| src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "pip delegates to build backends—specialized tools that manage the actual compilation and packaging process." | type: official

- [C12] PEP 518 引入 pyproject.toml 中的 `build-system.requires` 列出构建时依赖。| src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "PEP 518 introduced the `build-system.requires` key in `pyproject.toml` files, which specifies 'a list of requirement specifiers for build-time dependencies.'" | type: official

- [C13] pip 创建隔离构建环境，调用后端的 PEP 517 钩子（build_wheel、prepare_metadata_for_build_wheel 等）生成 wheel。| src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "Pip establishes an isolated environment where build dependencies are installed...calls the backend's metadata hook...builds a wheel to extract metadata." | type: official

### D5 依赖解析与速度

- [C14] pip 自 v20.3 使用回溯（backtracking）算法解析依赖版本冲突。| src: https://pip.pypa.io/en/stable/topics/dependency-resolution/ | quote: "Pip uses a backtracking algorithm introduced in version 20.3." | type: official

- [C15] 复杂依赖树下 pip 解析可能很慢；官方明确："it can take a very long time to complete"。| src: https://pip.pypa.io/en/stable/topics/dependency-resolution/ | quote: "it can take a very long time to complete...If pip starts backtracking, it does not know how many choices it will reconsider." | type: official

- [C16] pip resolver 优先保证正确性而非速度：减少破坏现有装置风险的做法。建议用锁文件加速。| src: https://pip.pypa.io/en/stable/topics/dependency-resolution/ | quote: "The resolver prioritizes correctness over speed, reducing risks of breaking existing installations." | type: official

### D6 私有源

- [C17] `--index-url` 设置主包索引（默认 https://pypi.org/simple），`--extra-index-url` 添加额外索引。| src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "--index-url: Sets the base URL...--extra-index-url: Allows specifying Extra URLs of package indexes to use in addition to --index-url" | type: official

- [C18] pip 支持三种认证机制：(1) URL 中嵌入凭证 `https://user:pass@host/simple`；(2) `.netrc` 文件；(3) keyring 库（`--keyring-provider` 选项）。| src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "Pip supports three primary authentication mechanisms: Basic HTTP Authentication...netrc File Support...Keyring Support via the `keyring` library." | type: official

- [C19] keyring 提供商选项：`auto`（默认）、`import`、`subprocess`。可通过环境变量 `PIP_KEYRING_PROVIDER` 设置。| src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "keyring provider with values like `auto`, `import`, or `subprocess`...also be set via environment variables like `PIP_KEYRING_PROVIDER`." | type: official

### D7 全局工具运行

- [C20] pip 本身无工具隔离机制（共享单个环境，易冲突）；官方指向 pipx。| src: https://pip.pypa.io/en/stable/ + https://pipx.pypa.io/latest/ | quote: "pip installs both libraries and applications with no isolation...pipx installs only applications, each in its own virtual environment." | type: official

- [C21] pipx 是 PyPA 官方维护的工具，使用 pip 实现但为每个应用创建隔离 venv 并在 PATH 上暴露命令。| src: https://pipx.pypa.io/latest/ | quote: "pipx installs and runs end-user Python applications in isolated environments...maintained under the Python Packaging Authority (PyPA)." | type: official

### D8 迁移路径

- [C22] pip 官方文档未提供从 requirements.txt 明确升级到锁文件的迁移指南；但 pip lock 命令可从 requirements 文件或 pyproject.toml 生成 pylock.toml。| src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "pip-compile...reads from...requirements.in...and generates a complete dependency list...The resulting file is designed to be compatible with standard pip install workflows." | type: official

### D9 生态定位

- [C23] pip 官方定位："the package installer for Python"，由 PyPA（Python Packaging Authority）维护。| src: https://pip.pypa.io/en/stable/ | quote: "pip is described as 'the package installer for Python.'" | type: official

- [C24] pip 是 PEP 517/518/440/508/751 等标准的参照实现之一，与 PyPA 的规范体系互为支撑。| src: https://pip.pypa.io/en/stable/reference/build-system/ + https://peps.python.org/pep-0751/ | quote: "PEP 517...PEP 518...establish standardized interfaces for building Python packages." | type: official

## conflicts

- pip lock 和 pip install -r pylock.toml 都标记为 experimental；无法确定是否会成为稳定特性或何时稳定。文档中的实验标记未给出预期时间表。

## gaps

- pip 是否有计划在常规版本中稳定 pylock.toml 支持；目前无 release notes 明确日期。
- pip-tools 是否计划支持输出 pylock.toml 格式。
- pip 的锁文件与 pip-tools 的 requirements.txt 在生成方式或精度上的差异未明确文档化。

## leads

- PEP 751 标准本身在 packaging.python.org 有完整规范，pip 实现仍处早期（experimental）。
- pipx 虽为官方推荐，但不是 pip 功能扩展，而是单独工具；用户需主动选择使用。
