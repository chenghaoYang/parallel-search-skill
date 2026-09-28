# grid — 实体 × 维度（状态：✅一手 ⚠二手 ⚔冲突 ❓缺口 ∅官方未写 —不适用）

维度（每个维度回答一个问题）：
- D1 持久化模型：执行状态记在哪、崩溃后怎么恢复？
- D2 代码确定性：哪部分代码必须确定性？引擎给什么兜底 API？
- D3 许可证与自托管：server/SDK 许可证、自托管限制？
- D4 托管云与计费：按什么计费？
- D5 SDK 语言：覆盖与成熟度？
- D6 等待外部世界：signal/event/sleep/cron 原语语义？
- D7 版本与升级：代码改了 in-flight 执行怎么办？
- D8 幂等与副作用：副作用执行几次？exactly-once 到哪层？
- D9 编程与部署形态：要跑哪些组件？DSL vs 内嵌？
- D10 执行语义定位：编排/队列/durable RPC？

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Temporal | ✅event history+replay | ✅workflow 必须确定，TS 沙箱换 random/Date | ✅server MIT | ✅Actions+存储，$50/M 起 | ✅8 SDK | ✅Signal/Query/Update/Await/Timer | ✅patching+Worker Versioning | ✅ALO/AMO，幂等归开发者 | ✅server+DB+UI | ✅编排运行时+job queue |
| Restate | ✅journal+Bifrost/RocksDB | ✅handler 确定，ctx.run/ctx.rand | ✅server BUSL-1.1/SDK MIT | ⚠usage-based，50k 免费；价目 secondary | ✅TS/JVM/Py/Go/Rust(+Ruby) | ✅awakeable/signal/promise/sleep | ✅immutable deployment+journal 兼容 | ✅invocation EO；ctx.run 副作用重试 | ✅单二进制，无 Kafka/PG | ✅durable RPC/actor |
| DBOS | ✅PG checkpoint 跳步恢复 | ✅workflow 函数确定；无 helper API(∅3页） | ✅SDK MIT；Conductor 商业 | ✅Conductor $99/$499 按 checkpoint；Cloud 询价 | ✅Py/TS/Go/Java | ✅send/recv/set_event/sleep/cron+backfill | ✅patch marker+app-version hash | ✅step ALO；入口 EO（id/调度/消息） | ✅纯库+Postgres | ✅lightweight 库 |
| Inngest | ✅step memoize，平台态存储 | ✅非确定逻辑进 step.run（memoize 非严格 replay） | ✅server SSPL+DOSP/SDK Apache | ✅executions=runs×(steps+1)，$99 起 | ✅TS/Py/Go(+kt/rs 未明） | ✅waitForEvent/invoke/sleep≤1yr/cron 去重 | ✅step-id 哈希 memoize | ✅step 成功不重跑；event.id 24h | ✅serve/connect+单二进制自托管 | ✅event-driven durable functions |
| Hatchet | ✅PG 事务化+checkpoint/event log | ✅durable task checkpoint 间须确定；DAG 无约束 | ✅MIT | ✅$10/M task runs；$500/$1k 档 | ✅Py/TS/Go/Ruby | ✅waitForEvent+CEL/sleep/cron（不补跑） | ⚠无 patching 靠 drain；in-flight 钉版本无明文 | ✅task ALO+TTL/CEL 幂等键 | ✅worker+engine；Lite 单镜像/embedded | ✅队列+DAG+durable 三合一 |

关键冲突/边界：
- Hatchet durable task 确定性要求（推翻 R1 假设）✅已确认
- Inngest self-host cloud-only 工具（self-hosting 页未列 vs MCP 页列出）⚔ 已记
- exactly-once 口径：Temporal 无此承诺（∅已查页）/ Restate invocation 级 / DBOS 入口级 / AWS Standard 状态机级
- 分类轴 v1：恢复机制（event-replay vs step-journal/checkpoint）× 状态载体（专有server/自包含二进制/Postgres/平台态）× 编程模型（DSL分离/装饰器step/step.*/DAG+task/actor-handler）——能解释全部 5 家差异

待查（R2 候选）：
- 反证：Temporal/Inngest「无 exactly-once」否定主张；DBOS「无 helper API」；Restate/Inngest 自托管「无功能限制」
- Restate 官方 pricing 数字（JS 页未取）
- Hatchet in-flight 版本钉住明文
- scout leads：Vercel Workflow/Resonate/Golem/LittleHorse 已收为相邻实体，不进矩阵
