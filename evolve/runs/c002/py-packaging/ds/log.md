# Log

## R0 定框架
- 实体：uv / pip / Poetry / PDM / pixi+conda 一族；hatch、rye、pip-tools 次要。
- 维度 D1–D11（锁文件、workspace、Python 版本、构建后端、元数据、venv、迁移、CI、私有源、脚本、非 Python 依赖）。
- 疑点：PEP 751 pylock.toml 的 uv/pip 支持现状；Poetry 2 的 [project] 表。
- R1 按来源边界拆：5 个实体工人（uv / pip+venv / Poetry / PDM / pixi+conda）+ 1 scout（坑与新实体线索）。共 6 spawn。
