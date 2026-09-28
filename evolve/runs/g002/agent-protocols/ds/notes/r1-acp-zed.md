# r1-acp-zed
question: Zed 的 Agent Client Protocol 官方规范里，全名、两端角色、核心方法、传输、会话状态、发现、鉴权、版本与治理，以及它是否把自己和 IBM 的 Agent Communication Protocol 或 MCP 放在一起说。
checked: https://agentclientprotocol.com/llms.txt, https://agentclientprotocol.com/get-started/introduction.md, https://agentclientprotocol.com/get-started/architecture.md, https://agentclientprotocol.com/get-started/registry.md, https://agentclientprotocol.com/protocol/v1/overview.md, https://agentclientprotocol.com/protocol/v1/initialization.md, https://agentclientprotocol.com/protocol/v1/authentication.md, https://agentclientprotocol.com/protocol/v1/session-setup.md, https://agentclientprotocol.com/protocol/v1/session-list.md, https://agentclientprotocol.com/protocol/v1/prompt-turn.md, https://agentclientprotocol.com/protocol/v1/transports.md, https://agentclientprotocol.com/protocol/v1/content.md, https://agentclientprotocol.com/protocol/v2/overview.md, https://agentclientprotocol.com/protocol/v2/prompt-lifecycle.md, https://agentclientprotocol.com/protocol/v2/migration.md, https://agentclientprotocol.com/community/governance.md, https://agentclientprotocol.com/rfds/about.md, https://agentclientprotocol.com/announcements/acp-v2-draft.md, https://agentclientprotocol.com/announcements/acp-agent-registry-stabilized.md, https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/README.md, https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/meta.json, https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v2/meta.json

