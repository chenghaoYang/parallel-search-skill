# r1-pip
question: pip 官方文档和 PEP 751 对「锁文件 / pylock.toml、项目元数据、workspace、Python 版本、构建后端、私有源、CI 缓存、从旧清单迁移」各自怎么规定？
checked: https://peps.python.org/pep-0751/, https://pip.pypa.io/en/stable/cli/pip_lock/, https://pip.pypa.io/en/stable/cli/pip_install/, https://pip.pypa.io/en/stable/news/, https://pip.pypa.io/en/stable/topics/workflow/, https://pip.pypa.io/en/stable/topics/repeatable-installs/, https://pip.pypa.io/en/stable/topics/caching/, https://pip.pypa.io/en/stable/topics/configuration/, https://pip.pypa.io/en/stable/topics/authentication/, https://pip.pypa.io/en/stable/topics/python-option/, https://pip.pypa.io/en/stable/reference/build-system/, https://packaging.python.org/en/latest/specifications/pylock-toml/

## claims
- [C1] PEP 751 Status: Final（Resolution 31-Mar-2025）；正典已迁 PyPA specs 的 pylock.toml spec。 | src: https://peps.python.org/pep-0751/ | quote: "The up-to-date, canonical spec, pylock.toml Specification, is maintained on the PyPA specs page." | type: official
- [C2] 锁文件名必须是 `pylock.toml` 或 `pylock.<name>.toml`。 | src: https://packaging.python.org/en/latest/specifications/pylock-toml/ | quote: "A lock file MUST be named `pylock.toml` or match the regular expression `r\"^pylock\\.([^.]+)\\.toml$\"`" | type: official
- [C3] pip 有 EXPERIMENTAL `pip lock` 写锁；`-o/--output` 默认 `pylock.toml`，例 `python -m pip lock -e .`。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "Lock file name (default=pylock.toml). Use - for stdout." | type: official
- [C4] 写 pylock.toml 自 pip 25.1 (2025-04-26) 起。 | src: https://pip.pypa.io/en/stable/news/ | quote: "Add a new, experimental, pip lock command, implementing PEP 751. (#13213)" | type: official
- [C5] 读/装 pylock.toml 自 pip 26.1 (2026-04-26) 起，入口 `-r pylock.toml`。 | src: https://pip.pypa.io/en/stable/news/ | quote: "Add experimental support to read requirements from standardized pylock.toml files (-r pylock.toml). (#13876)" | type: official
- [C6] `pip install -r`（及 pip lock -r）兼收 requirements.txt 与 pylock.toml。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "The file or URL can be in pip's requirements.txt format, or pylock.toml format." | type: official
- [C7] pip 的锁为 single-use：只保证当前 Python 版本/平台有效。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The generated lock file is only guaranteed to be valid for the current python version and platform." | type: official
- [C8] 锁记 URL/path+size+hashes（hashes 必填≥1 条）；`packages.index` 记来源 index URL。 | src: https://packaging.python.org/en/latest/specifications/pylock-toml/ | quote: "A table listing known hash values of the file where the key is the hash algorithm and the value is the hash value." | type: official
- [C9] meta：pip 不直接读 `[project]`；pyproject.toml 经 PEP 518/517/621/660 由 backend 产 metadata。 | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "first introduced in PEP 518 and later expanded in PEP 517, PEP 621 and PEP 660" | type: official
- [C10] meta：`--group`（install/lock 同有）从 pyproject.toml 装 named dependency-group。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "Install a named dependency-group from a \"pyproject.toml\" file." | type: official
- [C11] meta：requirements.txt 是 pip 自有格式、非标准；`--requirements-from-script` 另支持 PEP 723。 | src: https://peps.python.org/pep-0751/ | quote: "Unfortunately, the format is not a standard but is supported by convention." | type: official
- [C12] workspace ∅ + pyver ∅：pip 不管环境创建、解释器管理、「项目」整体；`--python <exe|venv>`（22.3+）仅操作已存在的解释器。 | src: https://pip.pypa.io/en/stable/topics/workflow/ | quote: "managing the Python interpreter itself, and managing the overall \"project\", are not part of pip's scope" | type: official
- [C14] backend：默认 build isolation——构建依赖装进临时目录加 sys.path。 | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "pip will install build-time Python dependencies in a temporary directory" | type: official
- [C15] backend：`--no-build-isolation`（PIP_NO_BUILD_ISOLATION）关闭隔离。 | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "This can be disabled using the `--no-build-isolation` flag" | type: official
- [C16] backend：无 `[build-system]` 但有 setup.py 时回退 `requires=["setuptools>=40.8.0"]`、`build-backend="setuptools.build_meta:__legacy__"`。 | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "requires = [\"setuptools>=40.8.0\"] build-backend = \"setuptools.build_meta:__legacy__\"" | type: official
- [C17] index：`-i, --index-url` 默认 https://pypi.org/simple、需 PEP 503 源（env PIP_INDEX_URL）；`--extra-index-url`（PIP_EXTRA_INDEX_URL）加副源；`--no-index` 关 index。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "Base URL of the Python Package Index (default https://pypi.org/simple). This should point to a repository compliant with PEP 503" | type: official
- [C18] index：pip.conf（`/etc/pip.conf`、`~/.config/pip/pip.conf`、`$VIRTUAL_ENV/pip.conf`；Win=pip.ini）+PIP_CONFIG_FILE；选项皆可用 `PIP_<UPPER_LONG_NAME>` 环境变量。 | src: https://pip.pypa.io/en/stable/topics/configuration/ | quote: "Pip's command line options can be set with environment variables using the format `PIP_<UPPER_LONG_NAME>`." | type: official
- [C20] index 认证：URL 内嵌凭据、`.netrc`、keyring（`--keyring-provider`=`auto|disabled|import|subprocess`，PIP_KEYRING_PROVIDER）。 | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "enabled by passing `--keyring-provider` with a value of `auto`, `disabled`, `import`, or `subprocess`" | type: official
- [C21] cicache：缓存默认开，`pip cache dir` 查目录；默认 `~/.cache/pip`/`~/Library/Caches/pip`/`%LocalAppData%\pip\Cache`。 | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "You can use `pip cache dir` to get the cache directory that pip is currently configured to use." | type: official
- [C22] cicache：缓存含 HTTP 响应（http-v2）与本地构建 wheel；`--no-cache-dir` 关闭，仅建议上层有缓存（容器分层）时关。 | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "recommended to **NOT** disable pip's caching unless you have caching at a higher level" | type: official
- [C23] migrate：`python -m pip lock -r requirements.txt` 即官方迁移路径（-r 收 requirements.txt，默认写 pylock.toml）。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The file or URL can be in pip's requirements.txt format, or pylock.toml format." | type: official
## conflicts
- 无。PEP 751 自述 historical、正典在 PyPA specs（措辞略异，属演进）。

## gaps
- 无独立「从锁安装」子命令；入口即 `-r pylock.toml`，未说明是否要求文件名匹配 `pylock*.toml`。
- `PIP_CACHE_DIR` 字面量未在已查页面出现（仅能由 `PIP_<UPPER_LONG_NAME>` 规则推出）。
- `pip lock` 能否输出 multi-use 锁未写明；C7 暗示 single-use。
- 无专门「CI 缓存」章节；pip 对锁内 hashes 的强制校验细节只在 PEP/spec 安装算法中规定。
- 无 pip-tools→pylock 专门迁移命令；官方仅称 pip-tools「builds upon pip」管理 requirements files（topics/repeatable-installs）。

## leads
- PEP 751 Inspiration 点名 uv/PDM/Poetry；monorepo 仅有「锁放共同目录」约定。
- pip 26.2 changelog 有 venv 化 build isolation 实验特性；`--trusted-host` 可在 pip.conf 多行追加（topics/configuration）。
- PEP 751 参考实现 mousebender（github.com/brettcannon/mousebender）。
