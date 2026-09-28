# Durable Execution 引擎怎么选：Temporal / Restate / DBOS / Inngest / Hatchet

> 五家持久化模型/确定性/部署/许可证/计费差异+三个传言核实。截至 2026-09-25；事实引一手来源，社区观点标（二手）。

## 0. 一屏看懂

- **五家是四类东西**：Temporal/DBOS 重放确定性函数恢复状态；Restate 把每步结果写进执行日志；Inngest 把函数从头重调、step 结果记忆化；Hatchet 是 Postgres 上的 DAG 任务队列（durable task 才有 checkpoint）。[1][2][3][4][5]
- **「所有代码必须确定性」只适用于重放派**：Temporal（全 SDK）与 DBOS 要求 workflow 函数整体确定性；Restate 只要求副作用包 `ctx.run`；Inngest 要求非确定逻辑进 `step.run`；Hatchet 普通 task 无约束（durable task 例外）。[2][6][7][8][9]
- **Math.random 传言按 SDK 分**：Temporal TS 沙箱把 `Math.random()` 换成确定性版本可直接用；Go SDK 才真没随机源，须用 Side Effect。[6]
- **许可证传言只对一半**：Temporal server、DBOS 库、Hatchet 均 MIT；Restate server 是 BSL 1.1（禁做托管竞品，4 年转 Apache）；Inngest server/CLI 是 SSPL+DOSP（3 年转 Apache）、只有 SDK 是 Apache。自托管跑业务没问题，「完全开源」不准确。[10][11][12][13][14]
- **durable execution ≠ 外部副作用 exactly-once**：各家保的是「代码路径/内部状态」恰好一次（Inngest 原话 "each step completes exactly once" 也指 step 结果不重跑）；外部副作用都 at-least-once+幂等兜底——Temporal 建议 Activity 幂等、Hatchet 明写 "at least once"。[15][16][17][55]
- **计费单位不可比**：Temporal 按 actions+存储、Restate 按 durable actions、Inngest 按 executions（run+step）、Hatchet 按 task runs、DBOS 按 checkpoints+席位。[19][20][21][22][23]
- **版本升级差异最大**：Restate 在跑 invocation 钉原版本最省心；Temporal/DBOS 靠 patching/版本路由；Inngest 认 step ID，改 ID 强制重跑；Hatchet 引擎大版本不迁移在跑 run。[24][25][26][27]

## 1. Taxonomy：两个分类轴

**轴 A — 状态怎么持久化/恢复**（决定确定性要求与升级玩法）：

| 家族 | 实体 | 为什么是一类 |
|---|---|---|
| 重放派 | Temporal、DBOS | 重跑函数+记录结果回填 → workflow 代码必须确定性 |
| journal 派 | Restate | 每步结果进执行日志、重放跳过已完成步 → 只约束副作用 |
| step 记忆化派 | Inngest | 平台每步调一次函数、结果按 step ID 记忆化 → 步骤间代码可重入 |
| DAG 队列派 | Hatchet | task 是独立函数不 replay → 无确定性概念（durable task 例外） |

**轴 B — 谁拉起代码**：worker 主动连引擎（Temporal 轮询、Hatchet gRPC）；平台反向调你的 HTTP/Lambda endpoint（Restate、Inngest，可跑 serverless）；进程内库（DBOS，除 Postgres 零基础设施）。

## 2. 对照矩阵

### 2a 持久化 / 确定性 / 执行

| | Temporal | Restate | DBOS | Inngest | Hatchet |
|---|---|---|---|---|---|
| 持久化 | Event History append-only 日志；持久层 Cassandra/PG/MySQL [28] | Bifrost 分布式日志为真源+RocksDB 缓存+Raft+S3 快照 [18] | 检查点写进你的 Postgres system DB [4] | 每步结果持久化、按 step ID 记忆化 [3] | Postgres 唯一必需（队列+可观测性），RabbitMQ 可选 [5] |
| 恢复 | 重跑代码与 Event History 比对，已完成 activity 不重跑 [1] | 重放 journal 跳过已完成步 [2] | 重调函数+检查点输入，已完成 step 返回记录输出 [4] | handler 从头重跑，已完成 step 注入记忆结果 [3] | task 独立重跑；durable task 重放 checkpoint [9] |
| 确定性 | workflow 代码整体确定性（平台硬要求）[2] | 非确定操作必须包 `ctx.run`，其余无约束 [7] | workflow 函数须确定性、同序调 step [8] | 非确定逻辑须进 `step.run()`；step 外代码每轮都执行 [3] | 普通 task 无；durable task 的 checkpoint 间代码须确定 [9] |
| 随机/时间 | TS 沙箱替换 Math.random/Date；Go 用 workflow.Now+Side Effect [6] | `ctx.rand.uuidv4()`/`ctx.date.now()` [7] | 放进 step（无专用 API） | 放进 step.run | 普通 task 无约束 [9] |
| 执行 | worker 同步 RPC 轮询 task queue；server 4 服务+持久库+建议 ES [28][30] | server 双向流推送到你的 HTTP/Lambda endpoint；单二进制全功能 [18] | 库嵌进程；Conductor 控制面可选 [4] | 平台每步一次 HTTP 回调（另有 Connect worker 模式）[3] | worker 双向 gRPC 连引擎，engine push 分发 [5] |

