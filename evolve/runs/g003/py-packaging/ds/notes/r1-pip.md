# r1-pip
question: pip 官方文档和 PEP 751 里，标准锁文件 pylock.toml 的状态是什么？pip 是生成它、安装它，还是两者？从哪个版本起、用哪条命令？以及 pip 在项目表、workspace、Python 版本、构建后端、环境、CI 缓存、私有源、依赖分组上官方写了什么。
checked: https://peps.python.org/pep-0751/, https://pip.pypa.io/en/stable/news/, https://pip.pypa.io/en/stable/cli/pip_lock/, https://pip.pypa.io/en/stable/cli/pip_install/, https://pip.pypa.io/en/stable/cli/pip/, https://pip.pypa.io/en/stable/user_guide/, https://pip.pypa.io/en/stable/topics/local-project-installs/, https://pip.pypa.io/en/stable/topics/authentication/, https://pip.pypa.io/en/stable/topics/caching/, https://pip.pypa.io/en/stable/topics/configuration/, https://pip.pypa.io/en/stable/topics/python-option/, https://pip.pypa.io/en/stable/topics/workflow/, https://pip.pypa.io/en/stable/topics/repeatable-installs/, https://pip.pypa.io/en/stable/reference/build-system/, https://pip.pypa.io/en/stable/installation/, https://pip.pypa.io/en/stable/development/ci/

