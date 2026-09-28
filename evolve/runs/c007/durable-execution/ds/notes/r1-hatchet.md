# r1-hatchet
question: Hatchet（hatchet.run）作为 durable execution / task queue 引擎，在 D1–D10 十个维度上官方文档实际怎么写。
checked: https://docs.hatchet.run, https://github.com/hatchet-dev/hatchet, https://hatchet.run/pricing, https://docs.hatchet.run/v1/durable-execution, https://docs.hatchet.run/self-hosting, https://docs.hatchet.run/v1/concurrency, https://docs.hatchet.run/v1/tasks, https://docs.hatchet.run/v1/idempotency, https://docs.hatchet.run/llms.txt, https://docs.hatchet.run/v1/architecture-and-guarantees, https://docs.hatchet.run/v1/cloud-vs-oss, https://docs.hatchet.run/v1/durable-sleep, https://docs.hatchet.run/v1/from-temporal-to-hatchet, https://docs.hatchet.run/v1/durable-event-waits, https://docs.hatchet.run/v1/workers, https://docs.hatchet.run/v1/events, https://docs.hatchet.run/v1/embedded, https://docs.hatchet.run/v1/task-eviction, https://docs.hatchet.run/v1/durable-tasks, https://raw.githubusercontent.com/hatchet-dev/hatchet/main/README.md

