# agent-protocols 参考答案（供人工检查用）

## 疑惑 1：网传的两个「ACP」是不是一回事？

不是一回事，是两个完全独立、只是撞了缩写的协议，其中一个现在已经死了：

- **IBM 的 Agent Communication Protocol（ACP）**：IBM Research 为自家 BeeAI 平台做的智能体通信协议，2025 年 3 月随 BeeAI 捐给 Linux Foundation。2025 年 8 月正式宣布并入 A2A（Agent2Agent），团队不再把它当独立协议继续开发，原仓库已归档，文档转去指引迁移到 A2A。
  来源：https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
- **Zed 的 Agent Client Protocol（也叫 ACP）**：Zed Industries 2025 年 8 月发布，标准化「编辑器」和「编码 agent」之间的通信（JSON-RPC over stdio，思路类似 LSP），现在仍在活跃发展，JetBrains、Google（Gemini CLI）、OpenAI Codex 等都已接入，2025 年 10 月起社区化治理（agentclientprotocol.com / github.com/zed-industries/agent-client-protocol）。
  来源：https://github.com/zed-industries/agent-client-protocol ，https://agentclientprotocol.com/
- 顺带一提：还有第三个「ACP」——AGNTCY 的 Agent Connect Protocol，也已在 2026 年归档并转向推荐 A2A，进一步说明「ACP」这个缩写历史上被撞了多次，现在活着的基本只剩 Zed 这个。

## 疑惑 2：MCP 的 SSE 传输是否已经废弃？

确认为真，而且比很多文章讲的还要新一步：

- 2025-03-26 版 MCP 规范就已经用 **Streamable HTTP** 取代旧的 **HTTP+SSE** 传输，旧传输当时就被标记为 deprecated，只允许保留用于向后兼容。
  来源：https://modelcontextprotocol.io/specification/2025-03-26/basic/transports
- 2026-07-28 的规范修订更进一步：把 legacy HTTP+SSE 传输正式重新分类为生命周期状态「Deprecated」（SEP-2596），给了大约一年的下线过渡期（offramp）；同一次修订里 Streamable HTTP 自身的可恢复性特性（`Last-Event-ID`／SSE 事件重放）也被移除，以及 Roots / Sampling / Logging 三个特性同时被标记废弃（至少还能用 12 个月）。
  来源：https://blog.modelcontextprotocol.io/posts/2026-07-28/
- 现状：stdio 和 Streamable HTTP 是目前官方定义的两种标准传输；HTTP+SSE 只是「还没死透」，新项目不应该再选它。

## 大厂支持情况一览（OpenAI / Anthropic / Google / 微软）

- **Anthropic**：MCP 的创造者（2024 年 11 月开源），Messages API 自带 `MCP connector`，可以不写 MCP client 直连远程 MCP 服务器，原生支持 OAuth Bearer token 鉴权。
  来源：https://platform.claude.com/docs/en/agents-and-tools/mcp-connector
- **OpenAI**：Responses API 原生支持接「remote MCP servers」或「Secure MCP Tunnel」，服务器可选 Streamable HTTP 或 HTTP/SSE 传输；没有官方自创的智能体互通协议变体，走的是 MCP + 自家 Agents SDK/AgentKit。
  来源：https://developers.openai.com/api/docs/guides/tools-connectors-mcp
- **Google**：A2A 的创造者（2025 年 4 月发布，随后捐给 Linux Foundation），自家 Agent Development Kit（ADK）同时是 MCP client（可用外部 MCP 工具）也能把 ADK 工具包成 MCP server。
  来源：https://a2a-protocol.org/latest/ ，https://adk.dev/mcp/
- **微软**：Microsoft Foundry Agent Service 两个协议都接：A2A 的 `a2a` 工具对应协议版本 1.0，状态已 GA，旧的 0.3 版本仍是 preview；同时 Foundry 也支持挂 MCP 工具/远程 MCP 服务器。微软也是 A2A 技术指导委员会成员之一。
  来源：https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/agent-to-agent
- 没有发现这四家里谁又发明了第五个「自家变体」协议——目前趋势反而是收敛：2025 年 12 月 Linux Foundation 成立 Agentic AI Foundation（AAIF），把 MCP 也收进来做中立治理，白金会员正好是 AWS、Anthropic、Block、Bloomberg、Cloudflare、Google、Microsoft、OpenAI 这些大厂。
  来源：https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation

## 其他常见问题

- **鉴权**：MCP 一侧主要靠 OAuth（Anthropic 的 MCP connector 用 OAuth Bearer token）；A2A 一侧鉴权是连接级的，微软 Foundry 给 A2A 连接开放了 none / custom-keys / OAuth2 / Entra token 等多种方式，实际由 Agent Card 里声明的 security scheme 决定。
- **版本**：MCP 用日期当版本号（2024-11-05 → 2025-03-26 → 2025-06-18 → 2026-07-28，逐版有 changelog）；A2A 用语义化版本号，2025 年 7 月还是 v0.3.0，2026 年 1 月发布 v1.0.0。
- **谁在治理**：MCP 由 Anthropic 发起，2025 年 12 月起并入 Linux Foundation 旗下新设的 Agentic AI Foundation（AAIF）；A2A 由 Google 发起，2025 年 6 月已捐给 Linux Foundation，由技术指导委员会（含 Google/Microsoft/AWS/Cisco/Salesforce/ServiceNow/SAP/IBM 代表）维护，2025 年 8 月吸收了 IBM 的 ACP；Zed 的 Agent Client Protocol 由 Zed 发起，2025 年 10 月起社区化（agentclientprotocol.com），JetBrains 是共同开发方之一；AG-UI 由 CopilotKit 发起并维护。
- **怎么选**：按「连接对象」分层最直观——模型/agent 要接工具和数据，用 MCP；agent 要和别的 agent 协作分工，用 A2A；agent 要把状态/工具调用流式推给终端用户界面，用 AG-UI；如果是在写编辑器/IDE 插件，去接第三方编码 agent，用 Zed 的 Agent Client Protocol（不是 IBM 那个已经死掉的 ACP）。这个三层划分是 AG-UI 官方文档自己给的定位。
  来源：https://docs.ag-ui.com/introduction