## claims
- [C1][D1] PEP 751：Status Final；Standards Track；Created 24-Jul-2024；Resolution 31-Mar-2025。 | src: https://peps.python.org/pep-0751/ | quote: "Status: Final" | type: official
- [C2][D1] 锁文件必须名为 pylock.toml（同句另有命名正则）。 | src: https://peps.python.org/pep-0751/ | quote: "A lock file MUST be named `pylock.toml`" | type: official
- [C4][D1] `lock-version` 必填，唯一合法值 `"1.0"`。`created-by`、`[[packages]]` 必填。 | src: https://peps.python.org/pep-0751/ | quote: "only valid value until future updates to the standard change it – as `\"1.0\"`." | type: official
- [C5][D1] 可选：`environments`、`requires-python`、`extras`、`dependency-groups`、`default-groups`（默认 `[]`）、`[tool]`。 | src: https://peps.python.org/pep-0751/ | quote: "Required?: no; defaults to `[]`" | type: official
- [C6][D1] 安装不应再做依赖解析。 | src: https://peps.python.org/pep-0751/ | quote: "without the need for dependency resolution at install-time." | type: official
- [C7][D1] 生成起点：news 最早 25.1（2025-04-26）。更早条目与 `25.1b` 标题皆无。未写 `--use-feature`。 | src: https://pip.pypa.io/en/stable/news/ | quote: "Add a new, *experimental*, `pip lock` command, implementing PEP 751." | type: official
- [C8][D1] 安装：news 最早 26.1（2026-04-26）`-r pylock.toml`。未写 `--use-feature`。 | src: https://pip.pypa.io/en/stable/news/ | quote: "read requirements from standardized pylock.toml files (`-r pylock.toml`)." | type: official
- [C9][D1] `pip install -r`/`--requirement` 接受 pylock.toml，experimental。`PIP_REQUIREMENT`。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "or pylock.toml format. pylock.toml support is experimental." | type: official
- [C10][D1] v26.2.1：`-o`/`--output`（`PIP_OUTPUT`）默认 pylock.toml。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "Lock file name (default=pylock.toml)." | type: official
- [C11][D2] 本地目录须有 pyproject.toml 或 setup.py。例：`python -m pip install -e .`。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "must contain a `pyproject.toml` or `setup.py`, otherwise pip will report an error" | type: official
- [C14][D2] 元数据经 build backend，未写直接解析 `[project]`。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "pip determines project metadata using the project’s build backend." | type: official
- [C13][D2] 组在 `[dependency-groups]`，`pip install --group groupA`，不是装项目本身。 | src: https://pip.pypa.io/en/stable/user_guide/ | quote: "“Dependency Groups” are lists of items to be installed stored in a `pyproject.toml` file." | type: official
- [C17][D3] user_guide、workflow、pip_lock、CLI 列表、development/ci 无 workspace，也无该子命令。 | src: https://pip.pypa.io/en/stable/topics/workflow/ | quote: "managing the overall “project”, are not part of pip’s scope." | type: official
- [C18][D3] PEP 只规定 monorepo 时锁文件放在容纳各项目的目录。 | src: https://peps.python.org/pep-0751/ | quote: "the `pylock.toml` file would be in the directory that held all the projects being locked." | type: official
- [C19][D3] 不搜索目录找 pyproject.toml；多项目须显式 `--group './sub1/pyproject.toml:groupA'`。 | src: https://pip.pypa.io/en/stable/user_guide/ | quote: "Pip does not search projects or directories to discover `pyproject.toml` files." | type: official
- [C20][D4] Installation 用 ensurepip/get-pip.py 把 pip 装进已有 Python。CLI 无装 CPython 的命令。 | src: https://pip.pypa.io/en/stable/installation/ | quote: "which can install pip in a Python environment." | type: official
- [C21][D4] pip 运行于这些解释器，而不是由 pip 安装它们。 | src: https://pip.pypa.io/en/stable/installation/ | quote: "CPython 3.10, 3.11, 3.12, 3.13, 3.14, 3.15 and latest PyPy3." | type: official
- [C22][D5] pip 不直接构建，交给 build backend。默认隔离。`--no-build-isolation` 关闭后 PEP 518 依赖须已装。 | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "This responsibility is delegated to “build backends”" | type: official
- [C24][D6] 装进与该 pip 关联的 Python。`python -m pip` 用指定解释器。默认不强制 venv。 | src: https://pip.pypa.io/en/stable/topics/local-project-installs/ | quote: "install the project into the Python that pip is associated with" | type: official
- [C25][D6] `--python`（22.3，`PIP_PYTHON`）可指向另一解释器或 venv。`--require-virtualenv` 才强制 venv。 | src: https://pip.pypa.io/en/stable/topics/python-option/ | quote: "the `--python` option to specify the interpreter you want to manage." | type: official
- [C26][D7] Repeatable Installs 全文无 pylock、无迁移步骤。仍是 `pip freeze`、`--hash`、wheelhouse、pip-tools。 | src: https://pip.pypa.io/en/stable/topics/repeatable-installs/ | quote: "pinned package versions can be generated using pip freeze." | type: official
- [C27][D7] PEP 不能完全取代 requirements 文件。 | src: https://peps.python.org/pep-0751/ | quote: "This PEP does NOT fully replace requirements files because:" | type: official
- [C23][D8] 缓存默认开（6.0）。`pip cache dir`（20.1）。Linux `~/.cache/pip`+`XDG_CACHE_HOME`；macOS `~/Library/Caches/pip`（26.2 起也尊重 XDG）；Windows `%LocalAppData%\pip\Cache`。 | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "You can use `pip cache dir` to get the cache directory" | type: official
- [C30][D8] `--cache-dir`/`PIP_CACHE_DIR`；`--no-cache-dir`/`PIP_NO_CACHE_DIR`。`pip cache info|remove|purge|list`。 | src: https://pip.pypa.io/en/stable/cli/pip/ | quote: "Store the cache data in <dir>." | type: official
- [C31][D9] `--index-url` 默认 https://pypi.org/simple（`PIP_INDEX_URL`、`PIP_PYPI_URL`）。`--extra-index-url`（`PIP_EXTRA_INDEX_URL`）找私有包被标不安全。另有 `--no-index`、`--find-links`。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "default https://pypi.org/simple" | type: official
- [C32][D9] INI，不是 pyproject。示例键 `index-url`。Unix `pip.conf`；Windows `pip.ini`。`PIP_CONFIG_FILE` 最后加载。 | src: https://pip.pypa.io/en/stable/topics/configuration/ | quote: "index-url = https://download.zope.org/ppix" | type: official
- [C33][D9] 凭据：URL 内用户名密码；`.netrc`；`--keyring-provider` 默认 auto，`PIP_KEYRING_PROVIDER`。keyring 须另装。 | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "[auto, disabled, import, subprocess]. (default: auto)" | type: official
- [C34][D10] `--group` 自 25.1（2025-04-26），形式 `group` 或 `path:group`，`PIP_GROUP`。 | src: https://pip.pypa.io/en/stable/news/ | quote: "installation from PEP 735 Dependency Groups." | type: official
- [C35][D10] 带路径时文件名必须是 pyproject.toml。未写从 pylock 选组。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "the name of the file must be “pyproject.toml”." | type: official

## conflicts
- 无已证实的双方原句冲突。pip 未写安装 pylock 时是否跳过 resolver。

## gaps
- PEP 页另写 "This PEP is a historical document." 指向现行规范 https://packaging.python.org/en/latest/specifications/pylock-toml/ ，该页未打开。
- D8：development/ci 无用户缓存路径。pip lock 页另有 "only guaranteed to be valid for the current python version and platform." 与 "locking from “requirements files”"。
- D7：无 requirements→pylock 迁移步骤。
- D2：无直接解析 `[project]` 的原句。
- D10：未写如何从 pylock 选 extras 或 dependency-groups。D3 的 workspace 否定限于已打开页，未做整站全文检索。未在源码核对 `--use-feature`。

## leads
- requirements.txt 与 `pip freeze` 仍在 repeatable-installs。
- constraints：`-c` / `PIP_CONSTRAINT`；另 `--build-constraint`。
- pip-tools：https://github.com/jazzband/pip-tools （repeatable-installs）。uv/Poetry/PDM/pixi 未查。
