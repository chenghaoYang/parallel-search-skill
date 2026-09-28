# Durable Execution 引擎对照：Temporal / Restate / DBOS / Inngest / Hatchet
> 新项目选型：持久化、确定性、许可证、计费、SDK、等待原语、版本升级、幂等八维差异。截至 2026-09-25。§0 结论 → §2 矩阵 → §4 坑。

## 0. 一屏看懂
- **「都要求确定性」大体成立，机制分两派**：Temporal 重放 Event History 比对 Commands，workflow 码须完全确定（TS 沙箱把 Math.random/Date 换成确定版；Go 用 workflow.Now/SideEffect）[1][2][3]；其余四家走 step/journal 注入，要求「非确定操作放进 step/run」[4][5][6][7]。例外见 §3（LittleHorse、Golem）[8][9]。
- **许可证不是都干净**：Temporal server、Hatchet、DBOS 库均 MIT [10][11][12]；Restate server=BUSL-1.1（非 OSI：自用生产允许、禁售托管 Restate，每版 4 年转 Apache-2.0）[13]；Inngest server=SSPL-1.0+DOSP（非 OSI：对外提供托管服务须开源全部 Service Source Code，3 年转 Apache-2.0）[14]。内部自托管无碍，「开源无限制」不准确。
- **durable ≠ 端到端 exactly-once**：各家都在编排/step 层用该词——Temporal「exactly once and to completion」、Activity「observed as completed exactly once」但可执行多次 [15][62]；Restate invocation 级；Inngest step 级 [63]；DBOS 入口级；副作用仍 at-least-once，幂等归开发者 [16][17][18]。
- **持久化**：Temporal=Event History+全量重放 [1]；其余=每步 checkpoint 落库、重跑注入：DBOS/Hatchet 落 Postgres [20][17]，Restate 内置 Bifrost+RocksDB [21]，Inngest 平台态存储 [22]。
- **版本升级**：Temporal patching+Worker Versioning 最重 [26][27]；Restate immutable deployment 钉旧版 [28]；Inngest step-id 哈希、改 id 才重跑 [29]；DBOS patch+app-version 蓝绿 [30]；Hatchet 靠排空旧 run [31]。
- **计费**：Temporal 按 Actions（$50/百万起）[32]；Hatchet $10/百万 task runs [33]；Inngest executions=runs×(steps+1)（$99/月起）[34]；Restate 按 action（Free 100k/月、Starter $75 含 5M）[64]；DBOS Conductor 按 checkpoint（$99/月起）[36]。

## 1. Taxonomy
三条分类轴解释主要差异：
- **恢复机制**：event-history replay（Temporal 全程重放+Commands 比对）vs step journal/checkpoint（其余注入已存结果；Hatchet 从最近 checkpoint 续跑）。
- **状态载体**：专有 server+DB（Temporal）/ 自包含二进制（Restate）/ Postgres 表（DBOS、Hatchet）/ 平台托管态（Inngest）。
- **编程模型**：workflow/activity 分离（Temporal）/ 装饰器+step（DBOS）/ step.* 内嵌（Inngest）/ DAG+durable task 双模（Hatchet）/ service|virtual object|workflow 三 handler（Restate，actor 风味）。

家族：Temporal（+Cadence/Azure DF）=replay 编排；Restate=durable-RPC；DBOS/Hatchet=Postgres 背书；Inngest=事件驱动平台。相邻见 §3。

