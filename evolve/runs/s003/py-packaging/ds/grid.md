# Taxonomy 网格 v0

状态：`✅` 一手来源 + 原文摘录；`⚠` 只有二手；`⚔` 来源冲突；`❓` 缺口；`∅` 官方未写（已定向查过）；`—` 不适用。

## 分类轴

- **轴 A 解析生态**：包从哪套索引解出来。PyPI / simple index，或 conda 频道（prefix）。这一轴解释「能不能装非 Python 的 .so / 系统库、锁文件长什么样」。
- **轴 B 管到哪一层**：只按需求装包；还是同时管项目元数据、锁、虚拟环境；还是管整个 prefix（含非 Python 依赖）。这一轴解释「新项目该不该用它当唯一工具」。
- **轴 C 标准对齐**（观察轴，不单独分家族）：PEP 621 `[project]`、PEP 517 `build-backend`、PEP 751 `pylock.toml`。用来解释家族内部的差异，而不是另分一组产品。

### 家族（v0）

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| PyPI 安装器 | pip | 只负责把已描述的依赖装进已有环境。不装 Python、不拥有项目生命周期。 |
| PyPI 项目管理器 | uv、Poetry、PDM | 读项目元数据、写锁、建虚拟环境、同步依赖。解析目标主要是 PyPI。 |
| conda/prefix 环境管理器 | pixi、conda | 以 prefix 为环境单位，索引是 conda 频道；可混入 PyPI。能管非 Python 依赖。 |

R1 不派 conda 专员工人（名额留给 scout）。conda 行保持 `❓`，等 scout 的 leads 决定 R2 是否单独立项。若 scout 证明 conda 与 pixi 在锁/版本/构建上不是同一层，就维持分行。

## 维度

每个维度回答一个问题。矩阵按此顺序排。

| 维度 | 这一列回答什么 |
|---|---|
| D1 锁 | 锁文件叫什么、哪条命令写出、是否 PEP 751 `pylock.toml`、锁不锁传递依赖与跨平台标记？ |
| D2 元数据 | 依赖和项目字段写在标准 `[project]`，还是工具私有表？旧表是否还读？ |
| D3 workspace | 一个仓库多包时，配置键叫什么、锁是一份还是多份、成员怎么互相引用？ |
| D4 Python 版本 | 谁安装解释器、钉在哪个字段、和虚拟环境的关系？ |
| D5 构建后端 | 默认 `build-backend` 是哪个包、能不能换、工具本身是不是后端？ |
| D6 依赖来源 | 默认索引/频道是什么、能否同时用 PyPI 和 conda？ |
| D7 私有源 | 私有索引怎么声明（字段名）、凭证从哪来？ |
| D8 CI 缓存 | 官方指出的缓存目录、action 或环境变量是什么？ |
| D9 迁移 | 官方从哪些旧工具迁入、命令或文档路径是什么？ |
| D10 日常命令 | 创建/同步环境的主命令是什么、是否自带虚拟环境或 prefix？ |

## 网格

行 = 实体。R0 全部 `❓`。

| 实体 | D1 锁 | D2 元数据 | D3 workspace | D4 Python | D5 后端 | D6 来源 | D7 私有源 | D8 CI | D9 迁移 | D10 命令 |
|---|---|---|---|---|---|---|---|---|---|---|
| pip | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| uv | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Poetry | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| PDM | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| pixi | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| conda | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

## 用户点名疑点（必须在成稿有结论）

| 疑点 | 落格 | 状态 |
|---|---|---|
| uv 是否支持 PEP 751 `pylock.toml` | uv × D1 | ❓ |
| pip 是否支持 PEP 751 `pylock.toml` | pip × D1 | ❓ |
| Poetry 2 是否改用标准 `[project]` | Poetry × D2 | ❓ |

## R1 派工（来源边界）

| 工人 | 实体/站点 | 要填的格 |
|---|---|---|
| r1-pip | pip.pypa.io + peps.python.org PEP 751 + packaging.python.org 中与 pip 直接相关的页 | pip 整行 |
| r1-uv | docs.astral.sh/uv | uv 整行 |
| r1-poetry | python-poetry.org/docs | Poetry 整行，D2 优先 |
| r1-pdm | pdm-project.org | PDM 整行 |
| r1-pixi | pixi.sh | pixi 整行 |
| r1-scout | 坑 + 网格外实体 | 只写 leads：conda 是否该分行、pip-tools/Hatch/Rye/mamba、用户会踩的坑、缺的维度 |

scout 的产出不直接进成稿。
