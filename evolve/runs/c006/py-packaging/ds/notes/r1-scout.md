# r1-scout
question: Python 包管理选型常见坑、横评应覆盖的实体/维度、社区共识点（线索搜集）
checked: discuss t/89778+t/46039, uv 12584/11708/12716/12604, poetry 10356, pip news, hatch history, poetry blog+repos, uv auth/compat/gh docs, pdm 3553, setup-uv+745, caktusgroup, pydevtools, nickjanetakis, pixi docs, sinoroc, pyopensci, datumlabs

## claims
- [C1] pip 25.1 (2025-04-26) added experimental `pip lock` (PEP 751); pip 26.1 (2026-04-26) added experimental `-r pylock.toml` | src: https://pip.pypa.io/en/stable/news/ | quote: "Add a new, *experimental*, `pip lock` command, implementing PEP 751" | type: official
- [C2] pip>=25.1, PDM>=2.24.0, uv>=0.6.15 export pylock.toml; PDM>=2.25.0 uses it as primary lock; uv installs via `uv pip sync pylock.toml` | src: https://discuss.python.org/t/community-adoption-of-pylock-toml-pep-751/89778 | quote: "pip, PDM, uv can now export pylock.toml files" | type: secondary
- [C3] uv can't use pylock.toml as its lock (no arbitrary graph entrypoints; `uv run -p` impossible) | src: https://github.com/astral-sh/uv/issues/12584 | quote: "no support for arbitrary entrypoints to the graph" | type: official
- [C4] Poetry 2.3 + poetry-plugin-export 1.10 export pylock.toml only; can't replace poetry.lock (no content-hash for `poetry check --lock`) | src: https://github.com/python-poetry/poetry/issues/10356 | quote: "can at least export `pylock.toml` files" | type: official
- [C5] Hatch v1.17.0 (2026-05-31) added PEP 751 lockfiles: `hatch env lock` → pylock.toml/pylock.<env>.toml, `hatch dep sync`, `locked=true`, UV+pip lockers | src: https://hatch.pypa.io/dev/history/hatch/ | quote: "generate PEP 751 compliant lockfiles (`pylock.toml`) for environments" | type: official
- [C6] `uv add` strips index-URL credentials from pyproject.toml → later `uv sync` 401s; intended, no warning | src: https://github.com/astral-sh/uv/issues/11708 | quote: "We never write plaintext credentials to a `pyproject.toml` or `uv.lock`" | type: official
- [C7] uv credential precedence: URL > netrc > `uv auth` store (plaintext; OS-native preview) > keyring (only "subprocess", off by default) | src: https://docs.astral.sh/uv/concepts/authentication/http/ | quote: "A keyring provider (off by default)" | type: official
- [C8] Google Artifact Registry: pip works via ambient keyring; uv needs index `authenticate = "always"` + `--keyring-provider subprocess` | src: https://github.com/astral-sh/uv/issues/12716 | quote: "set `authenticate = \"always\"` to force keyring lookup" | type: official
- [C9] PDM PDM_USE_UV=true passes index URLs to uv but not credentials → resolution failures | src: https://github.com/pdm-project/pdm/issues/3553 | quote: "the indexes are passed to `uv` on the command line but without the credentials" | type: official
- [C10] Poetry auth: `poetry config http-basic.foo`→keyring else auth.toml; keyring.enabled default true; pip-style keyring fallback; POETRY_HTTP_BASIC_* env; ~/.netrc conflicts | src: https://python-poetry.org/docs/repositories/ | quote: "stored to and retrieved from the keyring" | type: official
- [C11] `uv add -r` strips pins to uv.lock (`requests==2.31.0`→`requests`); on pip-tools .in files misses .in pins or pins all .txt sub-deps | src: https://www.caktusgroup.com/blog/2025/08/25/migrate-pip-tools-to-uv/ | quote: "Simply importing these with `uv add -r` does not work well" | type: secondary
- [C12] Pipenv→uv: `pipenv shell`→activate .venv or `uv run`; `migrate-to-uv` automates Pipfile→pyproject+uv.lock | src: https://pydevtools.com/handbook/how-to/how-to-migrate-from-pipenv-to-uv/ | quote: "The migrate-to-uv tool automates the conversion" | type: secondary
- [C13] uv venvs ship without pip; Astral won't seed pip or shim `pip`→`uv pip` | src: https://github.com/astral-sh/uv/issues/12604 | quote: "We do not want to seed `pip` by default… We do not want to shim `pip` to `uv pip`" | type: official
- [C14] uv = "drop-in replacement for common pip and pip-tools workflows" but not an exact clone: stricter pre-release opt-in, index validation, resolver priorities | src: https://github.com/astral-sh/uv/blob/8ee34679/docs/pip/compatibility.md | quote: "uv is _not_ intended to be an _exact_ clone of `pip`" | type: official
- [C15] uv pins package→index vs dependency confusion; `unsafe-best-match` ≈ pip but risks confusion (torchtriton) | src: https://github.com/astral-sh/uv/blob/8ee34679/docs/pip/compatibility.md | quote: "exposes users to the risk of \"dependency confusion\"" | type: official
- [C16] uv CI guidance: cache uv cache dir (key hashFiles('uv.lock')); `uv cache prune --ci` "optimized for CI"; .venv caching never suggested | src: https://docs.astral.sh/uv/guides/integration/github/ | quote: "used to reduce the size of the cache and is optimized for CI" | type: official
- [C17] Caching .venv breaks uv: restored venv "conflicts with `uv venv` on the next run (it refuses to overwrite)" | src: https://github.com/derekslinz/meta-data-mcp/blob/0cd9cedb74632107e9d3e4ab541cca2411901eb1/.github/workflows/ci.yml | quote: "DO NOT cache .venv" | type: secondary
- [C18] setup-uv `enable-cache: auto` skips release/tag/pull_request_target/workflow_run vs cache poisoning; prune-cache drops prebuilt wheels → PyPI re-downloads; same-key collisions → 409; PyPI admin: uv ≈50% of PyPI CI downloads | src: https://github.com/astral-sh/setup-uv/issues/745 | quote: "causing them to be re-downloaded from PyPI on every CI run" | type: official
- [C19] Poetry 2.0 (2025-01-05) supports [project]; most tool.poetry fields deprecated BUT "tool.poetry.dependencies is not deprecated"; coexist or `dynamic` | src: https://python-poetry.org/blog/announcing-poetry-2.0.0/ | quote: "`tool.poetry.dependencies` is not deprecated" | type: official
- [C20] conda→pixi: no base env (`pixi global`≈pipx); strict channel priority → "excluded due to strict channel priority"; env.yml `pip:`→`[pypi-dependencies]`; `platforms` = current machine only | src: https://pixi.prefix.dev/latest/switching%5Ffrom/conda/ | quote: "Pixi does not have a base environment" | type: official

