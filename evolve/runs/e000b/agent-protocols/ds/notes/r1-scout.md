# r1-scout
question: OpenAI、Anthropic、Google、Microsoft 四家官方文档/博客里，各自公开声明支持 MCP / A2A / ACP（Zed 的 Agent Client Protocol）/ AG-UI 中的哪些？有没有自家的协议变体或竞品？除了五个主要协议外还有哪些值得收录的关联协议？
checked: https://learn.chatgpt.com/docs/extend/mcp?surface=cli, https://www.anthropic.com/news/model-context-protocol, https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/, https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/ui/ag-ui/, https://zed.dev/acp, https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation, https://docs.ag-ui.com/, https://agntcy.org/, https://www.ibm.com/think/topics/agent-communication-protocol

## claims
- [C1] OpenAI officially supports MCP in ChatGPT Developer Mode (September 2025 beta), ChatGPT desktop, and Agents SDK | src: https://learn.chatgpt.com/docs/extend/mcp?surface=cli | quote: "MCP connects models to tools and context, allowing ChatGPT and Codex to access third-party documentation" | type: official
- [C2] Anthropic originated and maintains MCP (Model Context Protocol), donating it to Linux Foundation's Agentic AI Foundation in 2024 | src: https://www.anthropic.com/news/model-context-protocol | quote: "a universal, open standard for connecting AI systems with data sources, replacing fragmented integrations" | type: official
- [C3] Anthropic Claude SDK and Claude Managed Agents support AG-UI protocol for agent-user interaction | src: https://docs.ag-ui.com/integrations | quote: "Claude Managed Agents and Claude Agent SDK... are served over AG-UI in TypeScript, Python, and .NET" | type: official
- [C4] Google originated A2A (Agent2Agent Protocol) and provides A2A support through Agent Development Kit (ADK) and Gemini Enterprise | src: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ | quote: "A2A complements Anthropic's Model Context Protocol (MCP), which provides helpful tools and context to agents" | type: official
- [C5] Google ADK supports AG-UI protocol with documentation and demos available | src: https://docs.ag-ui.com/integrations | quote: "Google ADK is supported with documentation and demos" | type: official
- [C6] Microsoft Agent Framework (v1.0, April 3 2026) provides native support for MCP, A2A, and AG-UI protocols | src: https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/ | quote: "native MCP and A2A support" | type: official
- [C7] Zed developed Agent Client Protocol (ACP) standardizing agent-editor communication, adopted by Google (Gemini CLI) and other platforms | src: https://zed.dev/acp | quote: "open standard that enables any agent to integrate seamlessly with any editing environment" | type: official
- [C8] IBM developed Agent Communication Protocol (ACP) for agent-to-agent REST-based communication; merging with Google's A2A under Linux Foundation governance (2025) | src: https://www.ibm.com/think/topics/agent-communication-protocol | quote: "REST-based standard developed by IBM's BeeAI team... ACP has merged with A2A under the Linux Foundation umbrella" | type: official
- [C9] OpenAI created AGENTS.md as founding project of Agentic AI Foundation (launched December 2024 with Anthropic, Block, Google, Microsoft, AWS, Cloudflare, Bloomberg) | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "AGENTS.md by OpenAI as founding projects" | type: official
- [C10] Cisco-donated AGNTCY (Linux Foundation project, 65+ supporting companies) provides infrastructure for agent discovery, identity, messaging, and observability using Secure Low-Latency Interactive Messaging protocol | src: https://agntcy.org/ | quote: "AGNTCY... enables discovery, identity, messaging, and observability among AI agents from different vendors" | type: official
- [C11] Language Server Protocol (LSP) explicitly influenced MCP's design; both use JSON-RPC 2.0 and capability negotiation at connection time | src: https://dev.to/jozu/securing-mcp-applying-lessons-learned-from-the-language-server-protocol-338 | quote: "Anthropic introduced the Model Context Protocol, citing LSP as a design influence... MCP takes some inspiration from Language Server Protocol" | type: official
- [C12] OpenAI Agents SDK, Responses API, and ChatGPT desktop app announced March 2025 MCP support with Sam Altman stating adoption | src: https://openai.github.io/openai-agents-python/mcp/ | quote: "You can now connect your Model Context Protocol servers to Agents SDK" | type: official
- [C13] Microsoft partners with Anthropic to create official C# SDK for Model Context Protocol | src: https://developer.microsoft.com/blog/microsoft-partners-with-anthropic-to-create-official-c-sdk-for-model-context-protocol/ | quote: "Microsoft... create official C# SDK for the Model Context Protocol" | type: official
- [C14] Google Gemini Enterprise supports A2A protocol for agent-to-agent communication with Agent-to-UI (A2UI) for custom interfaces | src: https://docs.cloud.google.com/gemini/enterprise/docs/a2ui-agents/register-and-manage-an-a2ui-agent | quote: "Gemini Enterprise administrators can register agents... using A2UI... and A2A Protocol for communication" | type: official
- [C15] Agentic AI Foundation (AAIF) created by Anthropic, Block, OpenAI with Google, Microsoft, AWS, Cloudflare, Bloomberg support; governs MCP, AGENTS.md (OpenAI), and Goose (Block) | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "Agentic AI Foundation... co-founded by Anthropic, Block and OpenAI, with support from Google, Microsoft, AWS, Cloudflare and Bloomberg" | type: official

