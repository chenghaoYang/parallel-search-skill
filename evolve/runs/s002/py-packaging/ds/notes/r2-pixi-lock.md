# r2-pixi-lock
question: pixi.lock 的版本号到底是文档示例的 6，还是 changelog 说的 v7？现行文档或 changelog 有没有提到 pylock.toml / PEP 751？
checked: https://pixi.prefix.dev/latest/workspace/lock_file/, https://raw.githubusercontent.com/prefix-dev/pixi/main/docs/workspace/lock_file.md, https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md, https://github.com/prefix-dev/pixi/issues/3474

## claims
- [C1] 截至 2026-09-24，锁文件文档页（latest）示例仍是 `version: 6`，未改成 7。 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "version: 6" | type: official
- [C2] main 分支文档源码 docs/workspace/lock_file.md 同样仍是 `version: 6`（即不是渲染延迟，源文件就没改）。 | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/docs/workspace/lock_file.md | quote: "version: 6" | type: official
- [C3] 同页写明向后兼容方向：pixi 对 lock file 向后兼容、不向前兼容。 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "Pixi is backward compatible with the lock file, but not forward compatible." | type: official
- [C4] Changelog [0.68.0] - 2026-05-07 把 lock file 升到 v7，列为 Breaking change（PR #5607）。 | src: https://github.com/prefix-dev/pixi/blob/main/CHANGELOG.md | quote: "This release bump the lock file version to v7." / "- Lockfile-v7 by @baszalmstra in #5607" | type: official
- [C5] [0.71.0] - 2026-06-24 的条目证明 v7 已是现行格式（在处理旧文件迁移）。 | src: https://github.com/prefix-dev/pixi/blob/main/CHANGELOG.md | quote: "Resolve pre-v7 lockfiles for migrated platforms by @hunger" | type: official
- [C6] 对整份 CHANGELOG（5667 行全文 grep）只有 0.68.0 一处 lock-file 版本 bump；0.68.1→0.81.0（最新 2026-09-15）再无升级。注意 [0.77.0] 的 "pixi-build-api-version update to v7" 是构建 API 版本，与 lockfile 版本是两回事。 | src: https://github.com/prefix-dev/pixi/blob/main/CHANGELOG.md | quote: "Note that this is a `pixi-build-api-version` update to `v7`." | type: official
- [C7] 反例命中：官方仓库 issue #3474「PEP751 support」（open，label: enhancement/needs-design/python/uv，由维护者 tdejager 2025-04-01 提出）明确讨论 PEP 751。 | src: https://github.com/prefix-dev/pixi/issues/3474 | quote: "I believe we should start considering support for PEP 751, which introduces a standardized lock format for PyPI packages." | type: official
- [C8] 该 issue 提出把各环境的 PyPI 依赖导出为 PEP 751 格式、或切换为 TOML；目前仅是 ideation，无实现。 | src: https://github.com/prefix-dev/pixi/issues/3474 | quote: "We can easily export PyPI dependencies for each environment in this lock format... if we make the switch to TOML." | type: official

## conflicts
- 文档示例 vs changelog（R1 冲突仍在，双方都原样存在）：docs 页 quote "version: 6"（src: https://pixi.prefix.dev/latest/workspace/lock_file/，main 源码同）与 changelog quote "This release bump the lock file version to v7."（src: https://github.com/prefix-dev/pixi/blob/main/CHANGELOG.md，[0.68.0] - 2026-05-07）。文档示例疑似 stale，但按简令不裁决。
- R1「官方全文未提 pylock/PEP 751」被 C7 推翻：github.com/prefix-dev/pixi 的 issue #3474 标题即 "PEP751 support"。但该 issue 正文未出现字面 "pylock.toml"，只写 "PEP 751" 与 "this lock format"。

## gaps
- 字面文件名 "pylock.toml"：changelog 全文 grep 0 命中；pixi.prefix.dev 站内搜索 0 命中；issue #3474 正文只见 "PEP 751"/"switch to TOML"，未见 "pylock.toml" 字样。是否在任何官方页出现该文件名，未完全排除（issue 评论未逐条展开）。
- pixi.sh 域名下的页面未逐页排查 pylock/PEP 751（站点搜索覆盖 pixi.prefix.dev）。

## leads
- issue #3474 关联 rattler issue #1214（lock format 讨论）与 astral-sh/uv#12584（uv 不能以 pylock 为默认格式的限制）。
- 锁文件 satisfiability 实现代码：github.com/prefix-dev/pixi/blob/main/crates/pixi_core/src/lock_file/satisfiability/mod.rs（docs 页内链接）。
