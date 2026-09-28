产出文档 帮用户搞清楚 Redis、Valkey、Dragonfly、KeyDB 这几个内存 KV 存储现在有什么不同

seed keywords: Redis 8. Valkey. Dragonfly. KeyDB. RSALv2 / SSPLv1 / AGPLv3 / BSL-1.1. io-threads. shared-nothing

some user aware variation: 听说 Redis 先是改成非开源、后来又"改回开源"了——具体是哪一版、用的什么协议？Valkey 跟 Redis 现在还兼容吗？还有人说 Dragonfly 比 Redis 快 25 倍、KeyDB 被 Snap 收购后基本停更了——这些说法都对吗


起码先这 4 个，然后说清它们在许可证与治理归属、线程模型（单线程事件循环 / io-threads / 全多线程分片）、持久化（RDB / AOF / 快照 / FLASH）、集群与复制、以及与 Redis 协议和生态的兼容边界上的差异


以及其他用户需要知道的问题（新项目选型、从 Redis 迁移的路径、各家性能宣传的对照条件）


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长
