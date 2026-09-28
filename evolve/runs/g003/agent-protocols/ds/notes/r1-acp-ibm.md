# r1-acp-ibm
question: IBM / BeeAI 的 Agent Communication Protocol（ACP）官方文档如何定义两端、核心对象、传输、发现、生命周期、鉴权、版本与治理；它现在是否仍独立，还是已声明并入别的协议；官方文本有没有把自己说成 Zed 的 Agent Client Protocol。
checked: https://agentcommunicationprotocol.dev/llms.txt, https://agentcommunicationprotocol.dev/introduction/welcome, https://agentcommunicationprotocol.dev/about/mcp-and-a2a, https://agentcommunicationprotocol.dev/about/mission-and-team, https://agentcommunicationprotocol.dev/core-concepts/architecture, https://agentcommunicationprotocol.dev/core-concepts/agent-run-lifecycle, https://agentcommunicationprotocol.dev/core-concepts/agent-discovery, https://agentcommunicationprotocol.dev/core-concepts/message-structure, https://agentcommunicationprotocol.dev/core-concepts/production-grade, https://agentcommunicationprotocol.dev/spec/openapi.yaml, https://raw.githubusercontent.com/i-am-bee/acp/main/README.md, https://github.com/i-am-bee/acp, https://github.com/orgs/i-am-bee/discussions/5

## claims
- [C1] D1 两端是 ACP client 与 ACP server。client 可由 agent、application 或其他 service 调用；server 用 REST 托管一个或多个 agent。同一进程可兼作两端。 | src: https://agentcommunicationprotocol.dev/core-concepts/architecture | quote: "makes requests to an ACP server using the ACP protocol." | type: official
- [C2] D1 连接对象是 AI agents、applications 与 humans。 | src: https://agentcommunicationprotocol.dev/introduction/welcome | quote: "connecting AI agents, applications, and humans." | type: official
- [C3] D2 README 核心概念：Agent Manifest、Run、Message、MessagePart、Await、Sessions。Manifest 描述 name、description 及可选 metadata/status，不暴露实现。 | src: https://raw.githubusercontent.com/i-am-bee/acp/main/README.md | quote: "A model describing an agent's capabilities—its name, description, and optional metadata and status" | type: official
- [C4] D2 Message 必填 role 与 parts。role 为 user、agent 或 agent/{agent_name}，pattern ^(user|agent(/[a-zA-Z0-9_\-]+)?)$。 | src: https://agentcommunicationprotocol.dev/spec/openapi.yaml | quote: "Specifies the sender of the message. Allowed values:" | type: official
- [C5] D2 MessagePart 必填 content_type；content 与 content_url 至多其一；content_encoding 为 plain 或 base64。有 name 的 part 是 Artifact。 | src: https://agentcommunicationprotocol.dev/core-concepts/message-structure | quote: "Artifacts are specialized MessageParts with a name attribute." | type: official
- [C6] D2 AgentManifest 必填 name、description、input_content_types、output_content_types。Run 必填 agent_name、run_id、status、output、created_at。RunMode：sync、async、stream。Session 必填 id、history（URI 数组），可选 state。 | src: https://agentcommunicationprotocol.dev/spec/openapi.yaml | quote: "enum: [sync, async, stream]" | type: official
- [C7] D3 传输是 RESTful HTTP，对比 JSON-RPC。OpenAPI 3.1.1 示例 server 为 http://localhost:8000。POST /runs 的 200 可为 application/json 或 text/event-stream。 | src: https://agentcommunicationprotocol.dev/introduction/welcome | quote: "such as JSON-RPC), ACP leverages familiar HTTP conventions" | type: official
- [C8] D3 路径：GET /ping；GET /agents；GET /agents/{name}；POST /runs；GET 与 POST /runs/{run_id}；POST /runs/{run_id}/cancel；GET /runs/{run_id}/events；GET /session/{session_id}。 | src: https://agentcommunicationprotocol.dev/spec/openapi.yaml | quote: "Returns a list of agents." | type: official
- [C9] D4 四种发现：Basic（在线查运行中的 server）、Open（well-known URL）、Registry（在线或离线）、Embedded（离线嵌入元数据）。在线列表是 GET /agents，limit 默认 10（1–1000），offset 默认 0。 | src: https://agentcommunicationprotocol.dev/core-concepts/agent-discovery | quote: "Basic Discovery: Query running ACP servers directly (online)" | type: official
- [C10] D4 Open Discovery 路径为 https://your-domain.com/.well-known/agent.yml。Registry 与部署说明还不是官方 spec；BeeAI Platform 已实现 registry。 | src: https://agentcommunicationprotocol.dev/core-concepts/agent-discovery | quote: "While not yet part of the official ACP spec, this feature is implemented in the BeeAI Platform." | type: official
- [C11] D5 RunStatus：created、in-progress、awaiting、cancelling、cancelled、completed、failed。POST /runs 建 run；GET /runs/{run_id} 取状态；POST /runs/{run_id} 以 await_resume 恢复；POST /runs/{run_id}/cancel 返回 202。 | src: https://agentcommunicationprotocol.dev/core-concepts/agent-run-lifecycle | quote: "defines a structured lifecycle for individual agent runs, guiding them from creation to completion." | type: official
- [C12] D5 协议按设计无状态，再用 session 做有状态 agent。 | src: https://agentcommunicationprotocol.dev/core-concepts/production-grade | quote: "ACP is a stateless protocol by design, just like HTTP." | type: official
- [C13] D6 生产文档写 TLS、Basic Auth、Bearer tokens、JWTs 与反向代理。未规定 header 或必选方案。Identity Federation「under active development」。完整 OpenAPI 0.2.0 无 security/securitySchemes。 | src: https://agentcommunicationprotocol.dev/core-concepts/production-grade | quote: "Support for common authentication methods such as Basic Auth, Bearer tokens, and JWTs" | type: official
- [C14] D7 OpenAPI info.version 0.2.0，Apache 2.0，title 为 ACP - Agent Communication Protocol。包名 acp-sdk；TypeScript SDK 是 client libraries。 | src: https://agentcommunicationprotocol.dev/spec/openapi.yaml | quote: "version: 0.2.0" | type: official
- [C15] D8 Mission 页：ACP 属于 Linux Foundation AI & Data，治理开放且社区驱动，BeeAI 是参考实现。 | src: https://agentcommunicationprotocol.dev/about/mission-and-team | quote: "As part of the Linux Foundation AI & Data" | type: official
- [C16] D8 公告（Aug 25, 2025）写 BeeAI 连同 ACP donated to the Linux Foundation，时间是 Later that month。 | src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "Later that month, the BeeAI project—and with it, ACP—was donated to the Linux Foundation" | type: official
- [C17] D8/D9 同公告：ACP 正式并入 A2A；团队停止积极开发并直接贡献给 A2A。 | src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "the ACP team will be winding down active development" | type: official
- [C18] D8/D9 github.com/i-am-bee/acp 于 Aug 27, 2025 被 owner archive，现为 read-only。README 与欢迎页横幅同句。 | src: https://github.com/i-am-bee/acp | quote: "This repository was archived by the owner on Aug 27, 2025. It is now read-only." | type: official
- [C19] D9 MCP 是 Anthropic 的模型上下文标准，作用于单个 agent 内的 LLM 与 tools/resources；ACP 是 agent 之间通信，文档写二者一起用。 | src: https://agentcommunicationprotocol.dev/about/mcp-and-a2a | quote: "MCP and ACP work together to build powerful agentic systems" | type: official
- [C20] D9 欢迎页与 README 横幅声明已并入 A2A。对比页仍把 ACP 与 A2A 写成两个并列标准，见 conflicts。 | src: https://agentcommunicationprotocol.dev/introduction/welcome | quote: "ACP is now part of A2A under the Linux Foundation!" | type: official
- [C21] D9 自称 Agent Communication Protocol (ACP)，不是 Agent Client Protocol。welcome、mcp-and-a2a、README、openapi.yaml 全文检索 Zed、Agent Client Protocol、agentclientprotocol 均为零命中。 | src: https://raw.githubusercontent.com/i-am-bee/acp/main/README.md | quote: "ACP is an open protocol for communication between AI agents, applications, and humans." | type: official

