# Grid v0

## 分类轴
按「协议管的是哪条边界」分家族：
- F1 模型/Agent ↔ 工具·数据：MCP
- F2 Agent ↔ Agent：A2A、IBM-ACP
- F3 Agent ↔ 用户界面：AG-UI（+MCP-UI/A2UI 类邻近物）
- F4 编辑器/客户端 ↔ Agent：Zed-ACP
轴能否解释差异待 R1 验证。

## 维度
- D1 层/解决什么问题：管哪两个角色之间的边界？
- D2 发起方与治理：谁创建、现在谁治理（基金会/厂商/社区）、license/治理流程？
- D3 传输与封装：JSON-RPC？REST？事件流？stdio/HTTP/SSE/WS？
- D4 核心对象/抽象：官方 spec 里的一级名词（tools/resources/prompts；AgentCard/Task/Artifact；events…）
- D5 状态模型：无状态请求 vs Task 生命周期 vs run/thread 会话
- D6 鉴权：官方 spec 写的 auth 机制（OAuth 版本、scheme 声明位置）
- D7 版本与稳定性：最新 spec 版本/日期、近期 breaking change
- D8 大厂支持：OpenAI / Anthropic / Google / Microsoft 各自支持程度（用官方公告/文档）
- D9 SDK 与生态：官方/主流 SDK、registry、采用方
- D10 与其他协议关系：互补/替代/已并入/被弃用

## 网格（实体 × D1–D10）
| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| MCP | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| A2A | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| ACP-IBM (Agent Communication Protocol) | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | — | ❓ | ❓ |
| ACP-Zed (Agent Client Protocol) | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | — | ❓ | ❓ |
| AG-UI | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | — | ❓ | ❓ |
| OpenAI 变体/立场 | — | — | ❓ | ❓ | — | ❓ | ❓ | ❓ | ❓ | ❓ |
| Anthropic 立场 | — | — | — | — | — | — | — | ❓ | ❓ | ❓ |
| Google 立场 | — | — | — | — | — | — | — | ❓ | ❓ | ❓ |
| Microsoft 立场 | — | — | — | — | — | — | — | ❓ | ❓ | ❓ |
