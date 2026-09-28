# r1-acp-ibm
question: IBM / BeeAI 的 Agent Communication Protocol（ACP）现在还是不是独立规范：角色、原语、传输、任务生命周期、发现、鉴权、版本与治理，以及项目自己是否宣布并入 A2A 或停止独立演进。
checked: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/, https://github.com/orgs/i-am-bee/discussions/5, https://github.com/i-am-bee/acp/blob/main/README.md, https://github.com/i-am-bee/acp/releases, https://raw.githubusercontent.com/i-am-bee/acp/main/docs/spec/openapi.yaml, https://agentcommunicationprotocol.dev, https://agentcommunicationprotocol.dev/core-concepts/architecture, https://agentcommunicationprotocol.dev/core-concepts/message-structure, https://agentcommunicationprotocol.dev/core-concepts/agent-run-lifecycle, https://agentcommunicationprotocol.dev/core-concepts/agent-discovery, https://agentcommunicationprotocol.dev/core-concepts/agent-manifest, https://agentcommunicationprotocol.dev/core-concepts/production-grade, https://agentcommunicationprotocol.dev/about/mcp-and-a2a, https://agentcommunicationprotocol.dev/spec/agents-list, https://research.ibm.com/blog/agent-communication-protocol-ai, https://github.com/i-am-bee/beeai-framework/blob/main/README.md, https://github.com/i-am-bee/beeai-platform/blob/main/docs/community-and-support/acp-a2a-migration-guide.mdx

