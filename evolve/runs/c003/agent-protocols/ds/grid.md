# Grid v0

## 分类轴（family 划分依据）
「协议连接的是哪两个角色」——同一栈上的不同边：
- 模型/agent ↔ 工具与数据（tool edge）：MCP
- agent ↔ agent（agent edge）：A2A、IBM ACP
- 客户端/IDE ↔ agent（client edge）：Zed ACP
- UI 前端 ↔ agent（frontend edge）：AG-UI
备选第二轴：线格式谱系（JSON-RPC vs REST vs event stream）。

## 实体（行）
- MCP (Model Context Protocol)
- A2A (Agent2Agent)
- ACP-IBM (Agent Communication Protocol, IBM/BeeAI)
- ACP-Zed (Agent Client Protocol, Zed)
- AG-UI (CopilotKit)
- 大厂支持/变体（OpenAI、Anthropic、Google、Microsoft）——作为列在矩阵里体现
- 其他同 scope（由 scout leads 决定是否加行）

## 维度（列）
- D1 连接哪两个角色（scope）：这一列回答"它在 agent 栈里管哪条边"
- D2 通信角色与方向（client/server、谁发起）：回答"谁是 client 谁是 server"
- D3 线格式与传输（JSON-RPC? HTTP? SSE? WS?）：回答"线上跑什么"
- D4 核心抽象（tools/resources、task/message、session/run、event types）：回答"协议的 noun 是什么"
- D5 版本与时间线（最新 spec 版本、日期、preview/stable、废弃项）：回答"现在看哪个版本"
- D6 鉴权（OAuth 2.1? API key? 未规定）：回答"怎么认证授权"
- D7 治理（发起者、现归属基金会/组织、spec 仓库）：回答"谁在管"
- D8 大厂支持与变体：回答"OpenAI/Anthropic/Google/MS 各自支不支持、有无魔改"
- D9 发现机制（agent card、server 注册、manifest）：回答"怎么找到对方"
- D10 会话/状态模型（无状态? thread/run? session id）：回答"状态放哪端"

## 格子状态
（收束后填充）
