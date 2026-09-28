# log

R0：brief/grid 建好。5 实体 × D1–D10 维度，分类轴 v0 = 恢复机制(replay vs journal) × 状态载体(server/PG/log) × 编程模型(DSL vs 内嵌 step vs actor)。
R1 决策：按来源边界拆，5 实体各 1 工人覆盖全维度 + 1 scout 扫新实体/坑。spawn：6（上限 6）。

待查：

R1 观察：6/6 工人返回，172 claims（official 168）。网格 49/51 填上，taxonomy v1 轴（恢复机制×状态载体×编程模型）能解释全部差异，不换轴。
关键产出：Inngest server=SSPL+DOSP、Restate server=BUSL-1.1（用户疑点2 部分证伪）；Hatchet durable task 也要确定性（推翻假设）；exactly-once 各家口径不同。
收束：report.md 11801→8993（来源节 3400+，压缩手段：三表并一表、删 Vercel/Windmill/Trigger/River 行、砍 §4.6、收紧措辞）。快照 report.r1.md。
R2 决策：剩余缺口集中在边界主张反证 → 派 2 个窄工人：(a) 许可证+自托管限制+Restate 官方定价；(b) exactly-once 否定主张反证+Hatchet 版本钉住/不补跑复核。预计 spawn：2。
待查：终审时把一屏看懂 7 条 + 坑 5 条逐条回原页核对。

R2 观察：2/2 工人返回。推翻：Temporal 文档确有 exactly-once 承诺（workflow「exactly once and to completion」、Activity「observed as completed exactly once」）；Inngest 确有 step 级「executes exactly once」措辞；Inngest 自托管缺口扩大（单节点/无 retention/metrics 单 gauge/诊断 alpha）；Restate 官方五档定价到手（Free 100k、$75/5M、$300/20M、$1k/50M）；Hatchet 停机不补跑确认但 pause 可 queue/drop。
收束：report.md 9044→8955（改 §0 疑点 3、§4.3、§5、计费行；补 [62]-[66] 新源；删 §0 部署重量条）。快照 report.r2.md，同步 ./report.md。
终审：预算耗尽，不再 spawn；最高风险主张已由 R2 反证工人回源核对（相当于终审核验），其余为单源一手并在 §5 声明。
