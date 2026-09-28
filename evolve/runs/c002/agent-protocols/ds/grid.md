# grid v0 — 实体 × 维度

分类轴（主）：**协议跨越的边界** = 谁和谁说话
- 家族 A「模型/agent ↔ 工具与数据」：MCP
- 家族 B「agent ↔ agent」：A2A、IBM/BeeAI ACP
- 家族 C「客户端/编辑器 ↔ agent」：Zed ACP
- 家族 D「UI ↔ agent（面向用户的事件流）」：AG-UI
- 家族 E「相邻/其他」（payment、discovery 等，leads 决定要不要收）：AP2、x402、ANP、AGNTCY、MCP-UI、A2UI、Apps SDK…

## 维度（列）
- D1 边界与角色：谁发起、谁接收、解决什么
- D2 传输与 payload：stdio/HTTP/SSE/WebSocket/JSON-RPC/gRPC，消息单位
- D3 鉴权：OAuth? API key? 规范写没写
- D4 版本与状态：当前版本、日期、deprecated 项
- D5 治理：谁拥有、在哪个基金会、license
- D6 大厂支持：OpenAI / Anthropic / Google / Microsoft 各自是否支持、有无自家变体
- D7 与相邻协议的关系：互补/竞争/合并

## 网格（状态：❓ 待查）

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|---|
| MCP | ❓ | ❓(SSE废弃?) | ❓ | ❓ | ❓ | ❓ | ❓ |
| A2A | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓(ACP合并?) |
| IBM/BeeAI ACP | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Zed ACP | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| AG-UI | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| 大厂变体（Apps SDK 等） | — | — | — | — | — | ❓ | ❓ |