## claims
- [C1] D7：LF AI & Data 帖宣布 ACP 正式并入 A2A。帖址路径含 2025/08/29。 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "ACP is officially merging with the A2A under the Linux Foundation umbrella." | type: official
- [C2] D7：同一帖：停止积极开发，并把技术与专长直接贡献给 A2A。 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "the ACP team will be winding down active development and will begin contributing its technology and expertise directly to A2A." | type: official
- [C3] D7/D9：BeeAI 平台原先由 ACP 驱动，现改用 A2A。 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "The BeeAI platform, previously powered by ACP, now uses A2A to support agents from any framework." | type: official
- [C4] D9：Blair 称目标是单一标准。 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "we can build a single, more powerful standard for how AI agents communicate and collaborate" | type: official
- [C5] D7：讨论 #5 页眉为该日期。 | src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "Aug 25, 2025" | type: official
- [C6] D7：i-am-bee/acp 于 Aug 27, 2025 归档且只读。页面可打开。 | src: https://github.com/i-am-bee/acp/blob/main/README.md | quote: "This repository was archived by the owner on Aug 27, 2025. It is now read-only." | type: official
- [C7] D7：归档 README 置顶该句。 | src: https://github.com/i-am-bee/acp/blob/main/README.md | quote: "ACP is now part of A2A under the Linux Foundation!" | type: official
- [C8] D7：首页仍写社区治理。 | src: https://agentcommunicationprotocol.dev | quote: "ACP maintains transparent, community-driven governance" | type: official
- [C9] D7：OpenAPI info.version 为 0.2.0。这是规范文件版本，不是 SDK 标签。 | src: https://raw.githubusercontent.com/i-am-bee/acp/main/docs/spec/openapi.yaml | quote: "version: 0.2.0" | type: official
- [C10] D7：该发布行无年份。同页标题为 v1.0.3 且标 Latest，不在本 quote。 | src: https://github.com/i-am-bee/acp/releases | quote: "pilartomas released this 21 Aug 05:31" | type: official
- [C11] D7：beeai-framework README 该行含日期与并入句。该页无归档横幅。 | src: https://github.com/i-am-bee/beeai-framework/blob/main/README.md | quote: "2025/08/25 | Python | ACP is now part of A2A under the Linux Foundation!" | type: official
- [C12] D1：两端是 ACP client 与 ACP server。client 可由 agent、application 或其他 service 使用。 | src: https://agentcommunicationprotocol.dev/core-concepts/architecture | quote: "An ACP client can be used by an ACP agent, application, or other service that makes requests to an ACP server" | type: official
- [C13] D1：server 以 REST 托管一个或多个 agent。 | src: https://agentcommunicationprotocol.dev/core-concepts/architecture | quote: "The purpose of the ACP server is to expose agents through a REST interface." | type: official
- [C14] D1：消息 role 的一种合法形式是 user。 | src: https://agentcommunicationprotocol.dev/core-concepts/message-structure | quote: "`user` - for messages from users" | type: official
- [C26] D1：另一种是 agent/{name}，name 可含字母数字、下划线、连字符。 | src: https://agentcommunicationprotocol.dev/core-concepts/message-structure | quote: "`agent/{name}` - for specific agent messages where name can contain alphanumeric characters, underscores, and hyphens" | type: official
- [C15] D2：OpenAPI 自称为标准化 RESTful API，用于管理、编排、执行 agent。 | src: https://raw.githubusercontent.com/i-am-bee/acp/main/docs/spec/openapi.yaml | quote: "a standardized RESTful API for managing, orchestrating, and executing AI agents." | type: official
- [C16] D2/D4：创建 run 必填 agent_name、input；可选 session_id 与 mode（sync、async、stream）。 | src: https://agentcommunicationprotocol.dev/core-concepts/agent-run-lifecycle | quote: "Requires `agent_name`, `input`. Optional: `session_id`, `mode` (`sync`, `async`, `stream`)." | type: official
- [C17] D3：首页把 ACP 写成 HTTP 惯例，并以 JSON-RPC 为对照。 | src: https://agentcommunicationprotocol.dev | quote: "Unlike protocols requiring specialized communication methods (such as JSON-RPC), ACP leverages familiar HTTP conventions" | type: official
- [C18] D4：RunStatus 枚举为这七个值。 | src: https://raw.githubusercontent.com/i-am-bee/acp/main/docs/spec/openapi.yaml | quote: "- created - in-progress - awaiting - cancelling - cancelled - completed - failed" | type: official
- [C19] D4：Session 用 session id 跨多次交互保存状态与历史。 | src: https://github.com/i-am-bee/acp/blob/main/README.md | quote: "maintain state and conversation history across multiple interactions using session identifiers." | type: official
- [C20] D5：Basic discovery 是在线直接查询正在运行的 ACP server。 | src: https://agentcommunicationprotocol.dev/core-concepts/agent-discovery | quote: "Basic Discovery: Query running ACP servers directly (online)" | type: official
- [C21] D5：Open discovery 示例路径为该 URL。 | src: https://agentcommunicationprotocol.dev/core-concepts/agent-discovery | quote: "https://your-domain.com/.well-known/agent.yml" | type: official
- [C22] D6：生产页写支持这三类常见认证，未给出 ACP 专用头字段名。 | src: https://agentcommunicationprotocol.dev/core-concepts/production-grade | quote: "Support for common authentication methods such as Basic Auth, Bearer tokens, and JWTs" | type: official
- [C23] D6：规范站渲染的 GET /agents 片段 security 为空数组。 | src: https://agentcommunicationprotocol.dev/spec/agents-list | quote: "security: []" | type: official
- [C24] D9：该页把 ACP 定义为 agent 之间的协议。 | src: https://agentcommunicationprotocol.dev/about/mcp-and-a2a | quote: "ACP is a protocol that enables communication between agents." | type: official
- [C25] D7：所链迁移指南本次为 GitHub 404，步骤未读到。 | src: https://github.com/i-am-bee/beeai-platform/blob/main/docs/community-and-support/acp-a2a-migration-guide.mdx | quote: "404 - page not found" | type: official

## conflicts
- 并入 vs 仍独立：C1–C4、C7、C11 对 C8。首页另有 “ACP is now part of A2A under the Linux Foundation!” mcp-and-a2a 写 “both aim to create a standard interface for agent-to-agent communication.” 未裁决。
- 发现：同页 “While not yet part of the official ACP spec, this feature is implemented in the BeeAI Platform.”
- 鉴权：C22 对 C23。raw yaml 已读段未见 securitySchemes。

## gaps
- D8 未填。未打开 OpenAI、Anthropic、Google、Microsoft 产品文档。LF 帖有 Blair 加入 A2A TSC 一句，不把它写成这几家实现 ACP。
- 404 页写 agentstack 的 main 不含该迁移指南路径。
- 已看见未单列：role 还有 “agent - for generic agent messages”；Embedded Discovery；2025-03 启动并捐赠给 LF；license name Apache 2.0；RunMode sync/async/stream；身份联邦 under active development；2025-05-28 Blair “at least for now”。v1.0.3 行无年份。raw yaml 在 AgentDependency 截断。

## leads
- beeai-framework Serve 行只写 A2A 与 MCP。POST /runs 200 含 text/event-stream。取消路径正文与表不一致（run/ 对 /runs/）。
