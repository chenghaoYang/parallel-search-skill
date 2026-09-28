# r2-rebut
question: 对 5 条边界主张找一手反例（ACP 已弃用 / OpenAI 产品层不支持 A2A / Anthropic 对 A2A、AG-UI 无表态 / AG-UI 未加入 AAIF / A2A spec 无强制默认 binding）
checked: https://github.com/agntcy/acp-spec, https://github.com/orgs/agntcy/repositories?type=all&q=acp, https://spec.acp.agntcy.org, https://docs.agntcy.org, https://agntcy.org, https://agntcy.org/blog(404), https://aaif.io, https://aaif.io/projects, https://aaif.io/news, https://aaif.io/members, https://aaif.io/press/agentic-ai-foundation-welcomes-97-new-members..., https://a2a-protocol.org/latest/specification/, github.com/a2aproject/A2A docs/specification.md(全文 grep), docs/topics/custom-protocol-bindings.md, docs/topics/extension-and-binding-governance.md, https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai, https://www.anthropic.com/news/donating-the-model-context-protocol-..., https://platform.claude.com/docs/en/managed-agents/quickstart, https://openai.com/index/(403), help.openai.com/developers.openai.com 域内搜索

## claims
- [C1] 【反例-推翻主张3(A2A 部分)】anthropic.com 官方 webinar 页「Deploying multi-agent systems using MCP and A2A with Claude on Vertex AI」(2025-08-27)，Anthropic 与 Google Cloud 联合主讲，讲师含 Anthropic Technical Enablement Lead Alex Notov | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "How MCP and A2A complement each other" | type: official
- [C2] 【反例-推翻主张3(AG-UI 部分)】platform.claude.com 官方文档 Managed Agents quickstart 设「CopilotKit (AG-UI)」卡片，指向 anthropics/claude-quickstarts 的 AG-UI adapter | src: https://platform.claude.com/docs/en/managed-agents/quickstart | quote: "The AG-UI adapter for Claude Managed Agents maps each chat thread to a managed session and streams replies token by token" | type: official
- [C3] acp-spec 仓库已被 owner 于 2026-04-11 正式 archive（read-only），README 本身无 deprecation 声明 | src: https://github.com/agntcy/acp-spec | quote: "This repository was archived by the owner on Apr 11, 2026. It is now read-only." | type: official
- [C4] agntcy org 下全部 3 个 ACP 相关仓库均已 archive：acp-spec(最后更新 2025-05-23)、acp-sdk(2025-06-16)、workflow-srv(2025-09-15) | src: https://github.com/orgs/agntcy/repositories?type=all&q=acp | quote: "acp-sdk — Agent Connect Protocol SDK — Public archive" | type: official
- [C5] spec.acp.agntcy.org 仍在线（HTTP 200，页面 title "Agent Connect Protocol"，正文 JS 渲染无法确认内容）；docs.agntcy.org 导航无 ACP 条目 | src: https://spec.acp.agntcy.org | quote: "Agent Connect Protocol" (页面 title) | type: official
- [C6] agntcy.org 组件列表无 ACP；其 AgentBridge 组件改用 A2A | src: https://agntcy.org | quote: "Connects coding agents and other CLIs over A2A so they can hand off context, delegate tasks" | type: official
- [C7] aaif.io/projects 当前仅列 6 个项目：Model Context Protocol、goose、AGENTS.md、agentgateway、Agent2Agent(A2A)、Agent Router——无 AG-UI | src: https://aaif.io/projects | quote: "Model Context Protocol ... goose ... AGENTS.md ... agentgateway ... Agent2Agent ... Agent Router" | type: official
- [C8] OpenAI 是 AAIF 共同发起方之一，而 A2A 是 AAIF 托管项目——组织层关联存在，但非产品层支持表态 | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "co-founded by Anthropic, Block and OpenAI, with support from Google, Microsoft, Amazon Web Services (AWS), Cloudflare, and Bloomberg" | type: official
- [C9] A2A spec §5.2 只要求声明所支持的协议，未强制任一具体 binding；§12 明确自定义 binding 为 MAY | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "Agents **MUST** declare all supported protocols in their AgentCard" / "implementers **MAY** create custom protocol bindings" | type: official
- [C10] spec 中 binding 相关 MUST 均为通用约束（§3.2.6 service parameters、§3.3.2 error mapping、§3.5.2 event ordering、§4 数据模型等价、§5.1 多协议功能等价），无 "MUST support JSON-RPC/gRPC/REST" 语句 | src: https://github.com/a2aproject/A2A/blob/main/docs/specification.md | quote: "All protocol bindings **MUST** provide functionally equivalent representations of these data structures." | type: official

## conflicts
- C1+C2 推翻「Anthropic 对 A2A/AG-UI 无官方表态」：anthropic.com webinar 正面介绍 A2A（2025-08-27）；platform.claude.com 产品文档含官方 AG-UI adapter 示例（Managed Agents beta，betaHeader managed-agents-2026-04-01）。注意均为文档/webinar 层，非正式立场声明。
- C8 部分软化主张2：OpenAI 作为 AAIF 共同发起方与托管项目 A2A 有组织层关联，但未找到任何产品层（ChatGPT/API）A2A 支持表态，主张2本身未被推翻。

## gaps
- 主张1：未找到 agntcy 正式 deprecation 公告（agntcy.org/blog 404 不存在；README 无声明），但也未找到仍在维护的反例——archive(2026-04-11)+组件除名+AgentBridge 转用 A2A 反而强化弃用结论。spec.acp.agntcy.org 虽 200 但正文 JS 渲染未能验证内容。
- 主张2：help.openai.com/developers.openai.com 域内检索无 A2A 提及（multi-agent 文档只讲 MCP）；openai.com/index 仍 403；community.openai.com 有 A2A 讨论帖但非官方表态且不在来源政策内。
- 主张4：aaif.io/members 成员墙 JS 渲染未取到名单；97-new-members 新闻稿 Silver 名单中无 CopilotKit/AG-UI（可见部分）。

## leads
- aaif.io/projects 含「Agent Router」「agentgateway」，疑与 AGNTCY/Cisco 系项目并入 AAIF 有关，可查 AGNTCY 资产是否迁移进 AAIF。
- anthropics/claude-quickstarts repo 的 managed-agents/copilot-kit-ag-ui 目录可作 AG-UI adapter 一手代码证据。
