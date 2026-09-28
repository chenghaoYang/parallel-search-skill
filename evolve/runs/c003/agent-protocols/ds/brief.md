# Brief: agent 时代的协议对照文档

- 读者：看到 MCP / A2A / ACP / AG-UI 一堆名词、分不清各自管什么的工程师。
- 目标：5 分钟建立 taxonomy（谁跟谁之间说话、归谁管、什么格式、什么版本），再按矩阵查细节。
- 范围内：MCP、A2A、IBM/ BeeAI ACP（Agent Communication Protocol）、Zed ACP（Agent Client Protocol）、AG-UI；大厂（OpenAI/Anthropic/Google/Microsoft）对它们的支持与自家变体；鉴权、版本、治理、怎么选；调研中出现的同 scope 相关协议（如 AGNTCY/ANP/A2UI/MCP-UI 等）按 leads 酌情纳入。
- 范围外：具体框架用法教程、非协议类工具（纯 SDK）、性能 benchmark。
- 用户点名疑点（成稿必须给结论）：
  1. ACP 有两个（IBM Agent Communication Protocol vs Zed Agent Client Protocol），是不是一回事？
  2. MCP 的 SSE 传输是否已废弃？
- 完成标准：矩阵核心格 ✅/∅，疑点有带引用的结论；≤ 9000 字符；截至 2026-09。
- 参数：rounds 3, workers 6, budget 9000, dir ./ds, 终稿同时写 ./report.md。
