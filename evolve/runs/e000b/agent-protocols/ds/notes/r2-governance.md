# r2-governance
question: MCP 治理转交 AAIF 的精确日期是什么？AAIF 是 Linux Foundation 的下属基金会（类似 LF AI & Data 那样），还是完全独立于 Linux Foundation 的新基金会？AAIF、Linux Foundation 直属的「A2A Project」、LF AI & Data（ACP-IBM 曾挂靠、现已并入 A2A）这三者之间是什么层级关系？
checked: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation, https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation, https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/, https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/, https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents, https://aaif.io/blog/a2a-joins-aaif

## claims
- [C1] AAIF 成立并接收 MCP 的日期为 2025 年 12 月 9 日 | src: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | quote: "Linux Foundation Announces the Formation of the Agentic AI Foundation (AAIF), Anchored by New Project Contributions Including Model Context Protocol (MCP)" [December 9, 2025] | type: official
- [C2] AAIF 是「a directed fund under the Linux Foundation」，而非独立基金会 | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "The Agentic AI Foundation functions as 'a directed fund under the Linux Foundation'" | type: official
- [C3] MCP 为 AAIF 的 founding project（初创项目），与 goose、AGENTS.md 并列 | src: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | quote: "AAIF was established with three inaugural projects: Model Context Protocol (MCP) from Anthropic, Goose from Block, AGENTS.md from OpenAI" | type: official
- [C4] A2A 项目最初于 2025 年 6 月 23 日成为 Linux Foundation project | src: https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents | quote: "Agent2Agent (A2A) protocol became a Linux Foundation project as of June 23, 2025" | type: official
- [C5] IBM 的 ACP 在 2025 年 8 月与 A2A 合并 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "IBM's Agent Communication Protocol (ACP) is officially merging with Google's Agent2Agent Protocol (A2A) under the Linux Foundation" | type: official
- [C6] A2A 于 2026 年 8 月 27 日正式加入 AAIF 作为 hosted project（已托管项目），而非 founding project | src: https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/ | quote: "A2A officially became a Growth Stage project [of AAIF]" [August 27, 2026] | type: official
- [C7] LF AI & Data 与 AAIF 是 Linux Foundation 下的两个独立基金会组织 | src: https://www.linuxfoundation.org/blog/what-agentic-ai-asks-of-open-source-strategy-a-new-layer-for-ospos | quote: "LF AI Foundation (LF AI) is the organization building an ecosystem to enable and sustain open source innovation in artificial intelligence, while the Agentic AI Foundation (AAIF) is a separate foundation" | type: official
- [C8] MCP 在 AAIF 中保持独立的治理模式，maintainers 继续优先考虑社区意见 | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "The Model Context Protocol's governance model will remain unchanged: the project's maintainers will continue to prioritize community input and transparent decision-making" | type: official
- [C9] A2A 和 MCP 在 AAIF 的技术栈中扮演互补角色，MCP 为垂直集成（agent 与 tools），A2A 为水平通信（agent 与 agent） | src: https://aaif.io/blog/a2a-joins-aaif | quote: "MCP focuses on the vertical integration between agents and tools. A2A handles the horizontal communication between agents" | type: official

## conflicts

## gaps
- AAIF 官网（aaif.io）未在页面明确说明与 Linux Foundation 的「directed fund」关系或组织结构
- 未找到 a2a-protocol.org 的 community/governance 官方页面原文，与 A2A 成为 AAIF hosted project 前后的治理架构演变说明

## leads
- AAIF 官网可能有更详细的治理文档或 FAQ，说明三层关系（LF → AAIF → MCP/A2A）
- LF AI & Data 官网的项目列表可能展示其与 AAIF 项目的明确分界
