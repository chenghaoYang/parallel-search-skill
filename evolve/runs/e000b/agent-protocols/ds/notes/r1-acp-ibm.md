# r1-acp-ibm
question: IBM/BeeAI 发起的 Agent Communication Protocol（ACP）管什么、怎么传输、怎么鉴权、谁治理、当前版本、现状——它现在是否还在独立开发，还是已经合并/停止/转交给了 A2A 或 Linux Foundation 的 Agntcy 之类的组织？以及 IBM 官方文档有没有提到另一个同名的 Zed ACP？
checked: https://github.com/i-am-bee/acp, https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/, https://www.ibm.com/new/announcements/ibm-adds-open-source-projects-docling-beeaI-and-data-prep-kit-added-to-the-linux-foundation, https://www.ibm.com/think/topics/agent-communication-protocol, https://framework.beeai.dev/integrations/acp, https://workos.com/blog/ibm-agent-communication-protocol-acp

## claims
- [C1] IBM's Agent Communication Protocol focuses on agent-to-agent communication, not workflow management | src: https://www.ibm.com/think/topics/agent-communication-protocol | quote: "ACP enables agent orchestration for any agentic architecture, but it doesn't manage workflows, deployments or coordination" | type: official
- [C2] ACP uses JSON-RPC over HTTP/WebSockets for transport | src: https://workos.com/blog/ibm-agent-communication-protocol-acp | quote: "JSON‑RPC over HTTP/WebSockets" as foundational wire format | type: secondary
- [C3] ACP employs REST-based HTTP communication | src: https://www.ibm.com/think/topics/agent-communication-protocol | quote: "ACP uses standard HTTP conventions for communication" | type: official
- [C4] ACP supports capability tokens as authentication mechanism | src: https://workos.com/blog/ibm-agent-communication-protocol-acp | quote: "Capability tokens—described as unforgeable, signed objects that encode resource type, ops, and expiry" | type: secondary
- [C5] ACP includes Kubernetes RBAC bridge for security | src: https://workos.com/blog/ibm-agent-communication-protocol-acp | quote: "Kubernetes RBAC bridge—Maps capability claims onto existing cluster roles" | type: secondary
- [C6] ACP operates under open governance with community contributions | src: https://www.ibm.com/think/topics/agent-communication-protocol | quote: "welcomes contributions from developers, researchers and organizations through GitHub and Discord" | type: official
- [C7] IBM launched ACP in March 2025 for BeeAI Platform | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "IBM Research launched the Agent Communication Protocol (ACP) in March 2025 to power its BeeAI Platform" | type: official
- [C8] BeeAI project and ACP donated to Linux Foundation in March 2025 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "Later that month, the BeeAI project—and with it, ACP—was donated to the Linux Foundation" | type: official
- [C9] ACP merged with A2A in August 2025 | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "Today, we're excited to share that ACP is officially merging with the A2A under the Linux Foundation umbrella" | type: official
- [C10] ACP repository was archived August 27, 2025 | src: https://github.com/i-am-bee/acp | quote: "The Agent Communication Protocol (ACP) repository is now archived as of August 27, 2025 and is read-only" | type: official
- [C11] ACP team is winding down active development and redirecting to A2A | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "the ACP team will be winding down active development and will begin contributing its technology and expertise directly to A2A" | type: official
- [C12] Kate Blair (IBM Research Director of Incubation) led ACP development | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "says Kate Blair, Director of Incubation for IBM Research who has overseen ACP's development" | type: official
- [C13] IBM will have representation on A2A Technical Steering Committee | src: https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ | quote: "Blair will join the A2A Technical Steering Committee on behalf of IBM, alongside representatives from Google, Microsoft, AWS, Cisco, Salesforce, ServiceNow, and SAP" | type: official
- [C14] ACP supports synchronous, asynchronous, and streaming messaging patterns | src: https://workos.com/blog/ibm-agent-communication-protocol-acp | quote: "Synchronous: standard HTTP POST returning JSON responses; Asynchronous: fire-and-forget calls; Streaming: server pushes incremental messages over WebSockets/SSE" | type: secondary

## conflicts
- None found between IBM official sources

## gaps
- No specific version number (1.0, 0.9, etc.) found in official IBM documentation
- IBM/BeeAI official documentation does NOT mention or address Zed's "Agent Client Protocol" (also abbreviated ACP)
- No official IBM statement explaining the naming collision with Zed's ACP
- No explanation found for why IBM did not preemptively address the naming conflict after Zed's protocol gained prominence

## leads
- The lack of any IBM acknowledgment of the Zed ACP naming conflict is notable - suggest checking if there were any community discussions or issues on i-am-bee GitHub about this
- BeeAI migration guide for moving from ACP to A2A may contain additional technical details on protocol differences
- A2A protocol documentation should clarify which ACP features were incorporated vs. which were deprecated
