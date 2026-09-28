# r1-scout
question: 除了 MCP、A2A、ACP（IBM 的 Agent Communication Protocol 和 Zed 的 Agent Client Protocol）、AG-UI 之外，2024–2026 年「agent 互操作协议」领域还有哪些值得收录的协议或标准？请specifically 查证以下几个是否存在、是什么、谁提出的、一句话定位：ANP（Agent Network Protocol）、AGNTCY（Cisco 发起的 agent 互联倡议）、LMOS（Eclipse LMOS）、x402（Coinbase 发起的 agent 支付协议，是否算这个 scope）。此外，你观察到的这几类协议整体上在「鉴权标准化程度」「版本/治理模式」（单厂商 vs 基金会）上有没有可以先归纳的共性或对比线索？
checked: https://github.com/agent-network-protocol/AgentNetworkProtocol, https://www.agent-network-protocol.com/, https://w3c-cg.github.io/ai-agent-protocol/, https://eclipse.dev/lmos/, https://github.com/coinbase/x402, https://arxiv.org/html/2505.02279v1, https://arxiv.org/html/2602.11327v2

## claims
- [C1] ANP (Agent Network Protocol) 存在，由社区发起，定位为"Open protocol stack for the Agentic Web"支持去中心化身份、发现、消息和支付 | src: https://www.agent-network-protocol.com/ | quote: "Open protocol stack for the Agentic Web. Decentralized identity, discovery, messaging, and payment protocols" | type: official

- [C2] ANP白皮书发布时间为May 2025，以W3C White Paper形式发行 | src: https://arxiv.org/html/2505.02279v1 | quote: "ANP-Community published its Agent Network Protocol (ANP) as a W3C White Paper in May 2025" | type: secondary

- [C3] AGNTCY是由Cisco Outshift发起的agent互操作倡议，现由Linux Foundation托管，包含Agent Connect Protocol (ACP)作为核心 | src: https://tfir.io/ciscos-agntcy-takes-on-ai-agent-fragmentation-under-linux-foundation-umbrella/ | quote: "AGNTCY...now hosted under the Linux Foundation" | type: secondary

- [C4] LMOS (Language Model Operating System Protocol) 由Eclipse Foundation开发，定位为"foundational architecture for building an Internet of Agents" | src: https://eclipse.dev/lmos/docs/introduction/ | quote: "provide a foundational architecture for building an Internet of Agents (IoA)" | type: official

- [C5] LMOS使用W3C Decentralized Identifiers (DIDs)进行身份认证和OAuth2支持 | src: https://eclipse.dev/lmos/docs/lmos_protocol/introduction/ | quote: "agents and tools can leverage W3C Decentralized Identifiers (DIDs) for secure, verifiable, and self-sovereign authentication" | type: official

- [C6] x402是Coinbase发起的开放支付标准，使用HTTP 402 "Payment Required"状态码启用AI agents进行链上stablecoin支付 | src: https://github.com/coinbase/x402 | quote: "open standard for internet-native payments...leverages the long-reserved HTTP 402 Payment Required status code" | type: official

- [C7] x402基金会由Coinbase和Cloudflare于2025年成立，核心成员包括Google、Visa、AWS、Circle、Anthropic和Vercel | src: https://www.coinbase.com/developer-platform/discover/launches/x402 | quote: "Coinbase and Cloudflare launched the x402 Foundation in 2025...members...Google, Visa, AWS, Circle, Anthropic, and Vercel" | type: secondary

- [C8] ANP采用W3C DIDs (did:wba)进行去中心化身份认证，所有数据传输强制加密 | src: https://w3c-cg.github.io/ai-agent-protocol/ | quote: "Decentralized identity through did:wba...End-to-end encryption...All data is encrypted between sender and receiver" | type: official

- [C9] MCP在March 2025添加OAuth 2.0认证，但缺少会话关闭时的凭证撤销和强制审计追踪 | src: https://arxiv.org/html/2602.11327v2 | quote: "MCP added OAuth 2.0 authentication in March 2025, but MCP lacks credential revocation on session close" | type: secondary

- [C10] A2A通过agent cards (JSON文档)进行发现，使用OAuth 2.0/JWT认证 | src: https://arxiv.org/html/2602.11327v2 | quote: "Discovery happens through agent cards...authentication via OAuth 2.0/JWT" | type: secondary

- [C11] Linux Foundation在June 2025宣布启动A2A项目，Google将协议转移至Foundation；December 2025成立Agentic AI Foundation，MCP、goose和AGENTS.md为founding contributions | src: https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents/ | quote: "Google transferred the protocol...to the Linux Foundation...Agentic AI Foundation (AAIF) in December 2025" | type: official

- [C12] Coral Protocol采用W3C DIDs、blockchain微支付和端到端加密建立去中心化agent协作 | src: https://arxiv.org/html/2505.00749 | quote: "decentralized identity, on-chain micropayments using $CORAL token, and memory-augmented communication framework" | type: secondary

- [C13] AITP由NEAR Foundation发起，RFC发布于February 2025，显式聚焦于跨信任边界的agent互动，使用blockchain支持 | src: https://aitp.dev/vision | quote: "focus on enabling agent interactions across trust boundaries...Blockchain in decentralized multi-agent environments" | type: secondary

