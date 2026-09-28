# r2-temporal
question: Temporal Cloud 计费单位 "action" 的官方定义（哪些操作算 action）；Temporal 各 SDK 仓库 license 抽查。
checked: https://docs.temporal.io/cloud/pricing, https://docs.temporal.io/evaluate/cloud/actions, https://api.github.com/repos/temporalio/{sdk-python,sdk-java,sdk-typescript,sdk-go,sdk-dotnet,sdk-ruby,sdk-php,sdk-rust}, raw.githubusercontent.com LICENSE files for same 8 repos

## claims

### Action 定义（docs.temporal.io/evaluate/cloud/actions）
- [C1] Action 是 Temporal Cloud 消费计费的基本单位 | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "Actions are the primary unit of consumption-based pricing for Temporal Cloud" | type: official
- [C2] Action 追踪 Cloud 内可计费操作，如启动 Workflow、记 Heartbeat、发 Signal | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "track billable operations within the Temporal Cloud Service, such as starting Workflows, recording a Heartbeat, or sending Signals" | type: official
- [C3] Action 分 8 大类：Workflow、Activity、Timer、Signal、Query、Update、Schedule、Nexus，外加 Export、Fairness、Capacity | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "Workflow, Activity, Timer, Signal, Query, Update, Schedule, Nexus" plus "Export, Fairness, and Capacity" | type: official
- [C4] Workflow started 计 1 个 Action，含 client start、Continue-As-New、Child Workflow start；按 Workflow ID 去重的重复 start 不计 | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "Occurs via client start, Continue-As-New, Child Workflow start" / "De-duplicated Workflow starts that share a Workflow ID do not count as an Action" | type: official
- [C5] Start Child Workflow 计 2 个 Action | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "one for durably storing the intent to start a Child Workflow and one for the attempt to start it" | type: official
- [C6] Activity 每次启动或重试计 1 个 Action（Workflow Activity 与 Standalone Activity 均算） | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "Occurs each time a Workflow Activity or Standalone Activity is started or retried" | type: official
- [C7] Activity Heartbeat 只有到达 Temporal Server 才计 Action；SDK 按 Heartbeat Timeout 的 80% 节流 | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "counts as an Action only if it reaches the Temporal Server" | type: official
- [C8] 同一 Workflow Task 内所有 Local Activity 合计只算 1 个 Action | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "All Local Activities associated with one Workflow Task count as a single Action" | type: official
- [C9] Timer started 计 Action，含 SDK 因超时设置隐式创建的 Timer（Go `AwaitWithTimeout`、TS `condition`） | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "Includes implicit Timers that are started by a Temporal SDK when timeouts are set" | type: official
- [C10] 每个 Signal 计 1 Action（client 或 workflow 发出均算）；Signal-With-Start 无论是否真启动只算 1 | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "one total action occurs for any Signal-With-Start, regardless of whether the Workflow starts" | type: official
- [C11] 每个到达 Worker 的 Query 计 1 Action，含 Cloud UI 查看 call stack；内置 `__temporal_workflow_metadata` 除外 | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "An Action occurs for every Query, including viewing the call stack in the Temporal Cloud UI" | type: official
- [C12] 每个成功和被拒绝的 Update 都计 Action；按 Update ID 去重的不计 | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "Occurs for every successful Update and every rejected Update" / "De-duplicated Updates that share an Update ID do not count as an Action" | type: official
- [C13] 每次 Schedule 执行计 3 个 Action（Schedule Start 2 个 + 目标 Workflow started 1 个） | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "Each execution of a Schedule accrues three Actions" | type: official
- [C14] Nexus Operation 每次 schedule 或 cancel 在 caller Namespace 计 1 Action；handler 侧底层原语（workflow/activity/signal）照常计费 | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "not for handling the Nexus Operation itself or a retry of the Nexus Operation itself" | type: official
- [C15] Workflow Replay 期间的 Action 不计费；History Event Type 与 Action Type 非 1:1 映射 | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "do not count towards billed Actions" / "do not always map 1:1 to Action Types" | type: official
- [C16] UpsertSearchAttributes 每次调用计 1 Action（一次更新多个 SA 仍算 1）；Workflow 启动时设置的 SA 与 TemporalChangeVersion 除外 | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "Multiple Search Attributes updated in a single UpsertSearchAttributes command count as one Action" | type: official
- [C17] 每个导出的 Workflow 计 1 Action（Export）；Fairness 开启时每 Action 加收 0.1 | src: https://docs.temporal.io/evaluate/cloud/actions | quote: "Each Workflow exported accrues a single action" / "an additional 0.1 Action is charged per Action in the Namespace" | type: official
- [C18] HA replica 对被复制 Namespace 的 Actions 与 Storage 施加 2x 乘数 | src: https://docs.temporal.io/cloud/pricing | quote: "apply a 2x multiplier to the Actions and Storage in the Namespace you are replicating" | type: official
- [C19] Provisioned Capacity 不足最低量时系统按 `ns_capacity:tru` 子类型补记 Action 至配额 | src: https://docs.temporal.io/cloud/pricing | quote: "Actions of the subtype ns_capacity:tru will be recorded to the required volume" | type: official
- [C20] 计费页明确把 action 明细指向独立 Actions 页，自身只给高层定义 | src: https://docs.temporal.io/cloud/pricing | quote: "Specific Billable Actions are discussed on the Actions page" | type: official

