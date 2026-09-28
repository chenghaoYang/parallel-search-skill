# r1-pip
question: pip 官方文档和 PEP 751 原文里，pip 是否已经能读和/或写 pylock.toml？pip 在项目元数据、workspace、Python 版本、构建后端、依赖来源、迁移、CI 缓存、私有源上官方怎么定位自己？
checked: https://pip.pypa.io/en/latest/cli/pip_lock/, https://peps.python.org/pep-0751/, https://pip.pypa.io/en/stable/news/, https://pip.pypa.io/en/stable/cli/pip_install/, https://pip.pypa.io/en/stable/cli/pip/, https://pip.pypa.io/en/stable/cli/pip_cache/, https://pip.pypa.io/en/stable/topics/workflow/, https://pip.pypa.io/en/stable/topics/caching/, https://pip.pypa.io/en/stable/topics/authentication/, https://pip.pypa.io/en/stable/topics/repeatable-installs/, https://pip.pypa.io/en/stable/topics/python-option/, https://pip.pypa.io/en/stable/reference/build-system/ (docs: stable=v26.2.1, latest=v26.3.dev0)

## claims
- [C1] pip 能写 pylock.toml：`pip lock` 命令存在，标记 EXPERIMENTAL，默认输出 pylock.toml | src: https://pip.pypa.io/en/latest/cli/pip_lock/ | quote: "EXPERIMENTAL - Lock packages and their dependencies from: PyPI (and other indexes) using requirement specifiers." / "Lock file name (default=pylock.toml). Use - for stdout." | type: official
- [C2] pip 写的锁只对当前环境有效 | src: https://pip.pypa.io/en/latest/cli/pip_lock/ | quote: "The generated lock file is only guaranteed to be valid for the current python version and platform." | type: official
- [C3] pip 能读 pylock.toml：`pip install -r` 与 `pip lock -r` 接受 pylock.toml 格式（experimental）| src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "The file or URL can be in pip's requirements.txt format, or pylock.toml format. pylock.toml support is experimental." | type: official
- [C4] 写锁起点：pip 25.1 (2025-04-26) changelog 最早条目 | src: https://pip.pypa.io/en/stable/news/ | quote: "Add a new, experimental, pip lock command, implementing PEP 751. (#13213)" | type: official
- [C5] 读锁起点：pip 26.1 (2026-04-26) changelog | src: https://pip.pypa.io/en/stable/news/ | quote: "Add experimental support to read requirements from standardized pylock.toml files (-r pylock.toml). (#13876)" | type: official
- [C6] pip 26.2 (2026-07-29) 继续修 pylock 行为 | src: https://pip.pypa.io/en/stable/news/ | quote: "Honor --only-final when sourcing requirements with -r pylock.toml. (#13950)" | type: official
- [C7] PEP 751 状态：Status: Final；Type: Standards Track；Resolution 31-Mar-2025；Created 24-Jul-2024 | src: https://peps.python.org/pep-0751/ | quote: "Status: Final ... Type: Standards Track ... Resolution: 31-Mar-2025" | type: official
- [C8] PEP 751 锁文件名规则 | src: https://peps.python.org/pep-0751/ | quote: "A lock file MUST be named `pylock.toml` or match the regular expression `r\"^pylock\\.([^.]+)\\.toml$\"` if a name for the lock file is desired" | type: official
- [C9] PEP 751 顶层锁定字段：lock-version="1.0"（必填）、created-by（必填）、environments、requires-python、extras、dependency-groups、default-groups、[tool] | src: https://peps.python.org/pep-0751/ | quote: "**Type**: string; value of `\"1.0\"` ... **Required?**: yes"（lock-version）；"Records the name of the tool used to create the lock file."（created-by，Required? yes） | type: official
- [C10] PEP 751 包字段：[[packages]] 必填；name 必填；version/marker/requires-python/dependencies 可选；来源互斥表 vcs、directory、archive、sdist、wheels、index、attestation-identities | src: https://peps.python.org/pep-0751/ | quote: "mutually-exclusive with `packages.vcs`, `packages.directory`, `packages.archive`, `packages.sdist`, and `packages.wheels`"；"Tools MUST support wheel files, both from a locking and installation perspective." | type: official
- [C11] PEP 751 已是历史文档，规范移至 PyPA specs | src: https://peps.python.org/pep-0751/ | quote: "This PEP is a historical document. The up-to-date, canonical spec, pylock.toml Specification, is maintained on the PyPA specs page" | type: official
- [C12] pip 官方定位（meta/项目）：只管环境里的包，不管项目本身 | src: https://pip.pypa.io/en/stable/topics/workflow/ | quote: "The core purpose of pip is to manage the packages installed in your environment. ... managing the Python interpreter itself, and managing the overall \"project\", are not part of pip's scope." | type: official
- [C13] workspace 无概念：在 workflow、pip install、caching、authentication、build-system、repeatable-installs 六个页面全文 grep "workspace|monorepo" 均 0 命中；pip 命令清单亦无 workspace 相关命令 | src: https://pip.pypa.io/en/stable/topics/workflow/ | quote: 无原句（整页检索无命中） | type: official
- [C14] Python 版本：pip 不安装/管理解释器本身；仅可用 --python 指向其他解释器或 venv（pip 22.3 起）| src: https://pip.pypa.io/en/stable/topics/python-option/ | quote: "you can use the --python option to specify the interpreter you want to manage. This option can take one of two values: The path to a Python executable. The path to a virtual environment." | type: official
- [C15] 构建后端：pip 委托 PEP 517 backend，默认 build isolation，可调 --no-build-isolation | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "pip does not directly handle the build process for the package. This responsibility is delegated to \"build backends\"" | type: official
- [C16] 依赖来源（sources）| src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "Install packages from: PyPI (and other indexes) using requirement specifiers. VCS project urls. Local project directories. Local or remote source archives." | type: official
- [C17] 私有源/index 原名：-i/--index-url（默认 https://pypi.org/simple，env PIP_INDEX_URL、PIP_PYPI_URL）、--extra-index-url（PIP_EXTRA_INDEX_URL）、--no-index、-f/--find-links（PIP_FIND_LINKS）；要求 PEP 503 simple API | src: https://pip.pypa.io/en/latest/cli/pip_lock/ | quote: "Base URL of the Python Package Index (default https://pypi.org/simple). This should point to a repository compliant with PEP 503" | type: official
- [C18] 凭据方式：URL 内嵌 basic auth、.netrc、keyring（--keyring-provider 取 auto/disabled/import/subprocess）| src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "Pip supports loading credentials from a user's .netrc file. ... credentials stored in your keyring using the keyring library, which can be enabled by passing --keyring-provider" | type: official
- [C19] CI 缓存：pip cache dir/info/list/remove/purge；缓存默认开启；--cache-dir（env PIP_CACHE_DIR）、--no-cache-dir；默认路径 Linux ~/.cache/pip、macOS ~/Library/Caches/pip、Windows %LocalAppData%\pip\Cache；HTTP 缓存目录 http-v2（23.3 起）| src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "Pip provides an on-by-default caching ... You can use pip cache dir to get the cache directory" | type: official
- [C20] 迁移路径：`pip lock -r requirements.txt -o pylock.toml` 可从 requirements.txt 生成锁（-r 同时接受两种格式）；但 repeatable-installs 指南正文仍以 requirements.txt/pip freeze/hash-checking/pip-tools 为主，全文无 "pylock"（整页 grep 0 命中，仅导航栏有 pip lock 链接）| src: https://pip.pypa.io/en/stable/topics/repeatable-installs/ | quote: "A requirements file, containing pinned package versions can be generated using pip freeze." | type: official

## conflicts
- 无直接矛盾。注意落差：PEP 751 状态已是 Final（2025-03-31 决议），而 pip 文档仍把读和写都标为 EXPERIMENTAL；pip 生成的锁只保证当前 Python/平台有效，PEP 751 本身支持 multi-use 锁（extras/dependency-groups/environments），pip 文档未声称支持该面。不裁决，仅记录。

## gaps
- pip `-r` 是否接受命名锁文件 `pylock.<name>.toml`（文档只写 "pylock.toml format"，未验证文件名识别规则）。
- `pip install -r pylock.toml` 是否按 PEP 751 Installation 节强制校验 environments/requires-python/marker、是否默认校验哈希——pip install 页未述。
- 是否存在 `pip sync` 或专用 "install from lock" 子命令：CLI 清单无，但未找到明文说"没有"。
- pip 对 pylock.toml 中 extras/dependency-groups 选择的安装侧支持程度未在文档说明。

## leads
- 规范正典：https://packaging.python.org/en/latest/specifications/pylock-toml/（PEP 页自指为历史文档）。
- pip `--group` 支持 PEP 735 dependency-groups（pip 25.1 起），读 pyproject.toml 但不拥有 [project]。
- PEP 751 reference implementation: github.com/brettcannon/mousebender。
