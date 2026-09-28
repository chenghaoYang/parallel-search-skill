# r2-hatchet
question: Hatchet (a) 注册新 workflow version 后在跑 run 是否钉在原版本；(b) task 重试策略细节（默认次数、backoff）；(c) worker 心跳/失败时任务如何重新分配。
checked: https://docs.hatchet.run/llms.txt, https://docs.hatchet.run/v1/retry-policies, https://docs.hatchet.run/v1/workers, https://docs.hatchet.run/v1/worker-healthchecks, https://docs.hatchet.run/v1/advanced-assignment/sticky-assignment, https://docs.hatchet.run/v1/advanced-assignment/worker-affinity, https://docs.hatchet.run/v1/architecture-and-guarantees, https://docs.hatchet.run/v1/faq, https://raw.githubusercontent.com/hatchet-dev/hatchet/main/sql/schema/v1-core.sql, https://raw.githubusercontent.com/hatchet-dev/hatchet/main/pkg/repository/sqlcv1/triggers.sql, https://raw.githubusercontent.com/hatchet-dev/hatchet/main/pkg/repository/sqlcv1/tasks.sql, https://raw.githubusercontent.com/hatchet-dev/hatchet/main/frontend/docs/content/docs/v1/faq.mdx, https://raw.githubusercontent.com/hatchet-dev/hatchet/main/internal/services/shared/defaults/heartbeat.go, github.com/hatchet-dev/hatchet (code search)

## claims
- [C1] 每个新建 task 行持久化 workflow_version_id（NOT NULL），run 的任务图在建 run 时绑定到当时解析出的版本 | src: https://raw.githubusercontent.com/hatchet-dev/hatchet/main/sql/schema/v1-core.sql | quote: "CREATE TABLE v1_task ( ... workflow_version_id UUID NOT NULL," | type: official
- [C2] 事件触发的 run 只解析各 workflow 的最新版本：ListWorkflowsForEvents 用 DISTINCT ON + order DESC | src: https://raw.githubusercontent.com/hatchet-dev/hatchet/main/pkg/repository/sqlcv1/triggers.sql | quote: "-- Get all of the latest workflow versions ... ORDER BY \"workflowId\", \"order\" DESC" | type: official
- [C3] cron 分配也只计最新版本 | src: https://github.com/hatchet-dev/hatchet/blob/main/CHANGELOG.md | quote: "Engine: allocated crons are counted against the latest workflow version only (#4859)" | type: official
- [C4] task 重试默认不开启，需显式配置 retries | src: https://docs.hatchet.run/v1/retry-policies | quote: "If a task fails and `retries` is set to a value greater than 0, Hatchet will catch the error and retry the task." | type: official
- [C5] 默认重试间隔只是"short delay"，文档未给固定数值 | src: https://docs.hatchet.run/v1/retry-policies | quote: "with each retry being executed after a short delay to avoid overwhelming the system" | type: official
- [C6] 可选指数退避：Python/Ruby `backoff_max_seconds`+`backoff_factor`，TS `backoff:{maxSeconds,factor}`，Go `WithRetryBackoff(2,10)` | src: https://docs.hatchet.run/v1/retry-policies | quote: "This sequence will be 2s, 4s, 8s, 10s, 10s, 10s... due to the maxSeconds limit" | type: official
- [C7] 重试耗尽后 task 标记 failed | src: https://docs.hatchet.run/v1/retry-policies | quote: "If the task continues to fail after exhausting all the specified retries, the task will be marked as failed." | type: official
- [C8] 任务内可读重试次数：Python `ctx.retry_count`、TS `ctx.retryCount()`、Go `ctx.RetryCount()` | src: https://docs.hatchet.run/v1/retry-policies | quote: "ctx.retry_count" | type: official
- [C9] 各 SDK 提供 NonRetryable 异常以跳过重试 | src: https://docs.hatchet.run/v1/retry-policies | quote: "If your task raises this exception, it will not be retried." | type: official
- [C10] SDK client 重试与 task 重试是独立机制：Python TenacityConfig max_attempts 默认 5、指数退避带 jitter；Go REST 最多 5 次尝试、429 时遵从 Retry-After；可用 HATCHET_CLIENT_NO_RETRY 等关闭 | src: https://docs.hatchet.run/v1/retry-policies | quote: "Task retries and SDK client retries are separate mechanisms." | type: official
- [C11] v1_task 区分 retry_count / internal_retry_count / app_retry_count 三个计数列 | src: https://raw.githubusercontent.com/hatchet-dev/hatchet/main/sql/schema/v1-core.sql | quote: "retry_count INTEGER NOT NULL DEFAULT 0, internal_retry_count INTEGER NOT NULL DEFAULT 0, app_retry_count INTEGER NOT NULL DEFAULT 0," | type: official
- [C12] worker 每 4 秒发心跳；30 秒无心跳→engine 判 inactive→把其在飞任务重新排队给其他 worker | src: https://docs.hatchet.run/v1/faq | quote: "Workers send a heartbeat every **4 seconds**. If the engine does not receive a heartbeat for **30 seconds**, the engine considers the worker to be inactive, and re-queues its in-flight tasks for other workers to pick up." | type: official
- [C13] 优雅关闭：SIGTERM→worker 通知 engine 进入 PAUSED（不再领新任务）→排空在飞任务至 grace period→被 SIGKILL→停心跳→engine 判死→重分配 | src: https://docs.hatchet.run/v1/faq | quote: "A worker in a `PAUSED` state no longer receives _new_ tasks from the engine." | type: official
- [C14] 重分配意味着 at-least-once，官方建议任务幂等 | src: https://docs.hatchet.run/v1/faq | quote: "a reassign could result in work being executed more than once" | type: official
- [C15] 重分配 SQL（ListTasksToReassign）：Worker.lastHeartbeatAt < NOW()-30s，evicted 任务排除，LIMIT 默认 1000，FOR UPDATE SKIP LOCKED | src: https://raw.githubusercontent.com/hatchet-dev/hatchet/main/pkg/repository/sqlcv1/tasks.sql | quote: "AND w.\"lastHeartbeatAt\" < NOW() - INTERVAL '30 seconds'" | type: official
- [C16] 重分配由 task controller 的 processTaskReassignments 周期执行；server config ReassignLimit 默认 1000 | src: https://github.com/hatchet-dev/hatchet/blob/main/internal/services/controllers/task/process_reassignments.go | quote: "func (tc *TasksControllerImpl) processTaskReassignments(ctx context.Context, tenantId string)" | type: official
- [C17] dispatcher 代码中心跳间隔常量 4s，与 FAQ 一致 | src: https://github.com/hatchet-dev/hatchet/blob/main/internal/services/dispatcher/server.go | quote: "const HeartbeatInterval = 4 * time.Second" | type: official
- [C18] sticky SOFT：worker 不可用则改派其他 worker；HARD：pending 至原 worker 恢复或超时 | src: https://docs.hatchet.run/v1/advanced-assignment/sticky-assignment | quote: "if that worker is unavailable, it will be assigned to another worker." / "will remain in a pending state until the original worker becomes available or timeout is reached" | type: official
- [C19] affinity required:true 且无匹配 worker 时任务 pending 直到合适 worker 出现或被取消 | src: https://docs.hatchet.run/v1/advanced-assignment/worker-affinity | quote: "the task run will remain in a pending state ... until a suitable worker becomes available or the task is cancelled" | type: official
- [C20] worker 健康检查端点：Python `/health`（阻塞超阈值返回 503，默认阈值 5.0s）、TS `/readyz`（HEALTHY 才 200）`/livez`；文档警告重启不健康 worker 会丢在飞任务 | src: https://docs.hatchet.run/v1/worker-healthchecks | quote: "since restarting doesn't fix an upstream Hatchet outage and drops in-flight work" | type: official
- [C21] worker 与 engine 走双向 gRPC，断网后可重连 | src: https://docs.hatchet.run/v1/architecture-and-guarantees | quote: "Workers connect to the engine over bidirectional gRPC ... Workers reconnect after network interruptions" | type: official

