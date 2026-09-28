# 简报

读者：要开新 Python 项目、或从 pip / Poetry / conda 迁走的开发者。不是打包规范作者。

几分钟内要建立的认知：

1. 这些工具不是同一层的替代品。先按「解析生态」和「管到哪一层」分家族，再比锁文件、元数据、workspace、Python 版本、构建后端。
2. 新项目怎么选：只装 PyPI 包、要项目工作流、还是要 conda 频道和非 Python 依赖，三条路各对应谁。
3. 用户点名的疑点必须有明确结论（可以是「官方没写」或「截至日期、查过的页未见」）：
   - PEP 751 `pylock.toml`：uv 和 pip 是否都已经支持？支持到哪条命令、哪个版本？
   - Poetry 2 是否改用标准 `[project]` 表？旧 `[tool.poetry]` 还在不在？

## 范围

范围内：

- 种子：uv、pip、Poetry、PDM、pixi / conda。conda 与 pixi 在网格里分行（同生态、不同工具）。
- 维度：锁文件、项目元数据表、workspace/monorepo、Python 版本管理、构建后端、依赖来源、私有源、CI 缓存、从旧工具迁移、日常同步命令。
- 预期下游/变体（R0 先占位，R1 由 scout 记线索，不直接进成稿）：pip-tools、Hatch、Rye、pipx、mamba/micromamba、conda-lock、PEP 735 dependency-groups。

范围外：

- 某个库怎么打包上 PyPI 的逐步教程、setup.py 写法大全。
- 某个私有仓库（Artifactory/devpi/Nexus）的厂商配置手册，只记工具侧字段。
- 性能跑分、下载量排名、谁「更好」的主观榜。

## 完成标准

- 成稿按 `references/converge.md` 的骨架，`len(report.md) ≤ 9000`。
- 一屏看懂先回答两个疑点，并给出选型后果。
- 对照矩阵用原字段名；每格能追到笔记主张。
- 至少两轮扩展之后才终审。轮数上限 3，单轮工人上限 6。
- 最终文档同时写到工作目录 `ds/report.md` 和仓库根 `./report.md`。

## 种子词

uv、pip、Poetry、PDM、pixi、conda、PEP 751、pylock.toml、`[project]`、Poetry 2、lock、workspace、build-backend、私有源、CI cache。

## 参数

- rounds = 3
- workers = 6
- budget = 9000（`len()`，含来源节）
- dir = `./ds`
- 工人模型 = `swe-2-shim`（每次 spawn 显式传入）
- 检索 = 工人 `web_search` 找页、`web_fetch` 取原句。没有 pplx-safe。
- 主 agent 不搜索网页。
