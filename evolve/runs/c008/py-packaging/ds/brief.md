# Brief：Python 包/项目管理工具横向对比

## 任务
产出文档帮用户了解 uv / pip / Poetry / PDM / pixi(+conda) 的差异，新项目怎么选。讲清：锁文件、workspace/monorepo、Python 版本管理、构建后端；以及迁移、CI 缓存、私有源等实战问题。建立 taxonomy。

## 读者
会 Python、用过其中一两种工具、要给新项目选型的开发者。中文成稿。

## 用户点名疑点（成稿必须有结论）
- Q1: PEP 751 pylock.toml 是不是标准锁文件？uv 和 pip 支持了吗？
- Q2: Poetry 2 是不是改用标准 [project] 表（PEP 621）了？

## 范围内
uv、pip、Poetry、PDM、pixi/conda 五族；相关标准（PEP 621/658/751/735/723）；下游工具只在「变体与适配层」提（Hatch、pipenv、rye、pyenv、conda/mamba）。

## 范围外
不教基础 pip 用法；不评测性能跑分细节；不覆盖打包发布全流程细节。

## 完成标准
- len(report.md) ≤ 9000 字符
- Q1/Q2 在「一屏看懂」给结论，进一屏的边界主张过反证
- 矩阵每格有 [n] 来源或 ❓/∅
- 最终写 ./ds/report.md 和 ./report.md

## 参数
rounds=3 workers=6 budget=9000 dir=./ds 截止 2026-09-25
