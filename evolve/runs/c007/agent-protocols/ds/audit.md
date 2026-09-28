# audit 判定汇总

## verify-mcp（7 项，全 confirmed）
V1 HTTP+SSE→StreamableHTTP 取代 ✓；V2 deprecated registry 行逐项吻合 ✓；V3 SEP-2596 Final 2026-05-18 ✓；V4 OAuth OPTIONAL+RFC9728+RFC8707 ✓；V5 Registry preview ✓；V6 MCP Apps unifies 句在 apps.mdx（非 README）+ 2026-01-26 Stable ✓；V7 2026-07-28 为 current、两标准绑定、request-scoped SSE ✓

## verify-a2a（8 项，全 confirmed）
V1 三绑定 ✓；V2 agent-card.json 路径+0.3 改名 ✓；V3 v1.0.0 2026-03-12/v1.0.1/移除 /v1 前缀（原文 "v1s" 复数）✓；V4 五种 securitySchemes+TLS MUST（原文 "headers or metadata"）✓；V5 TaskState 9 值 ✓；V6 Google 创建+捐 LF ✓；V7 IBM ACP 并入 A2A ✓；V8 A2A/MCP 互补原句 ✓

## verify-acp-agui（9 项，全 confirmed）
V1–V5 Zed ACP 全名/v1 稳定/stdio SHOULD/authenticate+authMethods+logout/40 agents 列表 ✓（repo 已 301→agentclientprotocol org，需换 URL）；V6 "AG-UI defines no credential" ✓；V7 EventType 31 ✓；V8 intro+MIT ✓；V9 AGNTCY ACP=Agent Connect Protocol, OpenAPI 3.1.1, v0.2.3, 2026-04-11 归档 ✓

## verify-vendors（10 项：8 confirmed / 1 wrong / 2 走样→已改）
V1 走样：Apps SDK 页已改称 Plugins，措辞改为「ChatGPT apps 用 MCP」；V5 走样：GA 页不含 MCP 半句，已删该半句并给 Copilot Studio MCP 页补 [41]；V6 wrong：官方页写 "MAF support varies by SDK"，已改为「支持随 SDK 而异」；V10 走样：摘录为改写概括，但目录存在、成稿表述（官方示例）成立，保留。V2 经 Wayback confirmed（直连 403）。

## 终审结论：32 判定项 → 29 confirmed / 1 wrong / 2 走样（均已改正）；未核完 0。
