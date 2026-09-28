# r1-scout
question: 在 MCP、A2A、IBM ACP、Zed ACP、AG-UI 范围内，用户还会踩到哪些名字碰撞或相邻协议？下一轮网格应加入哪些实体；四大厂各哪页官方文档最适合填「支持哪些协议/有无自家变体」。
checked: https://research.ibm.com/projects/agent-communication-protocol, https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/, https://agentclientprotocol.com, https://modelcontextprotocol.io/specification/2025-06-18/basic/transports, https://openai.github.io/openai-agents-python/mcp/, https://platform.claude.com/docs/en/agents-and-tools/mcp-connector, https://adk.dev/a2a/, https://learn.microsoft.com/en-us/agents/architecture/multi-agent-patterns, https://developers.openai.com/apps-sdk/concepts/mcp-server, https://agent-network-protocol.com/, https://ucp.dev/

## claims
- [C1] IBM 的 Agent Communication Protocol 已并入 A2A：IBM Research 官方项目页顶部公告（页面未标注日期，公告称 ACP 2025-03 随 BeeAI 捐给 Linux Foundation）。| src: https://research.ibm.com/projects/agent-communication-protocol | quote: "IMPORTANT UPDATE - ACP is now part of A2A under the Linux Foundation!" | type: official
- [C2] 合并是 IBM+Google 联合官宣：LF AI & Data 社区博客 2025-08-29（页面更新 2025-09-04），署名 Kate Blair（IBM Research）与 Todd Segal（Google）；ACP 停止独立开发，Blair 加入 A2A TSC。| src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "ACP is officially merging with the A2A under the Linux Foundation ... the ACP team will be winding down active development and will begin contributing its technology and expertise directly to A2A." | type: official
- [C3]「ACP」缩写同名碰撞：Zed 的 Agent Client Protocol 是「编辑器/IDE ↔ 编码 agent」协议（JSON-RPC over stdio 本地、远程走 HTTP/WebSocket，且"re-uses the JSON representations used in MCP"），与 IBM 已并入 A2A 的 Agent Communication Protocol（agent↔agent REST）是两个不同协议，网上"ACP"常指前者。| src: https://agentclientprotocol.com | quote: "The Agent Client Protocol (ACP) standardizes communication between code editors/IDEs and coding agents" | type: official
- [C4] MCP 传输弃用易误读：2025-06-18 版规范只定义 stdio 与 Streamable HTTP 两种标准传输；2024-11-05 版的独立 HTTP+SSE 传输已被明确标记 deprecated（但被 Streamable HTTP 取代≠SSE 消失，Streamable HTTP 内部仍用 SSE 流）。| src: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports | quote: "This replaces the HTTP+SSE transport from protocol version 2024-11-05. ... maintain backwards compatibility with the deprecated HTTP+SSE transport" | type: official
- [C5] 弃用后厂商仍接受 SSE：Anthropic MCP connector（beta header mcp-client-2025-11-20，另有更新的 mcp-client-2026-09-15）仍同时接受两种 HTTP 传输，且只支持 tool calls、不支持本地 stdio 服务器。| src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: "The server must be publicly exposed through HTTP (supports both Streamable HTTP and SSE transports). Local STDIO servers cannot be connected directly." | type: official
- [C6]「MCP Apps / OpenAI Apps SDK」不是独立协议：OpenAI 文档把 MCP Apps 描述为 MCP server 可返回的 UI resource 能力（配合 @modelcontextprotocol/ext-apps），Apps SDK 文档已并入 developers.openai.com/plugins 树。| src: https://developers.openai.com/apps-sdk/concepts/mcp-server | quote: "An MCP server can also return an optional UI resource for clients that support MCP Apps" | type: official

## conflicts
- 无实质冲突。接近一条：MCP 规范将 HTTP+SSE 标记 deprecated（C4），而 Anthropic connector 文档仍写"supports both Streamable HTTP and SSE transports"（C5）——不是互相矛盾，规范允许为兼容保留旧传输，但读者易误读为"SSE 已不可用"或"SSE 仍是标准传输"，网格写作时需点明。

