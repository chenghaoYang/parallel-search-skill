# r1-inngest
question: Inngest 官方文档/官网/仓库中，它的持久化模型、确定性要求、执行模型、许可证、云计费、SDK 语言、外部事件原语、版本升级、副作用语义、官方定位分别是什么（填 D1–D10）
checked: https://github.com/inngest/inngest, https://raw.githubusercontent.com/inngest/inngest/main/LICENSE.md, https://www.inngest.com/docs/learn/how-functions-are-executed, https://www.inngest.com/docs/learn/inngest-steps, https://www.inngest.com/docs/learn/versioning, https://www.inngest.com/docs/self-hosting, https://www.inngest.com/docs/learn/serving-inngest-functions, https://www.inngest.com/docs, https://www.inngest.com/docs/features/inngest-functions/steps-workflows, https://www.inngest.com/docs/reference/functions/step-run, https://www.inngest.com/docs/reference/functions/step-invoke, https://www.inngest.com/docs/reference/functions/step-wait-for-event, https://www.inngest.com/docs/guides/handling-idempotency, https://www.inngest.com/docs/guides/concurrency, https://www.inngest.com/docs/faq, https://www.inngest.com/pricing, https://www.inngest.com/, https://github.com/inngest/inngest-kt, https://github.com/orgs/inngest/repositories?q=inngest, https://api.github.com/repos/inngest/inngest-js, https://raw.githubusercontent.com/inngest/inngest-js/main/packages/inngest/LICENSE.md

## claims

### D1 持久化
- [C1] Cloud：每个 step 结果返回平台并持久化在托管 state store，按 step ID hash 记忆化 | src: https://www.inngest.com/docs/learn/how-functions-are-executed | quote: "the results of each step are returned to Inngest and persisted in a managed function state store" | type: official
- [C2] 自托管为单二进制（`inngest start`，localhost:8288），内部组件含 Event API、event stream、Runner、Queue、Executor、State store、Database、GraphQL/REST API、Dashboard UI | src: https://www.inngest.com/docs/self-hosting | quote: "The Inngest CLI is a single binary that includes all Inngest services and can be run in any environment." | type: official
- [C3] 自托管默认：queue 与 state store 用内嵌内存 Redis，快照定期写入 SQLite `./.inngest/main.db` | src: https://www.inngest.com/docs/self-hosting | quote: "Use an in-memory Redis server for the queue and state store." / "Queue and state store snapshots are periodically saved to the SQLite database" | type: official
- [C4] 可选外部存储：`--redis-uri`/`INNGEST_REDIS_URI`（"Redis server URI for external queue and run state"），`--postgres-uri` 为 "PostgreSQL database URI for configuration and history persistence"；SQLite "does not support scaling beyond a single node" | src: https://www.inngest.com/docs/self-hosting | quote: "PostgreSQL database URI for configuration and history persistence" | type: official

### D2 确定性
- [C5] handler 每轮从头重跑，只注入已完成 step 的记忆化结果；step 之外的代码每次调用都会执行 | src: https://www.inngest.com/docs/learn/how-functions-are-executed | quote: "The function is re-executed, this time with the event payload data and the state of the previous execution in JSON." | type: official
- [C6] 官方要求非确定性逻辑放进 step | src: https://www.inngest.com/docs/learn/how-functions-are-executed | quote: "Any non-deterministic logic (such as DB calls or API calls) must be placed within a step.run() call" | type: official
- [C7] 官方自述与 Temporal 区别：非全函数 replay，而是 step memoization | src: https://www.inngest.com/docs/learn/how-functions-are-executed | quote: "Inngest uses a step-based memoization model where each step runs once, its result is persisted" / "This uses standard language features with no custom runtime rules." | type: official

### D3 执行
- [C8] 平台 HTTP 回调用户 app，无 worker；每个 step 一次 HTTP 请求 | src: https://www.inngest.com/docs/learn/how-functions-are-executed | quote: "Each step in your function is executed as a separate HTTP request." | type: official
- [C9] serve() 为主流接入；另有 Connect 模式（长连接 worker，支持 rolling deploys、appVersion）；自托管时 dev server/CLI 同样经 HTTP 调 app | src: https://www.inngest.com/docs/setup/connect | quote: "connect supports rolling releases: During a deployment of your app, Inngest will run functions on all connected workers" | type: official

