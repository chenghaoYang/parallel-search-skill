# brief — durable execution / 持久化工作流引擎选型对比

## 任务
产出对照文档：Temporal / Restate / DBOS / Inngest / Hatchet 五家 durable execution 引擎本质差异是什么，新项目怎么选。

## 读者
要给新项目选工作流引擎的工程师。目标：5 分钟建立「这几家的执行语义和持久化模型差异很大」的认知，再按维度查细节。

## 用户点名疑点（成稿必须有带引用的结论）
1. 「用 Temporal 写 workflow 所有代码都必须确定性，连 Math.random 都不能用」——这类引擎全都这么要求吗？
2. 「Restate 和 Inngest 都是开源的、自托管没限制」——许可证上真没问题吗？（注意 BSL/fair-code 可能）
3. 「上了 durable execution 就等于 exactly-once 了」——对吗？（at-least-once + memoization + 幂等 vs 真 exactly-once）

## 范围内
- 种子实体：Temporal, Restate, DBOS, Inngest, Hatchet
- 维度：持久化模型 / 确定性要求 / 执行与部署模型 / 许可证与自托管 / 托管云与计费 / SDK 语言 / 外部事件原语（signal、timer、wait-for-event）/ 版本升级与 replay 兼容 / 副作用与幂等 / 官方定位
- 相近实体（scout 线索决定是否在正文提一句）：LittleHorse、Dapr Workflow、Azure Durable Functions、AWS Step Functions、Cloudflare Workflows、Golem 等

## 范围外
- 性能基准、厂商内部实现
- Airflow/Dagster 类数据管道编排（不是 durable execution）

## 完成标准
- report.md ≤ 9000 字符（含来源节）；taxonomy + 对照矩阵 + 坑 + 未决
- 每个具体事实追到 notes 的 [C#] 与完整 URL；一手来源优先
- 三条疑点给出结论，哪怕是「官方没写」
