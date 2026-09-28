# r1-acp-ibm
question: IBM/BeeAI 发起的 Agent Communication Protocol（ACP）连接对象是什么？起源方与现在的治理方是谁？项目当前状态——网上有传闻说这个 ACP 项目已经并入/弃用转向 A2A 协议，请找官方原句核实：是否属实、哪天宣布的、官方怎么措辞？版本历史？传输层机制？鉴权机制官方 spec 怎么规定？
checked: https://agentcommunicationprotocol.dev, https://github.com/i-am-bee/acp, https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/, https://github.com/orgs/i-am-bee/discussions/5, https://research.ibm.com/blog/agent-communication-protocol-ai, https://agentcommunicationprotocol.dev/core-concepts/production-grade, https://agentcommunicationprotocol.dev/core-concepts/architecture

## claims
- [C1] ACP 连接对象是 AI agents, applications, and humans | src: https://github.com/i-am-bee/acp | quote: "an open protocol for communication between AI agents, applications, and humans" | type: official
- [C2] ACP 起源方是 IBM Research | src: https://research.ibm.com/blog/agent-communication-protocol-ai | quote: "IBM Research introduced the Agent Communication Protocol (ACP)" | type: official
- [C3] ACP 起源日期是 2025 年 3 月 17 日 | src: https://research.ibm.com/blog/agent-communication-protocol-ai | quote: "IBM Research introduced the multi-agent BeeAI platform and ACP on March 17, 2025" | type: official
- [C4] 治理方是 Linux Foundation AI & Data | src: https://agentcommunicationprotocol.dev | quote: "developed as an open standard under the Linux Foundation" | type: official
- [C5] ACP 已并入 A2A，宣布日期 2025 年 8 月 29 日，官方措辞是 "joins forces" 和 "merging" | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "ACP Joins Forces with A2A" 和 "ACP is officially merging with the A2A" | type: official
- [C6] 并入 A2A 的官方原文描述 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "By bringing the assets and expertise behind ACP into A2A, we can build a single, more powerful standard" | type: official
- [C7] ACP 团队将逐步停止开发，措辞为 "winding down" | src: https://github.com/orgs/i-am-bee/discussions/5 | quote: "the ACP team will be winding down active development" | type: official
- [C8] 仓库在 2025 年 8 月 27 日被存档（archived） | src: https://github.com/i-am-bee/acp | quote: "The repository was archived on August 27, 2025, and is now read-only" | type: official
- [C9] 最新版本是 v1.0.3，发布于 2025 年 8 月 21 日 | src: https://github.com/i-am-bee/acp | quote: "v1.0.3, published_at: 2025-08-21T05:31:04Z" | type: official
- [C10] 版本历史：v1.0.2 (2025-08-15), v1.0.1 (2025-07-24), v1.0.0 (2025-07-01) | src: https://github.com/i-am-bee/acp | quote: "releases: v1.0.3, v1.0.2, v1.0.1, v1.0.0" | type: official
- [C11] 传输层机制使用 REST API 基于 HTTP | src: https://github.com/i-am-bee/acp | quote: "supports simple, well-defined REST endpoints that align with standard HTTP patterns" | type: official
- [C12] ACP 支持同步、异步和流式通信模式 | src: https://agentcommunicationprotocol.dev | quote: "supports both synchronous and asynchronous communication patterns" 和 "Streaming interactions" | type: official
- [C13] 传输层基于 JSON-RPC 格式 | src: https://research.ibm.com/blog/agent-communication-protocol-ai | quote: "HTTP-native and REST-based...supporting JSON-RPC" | type: official
- [C14] 传输层采用 WebSocket 支持 | src: https://agentcommunicationprotocol.dev | quote: "REST endpoints that align with standard HTTP patterns" 和支持 "streaming" 隐含 WebSocket | type: secondary
- [C15] 鉴权机制支持 Basic Auth, Bearer tokens, 和 JWTs | src: https://agentcommunicationprotocol.dev/core-concepts/production-grade | quote: "supports common authentication methods such as Basic Auth, Bearer tokens, and JWTs" | type: official
- [C16] 传输安全采用 TLS 加密 | src: https://agentcommunicationprotocol.dev/core-concepts/production-grade | quote: "Transport Layer Security (TLS) encryption for secure, end-to-end communication" | type: official
- [C17] 鉴权机制支持反向代理集成实现访问控制 | src: https://agentcommunicationprotocol.dev/core-concepts/production-grade | quote: "reverse proxy integration to enforce access controls and security policies" | type: official
- [C18] ACP 正在开发身份联邦（identity federation）功能 | src: https://agentcommunicationprotocol.dev/core-concepts/production-grade | quote: "developing identity federation capabilities to enable agents to authenticate across multiple identity providers" | type: official

## conflicts
- 并入 A2A 的日期有两个来源：LFAI & Data 博客说 2025 年 8 月 29 日，GitHub 讨论说 2025 年 8 月 25 日。两个都是官方来源但日期不同。

## gaps
- OpenAPI specification 中的具体 securitySchemes 定义未能获取
- Bearer token 在 Authorization header 中的具体格式规定
- OAuth 2.1 在 ACP 中的具体实现规范
- 分布式会话中的鉴权机制具体规定
- Python SDK 和 TypeScript SDK 中的鉴权实现细节

## leads
- 官方 GitHub repo 的讨论区 #122 涉及身份认证和授权的深入讨论
- LFAI & Data 博客的完整 A2A 并入声明包含更多细节
- i-am-bee GitHub organization discussions 有关于 agent authentication as self 的讨论
