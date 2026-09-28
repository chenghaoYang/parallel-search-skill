# R0 brief

读者：要开新 Python 项目、或从 pip / Poetry / conda 迁走的开发者。听说过「标准锁文件」和 Poetry 2，但分不清 uv、pip、Poetry、PDM、pixi/conda 各管哪一层。

成稿要让他在几分钟内建立的认知：

1. 这些工具不是同一类东西的五个品牌，而是三条职责线（只装包 / 管 Python 项目 / 管 conda 级环境）。
2. 锁文件、`[project]` 表、workspace、解释器、构建后端上的具体差异（用官方字段名和命令，不意译）。
3. 点名疑点有明确结论：PEP 751 `pylock.toml` 上 uv 和 pip 各自支持到哪一步；Poetry 2 是否改用标准 `[project]` 表。
4. 迁移、CI 缓存、私有源怎么配，以及选错家族会踩的坑。

范围内：uv、pip、Poetry、PDM、pixi，以及和 pixi 成对出现的 conda（classic / mamba / micromamba 只作为对照，不展开每个发行版）。维度见 `grid.md`。相关但次要的变体（pip-tools、Hatch、Rye、pipenv、conda-lock）只在 scout 证实它们会改变选型时才升格。

范围外：具体业务项目的重构方案、某个私有索引的运维手册、性能跑分、非官方博客里的偏好结论（除非用来发现线索）。

种子词：uv、pip、Poetry、PDM、pixi / conda。

用户点名的疑点（成稿第 0 节必须给结论，哪怕结论是「官方没写」）：

- Q1：PEP 751（`pylock.toml`）uv 和 pip 是否都已经支持？支持的是读、写、还是安装？
- Q2：Poetry 2 是否改用标准 `[project]` 表？

完成标准：

- taxonomy 能解释矩阵里的大部分差异，而不是工具名罗列。
- 每个核心格子是 ✅、∅ 或有原因的 ❓/⚔；具体事实能追到笔记主张。
- `len(report.md) ≤ 9000`，且后一轮不得长过前一轮却没有删压缩。
- 工作目录 `./ds`；最终文档同时写到 `./report.md`。

参数：rounds=3，workers=6，budget=9000。检索只许工人用 web_search 找页、web_fetch 取原句。没有 pplx-safe。主 agent 不搜网页。
