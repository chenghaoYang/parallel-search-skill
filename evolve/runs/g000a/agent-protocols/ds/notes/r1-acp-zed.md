# r1-acp-zed
question: Zed 的 ACP（Agent Client Protocol，不是 IBM 的 Agent Communication Protocol）官方规范现在规定谁和谁通信、一等对象与方法原名、传输、发现、鉴权、版本、治理、状态放在哪一端、它和 MCP 的官方关系。
checked: https://agentclientprotocol.com/llms.txt, https://agentclientprotocol.com/get-started/introduction.md, https://agentclientprotocol.com/get-started/architecture.md, https://agentclientprotocol.com/protocol/v1/overview.md, https://agentclientprotocol.com/protocol/v1/initialization.md, https://agentclientprotocol.com/protocol/v1/authentication.md, https://agentclientprotocol.com/protocol/v1/session-setup.md, https://agentclientprotocol.com/protocol/v1/transports.md, https://agentclientprotocol.com/protocol/v1/schema.md, https://agentclientprotocol.com/protocol/v2/overview.md, https://agentclientprotocol.com/protocol/v2/transports.md, https://agentclientprotocol.com/get-started/registry.md, https://agentclientprotocol.com/get-started/agents.md, https://agentclientprotocol.com/get-started/clients.md, https://agentclientprotocol.com/community/governance.md, https://agentclientprotocol.com/rfds/about.md, https://agentclientprotocol.com/announcements/acp-v2-draft.md, https://agentclientprotocol.com/announcements/acp-agent-registry-stabilized.md, https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/README.md, https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/meta.json

## claims
- [C1] ACP-Zed.edge：全称 Agent Client Protocol（ACP），连接 code editors/IDEs 与 coding agents。 | src: https://agentclientprotocol.com/get-started/introduction.md | quote: "The Agent Client Protocol (ACP) standardizes communication between code editors/IDEs and coding agents and is suitable for both local and remote scenarios." | type: official
- [C2] ACP-Zed.edge：角色原名 Agents 与 Clients。 | src: https://agentclientprotocol.com/protocol/v1/overview.md | quote: "The Agent Client Protocol allows Agents and Clients to communicate by exposing methods that each side can call and sending notifications to inform each other of events." | type: official
- [C3] ACP-Zed.edge：本地 Agent 是编辑器子进程，走 JSON-RPC over stdio。 | src: https://agentclientprotocol.com/get-started/introduction.md | quote: "Local agents run as sub-processes of the code editor, communicating via JSON-RPC over stdio." | type: official
- [C4] ACP-Zed.objects：方法 initialize。 | src: https://agentclientprotocol.com/protocol/v1/overview.md | quote: "Client → Agent: `initialize` to establish connection" | type: official
- [C5] ACP-Zed.objects：方法 authenticate。 | src: https://agentclientprotocol.com/protocol/v1/overview.md | quote: "Client → Agent: `authenticate` if required by the Agent" | type: official
- [C6] ACP-Zed.objects：方法 session/new。 | src: https://agentclientprotocol.com/protocol/v1/overview.md | quote: "Client → Agent: `session/new` to create a new session" | type: official
- [C7] ACP-Zed.objects：方法 session/prompt。 | src: https://agentclientprotocol.com/protocol/v1/overview.md | quote: "Client → Agent: `session/prompt` to send user message" | type: official
- [C8] ACP-Zed.wire：编码是 JSON-RPC 2.0。 | src: https://agentclientprotocol.com/protocol/v1/overview.md | quote: "The protocol follows the JSON-RPC 2.0 specification with two types of messages:" | type: official
- [C9] ACP-Zed.wire：stdio 上 agent 读 stdin、写 stdout。 | src: https://agentclientprotocol.com/protocol/v1/transports.md | quote: "The agent reads JSON-RPC messages from its standard input (`stdin`) and sends messages to its standard output (`stdout`)." | type: official
- [C10] ACP-Zed.discovery：Registry 用来发现、安装、配置 agents。 | src: https://agentclientprotocol.com/announcements/acp-agent-registry-stabilized.md | quote: "The registry gives ACP clients a standard way to discover, install, and configure compatible agents." | type: official
- [C11] ACP-Zed.discovery：目录地址 registry/v1/latest/registry.json。 | src: https://agentclientprotocol.com/get-started/registry.md | quote: "curl https://cdn.agentclientprotocol.com/registry/v1/latest/registry.json" | type: official
- [C12] ACP-Zed.auth：initialize 响应字段 authMethods。 | src: https://agentclientprotocol.com/protocol/v1/authentication.md | quote: "Agents advertise authentication options in the `authMethods` field of the `initialize` response." | type: official
- [C13] ACP-Zed.version：稳定协议版本是 1。 | src: https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/README.md | quote: "The current stable ACP protocol version is `1`." | type: official
- [C14] ACP-Zed.version：initialize 中的协议版本是单个整数 MAJOR。 | src: https://agentclientprotocol.com/protocol/v1/initialization.md | quote: "The protocol versions that appear in the `initialize` requests and responses are a single integer that identifies a MAJOR protocol version." | type: official
- [C15] ACP-Zed.version：version 2 仍是 Draft。 | src: https://agentclientprotocol.com/announcements/acp-v2-draft.md | quote: "v2 is a Draft" | type: official
- [C16] ACP-Zed.gov：Zed 与 JetBrains 共同治理。 | src: https://agentclientprotocol.com/community/governance.md | quote: "ACP is jointly governed by Zed and JetBrains, who collaborate to ensure the protocol serves the broader ecosystem." | type: official
- [C17] ACP-Zed.gov：lead maintainers 是 Ben Brandt（Zed Industries）与 Sergey Ignatov（JetBrains）。 | src: https://agentclientprotocol.com/community/governance.md | quote: "ACP has two lead maintainers: Ben Brandt (Zed Industries) and Sergey Ignatov (JetBrains)." | type: official
- [C18] ACP-Zed.state：session 自带 context、conversation history 与 state。 | src: https://agentclientprotocol.com/protocol/v1/session-setup.md | quote: "Each session maintains its own context, conversation history, and state, allowing multiple independent interactions with the same Agent." | type: official
- [C19] ACP-Zed.state：由 Agent 恢复 session context 与 conversation history。 | src: https://agentclientprotocol.com/protocol/v1/schema.md | quote: "Restore the session context and conversation history" | type: official
- [C20] ACP-Zed.compose：全称 Model Context Protocol。 | src: https://agentclientprotocol.com/protocol/v1/session-setup.md | quote: "The Model Context Protocol (MCP) allows Agents to access external tools and data sources." | type: official
- [C21] ACP-Zed.compose：agent 直接连接编辑器传来的 MCP server。 | src: https://agentclientprotocol.com/get-started/architecture.md | quote: "This allows the agent to connect directly to the MCP server." | type: official

