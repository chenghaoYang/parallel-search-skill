# Agent 时代协议全景：MCP / A2A / ACP / AG-UI 怎么分工、怎么选

> 截至 2026-09-24。这些协议各管什么、有何不同、大厂支持谁、有哪些坑。[n] 见文末来源。

## 0. 一屏看懂

1. **不是一套协议，是四类不同问题**：MCP 管"模型怎么用工具/数据"；A2A 管"agent 怎么找到并委托另一个 agent"；ACP-Zed 管"编辑器怎么驱动本地 agent 子进程"；AG-UI 管"agent 怎么把过程/状态实时推给用户界面"。四者官方都自称互补、可叠加，不是竞争关系 [6][23]。
2. **"ACP" 撞名至少 3 次，互不相关**：IBM 的 Agent Communication Protocol（agent↔agent，2025-08-27 停止独立开发并入 A2A）；Zed 的 Agent Client Protocol（编辑器↔agent，仍活跃）；OpenAI+Stripe 的 Agentic Commerce Protocol（电商支付，2025-09-29 发布）。**结论：不是一回事**，规范互不提及、互不兼容 [10][11][14][33]。
3. **MCP 的 SSE 没有被"移除"**：2025-03-26 版把独立的 "HTTP+SSE" 传输标记 Deprecated，代替方案是 Streamable HTTP；但 SSE 作为 Streamable HTTP 内部的可选流式方式被保留。**结论：是迁移，不是砍掉** [2]。
4. **治理正收敛到同一个伞下**：MCP（2025-12-09 作为创始项目并入新设立的 Agentic AI Foundation/AAIF）、A2A（2025-06 捐给 Linux Foundation→2026-08-27 加入 AAIF）、已停用的 ACP-IBM（2025-08 并入 A2A）最终都落在 Linux Foundation/AAIF 之下。AG-UI（CopilotKit 独家）和 ACP-Zed（Zed+JetBrains 双 BDFL）是例外，没有捐给中立基金会 [4][9][10][25][26]。
5. **MCP 是唯一被四家都官方支持的协议**：A2A 有 Google/Microsoft 产品级支持，Anthropic 只到教育材料级别 [35]；AG-UI 无大厂官方采用声明。
6. **ACP-Zed "采用者列表"要看穿**：列表里的 Claude Code、Codex CLI 是 **Zed 写的桥接适配器**，非 Anthropic/OpenAI 原生；唯一确认厂商原生实现是 Google Gemini CLI [16][18][19]。
7. **鉴权都不强制**：MCP 推荐 OAuth，A2A 列 5 种可选方案，ACP-Zed 靠 agent 自己的 `authenticate`，AG-UI 靠实现方自定——没有协议规定"必须用 X"。
8. **MCP 2026-07-28 版从有状态改无状态**：旧版(≤2025-11-25)要求 stateful initialize 握手，现在请求自包含信息，照旧教程写的人会踩坑 [1]。

## 1. Taxonomy

**分类轴：协议连接的是交互栈里的哪一段？** 这条轴解释了矩阵里大多数技术差异——连"进程内子系统"用本地传输，连"独立服务"用网络传输+鉴权，连"UI"用事件流。

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| 模型↔工具/数据 | **MCP** | 唯一管"给模型接工具/数据源"的协议 |
| agent↔agent | **A2A**（历史上还有已并入的 ACP-IBM） | "发现能力→委托任务→取回结果"的对等/近对等协作 |
| client 应用↔本地 agent 子进程 | **ACP-Zed** | 唯一管"宿主应用驱动本地 agent 子进程"，类比 LSP [14] |
| agent↔终端用户界面 | **AG-UI** | 唯一管"把 agent 执行过程实时展示给用户" |

**次轴：治理谱系**（单厂商 → 中立基金会）：CopilotKit 独家(AG-UI) < Zed+JetBrains 双 BDFL(ACP-Zed) < Linux Foundation/AAIF(MCP、A2A)。

**维度**（下表按此排列）：管什么/拓扑/传输/格式/鉴权/状态/版本/治理/关系。

## 2. 对照矩阵