## conflicts
- setup-uv prune-cache default: #745 (2025-08) says default true strips prebuilt wheels; current action.yml shows `default: "false"` — version-dependent.
- Hatch lockfile: 2024 comparisons say "no lock files" vs Hatch v1.17.0 (2026-05-31) PEP 751 — recency conflict.
- uv #11708: users expect URL creds persisted by `uv add`; maintainers call removal intentional — documented but recurrent, no warning.

## gaps
- Dependabot/Renovate pylock status at 2026-09 unverified (mid-2025 tracking issues only).
- Per-tool lockfile cross-platform semantics (pdm.lock, poetry.lock, uv.lock) — per-tool worker.
- pip-tools maintenance status unchecked; uv ≈50%-PyPI-CI figure = PyPI-admin comment only.

## leads
- Entities to add: pip-tools, pipx, conda/mamba/micromamba, pixi, Hatch, Rye (maintenance, superseded by uv per discuss t/46039), conda-lock, migrate-to-uv, twine, build backends (hatchling/pdm-backend/poetry-core/uv-build/setuptools/maturin), tox/nox, poetry-plugin-export, poetry-dynamic-versioning, artifacts-keyring/google-artifactregistry-auth, pyenv/mise/asdf.
- Dimensions to add: self-install (Rust binary vs pipx/script); Python-version mgmt; env location global vs project; env matrix/task runner; plugins (Poetry yes, uv none); publish; workspace/monorepo; uses-uv-backend (Hatch/PDM/pixi); PEP 751 export/consume/primary-lock; lockfile cross-platform; index-priority/dep-confusion; keyring provider matrix; PEP 582 legacy; CI cache semantics; Docker (UV_PROJECT_ENVIRONMENT, --frozen --no-install-project).
- Variant consensus: "uv replaces pip" → drop-in for workflows not clone; pip stays bundled; uv venvs lack pip. "Poetry 2 killed [tool.poetry]" → false, dependencies field not deprecated. "Hatch can't lock" → outdated post-v1.17.0. "pip has no lockfile" → outdated: pip lock (25.1), -r pylock.toml (26.1).
