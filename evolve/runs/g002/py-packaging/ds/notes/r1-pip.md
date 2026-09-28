# r1-pip
question: pip 在 PEP 751 pylock.toml 上具体能做什么，以及 pip 作为安装器（不是项目管理器）在清单、workspace、CPython、构建后端、依赖组、CI 缓存、私有源上官方写了什么？
checked: https://peps.python.org/pep-0751/, https://pip.pypa.io/en/stable/cli/pip_lock/, https://pip.pypa.io/en/stable/topics/caching/, https://pip.pypa.io/en/stable/reference/build-system/, https://pip.pypa.io/en/stable/topics/authentication/, https://raw.githubusercontent.com/pypa/pip/25.1/NEWS.rst, https://raw.githubusercontent.com/pypa/pip/26.1/NEWS.rst, https://pip.pypa.io/en/stable/_sources/topics/workflow.md.txt, https://pip.pypa.io/en/stable/_sources/topics/secure-installs.md.txt, https://pip.pypa.io/en/stable/_sources/reference/requirements-file-format.md.txt, https://pip.pypa.io/en/stable/_sources/topics/python-option.md.txt, https://pip.pypa.io/en/stable/_sources/topics/repeatable-installs.md.txt, https://pip.pypa.io/en/stable/_sources/user_guide.rst.txt, https://pip.pypa.io/en/stable/_sources/cli/pip_install.rst.txt

