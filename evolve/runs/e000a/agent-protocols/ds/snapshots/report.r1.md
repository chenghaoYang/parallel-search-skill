# Agent 协议全景：MCP/A2A/ACP(两个)/AG-UI 怎么分清楚

> 截至 2026-09-24。按"协议管哪一层交互"建立 taxonomy，再给字段级对照表、大厂矩阵、常见坑。[n]对应文末来源；❓=未查到，⚠=仅二手，∅=官方未定义。

## 0. 一屏看懂

1. **"ACP" 撞名，两个互不相关的协议**：IBM/BeeAI 的 Agent Communication Protocol（agent↔agent）已于 2025-08-25 正式并入 A2A，GitHub 仓库归档只读，团队解散、转去给 A2A 贡献代码[17][18]。Zed 的 Agent Client Protocol（编辑器↔coding agent）是完全独立的协议，2025-08 发布，设计借鉴 LSP[21]。今天再看到"ACP"，指的基本是还活着的 Zed 这个。
2. **MCP 的 HTTP+SSE 确实废了**：自协议版本 2025-03-26 起"软弃用"，2026-07-28 版正式按 feature lifecycle 政策标记为 Deprecated（SEP-2596），官方建议迁移到 Streamable HTTP[3]。别再新写 SSE-only 的 MCP server。
3. **MCP 和 A2A 现在同属一个基金会**：MCP 由 Anthropic 于 2025-12-09 捐给新成立的 Agentic AI Foundation（AAIF，Linux Foundation 名下有向基金）[7][30]；A2A（原 Google 发起）2025-06 先捐给 Linux Foundation，2026-08-27 转为 AAIF 托管项目[13][14]。是"同基金会下两个独立协议"，不是合并。
4. **分层不重叠是官方共识**：MCP 管"agent 怎么用工具/数据"（官方称 vertical），A2A 管"agent 之间怎么协作"（horizontal），二者官方自称"complementary, not competing"[10]。AG-UI 再加一层，管"agent 后端怎么对接用户前端"[24]。三层组合已是官方认可的标准架构。
5. **AG-UI 和 ACP-Zed 都不是基金会中立治理**：AG-UI 2026-09-17 才发 v1.0.0[26]，由 CopilotKit（风投背景创业公司）主导，无基金会托管[27]；ACP-Zed 包版本仍是预1.0的 v0.13.6，由 Zed Industries 主导[22][s1]。跟 MCP/A2A 的基金会治理不是一个量级。
6. **鉴权没有统一标准**：MCP 强制 OAuth 2.1+PKCE，要求实现 RFC 8707/9728/9207 等一整套 IETF 规范[4]；A2A 支持 OAuth2.0(device code/PKCE)、mTLS、OIDC 多选[9]；ACP-Zed 和 AG-UI 把具体鉴权留给宿主/后端自己实现[24]。
7. **大厂站队不对称**：MCP 已是四家共识（OpenAI/Anthropic/Google/Microsoft 均原生支持）；A2A 是 Google 发起、Microsoft 力推，Anthropic 只在联合演示中出现过、OpenAI 未查到表态；AG-UI 只有 Microsoft 原生集成，Google 同时在推疑似竞品 A2UI。细节见第3节。

## 1. Taxonomy

按"管辖的交互双方"分三个家族：

| 家族 | 成员 | 交互双方 | 为什么是一类 |
|---|---|---|---|
| **M·模型↔工具** | MCP | LLM应用↔外部工具/数据源 | 给agent接数据和函数，Anthropic发起，已捐AAIF |
| **A·agent↔agent** | A2A、ACP-IBM(已并入A2A,历史实体) | 两个独立、可能互不信任的agent | agent间怎样互相委派任务，均归Linux Foundation/AAIF |
| **C·agent↔客户端** | ACP-Zed、AG-UI | agent与它的宿主(编辑器/Web前端) | agent的动作/输出怎么呈现，均单一公司主导，未入基金会 |

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
| D2抽象 | Tools/Resources/Prompts(server)+Elicitation(client)[1] | Task/Message/AgentCard/Part/Artifact[11] | Run/Message/MessagePart/Await/Sessions[17] | session/prompt turn/content block/tool call[21] | 17种事件：生命周期/文本/工具调用/状态/自定义[25] |
| D3传输 | stdio、Streamable HTTP(取代HTTP+SSE)[2] | JSON-RPC2.0(主流)/gRPC/HTTP+REST 三绑定[9] | RESTful over HTTP，同步+异步[19] | 本地:JSON-RPC over stdio；远程:HTTP/WS(研发中)[21] | 中间件层任意事件传输(SSE/WS/webhook)[25] |
| D4状态 | 2026-07-28起去掉initialize握手，官方称"eliminates handshake"[3] | Server端task状态("state kept in server-side task")[9] | Run状态机(created→…→cancelled)，隐含server持有[17] | 编辑器端存会话线程，agent自己管运行时/鉴权[s1] | 后端存threadId/runId，前端只管展示，不传history则视为无状态[24] |

