# r1-hatchet
question: Hatchet 的持久化模型、确定性要求、执行模型、许可证、云计费、SDK 语言、外部事件原语、版本升级、副作用语义、官方定位（D1–D10）
checked: docs.hatchet.run, docs.hatchet.run/llms.txt, /v1/tasks, /v1/workers, /v1/durable-execution, /v1/durable-tasks, /v1/durable-sleep, /v1/durable-event-waits, /v1/directed-acyclic-graphs, /v1/architecture-and-guarantees, /v1/idempotency, /v1/concurrency, /v1/rate-limits, /v1/events, /v1/cron-runs, /v1/scheduled-runs, /v1/webhooks, /v1/advanced-assignment/sticky-assignment, /v1/migrating/migration-guide-engine, /self-hosting, /self-hosting/upgrading-downgrading, /reference/changelog/platform, hatchet.run, hatchet.run/pricing, github.com/hatchet-dev/hatchet

## claims

D1 persistence:
- [C1] Postgres is the durable store; RabbitMQ optional | src: https://docs.hatchet.run/v1/architecture-and-guarantees | quote: "State is stored durably (PostgreSQL is the source of truth)." / "you can start with PostgreSQL-only and add components like RabbitMQ if you need higher throughput" | type: official
- [C2] Postgres backs both runtime and observability | src: https://github.com/hatchet-dev/hatchet | quote: "it uses Postgres as a durability layer for both the task runtime and the observability system" | type: official
- [C3] Self-host components: API server, engine, Postgres, optional RabbitMQ, dashboard; Lite=single image | src: https://docs.hatchet.run/self-hosting | quote: "RabbitMQ for inter-service communication and high-throughput real-time updates" (listed optional); "Single docker image with bundled engine and API" | type: official
- [C4] Postgres queue kind is Lite default/fallback; RabbitMQ optional since v0.73.4 (2025-09-16) | src: https://docs.hatchet.run/reference/changelog/platform | quote: "Allow RabbitMQ to be used with Hatchet Lite"; "fallback to using the `postgres` message queue kind" | type: official

D2 determinism:
- [C5] Durable tasks DO require determinism between checkpoints | src: https://docs.hatchet.run/v1/durable-tasks | quote: "the code between checkpoints must be deterministic"; "If a branch is taken on the first run, it must be taken again on replay"; "Push side effects into child tasks" | type: official
- [C6] Regular/DAG tasks: "a task is just a function", no determinism constraint stated | src: https://docs.hatchet.run/v1/tasks | quote: "The fundamental unit of work in Hatchet is a **task**"; "a task is just a function" | type: official
- [C7] Task→task data passing via parent outputs on ctx: `ctx.task_output(step)` (Py/Ruby), `ctx.parentOutput(t)` (TS), `ctx.ParentOutput(t,&out)` (Go) | src: https://docs.hatchet.run/v1/directed-acyclic-graphs | quote: "the outputs of its parents are available on its context object" | type: official
- [C8] additional_metadata is for CEL keys/metadata (concurrency keys, rate limits, cron metadata), not documented as task-data channel | src: https://docs.hatchet.run/v1/concurrency | quote: "can reference the `input` to the workflow and the `additional_metadata`" | type: official

D3 execution:
- [C9] Workers are long-running processes; engine dispatches over worker-initiated bidirectional gRPC (push over stream, not polling) | src: https://docs.hatchet.run/v1/architecture-and-guarantees | quote: "Workers connect to the engine over bidirectional gRPC"; "schedules ready tasks and dispatches them to connected workers" | type: official
- [C10] Worker slots default 100, local concurrency limit | src: https://docs.hatchet.run/v1/workers | quote: "The default slot count for workers in Hatchet is 100" | type: official
- [C11] Local run = `hatchet server start` CLI; deploys: Hatchet Lite / docker-compose / Helm | src: https://docs.hatchet.run/self-hosting | type: official

