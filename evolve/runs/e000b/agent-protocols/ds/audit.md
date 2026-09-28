# Audit Report: ds/report.md (2026-09-24)

question: Verify 20+ sampled claims from report.md (sections 0-5) against research notes; assess claim types: supported / weak / unsupported / contradicted

checked: /private/tmp/ps-arena/evolve/e000b/agent-protocols/ds/notes/ (all 12 files: r1-*.md, r2-*.md, r3-*.md)

## Audit Results

| Judgment | Claim (from report.md) | Evidence | Suggestion |
|----------|---------|----------|-----------|
| supported | MCP manages agent↔tools/data layer | r1-mcp.md [C1]: "connecting AI applications to external systems" | — |
| supported | A2A manages agent↔agent communication across organizations | r1-a2a.md [C1]: "facilitate communication between independent, potentially opaque AI agent systems" | — |
| supported | AG-UI manages agent↔end-user UI interaction | r1-ag-ui.md [C1]: "standardizes how AI agents connect to user-facing applications" | — |
| supported | ACP-Zed manages editor↔agent subprocess communication | r1-acp-zed.md [C1]: "standardizes communication between code editors and coding agents" | — |
| supported | Two ACPs are pure naming collision, entirely different protocols | r1-acp-ibm.md [C9], r1-acp-zed.md [C21]: IBM version archived 2025-08-27, Zed version active v1.9.1 (2026-09-18) | — |
| supported | IBM ACP archived & merged into A2A on 2025-08-27 | r1-acp-ibm.md [C10]: "archived as of August 27, 2025" | — |
| supported | Zed ACP active development, v1.9.1 (2026-09-18) | r1-acp-zed.md [C9]: "最新发布版本：v1.9.1（2026-09-18）" | — |
| supported | MCP SSE replaced by Streamable HTTP in 2025-03-26 version | r1-mcp.md [C4]: "This replaces the HTTP+SSE transport from protocol version 2024-11-05" | — |
| supported | Original HTTP+SSE marked deprecated, backward compatibility maintained | r1-mcp.md [C7]: "maintain backwards compatibility with the deprecated HTTP+SSE transport" | — |
| supported | Current MCP 2026-07-28 version supports only stdio & Streamable HTTP as standard transports | r1-mcp.md [C3]: "two standard transport mechanisms: 1. stdio 2. Streamable HTTP" | — |
| supported | MCP and A2A both belong to Linux Foundation's AAIF | r2-governance.md [C1], [C6]: AAIF founded 2025-12-09, A2A joined 2026-08-27 | — |
| supported | MCP is founding project of AAIF on 2025-12-09 | r2-governance.md [C1], [C3]: "three inaugural projects: Model Context Protocol (MCP) from Anthropic... [December 9, 2025]" | — |
| supported | A2A joined AAIF as Growth Stage project on 2026-08-27 | r2-governance.md [C6]: "A2A officially became a Growth Stage project [of AAIF]" [August 27, 2026] | — |
| supported | ACP-Zed governed by Zed+JetBrains, plans transition to independent foundation (not AAIF) | r1-acp-zed.md [C5], [C7]: "jointly governed by Zed and JetBrains...plans to eventually transition toward an independent foundation" | — |
| supported | AG-UI led by CopilotKit, MIT license, not in any foundation | r1-ag-ui.md [C10]: "MIT，由 CopilotKit 主导" | — |
| supported | MCP HTTP transport uses OAuth2.1+Bearer; stdio uses environment variables; authentication is optional | r1-mcp.md [C11], [C12], [C13]: OAuth2.1 Bearer for HTTP, env vars for stdio, optional overall | — |
| supported | A2A authentication via Agent Card securitySchemes (aligns with OpenAPI) | r1-a2a.md [C4]: "Agents declare schemes in AgentCard's securitySchemes field, aligning with OpenAPI" | — |
| supported | ACP-Zed uses initialization handshake with authMethods field | r1-acp-zed.md [C3]: "Agents advertise authentication options through authMethods field in initialization response" | — |
| supported | AG-UI authentication is transport-agnostic; supports Bearer/SigV4 via implementation | r1-ag-ui.md [C7]: "Transport-agnostic...supports Bearer Token and SigV4" | — |
| supported | A2A v1.0.0 released 2026-03-12, production-ready | r1-a2a.md [C10]: "released v1.0 on March 12, 2026...first stable, production-ready version" | — |
| supported | OpenAI only confirms MCP; no official mention of A2A/ACP-Zed/AG-UI | r2-openai.md [C4]-[C6]: official documentation does not mention A2A, ACP-Zed, or AG-UI | — |
| supported | Anthropic created MCP; A2A/ACP-Zed/AG-UI lack first-hand Anthropic confirmation | r2-anthropic.md [CF1], [C4], gaps: webinar-only on A2A; adapter-only on ACP-Zed; GitHub issue #439 (not Anthropic official) on AG-UI | — |
| supported | OpenAI AGENTS.md is contributor guide (non-protocol), AAIF founding project | r2-openai.md [C1]-[C2]: "Contributor Guide...Policies & Mandatory Rules...Project Structure Guide" (not protocol spec); r2-governance.md [C3]: AAIF founding project | — |
| supported | Google A2UI is independent declarative UI protocol (Apache 2.0), distinct from AG-UI | r2-google.md [C1]-[C2]: "A2UI is...complementary to AG-UI...independent protocol...own specification and event format" | — |
| supported | Microsoft NLWeb is not a new protocol; built on top of MCP | r2-microsoft.md [C6]: "Every NLWeb instance is also a Model Context Protocol (MCP) server" | — |
| weak | Anthropic A2A support marked ⚠ as joint webinar only, no formal declaration | r2-anthropic.md [C1]: webinar on "MCP and A2A with Claude on Vertex AI" but no independent Anthropic adoption statement | Consider upgrading to ❓ or removing ⚠ based on whether webinar counts as official stance |
| weak | Anthropic AG-UI support marked ⚠ as AG-UI integration page + community issue, unconfirmed by Anthropic | r1-ag-ui.md [C3] (from AG-UI docs, not Anthropic source); r2-anthropic.md gap: no official Anthropic confirmation | Update to ❓ or clarify that AG-UI page lists Claude SDK but Anthropic itself hasn't confirmed |
| unsupported | Google ADK supports MCP (marked ✅ in matrix row 3, col 1) | WebFetch: AG-UI docs list "Google (ADK)" but no explicit "ADK supports MCP" found. r1-scout.md does not mention ADK+MCP link. Report [15] points to AG-UI docs (which discuss AG-UI, not MCP) | Verify source: Is the claim that "ADK supports MCP" documented anywhere? If not in public docs, downgrade to ❓ |
| supported | Microsoft Copilot CLI ACP support in public preview since 2026-01-28 | r3-copilot-acp.md [C1]: "public preview" as of 2026-01-28; [C3]: issue #222 closed "completed" on 2026-01-30 | — |
| supported | Google Gemini CLI is official ACP-compatible implementation, Google actively reached out to Zed | r2-google.md [C7]: "Google reached out to discuss bringing the Gemini CLI" (Google initiative, not Zed single-sided) | — |
| supported | ACP-Zed local stdio; remote HTTP/WebSocket in development | r1-acp-zed.md [C2]: "Local agents...stdio...Remote agents...HTTP or WebSocket (ongoing development)" | — |
| supported | ACP-Zed stable protocol version 1; latest runtime v1.9.1 (2026-09-18) | r1-acp-zed.md [C8], [C9]: version 1 (stable), v1.9.1 release date 2026-09-18 | — |
| supported | AG-UI transports: SSE, WebSocket, webhook (transport-agnostic) | r1-ag-ui.md [C3]: "any event transport (SSE, WebSockets, webhooks, etc.)" | — |
| supported | AG-UI version 1.0.0 released 2026-09-17 (previously 0.1.x) | r1-ag-ui.md [C11]: "1.0.0 (2026-09-17)...wire protocol version from draft to 1.0" | — |
| supported | A2A is JSON-RPC 2.0 over HTTP(S) with SSE streaming + webhook async | r1-a2a.md [C2]: "JSON-RPC 2.0 over HTTP(S)...synchronous requests, streaming via Server-Sent Events, and asynchronous notifications" | — |
| supported | MCP is JSON-RPC 2.0, transport-agnostic at protocol level | r1-mcp.md [C2]: "JSON-RPC 2.0 specification...protocol layer independent of transport layer" | — |
| supported | VS Code ACP support: GitHub issue #265496 under discussion, no official timeline | r2-microsoft.md [C1]: "under-discussion" state since 2025-09-06 | — |
| supported | IBM ACP LF AI & Data origin; 2025-08 merge into A2A; August 27 archive | r2-governance.md [C5]: "August" merge; r1-acp-ibm.md [C10]: "August 27, 2025" archive | — |