### 2b 许可证 / 云计费 / SDK

| | Temporal | Restate | DBOS | Inngest | Hatchet |
|---|---|---|---|---|---|
| license | server MIT；SDK MIT（Java 例外 Apache-2.0）[10][31] | server BSL 1.1→4 年后 Apache，仅禁做托管平台服务；SDK MIT [11] | 库 MIT [12]；Conductor 专有闭源需 license key [32] | server/CLI SSPL+DOSP→3 年后 Apache；SDK Apache [13] | MIT [14] |
| 自托管 | 全功能开源，运维自扛 | 单二进制含全部集群特性 [33] | 库全功能；Conductor 付费 | 单二进制；SAML/RBAC/audit 属 Cloud dashboard 不进二进制 [34] | 全功能；Lite 单镜像 |
| 云计费 | actions $50/百万起阶梯至 $25/M + 存储 GBh [19][35] | durable actions：Free 100k/月…$1000/50M，超量 $25/M [20] | Pro $99/月起按 seats+apps+checkpoints [23] | executions（1 run+N step）：Free 50k、Pro $99/1M [21] | task runs：$10/百万，免费档含 100k [22] |
| SDK | Go/Java/TS/Py/.NET/Ruby/PHP/Rust [36] | TS/Java/Kotlin/Py/Go/Rust/Ruby [37] | Py/TS/Go/Java（Java 已 GA；首页另列 Rust 无文档 ⚔）[38] | TS/Py/Go 主；Kotlin/Java、Rust 仓库未进文档 [39] | Py/TS/Go/Ruby [14] |

### 2c 外部事件 / 版本升级 / 副作用

| | Temporal | Restate | DBOS | Inngest | Hatchet |
|---|---|---|---|---|---|
| 等外部事件 | Signal/Query/Update+`Await` [40] | signal/awakeable/promise（按 ID/key）[41] | `send/recv`+`set/get_event` [42] | `step.waitForEvent`/`waitForSignal`/`invoke`/`sendEvent` [43] | `ctx.waitForEvent`（CEL）+`on_events`+托管 webhook [44] |
| 定时 | durable timer 持久化 [45] | `ctx.sleep` 不耗资源、跨重启恢复 [41] | `DBOS.sleep` 唤醒时间存库 [8] | `step.sleep`/`sleepUntil` [43] | `ctx.sleepFor` 可 evict [46] |
| 版本升级 | `GetVersion` patch marker + Worker Deployments 钉版本 [24][25] | deployment 不可变、在跑 invocation 钉原版本；同 endpoint 改码被 journal 兼容检查拦下（RT0016）[26] | `DBOS.patch()` + 源码 hash 版本路由 [27] | 按 step ID：改 ID 强制重跑、删 ID 忽略 [47] | 建 run 时钉 workflow_version_id；引擎大版本不迁移在跑 run [48][49] |
| 副作用 | Activity 按 Retry Policy 重试、建议幂等；Update 按 ID 去重 [15][40] | `idempotency-key` 去重；宣称 "exactly-once"（指内部）[50] | step at-least-once 完成后不重跑；workflow ID 即幂等键 [8][42] | step 默认独立重试 4 次；event `id` 为 24h 幂等键 [51] | "at least once"、task 须幂等；重试默认关；幂等键 TTL+CEL [5][52][53] |

## 3. 家族外的同类

| 实体 | 一句话定位 |
|---|---|
| AWS Durable Execution SDK | Lambda 内 durable functions（TS/Py/Java/C#）；官方明说全流程不保证 exactly-once [17] |
| LittleHorse | 非 replay：WfSpec 预编译图+原生 human task [56] |

## 4. 用户需要知道的坑

- **改代码=确定性地雷（重放派）**：Temporal replay 比对 SDK 调用序列，不符即 nondeterminism error，须打 patch marker（社区高频问题是「忘记打版本」，二手）；DBOS 同病（`DBOS.patch()`+hash 路由）。[24][27][54]
- **Restate 省心有条件**：deployment 必须不可变；同 endpoint 改码使在跑 invocation 重放失败（RT0016），仅修 `ctx.run` 内部 bug 等两类 in-place 变更安全。[26]
- **Temporal 自托管运维重**：持久库选型 + 生产建议 ES；社区报告 shard 数不可变、故障反馈放大（二手）。[28][54]
- **Inngest 认 step ID**：改 ID=在跑 run 强制重跑、删 ID=旧状态被忽略。[47]
- **Hatchet**：引擎大版本不迁移在跑 run（v0→v1 双跑排空）；task 重试默认关，要自己配 `retries`。[49][52]
- **许可证的真实限制**：Restate BSL 仅禁做托管竞品；Inngest SSPL 约束把 server 对外提供为服务；DBOS Conductor 闭源且启动时回连验 license——都卡在「拿它做生意」上。[11][13][32]
- **「exactly-once」话术**：各家 exactly-once 只覆盖引擎内部（journal/step 结果不重跑）；外部副作用必须幂等。[15][16][17]

