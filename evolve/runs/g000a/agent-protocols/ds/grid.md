# Taxonomy 网格 v1

分类轴不变：**通信边**。同一条边才替代；不同边叠放。

第二轴：**状态落在哪一端**。用来区分 F2 内部的前身和现行协议，也用来解释为什么四份规范不能互换。

v0→v1：不增删维度。F2 从「A2A 与 IBM ACP 并列」改为「A2A 是现行协议，IBM ACP 是已归档前身；欢迎页与对比页互相矛盾，格子记 ⚔」。缩写不作为分类轴。厂商表仍全是 ❓。近邻只登记、本轮不填。

## 家族

| 家族 | 通信边 | 成员 | 为什么是一类 |
|---|---|---|---|
| F1 工具与上下文 | Host 内 Client ↔ 恰好一个 Server | MCP | Server 提供 Resources / Prompts / Tools，对话不在 Server |
| F2 智能体任务 | Client ↔ Remote Agent | A2A；ACP-IBM 为前身 | 不碰对方 memory 与 tools，只交工作单元。IBM 用 REST run，A2A 用 Task |
| F3 编码会话 | 编辑器 Client ↔ coding Agent | ACP-Zed | JSON-RPC 会话，形状接近语言服务器 |
| F4 界面事件 | producer ↔ consumer | AG-UI | 一次输入，一条有序事件流 |

## 维度

| 列 | 这一列回答什么问题 |
|---|---|
| edge | 哪两端在说话，请求朝哪边流？ |
| objects | 一等对象的协议原名是什么？ |
| wire | 传输、编码、会话怎么建立？哪些传输已弃用？ |
| discovery | 怎么找到对方，对方怎么自描述？ |
| auth | 官方鉴权机制的原名是什么，挂在哪种传输上？ |
| version | 现行版本号、兼容规则、被点名的弃用项？ |
| gov | 谁发布规范、谁治理、什么许可证？ |
| state | 对话、任务或 UI 状态记在哪一端？ |
| compose | 官方如何描述它和另外几个协议的关系？ |

## 协议网格

| 实体 | edge | objects | wire | discovery | auth | version | gov | state | compose |
|---|---|---|---|---|---|---|---|---|---|
| MCP | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ⚔ | ✅ | ✅ |
| A2A | ✅ | ✅ | ⚔ | ✅ | ⚔ | ✅ | ✅ | ⚔ | ✅ |
| ACP-IBM | ✅ | ✅ | ⚔ | ✅ | ⚔ | ✅ | ⚔ | ✅ | ⚔ |
| ACP-Zed | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ✅ |
| AG-UI | ✅ | ⚔ | ⚔ | ∅ | ∅ | ✅ | ✅ | ✅ | ✅ |

MCP.wire 的现行传输没有互斥说法，所以是 ✅。HTTP+SSE 的移除日期另见 Q-sse。MCP.auth 是同一授权页上的 OPTIONAL 与 MUST RFC9728，限定从句没摘全。MCP.gov 的治理主体是 ✅ 级事实，许可证 MIT 对 Apache-2.0 使该格记 ⚔。A2A.wire 是概念页「全部 JSON-RPC」对规范三种绑定。A2A.state 是 `TASK_STATE_*` 与无前缀旧名并存。ACP-IBM.wire 是 `/runs` 与 `run/` 路径不一致。

## 厂商采用

| 厂商 | MCP | A2A | ACP-IBM | ACP-Zed | AG-UI | 自家变体 |
|---|---|---|---|---|---|---|
| OpenAI | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Anthropic | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Google | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Microsoft | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

## 近邻（只登记，未核验进正文）

| 实体 | 身份一句话 | 是否与某个种子同一条边 | 状态 |
|---|---|---|---|
| Agentic Commerce Protocol | ❓ | ❓ | ❓ |
| Activity Protocol | ❓ | ❓ | ❓ |
| AP2 | ❓ | ❓ | ❓ |
| UCP | ❓ | ❓ | ❓ |

## 点名疑点

| id | 问题 | 状态 |
|---|---|---|
| Q-acp | IBM ACP 与 Zed ACP 是否同一协议 | ✅ 不是。全称、通信边、文档站都不同；两边都没把对方写成自己 |
| Q-sse | HTTP+SSE 是否废弃、被什么替代 | ✅ 自 2025-03-26 deprecated，现行 HTTP 传输叫 Streamable HTTP。移除日期 ⚔ |