D4 license:
- [C12] MIT | src: https://github.com/hatchet-dev/hatchet | quote: "MIT license"; homepage: "Fully MIT-licensed" (https://hatchet.run) | type: official

D5 cloud billing:
- [C13] Per-task-run billing: Developer free, "$10 per 1M task runs", first 100k runs included; Team $500/mo (10 users, 5 tenants, 3-day retention, 500 RPS); Scale $1,000/mo (unlimited users/tenants, 7-day retention, HIPAA); Enterprise custom | src: https://hatchet.run/pricing | quote: "$10 per 1M task runs"; "Unlimited users & tenants" | type: official

D6 SDKs:
- [C14] Python, TypeScript, Go, Ruby | src: https://github.com/hatchet-dev/hatchet | quote: "It supports applications written in Python, TypeScript, Go and Ruby" | type: official

D7 primitives:
- [C15] DAG via `parents=`; parallel where no dependency | src: https://docs.hatchet.run/v1/directed-acyclic-graphs | quote: "Tasks that don't depend on each other will be run in parallel" | type: official
- [C16] Durable task = checkpointed event log; waits + child spawning; evictable while waiting | src: https://docs.hatchet.run/v1/durable-tasks | quote: "Every time one of those happens, Hatchet writes a checkpoint to the durable event log" | type: official
- [C17] Durable sleep: `ctx.aio_sleep_for`/`sleepFor`/`SleepFor`/`sleep_for`; "no resources are consumed, and the task can also be evicted" | src: https://docs.hatchet.run/v1/durable-sleep | type: official
- [C18] Event waits: `ctx.aio_wait_for_event`/`waitForEvent`/`WaitForEvent`, Ruby `ctx.wait_for("event", UserEventCondition)`; CEL filter expr; scope + lookback | src: https://docs.hatchet.run/v1/durable-event-waits | type: official
- [C19] Event triggers `on_events`/`onEvents`, wildcards `subscription:*` (v0.65.0+); push via `hatchet.events.push`; filters with `scope` + CEL over input/payload/additional_metadata/event_key | src: https://docs.hatchet.run/v1/events | type: official
- [C20] Managed inbound webhooks: Hatchet-hosted URL per tenant+name; CEL "Event Key Expression" over input+headers; Basic/API-key/HMAC auth; Stripe/GitHub presets | src: https://docs.hatchet.run/v1/webhooks | quote: "allow external systems to trigger Hatchet workflows by sending HTTP requests to dedicated endpoints" | type: official
- [C21] Cron: `on_crons`/`on: {cron}`/`WithWorkflowCron`; 5- or 6-field exprs (6th=seconds); UTC; missed runs not replayed; enqueue-time semantics | src: https://docs.hatchet.run/v1/cron-runs | quote: "Hatchet will **not** automatically run the missed instances" | type: official
- [C22] One-off scheduled runs: `simple.schedule(datetime)` / `client.Schedules().Create` | src: https://docs.hatchet.run/v1/scheduled-runs | quote: "allow you to trigger a task at a specific time in the future" | type: official
- [C23] Concurrency: GROUP_ROUND_ROBIN, CANCEL_IN_PROGRESS, CANCEL_NEWEST, CANCEL_QUEUED_EXCEPT_NEWEST, CANCEL_QUEUED_EXCEPT_OLDEST; CEL keys; shared + dynamic max_runs (engine 0.106.0+) | src: https://docs.hatchet.run/v1/concurrency | type: official
- [C24] Rate limits: static (`rate_limits.put`) + dynamic (`dynamic_key` CEL upsert at runtime), units/weights; over-limit step runs re-queued | src: https://docs.hatchet.run/v1/rate-limits | quote: "Hatchet re-queues the step run until the rate limit is no longer exceeded" | type: official
- [C25] Sticky assignment SOFT/HARD pins children to same worker (beta; not for webhook workers) | src: https://docs.hatchet.run/v1/advanced-assignment/sticky-assignment | type: official
- [C26] Also documented: priorities, timeouts, streaming, task eviction, bulk retries/cancellations | src: https://docs.hatchet.run/llms.txt (paths /v1/priority /v1/timeouts /v1/streaming /v1/task-eviction /v1/bulk-retries-and-cancellations) | type: official