- [C14] Visa Trusted Agent Protocol (TAP)于October 2025发布，通过HTTP request headers中的加密身份签名验证agent合法性 | src: https://eco.com/support/en/articles/14845482-visa-trusted-agent-protocol-tap-explained | quote: "signs an AI agent's identity into HTTP request headers...answer one question cryptographically: is this agent legitimate" | type: secondary

- [C15] Agora protocol是Oxford University论文（October 2024），混合结构化routine与自然语言进行高效LLM通信，目前无官方开源实现 | src: https://arxiv.org/html/2504.16736v2 | quote: "academic discussions...no open-source framework implementing Agora's ideas yet" | type: secondary

- [C16] agents.json标准最后版本为February 2025，项目已弃用（404文档、过期Discord邀请、YouTube无更新） | src: https://agent-network-protocol.com/blogs/posts/agent-communication-protocols-comparison.html | quote: "last version dates from February 2025, and the project appears abandoned" | type: secondary

- [C17] ANP安全架构在W3C DID与强制加密方面表现最优，A2A通过OAuth 2.0/JWT提供中等保护，MCP和Agora因缺乏加密身份绑定漏洞更高 | src: https://arxiv.org/html/2602.11327v2 | quote: "ANP demonstrates the strongest security posture through W3C Decentralized Identifiers...A2A provides moderate protection via OAuth 2.0/JWT" | type: secondary

- [C18] 鉴权标准化主流方向分为四类：（1）W3C DIDs：ANP/LMOS/Coral；（2）OAuth 2.0/JWT：MCP/A2A/LMOS；（3）加密签名HTTP headers：TAP；（4）Blockchain身份：AITP/Coral | src: https://arxiv.org/html/2602.11327v2, https://eclipse.dev/lmos/docs/lmos_protocol/introduction/, https://w3c-cg.github.io/ai-agent-protocol/ | quote: "Multiple authentication schemes...DID-based identity solutions...cryptographic binding" | type: secondary

- [C19] 治理模式显著分化：单厂商向Foundation过渡（MCP/A2A/ACP转入Linux Foundation及Agentic AI Foundation）vs 开放/社区（ANP/LMOS/Coral）vs 行业联盟（x402 Foundation包含科技+支付公司） | src: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation/ | quote: "Agentic AI Foundation (AAIF) in December 2025, with founding contributions...MCP...goose...AGENTS.md" | type: official

- [C20] LMOS在Architecture层面选择传输协议无关性（agnostic），使用W3C WoT协议绑定抽象 | src: https://eclipse.dev/lmos/ | quote: "transport-protocol agnostic...leverages the W3C WoT protocol binding abstraction" | type: official

## conflicts
- IBM ACP vs Cisco ACP: 搜索结果显示Cisco AGNTCY框架中有Agent Connect Protocol (ACP)，但Linux Foundation在2025年8月宣布IBM's ACP团队将加入A2A Technical Steering Committee，合并ACP到A2A | src: https://arxiv.org/html/2602.11327v2 | quote: "August 2025, the Linux Foundation announced that ACP would merge into A2A" | type: secondary
- AITP vs agents.json可用性：AITP (NEAR Foundation, Feb 2025) 活跃开发，agents.json (Feb 2025)已弃用 | src: https://agent-network-protocol.com/blogs/posts/agent-communication-protocols-comparison.html vs https://aitp.dev/vision | type: secondary

## gaps
- ANP社区结构具体治理流程（仓库shows GaoWei Chang copyright，但无详细governance规则文档）
- LMOS是否已为W3C标准或仍为Eclipse孵化项目
- x402与agent协议"scope"边界清晰度（支付协议vs communication protocol分类）
- Coral Protocol官方/仓库地址确认（仅arxiv论文可得）
- AGNTCY完整组件列表及OASF/ADS/SLIM具体实现状态

## leads
- **x402 (Coinbase Payment Protocol)** — HTTP 402 Payment Required标准，支持链上stablecoin支付，x402 Foundation (2025) — 建议纳入正文（payment layer protocol，与core 5协议互补而非并行）
- **AITP (NEAR Foundation)** — Blockchain-native agent交互标准（RFC Feb 2025），聚焦跨信任边界认证 — 可选纳入（blockchain层独特视角）
- **TAP (Visa Trusted Agent Protocol)** — 商业payment系统中的agent身份验证（Oct 2025），HTTP headers加密签名 — 建议纳入（payment routing特定）
- **Coral Protocol** — 去中心化infrastructure integrating DIDs + blockchain + MCP，学术/研究阶段 — 可选纳入（architecture model对标）
- **鉴权标准化趋势**：W3C DIDs逐成主流（ANP/LMOS/Coral），单纯自声明身份（MCP v1）遭安全批评，payment protocols分化出HTTP 402 (x402) + blockchain (AITP/Coral) + HTTP headers (TAP)三轨
- **治理分化**：单厂商协议向Linux Foundation + Agentic AI Foundation集中（MCP/A2A/ACP）；去中心化视角由Eclipse/W3C支撑（LMOS向W3C标准化）；支付层由独立foundation主导（x402/AITP）
