# r2-restate
question: Restate (a) 官方「Restate vs Temporal」对比页自我定位差异；(b) server 升级/版本兼容语义（server/upgrading）；(c) 同 deployment 内 handler 代码变更时在跑 invocation 的 journal 重放是否出错（官方是否要求 handler 内步骤顺序稳定）；(d) 官方有无「自托管=全功能」表述或对照
checked: https://restate.dev/vs/temporal, https://docs.restate.dev/server/upgrading, https://docs.restate.dev/services/versioning, https://docs.restate.dev/server/overview, https://docs.restate.dev/hosting/overview, https://docs.restate.dev/get-restate

## claims
### (a) vs Temporal 官方口径（restate.dev/vs/temporal，营销页，无日期）
- [C1] 对比页定位：两者同为生产级 durable execution 系统，Restate 把 DE 变成全后端可用的构建块 | src: https://restate.dev/vs/temporal | quote: "Both are production-grade durable execution systems." + "Restate evolves Durable Execution into a building block you can use throughout your backend" | type: official
- [C2] 官方归纳差异为三轴：编程模型、执行开销、部署选项 | src: https://restate.dev/vs/temporal | quote: "the differences are their programming models, execution overhead, and deployment options" | type: official
- [C3] 部署差异：Temporal 四组件+外部 DB+worker 进程；Restate 单二进制自成复制集群 | src: https://restate.dev/vs/temporal | quote: "Temporal clusters have four components, an external database, and workflow workers." / "Restate is a self-contained single binary that forms a replicated cluster" | type: official
- [C4] 执行模型：Restate push 调用到服务 vs Temporal worker 轮询 Task Queue | src: https://restate.dev/vs/temporal | quote: "Restate pushes invocations to services." / "Temporal application code runs in Worker processes that poll Task Queues for Workflows and Activities." | type: official
- [C5] 编程模型：Temporal 只建模 Workflows/Activities；Restate 组合 durable functions、workflows、RPC、state、messaging、queues | src: https://restate.dev/vs/temporal | quote: "Temporal models applications as Workflows and Activities." / "Restate lets you compose durable functions, workflows, RPC, state, messaging, and queues" | type: official
- [C6] 状态：Temporal 无一等状态原语，workflow 变量靠重放 event history 重建；Restate 内嵌 RocksDB 按 key 存 durable K/V | src: https://restate.dev/vs/temporal | quote: "Temporal does not have a first-class primitive for this." / "Workflow variables, reconstructed by replaying event history." / "Restate stores durable K/V state per object key in its embedded store, backed by RocksDB" | type: official
- [C7] Serverless：Temporal polling 需长驻 Worker 不映射 serverless；Restate push 可直接调 serverless handler | src: https://restate.dev/vs/temporal | quote: "Temporal's polling model assumes a long-running Worker, which does not map directly to serverless." / "Restate's push model lets you invoke serverless handlers directly." | type: official
- [C8] 分发与成本口径：Temporal Cloud 无 BYOC；Restate 提供 Self-host/Cloud/BYOC，官方自称大规模成本最高省 10x | src: https://restate.dev/vs/temporal | quote: "Temporal Cloud is managed, but does not offer BYOC." / "Self-host, Restate Cloud or BYOC" / "up to 10× more cost efficient at scale" | type: official

### (b) server 升级语义（docs.restate.dev/server/upgrading）
- [C9] patch 升级总是可行；minor 升级保留对紧邻前版的功能兼容与全部持久数据 | src: https://docs.restate.dev/server/upgrading | quote: "Upgrading to the latest patch version should always be possible" / "Incremental minor version upgrades will retain functional compatibility with the immediate prior version" / "you will be able to upgrade from `x.y` to `x.(y+1)` while retaining all persisted data and metadata." | type: official
- [C10] 禁止跳 minor 版本，会绕过必要的数据存储迁移 | src: https://docs.restate.dev/server/upgrading | quote: "You must not skip minor version upgrades" | type: official
- [C11] 滚动升级须逐节点重启并等 partition 恢复；HTTP health check 不足以证明恢复 | src: https://docs.restate.dev/server/upgrading | quote: "Restart one node at a time and wait for its assigned partitions to recover before proceeding." / "A successful HTTP health check alone does not establish partition recovery." | type: official
- [C12] 单节点部署重启期间不可用 | src: https://docs.restate.dev/server/upgrading | quote: "A single-node deployment cannot remain available during its restart." | type: official
- [C13] 降级仅支持到上一 minor 的最新 patch，且未使用新版独有特性；不支持回退超过一个 minor | src: https://docs.restate.dev/server/upgrading | quote: "you can downgrade a Restate installation to the latest patch level of the previous minor version" / "rollback is only supported as long as you have not used any new features exclusive to the newer version." | type: official
- [C14] server 持久化兼容性标记检测不兼容数据版本；升级后首次启动可能因存储迁移变慢；建议先备份 | src: https://docs.restate.dev/server/upgrading | quote: "The server persists compatibility markers which enable it to detect incompatible data versions." / "Storage migrations can make the first startup after an upgrade take longer." | type: official
- [C15] SDK 与 server 独立版本化；注册服务的 SDK 须匹配 server 支持的 service protocol 版本 | src: https://docs.restate.dev/server/upgrading | quote: "Restate SDKs follow independent versioning from the server" | type: official

