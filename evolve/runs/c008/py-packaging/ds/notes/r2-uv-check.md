# r2-uv-check
question: 反证/确认 uv 三条边界主张（项目接口是否只消费 uv.lock、uv 是否默认 pylock.toml、最新版本号）+ uv_build 首次引入版本
checked: https://docs.astral.sh/uv/concepts/projects/layout/, https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md, https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.7.x.md, https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.6.x.md, https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.5.x.md, https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.4.x.md, https://docs.astral.sh/uv/reference/cli/, https://docs.astral.sh/uv/reference/settings/, https://api.github.com/repos/astral-sh/uv/releases/tags/0.5.0, .../0.6.5, .../0.7.19, .../0.12.19

## claims
- [C1] uv 最新 release 为 0.12.19，changelog 标注 Released on 2026-09-24（GitHub release published_at 2026-09-25T00:33Z，时区差）| src: https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md | quote: "## 0.12.19 Released on 2026-09-24." | type: official
- [C2] 项目接口仍只用 uv.lock（当前文档原文，2026-09-25 抓取）| src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv will continue to use the `uv.lock` format within the project interface." | type: official
- [C3] pylock.toml 无法表达 uv 全部功能（同页）| src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "Some of uv's functionality cannot be expressed in the `pylock.toml` format" | type: official
- [C4] `uv lock` 无 --format / 不接受 pylock.toml；只读写 uv.lock（CLI reference uv lock 段内 --format 出现 0 次、pylock 出现 0 次）| src: https://docs.astral.sh/uv/reference/cli/ | quote: "If the project lockfile ( uv.lock ) does not exist, it will be created." | type: official
- [C5] `uv sync` 段无 pylock / --format 选项（section 全文 grep 0 命中）| src: https://docs.astral.sh/uv/reference/cli/ | quote: (negation verified by full-section grep: pylock=0, --format=0 in "Usage uv sync" section) | type: official
- [C6] `uv export` 把 uv.lock 导出为 pylock.toml（PEP 751）：pylock 是导出目标 | src: https://docs.astral.sh/uv/reference/cli/ | quote: "Export the project's lockfile to an alternate format. At present, requirements.txt , pylock.toml (PEP 751) and CycloneDX v1.5 JSON output formats are supported." | type: official
- [C7] `uv run --with-requirements` 接受 pylock.toml 文件作为临时叠加依赖输入（非项目锁文件）——字面推翻「uv run 不消费 pylock.toml」| src: https://docs.astral.sh/uv/reference/cli/ | quote: "Run with the packages listed in the given files. The following formats are supported: requirements.txt , .py files with inline metadata, and pylock.toml . The same environment semantics as --with apply." | type: official
- [C8] `uv pip compile`/`uv pip sync` 读写 pylock.toml | src: https://docs.astral.sh/uv/reference/cli/ | quote: "uv pip compile Compile a requirements.in file to a requirements.txt or pylock.toml file; uv pip sync Sync an environment with a requirements.txt or pylock.toml file" | type: official
- [C9] settings reference 无任何 pylock 或 lock-format 设置项（全文 grep: pylock=0, lock-format=0）——项目锁格式不可配置 | src: https://docs.astral.sh/uv/reference/settings/ | quote: (negation verified by full-page grep) | type: official
- [C10] 0.12.x changelog 中全部 pylock 条目均为 uv pip/导出路径的校验加固（0.12.0 "Reject invalid pylock.toml files"、0.12.11 生成/校验 artifact hashes、0.12.16 archive sizes、0.12.17 wheel filename 校验），无任何条目让项目接口读/写 pylock.toml | src: https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md | quote: "**Reject invalid `pylock.toml` files and artifacts**" | type: official
- [C11] uv 自有 build backend 最早在 0.5.0（2024-11-07）以 experimental/preview 引入——比简报假设的 0.7.x 更早 | src: https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.5.x.md | quote: "Add support for building basic source distributions with the experimental uv build backend ([#8886])" （位于 "## 0.5.0" → "### Preview features" 下）| type: official
- [C12] `uv_build` 成为独立包名在 0.6.5（2025-03-06）| src: https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.6.x.md | quote: "Move the uv build backend into a separate, minimal `uv_build` package" | type: official
- [C13] uv build backend 在 0.7.19（2025-07-02）宣布 stable | src: https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.7.x.md | quote: "The **[uv build backend](https://docs.astral.sh/uv/concepts/build-backend/) is now stable**, and considered ready for production use." | type: official
- [C14] 0.7.3 起 build backend preview 默认开启 | src: https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.7.x.md | quote: "Build backend: Make preview default and add configuration docs ([#12804])" | type: official
- [C15] 0.12.0 起 `uv init` 默认使用 uv_build | src: https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md | quote: "Now, `uv init example` defines a `[build-system]` using `uv_build`, places application source code in `src/example`" | type: official

## conflicts
- 主张A 的强读法「uv sync/uv run/uv lock 不消费 pylock.toml」被 C7 部分推翻：`uv run --with-requirements`（及 uvx/uv tool install/upgrade 同名选项）接受 pylock.toml 作为叠加依赖文件。但项目锁文件本身仍是 uv.lock（C2/C4/C5/C9），pylock.toml 仅作 ephemeral 输入，不写回项目锁。弱读法（项目锁格式=uv.lock）成立。

## gaps
- 主张B 只确认了 uv 侧；pip/poetry/pdm/hatch 等其他 PyPI 系工具未查（超范围）。
- 0.12.x 之前各 minor（0.8–0.11）changelog 未逐条 grep pylock；但当前 live 文档（C2/C4/C5/C9）已足以否定「0.12+ 引入项目接口 pylock」。

## leads
- `uv pip install/uninstall` 也接受 pylock.toml 作 -r 输入，且 `--group` 可直接从 pylock.toml 读依赖组。
- 0.12.0 破坏性变更含 pylock 严格校验（文件名须为 pylock.toml 或单名变体 pylock.dev.toml）。
