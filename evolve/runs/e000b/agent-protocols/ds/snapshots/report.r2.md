# Agent 时代的协议全景：MCP / A2A / ACP(×2) / AG-UI

> 回答这几种「协议」各管什么、怎么选、两个 ACP 是不是一回事、MCP 的 SSE 是否已废弃。截至 2026-09-24；事实带 [n] 指向文末一手来源；❓=待核实。

## 0. 一屏看懂

- **四层协议，可以叠加用，不是四选一**：agent↔工具/数据用 **MCP**；agent↔agent（跨厂商任务委派）用 **A2A**；agent↔终端用户 UI 用 **AG-UI**；编辑器/IDE↔agent 子进程用 **ACP（Zed 版）**[1][2]。
- **两个 ACP 纯属撞名，不是一回事**：IBM 的 Agent Communication Protocol（agent 对 agent）已于 2025-08-27 归档、并入 A2A [8]；Zed 的 Agent Client Protocol（编辑器对 agent 子进程）活跃开发中，v1.9.1（2026-09-18）[10][13]。两边官方文档互不提及。
- **MCP 的 SSE 确实被替换了**：2025-03-26 版用 **Streamable HTTP** 替换 2024-11-05 版的独立 "HTTP+SSE" transport（标记 deprecated，仅保留向后兼容）；现行 2026-07-28 版标准传输只剩 stdio / Streamable HTTP，SSE 变成后者内部可选的流式手段 [1]。
- **治理有重大更新**：MCP 和 A2A 现在**同属**Linux Foundation 旗下的 **Agentic AI Foundation（AAIF，一个"directed fund"）**——MCP 是 2025-12-09 的三个创始项目之一，A2A 则在此前独立挂牌 Linux Foundation 近一年后，于 2026-08-27 才作为"成长期项目"并入 AAIF [28][29][30]。ACP-Zed 由 Zed+JetBrains 联合治理、计划移交独立基金会（不是 AAIF）[11]；AG-UI 由 CopilotKit 主导，MIT 协议，未加入任何基金会 [17]。
- **鉴权各管各的**：MCP 建议 HTTP 传输走 OAuth2.1+Bearer（stdio 走环境变量，整体可选）[2]；A2A 写进 Agent Card 的 securitySchemes（对齐 OpenAPI）[4]；ACP-Zed 用初始化握手 authMethods [12]；AG-UI 不定义自有鉴权，靠底层传输 [18]。
- **大厂支持不对称**：Microsoft、Google 四项（MCP/A2A/ACP-Zed/AG-UI）基本全线支持；OpenAI 只官方确认 MCP，专门查证过未提及其余三个；Anthropic 创立 MCP，但 A2A/ACP-Zed/AG-UI 都缺 Anthropic 自己的一手确认——现有的"支持"多是对方（Zed、AG-UI 社区）单方面公告，或一场联合 webinar，不是 Anthropic 官方声明 [14][21]。
- **没有厂商发布"第五个独立协议"**，但 Google 的 **A2UI**（声明式 agent-UI 规范，和 AG-UI 互补而非竞争）是最接近的"自家变体"；Microsoft 的 **NLWeb** 不是新协议，是搭建在 MCP 之上的网站自然语言接口工具包 [23][27]。

## 1. Taxonomy

分类轴：协议连接的两端是谁。

| 族 | 连接两端 | 成员 |
|---|---|---|
| 工具/上下文面 | agent ↔ 工具、数据源 | MCP |
| Agent 对等面 | agent ↔ 另一个 agent（跨组织任务委派）| A2A、ACP-IBM（已并入 A2A）|
| 宿主应用面 | agent ↔ 承载它的宿主/前端 | AG-UI（终端用户 UI）、ACP-Zed（编辑器宿主，类比 LSP）|

维度：定位层｜传输｜鉴权｜治理｜版本（下节按此排列；大厂支持另列一表）。

## 2. 对照矩阵