## conflicts
- 方法名：v1 “Client → Agent: `authenticate` if required by the Agent”；v2 “Client → Agent: `auth/login` if required by the Agent”，并要求 `auth/login` 与 `auth/logout`。src: https://agentclientprotocol.com/protocol/v1/overview.md , https://agentclientprotocol.com/protocol/v2/overview.md
- 回合：v1 “the `session/prompt` response with a stop reason”；v2 “`session/prompt` response once the prompt is accepted”。src: https://agentclientprotocol.com/protocol/v1/overview.md , https://agentclientprotocol.com/protocol/v2/overview.md
- 传输：introduction “communicating over HTTP or WebSocket”；v1/v2 均写 “Streamable HTTP (draft proposal in progress)”。v1 消息为 individual requests；v2 增加 batch arrays。src: https://agentclientprotocol.com/get-started/introduction.md , https://agentclientprotocol.com/protocol/v1/transports.md , https://agentclientprotocol.com/protocol/v2/transports.md
- 治理：governance “jointly governed by Zed and JetBrains”；RFD 页 “the Zed team as the lead (BDFL)”。src: https://agentclientprotocol.com/community/governance.md , https://agentclientprotocol.com/rfds/about.md

## gaps
- 已打开页、README、schema/v1/meta.json 均无 IBM 或 “Agent Communication Protocol”，不写与 BeeAI/IBM ACP 的差异。
- 未单列原句：UTF-8 编码；logout；MCP stdio MUST；鉴权类型 agent/terminal；Published July 20, 2026；v2.0.0-alphaX。无 OAuth/token，无 schema-v* semver。
- Clients 页点名 Zed；Agents 页点名 Junie by JetBrains。RFD 页有 “Request for Dialog (RFD)”。

## leads
- https://agentclientprotocol.com/rfds/streamable-http-websocket-transport.md 远程传输仍是 RFD。
- https://agentclientprotocol.com/rfds/mcp-over-acp.md 提议 MCP transport 类型 acp。
