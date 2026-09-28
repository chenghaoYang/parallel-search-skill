# r1-acp-ibm
question: IBM 的 Agent Communication Protocol（ACP，常与 BeeAI 一起出现）是什么、现在还是不是独立现行规范，以及它和 Google/Linux Foundation 的 A2A、和 Zed 的 Agent Client Protocol 是不是同一个东西。
checked: https://agentcommunicationprotocol.dev, https://agentcommunicationprotocol.dev/llms.txt, https://agentcommunicationprotocol.dev/core-concepts/architecture.md, https://agentcommunicationprotocol.dev/core-concepts/agent-run-lifecycle.md, https://agentcommunicationprotocol.dev/core-concepts/agent-discovery.md, https://agentcommunicationprotocol.dev/core-concepts/production-grade.md, https://agentcommunicationprotocol.dev/about/mcp-and-a2a.md, https://agentcommunicationprotocol.dev/about/mission-and-team.md, https://agentcommunicationprotocol.dev/introduction/whats-new.md, https://agentcommunicationprotocol.dev/spec/openapi.yaml, https://github.com/i-am-bee/acp, https://github.com/i-am-bee/acp/tags, https://github.com/orgs/i-am-bee/discussions/5, https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/

## claims
- [C1] parties：全称 Agent Communication Protocol (ACP)，开放协议，连接 agents、applications、humans | src: https://agentcommunicationprotocol.dev | quote: "The Agent Communication Protocol (ACP) is an open protocol for agent interoperability" | type: official
- [C2] parties：两端角色 ACP client / ACP server；client 可由 agent、app 或 service 使用 | src: https://agentcommunicationprotocol.dev/core-concepts/architecture.md | quote: "An ACP client can be used by an ACP agent, application, or other service that makes requests to an ACP server" | type: official
- [C3] parties：一个 server 托管多个 agents，经 REST 暴露 | src: https://agentcommunicationprotocol.dev/core-concepts/architecture.md | quote: "An ACP server can host one or more ACP agents that executes requests and returns results to the client" | type: official
- [C4] surface：核心对象 Agent Manifest、Run、Message、MessagePart、Await、Sessions；Run 为带输入的单次执行 | src: https://github.com/i-am-bee/acp | quote: "A single agent execution with specific inputs. Supports sync or streaming, with intermediate and final output." | type: official
- [C5] discovery：在线查 GET /agents；Open Discovery 在 well-known 路径发布 YAML manifest：/.well-known/agent.yml | src: https://agentcommunicationprotocol.dev/core-concepts/agent-discovery.md | quote: "Publish your agent metadata using a YAML file at a well-known location" | type: official
- [C6] discovery：Registry-Based 与 Embedded（容器镜像 label 嵌入 manifest）；registry 未入规范、BeeAI Platform 已实现 | src: https://agentcommunicationprotocol.dev/core-concepts/agent-discovery.md | quote: "While not yet part of the official ACP spec, this feature is implemented in the BeeAI Platform." | type: official
- [C7] transport：REST over HTTP，官方自述区别于 JSON-RPC | src: https://agentcommunicationprotocol.dev | quote: "ACP uses simple, well-defined REST endpoints that align with standard HTTP patterns." | type: official
- [C8] transport：流式用 SSE——POST /runs 的 200 响应 content 含 text/event-stream（schema Event）| src: https://agentcommunicationprotocol.dev/spec/openapi.yaml | quote: "text/event-stream:" | type: official
- [C9] auth：文档层声明 TLS + Basic Auth、Bearer tokens、JWTs + 反向代理访问控制 | src: https://agentcommunicationprotocol.dev/core-concepts/production-grade.md | quote: "Support for common authentication methods such as Basic Auth, Bearer tokens, and JWTs" | type: official
- [C10] state：RunStatus 枚举七值 created, in-progress, awaiting, cancelling, cancelled, completed, failed | src: https://agentcommunicationprotocol.dev/spec/openapi.yaml | quote: "RunStatus: type: string enum: - created - in-progress - awaiting - cancelling - cancelled - completed - failed" | type: official
- [C11] state：run 端点 POST /runs（mode sync/async/stream）、GET /runs/{run_id}、POST /runs/{run_id} resume、POST /runs/{run_id}/cancel | src: https://agentcommunicationprotocol.dev/core-concepts/agent-run-lifecycle.md | quote: "Requires `agent_name`, `input`. Optional: `session_id`, `mode` (`sync`, `async`, `stream`)." | type: official
- [C12] version：OpenAPI info.version 0.2.0（openapi 3.1.1，license Apache 2.0）；仓库最后 tag v1.0.3（2025-08-21）| src: https://agentcommunicationprotocol.dev/spec/openapi.yaml | quote: "version: 0.2.0" | type: official
- [C13] version：仓库 i-am-bee/acp 于 2025-08-27 归档只读 | src: https://github.com/i-am-bee/acp | quote: "This repository was archived by the owner on Aug 27, 2025. It is now read-only." | type: official
- [C14] version：官网横幅宣告并入 A2A | src: https://agentcommunicationprotocol.dev | quote: "ACP is now part of A2A under the Linux Foundation!" | type: official
- [C15] version：ACP 团队停止独立开发（公告 2025-08-25；LF 博客 2025-08-29，页标 Last updated 2025-09-04）| src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "the ACP team will be winding down active development and will begin contributing its technology and expertise directly to A2A." | type: official
- [C16] governance：IBM Research 2025 年 3 月发布 ACP 驱动 BeeAI Platform；同月 BeeAI（含 ACP）捐给 Linux Foundation | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "IBM Research launched the Agent Communication Protocol (ACP) in March 2025 to power its BeeAI Platform" | type: official
- [C17] governance：治理归 LF AI & Data，仓库 i-am-bee/acp，Apache 2.0；自称 "open standard under the Linux Foundation" | src: https://agentcommunicationprotocol.dev/about/mission-and-team.md | quote: "As part of the Linux Foundation AI & Data, ACP is committed to upholding the principles of open, collaborative, and community-driven practices." | type: official
- [C18] vendors：官方比较页点名 Anthropic（MCP）与 Google（A2A，2025-04）| src: https://agentcommunicationprotocol.dev/about/mcp-and-a2a.md | quote: "Model Context Protocol (MCP) is a popular open standard from Anthropic" | type: official
- [C19] vendors：公告列 A2A TSC 成员来自 Google, Microsoft, AWS, Cisco, Salesforce, ServiceNow, SAP（IBM 由 Kate Blair 代表）| src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "alongside representatives from Google, Microsoft, AWS, Cisco, Salesforce, ServiceNow, and SAP." | type: official
- [C20] relation：官方口径为「合并」 | src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "ACP is officially merging with the A2A under the Linux Foundation umbrella." | type: official
- [C21] relation：合并前官方页将二者列为同目标两规范 | src: https://agentcommunicationprotocol.dev/about/mcp-and-a2a.md | quote: "both aim to create a standard interface for agent-to-agent communication." | type: official
- [C22] relation：BeeAI 平台已从 ACP 切到 A2A，SDK 提供 A2AServer/A2AAgent 适配器 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "The BeeAI platform, previously powered by ACP, now uses A2A to support agents from any framework." | type: official

