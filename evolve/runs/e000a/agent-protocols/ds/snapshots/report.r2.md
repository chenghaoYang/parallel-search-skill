# Agent 协议全景：MCP/A2A/ACP(两个)/AG-UI 怎么分清楚

> 截至2026-09-24。按"协议管哪一层交互"建立taxonomy，再给对照表、大厂矩阵、常见坑。[n]对应文末来源；❓未查到，⚠仅二手，∅官方未定义。

## 0. 一屏看懂

1. **"ACP" 撞名，两个互不相关的协议**：IBM/BeeAI 的 Agent Communication Protocol（agent↔agent）已于 2025-08-25 并入 A2A，仓库归档只读（详见第4节）[17][18]。Zed 的 Agent Client Protocol（编辑器↔coding agent）是完全独立的协议，2025-08 发布，设计借鉴 LSP[21]。今天再看到"ACP"，指的基本是还活着的 Zed 这个。
2. **MCP 的 HTTP+SSE 确实废了**：自协议版本 2025-03-26 起"软弃用"，2026-07-28 版正式按 feature lifecycle 政策标记为 Deprecated（SEP-2596），建议迁移到 Streamable HTTP[3]。
3. **MCP 2026-07-28 变成了彻底无状态协议**：官方原句"remove protocol-level sessions and the `Mcp-Session-Id` header"——不只去掉握手，连会话 header 都删了；每个请求靠 `_meta` 里的 `protocolVersion` 独立生效，没有协商；跨调用状态得靠 server 发的 handle 当工具参数传[3]。四个协议里唯一主动砍掉"连接态"的设计。
4. **MCP 和 A2A 现在同属一个基金会**：MCP 2025-12-09 捐给新成立的 Agentic AI Foundation(AAIF，Linux Foundation名下)[7]；A2A(原Google发起)2025-06先捐LF，2026-08-27转AAIF托管，官方称MCP是"sibling project"[13]。各自独立到什么程度官方未细化，见第6节。
5. **分层不重叠是官方共识**：MCP管"用工具/数据"(vertical)，A2A管"agent间协作"(horizontal)，官方自称"complementary, not competing"[10]；AG-UI管"对接前端"[24]。常被误认为AG-UI竞品的Google A2UI，官方定位其实是互补——A2UI是生成式UI组件规范，AG-UI是承载它的传输协议，AG-UI官方"fully supports the A2UI spec"[40]。
6. **治理成熟度有梯度**：MCP/A2A已基金会化；ACP-Zed是**Zed+JetBrains联合治理**(非单一公司)，官方明说是"过渡安排，目标转向独立基金会"[22]；AG-UI由CopilotKit一家创业公司主导，暂无联合治理或基金会路线图[27]。
7. **鉴权没有统一标准**：MCP强制OAuth2.1+PKCE及RFC8707/9728/9207等[4]；A2A支持OAuth2.0(device code/PKCE)+mTLS+OIDC[9]；ACP-Zed定义`authenticate`骨架但机制留给agent实现方[22]；AG-UI不规定，交给后端框架[24]。
8. **大厂站队不对称**：MCP四家共识原生支持；A2A合作伙伴名单没有OpenAI/Anthropic，但两家都是现托管A2A的AAIF白金创始成员——治理层有关系，产品级声明暂无[39][30]；AG-UI集成列表里有Anthropic/Google/Microsoft，没有OpenAI[24]。细节见第3节。

## 1. Taxonomy

按"管辖的交互双方"分三个家族：

| 家族 | 成员 | 交互双方 | 为什么是一类 |
|---|---|---|---|
| **M·模型↔工具** | MCP | LLM应用↔外部工具/数据源 | 给agent接数据和函数，Anthropic发起，已捐AAIF |
| **A·agent↔agent** | A2A、ACP-IBM(已并入A2A,历史实体) | 两个独立、可能互不信任的agent | agent间怎样互相委派任务，均归Linux Foundation/AAIF |
| **C·agent↔客户端** | ACP-Zed、AG-UI | agent与它的宿主(编辑器/Web前端) | agent的动作/输出怎么呈现，治理成熟度是两者主要差异 |

比较维度（下表按此排列）：

| # | 维度 | 回答什么问题 |
|---|---|---|
| D1 | 定位 | 谁和谁对话？ |
| D2 | 核心抽象 | 协议里的第一公民叫什么？ |
| D3 | 传输 | 底层怎么封装消息？ |
| D4 | 状态 | 会话状态存在哪端？ |
| D5 | 鉴权 | 协议规定的认证方式？ |
| D6 | 版本 | 当前版本号/发布节奏？ |
| D7 | 治理 | 谁拥有决策权？ |
| D8 | 厂商 | 谁在官方实现？（见第3节矩阵） |
| D9 | 关系 | 官方怎么描述和别的协议的关系？ |
| D10 | 成熟度 | 是否 GA、有无生产警告？ |

## 2. 对照矩阵

### 2a 定位 / 抽象 / 传输 / 状态

