# r2-anthropic
question: Which of MCP / A2A / IBM ACP / Zed ACP / AG-UI does Anthropic official docs support; MCP connector params, headers, transport limits; proprietary variant?
checked: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | https://platform.claude.com/docs/en/api/beta-headers | https://platform.claude.com/llms.txt | https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview | https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration | https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai

## claims
- [C1] MCP supported: Messages API "MCP connector" connects to remote MCP servers w/o client; page featureMetadata status: beta, betaHeader `mcp-client-2025-11-20`. | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | quote: "connect to remote MCP servers directly from the Messages API without a separate MCP client" | type: official
- [C2] Request param `mcp_servers` (array) defines servers; fields `type` (only "url"), `url` ("Must start with https://"), `name`, optional `authorization_token` (OAuth). | src: same | quote: "MCP server definition (`mcp_servers` array): Defines server connection details (URL, authentication)" | type: official
- [C3] `tools` array holds `{"type":"mcp_toolset","mcp_server_name":...}` with `default_config`, `configs` (per-tool `enabled`, `defer_loading`), `cache_control`. | src: same | quote: "The MCPToolset lives in the `tools` array and configures which tools from the MCP server are enabled" | type: official
- [C4] Beta sent via `anthropic-beta` request header (SDK `betas` param); cURL example shows `-H "anthropic-beta: mcp-client-2025-11-20"`. | src: https://platform.claude.com/docs/en/api/beta-headers | quote: "To access beta features, include the `anthropic-beta` header in your API requests" | type: official
- [C5] Transport limits: remote HTTP only, Streamable HTTP + SSE; no stdio; only MCP tool calls (no prompts/resources via connector). | src: mcp-connector | quote: "The server must be publicly exposed through HTTP (supports both Streamable HTTP and SSE transports). Local STDIO servers cannot be connected directly." | type: official
- [C6] Only tool calls supported: "Of the feature set of the MCP specification, only tool calls are currently supported." Client-side SDK helpers cover stdio/prompts/resources (`pip install "anthropic[mcp]"`, `@anthropic-ai/sdk/helpers/beta/mcp`). | src: same | type: official
- [C7] Response block types: `mcp_tool_use` (id `mcptoolu_...`, `server_name`), `mcp_tool_result`; plus `mcp_tool_listing` under `mcp-client-2026-09-15`. | src: same | quote: "the response includes two new content block types" | type: official
- [C8] `mcp-client-2026-09-15` records/pins server tool lists; MCPToolset accepts `tools` array of {name,description,input_schema}. | src: same | quote: "It includes everything `mcp-client-2025-11-20` does, so send it in place of that header." | type: official
- [C9] `mcp-client-2025-04-04` deprecated; old shape put `tool_configuration`{`enabled`,`allowed_tools`} inside server def; migrate to MCPToolset. | src: same | quote: "The previous version of this feature (`mcp-client-2025-04-04`) is deprecated." | type: official
- [C10] Platform availability (featureMetadata): beta on Claude API, Claude Platform on AWS, Microsoft Foundry; "not available" Amazon Bedrock / Google Cloud; `zdr: not-eligible`. | src: same | type: official
- [C11] `inline-tools-2026-09-15` beta additionally allows adding an MCP server mid-conversation. | src: same | quote: "With the `inline-tools-2026-09-15` beta header as well, you can add an MCP server partway through a conversation." | type: official
- [C12] `mcp_servers` allowed in Message Batches API requests. | src: same | quote: "You can include `mcp_servers` in Message Batches API requests." | type: official
- [C13] Proprietary connectivity (still MCP): "MCP tunnels" research preview — cloudflared + Anthropic proxy reach private-network MCP servers; Tunnels API uses beta `mcp-tunnels-2026-06-22` on `/v1/tunnels`. | src: https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview ; https://platform.claude.com/docs/en/api/beta-headers | quote: "connect Claude to Model Context Protocol (MCP) servers that run inside your private network" | type: official
- [C14] Proprietary agent-to-agent mechanism (not A2A): Managed Agents `multiagent:{type:"coordinator",agents:[...]}` + `agent_toolset_20260401`; SSE thread events `agent.thread_message_received`/`agent.thread_message_sent`; beta `managed-agents-2026-04-01`. | src: https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration | quote: "each agent runs in its own **session thread**, a context-isolated event stream with its own conversation history" | type: official
- [C15] A2A only on marketing page: Anthropic+Google Cloud webinar "Deploying multi-agent systems using MCP and A2A with Claude on Vertex AI" (recorded event, Aug 27 2025). No A2A in API docs. | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "multi-agent systems using Model Context Protocol (MCP) and Agent-to Agent protocol (A2A) with Claude on Vertex AI" | type: official
- [C16] Endpoint-specific beta headers table: `/v1/agents`,`/v1/sessions`,`/v1/environments`→`managed-agents-2026-04-01`; `/v1/tunnels`→`mcp-tunnels-2026-06-22`; `/v1/memory_stores`→`agent-memory-2026-07-22`. | src: https://platform.claude.com/docs/en/api/beta-headers | type: official

## conflicts
- none (mcp-client-2026-09-15 is documented as superset of mcp-client-2025-11-20, not a contradiction; prior-round note of both headers is consistent).

## gaps
- https://platform.claude.com/llms.txt (full 637-page EN index) + site searches: no page contains "A2A", "Agent Client Protocol", "AG-UI", "Agent Communication Protocol", "agent2agent" (grep of fetched index + page: 0 hits).
- https://platform.claude.com/docs/en/agents-and-tools/mcp-connector : no mention of A2A / ACP / AG-UI / Agent Communication Protocol.
- anthropic.com: ACP (Zed), AG-UI, IBM Agent Communication Protocol not found in site search; only MCP + one A2A webinar.
- Whether claude.ai product connectors UI uses any non-MCP protocol: not verified (product docs not fetched).

## leads
- Managed Agents SSE event stream detail: https://platform.claude.com/docs/en/managed-agents/events-and-streaming
- Anthropic remote MCP server catalog: https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers
- github.com/anthropics SDK MCP helpers; MCP spec ref used: modelcontextprotocol.io spec 2025-11-25.
