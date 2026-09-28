产出文档 帮用户搞清楚各家 durable execution / 持久化工作流引擎有什么不同，新项目该怎么选

seed keywords: Temporal. Restate. DBOS. Inngest. Hatchet

some user aware variation: 听说用 Temporal 写 workflow 所有代码都必须确定性、连 Math.random 都不能用——是不是这类引擎全都这么要求？还有人说 Restate 和 Inngest 都是开源的、自托管没限制，许可证上真没问题吗？上了 durable execution 是不是就等于 exactly-once 了？


起码先这 5 个，然后讲清它们在持久化模型（event sourcing + replay vs journal vs Postgres 背书）、代码确定性要求、自托管 vs 托管云、SDK 语言覆盖、计费模型上的差异


以及其他用户需要知道的问题（signal/定时器/等外部事件的语义差异、版本升级与 replay 兼容、幂等与外部副作用）


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长
