# r2-counter-acp
question: 找反例推翻「IBM/BeeAI Agent Communication Protocol 与 Zed Agent Client Protocol 是两份不同规范」；并查 AGNTCY 是否发布第三份缩写为 ACP 的协议。
checked: https://agentclientprotocol.com/get-started/introduction | https://agentclientprotocol.com/llms.txt | https://agentclientprotocol.com/publications | https://agentcommunicationprotocol.dev/introduction/welcome | https://agentcommunicationprotocol.dev/llms.txt | https://agentcommunicationprotocol.dev/about/mcp-and-a2a | https://github.com/orgs/i-am-bee/discussions/5 | https://research.ibm.com/projects/agent-communication-protocol | https://zed.dev/blog/bring-your-own-agent-to-zed | https://github.com/agentclientprotocol/agent-client-protocol | https://github.com/agntcy/acp-spec | https://w3c-cg.github.io/ai-agent-protocol | https://docs.agntcy.org/pages/syntactic_sdk/connect.html (404)

## claims
- [C1] AGNTCY 确实发布过第三份缩写为 ACP 的协议，全名 Agent Connect Protocol：REST/OpenAPI 规范，定义"invoke and configure remote agents over an API"；规范仓 github.com/agntcy/acp-spec 于 2026-04-11 归档（read-only）。 | src: https://github.com/agntcy/acp-spec | quote: "This repo contains the specification of Agent Connect Protocol (ACP) proposed by the Agntcy Collective. The Agent Connect Protocol defines a standard interface to invoke and configure remote agents over an API." | type: official
- [C2] Zed 官方公告将自己协议命名为 Agent Client Protocol 并称"we created"之，JSON-RPC over stdio，editor↔agent；全文未提 IBM 的 Agent Communication Protocol，也无改名表述。 | src: https://zed.dev/blog/bring-your-own-agent-to-zed | quote: "we created the Agent Client Protocol (ACP)" | type: official
- [C3] Zed 官方站定义 ACP 为 editor/IDE↔coding agent 协议；llms.txt 全站索引（约 90 页）无任何 "Agent Communication Protocol" 条目。 | src: https://agentclientprotocol.com/get-started/introduction | quote: "standardizes communication between code editors/IDEs and coding agents" | type: official
- [C4] IBM/BeeAI 官方站定义其 ACP 为 agent↔agent RESTful API；全站 llms.txt 索引无 "Client Protocol" 页面；对比页 mcp-and-a2a 只与 MCP、A2A 比较，不提 Zed 协议。 | src: https://agentcommunicationprotocol.dev/introduction/welcome | quote: "enabling agents to communicate through a standardized RESTful API" | type: official
- [C5] IBM/BeeAI 官方合并公告只说 ACP 并入 A2A（Linux Foundation），未提及 Zed 的 Agent Client Protocol，不构成"同一协议/改名"证据。 | src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "ACP is officially merging with the A2A under the Linux Foundation" | type: official
- [C6] IBM Research 官方项目页独立描述 Agent Communication Protocol（REST、HTTP-native、agent-to-agent），未提及 Agent Client Protocol。 | src: https://research.ibm.com/projects/agent-communication-protocol | quote: "Agent Communication Protocol (ACP) is an open standard designed to enable seamless communication between AI agents" | type: official
- [C7] W3C CG 白皮书把 Agent Connect Protocol（Cisco/AGNTCY）与 Agent Communication Protocol（IBM/LF）列为两个独立条目分别评述——未涵盖 Zed 的 Agent Client Protocol（该文只讨论 agent-to-agent 网络协议）。 | src: https://w3c-cg.github.io/ai-agent-protocol | quote: "### Agent Connect Protocol (ACP) … ### Agent Communication Protocol (ACP)" | type: secondary
- [C8] Zed ACP GitHub 仓 README 定义为 editor↔coding-agent 协议，与 IBM 仓（i-am-bee/acp，REST）不同库不同规范。 | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: "standardizes communication between code editors … and coding agents" | type: official

## conflicts
- 无。未找到任何官方页声称两份 ACP 是同一协议、改名关系或共用规范；所有打开的一手页均支持"两份不同规范"的主张。

## gaps
- 未逐页打开 JetBrains 博客三篇 ACP 文章（仅经搜索摘要确认其只谈 editor↔agent）；zed.dev/acp、jetbrains.com/acp 落地页未直接打开。
- docs.agntcy.org 的旧 ACP 文档页（syntactic_sdk/connect.html）已 404/重构，AGNTCY ACP 细节仅依据已归档的 acp-spec 仓 README。
- 两个官方站点的站内全文搜索不可用；交叉引用检查依赖 llms.txt 索引与已打开页面。

## leads
- https://blog.jetbrains.com/ai/2025/10/jetbrains-zed-open-interoperability-for-ai-coding-agents-in-your-ide/ — JetBrains 官宣共建 ACP，可再核是否提及 IBM。
- https://github.com/agntcy/acp-sdk — AGNTCY ACP 的 SDK 仓（已归档）。
- https://spec.acp.agntcy.org/ — AGNTCY ACP OpenAPI 可视化（现疑似下线）。
- https://crystl.dev/blog/agent-communication-protocols/ 与 https://casys.ai/blog/mcp-a2a-acp-agent-protocols — 明确称"two ACPs / naming collision"的二手综述。