## 2. 对照矩阵
| | Temporal | Restate | DBOS | Inngest | Hatchet |
|---|---|---|---|---|---|
| 持久化/恢复 | Event History 事实源；从头重放、Commands 比对 [1][2] | journal+Bifrost+RocksDB，可快照 S3；重放跳过已完成步 [21][37] | 每步输出 checkpoint 到 PG；重跑函数逐步查表跳过 [20] | step 结果存平台态存储；重跑 handler 注入 memoized 结果 [6] | PG 事务化+checkpoint event log；从最近 checkpoint 续放 [17][38] |
| 确定性 | workflow 码必须确定；TS 沙箱换 Math.random/Date [1][3] | handler 须确定；ctx.run 包副作用、ctx.rand 按 invocation-id 播种 [4][18] | workflow 函数须同序同参调 step；无 helper API（∅）、非确定进 step [5] | 非确定逻辑必须进 step.run；step 外代码每次重跑 [6] | durable task checkpoint 间须确定；DAG task 无约束 [7][31] |
| server/SDK 许可证 | MIT / MIT（Java Apache）[10] | BUSL-1.1（4 年转 Apache）/ MIT [13][39] | 库 MIT；Conductor/Cloud 商业 [12][36] | SSPL-1.0+DOSP（3 年转 Apache）/ Apache [14] | MIT / MIT [11] |
| 自托管 | server+DB+UI；SAML/Audit Logs/Cloud Ops API 等为 Cloud 功能 [25][66] | server 全功能单二进制；console/控制面（env 日志、SAML/SCIM）属 Cloud/BYOC [23][65] | 库即自托管；Conductor 可 air-gapped（Enterprise）[36] | 同码但缺口多：默认单节点、无 retention、metrics 单 gauge、诊断 alpha [22][40] | 全功能，差在运维归属 [41] |
| 云计费 | Actions+存储，PAYG $50/百万起 [32] | actions 计费；Free $0/100k、Starter $75/5M、Business $300/20M、Premium $1k/50M [64] | Conductor $99（1M ckpt）/$499（10M）；Cloud 询价 [36] | executions=runs×(steps+1)；Free 50k/Pro $99/Business $499 [34] | $10/百万 task runs；Team $500/Scale $1k 每月 [33] |
| SDK 语言 | 8 种：.NET/Go/Java/PHP/Py/Ruby/Rust/TS [42] | TS/JVM/Py/Go/Rust[39] | Python/TS/Go/Java [43] | TS/Python/Go；kt/rs 仓库存在、docs 未列 [44] | Python/TS/Go/Ruby [45] |
| 等外部事件 | Signal 无回执/Query 只读/Update 可回执/Await 条件 [46] | awakeable（one-shot）+signal+promise [47] | send/recv+set_event/get_event（持久化） [48] | waitForEvent（CEL match+timeout）[49] | ctx.waitForEvent，可与 sleep 组 or-group [38] |
| 定时器 | timer 睡数年、百万级 [51] | ctx.sleep 无上限，suspend 不计费 [52] | DBOS.sleep 落库；cron 停机可 backfill [53] | step.sleep≤1 年（free 7 天）；cron 重叠去重 [54] | sleep 不占 slot 可 evict；停机错过**不补跑**（pause 可选 queue/drop）[55] |
| 版本升级 | GetVersion patch marker+Worker Versioning[26][27] | immutable deployment+journal 兼容检查；pause+resume 救场 [28] | patch marker+app 版本 hash 蓝绿 [30] | step-id 哈希 memoize：改 id 重跑、重排仅 warn [29] | 无 patching；定义带 version 字段，靠排空 [31] |
| 副作用语义 | workflow「exactly once and to completion」；Activity 可执行多次（仅 observed exactly once）；默认 at-least-once [15][62] | invocation 级 exactly-once；ctx.run 副作用会重试须幂等 [18] | step at-least-once；入口 exactly-once（id/调度/消息）[16][48] | step 级「executes exactly once」（memoize）；event.id 24h 去重 [63][19] | task at-least-once；TTL/CEL 幂等键拒重；并发 key 5 策略 [17][57] |

## 3. 变体与适配层（相邻实体）
- Cadence（Apache-2.0）：Temporal 前身，无升级路径 [58]
- Azure Durable Functions（Apache-2.0）：orchestrator 必须确定、禁 DateTime.Now/Guid.NewGuid [59]
- AWS Step Functions（专有）：Standard 称 exactly-once、≤1 年；Express at-least-once [60]
- LittleHorse（AGPL-3.0）：图编排非 replay，Kafka commit log，无确定性要求 [8]
- Golem（BUSL-1.1）：WASM 快照级持久化，无代码约束 [9]

## 4. 用户需要知道的坑
1. **replay 版本不兼容是最大生产坑**：Temporal 未版本化改动→nondeterminism error、in-flight 卡死；强推 Worker Versioning [26][27]。其余四家压小但没消灭 [31][29]。
2. **exactly-once 口径各指各的**：AWS=状态机层、DBOS=入口、Restate=invocation [60][48][18]；落到外部系统的副作用仍 at-least-once。
3. **自托管隐性差异**：Inngest 默认单节点、无 retention、metrics 单 gauge、诊断 alpha [22]；Restate console/控制面属 Cloud/BYOC [65]；Temporal SAML/Audit 属 Cloud [66]。
4. **幂等键机制不同**：Temporal WorkflowID 复用；Restate idempotency-key header（可 attach）[61]；DBOS workflow id 天然幂等 [5]；Inngest event.id 24h 去重 [19]；Hatchet TTL/CEL key 拒重 [57]。

