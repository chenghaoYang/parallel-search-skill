# r3-agntcy-status
question: AGNTCY 项目里，"Agent Connect Protocol (ACP)" 现在的官方地位到底是什么？ACP 被弃用是否有官方公告说明原因（例如"让位于 A2A"）？ACP 弃用后，AGNTCY 现在推荐用什么协议做 agent 间调用？请找到能直接支撑或推翻"AGNTCY deprecated ACP in favor of A2A"这句话的一手来源原句。
checked: https://github.com/agntcy/acp-spec,https://github.com/agntcy/acp-sdk,https://github.com/agntcy/.github/blob/main/profile/README.md,https://agntcy.org,https://docs.agntcy.org,https://raw.githubusercontent.com/agntcy/slim/main/README.md,https://slim.agntcy.org/latest/slim/slim-overview/,https://github.com/agntcy/acp-spec/issues/48,https://agntcy.github.io/csit/a2a-slimrpc/

## claims
- [C1] 官方 acp-spec 仓库已 archived: true，于 2026-04-11 | src: https://api.github.com/repos/agntcy/acp-spec | quote: "archived": true | type: official
- [C2] 官方 acp-sdk 仓库已 archived: true，于 2026-04-11 | src: https://api.github.com/repos/agntcy/acp-sdk | quote: "archived": true | type: official
- [C3] SLIM 是 A2A 的传输层："SLIM (Secure Low-Latency Interactive Messaging) is a next-generation communication framework that provides the secure, scalable transport layer for AI agent protocols like A2A (Agent-to-Agent)" | src: https://raw.githubusercontent.com/agntcy/slim/main/README.md | quote: "provides the secure, scalable transport layer for AI agent protocols like A2A (Agent-to-Agent)" | type: official
- [C4] AGNTCY 官方 GitHub 组织 profile README 不再提及 ACP，仅列举 SLIM、Identity、Agent Directory 等组件 | src: https://github.com/agntcy/.github/blob/main/profile/README.md | quote: "For more information, see the [AGNTCY documentation](https://docs.agntcy.org/), where you can find component-level getting started guides, such as [SLIM](https://docs.agntcy.org/messaging/slim-howto), [Identity](https://docs.agntcy.org/identity/identity-quickstart/), and [Agent Directory]" | type: official
- [C5] AGNTCY docs.agntcy.org 列出七大核心组件不包括 ACP：Agent Directory、SLIM、OASF、Identity、SHADI、Observability、CSIT | src: https://docs.agntcy.org | quote: "Seven main components... Agent Directory Service, SLIM, Open Agent Schema Framework (OASF), Identity, SHADI, Observability and Evaluation, CSIT" | type: official
- [C6] GitHub issue #48 (用户报告，非官方公告)：acp-spec 应被弃用，因为 AGNTCY 现已支持 A2A，时间 2026-03-27 | src: https://github.com/agntcy/acp-spec/issues/48 | quote: "This repository should be deprecated since AGNTCY now supports A2A" | type: secondary
- [C7] A2A over SLIMRPC 互操作性仪表板存在于 agntcy.github.io/csit/a2a-slimrpc/，显示 A2A 现已在 SLIMRPC 上实现 | src: https://agntcy.github.io/csit/a2a-slimrpc/ | quote: "A2A over SLIMRPC Interop Dashboard" | type: official

## conflicts
- Cisco Outshift 博客（2025年）称 ACP 是"AGNTCY 架构的核心组件"，但 AGNTCY 官方 docs.agntcy.org 与 profile README 已不列 ACP 为任何组件，改为 SLIM

## gaps
- 找不到 AGNTCY 官方的正式公告或 changelog，明确说明 ACP 被弃用的原因（例如"让位于 A2A"）
- 找不到官方博客文章或新闻稿解释这一过渡
- acp-spec CHANGELOG.md 无实质内容
- 官方 GitHub discussions 或公告中未见过正式的弃用声明

## leads
- GitHub issue #48 是唯一找到的"AGNTCY now supports A2A"关联引用，但这是用户报告，不是官方声明
- SLIM README 的官方表述"transport layer for...A2A (Agent-to-Agent)"是目前最直接的官方确认 A2A 为推荐协议的来源
- 无法找到"deprecated in favor of A2A"的一手官方原句支撑
