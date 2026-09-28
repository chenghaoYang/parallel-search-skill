# Log

## R0（定框架，不 spawn）
- 观察：任务给定 5 组种子实体（uv / pip / Poetry / PDM / conda+pixi），4 个必答维度，2 个用户点名疑点（PEP 751、Poetry 2 `[project]`），加迁移/CI缓存/私有源。
- 决策：拆 pixi 与 conda 为两行（行为差异大：pixi 有锁文件+workspace，conda 没有原生锁文件标准）；定 9 个维度、2 条分类轴、3 个家族（见 grid.md v0）。
- 下一步：R1 按实体分工，6 个工人（uv / pip+pip-tools / Poetry / PDM / conda / pixi），每人填自己那一行的全部 9 格，并在 D1 里显式核实 PEP 751 支持状态；Poetry 工人额外核实 `[project]` 表疑点。预计 spawn：6。

## R1 收束
- 6 个工人全部完成，125 条主张（official 124/secondary 1），3 处冲突，22 处缺口，15 条线索（`notes_lint.py` 输出）。
- 两个用户点名疑点都拿到一手结论：PEP 751 已 Final(2025-03-31)，但 uv/pip/PDM 均 experimental/preview、Poetry 未实现（开放 issue #10356）、conda/pixi 未提及；Poetry 2.0.0(2025-01-05) 确认支持 PEP 621 `[project]`，与 `[tool.poetry]` 并存无弃用时间表。
- taxonomy 校验：3 家族 + 2 分类轴成立，唯一例外是 pixi 原生桥接 PyPI+conda 两端，记入「变体」一节而非改轴。
- grid 填充率 89%（50/56），剩余：Poetry D2/D5/D8（workspace 缺失待反证、解析器速度缺、迁移指南缺），PDM D7（pipx 等价物证据是伪造 quote，需重查）。
- 用户点名的「CI 缓存」维度 R1 完全未覆盖（6 个工人按实体分工，没人跨实体查这个）。
- report.md 首版 10314 字符超预算，压缩来源节格式（每工具一行、共享域名前缀）后降到 8516，在 9000 预算内；已写 snapshots/report.r1.md，镜像到顶层 ./report.md。
- 观察 → 决策：核心矩阵已 89% 落地，剩余缺口集中在 Poetry 三格 + PDM 一格（可判定类）+ CI 缓存（用户点名、完全空缺）。按「核心格子 ❓」「弱证据只有 secondary/伪造 quote」「scout leads 有新维度未覆盖」三条规则，派比 R1 更少更窄的工人。
- 下一步：R2 派 3 个工人（少于 R1 的 6）：
  1. r2-poetry-gaps（Poetry D2 workspace 反证 + D5 解析器 + D8 迁移指南）
  2. r2-pdm-globaltool（PDM D7 pipx 等价物真实核实）
  3. r2-ci-cache（跨实体：uv/pip/Poetry/PDM/conda/pixi 在 CI 里官方推荐缓存什么）
  预计 spawn：3。

## R2 收束
- 3 个工人全部完成，40 条新主张（official 39/secondary 1），0 冲突，9 缺口（均低优先级：解析器算法名、次要文档页缺失），5 条线索。
- Poetry D2（workspace）从「❓不确定」升级为「∅已确认」：issue #936(2019) closed as not planned，且发现第三方插件 poetry-workspaces 佐证核心确实没有这功能；D8（迁移）确认没有官方指南、`poetry init`不支持自动导入。
- PDM D7 的伪造 quote 被替换为真实证据：`--global/-g` 是切全局项目配置文件，与 pipx 式隔离运行无关，PDM 确认没有全局工具机制。
- 新增 D10 CI 缓存维度，6 个实体全部填上（uv/pip/Poetry/PDM 官方 action 一行开启，conda 需手动配置，pixi 默认自动缓存），发现关键坑：Poetry 的 `cache: poetry` 缓存的是 virtualenv 目录而非包缓存，容易被忽视。
- grid 检查：4 个必答维度（D1 锁文件/D2 workspace/D3 Python版本/D4 构建后端）在 6 实体上全部 ✅/∅/—，**无一处 ❓**。剩余 ❓ 只在次要维度（Poetry/pixi 解析器算法名，均属官方未公开、非空缺型缺口）。
- report.md 重写后 9499 字符超预算，压缩一屏看懂重复表述 + D10 表格精简 + 未决节合并后降到 8998，snapshots/report.r2.md，镜像顶层 ./report.md。
- 观察 → 决策：核心矩阵已 91% 且本轮未发现新的高价值缺口/冲突，用户点名的两个疑点和「其他须知」三项（迁移/CI缓存/私有源）都已有明确结论。触发终审条件（核心格子均 ✅/∅，上轮改动集中在次要维度）。
- 下一步：不再扩展，进入终审——派 1 个审稿工人抽查 ≥20 条具体主张对照 notes/ 判定，然后我按审稿结果做最后一次不做新调研的收束。预计 spawn：1。

## R3 终审（不扩展，仅核验+收束）
- 审稿工人抽查 30 条主张（覆盖第0/2/3/4节），写入 `audit.md`：supported 28（93%）、weak 0、unsupported 1、contradicted 0。所有版本号/日期（PEP751、Poetry 2.0.0、uv 0.12.x、PDM v2.24/2.25/2.28/2.5、conda 23.10/26.5）逐一核对无误；所有「确认没有」类否定结论（Poetry workspace/全局工具、PDM全局工具、conda workspace、pip无锁）均有原句支撑；引用号未发现张冠李戴。
- 唯一 unsupported：一屏看懂第5条 + 矩阵 conda×D4 把「笔记里的 gap（未查到 PEP517 相关说明）」写成了「官方文档不提 PEP517」的断言式否定，证据强度不够。已改写为「与 PEP517/518 关系未说明」（如实反映「未查到」而非「确认不存在」），不是删除也不是反转成相反主张。
- 改完重新计入预算：8999/9000 字符，snapshots/report.r3.md，镜像顶层 ./report.md。
- 收尾状态：4 个必答维度在 6 个实体上零 ❓；用户点名的 2 个疑点（PEP 751 现状、Poetry `[project]`表）和 3 个「其他须知」（迁移、CI缓存、私有源）在正文都有明确结论；剩余未决仅 2 条低优先级细节（Poetry/pixi 解析器算法名），已在第5节列出。三轮字数轨迹 8516→8998→8999，全部未超预算，没有反复膨胀。
- 结论：任务完成，停止扩展。
