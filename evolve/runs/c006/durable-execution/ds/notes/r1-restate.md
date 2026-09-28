# r1-restate
question: Restate 官方文档/官网/仓库中，持久化模型、确定性要求、执行模型、许可证、云计费、SDK 语言、外部事件原语、版本升级、副作用语义、官方定位（D1–D10）。
checked: https://github.com/restatedev/restate, https://github.com/restatedev/restate/blob/main/LICENSE, https://api.github.com/repos/restatedev/restate/commits?path=LICENSE, https://api.github.com/repos/restatedev/restate/commits/35ff8e0f5d, https://github.com/restatedev/restate/issues/654, https://github.com/restatedev/sdk-typescript/blob/main/LICENSE, https://github.com/restatedev/sdk-java/blob/main/LICENSE, https://github.com/restatedev/sdk-python/blob/main/LICENSE, https://docs.restate.dev/, https://docs.restate.dev/concepts/durable_execution, https://docs.restate.dev/foundations/actions, https://docs.restate.dev/foundations/invocations, https://docs.restate.dev/foundations/services, https://docs.restate.dev/foundations/key-concepts, https://docs.restate.dev/references/architecture, https://docs.restate.dev/services/versioning, https://docs.restate.dev/develop/ts/durable-steps, https://restate.dev/pricing (+其 Next.js JS chunk)

## claims

### D1 持久化
- [C1] 每次执行每步结果记入 journal，崩溃重放跳过已完成步骤 | src: https://docs.restate.dev/concepts/durable_execution | quote: "Restate tracks every step of your code execution in a journal." / "Restate replays the journal, skipping completed steps and resuming from exactly where it left off." | type: official
- [C2] 持久化真源是分布式日志 Bifrost，quorum 提交 | src: https://docs.restate.dev/references/architecture | quote: "The log is the primary durability layer" / "A write is committed when a quorum of replicas acknowledges the append." | type: official
- [C3] 每个 processor 内嵌 RocksDB 作 journal/状态/幂等元数据/定时器的物化缓存，可从日志重建 | src: https://docs.restate.dev/references/architecture | quote: "maintains a materialized state cache in an embedded RocksDB" / "This cache is derivative—it can always be rebuilt from the log—and is not a second source of truth." | type: official
- [C4] 元数据用内置 Raft；RocksDB 分区快照上传 S3 以限恢复时间+日志裁剪 | src: https://docs.restate.dev/references/architecture | quote: "a built-in Raft-based metadata store" / "Processors create periodic snapshots of their RocksDB partition store and upload them to S3" | type: official
- [C5] Virtual Object/Workflow 的 K/V 状态由 server 内嵌存储保存、按 key 隔离 | src: https://docs.restate.dev/foundations/key-concepts | quote: "Each Virtual Object and Workflow execution has its own isolated state." / "The Restate Server stores all state and execution history, delivering them with each request." | type: official

### D2 确定性
- [C6] 非确定性操作（DB 调用、HTTP、UUID 生成）必须包进 ctx.run；其余普通代码不要求额外确定性约束 | src: https://docs.restate.dev/develop/ts/durable-steps | quote: "Non-deterministic operations (database calls, HTTP requests, UUID generation) must be wrapped to ensure deterministic replay." | type: official
- [C7] ctx.run 结果持久化进执行日志；run 块内不能再用 ctx | src: https://docs.restate.dev/develop/ts/durable-steps | quote: "have Restate store its result in the execution log" / "inside ctx.run, you cannot use the Restate context" | type: official
- [C8] 不包 run 的后果是重放结果不一致 | src: https://docs.restate.dev/foundations/actions | quote: "Without run(), these operations would produce different results during replay, breaking deterministic recovery." | type: official
- [C9] ctx.rand.uuidv4()/ctx.rand.random()/ctx.date.now() 提供重试下稳定值 | src: https://docs.restate.dev/develop/ts/durable-steps | quote: "return the same result on retries" | type: official

