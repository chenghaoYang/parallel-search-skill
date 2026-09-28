# r2-uv-counter
question: 三条 uv 主张（A: 项目接口继续只用 uv.lock；B: 0.6.15 是 preliminary pylock 起点、命令为 uv export / uv pip compile / uv pip install / uv pip sync；C: 现行文档仍演示 uv export -o pylock.toml 与 uv pip sync pylock.toml）在 0.6.15 之后的 release notes 或现行文档里有没有被改口？只找反例。
checked: https://docs.astral.sh/uv/concepts/projects/layout/, https://docs.astral.sh/uv/pip/compile/, https://docs.astral.sh/uv/concepts/preview/, https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md, https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.6.x.md, /0.7.x.md, /0.8.x.md, /0.9.x.md, /0.10.x.md, /0.11.x.md, /0.1.x.md–/0.5.x.md

## claims
- [C1] pylock.toml 支持仍是 preview：现行 preview 文档列出名为 `pylock` 的 preview feature，且说明会显示 preview 警告；不构成对 B 的改口，反而印证「仍 preliminary」 | src: https://docs.astral.sh/uv/concepts/preview/ | quote: "`pylock`: Allows installing from `pylock.toml` files. ... while `pylock.toml` support is in preview, you can use `uv pip install` with a `pylock.toml` file without additional configuration ... a warning will be displayed that the feature is in preview" | type: official
- [C2] 0.9.19 扩展了 pylock 支持到远程文件（uv pip 可从 URL 读 pylock.toml），是扩展不是删除 | src: https://github.com/astral-sh/uv/blob/main/changelogs/0.9.x.md | quote: "Support remote `pylock.toml` files ([#17119])" | type: official
- [C3] 0.7.0 起 uv 拒绝把任意 .toml 当 requirements.txt 处理，PEP 751 自定义名须形如 pylock.foo.toml；属收紧校验，未删命令 | src: https://github.com/astral-sh/uv/blob/main/changelogs/0.7.x.md | quote: "Reject non-PEP 751 TOML files in install, compile, and export commands ... If using PEP 751 lockfiles, use the standardized format for custom names instead, e.g., `pylock.foo.toml`." | type: official

## conflicts
- 无。三条主张均未被推翻：现行 layout 页（页脚 2026-07-21）仍逐字含 "uv will continue to use the `uv.lock` format within the project interface" 及 `uv export -o pylock.toml`/`uv pip sync pylock.toml` 示例；compile 页（页脚 2026-07-23）仍含 `uv pip sync pylock.toml`；0.1.x–0.6.14 changelog 零 pylock/PEP 751 提及（0.6.15 仍为首次）；0.6.16 至 0.12.18 无任何条目把 pylock 移入项目接口、宣布其稳定、或删除上述命令。

## gaps
- 未找到 A/B/C 的反例。查过的 release 范围：changelog 0.1.x 至 0.12.18（最早一条 pylock 提及为 0.6.15，GitHub tag 日期 2025-04-22；最晚一条为 0.12.18，Released on 2026-09-22）。0.6.15 之后所有 pylock 条目均为修复/校验/小扩展（如 0.8.x "Enforce `requires-python` in `pylock.toml`"、0.9.19 远程文件、0.11.x 校验 lock-version/requires-python、0.12.x hash/文件名校验）。
- preview 警告是否同样适用于 `uv export`/`uv pip compile` 写 pylock.toml，文档只描述了 install 场景，未逐条确认。
- 各 release 对应的 GitHub releases 页面未逐页打开；内容取自仓库 changelogs/*.md（与 release notes 同源）。

## leads
- 「pylock 在 uv 是否已稳定」：截至文档更新日 2026-07-24 仍是 preview feature（名为 `pylock`），可作为大题中 pylock 成熟度的证据。
