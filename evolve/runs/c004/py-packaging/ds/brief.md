# Brief: Python 包/项目管理工具对比

读者：要在 2026 年给新 Python 项目选工具的开发者。5 分钟内建立：有哪些家族、核心差异在哪、按场景怎么选。

## 范围内
- 实体：uv、pip、Poetry、PDM、pixi / conda（+ scout 发现的相邻实体：hatch、rye、pipenv、pyenv、mise、conda-lock 等，仅作变体/一行提及）
- 维度：锁文件（含 PEP 751 pylock.toml）、workspace/monorepo、Python 版本管理、构建后端、依赖/项目元数据格式、从老工具迁移、CI 缓存、私有源、非 Python 依赖
- 参数：rounds 3、workers 6/轮、budget 9000 字符、dir ./ds、成稿另写 ./report.md

## 用户点名疑点（成稿必须给结论）
1. PEP 751 / pylock.toml 是否已成标准，uv 和 pip 是否已支持
2. Poetry 2 是否改用标准 [project] 表（PEP 621）

## 范围外
- 各工具的完整命令教学；包发布流程细节；Linux 发行版打包
- 性能基准评测（只一句话量级提及）

## 完成标准
- 对照矩阵覆盖 5 实体 × 核心维度；每条事实有一手来源 [n]
- 「一屏看懂」含两个疑点的明确结论
- 未决事项单列一节
