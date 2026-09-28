# r1-acp-ibm
question: IBM 主导的 Agent Communication Protocol（ACP）官方项目现状——它管什么交互、拓扑、传输层、消息格式、鉴权机制、治理方、版本规则、当前项目状态是否仍在独立维护还是已合并/整合进 A2A 项目；同时确认 ACP-IBM 与 ACP-Zed 是否有任何关联。
checked: agentcommunicationprotocol.dev, github.com/i-am-bee/acp, lfaidata.foundation, research.ibm.com, zed.dev/acp, github.com/agentclientprotocol

## claims

### 项目定位与现状
- [C1] ACP 是"AI agents、applications、humans 之间的开放通信协议" | src: https://github.com/i-am-bee/acp | quote: "Open protocol for communication between AI agents, applications, and humans." | type: official
- [C2] ACP GitHub 仓库于 2025 年 8 月 27 日被 archived，现为 read-only | src: https://github.com/i-am-bee/acp | quote: "repository was archived on August 27, 2025" | type: official
- [C3] IBM Research 于 2025 年 3 月推出 ACP，作为 BeeAI Platform 的支撑协议 | src: https://research.ibm.com/blog/agent-communication-protocol-ai | quote: "IBM Research launched the Agent Communication Protocol (ACP) in March 2025" | type: official
- [C4] 2025 年 3 月，BeeAI 和 ACP 被捐赠至 Linux Foundation | src: https://medium.com/mitb-for-all/introducing-the-agent-communication-protocol-acp-abd882114139 | quote: "donated to the Linux Foundation in March" | type: official

### 治理与转移
- [C5] ACP 于 2025 年 8 月 25 日正式并入 A2A（Agent2Agent Protocol），归属 Linux Foundation | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "ACP is officially merging with the Agent2Agent Protocol (A2A) under the Linux Foundation" | type: official
- [C6] ACP 团队现已停止独立开发，开始向 A2A 贡献技术和专业知识 | src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "the ACP team will be winding down active development and will begin contributing its technology and expertise directly to A2A" | type: official
- [C7] Kate Blair（IBM Research Director of Incubation）代表 IBM 加入 A2A 技术指导委员会，委员会包括 Google、Microsoft、AWS、Cisco、Salesforce、ServiceNow、SAP 代表 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "Kate Blair, Director of Incubation for IBM Research... join the A2A Technical Steering Committee... Google, Microsoft, AWS, Cisco, Salesforce, ServiceNow, and SAP" | type: official
- [C8] ACP 作为 Linux Foundation AI & Data program 的一部分，遵循"开放、协作、社区驱动"的治理原则 | src: https://agentcommunicationprotocol.dev/introduction/welcome | quote: "developed as an open standard under the Linux Foundation... open governance principles" | type: official

### 管什么（交互域）
- [C9] ACP 规范 agent 与 agent 之间的通信，支持代理发现、多模态消息交换、任务委托与协作 | src: https://agentcommunicationprotocol.dev/core-concepts/agent-discovery | quote: "agent interoperability... agents discover capabilities... collaborate on tasks" | type: official
- [C10] ACP 支持多部署模式：单 agent 客户端、多 agent 服务器、分布式架构、路由 agent 模式 | src: https://agentcommunicationprotocol.dev/core-concepts/architecture | quote: "Single-Agent Setup... Multi-Agent Server... Distributed Architecture... Router Agent Pattern" | type: official

### 拓扑与方向
- [C11] ACP 的基础部署是 client 直接连接单个 agent（via REST over HTTP），或 server 承载多个可寻址的 agent | src: https://agentcommunicationprotocol.dev/core-concepts/architecture | quote: "simplest ACP deployment connects a client directly to a single agent... ACP Server can host multiple agents... individually addressable" | type: official
- [C12] 单个进程可同时充当 server（处理入站请求）和 client（发起出站请求），支持对等通信 | src: https://agentcommunicationprotocol.dev/core-concepts/architecture | quote: "a single process can act as both a server (handling incoming requests) and a client (making outbound requests)" | type: official

### 传输层
- [C13] ACP 使用 HTTP + REST 作为传输层，以"lightweight, runtime-free agent invocation"为特点 | src: https://agentcommunicationprotocol.dev/about/mcp-and-a2a | quote: "REST-based Communication: Enables lightweight, runtime-free agent invocation and scalable system integration" | type: official
- [C14] ACP 采用 HTTP 原生设计，如同 HTTP 协议一样是无状态的（stateless by design） | src: https://agentcommunicationprotocol.dev/core-concepts/architecture | quote: "ACP is a stateless protocol by design, just like HTTP" | type: official

