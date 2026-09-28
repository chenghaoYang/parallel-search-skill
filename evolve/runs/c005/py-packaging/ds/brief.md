# brief

## 任务
产出一份中文对照文档：现在 Python 包管理/项目管理工具（uv、pip、Poetry、PDM、pixi/conda）有何不同，新项目怎么选。

## 读者
会用 pip/venv 的 Python 开发者，听说过 uv 但不确定要不要换；5 分钟内建立选型认知，再按细节查。

## 用户点名疑点（成稿必须有结论）
1. PEP 751 标准锁文件 pylock.toml —— uv 是否已支持？pip 是否已支持？
2. Poetry 2 是否改用标准 `[project]` 表（PEP 621）？

## 范围内
- 实体：uv、pip（含 pip-tools/venv 生态位）、Poetry、PDM、pixi（含 conda 背景）。hatch/pyenv/mamba 等只作 leads/上下文。
- 维度：锁文件、workspace/monorepo、Python 版本管理、构建后端/发布、依赖声明格式、源与私有 index、CI 缓存、迁移路径、性能/实现语言、conda vs PyPI 生态位。
- 选型建议（新项目该选谁）。

## 范围外
- 深入 conda 科学计算栈细节；操作系统级包管理；容器镜像构建；各工具完整命令手册。

## 参数
rounds 3, workers 6, budget 9000 字符, dir ./ds, 终稿同时写 ./report.md

## 完成标准
- 每个核心格 ✅/∅ 或写明 ❓；疑点两条有结论；「一屏看懂」的边界主张已过反证；≤9000 字符。
