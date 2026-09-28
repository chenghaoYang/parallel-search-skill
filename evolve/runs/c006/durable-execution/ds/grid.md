# grid — 实体 × 维度

状态：✅ 一手来源+摘录 | ⚠ 二手 | ⚔ 冲突 | ❓ 缺口 | ∅ 官方未写 | — 不适用

## 分类轴（v1，R1 后确认）
- A 持久化/恢复机制：event history + 重放确定性函数（Temporal、DBOS）/ journal 记录每步结果（Restate）/ step 记忆化+函数重进入（Inngest）/ DAG 任务记录（Hatchet）
- B 谁拉起代码：worker 主动连引擎（Temporal RPC 轮询、Hatchet gRPC）/ 平台反向 HTTP 调 endpoint（Restate、Inngest）/ 进程内库（DBOS）
- 确定性边界由轴 A 推出，不再单列

## 维度
- D1 持久化模型 — 状态写在哪、崩溃后怎么恢复
- D2 确定性要求 — 哪部分用户代码必须确定；随机数/时间怎么办
- D3 执行模型 — 谁拉起用户代码；要跑什么基础设施
- D4 许可证与自托管 — server 与 SDK 的 license；自托管是否完整
- D5 托管云与计费 — 计费维度与档位
- D6 SDK 语言
- D7 外部事件原语 — signal/sleep/wait-for-event
- D8 版本升级 — 在跑执行怎么办
- D9 副作用与幂等 — 重试/dedup 语义；exactly-once 口径
- D10 定位

## 网格
| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Temporal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Restate | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| DBOS | ✅ | ✅ | ✅ | ✅ | ⚠(Cloud单价∅) | ⚔(首页列Rust无文档) | ✅ | ✅ | ✅ | ✅ |
| Inngest | ✅ | ✅ | ✅ | ⚠(自托管企业功能门控∅) | ✅ | ⚠(kt/rs成熟度) | ✅ | ✅ | ✅ | ✅ |
| Hatchet | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠(在跑run钉版本未明) | ✅(⚔已裁：checkpoint内exactly-once、task级at-least-once) | ✅ |

## R2 待补
- Temporal "action" 计费单位官方定义；SDK license 抽查
- Inngest "each step completes exactly once" 营销句逐字核（D9 边界主张反证）；自托管企业功能门控
- Hatchet 在跑 run 版本钉定；retry policy 页
- Restate vs Temporal 官方对比页；server 升级语义
- DBOS Java GA、Postgres 最低版本（低优先）
