# r1-acp-dual
question: 两个都叫 ACP 的协议分别是什么、是否一回事：(a) IBM 的 Agent Communication Protocol（BeeAI），(b) Zed 的 Agent Client Protocol。D1–D10：身份、连接两端、传输、现状、版本、采用者。
checked: https://agentclientprotocol.com, https://github.com/zed-industries/agent-client-protocol, https://github.com/i-am-bee/acp, https://agentstack.beeai.dev/, https://agentclientprotocol.com/llms.txt, https://agentclientprotocol.com/get-started/agents, https://agentclientprotocol.com/get-started/clients, https://www.ibm.com/think/topics/agent-communication-protocol, https://agentclientprotocol.com/protocol/v1/transports, https://zed.dev/blog/bring-your-own-agent-to-zed, https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/, https://research.ibm.com/projects/agent-communication-protocol, https://research.ibm.com/blog/agent-communication-protocol-ai

## claims
- [C1] Zed 的 ACP 全名 Agent Client Protocol，标准化「代码编辑器 ↔ 编程 agent」之间的通信 | src: https://github.com/zed-industries/agent-client-protocol | quote: "The Agent Client Protocol (ACP) standardizes communication between" code editors and coding agents; "A protocol for connecting any editor to any agent." | type: official
- [C2] Zed 创建 ACP，2025-08-27 发布博文宣布（作者 Nathan Sobo） | src: https://zed.dev/blog/bring-your-own-agent-to-zed | quote: "To make this possible, we created the Agent Client Protocol (ACP)" | type: official
- [C3] Gemini CLI 是首个/参考实现，Zed 与 Google 合作集成 | src: https://zed.dev/blog/bring-your-own-agent-to-zed | quote: "we've partnered with Google to integrate Gemini CLI as the initial reference implementation" | type: official
- [C4] Zed ACP 用 JSON-RPC 编码消息；客户端把 agent 作为子进程启动，走 stdio | src: https://agentclientprotocol.com/protocol/v1/transports | quote: "ACP uses JSON-RPC to encode messages." / "The client launches the agent as a subprocess." / "The agent reads JSON-RPC messages from its standard input (`stdin`) and sends messages to its standard output (`stdout`)." | type: official
- [C5] stdio 是规范层面应支持的传输；Streamable HTTP 仍是草案 | src: https://agentclientprotocol.com/protocol/v1/transports | quote: "Agents and clients **SHOULD** support stdio whenever possible." / "[Streamable HTTP] (draft proposal in progress)" | type: official
- [C6] Zed ACP 当前稳定协议版本为 1；仓库内另有 schema/v2 产物 | src: https://github.com/zed-industries/agent-client-protocol | quote: "The current stable ACP protocol version is `1`." | type: official
- [C7] ACP v2 处于 Draft 状态，文档站已放出 v2 草案与「Migrating from v1」 | src: https://agentclientprotocol.com/llms.txt | quote: "ACP v2 is available in Draft" | type: official
- [C8] Zed ACP 以 Apache 许可开源 | src: https://zed.dev/blog/bring-your-own-agent-to-zed | quote: "The protocol is open-source under the Apache license" | type: official
- [C9] 官方 agents 列表含 Gemini CLI、"Claude Agent"（经 Zed SDK adapter，链至 claude-agent-acp 仓库）、Codex CLI（经 ACP adapter）、GitHub Copilot（public preview）、Goose、Cline、OpenCode、Kimi CLI、Qwen Code 等约 40 个 | src: https://agentclientprotocol.com/get-started/agents | quote: "The following agents can be used with an ACP Client:"（列表含 "Gemini CLI"、"Claude Agent" via "Zed's SDK adapter"、"Codex CLI" via "ACP's adapter"、"GitHub Copilot"） | type: official
- [C10] 官方 clients 列表含 Zed、JetBrains、neovim（CodeCompanion 等 4 个插件）、Emacs（agent-shell.el）、VS Code（多个扩展）、Sublime Text、Qt Creator、Obsidian 等 | src: https://agentclientprotocol.com/get-started/clients | quote: 页面按 Editors and IDEs / CLI and TUI / Desktop and Web 等分组列出 "Zed"、"JetBrains"、"neovim"、"Emacs"、"Visual Studio Code" | type: official
- [C11] IBM 的 ACP 全名 Agent Communication Protocol，是让 AI agent 跨框架/语言/运行时互通的开放标准 | src: https://research.ibm.com/projects/agent-communication-protocol | quote: "Agent Communication Protocol (ACP) is an open standard designed to enable seamless communication between AI agents regardless of framework, programming language, or runtime environment." | type: official
- [C12] IBM ACP 连接的是 agent↔agent（对等体），也面向应用与人 | src: https://github.com/i-am-bee/acp | quote: "Open protocol for communication between AI agents, applications, and humans." | type: official
- [C13] IBM ACP 走 HTTP/REST 风格，默认异步；不需要专用库（cURL/Postman 可用） | src: https://www.ibm.com/think/topics/agent-communication-protocol | quote: "ACP uses standard HTTP conventions for communication that makes it easy to integrate into production." / "ACP is designed with asynchronous communication as the default" | type: official
- [C14] IBM Research 2025 年 3 月发布 ACP 驱动 BeeAI Platform；同月 BeeAI（含 ACP）捐给 Linux Foundation | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "IBM Research launched the Agent Communication Protocol (ACP) in March 2025 to power its BeeAI Platform… the BeeAI project—and with it, ACP—was donated to the Linux Foundation" | type: official
- [C15] 2025-08-29 LF AI & Data 官宣：ACP 正式并入 Linux Foundation 旗下的 A2A，ACP 团队停止独立开发、转向 A2A 贡献 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "ACP is officially merging with the A2A under the Linux Foundation… the ACP team will be winding down active development" | type: official
- [C16] i-am-bee/acp 仓库已归档只读，README 顶部宣告并入 A2A | src: https://github.com/i-am-bee/acp | quote: "This repository was archived by the owner on Aug 27, 2025. It is now read-only." / "ACP is now part of A2A under the Linux Foundation!" | type: official
- [C17] BeeAI 文档站 docs.beeai.dev 已 301 跳转至 agentstack.beeai.dev（Agent Stack），平台改为输出 A2A agent | src: https://agentstack.beeai.dev/ | quote: "automatically exposed as A2A-compatible agents" / "Agent Stack is an open-source project maintained as part of the Linux Foundation community." | type: official
- [C18] IBM think 页顶部加注：ACP 已并入 A2A，内容可能过时 | src: https://www.ibm.com/think/topics/agent-communication-protocol | quote: "ACP has merged with A2A under the Linux Foundation umbrella. The ACP team is winding down active development" | type: official
- [C19] 二者不是同一协议：全名不同（Communication vs Client）、创建者不同（IBM Research vs Zed Industries）、连接两端不同（agent↔agent vs editor↔agent）、传输不同（HTTP/REST vs JSON-RPC over stdio）——由 C1/C4/C11/C13/C14 各自一手定义并置得出 | src: https://github.com/zed-industries/agent-client-protocol | quote: 见 C1/C4/C11/C13 | type: official

## conflicts
- Zed ACP 远程传输表述不一：站点概览称 agent 也可经 HTTP/WebSocket 远程通信（WIP），而 v1 transports 规范页只把 stdio 列为 SHOULD、Streamable HTTP 标为 draft、未提 WebSocket。以规范页为准更稳妥。两边 URL：https://agentclientprotocol.com 与 https://agentclientprotocol.com/protocol/v1/transports

## gaps
- IBM ACP 具体 REST 端点路径（如 /runs、/agents）未取到原句：原 spec 文档站已随归档下线，ibm.com/think 页未列端点。
- 未见任何一手来源明确讨论缩写撞名（只是各自定义不同）。
- Zed ACP 的 WebSocket 传输状态（RFD 存在，规范页未提）。

## leads
- Claude Code 走 ACP 的适配器仓库：zed-industries/claude-agent-acp（agents 页所称 "Zed's SDK adapter"）。
- ACP v2 草案改动：Prompt Lifecycle 取代 Prompt Turn，暂无 File System/Terminals 页（llms.txt）。
- BeeAI 平台更名/演进为 Agent Stack（agentstack.beeai.dev），可能值得主文档单独一行。
