# r1-acp-zed
question: Zed 的 Agent Client Protocol（ACP，注意全称是 Client 不是 Communication）连接对象是什么？起源方（Zed Industries）与治理方式（是否完全开源、是否有其他编辑器/IDE 已采用，例如 Neovim、JetBrains 等）？版本历史？传输层机制（是否 JSON-RPC over stdio）？鉴权机制官方 spec 怎么规定（或明确说明未规定/依赖宿主）？核心概念（Session、Prompt 等对象怎么定义）？
checked: https://agentclientprotocol.com, https://github.com/agentclientprotocol/agent-client-protocol, https://zed.dev/docs/ai/external-agents, https://zed.dev/acp, https://zed.dev/blog/bring-your-own-agent-to-zed, https://zed.dev/blog/acp-progress-report, https://zed.dev/blog/jetbrains-on-acp, https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/rfds/auth-methods.mdx

## claims
- [C1] 连接对象：code editors 与 coding agents，本地 agents 作为 editor 的子进程 | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: "standardizes communication between code editors (interactive programs for viewing and editing source code) and coding agents (programs that use generative AI to autonomously modify code)." | type: official
- [C2] 传输层机制（本地）：JSON-RPC 2.0 over stdin/stdout | src: https://zed.dev/blog/bring-your-own-agent-to-zed | quote: "The protocol uses a lean framework that lets any client talk to any agent, as long as they follow the schema. It operates via JSON-RPC endpoints" | type: official
- [C3] 传输层机制（本地）补充：JSON-RPC envelope 用于 wire messages | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: "provides the Rust data model for ACP wire messages, including request, response, notification, JSON-RPC envelope, and protocol-version types" | type: official
- [C4] 远程传输机制（未完成）：HTTP 或 WebSocket 连接，仍在开发中 | src: https://agentclientprotocol.com | quote: "Remote agent support is currently under active development as the protocol team collaborates with cloud platforms" | type: official
- [C5] 起源方：Zed Industries 创建 ACP | src: https://zed.dev/blog/bring-your-own-agent-to-zed | quote: "Zed Industries has launched the Agent Client Protocol (ACP), enabling developers to integrate third-party AI agents directly within the Zed editor" | type: official
- [C6] 初始参考实现：Google Gemini CLI | src: https://zed.dev/blog/bring-your-own-agent-to-zed | quote: "The initial implementation features Google's Gemini CLI." | type: official
- [C7] 许可证：Apache License 2.0，无 CLA | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: "contributions are accepted under the following terms...licensed under the Apache License, Version 2.0" 和 "This project does not require a Contributor License Agreement (CLA)" | type: official
- [C8] 完全开源、社区欢迎 | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: "ACP is a protocol intended for broad adoption across the ecosystem" | type: official
- [C9] 编辑器/IDE 采用：JetBrains（IntelliJ IDEA、PyCharm、WebStorm） | src: https://zed.dev/blog/jetbrains-on-acp | quote: "JetBrains has committed to co-developing the Agent Client Protocol (ACP) alongside Zed, marking a significant expansion of the protocol's adoption. The company plans to integrate ACP support across its entire IDE lineup, including IntelliJ IDEA, PyCharm, and WebStorm." | type: official
- [C10] 编辑器/IDE 采用：Neovim 通过 CodeCompanion 和 avante.nvim 插件 | src: https://zed.dev/blog/acp-progress-report | quote: "Neovim users can access agents via CodeCompanion and avante.nvim plugins" | type: official
- [C11] 编辑器/IDE 采用：Emacs 通过 agent-shell 插件 | src: https://zed.dev/blog/acp-progress-report | quote: "Emacs integrated agent functionality through the agent-shell plugin" | type: official
- [C12] 编辑器/IDE 采用：marimo Python notebook 环境 | src: https://zed.dev/blog/acp-progress-report | quote: "marimo's Python notebook environment supports the protocol" | type: official
- [C13] 编辑器/IDE 采用：Eclipse IDE 原型实现 | src: https://zed.dev/blog/acp-progress-report | quote: "Eclipse IDE has a prototype implementation" | type: official
- [C14] 编辑器/IDE 采用：Toad 基于终端的代理代码支持 | src: https://zed.dev/blog/acp-progress-report | quote: "Toad is building terminal-based agentic coding support" | type: official
- [C15] 官方 SDK 支持语言：Kotlin、Java、Python、Rust、TypeScript | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: "Official Libraries...Kotlin...Java...Python...Rust...and TypeScript" | type: official
- [C16] 稳定协议版本：version 1 | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: "The current stable ACP protocol version is 1." | type: official
- [C17] 版本协商机制：protocolVersion 在 initialize 消息中交换 | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: "ACP wire compatibility is determined separately by the protocol version exchanged during initialize via protocolVersion" | type: official
- [C18] Repository 创建时间：2025-06-23 | src: https://github.com/agentclientprotocol/agent-client-protocol | quote: creation date 2025-06-23T17:39:36Z | type: official
- [C19] 最新 Rust Crate 版本：v1.9.1（2026-09-18） | src: https://github.com/agentclientprotocol/agent-client-protocol/releases | quote: "Rust Crate v1.9.1" published_at: "2026-09-18T14:02:29Z" | type: official
- [C20] 最新 Schema v1 版本：1.23.0（2026-09-18） | src: https://github.com/agentclientprotocol/agent-client-protocol/releases | quote: "Schema v1.23.0" published_at: "2026-09-18T10:43:39Z" | type: official
- [C21] Schema v2 开发状态：2.0.0-alpha.5（2026-09-18） | src: https://github.com/agentclientprotocol/agent-client-protocol/releases | quote: "Schema v2.0.0-alpha.5" published_at: "2026-09-18T10:43:41Z" | type: official
- [C22] 首个稳定版本发布：Rust Crate v1.0.0（2026-06-24） | src: https://github.com/agentclientprotocol/agent-client-protocol/releases | quote: "Rust Crate v1.0.0" published_at: "2026-06-24T12:13:53Z" | type: official
- [C23] 鉴权机制规范方式一："agent" 认证方法，通过 auth/login 和 auth/logout 处理 | src: https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/rfds/auth-methods.mdx | quote: "The standard agent type uses auth/login" | type: official
- [C24] 鉴权机制规范方式二："terminal" 认证方法，客户端在交互终端中启动代理 | src: https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/rfds/auth-methods.mdx | quote: "Add a terminal authentication method...A supporting Client launches the same configured Agent program in an interactive terminal" | type: official
- [C25] 鉴权机制规范：terminal 方法不通过 auth/login 或 auth/logout 处理 | src: https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/rfds/auth-methods.mdx | quote: "Terminal authentication is an out-of-band process. The Client does not pass a terminal method to v1 authenticate or v2 auth/login." | type: official
- [C26] 客户端鉴权选择：通过 AuthCapabilities（v1）或 capabilities.auth（v2）选择加入 | src: https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/rfds/auth-methods.mdx | quote: "Clients opt in because terminal authentication requires Client-side process and terminal support...advertises this capability only when it can reproduce the configured Agent invocation in an interactive terminal" | type: official
- [C27] 所有代理验证要求：代理必须在 ACP 握手期间返回有效的 authMethods | src: https://zed.dev/docs/ai/external-agents | quote: "All agents are verified to ensure they return valid authMethods in the ACP handshake" | type: official
- [C28] Terminal 认证方法字段（v1）：id、name、description、type、args、env | src: https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/rfds/auth-methods.mdx | quote: '{"id": "agent-login", "name": "Log in from the terminal", "description": "Open the Agent\'s interactive login flow", "type": "terminal", "args": ["--login"], "env": {"ACP_INTERACTIVE_LOGIN": "1"}}' | type: official
- [C29] Terminal 认证方法字段（v2）：methodId 替代 id，env 从对象改为数组结构 | src: https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/rfds/auth-methods.mdx | quote: '{"methodId": "agent-login"...,"env": [{"name": "ACP_INTERACTIVE_LOGIN", "value": "1"}]}' | type: official
- [C30] Terminal 认证的 v2 要求：代理实现 auth/login 和 auth/logout，保留基线认证表面规则 | src: https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/rfds/auth-methods.mdx | quote: "In v2, advertising any authentication method requires the Agent to implement both auth/login and auth/logout" | type: official

## conflicts
- None identified

## gaps
- 核心概念中 Session、Prompt 等具体对象的详细定义（仅见 Request、Response、Notification、protocolVersion）
- 消息签名或 MAC 机制规范（仅见传输层）
- 是否支持 TLS/SSL 加密（仅见 JSON-RPC 提及）
- Remote agents 的具体连接参数（仅知在开发中）
- 是否有速率限制或 QoS 规范

## leads
- Terminal 认证 RFD 标记为 Completed（2026-08-20），应检查该版本之后是否有后续规范更新
- v2 schema 仍为 alpha（最新 alpha.5 于 2026-09-18），应跟进最终稳定版本发布
- JetBrains partnership 公告后的具体采用时间表未在查阅的文档中找到
