# brief

读者：要开一个新的 Python 项目，或从 pip / requirements.txt、Poetry、conda 迁走的人。不是打包规范的作者。

成稿要让他在几分钟内建立的认知：

1. 这些工具不是同一层的替代品。先按「锁住并安装的是哪一种制品、工具拥不拥有解释器和项目元数据」分成家族，再比字段。
2. 新项目怎么选：纯 PyPI 库/应用、要不要 monorepo、要不要工具自己装 CPython、要不要 conda 二进制，四条就够落到一个家族。
3. 用户点名的两件事有明确结论：PEP 751 `pylock.toml` 在 uv 和 pip 上各自是什么状态；Poetry 2 是否改用标准 `[project]` 表。

范围内：

- 实体：pip、uv、Poetry、PDM、pixi、conda。
- 维度：锁文件、项目元数据表、workspace/monorepo、Python 版本、构建后端、环境形态、从旧工具迁入、CI 缓存、私有源、依赖分组。
- 标准只在「这些工具怎么实现它」的范围内：PEP 751、PEP 621、PEP 517、PEP 735（依赖组）。
- 选型相关的坑：迁移入口、CI 该缓存的目录、私有 index / channel 的配置位置。

范围外（进了 leads 也不进正文，除非它改变选型）：

- 解析器算法、性能跑分、安装耗时。
- 某个具体仓库的逐步迁移手册。
- pixi 的非 Python 语言细节（只保留「Python 项目会不会被带进 conda 前缀」）。
- 发布到 PyPI 的完整流程（只保留默认 build backend 的名字）。

种子词：uv、pip、Poetry、PDM、pixi / conda。

用户点名、成稿必须给结论的疑点：

- Q1：听说 Python 终于有标准锁文件了（PEP 751，`pylock.toml`）。uv 和 pip 是不是都已经支持？支持的是「生成」「安装」还是两者？从哪个版本起？
- Q2：Poetry 2 是不是也改用标准的 `[project]` 表了？`[tool.poetry]` 还要不要？

完成标准：

- `ds/report.md` 按 references/converge.md 的骨架重写，`len() ≤ 9000`。
- 同一份终稿抄到仓库根的 `./report.md`。
- Q1、Q2 在「一屏看懂」里各有一句带 `[n]` 的结论。
- 锁文件、workspace、Python 版本、构建后端四列没有静默留空：要么 ✅/⚠/⚔，要么 ∅（查过并写明查过的页）。
- 最后一轮是收束，不是扩展。

参数：rounds=3，workers=6，budget=9000，dir=./ds，工人模型 grok-4.7。没有 pplx-safe。检索只用 web_search 找页、web_fetch 取原句。日期锚：2026-09-24。