D8 versioning/upgrades:
- [C27] Workflow version is created per worker registration; APIs `workflows.get_version`, `ctx.workflow_version_id`; changing task config (e.g. slot cost) creates new version | src: https://docs.hatchet.run/v1/advanced-assignment/slot-cost | quote: "Changing a task's slot cost changes its workflow version, so the next registration creates a new version" | type: official
- [C28] v0→v1 (self-host >0.55.11): in-flight runs NOT migrated — run new v1 tenant, drain v0; v0 SDK bundled until 2025-09-30; v0 now removed | src: https://docs.hatchet.run/v1/migrating/migration-guide-engine | quote: "upgrading to the v1 engine will **not migrate your existing workflow runs**, including runs which are in a Running or Queued state" | type: official
- [C29] Engine upgrades auto-run DB migrations on startup; downgrade = snapshot restore, "data loss and some downtime" | src: https://docs.hatchet.run/self-hosting/upgrading-downgrading | quote: "Hatchet runs database migrations automatically on engine startup" | type: official

D9 side effects:
- [C30] At-least-once execution; user code must be idempotent | src: https://docs.hatchet.run/v1/architecture-and-guarantees | quote: "Hatchet is **at least once**: tasks are not silently dropped"; "a task can run more than once, so your task code should be idempotent" | type: official
- [C31] Idempotency keys: TTL-based + status-based, CEL key_expression; collision raises `IdempotencyCollisionError` w/ `existing_run_external_id`; event-triggered collisions swallowed | src: https://docs.hatchet.run/v1/idempotency | type: official
- [C32] Retries configurable w/ backoff | src: https://hatchet.run | quote: "Retries with flexible and configurable policies, such as exponential backoff" | type: official

D10 positioning:
- [C33] "An orchestration engine for background tasks, AI agents, and durable workflows" (repo); homepage "The orchestration engine for teams who ship"; README calls it "a _durable_ task queue" | src: https://github.com/hatchet-dev/hatchet; https://hatchet.run | type: official
- [C34] Selling points: fairness/concurrency policies, rate limits, priorities; AI-agent workloads; "374M / Tasks run daily on Hatchet Cloud"; Celery/Temporal migration guides | src: https://hatchet.run; https://docs.hatchet.run/v1/from-temporal-to-hatchet | type: official

## conflicts
- Exactly-once vs at-least-once wording: /v1/durable-tasks says checkpoint replay gives tasks "exactly-once semantics which you wouldn't get with many other task queue implementations"; /v1/architecture-and-guarantees says "Hatchet is **at least once**". Reading: exactly-once refers to intra-task checkpoint replay (no re-run of completed logic); task execution itself is at-least-once.
- /v1/durable-execution (overview) contains no determinism requirement, but /v1/durable-tasks has a dedicated "Determinism in durable tasks" section — determinism applies only to durable tasks' inter-checkpoint code, not to regular DAG tasks.

## gaps
- Whether a running workflow run stays pinned to its original workflow version after a new version registers — implied by `workflow_version_id` but not stated on checked pages.
- Worker heartbeat/failure-reassignment mechanics not detailed on architecture page.
- Earliest changelog entry introducing postgres task-queue option predates truncated page (earliest seen: v0.73.4, 2025-09-16).
- Retry policy page (/v1/retry-policies) not opened; backoff detail only from homepage.

## leads
- Hatchet Lite + `hatchet server start` = zero-dependency local dev story (Go SDK can run engine in-process via `hatchet.WithEmbeddedPostgres`).
- /v1/from-temporal-to-hatchet migration guide exists — useful for positioning comparison vs Temporal.
