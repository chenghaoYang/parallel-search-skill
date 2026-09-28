# r2-governance
question: MCP 和 A2A 的治理归属关系到底是什么、时间线如何，需要核实一处疑似冲突。
checked: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation, https://modelcontextprotocol.io/community/governance, https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation, https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation, https://aaif.io/about

## claims
- [C1] Anthropic 官方公告《Donating the Model Context Protocol and Establishing of the Agentic AI Foundation》发布于 2025 年 12 月 9 日（非 2025 年 3 月）| src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "[article published 2025-12-09]" | type: official
- [C2] MCP 在 2024 年 11 月由 Anthropic 开源 | src: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | quote: "MCP was open sourced by Anthropic in November 2024" | type: official
- [C3] Agentic AI Foundation (AAIF) 由 Linux Foundation 在 2025 年 12 月 9 日宣布成立，是 Linux Foundation 旗下的一个有向基金 | src: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | quote: "Linux Foundation Announces the Formation of the Agentic AI Foundation (AAIF)" | type: official
- [C4] AAIF 的创始成员包括 Anthropic（MCP）、Block（goose）、OpenAI（AGENTS.md），支持机构包括 Google、Microsoft、AWS、Cloudflare、Bloomberg | src: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | quote: "Founded by Anthropic, Block, and OpenAI, supported by Google, Microsoft, AWS, Cloudflare, and Bloomberg" | type: official
- [C5] MCP 作为创始项目与 AAIF 一起在 2025 年 12 月 9 日成立，通过 Anthropic 对 Linux Foundation 的捐赠 | src: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | quote: "Donating MCP to the Linux Foundation as part of the AAIF ensures it stays open, neutral, and community-driven" | type: official
- [C6] MCP 的组织法人形式是 "Model Context Protocol a Series of LF Projects, LLC" | src: https://modelcontextprotocol.io/community/governance | quote: "Model Context Protocol has been established as Model Context Protocol a Series of LF Projects, LLC" | type: official
- [C7] A2A 于 2026 年 8 月 27 日加入 AAIF，成为增长阶段项目（非创始项目） | src: https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/ | quote: "A2A joined the Agentic AI Foundation (AAIF) on August 27, 2026, as a Growth Stage project" | type: official
- [C8] AAIF 由 Linux Foundation 主办，为开放代理栈的多个协议（MCP、goose、AGENTS.md、A2A 等）提供中立治理框架 | src: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | quote: "Linux Foundation provides neutral, open governance" | type: official

## conflicts
- [CONFLICT-1] r1-scout-vendors.md [C3] 声称 Anthropic "在 2025 年 3 月" 捐赠 MCP 给 AAIF，但官方公告发布于 2025 年 12 月 9 日，AAIF 也是在这一天成立。MCP 是在 AAIF 成立时作为创始项目被纳入，而非提前 9 个月捐赠。
- [CONFLICT-2] r1-mcp.md [C19] 说 MCP 治理页自称只是 "LF Projects, LLC" 而 "没有直接提 AAIF"，但根据 2025 年 12 月 9 日的 Anthropic 官方公告，MCP 现已明确成为 AAIF 开放代理栈的创始项目。治理页的 "LF Projects, LLC" 表述是正确的，但这是 AAIF 的组织框架中的具体法人形式，并非排斥 AAIF 的关系。

## gaps
- 无法从当前检查的源获得 MCP 治理页面的最后更新日期，无法确认其是否已反映 2025 年 12 月 9 日 AAIF 成立后的最新信息或仍为旧版内容。

## leads
- 建议核实 modelcontextprotocol.io 治理页是否已更新以明确提及 AAIF 的创始成员身份（可能需要对比页面历史版本）。
