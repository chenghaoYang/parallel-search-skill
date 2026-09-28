# 简报

任务：帮用户看清现在 Python 的包管理 / 项目管理工具有什么不同，新项目该怎么选。

读者：会用 pip、听说过 Poetry / uv / conda，但分不清「安装器、项目管理器、conda 求解器」的人。要在几分钟内建立分类，再按表查锁文件、workspace、Python 版本、构建后端。

截至日期：调研日 2026-09-24。成稿里的版本结论必须带笔记里的文档版本或页面日期。

## 成稿要让读者建立的认知

1. 这些工具不是同一层的替代品。先按「项目真相放在哪」分家族，再比命令。
2. 新项目的默认选择能用一张决策表说完，例外（conda 科学栈、已有 Poetry 仓库、只往现成环境里装包）单独写。
3. 用户点名的两个疑点必须有明确结论（支持 / 不支持 / 官方没写），写在「一屏看懂」。

## 用户点名的疑点（成稿必须给结论）

- D1：PEP 751 的标准锁文件 `pylock.toml`，uv 和 pip 是不是都已经支持（读、写分别说清）？
- D2：Poetry 2 是不是改用标准的 `[project]` 表了？`[tool.poetry]` 还剩什么？

## 范围内

实体：uv、pip、Poetry、PDM、pixi。conda 作为种子里的相邻对象，先占一行，R1 由 scout 判断要不要升成独立对照实体。

维度（见 grid.md）：锁文件、项目元数据表、workspace/monorepo、Python 版本管理、构建后端、依赖宇宙、从旧工具迁移、CI 缓存、私有源。

## 范围外

- 手把手初始化一个具体项目、性能跑分、解析器算法内部、安全公告清单、非 Python 语言的打包细节（除非解释 pixi/conda 家族所必需）。
- hatch、rye、pip-tools、pipenv、mamba 只在 scout 的 leads 里出现；未升格前不进成稿正文。

## 完成标准

- `ds/report.md` 按 references/converge.md 的骨架写成，`len()` ≤ 9000。
- 同一份成稿复制到工作区根目录 `./report.md`。
- 每个具体事实能追到笔记主张；没来源的只出现在「未决」。
- 至少两轮扩展，至多三轮；最后一轮之后有终审，终审后再收束一次。

## 参数

- rounds 3，workers 6，budget 9000
- 工作目录 `./ds`
- 工人模型 swe-2-shim；检索只用 web_search + web_fetch；没有 pplx-safe