## conflicts
- 心跳常量口径：FAQ 与 dispatcher/server.go 均为 4s 心跳/30s 判死；但 internal/services/shared/defaults/heartbeat.go 写 `HeartbeatInterval = "5s"`、`StaleHeartbeatInterval = "15s"`——疑似 ticker/partition 等内部组件心跳，非 worker 心跳，未核实归属。
- FAQ 说 30s 无心跳判 inactive；defaults 里 StaleHeartbeatInterval=15s 语义未核实（可能对应不同组件）。

## gaps
- 版本钉扎的执行层面：v1_task/v1_dag 均带 workflow_version_id（结构性钉在创建时解析的版本），但未见代码/文档说明重分配时是否校验 worker 注册的版本——分派匹配观察到的键是 action_id/desired_worker_id/labels/sticky，未见 version 过滤；旧版本在飞任务若被新代码 worker 捡起，是否会跑新代码未证实。
- 未配置 backoff 时 task 重试的默认 delay 具体数值（文档只说 "a short delay"）；未查 engine 常量。
- worker 关闭 grace period 的默认值/可配置项未见数值。

## leads
- https://docs.hatchet.run/v1/bulk-retries-and-cancellations（批量重试/取消，未开）
- sdks/python/hatchet_sdk/worker/action_listener_process.py 注释：worker "stops heartbeats while tasks are still running, causing the engine to reassign"——关闭边缘语义
- v1-olap.sql 有 'REASSIGNED' task 事件枚举；Prometheus 指标 hatchet_tenant_reassigned_tasks
