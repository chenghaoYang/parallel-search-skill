# Log

## R0 定框架
观察：无（首轮）。
动作：写 brief.md（读者=选型开发者，Q1=PEP751 支持，Q2=Poetry2 [project] 表）；grid.md taxonomy v0（3 家族 × 11 维度，6 实体行）。
预计 spawn：R1 = 6（一实体一工人，覆盖 uv/pip+pip-tools/Poetry/PDM/pixi/conda）。

## R1 扩展（6 spawn）
6 个工人全部成功返回，无重派。151 条主张（official 143 / secondary 8），3 处 conflicts 字段非空但经检查均为「工人自己发现的表内差异」而非真冲突（例如 Poetry [project]/[tool.poetry] 共存），已在正文中说明，不算待核冲突。

## R1 收束
观察：notes_lint 显示 4 份笔记超 8000 字符软上限（conda 10539、pixi 8617、poetry 9757、uv 8991）但内容仍可用，未触发重派。grid 网格 54 格中 46 格可定论（✅+∅=85%），5 格 ⚠ 弱来源，1 格 ⚔ 冲突，2 格 ❓ 缺口。
动作：grid.md → v1（见上），report.md 从零重写（6467 字符，budget 9000，余量约 2500 给 R2 发现和坑清单）。taxonomy 三家族划分未被数据推翻，未换轴。Hatch 未被任何工人标记为必需单列行，维持不单列决定。
发现的关键待核项：
1. ⚔ conda「26.5+ 原生锁文件」——措辞与常识（conda 无原生锁，靠 conda-lock）冲突，未采信入 0/2 节，需核实原句版本号（对应观察表「与常识相反、影响大→先复核」规则）。
2. ❓ pixi D6 workspace 是否=monorepo 多子包，还是仅项目清单根改名，官方文档未给出清晰例子。
3. PEP751 规范本身尚无工人直接摘录 peps.python.org 原文用于第 3 节写作（目前第 3 节结论是从 uv/pip 笔记间接转述 PEP751 的 Final 日期，未摘录规范定义本身的关键属性）。
4. Poetry/conda 官方 CI action 存在性证据偏弱（二手/间接），值得一次直接确认搜索。
5. 第 4 节「用户需要知道的坑」内容单薄，R1 工人均聚焦「有什么」，缺「真实踩坑」素材（迁移转换、私有源多 index 解析顺序、lock 跨工具不可转换等）。

## R2 计划（4 workers，定向补缺，不重扫全表）
1. r2-conda-lock-verify — 核实 conda D2 冲突（docs.conda.io 原页 + conda 官方 changelog + conda-lock README 对自身定位的描述）。
2. r2-pixi-workspace — 核实 pixi D6（monorepo 多子包 vs 项目根改名），顺带确认 D3(PEP751)确系未提及、D7(Python包构建后端推荐)。
3. r2-pep751-spec — 直接读 peps.python.org/pep-0751/ 摘录规范本身定义（解决什么问题、是否支持多平台/多环境单文件、与 requirements.txt/其他锁格式关系），并确认 Poetry/conda 是否真无官方 CI action。
4. r2-gotchas — 定向搜「migrate pip to uv gotchas」「poetry.lock to uv.lock」「private index resolution order pip vs uv」「conda to pixi migration」等，为第 4 节找具体踩坑案例+官方/一手证据。
预计 spawn：4（R2 起更少更窄，符合「不许为了凑轮数凑人数」）。

