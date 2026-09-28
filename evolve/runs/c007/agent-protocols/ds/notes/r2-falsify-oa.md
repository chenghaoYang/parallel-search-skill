# r2-falsify-oa
question: 反证「OpenAI 对 A2A/AG-UI 无官方支持或表态」与「Anthropic 对 A2A/AG-UI 无官方支持或表态」；另找 OpenAI 官方（非 X 帖）宣布采纳 MCP 的公告页（2025-03 前后）。
checked: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai, https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/copilot-kit-ag-ui, https://github.com/openai/openai-agents-python/releases/tag/v0.0.7, https://openai.github.io/openai-agents-python/mcp/, https://github.com/openai/plugins/blob/main/plugins/cloudflare/skills/building-ai-agent-on-cloudflare/references/examples.md, api.github.com/search/repositories (org:openai|org:anthropics a2a/ag-ui/agent2agent), api.github.com/search/code (同条件), https://developers.openai.com/llms.txt, https://developers.openai.com/blog/llms.txt, https://docs.anthropic.com/llms.txt

## claims
- [C1] Anthropic 官网托管 webinar 页「Deploying multi-agent systems using MCP and A2A with Claude on Vertex AI」，日期 2025-08-27，由 Anthropic 与 Google Cloud 联合主讲 → 推翻主张 B 的 A2A 部分 | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "practical implementation of multi-agent systems using Model Context Protocol (MCP) and Agent-to Agent protocol (A2A) with Claude on Vertex AI" | type: official
- [C2] 同一 webinar 页列出议程「How MCP and A2A complement each other」「How to deploy an MCP server on Google Cloud」，官方表态将 A2A 与 MCP 视为互补标准 | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "How MCP and A2A complement each other" | type: official
- [C3] Anthropic 官方仓库 anthropics/claude-quickstarts（简介: "A collection of projects designed to help developers quickly get started with building deployable applications using the Claude API"）含目录 managed-agents/copilot-kit-ag-ui，是 AG-UI 官方集成示例 → 推翻主张 B 的 AG-UI 部分 | src: https://github.com/anthropics/claude-quickstarts/blob/main/managed-agents/copilot-kit-ag-ui/CLAUDE.md | quote: "A finance assistant chat app wiring a Claude Managed Agent to CopilotKit's self-hosted runtime over the AG-UI protocol." | type: official
- [C4] 该 quickstart 使用 npm 适配器 @ag-ui/claude-managed-agents 完成 Managed Agents ↔ AG-UI 转换（AG-UI thread 对应 managed session，TOOL_CALL_*/REASONING_* 事件） | src: https://github.com/anthropics/claude-quickstarts/blob/main/managed-agents/copilot-kit-ag-ui/CLAUDE.md | quote: "@ag-ui/claude-managed-agents does the whole Managed Agents ↔ AG-UI translation: one AG-UI thread per managed session" | type: official
- [C5] GitHub org:openai 中无 a2a / ag-ui / agent2agent 匹配仓库（repo search total=0）；code search org:openai 对 agent2agent、AgentCard、ag-ui、a2a-sdk 均 total=0 → 未发现可推翻主张 A 的一手来源 | src: https://api.github.com/search/repositories?q=org:openai+a2a | quote: "total: 0" | type: official
- [C6] org:openai 全部 "a2a" 代码命中均为哈希/base64 噪声，唯一实质命中是 openai/plugins 中 Cloudflare skill 的示例模板表，把 `a2a` 列为 Cloudflare Workers 模板名，非 OpenAI 对 A2A 协议的支持 | src: https://github.com/openai/plugins/blob/main/plugins/cloudflare/skills/building-ai-agent-on-cloudflare/references/examples.md | quote: "| `a2a` | Agent-to-agent communication |" | type: official
- [C7] OpenAI Agents SDK (Python) v0.0.7 发布于 2025-03-26T16:08Z，release notes 首条为 MCP support —— 即 Altman X 帖当日的官方非-X 公告（任务 C） | src: https://github.com/openai/openai-agents-python/releases/tag/v0.0.7 | quote: "Key changes: 1. MCP support" | type: official
- [C8] Agents SDK 官方文档有独立 MCP 页 | src: https://openai.github.io/openai-agents-python/mcp/ | quote: "MCP is an open protocol that standardizes how applications provide context to LLMs." | type: official
- [C9] developers.openai.com llms.txt（索引）与其 blog/llms.txt（40 行索引）均无 a2a/ag-ui 条目；blog 索引中 MCP 相关文章均为 2025 年晚些时候的工程文（connect-private-mcp-servers、skyscanner-codex-jetbrains-mcp），未见 2025-03 独立新闻稿 | src: https://developers.openai.com/blog/llms.txt | quote: "Making private MCP servers reachable without making them public" | type: official
- [C10] docs.anthropic.com/llms.txt（672 行索引）含 24 处 mcp，0 处 a2a/ag-ui/agent2agent → Anthropic 文档站不记录 A2A/AG-UI 支持；官方痕迹仅 webinar 页 + quickstarts 仓库 | src: https://docs.anthropic.com/llms.txt | quote: "（grep a2a|ag-ui|agent2agent 无命中）" | type: official

## conflicts
- 无官方来源互相打架；主张 B 被 C1–C4 推翻（Anthropic 对 A2A 有官方 webinar 表态、对 AG-UI 有官方 org 仓库集成示例）。主张 A 未被推翻。

## gaps
- openai.com 新闻页未逐页搜索（上轮 index 403）；本轮依赖 site 限定 WebSearch + llms.txt + GitHub org API，均未命中。
- @ag-ui/claude-managed-agents npm 包的发布方未核实（@ag-ui scope 属 CopilotKit），但引用它的是 anthropics/claude-quickstarts 官方示例。
- repo:anthropics/claude-agent-sdk-python 搜 a2a = 0；org:anthropics 搜 agent2agent/AgentCard = 0 → claude-agent-sdk 未见 A2A 支持。
- community.openai.com 有用户帖讨论 A2A（用户生成内容，非官方表态，不计）。

## leads
- npm @ag-ui/claude-managed-agents：若成稿需说明该适配器归属（CopilotKit scope），查 npmjs registry。
- Anthropic webinar 与 Google Cloud 联办、主题为「Claude on Vertex AI」，可作 Anthropic「A2A 互补 MCP」立场的佐证。
- openai/plugins 的 anthropic-best-practices.md 等 skill 文件显示 openai org 收录 Anthropic 生态材料，若成稿涉及跨厂商生态可再挖。