### D3 执行模型
- [C10] Restate server 主动推送调用到用户 service endpoint（双向流），非 worker pull | src: https://docs.restate.dev/references/architecture | quote: "invokes your handler code via a bidirectional stream" / "pushes the initial invoke journal entry to the handler" | type: official
- [C11] 服务部署在 endpoint 之后，须向 Restate 注册 endpoint 以便路由 | src: https://docs.restate.dev/foundations/services | quote: "you must register that endpoint with Restate so it can discover and route requests to it" | type: official
- [C12] 调用入口三条路：HTTP ingress、typed clients、Kafka topics | src: https://docs.restate.dev/foundations/invocations | quote: "There are three ways to invoke a handler: over HTTP, using typed clients, or through Kafka topics." | type: official
- [C13] 单二进制即可跑全部功能；集群按角色拆分（metadata-server, http-ingress, log-server, worker）；无外部共识依赖（内置 Raft），快照可选外部对象存储 | src: https://docs.restate.dev/references/architecture | quote: "all the essential features in a single process" / "Roles control which features run on any given node" / "a single binary with minimal upfront configuration needs" | type: official
- [C14] 服务可无状态横向扩容、可跑在 Lambda/Vercel/Cloudflare Workers 等 FaaS 上（versioning 页列 Lambda ARN 注册） | src: https://docs.restate.dev/services/versioning | quote: "For AWS Lambda, use the function ARN instead of a URL." | type: official

### D4 许可证
- [C15] restatedev/restate（server）为 Business Source License 1.1；许可方 Restate Software, Inc., Restate GmbH；Change Date「发布后 4 年」转 Apache-2.0 | src: https://github.com/restatedev/restate/blob/main/LICENSE | quote: "Business Source License 1.1" / "Change Date: 4 years after release" / "Change License: Apache License, Version 2.0" | type: official
- [C16] 唯一限制：不得用于「Public Restate Platform Service」（让第三方注册/调用自己 deployment 的托管服务）；自用、自托管、分布式均不受限 | src: https://github.com/restatedev/restate/blob/main/LICENSE | quote: "you may not use the Licensed Work for an Application Platform Service"（2025-06 更名为 Public Restate Platform Service 并澄清定义） | type: official
- [C17] LICENSE 自述「is not an Open Source license」，但到期转 Apache-2.0 | src: https://github.com/restatedev/restate/blob/main/LICENSE | quote: "The Business Source License … is not an Open Source license. However, the Licensed Work will eventually be made available under an Open Source License" | type: official
- [C18] 许可历史：2023-08-03 提交「Put Restate under Business Source License」首次加入 LICENSE（fix #654）；此前仓库无 LICENSE 文件（#654 标题「Set up license for Restate」，仅任务清单，未提旧许可证）；其后仅版权年份/措辞更新，未见再变更 | src: https://api.github.com/repos/restatedev/restate/commits?path=LICENSE | quote: "35ff8e0f5d 2023-08-03 Put Restate under Business Source License" | type: official
- [C19] SDK 许可证宽松：sdk-typescript、sdk-java MIT (c) 2023；sdk-python MIT (c) 2024 | src: https://github.com/restatedev/sdk-typescript/blob/main/LICENSE | quote: "MIT License" | type: official

### D5 云计费（restate.dev/pricing，数字取自页面 JS chunk，单位文本为页面原文）
- [C20] 计费单位为 durable action：每次 durable invocation 计 2 个 action（invocation+completion）加中间 durable action；含数据负载的 action 每 64KiB 起计 1 个 | src: https://restate.dev/pricing | quote: "Each durable invocation counts as 2 actions (invocation + completion) plus its intermediate durable actions." / "consume one action per started 64KiB of data" | type: official
- [C21] 套餐：Free $0 含 100k actions/月、burst 100/s、1GB；Starter $75/月 含 5M、500/s、5GB；Business $300/月 含 20M、1000/s、20GB；Premium $1,000/月 含 50M、2000/s、50GB；Enterprise 定制（burst 至 100k/s） | src: https://restate.dev/pricing | quote: 'name:"Free",priceLabel:"Free",monthly:0,includedActions:1e5 … "Starter" "$75" 5e6 … "Business" "$300" 2e7 … "Premium" "$1,000" 5e7 … "Enterprise" "Custom"' | type: official
- [C22] 超量按百万 action 计费，高档有折扣；超额存储 $0.5/GB；低档 overage $25/百万，Premium 段 $15/M（→100M）、$10/M（→200M） | src: https://restate.dev/pricing | quote: "usage beyond that is billed per million, with volume discounts on higher tiers" | type: official
- [C23] 另有 BYOC 选项；官方称「BYOC can also be up to 10× cheaper at scale」 | src: https://restate.dev/pricing | quote: "Choose fully-managed Restate Cloud or Bring Your Own Cloud (BYOC)." | type: official

### D6 SDK
- [C24] 文档 SDK 列表 7 个：TypeScript、Java、Kotlin、Python、Go、Rust、Ruby（Rust 链 docs.rs，Ruby 链 GitHub）；未列 .NET | src: https://docs.restate.dev/ | quote: "TypeScript, Java, Kotlin, Python, Go, Rust, and Ruby" | type: official