## claims
- [C1] PEP 751 页眉 Status 为 Final。 | src: https://peps.python.org/pep-0751/ | quote: "Final" | type: official
- [C2] PEP 751 页眉 Created 为 24-Jul-2024。 | src: https://peps.python.org/pep-0751/ | quote: "24-Jul-2024" | type: official
- [C3] 锁文件必须名为 pylock.toml，或匹配文中给出的命名正则（前缀 pylock.、后缀 .toml）。 | src: https://peps.python.org/pep-0751/ | quote: "A lock file MUST be named `pylock.toml` or match the regular expression" | type: official
- [C4] 写锁的是 lockers，安装的是 installers，可以是同一工具。 | src: https://peps.python.org/pep-0751/ | quote: "lockers which write the lock file, and *installers* which install from a lock file" | type: official
- [C5] 消费方应能在安装时不算依赖解析就确定要装什么。 | src: https://peps.python.org/pep-0751/ | quote: "without the need for dependency resolution at install-time." | type: official
- [C6] 生成：25.1（2025-04-26）NEWS Features 首次加入实验性 `pip lock`（PEP 751）。同文件 25.0 及更早没有这条。 | src: https://raw.githubusercontent.com/pypa/pip/25.1/NEWS.rst | quote: "Add a new, *experimental*, ``pip lock`` command, implementing :pep:`751`." | type: official
- [C7] 稳定文档页眉为 v26.2.1。`pip lock` 的 `-o`/`--output` 默认文件名是 pylock.toml，`-` 表示 stdout。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "Lock file name (default=pylock.toml). Use - for stdout." | type: official
- [C8] 生成的锁文件只保证对当前 Python 版本和当前平台有效。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "only guaranteed to be valid for the current python version and platform." | type: official
- [C9] 安装：26.1（2026-04-26）首次写实验性 `-r pylock.toml`。同文件 26.0 Features 没有这条。 | src: https://raw.githubusercontent.com/pypa/pip/26.1/NEWS.rst | quote: "Add experimental support to read requirements from standardized pylock.toml files (``-r pylock.toml``)." | type: official
- [C10] `-r`/`--requirement` 可是 requirements.txt 或 pylock.toml，pylock 仍 experimental，可重复；环境变量 `PIP_REQUIREMENT`。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The file or URL can be in pip's requirements.txt format, or pylock.toml format. pylock.toml support is experimental." | type: official
- [C11] 这类文件通常叫 requirements.txt，但文件名不是强制的。pylock.toml 不是该页所说的默认名。 | src: https://pip.pypa.io/en/stable/_sources/reference/requirements-file-format.md.txt | quote: "since `requirements.txt` is usually what these files are named (although, that is not a requirement)." | type: official
- [C12] 任一 requirement 带 `--hash` 就全局进入 hash-checking；哈希写在 requirements.txt 里。同页用 `--require-hashes` 强制，并用 `pip hash` 补其他归档的哈希。 | src: https://pip.pypa.io/en/stable/_sources/topics/secure-installs.md.txt | quote: "Specifying `--hash` against _any_ requirement will activate this mode globally." | type: official
- [C13] 文档标注 26.2 起有 `--no-require-hashes`，只校验带了哈希的 requirement。pip lock 页同时有 `PIP_REQUIRE_HASHES` 与 `PIP_NO_REQUIRE_HASHES`。 | src: https://pip.pypa.io/en/stable/_sources/topics/secure-installs.md.txt | quote: "a `--no-require-hashes` flag is available to disable this mechanism." | type: official
- [C14] D1：pip 用项目元数据（通常 pyproject.toml 或 setup.py）确定依赖，而不是去发现项目里的 requirements.txt。 | src: https://pip.pypa.io/en/stable/_sources/user_guide.rst.txt | quote: "not by discovering ``requirements.txt`` files embedded in projects." | type: official
- [C15] workflow 页把管理 Python 解释器本身排除在 pip 范围外。 | src: https://pip.pypa.io/en/stable/_sources/topics/workflow.md.txt | quote: "managing the Python interpreter itself" | type: official
- [C16] D4：`--python` 的两个取值是已有 Python 可执行文件路径，或虚拟环境路径。源文标注 versionadded 22.3。 | src: https://pip.pypa.io/en/stable/_sources/topics/python-option.md.txt | quote: "The path to a Python executable." | type: official
- [C17] D5：源码包构建交给 build backend。默认隔离构建：构建依赖装进临时目录并加入 sys.path。`--no-build-isolation` 关闭后，PEP 518 构建依赖须已安装。 | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "For building packages using this interface, pip uses an *isolated environment*." | type: official
- [C18] 有 build-system 但没有 build-backend 时，使用 `setuptools.build_meta:__legacy__`。 | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "The `setuptools.build_meta:__legacy__` build backend will be used." | type: official
- [C19] D6 extras 示例是 `python -m pip install 'SomePackage[PDF]'`。 | src: https://pip.pypa.io/en/stable/_sources/cli/pip_install.rst.txt | quote: "python -m pip install 'SomePackage[PDF]'" | type: official
- [C20] 安装依赖组：`python -m pip install --group groupA`。同节为 `[dependency-groups]`，`versionadded:: 25.1`。 | src: https://pip.pypa.io/en/stable/_sources/user_guide.rst.txt | quote: "python -m pip install --group groupA" | type: official
- [C21] NEWS 25.1：`--group` 形如 `group` 或 `path:group`，默认路径 pyproject.toml。 | src: https://raw.githubusercontent.com/pypa/pip/25.1/NEWS.rst | quote: "where the default path is ``pyproject.toml``" | type: official
- [C22] D7：`python -m pip freeze > requirements.txt` 仍是官方的钉版本 requirements 写法。 | src: https://pip.pypa.io/en/stable/_sources/user_guide.rst.txt | quote: "python -m pip freeze > requirements.txt" | type: official
- [C23] D8：缓存页写 Linux 尊重 `XDG_CACHE_HOME`；同页默认路径还有 `~/.cache/pip`、`~/Library/Caches/pip`、`%LocalAppData%\pip\Cache`。上层缓存例子是容器分层缓存。 | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "Pip will also respect `XDG_CACHE_HOME`." | type: official
- [C24] D9：`--index-url` 默认 `https://pypi.org/simple`。同页该选项的环境变量是 `PIP_INDEX_URL` 与 `PIP_PYPI_URL`。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "Base URL of the Python Package Index (default https://pypi.org/simple)." | type: official
- [C25] `--extra-index-url` 用来找主仓库没有的包（例如私有包）被标为不安全。 | src: https://pip.pypa.io/en/stable/_sources/cli/pip_install.rst.txt | quote: "not in the main repository (for example, private packages) is unsafe." | type: official
- [C26] 凭证示例是把用户名和密码放进 URL：`https://username:password@pypi.company.com/simple`。Authentication 全文没有“不要把凭证写入 URL”。 | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "https://username:password@pypi.company.com/simple" | type: official
- [C27] requirements 文件可用 `${API_TOKEN}`，文档建议把 token 和 key 放在环境变量里。 | src: https://pip.pypa.io/en/stable/_sources/reference/requirements-file-format.md.txt | quote: "You can now store sensitive data (tokens, keys, etc.) in environment variables" | type: official

## conflicts
- 无两段原文直接否定。PEP 要求安装时不做解析（C5）；pip 只写实验性 `-r pylock.toml`（C9–C10），未写该路径跳过 resolver。

## gaps
- D3：已打开的 user guide、workflow、pip lock、pip install 没有 workspace/monorepo 命令或表。不写成“不支持”。
- `--generate-hashes` 未出现在 secure-installs、requirements 每条选项、pip lock 选项页。
- 没有“无 -r 会/不会自动读 pylock.toml”的原句；示例都是显式 `-r requirements.txt`。
- `PIP_CACHE_DIR`、`--cache-dir`、`--trusted-host`、pip.conf 的 `index-url=` 所在页未整页打开。
- 没有“pip 下载 CPython”或“不下载”的原句。从 pylock 选 extras/groups、以及是否跳过 resolver，已打开的 pip 页没写。

## leads
- https://github.com/pypa/pip/issues/13952 与 https://github.com/pypa/pip/issues/13953（未整页打开）：维护者讨论 `-r pylock` 仍进 resolver，且 `pip lock` 不写 extras/groups。
- 页眉还有 Resolution 31-Mar-2025，并写 This PEP is a historical document。现行规范 https://packaging.python.org/en/latest/specifications/pylock-toml/ 未打开。
