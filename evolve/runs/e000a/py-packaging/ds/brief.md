# brief：Python 包管理/项目管理工具怎么选

## 任务复述
产出一份中文对照文档：帮一个要开始新项目、或想弄清现状的 Python 开发者，在 uv / pip / Poetry / PDM / pixi / conda
之间建立认知并做选型。核心讲清 5 个维度：锁文件（含 PEP 751 / pylock.toml 标准化现状）、workspace/monorepo、
Python 版本自身管理、构建后端；再覆盖迁移、CI 缓存、私有源等实操问题。

## 读者
会写 Python、但没系统跟踪过 2024–2026 packaging 生态变化的开发者/团队负责人。要在 5 分钟内知道「现在有哪些选项、
分别是什么定位、新项目选哪个」，然后能查具体字段名/命令。

## 范围内
- 实体：uv、pip（+ pip-tools）、Poetry（含 2.0）、PDM、pixi、conda（+ conda-lock）。
- 标准/规范：PEP 621（`[project]` 表）、PEP 517/518（构建后端接口）、PEP 751（`pylock.toml`）、PEP 508/440 视需要提及。
- 维度：锁文件格式与标准化程度、workspace/monorepo、Python 解释器版本管理、默认构建后端、依赖解析器特点、
  虚拟环境管理、私有源/认证、CI 缓存、从旧工具迁移的路径。
- 用户点名疑点（正文必须有明确结论，标注截至日期）：
  1. PEP 751 / `pylock.toml` 是否已定稿？uv、pip 是否已支持（读取/写出/两者）？
  2. Poetry 2.0 是否已改用标准 `[project]` 表（而非自定义 `[tool.poetry]` 描述元数据）？

## 范围外
- npm/cargo 等其他语言生态只做类比，不展开。
- 具体 CI 厂商 YAML 全文、公司内部镜像搭建细节。
- distutils/easy_install/virtualenv 历史只提一句背景。
- rye 已合并进 uv（Astral 收编），作为历史背景提及，不单独成行；hatch/flit/setuptools 只作为「构建后端」选项出现，不展开成实体行。

## 完成标准
- taxonomy 清楚（分类轴 + 家族），对照矩阵覆盖上述维度，字段名/命令/文件名写实名。
- 两条用户疑点在「一屏看懂」给出明确结论。
- 成稿 ≤ 9000 字符（含来源节），正文事实可追溯到 notes 里的主张。
