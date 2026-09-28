# r2-microsoft
question: Which of MCP / A2A / IBM ACP / Zed ACP / AG-UI do Microsoft official docs (Microsoft Learn, Agent Framework, Copilot Studio, NLWeb) support? Is NLWeb (or another MS protocol) an in-house variant, and how does Microsoft describe its relation to MCP?
checked: https://learn.microsoft.com/en-us/agents/architecture/multi-agent-patterns ; https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/agent-services/a2a ; https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/ ; https://learn.microsoft.com/en-us/agent-framework/integrations/ ; https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent ; https://github.com/nlweb-ai/NLWeb (README; former github.com/microsoft/NLWeb)

## claims
- [C1] Microsoft Learn recommends MCP for tool/data access: "use Model Context Protocol (MCP) for secure, authenticated access to tools and data" and "It's the recommended way to surface data and actions to agents" | src: https://learn.microsoft.com/en-us/agents/architecture/multi-agent-patterns | quote: "Use MCP for tool and data access, including Microsoft 365 service tools." | type: official | ms.date 2026-07-06
- [C2] Same page recommends A2A for cross-platform agents | src: https://learn.microsoft.com/en-us/agents/architecture/multi-agent-patterns | quote: "Use Linux Foundation Agent2Agent (A2A) protocol for cross-platform agent integration with published contracts" | type: official | ms.date 2026-07-06
- [C3] Microsoft frames MCP and A2A as complementary, not competing | src: https://learn.microsoft.com/en-us/agents/architecture/multi-agent-patterns | quote: "MCP (Model Context Protocol) and A2A (Linux Foundation's Agent2Agent) are complementary open source standards for building agentic applications." | type: official
- [C4] Agent Framework ships `A2AAgent` wrapping remote A2A endpoints as `AIAgent`; packages `Microsoft.Agents.AI.A2A` (.NET), `agent-framework-a2a` (Python), `provider/a2aprovider` (Go); also a "Host agents with A2A" server path | src: https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/agent-services/a2a | quote: "The `A2AAgent` enables your application to connect to remote agents that are exposed via the Agent-to-Agent (A2A) protocol." | type: official | ms.date 2026-09-16
- [C5] Copilot Studio connects to external agents via A2A | src: https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent | quote: "The Agent2Agent (A2A) protocol is an open standard for communication and collaboration between agents." | type: official | ms.date 2026-08-26
- [C6] Copilot Studio integration table maps MCP need to MCP servers | src: https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent | quote: "Use MCP tools or resources | MCP servers" | type: official
- [C7] Agent Framework supports AG-UI: exposes a MAF `AIAgent` as an AG-UI HTTP endpoint via `MapAGUIServer` (ASP.NET Core), `agent-framework-ag-ui` (Python/FastAPI), `aguiprovider` (Go); covers SSE streaming, HITL approvals, shared state, generative UI | src: https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/ | quote: "AG-UI is a standardized protocol for building AI agent interfaces" | type: official | ms.date 2026-09-08
- [C8] AG-UI integration release status is Preview | src: https://learn.microsoft.com/en-us/agent-framework/integrations/ | quote: "| [AG-UI](by-component/ui/ag-ui/) | Preview |" | type: official | ms.date 2026-08-31
- [C9] NLWeb natively supports MCP | src: https://github.com/nlweb-ai/NLWeb | quote: "It natively supports MCP (Model Context Protocol), allowing the same natural language APIs to serve both humans and AI agents." | type: official
- [C10] Every NLWeb instance is itself an MCP server; A2A planned, not yet shipped | src: https://github.com/nlweb-ai/NLWeb | quote: "Every NLWeb instance also acts as an MCP server (and soon A2A) and supports a core method, `ask`" | type: official
- [C11] NLWeb is Microsoft's own protocol layered above MCP/A2A, not an MCP variant | src: https://github.com/nlweb-ai/NLWeb | quote: "In short, NLWeb is to MCP/A2A what HTML is to HTTP." | type: official
- [C12] NLWeb's own protocol returns Schema.org JSON; spec hosted at nlweb.ai/spec | src: https://github.com/nlweb-ai/NLWeb | quote: "A simple protocol to interact with a site using natural language. It returns responses in JSON using Schema.org." | type: official
- [C13] Agent Framework integrations index lists only AG-UI, ChatKit, DevUI under UI protocols — no Agent Client Protocol or IBM ACP entries | src: https://learn.microsoft.com/en-us/agent-framework/integrations/ | quote: "UI: [AG-UI](by-component/ui/ag-ui/), [ChatKit](by-component/ui/chatkit), and [DevUI](by-component/ui/devui/)" | type: official
- [C14] VS Code uses Microsoft's own Agent Host Protocol (AHP) — open JSON-RPC between Agent Host and clients — at the editor/agent-client layer where Zed's ACP sits; `@microsoft/agent-host-protocol` client lib | src: https://code.visualstudio.com/blogs/2026/08/26/agent-host-architecture | quote: "AHP is the open, agent-agnostic JSON-RPC protocol connecting the Agent Host (server role) to clients" | type: official (code.visualstudio.com, MS domain but outside listed policy set)

## conflicts
- none

## gaps
- Zed Agent Client Protocol (ACP): not mentioned on any checked page (multi-agent patterns, AF integrations index, AG-UI page); site search returned no exact match — only checked pages, cannot say "unsupported" globally
- IBM Agent Communication Protocol: not mentioned on checked pages; site search returned no match on learn.microsoft.com
- Copilot Studio native AG-UI or ACP support: not checked directly (only A2A page fetched)

## leads
- IBM Research states ACP merged into Linux Foundation A2A (Aug 2025), spec archived: https://research.ibm.com/projects/agent-communication-protocol — explains MS docs only naming A2A
- Copilot Studio MCP server docs likely at learn.microsoft.com/en-us/microsoft-copilot-studio/ (search "copilot studio MCP server")
- NLWeb spec: https://nlweb.ai/spec ; repo moved microsoft/NLWeb → nlweb-ai/NLWeb (contact NLWebSup@microsoft.com)
- AF "Host agents with A2A" server page: learn.microsoft.com/en-us/agent-framework/hosting/self-hosting/a2a/server