### 2b 鉴权 / 版本 / 治理 / 成熟度

| | MCP | A2A | ACP-IBM | ACP-Zed | AG-UI |
|---|---|---|---|---|---|
| D5鉴权 | OAuth2.1强制+PKCE，RFC8707/9728/9207等[4] | OAuth2.0(device code/PKCE)+mTLS+OIDC，v1.0移除implicit/password[9] | ❓官方文档未明确鉴权机制 | ⚠init→可选认证→会话，具体机制由各agent自行实现(仅二手来源)[s1] | 协议不规定机制，交给后端框架(示例:OAuth2/JWT/Azure AD)[24] |
| D6版本 | 日期版：2024-10-07→2026-07-28，无semver"1.0"概念[5] | semver：v0.2.0(2025-06)→v1.0.0(2026-03,破坏性)→v1.0.1(2026-05)[12] | v1.0.0(2025-07-01)→v1.0.3(2025-08-21，末次发布)[17] | wire协议版本"1"(稳定)，包版本v0.13.6(预1.0，仍有breaking change预期)[22] | v1.0.0 GA于2026-09-17，此前多次预发布[26] |
| D7治理 | Anthropic创建(2024-11)→四层maintainer结构+SEP流程→2025-12捐AAIF，项目仍自治[6][7] | Google捐LF(2025-06)→创始成员AWS/Cisco/Google/MS/Salesforce/SAP/ServiceNow[15]→2026-08转为AAIF托管项目[13] | IBM Research主导→2025-05捐BeeAI给LF AI&Data→2025-08并入A2A，仓库归档[18] | Zed Industries主导，JetBrains参与注册表；⚠非基金会中立托管(二手定性)[s1] | CopilotKit(创业公司)主导；官方GitHub Discussion自述"始于内部方案"[27] |
| D10成熟度 | 称"production-grade infrastructure"/"enterprise-ready"，未称1.0[8] | v1.0稳定，LF称已有企业生产案例、150+支持组织[16] | 已停止独立维护，官方导流到A2A[18] | 预1.0，官方预期仍有breaking change[22] | 刚GA(发布约一周)，release note称已有大厂集成[26] |

## 3. 大厂支持矩阵

| | MCP | A2A | ACP(Zed) | AG-UI | 自家变体/竞品 |
|---|---|---|---|---|---|
| OpenAI | ✅原生：Agents SDK/Responses API/ChatGPT(2025-03起)，2025-09 ChatGPT全读写[28] | ❓无官方声明 | ⚠Codex agent可接入(Zed页列出，非OpenAI自述)[23] | ❓无官方声明 | Agents SDK/AgentKit——自家编排框架，非跨厂商协议 |
| Anthropic | ✅创造者，Claude系产品原生支持[29] | ⚠仅与Google联合办过MCP+A2A webinar，无独立声明[31] | ⚠Claude Agent可接入(Zed页列出)[23] | ❓无官方声明 | 无独立互操作协议；Claude Agent SDK内建MCP client |
| Google | ✅托管官方MCP服务，ADK双向支持[32][33] | ✅发起方，ADK原生集成[33] | ⚠Gemini CLI是首个集成方(Zed页列出)[23] | ⚠ADK为集成方之一[24]，二手称Google另推疑似竞品A2UI(2025-12)[s3] | A2UI——与AG-UI同层竞品(仅二手) |
| Microsoft | ✅SK(2025-04起)/Copilot Studio/Agent Framework均原生[34][36] | ✅Copilot Studio编排+SK "speaks A2A"[35][38] | ⚠VS Code被Zed页列为受支持编辑器，未见MS自述[23] | ✅Agent Framework官方专页集成[37] | Agent Framework——整合原SK+AutoGen |

## 4. 变体与适配层

- **ACP-IBM → A2A 是官方合并，不是竞争落败**：IBM 明确表态"把 ACP 的资产和专业知识并入 A2A，构建单一、更强的标准"[18]，旧用户用 A2AServer/A2AAgent 适配器迁移。
- **ACP-Zed 主动复用 MCP、借鉴 LSP**：官方原句"reuses JSON representations from MCP where applicable"，但为编程场景（如 diff 可视化）加了专有类型；同时承认"draws inspiration from the Language Server Protocol"[21]。
- **AG-UI 与 Google A2UI 关系不透明**：AG-UI 官方未提及 A2UI；仅二手称 A2UI 于 2025-12 发布时 AG-UI 是"launch partner"[s3]，两者同处一层（agent↔前端），合作或竞争官方未表态，见第5节。
- **三层协议设计为叠加使用**：AG-UI 官方文档直接给出画像——MCP 管工具、A2A 管 agent 间协作、AG-UI 管前端呈现，三者同时使用而非互斥[24]。