## claims
- [C1] 全名 Agent Client Protocol（ACP），两端是 code editors/IDEs 与 coding agents。 | src: https://agentclientprotocol.com/get-started/introduction.md | quote: "standardizes communication between code editors/IDEs and coding agents" | type: official
- [C2] D1 Agent 是用生成式 AI 自主改代码的程序。 | src: https://agentclientprotocol.com/protocol/v1/overview.md | quote: "Agents are programs that use generative AI to autonomously modify code." | type: official
- [C3] D1 Client 通常是 IDE 或文本编辑器，也可以是其他 UI。 | src: https://agentclientprotocol.com/protocol/v1/overview.md | quote: "typically code editors (IDEs, text editors) but can also be other UIs" | type: official
- [C4] D2 遵循 JSON-RPC 2.0：Methods 要响应，Notifications 不要。 | src: https://agentclientprotocol.com/protocol/v1/overview.md | quote: "The protocol follows the JSON-RPC 2.0 specification" | type: official
- [C5] D2 v1 基线方法是 session/new、session/prompt、session/cancel、session/update。 | src: https://agentclientprotocol.com/protocol/v1/initialization.md | quote: "MUST support session/new, session/prompt, session/cancel, and session/update." | type: official
- [C6] D2 v1 meta 中相邻键：session/load、session/set_mode、session/set_config_option。 | src: https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/meta.json | quote: "\"session_load\": \"session/load\", \"session_set_mode\": \"session/set_mode\", \"session_set_config_option\": \"session/set_config_option\"" | type: official
- [C7] D2 v1 client 相邻键：fs/write_text_file、fs/read_text_file、terminal/create。 | src: https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/meta.json | quote: "\"fs_write_text_file\": \"fs/write_text_file\", \"fs_read_text_file\": \"fs/read_text_file\", \"terminal_create\": \"terminal/create\"" | type: official
- [C8] D2 v2：authMethods 非空则必须实现 auth/login 与 auth/logout。 | src: https://agentclientprotocol.com/protocol/v2/overview.md | quote: "MUST implement both auth/login and auth/logout." | type: official
- [C10] D2 v2 删除 Client 文件系统、终端执行和 session modes API。 | src: https://agentclientprotocol.com/protocol/v2/migration.md | quote: "The Client file system, terminal execution, and session modes APIs are gone." | type: official
- [C11] D3 规范要求 agent 与 client SHOULD 支持 stdio。 | src: https://agentclientprotocol.com/protocol/v1/transports.md | quote: "Agents and clients SHOULD support stdio whenever possible." | type: official
- [C12] D3 引言把远程写成 HTTP 或 WebSocket。 | src: https://agentclientprotocol.com/get-started/introduction.md | quote: "communicating over HTTP or WebSocket" | type: official
- [C14] D4 每个会话自带上下文、历史和状态。 | src: https://agentclientprotocol.com/protocol/v1/session-setup.md | quote: "Each session maintains its own context, conversation history, and state" | type: official
- [C16] D4 v1 的 stopReason 为 end_turn、max_tokens、max_turn_requests、refusal、cancelled。 | src: https://agentclientprotocol.com/protocol/v2/migration.md | quote: "end_turn, max_tokens, max_turn_requests, refusal, cancelled" | type: official
- [C15] D4 v2 的 idle 表示 Agent 可以处理新 prompt。 | src: https://agentclientprotocol.com/protocol/v2/prompt-lifecycle.md | quote: "The Agent is ready to process a new prompt." | type: official
- [C19] D5 Registry 页给出拉取地址 registry.json。 | src: https://agentclientprotocol.com/get-started/registry.md | quote: "curl https://cdn.agentclientprotocol.com/registry/v1/latest/registry.json" | type: official
- [C20] D5 公告：Registry 用于 discover、install、configure 兼容 agent。 | src: https://agentclientprotocol.com/announcements/acp-agent-registry-stabilized.md | quote: "discover, install, and configure compatible agents." | type: official
- [C21] D6 v1 缺省鉴权类型是 agent。 | src: https://agentclientprotocol.com/protocol/v1/authentication.md | quote: "The default authentication method type is agent" | type: official
- [C22] D6 session/request_permission 用来向用户请求工具授权。 | src: https://agentclientprotocol.com/protocol/v1/overview.md | quote: "Request user authorization for tool calls." | type: official
- [C23] D7 当前稳定 ACP 协议版本是 1。 | src: https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/README.md | quote: "The current stable ACP protocol version is 1." | type: official
- [C24] D7 v2 公告写明稳定前仍会改。 | src: https://agentclientprotocol.com/announcements/acp-v2-draft.md | quote: "various pieces can, and will, change before stabilization." | type: official
- [C25] D7 两位 lead：Ben Brandt (Zed Industries) 与 Sergey Ignatov (JetBrains)。 | src: https://agentclientprotocol.com/community/governance.md | quote: "Ben Brandt (Zed Industries) and Sergey Ignatov (JetBrains)." | type: official
- [C26] D9 不要把 MCP 和 ACP 跑在同一个 socket 上。 | src: https://agentclientprotocol.com/get-started/architecture.md | quote: "Instead of trying to run MCP and ACP on the same socket" | type: official
- [C29] D9 elicitation 写明 Unlike MCP：{} 不算 form 支持。 | src: https://agentclientprotocol.com/protocol/v1/initialization.md | quote: "Unlike MCP, ACP does not treat {} as form support." | type: official
- [C28] D9 已读全文的 introduction、rfds/about、architecture、governance、两版 overview、content、README、registry 均无 IBM，也无 “Agent Communication Protocol”。 | src: https://agentclientprotocol.com/get-started/introduction.md | quote: "standardized protocol for agent-editor communication" | type: official

## conflicts
- 传输： “HTTP or WebSocket” https://agentclientprotocol.com/get-started/introduction.md ； “all communication happens over stdin/stdout” https://agentclientprotocol.com/get-started/architecture.md ； “Streamable HTTP (draft proposal in progress)” https://agentclientprotocol.com/protocol/v1/transports.md ； “not part of the core v2 protocol surface” https://agentclientprotocol.com/protocol/v2/migration.md 。
- 治理： “jointly governed by Zed and JetBrains” https://agentclientprotocol.com/community/governance.md 对 “Zed team as the lead (BDFL)” https://agentclientprotocol.com/rfds/about.md 。
- v2： “v2 is a Draft” https://agentclientprotocol.com/announcements/acp-v2-draft.md 对 “stable v2 baseline” / “still labeled draft” https://agentclientprotocol.com/protocol/v2/migration.md 。

## gaps
- D8 未填。未打开 OpenAI、Anthropic、Google、Microsoft 自家文档。
- IBM 否定只覆盖 checked 里读过全文的页。无 FAQ 页，无 schema 制品号。
- 未单列：Apache-2.0；独立基金会仍是 “transitioning”；v2 还有 requires_action；Agent 通常是 Client 子进程。

## leads
- Registry 卡片有 Claude、Codex、Gemini CLI、Copilot，不是厂商文档。
- 未读远程传输 RFD：streamable-http-websocket-transport。
