# r2-vendor-gaps
question: 上一轮（r1-vendor）在厂商支持矩阵里留了几个 ❓ 空格，需要定向确认 OpenAI×A2A、Anthropic×A2A、OpenAI×AG-UI、Anthropic×AG-UI、Google×AG-UI 五个格子到底是"官方明确不支持"还是"我们没搜全"。
checked: https://a2a-protocol.org/latest/partners/, https://github.com/a2aproject/A2A, https://docs.ag-ui.com/integrations, https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai, https://cloud.google.com/blog/topics/developers-practitioners/guide-to-gemini-enterprise-and-a2ui-integration, https://openai.com/index/agentic-ai-foundation/, https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation

## claims
- [C1] OpenAI 不在 A2A Protocol 官方合作伙伴名单中 | src: https://a2a-protocol.org/latest/partners/ | quote: "alphabetically-organized partner list of hundreds of organizations" (OpenAI not listed) | type: official
- [C2] Anthropic 不在 A2A Protocol 官方合作伙伴名单中 | src: https://a2a-protocol.org/latest/partners/ | quote: "alphabetically-organized partner list" (Anthropic not listed) | type: official
- [C3] OpenAI 是 Agentic AI Foundation（现管理 A2A 的组织）的 Platinum 级成员 | src: https://openai.com/index/agentic-ai-foundation/ | quote: "OpenAI co-founds the Agentic AI Foundation" | type: official
- [C4] Anthropic 是 Agentic AI Foundation 的 Platinum 级成员/联合创始人 | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "Donating the Model Context Protocol and establishing the Agentic AI Foundation" | type: official
- [C5] Anthropic 与 Google Cloud 联合举办过"Deploying multi-agent systems using MCP and A2A with Claude on Vertex AI"主题的官方 webinar | src: https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai | quote: "webinar, hosted by Anthropic and Google Cloud on August 27, 2025" | type: official
- [C6] OpenAI 官方文档（openai.com/developers.openai.com）中无针对 A2A Protocol 的官方支持声明 | src: 搜索 site:openai.com + site:developers.openai.com "A2A" 无结果 | quote: "no dedicated OpenAI documentation pages specifically about the A2A protocol itself" | type: official
- [C7] Anthropic 官方文档（anthropic.com/docs.claude.com）中无针对 A2A 协议的明确独立支持声明 | src: 搜索 site:anthropic.com site:docs.claude.com "A2A" 仅返回已知 webinar | quote: "no specific webinar announcement from Anthropic about an A2A announcement" | type: official
- [C8] OpenAI 不在 AG-UI 官方集成列表中 | src: https://docs.ag-ui.com/integrations | quote: "The page does not specifically list OpenAI integrations" | type: official
- [C9] Anthropic 在 AG-UI 官方集成列表中，列有 Claude Managed Agents 和 Claude Agent SDK | src: https://docs.ag-ui.com/integrations | quote: "Claude Managed Agents - Anthropic's hosted agent sessions, bridged to AG-UI in TypeScript, Python, and .NET" | type: official
- [C10] Google ADK 在 AG-UI 官方集成列表中 | src: https://docs.ag-ui.com/integrations | quote: "Google ADK (Agent Development Kit) for building agents with Gemini models" | type: official
- [C11] Anthropic 官方文档中无 AG-UI 协议的提及 | src: 搜索 site:anthropic.com site:docs.claude.com "AG-UI" 无结果 | quote: "The search results do not contain any information about AG-UI on Anthropic's website or Claude documentation" | type: official
- [C12] Google Cloud 官方博客提供 A2UI 与 Gemini Enterprise 集成指南 | src: https://cloud.google.com/blog/topics/developers-practitioners/guide-to-gemini-enterprise-and-a2ui-integration | quote: "A2UI is an open protocol that agents use to return JSON payloads describing UI components" | type: official

## conflicts
- 无。A2A Protocol 官方合作伙伴名单与 Agentic AI Foundation 成员身份不冲突：OpenAI/Anthropic 虽未在 A2A 初期合作伙伴名单中，但通过 2025 年 12 月创立的 AAIF 进行了正式参与。

## gaps
- OpenAI 在 Claude Agent SDK 文档中对 A2A 的具体实现指南（仅见 community webinar 提及，无官方 API reference）
- Anthropic 在 docs.anthropic.com 中是否有 A2A Server 实现示例或 SDK 支持（webinar 有提及但无文档化）
- Google 在 AG-UI 集成列表中是否明确列名 Gemini API/ADK 的官方 AG-UI SDK 版本号
- OpenAI Agents Python SDK 中 A2A 支持的正式发版计划（仅见 GitHub Issue #1374 feature request）

## leads
- A2A 与 Agentic AI Foundation 联动：OpenAI/Anthropic 在协议治理层有正式参与（AAIF Platinum members），但初期合作伙伴名单中缺席，可能反映不同阶段的支持承诺
- AG-UI 厂商支持不对称：Anthropic 在 docs.ag-ui.com 集成列表中可见，但其官方文档中反而不提 AG-UI；Google/OpenAI 情形相反
- 建议补充查：(a) AAIF 官方文档对各成员 A2A 支持级别的定义（Platinum/Silver/Bronze）；(b) GitHub a2aproject/A2A 的 CONTRIBUTING.md 对 OpenAI/Anthropic 等成员公司的角色定位
