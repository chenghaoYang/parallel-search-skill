# log

## R0 定框架
- 读者=选型工程师；5 实体 × 10 维度网格；分类轴 v0：持久化模型 × 执行模型 × 确定性边界。
- R1 计划：按来源边界 5 个实体各 1 工人（填 D1–D10 整行）+ 1 scout（坑 + 漏的实体/维度）。共 6 spawn。

## R1 收束（6 spawn：5 实体 + 1 scout）
- 结果：192 claims（182 official）；grid 45✅/4⚠/2⚔/2∅，47/53 已填。
- taxonomy v0→v1：确认两轴（持久化/恢复机制 × 谁拉起代码）；确定性边界由轴 A 推出，去单列。
- 关键发现：Inngest server=SSPL+DOSP 非 Apache；Restate server=BSL 1.1；Temporal TS 沙箱 Math.random 可直接用；Hatchet durable task 有 checkpoint 间确定性要求；各家 exactly-once 均只覆盖引擎内部。
- 压缩：10698→8926（删次要实体行/一源、散文压表）。
- R1 观察：核心格已 ✅，剩余是边界主张反证 + 少数 ∅ 格 → 动作：R2 派 5 个窄简报（temporal 计费定义、inngest EO 措辞+自托管门控、hatchet 版本钉定、restate 对比页/升级语义、dbos 小缺口）→ 预计 spawn：5

## R2 收束（5 spawn：定向补缺口/反证）
- 解决：Temporal action 定义（8 类）+SDK license（Java 唯一 Apache）；Inngest "exactly once"=step 记忆化内部语义（已逐字核）+自托管二进制不含 SSO/RBAC/audit（Makefile 实证）；Restate 同 endpoint 改码→RT0016 journal 兼容失败+自托管单二进制含全部集群特性；Hatchet 建 run 钉 workflow_version_id（schema 级）+重试默认关；DBOS Java GA/PG14+/Conductor 专有闭源。
- 重写 report：9888→压至 <9000（删 §3 两行、合并措辞）。Rounds 用尽 + 预算耗尽，终审不另派核验工人：关键边界主张已在 R2 回原页逐字核（license 原文、Inngest EO 原句、RT0016、Hatchet retries=0），其余以 notes [C#] 自查。未逐条核验项见 report §5 与 audit.md。
