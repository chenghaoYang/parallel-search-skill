# r2-zed
question: 反证三条边界主张：①Claude Code 接入 Zed ACP 是 Zed 自研 adapter、非 Anthropic 原生；②Zed ACP 远程 HTTP/WebSocket 传输仍是 WIP；③Anthropic 对 A2A/AG-UI 等协议无官方表态。
checked: https://github.com/zed-industries/claude-agent-acp, https://agentclientprotocol.com, https://github.com/zed-industries/agent-client-protocol, https://github.com/agentclientprotocol/agent-client-protocol/releases, https://github.com/orgs/anthropics/repositories?q=acp, https://zed.dev/blog/claude-code-via-acp, https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md, https://agentclientprotocol.com/rfds/streamable-http-websocket-transport, https://agentclientprotocol.com/protocol/v1/transports, https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/docs/docs.json, https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai, https://github.com/anthropics/claude-quickstarts/pull/438

## claims
- [C1] 主张①维持（措辞需微调）：Claude Code 走 ACP 仍靠社区 adapter，仓库已从 zed-industries 迁至 agentclientprotocol org（github.com/agentclientprotocol/claude-agent-acp），仍活跃（730 commits，每次 push main 发 @preview npm 包），README 自述"implements an ACP agent by using the official Claude Agent SDK" | src: https://github.com/zed-industries/claude-agent-acp | quote: "Use Claude Agent SDK from ACP-compatible clients!" | type: official
- [C2] Zed 官方博文（2025-09-03，Morgan Krey）仍描述 adapter 方案并呼吁 Anthropic "adopt ACP directly"，无更新注明原生支持 | src: https://zed.dev/blog/claude-code-via-acp | quote: "We built an adapter that wraps Claude Code's SDK and translates its interactions into ACP's JSON RPC format." | type: official
- [C3] Anthropic 侧无原生 ACP：anthropics org 搜 "acp" 返回 0 repos（"No repositories matched your search"）；anthropics/claude-code CHANGELOG 全文无 "ACP"/"Agent Client Protocol"；docs.claude.com 站内搜索无 ACP 文档 | src: https://github.com/orgs/anthropics/repositories?q=acp | quote: "No repositories matched your search." | type: official
- [C4] 主张②维持：官网仍写 "Full support for remote agents is a work in progress"，远程 agent "communicating over HTTP or WebSocket" | src: https://agentclientprotocol.com | quote: "Full support for remote agents is a work in progress" | type: official
- [C5] ACP v1 transports 文档仅 stdio 为定稿（"SHOULD support stdio whenever possible"）；Streamable HTTP 标 "(draft proposal in progress)"，正文仅 "In discussion, draft proposal in progress."；WebSocket 未出现于该页 | src: https://agentclientprotocol.com/protocol/v1/transports | quote: "In discussion, draft proposal in progress." | type: official
- [C6] HTTP/WebSocket 远程传输已有具体设计但仍是 Active RFD（非完成）：rfds/streamable-http-websocket-transport，2026-07-02 "Moved to Active to reflect current Transports Working Group focus"；方案为单一 /acp 端点 + Streamable HTTP（SSE GET 流 + POST 202 Accepted，需 HTTP/2）+ WebSocket upgrade；"Clients that support remote ACP over HTTP MUST support both Streamable HTTP and WebSocket" | src: https://agentclientprotocol.com/rfds/streamable-http-websocket-transport | quote: "ACP needs a standard remote transport" | type: official
- [C7] schema v2 ≠ 已发布 wire 版本：稳定 wire 版本仍为 1（"The current stable ACP protocol version is `1`"）；schema-v2.0.0-alpha.5 为 pre-release（2026-09-18），docs 中 v2 整组标 "Draft"；README 警告勿从 schema release 版本推断 wire 兼容 | src: https://github.com/agentclientprotocol/agent-client-protocol/releases | quote: "The current stable ACP protocol version is `1`." | type: official
- [C8] 主张③推翻（A2A）：anthropic.com 官方 webinar 页 "Deploying multi-agent systems using MCP and A2A with Claude on Vertex AI"（2025-08-27，Anthropic 与 Google Cloud 合办，Anthropic 方 Alex Notov） | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "presented by Anthropic and Google Cloud, will dive deep into the practical implementation of multi-agent systems using Model Context Protocol (MCP) and Agent-to Agent protocol (A2A)" | type: official
- [C9] 主张③推翻（AG-UI）：anthropics/claude-quickstarts PR #438 已 merged（2026-08-05，作者 cj-ant）：新增 managed-agents/copilot-kit-ag-ui quickstart，经 AG-UI 协议把 Claude Managed Agent 接入 CopilotKit runtime，桥接包为上游 @ag-ui/claude-managed-agents | src: https://github.com/anthropics/claude-quickstarts/pull/438 | quote: "wires a Claude Managed Agent to CopilotKit's self-hosted runtime over the AG-UI protocol" | type: official

## conflicts
- 主张③被 C8/C9 推翻：r1 称「Anthropic 对 A2A/AG-UI 无官方表态」，但 anthropic.com 有 A2A webinar 页（C8），anthropics org 有已合并的 AG-UI quickstart（C9）。
- 主张①措辞冲突（程度轻）：「Zed 自研」需注明 repo 现归属 agentclientprotocol org（社区 org），不再在 zed-industries 名下；「非 Anthropic 原生」部分成立（C3）。

## gaps
- anthropics org 无 acp repo 的负向证据基于 GitHub org 搜索页与 claude-code CHANGELOG；未逐页检查 docs.claude.com 全部站点地图（站内搜索无命中）。
- claude-agent-acp 是否仍由 Zed 员工主导维护未核实（仅确认 org 迁移）。
- AG-UI webinar/博客层面的正式表态未找到，仅有 quickstart 代码层面的官方采用。

## leads
- ACP 有 announcements/transports-working-group 与 announcements/acp-v2-draft 两个公告页，可追踪远程传输与 v2 进度。
- Agentic AI Foundation（AAIF，Linux Foundation，Anthropic/Block/OpenAI 联创）是 Anthropic 对开放 agentic 标准的主要表态渠道（anthropic.com/news/donating-the-model-context-protocol...）。
