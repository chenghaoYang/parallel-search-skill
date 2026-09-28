# r1-dbos
question: DBOS 官方文档/官网/仓库中，持久化模型、确定性要求、执行模型、许可证、云计费、SDK 语言、外部事件原语、版本升级、副作用语义、官方定位（D1–D10）
checked: docs.dbos.dev/, /architecture, /why-dbos, /python/tutorials/{workflow-tutorial,step-tutorial,upgrading-workflows,workflow-communication,scheduled-workflows}, /python/reference/contexts, /typescript/tutorials/workflow-tutorial, /production/{conductor,workflow-management}, dbos.dev/, dbos.dev/pricing, github.com/dbos-inc/dbos-transact-{py,ts,golang,java}, .../dbos-transact-ts/blob/main/src/dbos.ts

## claims

### D1 持久化
- [C1] workflow/step 检查点写 Postgres system database（含调度/队列状态）；输入输出全持久化 | src: https://docs.dbos.dev/architecture | quote: "This database stores all workflow checkpoints, step outputs, and schedule and queue state." | type: official
- [C2] 恢复=用已存输入重调 workflow 函数；已完成 step 直接返回检查点输出不重跑 | src: https://docs.dbos.dev/architecture | quote: "DBOS restarts each interrupted workflow by calling it with its checkpointed inputs." | type: official
- [C3] 中断后自动从最后完成 step 续跑 | src: https://docs.dbos.dev/python/tutorials/workflow-tutorial | quote: "DBOS automatically recovers its execution from the last completed step." | type: official

### D2 确定性
- [C4] workflow 函数必须 deterministic | src: https://docs.dbos.dev/python/tutorials/workflow-tutorial | quote: "a workflow function must be **deterministic**" | type: official
- [C5] 相同输入须同序调相同 step；随机数/本地时间等非确定操作应放 step | src: https://docs.dbos.dev/python/tutorials/workflow-tutorial | quote: "it should invoke the same steps with the same inputs in the same order" | type: official
- [C6] DBOS.sleep durable：唤醒时间存库 | src: https://docs.dbos.dev/python/tutorials/workflow-tutorial | quote: "This sleep is **durable**—DBOS saves the wakeup time in the database" | type: official
- [C7] TS 源码有 DBOS.randomUUID()，实现为 internal step（结果被检查点）；教程未文档化 | src: https://github.com/dbos-inc/dbos-transact-ts/blob/main/src/dbos.ts | quote: "Generate a random (v4) UUUID, similar to `node:crypto.randomUUID`." | type: official

### D3 执行 / Conductor
- [C8] 库内嵌进程；除 Postgres 无编排服务器/额外基础设施 | src: https://docs.dbos.dev/architecture | quote: "There's no separate orchestration server and no infrastructure required besides Postgres." | type: official
- [C9] Conductor=控制面：自动恢复中断 workflow 到健康 worker + dashboard | src: https://docs.dbos.dev/architecture | quote: "Conductor detects the failure and automatically recovers its workflows to a compatible live worker" | type: official
- [C10] Conductor 经 WebSocket 交换元数据/命令，不访问用户数据库，不在关键路径 | src: https://docs.dbos.dev/production/conductor | quote: "Conductor uses a WebSocket-based protocol to exchange workflow metadata and commands with your application." | type: official

### D4 许可证
- [C11] dbos-transact-py / -ts / -golang / -java 均 MIT | src: https://github.com/dbos-inc/dbos-transact-py | quote: "MIT license" | type: official
- [C12] Conductor 自托管仅 Enterprise 付费档 | src: https://dbos.dev/pricing | quote: "Option to self-host DBOS Conductor" | type: official

### D5 云计费
- [C13] Pro $99/月（2 seats、3 apps、1M checkpoints/月，超 $50/百万）；Teams $499/月（10/10/10M，$40/百万）；Enterprise 定制 | src: https://dbos.dev/pricing | quote: "1 million checkpoints (workflows, steps, transactions) per month" | type: official
- [C14] 计费=月订阅按 seats+apps+checkpoint 量；Transact 库 "free forever"；DBOS Cloud 需 Contact sales | src: https://dbos.dev/ | quote: "Use the open source DBOS Transact library, free forever." | type: official

