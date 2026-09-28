# Grid v0 — 实体 × 维度

实体：uv, pip, Poetry, PDM, pixi/conda
（变体/相邻：hatch, rye, pipenv, pyenv, mise, conda-lock — 只在适用处一行提及）

## 维度（每列回答的问题）
- D1 元数据：项目依赖写在哪、什么格式？（[project] PEP 621 vs 自有表）
- D2 锁文件：锁文件叫什么、什么格式？支持 PEP 751 pylock.toml？
- D3 workspace/monorepo：有没有原生多包 workspace？怎么声明成员/路径依赖？
- D4 Python 版本管理：工具自己装/管 Python 解释器吗？
- D5 构建后端：用什么 build backend 打包？是否自有？
- D6 迁移：从 pip/requirements、Pipfile、setup.py、conda env.yml 等迁过来走什么命令？
- D7 CI/缓存：官方推荐的 CI 用法与缓存键？
- D8 私有源：私有 index/凭证怎么配（extra-index-url、keyring、auth）？
- D9 非 Python 依赖：能装非 PyPI 的系统/conda 包吗？

## 分类轴（v0）
谱系轴：PyPI/pip 系（uv, pip, Poetry, PDM）vs conda 系（pixi, conda）——包来源与能否管非 Python 依赖是最大分界。
副轴：全栈项目管理（锁+环境+构建+脚本：uv, Poetry, PDM, pixi）vs 纯安装器（pip）vs 环境层（conda 本体）。

## 网格状态
| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| uv | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| pip | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Poetry | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| PDM | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| pixi/conda | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

疑点格（必须结论）：uv/pip × PEP751；Poetry × [project] 表。
