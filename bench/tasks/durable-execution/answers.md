# durable-execution 任务参考答案

给人工检查者用的简明答案，对应 task.md 里用户提出的疑问。核实日期：2026-09-24。

## 1. "写 workflow 所有代码都必须确定性、连 Math.random 都不能用——这类引擎全都这么要求吗？"

**半对。** "代码必须确定性"这个约束各家都有，但严格程度和落地方式差很多：

- **Temporal 最严格**：workflow 代码要能按 Event History 逐条 replay 出同样的 command 序列。TypeScript SDK 干脆把 workflow 跑在确定性沙箱里（V8 isolate/VM 隔离）：`Math.random()`、`Date`、`setTimeout` 被替换成确定性版本，`WeakRef`/`FinalizationRegistry` 直接抛错；能 import 的 npm 包不得引用 Node.js 或 DOM API（`fs`、`http` 这类用不了）。非确定性工作必须放进 Activity。注意：约束只管 workflow 代码，**Activity 就是普通代码**，随便写。
- **Restate**：普通 handler 代码没有沙箱，但 journal 顺序必须与代码产生的持久操作一致——非确定性操作（HTTP、数据库响应、UUID）要包进 `ctx.run`，结果写进 execution log，replay 时回放记录值。改代码导致 journal 不匹配会报 RT0016 journal mismatch。
- **DBOS**：要求 workflow 函数确定性——同样输入要以同样顺序调同样的 step，I/O 只能放进 step；step 至少执行一次、完成后不重跑。
- **Inngest**：step memoization 模型，函数会被整体重新调用，已完成 step 由 SDK 注入缓存结果。代码层面约束最松，但 step 边界外的非确定性（如在步骤外生成随机数再传给步骤）一样会踩坑。
- **Hatchet**：普通 task 根本不是 replay 模型，而是调度/重试语义；只有 durable task 的 wait/spawn 会写 durable event log checkpoint。所以"所有代码确定性"对 Hatchet 基本不适用。

来源：https://docs.temporal.io/workflow-definition ；https://docs.temporal.io/develop/typescript/workflows/basics ；https://docs.restate.dev/develop/ts/durable-steps ；https://docs.restate.dev/services/versioning ；https://docs.dbos.dev/python/tutorials/workflow-tutorial ；https://www.inngest.com/docs/learn/how-functions-are-executed ；https://docs.hatchet.run/v1/durable-tasks

## 2. "Restate 和 Inngest 都是开源的、自托管没限制" —— 许可证真没问题吗？

**半错，这正是最容易踩的坑。** 五家的协议现状：

| 引擎 | Server/运行时 | SDK |
|---|---|---|
| Temporal | **MIT**（宽松开源） | MIT |
| Restate | **BSL**（Business Source License，source-available，非 OSI；Additional Use Grant 限制拿它做对外 Application Platform Service） | MIT |
| DBOS | MIT（DBOS Transact 各语言库） | MIT |
| Inngest | **SSPL + DOSP**（server 和 CLI 是 Server Side Public License，代码延迟三年转 Apache 2.0） | Apache 2.0 |
| Hatchet | **MIT** | MIT |

所以"都是开源随便自托管"只对 Temporal、DBOS、Hatchet 成立。Restate 和 Inngest 内部自托管一般没问题，但如果你想把它嵌进对外售卖的平台/托管服务，BSL 和 SSPL 的附加条款就要法务过一遍了。注意"SDK 是 MIT/Apache"不等于"server 也是"——这是官网话术里常见的混淆点。

自托管形态也不同：Inngest 的 `inngest dev` 只是本地开发服务器（默认 SQLite + 内嵌 Redis，官方明说不能上生产），生产自托管要 `inngest start` 并外接 Postgres/Redis；Hatchet 自托管有 Lite/Docker Compose/Helm 三档；Restate 是单二进制 BSL server；Temporal 自托管是完整的集群（需要 Cassandra/Postgres/MySQL 等持久层 + Elasticsearch 可选）。

来源：https://docs.restate.dev/get-restate ；https://github.com/inngest/inngest ；https://github.com/temporalio/temporal ；https://github.com/hatchet-dev/hatchet ；https://github.com/dbos-inc/dbos-transact-ts ；https://www.inngest.com/docs/self-hosting

## 3. "上了 durable execution 是不是就等于 exactly-once？"

**不是。** Durable execution 保证的是"引擎对进度的认知"不丢——崩溃后能从记录的历史/journal/checkpoint 恢复，而不是把整个流程盲重跑。但任何跨到另一个独立系统的副作用（调支付 API、发邮件、写第三方库）都绕不开"崩溃发生在副作用成功之后、记录完成之前"的窗口。Temporal 官方都明说：把 Activity 最大重试次数设成 1 **并不**构成 exactly-once——worker 可能已完成外部副作用却没来得及记完成事件。正确姿势是：副作用放进引擎的持久边界内 + 给下游传由 workflow/run id 派生的幂等键。DBOS 是个特例亮点：如果业务写入和 workflow 状态在同一个 Postgres 事务里提交，就能拿到真正的事务级 exactly-once。

来源：https://docs.temporal.io/activities ；https://docs.dbos.dev/python/tutorials/workflow-tutorial ；https://docs.restate.dev/foundations/key-concepts

## 4. 持久化模型到底差在哪？

