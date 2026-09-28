# r2-agntcy-acp
question: Cisco（Outshift）发起、据称现由 Linux Foundation 托管的 AGNTCY 项目里，是否真的存在一个官方命名为 "Agent Connect Protocol"、缩写同样是 "ACP" 的组件？请在 AGNTCY 官方站点/文档/GitHub 找一手来源确认：（1）全称是否官方自称包含 "ACP" 这个缩写；（2）它标准化的是什么（连接对象是谁和谁）；（3）现在是否还在维护、最新版本/日期是什么；（4）和 IBM 的 Agent Communication Protocol、Zed 的 Agent Client Protocol 是否有任何关系、是否曾造成命名混淆的官方或社区讨论。
checked: https://github.com/agntcy/acp-spec,https://github.com/agntcy/acp-sdk,https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos,https://outshift.cisco.com/blog/ai-ml/mcp-acp-decoding-language-of-models-and-agents,https://www.boldare.com/blog/agent-communication-protocol-acp-explained-what-it-is-and-why-it-matters/,https://dev.to/kanywst/mapping-mcp-a2a-and-acp-telling-ai-agent-protocols-apart-in-2026-1hha,https://agntcy.org/

## claims
- [C1] AGNTCY 官方确实存在名为"Agent Connect Protocol"、缩写为"ACP"的组件 | src: https://github.com/agntcy/acp-spec | quote: "Agent Connect Protocol Specification" | type: official
- [C2] ACP 定义为"通过 API 调用和配置远程代理的标准接口" | src: https://github.com/agntcy/acp-spec | quote: "a standard interface to invoke and configure remote agents over an API" | type: official
- [C3] ACP 基于 OpenAPI REST 模式规范 | src: https://github.com/agntcy/acp-spec | quote: "specified in OpenAPI, a REST-based schema specification" | type: official
- [C4] ACP 于 2026 年 4 月 11 日被存档，标记为已废弃 | src: https://github.com/agntcy/acp-spec | quote: "This repository was archived on April 11, 2026 and is now read-only" | type: official
- [C5] ACP SDK 也于 2026 年 4 月 11 日被存档 | src: https://github.com/agntcy/acp-sdk | quote: "This repository was archived by the owner on Apr 11, 2026. It is now read-only" | type: official
- [C6] AGNTCY 已弃用 ACP 以支持 A2A 作为代理调用的标准 | src: https://www.boldare.com/blog/agent-communication-protocol-acp-explained-what-it-is-and-why-it-matters/ | quote: "AGNTCY deprecated Agent Connect Protocol in favor of A2A for agent invocation" | type: secondary
- [C7] Linux Foundation 官方公告未明确列出 ACP 为 AGNTCY 核心组件，仅列出：Agent Discovery、Agent Identity、Agent Messaging (SLIM)、Agent Observability | src: https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos | quote: "four foundational infrastructure elements" list omits ACP | type: official
- [C8] Cisco Outshift 官方博文提及 ACP 为"AGNTCY 架构的核心组件" | src: https://outshift.cisco.com/blog/ai-ml/mcp-acp-decoding-language-of-models-and-agents | quote: "Agent Connect Protocol is one of the core components of the AGNTCY architecture" | type: official
- [C9] 存在至少三个不同的官方"ACP"协议：IBM Agent Communication Protocol（已并入 A2A，2025 年 8 月）、Zed Agent Client Protocol（2025 年 8 月）、AGNTCY Agent Connect Protocol | src: https://www.boldare.com/blog/agent-communication-protocol-acp-explained-what-it-is-and-why-it-matters/ | quote: "Three Different Protocols Share the ACP Acronym" | type: secondary
- [C10] IBM ACP 已在 2025 年 8 月合并入 A2A 标准 | src: https://dev.to/kanywst/mapping-mcp-a2a-and-acp-telling-ai-agent-protocols-apart-in-2026-1hha | quote: "IBM-led Agent Communication Protocol merged into the broader A2A standard in August 2025" | type: secondary
- [C11] Zed Agent Client Protocol 于 2025 年 8 月发布，用于编辑器-代理通信 | src: https://www.boldare.com/blog/agent-communication-protocol-acp-explained-what-it-is-and-why-it-matters/ | quote: "Zed's Agent Client Protocol...addresses how code editors talk to coding agents" | type: secondary
- [C12] AGNTCY 官方 GitHub 组织维护多个 ACP 相关仓库（acp-spec、acp-sdk、workflow-srv 等） | src: https://github.com/agntcy | quote: "agntcy organization" hosts multiple ACP-related repositories | type: official
- [C13] OASF 活跃模式现将 ACP 相关字段标记为已废弃，明确推荐 A2A | src: https://www.boldare.com/blog/agent-communication-protocol-acp-explained-what-it-is-and-why-it-matters/ | quote: "live OASF schema marks ACP-related fields as deprecated and explicitly recommends A2A" | type: secondary
- [C14] AGNTCY 是独立于 ACP 的基础设施项目，涵盖代理发现、身份、消息传递和可观测性 | src: https://www.boldare.com/blog/agent-communication-protocol-acp-explained-what-it-is-and-why-it-matters/ | quote: "AGNTCY handles agent discovery, identity, messaging, and observability" | type: secondary
- [C15] Cisco 于 2025 年 3 月开源 AGNTCY，于 2025 年 7 月 29 日捐赠给 Linux Foundation | src: https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos | quote: "open-sourced by Cisco in March 2025 and officially welcomed to the Linux Foundation on July 29, 2025" | type: official

## conflicts
- Outshift 官方博客描述 ACP 为"AGNTCY 架构的核心组件"（C8），但 Linux Foundation 官方公告的"四个基础基础设施元素"列表（C7）中未提及 ACP，仅列出 Discovery、Identity、Messaging (SLIM)、Observability。在 ACP 于 2026 年 4 月 11 日被弃用前，ACP 的官方地位似乎模糊。

## gaps
- 无法从一手来源获得 ACP 规范的具体版本号（仅知道被存档日期为 2026-04-11）
- docs.agntcy.org/syntactic/connect/ 返回 404，无法获取官方文档页面中的 ACP 定义
- 无法从一手来源确认是否有官方或 AGNTCY 团队的公告明确讨论 ACP 与 IBM ACP、Zed ACP 的命名混淆问题
- Outshift 关于"MCP and ACP"的官方博文内容不完整，无法获取其中关于不同 ACP 的完整讨论

## leads
- Medium 文章"ACP Is Not One Protocol: A Chronological Guide to Four Different ACPs"（2026 年 8 月）是目前最完整的关于多个 ACP 混淆的官方或高信度讨论，但因 403 禁止访问无法验证具体内容
- OASF（Open Agent Schema Framework）官方文档可能包含 ACP 弃用和 A2A 迁移的详细说明，值得在后续调研中查阅
- Zylos Research 的"Agent Interoperability Protocols 2026"研究可能有更详细的历史和技术对比信息
