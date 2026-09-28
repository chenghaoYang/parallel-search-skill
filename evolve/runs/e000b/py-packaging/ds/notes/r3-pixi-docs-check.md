# r3-pixi-docs-check
question: 核实 pixi workspace 是稳定版已发布功能还是预览版/未发布功能。R2 工人发现文档在 `/dev/` 路径；需验证 `/latest/` 是否也有相同内容，以及 GitHub CHANGELOG 中是否确认版本发布。
checked: https://pixi.prefix.dev/latest/build/workspace/, https://pixi.prefix.dev/dev/build/workspace/, https://github.com/prefix-dev/pixi/releases

## claims
- [C1] pixi.prefix.dev/latest/build/workspace/ 页面存在（HTTP 200），包含完整的 workspace 文档内容 | src: https://pixi.prefix.dev/latest/build/workspace/ | quote: "Pixi enables developers to manage multiple packages within a single workspace" with support for root [workspace] table and member [package] tables | type: official
- [C2] workspace 功能在 pixi v0.75.0（2026-07-29）首次正式发布，标记为完整发布（非预发布） | src: https://github.com/prefix-dev/pixi/releases/tag/v0.75.0 | quote: "Immutable release. Only release title and notes can be modified." + release date 2026-07-29 | type: official
- [C3] v0.75.0 发布说明明确提及 `pixi publish` 功能，支持在依赖顺序中发布 workspace 包：`pixi publish now publishes every workspace package that opts in in dependency order` | src: https://github.com/prefix-dev/pixi/releases/tag/v0.75.0 | quote: "pixi publish now publishes every workspace package that opts in in dependency order" + requires package [package] name + publish = true declaration | type: official
- [C4] 最新稳定版为 v0.81.0（2026-09-15），距 v0.75.0 已发布 >1.5 个月，证实 workspace 功能已在多个后续版本中保留且持续演进 | src: https://github.com/prefix-dev/pixi/releases | quote: v0.81.0 release date 2026-09-15 | type: official

## conflicts
无冲突。/latest/ 文档与 /dev/ 文档内容一致，均为完整的 workspace 文档。

## gaps
无。

## leads
- pixi workspace 功能已随 v0.75.0（2026-07-29）进入稳定版发布，R2 报告中关于"/dev/ 预览路径"的时效性提醒现已过期，建议更新。