### 协议本身
| 协议 | 定位层 | 传输 | 鉴权 | 治理 | 版本 |
|---|---|---|---|---|---|
| MCP | agent↔工具/数据 [3] | JSON-RPC2.0；stdio/Streamable HTTP（原 HTTP+SSE 已废弃）[1] | HTTP 建议 OAuth2.1+Bearer；stdio 用环境变量；整体可选 [2] | AAIF（LF 旗下 directed fund），2025-12-09 创始项目 [28][29] | 2026-07-28（stable）[1] |
| A2A | agent↔agent [7] | JSON-RPC2.0 over HTTP(S)，SSE 流式+webhook 异步 [4] | Agent Card.securitySchemes：apiKey/oauth2/OIDC/mTLS [4] | LF 独立项目（2025-06-23）→ 2026-08-27 并入 AAIF；8 公司指导委员会 [5][6][30] | v1.0.0（2026-03-12，生产就绪）[6] |
| ACP-IBM（已并入 A2A）| agent↔agent [9] | REST/JSON-RPC over HTTP、WebSocket [9] | capability token+OAuth2（二手）[9] | 曾属 LF AI & Data，2025-08 并入 A2A [8] | 未给版本号；仓库 2025-08-27 归档只读 [8] |
| ACP-Zed | 编辑器↔agent 子进程 [10] | 本地 stdio；远程 HTTP/WebSocket（开发中）[10] | 初始化握手 authMethods [12] | Zed+JetBrains 联合，计划移交独立基金会 [11] | 协议版本 1；v1.9.1（2026-09-18）[13] |
| AG-UI | agent 后端↔终端用户 UI [15] | 传输无关：SSE/WebSocket/webhook [16] | 不定义自有鉴权；依赖实现（Bearer/API key/SigV4）[18] | CopilotKit 主导，MIT [17] | 1.0.0（2026-09-17，此前 0.1.x）[17] |

### 大厂支持矩阵
✅ 官方一手确认｜⚠ 间接（适配器/单方面/无正式声明）｜❓ 已查证官方渠道、未见表态

| 厂商 | MCP | A2A | ACP-Zed | AG-UI | 自家变体 |
|---|---|---|---|---|---|
| OpenAI | ✅ ChatGPT/Agents SDK [19] | ❓ [19] | ❓ [19] | ❓ [19] | AGENTS.md：仓库级"给 agent 看"的说明文件约定，非网络协议，AAIF 创始项目之一 [28] |
| Anthropic | ✅ 发起方 [20] | ⚠ 仅与 Google Cloud 联合 webinar 展示 MCP+A2A 共存，无正式采用声明 [21] | ⚠ Zed 自建适配器包住 Claude Code SDK，非 Anthropic 原生实现 [14] | ⚠ 仅 AG-UI 一侧集成页+社区 issue，Anthropic 未确认 [15] | 无 |
| Google | ✅ ADK 支持 [15] | ✅ 发起方 [22] | ✅ 官方确认：Gemini CLI 原生 `--acp`，Google 主动接洽 Zed [24] | ✅ ADK 支持 [15] | A2UI：独立声明式 UI 协议，Apache2.0，v0.9.1 生产/v1.0 RC，AG-UI 只是它可选传输之一 [23] |
| Microsoft | ✅ Build2025 广泛支持+Copilot Studio GA [25] | ✅ Agent Framework 原生，含跨 .NET/Python [25] | ⚠ VS Code 讨论中；Copilot CLI 文档称 public preview，但有未实现的冲突 issue [26] | ✅ Agent Framework 原生 [25] | NLWeb：网站自然语言接口工具包，每个实例本身即 MCP server，非独立协议 [27] |

## 3. 变体与适配层：两个 ACP 到底差在哪

| | ACP-IBM | ACP-Zed |
|---|---|---|
| 连的是谁 | agent↔agent，同 A2A 一层 | 编辑器/IDE↔agent 子进程 |
| 现状 | 2025-08 归档，团队并入 A2A | 活跃开发，v1.9.1（2026-09-18）|
| 传输 | REST/JSON-RPC over HTTP、WS | 本地 stdio；远程 HTTP/WS 开发中 |

两边官方文档都未提及对方，纯属命名巧合；用户提问时点上 IBM 版已停止独立存在超一年 [8][10]。

## 4. 用户需要知道的坑

- **把"MCP 和 A2A 互补"读成"可互相替代"**：官方定位纵向（MCP，agent→工具）vs 横向（A2A，agent→agent），是叠加关系 [7]。
- **以为 SSE 被整体弃用**：MCP 只是不再把 SSE 当独立 transport，Streamable HTTP 内部仍可选用 SSE 推流，能力还在 [1]。
- **搜"ACP"时把 IBM 和 Zed 的混为一谈**：注意时间线，IBM 版 2025-08 已死，此后"ACP"在社区语境里基本特指 Zed 版 [8][13]。
- **把"Claude Code 支持 ACP"当成 Anthropic 原生实现**：实际是 Zed 建的适配器包住 Claude Code SDK 做协议转换，不是 Anthropic 自己讲 ACP [14]。
- **把 GitHub Copilot CLI 的 ACP 支持当成确定可用**：官方文档称 public preview，但同时存在一个未实现的相关 issue，接入前建议实测 [26]。
- **把 A2UI 当 AG-UI 的别名**：A2UI 是 Google 独立协议（自己的事件格式和 spec），AG-UI 只是它众多可选传输之一，不是同一个东西 [23]。

## 5. 未决与置信度

