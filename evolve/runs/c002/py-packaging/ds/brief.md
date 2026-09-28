# Brief：Python 包/项目管理工具对比与选型（2026-09）

## 任务
产出一份对照文档：uv、pip、Poetry、PDM、pixi/conda 五个工具有什么不同，新项目该怎么选。

## 读者
有 Python 经验的开发者/团队 lead，要在 2026 年给新项目（或迁移老项目）选工具。5 分钟建立认知 + 可查细节。

## 用户点名的疑点（成稿必须给结论）
1. PEP 751 标准锁文件 `pylock.toml` 是否已被 uv 和 pip 支持？（版本起点、import/export 还是原生）
2. Poetry 2 是否改用标准 `[project]` 表（PEP 621）？（旧 `tool.poetry` 表还能否用）

## 范围内
- 实体：uv、pip（+venv/virtualenv 生态位）、Poetry、PDM、pixi/conda（conda/mamba/micromamba 作为同族）
- 维度：锁文件、workspace/monorepo、Python 版本管理、构建后端、项目元数据标准、迁移、CI 缓存、私有源、脚本/任务运行、非 Python 依赖
- 相邻对象：hatch、rye（已被 uv 吸收？）、pip-tools、pyenv、deadsnakes、conda-forge、prefix.dev

## 范围外
- 包内部性能基准数值详测、所有构建后端大百科、Linux 发行版打包（apt/dnf）

## 完成标准
- taxonomy 给出分类轴 + 家族；对照矩阵覆盖上述维度；迁移/CI/私有源一节可操作
- ≤ 9000 字符；每条事实追 [n] 来源（官方文档优先）
