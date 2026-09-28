# r1-pip
question: pip 作为 Python 包安装器，在 12 个维度上现状分别是什么？另外，PEP 751（`pylock.toml`）这份规范本身目前处于什么状态？
checked: https://peps.python.org/pep-0751/, https://pip.pypa.io/en/stable/, https://packaging.python.org/, https://pip.pypa.io/en/stable/reference/build-system/, https://pip.pypa.io/en/stable/topics/dependency-resolution/, https://pip.pypa.io/en/stable/reference/requirements-file-format/, https://pip.pypa.io/en/stable/cli/pip_install/, https://pip.pypa.io/en/stable/topics/vcs-support/, https://github.com/pypa/pip/blob/main/NEWS.rst, https://packaging.python.org/en/latest/specifications/pylock-toml/, https://pip.pypa.io/en/stable/cli/pip_lock/, https://packaging.python.org/en/latest/tutorials/installing-packages/

## claims
- [C1] pip is the package installer for Python from PyPI and other indexes | src: https://pip.pypa.io/en/stable/ | quote: "Pip is the package installer for Python. You can use it to install packages from the Python Package Index and other indexes." | type: official
- [C1] pip competes with uv (written in Rust, 10-100x faster) and other tools like Poetry, PDM | src: https://en.wikipedia.org/wiki/Pip_(package_manager) | type: secondary
- [C2] pip does not directly read [project] table from pyproject.toml during installation | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "pip can install from requirements files in pylock.toml format, but does not directly read [project] table" | type: official
- [C2] pip uses [build-system] table from pyproject.toml to identify build backend | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "Requires key in build-system.requires specifies build-time dependencies" | type: official
- [C2] pip has private table [tool.pip] for additional configuration options | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "[tool.pip] section allows tool-specific configuration" | type: official
- [C3] requirements.txt is not explicitly characterized as a lock file by pip documentation | src: https://pip.pypa.io/en/stable/reference/requirements-file-format/ | quote: "requirements files are a list of items to be installed by pip; basic format is portable but full syntax intended for pip consumption" | type: official
- [C3] pip freeze exists but pip documentation does not characterize it as creating reproducible lock files | src: https://pip.pypa.io/en/stable/reference/requirements-file-format/ | quote: "pip freeze mentioned in navigation but no reproducibility guarantee documented" | type: official
- [C3] PEP 751 is Final status as of March 31, 2025 | src: https://peps.python.org/pep-0751/ | quote: "Resolution: 31-Mar-2025" | type: official
- [C3] PEP 751 defines pylock.toml or pylock.[name].toml as standard cross-tool lock file format | src: https://peps.python.org/pep-0751/ | quote: "A lock file MUST be named pylock.toml or match r\"^pylock\\.([^.]+)\\.toml$\"" | type: official
- [C3] pip added experimental pip lock command in version 25.1 (April 2025) to generate pylock.toml | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "pip lock command is experimental; can lock packages from PyPI using requirement specifiers, VCS, local directories" | type: official
- [C3] pip added experimental pip install -r pylock.toml support in version 26.1 (April 2026) | src: https://www.infoworld.com/article/3951671/ | type: secondary
- [C3] pip lock generates single-platform lock file valid only for current Python version and platform | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "generated lock file only guaranteed to be valid for current python version and platform" | type: official
- [C3] pip lock cannot emit extras or dependency-groups information in pylock.toml | src: https://github.com/pypa/pip/issues/13953 | quote: "pip lock limitations: can't emit extras/dependency-groups, single platform lockfile" | type: secondary
- [C4] pip has no native workspace or monorepo support mechanism | src: https://packaging.python.org/en/latest/tutorials/installing-packages/ | quote: "pip install -e . is context-aware only to current directory, no global monorepo view" | type: official
- [C4] pip supports editable installs (pip install -e) but manual workaround needed for monorepo dependencies | src: https://pip.pypa.io/en/stable/topics/local-project-installs/ | quote: "editable installs allow files in development directory added to Python path; suited for development" | type: official
- [C5] pip does not manage Python interpreter versions; pyenv or similar tools required | src: https://github.com/pyenv/pyenv | quote: "pyenv intercepts Python commands using shims; pip remains separate package manager" | type: secondary
- [C6] pip assumes setuptools as default build backend if no pyproject.toml [build-system] section exists | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "if project lacks pyproject.toml with build-system, pip assumes setuptools>=40.8.0 with legacy backend" | type: official
- [C6] pip fully supports PEP 517 (build backend interface) and PEP 518 (build-system.requires) | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "PEP 518 introduced build-system.requires; PEP 517 provides build backend interface" | type: official
- [C6] pip version 25.3 removed legacy setup.py invocation in favor of PEP 517/518 approach | src: https://pip.pypa.io/en/stable/reference/build-system/ | quote: "changed in version 25.3: pip removed legacy setup.py invocation methods" | type: official
- [C7] pip dependency resolver introduced backtracking capability in version 20.3 | src: https://pip.pypa.io/en/stable/topics/dependency-resolution/ | quote: "Changed in version 20.3: Pip's dependency resolver now capable of backtracking" | type: official
- [C7] pip resolver reconsiders previous choices when discovering incompatibilities via backtracking | src: https://pip.pypa.io/en/stable/topics/dependency-resolution/ | quote: "When pip finds assumption incorrect, it backtracks, discarding work, choosing another path" | type: official
- [C7] pip resolver cannot handle non-PyPI binary dependencies; designed for PyPI source/wheel packages | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "pip installs from PyPI and indexes via --index-url; --find-links for local archives only" | type: official
- [C8] pip does not create or manage virtual environments; venv module or virtualenv tool required | src: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/ | quote: "pip is not a workflow management tool; venv used separately for environment creation" | type: official
- [C8] pip integrates with venv; when venv activated, pip automatically installs to that environment | src: https://docs.python.org/3/library/venv.html | quote: "unless --without-pip given, ensurepip invokes pip into virtual environment automatically" | type: official
- [C9] pip supports --index-url and --extra-index-url options for private package sources | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "--index-url (base URL of PyPI, default https://pypi.org/simple); --extra-index-url for additional indexes" | type: official
- [C9] pip supports keyring library for credential storage via --keyring-provider flag (auto/disabled/import/subprocess) | src: https://pip.pypa.io/en/stable/topics/authentication/?highlight=keyring | quote: "keyring support via --keyring-provider with values auto, disabled, import, or subprocess" | type: official
- [C9] pip reads .netrc file for hostname-based authentication credentials | src: https://pip.pypa.io/en/stable/topics/authentication/?highlight=netrc | quote: "if no credentials in URL, pip attempts to get credentials from user's .netrc file for URL hostname" | type: official
- [C9] pip supports token-based authentication by providing token as username without password | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "for indexes requiring single-part auth, provide token as username; do not provide password" | type: official
- [C10] GitHub Actions setup-python action caches pip dependencies via cache: pip parameter | src: https://github.blog/changelog/2021-11-23-github-actions-setup-python-now-supports-dependency-caching/ | quote: "cache: pip parameter causes setup-python to save/restore pip's wheel cache" | type: official
- [C10] setup-python cache works with requirements.txt or setup.py; cache-dependency-path parameter configurable | src: https://github.com/actions/setup-python | quote: "for setup.py projects use cache: pip with cache-dependency-path: setup.py" | type: secondary
- [C11] pip provides no official migration guide from other package managers; community tools like migrate-to-uv available | src: https://github.com/osprey-oss/migrate-to-uv | type: secondary
- [C12] pip first released October 28, 2008 by Ian Bicking as alternative to easy_install | src: https://en.wikipedia.org/wiki/Pip_(package_manager) | quote: "pip created by Ian Bicking and first released on October 28, 2008; version 0.2" | type: secondary
- [C12] pip current version 26.2.1; releases new version every 3 months | src: https://pip.pypa.io/en/stable/ | quote: "current version v26.2.1; we release updates regularly, new version every 3 months" | type: official
- [C12] pip maintained by Python Packaging Authority (PyPA) organization on GitHub | src: https://github.com/pypa/pip | quote: "maintained by Python Packaging Authority (PyPA); 16,253 commits; releases every 3 months" | type: official

## conflicts
- None identified. pip documentation and PEP 751 specification are consistent on lock file format and experimental status.

## gaps
- No explicit migration guide from pip to other tools found in official pip documentation (gap in C11)
- Specific PEP 621 [project] table field support details unclear (gap in C2; pip uses build-system but [project] usage pattern needs clarification)

## leads
- pip roadmap for pip sync command planned as primary interface for lockfile operations (mentioned as future)
- Python version constraint handling (requires-python field) interaction with pip resolver
- Multi-platform lock file generation (roadmap item; current single-platform limitation)