| | MCP | A2A | ACP-IBM（已停用） | ACP-Zed | AG-UI |
|---|---|---|---|---|---|
| **管什么** | 模型↔工具/资源/提示词 [1] | agent 间任务委托协作 [6] | 曾是 agent↔agent 通信 [12] | 编辑器↔本地 agent 子进程 [14] | agent 后端↔用户前端 [21] |
| **拓扑** | Host—Client(1:1)—Server [1] | Client→Server(Remote Agent)，非对等 [6] | client↔单agent 或多 agent server，双向 [12] | Client=编辑器，Server=agent子进程 [14] | Producer(agent)发事件流→Consumer(UI) [21] |
| **传输** | 本地 stdio；远程 Streamable HTTP(含可选SSE) [1] | JSON-RPC2.0(HTTP)/gRPC/HTTP+REST 三选一 [6] | HTTP+REST，"like HTTP" [12] | 本地 JSON-RPC2.0 over stdio；远程HTTP/WS(开发中) [14] | 主HTTP POST+SSE；也支持WebSocket/二进制 [23] |
| **格式** | JSON-RPC 2.0 [3] | JSON / Protobuf(gRPC) [6] | MIME multipart [12] | JSON-RPC 2.0 [14] | 30种类型化JSON事件 [21] |
| **鉴权** | HTTP传输推荐OAuth；bearer/APIkey [1] | APIKey/OAuth2/OIDC/mTLS可选 [6] | bearer/basic/JWT，可选mTLS（二手）| 无强制；可选`authenticate`方法 [17] | CORS+token+审计日志，实现方自定 [23] |
| **状态** | 2026-07-28起无状态；此前版本有状态握手 [1] | Server管理Task，7态枚举 [6] | 声称"stateless by design" [12] | 编辑器持有session+"危险能力" [17] | agent发SNAPSHOT/DELTA(RFC6902)同步 [21] |
| **版本** | 日期式，最新2026-07-28 [1] | semver，v1.0.1(2026-05-28) [6][7] | semver，终版v1.0.3(2025-08-21) [11] | 稳定版v1，握手期协商 [14] | semver+日期，1.0.0(2026-09-17) [21] |
| **治理** | LF("...a Series of LF Projects")，2025-12-09并入AAIF创始 [4][25] | 2025-06捐LF→2026-08-27加入AAIF(成长期) [8][9] | 2025-03 IBM发布→2025-08-27归档并入A2A TSC [10][11] | Zed+JetBrains双BDFL，Apache2.0 [15] | CopilotKit独家，未捐基金会(2026-09仍如此) [22][24] |
| **关系** | 官方文档未提A2A/ACP/AG-UI [1] | Appendix B明说与MCP互补 [6] | 支持"MCP extension"调工具 [12] | 类比LSP；"MCP连工具,ACP连编辑器" [14] | 官方原句:"MCP=agent-to-tool, A2A=multi-agent, AG-UI=human-in-loop presentation tier...non-conflicting and stackable" [23] |

## 3. 变体与适配层

### 3.1 三个 "ACP" 消歧

| | Agent Communication Protocol (IBM) | Agent Client Protocol (Zed) | Agentic Commerce Protocol (OpenAI) |
|---|---|---|---|
| 管什么 | agent↔agent | 编辑器↔agent | 买家 agent↔商户结账支付 |
| 现状 | 2025-08-27 归档，并入 A2A [11] | 活跃开发，v1 [14] | 活跃，最新2026-04-17 [33] |
| 治理 | 原IBM Research，现属A2A TSC | Zed+JetBrains | OpenAI+Stripe联合，Apache2.0 [33][34] |

三者只是缩写撞车，规范互不提及、互不兼容，**不能混用**。

### 3.2 大厂支持矩阵
● 原生/产品级　◐ 适配器/教育级　○ 未支持　— 未见声明　N/A 已停用

| | MCP | A2A | ACP-IBM | ACP-Zed | AG-UI |
|---|---|---|---|---|---|
| **OpenAI** | ● Responses API/ChatGPT [27] | — (AAIF创始机构,非产品支持) | N/A | ◐ Codex CLI社区适配器,官方文档只提MCP | — |
| **Anthropic** | ● 创造者,已捐AAIF [25] | ◐ 仅Vertex AI教育网研 [35] | N/A | ◐ Claude Code经Zed适配器,非原生 [18] | — |
| **Google** | ● Gemini Enterprise支持MCP服务器 | ● 发起方 [8] | N/A | ● Gemini CLI原生(`gemini --acp`) [19] | — (自有A2UI协议,非AG-UI) [30] |
| **Microsoft** | ● Copilot Studio/Azure Foundry [31] | ● Copilot Studio(2026-05 GA) [31] | N/A | ○ VS Code仅讨论中issue,无承诺 [20] | — |

**自家框架**：OpenAI **Agents SDK**[28]；Google **ADK**(多语言)[29]、**A2UI**(agent驱动UI树)[30]；Microsoft **Agent Framework**(SK后继)[32]；Anthropic 无独立框架,MCP即其出品。

## 4. 用户需要知道的坑