## claims
- [C1] D1: Postgres 是状态存储与事实源 | src: https://docs.hatchet.run/v1/architecture-and-guarantees | quote: "PostgreSQL is the durable store for workflow definitions and execution state." | type: official
- [C2] D1: 状态转换事务化，引擎重启不丢状态 | src: https://docs.hatchet.run/v1/architecture-and-guarantees | quote: "Workflow state is persisted in PostgreSQL, and state transitions are performed transactionally." / "The engine and API server are designed to restart without losing state." | type: official
- [C3] D1/D2: durable task 崩溃恢复靠 checkpoint+event log 回放 | src: https://docs.hatchet.run/v1/durable-execution | quote: "every time a piece of a durable task completes, it creates a new checkpoint" in "a durable event log"; "replay the task from whatever checkpoint it last reached" | type: official
- [C4] D2: durable task 代码在 checkpoint 之间必须确定（简报假设被推翻）| src: https://docs.hatchet.run/v1/durable-tasks | quote: "the code between checkpoints must be deterministic"; 须 "deterministic given the event history" | type: official
- [C5] D2: 与 Temporal 相同的确定性规则仅限 durable task；DAG task 无约束 | src: https://docs.hatchet.run/v1/from-temporal-to-hatchet | quote: durable task "carries the same determinism rules a Temporal workflow does"; "There is no determinism constraint on a DAG task" | type: official
- [C6] D2: durable task 只能调 durable context 方法或 spawn child，副作用须放进 child task | src: https://docs.hatchet.run/v1/durable-tasks | quote: "not directly access your database or an external API, or generate random numbers"; "Push side effects into child tasks" | type: official
- [C7] D2/D6: sleep 为 durable wait：等待时任务可被 evict，不占 slot，满足后回放 event log 恢复 | src: https://docs.hatchet.run/v1/durable-sleep | quote: "While the task is sleeping, no resources are consumed"; "guaranteed to respect the original duration across interruptions" | type: official
- [C8] D3: 许可证 MIT | src: https://github.com/hatchet-dev/hatchet | quote: "License: MIT"（badge）；docs 首页称 "MIT-licensed open source" | type: official
- [C9] D3: 自托管全功能，差异仅在运维归属 | src: https://docs.hatchet.run/v1/cloud-vs-oss | quote: "programming model is the same: you write tasks/workflows in code and run workers that connect to Hatchet"；无 cloud-only 功能列出 | type: official
- [C10] D4: Cloud 按 task run 计费 | src: https://hatchet.run/pricing | quote: "$10 per 1M task runs"; "First 100,000 runs included" | type: official
- [C11] D4: 档位：Developer 免费 / Team $500/mo / Scale $1,000/mo / Enterprise custom | src: https://hatchet.run/pricing | quote: "Team $500/mo + usage"; "Scale $1,000/mo + usage"; Enterprise "Let's Talk" | type: official
- [C12] D5: 官方 SDK：Python、TypeScript、Go、Ruby，均有完整 API reference | src: https://docs.hatchet.run | quote: "applications written in Python, TypeScript, Go and Ruby" | type: official
- [C13] D5: Ruby 成熟度稍逊——embedded mode 尚无 Ruby | src: https://docs.hatchet.run/v1/embedded | quote: "Embedded mode for the Ruby SDK is coming soon." | type: official
- [C14] D6: durable task 原语 = wait(sleep/event 可组 or-group) 或 spawn child | src: https://docs.hatchet.run/v1/durable-execution | quote: "wait for something, such as a sleep to complete or an event to be received" or spawn children; "wait for either a sleep to complete or an event to be pushed, whichever comes first" | type: official
- [C15] D6: wait API 在 DurableContext 上 | src: https://docs.hatchet.run/v1/durable-event-waits | quote: Python `ctx.aio_wait_for_event("user:update")`; TS `ctx.waitForEvent(EVENT_KEY)`；可加 CEL 过滤表达式 | type: official
- [C16] D6: 事件推送经 SDK event client 或 incoming webhook | src: https://docs.hatchet.run/v1/events | quote: `hatchet.event.push("user:create", {...})`；事件可作 run 触发器（run-on-event）并支持 CEL filter | type: official
- [C17] D6: cron + scheduled run 均为一级原语；错过的调度不补跑 | src: https://docs.hatchet.run/cron-runs | quote: "If a scheduled task is missed (e.g., due to system downtime), Hatchet will not automatically run the missed instances." | type: official
- [C18] D6/D9: 等待中的 durable task 可被 evict 释放 slot，满足条件后原 worker 上重放恢复 | src: https://docs.hatchet.run/v1/task-eviction | quote: "evict durable tasks from workers when they're in one of these waiting states"; "its event log is replayed up to the checkpoint where it left off" | type: official
- [C19] D7: 无 Temporal patching/GetVersion 等价物；官方做法=部署新定义让旧 run 排空 | src: https://docs.hatchet.run/v1/from-temporal-to-hatchet | quote: "Hatchet has no equivalent."；建议 deploy "a new durable task definition and letting the old work drain" | type: official
- [C20] D7: workflow/task 定义带 `version` 字段，API 有 get_version，run context 暴露 workflow_version_id | src: https://docs.hatchet.run/reference/python/feature-clients/workflows.md | quote: "Get a workflow version by the workflow ID and an optional version." | type: official
- [C21] D8: 执行语义 = at-least-once，task 可能跑多次，代码应幂等 | src: https://docs.hatchet.run/v1/architecture-and-guarantees | quote: "Hatchet is at least once: tasks are not silently dropped, and failures retry according to your configuration." | type: official
- [C22] D8: durable task 的 checkpoint 被宣传为接近 exactly-once（与 C21 存在口径张力）| src: https://docs.hatchet.run/v1/durable-tasks | quote: "exactly-once semantics which you wouldn't get with many other task queue implementations" | type: official
- [C23] D8: 幂等键：TTL-based 与 status-based 两种，CEL 表达式求 key，冲突时引擎拒收 run | src: https://docs.hatchet.run/v1/idempotency | quote: "Only one run for a given key will occur in the time window"; "the engine will reject the workflow run" | type: official
- [C24] D8: 并发控制 = CEL concurrency key + 5 种策略 | src: https://docs.hatchet.run/v1/concurrency | quote: "GROUP_ROUND_ROBIN", "Cancel In Progress", "Cancel Newest", "Cancel Queued Except Newest", "Cancel Queued Except Oldest"；可跨 workflow 共享命名策略 | type: official
- [C25] D8: child_key 去重子 run | src: https://docs.hatchet.run/reference/python/runnables | quote: "`child_key` ... "An optional key for deduplicating child workflow runs." | type: official
- [C26] D9: worker = 长驻进程，启动时向 engine 注册 task/workflow，slot 本地限流默认 100 | src: https://docs.hatchet.run/v1/workers | quote: "registers each of its tasks and workflows with Hatchet"; "The default slot count for workers in Hatchet is 100" | type: official
- [C27] D9: 自托管组件 = Postgres（必需）+ RabbitMQ（可选）+ API server/Engine(gRPC)/Dashboard；Lite 为单镜像 | src: https://docs.hatchet.run/self-hosting | quote: "PostgreSQL for storing workflow state and metadata"; "RabbitMQ for inter-service communication" (optional); "Single docker image with bundled engine and API" | type: official
- [C28] D9: embedded mode：Go 进程内运行引擎，TS/Python 用 sidecar + embedded-postgres | src: https://docs.hatchet.run/v1/embedded | quote: "a full Hatchet engine running locally without any external dependencies including Postgres"（默认 embedded-postgres 供给库）| type: official
- [C29] D9: 两种编程模型并存：DAG（parents=[...] 声明式）与 durable task（过程式 checkpoint）| src: https://docs.hatchet.run/v1/from-temporal-to-hatchet | quote: Fixed sequences become `parents=[...]` declarations；另有专页 /v1/directed-acyclic-graphs | type: official
- [C30] D10: 自我定位 | src: https://raw.githubusercontent.com/hatchet-dev/hatchet/main/README.md | quote: "An orchestration engine for background tasks, AI agents, and durable workflows" | type: official
- [C31] D10/D1: Postgres 同时是运行时与可观测性的 durable layer | src: https://raw.githubusercontent.com/hatchet-dev/hatchet/main/README.md | quote: "it uses Postgres as a durability layer for both the task runtime and the observability system" | type: official
- [C32] D10: 对标 Temporal/DBOS/Celery | src: https://raw.githubusercontent.com/hatchet-dev/hatchet/main/README.md | quote: "Hatchet's durable tasks feature is a drop-in replacement for Temporal or DBOS workflows."; "Traditional task queues like BullMQ and Celery trade off durability for throughput." | type: official
- [C33] D10: 吞吐量口径 | src: https://raw.githubusercontent.com/hatchet-dev/hatchet/main/README.md | quote: "Hatchet has been load-tested up to 10k tasks/second" | type: official
- [C34] D10: 目标负载 = AI agent + 大规模 fan-out | src: https://docs.hatchet.run | quote: "mission-critical AI agents, durable workflows, and background tasks"；声称月产 billions of tasks | type: official