- A2UI 完整 HTTP endpoint 规范细节未能从 GitHub 一手抓取核实（返回 404）[23]。
- VS Code、GitHub Copilot Chat 对 ACP-Zed 的最终支持时间表未定，均处于讨论/预览阶段 [26]。
- Anthropic 对 A2A 没有正式采用声明；联合 webinar 只说明技术上可共存，不构成协议承诺 [21]。
- ACP-IBM 的鉴权细节（capability token、K8s RBAC）仅二手来源（workos.com 博客）[9]。
- AGNTCY（Cisco 主导，Linux Foundation，65+ 公司）是 agent 发现/身份/消息基础设施层，与本文协议互补不竞争，因篇幅未展开 [31]。

## 来源
[1] MCP transports 2024-11-05/2025-03-26/2026-07-28 — https://modelcontextprotocol.io/specification/2024-11-05/basic/transports ; https://modelcontextprotocol.io/specification/2025-03-26/basic/transports ; https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
[2] MCP authorization（现行版）— https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
[3] MCP 治理与定位 — https://github.com/modelcontextprotocol ; https://modelcontextprotocol.io
[4] A2A 规范 — https://a2a-protocol.org/latest/specification/
[5] A2A → Linux Foundation（2025-06-23）— https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents
[6] A2A v1.0（2026-03-12）— https://a2a-protocol.org/latest/blog/2026/03/12/a2a-protocol-ships-v10-production-ready-standard-for-agent-to-agent-communication/
[7] A2A 与 MCP 关系 — https://a2a-protocol.org/latest/topics/a2a-and-mcp/
[8] ACP-IBM 并入 A2A 公告+仓库归档 — https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ ; https://github.com/i-am-bee/acp
[9] ACP-IBM 概览 — https://www.ibm.com/think/topics/agent-communication-protocol
[10] ACP-Zed 简介与传输 — https://agentclientprotocol.com/get-started/introduction
[11] ACP-Zed 治理 — https://agentclientprotocol.com/community/governance
[12] ACP-Zed 鉴权 — https://agentclientprotocol.com/protocol/v2/authentication
[13] ACP-Zed 采用者与版本 — https://zed.dev/acp
[14] Claude Code 经 ACP 接入 Zed（适配器说明）— https://zed.dev/blog/claude-code-via-acp
[15] AG-UI 首页/协议关系/集成页 — https://docs.ag-ui.com ; https://docs.ag-ui.com/agentic-protocols ; https://docs.ag-ui.com/integrations
[16] AG-UI 架构/传输/事件 — https://docs.ag-ui.com/concepts/architecture
[17] AG-UI GitHub — https://github.com/ag-ui-protocol/ag-ui
[18] AG-UI AWS Bedrock 实现（鉴权）— https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-agui-protocol-contract.html
[19] OpenAI 官方文档（MCP 支持+未提及 A2A/ACP-Zed/AG-UI）— https://raw.githubusercontent.com/openai/openai-agents-python/main/docs/mcp.md ; https://raw.githubusercontent.com/openai/openai-agents-python/main/README.md ; https://learn.chatgpt.com
[20] Anthropic MCP 起源 — https://www.anthropic.com/news/model-context-protocol
[21] Anthropic×Google Cloud webinar（MCP+A2A on Vertex AI）— https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai
[22] Google A2A 发起 — https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
[23] Google A2UI（发布公告+spec+v0.9 博客）— https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/ ; https://a2ui.org/ ; https://github.com/google/A2UI
[24] Google×Zed（Gemini CLI 集成公告）— https://developers.googleblog.com/gemini-cli-is-now-integrated-into-zed/
[25] Microsoft MCP/A2A/AG-UI 支持 — https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/ ; https://blogs.microsoft.com/blog/2025/05/19/microsoft-build-2025-the-age-of-ai-agents-and-building-the-open-agentic-web/ ; https://www.microsoft.com/en-us/copilot/blog/copilot-studio/model-context-protocol-mcp-is-now-generally-available-in-microsoft-copilot-studio/
[26] Microsoft ACP-Zed 现状 — https://docs.github.com/en/copilot/reference/copilot-cli-reference/acp-server ; https://github.com/github/copilot-cli/issues/222 ; https://github.com/microsoft/vscode/issues/265496
[27] NLWeb（构建于 MCP 之上）— https://news.microsoft.com/source/features/company-news/introducing-nlweb-bringing-conversational-interfaces-directly-to-the-web/
[28] AAIF 成立公告（2025-12-09，三创始项目）— https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
[29] AAIF=LF 旗下 directed fund；MCP 治理模式不变 — https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
[30] A2A 加入 AAIF（2026-08-27，成长期项目）— https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/
[31] AGNTCY — https://agntcy.org/
