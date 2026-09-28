# r1-acp2
question: 同名歧义「ACP」——IBM/BeeAI 的 Agent Communication Protocol 与 Zed 的 Agent Client Protocol 分别是什么、是否一回事、各自现状。
checked: https://agentcommunicationprotocol.dev, https://github.com/i-am-bee/acp, https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/, https://agentcommunicationprotocol.dev/spec/openapi.yaml, https://agentcommunicationprotocol.dev/core-concepts/production-grade, https://agentclientprotocol.com, https://agentclientprotocol.com/protocol/overview, https://agentclientprotocol.com/protocol/v1/authentication, https://agentclientprotocol.com/overview/agents, https://agentclientprotocol.com/overview/clients, https://github.com/zed-industries/agent-client-protocol, https://zed.dev/blog/bring-your-own-agent-to-zed, https://zed.dev/blog/jetbrains-on-acp, https://zed.dev/blog/claude-code-via-acp, https://www.ibm.com/think/topics/agent-communication-protocol, https://research.ibm.com/projects/agent-communication-protocol

## claims

- [C1] 结论：两个 ACP 仅缩写巧合——全称、作者、连接面、传输全不同；均为 Apache-2.0 | src: https://github.com/i-am-bee/acp , https://github.com/zed-industries/agent-client-protocol | quote: "Open protocol for communication between AI agents, applications, and humans" vs "A protocol for connecting any editor to any agent" | type: official

### ACP-IBM（Agent Communication Protocol）
- [C2] D1 定位：开放 agent 互操作协议，RESTful API 连接 agents/applications/humans；交换 multimodal messages、stream responses、long-running tasks | src: https://agentcommunicationprotocol.dev , https://github.com/i-am-bee/acp | quote: "an open protocol for agent interoperability" ... "a standardized RESTful API" ... "powers agent communication on the BeeAI Platform" | type: official
- [C3] D2 治理+license：IBM Research 2025-03 发布，同月随 BeeAI 捐给 Linux Foundation（LF AI & Data）；Apache-2.0 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ , https://github.com/i-am-bee/acp | quote: "IBM Research launched the Agent Communication Protocol (ACP) in March 2025" / "the BeeAI project—and with it, ACP—was donated to the Linux Foundation" | type: official
- [C4] D3 传输：REST/HTTP | src: https://agentcommunicationprotocol.dev | quote: "ACP uses simple, well-defined REST endpoints that align with standard HTTP patterns" | type: official
- [C5] D4 抽象：OpenAPI 端点 /ping、/agents、/runs、/runs/{id}、/runs/{id}/cancel、/runs/{id}/events、/session/{id}；顶层对象 = agent、run、message（MIME）、session、manifest | src: https://agentcommunicationprotocol.dev/spec/openapi.yaml | quote: "title: ACP - Agent Communication Protocol" | type: official
- [C6] D5 鉴权：spec 内无 securitySchemes（907 行仅 1 处 auth）；部署层称支持 TLS、Basic/Bearer/JWT、reverse proxy；身份联邦 "under active development" | src: https://agentcommunicationprotocol.dev/core-concepts/production-grade | quote: "Support for common authentication methods such as Basic Auth, Bearer tokens, and JWTs" | type: official
- [C7] D6 现状：OpenAPI spec version 0.2.0；repo 2025-08-27 归档只读 | src: https://github.com/i-am-bee/acp | quote: "This repository was archived by the owner on Aug 27, 2025. It is now read-only." | type: official
- [C8] D6/D7 并入 A2A：LF 官方 2025-08-29 宣布合并，团队停更转向 A2A；IBM 自认 A2A "Introduced by Google" | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ , https://www.ibm.com/think/topics/agent-communication-protocol | quote: "ACP is officially merging with the A2A under the Linux Foundation" / "the ACP team will be winding down active development" | type: official
- [C9] D8 实现：BeeAI Framework（Python/TS）+ BeeAI Platform；官方 SDK Python、TypeScript | src: https://research.ibm.com/projects/agent-communication-protocol | quote: "Its primary implementation is provided by the BeeAI Framework" | type: official

