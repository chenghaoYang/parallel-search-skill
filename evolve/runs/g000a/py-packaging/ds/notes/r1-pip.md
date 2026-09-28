# r1-pip
question: pip 官方文档和 PEP 751 原文里，标准锁文件 pylock.toml 的状态是什么，pip 能否读取、能否生成；pip 在元数据、workspace、Python 版本、构建后端、环境、依赖组、私有源、缓存、迁移上管到哪一层？
checked: https://peps.python.org/pep-0751/, https://packaging.python.org/en/latest/specifications/pylock-toml/, https://pip.pypa.io/en/stable/cli/pip_lock/, https://pip.pypa.io/en/stable/cli/pip_install/, https://pip.pypa.io/en/stable/cli/pip/, https://pip.pypa.io/en/stable/cli/pip_freeze/, https://pip.pypa.io/en/stable/news/, https://pip.pypa.io/en/stable/topics/workflow/, https://pip.pypa.io/en/stable/topics/local-project-installs/, https://pip.pypa.io/en/stable/topics/caching/, https://pip.pypa.io/en/stable/topics/authentication/, https://pip.pypa.io/en/stable/topics/python-option/, https://pip.pypa.io/en/stable/topics/dependency-resolution/, https://pip.pypa.io/en/stable/reference/build-system/, https://pip.pypa.io/en/stable/user_guide/

## claims
- [C1] D2 PEP 751 状态 Final（Standards Track，Resolution 31-Mar-2025，Replaces 665）。 | src: https://peps.python.org/pep-0751/ | quote: "Status: Final" | type: official
- [C2] D2 PEP 751 是历史文档；同段指向 PyPA 现行 pylock.toml Specification。 | src: https://peps.python.org/pep-0751/ | quote: "This PEP is a historical document." | type: official
- [C3] D2 文件名 pylock.toml 或 pylock.<name>.toml（例 pylock.spam.toml）。 | src: https://peps.python.org/pep-0751/ | quote: "would first look for `pylock.spam.toml` to install from, and if that file didn’t exist then install from `pylock.toml`" | type: official
- [C4] D2 不支持的 lock-version major 必须报错。Example 写 lock-version = '1.0'。 | src: https://peps.python.org/pep-0751/ | quote: "If a tool doesn’t support a major version, it MUST raise an error." | type: official
- [C5] D2 安装器应能不算依赖解析就决定装什么。 | src: https://peps.python.org/pep-0751/ | quote: "Installers consuming the file should be able to calculate what to install without the need for dependency resolution at install-time." | type: official
- [C6] D2 locker 可以只导出 single-use。 | src: https://peps.python.org/pep-0751/ | quote: "Lockers MAY choose to not support writing lock files that support extras and dependency groups (i.e. tools may only support exporting a single-use lock file)." | type: official
- [C10] D2 pip 25.1（2025-04-26）加入实验性 pip lock，实现 PEP 751。能生成。 | src: https://pip.pypa.io/en/stable/news/ | quote: "Add a new, experimental, pip lock command, implementing PEP 751." | type: official
- [C11] D2 pip 26.1（2026-04-26）起可用 -r pylock.toml 实验性读取。 | src: https://pip.pypa.io/en/stable/news/ | quote: "Add experimental support to read requirements from standardized pylock.toml files (-r pylock.toml)." | type: official
- [C12] D2 v26.2.1 pip lock 仍 EXPERIMENTAL；默认名 pylock.toml（-o/--output，PIP_OUTPUT，- 为 stdout）。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "Lock file name (default=pylock.toml). Use - for stdout." | type: official
- [C13] D2/D4 pip 生成的锁只保证当前 Python 版本和当前平台。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The generated lock file is only guaranteed to be valid for the current python version and platform." | type: official
- [C14] D2 稳定版 pip install -r 接受 pylock.toml，并标明实验性（PIP_REQUIREMENT）。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "pylock.toml support is experimental." | type: official
- [C15] D1 依赖来自项目元数据（通常 pyproject.toml 或 setup.py），不靠项目内 requirements.txt。 | src: https://pip.pypa.io/en/stable/user_guide/ | quote: "pip determines package dependencies using the project metadata (typically in pyproject.toml or setup.py), not by discovering requirements.txt files embedded in projects." | type: official
- [C16] D1/D5 pip 不自己构建源码包。 | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "pip does not directly handle the build process for the package." | type: official
- [C17] D5 没有构建 sdist 的对应命令。 | src: https://pip.pypa.io/en/stable/topics/workflow/ | quote: "there is no corresponding command to build a source distribution." | type: official
- [C18] D3/D4/D6 不管环境创建、开发任务、Python 解释器本身和整体 project。 | src: https://pip.pypa.io/en/stable/topics/workflow/ | quote: "managing the Python interpreter itself, and managing the overall “project”, are not part of pip’s scope." | type: official
- [C19] D3 pip 不搜索目录发现 pyproject.toml。--group 默认 cwd 的该文件，也可 path:group。 | src: https://pip.pypa.io/en/stable/user_guide/ | quote: "Pip does not search projects or directories to discover pyproject.toml files." | type: official
- [C20] D4 --python（PIP_PYTHON，22.3 起）只改用已有解释器或已有 venv，不安装 CPython。 | src: https://pip.pypa.io/en/stable/topics/python-option/ | quote: "In both cases, pip will run exactly as if it had been invoked from that Python environment." | type: official
- [C21] D4 --python-version 只检查 wheel 与 Requires-Python，不安装解释器。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "The Python interpreter version to use for wheel and “Requires-Python” compatibility checks." | type: official
- [C22] D6 本地项目装进与该 pip 关联的 Python。--require-virtualenv（PIP_REQUIRE_VIRTUALENV、PIP_REQUIRE_VENV）可强制 venv。 | src: https://pip.pypa.io/en/stable/topics/local-project-installs/ | quote: "This will install the project into the Python that pip is associated with" | type: official
- [C23] D7 Dependency Groups（user guide：Added in version 25.1）存在 pyproject.toml；pip lock 也有 --group / PIP_GROUP。 | src: https://pip.pypa.io/en/stable/user_guide/ | quote: "“Dependency Groups” are lists of items to be installed stored in a pyproject.toml file." | type: official
- [C24] D8 默认 https://pypi.org/simple（--index-url；PIP_INDEX_URL、PIP_PYPI_URL）。--extra-index-url（PIP_EXTRA_INDEX_URL）无优先级，文档称不安全。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "Using the --extra-index-url option to search for packages which are not in the main repository (for example, private packages) is unsafe." | type: official
- [C25] D8 keyring 用 --keyring-provider，取值 auto、disabled、import、subprocess，默认 auto；另有 .netrc 与 PIP_KEYRING_PROVIDER。 | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "Pip supports loading credentials stored in your keyring using the keyring library" | type: official
- [C26] D9 默认目录 ~/.cache/pip、~/Library/Caches/pip、%LocalAppData%\pip\Cache。PIP_CACHE_DIR 对应 cli/pip 的 --cache-dir。 | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "You can use `pip cache dir` to get the cache directory that pip is currently configured to use." | type: official

