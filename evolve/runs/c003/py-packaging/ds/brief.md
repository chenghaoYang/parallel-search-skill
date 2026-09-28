# brief

## 任务
产出文档：帮用户了解当前 Python 包管理/项目管理工具（uv、pip、Poetry、PDM、pixi/conda）的差异，新项目怎么选。

## 读者
有一定 Python 经验、用过 pip/venv 或 Poetry 的开发者；可能听过 uv 但不确定要不要换。5 分钟内建立对比认知，再按需查细节。

## 用户点名的疑点（成稿必须给结论）
- Q1: PEP 751 标准锁文件（pylock.toml）是否已定稿？uv 和 pip 是否已支持？
- Q2: Poetry 2 是否已改用标准 [project] 表？

## 必须覆盖的维度
锁文件、workspace/monorepo、Python 版本管理、构建后端；另加迁移、CI 缓存、私有源。

## 范围内
uv、pip、Poetry、PDM、pixi（含 conda 生态对比）。下游实体如 hatch/hatchling、rye、conda-lock、poetry-plugin-export 可作线索/次要提及。

## 范围外
纯构建后端深度对比（setuptools internals）、打包成二进制（PyInstaller/pex）、Linux 发行版包管理、虚拟环境教学。

## 参数
rounds=3, workers=6, budget=9000 chars, dir=./ds, 终稿同时写 ./report.md。今天 2026-09-24。

## 完成标准
- taxonomy 有分类轴 + ≥8 维度；矩阵每格有 [n] 或 ❓/∅。
- Q1、Q2 在「一屏看懂」有明确结论。
- 迁移/CI 缓存/私有源各有一节或一条矩阵。