- **Temporal**：最典型的事件溯源——每条 workflow execution 一条 append-only Event History，worker replay 代码重建状态，已完成的 Activity 结果从历史读取不重跑。
- **Restate**：log-first 分布式运行时（Bifrost 复制日志）。每个 partition 一个 leader 定序、quorum 复制；log 是主持久层，RocksDB 只是可从 log 重建的物化缓存；周期性快照到 S3 以裁剪日志。应用侧看到的是 invocation journal replay。
- **DBOS**：没有独立服务，库嵌进应用，Postgres 系统库存 workflow 输入/状态、step 输出、队列和调度；恢复时重进 workflow 函数、逐 step 查 checkpoint，在第一个没 checkpoint 的 step 恢复执行。
- **Inngest**：托管的 step memoization——函数每次被重新调用，已完成 step 的结果由 SDK 注入 `step.run` 返回值，只跑第一个未完成的 step。
- **Hatchet**：Postgres 为事实源的调度引擎（Engine 调度分发、记录状态转移，高吞吐可加 RabbitMQ 类 broker）；durable task 在 wait/spawn 时往 durable event log 写 checkpoint。

来源：https://docs.temporal.io/workflow-definition ；https://docs.restate.dev/references/architecture ；https://docs.dbos.dev/architecture ；https://www.inngest.com/docs/learn/how-functions-are-executed ；https://docs.hatchet.run/v1/architecture-and-guarantees

## 5. SDK 语言覆盖

- **Temporal**：8 门官方 SDK——Go、Java、Python、TypeScript、.NET、Ruby、PHP、Rust。
- **Restate**：7 门——TypeScript、Java、Kotlin、Go、Python、Rust、Ruby。
- **DBOS**：4 门——Python、TypeScript、Go、Java（同一套 Postgres schema，跨语言可用 client 互操作）。
- **Hatchet**：Python、TypeScript、Go、Ruby。
- **Inngest**：TypeScript、Python、Go 官方 SDK，其它语言走 REST API。

来源：https://docs.temporal.io/encyclopedia/architecture/temporal-sdks ；https://docs.restate.dev/ ；https://docs.dbos.dev/ ；https://github.com/hatchet-dev/hatchet ；https://www.inngest.com/docs/reference

## 6. 托管云计费模型（容易估错的地方）

- **Temporal Cloud**：按 **Action** 计费（启动 workflow、heartbeat、signal/message 都算），起步 $50/百万 Action、按量阶梯降到 $25/百万（200M 以上议价）；存储按 GBh 另算，还有 plan/support 费（Essentials $100/月或消费的 5% 起、Business $500/月或 10% 起）。开 HA replica 约等于 Action+存储 ×2。
- **Inngest Cloud**：按 **execution** 计费 = 函数运行本身 1 个 + 每个 `step.run` 各 1 个（5 step 的运行 = 6 executions）。免费档 50k executions/月；Pro $99/月起含 1M；Business $499/月起含 10M。AI agent 类工作流一次跑 10+ executions 很常见，按"触发次数"估会严重低估。
- **Restate Cloud**：免费档 50k durable actions/月；付费 $75/月起按量；另有 BYOC（部署在你自己 AWS/GCP，按预留容量计费）。
- **Hatchet Cloud**：Developer 免费含 100k task runs，之后 $10/百万 runs；Team $500/月、Scale $1000/月起 + 用量。
- **DBOS**：库本身 MIT 免费；托管控制面 DBOS Conductor 另算（免费档 + 按量）。

来源：https://docs.temporal.io/cloud/pricing ；https://www.inngest.com/pricing ；https://restate.dev/pricing ；https://hatchet.run/pricing

## 7. 等外部事件/signal 的语义差异（选型时很容易忽略）

- **Temporal**：Signal 是发给某个**正在运行的** execution 的异步消息、进 Event History；handler 更新状态，workflow 用 `workflow.condition` 阻塞等谓词为真。`signalWithStart` 原子地"没在跑就先启动再投递"，适合 webhook 先到的场景。
- **Inngest**：`step.waitForEvent` 按 match 表达式匹配**之后到达**的事件流（早发的事件不匹配），超时返回 null；`step.waitForSignal` 是对某个具体 run 的定向 API 唤醒，延迟更低。
- **Restate**：三种原语——signal（发到 keyed workflow）、awakeable（生成一次性 callback ID 给外部系统回掉）、durable promise（按 workflow key 命名的一次性 promise）。
- **DBOS**：`DBOS.recv()` 按 topic 消费发到 workflow 的消息队列，超时返回 null。
- **Hatchet**：durable task 的 wait 可以等事件 key（SDK 或 webhook 投递），崩溃后从 durable event log 恢复。

来源：https://docs.temporal.io/develop/typescript/workflows/message-passing ；https://www.inngest.com/docs/features/inngest-functions/steps-workflows/wait-for-event ；https://www.inngest.com/docs/features/inngest-functions/steps-workflows/wait-for-signal ；https://docs.restate.dev/develop/ts/external-events ；https://docs.dbos.dev/typescript/tutorials/workflow-communication ；https://docs.hatchet.run/v1/durable-event-waits

## 8. 一句话选型

- 要成熟的控制面、长生命周期状态机、跨服务编排 → **Temporal**（接受确定性约束 + 单独集群/云）。
- 想要"普通服务 handler + 持久 RPC + keyed 状态（Virtual Object）" → **Restate**（接受 BSL）。
- 已标准化 Postgres、想要库级嵌入、SQL 可直接查工作流状态 → **DBOS**。
- 事件驱动/serverless 优先、托管运维最少 → **Inngest**（按 execution 数估成本）。
- 后台任务/任务图/调度/AI agent 执行为重心、要 MIT 自托管 → **Hatchet**。