### (c) 同 deployment 内代码变更（services/versioning 的 "In-place code changes" 节）
- [C16] 官方定义 in-place change = 同 endpoint 改代码；明确称其违反不可变 deployment 原则，可使在跑 invocation 用新代码重放时失败 | src: https://docs.restate.dev/services/versioning | quote: "Modifying deployed code at the same endpoint." / "This violates the immutable deployment principle and can cause in-flight invocations to fail" "when they replay with the updated code." | type: official
- [C17] 重放时 server 做 journal 兼容性检查；错误 RT0016 表示重放代码产生了与原执行不同的 journal | src: https://docs.restate.dev/services/versioning | quote: "Restate performs journal compatibility checks during replay to prevent corruption." / "it means the code executed during replay has produced a different journal than the original execution" | type: official
- [C18] 不安全变更清单：重排 SDK 操作（run/state/调用/awakeable）、增删执行路径上的操作、改操作输入（state key、调用 payload）、改影响哪些操作执行的条件逻辑 | src: https://docs.restate.dev/services/versioning | quote: "Reordering Restate SDK operations (`run`, state access, service calls, awakeables)" / "Adding or removing SDK operations in the execution path" / "Changing operation inputs (state keys, service call payloads)" / "Modifying conditional logic that affects which operations execute" | type: official
- [C19] 安全 in-place 变更仅两类：修 ctx.run 内部的 bug；修一致复现的 bug（如反序列化错误） | src: https://docs.restate.dev/services/versioning | quote: "Fixing a bug inside `ctx.run`" / "Fixing a bug that consistently reproduces (e.g. deserialization error)" | type: official
- [C20] 本地开发可用 --force 重注册同 endpoint，但在跑 invocation 可能持续报 non-determinism 错误 | src: https://docs.restate.dev/services/versioning | quote: "In-flight invocations might keep failing with non-determinism errors" | type: official

### (d) 自托管完整性表述
- [C21] server overview：Restate 以单二进制分发，实现单节点或多节点集群所需的全部特性 | src: https://docs.restate.dev/server/overview | quote: "Restate is distributed as a single binary that implements all features required to run a single- or multi-node cluster" | type: official
- [C22] hosting/overview 对照页：托管方式不改变 service/handler 的实现，只决定 environment 跑在哪、由谁运营 | src: https://docs.restate.dev/hosting/overview | quote: "Your hosting choice does not change how you implement Restate services and handlers." / "It determines where the Restate environment runs and who operates it." | type: official
- [C23] hosting/overview 对照表差异仅在运营方、部署位置、setup、数据/网络边界与定价；无 Cloud 独占功能行 | src: https://docs.restate.dev/hosting/overview | quote: "Scaling, upgrades, and monitoring" — "Managed by Restate" vs. "Managed by you" / "Taking full control of deployment and operations" (self-hosted best-for) | type: official
- [C24] get-restate 页三选项并列：自托管=自己装自己运营；Cloud=Restate 代管；BYOC=Restate 代管跑在你账户 | src: https://docs.restate.dev/get-restate | quote: "Install and operate Restate on infrastructure you choose." / "Use a Restate environment managed by Restate in a Restate cloud region." | type: official

## conflicts
- 无。（C16–C19 与 R1 的「deployment 不可变+in-flight 钉版本」一致且互补：钉版本是推荐路径，in-place 改代码属违规路径，重放会被 journal 兼容性检查拦下报 RT0016。）

## gaps
- 无逐字「self-hosted = full-featured / 与 Cloud 功能等价」表述；最接近的是 C21（单二进制含全部集群特性）+ C22（托管不改实现）+ C23（对照表无 Cloud 独占功能行）。已查 /hosting/overview、/server/overview、/get-restate。
- vs/temporal 与 upgrading 页均未在 fetch 内容中显示发布/更新日期。
- upgrading 页称滚动更新命令需 Restate ≥v1.7.10，但未取「该语义自何版本起生效」的 changelog 起点。

## leads
- RT0016 错误详情：https://docs.restate.dev/references/errors#rt0016
- vs/temporal 的「10× cost efficient」等性能/成本主张为官方单方口径，无第三方基准引用。
- 滚动升级实操命令：restatectl rolling-update（需 admin 节点 fabric 地址 :5122）。
