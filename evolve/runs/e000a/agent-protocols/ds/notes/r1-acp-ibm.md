# r1-acp-ibm
question: IBM / BeeAI 的 Agent Communication Protocol（ACP）官方现状：定位/管辖层、核心抽象、传输/消息格式、鉴权、版本历史、治理主体、成熟度现状；特别要确认这个 ACP 项目现在是否还独立存在、还是已并入 A2A 或被 sunset/deprecated。
checked: https://github.com/i-am-bee/acp, https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/, https://research.ibm.com/blog/agent-communication-protocol-ai, https://agentcommunicationprotocol.dev, https://www.ibm.com/think/topics/agent-communication-protocol, https://github.com/i-am-bee/acp/releases

## claims
- [C1] ACP 由 IBM Research 开发，2025 年 3 月在旧金山 AI Dev 25 会议展示 | src: https://research.ibm.com/blog/agent-communication-protocol-ai | quote: "demonstrated in early form at the AI Dev 25 conference in San Francisco in March 2025" | type: official
- [C2] IBM Research 产品孵化总监 Kate Blair 领导 ACP 团队 | src: https://research.ibm.com/blog/agent-communication-protocol-ai | quote: "Kate Blair, director of product incubation at IBM Research, leads the team" | type: official
- [C3] ACP 核心抽象包括：Agent Manifest、Run、Message、MessagePart、Await、Sessions | src: https://github.com/i-am-bee/acp | quote: "Agent Manifest...Run...Message...MessagePart...Await...Sessions...for discovery and composition...single agent execution...communication, consisting of ordered components...pause to request information" | type: official
- [C4] ACP 使用基于 HTTP 的 REST 架构，支持异步和同步通信 | src: https://research.ibm.com/blog/agent-communication-protocol-ai | quote: "ACP employs a RESTful architecture implemented over HTTP, enabling both synchronous and asynchronous agent interactions" | type: official
- [C5] 消息格式支持 MIME 类型和多模态内容；运行状态包括 created、in-progress、completed、failed、awaiting、cancelling、cancelled | src: https://github.com/i-am-bee/acp | quote: "REST-based Communication...supports multiple modalities and leverages MimeTypes for content identification...async-first, sync supported" | type: official
- [C6] OpenAPI 规范版本 0.2.0，定义端点包括 /agents、/runs、/runs/{run_id}、/runs/{run_id}/events、/runs/{run_id}/cancel | src: https://github.com/i-am-bee/acp/blob/main/docs/spec/openapi.yaml | quote: "openapi: 3.1.1...title: ACP - Agent Communication Protocol...version: 0.2.0...paths: /agents...get: /agents/{name}...post: /runs...get: /runs/{run_id}...post: /runs/{run_id}/cancel" | type: official
- [C7] 官方 Python SDK 和 TypeScript SDK 可用；无需 SDK 可用标准 HTTP 工具（curl、Postman） | src: https://github.com/i-am-bee/acp | quote: "No SDK Required (but available)...Python SDK...TypeScript SDK...easily create and interact with ACP agents" | type: official
- [C8] 2025 年 5 月 IBM 将 BeeAI 平台捐献给 Linux Foundation，ACP 纳入 Linux Foundation AI & Data 项目治理 | src: https://github.com/i-am-bee/acp | quote: "Developed by contributors to the BeeAI project, this initiative is part of the Linux Foundation AI & Data program...open, collaborative, and community-driven practices" | type: official
- [C9] 版本历史：v1.0.0 发布于 2025 年 7 月 1 日；最后版本 v1.0.3 发布于 2025 年 8 月 21 日 | src: https://github.com/i-am-bee/acp/releases | quote: "v1.0.0 - July 1, 2025...v1.0.3 - August 21, 2025...fix(python): revert cachetools version bump" | type: official
- [C10] 2025 年 8 月 25 日宣布 ACP 与 A2A 合并，ACP 并入 Linux Foundation 的 A2A 项目 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "The Agent Communication Protocol officially merged with Agent2Agent Protocol under the Linux Foundation umbrella" | type: official
- [C11] ACP 团队停止独立开发，转向为 A2A 贡献代码；BeeAI 用户通过 A2AServer 适配器或 A2AAgent 客户端进行迁移 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "the ACP team will be winding down active development and will begin contributing its technology and expertise directly to A2A" | type: official
- [C12] GitHub 仓库 i-am-bee/acp 于 2025 年 8 月 27 日存档（read-only）| src: https://github.com/i-am-bee/acp | quote: "ACP is now part of A2A under the Linux Foundation! Learn more...Migration Guide" | type: official
- [C13] Kate Blair 证实合并理由："通过将 ACP 的资产和专业知识融入 A2A，我们可以构建单一、更强大的 AI 代理通信和协作标准" | src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "By bringing the assets and expertise behind ACP into A2A, we can build a single, more powerful standard for how AI agents communicate and collaborate" | type: official
- [C14] ACP 与 Zed 的 Agent Client Protocol 是不同的协议，分别于 2025 年 3 月和 8 月发布；IBM ACP 用于代理间通信，Zed ACP 用于编辑器与代理通信 | src: https://4sysops.com/archives/comparing-ai-protocols-mcp-a2a-agp-agntcy-ibm-acp-zed-acp/ | quote: "IBM's Agent Communication Protocol...Zed Industries...released in August 2025...agent-to-agent interoperability protocol...communication between code editors and coding agents" | type: secondary
- [C15] ACP 与 MCP 的区别：ACP 用于代理间通信（agent-to-agent），MCP 用于代理与工具/资源通信（within agents） | src: https://agentcommunicationprotocol.dev/about/mcp-and-a2a | quote: "MCP handles internal agent operations, while ACP facilitates communication between separate agents...MCP = within agents; ACP/A2A = between agents" | type: official
- [C16] 维护者 10 人，主要来自 BeeAI 项目贡献者（Paolo Dettori、Tomáš Dvořák、Ismael Faro 等） | src: https://github.com/i-am-bee/acp | quote: "Current Maintainers...Paolo Dettori...Tomáš Dvořák...Ismael Faro...Matous Havlena...Lukáš Janeček" | type: official
- [C17] ACP 定位为"代理的 HTTP"，强调简单 REST 调用、无厂商锁定、离线代理发现 | src: https://research.ibm.com/blog/agent-communication-protocol-ai | quote: "ACP as 'the HTTP of agent communication'...vendor lock-in...peer-to-peer agent interactions" | type: official
- [C18] 成熟度现状：有参考实现（BeeAI 框架）、完整文档、OpenAPI 规范、Python/TypeScript SDK，Linux Foundation 支持表明社区驱动开发 | src: https://agentcommunicationprotocol.dev/introduction | quote: "The protocol includes a reference implementation through the BeeAI framework...comprehensive documentation, OpenAPI specifications, and SDKs...foundation-level governance signals maturity" | type: secondary

## conflicts
- None identified

## gaps
- 具体认证机制（如 Bearer token、API key、OAuth 支持）未在官方文档中明确文档化
- "定位/管辖层"（positioning/management layer）的具体架构细节
- MessagePart 的完整内容类型和编码选项列表
- ACP 与 A2A 的具体技术差异和迁移路径完整细节

## leads
- A2A (Agent2Agent Protocol) 现为标准发展方向，IBM 已转向该项目；新项目应评估采用 A2A 而非 ACP
- Linux Foundation AI & Data 项目治理结构和 A2A 技术委员会成员（包括 IBM、Google、Microsoft、AWS、Cisco、Salesforce、ServiceNow、SAP）
- BeeAI 平台的完整 ACP-to-A2A 迁移指南在 GitHub 官方仓库中提供
