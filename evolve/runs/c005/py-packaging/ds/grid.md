# grid v0

## 分类轴
- 轴1「管什么」：只管 PyPI 包（pip/uv/Poetry/PDM）vs 管 conda 生态 + 系统级依赖（pixi/conda）。
- 轴2「要不要自建生态位」：薄工具（pip 只管装，锁靠 pip-tools）vs 一体化项目管理器（uv/Poetry/PDM/pixi 管 env+lock+publish+python 本身）。

## 维度
- D1 锁文件：叫什么、是否自有格式、PEP 751 pylock.toml 支持度（export/import/默认）。
- D2 workspace/monorepo：官方 workspace 概念？路径依赖？多包根 lock？
- D3 Python 版本管理：能否自动下载/切换解释器？靠什么（python-build-standalone/conda 包/不管）？
- D4 构建后端与发布：默认 backend、build/publish 命令、是否支持 PEP 517 插件式后端。
- D5 依赖声明：pyproject [project] (PEP 621) 还是自有表？dependency-groups？
- D6 源与私有 index：index 配置方式、认证、多源优先级（含 uv/pixi 的 index 策略差异）。
- D7 CI/缓存：官方 cache 目录、CI 缓存做法、lockfile 校验命令。
- D8 迁移与互操作：从 requirements.txt/Pipfile/poetry.lock 迁入；导出 requirements.txt。
- D9 实现与性能：语言、相对 pip 的速度声明、venv 管理策略。

## 格子状态（行=实体 列=D1..D9）
| | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| uv | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| pip (+pip-tools) | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Poetry | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| PDM | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| pixi/conda | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

疑点：S1 pylock.toml 在 uv/pip 的支持状态；S2 Poetry 2 的 [project] 表。
