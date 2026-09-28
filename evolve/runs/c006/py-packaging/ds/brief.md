# brief：Python 包/项目管理工具横评与新项目选型

## 任务
产出一份对照文档：uv / pip / Poetry / PDM / pixi（conda）现在的差异，新项目怎么选。

## 读者
有 Python 经验的开发者，听过部分工具名，要在新项目选型。目标：5 分钟建立 taxonomy，能按自己场景定位到家族，再查细节。

## 用户点名疑点（必须在成稿给明确结论）
- Q1: PEP 751 标准锁文件（pylock.toml）——uv 和 pip 是否已支持？
- Q2: Poetry 2 是否改用标准 [project] 表（PEP 621）？

## 范围内
- 5 个实体：uv、pip、Poetry、PDM、pixi/conda
- 维度：锁文件、依赖声明格式、workspace/monorepo、Python 版本管理、构建后端、虚拟环境、迁移、CI 缓存、私有源
- 相关坑：从老工具迁移、CI、私有源认证

## 范围外
- Hatch/flit/setuptools 纯构建后端的细节对比（只在构建后端维度提及）
- 包发布到 PyPI 的完整流程、betterer 工具（pipx、rye 已并入 uv 的历史细节）

## 参数
rounds=3, workers=6, budget=9000 chars, dir=./ds, report 同时写 ./report.md

## 完成标准
- taxonomy 有分类轴，矩阵格子带 [n] 引用
- Q1/Q2 有结论（哪怕是「官方未写」）
- 坑节覆盖：迁移、CI 缓存、私有源
