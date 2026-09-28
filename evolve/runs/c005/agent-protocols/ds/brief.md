# Brief：agent 时代「协议」横向对照

## 任务
帮用户理清 MCP、A2A、ACP（两个同名）、AG-UI 分别管什么、有什么不同；大厂（OpenAI/Anthropic/Google/Microsoft）各自支持哪些、有无自家变体；以及鉴权、版本、治理、怎么选。

## 读者
知道 LLM agent 概念、被一堆缩写搞混的工程师。目标：5 分钟建立 taxonomy + 对照认知，能回答「我这个场景该用谁」。

## 范围内
- MCP（含传输、版本线、鉴权、registry、SSE 弃用疑点）
- A2A（Google/LF；与 IBM ACP 的合并关系）
- ACP ×2：IBM/BeeAI Agent Communication Protocol vs Zed Agent Client Protocol（必须给结论：是不是一回事）
- AG-UI（CopilotKit；UI↔agent 层）
- 大厂支持与变体（OpenAI Apps SDK、Microsoft 自家实现、Google 对 MCP 的支持等）
- 治理（LF Agentic AI Foundation 等）、鉴权、版本线、选型建议
- leads 里出现的范围内实体（AGNTCY、ANP、MCP UI/Apps、A2UI 等）→ R2 决定

## 范围外
- 单家 SDK 教程级细节；非 agent 协议（OAuth 本身只讲到协议怎么用它的程度）；模型 API（Responses/Chat Completions 只在「变体」语境出现）。

## 用户点名疑点（成稿必须给结论）
1. 两个 ACP 是不是一回事？（预期：不是，不同作者不同层；IBM 那个并入了 A2A——需核验）
2. MCP 的 SSE 传输是否已废弃？（预期：2025-03-26 spec 引入 Streamable HTTP 取代 HTTP+SSE，SSE 标 deprecated 但向后兼容——需核验版本与措辞）

## 完成标准
- 四个协议 + 两个 ACP 消歧 + 大厂矩阵 + 鉴权/版本/治理/选型
- ≤ 9000 字符；每个具体事实可追到笔记 [C#]；boundary 主张经反证或标范围
