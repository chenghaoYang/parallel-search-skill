# r2-pylock-edge
question: 反证/核验 5 条 pylock.toml 边界主张（poetry import、uv export preview gating、setup-uv glob、dependabot/renovate、hatch 1.17.0 + pipenv 页）
checked: https://raw.githubusercontent.com/python-poetry/poetry/main/CHANGELOG.md, https://python-poetry.org/docs/cli/, https://github.com/python-poetry/poetry-plugin-export (README/command.py via gh code search), https://docs.astral.sh/uv/concepts/preview/, https://docs.astral.sh/uv/concepts/projects/export/, https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md, https://raw.githubusercontent.com/astral-sh/setup-uv/main/action.yml, https://github.com/dependabot/dependabot-core/issues/12094, https://github.com/renovatebot/renovate/discussions/35704, https://docs.renovatebot.com/modules/manager/, https://hatch.pypa.io/latest/plugins/locker/, https://hatch.pypa.io/latest/history/hatch/, https://raw.githubusercontent.com/pypa/hatch/master/docs/blog/posts/release-hatch-1170.md, https://pipenv.pypa.io/en/stable/pylock.html

## claims
- [C1] Poetry 2.3.0 (2026-01-18) changelog 唯一 pylock 条目是导出能力；全仓库 gh code search "pylock" 仅命中 CHANGELOG.md，源码无 pylock 读入路径 | src: https://github.com/python-poetry/poetry/blob/main/CHANGELOG.md | quote: "Add support for exporting `pylock.toml` files with `poetry-plugin-export` ([#10677])" | type: official
- [C2] python-poetry.org CLI 文档全文无 pylock/pylock.toml；lock/install 仅描述 poetry.lock | src: https://python-poetry.org/docs/cli/ | quote: "This command locks (without installing) the dependencies specified in `pyproject.toml`." | type: official
- [C3] poetry-plugin-export 仅提供导出侧 pylock.toml 格式选项 | src: https://github.com/python-poetry/poetry-plugin-export | quote: "`--format (-f)`: The format to export to (default: `requirements.txt`). Additionally, `constraints.txt` and `pylock.toml` are supported." | type: official
- [C4] uv preview 特性清单中 `pylock` 仅覆盖安装侧 | src: https://docs.astral.sh/uv/concepts/preview/ | quote: "`pylock`: Allows installing from `pylock.toml` files." | type: official
- [C5] uv export 文档把 pylock.toml 列为普通 --format 值，唯一标 preview 的导出格式是 CycloneDX | src: https://docs.astral.sh/uv/concepts/projects/export/ | quote: "`pylock.toml`: The standardized Python lockfile format defined in [PEP 751] ... Support for exporting to CycloneDX is in preview, and may change in any future release." | type: official
- [C6] uv CHANGELOG 中 pylock 条目（0.12.0 校验、0.12.11 哈希生成等）均未标 preview，属 GA 功能的修复/强化 | src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: "Generate missing artifact hashes when exporting `pylock.toml` files to ensure they conform to PEP 751 ([#20146])" | type: official
- [C7] setup-uv action.yml 的 cache-dependency-glob 默认值逐字为 7 个 glob，含 `**/*.py.lock` 但不含 pylock.toml/pylock.*.toml | src: https://github.com/astral-sh/setup-uv/blob/main/action.yml | quote: "default: |\n  **/*requirements*.txt\n  **/*requirements*.in\n  **/*constraints*.txt\n  **/*constraints*.in\n  **/pyproject.toml\n  **/uv.lock\n  **/*.py.lock" | type: official
- [C8] dependabot-core issue #12094 "PEP 751 pylock.toml support"（2025-04-18, groodt）仍 OPEN，无维护者回复；gh code search "pylock" 在 dependabot-core 零命中 | src: https://github.com/dependabot/dependabot-core/issues/12094 | quote: "PEP 751 pylock.toml support ... State: Open ... labels L: python, L: python:uv, T: feature-request" | type: official
- [C9] renovate discussion #35704 "Add support for PEP 751 lockfiles (pylock.toml)" 仍开放，维护者 rarkins 回复 "PR welcome"，未实现 | src: https://github.com/renovatebot/renovate/discussions/35704 | quote: "After a contributor pointed out that pylock.toml includes a `created-by = \"pdm\"` attribute identifying the generating tool, rarkins responded: \"PR welcome.\"" | type: official
- [C10] renovate 官方 manager 列表页无 pylock/PEP 751，Python managers 仅列 pep621/pip-compile/pipenv/poetry 等 | src: https://docs.renovatebot.com/modules/manager/ | quote: "pep621, pep723, pip-compile, pip_requirements, pip_setup, pipenv, pixi, poetry, pyenv, runtime-version, setup-cfg" | type: official
- [C11] Hatch 1.17.0 (2026-05-31) history 页确认 `hatch env lock` 产 pylock.toml | src: https://hatch.pypa.io/latest/history/hatch/ | quote: "Add `hatch env lock` command to generate PEP 751 compliant lockfiles (`pylock.toml`) for environments" | type: official
- [C12] release-hatch-1170 博文（仓库 master 源文件，date 2026-05-30）原文确认命令输出 pylock.toml | src: https://raw.githubusercontent.com/pypa/hatch/master/docs/blog/posts/release-hatch-1170.md | quote: "$ hatch env lock\nLocking environment: default\nWrote lockfile: pylock.toml ... The `default` environment produces `pylock.toml`, while others follow the `pylock.<name>.toml` convention from PEP 751." | type: official
- [C13] hatch locker 文档确认内置 pip locker 的 apply_lock 是 no-op | src: https://hatch.pypa.io/latest/plugins/locker/ | quote: "`apply_lock` is a no-op — use UV for `locked` installs from a pylock today." | type: official
- [C14] pipenv pylock 文档页真实存在，写明 use_pylock 配置与优先级 | src: https://pipenv.pypa.io/en/stable/pylock.html | quote: "Pipenv supports PEP 751 pylock.toml files ... To enable this feature, add the following to your Pipfile: use_pylock = true ... whenever Pipenv updates the Pipfile.lock file (e.g., when running `pipenv lock`), it will also generate a pylock.toml file" | type: official

## conflicts
- 无实质冲突。hatch 博文渲染 URL（hatch.pypa.io/latest/ 与 /dev/ blog/posts/release-hatch-1170/）均 404，但源文件存在于 master 分支 docs/blog/posts/release-hatch-1170.md——站点未发布该页 vs 文件存在的差异，内容已按源文件核验。

## gaps
- uv CHANGELOG.md 未找到 `uv export --format pylock.toml` 的最初添加条目：该文件内嵌条目仅覆盖 0.12.x，0.6.x–0.11.x 为折叠指针；但 preview 页与 export 文档一致表明导出侧从未 gated。未能逐条核对 0.6.15–0.11.x 的 GitHub release notes。
- poetry issues 未逐条检索；以全仓库 code search（仅 CHANGELOG 命中）+ CLI 文档无 pylock 作为「不能读入」的佐证。
- dependabot issue 无维护者评论，「不支持」结论由 OPEN feature-request + 代码零命中推得，无官方明示拒绝声明。

## leads
- pipenv: 当 Pipfile.lock 与 pylock.toml 并存时优先 pylock.toml；另有 `pipenv pylock --generate/--validate/--from-pyproject` 子命令。
- uv 警告文案显示 `uv pip compile` 同样可产 pylock.toml（uv-lock/pylock_toml.rs）。
- hatch 1.17.0 还加了 `hatch dep lock`/`hatch lock`/`hatch dep sync` 与 `locked = true`/`lock-envs = true` 配置。
