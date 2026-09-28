# brief: Python 包/项目管理工具对比（2026-09）

读者：要给新项目选工具的 Python 开发者，听说过 PEP 751 和 Poetry 2。
成稿目标：5 分钟建立 taxonomy（哪个生态、哪层定位），再按矩阵查细节（锁文件、workspace、Python 版本、构建后端、迁移/CI/私有源）。

## 范围内
- 实体：uv、pip、Poetry、PDM、pixi、conda（+ leads 里的 hatch/rye/pyenv/pipenv 等只进对照或一句话）
- 维度：定位层、锁文件、元数据表、workspace/monorepo、Python 版本管理、构建后端、环境模型、操作性（迁移/CI 缓存/私有源）

## 范围外
- 各工具完整教程、benchmark 细节、编辑器集成细节

## 用户点名疑点（成稿必须有明确结论）
- Q1: PEP 751 (pylock.toml) 标准锁文件：uv 和 pip 是否已支持？什么版本/命令？
- Q2: Poetry 2 是否改用标准 [project] 表（PEP 621）？

## 完成标准
- grid 核心格 ✅/∅；一屏与疑点结论经过反证或终审；≤ 9000 字符。
