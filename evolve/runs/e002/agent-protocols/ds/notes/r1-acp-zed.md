# r1-acp-zed
question: Zed 编辑器团队的 Agent Client Protocol（ACP）官方规范说了什么——拓扑、传输层、消息格式、鉴权、状态归属、版本规则、治理、采用者、与 LSP 类比、与 IBM ACP 撞名
checked: https://agentclientprotocol.com,https://github.com/zed-industries/agent-client-protocol,https://zed.dev/acp,https://blog.marcnuri.com/agent-client-protocol-acp-introduction,https://zed.dev/blog/acp-registry

## claims
- [C1] ACP 管什么交互：代码编辑器（Zed、JetBrains IDEs 等）与本地 agent 子进程间通信 | src: https://agentclientprotocol.com | quote: "standardizes communication between code editors and coding agents"
- [C2] 拓扑：Client 是编辑器/IDE，Server 是 agent 子进程 | src: https://zed.dev/acp | quote: "any agent to integrate seamlessly with any editing environment"
- [C3] 传输层（本地）：JSON-RPC 2.0 over stdin/stdout，newline-delimited JSON | src: https://blog.marcnuri.com/agent-client-protocol-acp-introduction | quote: "JSON-RPC 2.0 over stdin/stdout"
- [C4] 传输层（远程）：HTTP 和 WebSocket，远程支持开发中 | src: https://agentclientprotocol.com | quote: "Remote agents support HTTP/WebSocket (with ongoing development for full cloud support)"
- [C5] 消息格式：JSON-RPC 2.0，包括 requests（带 id）、responses（result/error）、notifications（无 id）；所有消息必须包含 `"jsonrpc": "2.0"` | src: https://raw.githubusercontent.com/zed-industries/agent-client-protocol/refs/heads/main/schema/v1/meta.json | quote: "requests, responses, notifications" per JSON-RPC 2.0
- [C6] 鉴权机制：规范支持可选的 `authenticate` 方法；初始化流程为 initialize → authenticate（可选）→ session management | src: https://zed.dev/docs/ai/external-agents | quote: "initialize request...authenticate to allow the agent to perform any authentication actions (like an OAuth flow)"
- [C7] 子进程模式下鉴权：不需要额外认证机制；代理在子进程中运行，继承编辑器的环境变量，可通过 authenticate 方法进行代理自己的认证 | src: https://zed.dev/docs/ai/external-agents | quote: "boots it as a sub-process (inheriting any environment variables)"
- [C8] 状态归属：编辑器/客户端拥有 session 状态和"危险能力"（文件系统读写、终端控制）；agent 拥有自己的运行时、auth、模型选择、工具、本地配置 | src: https://zed.dev/docs/ai/external-agents | quote: "Zed hosts the thread in the Agent Panel...the client owns the dangerous capabilities"
- [C9] 版本规则：Rust crate 版本和 JSON Schema 版本独立；wire compatibility 由初始化期间交换的 `protocolVersion` 决定，不由 crate 版本推断 | src: https://github.com/zed-industries/agent-client-protocol/blob/main/README.md | quote: "wire compatibility is determined by the protocolVersion exchanged during initialize"
- [C10] 当前协议版本：稳定版本为 1；v2 schema 开发中 | src: https://github.com/zed-industries/agent-client-protocol/blob/main/README.md | quote: "current stable ACP protocol version is 1"
- [C11] 治理方：Zed Industries 和 JetBrains 联合领导（BDFL 模式）；Ben Brandt (Zed) 和 Sergey Ignatov (JetBrains) 为 Lead Maintainers，享有全局否决权 | src: https://agentclientprotocol.com/community/governance | quote: "lead by Zed Industries and JetBrains...Ben Brandt (Zed) and Sergey Ignatov (JetBrains) serve as benevolent dictators"
- [C12] 治理结构：分层治理，包括 Core Maintainers（驱动方向、可否决）、Maintainers（各组件独立决定）、Contributors；双周技术治理会议；无 CLA；Apache 2.0 许可 | src: https://agentclientprotocol.com/community/governance | quote: "hierarchical governance model...Core Maintainers drive overall direction...all repositories use Apache 2.0 licensing"
- [C13] 官方采用者列表：Google Gemini CLI、Claude Code、Codex CLI、GitHub Copilot CLI、OpenCode、OpenHands 等 50+ agents；11+ editors（Zed、JetBrains IDEs、VS Code、Neovim、Emacs） | src: https://zed.dev/acp | quote: "50+ agents...11+ editors including Zed, JetBrains IDEs, VS Code, Neovim, Emacs"
- [C14] ACP Registry：2026年1月上线，集中发现机制；Zed 和 JetBrains 提供内置支持 | src: https://zed.dev/blog/acp-registry | quote: "ACP Registry...enables agent developers to register implementations once and make them available across all compatible clients"
- [C15] 官方 SDK：Kotlin、Java、Python、Rust、TypeScript；各有官方实现和示例代码 | src: https://github.com/zed-industries/agent-client-protocol/blob/main/README.md | quote: "Official Libraries: Kotlin, Java, Python, Rust, TypeScript"
- [C16] 与 LSP 类比：官方文档明确提到"类似 LSP 统一语言服务的方式，ACP 为编程代理提供统一协议" | src: https://agentclientprotocol.com | quote: "Similar to how LSP standardized language servers, ACP provides a unified protocol"
- [C17] MCP 与 ACP 互补：MCP 连接 agents 与工具/数据源；ACP 连接编辑器与 agents | src: https://blog.marcnuri.com/agent-client-protocol-acp-introduction | quote: "MCP connects agents to tools, while ACP connects editors to agents"

## conflicts
- [无]

## gaps
- IBM ACP 撞名/混淆：官方文档中完全未提及 IBM；Web 搜索结果明确指出 IBM 的 Agent Communication Protocol（agent-to-agent）于 2025年8月合并至 A2A 并被归档，与 Zed 的 ACP（agent-to-client）为完全不同的协议。官方页面无撞名混淆的提及，两者彼此无关。

## leads
- 状态机详细流程：官方文档尚未给出完整的会话生命周期状态图
- 权限模型：`session/request_permission` 请求的具体权限类型和处理流程
- initialization handshake 的完整字段规范（capabilities negotiation）
- 基于角色的权限控制（RBAC）在协议中的体现