## 5. 常见坑

1. **别把两个"ACP"的资料混着查**：`agentcommunicationprotocol.dev`/`github.com/i-am-bee`是已归档的 IBM 版；`agentclientprotocol.com`/`github.com/zed-industries`是仍在更新的 Zed 版[17][21]。
2. **新 MCP server 别再只实现 HTTP+SSE**：官方要求至少 12 个月弃用窗口，但新项目直接上 Streamable HTTP 更省事，旧 server 迁移参考 changelog 的 Migrate 指引[3]。
3. **MCP 版本号不是语义化版本**：`2026-07-28` 表示"最后一次不兼容变更的日期"，不代表第几个大版本；判断兼容性要看运行时 `protocolVersion` 协商结果，别套 semver 直觉[5]。
4. **A2A 和 MCP 不是二选一**：官方设计成一起用——agent 先用 MCP 拿数据/工具，再用 A2A 找别的 agent 协作[10]，架构里同时出现两者是正常设计。
5. **AG-UI / ACP-Zed 暂不具备"厂商中立"保证**：治理权分别在一家创业公司和一家产品公司手里，长期依赖前应评估锁定/路线图风险[27][s1]。
6. **IBM 版 ACP 搜索引擎仍能查到，但已是历史文档**：仓库已归档只读，新项目别基于它开发，官方导流方向是 A2A[17][18]。

## 6. 未决与置信度

- ACP-IBM鉴权(❓官方未写)、ACP-Zed鉴权与治理定性(⚠仅二手rywalker.com)：R2直查agentclientprotocol.com协议页核实。
- MCP"取消initialize握手"是否等于完全无状态(Streamable HTTP的Session-Id是否仍隐含会话)，仅有changelog一句概括，未核对lifecycle原文。
- "MCP/A2A在AAIF下各自独立维护"来源是第三方博客，非两家官方原文，待一手确认。
- OpenAI/Anthropic对A2A、三家对AG-UI，目前只是"没查到声明"，未确认是"明确不支持"还是"未表态"。
- Google A2UI与AG-UI合作还是竞争，只有二手来源，未见双方官方对话。
- Microsoft VS Code对ACP-Zed的支持，来源是Zed官方列表而非微软声明，官方插件还是社区插件待确认。

## 来源
[1] modelcontextprotocol.io/specification/2026-07-28(+/architecture) [2] .../2026-07-28/basic/transports [3] github.com/modelcontextprotocol/modelcontextprotocol(changelog.mdx) [4] modelcontextprotocol.io/specification/draft/basic/authorization [5] modelcontextprotocol.io/specification/versioning [6] github.com/modelcontextprotocol/modelcontextprotocol(governance.mdx) [7] blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation [8] MCP spec-GA博客(2026-07-28-spec-ga)
[9] a2a-protocol.org/latest/specification [10] .../latest/topics/a2a-and-mcp [11] github.com/a2aproject/A2A(a2a.proto) [12] github.com/a2aproject/A2A/releases [13] a2a-protocol.org/.../a-new-chapter-for-a2a-joining-the-agentic-ai-foundation [14] developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation [15] linuxfoundation.org/press/...-launches-the-agent2agent-protocol-project [16] linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations
[17] github.com/i-am-bee/acp(已归档) [18] lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a... [19] research.ibm.com/blog/agent-communication-protocol-ai [20] agentcommunicationprotocol.dev/about/mcp-and-a2a
[21] agentclientprotocol.com [22] github.com/zed-industries/agent-client-protocol [23] zed.dev/acp
[24] docs.ag-ui.com/introduction [25] github.com/ag-ui-protocol/ag-ui [26] .../ag-ui/releases [27] .../ag-ui/discussions/166
[28] developers.openai.com/api/docs/guides/tools-connectors-mcp [29] anthropic.com/news/model-context-protocol [30] anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation [31] anthropic.com/webinars/deploying-multi-agent-systems-using-mcp-and-a2a-with-claude-on-vertex-ai [32] cloud.google.com/blog/.../announcing-official-mcp-support-for-google-services [33] adk.dev/mcp [34] devblogs.microsoft.com/semantic-kernel/...-mcp-support-for-python [35] learn.microsoft.com/.../microsoft-copilot-studio/add-agent-agent-to-agent [36] devblogs.microsoft.com/foundry/microsoft-agent-framework-version-1-0 [37] learn.microsoft.com/.../agent-framework/integrations/ag-ui [38] devblogs.microsoft.com/foundry/semantic-kernel-a2a-integration
[s1] rywalker.com/research/zed-agent-client-protocol(二手) [s2] 4sysops.com/archives/comparing-ai-protocols-...(二手) [s3] levelup.gitconnected.com/ag-ui-vs-mcp-competing-protocols-...(二手)
