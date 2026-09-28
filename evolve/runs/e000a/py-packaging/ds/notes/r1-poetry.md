# r1-poetry

question: Poetry（含 2.0 版本变化）在以下 12 个维度上现状分别是什么？

checked: https://python-poetry.org/docs/pyproject/, https://github.com/python-poetry/poetry/blob/master/CHANGELOG.md, https://python-poetry.org/blog/announcing-poetry-2.0.0/, https://python-poetry.org/blog/announcing-poetry-2.1.0/, https://python-poetry.org/docs/configuration/, https://python-poetry.org/docs/managing-dependencies/, https://python-poetry.org/docs/pyproject/#build-system

## claims

- [C1] Poetry is a tool for dependency management and packaging in Python | src: https://python-poetry.org/docs/ | quote: "Poetry is a tool for dependency management and packaging in Python" | type: official

- [C2-1] Poetry 2.0.0 (January 5, 2025) introduces support for [project] table per PEP 621 | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "respects the [project] section in pyproject.toml as specified by PEP 621" | type: official

- [C2-2] [tool.poetry] remains in Poetry 2.0 for Poetry-specific features: dependencies, dependency groups, packages, exclude/include | src: https://python-poetry.org/docs/pyproject/ | quote: "Still used in [tool.poetry]: package-mode, packages, dependencies and dependency groups" | type: official

- [C2-3] Migration to [project] gradual; backward compatible, no automatic migration tool provided | src: https://python-poetry.org/docs/pyproject/ | quote: "gradually migrating to [project] while [tool.poetry] remains supported" | type: official

- [C3-1] Lock file format version 2.0 introduced in Poetry 1.3.0 | src: https://github.com/python-poetry/poetry/blob/master/CHANGELOG.md | quote: "Poetry 1.3.0 introduced new lock file format (version 2.0)" | type: official

- [C3-2] poetry-plugin-export exports poetry.lock to requirements.txt format | src: https://github.com/python-poetry/poetry-plugin-export | quote: "allows export of locked packages to requirements.txt and other formats" | type: official

- [C3-3] Poetry 2.3.0+ exports to pylock.toml (PEP 751) via poetry-plugin-export 1.10.0+ | src: https://python-poetry.org/blog/announcing-poetry-2.3.0/ | quote: "Poetry provides necessary information for poetry-plugin-export to export pylock.toml files" | type: official

- [C4-1] No native workspace; monorepo via path dependencies with develop=true flag | src: https://python-poetry.org/docs/managing-dependencies/ | quote: "Poetry does not provide workspace hoisting" | type: official

- [C4-2] poetry-monorepo-dependency-plugin handles complex monorepos with path dependencies | src: https://github.com/python-poetry/poetry | quote: "plugin facilitates complex monorepo structures by pinning version dependencies" | type: secondary

- [C5-1] Poetry requires pre-installed Python; relies on system, pyenv, or other version managers | src: https://python-poetry.org/docs/managing-environments/ | quote: "If you use tool like pyenv to manage Python versions, Poetry will use it" | type: official

- [C5-2] Poetry 2.1.0 (January 11, 2025) adds experimental poetry python install and poetry env use commands | src: https://python-poetry.org/blog/announcing-poetry-2.1.0/ | quote: "poetry python install 3.13 to add Python version, poetry env use 3.13 to configure" | type: official

- [C6-1] Default build backend: poetry-core 1.0.0+ with build-backend = poetry.core.masonry.api | src: https://python-poetry.org/docs/pyproject/#build-system | quote: "requires = [\"poetry-core>=1.0.0\"] build-backend = \"poetry.core.masonry.api\"" | type: official

- [C7-1] Dependency resolver uses PubGrub algorithm (conflict-driven solver) | src: https://python-poetry.org/docs/faq/ | quote: "Poetry uses PubGrub algorithm for conflict-driven solving of dependencies" | type: official

- [C7-2] Resolution is NP-complete; can be slow with packages having many versions | src: https://python-poetry.org/docs/faq/ | quote: "dependency resolution is NP Complete problem" | type: official

- [C8-1] Virtual environment managed via virtualenvs.in-project (stores .venv in project root) | src: https://python-poetry.org/docs/configuration/ | quote: "virtualenvs.in-project - Store venv in project root (.venv)" | type: official

- [C8-2] Custom venv location via virtualenvs.path configuration | src: https://python-poetry.org/docs/configuration/ | quote: "virtualenvs.path - Specify venv storage location" | type: official

- [C9-1] Private sources via [[tool.poetry.source]] in pyproject.toml | src: https://python-poetry.org/docs/managing-dependencies/ | quote: "repositories.<name>.url - Add custom package sources" | type: official

- [C9-2] Authentication via http-basic.* and pypi-token.* config; keyring support available | src: https://python-poetry.org/docs/configuration/ | quote: "http-basic.* and pypi-token.* - Manage authentication" | type: official

- [C10-1] CI caching recommended using poetry.lock hash as key for cache invalidation | src: https://python-poetry.org/docs/ | quote: "poetry.lock file serves as basis for cache invalidation" | type: official

- [C11-1] Migration from pip/requirements.txt via poetry init wizard | src: https://python-poetry.org/docs/cli/ | quote: "poetry init interactively guides creating pyproject.toml file" | type: official

- [C11-2] No official Poetry→uv migration tool; uv can read poetry.lock files | src: https://github.com/astral-sh/uv | quote: "uv can read poetry.lock files" | type: secondary

- [C12-1] Founded July 2016 by Sébastien Eustace; current version 2.1.0+ (January 2025) | src: https://python-poetry.org/blog/announcing-poetry-2.1.0/ | quote: "Poetry 2.1.0 released January 11, 2025" | type: official

- [C12-2] Requires Python 3.10+; actively maintained by python-poetry organization | src: https://python-poetry.org/docs/ | quote: "Poetry requires Python 3.10 or later" | type: official

- [C12-3] 34.3k GitHub stars indicating mature adoption | src: https://github.com/python-poetry/poetry | quote: "Project has 34.3k stars on GitHub" | type: secondary

## conflicts

- Lock file format: Only version 2.0 explicitly documented (Poetry 1.3.0+); no incremental versions found

## gaps

- Exact fields staying in [tool.poetry] vs moving to [project]; official migration checklist not found
- Performance comparison with uv/PDM not in official docs
- Keyring fallback behavior when unavailable
- poetry.lock backward compatibility across 2.x versions

## leads

- Poetry's movement toward Python version management (2.1.0) suggests broader environment self-containment in roadmap
- PEP 751 adoption (pylock.toml export in 2.3.0) indicates standardization path; check future versions for native replacement