## conflicts
- 并入 vs 并列。欢迎页：「ACP is now part of A2A under the Linux Foundation!」https://agentcommunicationprotocol.dev/introduction/welcome 。公告 Aug 25, 2025：「ACP is officially merging with the A2A」https://github.com/orgs/i-am-bee/discussions/5 。对比页无 merge：「launched by IBM in March 2025 and Agent2Agent Protocol (A2A), launched by Google in April 2025」https://agentcommunicationprotocol.dev/about/mcp-and-a2a 。未裁决。
- Mission 仍写 ACP 属于 LF AI & Data https://agentcommunicationprotocol.dev/about/mission-and-team ；公告写开发收束并进入 A2A TSC。仓库 Aug 27, 2025 已 archive。
- 生产页写支持 Basic/Bearer/JWT；OpenAPI 0.2.0 无 securitySchemes。可视为部署层 HTTP，不是 schema 字段。

## gaps
- 未找到 i-am-bee/acp 的 changelog/release notes，不能钉 0.2.0 的起始日期。acp-sdk 的 semver 只在徽章图里，README 正文无数字。
- Zed 检索只覆盖 welcome、mcp-and-a2a、README、OpenAPI 与 GitHub 仓库页，未扫完整站。
- 未打开迁移指南与 LF 新闻稿；捐赠与 merge 原句来自 BeeAI 公告。

## leads
- 迁移指南 https://github.com/i-am-bee/beeai-platform/blob/main/docs/community-and-support/acp-a2a-migration-guide.mdx ；公告写 BeeAI platform 已改用 A2A。
- 公告写「bringing ACP features into ACP」再链到 A2A GitHub，疑似笔误。GET /session/{session_id} 的参数名叫 name。
