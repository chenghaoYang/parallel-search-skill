# Agent 时代的「协议」全景：MCP / A2A / ACP / AG-UI 怎么分清楚

> 本文回答 agent 生态里几种互操作「协议」各管什么、谁治理、怎么选。截至 2026-09-24；部分数据时效性强，见第 5 节。先看「一屏看懂」，需要细节再查表。**（本版本大厂支持面调研中，R2 补全）**

## 0. 一屏看懂
1. **「ACP」这个缩写至少撞了两次名，可能是三次**：IBM/BeeAI 的 *Agent Communication Protocol* 已于 2025-08-29 正式并入 A2A、仓库归档 [3]；Zed 的 *Agent Client Protocol* 连接的是"编辑器↔本地 agent 子进程"，和前者无关、仍在活跃开发 [5]；Cisco 发起的 AGNTCY 项目据传也有个组件叫 "Agent Connect Protocol"，本轮只有二手来源，未核实（第 5 节）。
2. **MCP 的 SSE 传输确实已废弃**：2025-03-26 版本标记 deprecated，2026-07-28 版本正式 reclassify 为 Deprecated，替代方案是 Streamable HTTP；相关 SEP 转正后 3 个月即可移除 [1]。
3. 四个协议连的是四种不同的"两端"：MCP＝agent↔工具/数据；A2A/ACP-IBM＝agent↔agent；AG-UI＝agent 后端↔用户界面；ACP-Zed＝宿主应用↔本地 agent 子进程。**官方立场是互补不是竞争**——AG-UI 文档明确说"三者通常被同一个 agent 同时使用"[4]。
4. 治理正在向中立基金会集中，但进度不一：A2A 已捐给 Linux Foundation（2025-06-23）[2]；MCP 据称是 Linux Foundation 新设 Agentic AI Foundation 的 founding contribution 之一（2025-12，本轮为二手来源）；ACP-Zed 是 Apache-2.0 独立开源项目，未捐赠基金会；AG-UI 由刚融完 A 轮的创业公司 CopilotKit 主导，同样未捐赠基金会 [4]。
5. 鉴权没有一套标准打天下：MCP 用 OAuth 2.1+RFC8707/9207 [1]；A2A 支持 OAuth2/API key/mTLS/HTTP Basic 且强制 TLS1.2+ [2]；ACP-Zed 鉴权在"宿主进程"层面，只定义 agent/terminal 两种登录握手，不规定凭证格式 [5]；AG-UI 明确说"不内置鉴权，复用宿主 HTTP 端点机制"[4]。

## 1. Taxonomy
分类轴：协议标准化的是"哪两端"之间的通信。

| 家族 | 两端 | 成员 |
|---|---|---|
| Agent ↔ 工具/数据 | agent 运行时 ↔ 外部工具、API、数据源 | MCP |
| Agent ↔ Agent | 独立 agent/系统跨主体协作 | A2A、ACP-IBM（已并入 A2A）|
| Agent 后端 ↔ 用户界面 | agent 逻辑 ↔ 前端/聊天 UI | AG-UI |
| 宿主应用 ↔ 本地 Agent | 编辑器/IDE ↔ 它拉起的 agent 子进程 | ACP-Zed |

维度：连接对象｜起源→现治理｜版本｜传输层｜消息格式｜鉴权｜核心概念｜采用者｜与其他协议关系。

## 2. 对照矩阵

**谁连谁 / 谁治理 / 多新**

| 协议 | 连接对象 | 起源 → 现治理 | 版本 |
|---|---|---|---|
| MCP | LLM 应用 ↔ 工具/数据/工作流 | Anthropic（2024-11）→ LF Agentic AI Foundation founding contribution（2025-12，二手）[1] | 2024-10-07 首发 → 2026-07-28 最新 [1] |
| A2A | 独立 agent 系统间协作 | Google（2025-04-09）→ Linux Foundation（2025-06-23 捐赠）；TSC 8 家含 Microsoft/Cisco/AWS/IBM 等 [2] | v0.1 → v1.0.1（2026-05-28）[2] |
| ACP-IBM | agent/应用/人类之间通信 | IBM Research（2025-03-17）→ 已并入 A2A（2025-08-29"joins forces"，仓库归档）[3] | v1.0.0 → v1.0.3（2025-08-21，末版）[3] |
| ACP-Zed | 编辑器 ↔ 本地 agent 子进程 | Zed Industries（2025-06-23）→ 独立开源 Apache-2.0，JetBrains 共同开发 [5] | v1 稳定（2026-06-24）→ schema 1.23.0；v2 alpha [5] |
| AG-UI | agent 后端 ↔ 用户界面 | CopilotKit（VC 背景创业公司）[4] | 规范 2026-07-18 首发 → v1.0（2026-09-17）[4] |

**怎么连 / 鉴权 / 核心概念**