### SDK license 抽查（github.com/temporalio，GitHub API spdx_id + LICENSE 首行）
- [C21] sdk-python：MIT | src: https://github.com/temporalio/sdk-python/blob/main/LICENSE | quote: "The MIT License  Copyright (c) 2022 Temporal Technologies Inc." | type: official
- [C22] sdk-java：Apache-2.0（8 个抽查 SDK 中唯一非 MIT） | src: https://github.com/temporalio/sdk-java/blob/main/LICENSE | quote: "Apache License Version 2.0, January 2004" | type: official
- [C23] sdk-typescript：MIT | src: https://github.com/temporalio/sdk-typescript/blob/main/LICENSE | quote: "The MIT License  Copyright (c) 2021-2025 Temporal Technologies Inc." | type: official
- [C24] sdk-go：MIT | src: https://github.com/temporalio/sdk-go/blob/master/LICENSE | quote: "The MIT License  Copyright (c) 2020 Temporal Technologies Inc." | type: official
- [C25] sdk-dotnet：MIT | src: https://github.com/temporalio/sdk-dotnet/blob/main/LICENSE | quote: "The MIT License  Copyright (c) 2022 Temporal Technologies Inc." | type: official
- [C26] sdk-ruby：MIT | src: https://github.com/temporalio/sdk-ruby/blob/main/LICENSE | quote: "The MIT License  Copyright (c) 2024 Temporal Technologies Inc." | type: official
- [C27] sdk-php：MIT | src: https://github.com/temporalio/sdk-php/blob/master/LICENSE.md | quote: "The MIT License  Copyright (c) 2020 Temporal Technologies Inc." | type: official
- [C28] sdk-rust：MIT | src: https://github.com/temporalio/sdk-rust/blob/main/LICENSE.txt | quote: "The MIT License  Copyright (c) 2021 Temporal Technologies, Inc." | type: official

## conflicts
- 无。R1 所述 "actions 定义难懂" 与本页一致：定义分散、metric name 与 History Event Type 非 1:1（C15），属结构复杂而非文档矛盾。

## gaps
- 未逐条核对 Actions 页全部 metric name 表（仅摘录了代表性条目）；如成稿需完整 usage→metric 对照表需再取。
- sdk-core / api / cli 等其余 temporalio 仓库 license 未查（不在简报抽查清单）。
- Action 定价分层（$50/M 之后的梯度）属 R1 格子，未重复查。

## leads
- Actions 页存在 metric name（如 `start_workflow`、`record_activity_heartbeat`），可作计费审计/对账字段；Billing API 不提供 Action Category/Type 维度（"Action Categories and Action Types are not available in the Billing API"）。
- sdk-java 的 Apache-2.0 是 license 矩阵里的唯一例外，成稿若统一写 "SDK 全 MIT" 会错。
