# brief: agent 时代的「协议」 taxonomy

读者：听到 MCP/A2A/ACP/AG-UI 一堆名词但分不清谁管什么的工程师/技术决策者。
目标：5 分钟建立「每个协议管哪条边界」的认知，再按表查细节（传输、鉴权、版本、治理、厂商支持、怎么选）。

## 范围内
- 种子：MCP、A2A、ACP（两个同名：IBM/BeeAI Agent Communication Protocol vs Zed Agent Client Protocol）、AG-UI
- 大厂支持矩阵：OpenAI、Anthropic、Google、Microsoft 各自支持哪些、有无自家变体
- 横向问题：鉴权、版本状态、治理主体、选型建议
- 边缘实体（值不值得进网格由 scout/leads 决定）：AG-UI 家族旁的 MCP-UI/A2UI/OpenAI Apps SDK；支付协议 AP2/x402；Cisco AGNTCY、ANP、UCP 等

## 范围外
- 各协议的完整 API 教程、SDK 用法
- 非「agent 协议」的东西（REST/gRPC 本身）

## 用户点名疑点（成稿必须给结论）
1. 两个 ACP 是不是一回事？（预期：不是，一个是 agent↔agent、一个是 client↔agent editor）
2. MCP 的 SSE 传输是否已废弃？（预期：2025-03-26 起被 Streamable HTTP 取代，旧 SSE 为 backward-compat 保留；需一手确认）

## 完成标准
- taxonomy 用「协议跨越的边界」作主分类轴
- 对照矩阵覆盖：管什么边界 / 传输与payload / 鉴权 / 版本与状态 / 治理 / 大厂支持
- 预算 ≤ 9000 字符；每轮重写不追加