## conflicts
- IBM ACP (Agent Communication Protocol, REST-based, March 2025) vs Zed ACP (Agent Client Protocol, HTTP-based for editor integration): Both abbreviated ACP but serve different purposes; IBM ACP merging into A2A under Linux Foundation, while Zed ACP remains independent editor protocol
  - IBM ACP src: https://www.ibm.com/think/topics/agent-communication-protocol | quote: "REST-based standard developed by IBM"
  - Zed ACP src: https://zed.dev/acp | quote: "open standard that enables any agent to integrate seamlessly with any editing environment"

## gaps
- No evidence found of OpenAI official support for Zed's ACP (Agent Client Protocol) in docs or announcements
- No evidence found of Anthropic official support for A2A protocol despite Google's claim of complementarity
- Microsoft's stance on Zed ACP (Agent Client Protocol) not mentioned in Agent Framework documentation
- Whether Google supports IBM's ACP variant or only A2A unclear; Zed's ACP mentioned only with Gemini CLI prototype
- Whether AG-UI is officially part of AAIF governance or remains community-driven unclear
- Exact relationship between A2UI (Agent-to-UI, Gemini Enterprise) and AG-UI protocol needs clarification

## leads
- **R2 priority URLs per company:**
  - OpenAI: https://openai.github.io/openai-agents-python/mcp/ (Agents SDK docs, March 2025 announcement), https://learn.chatgpt.com/docs/extend/mcp?surface=cli (ChatGPT MCP docs)
  - Anthropic: https://www.anthropic.com/news/model-context-protocol (MCP origin announcement), https://docs.claude.com (Claude API/SDK integration points for MCP and AG-UI)
  - Google: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ (A2A announcement), https://docs.cloud.google.com/gemini/enterprise/docs/ (Gemini Enterprise A2A/A2UI support)
  - Microsoft: https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/ (Agent Framework v1.0 with MCP/A2A/AG-UI), https://learn.microsoft.com/en-us/agent-framework/ (full Agent Framework docs)

- **Grid dimensions found beyond initial five protocols:**
  - ACP-IBM (Agent Communication Protocol, REST-based, 2025): merging with A2A, governs enterprise agent communication
  - AGNTCY (Cisco/Linux Foundation, 65+ companies): infrastructure layer for agent discovery/identity/messaging/observability
  - AGENTS.md (OpenAI, AAIF founding project): competing or complementary to MCP?
  - A2UI (Google Gemini Enterprise): custom UI spec distinct from AG-UI
  - Goose (Block, AAIF founding project): nature/scope not yet clear

- **Agntcy relationship findings:**
  - AGNTCY is infrastructure layer (discovery/messaging/observability) under Linux Foundation
  - A2A (Google) defines message formats and interaction patterns for direct agent-to-agent communication
  - ACP-IBM (merged into A2A) was REST-based agent communication protocol
  - Relationship: AGNTCY provides plumbing; A2A/ACP-IBM provide protocols; they complement not compete
  - All three now governed by Linux Foundation under AAIF umbrella

- **LSP-MCP relationship (documented):**
  - Anthropic explicitly cites LSP as design influence for MCP
  - Both use JSON-RPC 2.0 messaging and capability negotiation
  - LSP abstraction for IDE-compiler integration; MCP analogous for AI tools-context integration
  - No direct mention of LSP relationship to A2A, AG-UI, or ACP in official docs (second-level protocols evolved independently)
