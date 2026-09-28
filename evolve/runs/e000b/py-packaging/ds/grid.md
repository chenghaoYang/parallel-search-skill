# Grid v2（R2 收束后）

状态：✅ 一手来源+原文摘录｜⚠ 只有二手/弱来源｜⚔ 冲突/存疑待核｜❓ 缺口｜∅ 官方查过确认未写｜— 不适用

## 分类轴（沿用 v0，R1+R2 均未推翻）
Family A｜PyPI 专用・一体化：uv, Poetry, PDM。Family B｜PyPI 专用・拼装式：pip(+pip-tools)。Family C｜跨语言・conda-forge：pixi, conda(+conda-lock)。

## 网格（与 v1 相比的变化用 → 标出）

| 实体 | D1 | D2 | D3 PEP751 | D4 | D5 | D6 workspace | D7 构建后端 | D8 | D9 | D10 CI缓存 | D11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| uv | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠ |
| pip | ✅ | ✅ | ✅ | — | ✅ | — | — | — | ✅ | ✅ | — |
| Poetry | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠ | ✅ | — | ✅ | ∅ | ⚠ |
| PDM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| pixi | ✅ | ✅ | ∅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❓ |
| conda | — | ✅ | — | ✅ | ✅ | — | — | ✅ | ✅ | ✅ | ⚠ |

变化说明（v1→v2）：Poetry D10「⚠弱来源」→「∅ R2 独立核实确认无官方action」；PDM D6 维持✅但日期(2026-06-23)待最终审稿spot check；pixi D6「❓」→「✅ 真monorepo」，但来源是 `/dev/` 预览文档，稳定版是否已发布待最终审稿核实；pixi D7「—」→「✅」setuptools默认/hatchling推荐；conda D2「⚔」→「✅」26.5实验性原生lock(EXPERIMENTAL标记)，R2 双源交叉确认。

resolved：46/54 (85%, v1) → 50/58 (86%, v2，含新增 pixi D7 列后分母变化)。剩余 ❓/⚠：uv D11、Poetry D6/D11、conda D11（均为「有但弱」，非空白缺口）、pixi D11（未查，低优先级）。

## R2 新增关键事实
- conda D2 最终结论：R1 引文是 AI 改写误导，R2 用 CHANGELOG（PR #15927 EXPERIMENTAL、#16086）+ 官方文档原句「Lockfile support is available in conda 26.5 and later」双重确认——**真实但实验性**，原生支持 `conda-lock.yaml` 和 `pixi.lock` 两种输出，conda-lock 项目 README 尚未提及此事。
- pixi D6：`pixi.prefix.dev/dev/build/workspace/` 描述了完整 monorepo 机制（根 `[workspace]` 表+子包各自 `[package]` 表、`{ workspace = true }` 源依赖、`pixi publish` 按依赖顺序发布）。**但 URL 路径是 `/dev/` 不是 `/latest/`**——pixi 文档站用 `/dev/` 表示预览/未发布文档，需要 R3 核实这个 multi-package workspace 是否已随稳定版发布，还是仍是 preview。
- pixi D7：无 `[build-system]` 时默认 setuptools；`pixi init --format pyproject` 生成 hatchling 配置；另有 pixi 专属 `pixi-build-python` 后端（次要）。
- PEP751 规范本身：文件名可以是 `pylock.toml` 或匹配 `pylock.<name>.toml`；规范包含 `environments` 字段，理论上支持单文件覆盖多环境（PDM/Poetry/uv "尝试"支持多环境锁）；规范明确不涉及 conda 等非 PyPI 生态；2024-07-24 创建，2025-03-31 Final，取代 PEP 665。
- Poetry/conda 官方 CI action：R2 独立核实仍是「无官方 action，只有社区/incubator 方案」，可从 ⚠ 升级为确定结论。
- 坑（第4节新素材）：uv 默认 `first-index` 策略（第一个含该包的 index 即止，防依赖混淆），pip 默认合并所有 index 选最优版本（`unsafe-best-match` 语义，更易被依赖混淆攻击）；但 uv 在内部 index 缺凭证时会静默回退到公共 PyPI（issue #9429，属已知漏洞而非文档特性）；uv 明确 **wontfix** 不支持直接读 poetry.lock/Pipfile.lock（issue #1804），迁移必须重新 resolve；GitHub Actions 缓存 key 若不含 OS 小版本号，跨 Ubuntu 20.04/22.04 会装到 ABI 不兼容的 wheel（setup-python issue #432）。

## R3 计划（1 worker：终审+定向核实合并）
不再新开话题，只核实+审稿：
1. 核实 pixi multi-package workspace 是否已在 `/latest/`（稳定版）文档出现，还是仍只在 `/dev/`。
2. 标准审稿流程：≥20 条抽查，`supported/weak/unsupported/contradicted` 判定，写 `audit.md`。