## gaps
- OpenAI 是否在任何官方页把 function calling 称为"协议"：未取到原句，本轮未确认。
- AGNTCY（Cisco 系）是否真有第三个缩写为 ACP 的协议（传闻为 Agent Connect Protocol）：未打开官方页，未确认。
- a2a-protocol.org 规范本体未打开（本轮只从 adk.dev 链接确认其为 A2A 官方站）。
- MCP Apps 在 modelcontextprotocol.io 上的官方扩展规范页未打开（仅经 OpenAI 页间接确认存在 ext-apps）。

## leads
- Agent Network Protocol (ANP) | 面向"Agentic Web"的分层协议栈（did:wba 身份、发现、E2E 消息、支付），与 A2A 同层易被混为一谈；已打开首页显示 ANP 1.1 | https://agent-network-protocol.com/ （已打开）
- Universal Commerce Protocol (UCP) | 2026-01 由 Google 联合 Shopify/Microsoft/Amazon 等发布的 agentic commerce 协议，自述"Compatible with MCP, A2A"并内置 AP2——典型相邻协议 | https://ucp.dev/ （已打开）；规范 https://ucp.dev/latest/specification/overview/
- Agent Payments Protocol (AP2) | 支付授权 mandate 协议，UCP/ANP 页均引用；Google 系 | https://ap2-protocol.org/ （未打开）
- Agent Protocol（AI Engineer Foundation / agi-inc）| OpenAPI 3.0.1 REST 规范（/ap/v1/agent/tasks+steps+artifacts），client↔agent 层；通用名"agent protocol"易与整组混淆；LangGraph Platform 实现其超集 | https://github.com/AI-Engineer-Foundation/agent-protocol （未打开）；综述站 https://agentprotocol.ai （未打开，非官方）
- NLWeb (Natural Language Web, Microsoft) | Build 2025 发布，让网站以 NL 接口服务 agent；每个 NLWeb 实例同时是 MCP server，极易与 MCP/A2A 混读 | https://github.com/microsoft/NLWeb （未打开）；官宣 https://news.microsoft.com/source/features/company-news/introducing-nlweb-bringing-conversational-interfaces-directly-to-the-web （未打开）
- AGNTCY / Internet of Agents（Cisco 主导联盟）| 聚合多个 agent 互操作协议组件，可能含第三个"ACP"——下轮核实 | https://agntcy.org/ （未打开）
- OpenAI 入口 | https://openai.github.io/openai-agents-python/mcp/ （已打开）：讲支持——HostedMCPTool（Responses API 代调）+ MCPServerStdio/Sse/StreamableHttp 三类本地连接，页内警告"The MCP project has deprecated the Server-Sent Events transport"；自家变体入口为 Apps SDK https://developers.openai.com/apps-sdk/（子页已打开，现归入 plugins 文档树，基于 MCP+MCP Apps UI）
- Anthropic 入口 | https://platform.claude.com/docs/en/agents-and-tools/mcp-connector （已打开）：讲支持——Messages API 的 mcp_servers 参数直连远程 MCP server（beta）；注意 docs.anthropic.com 已 301 到 platform.claude.com。自家变体维度：MCP 本身是 Anthropic 主导规范 https://modelcontextprotocol.io/specification/2025-06-18/basic/transports（已打开）
- Google 入口 | https://adk.dev/a2a/ （已打开，自 google.github.io/adk-docs 重定向）：支持+自家混合——ADK 的 A2A exposing/consuming 指南；A2A 规范站 https://a2a-protocol.org/（未打开）即 Google 自家协议；UCP https://ucp.dev/（已打开）是更新的自家协议
- Microsoft 入口 | https://learn.microsoft.com/en-us/agents/architecture/multi-agent-patterns （已打开，ms.date 2026-07-06）：讲支持——官方建议 MCP 用于工具/数据、A2A 用于跨平台 agent 间通信，附 MCP vs A2A 对比表；实现细节在 Agent Framework A2A provider 页 https://learn.microsoft.com/en-us/agent-framework/agents/providers/agent-to-agent（未打开）
