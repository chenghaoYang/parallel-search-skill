# kv-stores 任务参考答案

给人工检查者用的简明答案，对应 task.md 里用户提出的疑问。核实日期：2026-09-24。

## 1. "Redis 先改成非开源、后来又改回开源了" —— 对吗？

**方向对，细节容易错。** 完整时间线：

- **Redis 7.2.x 及更早**（2009–2024 年 3 月）：BSD-3-Clause，7.2.4 是最后一个 BSD 版本线。
- **2024 年 3 月 20 日 / Redis Community Edition 7.4 起**：改为 RSALv2 或 SSPLv1 双许可，两个都不是 OSI 批准的开源协议（即"source available"）。7.4–7.8 一直是这个状态。
- **2025 年 5 月 1 日 / Redis 8.0 GA**：**新增** AGPLv3 作为第三个选项——注意不是"换回 BSD"，而是 RSALv2、SSPLv1、AGPLv3 三选一，其中只有 AGPLv3 是 OSI 批准的。免费产品同期从 "Redis Community Edition" 改名 "Redis Open Source"。Redis 8 还把原 Redis Stack 的模块（JSON、时序、概率结构、查询引擎、向量集合 beta）合进主发行版。

来源：https://redis.io/legal/licenses/ ；https://redis.io/blog/agplv3/ ；https://redis.io/blog/redis-8-ga/

## 2. "Valkey 跟 Redis 现在还兼容吗？" —— 分层次看

- **客户端/协议层：基本兼容。** Valkey 讲 RESP2/RESP3，命令面以 Redis 7.2.4 为基线，常见 Redis 客户端（redis-py、ioredis、go-redis 等）直连通常不用改代码；安装时还会建 `redis-server`/`redis-cli` 兼容 symlink。
- **数据文件/复制层：有明确边界。** Valkey 官方迁移文档写明兼容 Redis OSS 7.2 及更早版本；**Redis CE 7.4+ 产出的 RDB/AOF 数据文件与 Valkey 不兼容**。官方迁移路径是把 Valkey 节点作为副本挂进 Redis ≤7.2 集群、同步后逐个 `CLUSTER FAILOVER` 提升——混部是过渡手段，不是长期形态。
- **功能层：已在分化。** Valkey 9 加了原子 slot 迁移、cluster 模式多数据库、hash 字段过期等 Redis 没有的东西；Redis 8 也各有自己的新功能。别再当"永远是 drop-in 等价物"。Valkey 本身是 Linux 基金会托管的社区项目（2024 年 3 月从 Redis 7.2.4 fork，BSD-3-Clause），治理不归单一厂商。

来源：https://valkey.io/topics/migration/ ；https://valkey.io/blog/valkey-9-1-delivers-improvements-in-security-performance-and-more/

## 3. "Dragonfly 比 Redis 快 25 倍？" —— 半对

- **25× 的出处**：Dragonfly 官方基准，对比对象是**单进程 Redis**（只能用一个核）vs 吃满整机核的 Dragonfly（AWS c6gn.16xlarge），测得 3.8M+ QPS。这个对比说明的是"单进程吃满多核"，不是同拓扑下的公平对比。
- **Redis 的反测**：Redis 官方 2022 年用 **40 分片 Redis 7.0 集群**（只用 64 核中的 40 核）在同一机型上测得吞吐比 Dragonfly 高 **18%–40%**（pipeline=30 时差距更大）。所以"谁快"取决于你拿 Redis 单实例还是 Redis Cluster 来比。
- **代价面**：Dragonfly 是 BSL 1.1（源码可用、非 OSI 开源，禁止拿它做竞争性托管内存库服务，change date 后转 Apache 2.0）；**不支持 AOF**，持久化只有快照；多节点 cluster 模式存在但控制面（健康检查、自动 failover、slot 迁移）要你自己用 `DFLYCLUSTER` 管或买 Dragonfly Cloud/Swarm，且多分片模式只支持 db0。

来源：https://github.com/dragonflydb/dragonfly ；https://redis.io/blog/redis-architecture-13-years-later/ ；https://github.com/dragonflydb/dragonfly/blob/main/LICENSE.md ；https://www.dragonflydb.io/docs/managing-dragonfly/aof ；https://www.dragonflydb.io/docs/managing-dragonfly/cluster-mode

## 4. "KeyDB 被 Snap 收购后基本停更了？" —— 基本属实