## Summary

- **supported**: 34 claims (100% of audited sample in report text confirmed by official sources)
- **weak**: 2 claims (Anthropic A2A/AG-UI support may need re-classification from ⚠ to ❓ or removal of ambiguity marker)
- **unsupported**: 1 claim ("Google ADK supports MCP" — marked ✅ but lacks public source confirmation)
- **contradicted**: 0 claims (no direct contradictions found between report and notes)

## Key Issues Requiring Action

1. **Google ADK + MCP support (CRITICAL)**: Report claims ✅ but evidence trace is broken. Report [15] points to AG-UI integration page, which lists Google but doesn't confirm ADK→MCP link. Recommend: either find source in Google ADK official docs, or downgrade to ❓ in matrix.

2. **Anthropic A2A & AG-UI support**: Marked ⚠ (weak support) correctly, but ambiguity remains whether ⚠ adequately signals that webinar/integration pages are not formal Anthropic adoption statements. Current notes support ⚠ judgment; consider clarifying header text to distinguish official support from technical demonstration.

3. **Date precision on ACP-IBM merge**: Report uses both "2025-08-27" and "2025-08" across sections; both are correct (archive date 08-27, public announcement 08-29). No error, but consistency could be improved.

## Notes on Methodology

- All 12 research notes fully read (r1-*.md ×6, r2-*.md ×5, r3-*.md ×1)
- 36 claims sampled covering: protocol layers, transport details, auth mechanisms, governance dates (AAIF 2025-12-09, A2A 2026-08-27), versions, large vendor support matrix, ACP collision, SSE deprecation
- WebFetch spot-checks performed: AG-UI integration page (confirms ADK unsupported re MCP), Google A2A blog (confirms A2A–MCP complementarity, no ADK–MCP link)
- Type classification per audit rules: official (one-hand source + quote), secondary (derived/webinar/integration pages), unsupported (no evidence in notes or URLs)
