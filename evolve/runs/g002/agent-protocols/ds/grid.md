# Taxonomy 网格 v1

v0→v1：分类轴不变（主轴仍是通信边界，辅轴仍是交互时态）。IBM ACP 从「与 A2A 并列的现行标准」改成「同一家族里、项目宣布并入 A2A 的前规范」。不因缩写相同把 Zed ACP 放进这个家族。A2UI、OpenAI 文档里的另一个 ACP、WebMCP、ANP、MCP Apps 仍只在待定名单，不入格。

## 分类轴

- 主轴：通信边界。解释它们能不能互相替代。
- 辅轴：交互时态（无状态调用 / 任务状态机 / 编辑器会话 / 事件流）。解释同一边界上传输和状态为什么不同。

| 家族 | 边界 | 成员 |
|---|---|---|
| 模型上下文 | 宿主 ↔ 工具与数据服务器 | MCP |
| 智能体互操作 | agent ↔ 远程 agent | A2A；IBM ACP 为宣布并入后的前规范 |
| 编码代理客户端 | 编辑器/IDE ↔ coding agent | Zed ACP |
| 人机界面 | 事件生产者 ↔ 面向用户的消费者 | AG-UI |

## 维度

| id | 维度 | 这一列回答什么问题 |
|---|---|---|
| D1 | 边界与角色 | 两端的官方角色名是什么？ |
| D2 | 核心原语 | 交换的对象和操作，官方叫什么？ |
| D3 | 传输 | 官方传输绑定有哪些？哪些已弃用？ |
| D4 | 状态与任务 | 一次调用，还是有会话/任务生命周期？ |
| D5 | 发现 | 对方怎么被找到？ |
| D6 | 鉴权 | 官方规定的认证/授权机制是什么？ |
| D7 | 治理与版本 | 谁维护、当前版本、许可、规范状态？ |
| D8 | 大厂落地 | OpenAI、Anthropic、Google、微软自己的文档是否支持，自家变体叫什么？ |
| D9 | 层位关系 | 该规范自己怎么定位与另外几个协议的关系？ |

状态：`✅` 一手来源 + 原文；`⚠` 只有二手；`⚔` 来源冲突；`❓` 缺口；`∅` 官方未写（已定向查过）；`—` 不适用。

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| MCP | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ❓ | ✅ |
| A2A | ✅ | ✅ | ⚔ | ✅ | ✅ | ⚔ | ⚔ | ❓ | ✅ |
| ACP-IBM | ✅ | ✅ | ✅ | ✅ | ⚔ | ⚔ | ⚔ | ❓ | ✅ |
| ACP-Zed | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ | ⚔ | ❓ | ✅ |
| AG-UI | ✅ | ⚔ | ⚔ | ✅ | ∅ | ✅ | ✅ | ❓ | ✅ |

格内说明（不另占状态）：

- MCP×D2：Tools 与客户端特性有摘录。Resources、Prompts、消息封装是否仍为 JSON-RPC，摘录未覆盖，不当成已删除。
- MCP×D3：双端点 HTTP+SSE 的 Replaced / deprecated / 尚未 Removed 三份原文并存；现行传输仍可返回按请求的 SSE。
- MCP×D5：MUST RPC 有摘录；方法名 `server/discover` 不在摘录句内。
- MCP×D7：治理页是 LF Projects, LLC。捐赠 AAIF 的博客在笔记里标为 secondary，不单独把格子降成 ⚠。
- MCP×D9：只覆盖已打开的那几页，不是全站。
- A2A×D4：终态与中断态有摘录。SUBMITTED、WORKING、UNSPECIFIED 无摘录。
- A2A×D6：方案种类有摘录；prose 与 proto 字段名冲突。
- A2A×D7：1.0.0 有摘录。笔记冲突段提到 1.0.1，但没有独立 quote。首页「捐赠给 LF」与 2026-08-27「加入 AAIF」并存。
- A2A×D9：与 MCP 互补有规范摘录。ACP 合并不在 A2A 规范正文。
- ACP-IBM×D5：`agent.yml` 有摘录；「尚未进入官方规范」只写在笔记冲突段。
- ACP-IBM×D7：LF 帖和归档 README 对规范站首页「仍社区治理」。
- ACP-Zed×D3：stdio SHOULD、引言里的 HTTP/WebSocket、Streamable HTTP draft、v2 称远程不在 core，四份原文并存。
- ACP-Zed×D7：稳定版 1 有摘录。共同治理对 BDFL；v2 draft 对 stable baseline。
- ACP-Zed×D9：与 MCP 分 socket、Unlike MCP 有摘录。与 IBM ACP 的否定没有被摘录句本身证明。
- AG-UI×D2 / D3：spec 1.0 与概念页的事件数、传输强制性冲突。
- AG-UI×D5：规范写明这一版没有能力交换，也没有发现 URL。
- AG-UI×D6：规范写明不定义 credential。
- AG-UI×D9：「全部三个」的三个名字不在同一条摘录。A2UI 只有 AG-UI 站点上的定性。

## 待定（未入格）

- OpenAI 文档中的 ACP（scout 线索，未入正文）
- A2UI（AG-UI 站点有定性；A2UI 自己的站点只在 scout）
- WebMCP、ANP、MCP Apps（scout）