| 协议 | 传输层 | 鉴权 | 核心概念 |
|---|---|---|---|
| MCP | stdio／Streamable HTTP（**HTTP+SSE 已废弃**，2025-03-26 起，2026-07-28 正式 reclassify）[1] | OAuth 2.1 + RFC6750/8707/9207（issuer 校验，2026-07-28 起）[1] | Tools/Resources/Prompts（服务端）；Elicitation（客户端）[1] |
| A2A | JSON-RPC 2.0／gRPC／HTTP+REST 三选一等效，强制 TLS1.2+ [2] | OAuth2／API key／mTLS／HTTP Basic；401/403 语义明确 [2] | AgentCard、Task、Message、Part、Artifact [2] |
| ACP-IBM | REST／JSON-RPC／WebSocket，同步+异步+流式 [3] | Basic Auth／Bearer／JWT；TLS；身份联邦曾在开发中 [3] | 已停止演进（末版 v1.0.3）[3] |
| ACP-Zed | JSON-RPC 2.0 over stdio（本地）；HTTP/WS 远程传输开发中 [5] | 协议层不规定凭证格式，定义 agent/terminal 两种登录握手 [5] | Request/Response/Notification，protocolVersion 握手 [5] |
| AG-UI | SSE 或 WebSocket，JSON 事件流，17 种标准事件分 5 类 [4] | 不内置，复用宿主 HTTP 端点鉴权；ThreadId≠鉴权凭证 [4] | RunStarted/TextMessage*/ToolCall*/State* 等事件 [4] |

## 3. 变体与适配层

**同名不同物：三个"ACP"**

| | IBM/BeeAI ACP | Zed ACP | AGNTCY "ACP"（未核实）|
|---|---|---|---|
| 全称 | Agent Communication Protocol | Agent Client Protocol | Agent Connect Protocol（二手来源）|
| 连接对象 | agent ↔ agent（跨主体）| 编辑器 ↔ 本地 agent 子进程 | 不明确，见第 5 节 |
| 现状 | 已并入 A2A，仓库归档（2025-08）[3] | 活跃开发，v1 稳定，JetBrains 等 11+ 采用 [5] | 未核实 |

MCP/A2A/AG-UI 官方互相定位、不重叠：MCP 负责"agent 拿到工具和数据"，A2A 负责"agent 之间怎么协调"，AG-UI 负责"agent 怎么把过程实时呈现给终端用户"；AG-UI 已支持"代理"MCP/A2A agent 的握手模式 [4]。

## 4. 用户需要知道的坑
1. "SSE 已废弃"≠"MCP 不能用 HTTP"——废弃的是纯 SSE 长连接方案，替代方案 Streamable HTTP 仍用 SSE 做单次请求内的流式响应，只是取消了跨请求恢复（Last-Event-ID）[1]。老教程如果还在讲"SSE transport"，对应的是 2024-11-05 那版协议。
2. 看到"ACP"先看它连的是谁，别只看展开的英文全称——三个候选任何一个都可能被简称"ACP"。
3. AG-UI 不是中立基金会治理，是一家刚融完 A 轮的创业公司主导 [4]——评估长期稳定性时要考虑这点和 MCP/A2A 的治理成熟度不同。
4. 鉴权没有统一标准：接 MCP 按 OAuth2.1，接 A2A 可能是 mTLS 也可能是 API key（由对方 agent 决定），接 AG-UI 基本靠宿主应用自己的鉴权，不能假设协议自带鉴权。

## 5. 未决与置信度
- **大厂支持面（OpenAI/Anthropic/Google/Microsoft 各自支持什么协议、自家变体）本轮未调研，Grid B 为空，是 R2 首要目标。**
- AGNTCY 是否真的官方使用"Agent Connect Protocol (ACP)"这个名字：本轮只有一条二手来源（tfir.io），未经一手确认，R2 核实。
- MCP 捐赠给 Linux Foundation Agentic AI Foundation 的确切日期/原句：本轮只有二手来源，R2 用 linuxfoundation.org 一手来源核实。
- ACP-IBM 并入 A2A 的宣布日期：官方博客说 8-29，GitHub Discussion 提到 8-25——更可能是"内部讨论(8-25)→仓库归档(8-27)→对外公告(8-29)"的时间线而非冲突，以官方博客日期为准。
- 除本文 5 个协议外，业内还有 ANP、LMOS、x402、AITP、TAP 等至少 9 个相关协议/标准，多为 secondary 来源，本文按 budget 限制未逐一展开。

## 来源
[1] MCP 官方 spec/changelog — https://modelcontextprotocol.io/specification/2026-07-28/changelog ，https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization ，https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http ，https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
[2] A2A 官方 spec/治理 — https://a2a-protocol.org/latest/specification/ ，https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/ ，https://github.com/a2aproject/A2A/blob/main/GOVERNANCE.md
[3] ACP-IBM 官方公告/仓库 — https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ ，https://github.com/i-am-bee/acp ，https://research.ibm.com/blog/agent-communication-protocol-ai
[4] AG-UI 官方文档 — https://docs.ag-ui.com/introduction ，https://docs.ag-ui.com/agentic-protocols ，https://github.com/ag-ui-protocol/ag-ui/
[5] ACP-Zed 官方文档 — https://agentclientprotocol.com ，https://github.com/agentclientprotocol/agent-client-protocol ，https://zed.dev/blog/jetbrains-on-acp
[6] 其他协议线索（scout，多为二手）— https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation/ ，https://tfir.io/ciscos-agntcy-takes-on-ai-agent-fragmentation-under-linux-foundation-umbrella/