- [C30] D10 没有 migrate 子命令。最接近的是实验性 pip lock 从 requirements files 锁定。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "pip also supports locking from “requirements files”, which provide an easy way to specify a whole environment to be installed." | type: official

## conflicts
- 文件名优先级：PEP 751 写 “See packages.vcs.path.”（https://peps.python.org/pep-0751/）。规范写 “If packages.archive.url is also specified, the filename as specified by this key takes precedence.”；History：“March 2026: Clarify file name precedence for archives, sdists, and wheels.”（https://packaging.python.org/en/latest/specifications/pylock-toml/）。
- pip 站内：Dependency Resolution 仍写 “You can create this with pip-tools.”（https://pip.pypa.io/en/stable/topics/dependency-resolution/）。changelog/cli 已有实验性 pip lock（https://pip.pypa.io/en/stable/news/，https://pip.pypa.io/en/stable/cli/pip_lock/）。
- 安装模型：PEP 要求安装时不必解析（C5）。pip 26.1/26.2 把 pylock 当 experimental requirements，并写 “conflicts with requirements from -r pylock.toml”（https://pip.pypa.io/en/stable/news/）。没写是否跳过 resolver。

## gaps
- D3：user guide、workflow、local-project-installs 无 workspace。规范只要求多项目锁文件放在包住这些项目的目录，没说 pip 实现了 workspace。
- D10：v26.2.1 命令列表无 migrate。无官方从 Poetry/requirements 迁移的命令句。
- 未写明：pip lock 是否写出 extras、dependency-groups、environments、requires-python、created-by；install -r pylock.toml 是否跳过解析。
- 未全文打开 https://pip.pypa.io/en/latest/（v26.3.dev0）。稳定文档停在 v26.2.1（2026-08-04）。
- --trusted-host 与凭据嵌入矩阵未逐条摘。已核对 index-url、extra-index-url、no-index、find-links、keyring、netrc。

## leads
- packaging.pylock 在 packaging 文档（未展开）。PEP 751 点名 PDM、pip-tools、Poetry、uv，未查它们是否读写 pylock。
