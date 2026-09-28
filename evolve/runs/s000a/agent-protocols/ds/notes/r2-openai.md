# r2-openai
question: OpenAI 自己的官方文档说它支持哪些智能体协议（MCP、A2A、IBM ACP、Zed ACP、AG-UI），有没有自家协议或变体的原名。
checked: https://github.com/openai/openai-agents-python, https://raw.githubusercontent.com/openai/openai-agents-python/main/docs/mcp.md, https://developers.openai.com/plugins/, https://developers.openai.com/plugins/concepts/mcp-server.md, https://developers.openai.com/api/docs/guides/tools-connectors-mcp, https://developers.openai.com/commerce, https://developers.openai.com/commerce/guides/key-concepts.md, https://github.com/openai/openai-agents-python/issues/472, https://api.github.com/repos/openai/codex/git/trees/main?recursive=1 (9514 paths grepped), https://raw.githubusercontent.com/openai/codex/main/docs/agents_md.md, https://raw.githubusercontent.com/openai/codex/main/codex-rs/app-server/README.md, https://raw.githubusercontent.com/openai/codex/main/codex-rs/app-server-protocol/src/lib.rs, https://openai.com/index/buy-it-in-chatgpt/ (bot-blocked, empty), https://openai.com/index/agentic-ai-foundation/ (bot-blocked, empty), https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk (bot-blocked, empty)

## claims
- [C1] MCP 支持：OpenAI Agents SDK (Python) 官方文档有 MCP 专章，支持 stdio/SSE/Streamable HTTP/HostedMCPTool 四种接入 | src: https://github.com/openai/openai-agents-python/blob/main/docs/mcp.md | quote: "The Agents Python SDK understands multiple MCP transports." | type: official
- [C2] MCP 支持：Responses API 有一等公民 `type: "mcp"` 工具，可接公网 remote MCP server 或经 Secure MCP Tunnel 接本地/私有 MCP server | src: https://developers.openai.com/api/docs/guides/tools-connectors-mcp | quote: "you can give models new capabilities using remote MCP servers or Secure MCP Tunnel" | type: official
- [C3] MCP 支持：ChatGPT 插件/Apps 体系即 MCP server——OpenAI 开发者文档整个 Plugins（原 Apps SDK）文档集以 MCP server 为核心 | src: https://developers.openai.com/plugins/ | quote: "Build and publish plugins with skills, MCP servers, and optional UI." | type: official
- [C4] MCP 细节：插件内 MCP server 暴露 tools/resources/prompts/instructions；Responses API 兼容 Streamable HTTP 或 HTTP/SSE 传输的远程 MCP server | src: https://developers.openai.com/plugins/concepts/mcp-server.md | quote: "The Model Context Protocol (MCP) is an open specification for connecting AI clients to external tools and data." | type: official
- [C5] MCP 版本注记：`connector_id`（内置连接器，本质是 MCP 工具的一种）对 2026-09-01 之后发布的模型已弃用 | src: https://developers.openai.com/api/docs/guides/tools-connectors-mcp | quote: "`connector_id` is deprecated for models released after September 1, 2026." | type: official
- [C6] A2A 文档未写：openai 域名内唯一痕迹是 openai-agents-python issue #472（2025-04-10 提出，enhancement 标签，现已 Closed），属用户请求而非 OpenAI 承诺；SDK 文档与仓库文件树均无 A2A | src: https://github.com/openai/openai-agents-python/issues/472 | quote: "It would be great to support the A2A (Agent2Agent) protocol, which Google has just introduced." | type: official
- [C7] ACP-IBM（IBM Agent Communication Protocol）文档未写：openai.com/developers.openai.com/github.com/openai 全域无此协议任何提及（搜 "OpenAI Agent Communication Protocol"、grep openai-agents-python 1887 路径与 openai/codex 9514 路径均无） | src: https://github.com/openai/openai-agents-python | quote: "N/A — absence of mention across checked pages" | type: official
- [C8] ACP-Zed（Zed Agent Client Protocol）文档未写：openai/codex 仓库 9514 文件路径无 acp/agent-client 字样；Codex 的 ACP 适配器是第三方仓库 agentclientprotocol/codex-acp，不在 github.com/openai 下 | src: https://github.com/openai/codex | quote: "N/A — repo tree grep, no ACP files" | type: official
- [C9] AG-UI 文档未写：openai 域名无 AG-UI 提及；openai-agents-python 文件树无 ag-ui；AG-UI 侧 "OpenAI Agent SDK: In Progress" 仅为对方路线图（上轮已记），非 OpenAI 承诺 | src: https://github.com/openai/openai-agents-python | quote: "N/A — absence of mention across checked pages" | type: official
- [C10] 自家协议（新协议，非 MCP）：Agentic Commerce Protocol (ACP)，与 Stripe 共建，驱动 ChatGPT Instant Checkout；规范分 Agentic Checkout Spec 与 Delegated Payment Spec | src: https://developers.openai.com/commerce/guides/key-concepts.md | quote: "ChatGPT calls the merchant's Agentic Commerce Protocol endpoints to create or update a checkout session" | type: official
- [C11] 自家协议补充：Delegated Payment Spec 由 PSP 实现，Stripe 的 Shared Payment Token 是首个兼容实现；commerce 文档自述 "Start your ACP integration" | src: https://developers.openai.com/commerce/guides/key-concepts.md | quote: "Stripe's Shared Payment Token is the first Delegated Payment Spec-compatible implementation" | type: official
- [C12] 自家变体（MCP 用法/扩展，非新线路协议）：Plugins（原 Apps SDK，/apps-sdk/ 已重定向到 /plugins/）= MCP server + skills + ChatGPT 专属 UI 扩展（MCP Apps UI resource） | src: https://developers.openai.com/plugins/ | quote: "Reference for ChatGPT-specific UI extensions and metadata." | type: official
- [C13] 自家协议（内部/客户端协议）：Codex app-server protocol——github.com/openai/codex 内 codex-rs/app-server-protocol 是自研 JSON-RPC 协议（schema 含 ClientRequest/ClientNotification/JSONRPC*），第三方 codex-acp 正是桥接它 | src: https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md | quote: "`model/list` returns JSON-RPC error `-32600` asking the client to restart Codex" | type: official
- [C14] AGENTS.md：OpenAI 创立的 Markdown 约定（非线路协议），codex 仓库 docs/agents_md.md 指向官方指南；原 developers.openai.com 指南现 301 到 learn.chatgpt.com/docs/agent-configuration/agents-md | src: https://github.com/openai/codex/blob/main/docs/agents_md.md | quote: "For information about AGENTS.md, see [this documentation](https://developers.openai.com/codex/guides/agents-md)." | type: official