## 5. 未决与置信度
- 「Hatchet in-flight run 钉旧版本」无明文，仅 drain 建议+version id 间接证据 [31]；「DBOS 无 random/now 类 helper」查过 3 页 ∅。
- 成熟度未标：Inngest-kt/rs、DBOS Go/Java、Temporal Ruby/Rust、Restate Rust/Ruby。
- 注：最高风险主张（许可证、自托管、exactly-once、Hatchet 调度/版本）已经 R2 回源核对；其余矩阵格为单源一手。

## 来源
[1] https://docs.temporal.io/workflows [2] https://docs.temporal.io/workflow-execution [3] https://docs.temporal.io/develop/typescript/workflows/basics [4] https://docs.restate.dev/foundations/actions [5] https://docs.dbos.dev/python/tutorials/workflow-tutorial [6] https://www.inngest.com/docs/learn/how-functions-are-executed [7] https://docs.hatchet.run/v1/durable-tasks [8] https://littlehorse.io/docs [9] https://github.com/golemcloud/golem/blob/main/LICENSE [10] https://api.github.com/repos/temporalio/temporal [11] https://github.com/hatchet-dev/hatchet [12] https://github.com/dbos-inc/dbos-transact-py [13] https://raw.githubusercontent.com/restatedev/restate/main/LICENSE [14] https://github.com/inngest/inngest/blob/main/LICENSE.md [15] https://docs.temporal.io/evaluate/features/job-queue [16] https://docs.dbos.dev/python/tutorials/step-tutorial [17] https://docs.hatchet.run/v1/architecture-and-guarantees [18] https://docs.restate.dev/develop/ts/durable-steps [19] https://www.inngest.com/docs/guides/handling-idempotency [20] https://docs.dbos.dev/architecture [21] https://docs.restate.dev/references/architecture [22] https://www.inngest.com/docs/self-hosting [23] https://docs.restate.dev/server/overview [24] https://docs.hatchet.run/self-hosting [25] https://docs.temporal.io/self-hosted-guide/deployment [26] https://docs.temporal.io/develop/go/versioning [27] https://docs.temporal.io/production-deployment/worker-deployments [28] https://docs.restate.dev/services/versioning [29] https://www.inngest.com/docs/learn/versioning [30] https://docs.dbos.dev/python/tutorials/upgrading-workflows [31] https://docs.hatchet.run/v1/from-temporal-to-hatchet [32] https://temporal.io/pricing [33] https://hatchet.run/pricing [34] https://www.inngest.com/pricing [36] https://dbos.dev/pricing [37] https://docs.restate.dev/foundations/key-concepts [38] https://docs.hatchet.run/v1/durable-execution [39] https://api.github.com/orgs/restatedev/repos [40] https://www.inngest.com/docs/ai-dev-tools/mcp [41] https://docs.hatchet.run/v1/cloud-vs-oss [42] https://docs.temporal.io/develop [43] https://docs.dbos.dev/ [44] https://www.inngest.com/docs/learn/inngest-functions [45] https://docs.hatchet.run [46] https://docs.temporal.io/encyclopedia/workflow-message-passing [47] https://docs.restate.dev/develop/ts/external-events [48] https://docs.dbos.dev/python/tutorials/workflow-communication [49] https://www.inngest.com/docs/reference/typescript/functions/step-wait-for-event [51] https://docs.temporal.io/develop/go/timers [52] https://docs.restate.dev/develop/ts/durable-timers [53] https://docs.dbos.dev/python/tutorials/scheduled-workflows [54] https://www.inngest.com/docs/learn/inngest-steps [55] https://docs.hatchet.run/cron-runs [57] https://docs.hatchet.run/v1/idempotency [58] https://github.com/cadence-workflow/cadence [59] https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-code-constraints [60] https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html [61] https://docs.restate.dev/foundations/invocations [62] https://docs.temporal.io/activity-definition [63] https://www.inngest.com/docs/examples/durable-endpoints [64] https://restate.dev/pricing [65] https://docs.restate.dev/byoc/overview [66] https://docs.temporal.io/cloud/audit-logs
