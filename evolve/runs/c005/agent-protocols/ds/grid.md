# Grid v0

## 分类轴
**协议连接的是哪两端**（family axis，taxonomy 主骨架）：
- A. agent ↔ 工具/数据源：MCP
- B. agent ↔ agent（跨组织任务委派）：A2A、ACP-IBM
- C. 客户端/编辑器 ↔ agent 进程（本地交互）：ACP-Zed
- D. 前端 UI ↔ agent 后端（交互式界面）：AG-UI

## 实体 × 维度

维度（列）：
- D1 两端：谁↔谁
- D2 发起/治理：作者、现治理方、基金会
- D3 传输与格式：JSON-RPC/REST/SSE/stdio/gRPC
- D4 核心抽象：tool·resource·prompt / AgentCard·Task·Artifact / session·turn / event 流
- D5 鉴权：OAuth 版本、API key、mTLS、未规定
- D6 版本线与弃用：当前 spec 版本+日期、deprecated 项
- D7 大厂支持：OpenAI / Anthropic / Google / Microsoft
- D8 典型实现：SDK、客户端、registry

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 |
|---|---|---|---|---|---|---|---|---|
| MCP | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| A2A | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| ACP-IBM（Agent Communication Protocol） | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| ACP-Zed（Agent Client Protocol） | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| AG-UI | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| （leads 追加：AGNTCY/ANP/MCP-UI/A2UI…） | | | | | | | | |