1. **认协议先认域名**：ACP 撞名 3 次（见 3.1），配置/SDK 对不上时先查官方域名（agentcommunicationprotocol.dev / agentclientprotocol.com / developers.openai.com/commerce），别猜。
2. **ACP-Zed "adopter" 要问是谁写的适配器**：Zed 自己写了 `@zed-industries/claude-code-acp` 这类桥接层，被列入 adopter 不代表该厂商原生实现（见一屏看懂 #6）[16][18][19]。
3. **旧 MCP 教程的 stateful 逻辑会报错**：2026-07-28 版已无状态，对照当前 spec 版本号重新核对（见一屏看懂 #8）[1]。
4. **"捐给基金会"要看具体机构和日期**：MCP 治理页早存在，但上级 AAIF 到 2025-12-09 才成立；判断"是否中立"不能只看有没有 Linux Foundation 字样 [4][25][26]。
5. **AG-UI 目前是单厂商项目**：CopilotKit 是风投创业公司，2026-05 的 $27M 融资明确与 AG-UI 采用挂钩，选型按厂商锁定风险评估 [24]。
6. **A2A 有三种协议绑定**（JSON-RPC/gRPC/REST），功能等价但线上格式不同，接入前先确认对方用哪种 [6]。

## 5. 未决与置信度

- AG-UI 何时捐给中立基金会：二手分析称存在利益冲突，官方未宣布计划，截至 2026-09 治理未变 [24]。
- 传闻 "ACP" 撞名达 4 次，第 4 个身份未查实，不纳入正文，仅供留意。
- ACP-IBM 鉴权细节（mTLS/JWS）仅二手来源（ml4devs.com），协议已停维护未再核实。
- GitHub Copilot CLI 是否"官方"支持 ACP-Zed：仅见 Zed adopter 列表，registry 不分官方/社区；勿与 VS Code 讨论中的 issue #265496 混淆 [20]。
- MCP 治理页是否已反映 2025-12-09 后的 AAIF 创始项目身份：内容不冲突，但更新时间戳未查到。

## 来源

[1] MCP Architecture — https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
[2] MCP Deprecated transports — https://modelcontextprotocol.io/specification/2026-07-28/deprecated
[3] MCP Basic spec — https://modelcontextprotocol.io/specification/2026-07-28/basic
[4] MCP Governance — https://modelcontextprotocol.io/community/governance
[6] A2A Specification v1.0.1 — https://a2a-protocol.org/v1.0.1/specification/
[7] A2A GitHub releases — https://github.com/a2aproject/A2A
[8] LF launches A2A project — https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents
[9] A2A joins AAIF — https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/
[10] LF AI&Data: ACP joins A2A — https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
[11] ACP-IBM GitHub(archived) — https://github.com/i-am-bee/acp
[12] ACP-IBM Architecture — https://agentcommunicationprotocol.dev/core-concepts/architecture
[14] Zed ACP — https://agentclientprotocol.com
[15] Zed ACP Governance — https://agentclientprotocol.com/community/governance
[16] Zed ACP adopters — https://zed.dev/acp
[17] Zed external agents(state/auth) — https://zed.dev/docs/ai/external-agents
[18] Zed: Claude Code via ACP — https://zed.dev/blog/claude-code-via-acp
[19] Gemini CLI ACP mode — https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/acp-mode.md
[20] VS Code ACP tracking issue — https://github.com/microsoft/vscode/issues/265496
[21] AG-UI Spec 1.0 — https://docs.ag-ui.com/spec/1.0
[22] CopilotKit × AG-UI — https://www.copilotkit.ai/ag-ui
[23] AG-UI blog — https://webflow.copilotkit.ai/blog/ag-ui-protocol-bridging-agents-to-any-front-end
[24] AG-UI governance(secondary) — https://rywalker.com/research/ag-ui
[25] Anthropic: donating MCP & AAIF — https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
[26] LF announces AAIF formation — https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
[27] OpenAI MCP support — https://developers.openai.com/api/docs/mcp
[28] OpenAI Agents SDK — https://openai.com/index/the-next-evolution-of-the-agents-sdk/
[29] Google ADK blog — https://developers.googleblog.com/build-cross-language-multi-agent-team-with-google-agent-development-kit-and-a2a/
[30] Google A2UI — https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/
[31] Azure MCP+A2A blog — https://azure.microsoft.com/en-us/blog/agent-factory-connecting-agents-apps-and-data-with-new-open-standards-like-mcp-and-a2a/
[32] Microsoft Agent Framework — https://learn.microsoft.com/en-us/agent-framework/overview/
[33] OpenAI Agentic Commerce Protocol — https://github.com/agentic-commerce-protocol/agentic-commerce-protocol
[34] Stripe: Agentic Commerce Protocol — https://stripe.com/blog/developing-an-open-standard-for-agentic-commerce
[35] Anthropic×Google webinar(MCP+A2A) — https://www.anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai
