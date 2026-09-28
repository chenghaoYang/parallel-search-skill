# Grid v0：实体 × 维度

## 实体（行）
uv, pip(+venv), Poetry, PDM, pixi, conda（同族参照）, hatch（次要）, rye/pip-tools（历史/适配层，次要）

## 分类轴 v0
- **轴1 依赖生态**：纯 PyPI 包 vs conda 包（非 Python 系统依赖也管）→ pixi/conda 一族，其余一族
- **轴2 抽象层级**：项目级工作流（锁文件/虚拟环境/构建/发布一体）vs 组件级工具（只装包，虚拟环境/版本管理另配）
- **轴3 标准采用度**：PEP 621 `[project]` / PEP 751 `pylock.toml` 原生 vs 自有格式

## 维度（列）
| # | 维度 | 回答什么 |
|---|---|---|
| D1 | 锁文件格式 | 用什么锁文件？支持/产出 PEP 751 `pylock.toml` 吗（原生/导入导出/不支持）？ |
| D2 | workspace/monorepo | 单仓多包怎么组织？成员间 path 依赖、共享锁文件？ |
| D3 | Python 版本管理 | 自己装/切 Python 解释器吗？靠什么（uv python / pyenv / conda 包）？ |
| D4 | 构建后端 | 默认/捆绑的 PEP 517 后端是什么？发 sdist/wheel、可编辑安装怎么做？ |
| D5 | 项目元数据 | `[project]`(PEP 621) 还是自有表？requires-python、依赖写哪？ |
| D6 | 虚拟环境 | 自建 .venv？位置/激活方式？还是 conda env 前缀目录？ |
| D7 | 迁移路径 | 从 pip+requirements / conda env / poetry 1.x 迁过来的官方工具或文档？ |
| D8 | CI 缓存 | 官方 action/缓存键/全局缓存目录？离线/复现安装命令？ |
| D9 | 私有源 | 私有 index 配置语法、凭证（env var/keyring/netrc）、多源优先级？ |
| D10 | 脚本/任务 | 有没有 task runner / `xxx run`？hook？ |
| D11 | 非 Python 依赖 | 能不能装编译器/CUDA/系统库（conda 族强项）？ |

## 网格状态（收束时填）
（R1 后填充）