## conflicts
- 简报假设「Hatchet 大概率不要求确定性」被推翻：durable task 明确要求 "the code between checkpoints must be deterministic"（durable-tasks）与 "the same determinism rules a Temporal workflow does"（from-temporal）；仅 DAG/普通 task 无约束。区别在 Hatchet 从最近 checkpoint 续跑而非从头 replay 全程。
- at-least-once（architecture-and-guarantees: "a task can run more than once"）vs "exactly-once semantics"（durable-tasks/durable-execution 的营销口径）：前者指投递语义、后者指 checkpoint 内部不重复执行已完成的步骤，文档未调和两措辞。

## gaps
- in-flight run 是否固定在触发时的 workflow version 上执行：无显式语句；"let the old work drain" 隐含旧 worker 继续服务旧版本，未见文档明说。
- worker 崩溃 mid-task 的重指派细节（heartbeat 超时→重排）未逐句描述，仅有 "at least once" + "Workers reconnect after network interruptions" 兜底。
- 事件推送的 REST 端点：events 页只写 SDK push + incoming webhook，未列 REST path。
- Ruby SDK 引入时间/成熟度未量化（仅 embedded 缺失佐证其较新）。
- worker labels/affinity 细节在 workers 页未见（有独立 advanced-assignment 页未取）。

## leads
- /cookbooks/durable-tasks-vs-dags：DAG vs durable task 选型细则
- /self-hosting/upgrading-downgrading + /self-hosting/downgrading-db-schema-manually：引擎升级兼容策略
- /reference/changelog/{platform,python,typescript,ruby}：feature 起始版本可查