## conflicts
- 命名漂移：简报所称 "Apps SDK" 在 developers.openai.com 已改名为 "Plugins"（/apps-sdk/ 整站重定向到 /plugins/）；help.openai.com 的 "Build with the Apps SDK" 文章仍存在但被反爬挡住，未能核对新旧名是否并存。

## gaps
- openai.com 公告页（buy-it-in-chatgpt、agentic-ai-foundation）对 web_fetch 与 curl 均返回反爬空页：ACP "co-developed with Stripe" 与 "OpenAI 捐 AGENTS.md 给 AAIF" 仅获二手检索摘要，未取到原句。
- help.openai.com（ChatGPT 端用户级 MCP connectors，beta）同样被反爬；ChatGPT 产品侧的 MCP 支持只有搜索摘要，无原句。
- A2A：issue #472 状态为 Closed，但未抓取评论，无法判定是已实现还是拒绝——SDK 文档无任何 A2A API。
- IBM ACP / Zed ACP / AG-UI 的"文档未写"结论基于 grep 与站内搜索的缺席证据，非 OpenAI 明文声明不支持。

## leads
- Codex app-server JSON-RPC 协议（codex-rs/app-server-protocol）是 Zed/ACP 适配器实际桥接的对象——若矩阵需要 "OpenAI 侧客户端协议" 一格，这是原名。
- 检索摘要显示 AAIF（OpenAI/Anthropic/Block 联合创立）托管的项目里含 Agent2Agent——OpenAI 对 A2A 的关系可能是"基金会层面托管"而非产品支持，值得单独一轮核实 openai.com 公告原文。
- "MCP Apps" UI descriptor（mcpAppUi、preferredModelDisplayMode）出现在 codex app-server README，说明 OpenAI 的 UI-extension 面正在与 MCP Apps 规范对齐。
