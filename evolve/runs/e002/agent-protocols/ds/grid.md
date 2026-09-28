# Grid v0

## 分类轴
协议连接的是哪两端？这条轴应能解释传输层、状态归属、鉴权模型的大部分差异。
- **模型↔工具/数据源**：MCP
- **agent↔agent（对等，任务委托/协作）**：A2A、ACP-IBM
- **client应用（编辑器/IDE）↔agent 子进程**：ACP-Zed
- **agent↔前端 UI（面向终端用户的展示层）**：AG-UI

次轴：治理谱系（Anthropic 主导 / Google 主导→捐赠中立基金会 / IBM 主导→合并 / 单厂商 Zed / 框架商 CopilotKit）。

## 实体（行）
| 实体 | 全称 | 主导方（待核实） |
|---|---|---|
| MCP | Model Context Protocol | Anthropic |
| A2A | Agent2Agent Protocol | Google → Linux Foundation? |
| ACP-IBM | Agent Communication Protocol | IBM / BeeAI → 状态待核实（传闻已并入 A2A） |
| ACP-Zed | Agent Client Protocol | Zed Industries |
| AG-UI | Agent-User Interaction Protocol | CopilotKit |

## 维度（列）
1. **管什么**——这个协议约束的是哪一段交互？
2. **拓扑/方向**——谁是 client、谁是 server（或是否对等）？
3. **传输层**——stdio / HTTP / SSE / Streamable HTTP / gRPC / WebSocket，用什么承载消息？
4. **消息格式**——JSON-RPC 2.0？REST+JSON？Protobuf？事件流？
5. **鉴权**——规范里规定了什么鉴权机制，还是留给实现方？
6. **状态归属**——会话/任务状态由谁持有（client、server、双方）？
7. **版本规则**——版本号怎么编（日期式/semver），当前最新版本
8. **治理**——spec 由谁维护，是否有开放治理机构/steering committee
9. **典型实现/采用者**——官方列出的 SDK、参考实现、知名采用方
10. **与其他协议关系**——是否声称与其他 4 者互补/竞争/可叠加使用

## Grid 状态（R2 收束后，详见 notes/、report.md）
| 实体 \ 维度 | 1管什么 | 2拓扑 | 3传输 | 4格式 | 5鉴权 | 6状态 | 7版本 | 8治理 | 9采用者 | 10关系 |
|---|---|---|---|---|---|---|---|---|---|---|
| MCP | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ∅（官方未提其他协议） |
| A2A | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ACP-IBM | ✅ | ✅ | ✅ | ✅ | ⚠（仅二手） | ✅ | ✅ | ✅ | ✅ | ✅（已确认与ACP-Zed无关） |
| ACP-Zed | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| AG-UI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅（R2反证：仍CopilotKit独家）| ⚠（大厂未官方采用） | ✅ |

9/10 维度核心矩阵已 ✅/∅；唯一弱项 ACP-IBM×鉴权（协议已停用，不再追）。

## 大厂矩阵（R2 更新，● 原生/产品级 ◐ 适配器/教育级 ○ 未支持 — 未见声明 N/A 已停用）
| 大厂 | MCP | A2A | ACP-IBM | ACP-Zed | AG-UI | 自家变体/框架 |
|---|---|---|---|---|---|---|
| OpenAI | ● | — (AAIF创始机构,非产品支持) | N/A | ◐ 社区适配器(Codex CLI) | — | Agents SDK；另有撞名的 Agentic Commerce Protocol(电商支付) |
| Anthropic | ● 创造者 | ◐ 仅教育网研 | N/A | ◐ Zed造适配器(Claude Code) | — | 无独立框架 |
| Google | ● | ● 发起方 | N/A | ● 原生(Gemini CLI) | — (自有A2UI) | ADK、A2UI |
| Microsoft | ● | ● | N/A | ○ VS Code仅讨论中issue | — | Agent Framework(SK后继) |

## 用户疑点（必须有结论）
- [x] Q1：ACP-IBM 与 ACP-Zed 是否同一物？**否**——三方独立信源确认无关联；且发现第三个撞名 ACP（OpenAI Agentic Commerce Protocol，电商支付场景）
- [x] Q2：MCP 的 SSE 传输是否已废弃，官方原话？**部分废弃**——独立"HTTP+SSE"传输 2025-03-26 起 Deprecated(SEP-2596)，被Streamable HTTP取代；SSE本身作为Streamable HTTP的可选流式方式被保留

## R1 分工计划（6 workers，按来源边界拆）
1. r1-mcp：MCP 官方 spec/文档站（modelcontextprotocol.io + GitHub spec repo）→ 填 MCP 整行 + Q2
2. r1-a2a：A2A 官方站（a2a-protocol.org / GitHub a2aproject）→ 填 A2A 整行 + 治理归属
3. r1-acp-ibm：ACP-IBM 官方页（agentcommunicationprotocol.dev / GitHub i-am-bee 或 IBM）→ 填 ACP-IBM 整行 + 现状（是否合并/存续）
4. r1-acp-zed：ACP-Zed 官方页（agentclientprotocol.com / GitHub zed-industries）→ 填 ACP-Zed 整行 + 与 LSP 类比 + Q1 的 Zed 侧证据
5. r1-agui：AG-UI 官方页（ag-ui.com / GitHub ag-ui-protocol）→ 填 AG-UI 整行 + 与 MCP/A2A 关系声明
6. r1-scout-vendors：大厂矩阵 scout——OpenAI/Anthropic/Google/Microsoft 官方博客/文档中对 MCP/A2A/ACP/AG-UI 的支持声明；顺带收集 leads（鉴权细节、governance 机构全称、遗漏的实体或维度）
