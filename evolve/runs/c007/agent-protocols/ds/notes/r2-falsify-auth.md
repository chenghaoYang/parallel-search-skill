# r2-falsify-auth
question: 反证两条否定主张：A「AG-UI spec 不定义任何鉴权机制」；B「Zed ACP 没有鉴权概念」
checked: https://agentclientprotocol.com/protocol/initialization, https://agentclientprotocol.com/protocol/overview, https://agentclientprotocol.com/protocol/authentication, https://agentclientprotocol.com/protocol/transports, https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/schema.json, https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v2/schema.json, https://api.github.com/repos/agentclientprotocol/agent-client-protocol/git/trees/main?recursive=1, https://docs.ag-ui.com/, https://docs.ag-ui.com/llms.txt, https://docs.ag-ui.com/spec/1.0/schema.json, https://docs.ag-ui.com/spec/1.0/basic/transports/index.md, https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse.md, https://docs.ag-ui.com/spec/1.0/basic/run-input.md, https://docs.ag-ui.com/spec/1.0/basic/capabilities.md, https://docs.ag-ui.com/sdk/js/client/http-agent.md, https://api.github.com/repos/ag-ui-protocol/ag-ui/git/trees/main?recursive=1, https://raw.githubusercontent.com/ag-ui-protocol/ag-ui/main/docs/spec/1.0/basic/transports/index.mdx

## claims
- [C1] B 被推翻：ACP v1 schema 定义 `authenticate` JSON-RPC 方法（AuthenticateRequest，x-side=agent，x-method="authenticate"） | src: https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/schema.json | quote: "Request parameters for the authenticate method.\n\nSpecifies which authentication method to use." | type: official
- [C2] ACP v1 `initialize` 响应含 `authMethods` 字段（数组，元素为 AuthMethod） | src: https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/schema.json | quote: "Authentication methods supported by the agent." | type: official
- [C3] `authenticate` 请求参数 `methodId` 必须来自 initialize 响应中宣告的方法 | src: https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/schema.json | quote: "The ID of the authentication method to use.\nMust be one of the methods advertised in the initialize response." | type: official
- [C4] ACP v1 AuthMethod 有 `agent`（默认）与 `terminal` 两种 type；terminal 由 client 交互式运行 agent 程序，不传给 authenticate | src: https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/schema.json | quote: "When no `type` is present, the method is treated as `agent`." 及 "The client MUST NOT pass this method to `authenticate`." | type: official
- [C5] ACP v1 还有 `logout` 方法，由 agentCapabilities.auth.logout 宣告 | src: https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/schema.json | quote: "Whether the agent supports the logout method.\n\nOptional. Omitted or `null` both mean the agent does not advertise support." | type: official
- [C6] client 侧有 clientCapabilities.auth.terminal 布尔能力位 | src: https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v1/schema.json | quote: "Whether the client supports `terminal` authentication methods." | type: official
- [C7] agentclientprotocol.com 有专页 /protocol/authentication；overview 消息流含 authenticate | src: https://agentclientprotocol.com/protocol/overview | quote: "Client → Agent: `authenticate` if required by the Agent" | type: official
- [C8] authentication 页确认 authMethods 在 initialize 响应中宣告；terminal 方法禁止传给 authenticate | src: https://agentclientprotocol.com/protocol/authentication | quote: "Agents advertise available authentication methods in `authMethods`." | type: official
- [C9] ACP v2 草案把方法名改为 `auth/login` 与 `auth/logout`（LoginAuthRequest/LogoutAuthRequest 等定义存在） | src: https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/schema/v2/schema.json | quote: "Supplying one or more valid methods means\nthe agent MUST support both `auth/login` and `auth/logout`." | type: official
- [C10] ACP 仓库含 auth 相关 RFD：docs/rfds/auth-methods.mdx、get-auth-state.mdx、logout-method.mdx | src: https://api.github.com/repos/agentclientprotocol/agent-client-protocol/git/trees/main?recursive=1 | quote: "docs/rfds/auth-methods.mdx" | type: official
- [C11] A 成立且被 spec 明文确认：transports 页声明 AG-UI 不定义凭据，鉴权属于 binding/应用层 | src: https://docs.ag-ui.com/spec/1.0/basic/transports/index.md | quote: "Authentication and authorization are properties of the binding and the application, not of the protocol: AG-UI defines no credential, and a binding carries whatever its channel uses (HTTP authentication, ambient process identity, or nothing)." | type: official
- [C12] AG-UI schema.json 无任何 auth 字段（grep 仅命中 "author"×3） | src: https://docs.ag-ui.com/spec/1.0/schema.json | quote: "（无 auth 字段；94KB schema 中仅 3 处 author）" | type: official
- [C13] 但 AG-UI JS SDK 的 HttpAgent 支持 headers 配置，文档示例即 Bearer token（SDK 层，非 spec 层） | src: https://docs.ag-ui.com/sdk/js/client/http-agent.md | quote: "headers?: Record<string, string> // Optional HTTP headers" 及示例 "Authorization: \"Bearer your-api-key\"" | type: official
- [C14] AG-UI HTTP+SSE transport 页承认 auth 失败是 HTTP 错误（但不定义机制） | src: https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse.md | quote: "malformed JSON, failed validation, refused auth — is an HTTP error status with no event stream" | type: official
- [C15] ACP transports 页：stdio 是唯一完整规范的传输，协议本身 transport-agnostic；该页不提 auth（auth 在 JSON-RPC 层） | src: https://agentclientprotocol.com/protocol/transports | quote: "The protocol is transport-agnostic" 及 "Agents and clients **SHOULD** support stdio whenever possible." | type: official

## conflicts
- 主张 B「Zed ACP 没有鉴权概念」被推翻：v1 schema 有 authenticate/logout 方法、authMethods 字段、AuthMethod(agent|terminal)、双侧 auth 能力位（C1–C8），v2 草案扩展为 auth/login+auth/logout（C9），仓库有三个 auth RFD（C10）。stdio 子进程模型不妨碍鉴权——terminal 类型正是让 client 交互式跑 agent 登录程序。
- 主张 A 未找到反例，且 spec 明文自我确认（C11）。但措辞须限于"spec 不定义"：SDK HttpAgent 可传 Authorization Bearer（C13），transports 页承认 binding 可携带 HTTP authentication（C11/C14）——若成稿写成"AG-UI 无法鉴权"则错误。

## gaps
- AG-UI 反例查找已覆盖：llms.txt 全站索引（无 security/auth/deployment 页）、schema.json 全文 grep、transports/index、http-sse、run-input、capabilities 页、仓库 docs/spec 目录树——均无 spec 级鉴权机制。未逐页 grep concepts/* 全部 14 个 mdx（已查 architecture），但 llms.txt 索引与 spec 自述（C11）使反例存在概率极低。
- ACP v1 文档页 URL 现为 /protocol/authentication（initialization 页内链写作 /protocol/v1/authentication#logging-out），v1/v2 路径前缀混用未逐一核对。
- zed-industries/agent-client-protocol 已 301 至 agentclientprotocol/agent-client-protocol，引文 URL 建议用新 org。

## leads
- ACP RFD get-auth-state.mdx（查询当前鉴权状态）与 streamable-http-websocket-transport.mdx（HTTP 传输草案）可能为成稿提供下一步细节。
- AG-UI「binding 携带 channel 的鉴权」意味着部署时可叠加任意 HTTP auth——成稿可借此精确表述。
- ACP terminal auth 用 args/env 字段注入登录参数，是好细节。