### 消息格式
- [C15] ACP 消息采用 MIME-type 多部分结构（multipart message structure），支持可扩展性 | src: https://agentcommunicationprotocol.dev/about/mcp-and-a2a | quote: "MIME-type-based message structure designed for extensibility" | type: official
- [C16] ACP 消息包含角色标识、零件数组、内容类型字段；每个消息部分含 content、content_type、content_encoding、content_url | src: https://agentcommunicationprotocol.dev/introduction/quickstart | quote: "Role identification... Parts array containing content objects... content_type field... content_encoding... content_url" | type: official
- [C17] ACP 支持多模态消息，包括结构化数据、文本、图像、embeddings | src: https://research.ibm.com/projects/agent-communication-protocol | quote: "multimodal message support including structured data, text, images, and embeddings" | type: official

### 鉴权机制
- [C18] ACP 规范支持 Bearer tokens、Basic Auth、JWT 等标准 HTTP 认证方法 | src: https://www.ml4devs.com/what-is/acp-agent-communication-protocol/ | quote: "Standard HTTP authentication methods such as Bearer tokens, Basic Auth, and JWTs are supported" | type: secondary
- [C19] ACP 支持可选的 mTLS（mutual TLS），消息部分通过 JSON Web Signatures (JWS) 加强完整性 | src: https://www.ml4devs.com/what-is/acp-agent-communication-protocol/ | quote: "authentication... bearer tokens or optional mutual TLS (mTLS), while integrity is reinforced through JSON Web Signatures (JWS)" | type: secondary

### 版本规则
- [C20] ACP 采用 semantic versioning，最新版本为 v1.0.3（发布于 2025 年 8 月 21 日） | src: https://github.com/i-am-bee/acp/releases | quote: "Latest release is v1.0.3, published on August 21, 2025" | type: official
- [C21] ACP 版本演进：v1.0.0（2025-07-01）、v1.0.1（2025-07-24）、v1.0.2（2025-08-15）、v1.0.3（2025-08-21） | src: https://github.com/i-am-bee/acp/releases | quote: "v1.0.0 – July 1, 2025... v1.0.1 – July 24, 2025... v1.0.2 – August 15, 2025... v1.0.3 – August 21, 2025" | type: official

### 典型实现与采用者
- [C22] BeeAI Framework 是 ACP 的参考实现，提供 Python 和 TypeScript SDK | src: https://github.com/i-am-bee/acp | quote: "Python SDK with server implementation and client libraries, a TypeScript SDK with client libraries" | type: official
- [C23] ACP 官方文档站点为 agentcommunicationprotocol.dev，由 Linux Foundation 维护 | src: https://agentcommunicationprotocol.dev/introduction/welcome | type: official

### 与其他协议关系
- [C24] ACP 支持 MCP（Model Context Protocol）扩展，允许 agent 在网络上暴露和访问工具 | src: https://agentcommunicationprotocol.dev/core-concepts/architecture | quote: "ACP supports the MCP extension, allowing agents to expose and access tools across the network" | type: official
- [C25] ACP-IBM 和 Zed 的 Agent Client Protocol (ACP-Zed) 是两个不同的协议，无任何关联 | src: https://zed.dev/acp | quote: "Agent Client Protocol is an open standard that enables any agent to integrate seamlessly with any editing environment" vs https://github.com/i-am-bee/acp | quote: "Open protocol for communication between AI agents, applications, and humans" | type: official

## conflicts
- 关于 A2A 合并的开始日期：一些来源说"2025 年 8 月 25 日"，但 GitHub 讨论和官方博客都确认是这个日期。无实质冲突，仅精度差异。

## gaps
- 状态归属（维度 6）：官方文档未明确说明 session/task state 由谁持有（是否由 client、server 还是双方共同维护），只提及"stateless by design"。
- 鉴权具体实现细节：官方文档提到支持哪些鉴权方式，但未提供具体的 header 字段名称或请求示例。
- 与 MCP 的互补性详细说明：仅提及"支持 MCP extension"，未详述如何配合使用或分工。

## leads
- BeeAI Platform 迁移指南：查看 https://github.com/i-am-bee/beeai-platform 获取从 ACP 到 A2A 的具体适配器和迁移步骤
- A2A 技术委员会完整名单与具体分工：查看 Linux Foundation 官方 A2A 项目页面
- 其他采用 ACP 或计划迁移至 A2A 的开源框架/企业用户

## Q1 答案：ACP-IBM 与 ACP-Zed 是否同一物
**否。它们是完全不同的两个协议，无任何关联。**

- **ACP-IBM**（Agent Communication Protocol）：IBM Research 主导，用于 **agent↔agent** 之间的通信，支持代理发现、任务委托、协作。基于 HTTP/REST。
- **ACP-Zed**（Agent Client Protocol）：Zed 和 JetBrains 主导，用于 **编辑器/IDE↔AI 代理** 的通信，基于 JSON-RPC 2.0，类似 Language Server Protocol（LSP）但用于 agent。

两个协议的目标场景、技术方案、治理方完全不同。官方文档中无任何提及对方的记录。
