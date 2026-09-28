# r2-acp-zed-verify
question: Verify Zed's Agent Client Protocol authentication mechanism and governance definition from primary sources (agentclientprotocol.com and github.com/zed-industries/agent-client-protocol), specifically: (1) authenticate method JSON-RPC schema, parameters, implementation responsibility; (2) official governance structure, project maintenance, neutrality
checked: https://agentclientprotocol.com, https://github.com/zed-industries/agent-client-protocol, https://agentclientprotocol.com/community/governance, https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/schema/v1/schema.json, https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/MAINTAINERS.md, https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/CONTRIBUTING.md, https://agentclientprotocol.com/community/working-interest-groups

## claims
- [C1] AuthenticateRequest is the JSON-RPC method for authentication, called when agent requires authentication before session creation | src: https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/schema/v1/schema.json | quote: "Authenticates the client using the specified authentication method. Called when the agent requires authentication before allowing session creation." | type: official
- [C2] authenticate method takes methodId parameter that must be one of the methods advertised in initialize response | src: https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/schema/v1/schema.json | quote: "The ID of the authentication method to use. Must be one of the methods advertised in the initialize response." | type: official
- [C3] Protocol defines two authentication method types: "terminal" (client runs agent as separate interactive process) and "agent" (agent handles authentication itself) | src: https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/schema/v1/schema.json | quote: "Client runs the configured agent program as a separate interactive process... Agent handles authentication itself through `authenticate`. This is the default when no `type` is specified." | type: official
- [C4] AuthMethodAgent is default authentication type where implementation details are left to agent | src: https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/schema/v1/schema.json | quote: "Agent handles authentication itself through `authenticate`. This is the default authentication method type." | type: official
- [C5] Lead Maintainers are Ben Brandt (Zed) and Sergey Ignatov (JetBrains) with governance authority | src: https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/MAINTAINERS.md | quote: "Ben Brandt benjamin@zed.dev ... Sergey Ignatov sergey.ignatov@jetbrains.com" | type: official
- [C6] Core Maintainers team includes Agus Zubiaga, Anna Zhdan, Niko Matsakis, Vadim Briliantov | src: https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/MAINTAINERS.md | quote: "Core Maintainers: Agus Zubiaga, Anna Zhdan, Niko Matsakis, Vadim Briliantov" | type: official
- [C7] Project governance is jointly managed by Zed and JetBrains representing collaborative model to serve broader ecosystem | src: https://agentclientprotocol.com/community/governance | quote: "ACP is jointly governed by Zed and JetBrains, representing a collaborative model where the protocol serves the broader ecosystem." | type: official
- [C8] Interim governance arrangement aims toward eventual transition to independent foundation status | src: https://agentclientprotocol.com/community/governance | quote: "The interim arrangement aims toward eventual transition to independent foundation status, balancing commercial stakeholder interests with community input through open communication channels and public decision documentation." | type: official
- [C9] RFD (Request for Discussion) process required for significant protocol changes | src: https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/CONTRIBUTING.md | quote: "Before a significant change or addition to the protocol is made, you should likely open an RFD following our RFD process to get feedback on your proposed changes before you do a lot of implementation work." | type: official
- [C10] Core maintainers convene biweekly to discuss proposals with emphasis on public decision-making | src: https://agentclientprotocol.com/community/governance | quote: "The core maintainer group convenes biweekly to discuss proposals. The governance framework emphasizes transparency: The core maintainers should publicly articulate their decision-making." | type: official
- [C11] Project licensed under Apache 2.0 without requiring Contributor License Agreement | src: https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/CONTRIBUTING.md | quote: "This project does not require a Contributor License Agreement (CLA). Instead, contributions are accepted under the following terms" | type: official
- [C12] MAINTAINERS.md updated June 1, 2026 documenting governance structure | src: https://raw.githubusercontent.com/zed-industries/agent-client-protocol/main/MAINTAINERS.md | quote: "Last updated: June 1, 2026" | type: official

## conflicts
None identified

## gaps
- Specific JSON-RPC wire format examples for authenticate request/response not found in schema or docs pages accessed
- Details on how agents actually implement authentication beyond the protocol framework (implementation patterns, examples) not documented at agentclientprotocol.com or main repo
- Formal transition timeline or conditions for moving to independent foundation status not specified
- Whether Zed or JetBrains has final decision authority in case of governance disagreements not explicitly documented

## leads
- SDK implementations (Rust, TypeScript, Python, Kotlin, Java) may contain concrete authenticate method implementation examples
- agentclientprotocol.com/protocol/initialization might have additional initialization/auth flow details
- GitHub discussions or issues may document rationale behind dual-maintainer (Zed/JetBrains) governance model
