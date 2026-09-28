/deep-search 产出文档 帮用户搞清楚各家 durable execution / 持久化工作流引擎有什么不同，新项目该怎么选

seed keywords: Temporal. Restate. DBOS. Inngest. Hatchet

some user aware variation: 听说用 Temporal 写 workflow 所有代码都必须确定性、连 Math.random 都不能用——是不是这类引擎全都这么要求？还有人说 Restate 和 Inngest 都是开源的、自托管没限制，许可证上真没问题吗？上了 durable execution 是不是就等于 exactly-once 了？


起码先这 5 个，然后讲清它们在持久化模型（event sourcing + replay vs journal vs Postgres 背书）、代码确定性要求、自托管 vs 托管云、SDK 语言覆盖、计费模型上的差异


以及其他用户需要知道的问题（signal/定时器/等外部事件的语义差异、版本升级与 replay 兼容、幂等与外部副作用）


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长

---
外层说明（Claude Code，benchmark 固定设置）：
- 参数：--rounds 3 --workers 6 --budget 9000。
- skill 目录是 .claude/skills/deep-search。工作目录用 ./ds（dir=./ds）。最终文档同时写到 ./report.md。
- 工人用 subagent_type "research-worker"（模型已由外层固定，不要传 model）。
- 检索：工人用 WebSearch 找页面，再用 WebFetch 打开一手页面取原句。本次运行没有 pplx-safe。
- 当前目录之外的文件与本任务无关，不要读。