- **2022 年 5 月** Snap 收购 KeyDB，项目合并为单一 **BSD-3-Clause** 仓库（仍是真开源）。
- 公开仓库最新 release 停在 **v6.3.4（2023 年 10 月 30 日）**，主分支公开提交 2024 年 4 月后基本停了。KeyDB 作者 John Sully 2025 年 1 月离开 Snap，公开建议新投入应该去 Valkey。
- 结论：存量部署能用就继续用，但**新项目别选 KeyDB**，要 BSD + 活跃治理的 Redis 系替代品选 Valkey。

来源：https://github.com/Snapchat/KeyDB ；https://github.com/Snapchat/KeyDB/releases ；https://www.gomomento.com/blog/why-snap-was-willing-to-fork-and-why-they-still-came-back/

## 5. 线程模型（本题最容易写错的维度）

- **Redis**：命令执行单线程（官方原话 "mostly a single-threaded server from the POV of commands execution"），原子性靠串行化天然保证；Redis 6 起有 **io-threads** 把 socket 读写和 RESP 解析下放给 I/O 线程，Redis 8 重写了这套实现（按连接分配 I/O 线程），`io-threads` 默认仍是 **1**，设 8 时官方测得吞吐最高 +112%。多核扩展的正统姿势仍是多实例/Cluster 分片。
- **Valkey 8**：同样"执行单线程 + I/O 多线程"，但实现是增强版（I/O 线程还承担 epoll 轮询、内存释放），官方基准称比 Valkey 7.2 快约 230%（360K→1.19M RPS，8 个 I/O 线程）。
- **Dragonfly**：真·全多线程 **shared-nothing**——keyspace 按线程分片、各管各的 slice，多键事务用类 VLL 的锁管理协调分片，不用 mutex/spinlock。
- **KeyDB**：多线程执行（当年卖点就是真并行跑命令），另有 active-active 复制、FLASH 分层存储；但项目已停滞（见上）。

来源：https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/ ；https://redis.io/blog/redis-8-ga/ ；https://valkey.io/blog/unlock-one-million-rps/ ；https://github.com/dragonflydb/dragonfly

## 6. 持久化

- **Redis / Valkey / KeyDB**：RDB 快照 + AOF（`everysec` 约 1 秒 RPO，`always` 最强但最贵），可叠加。
- **Dragonfly**：只有 point-in-time 快照，**无 AOF**（官方文档明说 "Currently, Dragonfly does not support AOF"）——要低 RPO 的本地写日志别选它，或让外部持久层兜底。好处是快照是 forkless 的，没有 Redis fork/CoW 的内存峰值问题。
- **KeyDB FLASH**：RocksDB 扛的 SSD 分层存储，冷数据留在盘上、热数据在内存，官方称持久性约等于 AOF `everysec`，标 **beta**——解决的是"内存贵"问题，不是替代副本和备份。

来源：https://redis.io/tutorials/operate/redis-at-scale/persistence-and-durability/ ；https://www.dragonflydb.io/docs/managing-dragonfly/aof ；https://docs.keydb.dev/docs/flash/

## 7. 集群与复制

- **Redis**：Redis Cluster 多进程分片（16384 slot、MOVED/ASK 重定向），主从复制 + failover 成熟；Redis 8 还改了全量同步机制（两路并行流，峰值复制 buffer 降 35%）。
- **Valkey**：继承 Redis Cluster 模型，迁移期可与 Redis ≤7.2 混部；9.x 加原子 slot 迁移、`CLUSTERSCAN`、cluster 模式多 DB。
- **Dragonfly**：单节点有 emulated cluster 模式（兼容 Redis Cluster 客户端）；多节点 cluster 是数据面，拓扑/健康/failover/slot 迁移要自己配或用 Dragonfly Cloud/Swarm；多分片模式仅 db0。
- **KeyDB**：支持标准主从 + 独有的 active-active 多主复制，但上游停更，生产谨慎。

## 8. 一句话选型

- 要**协议兼容 + 真开源 + 活跃多厂治理**：Valkey（ElastiCache 等云托管也已默认提供）。
- 已在 Redis 生态、要官方模块和新功能：Redis 8（能接受 AGPLv3/RSALv2/SSPLv1 三选一）。
- 单机要榨干多核、能接受 BSL 和快照级持久化：Dragonfly。
- KeyDB：仅存量维护，新项目不选。
