# r1-acp-zed
question: Zed 编辑器发起的 Agent Client Protocol（ACP）管什么、怎么传输、怎么鉴权、谁治理、当前版本、谁在用（哪些 coding agent 已经实现了它，例如 Claude Code、Gemini CLI 等）。
checked: agentclientprotocol.com,github.com/zed-industries/agent-client-protocol,zed.dev/acp,zed.dev/blog/bring-your-own-agent-to-zed,zed.dev/docs/ai/external-agents,agentclientprotocol.com/community/governance,agentclientprotocol.com/protocol/v2/authentication,agentclientprotocol.com/get-started/introduction,zed.dev/blog/acp-progress-report

## claims
- [C1] ACP 管理代码编辑器与 AI 编码 agent 之间的通信 | src: https://github.com/zed-industries/agent-client-protocol | quote: "standardizes communication between _code editors_ (interactive programs for viewing and editing source code) and _coding agents_ (programs that use generative AI to autonomously modify code)." | type: official
- [C2] 本地 agent：JSON-RPC over stdio 子进程通信；远程 agent：HTTP/WebSocket（开发中） | src: https://agentclientprotocol.com/get-started/introduction | quote: "Local agents communicate through JSON-RPC over standard input/output as editor subprocesses. Remote agents connect via HTTP or WebSocket (with ongoing development for full cloud support)" | type: official
- [C3] 鉴权：agent 在初始化时通过 authMethods 字段声明可用鉴权方法 | src: https://agentclientprotocol.com/protocol/v2/authentication | quote: "Agents advertise authentication options through the `authMethods` field in their initialization response." | type: official
- [C4] 鉴权支持两种标准类型：Agent 自主处理或终端交互认证 | src: https://agentclientprotocol.com/protocol/v2/authentication | quote: "Agent-handled authentication: The agent manages the login flow directly. Terminal authentication: The client launches an interactive login process separately, then reconnects." | type: official
- [C5] 治理：Zed Industries（Ben Brandt）和 JetBrains（Sergey Ignatov）两位主维护者共同监管 | src: https://agentclientprotocol.com/community/governance | quote: "ACP is jointly governed by Zed and JetBrains, who collaborate to ensure the protocol serves the broader ecosystem. The two lead maintainers are: Ben Brandt (Zed Industries) and Sergey Ignatov (JetBrains)." | type: official
- [C6] Zed 负责处理安全漏洞和安全问题 | src: https://agentclientprotocol.com/community/governance | quote: "Zed will triage all potential security and vulnerability issues between the Zed team and other maintainers." | type: official
- [C7] 计划向独立基金会过渡 | src: https://agentclientprotocol.com/community/governance | quote: "plans to eventually transition toward an independent foundation." | type: official
- [C8] 当前稳定版本号：1 | src: https://github.com/zed-industries/agent-client-protocol | quote: "The current stable ACP protocol version is `1`." | type: official
- [C9] 最新发布版本：v1.9.1（2026-09-18） | src: https://api.github.com/repos/agentclientprotocol/agent-client-protocol/releases | quote: Published 2026-09-18T14:02:29Z | type: official
- [C10] Claude Code、Gemini CLI、GitHub Copilot 已实现 ACP | src: https://zed.dev/blog/bring-your-own-agent-to-zed | quote: "Claude Code: Beta support was added as of September 3rd. Gemini CLI: Google's reference implementation, running as a subprocess with ACP integration" | type: official
- [C11] 40+ agent 在 ACP 注册表中实现该协议 | src: https://agentclientprotocol.com/overview/agents | quote: "The page lists over 40 agents supporting the Agent Client Protocol, including Cline, Cursor, OpenHands, Goose, and many others." | type: secondary
- [C12] 支持的编辑器：Zed、VS Code、JetBrains IDEs、Neovim、Emacs 等 12+ 编辑器 | src: https://zed.dev/acp | quote: "The ecosystem includes 12+ editors (Zed, VS Code, JetBrains IDEs, Neovim, Emacs, and others)" | type: official
- [C13] Zed 在 2026 年 4 月 29 日发布 1.0 版本时推出 ACP，Claude Code、Codex CLI、Gemini CLI、OpenCode 作为首批 agent | src: https://zed.dev/acp | quote: "ACP was the headline feature of Zed 1.0 on April 29, 2026, with Claude Code, Codex CLI, Gemini CLI, and OpenCode running inside the editor at launch." | type: secondary

## conflicts
- 无重大冲突。IBM 的同名 ACP（Agent Communication Protocol）针对 agent↔agent 通信，已在 2025 年 8 月并入 A2A 并存档；Zed 的 ACP 针对 editor↔agent 通信，两者层次不同，无协议竞争。

## gaps
- 环境变量认证方法详细规范（如 env_var 类型的 vars 数组具体格式）
- 远程 agent 的 HTTP/WebSocket 传输完整规范（仍在开发中）
- ACP RFD 流程（RFC）的具体决策机制文档

## leads
- [L1] Zed 官方文档明确表述 ACP 设计受 LSP（Language Server Protocol）启发：https://agentclientprotocol.com/get-started/introduction 引述"Similar to how the Language Server Protocol (LSP) standardized language server integration"，确认了对 LSP 的设计借鉴关系，但无提及与 IBM ACP 的直接对比说明。
- [L2] IBM 的同名 ACP 已历史存档：研究报告及 Medium 文章（https://medium.com/@mertbasar30/...）记录命名碰撞的历史事实，但在 agentclientprotocol.com 官方网站上未找到对此碰撞的主动说明或澄清声明。
