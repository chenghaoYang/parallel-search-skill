# r2-openai
question: OpenAI 对 A2A、ACP-Zed（Zed 的 Agent Client Protocol）、AG-UI 三者各自有没有官方立场（哪怕是"评估中"或完全没提）？OpenAI 的 AGENTS.md 准确定位是什么——它是不是一个"协议"，还是纯粹的文件约定（类似给 agent 看的 README 规范）？它和 MCP 有没有关系？
checked: https://raw.githubusercontent.com/openai/openai-agents-python/main/AGENTS.md, https://raw.githubusercontent.com/openai/openai-agents-python/main/README.md, https://raw.githubusercontent.com/openai/openai-agents-python/main/docs/mcp.md, https://learn.chatgpt.com, https://github.com/openai/openai-agents-python, https://developers.openai.com/api/docs/agents

## claims
- [C1] AGENTS.md 是 openai-agents-python 仓库的贡献者指南，包含强制性规则、代码审查规则、项目结构指南和操作指南，而非协议规范 | src: https://raw.githubusercontent.com/openai/openai-agents-python/main/AGENTS.md | quote: "Contributor Guide" (目录标题) | type: official
- [C2] AGENTS.md 的定位是文件约定/贡献者规范，包括安全检查清单、必须的技能使用、工作状态报告等指导 | src: https://raw.githubusercontent.com/openai/openai-agents-python/main/AGENTS.md | quote: "Policies & Mandatory Rules / Code Review Rules / Project Structure Guide / Operation Guide" | type: official
- [C3] OpenAI Agents SDK 官方文档明确支持 MCP（Model Context Protocol），并提供详细的集成指南 | src: https://raw.githubusercontent.com/openai/openai-agents-python/main/docs/mcp.md | quote: "MCP standardises how applications expose tools and context to language models" | type: official
- [C4] OpenAI 官方文档中未提及 A2A（Agent-to-Agent Protocol）| src: https://raw.githubusercontent.com/openai/openai-agents-python/main/README.md | quote: (README 未出现"A2A") | type: official
- [C5] OpenAI 官方文档中未提及 ACP-Zed（Zed Agent Client Protocol）| src: https://raw.githubusercontent.com/openai-agents-python/main/docs/mcp.md | quote: (MCP 文档未出现"ACP-Zed") | type: official
- [C6] OpenAI 官方文档中未提及 AG-UI | src: https://raw.githubusercontent.com/openai/openai-agents-python/main/README.md | quote: (README 未出现"AG-UI") | type: official
- [C7] OpenAI Agents 支持的多代理模式为"Agents as tools"和"Handoffs"，这是 OpenAI 自有的编排模式，不基于 A2A、ACP-Zed 或 AG-UI | src: https://raw.githubusercontent.com/openai/openai-agents-python/main/docs/multi_agent.md | quote: "two orchestration patterns: Agents as tools / Handoffs" | type: official
- [C8] AGENTS.md 与 MCP 无直接关系——AGENTS.md 是贡献者指南，MCP 是 OpenAI Agents SDK 支持的一个工具/上下文协议 | src: https://raw.githubusercontent.com/openai/openai-agents-python/main/AGENTS.md (贡献者指南) 和 https://raw.githubusercontent.com/openai/openai-agents-python/main/docs/mcp.md (MCP 集成文档) | quote: N/A (两份文件各自独立) | type: official
- [C9] learn.chatgpt.com 官方文档中未提及 A2A、ACP-Zed、AG-UI 等协议 | src: https://learn.chatgpt.com | quote: (検索结果:"does **not** mention A2A, ACP-Zed, AG-UI") | type: official

## conflicts
无

## gaps
- OpenAI 是否在任何内部设计评审或产品规划中考虑过 A2A/ACP-Zed/AG-UI（即使未公开）
- OpenAI 对 A2A/ACP-Zed/AG-UI 的明确拒绝或"评估中"的官方陈述（目前未找到任何肯定或否定的表态）

## leads
- OpenAI 的多代理模式采用自有的 handoff 和 agents-as-tools 设计，表明 OpenAI 在代理编排上走的是独立路线，未采纳或参考 A2A/ACP 等第三方协议
- AGENTS.md 的真实性质（贡献者指南而非协议）需在最终文档中明确，以澄清"OpenAI 自家变体"行的"AGENTS.md"格子并非协议定义