| | MCP | A2A | ACP-IBM(已并入A2A) | ACP-Zed | AG-UI |
|---|---|---|---|---|---|
| D1定位 | Host-Client-Server；LLM应用↔工具/数据[1] | 独立 agent 之间的水平协作[9] | agent↔agent，REST化[19] | 编辑器(客户端)↔coding agent[21] | agent后端↔用户前端应用[24] |
| D2抽象 | Tools/Resources/Prompts(server)+Elicitation(client)[1] | Task/Message/AgentCard/Part/Artifact[11] | Run/Message/MessagePart/Await/Sessions[17] | session/prompt turn/content block/tool call[21] | 17种事件:生命周期/文本/工具/状态/自定义[25] |
| D3传输 | stdio、Streamable HTTP(取代HTTP+SSE)[2] | JSON-RPC2.0(主流)/gRPC/HTTP+REST[9] | RESTful over HTTP，同步+异步[19] | 本地JSON-RPC over stdio；远程HTTP/WS(研发中)[21] | 中间件层任意事件传输(SSE/WS/webhook)[25] |
| D4状态 | 协议级完全无状态:无握手、无Session-Id header，跨调用状态靠server发的显式handle[3] | Server端task状态[9] | Run状态机(created→…→cancelled)，隐含server持有[17] | 客户端存会话线程；鉴权/状态由agent实现方自管[21] | 后端存threadId/runId，前端只管展示[24] |

### 2b 鉴权 / 版本 / 治理 / 成熟度

| | MCP | A2A | ACP-IBM | ACP-Zed | AG-UI |
|---|---|---|---|---|---|
| D5鉴权 | OAuth2.1强制+PKCE，RFC8707/9728/9207等[4] | OAuth2.0(device code/PKCE)+mTLS+OIDC[9] | ❓官方未明确鉴权机制 | `authenticate`方法+`methodId`，terminal/agent两类(默认agent自行实现)[22] | 不规定机制，交给后端框架(示例:OAuth2/JWT/Azure AD)[24] |
| D6版本 | 日期版：2024-10-07→2026-07-28，无semver"1.0"概念[5] | semver：v0.2.0(2025-06)→v1.0.0(2026-03,破坏性)→v1.0.1(2026-05)[12] | v1.0.0(2025-07)→v1.0.3(2025-08-21，末次)[17] | wire协议版本"1"(稳定)，包版本v0.13.6(预1.0)[22] | v1.0.0 GA于2026-09-17[26] |
| D7治理 | Anthropic创建(2024-11)→四层maintainer+SEP流程→2025-12捐AAIF，项目仍自治[6][7] | Google捐LF(2025-06)→创始成员7家+IBM后加入TSC[15][18]→2026-08转AAIF[13] | IBM主导→2025-05捐LF AI&Data→2025-08并入A2A，仓库归档[18] | **Zed+JetBrains联合治理**，Lead各出一人，RFD流程，官方称"过渡安排、目标转向独立基金会"[22] | CopilotKit(创业公司)主导，无联合治理/基金会路线图[27] |
| D10成熟度 | 称"production-grade"，未称1.0[8] | v1.0稳定，LF称已有企业生产案例、150+支持组织[16] | 已停止独立维护，官方导流A2A[18] | 预1.0，官方预期仍有breaking change[22] | 刚GA(约一周)，release note称已有大厂集成[26] |

## 3. 大厂支持矩阵

| | MCP | A2A | ACP(Zed) | AG-UI | 自家变体/竞品 |
|---|---|---|---|---|---|
| OpenAI | ✅Agents SDK/Responses API/ChatGPT(2025-03起)[28] | ⚠不在A2A合作伙伴名单，但AAIF白金创始成员[39] | ⚠Codex agent可接入(Zed页列出)[23] | ∅未在集成列表[24] | Agents SDK/AgentKit——自家编排框架 |
| Anthropic | ✅创造者，Claude系产品原生[29] | ⚠同上+联合Google办过webinar[30][31] | ⚠Claude Agent可接入(Zed页列出)[23] | ✅集成列表列Claude Managed Agents/SDK[24] | 无独立协议；Agent SDK内建MCP client |
| Google | ✅托管官方MCP服务+ADK双向支持[32][33] | ✅发起方，ADK原生集成[33] | ⚠Gemini CLI首个集成方(Zed页列出)[23] | ✅ADK为集成方[24]；另推A2UI(互补非竞争)[40] | A2UI——生成式UI组件规范 |
| Microsoft | ✅SK(2025-04起)/Copilot Studio/Agent Framework均原生[34][36] | ✅Copilot Studio编排+SK "speaks A2A"[35][38] | ⚠VS Code被Zed页列为受支持编辑器[23] | ✅Agent Framework官方专页集成[37] | Agent Framework——整合原SK+AutoGen |

## 4. 变体与适配层

