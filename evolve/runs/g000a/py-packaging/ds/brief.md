# brief

读者：要开新 Python 项目，或从 pip / Poetry / conda 迁走的开发者。几分钟内要能选出工具，并知道锁文件、workspace、Python 版本、构建后端差在哪。

成稿要建立的认知：

1. 这些工具不是同一层的替代品。先按「包从哪个宇宙来」和「替你管到哪一层」分家族，再比字段。
2. 用户点名的两件事必须有明确结论：PEP 751 `pylock.toml`，uv 和 pip 各自是否能读、能写；Poetry 2 是否改用标准 `[project]` 表。
3. 对照表用官方原名（文件名、表名、命令、环境变量），方便直接去文档核对。

## 范围内

- 实体：uv、pip、Poetry、PDM、pixi。conda 与种子写在一起，若它和 pixi 不是同一产品，单列一行（R1 由 scout 判断，R2 再填）。
- 维度：元数据表、锁文件（含 PEP 751）、workspace/monorepo、Python 版本管理、构建后端、环境落点、依赖组、私有源、CI 缓存、官方迁移入口。
- 用户还需要知道的：从旧工具迁入、CI 缓存、私有源，以及 scout 找到的高频坑。

## 范围外

- 某个包的发布步骤教程、PyPI 可信发布（trusted publishing）细节、漏洞扫描。
- 性能跑分、IDE 插件、与 Docker 基础镜像的搭配，除非官方文档把它写成该工具的既定用法。
- conda-forge 配方怎么写、rattler-build 的完整语法。只记录它和 pixi 的关系。

## 种子词

uv、pip、Poetry、PDM、pixi / conda、PEP 751、pylock.toml、PEP 621、`[project]`、Poetry 2。

## 用户点名的疑点（成稿必须给结论）

1. Python 是否有了标准锁文件（PEP 751，`pylock.toml`）？uv 和 pip 是否都已经支持？支持的是读、写，还是两者？从哪个版本起？
2. Poetry 2 是否改用标准 `[project]` 表？`[tool.poetry]` 还剩什么？

## 完成标准

- taxonomy 能解释矩阵里的大部分差异。
- 五个种子实体在十个维度上有一手来源、官方明确未写（∅），或标明冲突。
- 两个疑点写在「一屏看懂」，且每条都能追到笔记主张。
- `ds/report.md` 字符数 `len()` ≤ 9000。最终同时写到仓库根目录 `report.md`。
- 文档详细但能快速扫完：结论 → 家族 → 表 → 坑 → 未决。

## 参数

- rounds 3，workers 6，budget 9000
- dir `./ds`
- 工人模型 grok-4.7；检索只用 web_search + web_fetch；没有 pplx-safe
- 主 agent 不搜网页