### D4 许可证（重要：非纯 Apache）
- [C10] inngest server/CLI 仓库为 SSPL v1.0 + DOSP：3 年后转 Apache 2.0 | src: https://raw.githubusercontent.com/inngest/inngest/main/LICENSE.md | quote: "Server Side Public License, Version 1.0, Oct 16, 2018" / "effective on the third anniversary of the date we make the Software available"（Apache 2.0 Future License） | type: official
- [C11] README 明示 dual license 策略与 SDK 例外 | src: https://github.com/inngest/inngest | quote: "All Inngest SDKs are all available under the Apache 2.0 license." / "Self-hosting the Inngest server is possible and easy to get started with." | type: official
- [C12] SDK license 实证：inngest-js 的 packages/inngest/LICENSE.md 为 Apache 2.0、package.json `"license": "Apache-2.0"`；inngestgo/inngest-py/inngest-kt/inngest-rs 仓库标注 Apache 2.0 | src: https://raw.githubusercontent.com/inngest/inngest-js/main/packages/inngest/LICENSE.md | quote: "Apache License Version 2.0, January 2004" | type: official
- [C13] 自托管 vs Cloud：自托管文档未列功能门控，差异仅提支持 | src: https://www.inngest.com/docs/self-hosting | quote: "Inngest's support team does not guarantee direct support for self-hosted instances" | type: official
- [C14] Cloud 侧企业功能：Enterprise 档含 "SAML, RBAC, audit trails"、Dedicated Slack、trace/log exports；HIPAA 为 Pro/Business add-on、Enterprise 含；Datadog observability $300/mo add-on | src: https://www.inngest.com/pricing | quote: "SAML, RBAC, audit trails" | type: official

### D5 云计费
- [C15] 计费主维度 executions = run + step | src: https://www.inngest.com/pricing | quote: "A function with 5 step.run() calls uses 6 executions total — 1 for the run, 5 for the steps." | type: official
- [C16] 档位：Free $0（50k executions/月、5 seats、5 concurrent steps、500k events）；Pro 起 $99/mo（1M executions，超额 $0.000050→$0.000015/execution）；Business 起 $499/mo（10M）；Enterprise custom | src: https://www.inngest.com/pricing | quote: "from $0.000050 down to $0.000015 per execution" | type: official
- [C17] 其他计量维度：seats、concurrent steps、workers、events ingested、queue depth、event size、realtime connections/messages、span data、scores、trace retention | src: https://www.inngest.com/pricing | quote: (维度行汇总，见 pricing 表) | type: official

### D6 SDK
- [C18] 文档主推三语言 | src: https://www.inngest.com/docs | quote: "Write functions in TypeScript, Python or Go to power background and scheduled jobs, with steps built in." | type: official
- [C19] GitHub org 官方 SDK 仓库：inngest-js（TS/JS）、inngest-py（Python）、inngestgo（Go）、inngest-kt（"Kotlin/Java SDK for Inngest"，README 称 Java "Coming soon"）、inngest-rs（Rust，Apache 2.0） | src: https://github.com/orgs/inngest/repositories?q=inngest | quote: "Kotlin/Java SDK for Inngest" | type: official

### D7 原语
- [C20] step 方法清单：step.run / sleep / sleepUntil / waitForEvent / waitForSignal / invoke / sendEvent；sleepUntil、waitForSignal 无 Go 版；Go 发事件用 client.Send() 包进 step.Run | src: https://www.inngest.com/docs/learn/inngest-steps | quote: "pauses a run's execution until a specific signal is received via our SDK or API" | type: official
- [C21] step.invoke 跨语言调另一函数并等待结果 | src: https://www.inngest.com/docs/reference/functions/step-invoke | quote: "Use step.invoke() to asynchronously call another function and handle the result." | type: official
- [C22] step ID + counter 记忆化，支持循环内同 ID | src: https://www.inngest.com/docs/learn/inngest-steps | quote: "Inngest's SDK also records a counter for each unique step ID. The counter increases every time the same step is called." | type: official
- [C23] 事件触发模型：函数由 event 触发（支持 fan-out 一事件触发多函数、cron 调度） | src: https://www.inngest.com/docs/guides/handling-idempotency | quote: "Events that fan-out to multiple functions will trigger each function as they normally would." | type: official

