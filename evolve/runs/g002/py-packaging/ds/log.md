# 日志

## R0

观察：任务要在 9000 字以内比较 uv、pip、Poetry、PDM、pixi/conda，并回答 PEP 751 与 Poetry 2 `[project]` 两个疑点。还没有笔记。

决策：taxonomy v0 用两根轴——包宇宙（PyPI vs conda）和职责（只安装 vs 拥有项目）。维度 D1–D9 覆盖锁文件、workspace、CPython、构建后端、依赖组、迁移、CI、私有源。conda 先占一行，但是否并列由 scout 决定。候选 pip-tools、Hatch、Rye、mamba、conda-lock 不入格。

动作：R1 按官方文档站派 6 个工人（5 个实体 + 1 个 scout）。

预计 spawn：6。