## R2 扩展（4 spawn）
4 个工人全部成功返回，无重派。33 条新主张（official 30 / secondary 3）。关键结果：
- conda「26.5 原生锁」claim 被 R2 用 CHANGELOG(PR #15927/#16086) + 官方文档原句双源交叉确认为真，但为 EXPERIMENTAL；R1 引文本身有 AI 改写失真（"Modern conda supports..." 不是原文），R2 已用准确原句替换。
- pixi workspace 被确认是真正的多子包 monorepo（根`[workspace]`+子包`[package]`+`{workspace=true}`源依赖+`pixi publish`按序发布），但证据来自 `pixi.prefix.dev/dev/...`（预览文档路径），不是 `/latest/`（稳定版），需要终审核实是否已发布。
- PEP751 规范原文摘录到位：文件名规则、单文件多环境理论支持、明确排除 conda 生态、精确日期链（2024-07-24 创建→2025-03-31 Final→取代PEP665）。
- Poetry/conda 官方 CI action 独立复核仍是「确认没有」，⚠ 升级为 ∅。
- gotchas 工人拿到 10 条高质量主张：uv/pip 私有源解析策略差异（first-index vs 合并选优，依赖混淆安全含义）+ uv 缺凭证静默回退 PyPI 的已知漏洞(issue #9429)；uv 明确 wontfix 不支持导入 poetry.lock/Pipfile.lock(issue #1804)；GH Actions 缓存 key 不含 OS 小版本号会跨 Ubuntu 版本装错 ABI 不兼容 wheel(issue #432)。

## R2 收束
观察：notes_lint 全部干净（0 空笔记、0 超长、0 缺 src/quote 除 2 处引用型 quote 字段属预期格式）。grid v1→v2：46/54(85%)→50/58(86%)（分母因新增 pixi D7 列变化）。四个待核项全部得到实质性推进：3 个完全解决(conda D2、Poetry/conda D10、PEP751 spec)，1 个部分解决但引出新的更精确问题(pixi D6 从"是否monorepo"变成"monorepo机制是否已stable发布")。
动作：report.md 从零重写（7686 字符，budget 9000，余量 ~1300）。taxonomy 未变。第 0 节新增"私有源默认策略不同"结论性 bullet（原为第4节独有内容，因其安全含义重要，提升到一屏看懂）；第 4 节从 4 条单薄坑扩到 5 条有一手来源的具体坑；第 3 节补入 PEP751 规范原文细节；第 5 节从 5 条缩到 4 条，多数旧疑点已解决或降级为"时效性提醒"而非"未知"。

## 观察 → R3 决策
观察：核心格子（D1-D5, D8-D10 六工具）已基本 ✅/∅，仅剩 1 个中等重要的时效性问题（pixi workspace 是否已 stable 发布，直接影响第 0 节 workspace bullet 的措辞confidence）和常规终审（迄今未做任何抽查校对）。按观察表规则：「核心格子都是✅/∅，或上一轮几乎没改变网格」→ 终审；同时命中「与常识相反/影响大的主张，先复核」（pixi dev-docs 这条本质是同一类风险）。rounds 参数=3，这是最后一轮扩展，不能再开新话题。
动作：R3 派 1 个 worker，合并「pixi workspace stable-vs-dev 核实」+「标准终审（≥20条抽查）」，因为终审工人本来就要读 report.md 全文、可以顺手多做这一次定向 fetch，没必要为一件事单独占用一个 spawn。
预计 spawn：1。

## R3 终审（1 spawn）
worker 完成两项任务：(1) 核实 pixi workspace/monorepo 机制的发布状态——**结论：已于 v0.75.0（2026-07-29）进入稳定版**，`/latest/` 路径文档已存在，最新稳定版 v0.81.0（2026-09-15）仍保留该功能，R2 时"预览路径"的说法在当时准确、现已过期。(2) 对 report.md 正文抽查 34 条具体主张：30 supported / 2 weak / 1 unsupported / 0 contradicted。

## 终审后修正（不再 spawn，直接编辑 report.md）
- 删除 unsupported 的"uv 速度最快"营销式断言（A1），改写为中性可核实的"Rust 实现"。
- pixi workspace 相关三处（第0节、第2节矩阵、来源[19]）从"待核/预览路径"更新为"已确认稳定版功能，v0.75.0起"，源URL从`/dev/`换成`/latest/`+release notes。
- 第5节重写：加入终审汇总数字（34条抽查/30 supported/0 contradicted），weak项（pip 25.1/26.1细节、PDM workspace单源）保留但降低措辞强度，不再列已解决的pixi条目。
- 标题行标注"终审版"。

## 收尾
grid 最终态：✅48 / ⚠4 / ⚔0 / ❓1 / ∅2，resolved 50/55 (91%)，冲突全部清零。report.md 三轮字符轨迹 6467→7686→8010，全程未超 budget=9000，且每轮都是重写而非追加。共 3 轮扩展、11 次 spawn（R1=6, R2=4, R3=1，另加本机执行的编辑/脚本步骤不计入 spawn），符合 --rounds 3 --workers 6 的外层限制。终稿同步写入 ds/report.md 与仓库根 report.md。任务完成，停止扩展。
