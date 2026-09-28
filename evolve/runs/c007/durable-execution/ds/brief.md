# brief — durable execution 引擎选型对照

- 读者：要给新项目选 durable execution / 持久化工作流引擎的工程师。5 分钟内建立 taxonomy 和关键差异认知，再按矩阵查细节。
- 范围：Temporal、Restate、DBOS、Inngest、Hatchet（种子 5 家）。可扩展到 leads 发现的范围内新实体（如 LittleHorse、Golem、Restate 之外的 durable RPC 类）。
- 用户点名疑点（成稿必须给结论）：
  1. 「所有这类引擎都要求 workflow 代码确定性、Math.random 都不能用」——是不是全都这么要求？
  2. 「Restate 和 Inngest 都开源、自托管没限制」——许可证真没问题？（注意 BSL/SSPL/FSL/commons clause 等）
  3. 「上了 durable execution = exactly-once」——对不对？
- 必答维度：持久化模型（event sourcing+replay vs journal vs Postgres 背书）、代码确定性要求、自托管 vs 托管云、SDK 语言、计费模型、signal/定时器/外部事件语义、版本升级与 replay 兼容、幂等与外部副作用。
- 参数：rounds 3，workers 6/轮，budget 9000 字符，dir ./ds。