### D8 版本升级
- [C24] 无版本 pin：进行中 run 跑新部署代码，已完成 step 跨部署记忆化 | src: https://www.inngest.com/docs/learn/versioning | quote: "completed steps are never re-executed, even across deployments" / "determines what to run based on the step identifiers in your code, not version numbers" | type: official
- [C25] 变更规则：加 step 安全（in-progress run 遇到即执行）；同 ID 改逻辑安全；改 ID 强制重跑；删 step 旧状态被忽略；乱序仅告警 | src: https://www.inngest.com/docs/learn/versioning | quote: "Changing step IDs forces re-execution." / "the SDK logs a warning rather than failing the function" | type: official
- [C26] 不兼容重写推荐 "new function pattern with timestamp-based routing"（同事件双函数 + if 表达式），或 event `v` 字段路由 | src: https://www.inngest.com/docs/learn/versioning | quote: "In-progress runs complete with the original logic" / "New events trigger the updated function" | type: official

### D9 副作用语义
- [C27] step 独立重试计数，默认 4 次重试（共 5 次尝试）→ 语义为 at-least-once（官网页面未直接使用该词） | src: https://www.inngest.com/docs/reference/functions/step-run | quote: "each step.run() will be retried up to 4 times independently (5 total attempts including the initial attempt)" | type: official
- [C28] step 是代码级事务：整体成功才完成 | src: https://www.inngest.com/docs/learn/inngest-steps | quote: "step.run() acts as a code-level transaction. The entire step must succeed to complete." | type: official
- [C29] 事件去重：event `id` 为 24h 幂等键；函数级 `idempotency` CEL 表达式 24h 去重；debounce/batch/pause 时忽略 | src: https://www.inngest.com/docs/guides/handling-idempotency | quote: "Event IDs will only be used to prevent duplicate execution for a 24 hour period." | type: official
- [C30] 并发控制作用于 step 级（key → 每 key 虚拟队列）；throttle 在函数级 | src: https://www.inngest.com/docs/guides/concurrency | quote: "Inngest's concurrency control enables you to manage the number of *steps* that concurrently execute." / "Throttling is applied at the function level, compared to concurrency which is at the step level" | type: official

### D10 定位
- [C31] 官网定位：durable execution for workflows & AI，强调无 worker/队列 | src: https://www.inngest.com/ | quote: "Unbreakable Agents. Invisible Infra." / "From background jobs to agents, in one codebase." | type: official
- [C32] GitHub README 定位 | src: https://github.com/inngest/inngest | quote: "Run stateful step functions and AI workflows on serverless, servers, or the edge." | type: official

## conflicts
- GitHub API 把 inngest-js 仓库 license 识别为 "gpl-3.0"（api.github.com/repos/inngest/inngest-js），但仓库树中无任何 GPL LICENSE 文件，发布的 npm 包 LICENSE.md/package.json 均为 Apache-2.0 —— 疑似 GitHub 检测陈旧；不影响「SDK 均为 Apache 2.0」结论。
- 用户假设「Inngest 开源 Apache 2.0」对 server 不成立：server 是 SSPL+DOSP（3 年后转 Apache），自托管商用需注意 SSPL 第 13 条（as-a-service 提供限制）。

## gaps
- 自托管二进制里 SSO/审计等企业功能是否被编译剔除/门控，官方文档未明说（pricing 只列 Cloud 档位差异；self-hosting 页只提 support 差异）。
- step.ai.* 原语（ai.infer/ai.wrap）仅在 step-run 参考页导航出现，未取到描述原文。
- inngest-rs（Rust）在 org 内但文档未列出，成熟度/官方状态未确认。

## leads
- connect 模式 + checkpointing（step 级 checkpoint 恢复）是 2025–2026 新执行路径，值得单独查。
- 官网新增 "Durable Endpoints"（普通 HTTP handler 内嵌 step.run），文档出现 "guarantee that each step completes exactly once" 营销表述（examples/durable-endpoints，未直接核对）。