- **ACP-IBM→A2A 是官方合并，不是竞争落败**：IBM 表态"把 ACP 的资产和专业知识并入 A2A，构建单一、更强的标准"[18]，团队负责人 Kate Blair 随后正式加入 A2A 技术指导委员会，代表 IBM 与 Google/Microsoft/AWS/Cisco/Salesforce/ServiceNow/SAP 并列[18]——真整合而非项目死亡。
- **ACP-Zed 主动复用 MCP、借鉴 LSP**：官方"reuses JSON representations from MCP where applicable"，为编程场景(diff可视化)加专有类型，并承认"draws inspiration from the Language Server Protocol"[21]。
- **AG-UI 与 Google A2UI 是互补，不是竞品**：Google 称 AG-UI 是 A2UI 的"launch partner"/"day-zero compatibility"；AG-UI 官方区分两者层级——"A2UI is a generative UI specification" vs "AG-UI is the Agent↔User Interaction protocol"[40]。此前"两者竞争"的说法是误读。
- **三层协议设计为叠加使用**：MCP管工具、A2A管agent间协作、AG-UI管前端呈现，官方画像是同时使用而非互斥[24]。

## 5. 常见坑

1. **别把两个"ACP"的资料混着查**：`agentcommunicationprotocol.dev`/`i-am-bee`是已归档的 IBM 版；`agentclientprotocol.com`/`zed-industries`是仍在更新的 Zed 版[17][21]。
2. **新 MCP server 别再只实现 HTTP+SSE**：官方要求至少12个月弃用窗口，新项目直接上 Streamable HTTP 更省事[3]。
3. **MCP 老 client 假设"有会话"会在 2026-07-28 上栽跟头**：连接复用、Session-Id 这类旧假设全部作废，升级前重读 lifecycle 页[3]。
4. **MCP 版本号不是语义化版本**：`2026-07-28` 表示"最后一次不兼容变更日期"，判断兼容性看运行时 `protocolVersion` 协商结果，别套 semver 直觉[5]。
5. **A2A 和 MCP 不是二选一**：官方设计成一起用——agent 先用 MCP 拿数据/工具，再用 A2A 找别的 agent 协作[10]。
6. **AG-UI 暂不具备"厂商中立"保证，ACP-Zed 已在路上**：前者治理权在一家创业公司手里，后者至少两家公司联合治理且承诺过渡到独立基金会，长期依赖前评估锁定风险[27][22]。

## 6. 未决与置信度

- "MCP/A2A在AAIF下各自完全独立维护maintainers/spec/发版"：A2A官方只说MCP是"sibling project"，未细化独立程度，具体措辞仅二手来源(pebblous.ai)给出。
- ACP-IBM鉴权机制官方从未写明(协议已归档停更，大概率不会再补)。
- Microsoft VS Code对ACP-Zed的支持，来源是Zed官方列表而非微软声明，官方插件还是社区插件未确认。
- AAIF成员分级(Platinum/Silver/Bronze)具体定义和权利差异未查到官方文档。
- OpenAI Agents SDK对A2A支持有GitHub feature request(issue #1374)但无官方发版承诺。

## 来源
[1]modelcontextprotocol.io/specification/2026-07-28(+architecture) [2]同/basic/transports(+streamable-http) [3]同/changelog、/basic/versioning；github.com/modelcontextprotocol/modelcontextprotocol(changelog.mdx) [4]modelcontextprotocol.io/specification/draft/basic/authorization [5]modelcontextprotocol.io/specification/versioning [6]github.com/modelcontextprotocol/modelcontextprotocol(governance.mdx) [7]blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation [8]MCP spec-GA博客(2026-07-28-spec-ga)
[9]a2a-protocol.org/latest/specification(+partners) [10]同/topics/a2a-and-mcp [11]github.com/a2aproject/A2A(a2a.proto) [12]同/releases [13]a2a-protocol.org/.../a-new-chapter-for-a2a-joining-the-agentic-ai-foundation [14]developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation [15]linuxfoundation.org/press/...-agent2agent-protocol-project [16]linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations
[17]github.com/i-am-bee/acp(已归档) [18]lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a... [19]research.ibm.com/blog/agent-communication-protocol-ai [20]agentcommunicationprotocol.dev/about/mcp-and-a2a
[21]agentclientprotocol.com(+community/governance) [22]github.com/zed-industries/agent-client-protocol(schema/MAINTAINERS/CONTRIBUTING) [23]zed.dev/acp
[24]docs.ag-ui.com/introduction(+integrations) [25]github.com/ag-ui-protocol/ag-ui [26]同/releases [27]同/discussions/166
[28]developers.openai.com/api/docs/guides/tools-connectors-mcp [29]anthropic.com/news/model-context-protocol [30]anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation [31]anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai [32]cloud.google.com/blog/.../announcing-official-mcp-support-for-google-services [33]adk.dev/mcp [34]devblogs.microsoft.com/semantic-kernel/...-mcp-support-for-python [35]learn.microsoft.com/.../copilot-studio/add-agent-agent-to-agent [36]devblogs.microsoft.com/foundry/microsoft-agent-framework-version-1-0 [37]learn.microsoft.com/.../agent-framework/integrations/ag-ui [38]devblogs.microsoft.com/foundry/semantic-kernel-a2a-integration [39]openai.com/index/agentic-ai-foundation [40]developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces
[s1]rywalker.com/research/zed-agent-client-protocol(二手,部分结论已被一手修正) [s2]4sysops.com/archives/comparing-ai-protocols-...(二手)