### ACP-Zed（Agent Client Protocol）
- [C10] D1 定位：标准化 code editor/IDE ↔ coding agent 通信，类比 LSP；Agent = "programs that use generative AI to autonomously modify code" | src: https://agentclientprotocol.com , https://agentclientprotocol.com/protocol/overview | quote: "similar to how the Language Server Protocol (LSP) standardized language server integration" | type: official
- [C11] D2 治理+license：Zed Industries 创建（博文 2025-08-27），Apache license；JetBrains 宣布共同开发 | src: https://zed.dev/blog/bring-your-own-agent-to-zed , https://zed.dev/blog/jetbrains-on-acp | quote: "we created the Agent Client Protocol (ACP)" / "JetBrains has announced it will co-develop the Agent Client Protocol with us" | type: official
- [C12] D3 传输：本地 agents 为编辑器子进程，JSON-RPC over stdio；远程 HTTP/WebSocket 仍 WIP；复用 MCP 的 JSON 表示 | src: https://agentclientprotocol.com | quote: "run as sub-processes of the code editor, communicating via JSON-RPC over stdio" / "Full support for remote agents is a work in progress" | type: official
- [C13] D4 抽象：session（session/new、load、prompt→流式 session/update、cancel、set_mode）、session/request_permission、fs/read_text_file+write_text_file、terminal/* 5 方法、elicitation；握手 initialize+authenticate | src: https://agentclientprotocol.com/protocol/overview | quote: "All file paths in the protocol MUST be absolute." | type: official
- [C14] D5 鉴权：initialize 响应含 authMethods；类型仅 "agent"（默认）与 "terminal"（client 以 args/env 交互跑 agent）；authenticate(methodId) 不收 terminal 方法；可选 logout | src: https://agentclientprotocol.com/protocol/v1/authentication | quote: "Clients MUST NOT pass a `terminal` method." | type: official
- [C15] D6 版本：wire 协议稳定版 1；schema 目录含 v1/v2 且 crate/schema 版本与 wire 版本独立；公告 2025-08-27 | src: https://github.com/zed-industries/agent-client-protocol | quote: "The current stable ACP protocol version is `1`." | type: official
- [C16] D7 大厂：Google 启动伙伴、Gemini CLI 为 "the initial reference implementation"；Claude Code 经 Zed 自研 adapter 包装其 SDK（非 Anthropic 原生）；OpenAI "Codex CLI (via ACP's adapter)"；JetBrains 共同开发并接入全线 IDE | src: https://zed.dev/blog/bring-your-own-agent-to-zed , https://zed.dev/blog/claude-code-via-acp , https://agentclientprotocol.com/overview/agents | quote: "We built an adapter that wraps Claude Code's SDK" | type: official
- [C17] D8 实现：官方 SDK Kotlin/Java/Python/Rust/TS；agents 约 40 个（Gemini CLI、Claude Agent、Codex CLI、Goose、Cline、OpenCode、GitHub Copilot 预览、Kimi/Qwen CLI 等）；clients 含 Zed、JetBrains IDEs、Neovim、Emacs、VS Code 扩展、Sublime | src: https://agentclientprotocol.com/overview/agents , https://agentclientprotocol.com/overview/clients | quote: "Claude Agent (via Zed's SDK adapter)" ... "Codex CLI (via ACP's adapter)" | type: official

## conflicts
- 命名：agents 列表写 "Claude Agent (via Zed's SDK adapter)"，Zed 博文写 "Claude Code"——同一集成（repo: zed-industries/claude-agent-acp），称谓不同。
- 日期巧合：IBM acp repo 归档日与 Zed ACP 公告同为 2025-08-27，两项目无关联。

## gaps
- IBM ACP 是否有 >0.2.0 的 spec release / 最终 git tag：未查。
- "BeeAI: ACP to A2A Migration Guide" 内容未展开。
- Zed ACP schema/v2 是否对应已发布的 wire v2：未确认。

## leads
- JetBrains×Zed 共同开发：ACP-Zed 治理正从单一厂商走向多厂商。
- IBM ACP 文档站仍在线但项目停更——成稿应写「已并入 A2A、repo 归档」。