### D7 原语
- [C25] signal：按 invocation ID+名字寻址的 durable 通知，可多次 resolve；awakeable：一次性 signal，外部系统经 Restate resolve/reject，「similar to a task token」；workflow promise：按 workflow key 命名、只能 resolve/reject 一次、可被全 handler 读 | src: https://docs.restate.dev/foundations/actions | quote: "A durable notification addressed by invocation ID and signal name." / "A convenient shorthand for a one-shot signal" / "A named value scoped to a workflow key" | type: official
- [C26] ctx.sleep durable timer：睡眠不耗资源、跨重启准点恢复 | src: https://docs.restate.dev/foundations/actions | quote: "Handlers consume no resources while sleeping and resume at exactly the right time, even across restarts" | type: official
- [C27] Virtual Object：按 key 寻址的有状态实体，每 key 同时至多一个写 handler | src: https://docs.restate.dev/foundations/services | quote: "Stateful entities identified by a unique key." / "At most one handler with write access can run at a time per object key." | type: official
- [C28] Workflow：run handler 每 workflow ID 恰好执行一次；shared handler 并发 resolve workflow promise | src: https://docs.restate.dev/foundations/services | quote: "The run handler executes exactly once per workflow ID" / "Shared handlers run concurrently with the run handler to resolve workflow promises" | type: official

### D8 版本升级
- [C29] deployment 不可变：每版代码一个唯一 endpoint 并注册；运行中 invocation 钉在原 deployment，重试也发回同一 endpoint；新请求路由到最新 deployment | src: https://docs.restate.dev/services/versioning | quote: "you give it an immutable, unique endpoint and register it with Restate" / "Restate then makes sure that requests start and end on the same version" / "Existing requests continue on the original deployment" | type: official
- [C30] 因 invocation 钉版本，代码里「no version compatibility logic is needed」；注册用 `restate deployments register http://…`，Lambda 用 ARN | src: https://docs.restate.dev/services/versioning | quote: "no version compatibility logic is needed" | type: official

### D9 副作用语义
- [C31] 官方宣称服务间调用「guaranteed execution and exactly-once semantics」 | src: https://docs.restate.dev/ | quote: "Call services sync or async with guaranteed execution and exactly-once semantics" | type: official
- [C32] 幂等：请求头 `idempotency-key` 去重；重试返回首个 invocation 结果或 attach | src: https://docs.restate.dev/foundations/invocations | quote: "Add an idempotency key to your request header to let Restate deduplicate retries" / "On retry, Restate returns the first invocation's result or lets you attach to it" | type: official
- [C33] ctx.run 失败同普通 handler 错误：默认重试，可配次数/时限；耗尽抛 TerminalError | src: https://docs.restate.dev/develop/ts/durable-steps | quote: "Restate will retry it unless configured otherwise or unless a TerminalError is thrown" | type: official

### D10 定位
- [C34] 官方定位：「a lightweight runtime to turn AI agents, workflows, and backend services into durable processes」；站点标语「Build innately resilient backends and AI agents」 | src: https://docs.restate.dev/ | quote: "Restate is a lightweight runtime to turn AI agents, workflows, and backend services into durable processes." | type: official
- [C35] 仓库自述用例：Durable AI Agents、Workflows-as-Code、Microservice Orchestration、Event Processing、Async Tasks | src: https://github.com/restatedev/restate | quote: "a distributed durable version of your everyday building blocks" | type: official

## conflicts
- 无实质冲突。LICENSE commit 的 Additional Use Grant 措辞 2023 年版为「Application Platform Service」，2025-06-11 提交改为「Public Restate Platform Service」并澄清定义——同一限制的措辞演进，非冲突。

## gaps
- BSL 生效前（repo 公开至 2023-08-03）仓库无 LICENSE 文件；#654 只写「Decide on license」，未说明之前按什么授权——严格讲不能断言「一直是 BSL」，只能断言自该提交起为 BSL。
- 「自托管功能完整」无明确官方对比表；依据是架构文档公开描述集群各角色、LICENSE 未列功能限制，未见单独 enterprise 版——建议成稿措辞谨慎。
- Rust SDK 实际版本/成熟度未核实（docs 链 docs.rs）；.NET 未在 SDK 列表但可能有社区实现，未查。
- pricing 页为客户端渲染，套餐数字取自其 JS chunk（restate.dev 官方域名），页面可见文本只有 FAQ/单位定义。

## leads
- restate.dev 有「Restate vs Temporal」对比页（定价页导航可见），对 durable execution 横评有用。
- docs.restate.dev/llms.txt 是全文档索引，后续逐页核对可用。
- server/upgrading 页（restate server 自身升级流程）未查，D8 若需 server 侧升级语义可补。
