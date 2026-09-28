# r2-google
question: Google 官方是否支持 MCP（Model Context Protocol）？在 Gemini API、Agent Development Kit (ADK)、Vertex AI 等产品线是否集成，官方原句和日期是什么？对 ACP（IBM 的 Agent Communication Protocol 或 Zed 的 Agent Client Protocol）的支持情况？对 AG-UI 的支持情况？Google 自己的 Agent Development Kit (ADK) 与 A2A/MCP 是什么关系——是否只是客户端实现，还是有自己的协议级扩展或专有变体？
checked: https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services, https://adk.dev/mcp/, https://developers.googleblog.com/en/datacommonsmcp/, https://developers.googleblog.com/delight-users-by-combining-adk-agents-with-fancy-frontends-using-ag-ui/, https://adk.dev/integrations/ag-ui/, https://adk.dev/a2a/a2a-extension/, https://adk.dev/tools-custom/mcp-tools/, https://zed.dev/blog/bring-your-own-agent-to-zed, https://www.theregister.com/2025/08/28/google_zed_acp/, https://geminicli.com/docs/cli/acp-mode/

## claims
- [C1] Google Cloud 宣布官方 MCP 支持服务于 2025 年 12 月 11 日，初期支持 Maps、BigQuery、Compute Engine、Kubernetes Engine | src: https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services | quote: "Date: December 11, 2025. Google announced official Model Context Protocol (MCP) support" | type: official
- [C2] Google Data Commons MCP Server 公开发布于 2025 年 9 月 24 日 | src: https://developers.googleblog.com/en/datacommonsmcp/ | quote: "announced on September 24, 2025" | type: official
- [C3] ADK 集成 MCP 支持，通过 McpToolset 类实现与 MCP 服务器的连接 | src: https://adk.dev/tools-custom/mcp-tools/ | quote: "The McpToolset class enables agents to connect to MCP servers" | type: official
- [C4] Gemini SDK 支持 MCP（Python 和 JavaScript），可连接本地和远程 MCP 服务器 | src: https://adk.dev/mcp/ | quote: "ADK leverages FastMCP, a Python framework handling protocol complexities" | type: official
- [C5] Google ADK 宣布 AG-UI 协议集成，发布日期为 2025 年 9 月 26 日 | src: https://developers.googleblog.com/delight-users-by-combining-adk-agents-with-fancy-frontends-using-ag-ui/ | quote: "SEPT. 26, 2025. combine Google's Agent Development Kit backend with AG-UI" | type: official
- [C6] ADK 通过 Python 中间件官方支持 AG-UI 协议 | src: https://adk.dev/integrations/ag-ui/ | quote: "AG-UI works across diverse technology stacks, with implementations for web, mobile, backend" | type: official
- [C7] Google ADK 支持 A2A 协议及 A2A Extension 以改进流式通信的可靠性 | src: https://adk.dev/a2a/a2a-extension/ | quote: "extension addresses critical limitations in legacy A2A-ADK implementations" | type: official
- [C8] Google 通过 Gemini CLI 参考实现支持 Zed 的 Agent Client Protocol (ACP)，基于 JSON-RPC 2.0 | src: https://zed.dev/blog/bring-your-own-agent-to-zed | quote: "Zed has introduced the Agent Client Protocol (ACP), with Google's Gemini CLI as reference implementation" | type: official
- [C9] Gemini CLI 在 ACP 模式下与客户端建立 stdio JSON-RPC 2.0 通信 | src: https://geminicli.com/docs/cli/acp-mode/ | quote: "communication happens over standard input/output (stdio) using JSON-RPC 2.0 protocol" | type: official
- [C10] Google 与 Zed 合作开发 ACP (Agent Client Protocol)，初期参考实现为 Gemini CLI，目标为跨编辑器通用 | src: https://www.theregister.com/2025/08/28/google_zed_acp/ | quote: "Google initiated the project through its Gemini CLI team, wanted deeper Zed integration" | type: official

## conflicts
- 无 ACP 命名冲突记录在 Google 官方文档。搜索中发现 IBM 有独立的 Agent Communication Protocol (ACP)，但 Google 官方文档未提及对 IBM ACP 的支持。

## gaps
- Google 官方是否正式支持 IBM 的 Agent Communication Protocol (ACP)：未找到官方确认
- Vertex AI 对 MCP 的集成详情：仅找到 Gemini Enterprise Agent Platform 支持 MCP，未找到其他 Vertex AI 服务的具体支持列表
- Gemini API (标准) 对 MCP 的原生支持范围：SDK 支持确认，但未找到 API 端点级别的公告日期

## leads
- A2A Extension 是 Google 专有的协议级扩展，声明机制为 HTTP header 或 gRPC metadata 中的 "X-A2A-Extensions" 或 "use_legacy=False"，表明 ADK 不止是客户端实现
- Zed ACP (Agent Client Protocol) 是编辑器-代理通信层，与 Google 的 A2A (Agent-to-Agent) 协议层次不同，Google 的支持限于参考实现 Gemini CLI
- AG-UI 列表中 ADK 被列为 2025 年 9 月 26 日的官方采用者，符合简报中的已知信息
