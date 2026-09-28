# grid — taxonomy v1

分类轴（v0 → v1，轴没换）：**线上两端是谁**。v1 只改了一处归属：ACP-IBM 不再算「和 A2A 并列的现行规范」，而是同一家族里 2025-08 宣布并入、仓库已归档的前身。轴仍然解释替代关系：同端才可替代，异端就叠放。

| 家族 | 两端 | 行 | 为什么是一类 |
|---|---|---|---|
| 能力与上下文 | 宿主内 Client ↔ Server | MCP | 暴露 Resources / Prompts / Tools |
| 智能体互操作 | Client ↔ 远端 Agent | A2A、ACP-IBM | A2A 是现行规范。ACP-IBM 是 REST 前身 |
| 编辑器客户端 | 编辑器 Client ↔ 编码 Agent | ACP-Zed | 类比 LSP，仓库和全称都与 IBM ACP 不同 |
| 生成式界面 | producer ↔ consumer | AG-UI | 一次 run 的事件流 |

维度不变：parties 两端角色；surface 对象原名；discovery 发现与握手；transport 传输与弃用；auth 鉴权；state 状态在哪；version 版本与弃用；governance 治理与许可；vendors 四厂自家文档（协议站名单只算 ⚠）；relation 官方关系。

证据：✅ 官方原句；⚠ 只有二手或协议站自述厂商；⚔ 官方冲突未裁决；❓ 没查到；∅ 定向查过、官方没写。

## 状态网格

| 实体 | parties | surface | discovery | transport | auth | state | version | governance | vendors | relation |
|---|---|---|---|---|---|---|---|---|---|---|
| MCP | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠ | ∅ |
| A2A | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠ | ⚔ | ✅ | ⚠ | ✅ |
| ACP-IBM | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ | ⚠ | ✅ |
| ACP-Zed | ✅ | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ⚠ | ✅ |
| AG-UI | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠ | ✅ |

vendors 全是 ⚠：只有协议网站点名，没有厂商域名原句。
MCP transport / discovery / state 的「删除 initialize、HTTP+SSE 传输 Deprecated」有规范原句，但是高影响、与旧教程相反，R2 回页复核前不进一屏口号。格子仍记 ✅。
A2A state 只有 “interrupted state” 的原句，枚举名未入摘录，所以是 ⚠。
ACP-IBM relation 取合并公告为可确认的一侧（横幅、讨论、LF 博客）；优点页未更新，写在成稿第 4 节，不把整格留在 ⚔。
AG-UI surface 以规范 1.0 的 31 个 EventType 为可确认一侧；README 约 16 种留在 ⚔。
relation 的 ✅ 只覆盖摘录里那一句：A2A↔MCP 互补，Zed↔LSP/MCP 类型，AG-UI↔A2UI。没写到的邻居见成稿第 5 节的 ∅。

## 点名疑点

- 两个 ACP：结论已进成稿第 0 节。全称、两端、仓库都不同。IBM 侧宣布并入 A2A 并归档。两边官网都没写对方。
- MCP SSE：传输表写了两句（HTTP+SSE 传输 Deprecated；请求级 SSE 仍合法）。复核前不收成口号。
- 四厂：整列 ⚠，R2 的主任务。

## 未入行（scout 只留线索，定义不进成稿）

A2UI、WebMCP、ANP、NLWeb、AP2、MCP Apps、Agent Skills、Activity Protocol、UTCP、MHS。
下一轮优先厂商域名。A2UI 只在 Google 工人碰到自家变体时顺手记原句，不单独开行，除非那一页表明它和 AG-UI 同级、必须进矩阵。