## conflicts
- 官网未同步更新：welcome 页与仓库横幅宣告并入 A2A（2025-08），about/mcp-and-a2a.md 仍以竞品口吻列 "Advantages of ACP"（Open Governance、REST-based、Offline Discovery 等七条）对比 A2A，不提合并。两边均官方。
- LF 官方博客疑似笔误："The first issues aimed at bringing ACP features into ACP are already in the A2A github"（应为 into A2A）。

## gaps
- 官方站点、llms.txt 全页索引与仓库 README 均未提及 Zed 或 "Agent Client Protocol"；IBM 一手来源无同名歧义说明，无法据此确认两者关系。
- OpenAI 未在任何已查官方页面被点名。
- OpenAPI 0.2.0 无 securitySchemes 字段（grep 仅命中无关 "author"），鉴权只有文档叙述。
- 文档页无日期；规范版本号仅 info.version 0.2.0。
- pypi.org/project/acp-sdk 被反爬拦截，SDK 最后发布日期未取到（以 tag v1.0.3 / 2025-08-21 近似）。

## leads
- ACP→A2A 官方迁移指南：https://github.com/i-am-bee/beeai-platform/blob/main/docs/community-and-support/acp-a2a-migration-guide.mdx（未打开）
- A2A 现行规范仓库：https://github.com/a2aproject/A2A
- 第三方对两个 ACP 同名歧义的辨析（secondary，留 Zed 支线）：https://crystl.dev/blog/agent-communication-protocols/
