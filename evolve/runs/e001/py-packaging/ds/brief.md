# Brief — Python 包管理/项目管理工具对比

## 任务
产出一份文档，帮读者在几分钟内看懂 2026 年 Python 包管理/项目管理工具的差异，并据此为新项目选型。

## 读者
会写 Python、但可能只用过 pip/requirements.txt、或旧版 Poetry/conda 的开发者；想知道新项目该选什么工具、老项目要不要迁移、CI 怎么配。

## 成稿要在几分钟内建立的认知
- 这些工具分几个家族，家族之间的根本差异是什么（不是功能罗列）
- 5 个核心工具在锁文件、workspace/monorepo、Python 版本管理、构建后端上具体怎么做（字段名、文件名）
- 迁移/CI缓存/私有源这些实操问题去哪查

## 范围内
uv、pip(+pip-tools)、Poetry(1.x→2.x)、PDM、pixi、conda(+mamba/libmamba)；PEP 517/518/621/751 这几个标准；构建后端（setuptools/hatchling/poetry-core/pdm-backend，附带提及，不单独展开成行）；CI 缓存（常见 CI 官方指引/action）；私有源（index/channel + 认证方式）。

## 范围外
Node/Rust/Go 等其他语言的包管理器；IDE 集成细节；rye（已并入 uv，提一句即可）；非常小众/实验性工具；conda-build/meta.yaml 的打包细节（只需说明它和 PyPI 构建后端概念的关系，不展开）。

## 种子词
uv, pip, Poetry, PDM, pixi, conda

## 用户点名疑点（成稿必须给出明确结论）
1. Python 是否已有标准锁文件 PEP 751（pylock.toml）？uv 和 pip 是否都已支持？
2. Poetry 2 是否已经改用标准的 `[project]` 表（PEP 621）？

## 完成标准
- 「一屏看懂」5–8 条结论覆盖以上两个疑点，且和后文矩阵一致
- 「Taxonomy」有分类轴（家族划分依据）和正交的维度清单
- 「对照矩阵」按维度给出 6 个核心实体的具体字段名/文件名/命令，不用「支持」「不支持」这种空泛词
- 覆盖迁移路径、CI 缓存、私有源三类额外必知问题
- 全文（含来源节）≤ 9000 字符；未决问题在末节列出，不進正文