## 5. 未决与置信度

- Hatchet：重分配是否校验 worker version 未证实；心跳口径 4s/30s vs 内部 5s/15s 不一致。[49][54]
- Inngest：无官方自托管 vs Cloud 功能对照表；dashboard 的 CEL 搜索被 flag 锁住是回归还是门控未定（issue 未复）。[34]
- Restate：无逐字「自托管=全功能」，依据是单二进制含全部集群特性+对照表无独占行；价格取自 JS chunk。[20][33]
- DBOS：Postgres 14+ 下限来自 CLI 支持矩阵非 requirements 文档；Cloud CPU 单价不公开。[23][29]
- Temporal：.NET/PHP/Ruby SDK 确定性细节未逐页核。[36]
- 已双核高置信项：四家 license 原文、Inngest "exactly once" 语境、Restate RT0016、Hatchet 默认不重试。[11][13][17][26][52]

## 来源

[1] https://docs.temporal.io/workflows
[2] https://docs.temporal.io/workflow-definition
[3] https://www.inngest.com/docs/learn/how-functions-are-executed
[4] https://docs.dbos.dev/architecture
[5] https://docs.hatchet.run/v1/architecture-and-guarantees
[6] https://docs.temporal.io/develop/typescript/workflows/basics
[7] https://docs.restate.dev/develop/ts/durable-steps
[8] https://docs.dbos.dev/python/tutorials/workflow-tutorial
[9] https://docs.hatchet.run/v1/durable-tasks
[10] https://raw.githubusercontent.com/temporalio/temporal/main/LICENSE
[11] https://github.com/restatedev/restate/blob/main/LICENSE
[12] https://github.com/dbos-inc/dbos-transact-py
[13] https://raw.githubusercontent.com/inngest/inngest/main/LICENSE.md
[14] https://github.com/hatchet-dev/hatchet
[15] https://docs.temporal.io/activities
[16] https://docs.temporal.io/local-activity
[17] https://docs.aws.amazon.com/durable-execution/
[18] https://docs.restate.dev/references/architecture
[19] https://docs.temporal.io/cloud/pricing
[20] https://restate.dev/pricing
[21] https://www.inngest.com/pricing
[22] https://hatchet.run/pricing
[23] https://dbos.dev/pricing
[24] https://docs.temporal.io/develop/go/workflows/versioning
[25] https://docs.temporal.io/worker-versioning
[26] https://docs.restate.dev/services/versioning
[27] https://docs.dbos.dev/python/tutorials/upgrading-workflows
[28] https://docs.temporal.io/temporal-service/persistence
[29] https://raw.githubusercontent.com/dbos-inc/dbos-ctl/main/supported-databases.json
[30] https://docs.temporal.io/task-queue
[31] https://github.com/temporalio/sdk-java/blob/main/LICENSE
[32] https://www.dbos.dev/conductor-license
[33] https://docs.restate.dev/server/overview
[34] https://github.com/inngest/inngest/blob/main/Makefile
[35] https://docs.temporal.io/evaluate/cloud/actions
[36] https://docs.temporal.io/encyclopedia/architecture/temporal-sdks
[37] https://docs.restate.dev/
[38] https://github.com/dbos-inc/dbos-transact-java/releases
[39] https://github.com/orgs/inngest/repositories?q=inngest
[40] https://docs.temporal.io/develop/go/workflows/message-passing
[41] https://docs.restate.dev/foundations/actions
[42] https://docs.dbos.dev/python/tutorials/workflow-communication
[43] https://www.inngest.com/docs/learn/inngest-steps
[44] https://docs.hatchet.run/v1/durable-event-waits
[45] https://docs.temporal.io/workflow-execution/timers-delays
[46] https://docs.hatchet.run/v1/durable-sleep
[47] https://www.inngest.com/docs/learn/versioning
[48] https://raw.githubusercontent.com/hatchet-dev/hatchet/main/sql/schema/v1-core.sql
[49] https://docs.hatchet.run/v1/migrating/migration-guide-engine
[50] https://docs.restate.dev/foundations/invocations
[51] https://www.inngest.com/docs/reference/functions/step-run
[52] https://docs.hatchet.run/v1/retry-policies
[53] https://docs.hatchet.run/v1/idempotency
[54] https://news.ycombinator.com/item?id=48314087
[55] https://www.inngest.com/docs/examples/durable-endpoints
[56] https://littlehorse.io/compare/durable-execution
