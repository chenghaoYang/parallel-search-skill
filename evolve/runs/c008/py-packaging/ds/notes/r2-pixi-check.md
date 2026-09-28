# r2-pixi-check
question: 反证/确认 pixi 三条边界主张 + 版本缺口（members 字段、pixi-build preview 状态、lock version、最新版本、pypi 入锁例外）
checked: https://pixi.prefix.dev/latest/reference/pixi_manifest/, https://pixi.prefix.dev/latest/build/workspace_dependencies/, https://pixi.prefix.dev/latest/workspace/lock_file/, https://github.com/prefix-dev/pixi/releases, https://api.github.com/repos/prefix-dev/pixi/releases/latest, https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md, https://raw.githubusercontent.com/conda/rattler/main/crates/rattler_lock/src/file_format_version.rs

## claims
- [C1] 主张A确认（无反例）：[workspace] 表无 members 字段。manifest reference 枚举的全部字段为 channels/platforms（必填）+ name/version/authors/description/license/license-file/readme/homepage/repository/documentation/conda-pypi-map/channel-priority/solve-strategy/requires-pixi/exclude-newer/build-variants/build-variants-files/dependencies/preview/target；全页唯一 "member" 出现是散文 "re-anchored per consuming member" | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "Preview flags are disabled by default and can be enabled by setting the `preview` field in the workspace manifest." | type: official
- [C2] 主张A确认：pixi monorepo 模型=每个成员包有自己的 pixi manifest，根 workspace 用 [workspace.dependencies] 里的 path/git 源条目引用（如 `shared-lib = { path = "packages/shared-lib" }`），消费方写 `{ workspace = true }` 继承；文档未提及任何成员发现/glob/显式成员清单机制 | src: https://pixi.prefix.dev/latest/build/workspace_dependencies/ | quote: "Relative `path` specs are resolved against the workspace manifest's directory" | type: official
- [C3] 主张B确认：截至最新文档（v0.81.0 时代），[package] 各表与 workspace.dependencies 中的 path/git 源条目仍需 preview=["pixi-build"] | src: https://pixi.prefix.dev/latest/build/workspace_dependencies/ | quote: "require the `pixi-build` preview, as do source (`path`/`git`) entries in the pool itself" | type: official
- [C4] 主张B细化：v0.73.0（2026-07-15）起环境依赖表（[dependencies]/[feature.*.dependencies]）用 `{ workspace = true }` 继承 [workspace.dependencies] 不再需要 preview；仅 package 依赖表仍需 | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md | quote: "Until now, `{ workspace = true }` only worked in the package dependency tables and required the `pixi-build` preview. With this release, the environment tables can inherit from `[workspace.dependencies]` as well, no preview needed." | type: official
- [C5] 主张B确认：changelog 中 pixi-build 仍被称为 preview（v0.62.0, 2025-12-17："Breaking change for `pixi-build` preview"）；全 changelog 无 pixi-build 转正式的条目 | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md | quote: "This release removes the input hashes from the lockfile for source dependencies" | type: official
- [C6] 主张C：官方 lock_file 文档示例仍写 `version: 6`，含义为锁文件格式版本，"to ensure that the lock file is compatible with the local version of pixi"；"Pixi is backward compatible with the lock file, but not forward compatible" | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "The lock file also has a version number, this is to ensure that the lock file is compatible with the local version of pixi." | type: official
- [C7] 主张C：pixi v0.68.0（2026-05-07）changelog 宣布 bump lock file 到 v7——"Reproducible source package builds / Less lockfile churn / More portable lockfiles: no absolute, machine-specific paths"；故当前 pixi（≥0.68.0）实际写 version: 7 | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/CHANGELOG.md | quote: "This release bump the lock file version to v7." | type: official
- [C8] 主张C佐证：rattler_lock FileFormatVersion 枚举 V7=7 "Allow for relative file paths in URLs"，LATEST=V7；V6=6 为 "fields are derived from the location and the `kind` is merged with the location" | src: https://raw.githubusercontent.com/conda/rattler/main/crates/rattler_lock/src/file_format_version.rs | quote: "pub const LATEST: Self = FileFormatVersion::V7;" | type: official
- [C9] 主张D：最新 pixi 版本 v0.81.0，发布于 2026-09-15（GitHub API tag_name=v0.81.0, published_at=2026-09-15T15:07:21Z，releases 页标 Latest）；前一版 v0.80.0 为 2026-09-07 | src: https://api.github.com/repos/prefix-dev/pixi/releases/latest | quote: "\"tag_name\": \"v0.81.0\"" | type: official
- [C10] 主张E确认（无例外）：lock_file 页声明锁内容须 "compatible with the requirements in the manifest file, for both `conda` and `pypi` packages"，且 pypi editable 包的 hashes 也记录入锁；该页未提任何 pypi-dependencies 不入 pixi.lock 的例外 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "All hashes for the `pypi` editable packages are correct" | type: official

## conflicts
- 文档示例过时：lock_file 文档示例 `version: 6`（https://pixi.prefix.dev/latest/workspace/lock_file/）与 changelog v0.68.0 "bump the lock file version to v7" + rattler LATEST=V7 矛盾。当前 pixi ≥0.68.0 实际产出 version: 7，文档代码块未更新。
- 细化（非冲突）：r1 笔记 C11 写 workspace.dependencies "需 preview=[pixi-build]" 过宽——v0.73.0 起环境表继承免 preview，仅 package 表与 path/git 源条目仍需。

## gaps
- lock_file 文档示例 version: 6 何时更新未查（文档站滞后于 v0.68.0+）。
- pixi 是否在任何页提及成员包"发现"机制（如自动扫描子目录 manifest）：manifest reference 与 workspace_dependencies 两页均无，未全站搜。
- detached environments 的锁模型是否与 workspace pixi.lock 分离（涉及 E 的边界）未查。

## leads
- `pixi workspace preview` 子命令（changelog v0.7x 新增）暗示 preview flag 有 CLI 管理面，转正路线可追踪。
- detached environments 可能是 pypi/conda 不共享 pixi.lock 的真实例外场景，值得下轮查。