### D6 SDK
- [C15] 文档：Python/TypeScript/Go/Java；dbos.dev 另列 Rust 库 | src: https://docs.dbos.dev/ | quote: "Develop with Python ... Develop with TypeScript ... Develop with Go ... Develop with Java" | type: official

### D7 原语
- [C16] DBOS.send(dest_id,msg,topic)/recv(topic,timeout=60)：workflow 间消息按 topic 排队 | src: https://docs.dbos.dev/python/tutorials/workflow-communication | quote: "Messages can optionally be associated with a topic and are queued on the receiver per topic." | type: official
- [C17] set_event(key,val) 发布/更新键值；get_event(wf_id,key,timeout) 等待读取；"All messages are persisted to the database" | src: https://docs.dbos.dev/python/tutorials/workflow-communication | quote: "to publish a key-value pair, or update its value if it has already been published" | type: official
- [C18] cron（croniter、可选秒、UTC）；schedule 存库可运行时增删暂停；每触发恰一 worker 执行 | src: https://docs.dbos.dev/python/tutorials/scheduled-workflows | quote: "Each time a schedule fires, its workflow is executed by exactly one worker process." | type: official

### D8 版本升级
- [C19] breaking change=改了跑哪些 step 或其顺序；两策略 patching+versioning | src: https://docs.dbos.dev/python/tutorials/upgrading-workflows | quote: "DBOS supports two strategies for safely upgrading workflow code: patching and versioning." | type: official
- [C20] DBOS.patch() 新 wf 返 True/旧返 False（operation_outputs 表插 patch marker）；deprecate_patch() 过渡 | src: https://docs.dbos.dev/python/tutorials/upgrading-workflows | quote: "DBOS.patch() returns `True` for new workflows (those started after the breaking change) and `False` for old workflows" | type: official
- [C21] versioning：默认源码 hash 得版本；只恢复同版本 workflow；推荐蓝绿；另 fork 从指定 step 复制新 ID 续跑 | src: https://docs.dbos.dev/python/tutorials/upgrading-workflows | quote: "it only recovers workflows whose version matches the current application version" | type: official

### D9 副作用
- [C22] step at-least-once、完成后永不重跑；transaction "commit exactly once" | src: https://docs.dbos.dev/python/tutorials/workflow-tutorial | quote: "Steps are tried *at least once* but are never re-executed after they complete." | type: official
- [C23] workflow ID=幂等键："executes only once"；wf 内 send 保 exactly-once 投递 | src: https://docs.dbos.dev/python/tutorials/workflow-communication | quote: "If you're sending a message from a workflow, DBOS guarantees exactly-once delivery." | type: official
- [C24] step 重试：retries_allowed/max_attempts=3/backoff_rate=2.0；全败抛 DBOSMaxStepRetriesExceeded | src: https://docs.dbos.dev/python/tutorials/step-tutorial | quote: "automatically retry any exception a set number of times with exponential backoff" | type: official

### D10 定位
- [C25] "DBOS is a library for building reliable programs." | src: https://docs.dbos.dev/ | quote: "DBOS is a library for building reliable programs." | type: official
- [C26] 对标 Temporal 重量级编排服务："DBOS implements them in a Postgres-backed library." | src: https://docs.dbos.dev/why-dbos | quote: "DBOS implements them in a Postgres-backed library." | type: official

## conflicts
- 语言列表：docs.dbos.dev 导航仅 Python/TypeScript/Go/Java 教程；dbos.dev 首页把 Rust 也列为 "Durable Execution Library"（无对应文档章节）。

## gaps
- 无确定性时间 API（无 Temporal workflow.now 等价物）：Python contexts reference 未收录；官方路径=非确定操作放 step。
- Conductor 未见开源仓库/license；自托管仅 Enterprise。
- Postgres 最低版本未查；Java SDK GA/preview 未确认；DBOS Cloud 无公开单价。

## leads
- Durable queues（并发/rate limit）：docs.dbos.dev/python/tutorials/queue-tutorial。
- DBOS Client 可从应用外 enqueue/get_event。
- "Build Durable AI Agents"/hitl 页：send/recv 做 human-in-the-loop。
