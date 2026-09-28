# audit r3-audit
question: Verify 25 extracted claims from report.md against all research notes
checked: report.md, r1-pip.md, r1-uv.md, r1-poetry.md, r1-pdm.md, r1-pixi.md, r1-conda.md, r2-pip-pylock-verify.md, r2-ci-cache-poetry-pdm.md, r2-conda-verify.md

## audit results

supported | PEP 751 标准状态（2025-03-31 Final）| r1-pip [C3] | "Resolution: 31-Mar-2025"
supported | pip 25.1 实验性 `pip lock` 生成单平台锁文件 | r1-pip [C3] | "pip added experimental pip lock command in version 25.1 (April 2025)"
supported | pip 26.1 支持 `pip install -r pylock.toml` 读取（实验性）| r2-pip-pylock-verify [C1] | "Add experimental support to read requirements from standardized pylock.toml files"
supported | pip 26.2 添加 --uploaded-prior-to 支持（upload-time 字段）| r2-pip-pylock-verify [C2] | "Add support for ``pylock.toml`` ``upload-time`` field, so ``--uploaded-prior-to`` works"
supported | pip 26.2 添加 --only-final 标志支持 pylock.toml | r2-pip-pylock-verify [C3] | "Honor ``--only-final`` when sourcing requirements with ``-r pylock.toml``"
supported | uv v0.12.11+ 支持导出 pylock.toml（缺失哈希值生成）| r1-uv [C3-pep751-v0.12.11] | "Generate missing artifact hashes when exporting pylock.toml files"
supported | uv v0.12.17+ 校验 pylock.toml（wheel 文件名匹配）| r1-uv [C3-pep751-v0.12.17] | "Reject pylock.toml files whose wheel filenames do not match"
supported | uv PEP 751 支持处于 preview 阶段（导出+校验）| r1-uv [C3-pep751-status] | "PEP 751 支持目前处于 preview 阶段"
supported | Poetry 2.0（2025-01-05）支持标准 [project] 表 | r1-poetry [C2-1] | "respects the [project] section in pyproject.toml as specified by PEP 621"
supported | Poetry 2.3.0+ 支持导出 pylock.toml（via 插件）| r1-poetry [C3-3] | "Poetry 2.3.0+ exports to pylock.toml (PEP 751) via poetry-plugin-export"
supported | PDM v2.26+ 支持 pylock.toml（可选导出）| r1-pdm [C3b] | "Support pylock as alternative lock format and make it opt-in by config"
supported | pixi issue #3474 设计阶段（PEP 751）| r2-conda-verify [C4] | "issue #3474 'PEP751 support' 标记为 needs-design"
supported | pixi issue #3889 导出功能（已分配 @wolfv）| r2-conda-verify [C5] | "issue #3889 'Support export to pylock.toml' 已分配给 @wolfv"
supported | conda-lock 无 PEP 751 支持（社区沉默）| r2-conda-verify [C6] | "未见 'PEP 751'、'PEP-751'、'pylock' 任何提及"
weak | pip/uv/Poetry/PDM 只管 PyPI 生态 | r1-uv [C7-binary], r1-pip [C7] | 仅有 uv/pip 明确证据，Poetry/PDM 缺少直接原文
supported | pixi/conda 是跨语言环境管理器 | r1-pixi [C1], r1-conda [C1-a] | pixi: "cross-platform, multi-language"; conda: "any language"
supported | uv 用 Rust 实现 | r1-uv [C1] | "written in Rust"
supported | pixi 用 Rust 实现（rattler 解析器）| r1-pixi [C10] | "pixi 依赖解析器为 rattler（Rust 实现）"
supported | uv 性能：10-100x 快于 pip | r1-uv [C1-perf] | "10-100x faster than pip"
supported | pixi 性能：10x 快于 conda | r1-pixi [C10] | "pixi...比 conda 快 10 倍"
supported | Poetry 官方无 CI Action | r2-ci-cache-poetry-pdm [C2] | "Poetry 官方文档中没有推荐的 GitHub Action"
weak | pip 锁文件无私有格式 | r1-pip [C3]（隐含） | 支持来自于 pip 使用标准 pylock.toml，但未明确说"无私有格式"
supported | uv 锁文件：uv.lock（私有）| r1-uv [C3-lockfile] | "uv.lock（TOML 格式，uv 原生格式）"
supported | Poetry 锁文件：poetry.lock v2.0（私有）| r1-poetry [C3-1], [C3-2] | "Lock file format version 2.0 introduced in Poetry 1.3.0"
supported | PDM 锁文件：pdm.lock（私有）| r1-pdm [C3a] | "pdm.lock 格式为 TOML，用于锁定依赖版本"
supported | Poetry CI 缓存：仅给 cache-dir 路径 | r2-ci-cache-poetry-pdm [C1] | "仅在 Configuration 页面提供通用的 cache-dir 配置"
supported | PDM CI 缓存：setup-pdm Action + cache: true | r2-ci-cache-poetry-pdm [C4] | "cache: true 启用，缓存键默认基于 `pdm.lock` 文件"
supported | conda export --platform 可重复生成多平台 | r2-conda-verify [C1], [C2] | "repeat the flag to produce a single file covering every platform"
supported | Anaconda 官方条款：200+ 员工需付费 Business license | r2-conda-verify [C7] | "Users within organizations with 200+ employees/contractors require a paid Business license"

## summary statistics
- Total claims checked: 29
- supported: 27
- weak: 2
- unsupported: 0
- contradicted: 0

## weak claims detail
1. **pip/uv/Poetry/PDM 只管 PyPI 生态** — r1-uv [C7-binary] 和 r1-pip [C7] 仅提供 uv 和 pip 的明确表述，Poetry 和 PDM 缺少官方原文直接支撑。report.md 可考虑补充或限定为"至少 uv/pip"。
2. **pip 锁文件无私有格式** — r1-pip 笔记隐含支持（pip 使用标准 pylock.toml），但缺少显式的"无私有格式"表述。可从 NEWS.rst 中补充原句。

## key R2 corrections verified
✓ pip 26.1/26.2 pylock.toml 支持：r2-pip-pylock-verify.md 三条主张 [C1-C3] 全部 official，NEWS.rst 原句清晰。
✓ PDM setup-pdm Action 缓存机制：r2-ci-cache-poetry-pdm [C4-C5] 提供官方文档原句。
✓ Poetry 无 CI Action：r2-ci-cache-poetry-pdm [C1-C2] 明确官方状态。
✓ conda export --platform 多平台：r2-conda-verify [C1-C2] 有原文证据（可重复参数）。
✓ pixi issue 号 #3474/#3889 及分配：r2-conda-verify [C4-C5] 已确认。
✓ Anaconda ToS 200+ 员工原句：r2-conda-verify [C7] 有完整原文。

## leads
- 两条 weak 主张都可通过补充官方原文或限定范围升级为 supported
- report.md 矩阵和坑部分证据充分、准确度高
